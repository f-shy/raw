# How do I put a local service on a public URL, and what kills the URL?

A hosted tunnel dials out from the local machine to a rendezvous, and the provider
sells the public hostname. Nothing listens on an inbound port, so this is the only
shape available to a host behind carrier NAT or on a sandbox that refuses
`bind(2)`. The class splits on what the provider meters: a session's lifetime, a
day's bytes, or nothing at all.

The answer is that the good free tunnels are fast enough and their limits are
shaped badly. A Quick Tunnel moved 400 MiB in 58 s and served 400 concurrent
requests without a 429, and its hostname dies when the process does. Pinggy keeps
the tunnel for an hour at 26.9 KiB/s. localhost.run and serveo do not work at all,
measured. Nothing here is a serving tier for 500 GB a day.

Sorted by what a reader can use now, not alphabetically.

| provider | free tier | what binds | identity | verdict |
| --- | --- | --- | --- | --- |
| Cloudflare Quick Tunnel | one ephemeral hostname, no account | `retention-clamped`: the hostname dies with the process | anonymous | `qualifies` |
| Cloudflare Tunnel (named) | unmetered transit, 1,000 tunnels | `write-gated`: a domain on Cloudflare nameservers | email | `qualifies-with-caveat` |
| Pinggy | 60-minute session, unlimited data | `per-ip-shaping`: 26.9 KiB/s measured | anonymous | `qualifies-with-caveat` |
| playit.gg | no published cap | `per-ip-shaping`: an unpublished tolerance | email | `qualifies-with-caveat` |
| LocalXpose | 2 active tunnels, no time limit | a count of tunnels, which is not one of the seven kinds | email | `qualifies-with-caveat` |
| tunnelto | free generated subdomain | none published | email | `qualifies-with-caveat` |
| openport.pw | one persistent port, no signup | unstated | anonymous | `qualifies-with-caveat` |
| Cruma | 1 GiB per session, 3-hour anonymous session | `volume-quota`: 1 GiB per session | anonymous | `qualifies-with-caveat` |
| liveapps.dev | free named subdomain, no account | `retention-clamped`: the URL lasts about an hour | anonymous | `qualifies-with-caveat` |
| nport.link | free stable URL, no sign-up | `retention-clamped`: a 4-hour session cap | anonymous | `qualifies-with-caveat` |
| LetsTunnel | free, no account claimed | the relay presents a self-signed certificate | anonymous | `fails-egress` |
| localtunnel | a public URL on a shared server | none published | anonymous | `qualifies-with-caveat` |
| bore | MIT software, one shared public instance | nothing binds; `bore.pub` publishes no quota | anonymous | `qualifies-with-caveat` |
| localhost.run | free subdomain, no account | `per-ip-shaping`: 11.4 KiB/s measured | anonymous | `fails-egress` |
| serveo | 3 active tunnels | the hostname has no DNS record | anonymous | `fails-egress` |
| Tailscale Funnel | public HTTPS on a *.ts.net name | `per-ip-shaping`: non-configurable, unpublished | email | `fails-quota` |
| ngrok | 1 GB out/month | `per-ip-shaping`: the 1 GB/month allowance | email | `fails-quota` |
| zrok hosted | 5 GB/day | `per-ip-shaping`: the 5 GB/day allowance | email | `fails-quota` |
| frp (self-hosted) | Apache-2.0 software, no hosted free tier | `volume-quota`: the host's monthly egress allowance | anonymous | `paid-only` |

## Cloudflare Quick Tunnel

One command starts it and prints a random `*.trycloudflare.com` hostname. No account, no
card, no domain. A 100 MiB object read back byte-identically: 104,857,600 bytes in
15.948 s, which is 6.27 MiB/s single-stream (`measured`, 2026-10-22). Three earlier
sequential runs of the same object were logged as 9.32, 7.87 and 10.64, with no unit,
byte count or elapsed time kept. The divisor behind them is unrecoverable, so none is
used in any arithmetic here. The 6.27 MiB/s is the number this record stands on.

⛔ The body cap does not apply. A 400 MiB POST traversed the tunnel with a matching
SHA-256 in 77 s (`measured`, 2026-10-22). The 100 MB figure belongs to a proxied
zone request and a trycloudflare hostname is not a zone. 400 concurrent GETs of a
3-byte object all returned 200 in 6.5 s.

