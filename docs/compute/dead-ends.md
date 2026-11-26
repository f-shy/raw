# The closed doors, with the evidence of closure

A dead end recorded is not investigated twice. This document carries the doors that
are shut: a product withdrawn, a free tier removed, a creation gate, a quota that
cannot carry the work, and an identity the reader cannot produce. Each one has a
record with `verdict: dead` or `verdict: fails-*` and the evidence of its failure,
and none is deleted.

The counts below are rendered from the records, because a dead-end count is only
useful if it is a count of records. The rest of the closed doors are `paid-only`: a
product that exists and sells, with no free lane. The distinction matters: a product
recorded dead for having no free tier is re-investigated for the wrong reason.

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

## Withdrawn, with the sentence

**`the-hosting` The.Hosting, formerly PQ.Hosting.** The vendor's news page, dated
2026-05-30, states that "due to unforeseen and unavoidable force majeure circumstances,
The.Hosting is forced to permanently discontinue all its operational services and wind down
its activities", that "all active forms of registration, ordering, and renewals have been
disabled", and that "all accounts and data will be permanently deleted". The homepage and
several service pages still market capacity and a 3-day KYC-gated trial, so a reader who
lands on the wrong page sees a live host; the notice is the later artefact.

**`pq-hosting` PQ.Hosting.** The domain no longer sells hosting: `pq.hosting/en` is titled
"Global Hosting Catalog - Compare VPS, Dedicated Servers & Hosting Providers", every ranked
VPS entry links through `go.php?id=`, and the sitemap's 108 URLs contain no order, cart or
login path. The shop moved to `the.hosting`, which has since closed. A reader who finds
PQ.Hosting in an older price list is looking at an affiliate catalogue.

**Run Cloud.** `docs.run.cloud/sandboxes/index.md` (read 2026-10-22) states that
Linux microVM sandboxes are deprecated, that the capability is being retired, and
that it is no longer available to new organizations. This was the cheapest row in
the catalogue at USD 0.00, and a free-tier census counted a USD 15 a month recurring
credit.

**Play with Docker.** Unavailable from 2026-03-01. The canonical anonymous free VM
in every older list.

**`playht-playai` PlayHT / PlayAI.** Meta acquired the PlayAI team in July 2025 and the
platform was switched off at the end of 2025. Measured on 2026-10-22: the name no longer
resolves to a service. A voice-generation account was never general compute. The offer
vanished because the team was acquired, not because the product failed, which is a
failure mode no free-tier list tracks.

**Fly.io.** `fly.io/docs/about/pricing/` (read 2026-10-22) states in one sentence
that new organizations get no free tier and no monthly free usage allowance. The
trial is 2 hours of Machine runtime or 7 days. The host is up and the offer is gone,
so a verdict of dead is right and a verdict that the host is down is not.

**Cua.** `cua.ai/pricing` (read 2026-10-22) states the current offer connects
computer-use agents to the customer's own compute and the earlier hosted Fleet rate
is no longer published. Dead as a host, alive as a framework.

**Browser Linux emulators.** WebVM is the strongest: real Debian on x86 and real
Tailscale networking. The processor is the local machine and the machine dies with
the tab. Not remote capacity at all.

**Inference API hosts as a compute class.** An API that answers tokens is not a
machine that stays up. Recorded as a class-level dead end so the compute census
stops counting them; the providers themselves are the inference topic's.

## Gated at creation, which no keepalive fixes

**Hugging Face Spaces CPU Basic.** The hardware lists as FREE at 2 vCPU and 16 GB.
Creating a Gradio or Docker Space that uses it requires PRO for personal accounts
(`huggingface.co/docs/hub/en/spaces-overview`, read 2026-10-22). A create-time plan
gate is a wall: nothing a relay or a keepalive does changes it. The verdict is
`paid-only` with `binding: write-gated` rather than `dead`: the product is alive and
sells, and two records for one provider give a reader two answers.

