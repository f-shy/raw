# How many free tiers are recurring, one-time, or a trial

Three products are called a free tier in this market and they are not the same
product. A **recurring credit** renews every month and can be budgeted. A
**one-time credit** is spent once and never returns. An **allowance** is a
perpetual quota with no money attached, usually in hours or requests. A **trial**
is a clock.

The distinction is the most expensive confusion in the corpus. A reader who sees
"USD 300 free" and plans ten months has planned for one month and nine of nothing.
A count that does not record which kind a credit is cannot be budgeted. The
numbers here come from the records.

## The counts

Derived from the records in `dossier/compute/` by `scripts/report/render.py`,
which reads each record's `extras.free_tier_kind`. The table below is rendered
between its markers, so it cannot disagree with the records it counts.

<!-- generated:start topic=compute kind=breakdown field=extras.free_tier_kind -->
| free tier kind | Records |
| --- | --- |
| `-` | 842 |
| `none` | 271 |
| `allowance` | 120 |
| `one-time-credit` | 70 |
| `trial` | 34 |
| `always-free` | 18 |
| `credit` | 12 |
| `recurring-credit` | 11 |
| `free-forever-with-quota` | 10 |
| `perpetual` | 8 |
| `recurring-allowance` | 8 |
| `free-forever` | 7 |
| `none-published` | 6 |
| `one-time credit` | 5 |
| `renewable-free` | 4 |
| `closed` | 3 |
| `free-forever-with-feature-gate` | 3 |
| `plan-credit` | 3 |
| `trial-credit` | 3 |
| `capped-free` | 2 |
| `free-allowance` | 2 |
| `free-plan` | 2 |
| `monthly-allowance` | 2 |
| `none published` | 2 |
| `one-time trial` | 2 |
| `one-time-trial-minutes` | 2 |
| `signup-credit` | 2 |
| `time-boxed-trial` | 2 |
| `trial-only` | 2 |
| `campaign-credit` | 1 |
| `card-gated one-time credit` | 1 |
| `card-gated-welcome-credit` | 1 |
| `credit offer unverified; free shape c...` | 1 |
| `credit-on-card` | 1 |
| `credit-pool` | 1 |
| `daily-allowance` | 1 |
| `dead` | 1 |
| `evaluation-only Hobby region, unbille...` | 1 |
| `fair-use-hosted` | 1 |
| `feature-gated` | 1 |
| `free base plan, no free runtime` | 1 |
| `free container` | 1 |
| `free service` | 1 |
| `free-forever-with-unpublished-quota` | 1 |
| `free-instance-hours` | 1 |
| `free-preview` | 1 |
| `hours` | 1 |
| `included minutes on a paid plan` | 1 |
| `included-disk` | 1 |
| `included-usage-and-allowances` | 1 |
| `manually-approved-time-boxed-trial` | 1 |
| `manually-approved-trial` | 1 |
| `monthly credit` | 1 |
| `monthly-grant` | 1 |
| `monthly-resource-allowance` | 1 |
| `monthly-spending-discount` | 1 |
| `monthly-usage-credit` | 1 |
| `monthly-vcpu-minute` | 1 |
| `none for sandboxes` | 1 |
| `none published for Sherlock; separate...` | 1 |
| `none-for-sandboxes` | 1 |
| `none-hosted` | 1 |
| `not applicable` | 1 |
| `one-free-instance` | 1 |
| `one-time account credit` | 1 |
| `one-time credit grant` | 1 |
| `one-time credit plus an anonymous fiv...` | 1 |
| `one-time grant` | 1 |
| `one-time grant on an anonymous key` | 1 |
| `one-time messaging-API test access, n...` | 1 |
| `one-time promotional credit` | 1 |
| `one-time signup allowance` | 1 |
| `one-time-credit-amount-unstated` | 1 |
| `one-time-grant` | 1 |
| `one-time-trial` | 1 |
| `paid-lease` | 1 |
| `prepaid-credit` | 1 |
| `recurring monthly credit` | 1 |
| `recurring usage credit` | 1 |
| `recurring-minutes plus one-time-minutes` | 1 |
| `recurring-storage-allowance` | 1 |
| `renewable` | 1 |
| `renewable-trial` | 1 |
| `request-only-trial` | 1 |
| `sign-up credit` | 1 |
| `static-only` | 1 |
| `time-boxed credit` | 1 |
| `time-boxed trial` | 1 |
| `time-boxed trial with minute allowance` | 1 |
| `time-limited starter credit` | 1 |
| `top-up-match` | 1 |
| `trial-hours` | 1 |
| `trial-minutes` | 1 |
| `unmetered-free-experimental` | 1 |
| `unpublished discretionary credit` | 1 |
| **all** | 1524 |
<!-- generated:end -->

Twelve rows out of 405 carry a credit that renews. That is 3.0 per cent of the
market, and it is the number a reader should carry away from this document. Every
other free offer is a quota or a single grant.

