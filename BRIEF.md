# BRIEF.md — the slow state of this corpus

It answers three questions: **what is covered**, **what is settled** and **what is
dead**, with the checks that are red on `main`. It is not a tutorial (that is
`METHODOLOGY.md`), not a router (that is `AGENTS.md`), and not the findings
themselves (those are in `docs/`).

⛔ **Every fact here is a pointer, not a home.** When this file states a number,
the number's owner is the dossier record cited beside it. If the two disagree, the
dossier wins and this file is the defect.

**Corpus state:** fifteen topics. The table of section 2 is generated from
`dossier/` and is current; `scripts/rq context TOPIC` prints a topic's counts.

---

## 1. What the corpus prices, in numbers

The corpus assumes no local hardware and no institutional login, and prices only
free, trial and cheapest-paid capacity. Every resource it records belongs to
somebody else.

**The target is every cheap resource, not storage.** The table below is the
storage-shaped part of the need. A free GPU hour, a working email sender, a
managed Postgres and 100 GB of object storage are findings of the same rank.

| resource | the shape of the need |
|---|---|
| Hot working set | ~10 TiB stored, read and written often |
| Serving | 500 GB – 1 TiB of egress per day, HTTP GET, cacheable |
| Cold archive | 20 TiB, growing, write once, rare read |
| Compute | something that stays up; a sandbox for an agent; GPU time |
| Inference | a model that answers without a card |
| The rest | egress, email, DNS, databases, CI runners, credentials — each a blocker when it costs money |

**The rules that shape every verdict.**

⛔ **Owning hardware is never an option, and self-hosting is the last resort.** The
corpus prices no hardware purchase. A rented or managed box with a monthly
invoice is a service and is often the answer; a box that must be bought, housed and
powered is not an option. Software installed and run by the reader, also on a
rented or free machine, comes after every hosted offer and is never the answer
while a hosted one exists, never starred or ranked first.

Hard filters for **storage**: a reachable interface (S3 / REST / WebDAV / SFTP /
OCI / Git / a protocol a wrapper could speak); free or Cloudflare-covered egress;
registrable by somebody with an email address at most.

**Identity is the binding constraint on almost every large quota.** A 100 TB
allowance behind an institutional login is worth zero, and a document that quotes
it without saying so has misled its reader. Every record carries `identity_cost`.

**Out of scope, permanently:** the published conditions and legality. Account
closure, throttle and data-loss are recorded as one-line technical reliability
notes.

---

## 2. What is covered

Every count in this table is generated from `dossier/` by `scripts/report/render.py`
and is authoritative. Never type into it: a hand-written count is a defect
waiting to happen, and `render.py --check` refuses one.

<!-- generated:start kind=topics link=1 -->
| topic | records | qualifies | trial or paid | fails | dead | measured or documented | documents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`ci-cd-runners`](docs/ci-cd-runners/README.md) | 34 | 23 | 7 | 1 | 3 | 34 | 7 |
| [`coding-subs`](docs/coding-subs/README.md) | 50 | 26 | 20 | 2 | 2 | 50 | 8 |
| [`compute`](docs/compute/README.md) | 1411 | 499 | 653 | 175 | 84 | 1211 | 63 |
| [`crawler-scraper`](docs/crawler-scraper/README.md) | 61 | 40 | 10 | 3 | 8 | 57 | 15 |
| [`data-apis`](docs/data-apis/README.md) | 155 | 127 | 8 | 12 | 8 | 153 | 1 |
| [`databases-kv`](docs/databases-kv/README.md) | 23 | 18 | 2 | 0 | 3 | 23 | 10 |
| [`debrid`](docs/debrid/README.md) | 526 | 316 | 108 | 50 | 52 | 467 | 19 |
| [`dev-services`](docs/dev-services/README.md) | 61 | 55 | 4 | 2 | 0 | 61 | 1 |
| [`domains-dns`](docs/domains-dns/README.md) | 33 | 26 | 5 | 1 | 1 | 29 | 6 |
| [`egress`](docs/egress/README.md) | 458 | 62 | 168 | 204 | 24 | 312 | 20 |
| [`email`](docs/email/README.md) | 38 | 25 | 10 | 3 | 0 | 37 | 5 |
| [`inference`](docs/inference/README.md) | 108 | 40 | 46 | 10 | 12 | 104 | 11 |
| [`ip-proxy`](docs/ip-proxy/README.md) | 87 | 23 | 49 | 9 | 6 | 80 | 10 |
| [`netdisk-pan`](docs/netdisk-pan/README.md) | 104 | 54 | 4 | 32 | 14 | 58 | 22 |
| [`storage`](docs/storage/README.md) | 1720 | 383 | 137 | 1092 | 108 | 173 | 29 |
| **all** | 4869 | 1717 | 1231 | 1596 | 325 | 2849 | 227 |
<!-- generated:end -->

