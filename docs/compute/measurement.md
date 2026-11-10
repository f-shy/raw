# How each number here was obtained, and what was not measured

Every claim in this topic carries one rung of the evidence ladder, and the
counts below are rendered from the records rather than typed.

<!-- generated:start topic=compute kind=totals fields=records,reported,documented,measured,unverified labels=records,reported,documented,measured,unverified -->
records 1411; reported 179; documented 1207; measured 4; unverified 15
<!-- generated:end -->

The `reported` rows came from a pinned third-party catalogue and no page was
opened for them. The `documented` rows had a vendor page read and the sentence
quoted. The `unverified` row says why in the sentence that states the claim.

⚠ **Four records carry `measured`, and none of them measures a quota.** A probe
proves that a socket opened and a banner arrived. It does not prove the quota, the
retention clock or the registration gate, and those are the fields each verdict here
rests on. `METHODOLOGY.md` section 3.1 takes the weakest field, so a record with a
measured reachability and a documented quota is a `documented` record carrying a
probe. The pubnix records carry the saved probe plus a `confidence_note` that says
why the rung is `documented`.

That distribution is the first thing a reader should know. A catalogue inherited
without re-reading each page is not a measurement, and calling it one would be the
single most expensive thing this document could do.

## What was actually measured

Twelve SSH endpoints were dialled, one connect and one banner read each. The run is
saved as `sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json`, written by
`scripts/probe/tcpprobe.py`, and every record that cites a probe cites that file.
A connect time that is not in the file is a number nobody can check.

Twelve endpoints, the saved run:

| Host | Port | Result |
| --- | --- | --- |
| tilde.green | 22 | connect 0.30 s, banner `SSH-2.0-OpenSSH_10.6p1 Debian-1` |
| ctrl-c.club | 22 | connect 0.32 s, banner `SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.18` |
| hashbang.sh | 22 | connect 0.35 s, no banner within 6 s |
| tilde.zone | 22 | connect 0.38 s, banner `SSH-2.0-OpenSSH_10.0p2 Debian-7+deb13u4` |
| tilde.guru | 22 | connect 0.41 s, no banner within 6 s |
| serv00.com | 22 | connect 0.51 s, banner `SSH-2.0-OpenSSH_9.9 FreeBSD-20250219` |
| sdf.org | 22 | connect 0.56 s, banner `SSH-2.0-OpenSSH_10.4` |
| tilde.town | 22 | connect 0.56 s, banner `SSH-2.0-OpenSSH_10.0p2 Debian-7+deb13u4` |
| tilde.club | 22 | connect 3.69 s, banner `SSH-2.0-OpenSSH_10.0` |
| railway.new | 22 | timeout at 8.1 s, DNS resolves to 66.33.22.2 |
| blinkenshell.org | 2222 | timeout at 16.2 s |
| blinkenshell.org | 22 | timeout at 16.0 s |

⚠ **The connect time is a property of the path, not of the host, and this run
proves it.** A second run recorded tilde.town at 7.49 s where this run records
0.56 s, and tilde.club at 4.51 s where this run records 3.69 s. The
same eight hosts appear in both runs and the order changes. So no record here
states a connect time as a host property: the records carry the banner and the
reachability, and the times above are printed once, as one run's raw output, for a
reader who wants to see the spread.

⭐ **The Railway result is the one that changed a finding.** The anonymous-VM row
was `banner-verified` from a relay. From a normal host on this network the port does
not answer, twice, while eight other SSH hosts answer on the same machine. That is
not proof that Railway is down, and it is proof that a relay's verification does not
transfer to a direct connection.

⚠ A timeout is a fact about the path, not about the provider. It is recorded as
`unverified: no TCP answer from this host` rather than as a dead endpoint. The
difference matters: a provider recorded dead on a filtered port is deleted from a
recommendation for the wrong reason.

⛔ **A probe does not earn the `measured` rung on its own.** It proves that a
socket opened and a banner arrived. It does not prove the quota, the retention
clock or the registration gate, and those are the fields each of these records'
verdicts actually rests on. Under `METHODOLOGY.md` section 3.1 the weakest field
decides, so the pubnix records are `documented`, not `measured`, and each one
carries a `confidence_note` that says so.

## What was read, and how

Ninety-one pages were read through the read broker on 2026-10-22 between 02:16Z and
02:35Z. Each capture is a Markdown rendering of the page with its own
`fetched_at`, and each record's `evidence[]` names the URL, the date and the
specific sentence the read established.

The read broker is not the origin. It returns a rendering, and a rendering can drop
a table that a browser would show. Two pages in this topic rendered without the
table they exist for: `hetzner.com/cloud/` returned the prose and none of the price
table, and `vast.ai/pricing` returned the tier descriptions and no card prices. In
both cases the record carries a gap rather than a number, and the gap names what
would fill it.

## What was not measured, and why

| Item | Why | What would close it |
| --- | --- | --- |
| whether any free tier works after signup | no account was created, and none can be | one signup, then a probe against the API |
| Railway's anonymous VM from a residential IP | port 22 timed out from this network | one `ssh railway.new` from a home connection |
| egress on nine of the leaders | the pricing pages do not carry the term | a per-provider read of the egress or fair-use page |
| the disk term on zipbox, Agent 37 and Upstash | not stated on the page read | the provider's terms page, or a support answer |
| Blinkenshell reachability on port 2222 | two timeouts from this host | a dial from another network |
| Vast.ai card prices | rendered client-side, not extracted | an API call or a browser render |
| whether Lizard enforces the Small shape at create time | the sizes API returns 401 unauthenticated | an authenticated create |
| the Google Cloud Run grant's meter | not resolved by any read so far | the Instances section and its footnotes |
| throughput from any provider | no object was transferred | a ranged-GET benchmark with a baseline |

## The four fields the schema was missing

The schema had no field for network policy, session caps, volume durability or
egress. All four are now schema fields, and they are populated where a page or a
card answered them rather than on every record.

**Session cap.** `extras.session_cap` carries the wall-clock cap, the idle reap and
whether a restart is required, with a note where the provider publishes nothing.
This is the axis that decides usability.

**Persistent storage.** `extras.persistent_storage` carries what survives a stop,
what survives a destroy and the maximum retention. The distinction between the last
two is what separates boat's 14-day clock from Agent 37's disk that lives until
deleted.

**Network out.** `extras.network_out` carries whether outbound is allowed, whether
inbound listening is possible, the ports, and the per-session byte cap. It is
answered for the records that were read and carried as a gap for the rest. The three
counts below are rendered from the records.

<!-- generated:start topic=compute kind=totals fields=has:extras.network_out,has:extras.session_cap,has:extras.persistent_storage labels=network_out,session_cap,persistent_storage -->
network_out 298; session_cap 542; persistent_storage 77
<!-- generated:end -->

**Egress.** The schema has an `egress` field, structured rather than the string
`"egress unpublished"` that many rows carried. The `paid/egress-and-network.md`
document is the view.

## The finding the older records could not carry

Modal began charging for network egress on 2026-10-01, three weeks before the read
that recorded it. Records written before that date carry no egress term for Modal
because there was none, and a reader working from one would price a Modal workload
at zero.

That is the mechanism the staleness policy exists for. The compute topic's window
is 45 days, and a three-week-old change is inside it and still changes a
recommendation.

## The records behind these claims

Every `documented` record in this topic, generated from the records so the index
cannot drift from them. A reader who disputes a number here starts at its row.

⚠ **This index is not decoration; it is also the citation.** The gate's links
check matches a record slug against the text of `docs/`, using a pattern that
requires a hyphen, so a single-word slug such as `modal` or `vultr` can never match
however often a document names it. Listing every verified record here is what keeps
those records cited, and the alternative would be renaming a slug, which is a
breaking change.

