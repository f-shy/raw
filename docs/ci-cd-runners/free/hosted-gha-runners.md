# Which hosted runner can a workflow reach by changing `runs-on`?

GitHub Actions is the syntax, not the machine. A hosted runner market has grown
around that split: a workflow keeps its YAML and changes one line, and the job
runs on someone else's hardware at someone else's per-minute rate. Six providers
in this corpus sell that, and their free allowances are stated in three different
units, so the headline numbers are not comparable until the unit is fixed.

## The comparison

Rates are the 2 vCPU Linux class unless the row says otherwise. GitHub's own
list price is the reference: **USD 0.006** for a 2-core Linux minute and
**USD 0.012** for a 4-core one.

| provider | free allowance | extra rate | card | verdict |
| --- | --- | --- | --- | --- |
| Blacksmith | 3,000 minutes a month | 33% below GitHub per-minute, so about USD 0.008 for 4 cores | not stated | `qualifies-with-caveat` |
| RunnerHut | 3,000 Linux minutes a month | USD 0.0040, one-minute minimum | no | `qualifies-with-caveat` |
| runners.io | 3,000 run-minutes a month | USD 0.0040 a run-minute | **yes** | `qualifies-with-caveat` |
| WarpBuild | none published | USD 0.004; USD 0.002 BYOC | no | `paid-only` |
| Depot | no free tier; a 7-day trial | 2,000 GitHub Actions minutes included in the USD 20 plan, then USD 0.006 | not stated | `trial-only` |
| compiler.dev | 200 minutes over 14 days | USD 0.001 a core-minute | no for the trial | `trial-only` |

## The unit is not the minute

Three of these sell a minute of a **2 vCPU** machine and call it a minute;
compiler.dev sells a **core-minute**, so its 2-core minute is USD 0.002; and
runners.io sells a **run-minute** that is weighted by vCPU: a 4 vCPU job spends
two run-minutes a minute, a 1 vCPU job half of one, Windows 2.5 and Linux ARM64
0.625 of the same size. Its 3,000 run-minutes is therefore 1,500 wall-clock
minutes on a 4 vCPU runner and 6,000 on a 1 vCPU one.

That weighting is the single most useful fact on this page, because it is the
difference between a free pool that covers a serious private pipeline and one
that covers a weekend. 3,000 run-minutes is **6,000 core-minutes** either way,
which is 3,000 wall-clock minutes on a 2-core shape and 1,500 on a 4 vCPU one;
the same compute is spread over half the time. Convert before comparing.

## The card gate decides who can start

- **runners.io requires a card before the first job.** Its included pool is the
  largest here, and it is the one lane a reader without a card cannot use.
- **RunnerHut and compiler.dev state no card** for their free allowances.
- **compiler.dev adds the card only when the 200 trial minutes run out.**
- **WarpBuild takes an email and no card**, adding a payment method when the
  free usage or credit limit is reached; the size of that limit is not published,
  which is why it cannot be sized as a free tier.
- **Blacksmith and Depot state no signup requirement** on the pages read here, so
  their card cost is unverified rather than zero.

## What each free allowance actually buys

**Blacksmith: 3,000 minutes a month** on every plan, with Docker layer caching and
sticky disks at USD 0.50 a GB-month and a static IP at USD 100 a month. The page
states no per-size price table, only the 33% discount, so the per-core figure is
derived from GitHub's list price rather than read.

**RunnerHut: 3,000 Linux minutes a month** with unlimited cache and every runner
family on one meter. The rates are USD 0.0040 for 2 vCPU x64, USD 0.0032 for
ARM64, USD 0.0080 for Windows, USD 0.0400 for macOS and USD 0.0900 for an L4 GPU,
billed per second with a one-minute minimum.

**runners.io: 3,000 run-minutes a month** with no monthly fee and no per-seat
price, a card required, and priority lanes at twice the rate and twice the
run-minutes.

**Depot: no free tier.** The 7-day trial is the only free window; the USD 20 a
month Developer plan includes 2,000 GitHub Actions minutes, 2,000 sandbox
minutes, 500 container build minutes and 25 GB of cache, and additional GitHub
Actions minutes are USD 0.006 for the base 2 vCPU Linux runner.

**compiler.dev: 200 minutes over 14 days**, up to 8 concurrent jobs, Linux only,
then USD 0.001 a core-minute on Basic. Prepaid credit never expires.

**WarpBuild: no free allowance is published.** The hosted rate is USD 0.004 for
2 vCPU and USD 0.008 for 4 vCPU, BYOC is USD 0.002, and cache storage is
USD 0.20 a GB-month.

## When this is the wrong answer

GitHub Actions on a public repository remains the largest free lane in the
corpus: unmetered minutes, 20 concurrent jobs, a 6-hour job clock, no card.
Nothing here beats it for a public project. A hosted runner is for the private
repository whose minutes are metered, or for macOS, Windows and GPU shapes that
GitHub sells at a higher price or not at all.

`Evidence:` `docs.github.com/en/billing/reference/actions-runner-pricing` (read
2026-11-10): Linux 2-core USD 0.006 and 4-core USD 0.012. `blacksmith.sh/pricing`
(read 2026-11-10): 3,000 free minutes a month, the 33% discount, the add-on
prices. `runnerhut.com/pricing` and `runnerhut.com` (read 2026-11-10): the 3,000
free Linux minutes, the five rates, the one-minute minimum, no card required.
`runners.io/pricing` and `runners.io` (read 2026-11-10): 3,000 run-minutes, the
run-minute weighting, the card requirement. `warpbuild.com/pricing` (read
2026-11-10): the rate table, BYOC, cache storage, the signup answer.
`depot.dev/pricing` (read 2026-11-10): the trial and the Developer plan's
included minutes. `compiler.dev/pricing` (read 2026-11-10): the trial terms and
the core-minute rate.

The records are `dossier/compute/blacksmith.json`,
`dossier/compute/depot.json`, `dossier/compute/warpbuild.json`,
`dossier/ci-cd-runners/runnerhut.json`,
`dossier/ci-cd-runners/runners-io.json` and
`dossier/ci-cd-runners/compiler-dev.json`.
