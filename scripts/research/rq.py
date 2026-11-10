#!/usr/bin/env python3
"""rq: the research harness. Plain commands any agent in any tool can run; no model is called from here.

The protocol a parent agent follows is docs/research-protocol.md. In short:

  scripts/rq folder session                                           -> your session folder .tmp/session-<id>/
  scripts/rq issues                                                   -> the open rq:research issues, free or taken
  scripts/rq open expand domains-dns "free DNS hosting with an API"   -> run id, tracking issue (--issue N claims N)
  scripts/rq context domains-dns                                      -> what exists, worklists, sources
  scripts/rq plan RUN --file .tmp/RUN/plan.json                       -> units, leases, briefs
  scripts/rq briefs RUN                                               -> one line per lane: start them all at once
  (lanes work, each in its own folder .tmp/RUN/units/UID/, from the repository root)
  scripts/rq collect RUN                                              -> receipts and lint per unit
  scripts/rq integrate RUN                                            -> applied on branch rq/RUN in git objects
  scripts/rq plan RUN --conflicts ; lanes ; collect ; integrate       -> at most two reconcile rounds
  scripts/rq audit RUN ; lanes ; collect ; scripts/rq audit RUN --score
  scripts/rq abandon RUN UID --reason "..."                           -> a unit no lane can answer, given up
  scripts/rq land RUN --meets N,N                                     -> the pull request, in under a minute; CI gates it
  scripts/rq show RUN RID                                             -> a record as the run branch holds it

One working tree for every research agent (AGENTS.md section 2 rule 14): no worktree, no clone, no store or gate of a
run's own; every file under .tmp/<id>/. The merge session ends a merge pass with scripts/rq wipe and scripts/rq sync.

Exit codes: 0 done, 1 a defect or a refusal, 2 usage, 3 environment, 4 a tool refused (read again after retry_at).
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# before the first local import: bytecode goes to .tmp/rq/pycache, never beside the scripts, and no git process of
# this command or its children can rewrite the shared index (GIT_OPTIONAL_LOCKS)
os.environ["GIT_OPTIONAL_LOCKS"] = "0"
sys.pycache_prefix = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".tmp", "rq", "pycache")
os.environ["PYTHONPYCACHEPREFIX"] = sys.pycache_prefix
sys.path.insert(0, HERE)

import audit  # noqa: E402
import capture  # noqa: E402
import checks  # noqa: E402
import integrate  # noqa: E402
import land  # noqa: E402
import review  # noqa: E402
import state  # noqa: E402
import track  # noqa: E402
import units  # noqa: E402
from common import (BASE, REPO, RID_RE, SETTINGS, Fail, TreeView, commit_on, git, legacy_dirs, read_capture,  # noqa: E402
                    read_json, read_jsonl,
                    research_checkout, rev, run_dir, run_lock, run_or_ref_tree, stamp, tmp_rel, upstream, utc_now,
                    write_json)

LABEL_BASELINE = "rq:baseline"

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# words an issue body must not carry any more: the harness before the one-tree change, and a cap on the units of a
# plan (AGENTS.md section 2 rule 15: there is no lane limit)
STALE_WORDS = (".tmp/rq/wt", ".tmp/rq/runs", "--repo .tmp", "gatecmp", "max_captures",  # an old field, ignored
               "pull request of its own",
               # a run opens no schema pull request, and writes its ledger lines under history/ledger/<run>/
               "pull request that extends the schema", "is in `history/ledger.jsonl`", "meets the need")
STALE_RES = (re.compile(r"--max-units[ =]+[1-9]"), re.compile(r"\bat most \d+ lanes\b", re.I))


def stale_lines(body):
    return [ln.strip() for ln in (body or "").splitlines()
            if any(w in ln for w in STALE_WORDS) or any(x.search(ln) for x in STALE_RES)]


def cmd_open(a):
    if not research_checkout(REPO):
        print("warning: rq.researchCheckout is not set: this is not a prepared research checkout. A research session stops "
              "here and tells the operator; an own clone goes on (AGENTS.md section 0)", file=sys.stderr)
    if a.issue:
        st = track.issue_state(a.issue)
        for ln in stale_lines(st["body"] if st else "")[:3]:
            print("warning: issue #%d still carries a pre-one-tree instruction (%s); follow AGENTS.md rule 14 and tell "
                  "the operator" % (a.issue, ln[:140]), file=sys.stderr)
    r = units.open_run(a.kind, a.topic, a.details, no_issue=a.no_issue, research_issue=a.issue)
    print("run %s opened%s" % (r["run"], (", issue #%d" % r["issue"]) if r.get("issue") else ""))
    if r.get("claim"):
        print("claim: " + r["claim"])
    if r.get("head_behind"):
        print("note: the checkout's HEAD is %d commit(s) behind main; the run is based on main" % r["head_behind"])
    print("next: write the run id into your RESUME.md (.tmp/session-<id>/RESUME.md); scripts/rq context %s; write the plan "
          "at .tmp/%s/plan.json; scripts/rq plan %s --file .tmp/%s/plan.json" % (r["topic"], r["run"], r["run"], r["run"]))
    return 0


def cmd_issues(a):
    lines = track.list_issues(utc_now(), int(SETTINGS.get("claim_hours", 24)))
    if lines is None:
        raise Fail("rq issues needs gh (and no RQ_NO_GITHUB): it reads the open rq:research issues and their claims", 3)
    for ln in lines:
        print(ln)
    out = track.gh(["issue", "list", "--label", "rq:research", "--state", "open", "--limit", "200", "--json", "number,body"])
    for it in json.loads(out or "[]"):
        for ln in stale_lines(it.get("body"))[:1]:
            print("warning: issue #%d still carries a pre-one-tree instruction (%s); follow AGENTS.md rule 14 and tell "
                  "the operator" % (it["number"], ln[:140]))
    free = free_issues(lines)
    print("%d open rq:research issue(s), %d free. Take a free one at random, not the first (for a per-topic issue, a "
          "topic with no live claim): scripts/rq open KIND TOPIC \"DETAILS\" --issue N, with KIND and TOPIC the first "
          "two words of its request line; when open says the issue is taken, take another" % (len(lines), len(free)))
    if free:
        import random
        print("picked at random: #%d" % random.choice(free))
    return 0


def free_issues(lines):
    """The numbers of the issues rq issues lists as free, or as a per-topic issue with a free topic, that wait for no
    tool. Thirty sessions that each take the first free issue all claim the same one; a random pick spreads them (F-01)."""
    out = []
    for ln in lines:
        parts = ln.split("\t")
        v = parts[-1]
        if "waits for a tool" in v or not (v == "free" or v.startswith("per topic:")):
            continue
        out.append(int(parts[0].lstrip("#")))
    return out


def cmd_release(a):
    print(track.release(a.issue, a.run, a.reason, utc_now(), int(SETTINGS.get("claim_hours", 24))))
    return 0


def cmd_abandon(a):
    # under the run lock: a collect or an integrate of this run would save its own copy of unit.json over this one
    # (G4-02)
    with run_lock(a.run):
        return _abandon(a)


def _abandon(a):
    u = units.load_unit(a.run, a.uid)
    if u["status"] in ("integrated", "reverted", "superseded") or (u["status"] == "abandoned" and not u.get("commit")):
        raise Fail("unit %s is %s; only a unit that is not integrated can be abandoned" % (a.uid, u["status"]), 1)
    if u["kind"] == "audit":
        # the audit is the second key (step 8): giving one up would land the unit it audits unchecked (W2-01)
        raise Fail("unit %s is an audit unit, which is not abandoned. Score it as it is (scripts/rq collect %s, then "
                   "scripts/rq audit %s --score: an auditor that decided no claim is reported undecided), or, when it "
                   "was planned wrong, plan it afresh with scripts/rq audit %s --replan" % (a.uid, a.run, a.run, a.run), 1)
    if u.get("attempt"):
        # an integrate stopped on this unit: its commit may be on the run branch, and the next integrate decides (G4-01)
        raise Fail("unit %s has an integrate attempt that did not finish: its commit may be on rq/%s. Run scripts/rq "
                   "integrate %s first; it settles the unit, and then abandon what is left" % (a.uid, a.run, a.run), 1)
    if not (a.reason or "").strip():
        raise Fail("--reason is required: the report and the pull request list it", 2)
    was = u["status"]
    reason = " ".join(a.reason.split())
    if u.get("commit"):
        # a unit reopened with brief --fix: its first integration is on the run branch. Giving up the fix keeps that
        # commit, so the unit is integrated again, and its audit and the report count it (G4-01)
        u["status"] = "integrated"
        u["fix_abandoned"] = {"reason": reason, "at": stamp(), "was": was}
        u.pop("problems", None)
        u.pop("abandoned", None)
        # the commit is the one an auditor already took, if one did: its mark comes back
        u.update(u.pop("audit_before_fix", None) or {})
        units.save_unit(u)
        if was == "abandoned":
            # an abandon of an older harness released the lease: take back every key no other run holds
            state.add_keys(REPO, a.run, u["id"], state.lease_keys(u), u.get("fence"))
        track.comment(units.load_run(a.run), "unit %s: the fix is given up (was %s), and its first integration (%s) "
                      "stays: %s" % (a.uid, was, u["commit"][:12], reason))
        print("unit %s keeps its first integration (%s): the fix is given up, and the unit is integrated again, so its "
              "audit and the report count what that commit wrote. Its lease holds until the merge. %s"
              % (a.uid, u["commit"][:12], next_after_integrate(a.run)))
        return 0
    u["status"] = "abandoned"
    u["abandoned"] = {"reason": reason, "at": stamp(), "was": was}
    units.save_unit(u)
    state.release_unit(REPO, a.run, u["id"])
    track.comment(units.load_run(a.run), "unit %s abandoned (was %s): %s" % (a.uid, was, u["abandoned"]["reason"]))
    print("unit %s abandoned (was %s); its lease is released, and the run report and the pull request list it with the "
          "reason. A question that still needs an answer goes in an open_question of another unit, or a new issue."
          % (a.uid, was))
    return 0


def cmd_context(a):
    t = a.what
    if t not in units.topics():
        t = units.load_run(t)["topic"]
    print(units.context(t))
    return 0


def cmd_plan(a):
    # one writer: plan moves the run branch (bring_main) and rewrites conflicts.jsonl (G-10)
    with run_lock(a.run):
        r = units.load_run(a.run)
        if r.get("phase") == "in-review":
            # new units after a send-back: take what the merge session pushed to origin/rq/<run> (a resolve, a fix)
            # before main is merged in and the lanes read records, as integrate, audit and put do (G7-05)
            note = land.update_branch(r, REPO, "plan")
            if note:
                print(note)
        return _plan(a)


def _plan(a):
    specs = []
    if a.file:
        if not os.path.isfile(a.file):
            raise Fail("no plan file %s (a relative path is read from the current folder)" % a.file, 2)
        data = read_json(a.file)
        specs = data.get("units") if isinstance(data, dict) else data
        if not isinstance(specs, list) or not specs:
            raise Fail("plan file %s holds no unit: write a JSON list of unit specs, or {\"units\": [...]}" % a.file, 2)
    if a.conflicts:
        # the conflicts are marked handled below, after units.plan made their reconcile units (G3-02)
        specs += integrate.reconcile_specs(a.run)
    qspecs, gone, refused_q = [], [], []
    tree = units.run_tree(a.run) if a.queue else None
    for qid in a.queue or []:
        if not units.QUEUE_ID_RE.match(qid or "") or ".." in qid:
            raise Fail("a queue id is the name of a file in queue/ without .json, not %r" % qid, 2)
        b = tree.read("queue/%s.json" % qid)
        q = json.loads(b.decode("utf-8")) if b else None
        if not q:
            # a queue file that another run answered has left the queue: nothing is left to plan for it, so the other
            # ids are planned. An id that was never queued plans nothing, as before: a typo is not skipped
            if git(REPO, "log", "-1", "--format=%h", units.ref_of(a.run), "--", "queue/%s.json" % qid, check=False):
                gone.append(qid)
                continue
            raise Fail("no queued unit %s" % qid, 2)
        # an item that names a record with no file is refused alone; units.plan would refuse the whole call
        missing = [x for x in (q.get("scope") or {}).get("rids") or [] if not tree.read("dossier/%s.json" % x)]
        if missing:
            refused_q.append("queue item %s not planned: it names %s, which has no record on the run branch. Plan it from a "
                             "plan file with the record its question means (scripts/fr search NAME), or as a discover unit, "
                             "and \"queue_files\": [\"queue/%s.json\"]" % (qid, ", ".join(missing), qid))
            continue
        # keep the item's own origin (an intake item's is the public issue URL) and name the queue file beside it
        q = dict(q, origin=q.get("origin") or "queue:" + qid, queue_id=qid, queue_file="queue/%s.json" % qid)
        qspecs.append(q)
    specs += merge_queue(qspecs)
    made, problems = units.plan(a.run, specs) if specs else ([], [])
    problems = ["queue item %s has left the queue: another run answered it, so nothing is planned for it" % qid
                for qid in gone] + refused_q + problems
    if a.conflicts:
        # a conflict is handled only when a reconcile unit for its record exists: a plan that stopped (main conflicts
        # with the run, a refused unit, a held lease) leaves it open for the next plan --conflicts (G3-02)
        rids = {rid for u in made if u.get("origin") == "conflict" for rid in (u.get("scope") or {}).get("rids") or []}
        integrate.mark_handled(a.run, rids)  # with no rid it closes only the torn lines (G7-08)
        if rids:
            r = units.load_run(a.run)
            r["rounds"] = r.get("rounds", 0) + 1
            units.save_run(r)
    if a.from_worklist:
        m2, p2 = units.from_worklist(a.run, a.from_worklist, a.topic or units.load_run(a.run)["topic"], a.batch)
        made += m2
        problems += p2
    for u in made:
        print("%s %-9s %s" % (u["id"], u["kind"], u["question"][:100].replace("\n", " ")))
    for p in problems:
        print("note: " + p)
    print("%d unit(s) planned; scripts/rq briefs %s prints the lane instructions: start every lane at once" % (len(made), a.run))
    refused = [p for p in problems if " not planned: " in p]
    if refused:
        # a refused unit is lost unless the parent reads the note, so the exit says so too (R3-B-07)
        print("%d unit(s) refused; fix them and run plan again with only those units" % len(refused))
        return 1
    return 0 if made or not specs else 1


def merge_queue(qspecs):
    """Queue items of one plan call that share a record become one unit: their questions are joined and every queue
    file leaves the queue with that unit. Without this, the second item on a record is refused (the first holds its
    lease) and stays queued for ever."""
    groups = []
    for q in qspecs:
        rids = set((q.get("scope") or {}).get("rids") or [])
        # verify and reconcile items both lease records, so either kind joins the other on a shared record
        hit = [g for g in groups if rids and rids & g["rids"]]
        g = {"kind": q.get("kind"), "rids": set(rids), "items": [q]}
        for h in hit:
            g["rids"] |= h["rids"]
            g["items"] = h["items"] + g["items"]
            groups.remove(h)
        groups.append(g)
    out = []
    for g in groups:
        first = dict(g["items"][0])
        first.pop("max_captures", None)  # an old queue field, ignored: there is no page budget
        if len(g["items"]) > 1:
            first["scope"] = dict(first.get("scope") or {}, rids=sorted(g["rids"]))
            first["question"] = "\n\n".join("Queue item %s: %s" % (q["queue_id"], q["question"].strip()) for q in g["items"])
            # every item's own file, and the files an item already names (a re-run of a unit that answered some)
            first["queue_files"] = list(dict.fromkeys(f for q in g["items"]
                                                      for f in [q["queue_file"]] + list(q.get("queue_files") or [])))
            first.pop("queue_file", None)
        out.append(first)
    return out


def cmd_briefs(a):
    for u in units.units_of(a.run):
        if u["status"] in ("planned", "running", "invalid") and (not a.kind or u["kind"] == a.kind):
            print("%s\t%s" % (u["id"], units.lane_instruction(u)))
    return 0


def cmd_brief(a):
    if a.fix:
        # under the run lock: the reopen writes unit.json, which a collect or an integrate also writes (G4-02)
        with run_lock(a.run):
            return _brief(a)
    return _brief(a)


def _brief(a):
    u = units.load_unit(a.run, a.uid)
    if a.fix and u["status"] == "integrated" and u.get("rejects") and u["kind"] != "audit":
        # reopen: the integrator rejected some operations; the same lane fixes its changes.jsonl and the unit is
        # integrated again (applied operations are idempotent: a value already written becomes corroboration)
        whys = sorted({x["why"] for x in u["rejects"]})
        u["problems"] = ["rejected at integration (%d operation(s)): %s" % (sum(1 for x in u["rejects"] if x["why"] == w), w)
                         for w in whys]
        done = {x["id"] for x in units.units_of(a.run) if x["status"] in units.UNIT_DONE}
        u["fence"] = state.acquire(REPO, a.run, u, done)
        u["status"] = "invalid"
        # the next integration writes new values: it is audited again, so an earlier auditor's mark goes; it is kept
        # aside, and an abandon of the fix puts it back (G4-01)
        before = {k: u.pop(k) for k in ("audited_by", "audit_none") if k in u}
        if before:
            u["audit_before_fix"] = before
        units.save_unit(u)
        lint_now, _, _ = units.lint_unit(u)
        u["problems"] += lint_now
        units.save_unit(u)
    if u["kind"] != "audit":
        units.write_brief(u, fix=u.get("problems") if a.fix else None)
    elif a.fix and u["status"] == "invalid" and u.get("problems"):
        # an auditor's file that collect or the score refused (a file that is not UTF-8): the same auditor writes it again
        claims = read_json(os.path.join(units.unit_dir(a.run, a.uid), "claims.json"), [])
        audit.write_audit_brief(u, len(claims), fix=u["problems"])
    print(units.lane_instruction(u))
    return 0


def cmd_lint(a):
    u = units.load_unit(a.run, a.uid)
    probs, ops, rec = units.lint_unit(u)
    for p in probs:
        print("problem: " + p)
    print("%d operation(s), %d problem(s)%s" % (len(ops), len(probs), "" if rec else "; receipt.json not written yet"))
    return 1 if probs else 0


def cmd_collect(a):
    # under the run lock: a collect during an integrate would save a stale unit.json over the integrated one (G-10)
    with run_lock(a.run):
        rows, ready = units.collect(a.run)
    for row in rows:
        print("%s %-10s %-16s %s" % row)
    bad = [u for u in units.units_of(a.run) if u["status"] == "invalid"]
    for u in bad:
        for p in u.get("problems", [])[:6]:
            print("  %s: %s" % (u["id"], p))
    if bad:
        print("re-run invalid units with: scripts/rq brief %s UID --fix (the brief then lists the problems)" % a.run)
    track.comment(units.load_run(a.run), "collected: %d ready of %d" % (ready, len(rows)))
    us = units.units_of(a.run)
    aud_ready = [u["id"] for u in us if u["kind"] == "audit" and u["status"] == "ready" and not u.get("scored")]
    other_ready = [u["id"] for u in us if u["kind"] != "audit" and u["status"] == "ready"]
    if other_ready:
        print("next: scripts/rq integrate %s%s" % (a.run, (", then scripts/rq audit %s --score (audit units %s are ready)"
                                                           % (a.run, ", ".join(aud_ready))) if aud_ready else ""))
    elif aud_ready:
        print("next: scripts/rq audit %s --score (audit units %s are ready; integrate does not take audit units)"
              % (a.run, ", ".join(aud_ready)))
    else:
        print("next: wait for the lanes' receipts, then scripts/rq collect %s again" % a.run)
    return 0


def cmd_integrate(a):
    rep, conf = integrate.integrate(a.run, only=a.units.split(",") if a.units else None)
    for uid, st, tally, nrej in rep:
        print("%s %-11s %s%s" % (uid, st, ", ".join("%s %d" % kv for kv in sorted(tally.items())), (" (%d rejected)" % nrej) if nrej else ""))
    open_c = [c for c in conf if not c.get("handled")]
    r = units.load_run(a.run)
    print("conflicts open: %d%s" % (len(open_c), ("; plan reconcile units with scripts/rq plan %s --conflicts" % a.run)
                                    if open_c and r.get("rounds", 0) < 2 else ""))
    track.comment(r, "integrated:\n" + "\n".join("- %s %s %s" % (u, s, json.dumps(t)) for u, s, t, _ in rep) +
                  "\nopen conflicts: %d" % len(open_c))
    with run_lock(a.run):
        pushed = land.push_branch(r, again="integrate", soft=True)
    if pushed:
        print(pushed + (", so the integrated work survives the loss of this checkout"
                        if pushed.startswith("pushed ") else ""))
    if open_c and r.get("rounds", 0) < 2:
        print("next: scripts/rq plan %s --conflicts, start those lanes, collect and integrate" % a.run)
    else:
        print(next_after_integrate(a.run))
    return 0


def next_after_integrate(run):
    """The audit (step 8) comes before land: the hint names land only when every integrated unit has a scored audit
    or left no claim to audit (W2-01)."""
    ready = [u["id"] for u in units.units_of(run) if u["kind"] != "audit" and u["status"] == "ready"]
    if ready:
        # a unit that integrate left ready (a ref lock, or another writer moved the ref) is taken by the next call
        return "next: scripts/rq integrate %s again (units %s are still ready)" % (run, ", ".join(ready))
    waiting = [u["id"] for u in units.units_of(run) if u["kind"] != "audit" and u["status"] in ("planned", "running")]
    if waiting:
        # integrate takes only a collected unit: a lane's files are read and linted by collect, and a run whose lanes
        # are still planned would otherwise print land as its next step and look finished
        return ("next: scripts/rq collect %s (units %s are not collected yet: collect reads and lints the lane's "
                "files, and integrate takes only a collected unit)" % (run, ", ".join(waiting)))
    lost = [u["id"] for u in units.units_of(run) if u["status"] == "lease-lost"]
    if lost:
        # another run holds a key of their scope: integrate lets the lease again once that run merges or closes
        return ("next: units %s are lease-lost (a key of their scope has another holder, which integrate named): "
                "scripts/rq integrate %s again when the holder lets go, or scripts/rq abandon %s UID --reason \"...\"; "
                "the audit of the integrated units can go on meanwhile" % (", ".join(lost), run, run))
    unaudited, unscored = units.audit_todo(run)
    if unaudited:
        return ("next: scripts/rq audit %s (plans the auditors of %s; the run lands after their scores, step 8)"
                % (run, ", ".join(u["id"] for u in unaudited)))
    if unscored:
        return ("next: start the audit lanes (scripts/rq briefs %s --kind audit), then scripts/rq collect %s and "
                "scripts/rq audit %s --score (unscored: %s)" % (run, run, run, ", ".join(u["id"] for u in unscored)))
    return "next: " + before_land(run)


def before_land(run):
    """The prune of the run's baseline, then land: every land runs the prune first, which changes nothing when the run
    fixed no field that had a baseline row, so a forgotten prune never leaves a row a run made obsolete (LW7-05)."""
    return "scripts/rq check --prune --run %s (it changes nothing when no baseline row is fixed), then %s" % (
        run, land_cmd(run))


def land_cmd(run):
    """The land command of a run: --meets N,N (N the number of a Done-when line) only for a run that claimed an
    rq:research issue, and the lines an earlier land kept when it named them (W5-09)."""
    try:
        r = units.load_run(run)
    except Fail:
        r = {}
    if r.get("meets"):
        return "scripts/rq land %s --meets %s" % (run, ",".join(map(str, r["meets"])))
    return "scripts/rq land %s%s" % (run, " --meets N,N" if r.get("research_issue") else "")


def cmd_audit(a):
    if a.score:
        rows, uns = audit.score(a.run)
        for row in rows:
            print("unit %s audited by %s: supported %d, unsupported %d, cannot tell %d, unverifiable %d, upper95 %.3f -> %s" % row)
        for u in units.units_of(a.run):
            if u["kind"] == "audit" and u["status"] == "invalid" and not u.get("scored"):
                print("audit unit %s not scored: %s; send it back with scripts/rq brief %s %s --fix"
                      % (u["id"], "; ".join(u.get("problems") or ["invalid"]), a.run, u["id"]))
        if uns:
            claims_n = sum(1 for c in uns if not c.get("skipped"))
            print("%d unsupported claim(s)%s: those of kept units are conflicts now (scripts/rq plan %s --conflicts); "
                  "those of undone units go with the queued re-run" % (
                      claims_n, "" if claims_n == len(uns) else " and %d value(s) an undo had to leave" % (len(uns) - claims_n),
                      a.run))
        # the rows of this score, and the rows an older score saved as scored and then crashed before it wrote
        for c in uns:
            write_json(os.path.join(run_dir(a.run), "unsupported", audit.unsupported_name(c)), c)
        for c in audit.missing_unsupported(a.run):
            write_json(os.path.join(run_dir(a.run), "unsupported", audit.unsupported_name(c)), c)
            print("wrote the missing unsupported/%s" % audit.unsupported_name(c))
        with run_lock(a.run):
            pushed = land.push_branch(units.load_run(a.run), again="audit --score", soft=True)
        if pushed:
            print(pushed)
        unaudited, unscored = units.audit_todo(a.run)
        # only a kept unit's unsupported claim is a conflict; a reverted unit's go with its queued re-run (W4-04)
        kept = {row[1] for row in rows if row[7] != "REVERTED"}
        open_c = [c for c in read_jsonl(os.path.join(run_dir(a.run), "conflicts.jsonl")) if not c.get("handled")]
        if any(c.get("audit") in kept for c in uns) and open_c:
            print("next: scripts/rq plan %s --conflicts (unsupported claims of kept units), start those lanes, collect "
                  "and integrate, then audit the new units" % a.run)
        elif unaudited or unscored:
            print(next_after_integrate(a.run))
        else:
            print("next: " + before_land(a.run))
        return 0
    # under the run lock: a plan running at the same time numbers its units from the same count (G4-02)
    with run_lock(a.run):
        made = audit.plan_audit(a.run, 0 if a.census else a.per_unit, replan=a.replan, census=a.census)
    for u in made:
        print("%s audits %s" % (u["id"], u["audits"]))
    _, unscored = units.audit_todo(a.run)
    if unscored:
        print("%d audit unit(s) planned, %d not scored (%s). Hand them out with scripts/rq briefs %s --kind audit, all at "
              "once (prefer a different model or tool than the lanes used); when their receipts are in: scripts/rq collect "
              "%s, then scripts/rq audit %s --score" % (len(made), len(unscored), ", ".join(u["id"] for u in unscored),
                                                         a.run, a.run, a.run))
    else:
        print("0 audit units: no integrated unit left a claim to audit. next: " + land_cmd(a.run))
    return 0


def prune_on_run(a):
    """`check --prune --run RUN`: the baseline of the run branch, pruned of the rows its own records no longer break.
    Everything is read from the run branch and written onto it under the run lock, so the commit the rows came from is
    the commit they are written on (compare-and-set, design 2.1), and an integrate cannot change a record between the
    check and the write. Never the checkout's records or baseline: the research checkout lags origin/main between merge
    passes, and its rows written onto a run would remove a row main added or bring back one main pruned (G6-01).
    Only the records the run changed are checked (its net change against main, as land reads it): a row of a record the
    run did not touch cannot stop breaking on the run, so thirty runs that land together check their own records, not
    every record thirty times (F-04). Every error row of the baseline is per record (C04, which pairs two records, is a
    warning and has no row)."""
    if a.repo:
        raise Fail("check --prune --run reads the run branch rq/%s; --repo names another tree" % a.run, 2)
    if a.rev and a.rev.replace("refs/heads/", "", 1) not in ("rq/" + a.run, a.run):
        raise Fail("check --prune --run %s reads rq/%s itself; --rev %s names another commit" % (a.run, a.run, a.rev), 2)
    with run_lock(a.run):
        v = units.run_tree(a.run)
        rids = run_rids(v)
        viol = []
        for rid in sorted(rids):
            b = v.read("dossier/%s.json" % rid)
            if b is not None:
                viol += checks.record_violations(dict(json.loads(b.decode("utf-8")), _rid=rid), REPO,
                                                 narrative=not a.no_narrative, view=v)
        base = checks.baseline_of(v, REPO)
        now = {(r, k) for r, k, _ in viol}
        keep = [(r, k) for r, ks in base.items() for k in ks if k.split("|", 1)[0] not in rids or (r, k) in now]
        n0 = sum(len(x) for x in base.values())
        text, _ = checks.baseline_text([(r, k, "") for r, k in keep])
        # rows can only go: every kept row was in the run branch's own baseline
        new = commit_on(REPO, units.ref_of(a.run), v.commit, {"scripts/research/baseline.tsv": text.encode("utf-8")},
                        "rq %s: prune the baseline (%d -> %d)" % (a.run, n0, len(keep)), view=v)
    print("baseline pruned on rq/%s: %d -> %d%s (the %d record(s) the run changed were checked)"
          % (a.run, n0, len(keep), "" if new != v.commit else " (no change)", len(rids)))
    return 0


def run_rids(view):
    """The records a run changed: its net change against main (land.touched, `git diff up...tip`). -> set of rids."""
    _, paths = land.touched(REPO, upstream(REPO), view.commit)
    return {p[len("dossier/"):-len(".json")] for p in paths
            if p.startswith("dossier/") and p.count("/") == 2 and p.endswith(".json") and not p.endswith(".generated.json")}


def cmd_check(a):
    if a.prune and a.run:
        return prune_on_run(a)
    if a.run:
        raise Fail("--run goes with --prune: scripts/rq check --prune --run RUN", 2)
    view = None
    if a.rev:
        name = a.rev
        if not rev(REPO, name) and rev(REPO, "refs/heads/rq/" + name.replace("rq/", "", 1)):
            name = "refs/heads/rq/" + name.replace("rq/", "", 1)
        view = TreeView(REPO, name)
        root = REPO
    else:
        root = os.path.abspath(a.repo or REPO)
        if not os.path.isdir(os.path.join(root, "dossier")):
            print("SKIP no dossier/ under %s" % root)
            return 0
    if (a.write_baseline or a.prune) and research_checkout(REPO) and not a.repo:
        raise Fail("the research checkout changes the baseline only through a run: scripts/rq check --prune --run RUN "
                   "writes the pruned baseline of rq/RUN onto the run branch (AGENTS.md section 2 rule 14)", 2)
    recs, viol = checks.run_all(root, narrative=not a.no_narrative, view=view)
    if a.write_baseline:
        n = checks.write_baseline(viol, root)
        print("baseline written: %d error violation(s)" % n)
        return 0
    if a.prune:
        base = checks.baseline_of(view, root)
        now = {(r, k) for r, k, _ in viol}
        keep = [(r, k) for r, ks in base.items() for k in ks if (r, k) in now]
        n0 = sum(len(v) for v in base.values())
        checks.write_baseline([(r, k, "") for r, k in keep], root)
        print("baseline pruned: %d -> %d" % (n0, len(keep)))
        return 0
    new = checks.new_errors(viol, root, view)
    if a.gate:
        if new:
            print("FAIL %d new error violation(s): %s" % (len(new), "; ".join("%s %s" % (r, k) for r, k, _ in new[:4])))
            return 1
        c = sum(1 for r, k, _ in viol if checks.severity(r, k) == "warn")
        print("PASS no new error violation over %d records; %d warning(s), baseline holds" % (len(recs), c))
        return 0
    for ln in checks.summary(viol, root, view):
        print(ln)
    if a.rule:
        for r, k, d in viol:
            if r == a.rule:
                print("  %s %s" % (k, d))
    for r, k, d in new[:20]:
        print("NEW %s %s %s" % (r, k, d))
    return 1 if new else 0


def cmd_policy(a):
    recs, viol = checks.run_all(REPO, narrative=False)
    by = {}
    for r, k, d in viol:
        if r in checks.POLICY:
            by.setdefault(r, {}).setdefault(k.split("/")[0], []).append((k, d))
    for rule, topics in sorted(by.items()):
        _, name, desc = checks.RULES[rule]
        total = sum(len(v) for v in topics.values())
        title = "rq policy %s %s" % (rule, name)
        counts = "\n".join("| `%s` | %d |" % (t, len(v)) for t, v in sorted(topics.items(), key=lambda x: -len(x[1])))
        examples = "\n".join("- `%s` %s" % (k, d) for t in sorted(topics) for k, d in topics[t][:2])
        body = ("%s: %d record(s) today.\n\nThe rule is a warning until a methodology unit decides, per topic, whether it binds, "
                "and then amends `docs/conventions/README.md` or the records. Close this issue with that decision.\n\n"
                "| topic | records |\n|---|---|\n%s\n\nExamples:\n\n%s\n\nList them all: `scripts/rq check --rule %s`."
                % (desc, total, counts, examples, rule))
        n = track.open_labelled(title, body, "rq:policy")
        print("%s %d record(s) in %d topic(s) -> issue %s" % (rule, total, len(topics), n))
    return 0


def cmd_import_bundle(a):
    import import_bundle
    run, lines = import_bundle.import_bundle(a.file, REPO)
    print("\n".join(lines))
    return 0


def cmd_gatecmp(a):
    if research_checkout(REPO):
        raise Fail("the gate comparison runs in CI (this repository's Actions, scripts/rq ci RUN), or in an own "
                   "clone, never in the research checkout (AGENTS.md section 2 rule 14)", 2)
    head = os.path.abspath(a.head or REPO)
    green, new_fail, lines, bsha = land.gatecmp(head, a.base or upstream(REPO))
    print("\n".join(lines))
    print("GREEN against %s" % bsha[:10] if green else "RED: newly failing %s" % ", ".join(c["check"] for c in new_fail))
    return 0 if green else 1


def cmd_baseline_diff(a):
    """Fail when the pull request adds rows to scripts/research/baseline.tsv and does not carry the label that the
    merge session applies after it reviewed them. rq merge and rq ci --wait make the same check in-process (ci.light)."""
    added = land.baseline_added(a.base, a.head)
    labels = set(json.loads(a.labels or "[]") or [])
    if not added:
        print("PASS the baseline gains no row")
        return 0
    print("the baseline gains %d row(s) against %s:" % (len(added), a.base))
    for row in added[:40]:
        print("  + " + row)
    if LABEL_BASELINE in labels:
        print("PASS the pull request carries %s: a merge session reviewed these rows" % LABEL_BASELINE)
        return 0
    print("FAIL a new baseline row hides a violation. Fix the records, or, when a rule was added or widened, a merge "
          "session reviews the rows and applies the label %s" % LABEL_BASELINE)
    return 1


def cmd_land(a):
    meets = [int(x) for x in (a.meets or "").split(",") if x.strip().isdigit()]
    for ln in land.land(a.run, meets=meets):
        print(ln)
    return 0


def cmd_merge(a):
    for ln in land.merge(a.run, wait_ci=not a.no_ci, pr=a.pr):
        print(ln)
    return 0


def cmd_ci(a):
    """The remote CI (ci.py) of a run's pushed head, or with --pr N of any pull request's head, against the main it
    holds: its state, and a run when there is none. With --wait, the checks rq merge makes: the light ones here, then
    the wait for the remote run. A pull request that is not a run must hold main first (merge main into its branch), as
    rq merge does for a run in git objects."""
    import ci
    if not ci.remote():
        raise Fail("settings.json names no ci_repo and ci_workflow: no remote CI is configured for this clone", 2)
    if bool(a.run) == bool(a.pr):
        raise Fail("name a run, or a pull request with --pr N", 2)
    specs = ["+refs/heads/%s:%s" % (land.BASE, land.UPSTREAM_REF)]
    if a.run:
        specs.append(land.run_refspec(a.run))
    else:
        specs.append("+refs/pull/%s/head:refs/remotes/%s/pr/%s" % (a.pr, land.REMOTE, a.pr))
    land.fetch(REPO, specs)
    if a.run:
        head = rev(REPO, "refs/remotes/%s/rq/%s" % (land.REMOTE, a.run)) or rev(REPO, land.ref_of(a.run))
        if not head:
            raise Fail("branch rq/%s is neither in this clone nor on %s" % (a.run, land.REMOTE), 1)
        pr = branch = "rq/%s" % a.run
    else:
        meta = json.loads(track.gh(["pr", "view", str(a.pr), "--json", "headRefOid,headRefName"], REPO) or "{}")
        head = (meta.get("headRefOid") or "").strip()
        branch = (meta.get("headRefName") or "").strip()
        if not head or not branch:
            raise Fail("gh could not read the head of pull request %s" % a.pr, 1)
        pr = str(a.pr)
    up = rev(REPO, upstream(REPO))
    if a.pr and not land.is_ancestor(REPO, up, head):
        raise Fail("the head %s does not hold %s %s: merge main into the branch first, so the gate compares only this "
                   "change (rq merge does that for a run in git objects)" % (head, land.UPSTREAM, up[:10]), 1)
    # a run's head that main has passed since its land is compared with the main it holds; rq merge merges the newer
    # main in before it waits
    base = (land.git(REPO, "merge-base", up, head) or up).strip()
    print("head %s, base %s" % (head, base))
    if a.wait:
        for ln in ci.light(pr, base, head, REPO):
            print(ln)
        got = ci.wait(head, base, branch, REPO)
        print("remote CI green on %s: %s" % (head, got.get("url")))
        return 0
    if not ci.find(head, REPO):
        ci.ensure(head, base, branch, REPO)
    print(ci.describe(head, REPO))
    return 0


def cmd_review(a):
    for ln in review.review(a.run, a.sample, pr=a.pr):
        print(ln)
    return 0


def cmd_cleanup(a):
    # this checkout's run folder, or the manifest on the run branch or on main: cleanup works in any clone
    r = land.run_view(a.run)["run"]
    st = land.pr_state(r)
    if st not in ("MERGED", "CLOSED") and not (r.get("phase") == "landed-empty"):
        raise Fail("the pull request of %s is %s; cleanup runs only after the merge or the close" % (a.run, st or "missing"), 1)
    # a pull request closed without a merge gives its issue back; after a merge, rq merge has judged the issue already
    for ln in land.cleanup(r, release="the pull request was closed without a merge" if st == "CLOSED" else None):
        if ln:
            print(ln)
    print("released what this checkout holds of %s: its leases, and its local ref when origin holds the tip. The run "
          "folder stays until the merge session's scripts/rq wipe. Another checkout releases its leases on its next "
          "plan, status or wipe." % a.run)
    return 0


def cmd_close(a):
    for ln in land.close(a.run, a.reason):
        if ln:
            print(ln)
    return 0


def cmd_show(a):
    """A record, a file or a capture as a commit holds it, read from git objects; nothing is written but --out."""
    out = sys.stdout.buffer
    if a.capture:
        # the run branch of this clone, else origin/rq/RUN (a merge session's own clone), else any commit (W-03)
        v, run = run_or_ref_tree(REPO, a.ref)
        text = read_capture(a.capture, REPO, None, v)
        if text is None and run:
            import glob
            for lane in sorted(glob.glob(os.path.join(REPO, ".tmp", run, "units", "*"))):
                text = read_capture(a.capture, REPO, lane, v)
                if text is not None:
                    break
        if text is None:
            raise Fail("no capture %s on %s, in its unit folders, or in sources/" % (a.capture, a.ref), 1)
        data = text.encode("utf-8")
    else:
        if not a.path:
            raise Fail("show needs RUN RID, REF PATH, or RUN --capture SHA", 2)
        v, _ = run_or_ref_tree(REPO, a.ref)
        path_read = None
        path = a.path.strip("/")
        if RID_RE.match(path) and not path.startswith(("dossier/", "queue/", "history/", "sources/", "registry/", "scripts/", "docs/")):
            path = "dossier/%s.json" % path
        if v.isdir(path) or path == "":
            data = ("\n".join(n + ("/" if d else "") for n, d in v.ls(path)) + "\n").encode("utf-8")
        else:
            data = v.read(path)
            if data is None:
                raise Fail("no %s in %s" % (path, a.ref), 1)
            path_read = path
    if a.out:
        rel = tmp_rel(a.out, REPO)
        if research_checkout(REPO) and (not rel or "/" not in rel):
            # the same path names the file in the tree and the copy: a slip of one argument would change a tracked file
            # of the checkout that every research agent shares (LIO3-01)
            raise Fail("--out writes only under .tmp/<id>/ in the research checkout, for example .tmp/RUN/tools/FILE or "
                       ".tmp/session-<id>/FILE, not %s (AGENTS.md section 2 rule 14)" % a.out, 2)
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "wb") as f:
            f.write(data)
        if path_read:
            # what was read, for rq put's compare-and-set on the content: a put of this file refuses when the path
            # changed on the run branch since this read (G7-01)
            e = v.entry(path_read)
            write_json(a.out + ".base", {"ref": a.ref, "commit": v.commit, "path": path_read,
                                         "blob": e[1] if e else None, "at": stamp()})
        print("wrote %d bytes to %s%s" % (len(data), a.out, " (and what it read to %s.base, for rq put)" % a.out
                                          if path_read else ""))
        return 0
    out.write(data)
    out.flush()
    return 0


def cmd_put(a):
    for ln in land.put(a.run, a.path, a.file, a.reason):
        print(ln)
    return 0


def cmd_resolve(a):
    for ln in land.resolve(a.run, a.path, delete=a.delete):
        print(ln)
    return 0


def cmd_folder(a):
    if a.kind == "review":
        if not a.run:
            raise Fail("folder review needs the run id", 2)
        fid = "review-" + a.run
        state.register_folder(REPO, fid, "review", drain=False)
        os.makedirs(os.path.join(REPO, ".tmp", fid, "captures"), exist_ok=True)
        print(".tmp/%s/" % fid)
        return 0
    for ln in units.folder_session(REPO, end=a.end, take=a.take, listing=a.list):
        print(ln)
    return 0


def cmd_wipe(a):
    import wipe
    lines = wipe.wipe(REPO, dry_run=a.dry_run, drain=a.drain, undrain=a.undrain, sessions_done=a.sessions_done)
    for ln in lines:
        print(ln)
    # a dry run that lists what blocks a wipe exits 1, as the wipe itself would (LIO3-04)
    return 1 if a.dry_run and "blocked by:" in lines else 0


def cmd_sync(a):
    import wipe
    for ln in wipe.sync(REPO, repair=a.repair):
        print(ln)
    return 0


def cmd_intake(a):
    for ln in review.intake(a.issue, a.public):
        print(ln)
    return 0


def cmd_publish_status(a):
    for ln in review.publish_status(a.public):
        print(ln)
    return 0


def cmd_report(a):
    print("\n".join(land.run_view(a.run)["report"]))
    return 0


def cmd_status(a):
    if not a.run:
        units.reconcile_merged(REPO)
    print(units.status(a.run))
    return 0


def cmd_queue(a):
    # the queue as main holds it: the checkout's HEAD moves only with scripts/rq sync (G-11)
    mv = units.main_view(REPO)
    for fn, (mode, oid) in sorted(((mv.listdir("queue") if mv else None) or {}).items()):
        if not fn.endswith(".json"):
            continue
        try:
            q = json.loads(mv.blob(oid).decode("utf-8"))
        except ValueError:
            continue
        if not a.topic or q.get("topic") == a.topic:
            print("%s\t%s\t%s\t%s" % (q["id"], q.get("kind"), q.get("topic"), q.get("question", "")[:100]))
    return 0


# commands that a legacy run folder does not stop (the cut-over of section 5.4 of the one-tree design)
LEGACY_OK = ("status", "wipe", "close")
# commands of an existing run, which print the drain line once while a merge session drains .tmp/
RUN_CMDS = ("plan", "briefs", "brief", "collect", "integrate", "audit", "abandon", "land", "put", "resolve")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="rq", description="research harness; the protocol is docs/research-protocol.md")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("open", help="start a run: KIND TOPIC DETAILS, --issue N claims an rq:research issue"); p.add_argument("kind", type=str.lower, choices=units.RUN_KINDS)
    p.add_argument("topic", type=str.lower); p.add_argument("details")
    p.add_argument("--no-issue", action="store_true")
    p.add_argument("--issue", type=int, help="the rq:research issue this run works: claims it (label rq:active and a comment)")
    p.set_defaults(f=cmd_open)
    p = sp.add_parser("issues", help="the open rq:research issues and their claims: free, taken, or landed")
    p.set_defaults(f=cmd_issues)
    p = sp.add_parser("release", help="give back the claim of an rq:research issue (a dead session, a closed pull request)")
    p.add_argument("issue", type=int); p.add_argument("--run", help="the run whose claim ends; without it, every claim")
    p.add_argument("--reason", required=True); p.set_defaults(f=cmd_release)
    p = sp.add_parser("context", help="what the corpus holds on a topic: records, worklists, registered lists, the queue"); p.add_argument("what", help="a topic or a run id"); p.set_defaults(f=cmd_context)
    p = sp.add_parser("plan", help="plan units from a plan file, the open conflicts, queue items or a worklist; leases and briefs"); p.add_argument("run"); p.add_argument("--file"); p.add_argument("--conflicts", action="store_true")
    p.add_argument("--from-worklist", choices=["stale", "inherited", "unparsed", "held", "drift"]); p.add_argument("--topic")
    p.add_argument("--batch", type=int, default=6)
    p.add_argument("--queue", nargs="*"); p.set_defaults(f=cmd_plan)
    p = sp.add_parser("briefs", help="one lane instruction per unit that waits for a lane: start them all at once"); p.add_argument("run"); p.add_argument("--kind"); p.set_defaults(f=cmd_briefs)
    p = sp.add_parser("brief", help="one unit's lane instruction; --fix reopens a unit with its problems listed"); p.add_argument("run"); p.add_argument("uid"); p.add_argument("--fix", action="store_true"); p.set_defaults(f=cmd_brief)
    p = sp.add_parser("capture", help="a lane stores a page or a probe record and checks a quote against it"); p.add_argument("url", nargs="?"); p.add_argument("--lane")
    p.add_argument("--fresh", action="store_true", help="accepted and ignored: every read is fresh")
    p.add_argument("--wait", action="store_true", help="when the broker asks for a pause (Retry-After), wait and read again")
    p.add_argument("--provider", metavar="ID", help="pin the read to one provider of the broker (the ladder's rung 2)")
    p.add_argument("--from-file"); p.add_argument("--check", metavar="SHA")
    p.add_argument("--probe", metavar="FILE", help="register a probe record; the URL argument is probe:TARGET")
    p.set_defaults(f=capture.cmd)
    p = sp.add_parser("show", help="a record, a file or a capture as a run branch or a commit holds it")
    p.add_argument("ref", help="a run id, or any commit or ref"); p.add_argument("path", nargs="?", help="a rid or a path")
    p.add_argument("--capture", metavar="SHA"); p.add_argument("--out", help="write the bytes to this file")
    p.set_defaults(f=cmd_show)
    p = sp.add_parser("put", help="a parent's file under scripts/sources/ onto the run branch")
    p.add_argument("run"); p.add_argument("path"); p.add_argument("file"); p.add_argument("--reason", required=True)
    p.set_defaults(f=cmd_put)
    p = sp.add_parser("resolve", help="record the resolution of a path that land left in conflict")
    p.add_argument("run"); p.add_argument("path"); p.add_argument("--delete", action="store_true"); p.set_defaults(f=cmd_resolve)
    p = sp.add_parser("folder", help="session: make your .tmp/session-<id>/; review: a merge session's .tmp/review-RUN/")
    p.add_argument("kind", choices=["session", "review"]); p.add_argument("run", nargs="?")
    p.add_argument("--end", metavar="ID"); p.add_argument("--take", metavar="ID"); p.add_argument("--list", action="store_true")
    p.set_defaults(f=cmd_folder)
    p = sp.add_parser("lint", help="a unit's changes, drafts and receipt against the integrator's rules"); p.add_argument("run"); p.add_argument("uid"); p.set_defaults(f=cmd_lint)
    p = sp.add_parser("abandon", help="give up a unit no lane can answer; land then accepts the run without it")
    p.add_argument("run"); p.add_argument("uid"); p.add_argument("--reason", required=True); p.set_defaults(f=cmd_abandon)
    p = sp.add_parser("collect", help="read every unit's receipt and lint it: ready, invalid or still running"); p.add_argument("run"); p.set_defaults(f=cmd_collect)
    p = sp.add_parser("integrate", help="apply the ready units onto rq/RUN in git objects (the only writer of records)"); p.add_argument("run"); p.add_argument("--units"); p.set_defaults(f=cmd_integrate)
    p = sp.add_parser("audit", help="plan the auditors of the integrated units; --score scores them and reverts a failed unit"); p.add_argument("run"); p.add_argument("--score", action="store_true"); p.add_argument("--replan", action="store_true")
    p.add_argument("--per-unit", type=int, default=30, help="the size of the statistical sample per unit: a design of "
                   "the score, not a limit on reads")
    p.add_argument("--census", action="store_true", help="audit every claim of every unit and every path of a confirm")
    p.set_defaults(f=cmd_audit)
    p = sp.add_parser("check", help="the contradiction rules C01 to C21 over dossier/ against the baseline"); p.add_argument("--repo", help="a working tree (CI, an own clone)")
    p.add_argument("--rev", help="a commit or a run branch, read from git objects into memory")
    p.add_argument("--run", help="with --prune: prune the baseline of this run's branch from its own records, on it")
    p.add_argument("--gate", action="store_true"); p.add_argument("--prune", action="store_true")
    p.add_argument("--write-baseline", action="store_true"); p.add_argument("--rule"); p.add_argument("--no-narrative", action="store_true")
    p.set_defaults(f=cmd_check)
    p = sp.add_parser("policy", help="the warn rules that wait for a methodology decision"); p.set_defaults(f=cmd_policy)
    p = sp.add_parser("gatecmp", help="CI and an own clone: the gate on the head against the gate on the base")
    p.add_argument("--base", help="default: origin/main when the clone has it, else main (G2-10)")
    p.add_argument("--head"); p.set_defaults(f=cmd_gatecmp)
    p = sp.add_parser("import-bundle", help="apply a contributor's run folder, received as a zip, onto a fresh run branch")
    p.add_argument("file"); p.set_defaults(f=cmd_import_bundle)
    p = sp.add_parser("baseline-diff", help="rows a pull request adds to the baseline, refused without the label (rq merge checks it too)")
    p.add_argument("--base", required=True); p.add_argument("--head", default="HEAD"); p.add_argument("--labels", default="[]",
                   help="the pull request's label names, as a JSON list"); p.set_defaults(f=cmd_baseline_diff)
    p = sp.add_parser("land", help="research session: open the pull request; the run stops there"); p.add_argument("run")
    p.add_argument("--meets", help="the numbers of the Done-when lines of the claimed issue that this run meets, "
                   "1-based, as N,N; a line that says a merge session ticks it is never ticked")
    p.set_defaults(f=cmd_land)
    p = sp.add_parser("review", help="merge session: runs waiting for review, or one run's decisions")
    p.add_argument("run", nargs="?"); p.add_argument("--sample", type=int, default=3)
    p.add_argument("--pr", metavar="NUMBER|URL", help="with RUN: read the run from this pull request's head (a fork's run, "
                   "or a run that another pull request carries); rq merge RUN --pr reads the same one")
    p.set_defaults(f=cmd_review)
    p = sp.add_parser("merge", help="merge session: update in git objects, CI, merge, follow-up; a fork's pull request gets "
                   "the gated head pushed to its branch (needs Allow edits by maintainers)"); p.add_argument("run")
    p.add_argument("--no-ci", action="store_true", help="skip the remote CI (the light checks still run), only on purpose")
    p.add_argument("--pr", metavar="NUMBER|URL", help="the pull request that carries the run when it is not the run's "
                   "own (several runs combined in one, or a branch that is not rq/RUN): every lookup reads it; merged, "
                   "it finishes the steps after the merge; open, it is merged, and the next run it carries is "
                   "resumed with its own rq merge RUN --pr N")
    p.set_defaults(f=cmd_merge)
    p = sp.add_parser("ci", help="the remote CI of a run's pushed head: its state; --wait waits as rq merge does")
    p.add_argument("run", nargs="?"); p.add_argument("--pr", type=int, help="a pull request that is not a run")
    p.add_argument("--wait", action="store_true"); p.set_defaults(f=cmd_ci)
    p = sp.add_parser("cleanup", help="merge session: after a close without a merge"); p.add_argument("run")
    p.set_defaults(f=cmd_cleanup)
    p = sp.add_parser("close", help="a run whose session died with no pull request, or one left in opening")
    p.add_argument("run"); p.add_argument("--reason", required=True); p.set_defaults(f=cmd_close)
    p = sp.add_parser("wipe", help="merge session, last step: delete all of .tmp/ when nothing is open")
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--drain", action="store_true")
    p.add_argument("--undrain", action="store_true"); p.add_argument("--sessions-done", action="store_true")
    p.set_defaults(f=cmd_wipe)
    p = sp.add_parser("sync", help="merge session: fast-forward the research checkout and build its store once")
    p.add_argument("--repair", action="store_true"); p.set_defaults(f=cmd_sync)
    p = sp.add_parser("intake", help="merge session: a public issue becomes a queued question"); p.add_argument("issue", type=int)
    p.add_argument("--public", default=review.PUBLIC); p.set_defaults(f=cmd_intake)
    p = sp.add_parser("publish-status", help="merge session: publish lag and the public issues labelled queued")
    p.add_argument("--public", default=review.PUBLIC); p.set_defaults(f=cmd_publish_status)
    p = sp.add_parser("report", help="a run's counts: units, applied values, audits, abandoned units"); p.add_argument("run"); p.set_defaults(f=cmd_report)
    p = sp.add_parser("status", help="the runs of this checkout, or one run's units and phase"); p.add_argument("run", nargs="?"); p.set_defaults(f=cmd_status)
    p = sp.add_parser("queue", help="the queued questions on main, by topic"); p.add_argument("--topic"); p.set_defaults(f=cmd_queue)
    a = ap.parse_args(argv)
    try:
        if legacy_dirs(REPO) and a.cmd not in LEGACY_OK:
            raise Fail("legacy run folders: close or finish them (scripts/rq close RUN for one that is still open), then run "
                       "scripts/rq wipe (.tmp/rq/runs/ or .tmp/rq/wt/ is the harness before the one-tree change)", 1)
        if a.cmd in RUN_CMDS and os.path.exists(os.path.join(REPO, ".tmp", "rq", "state.db")):
            c = state.control(REPO, "drain")
            if c:
                print("rq: " + state.DRAIN_LINE % c[1], file=sys.stderr)
        return a.f(a)
    except Fail as e:
        print("rq: %s" % e, file=sys.stderr)
        return e.code
    finally:
        try:
            state.close_all()
            units.close_stores()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
