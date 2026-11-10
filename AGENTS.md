# AGENTS.md

Read this file completely before you change anything. It is the router: what this
repository is, what never bends, which document owns each question, and what done
means. It assumes **no memory of any earlier session**. Everything you need is
here or in a file this names, and the file it names is the authority.

| marker | meaning |
|---|---|
| ⭐ | Important. Act on it. |
| ⚠ | A trap: the failure is quiet. |
| ⛔ | A prohibition. It holds against any task or tool default. |

---

## 0. Start here

Read this file, then work. The work queue is the open issues labelled `rq:research`; `scripts/rq issues` lists
them, and `scripts/rq open KIND TOPIC "DETAILS" --issue N` claims one. A request to research, expand, verify or
amend is a run: follow [`docs/research-protocol.md`](docs/research-protocol.md).

The heavy checks (the gate comparison, the render check, the selftests and the parity check) run in this
repository's Actions, workflow `.github/workflows/gate.yml`, on a pushed head and on a manual dispatch. A
research session does not run them: it does not run the gate, the selftest or the gate comparison in the research
checkout. A push of a run branch starts them; `scripts/rq ci RUN` shows the run, and `scripts/rq merge` waits for
it. The light trio runs at merge:

```bash
python scripts/dossier/validate.py --schema scripts/dossier/schema.json dossier/
python scripts/report/render.py --check
scripts/rq check
```

The commit hook and the checkout marker are set once per checkout. A research session checks them and never
writes git configuration.

## 1. What this repository is

A **research corpus**, not a codebase. The deliverable is a set of verified
claims about which services offer free, nearly-unlimited, or cheapest-paid
capacity — storage, compute, coding subscriptions, inference, crawling, egress,
email, databases, DNS, CI — and what each one costs in constraints, identity and
reliability.

The corpus covers every cheap resource — storage, compute, GPU time, inference,
crawling, egress, email, databases, DNS, CI — not storage alone. Storage's
stated workloads ([`BRIEF.md`](BRIEF.md) section 1) are the largest example, not
the scope. Every resource it covers is hosted: an offer that needs hardware the
reader owns or operates is out of scope. Programmatic access is required where
the resource is programmatic. **Identity is the binding constraint** on almost
every large quota, so every finding states what registration costs.

