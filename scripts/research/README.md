# scripts/research: the research harness

`scripts/rq` is a set of plain commands for research with many lanes and one writer. It calls no model.
The procedure a parent agent follows is [`../../docs/research-protocol.md`](../../docs/research-protocol.md);
this file is the reference for the code: the commands, the rules, the files and the tests.

Python 3.9 or later, standard library only. `git` 2.43 or later is required (`merge-tree --write-tree -X no-renames`). `gh` is
optional: without it, issue text goes to `.tmp/<run>/issue.md` and `land` stops before the pull request. The
wrapper `scripts/rq` needs `sh`; without it, run `python scripts/research/rq.py` with the same arguments (the usual
entry on Windows).

⛔ **One working tree** ([`../../AGENTS.md`](../../AGENTS.md) section 2 rule 14). Every research agent on the
machine works in the research checkout (`git config rq.researchCheckout true`). The harness makes no git worktree,
clone or copy of the tree, and never changes the checkout's branch, index, tracked files or git configuration: a
run branch `rq/<run>` exists only as git objects and a ref, written with plumbing (`common.TreeView`, `Overlay`,
`commit_on`), and every git command goes through `common.git()`, which refuses anything outside an allowlist. Every
file an agent makes is under `.tmp/<id>/`. Only the merge session's `scripts/rq sync` moves the checkout's HEAD.

| variable | effect |
|---|---|
| `RQ_NO_GITHUB=1` | no `gh` call and no push to a network `origin`; issue text goes to the run folder, `land` writes the pull request's body to `.tmp/<run>/pr.md` and its title to `.tmp/<run>/pr-title.txt` and prints the operator's commands, and no claim is written |
| `RQ_NO_PUSH=1` | `integrate` and `audit --score` do not push the run branch |
| `RQ_BASH` | the bash that runs `broker.sh`, and the gate script in CI or an own clone. On Windows the default is the bash of Git for Windows, never the WSL launcher in System32 |
| `PYTHON` | the interpreter `scripts/rq`, `scripts/fr`, `broker.sh` and the gate script (in CI or an own clone) use; default the first of `python3` and `python` that runs. `capture` passes its own, so `broker.sh` starts no Python to find one |
| `BROKER_WAIT=1` | `broker.sh` waits for a broker 429 or 503 with `Retry-After` and repeats only the `curl` call; `scripts/rq capture --wait` sets it |
| `RQ_SELFTEST`, `RQ_TEST_NOW`, `RQ_TEST_STOP_AFTER` | the selftest only: test refs, a moved clock, a kill at a named point |

## The commands

