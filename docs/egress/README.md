# egress

Traffic leaving a machine, or reaching it, without a bill. Tunnels, relays, CDN
fronting, WireGuard ingress, mesh signalling, origin quotas and the paid
per-gigabyte ladder.

Two questions, and they are different:

1. **Can 500 GB to 1 TiB of daily traffic leave a machine, or reach it, for nothing?**
   The answer is that no free path reaches the public web at that volume.
2. **Can one public UDP port reach a WireGuard endpoint, free?**
   ⭐ The answer is **yes, at ten or more providers**.

## The ingress answer

A WireGuard endpoint needs exactly one UDP port. It does not need a hostname, a
path or a certificate. So the question is not "who speaks WireGuard" but "which
free UDP forward carries a terabyte a month", and that reframing opens a market
the obvious question hides.

| provider | what it gives | free volume | UDP | verdict |
| --- | --- | --- | --- | --- |
| ROUTE64 | a routed IPv6 `/56` over WireGuard | no meter | yes | `qualifies` |
| TaipanTransit | a WireGuard tunnel with 1 TB included | EUR 2/month, not free | yes | `paid-only` |
| portwarp | one UDP port, one tunnel | "unlimited bandwidth", stated | yes | `qualifies-with-caveat` |
| playit.gg | anycast custom UDP | no cap, 1 to 2 TB/day tolerated | yes | `qualifies-with-caveat` |
| ProxyLink | a WG peer plus public TCP and UDP | "no usage limits" in early access; the published grid gives Free zero tunnels | yes | `trial-only` |
| portmap.io | one rule on a random port | "unlimited bandwidth", stated | yes | `qualifies-with-caveat` |
| TCPShield Sentry | any TCP or UDP over VXLAN | 1.0 TB/month (0.909 TiB) | yes | `qualifies-with-caveat` |
| NetBird reverse proxy | L4 proxy, TCP and UDP | none published | yes | `qualifies-with-caveat` |
| Oracle Always Free | a VM with a public IP | 10 TB/month (9.09 TiB) | yes | `qualifies-with-caveat` |
| freefrp.com | a public frps, ports 10000 to 60000 | no quota, 30 Mbit/s ceiling | yes | `qualifies-with-caveat` |
| openport.pw | one persistent port, no signup | none published | yes | `qualifies-with-caveat` |

⭐ **1 TiB/month is 33.3 GiB/day, which is 3.24 Mbit/s sustained.** The volume bar
is low and the rate bar is not, so a provider that caps a free tunnel at 10 Mbit/s
still clears 3.2 TB/month.

Full detail: [`free/wireguard-ingress.md`](free/wireguard-ingress.md).

## The egress answer

GiB per day to the public web, for a reader who is not on the same overlay.

⭐ **GitHub Releases serves ranged GETs at 14.11 MiB/s with no bandwidth limit**,
measured here, which is 1.16 TiB per day. That is the only hosted free path
**measured** above the floor. Cloudflare Tunnel is unmetered and Oracle carries
10 TB per month, and neither was measured, so neither is a stronger claim at this
rung.

Everything hosted and centrally operated that transits bytes is metered, and the
metered allowances are two to three orders of magnitude short: Cloudflare TURN's
1,000 GB per month is 33.3 GB per day, which is 3.03% of one day's work.

## The distinction that decides every verdict

Every provider in this topic either **signals** or **relays**. A third case
matters: a provider can relay **inside a private overlay** and carry nothing to the
public internet.

| the provider's role | what it costs the provider | is the free tier real | who is in it |
| --- | --- | --- | --- |
| signalling: introduces two peers, then leaves the path | about nothing after hole-punch | yes, because no bytes transit | Tailscale, ZeroTier, NetBird, libp2p hole-punched, iroh direct, Headscale (self-hosted) |
| relaying: bytes transit the provider to the public internet | bandwidth multiplied by time, or a metered volume | only if it meters rate | playit.gg, iroh public, DERP |
| relaying inside an overlay only: bytes transit, but never to a public reader | the peer's link rate | yes, and irrelevant to this workload | Yggdrasil public peers |
| relaying with a byte quota | a metered volume | no, arithmetically | Cloudflare TURN, ngrok, zrok, iroh Shared, Fastly, Vercel |

