"""rq audit: the second key. Sample each integrated unit's claims, have a fresh lane re-read them from the
capture (or a fresh capture), score each unit with a 95% bound, revert units that fail.

A unit is reverted when more than 10% of its decided claims are unsupported, or, when the audit read a sample
rather than every claim, when the Wilson 95% upper bound on that rate exceeds 25%. Each unsupported claim of a
kept unit becomes a conflict, and so a reconcile item.
"""
import hashlib
import json
import math
import os
import random
import re

import track
import units
from common import (REPO, Fail, Overlay, append_jsonl, commit_on, fr, json_bytes, quote_found, read_capture, read_json,
                    read_jsonl, run_dir, run_lock, stamp, utf8_problem, write_json)

RATE, BOUND = 0.10, 0.25


def failed(uns, n, census):
    """A sample bounds the rate of the claims nobody read (Wilson); a census read them all, so only the
    observed rate decides."""
    return n > 0 and uns > 0 and (uns / n > RATE or (wilson_upper(uns, n) > BOUND and not census))


def wilson_upper(errors, n, z=1.96):
    if n == 0:
        return 1.0
    p = errors / n
    return (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n)


def unknown_text(text):
    """The brief's form of an unknown value, `unverified: <the reason>` (or the bare word): the text starts with it.
    A sentence that states a fact and calls one part of it unverified is still a claim (W5-02)."""
    return isinstance(text, str) and text.strip().lower().startswith("unverified")


def declared_unknown(rec, path, value):
    """A value its author marked unverified is not a claim, so it is not audited."""
    if unknown_text(value):
        return True
    if path == "$.identity_cost.kind":
        return unknown_text((rec.get("identity_cost") or {}).get("detail") or "")
    return False


def claims_for_unit(view, run, uid, census=False):
    """The claims a unit left on the run branch, read through the run tree (no worktree, no file written). A confirm
    gives the first three paths it names, or every path with census."""
    import integrate
    m = fr()
    led = integrate.ledger_lines(view, run, uid)
    out = []

    def rec_of(rid):
        return json.loads(view.read("dossier/%s.json" % rid).decode("utf-8"))

    def value_at(rec, path):
        try:
            v = m.get_path(rec, m.parse_jpath(path))
        except Exception:
            return None
        return None if v is m.ABSENT else v

    for l in led:
        if l.get("unit") != uid or l.get("op") not in ("set", "confirm", "dead", "add_record"):
            continue
        if not view.exists("dossier/%s.json" % l["rid"]):
            continue
        if l["op"] == "add_record":
            rec = rec_of(l["rid"])
            evs = [e for e in rec.get("evidence") or [] if isinstance(e, dict) and e.get("capture")]
            if not evs:
                continue
            for path in ("$.verdict", "$.free_tier.stated", "$.identity_cost.kind"):
                val = value_at(rec, path)
                if not declared_unknown(rec, path, val):
                    # a new record's fields rest on its evidence as a whole: the auditor gets every captured row
                    out.append({"rid": l["rid"], "path": path, "value": val, "evidence": evs[0], "evidence_all": evs,
                                "op": "add_record"})
        elif l["op"] == "confirm":
            rec = rec_of(l["rid"])
            paths = (l.get("reason") or "").split(", ")
            for path in paths if census else paths[:3]:
                if path.startswith("$."):
                    val = value_at(rec, path)
                    if not declared_unknown(rec, path, val):
                        out.append({"rid": l["rid"], "path": path, "value": val, "evidence": l.get("evidence"), "op": "confirm"})
        else:
            if not declared_unknown(rec_of(l["rid"]), l.get("path"), l.get("new")):
                out.append({"rid": l["rid"], "path": l.get("path"), "value": l.get("new"), "evidence": l.get("evidence"), "op": l["op"]})
    return out