| command | does | prints |
|---|---|---|
| `scripts/rq issues` | every open `rq:research` issue (up to 200) with its claim: free, taken by a run, or landed and waiting for a merge session; for an issue that is run once for each topic, the topics that are taken; last, one free issue picked at random, which a parent takes rather than the first. Needs `gh` | one line per issue |
| `scripts/rq folder session [--end ID] [--take ID] [--list]` | makes and registers your session folder `.tmp/session-<id>/` (for `RESUME.md`, notes and captures); `--end` marks it ended, `--list` shows each as live, idle or ended, `--take` lets a resuming session take one. `scripts/rq folder review RUN` is a merge session's `.tmp/review-RUN/` | the folder |
| `scripts/rq open KIND TOPIC "DETAILS" [--issue N]` | opens a run: the ref `rq/RUN` at `origin/main`, the folder `.tmp/RUN/` with `run.json`, and an `rq:run` issue. Refuses while a merge session drains `.tmp/`, and when HEAD is not in `origin/main`. The id is `YYYYMMDD-HHMM-KIND-TOPIC-<4 hex>`. `--issue N` first claims `rq:research` issue N for TOPIC (label `rq:active` and a comment `rq claim: run RUN topic TOPIC ...`), and refuses an issue that another run of the same topic holds | the run id, and the claim |
| `scripts/rq release N [--run RUN] --reason "..."` | gives back the claim of RUN on issue N (without `--run`, every claim): a comment `rq released:`, and `rq:active` comes off when no claim lives. For a session that died | one line |
| `scripts/rq context TOPIC` | counts, worklists, sources and the open queue of a topic, from the store | about 15 lines |
| `scripts/rq plan RUN --file PLAN.json` | units from a plan file: leases, workspaces, briefs. Unit kinds `discover`, `verify`, `reconcile`; a rid with no record is refused | one line per unit, and refusals |
| `scripts/rq plan RUN --from-worklist stale\|inherited\|unparsed\|held\|drift` | verify units from a store worklist | one line per unit |
| `scripts/rq plan RUN --conflicts` | one reconcile unit per record with open conflicts; counts a round | one line per unit |
| `scripts/rq plan RUN --queue ID ...` | units from `queue/<id>.json` items; items of one call that share a record become one unit; each item leaves the queue when its unit integrates | one line per unit |
| `scripts/rq briefs RUN` | the one-line instruction for each unit that needs a lane | `uid<TAB>instruction` |
| `scripts/rq brief RUN UID [--fix]` | rewrites one brief; `--fix` adds the unit's lint problems (also to an invalid audit unit's brief, such as a `verdicts.jsonl` that is not UTF-8), and reopens an integrated unit whose operations were rejected | the instruction |
| `scripts/rq capture --lane WS URL [--wait] [--provider ID]` | reads a page through the broker, with no client-side cap and no cache; `--provider` pins the read to one provider (the ladder's rung 2). On a broker 429 or 503 with `Retry-After` it prints `retry_after` and `retry_at` and exits 4 at once; `--wait` waits and repeats only the `curl` call. `--from-file` registers a page fetched by another tool, with the location in a `cf-ray` or `cf-placement` header replaced by `[redacted]`. Exits 0 whenever it stored the page, whatever the origin answered (`status=` in the printed line says what: a 404 or a 403 is stored and is a finding). Refuses a lane folder that does not exist | `sha256:... path status=N` |
| `scripts/rq capture --lane WS probe:TARGET --probe FILE` | registers a probe record for a `measured` claim: the JSON of `scripts/probe/*.py`, another JSON file with `probed_at`, or a text or TSV file; each must name the target's host when the target has one. The integrator copies it to `sources/p/` | `sha256:... path` |
| `scripts/rq capture --lane WS --check SHA "QUOTE"` | is the quote in that capture; with a merge session's `.tmp/review-RUN`, it also reads the run branch (`origin/rq/RUN` in a clone that did not run it) | `exact`, `fragments`, `fuzzy` or `miss` |
| `scripts/rq show RUN RID`, `scripts/rq show REF PATH [--out FILE]`, `scripts/rq show RUN --capture SHA` | read-only (RUN may be `rq/RUN`; this clone's branch, else `origin/rq/RUN`, else any commit): a record as the run branch holds it now, the bytes of a file of any commit (`--out` writes them itself, so a shell cannot change the line ends, and writes `FILE.base` beside them with the commit and the blob it read, for `put`; in the research checkout `--out` writes only under `.tmp/<id>/`), or the text of a capture | the text |
| `scripts/rq put RUN PATH FILE --reason "..."` | a parent's file under `scripts/sources/` (a registry diff) onto the run branch, as one commit; refuses a carriage return in a file whose base has none, and a file whose `FILE.base` (written by `show --out`) names a blob the path no longer has on `rq/RUN`, or that has no `FILE.base` for a path the branch has: a compare-and-set on the content it read | one line |
| `scripts/rq resolve RUN PATH [--delete]` | records the parent's resolution of a path `land` left in conflict (`.tmp/RUN/conflicts/PATH`), or a deletion; refuses a conflict marker, a record that does not validate, or a new error violation | one line |
| `scripts/rq lint RUN UID` | the lane-side lint of one unit (a lane runs it before its receipt) | problems |
| `scripts/rq abandon RUN UID --reason "..."` | gives up a unit no lane can answer: status `abandoned`, its lease released; `land` accepts it, and the report and the pull request list it with the reason | one line |
| `scripts/rq collect RUN` | reads receipts, lints every unit, marks `ready` or `invalid` | one line per unit |
| `scripts/rq integrate RUN` | the single writer: applies ready units on branch `rq/RUN` in git objects (one commit per unit, compare-and-set on the ref), then pushes the branch to a network `origin` (no pull request, no force) | tallies per unit, open conflicts |
| `scripts/rq audit RUN [--per-unit N \| --census]` / `--score` / `--replan` | plans auditors (a sample of 30 claims per unit, a design of the score and not a limit on reads; `--census` audits every claim and every confirmed path) / scores them, undoes failed units and turns a kept unit's unsupported claims into conflicts / sets unscored auditors aside and plans new ones | one line per auditor / scores |
| `scripts/rq check [--rev REV] [--gate] [--rule R]`, `scripts/rq check --prune --run RUN` | the contradiction rules over `dossier/`; `--rev` reads the records of a commit or a run branch from git into memory; `--prune --run RUN` reads `rq/RUN` itself, under the run lock, and writes onto it the run branch's baseline without the rows its own records no longer break (a `--rev` must name `rq/RUN`; no `--repo`). `--prune` alone, and `--write-baseline`, are for an own clone | counts per rule; `--gate` exits 1 on a new error |
| `scripts/rq policy` | one `rq:policy` issue per warn rule and topic | issue numbers |
| `scripts/rq gatecmp --base REF` | CI (this repository's Actions) and an own clone, never the research checkout: the gate on this tree against the gate on REF, whose tree is extracted with `git archive` into `.tmp/gate-<sha>/`; a skipped check is never green | green or the checks that are not |
| `scripts/rq baseline-diff --base REF [--labels JSON]` | the rows a pull request adds to `baseline.tsv`; fails without the label `rq:baseline` (`rq merge` and `rq ci --wait` make the same check in-process) | the added rows |
| `scripts/rq ci RUN` / `scripts/rq ci --pr N [--wait]` | any session: the remote CI of a run's pushed head (or of a pull request that is not a run and holds main) against the main it holds, in this repository's Actions; a run when there is none. `--wait` makes the checks `rq merge` makes: the light ones in-process, then the wait for a run whose jobs `gate`, `harness-windows` and `parity` all succeeded | the head and base, the run's state and the failed checks by name |
| `scripts/rq land RUN [--meets N,N]` | the run's last step, under a minute: merge main into the branch in git objects (`merge-tree`; a conflict only in generated blocks keeps main's side and renders again; any other conflict stops with the files under `.tmp/RUN/conflicts/` and the `rq resolve` steps), render the tables of the touched topics with the tree's own `render.py` (a new `measured` or `documented` record goes into the "Records that no other document names" block of its topic README), check the touched records, commit the render and the run manifest `history/ledger/RUN/manifest.json`, push without force, open the pull request labelled `rq:review` or rewrite its body, and delete the unit folders' copies of captures the branch now holds. It runs no gate: the push starts the remote CI on that head (the gate comparison, the render check, the selftests, the parity check); a fork's push starts nothing, so `land` dispatches a run there. With a claimed issue, the body says "Part of #N" and ticks the "Done when" lines `--meets` names (each N the number of a line; a line a merge session ticks is never ticked). Refuses a unit that is not integrated or abandoned. A killed `land` runs again from the top. The run stops there; the session takes the next issue, unless the operator's prompt named one issue | the report and the PR URL |
| `scripts/rq review [RUN]` | merge session, in any clone: the runs waiting for review, or one run's report, merged drafts, the new records that share a domain and provider with a record of `main` of another tier (both tier labels: check each is a different offer), unrestored undos, open conflicts and claims to re-check (from the run folder, else from the manifest on the branch) | lines to read |
| `scripts/rq merge RUN [--no-ci] [--pr NUMBER\|URL]` | merge session, in any clone, with no worktree. `--pr` names the pull request that carries the run when it is not the run's own (several runs combined in one, a branch that is not `rq/RUN`, or a fork's pull request, whose `rq/RUN` is not on origin): every lookup reads it; merged, `merge` finishes the steps after the merge, and the run's own `rq:run` issue closes when it is still open; open, `merge` merges it. A pull request from a fork gets the gated head pushed to its branch, fast-forward only, after the push to `rq/RUN` on origin (the gate runs there); that needs "Allow edits by maintainers", and without it `merge` stops before the merge. The same update in git objects and render when main moved, the light checks (the commit hook on every commit and on the pull request's text, the baseline rows), the remote CI on that head against the main it holds (a run whose required jobs did not all succeed is a stop; `--no-ci` skips only that wait), `gh pr merge --match-head-commit` with `--author-email` set to the account's noreply address (`ID+LOGIN@users.noreply.github.com`, asked once from `gh api user`; without an answer it stops before the merge, because gh otherwise authors the merge commit with the account's primary address, which is private), the follow-up issue, the claimed issue (the claim ends with an `rq merged:` comment that lists the lines left; the issue closes when every "Done when" line is ticked; `rq:active` comes off when no other claim lives), the leases, the refs, the public issues the run answers, and last the comment `rq merged:` on the pull request. A merge killed after `gh pr merge` resumes there | the PR URL |
| `scripts/rq cleanup RUN` | merge session, only after a merge or a close: the run's leases and local ref, phase `closed`; after a close without a merge it also releases the claimed issue. The run folder stays until the wipe | one line |
| `scripts/rq close RUN --reason "..."` | a run whose session died with no pull request, or one left in phase `opening` (a legacy run too): releases its leases and claim, keeps its branch, sets phase `closed`, says whether the branch was pushed | one line |
| `scripts/rq wipe [--dry-run] [--drain \| --undrain] [--sessions-done]` | merge session, the last step of a merge pass in the research checkout: deletes all of `.tmp/` when no run is open, no lease is live, no session folder is live, no merge is unfinished and no store build runs; otherwise refuses and names each one (exit 1; `--dry-run` exits 1 too when something blocks). A run whose pull request is open or merged blocks or counts as merged whatever its phase. It deletes the local and the remote-tracking refs of the done runs, removes the old harness's worktrees and a subagent's worktree under `.claude/worktrees/` that has no change and whose tip a remote-tracking ref holds, and names every other linked worktree with the commands that remove it. `--drain` stops new runs until a wipe can complete; `--undrain` lifts that; `--sessions-done` treats every session folder as ended, only when the operator says no research session runs | what it deleted, or what blocks |
| `scripts/rq sync [--repair]` | merge session, after the wipe (or a wipe that refused): fast-forwards the research checkout to `origin/main`, builds its store once, deletes other commits' stores, deletes the local `intake/fshy-N` branches whose tip `main` holds, refreshes the index, and runs `git maintenance run --auto` only when no run is open (it packs refs, which takes each run ref's lock for a moment). Refuses another branch, a tracked change, HEAD ahead of `origin/main`, or an untracked file on a path the fast-forward writes (named); a fast-forward that stops prints git's own message | the old and new HEAD |
| `scripts/rq intake N` | merge session, in either checkout: issue N of the public repository becomes `queue/intake-fshy-N.json` on a branch `intake/fshy-N` from `origin/main`, written in git objects with no file in the working tree, pushed, with its pull request. The report is quoted as data; the slice is fixed text; links to public hosts become leads, never seeds. Refuses a second intake, a body whose form headings are wrong, and reports a failed comment or label | the branch and the pull request |
| `scripts/rq publish-status` | merge session: the commits of `origin/main` no publish carries yet, and where each public issue labelled `queued` stands | lines to read |
| `scripts/rq report RUN` | the run in about ten lines (from the manifest in a clone that did not run it) | the report |
| `scripts/rq status [RUN]` | all runs, or the units of one; with no run, a health line of the research checkout (HEAD and how far behind `origin/main`, tracked files that differ, untracked files outside `.tmp/`, the linked worktrees, each named as one against rule 14, a ref that shadows `origin/main` or `main`, open runs, leases, session folders, a drain, the store) | states |
| `scripts/rq queue [--topic T]` | the open questions lanes filed | one line per item |

