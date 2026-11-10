# What can I run, for how long, and what reaps it?

Compute is the only topic in this repository where the price is almost never the
constraint. A sandbox that costs USD 4.76 a month and is killed after fifteen
minutes of silence is worth less to the reader than a free VM that stays up, and
the sheets that rank compute by hourly rate hide that. So every document here
prints two columns, `billed-while-running` and `held-24/7`, and every row names
the clock that stops it.

The answer, in one paragraph. For a machine that stays up for no money, two
remain: Oracle Cloud Always Free (2 OCPU, 12 GB, 200 GB, 10 TB a month
outbound, card and phone at signup), and Google Cloud's e2-micro (1 GB, 30 GB,
and 1 GB of egress a month, which is 0.0067 per cent of one day's 500 GB
serving). Both want a card. A third was the free Lightning AI Studio (24/7 CPU,
no card, restarted every four hours), and the vendor revoked all user access to
the platform on 2026-10-16, so the free lane has no always-on VM that takes an
email address alone. For work that runs in bursts there are a dozen cheap
sandboxes, and the cheapest credible 2 vCPU box is Agent 37 at USD 2.17 a month
at 10 hours a day, of which USD 0.36 is the disk for the month. For a
shell with a cron and no bill there is the pubnix layer, which gives 1 to 3 GB
and an outbound-only network. Everything else in this topic is either a trial, a
credit that does not renew, or a product that has been withdrawn.

## The four questions this topic answers first

| question | the answer | the document |
| --- | --- | --- |
| the beefiest always-on machine under USD 5 a month, as a daily driver | **VolpaByte Ryzen KVM 8 GB at EUR 50.90 a year**: 6 AMD Ryzen vCores, 8 GiB ECC, 100 GB, unlimited traffic, cart-verified; its renewal is not stated. The cheapest 8 GiB is GreenCloudVPS at USD 45.00 a year (4 vCPU / 60 GB), on clearance stock | [`paid/under-five.md`](paid/under-five.md) |
| the beefiest machine under USD 1 a month, as a VPN node or a health monitor | **USD 3.50 a year, USD 0.29 a month**, from Gullo's, which is the only row in the band with a public report of WireGuard running; luo_cloud sells a monthly USD 0.22 box that is thinner still | [`paid/under-one.md`](paid/under-one.md) |
| a credible free tier with no credit card, or a debit card, and no strict ID check | USD 200 of Daytona credit is 31 days of a 4 vCPU VM on an email alone, but Tier 1 egress is restricted; the no-card machine with no clock is still missing | [`free/no-card.md`](free/no-card.md) |
| the cheapest usable Windows machine at 16 GiB, 4 vCPU and 50 GB | **Layer7 AMD Epyc VPS at EUR 9.06 a month (USD 10.14), or EUR 86.97 a year (USD 8.11 a month, USD 97.35 first payment)**, for 4 cores / 16 GiB / 80 GB with a Windows Server Evaluation image. **Saganetwork** is the cheapest row a buyer can start on a monthly term, at USD 8.23 ex VAT and USD 9.88 paid for 6 / 16 / 120, with its Windows path unverified. **Rabisu** is the cheapest row with a Windows image at no surcharge, at USD 10.99 a month or USD 8.79 annual for 6 / 16 / 120, and its licence is unresolved. Then NetVolo USD 13.98, HOSTKEY USD 15.67, Linveo USD 16.00, By-Hoster USD 19.02 with the buyer supplying the licence, Virtarix USD 27.40 with the licence printed, ServerPacket USD 32.19, windowsvps.host USD 36.00, InterServer USD 40.00 and Kimsufi KS-3 USD 64.00 all-in. ⛔ The USD 7 Windows VPS is 2 GiB or 12 GiB. At least 316 distinct provider labels were searched and nothing below USD 8.11 was found. No machine was booted | [`paid/windows-vps.md`](paid/windows-vps.md) |

⛔ **The card is the gate.** A free tier that holds USD 29 on a card, or refuses a
prepaid card, is not free. The hold amount, the accepted instruments and the phone or ID
requirement are in [`free/no-card.md`](free/no-card.md), and every row there names the page
it was read from.


⚠ **The clock column is thinner than it sounds.** Only 67 records state a session cap or
an idle reap as a number: 52 carry a numeric `wall_clock_min` and 24 a numeric
`idle_reap_s`, nine of them both. [`the-clock.md`](the-clock.md) lists the caps and reaps
that exist, and 542 records carry a `session_cap.note`, 475 of them with no number in
either field.
So "the price is almost never the constraint" is this topic's thesis and it is not yet
measured: it rests on a column that is populated on 4.7 per cent of the records.