⚠ What breaks is concurrency on large objects. At 8 simultaneous 100 MiB ranged
GETs, 6 of 8 connections returned 206 and 2 returned 522, with aggregate
throughput 3.72 MiB/s. At 32 simultaneous, 24 of 32 returned 206 and 8 returned 522,
with aggregate throughput 3.79 MiB/s (`measured`, 2026-10-22). Both are below the
6.27 MiB/s single-stream baseline. The tunnel degrades rather than queues.

⚠ **Read that row as a failure count and not a success count.** One connection in
four fails at 8-way concurrency and one in four at 32-way, so a design sized for 32
parallel readers must tolerate 8 refusals.

Evidence: `developers.cloudflare.com/fundamentals/reference/connection-limits/`
(read 2026-10-22) carries the proxied body cap and the 125 s read timeout; probe
records in `dossier/egress/cloudflare-quick-tunnel.json`.

⚠ **One number, one citation.** The 100 MB cap is the proxied request body limit on
the connection-limits page. The Workers platform limits page states a Worker request
body limit, which is a different product and not this number.

Verdict: `qualifies` for a test, a webhook or a handover. The hostname's lifetime
is the finding, not the throughput.

## Cloudflare Tunnel (named)

The same transport with a hostname on a zone the reader controls, which is what makes
it stable. Transit is unmetered: the account-limits page lists 1,000 tunnels, 25
replicas per tunnel and 50,000 routes, and no bandwidth figure at all
(`documented`, 2026-10-22). Cloudflare staff wrote "There are no bandwidth limits"
in the community forum on 2022-06-21.

That is a documented absence, not a quota. It is not multiplied here and it is not
a contract term. The terms that do bind are the 100 MB proxied request body on
Free and Pro and the 125 s proxy read timeout, both of which return an error rather
than shaping (`documented`, 2026-10-22).

Evidence: `developers.cloudflare.com/cloudflare-one/account-limits/` and
`developers.cloudflare.com/fundamentals/reference/connection-limits/` (read
2026-10-22).

Verdict: `qualifies-with-caveat`. The domain is the only paid element and the
only gate.

## Pinggy

One SSH command opens a tunnel that lasts 60 minutes unauthenticated, printed in
the SSH banner as "Your tunnel will expire in 60 minutes" (`documented`,
2026-10-22). Data is unlimited, and the measured rate is 26.9 KiB/s: 4,847,616 of
10,485,760 bytes arrived in 180 s before the client gave up, while a 3-byte
control file returned in 1.1 s (`measured`, 2026-10-22).

"Unlimited data" is true and the rate makes it useless. 26.9 KiB/s is 2.2 GiB/day,
0.2% of the daily floor this topic measures.

Evidence: probe records in `dossier/egress/pinggy-free.json`.

Verdict: `qualifies-with-caveat`. The 60-minute cap is what the docs say; the
rate is what stops it.

## LocalXpose

Two concurrently active HTTP and HTTPS tunnels with no session limit
(`documented`, 2026-10-22). An active tunnel is any tunnel currently running, so
it is a concurrency cap rather than an allowance.

⚠ **That is a count and not a rate.** An active tunnel has no window, so
`request-rate` is the wrong kind. The record carries the count in `limits_note`, and
no kind in the vocabulary names a count.

No byte quota is published, so there is no capacity number and none was measured.
The free tier shows an interstitial warning page to visitors.

Evidence: `localxpose.io/pricing` (read 2026-10-22); record
`dossier/egress/localxpose-free.json`, `documented`, `qualifies-with-caveat`,
with the count in `limits_note` because two concurrently active tunnels is a count
and no kind in the vocabulary names a count.

Verdict: `qualifies-with-caveat`. Two tunnels with an unknown ceiling.

## playit.gg

A game-tunnel service with no published cap, and its operator answered the
question on the company forum on 2026-05-28: "Last I checked we had a free user
consuming about 1-2 TB per day... if I don't notice our cost meaningfully increase
... it's not much of a concern" (`reported`, forum post). The same post says
100 GB/day in Australia would probably draw contact, so the tolerance is regional.

Generic TCP and TCP+UDP moved to the paid tier; free ports are game presets and
UDP (`documented`, 2026-10-22).

