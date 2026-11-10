# scripts

The repository's instrumentation. Every script here exists because a session
without it made a mistake that cost a wave.

A script in this directory has to clear a bar that a research document does not:
it must be **hermetic** (standard library only, no network except the thing it is
measuring, no dependency on this machine's state), **re-runnable** (the same
inputs produce the same decision, even if the numbers differ), and **honest when
it fails** (a non-zero exit and a sentence a reader can act on, never a silent
zero).

⭐ **This file describes the scripts that exist.** Anything named as planned is
marked planned, in its own section, with the reason it is not built. A catalogue
of intended tools is not a contract: the previous version of this file listed
six scripts that did not exist and called them the authority for rules in
`METHODOLOGY.md` and `docs/conventions/README.md`, so a session that followed the
documentation got `No such file or directory` and concluded the corpus was
incomplete rather than the catalogue.

## What exists

```text
scripts/
  README.md            this file: the contract for everything below
  SELFTEST.md          what was run, and what it proved
  gate.sh              the definition of done; twelve checks, exit 1 on a defect; CI runs it on every pushed head
  hygiene.py           refuse to commit scratch, secrets, build output, oversize captures
  linkcheck.py         every relative Markdown link in the tree resolves
  own-hardware.py      refuse a recommendation to acquire physical hardware
  self-hosted-last.py  refuse a list or a need that puts a self-hosted record above a hosted one, or recommends it
  check-readme-commands.sh   run every command this file documents, and fail on exit 2
  probe/
    probe.py           the core primitive: one HTTP request, one JSON evidence record
    tcpprobe.py        TCP connect and banner for a fixed endpoint list, one saved run per call
    cartcheck.py       does a WHMCS/Blesta cart price the plan? carries a cookie jar, so a live store is not called dead
  broker/
    broker.sh          thin wrappers over the web-access broker, so nobody hand-rolls a curl
  dossier/
    schema.json        the canonical record schema
    validate.py        schema check over dossier/
    staleness.py       what has rotted, by rung window, topic window and evidence age; --mark (own clone only) writes stale
    staleness.policy.json   the per-topic and per-rung windows, as data
    promote-records.py own clone only (the harness before scripts/rq): accept a lane's records into a topic, refusing duplicates
    merge-records.py   own clone only: collapse duplicate lane records, union their evidence, report every disagreement
    apply-decisions.py own clone only: write a reconciler's decisions into records, keeping the rejected value under extras
  sources/
    manifest.py        verify sources/MANIFEST.tsv against the files on disk
    aggregators.tsv    every source that lists other providers, with a cadence and a last-diff date
    aggregator-diff.py diff one source against dossier/, and fail the gate on an undiffed or overdue one
  report/
    render.py          the generated tables in docs/ and BRIEF.md, and --check
    compute-price.py   every paid compute figure in docs/compute/, from a published rate
    history-index.py   history/INDEX.md, generated from the entry headers
  discover/
    probe-alist.sh     probe a public AList instance for what it really allows
  fshy/                the derived store and the public projection (see fshy/README.md); the wiki is in f-shy/fshy.ajam.dev
    build.py           dossier/ to the store (.tmp/fshy/local-<HEAD 12>-s<F>.db, built once per commit by scripts/fr);
                       --public OUT the projection a publish exports; --check is the gate's projection check;
                       in the research checkout it refuses, so never run it by hand there
    fr.py              query and amend the corpus: search, filter, need, sql, amend, add, dead, relate, mcp
    check_lock_fresh.py  fails when fshy/public.lock is behind a public change of the Worker's rules; needs the network, so CI runs it (--selftest is offline; docs/maintenance.md)
    rules/             projection.json (what the public build strips, and why) and needs.json (best-per-need queries)
  fr                   wrapper: `scripts/fr <command>`
  research/            the research harness (see research/README.md and docs/research-protocol.md)
    rq.py              open, issues, release, abandon, context, plan, briefs, brief, capture, show, put, resolve,
                       folder, lint, collect, integrate, audit, check, policy, import-bundle, land, report,
                       status, queue, close;
                       in CI or an own clone: gatecmp, baseline-diff;
                       for a merge session: review, ci, merge, cleanup, intake, publish-status, wipe, sync
    checks.py          the contradiction rules C01 to C21, with baseline.tsv as the ratchet
    test_rq.py         the harness selftest, in a throwaway clone with no network
  rq                   wrapper: `scripts/rq <command>`; without sh, `python scripts/research/rq.py <command>`
  fixtures/            one deliberately broken case per gate check
```