---

## 3. What is settled

The headlines a reader needs before reading anything else. Each one is a pointer.

### 3.1 Free capacity that survives contact

| provider | the offer | what binds it | identity | record |
|---|---|---|---|---|
| Cloudflare Pages | 488 GiB × 100 projects | `per-object-cap` 25 MiB, and a mean object size of ≥10.49 MiB or the total collapses | email | `dossier/storage/cloudflare-pages.json` |
| BigFile.net | no account, no quota | `per-object-cap` 256 GB, sliding 365-day retention | **anonymous** | `dossier/storage/bigfile-net.json` |
| Internet Archive | 1 TB per item, unlimited items | `per-ip-shaping` ~150 GB/day/stream-IP | email | `dossier/storage/internet-archive.json` |
| Zenodo | 50 GB per record inside a shared 150 GB pool | `write-gated`: a DOI mints on publish and files are then immutable outside a 30-day window | email | `dossier/storage/zenodo.json` |
| GitHub Releases | no total cap, ~1.95 TiB per release | `per-object-cap` 2 GiB | email | `dossier/storage/github-releases.json` |

### 3.2 Free WireGuard ingress

A WireGuard endpoint needs one UDP port, so any free UDP forward is a WireGuard
ingress provider. The topic answers that question directly.

| provider | the offer | what binds it | identity | record |
|---|---|---|---|---|
| ROUTE64 | a routed IPv6 `/56` over WireGuard | `none`: no byte meter, 200 Mbit/s design | email | `dossier/egress/route64-org.json` |
| portwarp | one UDP port, one tunnel | `per-ip-shaping`: "unlimited", no published tolerance | email | `dossier/egress/portwarp.json` |
| playit.gg | anycast custom UDP | `per-ip-shaping`: 1 to 2 TB/day tolerated, one operator | email | `dossier/egress/playit-gg.json` |
| TCPShield Sentry | any TCP or UDP over VXLAN | `volume-quota`: 1.0 TB/month, and Sentry on Free is unstated | email | `dossier/egress/tcpshield.json` |
| Oracle Always Free | a VM with a public IP | `volume-quota`: 10 TB/month, card at signup | card | `dossier/egress/oracle-always-free.json` |

⭐ **TCPShield is the free row whose published cap falls short of 1 TiB**: 1.0 TB a
month is 0.909 TiB. Oracle publishes 10 TB a month behind a card. The rows with no
published cap are the ones that clear the bar, and none of them can be designed against.
Read [`docs/egress/free/wireguard-ingress.md`](docs/egress/free/wireguard-ingress.md).

### 3.3 The cheapest paid lane
Free is not the only answer, and it is often not the best one.
The finding is *free where free wins, paid where it does not*.

