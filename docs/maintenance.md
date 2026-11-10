# Repository maintenance

What a session does when it is not researching: keeping the instrumentation and
the corpus's own consistency from rotting. ⛔ It works in its own clone, never in the
research checkout, where all research runs ([`../AGENTS.md`](../AGENTS.md) section 2
rule 14).

## The weekly five minutes

```bash
# in CI (this repository's Actions, on every pushed head), or in an own clone; never in the research checkout
sh scripts/gate.sh --root .                 # CI or an own clone: definition of done; exit 0 or a named defect
python scripts/report/render.py --check     # do the documents still agree with the records
python scripts/sources/manifest.py --verify sources/
python scripts/hygiene.py --root . --all    # nothing staged that must never be committed
python scripts/report/history-index.py --check
scripts/rq review                           # pull requests that wait for a merge
scripts/rq publish-status                   # merged research with no publish yet, and queued public reports
gh run list --repo f-shy/fshy.ajam.dev --workflow f-research-ci.yml --event schedule --limit 8  # a week of the daily lock-fresh check and the Monday backup
```

Each one answers a different question, and a green `gate.sh` does not imply the
others are green:

| command | refuses |
|---|---|
| `gate.sh` (CI in this repository's Actions, or an own clone) | a schema defect, a stale record, an uncited verified record, a missing document, an AI attribution, a decimal unit where a binary one belongs |
| `render.py --check` | a table in `docs/` that disagrees with the records it is a view of |
| `manifest.py --verify` | a `sources/` capture whose hash or size no longer matches its manifest row, or a file with no row |
| `hygiene.py` | scratch, a credential, build output, a vendored `.git` or an oversize capture heading for a commit |
| `history-index.py --check` | an entry whose six-line header is incomplete, or an index that has drifted |
| `rq review` | nothing; it lists the pull requests labelled `rq:review`. One older than a week is stalled |
| `rq publish-status` | nothing; it names the publish lag and each public issue labelled `queued`, and says which can close |
| `gh run list --repo f-shy/fshy.ajam.dev --workflow f-research-ci.yml --event schedule` | nothing; a red Monday run (job `backup`) means no backup of this repository this week: the workflow `f-research-ci` of `f-shy/fshy.ajam.dev` writes a git bundle of every branch and tag to the private R2 bucket every Monday, under `f-research/`. The bucket, its rules and the restore are in `docs/backup.md` of that repository. A red daily run (job `lock-fresh`) means `scripts/fshy/public.lock` is behind a change of the public Worker's rules, or that the check could not ask. See "When `lock-fresh` is red". The log prints only PASS or FAIL lines |

## When the gate is red

Read the check name, not the count.

1. **`schema`** — a record does not match `scripts/dossier/schema.json`. Run
   `python scripts/dossier/validate.py --schema scripts/dossier/schema.json dossier/<topic>/`
   to see the field and the reason.
2. **`staleness`** — a record is past its class or topic window. The message
   separates three different things and they need different fixes: `stale` means
   the evidence is genuinely old and somebody must re-verify; `bulk` means
   `verified_at` was moved without new evidence, which is a lie to correct at
   source, not a date to nudge; `undated` means the sentinel was used honestly and
   the record needs a real probe.
3. **`binding`** — a `measured` or `documented` record names no binding
   constraint. Read the record and name which of the seven decides its verdict.
4. **`links`** — either a document named in `docs/README.md` is missing, or a
   `measured`/`documented` record is cited by no document. The second is the one
   that matters: an uncited verified claim has no reader to correct it.
5. **`attribution`** — a trailer or a credit line that names a tool as the author
   of this repository's text. If the match is a sentence about a vendor's product,
   rewrite it so the fact stays. A banned marketing word or an own-hardware
   recommendation is removed.
6. **`units`** — a decimal unit where a binary one belongs, or a local-time
   timestamp. Note the advisory count separately: those are vendor quotes in
   decimal, which the conventions explicitly protect.
7. **`projection`**: the public projection lost a value's disposition, or the
   leak scan found a private host, a personal detail, a description of a person,
   process narrative or terms text in the public store.
   The line names the table, the record and the text. Fix the source with
   `scripts/fr amend`, or add a rule to `scripts/fshy/rules/projection.json` with
   a case in `scripts/fshy/test_projection.py`.
8. **`selfhosted`**: a list in `docs/` names a self-hosted record above a hosted
   one, or a self-hosted row says best, recommended or carries a star; or a need
   lists a self-hosted row above a hosted one; a sentence recommends a self-hosted
   record without saying so; a record whose category or tooling says it is
   self-hosted lacks the marker; or a marked record gives no reason (fix it with
   `scripts/fr amend` and a vendor page). A row is tied to records by a record path,
   a backticked slug of the document's topic, or a provider name (whole, cut short,
   or with more words after it) whose records are all hosted or all self-hosted. Move the row to the bottom of
   its list, label it `(self-hosted)` and drop the recommendation. A generated table is fixed by
   `python scripts/report/render.py`. Run
   `python scripts/self-hosted-last.py --root .` for the line.
