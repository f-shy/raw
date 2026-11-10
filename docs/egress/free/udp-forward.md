# Free hosted UDP port forwards

A hosted UDP forward is the smallest unit of this market: one public address, one UDP
port, mapped to one port behind a NAT. No hostname, no certificate, no HTTP.

⭐ **One UDP port is all a WireGuard endpoint needs.** A provider in this class is
therefore a WireGuard ingress provider whether or not it has ever heard of
WireGuard, and the question is only whether the free tier carries a terabyte a
month.

The bar is 1 TiB/month, which is 33.3 GiB/day, or 3.24 Mbit/s sustained. Most
free tiers in this class fail on bytes by two orders of magnitude, and the ones
that do not publish a number are the ones worth reading.

| provider | free tier | UDP port | free volume | identity | verdict |
| --- | --- | --- | --- | --- | --- |
| portwarp | 1 tunnel, 2 extra ports | yes, dashboard-assigned | "unlimited bandwidth", stated | email | `qualifies-with-caveat` |
| playit.gg | anycast, custom UDP | yes, free port type | no cap; 1 to 2 TB/day tolerated | email | `qualifies-with-caveat` |
| portmap.io | 1 rule on a random port | yes, over OpenVPN | "unlimited bandwidth", stated | email | `qualifies-with-caveat` |
| openport.pw | 1 persistent port | yes, default on | none published | anonymous | `qualifies-with-caveat` |
| Pinggy | a session, not a tunnel | yes, with a free token | unlimited bytes, 60 minutes | anonymous | `qualifies-with-caveat` |
| Port Buddy | 1 UDP tunnel | yes | none published | email | `qualifies-with-caveat` |
| rustunnel | Hobby, 1 GB/month | yes on the managed cloud | 1 GB | email | `fails-quota` |
| wstunnel demo | an allowlisted demo relay | only demo hosts | none | anonymous | `trial-only` |

## portwarp

One active tunnel, two extra ports per tunnel, TCP and UDP, and the sentence that
puts it at the top of this page: "Every plan includes TCP, UDP, encrypted
tunnels, and unlimited bandwidth" (`documented`, read 2026-10-23). The public
address is shown in the dashboard and the port is a stored property of the
tunnel, so it survives a reconnect.

⚠ **"Unlimited" here is a claim about a missing meter, and the record says so.**
Nothing countable is published, so the first failure is an unpublished tolerance
on a single relay. That is weaker than a quota and stronger than a service that
publishes 1 GB.

Evidence: `portwarp.com/pricing` (read 2026-10-23); `dossier/egress/portwarp.json`.

## playit.gg

A global anycast relay whose free tier carries game presets and "custom TCP/UDP
for anything else", with the provider describing 1 to 2 TB/day on a free account
as tolerated in a forum post (`reported`, read 2026-10-23). Generic TCP moved to
the paid tier; custom UDP did not.

⚠ **A tolerance is not a quota, and the same post says it moves with regional
bandwidth cost.** This is the strongest free relay found and the weakest evidence
in this topic: one operator, one sentence, one day.

Evidence: `discuss.playit.gg/t/traffic-limits/5574` (read 2026-10-23);
`dossier/egress/playit-gg.json`.

## portmap.io

One configuration, one forwarding rule, a random external port, and "Unlimited
bandwidth" as a product line (`documented`, read 2026-10-23). The transport is
OpenVPN, so the forwarded UDP port carries an OpenVPN session and a WireGuard
endpoint runs inside it.

The free rule is a random port and a custom external port is paid, so the address
moves whenever the tunnel is recreated. That is a `per-ip-shaping` row in the
record because the port, not the byte count, is what fails first.

Evidence: `portmap.io` (read 2026-10-23); `dossier/egress/portmap-io.json`.

## openport.pw

One persistent port with no signup, and UDP is on by default (`documented`, read
2026-10-23). It is the only row here that needs no identity at all, which matters
more than its unpublished volume.

⚠ **A single-operator service with no account is also a service with no recourse
when it stops.** The record keeps the fact and does not promise continuity.

Evidence: `openport.pw` (read 2026-10-23); `dossier/egress/openport-pw.json`.

## Pinggy

UDP works on the free tier through a documented one-liner, and the free host form
returns a public port such as `udp://rndnj-103-170-183-11.a.free.pinggy.online:43210`
(`documented`, read 2026-10-23). The free session lasts 60 minutes.