⭐ **The lane front pages are the fastest route in.** [`free/README.md`](free/README.md)
ranks the free lane by what a reader can obtain tonight, and
[`paid/README.md`](paid/README.md) prices the paid lane at three hold times. Neither
restates the four provider documents it summarises.

## The three facts that decide every recommendation

**A free tier is almost never a machine.** The record set keeps `kaggle` and
`kaggle-notebooks` as two slugs of one provider so a lookup lands on the fact.
Most of the working rows are a credit or an allowance. The largest recurring
credit in this market is Modal's USD 30 a month, and it buys about 126 hours
of a 2 vCPU sandbox. Modal prices a Sandbox at the non-preemptible rate of USD
0.00003942 per physical core-second and USD 0.00000667 per GiB-second, and a
physical core is 2 vCPU, so the 2 vCPU / 4 GiB shape is one core plus four
GiB: USD 0.2380 an hour. The USD 200 and USD 300 grants are one-time.

<!-- generated:start topic=compute kind=totals fields=records,providers,recurring-credit,dead,qualifies labels=records,providers,recurring-credit,dead,qualifies -->
records 1411; providers 1336; recurring-credit 10; dead 84; qualifies 499
<!-- generated:end -->

**The binding constraint is time.** Across the sandbox class, what stops a
workload is a session cap or an idle reap: E2B at 1 hour, Vercel at 45 minutes,
Daytona at 15 minutes idle, Browserbase at 15 minutes, Render at 15 minutes,
Koyeb at 1 hour, Railway's anonymous box at 24 hours, and the free Lightning
Studio at 4 hours until the vendor revoked all user access on 2026-10-16. Money
is secondary and usually absent.

**Egress is the bill nobody publishes.** Five of the eighteen rows in
`paid/egress-and-network.md` publish no per-GB term at all. The serving target
assumed here is 500 GB a day to 1 TiB a day. At the vendor's decimal gigabyte, 500 GB a day
for 30 days is 15,000 GB, which is USD 300 at USD 0.02/GB and USD 1,350 at
USD 0.09/GB. One tebibyte a day for 30 days is 30 TiB, which is 32,986 GB, so it
is USD 660 and USD 2,969. The compute is frequently cheaper than the traffic it
enables.

## The comparison

Sorted by what a reader can use tonight, free lane first. Every row is a record in
`dossier/compute/`. `Identity` is what registration costs. `Binds` is the
constraint that fails first at the assumed scale.

| Provider | Free tier | Binds | Identity | Held 24/7 | Verdict |
| --- | --- | --- | --- | --- | --- |
| Oracle Cloud Always Free | 2 OCPU for 24/7, 200 GB block, 10 TB egress | 7-day idle reclaim at p95 under 20% CPU | card | USD 0 | qualifies-with-caveat |
| Lightning AI | 1 Studio free 24/7, 80 GPU hours to start | 4-hour forced restart; access revoked 2026-10-16 | email | USD 0 | dead |
| Google Cloud Free Tier | 1 e2-micro, 30 GB disk, 1 GB egress a month | 1 GB of outbound a month | card | USD 0 | qualifies-with-caveat |
| Cloudflare Workers | 100,000 requests a day, 10 ms CPU, 128 MB | 10 ms of CPU per request | email | USD 0 | qualifies-with-caveat |
| GitHub Codespaces | 120 core-hours and 15 GB-months a month | 120 core-hours, then blocked without a card | card | USD 120.60 | qualifies-with-caveat |
| Freestyle | 200 vCPU-h and 400 GiB-h a month, hard stop | no persistent VMs and no snapshots on Free | email | USD 96.54 | qualifies-with-caveat |
| Kaggle Notebooks | 30 GPU hours a week on a P100 | 60-minute idle timeout | any-phone | USD 0 | qualifies-with-caveat |
| E2B | USD 100 one-time, 20 concurrent | 1 hour per session | email | USD 120.89 | trial-only |
| Railway | anonymous 2 vCPU / 2 GB, no account | 24 hours to claim, 3 boxes per IP per day | anonymous | USD 1.00 | trial-only |
| Modal | USD 30 a month, recurring | 5-minute default lifetime | email | USD 173.71 | qualifies-with-caveat |
| Agent 37 | USD 5 after a card | disk bills while stopped | card | USD 4.76 | qualifies-with-caveat |
| zipbox | USD 25 after a USD 5 top-up | 80 GB disk, 6 vCPU ceiling | card | USD 10.00 | qualifies-with-caveat |
| boat | none; USD 20 plan is credit | disk deleted 14 days after stop | card | USD 13.14 | qualifies |
| Lizard | 7-day trial, USD 5 of credits | 5-minute SDK default lifetime | card | USD 11.83 | qualifies-with-caveat |
| Hetzner Cloud | none | none; monthly cap | card | USD 6.49 | qualifies |
| Contabo | none | unlimited traffic with no published rate | card | USD 6.60 | qualifies-with-caveat |
| netcup | none | 12-month contract | card | USD 9.50 | qualifies-with-caveat |
| Vercel Sandbox | 5 active-CPU hours a month | 45-minute maximum session | email | USD 248.78 | qualifies-with-caveat |
| Daytona | USD 200 one-time | 15 minutes idle by default | email | USD 120.89 | qualifies-with-caveat |
| Upstash Box | 5 CPU hours a month | 5 GB disk on the entry shape | email | USD 8.00 | qualifies-with-caveat |
| Fly.io | no free tier | trial is 2 hours or 7 days | card | USD 2.19 | dead |
| Run Cloud | withdrawn from new organizations | unreachable | card | USD 0.00 | dead |
| Hugging Face Spaces | static only; compute Spaces need PRO | create-time plan gate | card | USD 9.00 | paid-only |
| SDF Public Access UNIX | 20 MB x4, 500 files | 2-year login expiry | email | USD 0 | qualifies-with-caveat |
| tilde.club | 1 GB soft, 3 GB hard | no idle policy published | email | USD 0 | qualifies-with-caveat |
| hashbang | 512 MB, 50% CPU | 30-day login sweep | email | USD 0 | qualifies-with-caveat |