9. **`contradictions`**: a record has a new error violation (C01 to C21). Run
   `scripts/rq check` for the rule and the record. Never add a baseline row by
   hand.
10. **Exit 3**: no Python 3.9 or later was found. Install it, or set `PYTHON`.
   A gate that skipped the Python checks would prove nothing, so it stops.

⚠ `staleness` depends on the clock: a clean tree turns red as records age. The
test of a change is CI's `scripts/rq gatecmp --base origin/main`, which fails only on
a check that passes on `main`, or on a skipped check.

## When `lock-fresh` is red

`lock-fresh` is not a check of `gate.sh`, which CI runs offline; `lock-fresh` needs the network. The script
`scripts/fshy/check_lock_fresh.py` is its check, and the job `lock-fresh` of the workflow `f-research-ci` in
`f-shy/fshy.ajam.dev` runs it on `main` every day at 06:40 UTC and on a manual run
(`gh workflow run f-research-ci.yml --repo f-shy/fshy.ajam.dev -f mode=lock`). A pull request that moves the pin
runs it inside the `gate` job of this repository's workflow (`scripts/research/ci-checks.sh linux`); a clone that
moves the pin runs `sh scripts/research/ci-checks.sh lock` itself. It is a network check, not a heavy one. The `parity` job does not run it. The pin exists so that a merge in the public repository cannot turn an
unrelated pull request here red, and every research pull request waits for every check.

**What it checks.** `public.lock` pins a commit of `f-shy/fshy.ajam.dev`, and the twins `fr.py` and `build.py`
are tested against that commit. The check asks the GitHub API for the newest commit of the public default branch
that changed each of `site/worker/guard.js`, `site/worker/rank.js`, `site/worker/text.js` and
`site/worker/test/parity.json`. It then asks the compare endpoint whether the pin contains that commit, so ancestry
decides and the date does not. It passes when the pin is that commit or ahead of it.

Run it by hand with `python scripts/fshy/check_lock_fresh.py`, and read the exit code unpiped.

| exit | the first line says | what it means | what to do |
|---|---|---|---|
| 0 | `fresh` | the pin contains the newest public change of every watched file | nothing |
| 1 | `STALE` | the pin is behind a public change of a watched file, or diverged from it. The check names the file and the public commit | change the twins and move the pin in one pull request, as below |
| 2 | `CANNOT DECIDE` | the network or the API failed, the rate limit is spent, or the lock is unreadable. This is not a stale pin | run the job again. A spent rate limit clears within the hour. If it keeps failing, run the check by hand |

⚠ **Do not move the pin only to turn the check green.** A commit that does not hold the rule makes the twins
give the old answers against the new Worker, and `parity` still passes on the old fixture.

To fix a stale pin, follow the order in "Parity with the public Worker" of `scripts/fshy/README.md`.

1. Read the public commit the check names, and the public pull request that merged it.
2. Check out the public commit to pin. Prefer the merge commit of that pull request.
3. Set `FSHY_PUBLIC` to that checkout, put the commit in `scripts/fshy/public.lock`, and run
   `python scripts/fshy/test_fr.py`. Change `fr.py` or `build.py` until every parity case passes.
4. Open one pull request with the changed twins and the moved pin together. The check prints a `sed` command that
   writes the head of the public default branch. Use it when that head is the commit to pin.

A public change that does not alter a rule still needs the pin to move. The parity test then shows that the twins
did not need a change.

## Monthly

