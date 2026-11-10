# What can I run by pretending it is a build?

A CI system is a machine for a bounded time, destroyed at the end, with no inbound network and a
per-job clock. That shape decides everything in this topic. The minutes are almost never the
constraint; the per-job wall clock, the concurrency and the artifact retention are.

Two markets share a UI. On GitHub, minutes are unlimited on a public repository and metered on a
private one, and that single fact decides the strategy. Everywhere else a monthly minute pool is
the whole product.

## The two markets

| market | free shape | who is in it | what binds |
| --- | --- | --- | --- |
| unlimited minutes, gated on repository visibility | no minute cap, 20 concurrent jobs, 6 h/job | GitHub Actions on a public repo, AppVeyor on a public repo | the per-job clock and the concurrency |
| a monthly minute allowance, gated on identity | 400 to 30,000 units a month | GitLab, CircleCI, Buildkite, Azure, Cirrus | the monthly pool |
| a monthly minute pool on a GitHub-compatible runner | 200 to 3,000 minutes a month | Blacksmith, RunnerHut, runners.io, WarpBuild, Depot, compiler.dev | the monthly pool, the vCPU-weighted unit and the card gate |
| run the runner on a rented VM | unlimited minutes, no minute cap, gated on the VM's clock | Woodpecker, Forgejo Actions, Drone (dead) | the VM's monthly invoice and its uptime |

## The three numbers that decide it

⛔ **The per-job wall clock is the ceiling on one unit of work.** GitHub gives **6 hours** on a
hosted runner and **5 days** on a self-hosted one. Azure gives **60 minutes** on the free grant.
AppVeyor gives **60 minutes**. Codeberg's hosted runners give **2, 5 or 10 minutes**. Cirrus gives
**2 hours** on a free task. A job that needs seven hours cannot be run on GitHub's hosted runners
at any price, and no minute allowance changes that.

⭐ **Concurrency sets the flow, and the per-job cap sets the stock.** GitHub Free gives 20 concurrent
jobs of up to 6 hours, so 20 slots x 24 hours is **480 runner-hours a day** with no minute meter
while the repository is public. The 20 x 6 is **120 runner-hours held at one instant**, which is a
stock; multiplying it by 24 produces runner-hours squared per day and not a rate. 480 is still the
largest free lane in this corpus, and it is available only while the repository is public.

⚠ A figure of 2,880 runner-hours a day is a units error. It would need 120 concurrent slots,
and GitHub Free provides 20.

⚠ **Persistent storage is the scarce half.** Compute is abundant and keeping the output is not. On
GitHub Free: **500 MB** of artifacts, **500 MB** of packages and container images in the same
pool, and **10 GB** of cache that evicts entries not accessed in 7 days. Artifacts default to 90
days of retention.

## Can a CI runner be used as general compute?

Partly, and the shape is narrow. What a job gets is a 4 vCPU, 16 GB, 14 GB-disk Ubuntu machine
that lives at most six hours, cannot accept an inbound connection, and is destroyed at the end. It
can reach out, so it can upload its results, fetch inputs, and hold a long-polling connection.

What reaps it is the per-job clock, and the clock is not negotiable. A job that hits six hours "is
terminated and fails". There is no grace period and no extension.

So the honest answer is that a CI runner is a batch worker: short, parallel, ephemeral, outbound
only. A serving workload, a persistent socket, or anything that needs more than six hours of
continuity is not what this is. Every hosted lane keeps that clock. Only self-hosting removes it, and
it is the last resort: a runner on a rented or free machine, attached to a free control plane, where
the machine is the cost and the CI system is only a scheduler.

## The documents

| document | answers |
| --- | --- |
| [`free/github-actions.md`](free/github-actions.md) | the public-versus-private split, the 6-hour cap, the 20-job concurrency, and the cache and artifact pools |
| [`free/hosted-gha-runners.md`](free/hosted-gha-runners.md) | the hosted runners a workflow reaches by changing `runs-on`, and what each free allowance buys in vCPU-minutes |
| [`free/other-hosted.md`](free/other-hosted.md) | GitLab, CircleCI, Buildkite, Azure, AppVeyor, Cirrus and Codeberg, with the caps each one hides |
| [`free/registries-and-cache.md`](free/registries-and-cache.md) | GHCR at 500 MB, the GitHub Packages pool, the GitLab registry exclusion, and Docker Hub's anonymous tokens |
| [`paid/minute-packs.md`](paid/minute-packs.md) | what a minute costs beyond the allowance, and the cheapest way to buy more |
| [`free/self-hosted.md`](free/self-hosted.md) | the last resort, after every hosted lane: Woodpecker, Forgejo Actions, and a self-hosted runner, which removes the per-job cap |

## What is dead in this topic

**Three providers carry a non-qualifying verdict**: `azure-pipelines-public` and `travis-ci` are
`dead`, and `drone-ci` is `paid-only`. A further set of dead ends below are misuses of a live
provider rather than rejected providers, and each has its own record or is cited in a document's
"What did not work" section. The ones that cost the most to establish:

- **Azure Pipelines for public projects**: retired. New public projects cannot obtain the grant
  and existing ones lose it in 2027 (`azure-pipelines-public`, `dead`).
- **Travis CI**: the free trial is withdrawn and open-source credits are granted by support rather
  than self-serve (`travis-ci`, `dead`).
- **Codeberg's "600 free minutes"**: no such allowance exists. The hosted runners cap a job at
  2, 5 or 10 minutes and every project needs manual approval. This is the most-repeated wrong
  number found in this topic.