Every script listed above exists. That claim is not a reading of the tree: it is
the recorded exit code of each command in §Running them, executed from the
repository root with `scripts/check-readme-commands.sh scripts/README.md`, in CI or an
own clone (it runs every documented command, so it refuses in the research checkout,
AGENTS.md section 2 rule 14). Run it again; a date written here would only say when
somebody last did.

## Planned, and why each is not built

| script | what it would do | why it is not built |
|---|---|---|
| `probe/probe-bench.py` | parallel ranged GETs with a baseline, the only honest throughput number | **Not needed.** `probe.py --shard-bytes N --concurrency N` already does exactly this, with `--no-baseline` to skip the single-connection run. It was planned before that flag existed. Use `probe.py`. |
| `dossier/index.py` | rebuild `dossier/_index.generated.tsv` from the records | **Superseded by `fshy/build.py`**, which builds a SQLite store into `.tmp/fshy/` and never commits it, so no second committed copy of the record set exists. See [`../history/2026-10-27T073916Z/a-derived-store-is-built-and-never-committed.md`](../history/2026-10-27T073916Z/a-derived-store-is-built-and-never-committed.md). |
| `sources/refresh.sh` | re-capture the pages we cite, append-only | The capture path is `scripts/rq capture URL --lane .tmp/session-<id>` (a session folder, `scripts/rq folder session`), and the run that cites it copies it into `sources/c/`. A refresher has to decide *which* records still need a capture and *when* re-capturing changes a verdict; that policy does not exist yet, and a refresher without it is a cron job that rewrites evidence. |
| `discover/discover.sh` | topic-agnostic discovery: run a query set, emit candidates | The discovery loop that ran the seed used a per-topic query set that was never generalised. `broker.sh search` plus a hand-written query list is how the work is actually done. |
| `lib/common.sh` | shared shell helpers: logging, exit codes, temp dirs | Two shell scripts exist. A shared library for two callers is a dependency with no second user; the gate script and `broker.sh` each carry their own five-line `record`/`die` helpers. |

A planned script is not an authority. No rule in `METHODOLOGY.md` or
`docs/conventions/README.md` may cite one of these as the thing that enforces it
until it exists.

## The exit-code contract

Every script in this directory follows the same mapping, because the gate that CI
runs and future automation branch on it:

| code | meaning |
|---|---|
| `0` | success, and the thing it checked passed |
| `1` | a check ran and found a defect; the defect is the output |
| `2` | usage error: bad arguments, missing file, unreadable input |
| `3` | the environment is wrong: a required tool is absent, a network is down |
| `4` | the remote said no: a 429, a 503, a challenge page. Retryable, or wait |
| `64` and up | reserved; do not use |

`1` and `3` are the pair that matters. A script that returns `3` because the
broker is rate-limiting has told the caller nothing about the corpus, and a
script that returns `1` in that situation has lied.

⚠ **Exit 2 is not a passing grade.** A command that exits 2 because it rejected
its own arguments has verified nothing. That is why every command in this file
carries its measured exit code: a documented command with no recorded exit code
is a command nobody ran.

## The rules

1. **Never trust HTTP 200.** A `probe.py` record with `status: 200` and a
   challenge signature is a failure, and the tool says so. Dead hosts return 200
   with an HTML error page, a zero length, or a 106-byte JSON 401 body.
2. **Hash every download.** A byte-identical readback is the only proof that a
   write worked. `sha256` is a field on every probe record, not an option.
3. **Measure a baseline.** A throughput number without a single-stream baseline
   cannot distinguish "the host is slow" from "the host collapses under
   concurrency", and those imply opposite decisions.
4. **Mint a URL per connection.** Parallel GETs against one presigned URL measure
   the signature, not the host.
5. **Timestamp everything in UTC, with milliseconds and `Z`.** A local-time
   timestamp in an evidence record is unusable by anybody else.
6. **Be idempotent.** A re-run that changes nothing must write nothing.
   `render.py` reports the change exactly once and a second run is a no-op.
7. **Never write outside `.tmp/`, `sources/`, `dossier/` or a generated file.**
   A script that edits a hand-written document is a bug: documents are written by
   people, the tables inside them are generated between markers. In the research
   checkout (`git config rq.researchCheckout` is `true`), a script writes only
   under `.tmp/`: the tree changes only through `scripts/rq` on a run branch, and a
   script that would write the tree refuses (exit 2): `render.py`, `aggregator-diff.py`,
   `history-index.py`, `recheck.py` and the `promote`, `merge` and `apply` scripts of
   `dossier/`, which belong to a session in an own clone.