Exit codes follow [`../README.md`](../README.md): 0 done, 1 a defect or a refusal, 2 usage, 3 environment,
4 a tool refused (read again after `retry_at` when one is printed; nothing is established about the target).

## The modules

| file | owns |
|---|---|
| `rq.py` | the command line |
| `common.py` | paths, JSON helpers, the git allowlist, `TreeView`, `Overlay`, the object writer and `commit_on`, the file locks, the joined fetch, the quote matcher, the number check, captures under `sources/c/` and probe records under `sources/p/`, the bash to run |
| `settings.json` | the values the modules share: the remote and the base branch, the GitHub repository, the public repository, the capture cutover dates (pages and probe records), the lease hours, the claim hours |
| `state.py` | `.tmp/rq/state.db`: leases with fence numbers (work, which expires after the lease hours; held, for an integrated unit; review, for a landed run; held and review last until the merge or the close), the folder registry, the records a live run created, the drain and wipe rows, the local claims of issues (a second claim of one topic of one issue in this checkout is refused), and the labels the repository is known to have (listed once per checkout) |
| `units.py` | runs, units, plans, briefs, lint, collect, status, session folders, and the store queries behind `context` |
| `capture.py` | page captures and probe records by content hash, broker refusals and `Retry-After` |
| `wipe.py` | `rq wipe`: the merge session's deletion of `.tmp/` |
| `integrate.py` | the single writer, the per-unit ledger, dedupe, conflicts, reconcile specs, undo |
| `checks.py` | the rules below, and the baseline |
| `audit.py` | auditor planning, scoring with the Wilson bound, the undo and the re-run |
| `land.py` | `land` without a worktree (merge-tree, the render of the touched topics, the local checks), `put`, `resolve`, `close`, `sync`, the gate comparison (CI and an own clone), the run manifest, the pull request, the merge, the follow-up issue, the run report |
| `review.py` | what a merge session reads (`review`), public reports into the queue (`intake`), and `publish-status` |
| `track.py` | GitHub issues as the parent's tracker, with a local fallback; the labels, listed once per checkout; the claim of an `rq:research` issue (the claim lock of the issue and topic, every write checked and undone on a failure, the read-back that gives way to a claim GitHub lists first); a 403 or 429 with `Retry-After` waited out once; the push of a run branch |
| `templates/lane.md`, `templates/audit.md` | the lane and auditor briefs: the whole contract a lane gets |
| `baseline.tsv` | the error violations that existed when each rule was adopted |
| `eol.py` | keeps each file's line endings as they are at HEAD; new files are LF |
| `test_rq.py` | the selftest |