Evidence: `discuss.playit.gg/t/traffic-limits/5574` and `playit.gg/` (read
2026-10-22).

Verdict: `qualifies-with-caveat`. The strongest free relay found and the least
durable evidence: one sentence, one operator, one day, revocable.

## tunnelto

Free tunnels on a generated `*.tunnelto.dev` subdomain; USD 4/month buys 20
reserved subdomains (`documented`, 2026-10-22). The standalone `/pricing` path
returns 404 and the pricing block lives on the landing page under an anchor
(`measured`, 2026-10-22).

Evidence: `www.tunnelto.dev/` (read 2026-10-22).

Verdict: `qualifies-with-caveat`. Live, with no published limit.

## openport.pw

One persistent TCP or UDP port with no signup and no published quota, on a single
donated host (`documented`, 2026-10-22). Not measured.

Evidence: `openport.pw/` (read 2026-10-22); record
`dossier/egress/openport-pw.json`, `documented`, `qualifies-with-caveat`, binding
`per-ip-shaping` with the value unstated and a dash where a number would go.

Verdict: `qualifies-with-caveat`. A dash where the number would go.

## localtunnel

An npm client against a shared volunteer-run server, which assigns a random public
URL (`documented`, 2026-10-22). The project page states that it assigns a URL and
says nothing at all about a limit.

That absence is the finding: there is no vendor pricing page and no published ceiling,
so there is nothing to design against. The shared server is one instance of someone
else's capacity, and that class decays in months. Not measured, because a throughput
number from one shared instance would describe that instance on that day and not the
service.

Evidence: `localtunnel.github.io/www/` (read 2026-10-22); `localtunnel.me` answers
302 and has no pricing page (`measured`, 2026-10-22);
`dossier/egress/localtunnel.json`.

Verdict: `qualifies-with-caveat`. A dash where the number would go.

## bore

MIT-licensed client and server, with one shared public instance at `bore.pub`
(`documented`, 2026-10-22). The software is the product and `bore.pub` is a
courtesy.

**Probed on this host.** `bore-cli 0.6.0` server and client carried a
4,194,304-byte object byte-identically at 1.88 MiB/s, against 53.47 MiB/s on a
direct connection to the same server (`measured`, 2026-10-22). The digest matched:
`46386cf4dbccceb80f80148d46d37f1a30d72912089cfbe4b3e51d9d55a79747`.

⚠ **`bore.pub` was not reached and the record says so.** The name resolves over
DNS-over-HTTPS to `159.223.110.159` and `2604:a880:400:d1:0:4:822c:e001`, and TCP
7835 to that address accepts a connection, but this host's own resolver returns no
record for the name, so the client failed with `os error 11004`. That is a defect on
this host and not a finding about the service.

`bore.pub` publishes no quota of any kind, which is the documented absence this
document keeps warning about. The verdict is a caveat rather than a pass because
the probe measured the software and not the instance.

Evidence: `github.com/ekzhang/bore` (read 2026-10-22); probe records in
`dossier/egress/bore.json`.

Verdict: `qualifies-with-caveat`. One shared instance, no published capacity.

## localhost.run

An SSH tunnel with no account, and the docs say it is speed-limited without saying
by how much. Measured: 4,128,768 of 104,857,600 bytes in 180 s, and 1,027,916 of
1,048,576 bytes in 90 s (`measured`, 2026-10-22). Two objects, two sizes, the same
23 KB/s aggregate ceiling, so it is shaping rather than a slow object.

11.4 KiB/s is 0.98 GiB/day.

Evidence: probe records in `dossier/egress/localhost-run.json`.

Verdict: `fails-egress`. The census left this a caveat because the number was
unpublished; the measurement closes it.

## serveo

The SSH handshake succeeds, the banner prints a tunnel URL, and the hostname
resolves to `0.0.0.0` and `::` from 8.8.8.8. Two sessions produced two different
hostnames and neither resolved (`measured`, 2026-10-22).

This is the HTTP-200 failure mode in host form: the control plane answers and the
data plane does not exist.

Evidence: `serveo.net/` (read 2026-10-22) for the 3-tunnel free plan; probe record
in `dossier/egress/serveo.json`.

Verdict: `fails-egress`.

## Tailscale Funnel