def plan_audit(run, per_unit=30, repo=REPO, replan=False, census=False):
    """One auditor per integrated unit that left a claim. per_unit is the size of the statistical sample (0: every
    claim); it is a design of the score, not a limit on reads: an auditor makes every read its claims need."""
    r = units.load_run(run, repo)
    view = units.run_tree(run, repo)
    made = []
    if replan:
        # set aside every auditor not scored yet (a planning defect, not a verdict), and plan afresh
        for a in units.units_of(run, repo):
            if a["kind"] == "audit" and not a.get("scored"):
                a.update({"status": "superseded", "scored": True})
                units.save_unit(a, repo)
                t = units.load_unit(run, a["audits"], repo)
                t.pop("audited_by", None)
                units.save_unit(t, repo)
    for u in units.units_of(run, repo):
        if u["kind"] == "audit" or u["status"] != "integrated" or not u.get("commit") or u.get("audited_by"):
            continue
        cl = claims_for_unit(view, run, u["id"], census)
        if not cl:
            u["audit_none"] = True  # no claim to re-read: the hints and the report do not ask for its audit (W2-01)
            units.save_unit(u, repo)
            continue
        rnd = random.Random("%s/%s" % (run, u["id"]))
        sample = cl if not per_unit or len(cl) <= per_unit else rnd.sample(cl, per_unit)
        for i, c in enumerate(sample, 1):
            c["cid"] = "c%02d" % i
        n = len(units.units_of(run, repo)) + 1
        aid = "u%02d" % n
        a = {"id": aid, "run": run, "kind": "audit", "topic": u["topic"], "audits": u["id"],
             "question": "Re-read %d claim(s) integrated by unit %s and judge each against its source." % (len(sample), u["id"]),
             "scope": {}, "seeds": [], "status": "planned", "created": stamp(),
             "census": len(sample) == len(cl)}
        d = units.unit_dir(run, aid, repo)
        # the folders a lane has, but new/ (an auditor drafts no record): the brief writes broker output into tmp/ and
        # probe records into probe/ (W3-01)
        for sub in ("captures", "probe", "tmp"):
            os.makedirs(os.path.join(d, sub), exist_ok=True)
        # claims.json names each cited capture by hash; the auditor reads it with scripts/rq show RUN --capture SHA,
        # so no copy of a capture is written into an auditor folder (IO-11)
        write_json(os.path.join(d, "claims.json"), sample)
        units.save_unit(a, repo)
        write_audit_brief(a, len(sample), repo)
        u["audited_by"] = aid
        units.save_unit(u, repo)
        made.append(a)
    if made:
        track.comment(r, "audit planned: %s" % ", ".join("%s audits %s" % (a["id"], a["audits"]) for a in made), repo)
    return made