| provider | cost | the catch | record |
|---|---|---|---|
| Hetzner Storage Box BX41 | EUR 40.60/mo for 20 TB, excl. VAT | card and KYC | `dossier/storage/hetzner-storage-box-bx41.json` |
| 1fichier GOLD | ~EUR 108/yr for 10 TB cold | retention if dormant | `dossier/storage/1fichier-premium-gold.json` |

This table is illustrative, not complete. The full lane is in
[`docs/storage/paid/`](docs/storage/paid/README.md).

### 3.4 The seven constraints that reframe most findings

1. **`request-rate`** — a count per unit time, often monthly.
2. **`pull-count`** — a cap on fetches of a stored object.
3. **`per-ip-shaping`** — throughput or daily volume attached to the caller.
4. **`per-object-cap`** — the largest single object, which sets the shard size.

Three more, each one a way the marketing number is defeated:

5. **`write-gated`** — a curator, review, build recipe or phone PIN between the
   caller and a write.
6. **`retention-clamped`** — the server quietly shortens what was requested.
   Client-side limits are worthless as evidence.
7. **`volume-quota`** — a byte allowance per period for the whole account, such as
   1 TB a month. It is not `per-object-cap`, which is one object.

The vocabulary is defined in `dossier/README.md`; the discipline for applying it
is `METHODOLOGY.md`.

### 3.5 The rules

In `METHODOLOGY.md`. Read them before the first probe.

### 3.6 Retrieval: what a byte costs

The `debrid` topic answers the same question as storage for the opposite
direction: not where bytes live, but what it costs to pull them.

| provider | the offer | what binds it | identity | record |
| --- | --- | --- | --- | --- |
| TorBox Essential | USD 3.00/month, 200 GB per object, WebDAV | `per-object-cap` | email | `dossier/debrid/torbox-essential.json` |
| 115 traffic pack | CNY 38.88/TB at the 100 TB pack | - | `country-phone(+86)` | no record holds the pack: `docs/debrid/free/chinese-retrieval.md` |
| UsersDrive free | 73 GB/day, 1.99 TiB a month | `retention-clamped` at 11 days | email | `dossier/debrid/usersdrive.json` |
| PikPak | 6 GB free, 10 TB at about USD 20 to 58 a year | `per-object-cap` | email | `dossier/debrid/pikpak-free-download.json` |
| XS News block | EUR 59.95 per 5 TB, no expiry | `volume-quota` | card | `dossier/debrid/xs-news.json` |
| CoolSpeeds | USD 0.036/GB | a crypto-only rail | email, not confirmed | `dossier/debrid/coolspeeds-com.json` |

⭐ **For nothing, the no-card ladder reaches 1,116 GB in month one and 1,046 GB in
month two** from fourteen signups. Month one clears 1 TiB by 16.5 GB and rests on
three unproven assumptions.

⛔ **Price is not the first gate. The caller's address is.** Five of the nine
best-known multi-hosters refuse datacenter, VPS, proxy or cloud addresses, and
every machine the corpus can rent is one of those.

### 3.7 The credit ladder, ranked

The ranking, the hourly rate each balance sustains, and the 24/7 machine each one
buys are in [`docs/compute/free/credit-ranking.md`](docs/compute/free/credit-ranking.md).
**Modal and Northflank are card-gated**, and **Daytona's USD 200 is one month at
4 GiB and 25 days at 8 GiB**, with Tier 1 egress restricted.
[`history/2026-10-24T025000Z/card-gate-and-verdicts.md`](history/2026-10-24T025000Z/card-gate-and-verdicts.md)
records the correction.

