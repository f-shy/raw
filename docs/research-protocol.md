# Research protocol: one request, many lanes, one writer

⭐ **This document is the whole procedure for a research run.** A request is one line, for example
`Expand domains-dns free DNS hosting with an API`. A parent agent reads this document and does the rest.
The parent can be any agent in any tool, on any model. The lanes can be any agents too.

The harness is a set of plain commands, `scripts/rq` (code in [`../scripts/research/`](../scripts/research/README.md)).
It calls no model. The parent starts lanes with the subagent mechanism of its own tool. The harness gives
each lane one line to read, checks what the lane hands back, and applies it through one program.

⛔ **The parent never edits `dossier/`, `history/`, `registry/`, `sources/` or `queue/` during a run, and never
runs a git command that writes** ([`../AGENTS.md`](../AGENTS.md) section 2 rule 14). Only `scripts/rq integrate`
writes there, on the run's own branch, in git objects: the run branch `rq/<run>` is a git ref, never a checkout.

⛔ **A run does not edit `BRIEF.md`, a topic document or a `history/` entry by hand.** The integrator writes the
records and their ledger lines (the ledger is the history of a changed value). A run changes a topic document only
through the render that `land` runs: it re-renders the generated tables of `docs/` from the records. One of them is
the block "Records that no other document names" at the end of each topic README. It lists each `measured` or
`documented` record that no other document names, so a record the run added is cited and the gate's `links` check
passes with no hand edit of prose. The handover is the pull request body that `land` writes and the follow-up
issue that `merge` files. The work queue is the open issues labelled `rq:research` (section 9).

⛔ **No agent creates an account, signs up, enters a payment detail, buys anything or provisions a resource
that needs an account or a payment** ([`../AGENTS.md`](../AGENTS.md) section 2 rule 13). The sign-up gate a lane sees is the finding. A value that
only an account shows is `unverified: behind a sign-up`, and a step that needs an account goes to the open
issue labelled `rq:operator`.

⛔ **One working tree, every file under `.tmp/<id>/`** ([`../AGENTS.md`](../AGENTS.md) section 2 rule 14). All
research on the machine runs in the research checkout, 30 or more agents at the same time. No agent makes a git
worktree, a clone or a fork, changes the checkout's branch, index, tracked files or git configuration, builds a
store of its own or runs the gate. Every file an agent makes goes under `.tmp/<run>/`, its unit folder or its
`.tmp/session-<id>/`, and the merge session deletes all of `.tmp/` with `scripts/rq wipe` after its merges.

⛔ **Never cap your own requests** ([`../AGENTS.md`](../AGENTS.md) section 2 rule 15). Start every lane of a plan
at once, read every page a question needs, and try every route. No client-side cap applies; the only pacing
is a server's own 429 or 503 with `Retry-After` (section 6).

⛔ **Self-hosting is the last resort** ([`../AGENTS.md`](../AGENTS.md) section 2 rule 9). Software a reader
installs and runs itself, on any machine, rented or free ones included, comes after every hosted offer (free,
trial or paid). Plan its units last; list it last in a plan, an issue comment, a pull request body and the report;
and never star it, rank it first or present it as the answer while a hosted offer (free, trial or paid) exists.

---

## Contents