⭐ **One relay in this topic was measured rather than read.** The relay at
`dossier/egress/ajam-ssh-relay.json` carries a whole SSH session in both directions,
caps one session at 64 MiB, closes an idle session at 180 seconds and gives the target a
Cloudflare egress address. That cap makes it an orchestration path and not a serving
path, and the measurement is in
[`free/sealed-sandbox-reach-in.md`](free/sealed-sandbox-reach-in.md).

A relay that only coordinates costs the provider nothing after hole-punch, so its
free tier is genuinely unlimited and its quota is irrelevant. A relay that transits
bytes is metered by definition, and the only question is whether it meters rate or
volume. That question decides the answer, so every record names which it is, in
`extras.bytes_transit`.

## Convert every claim to a rate before comparing it

A monthly allowance, a port speed and a per-second shaping number are not
comparable until each is per day.

| the provider states | sustained | share of 1 TiB/day |
| --- | --- | --- |
| 1,000 GB per month | 33.3 GB/day | 3.03% |
| 100 GB per month | 3.3 GB/day | 0.30% |
| 5 GB per day | 5 GB/day | 0.45% |
| 1 GB per month | 33.3 MB/day, or 31.8 MiB/day | 0.003% |
| 50 Mbit/s | 0.54 TB/day, or 0.49 TiB/day | 49% |
| 200 Mbit/s | 2.16 TB/day, or 1.96 TiB/day | 196% |
| 6.72 MiB/s | 0.61 TB/day, or 0.55 TiB/day | 55% |
| 14.11 MiB/s | 1.28 TB/day, or 1.16 TiB/day | 116% |

1 TiB per day is 12.14 MiB/s, or 101.8 Mbit/s. The arithmetic
`200 Mbit/s x 86,400 s / 8` gives 2.16 TB and 1.96 TiB; the two units differ by 10%,
and the binary figure belongs only to a binary computation.

⚠ **The share column is computed against 1 TiB and the month is 30 days.** At the
mean month of 30.4375 days, 1,000 GB per month is 2.99% rather than 3.03%.

## The documents

| document | the class | what it answers |
| --- | --- | --- |
| [`free/wireguard-ingress.md`](free/wireguard-ingress.md) | WireGuard ingress | which provider gives a public UDP port to a WireGuard endpoint, free or nearly |
| [`free/udp-forward.md`](free/udp-forward.md) | hosted UDP forwards | the commercial one-port class, and every row that fails on bytes |
| [`free/cn-frp.md`](free/cn-frp.md) | public frp relays | the largest free UDP surface, and the identity wall in front of half of it |
| [`free/l4-edge.md`](free/l4-edge.md) | L4 edge proxies | the free Spectrum class, and the one free row in it |
| [`free/ipv6-ingress.md`](free/ipv6-ingress.md) | routed IPv6 | a free public prefix with every port open, over WireGuard where it exists |
| [`free/mesh-and-ztna.md`](free/mesh-and-ztna.md) | overlays | why a WireGuard mesh publishes nothing, and the four products that do |
| [`free/paas-l4.md`](free/paas-l4.md) | platform raw ports | which free platform tier exposes a TCP or UDP port |
| [`free/regional-and-small.md`](free/regional-and-small.md) | the long tail | the small and regional providers, each with the sentence that decides it |
| [`free/wireguard-transports.md`](free/wireguard-transports.md) | wrappers | how a datagram crosses TCP or WebSocket, and why that needs a host |
| [`free/expose-a-local-port.md`](free/expose-a-local-port.md) | hosted tunnels | how do I put a local service on a public URL, and what kills the URL |
| [`free/sealed-sandbox-reach-in.md`](free/sealed-sandbox-reach-in.md) | a measured relay | how does a host that cannot bind a port get reached, and what does the path cost |
| [`free/bulk-egress.md`](free/bulk-egress.md) | the lanes that carry a day | which free path actually moves 500 GB to 1 TiB in a day |
| [`free/signalling.md`](free/signalling.md) | mesh and relay signalling | what is genuinely unmetered, and why |
| [`free/inbound-and-address.md`](free/inbound-and-address.md) | stable ingress | how do I get a stable address with no static IP |
| [`free/tunnel-sweep.md`](free/tunnel-sweep.md) | the tunnel catalogues | what 105 listed tunnel products reduce to when the question is UDP |
| [`paid/wireguard-ingress.md`](paid/wireguard-ingress.md) | the paid ladder | what a terabyte costs when free is not enough |
| [`paid/per-gigabyte.md`](paid/per-gigabyte.md) | metered egress | what does a day cost when free is not enough |
| [`paid/credits.md`](paid/credits.md) | credits and trials | which cloud credit buys a terabyte a month, and which does not |
| [`watchlist.md`](watchlist.md) | the sources | every list this topic is measured against, and what each is not |

