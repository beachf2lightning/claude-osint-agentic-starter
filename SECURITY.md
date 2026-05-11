# Security policy

This document describes how to report a vulnerability in this defensive OSINT and recon-automation starter, which versions receive security fixes, what we expect a good report to look like, and the scope of issues we treat as security concerns.

For general contribution workflow see [CONTRIBUTING.md](CONTRIBUTING.md). For project guardrails and the defensive safety scope see [CLAUDE.md](CLAUDE.md).

## How to report a vulnerability

Use **GitHub Security Advisories** to report a vulnerability privately.

1. Open the repository on GitHub.
2. Go to the **Security** tab.
3. Choose **"Report a vulnerability"**.
4. Fill in the private draft advisory.

The draft is visible only to repository maintainers and the reporter until publication.

**Do not file public issues, pull requests, or discussions for security reports.** A public report exposes the vulnerability before a fix is available. This project uses GitHub Security Advisories as the only supported intake channel — there is no security email address.

## Supported versions

The project is pre-1.0 with no tagged releases yet. Security fixes land on `main` first.

| Version | Supported |
|---|---|
| `main` branch (HEAD) | Yes — security fixes land here first. |
| Tagged releases | None yet. Once `0.1.0` ships, the latest minor will receive fixes. |
| Forks and downstream packages | Not maintained by this project; report to the fork or distributor. |

If you need stability today, pin to a specific commit and watch the repository for advisories.

## What to include in a report

A useful report contains:

- The affected component or file path (for example, `src/agentic_starter/targets.py`).
- Your severity assessment in your own words (low, medium, high, critical) and the reasoning.
- A minimal reproduction — ideally a failing test or a short command sequence.
- Impact: what an attacker could do, under what assumptions, and against whom.
- A suggested mitigation if you have one.
- Environment details when relevant: Python version, OS, install method (editable, Docker, etc.).

## What NOT to include in a report

To keep reports safe to read and act on:

- **No real production secrets or live tokens.** Even rotated ones — do not paste them. Use redacted or synthetic values.
- **No real customer or client data.** No real domains, IP ranges, asset lists, or user records.
- **Nothing obtained through unauthorized access or testing.** If reproducing the issue required violating someone's terms of service or applicable law, do not include those details.
- **No raw automated-scanner output without analysis.** Provide a focused repro, not a dump.
- **No weaponized PoCs, working malware, or persistence chains.** Defensive PoCs only — enough to demonstrate the issue, not enough to exploit at scale.
- **No RFC1918 ranges from real internal networks.** Use RFC 5737 documentation IPs (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) and RFC 2606 documentation domains (`example.com`, `example.org`, `example.net`).

## Our response process

This is a solo-maintained starter repository, so the process is best-effort rather than a service-level commitment:

- We will acknowledge receipt as soon as practical.
- We will triage and assess severity, and let you know if more information is needed.
- We will work toward a fix and a published advisory, coordinating the timeline with the reporter where possible.
- For issues with active exploitation evidence, the timeline accelerates and disclosure may follow the fix immediately.
- Reporters are credited in the published advisory by default. If you would prefer to remain anonymous, say so in your report and we will leave you out of the credit line.

We will not set hard SLAs we cannot honor. If a report sits unanswered longer than feels reasonable, please nudge via a follow-up comment on the draft advisory.

## Out of scope

The following are not handled through the security disclosure channel:

- **Findings against third-party dependencies.** Report to the upstream project. We will bump pinned versions promptly once an upstream fix lands.
- **Documentation typos, style issues, or markdown rendering quirks.** Use a regular pull request.
- **Issues only reproducible by violating the project's documented safety scope** — see the "Not allowed" list in [CLAUDE.md](CLAUDE.md) and [CONTRIBUTING.md](CONTRIBUTING.md). The scope is a feature, not a bug.
- **Example fixtures and placeholder data.** RFC 2606 reserved domains and RFC 5737 documentation IPs in `examples/` and `tests/` are intentional. Domains like `example.com` are not vulnerabilities.
- **Vulnerabilities in deployments or forks** of this code by third parties. Those are the operator's responsibility.
- **CVE assignment requests.** This project does not currently assign CVEs. If you need one, request via MITRE or your CNA.

## Safe testing guidelines

If you are exploring whether something is a security issue:

- Test only against assets you own or are explicitly authorized to assess.
- Stay passive (no active probing) unless authorization is documented.
- Use lab targets for any active behavior — see `examples/osint-targets/authorized-scope.example.txt` for the format.
- Do not test against GitHub, Anthropic, or downstream consumers as part of testing this repository.

This project is built for defensive use. Reports demonstrating only that the codebase could be modified to do something unsafe (for example, "this could be rewritten to scan unauthorized targets") are out of scope under the "Out of scope" section above.

## Thank you

Responsible disclosure makes the ecosystem better. Thanks for taking the time to report issues privately and to work with maintainers on a coordinated fix. For everything outside of security, see [CONTRIBUTING.md](CONTRIBUTING.md).