8. **React to the server, and invent no cap.** A 429 or 503 with `Retry-After` is
   read again after that time. A refusal is about the tool, never a finding about
   the target (exit 4). A script carries no rate, concurrency cap, page limit or
   delay of its own; a wait that a measurement needs (a read-back after an upload)
   is part of the measurement and says so.
9. **Say what it could not do.** A check that examined zero rows must not report
   success. `hygiene.py` exits 2 and says "the staged set is empty, so this
   examined nothing" rather than printing `0 path(s), 0 problem(s)`.

## Running them

Every command below was executed from the repository root on 2026-10-22 and
carries its real exit code. `--selftest` exits 0 when every planted defect is
caught and every clean fixture accepted. `scripts/check-readme-commands.sh` runs
every line of the block below and records the exit codes in a folder of its own,
`.tmp/readme-check-<UTC>-<pid>/exitcodes.txt`, where `DIR` also points; exit 2 is
reported as a defect, because a command that rejected its own arguments has verified
nothing. It runs in CI or an own clone, never in the research checkout.

```bash
# the gate runs in CI (this repository's Actions) on every pushed head, or in an own clone; never in the research checkout
sh scripts/gate.sh --root .                          # 0, or 1 while staleness is red (BRIEF.md section 5); CI or an own clone
sh scripts/gate.sh --selftest                        # 0: 15 cases; CI or an own clone
sh scripts/gate.sh --root . --check units,links      # 0 when both pass; CI or an own clone
sh scripts/gate.sh --root . --json                   # 0, or 1 while staleness is red; valid JSON either way; CI or an own clone
sh scripts/gate.sh --root . --strict                 # 0, or 1 while staleness is red; a SKIP becomes a FAIL; CI or an own clone

# The annotation is the exit code this tree produces, and check-readme-commands.sh
# fails a line that exits with any other code. A clock-dependent line names both.

python scripts/probe/probe.py --selftest             # 0: 33 cases, no network
python scripts/probe/probe.py URL                    # 0 usable, 1 not, 4 retryable
python scripts/probe/probe.py --url URL --out DIR    # same, and writes the record
python scripts/probe/probe.py URL --shard-bytes 1048576 --concurrency 4
#   a sharded benchmark reads only the first N bytes, so `usable` is false and the
#   exit is 1 by design: the record carries the throughput, not a whole-object read.
#   Read `runs[].status`: 206 on every shard means the ranges were honoured; 416
#   means the object is smaller than N and the shard size is wrong for that URL.

python scripts/dossier/validate.py --selftest        # 0: 20 cases

# cartcheck carries a cookie jar, because WHMCS and Blesta refuse to resolve a
# product group without a session. A cookieless read of VolpaByte or AlphaVPS
# answers "Could not load any product groups" and looks like a dead vendor; the
# same URL with a jar warmed from the homepage prints every billing cycle.
#   python scripts/probe/cartcheck.py CART_URL       # 0 priced, 1 not priced
#   python scripts/probe/cartcheck.py CART_URL --json
# No command here, because it needs the network and this block is executed.
python scripts/dossier/validate.py --schema scripts/dossier/schema.json dossier/   # 0: every record valid
python scripts/dossier/staleness.py dossier/ --summary          # 0, or 1 while something is stale
python scripts/dossier/staleness.py dossier/ --stale-only       # 0, or 1: the rows that are
python scripts/dossier/staleness.py --selftest                  # 0: 27 cases
python scripts/dossier/staleness.py --fixtures scripts/fixtures/staleness   # 0

python scripts/report/render.py                      # 0: rewrite every block
python scripts/report/render.py --check              # 0 agree, 1 disagree
python scripts/report/render.py --selftest           # 0: 8 cases
python scripts/report/compute-price.py               # 0: the paid table and the Modal derivation
python scripts/report/compute-price.py --modal       # 0: the Modal arithmetic alone

python scripts/probe/tcpprobe.py --out DIR           # 0 all answered, 1 a timeout or no banner
python scripts/probe/tcpprobe.py --endpoint example.com:80 --out DIR   # 0, or 1: no banner on a port that waits

python scripts/sources/manifest.py --verify          # 0 clean, 1 a file with no row or a wrong hash
python scripts/sources/manifest.py --selftest        # 0
python scripts/sources/aggregator-diff.py --check    # 0: every registered source is diffed and fresh
python scripts/sources/aggregator-diff.py --selftest # 0: 3 checked, extraction, diff and round trip
python scripts/hygiene.py                            # 0 clean, 1 problem, 2 nothing staged
python scripts/hygiene.py --walk                     # 0 clean, 1 problem
python scripts/hygiene.py --selftest                 # 0

sh scripts/broker/broker.sh status --human           # 0, 3 unreachable, 4 refused
sh scripts/broker/broker.sh read URL                 # 0, 1 origin said no, 4 broker said no
bash scripts/discover/probe-alist.sh --help            # 0
```

