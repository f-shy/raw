# What a tunnel catalogue reduces to

The public tunnel lists are long. Read one end to end and count what survives a
single question: does this service carry arbitrary UDP to a client, for 1 TiB per
month, at no cost? This page records what one such list reduces to.

⭐ **The result is a rule about the class, not a list of near misses.** A tunnel
product almost always sells an HTTPS URL for one local port. That product shape
cannot carry UDP even when its marketing says "unlimited", and the price is not
the obstacle. Every entry is recorded because the entry is what answers the
next reader who finds the same vendor.

The sweep covered 105 entries. Twenty-one reached the `documented` rung, which means a
page was read and the sentence is quoted in the record. The rest are `reported`.

## The entries

Sorted by verdict, because the verdict is what a reader acts on.

| provider | transport | free ceiling | identity | verdict |
| --- | --- | --- | --- | --- |
| Global Socket | TCP, public relay | no limit published | anonymous | `qualifies-with-caveat` |
| tuns.sh | TCP and UDP | none, paid membership | email | `paid-only` |
| UpVPN | TCP and UDP | none, metered or annual | card | `paid-only` |
| LocalCan | HTTPS, TCP on paid | 1 GB per month | email | `fails-quota` |
| Microsoft Dev Tunnels | TCP, ports 1 to 65535 | 5 GB per month | email | `fails-quota` |
| Beeceptor Local Tunnel | HTTPS | none published | email | `fails-egress` |
| Horizon Tunnel | HTTPS | none published | email | `fails-egress` |
| InstaTunnel | HTTPS | none published | email | `fails-egress` |
| Livecycle | HTTPS | none published | email | `fails-egress` |
| Svix Play | HTTPS webhook | none published | anonymous | `fails-egress` |
| tunnel.pyjam.as | HTTPS over a WireGuard link | none published | anonymous | `fails-egress` |
| Tunnelite | HTTPS and WebSocket | none published | email | `fails-egress` |
| Tunnet | HTTPS public, mesh private | none published | email | `fails-egress` |
| Defined Networking | Nebula overlay | 100 devices | email | `fails-egress` |
| EasyTier | volunteer relays | not published | anonymous | `fails-egress` |
| Lantunnel | mesh, no public URL | not published | email | `fails-egress` |
| SSH-J.com | SSH jump, no public port | not published | anonymous | `fails-egress` |
| Optimistix Tunnel | none, service shut down | not applicable | anonymous | `dead` |
| Lokal.so | none, domain repurposed | not applicable | anonymous | `dead` |
| pgrok (proxy.jetzt) | none, archived relay | not applicable | anonymous | `dead` |
| Tabserve.dev | none, domain repurposed | not applicable | anonymous | `dead` |

## The row that qualifies

Global Socket is the entry with no account that survives the sweep. It is a binary
plus a public relay, and the project page shows SSH reached over the relay with a
shared secret as the only credential (`documented`, read 2026-10-23). It publishes
no byte, port or time limit and carries no price, so the allowance is a lead rather
than a number. A sandbox measured a 2.6-3.1 s round trip per request through the
public relay on 2026-11-05, the cost of an SRP-4096 handshake per connection.

⚠ **A relay with no published limit is the cheapest thing here and the least
certain.** The provider is a volunteer project, so a tolerance exists whether or not it is
written down. It is the one entry in this list worth a sustained transfer before any
other.

Optimistix Tunnel, the previous answer, has been **permanently discontinued**: its
own page says so, points readers at Cloudflare Tunnel, and states that all tunnels,
subdomains and accounts are no longer active (`documented`, read 2026-11-10). A
challenge page had once made it look alive, which is why a third-party harness
rechecked it and recorded the shutdown on 2026-11-05. Its two limits are moot now:
it never published a byte tolerance, and the protocol wall was TCP only.

## The limits table the overview omits

Microsoft Dev Tunnels is recorded as `fails-quota`, and the number is 5 GB per month.
The overview page and the FAQ state no allowance at all, which reads as an unpriced free
forward. The limits table on Microsoft's own page states otherwise (`documented`, read
2026-10-23):

| resource | limit |
| --- | --- |
| Bandwidth | 5 GB per user |
| Tunnels | 10 per user |
| Active connections | 1,000 per port |
| Ports | 10 per tunnel |
| HTTP request rate | 1,500 per minute per port |
| Data transfer rate | up to 20 MB/s per tunnel |
| Web-forwarding request body | 16 MB |