- **Cirrus CI's live site**: `cirrus-ci.org` and `www.cirrus-ci.com` did not resolve on
  2026-10-22, `cirrus-ci.com` resolved but failed the TLS handshake, and the read broker reported
  a Cloudflare 525. Its figures here come from a dated archive capture.

## The three findings a reader should carry

- **GitHub Actions on a public repository is the only lane in this corpus with a published
  statement that minutes are free and unlimited, and the largest flow by two orders of magnitude.**
  20 concurrent slots x 24 hours is **480 runner-hours a day**, and 20 jobs of up to 6 hours hold
  120 runner-hours at one instant. AppVeyor also publishes no minute cap and caps concurrency at
  one; Codeberg publishes no cap of either kind and caps a job at ten minutes. The cost of the
  GitHub lane is that the repository, its workflows and its logs are public.
- **Codeberg's hosted Forgejo runners publish no job-count and no minute cap, and each job is
  capped at 2, 5 or 10 minutes.** That is 40 CPU-minutes on the medium label, on a service in open
  alpha that is governed by fair use rather than a published ceiling. It is the second-best free
  compute lane here and the least known, and the word for it is "no published cap", not "unlimited".
- Last, and only after every hosted lane: a self-hosted runner removes the per-job cap. GitHub
  allows a self-hosted job to run 5 days instead of 6 hours, and Woodpecker imposes none at all. At
  that point the cost is the machine, which is the compute topic's question.

## The records

Every provider named in this topic has one record.

| slug | provider | verdict | confidence |
| --- | --- | --- | --- |
| `github-actions-public` | GitHub Actions on a public repository | qualifies | documented |
| `github-actions-private` | GitHub Actions on a private repository | qualifies-with-caveat | documented |
| `gitlab-ci` | GitLab CI on GitLab.com Free | qualifies-with-caveat | documented |
| `circleci-free` | CircleCI Free | qualifies-with-caveat | documented |
| `buildkite-free` | Buildkite Free | qualifies-with-caveat | documented |
| `appveyor` | AppVeyor | qualifies-with-caveat | documented |
| `azure-pipelines-private` | Azure Pipelines, private project | qualifies-with-caveat | documented |
| `azure-pipelines-public` | Azure Pipelines, public project | dead | documented |
| `travis-ci` | Travis CI | dead | documented |
| `codeberg-ci` | Codeberg CI (Woodpecker) | qualifies-with-caveat | documented |
| `codeberg-forgejo-actions` | Codeberg Forgejo Actions | qualifies-with-caveat | documented |
| `compiler-dev` | compiler.dev | trial-only | documented |
| `runnerhut` | RunnerHut | qualifies-with-caveat | documented |
| `runners-io` | runners.io | qualifies-with-caveat | documented |
| `cirrus-ci` | Cirrus CI | qualifies-with-caveat | documented |
| `ghcr` | GitHub Container Registry | qualifies-with-caveat | measured |
| `github-packages` | GitHub Packages | qualifies-with-caveat | documented |
| `gitlab-container-registry` | GitLab Container Registry | qualifies-with-caveat | documented |
| `woodpecker-selfhost` (self-hosted) | Woodpecker CI | qualifies | documented |
| `forgejo-gitea-actions` (self-hosted) | Forgejo and Gitea Actions | qualifies | documented |
| `drone-ci` (self-hosted) | Drone CI | paid-only | documented |

## Where a number here came from

`documented` means a first-party page was read on 2026-10-22. `measured` means a request was made
that day: the Docker Hub token endpoint, the DNS and TLS behaviour of Cirrus, and three GHCR
anonymous token requests each followed by a manifest fetch. No workflow was executed, so no
throughput or duration figure here is `measured`, and the records say so.

⚠ **The GHCR record is `documented`, not `measured`, and a probe of a repository that does not
exist once put it at `measured`.** `library/hello-world` is Docker Hub's namespace; GHCR has no
`library/*`, so the 403 that carried the `measured` rung answered a path and not a policy. The
correction is in
[`history/2026-10-22T041501Z/ghcr-anonymous-pull-wrong-namespace.md`](../../history/2026-10-22T041501Z/ghcr-anonymous-pull-wrong-namespace.md).

The records are in [`../../dossier/ci-cd-runners/`](../../dossier/ci-cd-runners/).

## Records that no other document names

Each `measured` or `documented` record of this topic that no other document of `docs/` names.

<!-- generated:start topic=ci-cd-runners kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `actuated` | Actuated | paid-only | documented |
| `appcircle-starter` | Appcircle | qualifies-with-caveat | documented |
| `cloudflare-artifacts` | Cloudflare Artifacts | paid-only | documented |
| `cloudflare-pages-builds` | Cloudflare Pages builds | qualifies-with-caveat | documented |
| `cloudflare-workers-builds` | Cloudflare Workers Builds | qualifies-with-caveat | documented |
| `codefresh-ci` | Codefresh CI (Octopus Deploy) | paid-only | documented |
| `dev-ramps-free` | Dev Ramps | qualifies-with-caveat | documented |
| `garnix` | Garnix | dead | measured |
| `harness-ci-free` | Harness CI Free plan (Harness Cloud) | fails-identity | documented |
| `nixci` | NixCI | trial-only | documented |
| `semaphore-cloud` | Semaphore Cloud | qualifies-with-caveat | documented |
| `sourcehut-builds` | SourceHut builds.sr.ht | paid-only | documented |
| `vercel-ci` | Vercel CI | qualifies-with-caveat | documented |
<!-- generated:end -->