## The rules

Counts measured on 2026-10-29 at the commit this table was last changed in. They rot: `scripts/rq check` prints
the counts of today. A rule fires only on stated values: a defaulted placeholder is not a claim, so it never
makes a contradiction.

| rule | severity | name | fires when | count |
|---|---|---|---|---|
| C01 | error | qualifies-no-free-tier | a qualifying verdict while the record's own free tier says there is none | 184 |
| C03 | error in `storage` and `netdisk-pan`, warn elsewhere | qualifies-no-probe | verdict `qualifies` with no probe evidence | 167 (58 errors) |
| C04 | warn | duplicate-disagreement | two records of one topic, domain and name disagree on verdict or a stated identity; two records whose `tier` differs are two offers and never a pair | 191 |
| C07 | error | unit-system | `free_tier.unit` names one unit system and the stated text uses only the other | 314 |
| C09 | error | binding-not-in-limits | `binding` names a kind that no `limits[]` row has | 37 |
| C10 | error | evidence-after-verified | an evidence row is dated after `verified_at` | 28 |
| C14 | warn | source-not-in-evidence | `free_tier.source_url` is not among the evidence URLs | 189 |
| C15 | error | price-no-iso-currency | a price with a number and no ISO 4217 code | 113 |
| C16 | info | provenance-flags | evidence with a synthetic date or a placeholder probe | 993 |
| C17 | warn | fails-egress-not-assessed | verdict `fails-egress` while egress was never assessed | 68 |
| C18 | error | qualifies-gated-identity | verdict `qualifies` behind an institution, a national ID or a country phone | 16 |
| C19 | error | measured-no-probe | `confidence: measured` with no probe | 14 |
| C20 | error | narrative-in-field | process narrative or personal wording in a record field, by the public projection rules of class `narrative` or `personal`; a rule of class `pointer` (a path of a private file, such as a stored copy in `sources/p/`) is withheld from the public build and not counted | 18,614 |
| C21 | error | evidence-needs-capture | an `http` evidence row dated 2026-10-28 or later, or a `probe:` row dated 2026-10-30 or later, without a capture that holds its quote | 0 |