⚠ **`validate.py` needs `--schema`.** The documented form in earlier revisions of
`dossier/README.md` was `validate.py dossier/`, which exits 2. The schema is a
file next to the validator; name it. The gate script, which CI runs, needs `--root` for
the same reason: run with no argument, it exits 2 and says so.

## False positives that were fixed, and how

A gate that is red for reasons a reader can disprove is worse than no gate,
because it teaches the reader to ignore red. Three checks were fixed on
2026-10-22, and each is recorded here because the failure mode is worth
recognising again.

| check | the defect that was there | what it looked like | how it is fixed |
|---|---|---|---|
| `units` | The exemption regex understood `(2026-10-21)` and `read 2026-10-21` but not the corpus's own citation form. | `1024 GB free ('Network disk capacity limited to 1024GB') (documented, 2026-10-21.)` reported as a defect | the regex now matches `(documented, 2026-10-21.)` and the other four rung labels |
| `links` | The slug extractor required a hyphen, so `serv00`, `apify` and 687 others were orphans by construction. | `uncited-verified-record` on a record a document named verbatim | `[a-z0-9]+(?:-[a-z0-9]+)*` — the hyphen is optional |
| `links` | **The classification step read its slug list through a heredoc, which owns stdin, so it read zero slugs and passed every time.** | `PASS links` on a tree with 118 uncited verified records | the slugs go in on a file descriptor the heredoc does not claim |

⚠ **The third one is the reason to keep this section.** A check that passes
without examining anything is indistinguishable from a check that examined
everything and found nothing, and it reported green for the whole build until a
reviewer read the source. When a check has an internal pipeline, test it against a
fixture it must **fail**.

## The checks the gate runs, and the ones it does not

`gate.sh` (in CI, or in an own clone) runs exactly twelve: `schema`, `staleness`, `binding`, `links`,
`attribution`, `units`, `tree`, `rellinks`, `sources`, `projection`, `selfhosted` and
`contradictions` (which runs `scripts/rq check --gate`). `projection`
builds the public store with `fshy/build.py --check`: every source value must get
exactly one disposition and the leak scan must find no operator host, personal
detail, process narrative or terms text. `selfhosted` runs `self-hosted-last.py`
on that store, on every list in `docs/` whose rows it can tie to records (a record path, a
backticked slug, or a provider name), and on the records: a self-hosted record
(`self_hosted: true`) comes after every hosted one and is never recommended, a record whose
category or tooling says self-hosted carries the marker, and a marked record says why (its text, or a
ledger entry with a source other than an inherited catalogue card). Anything else named in
`docs/conventions/README.md` §9, such as `markers` and `render`, is not run by the gate. `render.py --check`
runs in CI as a step of its own. `manifest.py --verify` exists and works; it is run by hand and by
`scripts/check-readme-commands.sh`.

⭐ **`check-readme-commands.sh` is the meta-check**: it extracts every command from
this README and the repository's documents and runs them, so a documented
invocation that no longer works is caught rather than discovered by a reader.

## Adding a script

A new script is accepted when it answers: **which mistake does this prevent, and
what did that mistake cost last time?** If the answer is "it saves typing", it
belongs in your own `.tmp/<id>/` folder, which the merge session's wipe deletes.
Every script carries a header comment naming
that mistake, its exit codes, and one invocation that demonstrates it working,
and a `--selftest` that plants each defect it claims to catch.

⛔ **A `--selftest` case that passes because a fixture failed to copy is not a
pass.** Assert the fixture landed, then assert which check fired and that it said
`FAIL`. A skip scored as a catch is worse than no selftest, and that is exactly
the bug that case 2 of the gate's selftest (which CI runs) had.

`tools/` is the companion directory for anything that must be **compiled** — a
binary whose speed or portability justifies a build step. Nothing in `scripts/`
may require a compiler, and nothing in `tools/` may require a runtime the
operator's machine does not already have.

Run this file's own commands, which is the only proof that it describes the tree:

```bash
sh scripts/check-readme-commands.sh scripts/README.md
```