A dash in `Held 24/7` would mean the number is unknown. Every row above has one
because each record states its own rate.

## What the price columns mean, and why there are two

A sandbox bills only while it runs. A VPS bills whether it runs or not. Print one
column and one of the two is misranked. Contabo's Cloud VPS 4 shows USD 2.71 when
a month is divided by 730 hours and USD 6.60 when the bill is clamped to one
month. Both are true and only one is a bill. `billed-while-running` is the cost of
a workload that runs ten hours a day; `held-24/7` is the cost of a box that must
never stop.

A price here is a triple: a shape, a horizon, and what the number includes. A rate
with no shape is not a price, and `extras.shape` is a shell on most records: 123
carry at least one shape field and 282 carry none at all. Those records are
excluded from every comparison rather than ranked. ⚠ **The shape keys are not
uniform.** 61 records write `ram` and 38 write `disk`, where 23 write `ram_gib` and
22 write `disk_gib`, so a count over the `_gib` spelling alone understates the
coverage by a factor of three. A reader counting shapes must test both.

## The documents

The free lane and the paid lane each have a front page. Read the lane page first
when reading this topic cold.

| Document | Answers |
| --- | --- |
| [`free/README.md`](free/README.md) | what the free lane is, the three kinds of free tier, and what a reader can obtain tonight |
| [`paid/README.md`](paid/README.md) | what money buys, the three hold times, and where the floor is |
| [`the-clock.md`](the-clock.md) | which machines have a deadline, what it is, and why only 67 records state one |
| [`watchlist.md`](watchlist.md) | which third-party sources publish tables of other vendors, and when to re-read each one |
| [`economics.md`](economics.md) | how a free tier is funded, and what the funding model predicts about survival |
| [`free/sandboxes-container-vm.md`](free/sandboxes-container-vm.md) | which sandbox can I hold a session open in tonight, and for how long |
| [`free/sandbox-long-tail.md`](free/sandbox-long-tail.md) | the other 110 sandboxes, by kind, and what a credit actually buys |
| [`free/sandbox-newcomers.md`](free/sandbox-newcomers.md) | what the newer sandboxes charge, and which aggregator tier is missing |
| [`free/always-on-free.md`](free/always-on-free.md) | which free machine answers at 03:00 without a keepalive |
| [`free/anonymous-vms.md`](free/anonymous-vms.md) | what can I get with no account at all |
| [`free/platform-hosts.md`](free/platform-hosts.md) | which free PaaS keeps a process up, and the four that need a cloud account |
| [`free/platform-host-long-tail.md`](free/platform-host-long-tail.md) | the other 15 platform hosts, the eight that need hardware the reader supplies, and the clock none of them states |
| [`free/dev-environments.md`](free/dev-environments.md) | which free IDE or devbox gives a persistent disk |
| [`free/dev-environment-long-tail.md`](free/dev-environment-long-tail.md) | the other 24 dev environments, and the durability axis nobody filled |
| [`free/gpu-notebooks.md`](free/gpu-notebooks.md) | which free GPU exists, in which class, for how many hours |
| [`free/agent-browser-hosts.md`](free/agent-browser-hosts.md) | how many free browser minutes, and what does the proxy cost |
| [`free/browser-host-long-tail.md`](free/browser-host-long-tail.md) | the other 29 browser hosts, and which allowances recur |
| [`free/runtimes-serverless.md`](free/runtimes-serverless.md) | what answers an HTTP request for nothing, and what is the CPU wall |
| [`free/free-tier-census.md`](free/free-tier-census.md) | how many free tiers are recurring, one-time, or a trial |
| [`free/chains.md`](free/chains.md) | which free resources compose into something none gives alone, and the two clocks that break each one |
| [`free/hpc-allocations.md`](free/hpc-allocations.md) | is any national supercomputer open to a person with no institution |
| [`free/research-grids.md`](free/research-grids.md) | which grids and science gateways open on an email address, and how little they award |
| [`free/startup-credits.md`](free/startup-credits.md) | which founder credits one person can reach, and which need a company |
| [`free/research-credits.md`](free/research-credits.md) | which research grants are real, and which need a PI and an institution |
| [`free/decentralized-gpu.md`](free/decentralized-gpu.md) | what the decentralized marketplaces are worth once supply is counted |
| [`free/regional-clouds.md`](free/regional-clouds.md) | what exists outside the US and EU mainstream, and what identity each one wants |
| [`free/asian-clouds.md`](free/asian-clouds.md) | which Chinese, Korean, Japanese and Indian lanes are reachable from outside the country |
| [`free/forum-hosts.md`](free/forum-hosts.md) | what the Chinese, Russian, Korean and Japanese forums offered that an English survey missed |
| [`free/student-and-education.md`](free/student-and-education.md) | which education gate verifies the person and which verifies the institution |
| [`free/perpetual-allowances.md`](free/perpetual-allowances.md) | what renews forever and survives an unattended month |
| [`free/ci-as-compute.md`](free/ci-as-compute.md) | which CI runner is usable as a machine, and which lane the minutes belong to |
| [`free/ai-and-data-credits.md`](free/ai-and-data-credits.md) | what an individual reaches from AI, data, voice and accelerator vendors, and what only a company can claim |
| [`free/devtool-and-platform-credits.md`](free/devtool-and-platform-credits.md) | developer tools, platform hosts, prizes, regional programmes, decentralized networks and open-source funds, cash separated from compute |
| [`paid/micro.md`](paid/micro.md) | the smallest invoice that returns a root shell, and the largest machine USD 2, 5, 10, 20 and 50 buy |
| [`paid/lowend-vps.md`](paid/lowend-vps.md) | the 114 cheap hosts one tracker lists, and the six ways its numbers are wrong |
| [`paid/storage-vps.md`](paid/storage-vps.md) | the cheapest disk per TB per month, and the largest machine at a price |
| [`paid/sandboxes-container-vm.md`](paid/sandboxes-container-vm.md) | the cheapest sandbox per hour at a named shape |
| [`paid/vps-monthly.md`](paid/vps-monthly.md) | the cheapest box that stays up, and what its traffic term is |
| [`paid/cloud-vms.md`](paid/cloud-vms.md) | the free cloud VM tiers, the reclaim clocks, and what traffic out costs |
| [`paid/brokers-and-bare-metal.md`](paid/brokers-and-bare-metal.md) | what a brokered GPU and a whole rented machine cost, and where the price hides |
| [`paid/os-hosts.md`](paid/os-hosts.md) | what a macOS or Windows machine costs, and who gives one away |
| [`paid/windows-vps.md`](paid/windows-vps.md) | the cheapest machine that boots Windows at 16 GiB, 4 vCPU and 50 GB, ranked across sixteen lanes with the licence path in every row, the USD 7 entry plans that miss the RAM floor, and the licence-supplied rows in a second table |
| [`paid/spot-interruptible.md`](paid/spot-interruptible.md) | what interruptible capacity costs, how much notice a reclaim gives, and what a checkpoint must survive |
| [`paid/dev-environments.md`](paid/dev-environments.md) | what a real devbox costs once the free hours are gone |
| [`paid/gpu-rental.md`](paid/gpu-rental.md) | the cheapest card by marketplace, and what preemption costs |
| [`paid/gpu-notebooks.md`](paid/gpu-notebooks.md) | the cheapest GPU hour, by card class |
| [`paid/agent-browser-hosts.md`](paid/agent-browser-hosts.md) | the cheapest browser hour, and what a GB of proxy adds |
| [`paid/minimum-bill.md`](paid/minimum-bill.md) | what a 30-minute run actually costs after rounding and plan floors |
| [`paid/egress-and-network.md`](paid/egress-and-network.md) | what traffic out costs, and who publishes it at all |
| [`paid/ci-adjacent.md`](paid/ci-adjacent.md) | what a CI runner costs per minute, and where that topic owns it |
| [`paid/bursty-workload.md`](paid/bursty-workload.md) | what a run-wait-run workload costs under each billing model |
| [`relay-egress.md`](relay-egress.md) | which machines cannot listen, and whether a relay fixes that |
| [`measurement.md`](measurement.md) | how each number here was obtained, and what was not measured |
| [`dead-ends.md`](dead-ends.md) | the closed doors, with the evidence of closure |
| [`gaps.md`](gaps.md) | the weak claims, the open contradictions, and what rotted |