def write_audit_brief(a, n, repo=REPO, fix=None):
    d = units.unit_dir(a["run"], a["id"], repo)
    rel = os.path.relpath(d, repo).replace("\\", "/")
    t = open(os.path.join(units.TEMPLATES, "audit.md"), encoding="utf-8").read()
    text = t.format(run=a["run"], uid=a["id"], audits=a["audits"], n=n, workspace=rel,
                    capture_cmd="%s capture --lane %s" % (units.RQ, rel), check_cmd="%s capture --lane %s --check" % (units.RQ, rel),
                    show_cmd="%s show %s --capture" % (units.RQ, a["run"]))
    if fix:
        text += units.fix_section(fix)
    with open(os.path.join(d, "brief.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def score(run, repo=REPO):
    r = units.load_run(run, repo)
    with run_lock(run, repo):
        if r.get("phase") == "in-review":
            import land
            land.update_branch(r, repo, "audit")
        view = units.run_tree(run, repo)
        return _score(r, run, view, repo)


def skip_cid(rid, path):
    """The claim id of a value an undo left (a later unit changed it since): stable, unique per (rid, path) and safe
    as a file name on every system, so `rq audit --score` can write `unsupported/<audit>-<cid>.json` for it."""
    raw = "%s %s" % (rid, path)
    return "skip-%s-%s" % (re.sub(r"[^A-Za-z0-9._-]+", "-", raw).strip("-")[:60],
                           hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8])


def skip_row(audit_id, s):
    """The unsupported row of one undo_skipped entry {rid, path, wrote, now}. It is not an auditor's verdict: the
    `skipped` flag keeps it out of the conflicts of a kept unit and out of the count of unsupported claims."""
    return {"cid": skip_cid(s["rid"], s.get("path")), "rid": s["rid"], "path": s.get("path"), "value": s.get("wrote"),
            "audit": audit_id, "skipped": True,
            "note": "the unit was undone, but a later unit has changed this value since; now %s"
            % json.dumps(s.get("now"), ensure_ascii=False)[:160]}


def missing_unsupported(run, repo=REPO):
    """The unsupported rows of the scored audits of a run that have no file in `unsupported/` yet. An older harness
    saved an audit as scored and then crashed on a skipped row (no cid) before it wrote the files, and a later score
    skips a scored audit; the rows are rebuilt from the audit's claims and verdicts and from the target's undo_skipped."""
    out = []
    udir = os.path.join(run_dir(run, repo), "unsupported")
    for a in units.units_of(run, repo):
        if a["kind"] != "audit" or not a.get("scored"):
            continue
        d = units.unit_dir(run, a["id"], repo)
        claims = {c["cid"]: c for c in read_json(os.path.join(d, "claims.json"), []) if c.get("cid")}
        rows = [dict(claims[v["cid"]], audit=a["id"], note=v.get("note"), quote=v.get("quote"))
                for v in read_jsonl(os.path.join(d, "verdicts.jsonl"))
                if v.get("cid") in claims and v.get("verdict") == "unsupported"]
        try:
            rows += [skip_row(a["id"], s) for s in units.load_unit(run, a["audits"], repo).get("undo_skipped") or []]
        except Fail:
            pass
        out += [c for c in rows if not os.path.exists(os.path.join(udir, unsupported_name(c)))]
    return out


def unsupported_name(c):
    """The file name of an unsupported row in `unsupported/`: audit id and claim id, made safe for Windows too."""
    cid = c.get("cid") or "skip-%s" % hashlib.sha1(("%s %s" % (c.get("rid"), c.get("path"))).encode("utf-8")).hexdigest()[:8]
    return re.sub(r'[^A-Za-z0-9._-]+', "-", "%s-%s" % (c.get("audit"), cid)) + ".json"


def _score(r, run, view, repo):
    rows, unsupported = [], []
    for a in units.units_of(run, repo):
        if a["kind"] != "audit" or a.get("scored"):
            continue
        d = units.unit_dir(run, a["id"], repo)
        bad = utf8_problem(os.path.join(d, "verdicts.jsonl"))
        if bad:
            # not scored: the auditor writes the file again (brief --fix), and the next score takes it
            a.update({"status": "invalid", "problems": [bad]})
            units.save_unit(a, repo)
            continue
        claims = {c["cid"]: c for c in read_json(os.path.join(d, "claims.json"), [])}
        target = units.load_unit(run, a["audits"], repo)
        tdir = units.unit_dir(run, target["id"], repo)
        verdicts = {v.get("cid"): v for v in read_jsonl(os.path.join(d, "verdicts.jsonl")) if v.get("cid") in claims}
        sup = uns = cant = bad = 0
        for cid, c in claims.items():
            v = verdicts.get(cid)
            if not v:
                continue
            verdict = v.get("verdict")
            if verdict == "supported":
                cap = v.get("capture") or (c.get("evidence") or {}).get("capture")
                text = None
                if cap:
                    text = read_capture(cap, repo, d, view) or read_capture(cap, repo, tdir, view)
                if not text or quote_found(v.get("quote") or "", text)[0] == "miss":
                    bad += 1  # a 'supported' whose quote is not in the capture is not a decision
                    continue
                sup += 1
            elif verdict == "unsupported":
                uns += 1
                unsupported.append(dict(c, audit=a["id"], note=v.get("note"), quote=v.get("quote")))
            else:
                cant += 1
        n = sup + uns
        upper = wilson_upper(uns, n)
        fail = failed(uns, n, a.get("census"))
        # no claim decided: the unit is kept, and the report and the follow-up issue say that nobody checked it
        undecided = n == 0 and bool(claims)
        sc = {"supported": sup, "unsupported": uns, "cannot_tell": cant, "unverifiable_quotes": bad, "decided": n,
              "upper95": round(upper, 3), "failed": fail, "undecided": undecided}
        # the audit unit is saved as scored last, after the undo, the target's state and the queued re-run: a kill
        # in between leaves it unscored, and the next score finishes what is missing and repeats nothing (G-09)
        if fail and target.get("commit"):
            import integrate
            led = integrate.ledger_lines(view, run, target["id"])
            if any(l.get("op") in ("undo", "undo_skipped") for l in led):
                # the undo commit is on the branch (a score killed before the target was saved): what it undid and
                # what it left are read back from its ledger lines, not from the unsaved state (G2-07)
                undone = target.get("undone") or sum(1 for l in led if l.get("op") == "undo")
                skipped = target.get("undo_skipped") or [
                    {"rid": l["rid"], "path": l.get("path"), "wrote": l.get("old"), "now": l.get("new")}
                    for l in led if l.get("op") == "undo_skipped"]
            else:
                undone, skipped = integrate.undo_unit(run, target["id"], "audit %s: %d of %d claims unsupported"
                                                      % (a["id"], uns, n), repo, view)
            target.update({"status": "reverted", "undone": undone, "undo_skipped": skipped})
            units.save_unit(target, repo)
            for s in skipped:
                unsupported.append(skip_row(a["id"], s))
            found = ["%s %s: %s" % (c["rid"], c.get("path"), (c.get("note") or "")[:300].replace("\n", " "))
                     for c in unsupported if c.get("audit") == a["id"] and c.get("rid")]
            q = {"id": "%s-%s-rerun" % (run, target["id"]), "kind": target["kind"], "topic": target["topic"],
                 "question": target["question"] + ("\nAn audit of the first attempt judged these claims unsupported by their "
                                                   "sources; settle each one first:\n" + "\n".join("- " + x for x in found)
                                                   if found else ""),
                 "scope": target["scope"], "origin": "audit %s of %s/%s failed: %d of %d unsupported"
                 % (a["id"], run, target["id"], uns, n), "created": stamp()}
            if integrate.queue_files_of(target):
                # the queued questions the unit answered are back in the queue (the undo restored them); the re-run
                # names them, so its brief lists them and its commit takes them out again (W4-03)
                q["queue_files"] = integrate.queue_files_of(target)
            if not view.exists("queue/%s.json" % q["id"]):
                new = commit_on(repo, units.ref_of(run), view.commit, {"queue/%s.json" % q["id"]: json_bytes(q)},
                                "rq %s: queue a re-run of %s after its audit failed" % (run, target["id"]),
                                view=view)
                if new != view.commit:
                    view.advance(new)
        else:
            # a kept unit's unsupported claims are conflicts: `scripts/rq plan RUN --conflicts` makes reconcile units
            cpath = os.path.join(run_dir(run, repo), "conflicts.jsonl")
            have = {(c.get("unit"), (c.get("op") or {}).get("rid"), (c.get("op") or {}).get("path"), c.get("why"))
                    for c in read_jsonl(cpath)}
            for c in unsupported:
                why = "audit %s judged it unsupported: %s" % (a["id"], (c.get("note") or "")[:400])
                if c.get("audit") == a["id"] and c.get("rid") and (target["id"], c["rid"], c.get("path"), why) not in have:
                    append_jsonl(cpath, {
                        "run": run, "unit": target["id"], "at": stamp(), "why": why,
                        "op": {"op": "set", "rid": c["rid"], "path": c.get("path"), "new": c.get("value"),
                               "evidence": c.get("evidence") or {}},
                        "current": c.get("value")})
        a.update({"scored": True, "status": "integrated", "score": sc})
        units.save_unit(a, repo)
        rows.append((a["audits"], a["id"], sup, uns, cant, bad, round(upper, 3),
                     "REVERTED" if fail else ("kept, UNDECIDED: no claim decided" if undecided else "kept")))
    if rows:
        track.comment(r, "audit scores (unit, auditor, supported, unsupported, cannot tell, unverifiable, upper95, result):\n"
                      + "\n".join("- %s %s %d %d %d %d %.3f %s" % x for x in rows), repo)
    return rows, unsupported