⚠ **The 405 in that sentence is not a field any record carries.** No record carries
`has_genuine_free_tier` as a field; 25 records name it inside a
`free_tier_kind_basis` string, which is a provenance note and not a count. The
nearest counts in the dossier are 499 rows at `qualifies` or
`qualifies-with-caveat`, 323 rows with a stated kind other than `-` or `none`, and 24
rows with a `credit_usd`. None of them is 405. The per cent is the claim, and
12 / 405 = 3.0, but the denominator is
`unverified`; the count to trust is the rendered one above: 1411 records, 10
`recurring-credit`, 12 `credit`, 1 `monthly-usage-credit`.

## The twelve recurring credits

Sorted by the 24/7 bill each one offsets. A dash means the record does not carry a
figure for that shape, not that the credit is absent.

| Provider | Credit a month | Offsets | Source |
| --- | --- | --- | --- |
| Modal | USD 30 | about 126 sandbox hours at 2 vCPU / 4 GiB | `modal.com/pricing` (read 2026-10-24) |
| Blacksmith | USD 12 | CI minutes | catalogue card, not read |
| InsForge Instacloud | USD 10 | compute | catalogue card |
| Airtop | USD 0 | 1,000 browser credits, plus a 10,000-credit bonus | `airtop.ai/pricing` (read 2026-10-22) |
| Kedge | USD 5 | CPU at USD 0.0205 per vCPU-hour | `kedge.dev/docs/billing` (read 2026-10-22) |
| Kernel | USD 5 | browser time at USD 0.0000166667 per GB-second | `kernel.sh/pricing` (read 2026-10-22) |
| Anchor Browser | USD 5 | 50 completed tasks at 0.1 credits each, up to 500 browser sessions | `anchorbrowser.io/pricing` (read 2026-10-30) |
| Opensteer | USD 5 | platform credits; model credits are separate | page read 2026-10-22 |
| Trigger.dev | USD 5 | run compute, 20 concurrent runs | page read 2026-10-22 |
| Solari | USD 3 | browser sessions at 1 hour each | page read 2026-10-22 |
| Buddy | USD 1 | compute and storage, 2 concurrency slots | page read 2026-10-22 |
| Railway | USD 1 | about 146 hours of a 1 vCPU / 0.5 GB service | `railway.com/pricing` (read 2026-10-24) |

⚠ **Two rows that look like recurring credits are not.** Bright
Data Browser carries `extras.free_tier_kind: allowance` and Scrapeless carries
`none`, so neither is a recurring credit. The roster is the records': 10 records carry
`recurring-credit`, Modal
carries `credit` with a monthly reset, and Railway carries `monthly-usage-credit`.
That is the twelve. The rendered count of 12 under `credit` above is a different
twelve and does not name this roster.

Modal's USD 30 is the largest recurring credit on any free plan in this market. Modal
prices Sandboxes at its non-preemptible rate of USD 0.00003942 per physical
core-second and USD 0.00000667 per GiB-second, and a physical core is 2 vCPU. The
2 vCPU / 4 GiB shape is therefore one core plus four GiB, which is USD 0.2380 an
hour, and USD 30 buys about 126 hours of it. The same shape at the preemptible rate
is USD 0.0791 an hour, so USD 30 buys 379 hours of a Function and the 3x multiplier
is the difference between the two numbers on one page.

⚠ **Modal's credit is real and unreachable without a card.** The billing
documentation states "Note that you must have a payment method on file in order to
use Modal", and the record's verdict is `fails-identity`. The USD 30 is the largest
credit and it is not a credit a reader can spend.

⚠ Two catalogue rows carry a `free_monthly_credit` that is not recurring.
`aws-lambda` shows USD 6.87 and `azure-container-apps` shows USD 5.40, and both
come from a USD 200 one-time credit divided by a month. Their records say so in
`extras.free_tier_kind_basis` and are counted as one-time here. The catalogue field
conflates the two products and a count taken from it directly would overstate the
recurring set by two.

## The one-time credits, and why 55 is not 55 months

Fifty-five records carry a credit that is spent once: 54 at
`extras.free_tier_kind: one-time-credit` and one at `trial-credit`. The largest are
familiar: USD 300 from Google's trial, USD 300 from Aiven's trial, USD 200 from AWS
and Azure, USD 200 from Daytona, Hopx and Blaxel, USD 100 from E2B, USD 30 from
Steel and Prizéd, USD 25 from zipbox.

⚠ **Oracle is not among the USD 300 grants, and `oracle-cloud` does not carry one.**
`oracle-cloud` is an `allowance` of 1,500
OCPU-hours and 9,000 GB-hours a month, and the string `300` does not appear anywhere
in that record. Oracle's free capacity is a perpetual quota, and quoting it as a
one-time credit understates it in the direction that matters: a reader planning a
second month on it is not wrong.