⛔ **A 60-minute tunnel is not a WireGuard endpoint.** The record still qualifies
because the path exists and is free, and the verdict carries the caveat that a
reader must reconnect hourly. The only rate measured on the free tier
is 26.9 KiB/s on the HTTP tier, which is 66 GiB/month and fails the bar if the
UDP tier behaves the same. That was not measured.

Evidence: `pinggy.io/docs/udp_tunnels/` (read 2026-10-23);
`dossier/egress/pinggy-free.json`.

## Port Buddy

HTTP and UDP tunnels are free with no card, and a `udp` subcommand is advertised
(`unverified`, read 2026-10-23). No monthly byte allowance is published for the
UDP tunnel, and the pricing page returned `application/problem+json` on the read
attempt.

⚠ The record is `unverified` and that is the finding: a free UDP tunnel with no
published volume is a lead, not a capacity.

Evidence: `portbuddy.dev` (read 2026-10-23); `dossier/egress/port-buddy.json`.

## What is dead in this class

Every row was read. Each has a record.

| provider | free ceiling | why it fails |
| --- | --- | --- |
| LocalToNet | 1 GB/month | 3% of the bar, and UDP is on some plans only |
| rustunnel | 1 GB/month | 0.1% of the bar, though TCP and UDP are both on the free plan |
| TunnelThat | 512 MB/month | 0.05% of the bar |
| OutRay | 2 GB/month | 0.2% of the bar |
| CloudPub | 250 GB/month | 25% of the bar, and TCP and UDP are PRO |
| Packetriot | HTTP only on free | port allocations are no longer available on the free tier |
| openport.io | 10 MB/month | 0.001% of the bar |
| PageKite | 2.5 GB trial, 31 days | a trial, not a tier |
| srv.us | no account, TCP only | an arbitrary TCP port wrapped in TLS, and no UDP |
| ngrok | 1 GB/month | no UDP at any tier, and a card for a raw TCP address |
| LocalXpose | 2 HTTP tunnels | TCP and UDP are PRO |
| Loophole, Tunnelmole, Tunnelto | HTTP only | no UDP path |
| tsocket | TCP only | no UDP path |
| bore.pub | no quota | TCP only, so a WireGuard datagram cannot cross it |
| localhost.run | no account | HTTP and TLS only, measured at 11.4 KiB/s |
| remote.it | 5 devices | UDP reaches enrolled peers only, so no public reader |
| zrok hosted | 5 GB/day | public shares are HTTP; TCP and UDP are private shares |
| 21tunnel | unlimited on paper | the control plane does not resolve: `agent.21tunnel.com` and `login.21tunnel.com` return NXDOMAIN while the marketing apex answers |

⭐ **The pattern in that table is the finding.** A tunnel vendor that lists UDP
usually sells it, and the ones that give it away either meter it in gigabytes, cap
the session in minutes, or decline to publish a number. The four rows at the top
of this page are the exceptions.

## Chaining

**The one-port chain.** `portwarp UDP port -> wg-quick on any host -> every port
and protocol inside the tunnel`. The scarce link is an unpublished tolerance.

**The anycast chain.** `playit.gg custom UDP -> a WireGuard listener`. The scarce
link is one operator's regional bandwidth cost.

**The no-identity chain.** `openport.pw or a public frps -> a UDP port -> a
WireGuard listener`. Nothing in the chain needs an address, and nothing in it is
guaranteed.

## The records

`dossier/egress/portwarp.json`, `playit-gg.json`, `portmap-io.json`,
`openport-pw.json`, `pinggy-free.json`, `port-buddy.json`, `rustunnel.json`,
`wstunnel-demo.json`, `localtonet.json`, `tunnelthat.json`, `outray.json`,
`cloudpub.json`, `packetriot.json`, `openport-io.json`, `pagekite.json`,
`srv-us.json`, `ngrok-free.json`, `localxpose-free.json`, `loophole-cloud.json`,
`tunnelmole.json`, `tunnelto.json`, `tunnels-io.json`, `tsocket.json`, `bore.json`,
`localhost-run.json`, `remote-it.json`, `zrok-hosted.json`, `21tunnel.json`.

⚠ **No free UDP forward was measured end to end.** Every provider allocates a
port only after an account exists, and no account was created.