**Gitpod.** The pricing URL resolves to a sales contact form asking for company
website, headcount and cloud provider (`ona.com/contact/sales`, read 2026-10-22).
Gitpod and Ona are one provider under two names and the catalogue carries both.

## A quota that cannot carry the work

**pythonanywhere.** `max_always_on_tasks = 0` on the free plan. The feature is
absent, not limited, and 100 CPU-seconds a day does not change that.

**Neon.** 100 compute unit-hours a month per project. A database that never sleeps
burns 730 hours and exhausts the allowance in about four days.

**Google Colab, at any tier.** Colab does not publish its limits because they vary
over time, and a paid user whose compute units are exhausted falls back to the free
policies (`research.google.com/colaboratory/faq.html`, read 2026-10-22). A workload
that needs a published ceiling cannot be scheduled here at any price.

## An identity the reader cannot produce

**ModelScope Studio on the `.cn` site.** The free Studio exists and the `.cn` site
wants a Chinese phone number. The `.ai` site is the international lane with a
different, larger tier. 2 vCPU and 8 GiB of free capacity that a registrant without
a Chinese phone number cannot reach is worth zero, and saying so is the finding.

**OpenReward.** The same shape for a different reason: compute bills by the second per
vCPU-hour and the only free credit route is an academic programme that has to be applied
for, which is an `institution` gate in practice.

## Trial-only, which is not dead

The `trial-only` records are usable tonight and they end. The largest are E2B at
USD 100 one-time with a 1-hour session, Daytona at USD 200 one-time, Railway's
anonymous box at 24 hours, Steel at USD 30 one-time, Vercel's 5 active-CPU hours a
month, and Hugging Face ZeroGPU at 5 minutes of GPU a day. A one-time credit is a
trial whatever its size, which is why DigitalOcean's USD 5 for 90 days and AWS
EC2's USD 100 are counted here with E2B's USD 100.

⚠ A trial is not a dead end and it is not a free tier. It is a clock. The
`free/free-tier-census.md` document counts the three kinds separately because the
distinction is easy to collapse.

## The paid-only records

A `paid-only` record is a product that exists, sells, and has no free lane worth
having. They are not failures and they are not dead. They are the rows a
reader should skip when looking for free capacity and consult when looking for the
cheapest paid path.

⛔ **Marking a no-free-tier product "DEAD" is the mistake this document exists to
prevent.** A provider marked dead on that basis is dropped from a recommendation and
re-investigated later, and the investigation finds a live product. Records
reclassified from `dead` to `paid-only` carry `extras.reclassified_from` so the
change is auditable.

## The doors that are only half shut

- **Blinkenshell** answers on 2222 and timed out on two probes. A timeout is a
  fact about the path; the record says `unverified` rather than dead.
- **Railway's anonymous VM** timed out on port 22 on two probes while nine pubnix
  hosts answered from the same network, seven of them in under 0.6 s. Unproven, and
  not withdrawn by the vendor.
- **tilde.guru** accepted a connection and sent no banner within 6 seconds. Slow
  greeting or a filter, and not a dead host.
- **Oracle's 403** was the probing host's egress and not the domain. `oracle.com`
  returns 200 to the same probe.
- **Lightning AI's 403** was the same thing. The offer is real and the page is
  reachable.

⭐ **An apparent death signal has three common causes**: a withdrawn product, a
regional block on the reader, and an offer that changed. Only the first is a dead
provider. Recording all three as "dead" deletes live rows, and that is the failure
this section exists to make visible.

## What the count means

A reader looking for free capacity tonight should read the `qualifies*` records
and treat everything else as a constraint rather than an absence. Two of the
`dead` rows are class-level census guards rather than providers.

⚠ A dead-end count is only useful if it is a count of records. A row can move from
`dead` to `paid-only` without a provider changing, which is why the records carry the
reclassification and the count is derived from the records rather than typed.