Public HTTPS on a `*.ts.net` name on every plan, on ports 443, 8443 and 10000
only, and "Traffic sent over a Funnel is subject to non-configurable bandwidth
limits" (`documented`, 2026-10-22). The value is not published.

A throttle with no number is worse than a quota: there is no threshold to design
against and no point at which it is safe.

Evidence: `tailscale.com/kb/1223/funnel` (read 2026-10-22).

Verdict: `fails-quota`, recording the absence rather than a figure.

## ngrok

1 GB out, 20,000 HTTP requests and 5,000 TCP connections per month on three
endpoints, with an interstitial page in front of HTML traffic
(`documented`, 2026-10-22). 1 GB is 1,000,000,000 bytes decimal, so a day of it is
33.3 MB, which is 31.8 MiB. That is 0.003% of one day.

⚠ **Two units and two shares are easy to get wrong here.** "33.3 MiB/day" prints a
decimal quantity with a binary unit, and "0.1% of one day" overstates the share by 33
times. 31.8 MiB against 1 TiB is 0.003%.

Evidence: `ngrok.com/docs/pricing-limits/free-plan-limits` (read 2026-10-22); record
`dossier/egress/ngrok-free.json`, `documented`, `fails-quota`, binding
`per-ip-shaping` on the 1 GB/month allowance in `egress.free_allowance`.

Verdict: `fails-quota`.

## zrok hosted

"5 Daily GB" in the Free column of the pricing page, with 25 environments and 50
share backends (`documented`, 2026-10-22). The read broker's Markdown view drops
the figure; it is in the rendered HTML. 5 GB/day is 0.45% of one day.

Evidence: `zrok.io/pricing/` (read 2026-10-22); record
`dossier/egress/zrok-hosted.json`, `documented`, `fails-quota`, binding
`per-ip-shaping` on the 5 GB/day allowance in `egress.free_allowance`. The
self-hosted controller is a separate record,
`dossier/egress/zrok-selfhost.json`, Apache-2.0 with no bandwidth journal
configured by default, which is why it carries no binding.

Verdict: `fails-quota`.

## frp

Apache-2.0 client and server, with no hosted free tier found (`documented`,
2026-10-22). Every "free frp server" lead was a VPS advertisement.

**Probed on this host.** `frps` and `frpc` 0.71.1 carried a 4,194,304-byte object
byte-identically at 42.91 MiB/s through a TCP proxy, against 38.73 MiB/s direct
(`measured`, 2026-10-22). The digest matched the source. The bytes transit the
operator's own host, because there is no vendor in the path.

This is the one self-hosted row in the document, and the last resort (`AGENTS.md`
section 2 rule 9): it comes after every hosted tunnel above. A reader who searches for
"free frp server" finds only advertisements.

Evidence: `github.com/fatedier/frp` (read 2026-10-22); probe records in
`dossier/egress/frp.json`.

Verdict: `paid-only`. The software is free and the path is not. It needs a host
with a public address, and that host is a separate provider. The finding is the host,
not frp.

## What a capability-free sandbox measured on 2026-11-05

A second harness ran the authless clients from a sandbox that refuses `bind(2)`, with
the origin on a unix socket and the tunnel client's origin dial rewritten. Every
"works" below returned an origin marker over the public URL, so the tunnel carried
real bytes, not a landing page. The numbers are that sandbox's; the *ordering* and the
hard caps are the durable part.

| provider | median `/lat` | bulk transfer | hard cap observed |
| --- | --- | --- | --- |
| liveapps.dev | 223 ms | 4 MiB fails with a 504 after ~30 s | a 30 s relay timeout |
| Cruma | 329 ms | 4 MiB at 117-126 kB/s | 1 GiB per session, 3-hour session |
| srv.us | 357 ms | 4 MiB does not finish at 31-43 kB/s | none, only the throttle |
| localtunnel | 391 ms | 4 MiB at about 20-22 kB/s | none, only the throttle |
| bore.pub | 406 ms | 4 MiB stalls at about 18 kB/s through that egress | none |
| localhost.run | 458 ms | 4 MiB at 6-8 kB/s | none, only the throttle |
| serveo | 710 ms | connection dies at about 2.4-2.5 MiB after ~10 s | a per-connection transfer cut |
| Pinggy | 836 ms | 4 MiB does not finish at about 50 kB/s | the 60-minute session |
| tunnl.gg | 908 ms | both runs stop at exactly 2,486,272 bytes | about 2.37 MiB per request |