⭐ **`gaps.md` is the page to read before acting on any number above.** It carries the
claims a plan would rest on, the contradictions in the records, and the four absences
this topic still has: no booted machine, no paid bill, no completed registration, and no
measured throughput.

## What is not here

CI-adjacent compute is the `ci-cd-runners` topic's, and no document here repeats
its numbers. Relays and tunnels are the `egress` topic's, and the one relay measured
for this corpus is in
[`../egress/free/sealed-sandbox-reach-in.md`](../egress/free/sealed-sandbox-reach-in.md).
Hosted inference APIs are the `inference` topic's; one record here
(`inference-api-hosts`) exists only to stop this census counting an API as a
machine.

⭐ **The price columns use the 2 vCPU / 4 GiB shape, and only 12 records carry
that shape explicitly.** That is the scope of every money figure here; the shape is
called `agent`. A 1 vCPU / 1 GiB shape, called `tiny`, is priced for 206 providers
and has no column here. That matters for one reason: the cheapest stock item in the
catalogue is at the tiny shape, not at this one.

Scaleway's STARDUST1-S is 1 vCPU / 1 GiB at USD 0.000683 an hour, which is
USD 0.20 a month at 10 hours a day against USD 6.89 for the same provider at 2 vCPU
/ 4 GiB. That is 34 times cheaper and it is the only machine in this topic under
USD 1 a month. The `scaleway` record carries it in `extras.shape` and
`extras.tiny_m10h_usd`, and the small shape is not an agent sandbox: 1 GiB cannot
hold a browser. Scaleway flags it stock-limited, so it is not guaranteed available.