⭐ **Errors ratchet.** The gate (`contradictions`, through `scripts/rq check --gate`) fails only on an error
violation that is not in `baseline.tsv`. C20 is keyed per field leaf and value, so an edit that keeps an
old narrative leaf does not fail, and an edit that writes a new one does. `scripts/rq check --prune --run RUN`
drops the rows of the records a run fixed, on its branch (`scripts/rq check --prune` in an own clone). ⛔ Never add a row by hand. A row is added only by `scripts/rq check --write-baseline`
in the pull request that adds or widens a rule; the light checks of `scripts/rq merge` and `scripts/rq ci --pr N --wait` refuse such a pull request until
a merge session reviews the rows and applies the label `rq:baseline`, and `scripts/rq land` refuses a run that
adds one ([`../../docs/research-protocol.md`](../../docs/research-protocol.md) section 8).

C01, C03 and C18 were policy rules, and the operator decided them on 2026-10-28
([`../../history/2026-10-28T135534Z/operator-rulings-of-2026-10-28.md`](../../history/2026-10-28T135534Z/operator-rulings-of-2026-10-28.md)).
A severity can depend on the topic (`checks.severity`): C03 is an error in `storage` and `netdisk-pan` only.
A warn rule that waits for a decision is listed in `POLICY`, and `scripts/rq policy` files one issue for it.