## The dead ends, in one place

The full list is in each document and in `dossier/` as `verdict: dead` or
`fails-*` records. The classes that are closed:

| class | why it fails | verdict |
| --- | --- | --- |
| HTTP-only tunnels as a WireGuard path | no UDP anywhere in the product | `fails-egress` |
| game proxies for a named protocol only | the free tier carries Java TCP and not arbitrary UDP | `fails-egress` |
| Chinese panels with a real-name check | the identity is unreachable | `fails-identity` |
| free tiers measured in megabytes | 10 MB to 2 GB is 0.001% to 0.2% of a terabyte month | `fails-quota` |
| Cloudflare Spectrum | Enterprise only, at every protocol | `paid-only` |
| WARP as an ingress | a device VPN gives a device an exit, not a server an address | `fails-egress` |
| 21tunnel | advertised a UDP port, a `.conf` and unlimited free bandwidth; its control plane does not resolve | `dead` |
| Yggdrasil public peers | no exit nodes, so no peer reaches the public internet | `fails-egress` |

## The records

One record per provider, in [`../../dossier/egress/`](../../dossier/egress/). The
tables above are a view of those records; where they disagree, the record is right.
Each carries `limits[]`, one `binding` kind, `identity_cost`, `confidence`,
`verified_at`, the probe evidence for every `measured` row, and four transport
fields in `extras`: `bytes_transit`, `ingress`, `wg_path` and `volume_tib_month`.

⚠ **A monthly or daily byte allowance has its own constraint kind.** The vocabulary
names it `volume-quota`, and a record that names `per-ip-shaping` for a byte allowance
has a `binding_note` that says why.

## What this topic does not know

- **No free UDP forward was measured end to end.** Every provider allocates a port
  only after an account exists, so the measurement needs an account.
- **No WireGuard handshake crossed a provider tunnel here.** The `wg_path` field
  says how a row could carry one, and it is a reading, not a probe.
- **Cloudflare Tunnel's unmetered claim was not measured.** A Quick Tunnel was,
  because it needs no account.
- **playit.gg's 1-2 TB/day is one sentence from the provider.** It is the
  strongest free relay found and the weakest evidence in the topic.
- **Every measurement here ran from one host on one network.** The absolute rates are
  that host's; the ratios between the lanes are the durable part. The first batch ran
  on 2026-10-22, and a capability-free sandbox added a second batch of authless relays
  on 2026-11-05; the two batches disagree on absolute throughput, which is the point.

## Records that no other document names

This list is generated by `scripts/report/render.py` from the records. It holds each
`measured` or `documented` record of this topic that no other document of `docs/` names,
so a reader finds it and the gate's `links` check counts it as cited. A document that
names the record removes its row at the next render.