- **Re-probe the inference endpoints.** They rot in days. Once
  `scripts/probe/inference-sweep.py` exists, its loop is weekly, as
  [`expansion/free-inference.md`](expansion/free-inference.md) says; until then, a
  `verify` run on `inference` with `--from-worklist stale` is the monthly step.
- **Run the netdisk sweep.** 7.4% monthly turnover. See
  [`netdisk-pan/auto-discovery.md`](netdisk-pan/auto-discovery.md).
- **Check the sources refresh.** A cited page that has changed is the most common
  way this corpus rots, and the manifest is how it is caught.

## Quarterly

- **Re-price the cheap-paid lane.** A price is the field most likely to move
  without an announcement.
- **Re-run the compute census.** Free tiers change a quarter at a time.
- **Read the history index.** Twenty entries is a pattern; if the same class of
  correction keeps appearing, the methodology is missing a rule, and the fix
  belongs in `METHODOLOGY.md`, not in another correction.

## If a provider disappears

Each row is one thing this repository depends on and that one holder can lose. ⚠ None has a second.
The rulings are on issue #48.

| what | who holds it | what stops without it | what still works | recovery |
|---|---|---|---|---|
| the maintainer's GitHub account | one holder, alone. It merges every pull request and holds the only `gh` token | push, pull requests, merges, issues, CI, the public repository | everything local: `sh scripts/gate.sh` in a local clone, `scripts/fr`, a research run up to `land` with `RQ_NO_GITHUB=1` (it stops before the pull request; issue text goes to `.tmp/<run>/issue.md`, the pull request's body to `.tmp/<run>/pr.md`) | restore the account, or push both repositories to another host from any clone (`git push --mirror NEWREMOTE`); every clone holds the full history |
| GitHub Actions of `f-shy/raw` | GitHub | the gate on each pushed head; `scripts/rq merge` stops when that run fails, skips a required job, or does not finish within 60 minutes | the same gate in a local clone: `sh scripts/gate.sh --root . --strict` and `scripts/rq gatecmp --base origin/main` | merge with `scripts/rq merge RUN --no-ci` (the light checks still run) only after the local gate is green, and say so in a pull request comment |
| the page broker, `*.web.pkgforge.dev` and `api.gh.pkgforge.dev` | one zone. There is no client-side cap. When it is saturated it answers 429 or 503 with `Retry-After`, and `scripts/rq capture` prints when to read again | `scripts/rq capture` and `scripts/broker/broker.sh` exit 4 | a fetch with another tool is registered: `scripts/rq capture --lane WS --from-file FILE URL`. The quote check is the same | `sh scripts/broker/broker.sh status --human`; point `BROKER_READ`, `BROKER_FETCH`, `BROKER_SEARCH`, `BROKER_ARCHIVE`, `BROKER_CRAWL`, `BROKER_RESEARCH` and `BROKER_GH` at another broker |
| the research machine and its `.tmp/` | the research checkout | run folders `.tmp/<run>/`, leases, session folders, the shared store; `scripts/rq wipe` deletes them at the end of each merge pass | a landed run: a merge session in any clone reads its manifest. An integrated run: its branch is on `origin` | make a new research checkout (a clone, with `git config rq.researchCheckout true`); plan the lost work again. Evidence that records cited under `.tmp/` and that still existed on 2026-10-28 is in `sources/p/` by content hash (issue #48); the 33 paths that were already lost, and the records whose claims must be re-measured, are issue #51 |
| Cloudflare, the public host | one Cloudflare account (public repository) | the public site, API and MCP | the published corpus is `data/` in git, and its build runs anywhere: `python publish/build.py --site site/dist` in a clone of the public repository, then `node site/worker/test/smoke.mjs` serves it on workerd | the deploy is not written yet (public issue #8 decided GitHub Actions, a `production` environment and an R2 bucket for the database files); until it is, there is nothing deployed to recover. When it is written, its recovery is the deploy workflow run against another account's token |

## Adding a check

A new check is accepted when it answers: **which published claim would be wrong
and stay wrong without it?** If the answer is "it is nice to know", it belongs in
a report, not in the gate. A gate that fires on things a reader can disprove
teaches a maintainer to stop running the gate, and then the corpus has no gate.

Every check needs a fixture it passes and a fixture it fails. A check that has
never failed has never been tested.