<!-- generated:start topic=compute kind=provider confidence=documented sort=slug -->
| provider | offer | verdict | confidence | per-object cap | retention | identity | record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1517 Medici Project | 'We give $1k cash grants to students and pe... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/1517-medici-project.json` |
| 24fire | no free tier; the Boerse rotates a small se... | qualifies-with-caveat | documented | not applicable: the unit is a m... | '100% zwanglos dank P... | email | `dossier/compute/24fire-kvm-borse-xeon-8gb.json` |
| 56IDC.Net / 无聊云 | No free tier. 玩具荷兰NAT2 is CNY 10.00 a year,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the page states '不支持任... | card | `dossier/compute/56idc-toy-nl-nat2.json` |
| 56IDC.Net (无聊云) | No free tier. The toy NAT line is CNY 10.00... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the container persist... | email | `dossier/compute/56idc-toy-vps-nat-384.json` |
| 62yun | no free tier; promo-S is RUB 239 a month, a... | qualifies-with-caveat | documented | not applicable: the unit is a m... | disks persist while t... | email | `dossier/compute/62yun-promo-vds.json` |
| Abeiyun | The vendor withdrew the free cloud server o... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/abeiyun.json` |
| ABLENET VPS | A ten-day free trial on every Linux plan, w... | trial-only | documented | not applicable: the unit is a m... | The trial is ten days... | card | `dossier/compute/ablenet-vps.json` |
| ACCESS | Explore ACCESS provides up to 400,000 ACCES... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/access.json` |
| AccuWeb Hosting | no free tier; VPS Mellite is USD 79.99/mont... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/accuweb-windows.json` |
| AceCloud | No standing free tier. The L40S page says n... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/acecloud.json` |
| Adaptable | nothing reachable: every path on adaptable.... | dead | documented | not applicable: the service doe... | the free Starter plan... | email | `dossier/compute/adaptable.json` |
| AdminVPS | Seven days of any VPS tariff free, obtained... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/adminvps.json` |
| Aeza | no free tier; the smallest general plan is... | paid-only | documented | not applicable: the unit is a m... | hourly or monthly bil... | email | `dossier/compute/aeza.json` |
| Aéza | no free tier; the entry shared plan is 'WAW... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/aeza-waws-1.json` |
| AffordableBytes | EUR 3.49 per month for the Xeon Gold 6150 e... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/affordablebytes.json` |
| Agency Tool Company | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/agency-tool-company.json` |
| Agent 37 | USD 5 of credit after adding a card; no per... | qualifies-with-caveat | documented | not applicable: the unit is a m... | disk billed while you... | card | `dossier/compute/agent-37.json` |
| Agent Relay | free to start and free to connect agents, w... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/agent-relay.json` |
| Agent37 | Add a card from the billing page (nothing i... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Stopped or sleeping i... | card | `dossier/compute/agent37.json` |
| AgentComputer | no free tier: pay-as-you-go at $0.07 a CPU-... | paid-only | documented | not stated | not stated | email | `dossier/compute/agentcomputer.json` |
| AI Grant | The page still advertises '$5,000 - $50,000... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ai-grant.json` |
| AI Horde | Text and image generation on volunteer GPUs... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/ai-horde.json` |
| AI Singapore | Co-funding of up to SGD 150,000 per project... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/ai-singapore.json` |
| AIcrowd | Sponsored compute credits for competition e... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/aicrowd.json` |
| AIMO Prize | USD 10,000,000 fund, quoted: 'XTX Markets h... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/aimo-prize.json` |
| ainclave | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/ainclave.json` |
| AirCloud | Hourly GPU rental with published per-model... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/aircloud.json` |
| Aircloud (aircloud.dev) | no free credit or trial is stated on the pa... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/aircloud-dev.json` |
| Airtop | Free at $0/mo with 1,000 credits a month pl... | dead | documented | not stated | not stated | email | `dossier/compute/airtop.json` |
| Aiven (USD 300 trial) | New accounts include $300 in free credits a... | trial-only | documented | not applicable: the offer is a... | 30 d | email | `dossier/compute/aiven.json` |
| Akamai EdgeWorkers | "Both EdgeWorkers and EdgeKV offer a free p... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/akamai-edgeworkers.json` |
| Akash Network | 'USD 1 in free credits - enough to run your... | trial-only | documented | not applicable: the unit is a m... | The USD 1 credit and... | email | `dossier/compute/akash-network.json` |
| AlbaHost | Geolocated AL 1 at EUR 6 per month: 1 core... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/albahost.json` |
| ALCC | ALCC allocates 10% to 30% of the allocatabl... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/alcc.json` |
| ALCF Director's Discretio... | A rolling award available year-round, usual... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/alcf-director-s-discretionary.json` |
| AlexHost | EUR 6.00/month for U1 in Moldova: 1 vCore,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/alexhost.json` |
| Alfred P. Sloan | 'The Foundation does not make grants to ind... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/alfred-p-sloan.json` |
| Alibaba Cloud AgentBay | the Basic plan is free and pays only for re... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/alibaba-agentbay.json` |
| Alibaba Cloud Agent Sandb... | no credit and no free compute; the only fre... | qualifies-with-caveat | documented | not stated | not stated | national-id | `dossier/compute/alibaba-agentrun.json` |
| Alibaba Cloud ESA | The Entrance plan is a permanently free tie... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/alibaba-cloud-esa.json` |
| Alibaba Cloud International | On 2026-10-23 the international free-trial... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/alibaba-cloud-international.json` |
| Alibaba Cloud Model | A new account gets an independent free quot... | trial-only | documented | not applicable: the unit is a m... | the 90-day expiry bin... | card | `dossier/compute/alibaba-cloud-model.json` |
| Alibaba Cloud (Simple App... | no free tier on the international site; the... | qualifies | documented | not applicable: the unit is a m... | the instance and its... | card | `dossier/compute/alibaba-swas-intl.json` |
| AllHost | BLACK FRIDAY GENOA [1,1,16] at GBP 19.00 pe... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/allhost.json` |
| AlphaVPS | Entry plan c2g: 2 GB ECC DDR4, 2 vCPU on In... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/alphavps.json` |
| AlphaVPS | No free tier. The entry plan C2G is EUR 2.5... | paid-only | documented | not applicable: the unit is a m... | The server persists w... | email | `dossier/compute/alphavps-c2g.json` |
| AlphaVPS | no free tier; the ladder starts at EUR 2.54... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/alphavps-c6g.json` |
| Aluy | Custom VPS at the configurator's minimum: E... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/aluy.json` |
| alwaysdata | 0 EUR a month for life: 1 GB of SSD, 256 MB... | fails-quota | documented | not applicable: the unit is a m... | 120 d | email | `dossier/compute/alwaysdata.json` |
| Amazon Alexa Prize | Each selected university team receives a re... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/amazon-alexa-prize.json` |
| Amazon EC2 Spot | The AWS Free Tier is now a plan with an ins... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/amazon-ec2-spot.json` |
| Amazon Polly | 'For Amazon Polly's Standard voices, the fr... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/amazon-polly.json` |
| Amazon Q Developer | Amazon Q Developer Free Tier: "Included age... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/amazon-q-developer.json` |
| Amazon SageMaker Studio | no free tier available: 'Amazon SageMaker S... | dead | documented | not applicable: the unit is a s... | not applicable: no ne... | email | `dossier/compute/amazon-sagemaker-studio.json` |
| AWS Free Tier | up to USD 200 in credits over 6 months: USD... | trial-only | documented | not applicable: the unit is a m... | 180 d | email | `dossier/compute/amazon-web-services-free-tier.json` |
| AMD Developer Cloud | 25 hours of complimentary cloud credit, sta... | trial-only | documented | not applicable: the unit is a m... | Two destruction trigg... | card | `dossier/compute/amd-developer-cloud.json` |
| AMD Radeon Cloud | AMD runs two sites. On the China site the A... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/amd-radeon-cloud.json` |
| AMD University Program | Node-hour allocations on a cluster of dual... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/amd-university-program.json` |
| Amika | $50 of credits per organisation, unlimited... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/amika.json` |
| Amp Orbs | no free tier: orbs bill by the minute from... | paid-only | documented | not stated | not stated | email | `dossier/compute/amp.json` |
| Anchor Browser | Free plan: 5 credits per month, 0.1 credits... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/anchor-browser.json` |
| Anthropic AI | 'If successful, we will apply up to $20,000... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/anthropic-ai.json` |
| Anyscale | USD 100 of credit on a new account, from 'G... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/anyscale.json` |
| ApexWeave | 'a 14-day live trial plus a 120-day grace p... | trial-only | documented | not applicable: the unit is a m... | the free window is a... | email | `dossier/compute/apexweave.json` |
| Apoxy | a free plan during an invite-only beta, req... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/apoxy.json` |
| Appish | Free plan, quoted: '1 slot', '4 hours each,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | a free slot expires a... | email | `dossier/compute/appish.json` |
| Apply.Build | 'Free tier: 0.5 vCPU and 512 MiB' and 'No c... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/apply-build.json` |
| Aptible | no free tier is published: deployment runs... | paid-only | documented | not stated | not stated | email | `dossier/compute/aptible.json` |
| Aquanode | no free tier or free credit is stated on th... | paid-only | documented | not applicable: the unit is a m... | a stopped pod keeps i... | email | `dossier/compute/aquanode.json` |
| ARC Prize Foundation | '$2M in prizes. 3 tracks. Open source progr... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/arc-prize-foundation.json` |
| Archal | $20 in free usage, no card: $5 at signup an... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/archal.json` |
| ARCHER2 Pump Priming | Pump Priming is always open and awards a ma... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/archer2-pump-priming.json` |
| Archil | Free includes 5 disks of up to 10 GB each,... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/archil.json` |
| Arct Cloud | USD 3.89 per month for cvm.pico in the Cost... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/arct-cloud.json` |
| ArenaStreaming | No free tier. LXC NAT Basic is Rp10.000,00... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the container persist... | email | `dossier/compute/arenastreaming-lxc-nat-basic.json` |
| Arga Labs | service twins that are short-lived or perma... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/arga-labs.json` |
| Arker | no free tier: the product is priced as a mu... | paid-only | documented | not stated | not stated | email | `dossier/compute/arker.json` |
| Arm Virtual Hardware | A free trial that is documented with real n... | trial-only | documented | not applicable: the unit is a m... | 100 core hours inside... | email | `dossier/compute/arm-virtual-hardware.json` |
| Artillery | Free tier with the quota row reading 'no li... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/artillery.json` |
| Arvan Cloud | Quoted, translated from Russian: free produ... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/arvan-cloud.json` |
| ASCS Cloud (AS Computer S... | Quoted from the plan card: 'Free', 'renew e... | qualifies-with-caveat | documented | not applicable: the unit is a c... | 30 d | email | `dossier/compute/ascs-cloud.json` |
| AsiaVM (PT Media Creative... | No free tier. The 1 GB Hetzner plan is USD... | dead | documented | not applicable: the unit is a m... | annual prepay; no del... | card | `dossier/compute/asiavm-nat-eu-hetzner-1gb.json` |
| AssemblyAI | '$50 in free credits at signup, no credit c... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/assemblyai.json` |
| Atlantic.net | USD 1.668 per GPU-hour on demand for AL40S.... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/atlantic-net.json` |
| Atomic_Net | 2GB Premium VPS at USD 8.00 per month (the... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/atomic-net.json` |
| Augment Code | no free tier: Standard is USD 20 a month in... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/augment-code.json` |
| AutoComputer | no free tier: the last published price list... | paid-only | documented | not stated | not stated | email | `dossier/compute/autocomputer.json` |
| AutoDL | Retail per-hour GPU rental with no minimum... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/autodl.json` |
| AvaHost | VPS One at EUR 5.00 per month, 1-month term... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/avahost.json` |
| AvenaCloud | KVM VPS/VDS 10 at EUR 5.50 per month, or EU... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/avenacloud.json` |
| Avian Compute | No free tier and no credit on the compute p... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/avian-compute.json` |
| Avoro | Basic S at EUR 4.07 per month excluding VAT... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/avoro.json` |
| AwardSpace | Free plan, quoted: 'Storage: 1 GB', 'Bandwi... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/awardspace.json` |
| AWS Academy | 'AWS Academy provides higher education inst... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/aws-academy.json` |
| AWS Activate, Founders | The Activate Founders tier offers USD 1,000... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/aws-activate-founders.json` |
| AWS Activate, Portfolio | The Activate Portfolio tier offers up to US... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/aws-activate-portfolio.json` |
| AWS Amplify Hosting | Free Tier for 12 months: 1,000 build minute... | trial-only | documented | not applicable: the unit is a m... | the 12-month clock en... | card | `dossier/compute/aws-amplify-hosting.json` |
| AWS Cloud Credit | 'Student awards will be up to a maximum of... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/aws-cloud-credit.json` |
| AWS Cloud Credits | 'we've provided AWS Promotional Credits to... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/aws-cloud-credits.json` |
| AWS Educate | 'AWS Educate is open to any individual, reg... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/aws-educate.json` |
| Amazon Web Services (Free... | Quoted from the t4g page: 'Free Trial: Try... | qualifies-with-caveat | documented | 750 hours a month of t4g.small,... | 'After your free acco... | email | `dossier/compute/aws-free-plan-t4g.json` |
| AWS Lambda | 400,000 GB-seconds and 1 million requests a... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/aws-lambda.json` |
| AWS Lightsail | The Linux/Unix general purpose ladder now s... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/aws-lightsail.json` |
| AWS Trainium Frontier | The organiser supplies the silicon, quoted:... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/aws-trainium-frontier.json` |
| Amazon WorkSpaces Persona... | 5 Performance AutoStop Ubuntu WorkSpaces wi... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/aws-workspaces.json` |
| Axelera AI Voyager | A free assistant for Axelera's Voyager SDK,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/axelera-ai-voyager.json` |
| Axion.host | USD 5.99 per month for AX-v1 in Frankfurt:... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/axion-host.json` |
| Axivora Cloud | No free tier. MCI-N-B is EUR 1.25 a month:... | qualifies-with-caveat | documented | not applicable: the unit is a m... | no retention statemen... | email | `dossier/compute/axivora-mci-n-b-ipv6.json` |
| Axivora Cloud (AXIVORA CO... | No free tier. MCI-N-C is EUR 1.25 billed qu... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Quarterly prepay; the... | email | `dossier/compute/axivora-mci-n-c-ipv6.json` |
| AyooCloud | A 24-hour trial of the entry plan, Ayoo VPS... | fails-identity | documented | not applicable: the unit is a v... | A trial machine is su... | national-id | `dossier/compute/ayoo-cloud.json` |
| Azion | The Hobby plan is free with all platform fe... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/azion.json` |
| Azure | 'Free monthly amounts of 20+ popular servic... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/azure.json` |
| Azure App Service (F1) | F1 Free Shared: 60 CPU minutes a day, 1 GB... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the app and its files... | card | `dossier/compute/azure-app-service-f1.json` |
| Azure Container Apps (Con... | per subscription per month: 'The first 180,... | qualifies-with-caveat | documented | not applicable: the unit is a r... | ephemeral storage per... | card | `dossier/compute/azure-container-apps.json` |
| Azure Container Apps Sand... | no sandbox-specific free allowance is publi... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/azure-container-apps-sandboxes.json` |
| Microsoft Dev Box (closed... | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/azure-dev-box.json` |
| Azure Functions | "Consumption plan pricing includes a monthl... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/azure-functions.json` |
| Microsoft Azure GPU VMs | USD 200 of Azure credit for 30 days on a ne... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/azure-gpu.json` |
| Azure Pipelines | one Microsoft-hosted CI/CD job with 1,800 m... | qualifies-with-caveat | documented | 60 minutes per Microsoft-hosted... | not stated | card | `dossier/compute/azure-pipelines.json` |
| Azure Research Credits | The vendor page offers no amount at all. It... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/azure-research-credits.json` |
| Azure Virtual Machines (L... | no free allowance for a Linux VM; the USD 2... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/azure-vm.json` |
| Azure Virtual Machines (W... | 750 hours each of B2ts v2, B2pts v2 and B2a... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/azure-windows.json` |
| AZVPS | no free tier; VPS Cheap 1 at 63.750 VND a m... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | any-phone | `dossier/compute/azvps-cheap-2.json` |
| BageVM | Los Angeles TINY at USD 2.99 per month (the... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/bagevm.json` |
| Baidu PaddlePaddle AI | '每日运行项目即送8点算力，可使用高级GPU V100 16GB算力运行16小时':... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/baidu-paddlepaddle-ai.json` |
| BandwagonHost | The host most often named in Chinese-langua... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/bandwagonhost.json` |
| Baponi | Free forever, no card: 1,000 credits a mont... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/baponi.json` |
| Baseten | No free tier, no credit and no trial on the... | paid-only | documented | not applicable: the unit is a s... | not applicable: no fr... | card | `dossier/compute/baseten.json` |
| Beam | No signup credit. 'Developer $20/month $20... | paid-only | documented | A persistent VM is 'from $0.030... | A stopped VM keeps it... | card | `dossier/compute/beam.json` |
| Beget | A perpetual free shared-hosting account: 1... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/beget.json` |
| Bentaus | no free tier and no credit on the B300 page... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/bentaus.json` |
| BERO HOST | No free tier. The provider's forum post adv... | dead | documented | not applicable: the unit is a m... | the vendor's IPv6 lin... | email | `dossier/compute/bero-host-ipv6-anniversary-xs.json` |
| Beyond.pl | no free tier or credit is stated on the GPU... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/beyond-pl.json` |
| Bitbucket Pipelines | 50 build minutes a month on the Free plan,... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/bitbucket-pipelines.json` |
| Bitrise (mobile CI) | a Free plan with build credits for a small... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/bitrise.json` |
| Bittensor | Permissionless GPU network of 128 subnets w... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/bittensor.json` |
| Bizfly Cloud | A 3-day free trial of one Cloud Server at u... | trial-only | documented | not applicable: the unit is a m... | The server trial is t... | country-phone | `dossier/compute/bizfly-cloud.json` |
| Black Forest Labs | Pay-as-you-go credits with a published calc... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/black-forest-labs.json` |
| Blacksmith (GitHub Action... | 3,000 free minutes a month on every plan th... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/blacksmith.json` |
| Blaxel | 'Up to $200 in free credits' on the pay-as-... | qualifies-with-caveat | documented | No per-sandbox vCPU or memory c... | 7 d | email | `dossier/compute/blaxel.json` |
| Blinkenshell | 100 MB disk quota, 128 MB memory limit, SSH... | fails-identity | documented | not applicable: the unit is a m... | no expiry is publishe... | any-phone | `dossier/compute/blinkenshell.json` |
| boat | No signup credit. 'Your first plan starts w... | paid-only | documented | Sizes: 'small 2 vCPU / 4 GB / 1... | 14 d | card | `dossier/compute/boat.json` |
| Bolt | Bolt Free: "Monthly AI Tokens 1M", "Daily T... | qualifies | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/bolt.json` |
| Botkeep | A perpetual free container that runs 24/7 w... | qualifies-with-caveat | documented | not applicable: the unit is a m... | An inactivity rule th... | email | `dossier/compute/botkeep.json` |
| boxd | €30 of free credits to start; RAM is billed... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/boxd.json` |
| BoxedTux | A free student vServer: '1 vCPU', '1 GB DDR... | fails-identity | documented | not applicable: the unit is a v... | 'Renew each semester... | institution | `dossier/compute/boxedtux.json` |
| boxes.dev | Trial plan, $0: 20 hours of compute include... | trial-only | documented | not stated | not stated | email | `dossier/compute/boxes-dev.json` |
| BoxLite Cloud | USD 100 in free credits, so you can build a... | paid-only | documented | per-box ceiling of 4 vCPU, 32 G... | Around 10 GiB of real... | card | `dossier/compute/boxlite-cloud.json` |
| BoxyBSD | Personal plan: EUR 0 a month for 1 vCPU, 1... | qualifies-with-caveat | documented | not applicable: the unit is a v... | Quoted: 'BoxyBSD rese... | email | `dossier/compute/boxybsd.json` |
| Bpifrance | A grant of 'un montant maximum de 30 000 EU... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/bpifrance.json` |
| Bright Data Browser API | a recurring 5,000 credits a month with 1 GB... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/bright-data-browser.json` |
| Brimble Sandboxes | a Free plan at $0/mo for hobby projects; th... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/brimble.json` |
| Browser Use | USD 15 of one-time credit; browsers cost US... | trial-only | documented | not applicable: the unit is a m... | credits never expire;... | email | `dossier/compute/browser-use.json` |
| BrowserAct | 200 free credits on signup, 2 free agent bu... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/browseract.json` |
| Browserbase | Free: 3 concurrent browsers, 1 browser hour... | trial-only | documented | not applicable: the unit is a m... | session recordings an... | email | `dossier/compute/browserbase.json` |
| BrowserCloud | 1 browser-hour on the free tier, against 12... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/browsercloud.json` |
| Browserless | Free plan at USD 0 a month, no card require... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not stated in catalog... | email | `dossier/compute/browserless.json` |
| Buddy Sandboxes | a free tier with 2 concurrency slots, 1 sea... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/buddy.json` |
| Buildkite | Quoted from the Free plan: 'Up to 5 users',... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 'Once the job is comp... | email | `dossier/compute/buildkite.json` |
| Buildkite hosted agents | a Free plan with no card: up to 10 concurre... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/buildkite-hosted.json` |
| BulkVM | Starter at USD 5/month: 1 vCore Intel, 1 GB... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/bulkvm.json` |
| Bullethost | Linux I at EUR 4.99/month: 2 vCores, 4 GB R... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/bullethost.json` |
| Bulutova | no free tier; the ladder starts at 99.83 TL... | fails-identity | documented | not applicable: the unit is a m... | the disk persists whi... | national-id | `dossier/compute/bulutova-vps-8.json` |
| Bunny Sandbox | A sandbox billed at Magic Containers rates:... | trial-only | documented | not applicable: the unit is a m... | The trial ends at 14... | email | `dossier/compute/bunny-sandbox.json` |
| BuyVM | SLICE 512: 1 core at 3.50+ GHz with fair-sh... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/buyvm.json` |
| BuyVM | no free tier; the ladder starts at 'SLICE 5... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/buyvm-slice-2048.json` |
| BuyVM | No free tier. SLICE 512 is USD 24.00 a year... | paid-only | documented | not applicable: the unit is a m... | The slice persists wh... | email | `dossier/compute/buyvm-slice-512.json` |
| By-Hoster | no free tier; Windows - Plus is EUR 16.99 a... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/by-hoster-windows.json` |
| ByteVirt (ByteVirt LLC) | No free tier. NAT-512-LXC is USD 7.70 a yea... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 3 d | card | `dossier/compute/bytevirt-nat-512-lxc.json` |
| C-Servers | no free tier; the ladder runs from USD 2.39... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/c-servers.json` |
| C-Servers (Centerfield Ltd) | no free tier; the category's smallest rung... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/c-servers-extravps-6144-ddr5.json` |
| C-Servers (Centerfield Ltd) | no free tier; the category's smallest rung... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/c-servers-extravps-6144-ddr5-nj.json` |
| C-Servers | no free tier; the cheapest server on this p... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/c-servers-nanovps.json` |
| C-Servers | No free tier. NanoVPS-384 Low-Cost Special... | qualifies | documented | not applicable: the unit is a m... | 7 d | card | `dossier/compute/c-servers-nanovps-384-us.json` |
| Cafe24 virtual server | The entry shape is KRW 9,000 a month includ... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/cafe24-virtual-server.json` |
| CamberCloud Student plan | Quoted from the pack changelog dated August... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cambercloud-student-plan.json` |
| CambridgeNexus | no free tier, no trial and no published rat... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cambridgenexus.json` |
| Capy | no free tier: the entry offer is $1 for 7 d... | paid-only | documented | not stated | not stated | card | `dossier/compute/capy.json` |
| Cartesia | Free plan at USD 0 with '20K credits / mont... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cartesia.json` |
| Caution | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/caution.json` |
| CDTI Neotec 2026 | Subsidies of up to 70 percent of the eligib... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cdti-neotec-2026.json` |
| Celesto Cloud | a one-time $5 runtime credit valid for 30 d... | trial-only | documented | not stated | not stated | email | `dossier/compute/celesto.json` |
| centron | a starting credit of EUR 200 for new accoun... | trial-only | documented | not applicable: the unit is a m... | not stated on the pag... | email | `dossier/compute/centron.json` |
| CepatCloud.id | A perpetual free VPS: 15 GB SSD, 1 core, 2... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/cepatcloud-id.json` |
| Cerebras Inference | No recurring free allowance. The FAQ reads:... | trial-only | documented | not applicable: the unit is a m... | the 30-day credit exp... | card | `dossier/compute/cerebras-inference.json` |
| Cerebras Inference Research | 'Selected Principal Investigators (PIs) may... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cerebras-inference-research.json` |
| Cerebrium | a Free tier priced as 'Free + compute a mon... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/cerebrium.json` |
| Chameleon Cloud | "Chameleon operates on a 'soft allocation m... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/chameleon-cloud.json` |
| Cheap-Host | no free tier; NAT Start is 59 RUB a month | qualifies-with-caveat | documented | not applicable: the unit is a m... | 1 d | email | `dossier/compute/cheap-host-nat-start.json` |
| Cheap-Host | No free tier. NAT Start is 59 RUB a month:... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 3 d | email | `dossier/compute/cheap-host-nat-start-de.json` |
| Chronicle Labs | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/chronicle-labs.json` |
| Chunkserve | Xeon Standard 1 at EUR 1.30/month: 1 vCPU X... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/chunkserve.json` |
| Chutes | The free tier is retired. Announcement quot... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/chutes.json` |
| CINECA ISCRA | ISCRA Class C awards up to 10,000 GPU hours... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cineca-iscra.json` |
| Cinfu (Closco Ltd) | No free tier. The German IPv6-only ladder s... | dead | documented | not applicable: the unit is a m... | billed monthly throug... | email | `dossier/compute/cinfu-ex2de-ipv6.json` |
| CircleCI | free tier published without a credit amount | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/circleci.json` |
| Cirrus CI | The allowance was real and is now gone. Quo... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cirrus-ci.json` |
| Cirrus Runners | none: Cirrus Runners is a subscription of $... | dead | documented | not stated | not stated | email | `dossier/compute/cirrus-runners.json` |
| Cirun | Quoted from the Open Source plan: 'Always f... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/cirun.json` |
| Civo Compute | USD 250 in credits on signup: 'You are enti... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/civo.json` |
| Claude Managed Agents | no compute tier: the product is priced per... | paid-only | documented | not stated | not stated | email | `dossier/compute/claude-managed-agents.json` |
| Claw 2 Agent | no free tier: a reviewed Cloud Pilot progra... | paid-only | documented | not stated | not stated | email | `dossier/compute/claw2agent.json` |
| ClawCloud | Withdrawn. The operator published a shutdow... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/clawcloud.json` |
| Clever Cloud | no free tier on the pricing page: every run... | paid-only | documented | not applicable: the unit is a s... | an FS Bucket can be m... | card | `dossier/compute/clever-cloud.json` |
| ClickHouse Cloud | Pricing page, quoted: 'Start free with $300... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/clickhouse-cloud.json` |
| Clore.ai | No free credit. Quoted: 'Create an account... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/clore-ai.json` |
| cloud.mu | Rs279/month for 1 CPU vCore, 1 GB, 32 GB SS... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cloud-mu.json` |
| Cloud.ru Evolution | RUB 4,000 starter grant credited when the f... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/cloud-ru-evolution.json` |
| CloudAxis | Free at $0 with 50 AI credits, 10 cloud bro... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/cloudaxis.json` |
| CloudBlast | VMA11 at EUR 3.6/month or EUR 0.0058/hour:... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cloudblast.json` |
| CloudBrowser AI | a 7-day free trial on the Basic plan and a... | trial-only | documented | not stated | not stated | email | `dossier/compute/cloudbrowser.json` |
| CloudCone | no offer: the URL resolves to an editorial... | dead | documented | not applicable: the unit is a m... | not applicable; there... | card | `dossier/compute/cloudcone-black-friday.json` |
| CloudCone | no free tier; SSD VPS 1 is USD 2.33 a month... | qualifies | documented | not applicable: the unit is a m... | the VPS persists whil... | card | `dossier/compute/cloudcone-ssd-vps-1.json` |
| CloudCone | no free tier; the smallest plan is 'SSD VPS... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/cloudcone-ssd-vps-2.json` |
| CloudCone | no free tier; WC2-3 is USD 62.75/month, and... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/cloudcone-windows.json` |
| CloudCruise | 2 automation hours of workflow runtime, the... | trial-only | documented | not stated | not stated | email | `dossier/compute/cloudcruise.json` |
| Cloudfanatic (formerly Se... | no free tier; the 1 GB standard plan is USD... | qualifies | documented | not applicable: the unit is a m... | the VPS persists whil... | card | `dossier/compute/cloudfanatic-standard-1gb.json` |
| Cloudflare Browser Run /... | Workers Free includes 10 minutes of browser... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/cloudflare-browser.json` |
| Cloudflare Containers | no free plan: the pricing table's Free row... | paid-only | documented | largest instance type standard-... | billing stops when th... | card | `dossier/compute/cloudflare-containers.json` |
| Cloudflare Durable Objects | 13,000 GB-seconds of Durable Object duratio... | qualifies-with-caveat | documented | not applicable: the unit is a m... | SQLite-backed storage... | email | `dossier/compute/cloudflare-durable-objects.json` |
| Cloudflare Containers (fr... | Cloudflare's machine product is paid; the f... | paid-only | documented | not applicable: the unit is a m... | not applicable: no fr... | card | `dossier/compute/cloudflare-egress-only.json` |
| Cloudflare Project Alexan... | 'Project Alexandria, our open source credit... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/cloudflare-project-alexandria.json` |
| Cloudflare Sandbox SDK /... | no free tier: the Free plan row reads N/A f... | paid-only | documented | not stated | not stated | email | `dossier/compute/cloudflare-sandbox.json` |
| Cloudflare Workers | Workers Free: 100,000 requests a day, 10 ms... | qualifies-with-caveat | documented | not applicable: the unit is a m... | a Worker holds no dis... | email | `dossier/compute/cloudflare-workers.json` |
| Cloudflare Workers AI | A daily allowance of 10,000 Neurons on both... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cloudflare-workers-ai.json` |
| Cloudflare Workers for Pl... | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/cloudflare-workers-for-platforms.json` |
| CloudGPU | no free tier and no signup credit: a prepai... | paid-only | documented | not applicable: the unit is a m... | Destroying an instanc... | email | `dossier/compute/cloudgpu.json` |
| Clouding.io | A 1 GB cloud server at EUR 0.004/hour cappe... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/clouding-io.json` |
| CloudLab | CloudLab gives free bare-metal nodes with n... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cloudlab.json` |
| Cloudnium LLC | No free tier. IPv6-1 is USD 1.50 a month: 1... | qualifies | documented | not applicable: the unit is a m... | monthly billing; the... | email | `dossier/compute/cloudnium-ipv6-1.json` |
| CloudRift AI Grant | USD 100 to USD 1,000 in GPU compute credits... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cloudrift-ai-grant.json` |
| CLOUDV | The MAXIO Linux virtual server is 1 core, 2... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/cloudv.json` |
| CloudVPS | A 7-day free VPS test: fill in a form with... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/cloudvps.json` |
| Cloudzy | no free tier; the 16 GB Windows VPS is USD... | trial-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/cloudzy-windows.json` |
| Clusy | $0/mo tier with 1 concurrent sandbox; Plus... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/clusy.json` |
| CoalByte Cloud | 'Starte deinen garantierten kostenlosen Ser... | qualifies-with-caveat | documented | 'Jeder Benutzer erhält bei der... | not published for the... | email | `dossier/compute/coalbyte-free.json` |
| Coasty | $5 of credit at signup on a $0.05-a-managed... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/coasty.json` |
| CoCalc | a free trial project with no expiry, descri... | fails-quota | documented | not applicable: the unit is a s... | trial projects do not... | email | `dossier/compute/cocalc-free.json` |
| Codeberg Forgejo Actions | 'The following runners are available on Cod... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not stated on the pag... | email | `dossier/compute/codeberg-forgejo-actions.json` |
| Codemagic (mobile CI) | the managed hosted Patch service is free be... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/codemagic.json` |
| CodeSandbox | CodeSandbox Free: "Every Free workspace get... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/codesandbox.json` |
| CodeSandbox SDK | catalogue documentation records a free mont... | trial-only | documented | not applicable: the unit is a m... | hibernation stops com... | email | `dossier/compute/codesandbox-sdk.json` |
| Codesphere | A Free plan at USD 0 that publishes exactly... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/codesphere.json` |
| Cohere trial keys | A trial (evaluation) key is free but limite... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cohere-trial-keys.json` |
| Cohesivity | Free tier is a metered monthly bucket on ho... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cohesivity.json` |
| Collimate | a free demo key with no card: 2 concurrent... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/collimate.json` |
| ColoCrossing | no free tier; the specials store's cheapest... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/colocrossing-8gb-annual.json` |
| ColoCrossing | no free tier; the page advertises yearly VP... | dead | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/colocrossing-cyber-monday.json` |
| Comfy Deploy | a free starting tier priced as credits; GPU... | qualifies-with-caveat | documented | not stated | not stated | any-phone | `dossier/compute/comfy-deploy.json` |
| Compound Reverie Grants | 'These are micro-grants to fund people expl... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/compound-reverie-grants.json` |
| Compshare | RTX4090 24G with 14 vCPU and 32G RAM at CNY... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/compshare.json` |
| Compute Cheap | no free tier and no pay-as-you-go: reserved... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/compute-cheap.json` |
| ComputerUse.space | no free tier: desktop time is sold in 30-da... | paid-only | documented | not stated | not stated | email | `dossier/compute/computeruse-space.json` |
| ConoHa VPS | no free tier; the plans start at JPY 460 a... | qualifies | documented | not applicable: the unit is a m... | the instance persists... | card | `dossier/compute/conoha-vps.json` |
| Contabo | no free tier; Cloud VPS 4 is USD 6.60 a mon... | paid-only | documented | not applicable: the unit is a m... | the server is rented... | card | `dossier/compute/contabo.json` |
| Contabo | no offer: the page reads 'Contabo Black Fri... | dead | documented | not applicable: the unit is a m... | not applicable; no of... | card | `dossier/compute/contabo-black-friday.json` |
| Contabo | no free tier; Cloud VPS 4 is the entry rung... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/contabo-cloud-vps-4.json` |
| Contabo | no free tier; Cloud VPS 8 is EUR 14.00/mont... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/contabo-windows.json` |
| Containarium | One price of USD 20 per seat per month for... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/containarium.json` |
| CoolVDS | No free tier published on the pricing page;... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Not stated on the pri... | card | `dossier/compute/coolvds.json` |
| CORESERVER V2 | CORE-X is JPY 830 a month on the monthly su... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/coreserver-v2.json` |
| CoreWeave | no free tier: GPU capacity at on-demand rat... | paid-only | documented | not stated | not stated | email | `dossier/compute/coreweave.json` |
| CrateDB Cloud | Free plan, quoted: 'Free Plan Available', '... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cratedb-cloud.json` |
| CreateOS Sandbox (NodeOps) | 500 free credits to start; a sandbox auto-p... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/createos.json` |
| CrockyHost (CROCKY S.R.L.) | No free tier. NVPS Micro is EUR 7.99 exclud... | qualifies-with-caveat | documented | not applicable: the unit is a m... | billed annually on th... | card | `dossier/compute/crockyhost-nvps-micro.json` |
| Crusoe | no free tier: hourly GPU capacity including... | paid-only | documented | not stated | not stated | email | `dossier/compute/crusoe.json` |
| CSCS Small | "Small projects may request up to 8'000 nod... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cscs-small.json` |
| CSTServer | A sale posted 2026-08-20 lists E5 bare meta... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cstserver.json` |
| CT8.PL | Quoted from the home page: '3 GB powierzchn... | fails-quota | documented | not applicable: the unit is a h... | 90 d | email | `dossier/compute/ct8-pl.json` |
| ctrl-c.club | a free shared Linux account on DigitalOcean... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 1825 d | email | `dossier/compute/ctrl-c-club.json` |
| Cube Computer | New accounts start with USD 25 of free cred... | trial-only | documented | not stated | files stay on a pause... | email | `dossier/compute/cube.json` |
| Cudo Compute | no free lane and no published rate. The pri... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/cudo-compute.json` |
| Cyclic | shut down: the shutdown post is dated 26 Ap... | dead | documented | not applicable | all usage was turned... | email | `dossier/compute/cyclic.json` |
| CyVerse | The free Basic tier is 5 GB of Data Store s... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/cyverse.json` |
| DAMODEL | RTX 4090 rental quoted at CNY 20 of credit... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/damodel.json` |
| DartNode Open Source | A free KVM VPS for any public GitHub reposi... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/dartnode-open-source.json` |
| Dasabo | SRP-1 at EUR 3.99/month: 1 GB RAM, 1 vCore,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/dasabo.json` |
| Databricks | 'Up to $400 in credits' on the free-trial t... | trial-only | documented | not applicable: the unit is a m... | 14 d | email | `dossier/compute/databricks.json` |
| DataCamp DataLab | a free DataLab tier with any DataCamp accou... | fails-quota | documented | not applicable: the unit is a s... | not stated | email | `dossier/compute/datacamp-datalab-free.json` |
| Datadog | 'Use this form to apply for access to Datad... | fails-identity | documented | unverified: the programme page... | unverified: the progr... | institution | `dossier/compute/datadog.json` |
| Datalayer Runtimes | Free plan: 50 wallet credits per month (res... | qualifies-with-caveat | documented | unverified: the pricing page st... | unverified: no page r... | email | `dossier/compute/datalayer.json` |
| Datalix | no free tier; the cheapest in-stock server... | qualifies-with-caveat | documented | not applicable: the unit is a m... | prepaid by the booked... | email | `dossier/compute/datalix.json` |
| Datalix | no free tier; the sale's smallest rung is t... | paid-only | documented | not applicable: the unit is a m... | 'Unsere Prepaid-Produ... | card | `dossier/compute/datalix-xeon-2026-sale-starter.json` |
| Datalix | no free tier; the sale's smallest rung is t... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 'Unsere Prepaid-Produ... | card | `dossier/compute/datalix-xeon-kvm-starter.json` |
| DataPacket | The entry configuration is an AMD EPYC 4245... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/datapacket.json` |
| DataPasa | No free tier. Cheapest paid offer: VPS-1, 1... | paid-only | documented | not applicable: the unit is a m... | a server is billed by... | email | `dossier/compute/datapasa.json` |
| Daytona | USD 200 in free compute included, one time.... | qualifies-with-caveat | documented | One sandbox is capped at 4 vCPU... | Container sandboxes k... | email | `dossier/compute/daytona.json` |
| Daytona GPU | The same platform sells GPUs by the hour, a... | paid-only | documented | not applicable: the unit is a m... | The preemptible tier... | email | `dossier/compute/daytona-gpu.json` |
| Daytona (Windows sandboxes) | $200 of free compute, no card: a Windows sa... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/daytona-windows.json` |
| Declaw | $100 of sandbox compute credit and a separa... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/declaw.json` |
| Dedalus Labs | $20 of one-time sign-up credit with up to 4... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/dedalus-labs.json` |
| DediOne | Los Angeles KVM at USD 3.99 a month for 2 v... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/dedione.json` |
| DediRock | Yearly Promo VPS Saver at USD 10.88/year: 1... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/dedirock.json` |
| DediRock | no free tier; the page sells annual promo p... | dead | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/dedirock-black-friday.json` |
| DediRock | no free tier; the page sells annual promo p... | dead | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/dedirock-cyber-monday.json` |
| DediRock | No free tier. The Black Friday page read to... | qualifies-with-caveat | documented | not applicable: the unit is a m... | The server persists w... | email | `dossier/compute/dedirock-promo-vps-saver.json` |
| DediRock | no free tier; this is the cheapest plan in... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | email | `dossier/compute/dedirock-promo-vps-special-ny.json` |
| DediRock Storage VPS | A large-disk VPS line in New York and Los A... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/dedirock-storage-vps.json` |
| Deepgram | 'Free $200 Credit' with 'No minimums. No ex... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/deepgram.json` |
| Deepgram Startup Program | 'Apply to Deepgram for Startups and get up... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/deepgram-startup-program.json` |
| DeepInfra DeepStart | 50,000,000,000 free inference tokens for an... | fails-identity | documented | not applicable: the unit is a m... | the funding gate fail... | institution | `dossier/compute/deepinfra-deepstart.json` |
| DeepInfra GPU | No free GPU allowance. Dedicated GPU rates... | paid-only | documented | not applicable: the unit is a m... | All container data is... | card | `dossier/compute/deepinfra-gpu.json` |
| DeepInfra Sandboxes | no free tier: 'the nano plan starts at just... | paid-only | documented | not applicable: the unit is a s... | 7 d | card | `dossier/compute/deepinfra-sandboxes.json` |
| Deepnote Education plan | 'Our Education plan is 100% free for studen... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/deepnote-education-plan.json` |
| Deepnote | Free forever, including the Basic machine a... | qualifies-with-caveat | documented | not applicable: the unit is a s... | not stated on the pri... | email | `dossier/compute/deepnote-free.json` |
| DeepSeek API | No free grant on the vendor's own pricing p... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/deepseek-api.json` |
| DeGirum AI Hub | Withdrawn. The company states: 'Effective A... | dead | documented | not applicable: the unit is a m... | the allowance did not... | email | `dossier/compute/degirum-ai-hub.json` |
| DeluxHost | VPS-1 at EUR 1.99/month in the Netherlands:... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/deluxhost.json` |
| Deno Deploy | Free at USD 0: 1 million requests a month,... | qualifies-with-caveat | documented | a 768 MB default memory allocat... | revision storage is 1... | email | `dossier/compute/deno-deploy.json` |
| Deno Sandbox | a free plan with a monthly request allowanc... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/deno-sandbox.json` |
| Deplexo | Free plan, quoted: '1 app', 'CPU per app 0.... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/deplexo.json` |
| Depot (GitHub Actions run... | No free tier: a 7-day trial, then the Devel... | trial-only | documented | not stated | not stated | email | `dossier/compute/depot.json` |
| DesignSafe-CI | A Startup Allocation may request up to 20,0... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/designsafe-ci.json` |
| Deta Space | nothing reachable: deta.space returned a Cl... | dead | documented | not applicable | data was deleted at t... | email | `dossier/compute/deta-space.json` |
| Devin , including | Devin Free: "Free $0", "Light quota to code... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/devin-including.json` |
| Dexto | free access to specific zero-priced models... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/dexto.json` |
| DigiRDP | Cloud VPS Host IPV6 at USD 1.00/month, with... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/digirdp.json` |
| Digital Catapult | A 14-week accelerator whose participants ge... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/digital-catapult.json` |
| Digital Research Alliance | Canada's national platform ran about 233,00... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/digital-research-alliance.json` |
| DigitalCloud | Lite Cloud: USD 7.99 list with printed disc... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/digitalcloud.json` |
| DigitalOcean Droplets | No current signup amount is published. Both... | paid-only | documented | not stated | not stated | card | `dossier/compute/digitalocean.json` |
| DigitalOcean | no free tier; the cheapest droplet is '512... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/digitalocean-droplet-1gb.json` |
| DigitalOcean Gradient AI | The prize carries cloud credit alongside ca... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/digitalocean-gradient-ai.json` |
| DigitalOcean Harness Runtime | Hardware-isolated microVM sandboxes with Ch... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/digitalocean-harness-runtime.json` |
| DigitalOcean Hatch | Hatch was DigitalOcean's startup credit pro... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/digitalocean-hatch.json` |
| DigitalOcean Startups | 12 months of DigitalOcean credits for accep... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/digitalocean-startups.json` |
| DigitalOcean student credit | The pack's cloud-credit headline is gone. Q... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/digitalocean-student-credit.json` |
| dimension.sh | A tilde community that is now a memorial: q... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/dimension-sh.json` |
| Docker Cloud Sandboxes | no free tier: compute bills per second from... | paid-only | documented | not stated | not stated | email | `dossier/compute/docker-cloud-sandboxes.json` |
| Dockerhosting.ru | no free tier; the entry plan is 'Start 299... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/dockerhosting-prodv.json` |
| Dockerhosting.ru | no free tier; Start at 299 RUB a month is t... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/dockerhosting-start.json` |
| Dockup | a Free-forever plan alongside $45 a month f... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/dockup.json` |
| DogYun | RMB 30.00/month for hk.st.s on the Hong Kon... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/dogyun.json` |
| Dothome | '무료호스팅 기본사양 무료' (free hosting, base spec, f... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/dothome.json` |
| Dreamify AI (Dreamifly, n... | 10 credits on each day the account visits,... | qualifies-with-caveat | documented | not applicable: the unit is a g... | 2 d | email | `dossier/compute/dreamify-ai.json` |
| DrivenData / DOE | 'Total Prize Pool: $300,000', split as 'Ini... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/drivendata-doe.json` |
| E2B | Hobby is USD 0 a month with 'One-time $100... | qualifies-with-caveat | documented | Sandboxes can be configured wit... | Sandbox storage is in... | email | `dossier/compute/e2b.json` |
| E2E Networks | no recurring free tier: GPU resources bill... | fails-identity | documented | not stated | not stated | institution | `dossier/compute/e2e-networks.json` |
| EcoHash | A USD 1.00 welcome credit on every new acco... | trial-only | documented | not applicable: the unit is a m... | Terminating the insta... | email | `dossier/compute/ecohash.json` |
| EFN | A free UNIX shell across Linux, BSD and Sol... | qualifies-with-caveat | documented | not applicable: the unit is a m... | The 60-day login cloc... | email | `dossier/compute/efn.json` |
| Egg Hosting | Dedicated-vCPU KVM instances: 2 vCPU with 4... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/egg-hosting.json` |
| EGI Cloud Compute | "Trial access: Try the service, prototype a... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/egi-cloud-compute.json` |
| Elende | VPS Linux 1 on the vendor's own KVM page: 1... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/elende.json` |
| ElevenLabs | Free plan at USD 0 with '10k credits per mo... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/elevenlabs.json` |
| ElevenLabs Startup Grants | 'Scale for 12 months ... 33,000,000 charact... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/elevenlabs-startup-grants.json` |
| Ellipsis | no per-seat fee for the platform; the compu... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/ellipsis.json` |
| ElypseCloud | 'CPU: 2 x E5-2697v4', 'RAM: 4 GB DDR4', 'Es... | dead | documented | not published on the page read | not published: the fr... | email | `dossier/compute/elypsecloud-free.json` |
| Emergent | Emergent Free: "10 credits on your first da... | trial-only | documented | not applicable: the unit is a m... | the 10 credits are gr... | email | `dossier/compute/emergent.json` |
| Emergent Ventures | A rolling grant and fellowship programme ru... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/emergent-ventures.json` |
| Encore Cloud | The Starter plan is free forever with no ti... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/encore-cloud.json` |
| Enterprise | A Start-up Grant of EUR 20,000 at 80 percen... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/enterprise.json` |
| Enterprise Compute Initia... | A SGD 150 million programme that passes clo... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/enterprise-compute-initiative.json` |
| envs.net | a shell account on a Debian 13 host with 20... | qualifies-with-caveat | documented | not applicable: the unit is a m... | files in /tmp are tem... | email | `dossier/compute/envs-net.json` |
| EQVPS | no free tier; Nano is USD 3.00 a month | qualifies-with-caveat | documented | not applicable: the unit is a m... | the server persists w... | anonymous | `dossier/compute/eqvps-nat-nano.json` |
| Esperanto Technologies | Ceased operations, while its own homepage s... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/esperanto-technologies.json` |
| EthernetServers | 1 GB KVM VPS from the vendor's own plan tab... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ethernetservers.json` |
| Eurobyte | RUB 14 per day, RUB 290 per month or RUB 29... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/eurobyte.json` |
| EuroHPC AI Factories | Fast Lane access offers up to 50,000 GPU ho... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/eurohpc-ai-factories.json` |
| EuroHPC JU Benchmark | A continuously open call with monthly cut-o... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/eurohpc-ju-benchmark.json` |
| Euronodes | The first row of the vendor's own VPS table... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/euronodes.json` |
| European Innovation Council | Grants below EUR 2.5 million combined with... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/european-innovation-council.json` |
| EUserv | A container-based Linux root server, free w... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 30 d | email | `dossier/compute/euserv.json` |
| EUserv VS2-free | A container-based Linux server with full ro... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 30 d | email | `dossier/compute/euserv-vs2-free.json` |
| Eventual | free tier published without a credit amount | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/eventual.json` |
| Everstack | Sandbox compute bills per second at USD 0.0... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/everstack.json` |
| Evolution Host | EUR 5.00/month for Starter: 1 CPU core at 4... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/evolution-host.json` |
| exe.dev | No free tier; a 7-day trial with a paid Cha... | paid-only | documented | not applicable: the unit is a m... | Persistent disks are... | card | `dossier/compute/exe-dev.json` |
| Exoscale | no free instance: resources bill by the sec... | paid-only | documented | not stated | not stated | email | `dossier/compute/exoscale.json` |
| Expo | Expo and the SDK are free and open source u... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/expo.json` |
| ExtraVM | The 1 GB plan at USD 4.50 per month (1 core... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/extravm.json` |
| Faable | Free plan, quoted: 'up to 3 projects per ac... | qualifies-with-caveat | documented | not applicable: the unit is a m... | a Free app sleeps aft... | email | `dossier/compute/faable.json` |
| FABRIC | FABRIC is an NSF-funded instrument of 29 si... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/fabric.json` |
| Factory | no free tier: individual plans are Pro at U... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/factory.json` |
| fal | free tier published without a credit amount | paid-only | documented | not stated | not stated | email | `dossier/compute/fal.json` |
| fal Research Grants | Free compute on fal's inference platform. T... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/fal-research-grants.json` |
| Fast Grants | The programme is offline. The domain now re... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/fast-grants.json` |
| Fastly Compute | "10 Million Compute requests free" a month... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/fastly-compute.json` |
| Featherless AI | no free tier of any kind. Every plan is pai... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/featherless-ai.json` |
| Featurize | Chinese GPU cloud and hosted notebook with... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/featurize.json` |
| Ferenz | The first plan card on the vendor's own VPS... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ferenz.json` |
| Ferr | up to 50 browser hours a month with 3 concu... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/ferr.json` |
| FiberState | no free tier; the cheapest listed server is... | paid-only | documented | not applicable: the unit is a m... | billed in advance and... | card | `dossier/compute/fiberstate.json` |
| Filecoin Foundation Next | 'Next Step Microgrants are awarded in the a... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/filecoin-foundation-next.json` |
| Firebase Hosting | On the no-cost Spark plan, Hosting storage... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/firebase-hosting.json` |
| Firebase Studio | "Firebase Studio is sunsetting on March 22,... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/firebase-studio.json` |
| Firecrawl Interact / Brow... | Free plan: 1,000 credits every month, no cr... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/firecrawl.json` |
| FireVM | No free allowance. Single-tenant bare-metal... | paid-only | documented | not applicable: the unit is a m... | Month to month: no lo... | national-id | `dossier/compute/firevm.json` |
| Fireworks AI, Muse | A free first LoRA fine-tune with no card: '... | trial-only | documented | not applicable: the unit is a m... | the 2026-11-30 window... | email | `dossier/compute/fireworks-ai-muse.json` |
| FirstByte | no free tier; a 24-hour test access is offe... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the server persists w... | card | `dossier/compute/firstbyte-msk-kvm-start.json` |
| FirstVDS | No free GPU trial; the minimum paid period... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/firstvds.json` |
| Flapjacks | No free tier. HK-T1ION-IPv6-Mini is USD 2.9... | dead | documented | not applicable: the unit is a m... | annual prepay; no del... | card | `dossier/compute/flapjacks-hk-t1ion-ipv6-mini.json` |
| Flightcontrol | The Single user plan is free with unlimited... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/flightcontrol.json` |
| Flow Swiss Mac Bare Metal | no free tier: Mac hardware from CHF 0.27 an... | paid-only | documented | not stated | not stated | email | `dossier/compute/flow-swiss-mac.json` |
| FlowVPS | The entry tier on the vendor's own pricing... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/flowvps.json` |
| Fluence | A multi-provider neocloud selling CPU and G... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/fluence.json` |
| Fluidstack | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/fluidstack.json` |
| Fly.io | no free tier: 'New organizations don't have... | trial-only | documented | not applicable: the unit is a M... | a stopped Machine bil... | card | `dossier/compute/fly-io.json` |
| Fly.io Machines | No. New organizations don't have a free tie... | trial-only | documented | not applicable: the unit is a m... | A stopped Machine kee... | card | `dossier/compute/fly-machines.json` |
| Fosshost | Free VPS, web hosting, mirror and AArch64 c... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/fosshost.json` |
| FOSSVPS | FOSSVPS is a free 2 vCPU / 4 GiB / 64 GiB V... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/fossvps.json` |
| FreeMach | 'FreeMach™ is a community-powered project t... | fails-identity | documented | '10/10 VMs Allocated (0 slots f... | not published as a cl... | institution | `dossier/compute/freemach-free.json` |
| freeshell.de | 'SSH to Ubuntu 24.04 LTS server with many t... | qualifies-with-caveat | documented | ulimit values per account: 'nof... | Not stated on the pag... | email | `dossier/compute/freeshell-de.json` |
| Freestyle | No cash credit. The Free plan includes 'Hou... | qualifies-with-caveat | documented | Free plan limits: 'Max vCPUs pe... | Free has no persisten... | email | `dossier/compute/freestyle.json` |
| freevps.edu.pl | 'Free Windows VPS Hosting For Students & De... | fails-identity | documented | not applicable: the unit is a m... | no expiration is stat... | institution | `dossier/compute/freevps-edu-pl.json` |
| FreeVPS.org | '1 core (fair share)', 'RAM 1GB, up to 2GB... | qualifies-with-caveat | documented | not applicable: the unit is a v... | 'There is no fixed te... | email | `dossier/compute/freevps-org.json` |
| FreeVPSTrial.net | Quoted from the plan card: 'Free Trial VPS... | dead | documented | Quoted from the terms: 'The Fre... | 'The trial lasts for... | any-phone | `dossier/compute/freevpstrial-net.json` |
| Fugaku Trial Access | Trial Access Projects on Fugaku award up to... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/fugaku-trial-access.json` |
| FuriosaAI Furiosa Access | Hands-on RNGD evaluation exists and is gate... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/furiosaai-furiosa-access.json` |
| Gabia Cloud Gen1 | Hourly or monthly billed virtual servers fr... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/gabia-cloud-gen1.json` |
| Gabia VPS hosting | The product still has a published ladder of... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/gabia-vps-hosting.json` |
| Galaxy Australia | "Galaxy Australia is one of the internation... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/galaxy-australia.json` |
| Galaxy Europe | "On the European Galaxy server every user h... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/galaxy-europe.json` |
| Galaxy Main | "The main Galaxy site at https://usegalaxy.... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/galaxy-main.json` |
| Gcore Cloud / Functions /... | no free tier: VMs from EUR 8.93 a month, wi... | paid-only | documented | not stated | not stated | email | `dossier/compute/gcore.json` |
| Google Compute Engine (Li... | 1 non-preemptible e2-micro instance for the... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/gcp-compute.json` |
| Google Compute Engine GPU... | not stated on https://cloud.google.com/prod... | paid-only | documented | not stated | not stated | card | `dossier/compute/gcp-compute-gpu.json` |
| Google Compute Engine (Wi... | not stated for the Windows Server image on... | paid-only | documented | not stated | not stated | card | `dossier/compute/gcp-windows.json` |
| GEANT Testbeds Service | "GTS is currently available to researchers... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/geant-testbeds-service.json` |
| Gemini API code execution | 'There's no additional charge for enabling... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/gemini-code-execution.json` |
| Genesis Cloud | trial credits exist and the amount is not p... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/genesis-cloud.json` |
| Gigalixir | Free tier, quoted: '1 App Replica (0.5 GB m... | qualifies-with-caveat | documented | not applicable: the unit is a m... | a Free app 'Sleeps af... | card | `dossier/compute/gigalixir.json` |
| GitHub Actions | On a public repository: 'Use of the standar... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 'When the job begins,... | email | `dossier/compute/github-actions.json` |
| GitHub Codespaces | 'All GitHub personal accounts include a quo... | qualifies | documented | not applicable: the unit is a s... | 30 d | email | `dossier/compute/github-codespaces.json` |
| GitHub Copilot cloud sand... | a metered quota on the Copilot plan, with c... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/github-copilot-cloud-sandboxes.json` |
| GitHub Copilot Student | Quoted from the pack: 'GitHub Copilot Stude... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/github-copilot-student.json` |
| GitHub Secure Open | Quoted from the programme page: 'It is $10,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/github-secure-open.json` |
| GitHub Sponsors | 'Anyone who contributes to an open source p... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/github-sponsors.json` |
| GitHub Student Developer | Aggregator of about 60 partner offers, most... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/github-student-developer.json` |
| GitLab | 50,000 compute minutes per month in the Git... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/gitlab.json` |
| GitLab Runners | 'The base monthly compute quota is determin... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 'Ephemeral runner VMs... | card | `dossier/compute/gitlab-runners.json` |
| Gitpod (now Ona) | no self-serve free tier is reachable: the p... | paid-only | documented | not applicable: the unit is a m... | not established | card | `dossier/compute/gitpod.json` |
| GKE Agent Sandbox | USD 300 of one-time Free Trial credit, vali... | qualifies-with-caveat | documented | not stated | suspending a sandbox... | card | `dossier/compute/gke-agent-sandbox.json` |
| Gladia | 'New accounts get EUR 50 in free credits, v... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the wallet is one yea... | email | `dossier/compute/gladia.json` |
| Gladiolus (vm.gl) | 'Virtual machines for people building thing... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 'No expiration: Keep... | email | `dossier/compute/gladiolus-vm-gl.json` |
| Glitch | shut down: the newest post on the blog is 2... | dead | documented | not applicable | project hosting ended... | email | `dossier/compute/glitch.json` |
| Global AI Hackathon | 'Compete for total $70,000+ in cash and clo... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/global-ai-hackathon.json` |
| GMI Cloud SCALE | a six-week equity-free cohort for AI startu... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/gmi-cloud-scale.json` |
| Godlike.Host | USD 2.00/month for Nitro 1 on a 1 Gbps port... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/godlike-host.json` |
| Golem Network | Peer-to-peer compute priced by each provide... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/golem-network.json` |
| Gologin Cloud Browser | a free start with no card, browser hours bi... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/gologin.json` |
| Gongji Compute individual | 'new-user trial: join the group, fill in th... | qualifies | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/gongji-compute-individual.json` |
| Google | Start tier is USD 2k for startups founded i... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/google.json` |
| Google Agent Runtime / Ag... | 180,000 vCPU-seconds and 360,000 GiB-second... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/google-agent-engine.json` |
| Google Cloud Build | 2,500 build-minutes a month per billing acc... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/google-cloud-build.json` |
| Google Cloud Free Tier (e... | 1 non-preemptible e2-micro VM instance a mo... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the Free Tier has no... | card | `dossier/compute/google-cloud-free-tier.json` |
| Google Cloud research | 'PhD students conducting research may apply... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/google-cloud-research.json` |
| Google Cloud Run | per billing account, monthly: 2 million req... | qualifies-with-caveat | documented | a request may run up to 60 minu... | no persistent disk; a... | card | `dossier/compute/google-cloud-run.json` |
| Google Cloud Shell | 50 hours a week of Cloud Shell, a 12-hour s... | qualifies-with-caveat | documented | not applicable: the unit is a s... | 5 GB of $HOME persist... | email | `dossier/compute/google-cloud-shell.json` |
| Google Cloud Spot | Google publishes two numbers that answer th... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/google-cloud-spot.json` |
| Google Cloud Text-to-Speech | A recurring monthly free allowance per voic... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/google-cloud-text-to-speech.json` |
| Google Cloud Free Trial (... | Signing up for the Free Trial creates a Fre... | trial-only | documented | not applicable: the offer is a... | 90 d | card | `dossier/compute/google-cloud-trial.json` |
| Google Colab | free of charge access to computing resource... | qualifies-with-caveat | documented | not applicable: the unit is a s... | the VM disk is delete... | email | `dossier/compute/google-colab.json` |
| Google Colab (paid tiers) | no published quota on any tier: Colab state... | fails-quota | documented | not applicable: the unit is a m... | a VM is deleted when... | card | `dossier/compute/google-colab-paid.json` |
| Google Gemini API | The free tier still exists and the pricing... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/google-gemini-api.json` |
| Google Open Source | 'you can claim rewards for proactive improv... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/google-open-source.json` |
| Google Summer | 'large projects range from $3000 to $6600 U... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/google-summer.json` |
| Google TPU Research | Free Cloud TPU quota granted to an approved... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the TPU quota is gran... | card | `dossier/compute/google-tpu-research.json` |
| gpu.ai | no free tier: a GPU marketplace that routes... | paid-only | documented | not applicable: the unit is a G... | not stated in the pag... | email | `dossier/compute/gpu-ai.json` |
| GPU.LAND | USD 0.25/hour for a vGPU instance, the vend... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/gpu-land.json` |
| GPU Outlet | no free tier and no rented machine: a marke... | fails-identity | documented | not applicable: the unit is res... | not applicable: the m... | institution | `dossier/compute/gpu-outlet.json` |
| Grafana Cloud | Free plan, quoted: 'Always free Always', '$... | qualifies-with-caveat | documented | 256kb per log line (max_line_si... | 14 d | email | `dossier/compute/grafana-cloud.json` |
| Graphcore IPU Cloud | The free tier is gone and what remains is a... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/graphcore-ipu-cloud.json` |
| Green Compute | No free tier. RTX 4090 rental is USD 0.40 p... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/green-compute.json` |
| GreenCloudVPS | no free tier; the sale's smallest rung is t... | qualifies-with-caveat | documented | not applicable: the unit is a m... | annual prepay; the ca... | card | `dossier/compute/greencloud-budget-kvm-8gb.json` |
| GreenCloudVPS | Budget KVM Sale: 22 of the 44 order lines a... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/greencloudvps.json` |
| Green Mini host | no free tier: dedicated Apple hardware from... | paid-only | documented | not stated | not stated | email | `dossier/compute/greenmini.json` |
| Grid'5000 | The page states plainly that "The Grid'5000... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/grid-5000.json` |
| Groq Cloud | A free plan per model, printed as RPM / RPD... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/groq-cloud.json` |
| GTHost | VPS-4, the first row of the vendor's own li... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/gthost.json` |
| Gullo's Hosting | NAT IPv4 128 MB, the entry row of the vendo... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/gullo-s-hosting.json` |
| Gullo's Hosting | No free tier. The smallest NAT container is... | qualifies | documented | not applicable: the unit is a m... | The container persist... | email | `dossier/compute/gullos-hosting-nat-128.json` |
| H Company / Surfer / H Ag... | a Free tier at $0 a month with up to 3 conc... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/h-company.json` |
| h3llo.cloud year-free pac... | A withdrawn offer that was the largest free... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/h3llo-cloud-year-free-package.json` |
| Haidian District Elastic | District government guideline, verbatim: 'T... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/haidian-district-elastic.json` |
| Halluminate | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/halluminate.json` |
| harvis.dev | Batch 1 recorded harvis.dev as a perpetual... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/harvis-dev.json` |
| hashbang | a free shared shell account; per-user limit... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 30 d | email | `dossier/compute/hashbang.json` |
| Hashnix.Club | 'Hashnix is a non-commercial, free to join... | qualifies-with-caveat | documented | not applicable: the unit is a h... | not stated: no inacti... | email | `dossier/compute/hashnix.json` |
| Hatchet | no credit card, and the first 100,000 runs... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/hatchet-run.json` |
| HengHost | CNY 88 per month is the vendor's stated flo... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/henghost.json` |
| Heroic Labs | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/heroic-labs.json` |
| Heroku | no free dyno: the pricing page prices dynos... | paid-only | documented | not applicable: nothing free | not applicable | card | `dossier/compute/heroku.json` |
| Heroku Open Source | 'one year of platform credits to qualifying... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/heroku-open-source.json` |
| Hetzner | Three SX models, all with SATA HDD plus NVM... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/hetzner.json` |
| Hetzner Cloud | no free tier; the entry shape CX23 is EUR 5... | paid-only | documented | not applicable: the unit is a m... | a VM is retained all... | card | `dossier/compute/hetzner-cloud.json` |
| Hetzner | no free tier; the cheapest cloud server is... | paid-only | documented | not applicable: the unit is a m... | the server is billed... | card | `dossier/compute/hetzner-cx23.json` |
| Hetzner GPU servers | no free tier: GEX GPU servers from EUR 214.... | paid-only | documented | not stated | not stated | email | `dossier/compute/hetzner-gpu.json` |
| Hetzner Server Auction | The auction listing served on 2026-10-22 ho... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hetzner-server-auction.json` |
| Hetzner SX storage servers | Three SX models, all with SATA HDD plus NVM... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hetzner-storage.json` |
| Hex | Community is free and includes Small comput... | qualifies-with-caveat | documented | not applicable: the unit is a s... | 7 d | email | `dossier/compute/hex-community.json` |
| Hexgrid Cloud | no free tier: dedicated GPUs by the hour, b... | paid-only | documented | not applicable: the unit is a G... | the home page says mo... | email | `dossier/compute/hexgrid-cloud.json` |
| Hinode | a one-time trial: eligible new accounts get... | trial-only | documented | not applicable: the unit is a m... | 1 d | card | `dossier/compute/hinode.json` |
| HLRS test access | A test account on HLRS systems carries a co... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/hlrs-test-access.json` |
| HOKAS | 'The free plan never expires', 'no credit c... | fails-quota | documented | not published as a count: the f... | The free plan is time... | email | `dossier/compute/hokas-free.json` |
| Hop179 (Hop179 OU) | No free tier. The IPv6-only plan is EUR 1.0... | qualifies | documented | not applicable: the unit is a m... | 10 d | email | `dossier/compute/hop179-v6-vps.json` |
| Hop179 OÜ | No free tier. The IPv6-only plan is EUR 11.... | qualifies | documented | not applicable: the unit is a m... | annual billing; the o... | email | `dossier/compute/hop179-v6-vps-frankfurt.json` |
| Hoplite | Free plan at $0 a month: 'Run agents yourse... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/hoplite.json` |
| Hopx | USD 200 in free credits with no credit card... | qualifies-with-caveat | documented | Resources are set by the templa... | A sandbox is destroye... | email | `dossier/compute/hopx.json` |
| Host Hong Kong | No free tier. The NAT-VPS page describes th... | dead | documented | not applicable: the unit is a m... | the page states 'Our... | card | `dossier/compute/host-hong-kong-nat-vps.json` |
| host2play | No free tier. LXC Lite is PLN 34.90 a year,... | qualifies | documented | not applicable: the unit is a m... | prepaid service, not... | email | `dossier/compute/host2play-lxc-lite.json` |
| HostAddon | No free tier. Cheapest paid offer: MVPS 1 o... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hostaddon.json` |
| HostBrr | no free tier; the entry rung is EUR 2.00 or... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostbrr.json` |
| HostBrr | No free tier. 'DE-Performance-1GBrr IPv6 On... | qualifies-with-caveat | documented | not applicable: the unit is a m... | The server persists w... | email | `dossier/compute/hostbrr-ipv6-1g.json` |
| HostBrr | no free tier; 'Cloud VPS - NVMe KVM Servers... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostbrr-value-2gb.json` |
| HostBrr | no free tier; the group's smallest rung is... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostbrr-value-4gb.json` |
| HostBrr | no free tier; the group's smallest rung is... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostbrr-value-8gb.json` |
| HostBrr | no free tier; the Value 16GB plan is USD 11... | fails-quota | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostbrr-windows.json` |
| HostData.id | No free tier. NAT SG SSD 1GB is IDR 20,000... | fails-identity | documented | not applicable: the unit is a m... | monthly billing; no d... | card | `dossier/compute/hostdata-id-nat-sg-ssd-1gb.json` |
| HostData.id | No free tier. NAT SG 1GB is Rp 20,000 IDR a... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not stated on any pag... | email | `dossier/compute/hostdata-nat-sg-1gb.json` |
| HostEons | The cheapest plan the vendor's pages let yo... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hosteons.json` |
| Hoster.kz | A 7-day free test of a cloud server, reques... | trial-only | documented | not applicable: the unit is a m... | The free window is se... | any-phone | `dossier/compute/hoster-kz.json` |
| Hosteroid | Archive-500GB at EUR 14.14/year VAT include... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hosteroid.json` |
| HostHatch | The cheapest NVMe compute VM in the standin... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/hosthatch.json` |
| HostHatch | no free tier; 'NVMe 2 GB from $4.00 / month' | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hosthatch-nvme-2gb.json` |
| Hostim.dev | No perpetual free tier; a 5-day trial witho... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hostim-dev.json` |
| Hosting Int | Linux VPS at EUR 5.90/month: 1 vCPU Xeon Go... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hosting-int.json` |
| Hostinger VPS | no free tier: VPS from $6.49 a month on a t... | paid-only | documented | not stated | not stated | email | `dossier/compute/hostinger-vps.json` |
| HOSTKEY | No free trial, stated in the provider's own... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/hostkey.json` |
| HOSTKEY | no free tier; EUR 14.00 a month on the Engl... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostkey-windows.json` |
| HostMyApple | no free tier: macOS packages from $24.99 a... | paid-only | documented | not stated | not stated | email | `dossier/compute/hostmyapple.json` |
| HostNamaste | OpenVZ-512 at USD 3.49/month: 1 CPU, 512 MB... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hostnamaste.json` |
| HostNowNow Flux | 'Yes. Flux Free is free forever with hard c... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hostnownow-flux.json` |
| HostSlate | A newly launched Chinese-language merchant... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hostslate.json` |
| Hostwinds | no free tier; Managed Windows SSD Cloud 7 i... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/hostwinds-windows.json` |
| Hot Aisle | AMD-only GPU host: the pricing page lists n... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hot-aisle.json` |
| Huawei Cloud AgentArts | the trial edition grants 20 CU of runtime o... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/huawei-cloud.json` |
| Huawei Cloud International | Withdrawn. The international free-packages... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/huawei-cloud-international.json` |
| Huawei Cloud (international) | 'Free trial is available for each product o... | fails-identity | documented | one newcomer package per user:... | Not stated on the fre... | card | `dossier/compute/huawei-cloud-intl-free-trial.json` |
| Hub71 | For the Access Programme: 'AED 250,000 wort... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/hub71.json` |
| Hugging Face Community | 'Do you have an awesome Space but need help... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hugging-face-community.json` |
| Hugging Face Inference | The monthly credits table now reads: "Free... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hugging-face-inference.json` |
| Hugging Face Jobs (hf-san... | no free compute allowance of its own: a Job... | paid-only | documented | not stated | not stated | email | `dossier/compute/huggingface-jobs.json` |
| Hugging Face Spaces | Static Spaces are free for everyone; Gradio... | qualifies-with-caveat | documented | not applicable: the unit is a m... | a Space on free hardw... | email | `dossier/compute/huggingface-spaces.json` |
| Hugging Face Spaces (CPU... | CPU Basic is listed at 2 vCPU / 16 GB for F... | paid-only | documented | not applicable: the unit is a s... | 50 GB of disk per Spa... | card | `dossier/compute/huggingface-spaces-cpu-basic.json` |
| Hugging Face ZeroGPU | a free account in good standing (verified e... | qualifies-with-caveat | documented | not applicable: the unit is a s... | the Space repo persis... | email | `dossier/compute/huggingface-spaces-zerogpu.json` |
| Hume AI | The API is no longer self-serve: 'The API i... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/hume-ai.json` |
| HyperAI | A membership whose monthly fee buys a fixed... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/hyperai.json` |
| Hyperbeam | 10,000 free minutes every month, then pay a... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/hyperbeam.json` |
| Hyperbolic | no free tier: on-demand GPU rental at start... | paid-only | documented | not stated | not stated | email | `dossier/compute/hyperbolic.json` |
| Hyperbrowser | 5,000 credits on a free account, enough for... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not stated on the pag... | email | `dossier/compute/hyperbrowser.json` |
| Hyperstack | no free tier: GPU and CPU capacity billed p... | paid-only | documented | not stated | not stated | email | `dossier/compute/hyperstack.json` |
| IBM Cloud | The free page states: 'You get credit for y... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ibm-cloud.json` |
| IBM Cloud VPC | no free tier: new VPC clients get 70% off f... | trial-only | documented | not stated | not stated | card | `dossier/compute/ibm-cloud-vpc.json` |
| IBM LinuxONE Community | A free virtual machine on real IBM LinuxONE... | trial-only | documented | not applicable: the unit is a m... | 120 d | email | `dossier/compute/ibm-linuxone-community.json` |
| IBM Quantum Open | Batch 1 recorded the Open Plan at 10 minute... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ibm-quantum-open.json` |
| IDCloudHost | No free VM. IDCloudHost gives a bonus balan... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/idcloudhost.json` |
| IDreg Net | No free tier. NAT-1 is Rp 8,500.00 a month:... | qualifies | documented | not applicable: the unit is a m... | 2 d | email | `dossier/compute/idreg-nat-1.json` |
| iExec | TEE compute on workerpools paid per executi... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/iexec.json` |
| iFog GmbH | No free tier. The 512 MB IPv6-only plan is... | qualifies | documented | not applicable: the unit is a m... | billed 3-monthly or 1... | email | `dossier/compute/ifog-bgp-basic-512-ipv6.json` |
| IHC | Three days of any VPS tariff free, but acti... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ihc.json` |
| iHostART (MAN HOSTING GMB... | No free tier and no price published: the st... | dead | documented | not applicable: the unit is a m... | not published on the... | card | `dossier/compute/ihostart-nat64-1g.json` |
| INCITE | Up to 60% of the allocatable time on Fronti... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/incite.json` |
| IncogNET | 512 MB plan at USD 4.62/month billed USD 27... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/incognet.json` |
| Incudal (黃帝云VPS) | No free tier was ever published. The cheape... | dead | documented | not applicable: the unit is a m... | the operator announce... | email | `dossier/compute/incudal.json` |
| IndiaAI Compute Portal | Empanelled AI cloud services at a subsidy o... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/indiaai-compute-portal.json` |
| Inference.net | Pay as you go is priced '$0+ usage' and inc... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/inference-net.json` |
| Inference-Time Compute Ha... | 'Participants will also receive serious com... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/inference-time-compute-hackathon.json` |
| InfluxDB Cloud Serverless | Two offers on one page. The Free Plan, quot... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/influxdb-cloud-serverless.json` |
| Infomaniak Public Cloud | 'Get started free of charge with CHF 300.-... | fails-identity | documented | once per customer: 'this offer... | the credits expire: '... | card | `dossier/compute/infomaniak-public-cloud.json` |
| Infrawire | EUR 8.30/month for VPS Entry in Istanbul, p... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/infrawire.json` |
| inis.run | New accounts get EUR 1.00 in credit, no car... | trial-only | documented | not applicable: the unit is a m... | The continuous-live b... | email | `dossier/compute/inis-run.json` |
| InsForge (InstaCloud) | $10 of usage credit a month that refreshes,... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/insforge-instacloud.json` |
| InstaBox | 'Free gives you one 4 vCPU / 8 GiB machine... | qualifies-with-caveat | documented | not applicable: the unit is a m... | The five-machine gran... | email | `dossier/compute/instabox.json` |
| InstaVM | Free with a $0 base price, $50 of credits t... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/instavm.json` |
| Intel Liftoff | The programme promises 'Free cloud credits... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/intel-liftoff.json` |
| Intel Tiber Developer | Free sandbox for oneAPI work: 120 days of a... | trial-only | documented | not applicable: the unit is a m... | the account expires a... | email | `dossier/compute/intel-tiber-developer.json` |
| InterServer | USD 3.00/month for 1 slice: 1 core, 2 GB me... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/interserver.json` |
| InterServer | no free tier; the Windows product starts at... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/interserver-windows.json` |
| Intuned | the $0 plan includes 3 compute hours, a $5... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/intuned.json` |
| Invs | The page is titled 'Server rental from 1200... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/invs.json` |
| io.net Intelligence | A free daily inference allowance exists and... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/io-net-intelligence.json` |
| IONOS Cloud | no free tier: CPU, RAM, storage and GPU tem... | paid-only | documented | not stated | not stated | card | `dossier/compute/ionos.json` |
| IONOS | VPS S+: 1 vCore, 2 GB RAM, 60 GB NVMe, unli... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ionos-2.json` |
| IONOS CLOUD | 'During the trial period, 8 cores, 20 GB RA... | fails-identity | documented | the trial pool is shared across... | 'After the test phase... | card | `dossier/compute/ionos-cloud-trial.json` |
| IONOS | no free tier; the entry plan is 'VPS S+' at... | paid-only | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/ionos-vps-s-plus.json` |
| IONOS | no free tier; Windows XL+ is USD 94.00/mont... | paid-only | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/ionos-windows.json` |
| is_hosting | Lite (order page 2026-11-07): 1 Month USD 6... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/is-hosting.json` |
| Isle | Free plan at $0 per month: 5 environment-ho... | qualifies-with-caveat | documented | Individual uploads and download... | not stated | email | `dossier/compute/isle.json` |
| Islo | starting credits at signup with no card; a... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/islo.json` |
| IT4Innovations Open Access | The 39th Open Access Grant Competition dist... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/it4innovations-open-access.json` |
| ITIDA StartIT / | USD 10,000 of AWS credit within a one-year... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/itida-startit.json` |
| iWebFusion | Tiny at $9.38 per month: 1 CPU core, 4 GB R... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/iwebfusion.json` |
| iwinv | no free tier; the smallest server is KRW 5,... | fails-identity | documented | not applicable: the unit is a m... | monthly billing; the... | national-id | `dossier/compute/iwinv.json` |
| ix | Three meters only: USD 0.0288 per vCPU-hour... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ix.json` |
| Jagoan Cloud | IDR 150,000 of credit for a 30-day trial, g... | trial-only | documented | not applicable: the unit is a m... | The credit expires af... | any-phone | `dossier/compute/jagoan-cloud.json` |
| Jarvislabs | no free tier: GPU instances are billed per... | paid-only | documented | not applicable: the unit is a s... | not stated on the pri... | card | `dossier/compute/jarvislabs.json` |
| JetBrains AI | JetBrains AI Free: "Unlimited AI completion... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/jetbrains-ai.json` |
| JetBrains Student Pack | The Student Pack is quoted as '10 JetBrains... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/jetbrains-student-pack.json` |
| Jetstream2 | Jetstream2 bills every instance in ACCESS s... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/jetstream2.json` |
| JJFLY (拼好鸡) | No free tier. 荷兰NAT is CNY 1.00 a month: 25... | qualifies | documented | not applicable: the unit is a m... | refunds rather than r... | email | `dossier/compute/jjfly-nl-nat.json` |
| JSC Test | Test projects grant a computing-time budget... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/jsc-test.json` |
| Jules | Jules free plan: 15 daily tasks on a rollin... | qualifies | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/jules.json` |
| Kaggle Notebooks | 30 hours of GPU a week: "You can use up to... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/kaggle.json` |
| Kaggle Benchmarks | Kaggle supplies compute and model access to... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/kaggle-benchmarks.json` |
| Kaggle Notebooks | 4 CPU cores and 30 GB RAM, or 1 Tesla P100... | qualifies | documented | not applicable: the unit is a s... | 20 GB of /kaggle/work... | any-phone | `dossier/compute/kaggle-notebooks.json` |
| KAGOYA CLOUD VPS | Day-rate billing with a monthly ceiling: th... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/kagoya-cloud-vps.json` |
| KakaoCloud Virtual Machine | no free tier: pay-as-you-go instances acros... | paid-only | documented | not stated | not stated | email | `dossier/compute/kakao-cloud.json` |
| KakaoCloud | KRW 300,000 of credit for new customers who... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/kakaocloud.json` |
| Kamatera | 'Sign up for a free 30-day trial to receive... | trial-only | documented | not stated | 30 d | card | `dossier/compute/kamatera.json` |
| Kamatera | no free tier on the pricing page; 'Our serv... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/kamatera-basic.json` |
| Kamatera | no free tier; the 4 vCPU Type A shape with... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/kamatera-windows.json` |
| Kedge | $5 of usage a month, recurring, consumed be... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/kedge.json` |
| Kencang | no free tier; K-1 at Rp29.900 a month is th... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | email | `dossier/compute/kencang-k3.json` |
| Kernel | free: USD 0 a month plus usage, USD 5 of fr... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 1 d | email | `dossier/compute/kernel.json` |
| KhanWebHost (KhanWebHost... | No free tier. FR 256 MB NAT is USD 5.99 a y... | qualifies-with-caveat | documented | not applicable: the unit is a m... | annual prepay; the st... | card | `dossier/compute/khanwebhost-fr-256mb-nat-kvm.json` |
| Killercoda | 'You can use Killercoda completely for free... | qualifies-with-caveat | documented | 'Open up to 3 scenarios at the... | 'All environments are... | email | `dossier/compute/killercoda-free.json` |
| Kilo Code | Kilo Code: the platform is free for individ... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/kilo-code.json` |
| Kimsufi | KS-5 at USD 19.90/month: Intel Xeon E3-1270... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/kimsufi.json` |
| Kimsufi (OVHcloud) | no free tier; KS-3 is USD 30.00 a month for... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disks persist whi... | card | `dossier/compute/kimsufi-windows.json` |
| KINX IXcloud | The 기본 인스턴스 ladder starts at 1 vCPU with 1... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/kinx-ixcloud.json` |
| Koara Cloud | RUB 279 per month for START-1 in Germany: 1... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/koara-cloud.json` |
| Koyeb | One Free Instance per organization: 512 MB... | fails-identity | documented | one Free Instance per organizat... | no persistent storage... | card | `dossier/compute/koyeb.json` |
| Krova Cloud | Claim $5 in free credit - one-time, per acc... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Power off a Cube and... | email | `dossier/compute/krova-cube.json` |
| Lambda | no free tier: self-serve instances priced p... | paid-only | documented | not stated | not stated | email | `dossier/compute/lambda.json` |
| Lambda Cloud credits | Get USD 1,000 in cloud credits to build AI... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/lambda-cloud-credits.json` |
| Lambda Research Grant | 'We're committed to supporting groundbreaki... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lambda-research-grant.json` |
| LandVPS | RUB 90/month (RU-0): 1 vCore Intel Gold at... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/landvps.json` |
| LangSmith Sandboxes | one free seat and one free Serverless (Smal... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/langsmith-sandbox.json` |
| Latitude.sh | no free compute tier: metal, VM and GPU ins... | paid-only | documented | not stated | not stated | email | `dossier/compute/latitude-sh.json` |
| LayerOne | no free tier; the cheapest plan, gc.pico, i... | paid-only | documented | not applicable: the unit is a m... | a server runs and bil... | email | `dossier/compute/layerone.json` |
| LCCF Horizon Leadership | Large allocations from 125,000 to 500,000 S... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/lccf-horizon-leadership.json` |
| LeaderGPU | European dedicated bare-metal GPU servers s... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/leadergpu.json` |
| Leafcloud | 50 GPU hours a month, free, every month, on... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Persistent storage is... | card | `dossier/compute/leafcloud-run.json` |
| Leap0 | machines that spin up in 100 ms and tear do... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/leap0.json` |
| Leapcell | Hobby at USD 0 per seat a month: 20 project... | qualifies-with-caveat | documented | up to 3 vCPUs and 4 GB RAM per... | not stated on the pri... | email | `dossier/compute/leapcell.json` |
| LeapSwitch | USD 9.00/month (G2-LU-4G): 2 Epyc vCPUs, 4,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/leapswitch.json` |
| Leonardo.Ai | Free plan at USD 0 a month with 'Fast Token... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/leonardo-ai.json` |
| LFX Mentorship | Quoted from the funding announcement: 'we s... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lfx-mentorship.json` |
| Liara | 'هزینه اعتبار اولیه لیارا برای افتتاح حساب،... | trial-only | documented | not applicable: the unit is a m... | One charge, then a ha... | email | `dossier/compute/liara.json` |
| Lightning AI | one CPU Studio free 24/7 with a restart eve... | dead | documented | not applicable: the unit is a m... | a Studio keeps its fi... | any-phone | `dossier/compute/lightning-ai.json` |
| LightNode | no free tier; the Tokyo Start plan is USD 7... | paid-only | documented | not applicable: the unit is a m... | hourly billing; the i... | email | `dossier/compute/lightnode-tokyo.json` |
| Lightpanda | Explorer: USD 0 for ever, 10 browser hours... | qualifies-with-caveat | documented | not applicable: the unit is a m... | no session storage is... | email | `dossier/compute/lightpanda.json` |
| Linceris | EUR 14.99/month for VPS Package 1 in Frankf... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/linceris.json` |
| Akamai Cloud / Linode | No English signup credit is published. The... | paid-only | documented | not stated | not stated | card | `dossier/compute/linode.json` |
| Linuxzoo | 'Learn Linux from the safety of your chair... | fails-egress | documented | 'You are allowed to have only o... | 'This previous image... | email | `dossier/compute/linuxzoo.json` |
| Linveo | no free tier; the 16 GB Windows plan is USD... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/linveo-windows.json` |
| lisahost | CNY 35 per month as a limited-time price ag... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lisahost.json` |
| LITE.HOST | RUB 285 per month for the Kallisto row: 1 v... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lite-host.json` |
| LiteServer | EUR 6.00/month (HDD-1G): 1 core, 1,024 MB R... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/liteserver.json` |
| Little Creek Hosting | No storage VPS. Three NVMe plans: Starter a... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/little-creek-hosting.json` |
| LittleCreek | USD 7.95/month (Starter VPS): 2 vCPU, 4 GB... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/littlecreek.json` |
| Lium | Quoted, read 2026-10-22: 'New accounts can... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lium.json` |
| Livepeer Studio | Sandbox plan, free: 1,000 transcoding minut... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/livepeer-studio.json` |
| Lizard | 'Pro costs $19 a month and includes $19 in... | trial-only | documented | 'Sandboxes come in three sizes... | A successful pause st... | card | `dossier/compute/lizard.json` |
| Locaweb | no free tier; R$ 15,90 a month on a 24-mont... | fails-identity | documented | not applicable: the unit is a m... | the server persists w... | national-id | `dossier/compute/locaweb-vps.json` |
| Lovable | Lovable Free: "Daily build credits 5/day, 3... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lovable.json` |
| LowHosting | EUR 3.00/month (RKVMProtected, 1 GB): 1 Ryz... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lowhosting.json` |
| Luma AI | The published individual plans begin at Plu... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/luma-ai.json` |
| LumaDock | no free tier; VPS.S1 at USD 4.99 is the che... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/lumadock-vps-s1.json` |
| LUMI | Access to LUMI requires membership of a pro... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/lumi.json` |
| luo_cloud | no free tier; the smallest card on the stor... | qualifies | documented | not applicable: the unit is a m... | the container persist... | email | `dossier/compute/luo-cloud-lxc-nat.json` |
| Luxvps | EUR 4.50/month (KVM Rootserver Tiny): 1 Int... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/luxvps.json` |
| Lyceum | GPUs are billed per second with no subscrip... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/lyceum.json` |
| machine0 | no free tier: per-minute billing from $0.01... | paid-only | documented | not stated | not stated | email | `dossier/compute/machine0.json` |
| MacinCloud | no free tier and no trial on dedicated plan... | paid-only | documented | not stated | not stated | email | `dossier/compute/macincloud.json` |
| MacStadium | no free tier: Mac hosting on fixed monthly... | paid-only | documented | not stated | not stated | email | `dossier/compute/macstadium.json` |
| Magalu Cloud | R$ 100 in promotional credits in the first... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/magalu-cloud.json` |
| Malaysia Digital Accelera... | Up to RM 2 million in performance-based fun... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/malaysia-digital-acceleration.json` |
| Manus | Manus Free: "Free Plan Price: $0/month", "D... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/manus.json` |
| Manus Cloud Computer | no free tier: Cloud Computer is a persisten... | paid-only | documented | not stated | not stated | email | `dossier/compute/manus-cloud-computer.json` |
| Maritime | Free at $0/mo, no card needed; the first pa... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/maritime.json` |
| Marlin | TEE and ZK coprocessors for delegating work... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/marlin.json` |
| Massed Compute | Operator-run on-demand GPU VMs with a full... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/massed-compute.json` |
| Mastra | Mastra Platform Starter, $0 a month: 100K e... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/mastra.json` |
| Matpool | Chinese GPU cloud (JuChiYun) publishing per... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/matpool.json` |
| Metorial | a free Dev plan, a fixed-price Scale plan a... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/metorial.json` |
| 喵云 (miaomiao.moe) | No free tier. HGC-Nano is CNY 6.60 a month,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | monthly billing; no d... | card | `dossier/compute/miaomiao-hgc-nat-nano.json` |
| microLXC | 'Get a free LXC container with instant* dep... | qualifies-with-caveat | documented | not applicable: the unit is a c... | no retention term is... | institution | `dossier/compute/microlxc-tiny.json` |
| microsandbox | a monthly pool of 5 vCPU-hours, 20 GiB-hour... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/microsandbox.json` |
| Microsoft | Up to USD 200 in Startup credits immediatel... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/microsoft.json` |
| Microsoft Agents Academy | The official rules award no cloud credit. T... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/microsoft-agents-academy.json` |
| Microsoft AI | 'a total of $5 million in Azure service cre... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/microsoft-ai.json` |
| Microsoft Azure credits | 'Many Microsoft product teams grant Azure c... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/microsoft-azure-credits.json` |
| Microsoft Azure Free Account | USD 200 of credit for 30 days plus 750 hour... | trial-only | documented | not applicable: the unit is a m... | 365 d | card | `dossier/compute/microsoft-azure-free-account.json` |
| Microsoft Learn Student | 'Complete the registration activities, rece... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/microsoft-learn-student.json` |
| Mikrus | No free tier on this plan. Mikrus 1.0 is PL... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 14 d | card | `dossier/compute/mikrus-10-ipv6-mostly.json` |
| Millenial | HK KVM NAT 512M at USD 4.00/month on the ca... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/millenial.json` |
| mini.biz.id | Withdrawn. The site published a 'Micro 1' p... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/mini-biz-id.json` |
| Minicor | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/minicor.json` |
| MIOSA | $1 of usage every month with no monthly cha... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/miosa.json` |
| MiraclePlus Compute | Live English page, verbatim: 'MiraclePlus C... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/miracleplus-compute.json` |
| Mistral La Plateforme | Free mode still exists and its limits are n... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mistral-la-plateforme.json` |
| Mitos | USD 100 of signup credit, no card; prepaid... | paid-only | documented | not applicable: the unit is a m... | Storage is metered at... | email | `dossier/compute/mitos.json` |
| mivoCloud | S1 at EUR 5.00/month billed monthly, EUR 14... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mivocloud.json` |
| MLPerf | MLPerf awards no compute at all. The progra... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/mlperf.json` |
| Modal | Starter has no monthly fee and includes USD... | fails-identity | documented | not applicable: the unit is a s... | Volumes persist while... | card | `dossier/compute/modal.json` |
| Modal for Academics | Stated as 'Unlock up to $10k of credits to... | fails-identity | documented | not applicable: the unit is a c... | not applicable: the g... | institution | `dossier/compute/modal-for-academics.json` |
| Modelence | a free tier for hobby projects and prototyp... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/modelence.json` |
| molab | free: 4 CPUs and 32 GB RAM per notebook, an... | qualifies | documented | not applicable: the unit is a s... | a limited amount of p... | email | `dossier/compute/molab.json` |
| Mondoze | 2GB LINUX VPS ('2 GB Linux VPS (MY) V2') at... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mondoze.json` |
| MongoDB | Free MongoDB Atlas credits and Voyage AI to... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/mongodb.json` |
| Moonshot Kimi Hosted Agen... | no free tier: each hosted-agent session run... | paid-only | documented | not stated | not stated | email | `dossier/compute/moonshot-kimi.json` |
| Morph Cloud | 'Starting credit allocation / 0 MCUs' on th... | paid-only | documented | Instances 'Up to 64 vCPU', RAM... | No retention term is... | email | `dossier/compute/morph-cloud.json` |
| Morpheus | OpenAI-compatible inference through TEE-bac... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/morpheus.json` |
| Mosaic Sandbox | no free tier: $0.05 an hour of active compu... | paid-only | documented | not stated | not stated | email | `dossier/compute/mosaic.json` |
| MotherDuck | Lite plan, quoted from the FAQ: 'We also of... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/motherduck.json` |
| Mozilla Builders Accelerator | The programme's own page still advertises,... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mozilla-builders-accelerator.json` |
| Mozilla Foundation Human-... | 'Applicants to this cohort will be eligible... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mozilla-foundation-human-scale.json` |
| Mozilla Open Source | 'Generally anyone who maintains an open sou... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mozilla-open-source.json` |
| MrVM | The cheapest entry on the largest price-sor... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/mrvm.json` |
| Binder (mybinder.org) | free and unauthenticated: at least 1 GB RAM... | fails-quota | documented | not applicable: the unit is a s... | none: 'We do not offe... | anonymous | `dossier/compute/mybinder.json` |
| NAIRR Pilot | Compute, model and platform allocations fro... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nairr-pilot.json` |
| NAISS / PDC | Small test allocations on the NAISS Dardel... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/naiss-pdc.json` |
| Namespace | a 30-day free trial of Compute, Devboxes, G... | trial-only | documented | not stated | not stated | email | `dossier/compute/namespace.json` |
| nanoHUB | "Each free nanoHUB account comes with 10 GB... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/nanohub.json` |
| Naranja | no free tier; the cheapest listed plan is '... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/naranja-kvm-nvme-2gb.json` |
| Narwhal Cloud (独角鲸云, fuck... | No price is published anywhere reachable wi... | dead | documented | not applicable: the unit is a m... | the terms state 'We d... | email | `dossier/compute/narwhal-cloud-nat.json` |
| National AI Innovation | A build-only challenge on N-ATLAS, Nigeria'... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/national-ai-innovation.json` |
| NATKVM (KhanWebHost Limited) | no free tier; the LXC NAT line starts at US... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the container persist... | card | `dossier/compute/natkvm-nat-lxc.json` |
| NATVPS | VPS - NAT512 at USD 7.50/year: 512 MB RAM,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/natvps.json` |
| NatVPS.net | No free tier. VPS - NAT512 is USD 7.50 a ye... | qualifies-with-caveat | documented | not applicable: the unit is a m... | annual prepay; no del... | card | `dossier/compute/natvps-net-kvm-512-recheck.json` |
| NATVPS (NatVPS Services) | No free tier. VPS - NAT512 is USD 7.50 a ye... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 5 d | email | `dossier/compute/natvps-net-nat512.json` |
| NAVER Cloud / LINE-NAVER... | no free tier: pay-as-you-go servers across... | paid-only | documented | not stated | not stated | email | `dossier/compute/naver-cloud.json` |
| NAVER Cloud Platform | KRW 100,000 of signup credit, valid 3 month... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/naver-cloud-platform.json` |
| NEAR AI Cloud | Attested TEE inference on open-weight model... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/near-ai-cloud.json` |
| Nebius | no free tier: computing resources bill per... | paid-only | documented | not stated | not stated | email | `dossier/compute/nebius.json` |
| Nebius ConTree (Token Fac... | free while in beta: runs do not consume cre... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/nebius-contree.json` |
| Nebius research grants | GPU cloud credits, Token Factory tokens and... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nebius-research-grants.json` |
| NeevCloud | 'Sign up today and claim INR 2,000 in FREE... | trial-only | documented | not applicable: the unit is a m... | The CPU credit burns... | email | `dossier/compute/neevcloud.json` |
| Neo4j AuraDB | AuraDB Free, quoted from the quotas page: '... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/neo4j-auradb.json` |
| NEOXIS Corp. | no free tier is published; one fixed-term p... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/neoxis.json` |
| NERSC Exploratory | "Research projects that are new to NERSC an... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nersc-exploratory.json` |
| netcup | no free tier; VPS 500 G12.5 is EUR 8.26 a m... | paid-only | documented | not applicable: the unit is a m... | rented for the contra... | card | `dossier/compute/netcup.json` |
| netcup | no free tier; VPS 1000 G12.5 is EUR 14.50 a... | paid-only | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/netcup-vps-1000.json` |
| netcup | no free tier; the smallest listed VPS is 'V... | paid-only | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/netcup-vps-500-g12-5.json` |
| netcup | no free tier; VPS 2000 G12.5 is EUR 26.92 a... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/netcup-windows.json` |
| Netlen | no free tier; the entry plan is 'VPS - 1 ..... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/netlen-vps-2.json` |
| Netlify | Free at USD 0 forever with a 300-credit mon... | qualifies-with-caveat | documented | not stated on the pricing page;... | not stated on the pri... | email | `dossier/compute/netlify.json` |
| Netlify Open Source | 'Our Open Source plan includes: 10,000 cred... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/netlify-open-source.json` |
| NetMind | No amount is stated on the live page: https... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/netmind.json` |
| NetVolo | no free tier and no monthly cycle: VPS-Wind... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/netvolo-windows.json` |
| NetX | no free tier; VPS-0 is the entry tariff | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/netx-vps-0.json` |
| Nevacloud | IDR 50,000 of credit as a promo code, grant... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/nevacloud.json` |
| NexusBytes | no free tier; the cheapest advertised VPS i... | paid-only | documented | not applicable: the unit is a m... | not stated on the pri... | card | `dossier/compute/nexusbytes.json` |
| NHN Cloud | KRW 200,000 signup credit after registering... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/nhn-cloud.json` |
| Nineteen AI | Bittensor subnet 19 (Rayon Labs) advertises... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/nineteen-ai.json` |
| Nobus Cloud | Up to NGN 500,000,000 of cloud credit acros... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nobus-cloud.json` |
| NoctHost | no free tier is published; GPU VPS by the h... | paid-only | documented | not applicable: the unit is a m... | a GPU server is delet... | email | `dossier/compute/nocthost-gpu.json` |
| Nodus Compute | no free tier: six CPU and memory sizes from... | paid-only | documented | not stated | not stated | email | `dossier/compute/nodus-compute.json` |
| Nomic | a Free plan that needs no card: 'No credit... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/nomic.json` |
| Northflank | Sandbox plan at USD 0: 'Up to $20/mo of res... | fails-identity | documented | 2 services, 2 jobs and 1 databa... | resources persist whi... | card | `dossier/compute/northflank.json` |
| Nosana | The USD 50 is real as an announcement but n... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/nosana.json` |
| Noteable | no offer: the domain is parked and for sale... | dead | documented | not applicable: the unit is a s... | not applicable: the s... | email | `dossier/compute/noteable.json` |
| Notte | a free start without a card: USD 10 of cred... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/notte.json` |
| Novita AI Agent Sandbox | $100 of promotional credits after an accoun... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/novita.json` |
| NSF NCAR Derecho | An Exploratory and Classroom allocation car... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nsf-ncar-derecho.json` |
| NumFOCUS Small Development | 'Up to $10,000 can be awarded for each prop... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/numfocus-small-development.json` |
| NVIDIA Academic Grant | 'Up to 30,000 NVIDIA H100 80 GB hours or eq... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nvidia-academic-grant.json` |
| NVIDIA DGX Cloud | No self-serve free tier. The product's own... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nvidia-dgx-cloud.json` |
| NVIDIA Inception | A free program with no application fees, de... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/nvidia-inception.json` |
| NVIDIA LaunchPad | Withdrawn. The 2024-02-29 capture states 'N... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/nvidia-launchpad.json` |
| O'Shaughnessy Fellowship | '1 Year. Up to $100,000.' The site states '... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/o-shaughnessy-fellowship.json` |
| OakHost | no free tier: dedicated Mac mini hosting fr... | paid-only | documented | not stated | not stated | email | `dossier/compute/oakhost.json` |
| oblako.kz | A free test server for up to 5 days for leg... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/oblako-kz.json` |
| Oblivus | no free GPU tier is published; on-demand ra... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/oblivus.json` |
| Observable | free notebooks with 'Few tokens / day' of a... | fails-quota | documented | not applicable: the unit is a s... | not stated | email | `dossier/compute/observable-free.json` |
| Ocean Network / | A self-serve grant with no wallet extension... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ocean-network.json` |
| OLCF Director's Discretio... | The OLCF Director's Discretionary program a... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/olcf-director-s-discretionary.json` |
| Omega Gradient | no free tier is published; the marketplace... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/omega-gradient.json` |
| Omnara | no platform fee: the software is free and u... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/omnara.json` |
| OmniRun | no free tier and no price list: capacity is... | paid-only | documented | not stated | not stated | email | `dossier/compute/omnirun.json` |
| Ona (formerly Gitpod) | no self-serve free tier is reachable: the G... | paid-only | documented | not stated | not established | card | `dossier/compute/ona.json` |
| Ona Cloud | The vendor's own notice, published 2026-10-... | dead | documented | not applicable: the unit is a m... | The product ends on a... | email | `dossier/compute/ona-cloud.json` |
| Onamae.com VPS | The 1 GB plan gives 2 vCPU, 1 GB memory and... | paid-only | documented | not applicable: the unit is a m... | The minimum period is... | card | `dossier/compute/onamae-com-vps.json` |
| OneCLI | Free, $0: an isolated VM per employee, all... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/onecli.json` |
| OneProvider | The Paris clearance tier lists an Atom C235... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/oneprovider.json` |
| OnWorks | 'It is a free emulation platform that does... | fails-quota | documented | one workstation per session; no... | 'OnWorks destroys the... | anonymous | `dossier/compute/onworks-workstation.json` |
| Open Intelligence Foundation | The application is a single web form with e... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/open-intelligence-foundation.json` |
| Open Technology Fund | 'Awards are between $10,000 and $900,000 fo... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/open-technology-fund.json` |
| Open Telekom Cloud / T Cl... | EUR 250 of starting credit on a booked cont... | trial-only | documented | not stated | not stated | institution | `dossier/compute/open-telekom-cloud.json` |
| OpenAI Codex | 'Open-source maintainers can apply for API... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/openai-codex.json` |
| OpenAI Containers (Code I... | no container tier: the API is priced per mi... | paid-only | documented | not stated | not stated | email | `dossier/compute/openai-containers.json` |
| OpenComputer | a Free tier with up to 2 shared vCPU, 2 GB... | paid-only | documented | not applicable: the unit is a m... | not stated | card | `dossier/compute/opencomputer.json` |
| OpenPond Cloud Sandboxes | a Free tier with limited monthly hosted usa... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/openpond.json` |
| OpenRelay | no free GPU tier is published; list rates p... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/openrelay.json` |
| OpenReward Sandboxes | no free tier for compute: resources bill by... | fails-identity | documented | not stated | not stated | institution | `dossier/compute/openreward.json` |
| OpenRouter | Free-model requests (model ids ending in:fr... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/openrouter.json` |
| Red Hat OpenShift (Harbor... | not stated: https://www.redhat.com/en/techn... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/openshift.json` |
| OpenSSF Alpha-Omega | 'With an annual budget of over $7M, Alpha-O... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/openssf-alpha-omega.json` |
| Opensteer | $5 of model credits at signup plus $5 a mon... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/opensteer.json` |
| Openworld | A free container VPS: 'Every plan includes... | qualifies-with-caveat | documented | not applicable: the unit is a c... | 7 d | email | `dossier/compute/openworld.json` |
| Opus Host | '1 vCPU, 1 GB RAM und 20 GB SSD - kostenlos... | qualifies-with-caveat | documented | one free server per account: th... | The plan object carri... | email | `dossier/compute/opus-host-free.json` |
| Oracle Cloud Always Free | 1,500 OCPU-hours and 9,000 GB-hours a month... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Always Free resources... | card | `dossier/compute/oracle-cloud.json` |
| Oracle Cloud Infrastructure | A refutation. A widely syndicated claim sta... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/oracle-cloud-infrastructure.json` |
| Oracle Cloud Free Trial (... | Oracle Cloud Free Tier allows you to sign u... | trial-only | documented | not applicable: the offer is a... | 30 d | card | `dossier/compute/oracle-cloud-trial.json` |
| Oracle Cloud Always Free | up to two VM.Standard.E2.1.Micro instances,... | qualifies-with-caveat | documented | 200 GB of combined boot and blo... | 7 d | card | `dossier/compute/oracle-cloud-vpn-node.json` |
| Oracle Startup Growth | Oracle may provide selected participants wi... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/oracle-startup-growth.json` |
| Ori Global Cloud | no free lane and no self-serve signup. Ori... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/ori-global-cloud.json` |
| orkestr Sandboxes | free to start with no credit card, on per-s... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/orkestr.json` |
| OSPool | "The OSPool is a source of computing capaci... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/ospool.json` |
| Outreachy | 'Paid - $7,000 USD total internship stipend... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/outreachy.json` |
| OVHcloud GPU instances | USD 200 of free credit for a new public-clo... | trial-only | documented | not stated | not stated | card | `dossier/compute/ovh-gpu.json` |
| OVHcloud Public Cloud | US$200 in Public Cloud credits for one mont... | trial-only | documented | not stated | not stated | card | `dossier/compute/ovhcloud.json` |
| OVHcloud | VPS 2027 line. VPS-1 starting at USD 4.54/m... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ovhcloud-2.json` |
| OVHcloud Kimsufi | The KS range is advertised from EUR 9.99 ex... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ovhcloud-kimsufi.json` |
| OVHcloud Rise | RISE-1 is EUR 56.99 a month for an Intel Xe... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ovhcloud-rise.json` |
| OVHcloud So you | soyoustart.com no longer sells to new custo... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ovhcloud-so-you.json` |
| OVHcloud | no free tier; VPS-1 is the entry rung of th... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/ovhcloud-vps-1-2027.json` |
| OVHcloud | no free tier; VPS-4 is EUR 23.49/month on t... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/ovhcloud-windows.json` |
| Ownkube | No subscription and no perpetual free allow... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ownkube.json` |
| Packet AI | no free GPU tier is published; the rate car... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/packet-ai.json` |
| PandaStack | a $5.40 free credit, 1 GiB of persistent vo... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/pandastack.json` |
| Paperspace | C4, C5 and C7 machines are included in a Fr... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/paperspace.json` |
| Paperspace Gradient | USD 0 with 'FREE GPU', a 12-hour auto-shutd... | qualifies-with-caveat | documented | not applicable: the unit is a s... | 5 GB of storage on th... | email | `dossier/compute/paperspace-gradient.json` |
| Paperspace (DigitalOcean)... | Quoted from the machine table: 'GPU+ (M4000... | qualifies | documented | 'Notebook Limit: Only one noteb... | 'For your machine lea... | email | `dossier/compute/paperspace-gradient-free-tier.json` |
| ParalonCloud | no free GPU tier is published; the RTX 4090... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/paraloncloud.json` |
| Party | $100 in credits, one time, with 2 concurren... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/party.json` |
| 帕斯云Nat (Pasyun NAT) | No free tier. 荷兰Nat4-DC1-1 is CNY 3.00 a mo... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 5 d | email | `dossier/compute/pasyun-nat4-dc1-1.json` |
| PenDC | Two months of free server hosting, stated o... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/pendc.json` |
| ph24 (ProHosting24) | No free tier. Cheapest orderable monthly of... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ph24.json` |
| ph24 Cloud (ProHosting24) | No free tier: every B1 server carries an ho... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ph24-cloud.json` |
| Phala Cloud | Confidential VMs from USD 0.06 per hour and... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/phala-cloud.json` |
| phoenixNAP dedicated outlet | The all-servers price list opens at EUR 89.... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/phoenixnap-dedicated-outlet.json` |
| PhotonVPS | NVMe - X at USD 5.00/month: 1 CPU core, 204... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/photonvps.json` |
| Pika | A USD 0 plan exists but carries no credit:... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/pika.json` |
| PillDrops | Start free with a $5 usage credit and no ca... | qualifies-with-caveat | documented | not applicable: the unit is a m... | unknown: Personal and... | email | `dossier/compute/pilldrops.json` |
| Pipekit | a free trial rather than a free tier; the p... | trial-only | documented | not stated | not stated | email | `dossier/compute/pipekit.json` |
| Pipeshift | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/pipeshift.json` |
| Play with Docker | no longer available: Play with Docker is un... | dead | documented | not applicable: the unit is a m... | the service is withdrawn | anonymous | `dossier/compute/play-with-docker.json` |
| Playgent | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/playgent.json` |
| Podway | During early access, 'your first app on a M... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/podway.json` |
| Porter | a startup programme granting 6 months free;... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/porter.json` |
| Posit Cloud | USD 0 forever: 25 compute hours a month, 1... | qualifies-with-caveat | documented | not applicable: the unit is a s... | 25 projects persist o... | email | `dossier/compute/posit-cloud-free.json` |
| PPIO GPU | RTX 4090 24GB in a 16 vCPU / 62 GiB contain... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/ppio-gpu.json` |
| PPIO Agent Sandbox | no free tier: vCPU and RAM bill independent... | paid-only | documented | not stated | not stated | email | `dossier/compute/ppio-sandbox.json` |
| PQ.Hosting | No server is sold at this domain. pq.hostin... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/pq-hosting.json` |
| PRACE | PRACE no longer runs its own access calls;... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/prace.json` |
| Predibase | gone as an independent product. The pricing... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/predibase.json` |
| Prime Intellect Sandboxes | no free tier: tier-free per-second pricing... | paid-only | documented | not stated | not stated | email | `dossier/compute/prime-intellect.json` |
| Prime Intellect | The grant program is gone. Its own page now... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/prime-intellect-2.json` |
| PrivateByte | USD 5.99/month for Flare: 1 vCPU, 2 GB RAM,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/privatebyte.json` |
| Privex (Privex Inc.) | No free tier. VNANO-SE-SSD is USD 0.99 a mo... | qualifies | documented | not applicable: the unit is a m... | 25 d | email | `dossier/compute/privex-vnano-se-ssd-ipv6.json` |
| Prized | 'New workspaces get $30 of free credit, onc... | qualifies-with-caveat | documented | On the free credit 'Nano, Micro... | Asleep, a box costs o... | email | `dossier/compute/prized.json` |
| PSC Neocortex | Free wafer-scale accelerator time on Cerebr... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/psc-neocortex.json` |
| Psifactor | 'kontener LXC zarządzany przez Incus', 'do... | qualifies-with-caveat | documented | 'możliwość podmontowania zasobó... | 'Nie można posiadać V... | card | `dossier/compute/psifactor-free.json` |
| PythonAnywhere | USD 0 a month: one web app, up to 2 console... | fails-quota | documented | not applicable: the unit is a m... | not stated on the pri... | email | `dossier/compute/pythonanywhere.json` |
| QDE | Ryzen Mini at EUR 3.95 a month on the cart'... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/qde.json` |
| Qiniu Cloud AI | Per-second billing with no free compute all... | fails-identity | documented | not applicable: the unit is a m... | A sandbox has a 5 min... | national-id | `dossier/compute/qiniu-cloud-ai.json` |
| Qoddi | The free tier covers static sites only: 'St... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/qoddi.json` |
| Qodo | no permanent free tier: "We don't offer a p... | trial-only | documented | not applicable: the unit is a m... | 14 days then zero, so... | email | `dossier/compute/qodo.json` |
| Qovery | No free plan. Starter is USD 299 a month bi... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/qovery.json` |
| Qualcomm AI Hub | Free compile, profiling and inference on re... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/qualcomm-ai-hub.json` |
| Quansight | This was the clearest free-GPU-CI offer in... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/quansight.json` |
| Quantum Inspire | "Quantum Computing for everybody - Quick an... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/quantum-inspire.json` |
| Quarto Pub | no free tier available: 'Quarto Pub is clos... | dead | documented | not applicable: the unit is a s... | not applicable to a n... | email | `dossier/compute/quarto-pub.json` |
| Qyrax | USD 3.00 per month for the Stryx plan in Ne... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/qyrax.json` |
| Rabisu | Aydin VPS x4 at USD 2.99 a month on the car... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/rabisu.json` |
| RackNerd | 1 GB KVM VPS at USD 21.99/year: 1 vCPU, 1 G... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/racknerd.json` |
| RackNerd | no free tier; the smallest plan on the spec... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | email | `dossier/compute/racknerd-1gb-special.json` |
| RackNerd | no free tier; the specials ladder starts at... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/racknerd-4gb.json` |
| RackNerd | no free tier; the specials ladder starts at... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/racknerd-8gb-annual-special.json` |
| RackNerd | no free tier; the Black Friday 2025 store l... | dead | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/racknerd-black-friday-2025.json` |
| RackNerd | no free tier; the smallest current special... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/racknerd-specials.json` |
| Railway | Free plan at USD 0 a month with USD 1 of us... | qualifies-with-caveat | documented | 1 vCPU and 0.5 GB RAM per servi... | the USD 1 credit does... | email | `dossier/compute/railway.json` |
| Rainyun | A one-yuan one-day trial of each product, q... | trial-only | documented | not applicable: the unit is a m... | The trial is one day... | national-id | `dossier/compute/rainyun.json` |
| ransomIT | KVM2GB at AUD 20 / month, on a page that st... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ransomit.json` |
| RareCloud | The vendor's pricing feed lists Micro KVM a... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/rarecloud.json` |
| ReadyDedis | AMD-1 at USD 5.00/month: 1 core, 1 GB RAM,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/readydedis.json` |
| ReconV | No free tier. The smallest LXC plan is PLN... | qualifies | documented | not applicable: the unit is a m... | not stated on any pag... | email | `dossier/compute/reconv-vps-nat512mb.json` |
| Red Hat Developer Sandbox | 'The Developer Sandbox provides you with a... | qualifies-with-caveat | documented | one project per sandbox, on a p... | 'Your Developer Sandb... | any-phone | `dossier/compute/red-hat-developer-sandbox.json` |
| Reflex | a Free plan at $0 with limited usage for AI... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/reflex.json` |
| Refresh | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/refresh.json` |
| Release | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/release.json` |
| Remote Browser | 1 browser-hour a month on Free with no card... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/remote-browser.json` |
| RemoteHost | Starter is USD 20 per month and includes 61... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/remotehost.json` |
| Render | A Free web service with an ephemeral filesy... | qualifies-with-caveat | documented | no per-object cap; the free tie... | the filesystem is eph... | email | `dossier/compute/render.json` |
| Render Hobby | Batch 1 recorded Render's Hobby plan at 5 G... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/render-hobby.json` |
| Render Network | The credit offer is withdrawn. Page quoted:... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/render-network.json` |
| RentaMac (rentamac.io) | no free tier: continuous 24/7 Mac access bi... | paid-only | documented | not stated | not stated | email | `dossier/compute/rentamac.json` |
| Replicas | $100 of free usage with no card required | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/replicas.json` |
| Replicate | no free tier: hardware bills per second fro... | paid-only | documented | not stated | not stated | email | `dossier/compute/replicate.json` |
| Replit | Starter is free: daily Agent credits up to... | trial-only | documented | not applicable: the unit is a s... | 30 d | email | `dossier/compute/replit.json` |
| RES | RES resources are free of charge through op... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/res.json` |
| Rescale | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/rescale.json` |
| Retzor | EUR 3 per month for 1 vCPU, 1 GB ECC REG, 1... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/retzor.json` |
| Rev AI | Pay-as-you-go with 'Free credits equivalent... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/rev-ai.json` |
| Revyl | a free start on a mobile test-automation se... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/revyl.json` |
| Rivet (Actors & agentOS) | 100,000 awake actor hours a month on the fr... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/rivet.json` |
| Riza Code Interpreter | an execution runtime with hard per-invocati... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/riza.json` |
| ROUTE64 (AS212895) | free IPv6 tunnel with a routed /56 subnet o... | qualifies-with-caveat | documented | a routed /56 per tunnel endpoin... | static IP allocations... | email | `dossier/compute/route64-tunnel.json` |
| Royal-Server.Ro | no free tier; the cheapest Linux VPS is Int... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/royal-server-ro.json` |
| Run Cloud | no longer available to new organizations; e... | dead | documented | not applicable: the unit is a m... | a sandbox can be snap... | card | `dossier/compute/run-cloud.json` |
| Runcrate | no free GPU tier is published; the live rat... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/runcrate.json` |
| RunKit | a Node.js notebook in the browser with ever... | paid-only | documented | not stated | not stated | email | `dossier/compute/runkit.json` |
| Runloop | 'Start Your Free Pro Trial', 'No credit car... | trial-only | documented | No devbox shape is published on... | '100 GB Free Storage'... | email | `dossier/compute/runloop.json` |
| RunMyJob | Batch 1 recorded RunMyJob as a perpetual fr... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/runmyjob.json` |
| RunPod | no free GPU tier is published; the on-deman... | paid-only | documented | not applicable: the unit is a m... | network storage is bi... | card | `dossier/compute/runpod.json` |
| Runsite | The free tier is static sites only: 'Static... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/runsite.json` |
| Runta | $50 trial balance with no payment method, c... | trial-only | documented | not stated | not stated | email | `dossier/compute/runta.json` |
| Runway | Free plan, printed as 'Free forever' with '... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/runway.json` |
| RUVDS | A 3-day free trial of any configuration cos... | trial-only | documented | not applicable: the unit is a m... | The trial is three da... | any-phone | `dossier/compute/ruvds.json` |
| RuWeb | Six days of VPS free, activated automatical... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/ruweb.json` |
| Sail Research (Sailboxes) | no free compute tier: the page prices model... | paid-only | documented | not stated | not stated | email | `dossier/compute/sail.json` |
| Sailboxes | A USD 5 monthly credit is advertised when a... | qualifies-with-caveat | documented | sandbox sizes S, M and L with a... | Independent disks and... | card | `dossier/compute/sailboxes.json` |
| Sakura Internet Cloud | no free tier: servers bill monthly, daily o... | paid-only | documented | not stated | not stated | email | `dossier/compute/sakura-cloud.json` |
| Sakura Cloud | No free trial, stated outright: 'さくらのクラウドは無... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/sakura-cloud-2.json` |
| Sakura Cloud certification | A one-month free Sakura Cloud learning envi... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/sakura-cloud-certification.json` |
| Sakura Cloud Koukaryoku | Japanese incumbent GPU VM with an hourly, d... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/sakura-cloud-koukaryoku.json` |
| Sakura Cloud student | 'アンバサダーには、毎月10万円分のクラウドリソースが無償で提供されます' (amba... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/sakura-cloud-student.json` |
| Sakura Internet (さくらのVPS) | no free tier; the 512 MB plan is JPY 590 a... | qualifies | documented | not applicable: the unit is a m... | the instance persists... | any-phone | `dossier/compute/sakura-vps.json` |
| Sakura VPS 2-week | Every plan is free for two weeks when the o... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/sakura-vps-2-week.json` |
| Salad | No free trial; pay-as-you-go with no minimu... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/salad.json` |
| SambaNova Cloud | No free lane left. The Free plan now reads... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/sambanova-cloud.json` |
| Samsung SDS Cloud Platform | no free tier: services bill by the used hou... | paid-only | documented | not stated | not stated | email | `dossier/compute/samsung-cloud.json` |
| Samsung Cloud Platform | KRW 300,000 of credit to a new account that... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/samsung-cloud-platform.json` |
| Sandbox as a Service | $5 of signup credit, which the page estimat... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/sandbox-as-a-service.json` |
| Sandbox0 | $5 of free credit for new users with no car... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/sandbox0.json` |
| Sandock | Plus is USD 5 per month for 5 sandboxes, 2... | paid-only | documented | not applicable: the unit is a m... | The session timeout i... | card | `dossier/compute/sandock.json` |
| Sanfengyun | A free cloud server at 1 core, 1 GiB RAM, 5... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/sanfengyun.json` |
| SAP Business Technology | "When using Kyma, the free plan is availabl... | trial-only | documented | not applicable: the unit is a m... | Kyma, the managed Kub... | card | `dossier/compute/sap-business-technology.json` |
| Savannaa | 750 hours a month of a t2.micro (1 vCPU, 1... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/savannaa.json` |
| Scaleway Instances | no free tier: instances from EUR 0.01428 an... | paid-only | documented | not stated | not stated | card | `dossier/compute/scaleway.json` |
| Scaleway | STARDUST1-S: 1 shared vCPU (AMD EPYC 7281 o... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/scaleway-2.json` |
| Scaleway Apple silicon (M... | no free tier: Apple Silicon instances from... | paid-only | documented | not stated | not stated | email | `dossier/compute/scaleway-apple-silicon.json` |
| Scaleway | no offer: the page reads 'No Black Friday d... | dead | documented | not applicable: the unit is a m... | not applicable; no of... | card | `dossier/compute/scaleway-black-friday.json` |
| Scaleway GPU instances | no free tier: pay-as-you-go GPU instances,... | paid-only | documented | not stated | not stated | email | `dossier/compute/scaleway-gpu.json` |
| Scaleway | no free tier; STARDUST1-S is 'EUR 0.0006 /H... | paid-only | documented | not applicable: the unit is a m... | the instance persists... | card | `dossier/compute/scaleway-stardust1-s.json` |
| Scalingo | no perpetual free tier: 'start free for 30... | trial-only | documented | not applicable: the unit is a c... | not applicable to a f... | card | `dossier/compute/scalingo.json` |
| SchnellNode | 15GB-R10SSD at EUR 4.00/month: 1 vCPU acces... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/schnellnode.json` |
| SciServer | Anyone can create a free account and run Ju... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/sciserver.json` |
| Scrapeless Agent Browser | no free tier: the product is a subscription... | paid-only | documented | not stated | not stated | email | `dossier/compute/scrapeless.json` |
| Scrapfly Cloud Browser | 1,000 API credits on a $0 plan with 5 concu... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/scrapfly.json` |
| Scraping Bee | 1,000 free API credits at signup with no ca... | trial-only | documented | not stated | not stated | email | `dossier/compute/scrapingbee.json` |
| SDF Public Access UNIX Sy... | The free USERS level: 20 MB disk quota for... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 730 d | email | `dossier/compute/sdf-public-access-unix.json` |
| Sealos DevBox | no free tier: fixed monthly resource packag... | paid-only | documented | not stated | not stated | card | `dossier/compute/sealos-devbox.json` |
| Segfault (THC) | 'Segfault offers free unlimited Root Server... | qualifies | documented | one root server per SECRET; a n... | 'Data in your home di... | anonymous | `dossier/compute/segfault-net.json` |
| Selectel | No free test. The provider's own FAQ states... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/selectel.json` |
| Senko Digital | EUR 2.29 per month for DE-BUDGET-1 in Frank... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/senko-digital.json` |
| Sentry | Open-Source Sponsorship Plan, granted on ap... | qualifies-with-caveat | documented | unverified: the sponsorship pla... | unverified: the spons... | email | `dossier/compute/sentry.json` |
| serv00 | 3 GB of SSD storage, unlimited data transfe... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 90 d | email | `dossier/compute/serv00.json` |
| Servarica | The dedicated list, in USD with a CAD figur... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/servarica.json` |
| Server4Agent | $2 of trial credits with 5 GB of storage; u... | trial-only | documented | not stated | not stated | email | `dossier/compute/server4agent.json` |
| Servera | EUR 3.16 per month on a 12-month term (EUR... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/servera.json` |
| ServerCrate | no free cloud server; the cheapest is SC-0... | paid-only | documented | not applicable: the unit is a m... | unverified: the cloud... | email | `dossier/compute/servercrate.json` |
| ServerHost | Starter 2GB VPS at USD 16.99/year (USD 1.42... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/serverhost.json` |
| ServerHost | No free tier. The advertised entry plan is... | paid-only | documented | not applicable: the unit is a m... | The VPS persists whil... | email | `dossier/compute/serverhost-2gb-promo.json` |
| Server Mikro | No free tier. VPS NAT LXC 1gb ram is Rp10.0... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the container persist... | email | `dossier/compute/servermikro-nat-lxc-1gb.json` |
| ServerPacket | no free tier; the 16 GB Windows plan is USD... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/serverpacket-windows.json` |
| Serverspace | A free trial of a virtual server of up to 8... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/serverspace.json` |
| ServeTheWorld | GP32 at NOK 79/month list price (NOK 39/mon... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/servetheworld.json` |
| ServTech | RUB 500 per month for MSK-PRO-1: 1 vCPU at... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/servtech.json` |
| Public Free Suffix - SEUS... | Quoted from the announcement body: 'One sha... | qualifies-with-caveat | documented | not applicable: the unit is a v... | 60 d | email | `dossier/compute/seus-light-servers.json` |
| Sevalla | static site hosting at USD 0 a month; appli... | paid-only | documented | not applicable to application h... | not applicable: nothi... | email | `dossier/compute/sevalla.json` |
| SF Compute (GPU | A market for whole 8-GPU nodes, not single... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/sf-compute-gpu.json` |
| SF Tensor | No per-GPU hourly price is listed on the pa... | paid-only | documented | not stated | not stated | email | `dossier/compute/sf-tensor.json` |
| SF Compute (GPU market +... | no free compute. The pricing table lists on... | paid-only | documented | not stated | not stated | email | `dossier/compute/sfcompute.json` |
| Shadeform | no free compute allowance is stated on the... | paid-only | documented | not stated | not stated | email | `dossier/compute/shadeform.json` |
| Shardflux | a trial at Pro limits that ends at the cap... | trial-only | documented | not stated | not stated | email | `dossier/compute/shardflux.json` |
| shellbox | No free tier; a prepaid balance with a USD... | qualifies-with-caveat | documented | not applicable: the unit is a m... | Parked (stopped) boxe... | anonymous | `dossier/compute/shellbox.json` |
| shellter.me | 'A free bash account on a shared FreeBSD ho... | qualifies | documented | not applicable: the unit is a Z... | 90 d | email | `dossier/compute/shellter-me.json` |
| Shin VPS | The 1 GB plan with 1 core and 30 GB NVMe is... | paid-only | documented | not applicable: the unit is a m... | The minimum term is t... | card | `dossier/compute/shin-vps.json` |
| Shiper | Free Hobby plan, quoted: 'USD 0 /mo - Autom... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/shiper.json` |
| Shuttle | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/shuttle.json` |
| Sieve | no GPU or compute price is listed: the page... | paid-only | documented | not stated | not stated | email | `dossier/compute/sieve.json` |
| SiliconFlow | International site (siliconflow.com): a new... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/siliconflow.json` |
| SiliconKiwi | Kiwi Go at NZD 8.00/month: 2 vCPU, 1 GB RAM... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/siliconkiwi.json` |
| Silly Development | '25% of a CPU core, 256 MB of memory, and 5... | qualifies-with-caveat | documented | '2 databases per account, 50 MB... | 'No renewal button an... | email | `dossier/compute/sillydev-free.json` |
| SiMa.ai Edgematic | A free cloud lane onto SiMa.ai MLSoC and ML... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the beta is the clock... | card | `dossier/compute/sima-ai-edgematic.json` |
| SIMPLE CLOUD | RUB 216 per month: 512 MB RAM, 1 CPU core,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/simple-cloud.json` |
| SimpleSandbox | Free $0: 1M credits a month, 3 concurrent s... | qualifies-with-caveat | documented | not applicable: the unit is a s... | The sandbox advertise... | email | `dossier/compute/simplesandbox.json` |
| SingleStore | Shared Edition, quoted: 'SingleStore provid... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/singlestore.json` |
| Skhron | XSIG-SE-0: the store cart read 2026-11-07 p... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/skhron.json` |
| Skhron | No free tier. XSIG-SE-0 is EUR 1.69 a month... | qualifies | documented | not applicable: the unit is a m... | the plan is billed pe... | email | `dossier/compute/skhron-xsig-se-0.json` |
| SKRIME | No free tier. EPYC 1G is EUR 0.99 a month c... | qualifies | documented | not applicable: the unit is a m... | not stated on any pag... | email | `dossier/compute/skrime-epyc-1g-ipv6.json` |
| Skyhook | a Kubernetes PaaS with preview environments... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/skyhook.json` |
| Skyvern | Free with 5,000 credits and 1 concurrent ru... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/skyvern.json` |
| SmartHost | USD 2.95/month: 10 GB NVMe, 1 GB guaranteed... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/smarthost.json` |
| SmokyHosts | Mini VPS at USD 2.95/month: 1 vCPU, 1 GB RA... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/smokyhosts.json` |
| smol machines | $100 of one-time credit that behaves as ord... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/smol-machines.json` |
| Smooth | a free tier with basic features and limited... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/smooth.json` |
| SnapDeploy | One Small container per app, up to 4 apps,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 100 running hours a m... | email | `dossier/compute/snapdeploy.json` |
| Snowflake | Start your 30-day Snowflake trial with USD... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/snowflake.json` |
| SoftShellWeb | USD 5.00/month in Amsterdam: 1 core, 1 GB E... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/softshellweb.json` |
| SoftShellWeb | No free tier. The cheapest plan is USD 9.95... | qualifies | documented | not applicable: the unit is a m... | The container persist... | email | `dossier/compute/softshellweb-lxc-ipv6-only.json` |
| Solari | $3 of credits a month on a $0 plan, session... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/solari.json` |
| SolidVPS | LNX-CS-2GB at USD 5.95/month: 1 vCore, 2 GB... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/solidvps.json` |
| Sourcegraph Cody | "As of July 23, 2025, the following plans w... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/sourcegraph-cody.json` |
| Sovereign Tech Fellowship | 'we will hire up to twelve Sovereign Tech F... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/sovereign-tech-fellowship.json` |
| Sovereign Tech Fund | Quoted requirement: 'The cost of the work d... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/sovereign-tech-fund.json` |
| SpaceWeb | Three days of any VPS tariff or of S3 objec... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/spaceweb.json` |
| SparkCloud | SparkCloud publishes a six-part free stack... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/sparkcloud.json` |
| SparkleHosting | none: the domain resolves to a HugeDomains... | dead | documented | not applicable: no service rema... | not applicable: no se... | anonymous | `dossier/compute/sparklehosting-dead.json` |
| Specific | Free with unlimited API requests and users... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/specific.json` |
| SpectraIP | VPS X2 at EUR 3.50/month: 1 CPU core, 2 GB... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/spectraip.json` |
| Speechmatics | 'Start with $100 in free credits, no card r... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/speechmatics.json` |
| SpeedyPage | AMD Ryzen VPS at GBP 3.50/month: 1 Ryzen co... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/speedypage.json` |
| Spheron | GPU marketplace that aggregates capacity fr... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/spheron.json` |
| Sprites (Fly.io) | no free tier: compute bills by the second f... | paid-only | documented | not stated | not stated | email | `dossier/compute/sprites.json` |
| SST | The SST Console is free for workspaces with... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/sst.json` |
| ST-Hosting | No free tier. The smallest IPv6-only LXC pl... | qualifies | documented | not applicable: the unit is a m... | 14 d | email | `dossier/compute/st-hosting-ipv6-lxc-type9.json` |
| Stability AI | 'Get started with 25 free credits', where '... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/stability-ai.json` |
| StarSling | no free tier: per-minute runners from $0.00... | paid-only | documented | not stated | not stated | email | `dossier/compute/starsling.json` |
| Start-Up Chile | Equity-free co-financing for a 4-month prog... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/start-up-chile.json` |
| Startup India Seed | Up to INR 20 lakh as a milestone-based gran... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/startup-india-seed.json` |
| Startup SG Tech | Competitive grant for deep-tech commerciali... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/startup-sg-tech.json` |
| StarverseAI student support | Quoted from the vendor announcement dated 2... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/starverseai-student-support.json` |
| StateSet Sandbox | Hobby is USD 0 a month 'plus usage, billed... | trial-only | documented | max sandbox runtime 45 minutes... | Not stated on the pri... | card | `dossier/compute/stateset.json` |
| Staxa | Free plan is a sandbox: '$0 - Tenants inclu... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/staxa.json` |
| Steel | Launch: USD 0 a month plus usage, USD 30 of... | trial-only | documented | not applicable: the unit is a m... | 7 d | email | `dossier/compute/steel.json` |
| Strapi Cloud | removed plan: the Free plan included 10 GB... | dead | documented | not applicable: the unit is a m... | Both dates are in the... | email | `dossier/compute/strapi-cloud.json` |
| STRATO | no free tier; VPS XL is EUR 79.00/month inc... | paid-only | documented | not applicable: the unit is a m... | the disk persists for... | card | `dossier/compute/strato-windows.json` |
| Strike | Budget line 'Pico' at EUR 25.00/year: 1 vCP... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/strike.json` |
| Strong Compute | a free account in demo mode, plus a 3-month... | paid-only | documented | not stated | not stated | email | `dossier/compute/strong-compute.json` |
| student voucher | A CNY 300 no-threshold voucher quoted as 通过... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/student-voucher.json` |
| Suga | Free plan at USD 0 with no credit card: 1 p... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/suga.json` |
| Suno | Free plan at USD 0: the vendor's own help c... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/suno.json` |
| Superserve | Free with $100 of credit, pay-as-you-go aft... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/superserve.json` |
| SURF | A Small Compute application can request "up... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/surf.json` |
| Surfsky | free credit at signup with no card, 10 conc... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/surfsky.json` |
| SwedenDedi | NVMe SSD VPS 2 GB at EUR 10.00 per month in... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/swedendedi.json` |
| Swiss AI Initiative | Small project grants of 'typically ... betw... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/swiss-ai-initiative.json` |
| Tabnine | no free lane and no self-serve price: tabni... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/tabnine.json` |
| tama | no free tier: machines from 1 to 32 vCPU an... | paid-only | documented | not stated | not stated | email | `dossier/compute/tama.json` |
| TAPGPU (listed as Stabili... | No free tier stated; GPU instances are bill... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | country-phone | `dossier/compute/tapgpu.json` |
| Targon | No signup credit. Inventory page, price per... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/targon.json` |
| Technology Innovation Agency | Grant funding for technology development at... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/technology-innovation-agency.json` |
| Teclada | a Free tier for non-commercial use; paid pl... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/teclada.json` |
| Tembo | Free trial: 'included usage allowance, up t... | paid-only | documented | not applicable: the unit is a m... | unknown: 'Stopped, sn... | email | `dossier/compute/tembo-computer.json` |
| Tencent Cloud Agent Runti... | no free tier: CPU bills at CNY 0.000081 a c... | paid-only | documented | not stated | not stated | email | `dossier/compute/tencent-agent-runtime.json` |
| Tencent Cloud International | A 3-month free trial of one Lighthouse 2C2G... | fails-identity | documented | not applicable: the unit is a m... | The trial is time-box... | national-id | `dossier/compute/tencent-cloud-international.json` |
| Tencent Cloud Studio | 免费额度内每月提供5万分钟通用工作空间使用时长和1万分钟高性能空间使用时长，超出后按量... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/tencent-cloud-studio.json` |
| Tencent CNB | translated from the CNB pricing table: clou... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/tencent-cnb.json` |
| Tencent Cloud Internation... | no free tier; Linux Starter is USD 4.2 per... | qualifies | documented | not applicable: the unit is a m... | the instance and disk... | card | `dossier/compute/tencent-lighthouse-intl.json` |
| Tencent Cloud SCF | a free quota exists for 云函数 (SCF), listed i... | qualifies-with-caveat | documented | not stated | not stated | national-id | `dossier/compute/tencent-scf.json` |
| Tenki Sandbox | USD 100 in free credits on a new account: U... | qualifies-with-caveat | documented | Starter caps a machine at 4 cor... | A paused sandbox stop... | card | `dossier/compute/tenki.json` |
| TensorDock | no free tier: homepage 'From' rates per hou... | paid-only | documented | not stated | not stated | email | `dossier/compute/tensordock.json` |
| Tensorlake Sandboxes | $5 to $20 prepaid credit packs to start, up... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/tensorlake.json` |
| TensorPool | no price is published: the home page sells... | paid-only | documented | not stated | not stated | email | `dossier/compute/tensorpool.json` |
| Tenstorrent TT Console | Tenstorrent's own documentation offers hard... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/tenstorrent-tt-console.json` |
| Terabix | CVM-4GB-M at USD 6/month: 2 vCPU (AMD EPYC... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/terabix.json` |
| Test Flight | 'One weekend, and $300,000 in compute credi... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/test-flight.json` |
| Texel.ai | no price is published: the home page descri... | paid-only | documented | not stated | not stated | email | `dossier/compute/texel-ai.json` |
| The Catalyst | A ten-week in-person incubation in Riyadh f... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/the-catalyst.json` |
| The Eigenprize | 'No-strings-attached prize money for talent... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/the-eigenprize.json` |
| the.hosting | The selling brand publishes one price floor... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/the-hosting.json` |
| THE.Hosting review-for-da... | 'Mevcut VPS'yi en az 1 ay i in sipari edin... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/the-hosting-review-for-days-scheme.json` |
| The Vibe Hosting | A root Ubuntu container on an HTTPS subdoma... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/the-vibe-hosting.json` |
| TheAI Cloud | No free tier and no single-GPU rental: whol... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/theai-cloud.json` |
| Theta EdgeCloud | On-demand GPU rental, from USD 0.05 per hou... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/theta-edgecloud.json` |
| Thiel Fellowship | 'The Thiel Fellowship gives $250,000 to you... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/thiel-fellowship.json` |
| Thunder Compute | no free tier: on-demand, non-preemptible GP... | fails-identity | documented | not stated | not stated | institution | `dossier/compute/thunder-compute.json` |
| TierHive | Four preset plans inside one calculator, al... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/tierhive.json` |
| TierHive (Kernel Keepers... | No free tier, but a free startup credit tha... | qualifies-with-caveat | documented | not applicable: the unit is a m... | 3 d | email | `dossier/compute/tierhive-micro.json` |
| TierNet | VPS Bronze at USD 8.99/month: 1 core, 4 GB... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/tiernet.json` |
| Tietokettu | Mini VPS at EUR 2.50/month on the vendor st... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/tietokettu.json` |
| Tiger Cloud | No free plan. Performance plan, quoted: 'St... | trial-only | documented | not applicable: the unit is a m... | the 30-day clock ends... | email | `dossier/compute/tiger-cloud.json` |
| tilde.club | a shared Unix computer with a 1 GB soft and... | qualifies-with-caveat | documented | not applicable: the unit is a m... | no expiry is publishe... | email | `dossier/compute/tilde-club.json` |
| tilde.green | a free shared Ubuntu 24.04 account; the ToS... | qualifies-with-caveat | documented | not applicable: the unit is a m... | no idle policy; the o... | email | `dossier/compute/tilde-green.json` |
| tilde.guru | a free FreeBSD pubnix account, about 214 us... | qualifies-with-caveat | documented | not applicable: the unit is a m... | no idle policy docume... | email | `dossier/compute/tilde-guru.json` |
| ~horse (tilde.horse) | 'tilde.horse is a digital community built u... | qualifies-with-caveat | documented | not published: no disk quota or... | not published: no ina... | email | `dossier/compute/tilde-horse-free.json` |
| tilde.institute | A free OpenBSD shell account on a pubnix: S... | qualifies-with-caveat | documented | not applicable: the unit is a h... | not stated: no inacti... | email | `dossier/compute/tilde-institute.json` |
| Tilde.run (discontinued) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/tilde-run.json` |
| tilde.team | a shared Linux account on Ubuntu with tilde... | dead | documented | not applicable: the unit is a m... | the host was rebuilt... | email | `dossier/compute/tilde-team.json` |
| tilde.town | a free shared shell account while active; n... | qualifies-with-caveat | documented | not applicable: the unit is a m... | no expired-account po... | email | `dossier/compute/tilde-town.json` |
| Tilion | no free tier: $2,000 a month, with a machin... | paid-only | documented | not stated | not stated | email | `dossier/compute/tilion.json` |
| Time_Host | KVM-MINI-NVMe at 139 RUB/month: 1 core, 768... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/time-host.json` |
| Time4VPS | Eight storage plans, all one vCPU, priced i... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/time4vps.json` |
| Time4VPS | no free tier; Linux 1 is EUR 2.99 a month a... | qualifies | documented | not applicable: the unit is a m... | the server persists w... | email | `dossier/compute/time4vps-linux.json` |
| Time4VPS | no free tier; the entry plan is 'Linux 1' a... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/time4vps-linux-4.json` |
| Time4VPS | no free tier; Windows 16 is listed at EUR 6... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/time4vps-windows.json` |
| Timeweb Cloud grant | 'Грант на облако: до 1 000 000 ₽, до 6 меся... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | national-id | `dossier/compute/timeweb-cloud-grant.json` |
| Tinfoil | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/tinfoil.json` |
| TinyFish | Search and Fetch are free at any wallet bal... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/tinyfish.json` |
| TNAHosting | SSD KVM 1GB at USD 1.33/month billed USD 16... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/tnahosting.json` |
| Together Code Sandbox | no separate sandbox allowance: model infere... | paid-only | documented | not stated | not stated | email | `dossier/compute/together-code-sandbox.json` |
| Together AI | no free GPU allowance. The pricing page lis... | paid-only | documented | not stated | not stated | email | `dossier/compute/together-gpu.json` |
| TopCloud.vn | No free tier. Cực Rẻ 1 is VND 12,000 for th... | dead | documented | not applicable: the unit is a m... | monthly billing with... | card | `dossier/compute/topcloud-vn-cuc-re-1.json` |
| Torchbyte | Game VPS Start at EUR 4.65/month: 1 vCPU (A... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/torchbyte.json` |
| Tothost | Cloud VPS TOT K from VND 67,500/month on th... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/tothost.json` |
| Trigger.dev | $5 a month of free credits with 20 concurre... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/trigger-dev.json` |
| True Digital Park | USD 25,000 of Google Cloud credit for verif... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/true-digital-park.json` |
| Ubicloud | no free tier: billed by the minute on provi... | paid-only | documented | not stated | not stated | email | `dossier/compute/ubicloud.json` |
| UCloud Agent Sandbox | no published free tier: sandboxes pause and... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/ucloud.json` |
| Ultahost | VPS Basic at USD 5.52/month on a 24-month t... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/ultahost.json` |
| UniHost | LVP-G1 at EUR 6.90 per month excluding VAT,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/unihost.json` |
| unsandbox | Free $0 forever: 1 concurrent container, 1... | qualifies-with-caveat | documented | 10 files per execution, 10 MB t... | unknown: sessions and... | card | `dossier/compute/unsandbox.json` |
| Untether AI | Gone. The vendor's own notice states 'Untet... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/untether-ai.json` |
| UpCloud | no free tier: servers from EUR 3 a month or... | paid-only | documented | not stated | not stated | email | `dossier/compute/upcloud.json` |
| Upstage | no free tier and no signup credit. The pric... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/upstage.json` |
| Upstash Box | Free: USD 0, 10 concurrent boxes, 5 CPU hou... | qualifies-with-caveat | documented | not applicable: the unit is a m... | standard boxes auto-p... | email | `dossier/compute/upstash-box.json` |
| Upsun | A 15-day free trial with no credit card, th... | trial-only | documented | not applicable: the unit is a m... | 15 days is the free c... | email | `dossier/compute/upsun.json` |
| upyun.cc (云上互联) | No free tier. 新加坡NAT 套餐二 is CNY 10.00 a mon... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not stated on any pag... | email | `dossier/compute/upyun-sg-nat-2.json` |
| use.computer | no free tier: Apple Silicon Mac minis at $0... | paid-only | documented | not stated | not stated | email | `dossier/compute/use-computer.json` |
| Utho | no free tier; the smallest cloud plan liste... | paid-only | documented | not applicable: the unit is a m... | monthly or quarterly... | card | `dossier/compute/utho.json` |
| v0 | v0 Free: "$0/month", "Free access to v0", "... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/v0.json` |
| Val Town | A free plan whose crons run every 15 minute... | qualifies-with-caveat | documented | not applicable: the unit is a m... | The 10-second idle ti... | email | `dossier/compute/val-town.json` |
| Valohai | no free tier: 'Valohai offers straightforwa... | paid-only | documented | not applicable: the unit is a s... | not applicable: no fr... | card | `dossier/compute/valohai.json` |
| Vast.ai | no free tier; prices are set by supply and... | paid-only | documented | not applicable: the unit is a m... | a stopped instance ke... | card | `dossier/compute/vast-ai.json` |
| vds.guru | 'The trial gets the same resources as the p... | trial-only | documented | one trial per account; the vend... | 'If you don't renew,... | any-phone | `dossier/compute/vds-guru-trial.json` |
| VDS6.NET (BREEZLE LLC) | No free tier. V6-1 is USD 0.49 a month: 1 C... | qualifies-with-caveat | documented | not applicable: the unit is a m... | yearly prepay; the sh... | email | `dossier/compute/vds6-v6-1.json` |
| VDSina | No trial, and the provider says so on its o... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/vdsina.json` |
| VDSina | no free tier and no monthly cycle: the AMD... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/vdsina-cloud-configurator.json` |
| VDSina | no free tier; the Hi-CPU 8-core, 16 GiB, 32... | paid-only | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/vdsina-windows.json` |
| velixir | Free plan, quoted: '0.25 vCPU', '256 MB RAM... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the free app sleeps w... | email | `dossier/compute/velixir.json` |
| VeloxMedia | Micro at USD 5.00 per month: 1 vCPU, 2 GB R... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/veloxmedia.json` |
| Venice AI | no free API allowance. The documentation st... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/venice-ai.json` |
| Vercel | Hobby at USD 0: 4 CPU-hours of active CPU,... | qualifies-with-caveat | documented | functions cap at 2 GB of memory... | no persistent disk; a... | email | `dossier/compute/vercel.json` |
| Vercel Sandbox | 'Sandbox is free for Hobby users within the... | qualifies-with-caveat | documented | 'You can provision 1 or an even... | Snapshot storage is 1... | email | `dossier/compute/vercel-sandbox.json` |
| Verda (formerly DataCrunch) | no free tier: pay-as-you-go GPU capacity on... | paid-only | documented | not stated | not stated | email | `dossier/compute/verda.json` |
| Vers | A single metered rate of USD 0.04 per vCPU-... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vers.json` |
| VESSL Cloud | Korean GPU cloud with an on-demand rate tab... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vessl-cloud.json` |
| Vesuvius Challenge | 'Open prize pool $2,140,000'. Grand prize,... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vesuvius-challenge.json` |
| Vibrant Labs | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/vibrant-labs.json` |
| VirMach | no free tier; the page offers 1 GB / 1 core... | dead | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/virmach-black-friday-cyber-monday.json` |
| VirNAT | No free tier. US-256-KVM (DC1) is USD 0.80... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the server persists f... | email | `dossier/compute/virnat-us-256-kvm.json` |
| Virtarix | no free tier; WIN VPS M is USD 27.40 a mont... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/virtarix-windows.json` |
| Virtbase | EUR 3.99/month for EPYC-01 in Eygelshoven,... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/virtbase.json` |
| Virtono | KVM 512M at EUR 2.50 per month: 1 vCPU, 512... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/virtono.json` |
| Virtury | 25GB NVMe cloud server at USD 10.00 per mon... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/virtury.json` |
| VK Cloud | RUB 5,000 of welcome bonuses for an individ... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vk-cloud.json` |
| VM6_Networks | UK Xeon S (order product Budget VPS UK 1) a... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vm6-networks.json` |
| VNG Cloud | 'B n d ng th mi n ph d nh cho kh ch h ng m... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/vng-cloud.json` |
| Volcengine (火山引擎) | '免费试用额度仅对完成中国大陆实名认证的账号开放，未完成认证的账号无法触发额度发放逻辑... | fails-identity | documented | one free trial quota per accoun... | Not stated on the art... | national-id | `dossier/compute/volcengine-free-trial.json` |
| VolpaByte | no free tier; the ladder starts at EUR 3.49... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/volpabyte-ryzen-kvm-8gb.json` |
| Voltage Park | no free tier: HGX H100 capacity from 1 to 8... | paid-only | documented | not stated | not stated | email | `dossier/compute/voltage-park.json` |
| VoltageGPU | No free tier. Prepaid per-second GPU rental... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/voltagegpu.json` |
| Voyage AI | The first 200 million tokens for voyage-4-l... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/voyage-ai.json` |
| VPS_Panda | KVM-1G at USD 4.50 per month (store: 'Start... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vps-panda.json` |
| vps1 | VPS 1 at $7.10 per month on the homepage, u... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | any-phone | `dossier/compute/vps1.json` |
| VPSDime | Linux VPS (order product Linux4GB) at USD 5... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vpsdime.json` |
| vpsFree.cz | Not free. Quoted: "one VPS requires a membe... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vpsfree-cz.json` |
| VPSFree.es | Not free. The vendor sells VPS from EUR 2.4... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/vpsfree-es.json` |
| VPS Indonesia | no free tier; Mini at Rp40.000 is the small... | qualifies | documented | not applicable: the unit is a m... | the disk persists whi... | email | `dossier/compute/vpsindonesia-mini.json` |
| VPSPioneer | Two product lines. Cloud VPS S is USD 8.49/... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/vpspioneer.json` |
| Vultr Cloud Compute | Promotional credit by code, not on signup:... | trial-only | documented | not stated | not stated | card | `dossier/compute/vultr.json` |
| Vultr | Cloud Compute entry rung: 1 vCPU, 0.5 GB me... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/vultr-2.json` |
| Vultr | no free tier; the cheapest regular plan is... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the instance persists... | card | `dossier/compute/vultr-regular-1gb.json` |
| Vultr Cloud Compute (Wind... | none for compute; the live pricing page car... | paid-only | documented | not stated | not stated | email | `dossier/compute/vultr-windows.json` |
| Waifly | 'Waifly's free plan gives 300 MB of RAM, 1... | qualifies-with-caveat | documented | '1 server, 1 MySQL database' on... | 'A server's status is... | email | `dossier/compute/waifly-free.json` |
| wap.ac | No free tier. TW 512 LXC is USD 1.00 a mont... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the container persist... | email | `dossier/compute/wapac-tw-512-lxc.json` |
| wap.ac (WAPAC) | No free tier. TW 512 LXC is USD 1.00 a mont... | fails-quota | documented | not applicable: the unit is a m... | monthly billing; the... | card | `dossier/compute/wapac-tw-512-lxc-ipv6.json` |
| Warp | Warp Free: "$0/month" with "Warp Agent CLI... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/warp.json` |
| WarpBuild (GitHub Actions... | No free allowance is published: the FAQ say... | paid-only | documented | not stated | not stated | email | `dossier/compute/warpbuild.json` |
| Wasmer | Free forever: 150 GB of bandwidth, a global... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/wasmer.json` |
| webapp.io | a free trial of hosted test environments th... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/webapp-io.json` |
| WebARENA Indigo | no free tier and no setup fee; billing is h... | qualifies | documented | not applicable: the unit is a m... | the instance bills fr... | card | `dossier/compute/webarena-indigo.json` |
| StackBlitz WebContainers | a free Personal plan with unlimited public... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/webcontainers.json` |
| WebHOST1 | Two free routes rather than a free tier. Th... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/webhost1.json` |
| Wholesale Internet | Preconfigured dedicated servers with free s... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/wholesale-internet.json` |
| Whplus (my.whplus.com) | No free tier. IIX NAT VPS 512MB is IDR 12,5... | qualifies-with-caveat | documented | not applicable: the unit is a m... | monthly billing; no d... | email | `dossier/compute/whplus-iix-nat-512mb.json` |
| Windmill Cloud | Community plan on Windmill Cloud: 1,000 exe... | qualifies-with-caveat | documented | unverified: the getting-started... | unverified: the getti... | email | `dossier/compute/windmill-cloud.json` |
| Windows 365 Cloud PC (Bus... | no free tier: Windows 365 Business is a mon... | trial-only | documented | not stated | not stated | card | `dossier/compute/windows-365.json` |
| Windows 365 for Agents | no free tier: $0.40 an hour per Cloud PC on... | paid-only | documented | not stated | not stated | email | `dossier/compute/windows-365-agents.json` |
| windowsvps.host | no free tier; DeluxeBox is USD 36.00 a mont... | qualifies-with-caveat | documented | not applicable: the unit is a m... | the disk persists whi... | card | `dossier/compute/windowsvps-host-windows.json` |
| Runtime (withruntime.com) | 100 free hours of a 1 GB machine in the fir... | qualifies-with-caveat | documented | free tier caps a sandbox at 2 v... | A paused sandbox keep... | email | `dossier/compute/withruntime.json` |
| WLX | No free tier. Lowest listed server is USD 1... | paid-only | documented | not applicable: the unit is a m... | billed in advance; ca... | card | `dossier/compute/wlx.json` |
| Woiden.id | A free NAT VPS with a shared IPv4 and a ded... | qualifies-with-caveat | documented | not applicable: the unit is a v... | 'You can renew your V... | any-phone | `dossier/compute/woiden-id.json` |
| WorldBus | Turkey VPS SSD (A) (portal product TR - SSD... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/worldbus.json` |
| Worldstream | The cheapest of the 43 entries in the vendo... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/worldstream.json` |
| WSO2 Choreo | The free plan is gone from the pricing page... | trial-only | documented | not applicable: the unit is a m... | there is no perpetual... | email | `dossier/compute/wso2-choreo.json` |
| 无忧云 (Wuyou Cloud) | No free tier. 德国NAT-LXC is CNY 1.99 a month... | qualifies-with-caveat | documented | not applicable: the unit is a m... | monthly billing; no d... | card | `dossier/compute/wuyoucloud-de-nat-lxc.json` |
| Apple Xcode Cloud | 25 compute hours a month included with Appl... | qualifies-with-caveat | documented | not stated | not stated | card | `dossier/compute/xcode-cloud.json` |
| XDN IDC | Shared virtual servers from a Guro Digital... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/xdn-idc.json` |
| xHosts | Budget 1G at GBP 3.50 a month in the cart (... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/xhosts.json` |
| XServer VPS | no free tier; the entry plan is JPY 1,265 a... | paid-only | documented | not applicable: the unit is a m... | monthly; the server p... | card | `dossier/compute/xserver-vps.json` |
| Xuhui District AI | 'Eligible applicants: this policy applies t... | fails-identity | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/xuhui-district-ai.json` |
| Yandex Cloud | Withdrawn: the live documentation states 'C... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/yandex-cloud.json` |
| YepCode Run | 50,000 Yeps, which are seconds of execution... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/yepcode.json` |
| Yotta Labs Academic | '$1000 Credits' plus 'Discounted Compute Us... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/yotta-labs-academic.json` |
| Z.ai GLM Flash | Three models are priced Free on every colum... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/z-ai-glm-flash.json` |
| Zappie | Starter 512 MB VPS [NZ]: USD 6.50 per month... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zappie.json` |
| Zeabur | Free Plan at USD 0: 'No credit card require... | qualifies-with-caveat | documented | a single file upload is capped... | 48 hours of logs on F... | email | `dossier/compute/zeabur.json` |
| Zenrows Browser Sessions | Free at $0/mo with 5,000 credits a month an... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/zenrows.json` |
| Zerops | The Lightweight Core project package is fre... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zerops.json` |
| Zettabyte (zCLOUD) | No free tier. On-demand H100 GPUs from USD... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zettabyte.json` |
| Zhipu Z Managed Agents | no free tier published: a managed-agent pla... | paid-only | documented | not stated | not stated | email | `dossier/compute/zhipu.json` |
| Zibra Labs | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/zibra-labs.json` |
| Zindi | Quoted from the open challenge read today:... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zindi.json` |
| zipbox | 'Every new account can get $25 in credit wi... | qualifies-with-caveat | documented | Four sizes: 'Tiny 1 vCPU · 2 GB... | 'Paused boxes cost $0... | card | `dossier/compute/zipbox.json` |
| Zo Computer | a 14-day free trial with limited usage and... | trial-only | documented | not stated | not stated | email | `dossier/compute/zo-computer.json` |
| Zoho Catalyst | A monthly allowance that renews forever: '2... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zoho-catalyst.json` |
| Zoltan's FLOPs GPU | 'Zoltan's FLOPs is a mini-grant program for... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zoltan-s-flops-gpu.json` |
| Zylora open source | USD 500 of GPU credits for startups pre-Ser... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/zylora-open-source.json` |
| Zylora startup GPU | Explorer: 'USD 25 one-time credits', instan... | trial-only | documented | not applicable: the unit is a m... | not applicable: the u... | card | `dossier/compute/zylora-startup-gpu.json` |
| Amp (self-hosted) | Amp Hobby: "Free" with "Pay-as-you-go for A... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/amp-2.json` |
| Veertu Anka Build Cloud (self-hosted) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/anka-build-cloud.json` |
| Browser Linux emulators (self-hosted) | a Linux userland running in the browser tab... | dead | documented | not applicable: the unit is a m... | dies with the tab | anonymous | `dossier/compute/browser-linux-emulators.json` |
| Butter (self-hosted) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/butter.json` |
| Bytebot (self-hosted) | the software is free and open source under... | qualifies-with-caveat | documented | not stated | not stated | anonymous | `dossier/compute/bytebot.json` |
| Cedana (self-hosted) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/cedana.json` |
| Coder (self-hosted) | free Community plan, installed from open so... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/coder.json` |
| Continue (self-hosted) | the vendor product is gone: "Continue has b... | dead | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/continue.json` |
| Cua (self-hosted) | no hosted sandbox rate is published: the pr... | dead | documented | not applicable: the unit is a m... | not applicable: no ho... | email | `dossier/compute/cua.json` |
| Cua (Cua Spaces) (self-hosted) | no rented Windows machine; the free tier is... | dead | documented | not applicable: no machine is p... | not applicable: no ma... | email | `dossier/compute/cua-windows.json` |
| Cyberdesk (self-hosted) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/cyberdesk.json` |
| Dagger (self-hosted) | the engine is open source and runs locally;... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/dagger.json` |
| Drone CI (self-hosted) | free software, no hosted lane: the Open Sou... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/drone-ci.json` |
| Expanse (self-hosted) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/expanse.json` |
| Expanso (self-hosted) | Bacalhau-derived pipelines that 'run on you... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | institution | `dossier/compute/expanso.json` |
| Gensyn (self-hosted) | No consumer-facing capacity. Quoted: 'RL Sw... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | email | `dossier/compute/gensyn.json` |
| Goose (self-hosted) | not stated: https://goose-docs.ai/ prints n... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/goose.json` |
| HumanLayer (self-hosted) | Free for small teams with up to 200 session... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/humanlayer.json` |
| joule (self-hosted) | Free access is real but is earned by contri... | fails-quota | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/joule.json` |
| Kasm Workspaces (self-hosted) | Community Edition is free for individuals a... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/kasm-workspaces.json` |
| Lapdev (self-hosted) | free during public beta, with unlimited dev... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/lapdev.json` |
| Magnitude (self-hosted) | the open-source engine is a free download t... | qualifies-with-caveat | documented | not stated | not stated | anonymous | `dossier/compute/magnitude.json` |
| Okteto (self-hosted) | Starter, self-hosted on a Kubernetes cluste... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/okteto.json` |
| Onlook (self-hosted) | Onlook "Free" is a download, not a hosted a... | paid-only | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/onlook.json` |
| RunsOn (self-hosted) | A free licence is provided for non-commerci... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/runs-on.json` |
| ScitiX Agent Sandbox (self-hosted) | free tier published without a credit amount | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/scitix-agent-sandbox.json` |
| Self-hosted bare-metal sa... (self-hosted) | no free server: the AX42 is rented, with fr... | paid-only | documented | not stated | not stated | email | `dossier/compute/self-host-baremetal.json` |
| Signadot (self-hosted) | ephemeral environments that share self-host... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/signadot.json` |
| Tart + Orchard (Cirrus Labs) (self-hosted) | a Free Tier licence that applies with no pu... | qualifies-with-caveat | documented | not stated | not stated | email | `dossier/compute/tart-orchard.json` |
| Tencent Cloud CubeSandbox (self-hosted) | no hosted tier: the project is self-hosted... | paid-only | documented | not stated | not stated | email | `dossier/compute/tencent-cubesandbox.json` |
| Trainy (self-hosted) | no free tier published | paid-only | documented | not stated | not stated | email | `dossier/compute/trainy.json` |
| Windmill (self-hosted) | Free and open source at USD 0 a month with... | qualifies-with-caveat | documented | not stated | not stated | anonymous | `dossier/compute/windmill.json` |
| Zed (self-hosted) | Zed Personal: "$0 forever", "Unlimited use... | qualifies-with-caveat | documented | not applicable: the unit is a m... | not applicable: the u... | anonymous | `dossier/compute/zed.json` |
<!-- generated:end -->

## How to re-run this

The probe output is kept in
`sources/2026-10-22/compute/tcp-probe-20261022T035515.270Z.json` and is listed in
`sources/MANIFEST.tsv`, so it survives a clean tree. Re-run it with
`scripts/probe/tcpprobe.py`. Every count in this topic is rendered by
`scripts/report/render.py`, and every paid figure is derived by
`scripts/report/compute-price.py`; a number that disagrees with either is a defect
in the document, not in the script.

A reader who distrusts a number here should re-run the page read and compare the
quoted sentence. Where a record says `reported`, the honest answer is that the page
was never opened, and that is the gap to close first.
