# Contributing

`raw` is the source corpus. A merge session exports a projection of it to
[`f-shy/fshy.ajam.dev`](https://github.com/f-shy/fshy.ajam.dev). A contribution is a research run: it
adds or changes records in `dossier/`, and the render turns them into the tables in `docs/`.

Read [`AGENTS.md`](AGENTS.md) first. It is the router: what this repository is, what never bends, and
which document owns each question.

## Clone

With a GitHub account, clone your fork, not the upstream: `gh` names your fork `origin` and the upstream
`upstream`, and `rq` pushes the run branch to `origin`.

```bash
gh repo fork f-shy/raw --clone
cd raw
git fetch upstream && git merge --ff-only upstream/main && git push origin main
```

Set the address your commits carry before the first one. A run branch keeps the author of every commit it
holds, and a merge does not rewrite them, so an address you would not publish reaches the public history
with the merge:

```bash
git config user.email "$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"
```

Without an account, clone the upstream read-only:

```bash
git clone https://github.com/f-shy/raw
cd raw
```

Do **not** set `rq.researchCheckout`. That marker belongs to the operator's shared checkout, where it
makes the writer commands refuse so that thirty agents cannot change one tree. An unmarked clone is
what a contributor wants: `scripts/fr amend`, `scripts/rq open` and the rest work locally and refuse
nothing.

`scripts/rq plan` builds the SQLite store on first use. It takes about two minutes on a fresh clone.
That is not a hang.

## Two paths

### A GitHub account and `gh`

```bash
gh auth login          # a token with the repo scope, on your own account
scripts/rq open amend TOPIC "RID: what is wrong" --no-issue
```

`--no-issue` opens a local run with no issue to claim. If the task names an issue, use `--issue N`
instead: `rq open` writes a comment that names the run and the topic, and adds the label `rq:active`
when your account has triage rights. Without those rights the comment alone is the claim, and
`run.json` records `claim_unlabelled: true`.

Work the lanes. A parent agent may dispatch one agent per lane; a solo agent walks the briefs in
order. Nothing in the harness requires subagents: a brief is a file under `.tmp/<run>/units/`.

Collect, then integrate. They are two steps: `collect` reads each lane's files and lints them, and
`integrate` takes only a collected unit. `integrate` on its own applies nothing, and now says so.

```bash
scripts/rq collect
scripts/rq integrate
scripts/rq land RUN
```

`land` pushes the branch to your fork and opens the pull request against `f-shy/raw`. The pull
request triggers no workflow by itself. A maintainer reviews it and starts the gate.

### No `gh` and no account

The same run, handed over as a zip:

```bash
scripts/rq open amend TOPIC "RID: what is wrong" --no-issue
# work the lanes, then:
scripts/rq collect
scripts/rq integrate
zip -r fshy-<run-id>.zip .tmp/<run>/          # Windows: Compress-Archive .tmp/<run> fshy-<run-id>.zip
```

`integrate` tries to push the run branch, and a read-only clone cannot: it says so and goes on, because the
branch is intact locally and the zip carries it. Nothing is lost.

Hand the zip to the maintainer by any channel. The bundle is data, not code. The maintainer imports
it with `scripts/rq import-bundle`, validates every record against the schema, applies it to a fresh
run branch, and lands it. Nothing in the bundle is executed.

## Collisions

Leases are local to one clone (`.tmp/rq/state.db`). Two contributors can plan the same `rid:` without
seeing each other. The collision surfaces at merge as a conflict in the record, not as a silent
overwrite. Before you start, run `scripts/rq issues` and take an issue that is free; that claim is the
only cross-machine lock.

## The rules that decide a review

- Every claim carries a rung: `measured`, `documented`, `reported`, `inferred`, `unverified`.
- A number without a URL and a date is a rumour. A quota without its binding constraint is marketing.
- Never invent a number. An unverified claim says `unverified` and why, in the sentence that states it.
- One fact, one home: the dossier owns the record; every table in `docs/` is a view of it.
- Never delete a finding. A dead provider becomes `verdict: dead` with the evidence; a superseded
  claim moves to `history/` with the reason.
- No credentials in the tree, ever. No tool or model attribution in a commit or a document.
- `scripts/fr amend` validates a record against the schema and appends the old value to
  `history/ledger.jsonl`, but it runs no render. A maintainer runs the render at merge, so a record
  that changes a table needs no hand edit of the table.

## What a maintainer does

A maintainer reviews the pull request, starts the gate on its head, and merges. `rq merge` is not a
command a contributor runs: it needs write access, it merges with `--match-head-commit`, and it files
the follow-up issue.

⭐ A pull request from your fork is merged at the head the gate checked. The maintainer names it with `--pr`, for
`scripts/rq review RUN --pr NUMBER` and for `scripts/rq merge RUN --pr NUMBER`, because `f-shy/raw` has no `rq/RUN`. `merge`
brings the branch up to date with `main`, pushes it to `rq/RUN` in `f-shy/raw`, where the gate runs, and then pushes
that same commit to your fork's branch, fast-forward only. That push needs "Allow edits by maintainers" on the pull
request, which GitHub offers by default when you open it. ⚠ Without it, `merge` stops before it merges: allow
edits, or merge `main` into your branch yourself, and the maintainer runs `merge` again. `merge` never deletes your
branch.

A run that another pull request carries (several runs combined in one) is merged with
`scripts/rq merge RUN --pr NUMBER`, once for each run it carries.