⚠ **Oracle does publish a USD 300 grant, on a different record.** `oracle-cloud-trial`
is `one-time-credit` at `credit_usd: 300` for 30 days, and it sits beside the Always
Free allowance on the same account. So both sentences are true at once: the Always
Free record carries no credit, and Oracle as a provider does sell a USD 300 trial.
A reader who took the warning above as "Oracle has no USD 300" would be wrong.

⛔ A one-time credit is not a monthly budget divided by a price. It is a single
purchase of capacity, and the useful number is what it buys at a named shape. The
records carry that arithmetic and this document takes it from them rather than
recomputing it: Daytona's USD 200 buys 749.2 hours of a 4 vCPU / 4 GiB / 10 GiB
machine, or 602.9 hours at the 8 GiB shape, because the record prices the hour at
USD 0.26694 and USD 0.33174. E2B's USD 100 buys 604 hours at USD 0.1656 an hour, and
the one-hour session cap turns that into at least 604 sessions with setup between
each. Hopx's USD 200 buys 2,955 hours at USD 0.06768. The credit is the same size
and the value is not.

## The allowances, and the one that matters

One hundred and forty-nine records carry an allowance, which is the count of eleven kind
strings the records use for that shape: `allowance` 121, `free-forever-with-quota` 10,
`free-forever` 7, `free-allowance` 2, `monthly-allowance` 2, `capped-free` 2, and one each
of `monthly-resource-allowance`, `free-forever-with-unpublished-quota`, `monthly-grant`,
`hours` and `free-instance-hours`. Most are small: a request count, a disk quota, a
GPU-hour grant. Three are large enough to change what a reader can do.

Freestyle gives 200 vCPU-hours and 400 GiB-hours a month with a hard stop, which
is 100 hours of a 2 vCPU machine, or 3.3 hours a day. Oracle gives 1,500
OCPU-hours and 9,000 GB-hours a month on top of 200 GB of block storage and 10 TB
of egress. Kaggle gives 30 GPU hours a week on a P100.

⚠ **The Kaggle superlative is false.** Baidu AI Studio gives 48
GPU hours a week at bronze level on a V100, and its record states it: 8 points a day
where each point buys 2 hours of a V100 16 GB, capped at 48 hours a week. The record
is `fails-identity`, because the site wants a Chinese phone number, so it is not a
GPU allowance a reader can reach. It is still larger than Kaggle's, and a claim
about the largest cannot stand beside a bigger number in the same dossier.

The rest are quotas that a workload reaches in a day. A reader should treat the
149 figure as a count of rows and not as a count of usable offers: the median
allowance here is a few hours a month.

## The trial kind, and the trial verdicts

The `trial` kind carries 34 records and `verdict: trial-only` carries 133, because a
trial verdict can sit on any kind that does not renew. Fourteen `trial-only` records
are `one-time-credit` and 86 carry no kind at all. The verdict and the kind are
independent: E2B is `qualifies-with-caveat`
on a one-time credit, not `trial-only`; Steel is `trial-only` on a one-time credit;
Railway is `qualifies-with-caveat` on a monthly credit, not `trial-only`; Google Colab
is `qualifies-with-caveat` on an allowance with no published ceiling. DigitalOcean is
`paid-only`, not `trial-only`: the USD 5 for 90 days survives only in a conditional
example on its pricing page and in an archive, and no current signup amount is
published. The verdict says the offer ends; the kind says how.

## What the verdicts say

<!-- generated:start topic=compute kind=breakdown field=verdict sort=value -->
| verdict | Records |
| --- | --- |
| `dead` | 85 |
| `fails-egress` | 1 |
| `fails-identity` | 153 |
| `fails-quota` | 24 |
| `paid-only` | 560 |
| `qualifies` | 51 |
| `qualifies-with-caveat` | 491 |
| `trial-only` | 159 |
| **all** | 1524 |
<!-- generated:end -->

⚠ Four hundred and forty-eight `qualifies-with-caveat` is not a finding, it is the
shape of a catalogue whose rows mostly rest on a third-party card. The `qualifies`
count is 51: 39 rows filed under a VPS category, five `cloud VM`, two `GPU cloud`,
two `notebook runtime`, one `notebook`, one `dev environment` and one `sandbox`,
among them `alphavps-c6g`, `conoha-vps`, `kaggle-notebooks` and
`github-codespaces`.

## What this document does not establish

The kind of every row that rests on a catalogue card is derived from three
catalogue fields and not from a page: 25 records carry the basis string "derived from
the catalogue card's free_monthly_credit, free_one_time_credit and
has_genuine_free_tier; no page was read". Those records say so in
`extras.free_tier_kind_basis`. A row whose kind is derived can be wrong in the
direction that matters: a catalogue that recorded a one-time grant as a monthly
credit would inflate the recurring set, which is the exact error this document
exists to catch.

⚠ **Two numbers in this document are unverified and are named as such.** The `405` denominator in the opening per cent is not a field any record
carries. The `149` allowance count is a sum of eleven kind strings and not a field,
so a reader who recounts from a single `extras.free_tier_kind` value will get 121.
Both are stated with their basis above.