## What the integrator decides, in order

1. The unit's lint: scope, schema of each operation, capture present (a page for an `http` row, a probe
   record for a `probe:` row), quote found, `measured` only with a probe record, the `paths` of a `confirm`,
   numbers in the source, narrative lint on every proposed value, then the record rules on a copy of each
   record with the unit's changes applied (the same rules as step 5, so the lane sees them first).
2. The lease: the unit still holds its fence number. A work lease that expired while the lane worked is let
   again to the unit when no other holder took a key since; otherwise the unit is `lease-lost`, the message names
   each key and its holder, and a later `integrate` takes the unit again once the holder lets go.
3. For `set`: the same value is corroboration (the evidence is added). A placeholder is replaced. Otherwise
   the lane's `old` must equal the current value (compare and set), the rung must not be weaker than the
   record's, and evidence older than the record's newest at the same rung is a conflict. For `drop_evidence`:
   the one row with the op's `url` and `capture` (no capture when the row has none) leaves the record; when
   several rows match, the op's `index`, the row's place in the record as the unit found it, must name one of
   them. The lint refuses a drop with no `reason`, of a row the record does not hold, and of the last row that
   cites a page a field names as its `source_url` or `source`. To restate a wrong row, a unit drops it and adds
   the right one (`append_evidence`, or the evidence of a `set` or `confirm`).
4. For `add_record`: a draft whose slug, or domain and near name, or a deep evidence URL on the vendor's own
   domain matches an existing record is corroboration when verdict and identity agree, and a conflict when
   they do not. A forum thread or a list page cited by many vendors is never a match. A draft and a record
   whose `tier` values differ are two offers (the schema's `tier`: two materially different tiers are two
   records), so neither the name nor a shared page makes them one; the same slug always does. Tiers compare
   casefolded, with punctuation and the words tier and plan left out, and a placeholder or a status as a tier
   (`none`, `n/a`, `unknown`, `dead`, `closed`) is no tier: a side without one keeps the name and page matches. A
   record another unit holds, or one another live run created (`pending_new` in `.tmp/rq/state.db`, which keeps
   its tier), is a conflict.