1. [Roles](#1-roles)
2. [From the request to a run](#2-from-the-request-to-a-run)
3. [The procedure](#3-the-procedure)
4. [The plan file](#4-the-plan-file)
5. [What the parent reads, and what it does not](#5-what-the-parent-reads-and-what-it-does-not)
6. [Parallel runs, leases and the broker](#6-parallel-runs-leases-and-the-broker)
7. [Evidence: a capture and a quote](#7-evidence-a-capture-and-a-quote)
8. [Checks, the gate and the ratchet](#8-checks-the-gate-and-the-ratchet)
9. [Issues: the parent's tracker](#9-issues-the-parents-tracker)
10. [Resuming a run](#10-resuming-a-run)
11. [Where each file lives](#11-where-each-file-lives)
12. [When something goes wrong](#12-when-something-goes-wrong)
13. [The merge session, in short](#13-the-merge-session-in-short)

---

## 1. Roles

| role | who | writes |
|---|---|---|
| operator | whoever asks for the run. States one line and reads the final report | nothing |
| parent | any agent. Runs `scripts/rq`, writes the plan, starts lanes, reads receipts and the report | `.tmp/<run>/` (the plan, `tools/`, `conflicts/`) and its `.tmp/session-<id>/` (`RESUME.md`, notes) |
| lane | any agent, any model. Gets one line, answers one question | only its own workspace, `.tmp/<run>/units/<unit>/`; every command from the repository root |
| integrator | a program, `scripts/rq integrate` | the run branch `rq/<run>`, with git plumbing; no worktree, no checkout |
| auditor | a lane with an audit brief. ⭐ Use a different model or tool from the lane it audits, when you have one | its own workspace |
| merge session | another session, which did not run the research, in any clone. Reviews the pull request, merges it, cleans up, and publishes to the public repository. At the end of a merge pass it deletes all of the research checkout's `.tmp/` with `scripts/rq wipe` and fast-forwards it with `scripts/rq sync`. Its procedure is `docs/merge-protocol.md` in `f-shy/fshy.ajam.dev`; section 13 has its commands | `main`, after review; the research checkout's HEAD, only through `scripts/rq sync` |

⛔ **A research session never merges its own run.** The run stops at an open pull request (step 9), and the
session goes on with the next run (step 11). The run folder `.tmp/<run>/` and the leases stay until a merge
session has merged or closed the pull request; a run's leases hold its records through the review (section 6). The
merge session deletes all of `.tmp/` with `scripts/rq wipe` after its merges.

⭐ **The merge session needs no file of the research checkout.** `land` commits the run manifest,
`history/ledger/<run>/manifest.json`, on the run branch. `scripts/rq review RUN`, `merge RUN`, `report RUN` and
`cleanup RUN` read this checkout's run folder when it ran the run, and the manifest on `origin/rq/<run>` (or on
`main` after the merge) when it did not. `merge` updates the branch in git objects; it makes no worktree.

A lane is independent of the parent's context. Its brief holds everything it needs, so a lane can run in another
tool or a day later. It runs in the research checkout, from the repository root, never in a clone or a worktree of
its own.

---

## 2. From the request to a run

| the request | run kind | units the parent plans |
|---|---|---|
| `Research <topic> <details>` | `research` | `discover` units for new offers, `verify` units for records the details touch |
| `Expand <topic> <details>` | `expand` | mostly `discover` units, one per slice or per name list |
| `Verify <topic>` or `Re-check <topic>` | `verify` | `verify` units from a worklist (`--from-worklist stale` or `inherited`) |
| `Amend <topic> <details>` or `Fix <topic> ...`; for a single record, the topic of its rid | `amend` | `verify` units on the records the details name: one unit for a single record |
| `Maintain` | `maintain` | `verify` units from the worklists, and `scripts/rq queue` items |
| (none: the harness makes these) | `reconcile` | one `reconcile` unit per record with open conflicts |

The topic must be one of the topics in [`README.md`](README.md); `scripts/rq open` refuses any other. ⚠ A new
topic is a decision, not a directory ([`conventions/README.md`](conventions/README.md) §2.2). If the request needs
a topic that does not exist, use the nearest topic, say so in the run's request text, and comment on the issue (or
file an `open_question`) naming the topic and the records that need it; a rules session in an
own clone opens the pull requests ([`../AGENTS.md`](../AGENTS.md) section 2 rule 12). The same holds for a value
that fits no term of a schema vocabulary.

⚠ **A record never moves to another topic.** `fr` refuses a change of `topic` or `slug`, and a lane has no move.
To bring an offer into a new topic, a `discover` unit adds the record there. After `integrate`, plan a `verify`
unit whose `scope.rids` holds the old record and the new one; its lane proposes `relate` with `src` the old
record, `kind` `duplicate_of` and `dst` the new record. The old record stays, and the store marks it as a
duplicate. A record that stays where it is gets the reason in its `notes`, through a `set`.

⭐ **A research agent does not write a tool.** A request that needs a program (a probe loop, a sweep, an
extractor) before its units can measure anything waits for that program. The parent comments the program's
specification on the issue and takes another issue; a tools session runs for it, in an own clone,
and a merge session reviews it as code (the same CI, the baseline check included: `scripts/rq ci --pr NUMBER --wait`). After the merge, a later run
plans the units that use it. `scripts/rq issues` shows an issue whose "Tool" line is unticked as "waits for a
tool". `rq plan` has no unit kind for a tool, and a lane writes only its own workspace.

⚠ **A registered provider list is updated by the parent, not by a lane.** A lane whose seeds name a registered
list writes the covered and missing counts as the first line of its `log.md` (its brief says so). The list's
registry file is `scripts/sources/aggregators.tsv` or a topic's own, such as `egress-aggregators.tsv`:
`grep -l SLUG scripts/sources/*aggregators*.tsv` names it, and `scripts/rq context TOPIC` prints it beside each
source. Before `land`, the parent records the counts on the run branch, with LIST that file's name:

```bash
scripts/rq show RUN scripts/sources/LIST --out .tmp/RUN/tools/LIST
python scripts/sources/aggregator-diff.py --registry .tmp/RUN/tools/LIST --record SLUG --covered N --missing M
scripts/rq put RUN scripts/sources/LIST .tmp/RUN/tools/LIST --reason "sources: diff SLUG"
```

`put` takes only a file under `scripts/sources/`, and refuses a carriage return in a file whose base has none. It
also compares what `show` read: `show --out FILE` writes `FILE.base` with the commit and the blob it read, and `put`
refuses when the path changed on `rq/RUN` since then (a merge of `main` by `plan`, or of `origin/rq/RUN` after a
send-back), or when `FILE.base` is missing for a path the branch has. Writing the file then would undo that change,
and the clean merge with `main` would carry the undo to `main`. Run `show` again and redo the edit. CI's gate
`sources` check reads the new `last_diff`.

---

## 3. The procedure

Run every command from the repository root. Each step prints the next command. Without `sh`, for example in
PowerShell, write `python scripts/research/rq.py` for `scripts/rq` and `python scripts/fshy/fr.py` for `scripts/fr`.

**Step 0. Preconditions.** Do these once per session, from the repository root of the research checkout.

```bash
git config --get core.hooksPath                # prints .githooks
git config --get rq.researchCheckout           # prints true
git --no-optional-locks status --short
scripts/rq folder session                      # your folder .tmp/session-<id>/, for RESUME.md and notes
```

⛔ If either `git config` line prints nothing, this is not a prepared research checkout: stop and
report it, and do not set them yourself. `scripts/rq status` prints the marker, and says when the checkout's HEAD
is not in `origin/main` (a feature branch, where `open` refuses).

⛔ Do not run the gate, `scripts/rq gatecmp` or the selftest: CI runs them on the pushed head, in the public
repository's Actions (AGENTS.md section 0), and `scripts/rq ci RUN` shows the result. Do not write git
configuration. The checkout stays on the branch it is on, and no run makes a worktree: the run branch is a git ref
that `scripts/rq` writes. ⚠ CI's gate can be red on a clean `main`: `staleness` and `sources` depend on the
clock. `BRIEF.md` section 5 "Known red checks" names what is red today, the issue that owns each red check, and what
clears it. A check that is red on `main` too is not your task; only the session whose issue owns it works on it.

**Step 1. Open the run on its issue.** Take an open `rq:research` issue that `scripts/rq issues` lists as free,
at random, not the first: thirty sessions that start together and each take the first free issue all claim the
same one. `scripts/rq issues` ends with one free issue picked at random. When `open` says the issue is taken, take
another free one the same way. KIND and TOPIC are the first two words of the issue's request line, in any case
(`Verify` is `verify`). In an issue run once for each topic, TOPIC is a placeholder: use a topic of its list that
`scripts/rq issues` shows free:

```bash
scripts/rq issues
scripts/rq open expand domains-dns "free DNS hosting with an API" --issue 39
```

`scripts/rq issues` prints every open `rq:research` issue (it reads up to 200) as free, taken by a run, or landed
and waiting for a merge session. `--issue N` claims issue N before the run exists: it adds the label `rq:active`
and a comment `rq claim: run RUN topic TOPIC started at TIME`, so another session, on the same GitHub account or
not, sees that the issue is taken. A claim holds only its own topic: an issue that is run once for
each topic (its last "Done when" line starts "Every topic of the list has a merged run", or its body says it is
run once for each topic) takes one run per topic
at a time, and `scripts/rq issues` shows the topics that are taken. `open` refuses a live claim of the same
topic: one younger than `claim_hours` (24, in `scripts/research/settings.json`) with no pull request, or one
whose run has landed and whose pull request is still open. Two sessions of this checkout never claim one topic
of one issue together: `open` holds the claim lock of the issue and topic (under `.tmp/rq/locks/`) from its read
of the issue to its read-back of the claim, and refuses a topic that a run of this checkout holds. A session on
another machine is not held by that lock, so after its comment `open` reads the issue again: when GitHub lists a
claim of the same topic before this one, this run comments `rq released:` and `open` refuses. `open` checks each
write to GitHub; when the comment or the label fails, it gives back what it wrote and refuses, and the run is
closed in phase `opening`. Then run `open` again, or take another issue. A claim ends when a merge session merges the run
(`rq merged:`), when the pull request is closed without a merge, or with `scripts/rq release N --run RUN --reason
"..."` (`rq released:`); a claim with no pull request after 24 hours has expired, and `open` takes the issue
over. Without `gh` the claim is not written, and `open` prints the two `gh` commands to run; with
`RQ_NO_GITHUB` it says only that the claim is not written.

This prints the run id, `YYYYMMDD-HHMM-<kind>-<topic>-<4 hex>`. The random part keeps apart two parents that
open the same kind and topic in one minute. It opens an `rq:run` issue when `gh` is available, and prints the plan
file to write, `.tmp/RUN/plan.json`. `open` refuses while a merge session drains `.tmp/` for a wipe: then open no
run, and finish and land the one you have.
⭐ Write the run id into your `RESUME.md` now (`.tmp/session-<id>/RESUME.md`, [`../AGENTS.md`](../AGENTS.md) section
0 step 4). It is the only thing a resuming session needs.

**Step 2. Read the context.**

```bash
scripts/rq context domains-dns
scripts/fr search "dns api"
```

`context` prints a screenful (about 15 lines): record counts, worklists, the sources, and the open queue for the
topic.
⚠ The store of the research checkout is built by the merge session at the end of its merges. When it is missing,
the first `context` or `scripts/fr` call builds it, once for the machine, in about two minutes; every other agent
waits for that build and then reads the same store. Run such a call in the background when your tool stops a
command after two minutes. The store holds `main` as the checkout has it: read a record as your run holds it with
`scripts/rq show RUN RID`.
Use `scripts/fr` for any other question. Do not read the topic's documents end to end to plan a run.

**Step 3. Plan the units.** Write a plan file (§4). An issue's "Suggested units" bullet is one object of the plan
list; when the issue has no "Suggested units", plan one unit for each list of records it names, and split a
bullet that asks two questions into two units. ⭐ In an issue run once for each topic, plan only the bullets whose
`topic` is the run's topic, or that carry none: another topic's bullets belong to that topic's run and claim, and
`plan` refuses them in such a run. The fields have the same names: `kind`, `question`, `scope.new.names` or `scope.new.slice` or `scope.rids`,
`queue_files`, `seeds`. Where the issue describes records in words, look up the rids
(`scripts/fr search NAME`, or the query the issue prints) and write them out; `plan` refuses a rid with no file.
A bullet that says "after the discover units integrate" is a second `plan` call on the same run after
`integrate`: `plan` reads the records the run added from its branch. For example, the bullet
`kind` verify. `question` "Q" `scope.rids` ["email/mailbig"]. `queue_files` ["queue/ID.json"] is the object
`{"kind": "verify", "question": "Q", "scope": {"rids": ["email/mailbig"]}, "queue_files": ["queue/ID.json"]}`.
Then:

```bash
scripts/rq plan RUN --file .tmp/RUN/plan.json
scripts/rq plan RUN --from-worklist stale --batch 6
scripts/rq plan RUN --queue QUEUE_ID ...
```

`--from-worklist` plans every row of the worklist, `--batch` records per unit.

`plan` makes one workspace and one brief per unit. It leases each unit's write scope. When `main` changed a
record that a unit names (or a topic's records, for a `discover` unit) since the run took `main`, because another
run merged, `plan` first merges `main` into the run branch in git objects. The lane then reads the record as
`main` holds it, and `integrate` compares against that value; a conflict there stops `plan` with the steps of
section 12. It checks every unit of
the file before it leases any, so a file with one invalid unit plans nothing: a `scope.rids` entry with no
record file is refused (exit 2), and `scripts/fr search NAME` finds the right rid. A unit whose scope another
unit holds, in this run or in any other run, is refused with a note, and `plan` then exits 1: the other units
are planned, so plan the refused one again on its own with a new scope, or drop it. Name a record in one unit
only, and plan a queue item with `--queue ID` instead of repeating its question in another unit. Queue items
given in one `--queue` call that share a record become one unit: their questions are joined, and every queue
file leaves the queue when that unit integrates. Each queue item is checked alone. An item that names a record with
no file is refused with a note, and `plan` exits 1: plan it from a plan file, with the record its question means
and its file in `queue_files`. An item whose file has left the queue, because another run answered it, is skipped
with a note. An id that was never queued still plans nothing (exit 2).

⚠ **Plan only what a lane can do with its commands.** A lane may run `scripts/rq capture` (with
`--provider ID` for a read pinned to one provider), `scripts/rq lint`, the `scripts/fr` read commands,
`sh scripts/broker/broker.sh search`, the ladder's other rungs (`sh scripts/broker/broker.sh fetch URL
--dump-headers` and `sh scripts/broker/broker.sh archive URL --at YYYY-MM`, each written into the lane's `tmp/`
and registered with `scripts/rq capture URL --lane WS --from-file FILE`), and three read-only probes:
`python scripts/probe/probe.py`, `python scripts/probe/tcpprobe.py --endpoint HOST:PORT` and
`python scripts/probe/cartcheck.py`, each writing into its workspace. Any other tool (a sweep, a script that
writes to a remote host, a GitHub code search) is a step of the parent. Run it before `plan`, save its output under
`.tmp/RUN/tools/`, and name the file in the unit's `seeds`. The lane registers the file with
`scripts/rq capture probe:TARGET --lane WS --probe FILE` and cites the hash. ⚠ `--probe` reads the content, not
the file name. Content that parses as JSON is taken only when it is a probe record (the three probes write one; a
JSON file that another tool wrote needs a `probed_at` key with the UTC time, which the parent adds before `plan`),
or when it is a body that `probe.py URL --save-body FILE --out DIR` saved, with the record in the same folder as
`FILE` naming its sha256: a lane registers such a body itself when the measured value is in it (a DoH answer's
`"Status": 3`). Any other text, a TSV among it, is taken as it is. The file, or the record of a body, must name the
target's host when the target has one (`probe:https://HOST/...`, `probe:HOST:PORT`).

**Step 4. Start the lanes.**

```bash
scripts/rq briefs RUN
```

This prints one line per unit: the unit id, a tab, and the instruction. Give each lane that one
instruction and nothing else. The instruction tells the lane to read its brief and to answer with the path
of its receipt.

- ⭐ **Start every lane at once.** There is no lane limit and no limit on pages. No client-side cap applies;
  a broker 429 or 503 with `Retry-After` makes `scripts/rq capture` print `retry_at` and exit 4, and the lane reads
  other pages and comes back ([`../AGENTS.md`](../AGENTS.md) section 2 rule 15). Thirty or more lanes at the same
  time is the expected load.
- ⛔ Start each lane in the research checkout, at the repository root, never with a subagent option that gives it a
  worktree or a clone.
- ⛔ Do not add context, findings or hints to the instruction. The brief is the contract. A lane that
  depends on the parent's context cannot be re-run or audited.
- ⛔ Do not read a lane's chat answer beyond the receipt path. The work is on disk.
- When your tool cannot start subagents, do the lanes yourself, one after another. Read each brief as
  if you knew nothing else, write only in that unit's workspace, and write its receipt before you start
  the next brief. The rest of the procedure does not change.

**Step 5. Collect.**

```bash
scripts/rq collect RUN
```

`collect` reads every receipt and lints every proposed operation: scope, schema, capture, quote, numbers,
narrative. A `changes.jsonl`, `receipt.json` or `verdicts.jsonl` that is not UTF-8 is a problem that names the
byte and the line. It then applies the unit's changes to a copy of each record and runs the rules the integrator
will run, so a change the integrator would refuse is a lint problem the lane can still fix. A clean unit
becomes `ready`. A unit with problems becomes `invalid`. For an invalid unit, run
`scripts/rq brief RUN UID --fix` and start a lane on the printed line again. The new brief lists the
problems. ⚠ When it fails again (invalid a second time, or no receipt after a second start), the same lane is
unlikely to do better: start it once more on a stronger model, or with a narrower scope (`scripts/rq abandon` it and
plan a smaller unit with the same question). Give a unit up only when neither is possible:

```bash
scripts/rq abandon RUN UID --reason "the vendor page is behind a sign-up, and no other page states the quota"
```

`abandon` marks the unit `abandoned` and releases its lease; the run report and the pull request list it with the
reason. A unit that `brief --fix` reopened after its first integration keeps that integration: `abandon` gives up
the fix and sets the unit back to `integrated`, so its audit and the report count what its commit wrote. `abandon`
refuses a unit whose integrate attempt did not finish: run `scripts/rq integrate RUN` first, which settles it by its
commit. `land` refuses a run with a unit that is `planned`, `running`, `ready`, `invalid` or `lease-lost`, and a unit
whose ledger lines are on the run branch while it is not integrated, so every unit is integrated or abandoned and
every written value is audited. A question that still needs an answer goes into an `open_question` of another unit,
or into a new issue.

**Step 6. Integrate.**

```bash
scripts/rq integrate RUN
```

The integrator applies each ready unit in order, with one commit per unit on `rq/RUN`. It writes git objects and
moves the ref; it never touches the checkout's files. For every operation
it checks the scope and the lease fence, the capture and the quote, the narrative lint, the old value
(compare and set), the evidence rung against the record's rung, duplicates of existing records, the schema,
and the record's error rules against the baseline. A draft whose `tier` differs from that of a record of the
same provider, domain or page is a new record, not a duplicate: two materially different tiers are two records.
It writes a ledger line for every change, with the old value, and for every evidence row a `drop_evidence`
took out, with the row and the reason. What it cannot decide by a rule becomes a conflict in `conflicts.jsonl`.
Then it pushes `rq/RUN` to `origin` with no pull request, so the integrated work survives the loss of this clone (not with
`RQ_NO_GITHUB` or `RQ_NO_PUSH`, not to a local remote, and not while the branch is still at its base). A push that
fails for any reason but a moved branch (the network, the authentication) says so, and the branch is intact
locally; `RQ_NO_PUSH=1` goes on without it. `audit RUN --score` pushes it again.

When `integrate` reports rejected operations for a unit, run `scripts/rq brief RUN UID --fix`. It reopens
the unit with the rejection reasons in its brief. Give the printed line to the same lane when your tool can
continue one; it fixes its `changes.jsonl` in a minute. Then collect and integrate again. Operations that
were already written are idempotent: the same value is corroboration, not a second change.

**Step 7. Reconcile.** When `integrate` prints open conflicts:

```bash
scripts/rq plan RUN --conflicts
```

This makes one `reconcile` unit per record. Go back to step 4 for those units only, then steps 5 and 6. A
conflict counts as handled only when its reconcile unit exists: a `plan --conflicts` that stopped (main conflicts
with the run, a refused unit, a held lease) leaves the conflicts open, and the same command plans them after the
cause is fixed.
⛔ At most two reconcile rounds per run. The harness counts them. What is still open after the second
round goes to an `rq:followup` issue when the run merges (section 9).

**Step 8. Audit.** This is the second key.

```bash
scripts/rq audit RUN
```

This plans one auditor per integrated unit. Each auditor re-reads a random sample of up to 30 of that
unit's claims against the captures and the probe records (and up to three paths of each confirm). The sample size
is a design of the score, not a limit on reads: an auditor makes every read and every probe its claims need, and
`scripts/rq audit RUN --census` audits every claim and every confirmed path. Start the auditors with
`scripts/rq briefs RUN --kind audit`, as in step 4, then:

```bash
scripts/rq collect RUN
scripts/rq audit RUN --score
```

⛔ An auditor is another context than the lane it audits ([`../METHODOLOGY.md`](../METHODOLOGY.md) section 9.5).
When the parent did the lanes itself (step 4, a tool that cannot start subagents), it does not audit them: another
session or tool runs `scripts/rq briefs RUN --kind audit` and the auditors, and the run waits at the audit until
their receipts are in.

A unit fails its audit when more than 10% of its decided claims are unsupported. When the auditor read a
sample, not every claim, the unit also fails when the Wilson 95% upper bound on that rate is above 25%:
the bound speaks for the claims nobody read. ⚠ A unit whose auditor decided no claim (every claim
`cannot-tell`) is kept and reported as undecided; the follow-up issue lists it. The integrator undoes a failed
unit from its ledger lines
and queues a re-run of it. A value that a later unit changed is not undone; it goes to the follow-up
issue. Each unsupported claim of a kept unit becomes a conflict, so run step 7 again for it.

⚠ When an audit was planned wrong (the claims carry the wrong evidence, or a value the lane marked
`unverified`), do not score it. `scripts/rq audit RUN --replan` sets the unscored auditors aside and plans
new ones. ⛔ An audit unit is never abandoned (`scripts/rq abandon` refuses one): score it as it is, or plan it
afresh. `integrate`, `collect` and `audit` print `scripts/rq land` as the next step only when every integrated unit
has a scored audit or left no claim to audit; the report of a run that skipped the audit says `not audited:` and
names the units. A value is left out of the audit only when it starts with `unverified` (the brief's
`unverified: <the reason>`); a sentence that states a fact and calls one part of it unverified is audited. A unit
that wrote values and left no claim is listed as `no claim audited:`.

**Step 9. Land.**

```bash
scripts/rq check --prune --run RUN     # every time; it changes nothing when no baseline row is fixed
scripts/rq land RUN --meets N,N
```

Every run runs `scripts/rq check --prune --run RUN` before `land`: it checks the records the run changed (its net
change against `main`) on `rq/RUN`, and writes onto the run branch its baseline without the rows of those records
that they no longer break. It checks no other record, and it writes nothing when the run fixed no field with a row
in `scripts/research/baseline.tsv`. `audit --score` prints both commands. `scripts/rq check
--prune` alone is for an own clone, and the research checkout refuses it.

`--meets N,N` names the "Done when" lines of the claimed issue that this run meets: each N is the number of a
line, 1 for the first. `land` copies the issue's "Done when" lines into the pull request as a checklist, ticks
those lines, and writes "Part of #N". ⚠ A line that says a merge session ticks it (a tools pull request, "Every
topic of the list has a merged run") is never ticked by a run; `land` says so when `--meets` names it. The line
"CI's `gate` job is green on the pull request that carries the work to `main`", with nothing after it but what the
job runs and its comparison with `main`, is ticked by `land` itself, whether `--meets` names it or not: `rq merge`
merges only a head whose CI is green, so the merge makes it true. It is worded for both contributor paths on
purpose: a contributor with an account opens the pull request, and a contributor who sends a zip cannot, so the
maintainer opens it when the bundle is imported. The older wording, "green on the pull request", is still accepted
by `land` and `rq merge` for issues written before the change. A line that asks for more than that (no new baseline row, a repaired record
that leaves the baseline) is an ordinary line: name it in `--meets` when it holds, and the merge session checks the
tick. It comments
`rq landed: run RUN topic TOPIC, pull request URL` on the issue; the claim holds until a merge session merges or
closes the pull request (section 9). When the pull request is open already (a second `land` after a send-back),
`land` rewrites its body, so the checklist and the report are current, and labels it `rq:review` again in place of
`rq:changes`, which puts it back in the merge session's queue.

`land` first merges the current `origin/main` into the run branch in git objects (`git merge-tree`), because
other runs may have landed since this one started. It then renders the generated tables of the topics the run
touched, with the `render.py` of the tree it writes. Each `measured` or `documented` record the run added goes into
the block "Records that no other document names" of its topic README, which the gate's `links` check counts as a
citation. It checks every record the run touched (the schema and the error rules of that tree, and the captures),
commits the render and the run manifest (section 1) on the branch, pushes the branch and opens a pull request
labelled `rq:review`, which closes the run's issue when it merges. After the push it deletes the copies of captures
and probe records in the unit folders that the pushed branch holds.

⚠ `land` takes under a minute. It runs no gate: a push starts the heavy checks (the gate comparison, the render check,
the selftests, the parity check) on the pushed head in the Actions of the repository that
`scripts/research/settings.json` names (`ci_repo`, workflow `ci_workflow`), and `scripts/rq merge` runs the light
ones (the text of the commits and of the pull request, the baseline rows) and waits for the remote run. That log is
public, so it prints only check names and PASS or FAIL; `scripts/rq ci RUN` names a failed check, and a merge
session reads its detail with `scripts/rq gatecmp --base origin/main` in its own clone. A red CI comes back as `rq:changes`: fix the cause
on the run branch with a new unit, `scripts/rq put` or `scripts/rq resolve`, then run `land` again, which labels the
pull request `rq:review` again. A `land` that was killed runs again from the top: it moves the branch only at its
end. A run whose units changed nothing (every op rejected or in conflict) lands empty: no pull request, and the
claim goes back, also when a merge of `main` moved its branch.

When `main` moved and the merge conflicts only in generated blocks (two runs that added records to one topic both
rewrote its README block and the counts of `BRIEF.md`), `land` keeps main's side of those files and renders the
blocks again from the merged records; it prints the files. Any other conflict stops `land` with the files under
`.tmp/RUN/conflicts/` and the steps: write the merged file there, then `scripts/rq resolve RUN PATH` (or
`scripts/rq resolve RUN PATH --delete` when the resolution deletes the path), then `land` again (section 12).

⛔ **`land` does not merge, and the run stops here.** It does not run `rq merge` or release the leases; under
`.tmp/` it deletes only the copies of captures and probe records that the pushed branch holds. A merge session
reviews the pull request (`scripts/rq review RUN`), merges it (`scripts/rq merge RUN`), and wipes `.tmp/` at the end
of its pass. When the review asks for changes, the research session (this one or a later one) makes them on the
run branch and runs `land` again.

**Step 10. Report.**

```bash
scripts/rq report RUN
```

About ten lines: units, applied, confirmed, added, rejected, conflicts, audit scores, the main rejection
reasons. ⭐ This is the report to hand back. List a self-hosted option last, after every hosted offer,
never starred or ranked first, and never as the answer while a hosted offer (free, trial or paid) exists.
`scripts/rq policy` files the `rq:policy` issue of a warn rule that waits for a methodology decision: the rules in
`POLICY` of `scripts/research/checks.py`. While that list is empty, as it is now, skip it; otherwise run it when
`scripts/rq check --rev rq/RUN --rule RULE` lists a record the run changed for such a rule.

**Step 11. Continue.** ⛔ A run ends at its pull request; the session does not ([`../AGENTS.md`](../AGENTS.md)
section 4). Do not wait for the merge, and never merge. When the request names one issue, the session
ends at that issue's pull request. Before you take a new issue, take back your own pull requests labelled
`rq:changes`. Otherwise take a free issue at random from `scripts/rq issues` (for an
issue that is run once for each topic, a topic with no live claim) and open it as a new run from step 1, with
`--issue N`; when `open` says it is taken, take another. Pick an issue whose records do not overlap a run that waits for review: its leases stay until the
merge, and `plan` refuses a leased record. `scripts/rq queue` lists the open questions that lanes filed; an issue
names the ones it covers. The session ends when no issue is left that it can run, or when the session
is interrupted. When you end, run `scripts/rq folder session --end ID` (ID as `folder session` printed it, as
`session-<id>` or as the bare id), so a merge session's wipe does not wait for your folder.

---

## 4. The plan file

A plan file is a JSON list of unit specs, or an object with a `units` list.

```json
[
  {"kind": "discover", "question": "Which DNS hosts give a free zone with a write API, and what does each cost in identity?",
   "scope": {"new": {"slice": "free DNS hosting with an API, not registrars"}},
   "seeds": ["scripts/fr search \"dns api\""]},
  {"kind": "discover", "question": "Confirm or reject these named hosts as free DNS with an API.",
   "scope": {"new": {"names": ["Host A", "Host B"]}}},
  {"kind": "verify", "question": "Re-check these records against their sources; correct what changed.",
   "scope": {"rids": ["domains-dns/desec", "domains-dns/he-dns"]}}
]
```

`Host A` and `Host B` stand for the names your request gives. The rids of the third unit are real records;
`plan` refuses a rid with no record file.

| field | rule |
|---|---|
| `kind` | `discover`, `verify` or `reconcile`; `plan` refuses any other. `audit` units are made by `scripts/rq audit` only |
| `question` | one question. A unit that answers two questions is two units |
| `scope.rids` | the records the unit may change. Required for `verify` and `reconcile`. ⭐ Keep it to 8 or fewer |
| `scope.new` | for `discover`: `names` (a list of offers) or `slice` (a description). A discover unit adds records and changes none |
| `seeds` | URLs or `scripts/fr` queries to start from. Optional |
| `topic` | defaults to the run's topic. In a run that claimed an issue run once for each topic, only the run's topic |
| `queue_files` | optional: `["queue/ID.json", ...]`, the queue items this unit answers; the lane's brief lists each one's question, each leaves the queue when the unit integrates, and an audit that reverts the unit puts them back. Use it when a `discover` queue item asks about a record that exists, so a `verify` unit answers it |

`plan` ignores the capture-count field of an older plan file: no count of pages applies.

⭐ **Size the plan to the request.** One unit for each sub-question, provider class or group of names the request
holds, as many as it needs, all started at once. Split by sub-question, by provider class or by name list, never by
"half of the work". Two units must not need the same record;
`plan` refuses that, because leases are exclusive.

---

## 5. What the parent reads, and what it does not

| the parent reads | the parent does not read |
|---|---|
| the output of each `scripts/rq` command (tens of lines) | a lane's `log.md`, unless one unit needs a diagnosis |
| `scripts/rq status RUN` | a lane's chat answer beyond the receipt path |
| `scripts/rq report RUN` | the topic's documents end to end |
| `scripts/fr` query results | the run branch's diff, line by line |

The output is the same size for 3 units or 30. This is how a parent stays inside its context when many
lanes run. One exception: the first line of the `log.md` of a lane that diffed a registered list holds the
covered and missing counts that the parent records with `aggregator-diff.py` (section 2).

---

## 6. Parallel runs, leases and the broker

- **One checkout.** All research on the machine runs in the research checkout, with 30 or more agents at the same
  time ([`../AGENTS.md`](../AGENTS.md) section 2 rule 14). Each run has a folder `.tmp/<run>/` and a branch
  `rq/<run>` that exists only as a git ref. No run makes a worktree or copies the tree.
- **Leases.** A unit leases `rid:` keys for its records, and a name or slice key for its new offers, in
  `.tmp/rq/state.db`. A record that a run creates is leased to it too. Leases hold until the run's pull request is
  merged or closed: a landed run's leases do not expire while it waits for review. Two runs can go on at the same
  time when their scopes do not overlap. A lease carries a fence number; the integrator refuses a unit whose lease
  was taken again. A unit's lease that is not integrated yet expires after 24 hours (a lane that died frees its
  scope); once the unit is integrated, its lease is held until the run merges or closes, however long the run
  takes to land. A lane that works longer than 24 hours (HTTP 429 pauses) keeps its work: `integrate` lets the
  expired lease again to the same unit when no other run took a key of its scope since, and the compare and set of
  each `set` catches a record that changed meanwhile. When another run, or a unit of this run that is not
  integrated, took a key, the unit becomes `lease-lost` and `integrate` names each key and its holder (section 12).
- **Duplicates.** A draft for an offer the corpus already has becomes corroboration. A draft for an offer that
  another live run has created becomes a conflict, settled after that run merges. When another unit holds the
  record, the draft becomes a conflict, and the reconcile round settles it.
- **The store.** One store per commit of the research checkout, built once under a lock and read by every agent.
  It holds `main` as the checkout has it; read a record as your run holds it with `scripts/rq show RUN RID`.
- **The broker.** No client-side cap: no rate, no lane count, no limit on pages, no cache, no delay. Start every
  lane at once. When the broker answers 429 or 503 with `Retry-After`, `scripts/rq capture` prints `retry_after`
  and `retry_at` and exits 4: read other pages and read that one again after `retry_at`, or run the capture with
  `--wait`, which waits in the same command. When the broker gives no `Retry-After`, `capture` exits 4 and nothing
  is established about the target.
- **Branches.** The integrator writes one file per unit for the ledger and for relations, so two runs never edit
  the same ledger or relation file.
- **The drain.** When `scripts/rq open` says a merge session is draining `.tmp/`, open no run: finish and land
  the one you have, then stop. The merge session wipes `.tmp/` once every run has landed and merged.

---

## 7. Evidence: a capture and a quote

⛔ **Every new evidence row with an `http` URL carries `capture` and `quote`.** `capture`
is the sha256 of the page text. `quote` is the exact sentence from that text that proves the value.
Rule C21 fails the gate on a new row without them.

A lane captures a page with `scripts/rq capture --lane WS URL`, or registers a page its own tool fetched
with `--from-file`. The integrator copies each cited capture to `sources/c/<aa>/<hash>.md.gz`, with a
JSON sidecar, on the run branch. `scripts/fr amend`, `add` and `dead` take `--capture` and `--quote` for a
hand change in an own clone; in the research checkout they refuse ([`../AGENTS.md`](../AGENTS.md)
section 2 rule 14), and a hand change is an `amend` run. A session that wants a page before it opens a run
captures it into its own folder: `scripts/rq capture URL --lane .tmp/session-<id>`; it prints the hash.

⛔ **`measured` needs a stored probe record.** A lane runs a probe into its workspace (section 3, step 3) and
registers the record with `scripts/rq capture probe:TARGET --lane WS --probe FILE` (a JSON file must carry the keys
the probes write, or `probed_at`, and a record must name the target's host: section 3, step 3). The evidence row has the URL
`probe:TARGET`, the printed hash as `capture`, and a span of the record as `quote`. The integrator copies the
record to `sources/p/<aa>/<hash>.json.gz` with a sidecar, so the audit and a merge session read what the probe
saw. The lint and the integrator refuse a `measured` operation without such a row, and a `probe:` row without a
stored record. Rule C21 also fails the gate on a new `probe:` row with no capture.

**A wrong evidence row is dropped, and the unit that wrote it stays.** A row that belongs to another
offer or tier, or whose quote or `proved` names a private path such as `scripts/probe/probe.py` (the public
projection's leak scan refuses it), is taken out with a `drop_evidence` operation: `rid`, the row's `url` and
`capture` (none when the row has none), a `reason`, and `index` (the row's place in the record's evidence list,
counting from 0) when several rows share that url and capture. The ledger line keeps the row and the reason
(AGENTS.md section 2 rule 4), and an undo of the unit puts the row back. To restate a wrong row, the same unit
drops it and adds the right one (`append_evidence`, or the evidence of a `set` or `confirm`). The lint refuses a
drop of the last row that cites a page a field names as its `source_url` or `source`, unless the unit cites that
page again. The run report lists every dropped row with its reason, for the merge session.

⚠ **A lane cannot lower a record's rung.** A change at a weaker rung than the record's becomes a conflict. When
the evidence for a rung is gone, the lane files an `open_question`. Lowering a rung is a hand change: a session
in an own clone runs `scripts/fr amend RID PATH VALUE --rung RUNG`, in a separate pull
request.

The quote check accepts an exact match, an ordered fragment match, or a fuzzy match of 0.9 or more. Every
number in a proposed value must be in the quote or the capture, or in a `derived` line built from quoted
numbers.

---

## 8. Checks, the gate and the ratchet

`scripts/rq check` runs the contradiction and invariant rules C01 to C21 over `dossier/`. The full table,
with each rule's measured count, is in [`../scripts/research/README.md`](../scripts/research/README.md).

| severity | effect |
|---|---|
| error | the gate fails on a violation that is not in `scripts/research/baseline.tsv` |
| warn | counted; `scripts/rq policy` files one `rq:policy` issue per rule and topic |
| info | counted only |

The baseline holds the error violations that existed when the rule was adopted. It shrinks when a record is
fixed: in a run, `scripts/rq check --prune --run RUN` removes the rows of the records the run fixed, on the run
branch (step 9); in an own clone, `scripts/rq check --prune` does the same in the working tree. It grows only
when a rule is added or widened, in the pull request that changes the rule, with
`scripts/rq check --write-baseline`. ⛔ Never add a row to the baseline by hand, and never in the change that adds the violation: the gate reads the baseline of
the same tree, so a row added beside a new violation hides it.

Two checks hold this. `scripts/rq merge` and `scripts/rq ci --pr NUMBER --wait` refuse a pull request that adds
rows while it does not carry the label `rq:baseline` (`scripts/rq baseline-diff` prints the rows). A merge session
reads the rows (`git diff origin/main...HEAD -- scripts/research/baseline.tsv`), confirms that each one comes from
the rule change and not from a record the pull request adds or edits, and only then applies the label and runs the
check again. A research run never carries the label: `scripts/rq land` refuses a run branch that adds a
baseline row, because a run fixes its records and does not change rules.
The gate's `contradictions` check runs `scripts/rq check --gate`.

A rule's severity can depend on the topic: C01 is an error, C18 is an error for a plain
`qualifies`, and C03 is an error in `storage` and `netdisk-pan` and a warning in every other
topic. The ruling is recorded in
[`../history/2026-10-28T135534Z/operator-rulings-of-2026-10-28.md`](../history/2026-10-28T135534Z/operator-rulings-of-2026-10-28.md).
A new warn rule that waits for a decision goes into `POLICY` in
`scripts/research/checks.py`, and `scripts/rq policy` files its issue.

---

## 9. Issues: the parent's tracker

⭐ **The issues are the parent's tracker, and rulings are written into them** (`rq:decided`). They let
a parent in any session or tool find the state of a run without that run's conversation. ⭐ **The open issues
labelled `rq:research` are the work queue.**

⭐ **Who closes an `rq:research` issue.** The run's pull request says "Part of #N" and ticks the "Done when"
lines the run meets (`land --meets`). The merge session checks each tick against the merged run
(`scripts/rq review RUN`) before it merges. After the merge, `scripts/rq merge RUN` ends the run's claim with a
comment `rq merged: run RUN topic TOPIC ...`, which lists the lines left, and removes `rq:active` when no other claim
lives. It closes the issue when every line of the pull request is ticked; otherwise the issue stays open for the
next run. ⚠ A line that says a merge session ticks it is never ticked by a run. The merge session ticks it in the
pull request body before `scripts/rq merge` (`gh pr edit NUMBER --body-file FILE`, with `- [x]` on that line), or
closes the issue by hand after the merge (`gh issue close N --comment "..."`), and only when the line is true.
⛔ `scripts/rq merge` is the only thing that closes an `rq:research` issue. GitHub closes an issue that a pull request
body or a commit message on `main` names right after a closing keyword (close, closes, closed, fix, fixes, fixed,
resolve, resolves, resolved, with or without a colon), whatever `rq merge` decides. So no text that the harness
writes puts such a word right before an issue reference: `land`, `merge`, the claim, the comments, the follow-up
issue and every harness commit write "closes issue #N" for "closes #N", also in the text they copy from an issue or
a lane. The one exception is `Closes #N` of the run's own `rq:run` issue. Write none either in a `--reason`, a note
or a comment.

- An issue whose first piece of work is a tools change (#24, #35, #37) has a "Tool" line for the merged tools pull
  request, and a "Units run" line that stays open until a run that uses the merged tool has landed: the tools pull
  request alone never closes it. `scripts/rq issues` shows such an issue as "waits for a tool" until the script its
  Tool line names is on `main`, or until the merge session that merged the tools pull request comments
  `rq tool merged: PR-URL` on the issue. An issue whose request says its run does not wait for the tool is free as
  usual.
- An issue that is run once for each topic (#25, #36, #47, #49, #51, #54, #59) ends with the line "Every topic of
  the list has a merged run". Each merge of one topic's run comments the lines left and keeps the issue open. The
  merge session of the last topic's run ticks that line, and every line an earlier run met (the earlier merge
  comments name them), and then merges; or it closes the issue by hand.

A claim of a run that will not merge is given back: `scripts/rq cleanup RUN` after a pull request is closed without
a merge, and `scripts/rq release N --run RUN --reason "..."` for a session that died (without `--run`, every claim
of the issue). Both comment `rq released:` and remove `rq:active` when no other claim lives.

| label | one per | opened by |
|---|---|---|
| `rq:run` | run. Every phase adds a comment. The landing pull request closes it | `scripts/rq open` |
| `rq:review` | pull request of a run that waits for a merge session | `scripts/rq land` |
| `rq:followup` | merged run with work left: the questions it queued and the re-runs an audit queued, conflicts after two rounds, values an undo could not restore. It carries `rq:research` too and has the shape of a research issue, so a run claims it from the queue and its merge closes it. The values behind a sign-up go to the open `rq:operator` issue instead; a run that left nothing else gets no follow-up | `scripts/rq merge` |
| `rq:policy` | warn rule and topic | `scripts/rq policy` |
| `rq:changes` | pull request of a run whose review asked for changes | a merge session |
| `rq:research` | unit of research work that waits for a run: the request line, the evidence, the suggested units, "Done when". The work queue | a methodology session |
| `rq:decided` | `rq:research` or `rq:policy` issue that carries a ruling; the ruling is in a comment | the session that records the ruling |
| `rq:operator` | work that needs a person: an account, a purchase, a real send, a decision | a session that meets such a step |
| `rq:active` | `rq:research` issue with a live claim. `scripts/rq issues` says which topic is taken; a claim holds only its own topic | `scripts/rq open --issue N`; `scripts/rq merge`, `cleanup` and `release` remove it when no claim lives |
| `rq:baseline` | pull request whose added baseline rows a merge session reviewed (section 8) | a merge session |

Without `gh`, or with `RQ_NO_GITHUB=1`, the same text goes to `.tmp/<run>/issue.md`, and a claim is not written
(`open` and `release` say so). Nothing in the harness depends on GitHub, except `rq issues`, the claim and the
Done-when lines of `open --issue`, the guards that read them (the per-topic guard of `plan`, which refuses another
topic's bullets in an issue run once for each topic, and the check of `--meets` against the Done-when lines), the
pull request in `land` and the merge in `merge`; without `gh`, read the issue on the web and pass `--issue N`, and
plan only the bullets of the run's topic yourself. Without `gh`, `land` stops before the pull request: it writes the body it computed to
`.tmp/<run>/pr.md` and the title to `.tmp/<run>/pr-title.txt`, keeps the `--meets` lines in `run.json`, and prints
the commands to run. A research session does not open the pull request by hand (section 10).

---

## 10. Resuming a run

All state of a run is in `.tmp/<run>/` and in the ref `rq/<run>` of the research checkout: `run.json`, one
`unit.json` per unit, the lane workspaces, the leases, and the run branch. Two parts also live off this disk: the
branch `rq/<run>` on `origin`, pushed after each integrate and each audit score, and from `land` on, the run
manifest on that branch. ⚠ Until the first integrate, a lost research checkout loses the run; after it, the
integrated records survive on `origin`, and the lane workspaces and the audit state do not. A session that resumes
does this:

```bash
scripts/rq status RUN
```

`status` prints the run's phase and each unit's state. Continue from the first step whose work is not
done: `planned` units need lanes (step 4), `ready` units need `integrate`, an integrated run with no audit
needs step 8, and a run in phase `in-review` waits for a merge session: there is nothing for a research
session to do on it. A lane that died leaves no receipt; start it again with `scripts/rq brief RUN UID`. When
it dies a second time, start it on a stronger model or replan a narrower scope (step 5); when neither is possible,
or your tool cannot start more lanes, give the unit up with `scripts/rq abandon RUN UID --reason "..."`: `land`
accepts an abandoned unit and lists it with the reason. A run that `land` stopped before the pull request (no `gh`, or `RQ_NO_GITHUB`) stays in phase
`integrated`; the leases of its integrated units hold until it merges or closes. Tell the operator, who pushes the
branch when `land` said it is not on `origin` yet (`git push origin rq/RUN`) and opens the pull request:
`gh pr create --base main --head rq/RUN --label rq:review --title "$(cat .tmp/RUN/pr-title.txt)" --body-file
.tmp/RUN/pr.md`. Then `scripts/rq land RUN` run again with `gh` (it reuses the `--meets` lines that the first `land`
kept in `run.json`) finds the pull request open, rewrites its body and moves the run to `in-review`. A run in phase `in-review` whose pull request was closed without a merge is cleaned with
`scripts/rq cleanup RUN`, which also gives its issue back. A run whose session died with no pull request, or a run
left in phase `opening`, is closed with `scripts/rq close RUN --reason "..."`: it gives the claim back and keeps the
branch.

---

## 11. Where each file lives

| path | holds | committed |
|---|---|---|
| `scripts/rq`, `scripts/research/` | the harness, the lane and audit templates, the baseline | yes |
| `.tmp/<run>/` | `run.json`, `plan.json`, `conflicts.jsonl`, `issue.md`, `pr.md` and `pr-title.txt` (a `land` without `gh`), `lock`, and `units/<unit>/` | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/<run>/units/<unit>/` | `brief.md`, `captures/`, `probe/`, `changes.jsonl`, `new/`, `log.md`, `receipt.json`, `unit.json`, `tmp/` (the broker's temporary files); an auditor also `claims.json` and `verdicts.jsonl` | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/<run>/tools/` | the output of a tool the parent ran for a unit (section 3, step 3) | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/<run>/conflicts/` | `land`'s base, ours, theirs and marked text of a conflicted file, the parent's resolution, and `index.json` of recorded resolutions | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `refs/heads/rq/<run>` | the run branch, a git ref with no checkout | the branch is, through its pull request |
| `.tmp/session-<id>/` | one session: `RESUME.md`, `notes.md`, `captures/` (`scripts/rq folder session`) | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/review-<run>/` | a merge session's fresh captures for one run (`scripts/rq folder review RUN`) | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/rq/state.db` | leases, fence numbers, the folder registry, records a live run created, the drain and wipe rows, the local claims of issues, and the labels the repository is known to have | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/rq/locks/`, `.tmp/rq/pycache/` | the fetch lock, the claim lock of each issue and topic, and the bytecode of every harness process | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/rq/tmp/` | the temporary files of a `broker.sh` call made with no `TMPDIR` under `.tmp/` (a capture, and a lane's direct call with the brief's `TMPDIR={workspace}/tmp`, put them in the lane's `tmp/`), and of the commit-message check of `scripts/rq put` | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `.tmp/fshy/local-<HEAD>-s<F>.db` | the store of the research checkout's HEAD, built once and shared | no; deleted by `scripts/rq wipe` at the end of a merge pass |
| `sources/c/<aa>/<hash>.md.gz` | captures that integrated evidence cites, with a `.json` sidecar | yes |
| `sources/p/<aa>/<hash>.json.gz` | probe records that integrated `measured` evidence cites, with a `<hash>.json` sidecar | yes |
| `sources/p/<aa>/<hash>.txt.gz` | a body that `probe.py --save-body` saved and evidence quotes; its `<hash>.json` sidecar keeps the probe record's status, final URL, content type, byte count, digest and time (`measurement`) | yes |
| `history/ledger/<run>/<unit>.jsonl` | one line per change: old value, new value, evidence | yes |
| `history/ledger/<run>/manifest.json` | the run manifest: units and audit scores, the report, merged drafts, undos that could not restore a value, open conflicts. Written by `land` for the merge session | yes, on the run branch |
| `registry/relations.d/<run>-<unit>.tsv` | relations a unit added | yes |
| `queue/<id>.json` | open questions lanes filed, and re-runs of failed units | yes |

---

## 12. When something goes wrong

| symptom | cause | action |
|---|---|---|
| `plan` refuses a unit: scope held | another unit, maybe in another run, leases that record | change the scope, or wait for that run to land |
| `integrate` prints `integrated (its work lease had expired and was let again ...)` | the lane worked longer than `lease_hours`, and no other run took its scope | nothing: the lane's work is integrated |
| `integrate` reports a unit `lease lost: scope KEY is leased by run R unit U` | the unit's work lease expired, and then run R (or unit U of this run) leased that key | do not plan the unit again: its lane's work is kept. Run `scripts/rq integrate RUN` again when the holder lets go (run R merges or closes, or unit U is integrated or abandoned); `integrate` takes a `lease-lost` unit with no `collect` and lets its lease again. Integrate and audit the other units meanwhile. When the holder will not let go soon, `scripts/rq abandon RUN UID --reason "..."` and file the question for a later run |
| `collect` or `audit --score` says a lane file is not UTF-8 | a lane or an auditor wrote `changes.jsonl`, `receipt.json` or `verdicts.jsonl` through a code page (on Windows, `0x92` is cp1252's right quote) | the unit is `invalid`, and the score skips an audit unit; `scripts/rq brief RUN UID --fix` sends the problem back to the same lane or auditor, which writes the file again as UTF-8 |
| `capture` exits 4 | the broker refused, or answered with its own problem JSON (a `422 no-content` that it passes through as the origin's status) | with `retry_at`, read other pages and read again after it, or use `--wait`; with none, nothing is established about the target. On the broker's problem answer nothing is stored, and `capture` prints the next route: `--provider ID` with the provider ids the broker's status lists for `read`, `fetch URL --dump-headers` registered with `--from-file`, or `archive URL --at YYYY-MM` |
| `capture` prints `status=401`, `403` or `429` | the origin walled the read (an undeclared-tool page, a challenge); the answer is stored and `capture` exits 0 | a walled page, not a gone one: take the next route it prints, every provider pin and every rung, before the field becomes `unverified: URL answered HTTP N on DATE; routes tried: ...` (lane brief rule 4). A `404` or `410` is a gone page at once |
| `open` refuses: a merge session is draining `.tmp/` | a merge session waits for every run to land so it can wipe | open no run; finish yours |
| a command refuses: rq/RUN is locked by pid N | another command of this run is running | wait for it, or find it by the pid and command the message names |
| push rejected: the run branch moved on origin | a merge session updated `origin/rq/RUN` | run the command it names again; it merges the remote head in git objects |
| the push of rq/RUN failed (not a rejection) | `origin` is unreachable, or the credentials are refused | the branch is intact locally; go on with `RQ_NO_PUSH=1`, and a later `integrate`, `audit --score` or `land` pushes it |
| many units `invalid` | the lanes did not read the brief, or the model cannot follow it | read one `log.md` and the `--fix` brief. Use a stronger model for those lanes |
| CI is red on the run's head (`scripts/rq ci RUN`) | the run added an error violation, or broke a check that passed on the base | fix on the run branch with a new unit, `scripts/rq put` or `scripts/rq resolve`, then `land` again |
| `land` stops: a record it touched fails a local check | the run's change breaks the schema, an error rule, C21, the gate's binding check (a `measured` or `documented` record with no `binding`) or its selfhosted check (a record whose category or tooling says self-hosted with no `self_hosted`, or `self_hosted: true` with no text that says the user installs or runs it) | the message names the record and the rule. Fix it with a new unit, or `scripts/rq resolve` for a conflict file |
| `land` stops: units wrote records and are not integrated | an older harness abandoned a unit after its commit, or an integrate attempt was lost | run `scripts/rq integrate RUN`; for an abandoned unit, `scripts/rq abandon RUN UID --reason "..."` sets it back to `integrated`, and its audit follows |
| `land` or `merge` prints: the conflicts were only in generated blocks | `main` moved; another run added records to the same topic, so both rewrote its README block and the counts of `BRIEF.md` | nothing: `land` kept main's side of those files and rendered the blocks again from the merged records |
| `land` or `merge` merged `scripts/research/baseline.tsv` | `main` moved, and both sides removed baseline rows (another run's `--prune`) or main added rows for a widened rule | nothing: `land` merges the baseline as a set of rows, so a row either side removed is gone and a row main added stays |
| `land` or `merge` stops: main (or `origin/rq/RUN`) conflicts in files that are not only generated blocks | `main` moved, and a file outside the generated blocks changed on both sides (a record that another run changed, or a delete on one side); or a merge session's send-back on `origin/rq/RUN` changed a file this checkout changed too | the message names the files and the side merged in; `.tmp/RUN/conflicts/` holds the base, ours, theirs and the marked text, and `scripts/rq resolve` merges that same side again. Write the merged file into `.tmp/RUN/conflicts/PATH`: in a record, main's value of every field this run did not change, and this run's value with its evidence row where it did. Then `scripts/rq resolve RUN PATH` (or `--delete` when the resolution deletes the path), and run the same `land` or `merge` again |
| `land` was killed, or timed out | a tool stopped it after a fixed time | run it again; it changed nothing until its last step. A `land` killed after it opened the pull request left the run in its old phase: the next `land` finds the open pull request, rewrites its body and moves the run to review, and `rq close` refuses such a run |
| `land` stops: the pull request was not opened | `gh pr create` failed (the network, an expired `gh` login, the branch not on `origin`) | the run keeps its phase, its leases and its claim, and the body waits in `.tmp/RUN/pr.md`; run `land` again |
| a lane never returns a receipt | the lane died, or the tool cannot start it | start it once more (`scripts/rq brief RUN UID`); then `scripts/rq abandon RUN UID --reason "..."` |
| `scripts/rq issues` shows a claim that no session works on | the session died after `open --issue N` | `scripts/rq release N --run RUN --reason "..."`; a claim with no pull request also expires after `claim_hours` |
| `open --issue N` says the issue is taken | another run holds that topic: on GitHub, in this checkout, or a claim written at the same moment that GitHub lists first | take another free issue from `scripts/rq issues`; a run of this checkout whose session died is closed with `scripts/rq close RUN --reason "..."` |
| `open --issue N` says a claim write failed | `gh` failed on the comment or the label (a refused call, an expired login, the network); a 403 or 429 with `Retry-After` was waited out once already | `open` gave back what it wrote and closed the run; run `open` again, or take another issue |
| an audit undoes a unit | its claims did not hold against the captures | the re-run is queued. Plan it with `scripts/rq plan RUN --queue ID` in a later run |
| the research checkout is lost | its disk, its run folders and its leases are gone | a landed run is not affected: a merge session in any clone reviews and merges it from the manifest. An integrated, not landed run survives as `origin/rq/<run>`; open a new run, plan its units again, and take the records from that branch as corroboration |
| the broker is down | `capture` exits 4 for every read; `sh scripts/broker/broker.sh status --human` names it | lanes fetch with their own tool and register each page with `scripts/rq capture --lane WS --from-file FILE URL`; the quote check is the same. See [`maintenance.md`](maintenance.md), section "If a provider disappears" |

---

## 13. The merge session, in short

The whole procedure is `docs/merge-protocol.md` in `f-shy/fshy.ajam.dev`. These are its commands in this
repository, in the order of a merge pass, so a checkout of this repository alone can review and merge. ⛔ A session
that ran any unit of a run never merges that run.

```bash
# once per checkout
git config core.hooksPath .githooks          # every checkout
git config rq.researchCheckout true          # the research checkout only

# each run (in the research checkout, or in your own clone)
scripts/rq review                            # the pull requests labelled rq:review, with their run ids
scripts/rq review RUN                        # the report, merged drafts, new records of another tier, unrestored undos, open conflicts, re-checks
scripts/rq ci RUN                            # the remote checks of the head: green, or stop (--pr N for a pull request that is not a run)
scripts/rq folder review RUN                 # prints .tmp/review-RUN/
scripts/rq capture --lane .tmp/review-RUN --wait URL [--provider ID]  # each re-check line: read the page again, with the pin its via= names
scripts/rq capture --lane .tmp/review-RUN --check sha256:... "QUOTE"  # a probe: line: read the stored record
git diff --stat origin/main...origin/rq/RUN -- dossier
git diff origin/main...origin/rq/RUN -- scripts/research/baseline.tsv  # no added row for a run (rows --prune removed are expected)
gh pr edit NUMBER --body-file FILE           # tick a line no run may tick (section 9), only when it is true
scripts/rq merge RUN                         # update in git objects, the light checks, the remote CI, merge, follow-up, the claimed issue
scripts/rq merge RUN --pr NUMBER             # the same for a pull request from a fork, or one that carries the run (a number or a URL)
scripts/rq cleanup RUN                       # only after a close without a merge; gives the claimed issue back
scripts/rq close RUN --reason "..."          # a run whose session died, with no pull request
scripts/rq intake NUMBER                     # a public report becomes a pull request on intake/fshy-NUMBER

# after the merges, in your own clone at origin/main: the merge lines (section 9), then close the issues

# last, in the research checkout
scripts/rq wipe --dry-run                    # exit 1 when something blocks the wipe
scripts/rq wipe --drain                      # wipes now, or stops new runs until a later wipe can
scripts/rq sync                              # fast-forward, the new store, the index refresh
git worktree list                            # no line but the checkout's; remove any other as rq status names it
```

⛔ **A merge pass ends in the research checkout with `scripts/rq wipe` and then `scripts/rq sync`.** The wipe comes
after the merges and after the issues are closed. It refuses while a run is open, a lease is live, a session folder
is live, a merge is unfinished or a store build runs, and names each one; a session folder whose session died
stops it until `scripts/rq wipe --sessions-done`, which treats every session folder as ended and is given only when
no research session is running. Otherwise it deletes all of `.tmp/`.
Nothing in `.tmp/` is needed after the merges: records, ledgers, captures and manifests are on `main`, open items
are in issues, and the store is built again by `scripts/rq sync`. `sync` fast-forwards the research checkout to the
merged `main` whether the wipe ran or refused.

⛔ **After `sync`, no linked worktree is left: `git worktree list` prints one line, the research checkout.** A
second line is a full-tree copy that an agent made against rule 14, most often a subagent started with worktree
isolation under `.claude/worktrees/`, which `.gitignore` hides from the stray-file check. `scripts/rq status` names
each one with its branch ("worktree against rule 14: PATH [BRANCH]"). The wipe removes one under
`.claude/worktrees/` that has no change and whose tip a remote-tracking ref holds, and the old harness's ones; it
names every other one. Do not remove such a one with `git worktree remove PATH` before its commits are pushed or
judged dead; then delete its branch with `git branch -D BRANCH`.

`scripts/rq review RUN` lists, beside the drafts merged into existing records, the new records that share a domain
and a provider with a record of `main` of another tier, with both tier labels. The integrator keeps two tiers apart
as two offers and C04 does not pair them, so a draft of an existing offer under another label ("Hobby" for "free")
would land as a duplicate that no check names: check that each pair is two offers, and send a duplicate back as for
a failed check below (a comment that names both records, and `rq:changes`).

A re-check line of `scripts/rq review RUN` names how the lane read its capture (`via=broker read --provider
firecrawl`). Read the page again the same way, with the same `--provider`: an unpinned read of a page that walls
undeclared tools stores the wall, which supports nothing.

A merge line is a "Done when" line that ends "(A merge session ticks this line.)": a query that only `main` after
the merge can answer. Answer it in your own clone, after your merges and before the wipe: `git fetch origin main`
and `git merge --ff-only origin/main` on that clone's `main`, `scripts/fr verify` (that clone's store, built once),
the query of each merge line, a tick in the merged pull request body (`gh pr edit`), and the close of the issue by
hand, with a link to the pull request, when every line is ticked.

A pull request that is not a run holds `main` (its author merges `main` into the branch) and is merged after
`scripts/rq ci --pr NUMBER --wait` is green: the light checks, then the remote run on its head. Then
`gh pr merge NUMBER --merge --match-head-commit SHA --author-email ADDRESS`, where ADDRESS is the account's noreply
address, `gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'`: without `--author-email` gh authors the
merge commit with the account's primary address, which is private. One that adds baseline rows (a rule added or widened) fails
that check until a merge session reviews the rows and runs `gh pr edit NUMBER --add-label rq:baseline`.

When a check fails, comment on the pull request with the record and the field, and swap the label:
`gh pr edit NUMBER --remove-label rq:review --add-label rq:changes`. The research session fixes the branch and
runs `land` again, which puts `rq:review` back, so `scripts/rq review` lists the pull request again. `merge` runs the
light checks and waits for the remote run on the head it merges (it starts one when there is none), and merges only
that head (`gh pr merge --match-head-commit`), with the account's noreply address as the merge commit's author
(`--author-email`, from `gh api user`; when gh cannot say it, `merge` stops before it merges); a remote run that fails, is cancelled, skips a required job, or does not finish within 60
minutes stops the merge, and `scripts/rq merge RUN --no-ci` skips the remote CI (the light checks still run), only on purpose. The heavy checks run
in this repository's Actions and nowhere else; nothing on this machine runs the gate for a merge.

⭐ **A pull request from a fork.** A contributor's `land` pushes `rq/RUN` to the contributor's fork and opens the pull
request against this repository, so the pull request's head is the fork's commit and `origin/rq/RUN` does not exist.
Pass the number, `scripts/rq merge RUN --pr NUMBER`: `merge` reads the head from `refs/pull/NUMBER/head`, brings it
up to date with `main` in git objects and pushes the result to `rq/RUN` on `origin`, where the gate runs on that
exact commit. When the run is green it pushes the same commit, fast-forward only and never forced, to the fork's
head branch, so that the pull request's head is the commit the gate checked, and then merges with
`--match-head-commit`. A head that already holds `main` needs no push to the fork. The push needs "Allow edits by
maintainers" on the pull request. ⛔ When the contributor did not allow edits, or the fork refuses the push, `merge`
stops before it merges and says so: ask the contributor to allow edits, or to merge `main` into the branch, and run
`merge` again. After the merge `merge` deletes `rq/RUN` on `origin` and never the fork's branch.

⭐ **A run that another pull request carries.** Several runs may be combined in one pull request (a branch
`combine/...`), and a pull request may come from a branch that is not `rq/RUN`. The manifest then has no pull request
for the run, and `scripts/rq merge RUN` cannot find it. `scripts/rq merge RUN --pr NUMBER` (a number or a pull request
URL) makes that pull request the one that every lookup reads: its state, its body for the "Done when" ticks, its
comments and the `rq merged:` comment. When it is merged and `main` holds the run's manifest, `merge` runs the steps
after the merge: the follow-up issue, the claimed issue, the run's own `rq:run` issue (it closes it when it is still
open, because a carrying pull request does not say "Closes #N" for it), the leases and the comment. When it is open,
`merge` merges it as above, and the other runs it carries are finished with `scripts/rq merge RUN2 --pr NUMBER`, one
run at a time. A carrying pull request whose body ticks no per-issue line is fine: `merge` comments the lines left
on the claimed issue.