5 GB is 0.0045 TiB, so the allowance fails about 220 times before the test. The
20 MB/s ceiling per tunnel would carry 1 TiB in about 15 hours, so the monthly
byte quota binds first.

⭐ **The lesson is a search rule, not a fact about Microsoft.** A vendor's
overview page and its FAQ can both omit the limits table, and the table is
usually on a resource-limits page under a different product. Read the limits
page before you conclude that a free tier is unmetered.

## The two UDP rows, and why both cost money

tuns.sh is the most interesting entry in the list. Its pricing page documents an
SSH-based UDP forward in a shipped command:

```bash
ssh -w 0:0 tuns.sh udp-forward=10000:local-ip-of-machines-main-interface:5553
```

That is a real UDP ingress path with no client software beyond OpenSSH
(`documented`, read 2026-10-23). It appears only in the `pico+` column, so the
first failure is the subscription rather than a byte quota.

UpVPN provisions WireGuard peers and prices 1 TiB at roughly USD 41 in data
charges on the metered plan, or USD 39.99 per year with no data charge
(`documented`, read 2026-10-23). It is the clearest paid WireGuard path in the
list, and it is in `docs/egress/paid/wireguard-ingress.md`.

⛔ **Both UDP rows charge, and both are recorded anyway.** A class where the
protocol works only on a paid plan is a finding about the class.

## The HTTPS tunnels

Nine entries sell an HTTPS URL for one local port. Beeceptor calls its product a
local tunnel and counts intercepted requests. Horizon Tunnel gives a random
subdomain with WebSockets and a request log, with no time limit on the free
plan. InstaTunnel allows three simultaneous tunnels and ends a session every 24
hours. Livecycle embeds the tunnel in a Docker collaboration product. Svix Play
relays webhooks and counts requests rather than bytes.

Tunnelite publishes the rule that the rest obey: "If you need TCP tunneling,
you'll have to host the server yourself." Its managed tier carries HTTP and
WebSocket only. Tunnet offers public HTTPS and a private mesh, and the public
path is HTTPS only. LocalCan adds TCP on a paid plan and gives 1 GB per month on
the free one, which is 0.0009 TiB.

tunnel.pyjam.as is the exception worth reading twice. It issues a WireGuard
config with one `curl`, then carries HTTPS over that link
(`documented`, read 2026-10-23). The WireGuard link is how the vendor reaches
its relay, not a port the client can listen on, so the ingress is still HTTPS
only. It is in `docs/egress/free/wireguard-transports.md` for that reason.

## The meshes with no public address

A private overlay is not ingress. Defined Networking gives 100 devices free on a
managed Nebula control plane, and an outside peer must be enrolled before it can
send a packet. EasyTier is software with volunteer relays: no hosted endpoint and
no published capacity. Lantunnel says "Direct connectivity is not guaranteed".
SSH-J.com is an anonymous jump host whose own page says "No public ports, only
in-SSH connectivity".

None of these is metered, so no quota fails at 1 TiB. The structure fails
first.

## What is dead

Three entries no longer exist as described. Lokal.so and Tabserve.dev now serve
unrelated content, one a casino page and one an Indonesian gambling page, and
both were recorded as `dead` with the sentence they serve today. pgrok's relay
domain serves the archived GitHub README of an ngrok 1.0 fork.

A fourth kind of death is silent and is not on this page: a vendor that answers
HTTP 200 with a placeholder body.

## What this list could not establish

No account was created, so no record is `measured`. Every free
ceiling here is a vendor sentence. The three entries whose pages a client script
renders, Teleport, Webhook Relay and Pritunl, returned markup without a readable
body and are recorded at a lower rung with the route that failed.

⚠ **The search is only as good as the list.** A vendor that forwards UDP and
publishes neither that fact nor a byte figure is invisible to this method. The
answer to that gap is a measurement per provider, not another list.

## The records

`dossier/egress/optimistix-tunnel.json`, `gsocket.json`, `tuns-sh.json`,
`upvpn.json`, `localcan.json`, `microsoft-dev-tunnels.json`, `beeceptor.json`,
`horizon-tunnel.json`, `instatunnel.json`,
`livecycle.json`, `svix-play.json`, `tunnel-pyjam-as.json`, `tunnelite.json`,
`tunnet.json`, `defined-networking.json`, `easytier.json`, `lantunnel.json`,
`ssh-j.json`, `lokal-so.json`, `pgrok-fork.json`, `tabserve.json`.