| provider | balance | clock | identity | record |
| --- | --- | --- | --- | --- |
| Snowflake | USD 400 | 30 days | email | `dossier/compute/snowflake.json` |
| CockroachDB Cloud | USD 400 | not stated | email or SSO | `dossier/databases-kv/cockroachdb-basic.json` |
| Databricks | up to USD 400 | 14 days of access | email | `dossier/compute/databricks.json` |
| Modal | USD 30 a month, renewing | monthly | card | `dossier/compute/modal.json` |
| Google Cloud | USD 300 | 90 days | card | `dossier/compute/google-cloud-trial.json` |
| Oracle Cloud | USD 300 | 30 days | card, not prepaid | `dossier/compute/oracle-cloud-trial.json` |
| ClickHouse Cloud | USD 300 | 30 days | email, card unstated | `dossier/compute/clickhouse-cloud.json` |
| Aiven | USD 300 | 30 days | email | `dossier/compute/aiven.json` |
| Civo | USD 250 | 31 days | card, verified before use | `dossier/compute/civo.json` |
| Vultr | USD 250 | 30 days | card, promo code | `dossier/compute/vultr.json` |
| Northflank | USD 20 a month, renewing | monthly | **card, per the billing docs** | `dossier/compute/northflank.json` |
| Deepgram | USD 200 | none while the account lives | email only | `dossier/compute/deepgram.json` |
| Daytona | USD 200 | **not published**; 31 days at 4 vCPU / 4 GiB | email for tier 1, egress restricted | `dossier/compute/daytona.json` |
| OVHcloud | USD 200 | 1 month | card | `dossier/compute/ovhcloud.json` |
| IBM Cloud | USD 200 | 30 days | card | `dossier/compute/ibm-cloud.json` |
| E2B | USD 100 | none stated | email only | `dossier/compute/e2b.json` |
| Speechmatics | USD 100 | none stated | email only | `dossier/compute/speechmatics.json` |
| Anyscale | USD 100 | none stated | work email | `dossier/compute/anyscale.json` |
| Kamatera | up to USD 100 | 30 days | card | `dossier/compute/kamatera.json` |
| Zylora | USD 100 | 6 months | review, or card for USD 25 | `dossier/compute/zylora-startup-gpu.json` |

⛔ **Azure and AWS are excluded from this ladder.** Both were refused at signup,
so their credit balances are unreachable capacity, not findings. The same applies
to every AWS offer: the AWS Free plan in section 3.8 is listed as `documented`,
not as reachable, until its signup is settled.

⭐ **Six document no card:** Snowflake, CockroachDB, Databricks, Deepgram, Aiven and
Speechmatics. **One renews:** Modal at USD 30 a month, and it is card-gated, so the renewal
is not reachable without a payment method on file. Northflank's USD 20 is the only offer here
that runs a service indefinitely, and its billing docs require a payment method on every plan.
⚠ **`dossier/README.md` owns the numbers; this table is a view.** The two rates that are
derived rather than published are IBM's per-profile rate and Google's `e2-standard-2` rate,
and both say so where they are used. Confluent Cloud publishes USD 400 and is excluded
because its storage record carries `fails-quota`.

### 3.8 Four compute questions, answered

The table answers four compute questions from vendor pages and cart charges rather
than aggregator cards. Every row is priced through the vendor's own **"Order now"**
link, and [`history/2026-10-24T064000Z/`](history/2026-10-24T064000Z/cart-audit-four-corrections.md)
records the four published recommendations the cart contradicted.