<!-- generated:start topic=egress kind=uncited -->
| record | provider | verdict | confidence |
| --- | --- | --- | --- |
| `affordablebytes-xeon-gold-6gb` | AffordableBytes | paid-only | documented |
| `bytehosting-xeon-6gb` | ByteHosting | paid-only | documented |
| `c-servers-nanovps-ii-384` | C-Servers | paid-only | documented |
| `chunkserve-xeon-standard-2` | ChunkServ | paid-only | documented |
| `cloudserver-linux-kvm-1gb` | CloudServer | paid-only | documented |
| `dedirock-promo-vps-saver-monthly` | DediRock | paid-only | documented |
| `dedirock-yearly-promo-vps-saver` | DediRock | paid-only | documented |
| `enderhost-budget-vps-4gb` | EnderHost | paid-only | documented |
| `expose-dev-hobby` | Expose (expose.dev managed service) | qualifies-with-caveat | documented |
| `expose-dev-pro` | Expose (expose.dev managed service) | paid-only | documented |
| `fastturn-net` | fastTURN | paid-only | documented |
| `finlandhosting-budget-small` | FinlandHosting | paid-only | documented |
| `firstbyte-eu-kvm-ssd-start-fin1` | FirstByte | paid-only | documented |
| `flipperhost-kvm-basic` | FlipperHost | paid-only | documented |
| `freevps-org-charity-donor` | FreeVPS.org | qualifies-with-caveat | documented |
| `freevps-org-regular` | FreeVPS.org | qualifies-with-caveat | documented |
| `gcore-cloud-vm` | Gcore | paid-only | documented |
| `godlike-host-nitro-1` | Godlike.Host | paid-only | documented |
| `greencloud-storage-0-5tb` | GreenCloudVPS | paid-only | documented |
| `gullos-hosting-nat-ipv4-128mb` | Gullo's Hosting | paid-only | documented |
| `gullos-hosting-nat-ipv4-256mb` | Gullo's Hosting | paid-only | documented |
| `hostbilby-bilbyboost-vds` | HostBilby | paid-only | documented |
| `hostdare-ssd1` | HostDare | paid-only | documented |
| `hosteons-hybrid-server-special-1` | HostEONS | paid-only | documented |
| `hosthatch-nvme-vps` | HostHatch | paid-only | documented |
| `hostkey-vps` | HOSTKEY | paid-only | documented |
| `hostnamaste-kvm-1gb` | HostNamaste | paid-only | documented |
| `infomaniak-vps-lite` | Infomaniak | paid-only | documented |
| `kamatera-basic-vps` | Kamatera | paid-only | documented |
| `khanwebhost-fr-256-mb-nat-kvm` | KhanWebHost | paid-only | documented |
| `khanwebhost-nl-256mb-nat` | KhanWebHost | paid-only | documented |
| `littlecreek-starter-vps` | LittleCreek | paid-only | documented |
| `massivegrid-cloud-vps-starter` | MassiveGRID | paid-only | documented |
| `ouiheberg-linux-vps-01g` | OuiHeberg | paid-only | documented |
| `racknerd-kvm-1gb` | RackNerd | paid-only | documented |
| `rarecloud-custom-kvm-vps` | RareCloud | paid-only | documented |
| `serverhost-kvm-2gb` | ServerHost | paid-only | documented |
| `servitro-1-server` | Servitro | paid-only | documented |
| `siliconkiwi-kiwi-go` | SiliconKiwi | paid-only | documented |
| `softshellweb-lxc-ipv6-only-la` | SoftShellWeb | paid-only | documented |
| `strato-linux-vserver-vps-s` | STRATO | paid-only | documented |
| `tierhive-micro-nat` | TierHive | paid-only | documented |
| `tunelo-net` | tunelo.net | fails-egress | documented |
| `upcloud-starter-vps` | UpCloud | paid-only | documented |
| `velohost-kvm-xs` | Velohost | paid-only | documented |
| `virmach-ryzen-512mb` | VirMach | paid-only | documented |
| `virtbase-epyc-01` | Virtbase | paid-only | documented |
| `vpspioneer-cloud-vps-s` | VPSPioneer | paid-only | documented |
| `webdock-vps-essential` | Webdock | paid-only | documented |
| `ngrok-operator-zufardhiyaulhaq` | ngrok-operator (zufardhiyaulhaq) (self-hosted) | fails-quota | documented |
| `pomerium-zero` | Pomerium (self-hosted) | fails-egress | documented |
<!-- generated:end -->