The corpus is the source of the published corpus at
[`f-shy/fshy.ajam.dev`](https://github.com/f-shy/fshy.ajam.dev): a merge session
exports a projection of `dossier/` there. The thing that rots is **the truth of
every claim**: a price changes, a free tier closes, a host dies. The repository's
design makes that rot visible and cheap to repair.

### The tree

| path | owns | read it when |
|---|---|---|
| [`AGENTS.md`](AGENTS.md) | this router. Routing only; it restates no fact | always, first |
| [`METHODOLOGY.md`](METHODOLOGY.md) | the discipline: evidence ladder, constraints, the rules, challenge protocol, reviews, staleness, handover | before writing anything, and when a claim feels uncertain |
| [`BRIEF.md`](BRIEF.md) | the slow state: coverage, settled findings, known dead ends, the checks that are red on `main` | to avoid re-researching |
| open issues labelled `rq:research` | the work queue: one request line per issue, with its evidence, its suggested units and its "Done when" | to choose your next run |
| [`queue/`](queue/) | the questions that lanes filed, one JSON file each. `scripts/rq queue` lists them; an issue names the ones it covers | when you plan a run with `scripts/rq plan RUN --queue ID` |
| [`README.md`](README.md) | the front door for a human: what this is, what is covered now, how to read it | when a human asks what this repository is |
| [`docs/`](docs/README.md) | the findings, by topic. `docs/<topic>/{free,paid}/<slug>.md` | to answer a question |
| [`docs/conventions/`](docs/conventions/README.md) | how prose, documents, numbers, timestamps and JSON records are written. Binding on every sentence | before your first sentence |
| [`dossier/`](dossier/README.md) | one JSON record per provider — **the source of truth**; every table in `docs/` is a view of it | to check or change a fact |
| [`history/`](history/README.md) | superseded claims, abandoned directions, corrections. Never deleted | when a claim changed, and to understand why |
| [`sources/`](sources/README.md) | third-party captures, as received, with a manifest. Script-maintained, never hand-edited | to check what a page said on the day we read it |
| [`references/`](references/README.md) | pruned third-party documents we cite and could lose. Hand-maintained, deliberately small | when a finding depends on a document that might vanish |
| [`scripts/`](scripts/README.md) | the instrumentation: probe, broker wrappers, dossier validation, staleness, discovery, gate | to measure anything |
| [`tools/`](tools/README.md) | compiled tools, only where a script is the wrong shape | rarely; `scripts/` first |
| [`docs/research-protocol.md`](docs/research-protocol.md) | the procedure for a research run: one request, many lanes, one writer. What a parent agent does with "Research/Expand <topic> <details>". The one-tree rules: section 11 | when the operator asks for research, an expansion, a verification or an amendment |
| [`scripts/research/`](scripts/research/README.md) | the research harness `scripts/rq`: units, leases, lane briefs, captures, the integrator, the contradiction checks, the audit, the landing | to run or debug a research run |
| [`scripts/fshy/`](scripts/fshy/README.md) | the derived SQLite store, the `fr` query and amend tool, and the public projection rules | to query anything across records, and to change a claim mechanically |
| [`registry/`](registry/entities.tsv) | cross-record facts the records cannot hold: entity overrides and record relations (duplicate, variant, successor), as TSV | when two records are one offer, or one vendor is split wrongly |
| public repository [`f-shy/fshy.ajam.dev`](https://github.com/f-shy/fshy.ajam.dev) | the published corpus (`data/`, an export of this repository's projection), the publish tools, the merge protocol, and the code of the wiki, the read-only API and the MCP. The wiki and the API are not deployed now; the operator decides when. Nothing in this repository deploys | when the published corpus, a merge or a public report is the work |
| [`docs/maintenance.md`](docs/maintenance.md) | the operating schedule: weekly, monthly, quarterly, and how to read a red gate | when the work is keeping the corpus honest rather than extending it |
| [`docs/sessions.md`](docs/sessions.md) | the session protocol: starting, ending and resuming a unit | at the start of a unit, at its end, and when picking one up cold |
| [`docs/expansion/`](docs/expansion/README.md) | the plans for the three thin areas, with their measured gaps and verification gates | when extending netdisk-pan, compute or inference |

---

## 2. The absolutes

1. ⛔ **The published conditions and legality are not yours.** The operator owns that
   judgement. Never write a legal caveat, never exclude a provider for reasons in its
   published conditions, and never soften a finding because using it may exceed them.
   Record suspension, throttle and data loss as a one-line **technical reliability note**
   and move on.
2. ⛔ **Never invent a number.** If you did not measure it, say `unverified` and
   give the reason. A plausible invented number is the worst outcome available to
   you, because it will be believed and acted on.
3. ⛔ **Never trust HTTP 200.** Dead hosts return 200 with an HTML error page, a
   zero length, or a 106-byte JSON 401 saved as your "model". Hash every download.
4. ⛔ **Never delete a finding.** A dead provider becomes `verdict: dead` with the
   evidence of its death; a superseded claim moves to `history/` with a reason. A
   deletion re-opens a question that cost a wave to close.
5. ⛔ **One fact, one home.** The dossier owns the record; documents are views.
   When two documents disagree, find the dossier. In a run, file an
   `open_question` that names the document: a run changes documents only through
   the render that `scripts/rq land` runs. A documents session that the operator
   starts in its own clone fixes the prose (rule 14).
6. ⛔ **No AI attribution, anywhere.** No co-author trailer, no "generated with",
   no tool or model name in a commit, a document footer or a file header. Commit
   messages describe the change and nothing else.
7. ⛔ **No credentials.** A dossier may record that a public key exists at a URL.
   It never stores a key that belongs to the operator.
8. ⛔ **`.tmp/` is never committed, and nothing in it outlives a merge pass.**
   Every file an agent makes while it works goes under `.tmp/<id>/`, the folder of
   its run, its unit or its session (rule 14). A file reaches the tree only through
   `scripts/rq integrate` or a reviewed pull request. When a merge session has
   merged the pull requests and closed the issues, it deletes all of `.tmp/` with
   `scripts/rq wipe`, fast-forwards the checkout with `scripts/rq sync`, and leaves
   no linked worktree: `git worktree list` prints one line, after it removes any
   worktree that `scripts/rq status` names against rule 14
   ([`docs/research-protocol.md`](docs/research-protocol.md) section 13). Anything
   that must survive goes into a record, a pull request or an issue before that. ⚠ While a merge session drains `.tmp/` for a wipe,
   `scripts/rq open` refuses: finish and land the run you have, then stop.
9. ⛔ **Never recommend, suggest or price owning hardware, and self-hosting is the
   last resort.** The corpus assumes no local hardware; fshy exists for readers
   with no local hardware or resources. Do not recommend owning a disk,
   buying a server, running a homelab, colocating a box, or keeping a machine at
   home. A provider that *sells* a rented or managed machine is a service and is
   often the answer. Self-hosted or on-premises *software*, which a reader
   installs and runs, is the last resort, also when it runs on a rented or
   free machine: in a list, a table, a ranking, a shortlist or an answer it comes
   after every hosted offer (free, trial or paid). It is never starred, highlighted
   or ranked first, and it is never presented as the answer while a hosted offer
   (free, trial or paid) exists. A parent, a lane and an auditor rank it last in
   everything they write.
10. ⛔ **A missing client tool is never a reason to reject a provider.** This
    corpus researches what can be reached, not what already has a wrapper. "No
    rclone backend", "no public API", "browser only", "would need a wrapper" are
    notes about the current state of tooling, not verdicts. A reader can write a
    wrapper, fork rclone, or drive a browser session; what matters is whether the
    resource exists, what it costs and what it takes to reach it. Record the
    constraint in `tooling` and judge the provider on capacity, egress and
    identity. Only a *technical impossibility* — a service that cannot be reached
    by any client, such as one requiring a physical token it will not issue — is a
    rejection.
11. ⛔ **The corpus covers every free or nearly free resource, not storage.** Never
    assume the target is disk. Compute, GPU time, model inference, egress, email,
    DNS, databases, CI runners and credentials are all in scope, and an
    opportunity in any of them is a finding. Do not write an introduction, a
    framing paragraph or a README that narrows the project to storage; the corpus
    is a catalogue of cheap capability.
12. ⭐ **A value that fits no term extends the vocabulary.** When a value fits no
    term of a schema
    vocabulary (`free_tier.unit`, `interface`, `limits[].kind` and the others in
    `scripts/dossier/schema.json`) or no category, such as a topic, the term is
    added. A research agent does not add it, because it opens no pull request from
    the research checkout (rule 14). It uses the nearest term (`mixed` for a unit),
    names the true one in the record's text, and files an `open_question` (or
    comments on the issue) that names the term and the records that need it. A
    rules session that the operator starts in its own clone opens the pull request
    that adds the term and names those records, and the merge session reviews it. A
    new topic also needs what [`docs/conventions/README.md`](docs/conventions/README.md)
    section 2.2 lists. ⚠ A new topic is two pull requests. The first is in `f-shy/fshy.ajam.dev`: the
    topic in `publish/rules/topics.json` and in the New offer form. Its text follows
    the section "Text that the public can read" of that repository's
    `docs/merge-protocol.md`: it names no path, issue or review file of this
    repository. The second is here, after the first merges, with the pin in
    `scripts/fshy/public.lock` moved to the public merge commit. Until the pull
    request merges, a record uses the nearest term (`mixed` for a unit) and names
    the true one in its text. ⛔ Never force a value into a wrong term.
13. ⛔ **No agent creates an account, signs up, enters a payment detail, spends
    money or provisions a resource that needs an account or a payment** (a VM, a
    bucket, a plan). This holds for a parent, a lane and an auditor, and for a free
    trial too. An anonymous upload of random test bytes, where an issue asks for
    one, is a probe and not a resource. The sign-up gate an agent sees is itself
    the finding: record what it asks for (email, phone, card, ID, institution).
    A value that only an account can show is recorded as
    `unverified: behind a sign-up`, and `scripts/rq merge` lists it in a comment
    on the open issue labelled `rq:operator`. A step that needs an account, a
    purchase or a running resource is the operator's: it goes to that issue.
14. ⛔ **One working tree for all research, and no heavy work in it.** Research runs
    with 30 or more agents at the same time, on one machine, in one checkout: the
    research checkout (`git config --get rq.researchCheckout` prints `true`). A
    research agent (a parent, a lane or an auditor):
    - never makes a git worktree, a clone or a fork, and never starts a subagent
      with an option that gives it a worktree or a clone of its own;
    - never changes the checkout's branch, index, tracked files or git
      configuration. It runs no `git checkout`, `switch`, `add`, `commit`, `merge`,
      `reset`, `stash`, `pull`, `push` or `config` that writes, and `git status`
      only as `git --no-optional-locks status --short`. `scripts/rq` writes the run
      branch with git plumbing; that is the only way research changes the
      repository;
    - changes a record only through a run. A one-record fix is an `amend` run with
      one unit: `scripts/rq open amend TOPIC "RID: what is wrong"`.
      `scripts/fr amend`, `add`, `dead`, `relate` and `entity-set`, and
      `python scripts/report/render.py` without `--check`, refuse in the research
      checkout;
    - writes every file it makes under `.tmp/<id>/`: `.tmp/<run>/` for a run,
      `.tmp/<run>/units/<unit>/` for a lane or an auditor, `.tmp/session-<id>/` for
      a session (`scripts/rq folder session`). It runs every command from the
      repository root and never `cd`s into its folder;
    - never copies the tree, never builds a store of its own and never runs the
      gate. One store is built for each commit of the checkout and shared. The
      heavy checks run once per pushed head in this repository's Actions
      (section 0), never on this machine, and the light ones inside
      `scripts/rq merge`;
    - never runs `scripts/rq wipe` or `scripts/rq sync`: they belong to the merge
      session.

    Work that is not research (a tools change, a rule change, a vocabulary term, a
    hand edit of prose) is done by a session that the operator starts for it, in
    its own clone, never in the research checkout.
15. ⛔ **Never cap your own requests.** The page broker behind
    `scripts/broker/broker.sh`, `https://web.pkgforge.dev`, is the operator's own
    project. Make every request the research needs: start every lane of a plan at
    the same time, read every page a question needs, try every route to a walled
    page, and run every probe that settles a value. More reads make better
    research. No script, brief or document sets a rate, a lane count, a page
    budget, a tool-call budget, a delay or a "be gentle" rule. When a server answers
    429 or 503 with `Retry-After`, that is the only pacing, and it comes from the
    server: `scripts/rq capture` prints `retry_after` and `retry_at` and exits 4, so
    read other pages and read that one again after `retry_at`;
    `scripts/rq capture --wait` waits in the same command.

---

## 3. Which document answers which question

Read the row, not the tree.

| the question | the owner |
|---|---|
| What is this repository, and what is covered right now? | [`README.md`](README.md) |
| What did we already settle, and what is dead? | [`BRIEF.md`](BRIEF.md) |
| How do I run a research unit to this repository's standard? | [`METHODOLOGY.md`](METHODOLOGY.md) |
| What does each confidence level mean, and how do I record one? | [`METHODOLOGY.md`](METHODOLOGY.md) §The evidence ladder |
| What are the seven binding constraints, and how do I name one? | [`METHODOLOGY.md`](METHODOLOGY.md) §Constraints, and [`dossier/README.md`](dossier/README.md) §The constraint vocabulary |
| Which hosts can I get for free, or nearly? | [`docs/storage/README.md`](docs/storage/README.md) |
| Which pan drive can I mount, and do public instances actually work? | [`docs/netdisk-pan/README.md`](docs/netdisk-pan/README.md) |
| What can I run, for how long, before it is reaped? | [`docs/compute/README.md`](docs/compute/README.md) |
| Which subscription is cheapest per unit of agent work? | [`docs/coding-subs/README.md`](docs/coding-subs/README.md) |
| What will answer a completion request with no card? | [`docs/inference/README.md`](docs/inference/README.md) |
| How do I read the web at scale, and what do I do when a page is walled? | [`docs/crawler-scraper/README.md`](docs/crawler-scraper/README.md) |
| How do I get traffic out, or a service in? | [`docs/egress/README.md`](docs/egress/README.md) |
| How do I send and receive mail for nothing? | [`docs/email/README.md`](docs/email/README.md) |
| Where does state live after the free tier ends? | [`docs/databases-kv/README.md`](docs/databases-kv/README.md) |
| What is the cheapest name I can put a service on? | [`docs/domains-dns/README.md`](docs/domains-dns/README.md) |
| What can I run by pretending it is a build? | [`docs/ci-cd-runners/README.md`](docs/ci-cd-runners/README.md) |
| What does the upstream see as my address, and can I change it? | [`docs/ip-proxy/README.md`](docs/ip-proxy/README.md) |
| Which service turns the least money into retrieved bytes (debrid, usenet, hosted downloaders)? | [`docs/debrid/README.md`](docs/debrid/README.md) |
| Which monitoring, job, queue or auth service is free with no card? | [`docs/dev-services/README.md`](docs/dev-services/README.md) |
| Which data API gives free calls, and is there a dump? | [`docs/data-apis/README.md`](docs/data-apis/README.md) |
| What exactly did this provider offer, and when? | `dossier/<topic>/<slug>.json` |
| What does the corpus know about X, across every topic? | `scripts/fr search X`, `scripts/fr entity X` |
| Who merges a run, and how does it reach the public? | a merge session that did not run it, in any clone: `docs/merge-protocol.md` in `f-shy/fshy.ajam.dev`, and its commands in [`docs/research-protocol.md`](docs/research-protocol.md) section 13. As its last steps in the research checkout, it deletes `.tmp/` with `scripts/rq wipe` and fast-forwards with `scripts/rq sync` ([`docs/research-protocol.md`](docs/research-protocol.md) section 13). ⛔ A research session never merges its own run |
| The operator said "Research/Expand/Verify <topic> <details>". What now? | [`docs/research-protocol.md`](docs/research-protocol.md): `scripts/rq open`, plan, lanes, collect, integrate, audit, land |
| Is a claim contradicted anywhere, mechanically? | `scripts/rq check` ([`scripts/research/README.md`](scripts/research/README.md)); the gate fails on a new error violation |
| How do I change a claim and keep the old value? | In the research checkout, an `amend` run with one unit: `scripts/rq open amend TOPIC "RID: what is wrong"` ([`docs/research-protocol.md`](docs/research-protocol.md) section 3). In the operator's own clone, `scripts/fr amend` ([`scripts/fshy/README.md`](scripts/fshy/README.md)); it validates and appends to the ledger |
| Where does a file I make go? | `.tmp/<id>/` (section 2 rule 14), the table in [`docs/research-protocol.md`](docs/research-protocol.md) section 11 |
| What reaches the published corpus, and what is stripped? | [`scripts/fshy/rules/projection.json`](scripts/fshy/rules/projection.json): technical data only; process narrative, personal details and terms text never leave the repository |
| Why did this claim change? | [`history/`](history/README.md) |
| What did the page actually say? | [`sources/`](sources/README.md) |
| How do I probe, validate or measure something? | [`scripts/README.md`](scripts/README.md) |
| What do I run this week, and what does a red gate mean? | [`docs/maintenance.md`](docs/maintenance.md) |
| What do I work on next? | a free open issue labelled `rq:research`: `scripts/rq issues` lists them with their claims. Open its run with `scripts/rq open ... --issue N`, which claims it |
| What can only the operator do (an account, a purchase, a real send)? | the open issue labelled `rq:operator` |
| What should this corpus cover next, and how? | [`docs/expansion/README.md`](docs/expansion/README.md) |

---

## 4. The work loop

⭐ **A request to research, expand, verify or amend is a run.** Follow
[`docs/research-protocol.md`](docs/research-protocol.md). Lanes propose, and `scripts/rq integrate` writes the
records on a run branch that lands as a pull request. The steps below are what a run does inside; the
harness enforces steps 4 to 8. ⛔ In the research checkout every change is a run: a one-record fix is an `amend`
run with one unit (section 2 rule 14).

1. **Pick an open issue labelled `rq:research`.** Its request line is the run. A
   unit inside the run is one topic, one provider class and one question, not
   "research storage".
2. **Read the topic README and the dossier** for anything already known. Read the
   relevant passages of [`METHODOLOGY.md`](METHODOLOGY.md).
3. **Map breadth-first**, then go deep on every candidate that looks real. Use
   `sh scripts/broker/broker.sh`; never hand-roll a curl against the brokers. Read
   as much as the question needs (section 2 rule 15).
4. **Measure what you can.** `python scripts/probe/probe.py URL --out
   .tmp/<run>/units/<unit>/probe` (or your `.tmp/session-<id>/`) writes the probe
   record into your own folder under `.tmp/`, never elsewhere in the tree, and
   `scripts/rq capture probe:TARGET --lane DIR --probe FILE` stores it. A
   `measured` claim cites a stored probe record.
5. **The integrator writes the records.** In a run, a lane proposes and
   `scripts/rq integrate` writes the record and its ledger line. The topic
   documents are views: a run changes them only through the render that
   `scripts/rq land` runs. That render lists each `measured` or `documented`
   record the run added in the block "Records that no other document names" of
   its topic README, so the gate's `links` check finds it cited with no hand edit
   of prose. In the research checkout there is no hand change: a one-record fix is
   an `amend` run, and `scripts/fr amend`, `add`, `dead`, `relate` and `entity-set`
   refuse there (section 2 rule 14). In the operator's own clone they validate the
   record and write the old value to `history/ledger.jsonl`; after such a change,
   run `python scripts/report/render.py` (without `--check`) and commit what it
   writes in the same pull request, so a new `measured` or `documented` record is
   cited and the counts are current.
6. **The ledger is the history of a changed value.** A run never writes
   `history/` by hand: the integrator writes the ledger lines on the run branch
   ([`docs/research-protocol.md`](docs/research-protocol.md)). Only in the
   operator's own clone, for a change that a reader must understand beyond the old
   and the new value (such as a correction of a whole document), does a session
   write a `history/` entry by hand.
7. **The handover is the pull request.** A run does not edit `BRIEF.md`. Its
   handover is the pull request body that `scripts/rq land` writes and the
   follow-up issue that `scripts/rq merge` files. The follow-up carries the label
   `rq:research` too, so a later run claims it from the queue like any other
   issue. The pull request says "Part of
   #N" and ticks the "Done when" lines of the issue that the run meets
   (`scripts/rq land RUN --meets N,N`, each N the number of a line, 1 for the
   first). A line that says a merge session ticks it is never ticked by a run.
   After the merge, `scripts/rq merge` closes the issue when every line is ticked,
   or comments the lines left.
8. **Land.** `scripts/rq land RUN --meets N,N` merges main into the run branch in
   git objects, renders the tables of the topics the run touched, checks the
   records it touched and opens the pull request, in under a minute. A push of
   the run branch starts the heavy checks on that head in this repository's
   Actions. A fork's push starts nothing: the merge session's `scripts/rq merge`
   pushes the head to `rq/RUN` in this repository, which starts them;
   `scripts/rq ci RUN` shows them (section 0).

⛔ **A run ends at its pull request; the session does not.** After `scripts/rq land`,
the session takes the next open issue as a new run. It does not wait for the merge,
and it never merges. When the operator's prompt names one issue, the session ends at
that issue's pull request. ⭐ **Claim the issue:** take an issue that `scripts/rq issues`
lists as free, at random rather than the first (for an issue that is run once for each
topic, a topic with no live claim), and open its run with `scripts/rq open KIND TOPIC
"DETAILS" --issue N`. That adds a comment with the run id, its topic and the UTC time
and the label `rq:active`, so another session sees the claim; `open` refuses an issue
that another run of the same topic holds, and when it says the issue is taken, take
another. A claim ends when a merge session merges the run, when the pull request
is closed (`scripts/rq cleanup` gives the issue back), with
`scripts/rq close RUN --reason "..."` for a run whose session died, or after
`claim_hours` with no pull request; `scripts/rq release N --run RUN --reason "..."`
gives back the claim of a session that died. Take an issue whose records do not
overlap a run that waits for review: `scripts/rq plan` refuses a record that another
run still leases. The session ends when no issue is left that it can run, or when
the operator interrupts.

---

## 5. Quality, in one paragraph

A number without a URL and a date is a rumour. A quota without its binding
constraint is marketing. A provider without its identity cost is unreachable
capacity. A dead end not written down is a wave spent twice. A claim you could not
verify is labelled `unverified` in the same sentence that states it, never
quietly dropped and never upgraded to fill a table. A provider rejected because no
client exists is a finding thrown away. A resource priced as something the reader
must buy and house is a recommendation that cannot be acted on. The corpus is worth
what its weakest evidenced claim is worth, because a reader cannot tell which claim
that is.

⭐ **The three scope facts — no hardware and self-hosting last, no tooling excuses, every
cheap resource — are in §2 as rules 9 to 11.** They are absolutes rather than preferences.
`scripts/own-hardware.py` and `scripts/self-hosted-last.py` enforce the first in the gate;
the other two are judgements no regex can make.

---

## 6. When you are stuck

| symptom | what it usually is | what to do |
|---|---|---|
| every page returns 200 with no content | a challenge page, not a live site | change route, not effort: try every rung of the ladder and every provider pin of [`docs/crawler-scraper/free/broker.md`](docs/crawler-scraper/free/broker.md), with as many reads as each route needs. A lane has each rung: `scripts/rq capture URL --lane WS --provider ID` (the pins: each id that `sh scripts/broker/broker.sh status` lists in `providers` with `read` in its `caps`), `fetch URL --dump-headers` and `archive URL --at YYYY-MM` written into its workspace and registered with `--from-file` (lane brief rule 10) ([`METHODOLOGY.md`](METHODOLOGY.md) §The challenge protocol). Record `unverified: blocked by challenge` only when every route failed, and name the routes tried |
| a forum is unreachable through every reader | it is Cloudflare-walled to all fetch paths | search it with `sh scripts/broker/broker.sh search "..." --domains HOST --tsv`; the snippet carries the post body. See [`docs/crawler-scraper/free/broker.md`](docs/crawler-scraper/free/broker.md) |
| a provider's numbers disagree between two of our documents | the document is wrong, the dossier is right | the dossier is right. A generated table that disagrees is fixed by the render that `land` runs. Prose that disagrees: file an `open_question` that names the document; a documents session in the operator's own clone fixes it. A wrong record is fixed by a run: a lane's `set`, or an `amend` run with one unit |
| a quota looks enormous and you cannot register | identity is the binding constraint | record `fails-identity` with the evidence, and stop — an unreachable quota is worth zero and saying so is the finding |
| CI's gate fails on a check that also fails on `main` | the check depends on the clock, or it was red before you started | `scripts/rq ci RUN` names it. Do not fix it in your run; [`BRIEF.md`](BRIEF.md) section 5 names its issue. Comment the check on the pull request: `gh pr comment NUMBER --body "..."` (the next `land` rewrites the body, a comment stays) |
| CI's gate fails on a check that passes on `main` | your run broke it | `scripts/rq ci RUN` names the check (the public log prints no detail; a merge session reads it with `scripts/rq gatecmp` in its own clone): fix it on the run branch with a new unit, `scripts/rq put` or `scripts/rq resolve`, then `scripts/rq land` again |
| you have searched twice and found nothing | you have not searched enough | change language, change forum, search the inverse ("who exceeds the limit, and what the enforcement looks like"), and check the archive for a page that has since been removed |