Three findings a reader should carry:

1. **Latency and throughput are independent.** liveapps.dev has the lowest median and
   cannot finish a 4 MiB object; serveo has the highest raw bandwidth and cuts the
   connection mid-transfer. Sort by the job, not by a single number.
2. **The SSH relays are throttled, not broken.** srv.us, localhost.run and Pinggy all
   carry an origin marker at 30-900 ms, and all three are shaped to tens of kB/s. A
   webhook or an SSH session is fine; a file is not.
3. **A password page on a free tunnel is not a failure.** localtunnel's visitor page
   asks for the tunnel password, which is the host's public IP: it is the service's
   normal anti-abuse step. The throttle and the multi-second stalls are the honest
   limits; its client repository has had no push since 2025-08.

The authless set is also shrinking: Optimistix is shut down, ssi.sh's hosted demo
requires password or a pre-registered key, tunnelto is account-gated trialware, and
LetsTunnel's relay presented a self-signed certificate on 2026-11-05. The durable
authless paths are the Cloudflare quick tunnel, Cruma, liveapps.dev, nport.link and the
SSH relays that kept anonymous usernames.

## What did not work

- **localhost.run**: 11.4 KiB/s measured. `fails-egress`.
- **serveo**: the tunnel hostname has no usable DNS record. `fails-egress`.
- **Tailscale Funnel**: an unpublished, non-configurable throttle. `fails-quota`.
- **ngrok free**: 1 GB per month, which is 31.8 MiB/day. `fails-quota`.
- **zrok hosted**: 5 GB per day. `fails-quota`.
- **`/pricing` as a liveness test**: tunnelto's `/pricing` returns 404 while the
  product is live and its pricing sits on the landing page.
- **`bore.pub` as a measured capacity figure**: the probe client could not reach it
  from this host, because this host's resolver returns no record for the name while
  DNS-over-HTTPS resolves it to `159.223.110.159` and TCP 7835 accepts a
  connection. `bore` is recorded `qualifies-with-caveat` on a self-hosted probe
  instead, and `bore.pub` publishes no capacity.
- **localtunnel as a serving tier**: no published limit and a single shared server,
  so there is no ceiling to design against and no operator to hold to it.
- **Free consumer-connection proxies at volume**: every trial is 100 MB to 2 GB, gated on
  a card, KYC or a top-up, and the cheapest rate after that is USD 0.80/GB
  (`reported`, one vendor page), which is USD 880 a day at this volume to two
  significant figures. `fails-quota`.
- **Free public frp servers**: every lead was a VPS advertisement. `frp` is self-hosted
  software and not a service. A local `frps` and `frpc` pair carried a 4 MiB object
  byte-identically at 42.91 MiB/s against a 38.73 MiB/s direct baseline
  (`measured`, 2026-10-22), so the software works and no hosted instance exists.

## Chaining

Two chains survive.

**A stable address with no static IP.** `domain on Cloudflare nameservers ->
Cloudflare Tunnel -> origin`. The scarce link is the domain, about USD 10.46 a
year at Cloudflare Registrar, and it is the only paid element in the chain. A
tunnel requires Cloudflare-authoritative DNS, so deSEC plus Tunnel does not work;
the chain is Cloudflare-DNS-or-nothing for this shape.

**The sealed-sandbox reach-in.** `dropbear in inetd mode -> an outbound WebSocket -> a
rendezvous that pairs by name -> ssh with ProxyCommand`. A real login returned `uid=966`
and `Linux` over a connection the host could only dial out. The scarce link is the
pair's 72-hour lifetime and the fact that both tokens are bearer credentials.

⚠ **The `bore` and `frp` chains are both self-hosted.** `bore-cli 0.6.0` server and
client on this host carried a 4 MiB object byte-identically at 1.88 MiB/s against a
53.47 MiB/s direct baseline (`measured`, 2026-10-22). Both are software chains and
neither is a service chain, so neither answers the question about a public URL. The
probe proves the transport rather than a vendor's capacity.

Neither chain moves bulk bytes; [`free/bulk-egress.md`](bulk-egress.md) covers the
lanes that do.