| question | answer | document |
| --- | --- | --- |
| ten free tiers a reader can sign up for | Nine that are reachable, and the AWS Free plan, which is not. [`docs/compute/shortlist.md`](docs/compute/shortlist.md) — molab (4 CPU / 32 GiB), GitHub Actions (4 vCPU / 16 GiB), Kaggle (4 cores / 30 GiB), **AWS Free plan (`t4g.small`, 2 vCPU / 2 GiB, 750 h/mo, no card — "No credit card is required for most new customers")**, which is not reachable: AWS refused the signup (section 3.7, #58), Daytona (USD 200 = 31.2 days of a 4 vCPU / 4 GiB VM, no card), Opus Host (1 GiB KVM with IPv4, no card), Oracle (card, **hold not published**), EUserv (IPv6 only), Silly Development, freeshell.de (42 GB + a listening port, gated on a **postcard**). **No provider in this corpus places a USD 50 hold**; the largest found is Infomaniak at CHF 20, then Koyeb at USD 29 | [`docs/compute/shortlist.md`](docs/compute/shortlist.md) |
| the beefiest always-on machine under USD 5 a month | **VolpaByte Ryzen KVM 8 GB, 6 AMD Ryzen vCores / 8 GiB ECC / 100 GB / unlimited traffic at EUR 50.90 a year**, cart-verified with a cookie jar. ⚠ Its renewal is not stated; EUR 4.99 monthly is the only evidence for month 13. **AlphaVPS C6G** (3 vCPU / 6 GiB / 55 GB / 6 TB, same EUR 50.90) is the pick when a **written** renewal matters — it says "LOCKED AT RENEWAL, FOREVER" three ways, but only 2 of 7 locations are in stock. ⛔ ColoCrossing's USD 3.33 8 GB reads **"orders have been suspended"**; GreenCloudVPS at USD 3.75 publishes **no renewal**, and the "USD 40.00/mo list, 10.7×" claim is **withdrawn as unverified** | [`docs/compute/paid/under-five.md`](docs/compute/paid/under-five.md) |
| the beefiest machine under USD 1 a month | **DediRock Promo Special NY at USD 0.82** — 2 GiB / 1 vCPU / 30 GB / 2 TB / **dedicated IPv4**, cart verified in a browser at **USD 9.88/yr**; the only sub-dollar row with a routable v4. **TierHive Micro at USD 0.10** for a monitor (no payment instrument at all). ⚠ DediRock's renewal is not published; VDS6 (2 GiB at USD 0.49) renders **"0 available"** | [`docs/compute/paid/under-one.md`](docs/compute/paid/under-one.md) |
| the cheapest usable Windows VPS or remote machine at 16 GiB RAM, 4 vCPU and 50 GB | **Layer7 AMD Epyc VPS at EUR 9.06/month (USD 10.14), or EUR 86.97/year (USD 8.11/month, USD 97.35 first payment)**, for 4 cores / 16 GiB / 80 GB with a Windows Server Evaluation image on the OS list. **Saganetwork VDS-16GB** is the cheapest row a buyer can start on a monthly term: USD 8.23 ex VAT and USD 9.88 paid, for 6 / 16 / 120, with its Windows path unverified. **Rabisu Aydin VPS x16** is the cheapest row with a Windows image at no surcharge, at USD 10.99/month or USD 8.79/month annual, for 6 / 16 / 120, and its licence is unresolved. Then **NetVolo at USD 13.98** billed for three years, **HOSTKEY at USD 15.67** with the licence sold separately, **Linveo at USD 16.00**, **By-Hoster at USD 19.02** with the buyer supplying the licence, **Virtarix at USD 27.40** with the licence printed at USD 16.00 inside the price, **ServerPacket at USD 32.19**, **windowsvps.host at USD 36.00**, **InterServer at USD 40.00** and **Kimsufi KS-3 at USD 64.00 all-in**. ⛔ The USD 7 Windows VPS is real but is 2 GiB or 12 GiB, not 16 GiB. A USD 40.00 floor that priced only provider-supplied licences is withdrawn. A sweep of at least 316 distinct provider labels found nothing below USD 8.11. No machine was booted | [`docs/compute/paid/windows-vps.md`](docs/compute/paid/windows-vps.md) |

⭐ **A page price is not a cart price.** Nine hosts advertised one price and charged
another, and three of those charged a *monthly* rate where the page quoted an
*annual* one. `docs/compute/shortlist.md` carries page price and cart price in
separate columns for that reason, and a row only counts as working when the cart
prices the plan.

⭐ **NAT and IPv6-only are covered.** The picks are **DeluxHost at USD 0.50/mo** for
IPv6-only with a /64 and all ports open, and **Skhron at EUR 1.69 + EUR 0.65** for
an IPv4 add-on with a routed /64 and a free /56.

⭐ **Old seasonal pages: 11 tested, 41 order links, one seller.** No Black Friday
page works. RackNerd's `/specials/` is the one long-lived sale page that works end
to end (all five pids price their own plan); DediRock's cheap SKU is alive but the
Black Friday page links to the wrong one.

⭐ **The cheap-paid floor is USD 3.75.** `paid/micro.md` lists eight machines below
USD 5, and the front page names the row. The earlier USD 6.49 claim is withdrawn;
[`history/2026-10-24T021500Z/`](history/2026-10-24T021500Z/under-five-floor-corrected.md)
records it.

### 3.9 Exit identity: what the upstream sees

The question is which source of IP addresses lets a Cloudflare-Workers-hosted
service reach an upstream that refuses Cloudflare's own ranges, for free or for the
least money. The topic is organised by **what the upstream keys on**, not by vendor
type, because a provider is not good or bad — it is a defence against a specific
keying strategy.

| rung | what the upstream counts | defeated by | status here |
| --- | --- | --- | --- |
| 2 | one address | any new address | measured; the gateway holds 102 relays for this |
| 3 | a subnet | an address in a different subnet | **inferred, never caught in the wild** |
| 4 | the ASN | a different network | measured |
| 5 | the registration class | an ISP-registered prefix | **2 of 6 vendors pass a registry check** |
| 6 | the account | a new account | measured (Meta, ZAI) |
| 7 | the client fingerprint | a different client stack | measured (OC-Free) |

⭐ **A non-Cloudflare exit from a Worker exists and is measured.** Proton
WireGuard inside a Worker exits from `149.50.216.236` = **AS212238 CDNEXT
Datacamp**, HTTP 200, 2026-10-03T19:09:40Z, captured in the gateway's own log. It is a
*hosting* ASN, so it buys rung 4 and refuses rung 5.

| finding | the number | record |
| --- | --- | --- |
| Cloudflare's egress pool spans three ASNs, and the caller cannot choose | AS13335, AS14789, AS132892, all Cloudflare, Inc.; a draw lands in one at random | `docs/ip-proxy/techniques.md` |
| the free `/48` does not defeat rotation | Meta's own IMC 2020 paper finds the `/48` closest to IPv4 in user-population size (a rate-limiting input) and recommends the full address or `/64` for blocklisting | `docs/ip-proxy/free/prefix-leases.md` |
| free proxy lists decay in minutes | 35 of 100 carried a payload at t0; **10 of those same 35 at +22 minutes** | `dossier/ip-proxy/monosans-proxy-list.json` |
| the cheapest per-address ISP rate | **USD 0.30/IP** at Webshare; USD 0.27 at Decodo | `dossier/ip-proxy/webshare-static-residential.json` |
| a VPN buys ASNs, not servers | Windscribe **58 ASNs** on a **USD 39/yr** plan; NordVPN 7,193 servers over **25** ASNs | `dossier/ip-proxy/windscribe-vpn.json` |
| the same hosting ASN recurs across vendors | AS212238 Datacamp is **26.5%** of the 1,720 prefixes measured, and it is the measured Proton exit | `docs/ip-proxy/paid/vpn-exits.md` |

⛔ **Two premises are wrong, and both matter.** First, the gateway does *not*
record that "rotation buys nothing"; it records three different things, and
rotation works against an address-keyed vendor. Second, residential proxy at
USD 0.80/GB is **USD 36 a month** at a volume of about 41.8 GiB (45 GB decimal),
not the USD 26,388 that `dossier/egress/residential-proxy-trial.json` implies.
That record's arithmetic is right for a 1 TiB/day workload, not for this one.

⛔ **The transport does not select the egress ASN.** A paired 12-draw test showed
both transports drawing from one pool with overlapping addresses, so the ASN is a
property of the draw and not of the road.
[`history/2026-10-24T111500Z/transport-does-not-select-asn.md`](history/2026-10-24T111500Z/transport-does-not-select-asn.md)
records the refuted claim.

---

## 4. What is dead

The dead ends live in the topic documents and in `dossier/` with
`verdict: dead`. This section records only the **classes** that are closed:

- **Institutional research clouds** (CSC Allas, LUMI-O, OSN, and the national
  Dataverse nodes) — the quota is real and the identity is unreachable. Closed by
  `fails-identity`, permanently.
- **Large consumer drive quotas obtained by stacking accounts** — Google Drive
  service accounts now report `limit: 0`; the class is dead, not the provider.
- **Free IPFS pinning** as bulk storage — the free ceiling is a few GiB and the
  pinning services churn. Dead as a *bulk* answer, alive as a redundancy layer.
- **Repository-as-blob-store** (commits, LFS, repo files) — 1–5 GB per repo, and
  the commit-message mechanism reaches ~0.9 GB/day. Dead at the scale this corpus prices.
- **Free tiers of the hyperscalers** — 5–20 GB. Not a mistake, but irrelevant.

The per-provider list, with reasons and evidence, is in
[`docs/storage/free/`](docs/storage/free/README.md) and the `dead_ends` sections
of the topic documents. It runs to several hundred entries.

---

## 5. Known red checks

⚠ **The gate is red on `main` on `staleness` and `sources`, and both checks depend on the clock.**

`sources` goes red when a registered list is past its cadence, which is one, seven or
fourteen days. On 2026-11-10 nine lists are: six in `scripts/sources/debrid-aggregators.tsv`
(`lowendbox-com-24`, `lowendtalk-com-26`, `world-debrid-com`, `reddit-com`, `reddit-com-37`
and `reddit-com-39`), one in `scripts/sources/egress-aggregators.tsv` (`lowendtalk`) and two in
`scripts/sources/ip-proxy-aggregators.tsv` (`monosans-proxy-list` and `cn-proxy-forums`). A
list clears when it is diffed and the new `last_diff` is committed
(`docs/research-protocol.md` section 2, "A registered provider list is updated by the
parent"). `python3 scripts/sources/aggregator-diff.py --root . --registry FILE --check` names
the lists past their cadence in one registry. A change that touches no list leaves this red
line as it is.

`staleness`: CI's gate prints the count (in an own clone, `sh scripts/gate.sh --root . --check staleness`), and
`python scripts/dossier/staleness.py dossier/ --stale-only` names the records; the `flags` column
says why. A record past its `verified_at` window, or with no fresh evidence (`evidence-past-limit`),
clears when its sources are re-read and the record confirmed; re-dating a record without that is the bulk
touch the check exists to catch. ⚠ A record flagged `evidence-past-topic` does not clear that way: its
oldest evidence row is older than the topic allows, and rows are only added. Five compute
records are of that kind. Whether a newer row of the same URL retires the old one is undecided.
Issue #4 holds the re-check of the storage records, which are most of the count.
CI tests each pushed head with `scripts/rq gatecmp` against the base it resolves; a pull request from a fork starts nothing.

⚠ **The count grows with the as-of date.** In an own clone, `sh scripts/gate.sh --root . --check staleness --as-of DATE` gives 3
records on 2026-10-28, 6 on 2026-11-04, 1,465 on 2026-11-05 and 1,677 on 2026-11-10.

### Known soft spots

Places where the corpus knows it is thin. These are honest gaps, not oversights:

- A `measured` number inherited from a source in `sources/SEED.md` is `documented` at best
  until re-run here.
- Public AList/OpenList instances have a half-life measured in months. Any list
  of them is a snapshot.
- Free inference endpoints change weekly. A document older than a month is a
  hypothesis.
- Prices for the cheap-paid lane are a snapshot with no feed behind them.