⚠ **A USD 0.03 a month figure for Scaleway is a shape error.** It is the tiny shape
priced as if it were the comparison shape. At the 2 vCPU / 4 GiB size the rest of
this document compares, Scaleway is USD 6.89 and not the cheapest.

The other shape priced in the catalogue is 4 vCPU / 8 GiB for 202 providers, and
only two records here carry it: boat and Contabo. A reader who needs either of those sizes
should read the record's `extras.shape` rather than this document's money columns.

⛔ The two questions have different answers. The cheapest credible *agent* box is
Agent 37 at USD 2.17 a month, at the 2 vCPU shape this document prices. The
cheapest box of any size is Scaleway's Stardust at USD 0.20 a month, and it is not
an agent box. A reader who quotes the second where the first is meant has made a
shape error.

## How to read the rungs

Every number carries its rung. `measured` means a probe or a fetch recorded the
result. `documented` means a vendor page was read on the date given. `reported`
means the number came from the pinned third-party catalogue
(`ariana-dot-dev/battleships` at commit `f6a71ab0`) and no vendor page was read for
it. Of the 1411 records, 1206 are `documented`, 180 `reported`, 15 `unverified`,
6 `inferred` and 4 `measured`. The `documented` and `measured` records are the ones a
recommendation rests on, and each `unverified` record says why. The counts are rendered
from the records.

<!-- generated:start topic=compute kind=breakdown field=confidence sort=value order=measured,documented,reported,inferred,unverified -->
| confidence | Records |
| --- | --- |
| `measured` | 4 |
| `documented` | 1207 |
| `reported` | 179 |
| `inferred` | 6 |
| `unverified` | 15 |
| **all** | 1411 |
<!-- generated:end -->

## Superseded claims

Figures this document has replaced, with the evidence that replaced them, are dated in
[`compute-seed-claims-superseded.md`](../../history/2026-10-22T030705Z/compute-seed-claims-superseded.md).

## Records that no other document names

This list is generated by `scripts/report/render.py` from the records. It holds each `measured` or
`documented` record of this topic that no other document of `docs/` names, so a reader
finds it and the gate's `links` check counts it as cited. A document that names the record
removes its row at the next render.

<!-- generated:start topic=compute kind=uncited -->
Every `measured` or `documented` record of this topic is named by a document.
<!-- generated:end -->