5. Each touched record is validated against the schema and checked against the error rules and the
   baseline. A record that would add a violation, or that a dropped row would leave with a field's source
   page uncited, is written back as it was, and its operations are rejected.
6. One ledger line per change, with the old value, in `history/ledger/<run>/<unit>.jsonl`; a `drop_evidence`
   line holds the dropped row verbatim, its place and the reason, so the history keeps every row a run took
   out. One commit per unit.

The undo after a failed audit reads those ledger lines newest first. It restores a value only where the
record still holds what the unit wrote, removes only the evidence rows the unit added, and puts each row the
unit dropped back in its place unless the record holds it again. A dropped row is no claim, so no auditor
reads it: the run report, and so the pull request and `scripts/rq review`, lists each one with its reason for
the merge session.

## Tests

```bash
python scripts/research/test_rq.py
```

It clones the repository into a temporary folder, copies the working scripts in, and runs open, plan,
briefs, lint, collect, integrate, check, audit and the undo, with no network and no GitHub. It prints one PASS
or FAIL per case, and `--only CASE,CASE` runs some of them. `RQ_TEST_KEEP=1` keeps the folder. It is test
scaffolding: CI runs it when the harness changes, and an own clone runs it there; never the research checkout.

The cases of the one-tree design: the primitives (`TreeView`, the object writer, `commit_on`, line endings), the
overlay, the git allowlist, the store lock, the run lock and the joined fetch, no client-side cap (a fake broker
that answers 429 with `Retry-After`), review leases, crash windows, the wipe, the sync, the research-checkout
refusals, `land` on a moved main, the rule text of the documents, and `relet_case` (an expired work lease let
again, a key that another run took named, lane files that are not UTF-8). The load test, `one_tree_load_case`, opens
three runs in one checkout, starts 30 lanes at once, integrates, audits, lands and syncs, and asserts that the
checkout's HEAD, index, configuration and tracked files did not change, that every git process was in the
allowlist, and that the run stayed inside its budgets: 300 s for the whole phase, 60 s for each `land`, 90 s for
each `integrate` of 10 units, 10 MB written under `.tmp/` and 10 MB of growth of `.git/`. The job
`harness-windows` of the workflow `gate` in `f-shy/raw` (`sh scripts/research/ci-checks.sh
windows BASE`) runs the Windows-specific cases and the load test on Windows when the harness changes (a change of
`scripts/research/baseline.tsv` alone is data, not a harness change). Its log is public, so it prints one line per
case, `PASS harness-windows.CASE` or `FAIL harness-windows.CASE`; the detail and the timings stay in the job's
private log file.

### CI: this repository's Actions, and the light checks here

`scripts/research/ci.py` reads the run of `f-shy/raw`'s workflow `gate` on one head (`settings.json` `ci_repo`,
`ci_workflow`), found by its head commit. The workflow runs on a push by a collaborator and on a manual dispatch, and
on nothing else: a pull request opened by anyone outside the team starts nothing. A push starts the run on the head
it pushed; a dispatch names the branch (`--ref`) and the base (`-f base=...`), which `rq land` and `rq merge` use for
a head that is not a push. The workflow runs
`scripts/research/ci-checks.sh` (`linux`: the gate comparison, the render check, the selftests, the harness selftest
when the harness changed; `windows`: the Windows cases; `parity`: fr's twin of the Worker). The script writes each
check's output to a file on the runner and prints only `PASS NAME`, `FAIL NAME` or `SKIP NAME`, and for the gate
`NAME base X head Y`: a public log carries no record, quote or path. `rq land` notes the run a push started; `rq ci
RUN` shows it; `rq merge` runs the light checks (`ci.light`: the commit hook on each commit and on the pull request's
text, the baseline rows and the `rq:baseline` label) and waits for the run (`ci.wait`), and merges only a head whose
run has every job of `ci_jobs` green (a skipped job is not green). `--no-ci` skips only that wait.
`rq ci --pr N --wait` does the same for a pull request that is not a run, once it holds main. A failed check is
named, never shown: its detail comes from `scripts/rq gatecmp --base origin/main` in an own clone.
