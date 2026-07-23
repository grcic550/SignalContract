# SignalContract Study-Resource Reference — July 2026 Verification

## TL;DR
- **Almost every resource a 2025-era roadmap would list is still live in mid-2026, but several key assumptions are now stale** and must be corrected before the schedule is built: the **OWASP Top 10 2025 is finalized** (announced November 2025 at the OWASP Global AppSec Conference in Washington, D.C. and released as the final version in January 2026), with two new categories and A09 renamed to "Security Logging & Alerting Failures"; **Python's current stable is 3.14** (Python 3.14.6 released 10 June 2026 — "the sixth maintenance release of 3.14, containing around 179 bugfixes"), not 3.13; **Astral's uv/Ruff/ty toolchain is being acquired by OpenAI** (announced 19 March 2026, tools to remain open source) and uv is now the mainstream package manager; and the **Helsinki Python MOOC 2026 edition exists and is open** (course listing: "Introduction to Programming, MOOC 12/1–31/8/2026"; the site states "The course will be open until the end of the year 2026").
- **The single most cost-sensitive decision is Hack The Box Academy.** With a verified university email the **Student plan is $96/year (~$8/month)** and "opens Tier I and II modules," which fully covers the **CPTS Penetration Tester path (28 modules)**; the **standalone CPTS exam voucher is $210** (2 attempts; 10-day practical window + 10-day report window). A Croatian university email (e.g. @unist.hr, @fesb.hr, @studenti.unist.hr) qualifies if the domain is already registered in HTB's database — otherwise a support ticket validates it or accepts proof of enrolment.
- **Anchor the plan on free/low-cost resources:** Helsinki MOOC + CS50P + Exercism (all free) for Python; the free GitHub Student Developer Pack (JetBrains PyCharm, GitHub Copilot student access, cloud credits) for tooling; HTB Academy Student plan as the one paid subscription (~$242 total to CPTS including the voucher); with Croatian community resources (Split Tech City, Python Hrvatska) as supplements and TryHackMe's ~$100/year student plan as a fallback.

## Key Findings

### CHANGED vs a 2025-era roadmap — flag and fix these
- **Python version:** current stable is **3.14** (3.14.6, released 10 June 2026; supported through Oct 2030), not 3.13. The Python Tutorial's section numbering is unchanged, but any roadmap text pinned to "3.13" is behind. Python 3.15 is in alpha (expected Oct 2026).
- **OWASP Top 10 2025 is FINAL** (announced November 2025 at OWASP Global AppSec, Washington D.C.; final version released January 2026). SSRF was absorbed into A01; two brand-new categories appear (A03 Software Supply Chain Failures, A10 Mishandling of Exceptional Conditions); Security Misconfiguration jumped to #2. A09 was renamed from "Security Logging and Monitoring Failures" to **"Security Logging & Alerting Failures"** — so the roadmap's category name is correct.
- **Astral (uv, Ruff, ty) being acquired by OpenAI** — announced 19 March 2026, deal pending regulatory approval, tools to remain open source. uv is now the de-facto mainstream recommendation over pip/venv/poetry.
- **ty (formerly "red-knot") shipped to beta** (December 2025) with a 1.0 target in 2026 — but is still beta and not the sensible default for a beginner project.
- **Pydantic remains v2** (v2.13.x); **no v3 has shipped**. **FastAPI is still on the 0.x line** (0.136.1, April 2026) and now requires Python 3.10+ (3.8/3.9 dropped).
- **Docker Desktop's education free-tier narrowed** (Dec 2024 Subscription Service Agreement): free "personal" use for educational organizations is now limited to *enrolled students* for academic/non-profit work; faculty/staff need a paid license.
- **pytest is now major version 9.x** (a roadmap assuming pytest 7/8 is behind).

### Still valid / unchanged
CS50P, Exercism, GitHub Skills "Introduction to GitHub," Pro Git (2nd edition), mypy, Typer, HTTPX, Hypothesis, OWASP API Security Top 10 (2023), OWASP ASVS (5.0 line), SARIF 2.1.0 for GitHub code scanning, and OpenTelemetry are all live at their expected URLs.

## Details

### PYTHON FOUNDATIONS

| Resource | Current URL | Cost (student) | Size/structure | Est. hours | Enrolment mechanics | 2026 status notes |
|---|---|---|---|---|---|---|
| Helsinki Python MOOC 2026 | https://programming-26.mooc.fi/ | Free worldwide; ECTS credit registration also free | Parts 1–7 = Introduction to Programming (BSCS1001, 5 ECTS); Parts 8–14 = Advanced Course in Programming (BSCS1002, 5 ECTS); 14 parts total | ~250–300 h for full 10 ECTS | Open self-study; started 12 Jan 2026, material open to end of 2026. ECTS requires Open University of Helsinki registration **plus an online proctored-style programming exam** (final grade 50% exercises / 50% exam). International students with no Finnish personal identity code register via UH Admission Services | TMC (Test My Code): **in-browser editor for early parts, VS Code plugin for later parts**. Confirmed edition exists. NB: you can no longer earn a study right via these courses |
| Harvard CS50P | https://cs50.harvard.edu/python/ | Free audit + free Harvard certificate; edX verified cert $299 | ~9 lectures, problem sets, final project | ~10 weeks, 3–9 h/week | Self-paced, open enrolment; auto-graded (check50); free Harvard cert at ≥70% on each problem set and the final project | Stable; CS50 has been on edX since 2012 (not Coursera) |
| Exercism Python | https://exercism.org/tracks/python | 100% free ("100% free, forever") | **146 exercises across 17 concepts** | Self-paced | Open; automated code analysis; free volunteer human mentoring (rate-limited, reputation-gated) | New "Jiki" beginner platform now promoted for absolute beginners; count is 146 (not ~140) |
| The Python Tutorial | https://docs.python.org/3/tutorial/ | Free | Standard section numbering | Reference | N/A | Current stable **Python 3.14**; section numbering matches roadmap — 3–5 syntax/control flow/data structures, 4.9 functions, 6 modules, 7 I/O, 8 exceptions, 9 classes, 12 virtual environments |

**Helsinki MOOC — ECTS mechanics for a Croatian (non-Finnish) student, verified:** The course material is free and open to all. To have the 5+5 ECTS recorded you must register through the Open University of Helsinki; registration for this specific MOOC is free of charge (unlike some other Finnish MOOCs that charge an Open University fee). A Finnish personal identity code is *not* strictly required — international students without one contact UH Admission Services to register. Credits require both the TMC exercises **and** an online programming exam (not just exercises). You enrol for credit via your mooc.fi profile after the exam is graded.

**Helsinki MOOC 2026 upcoming exam dates:** Introduction to Programming — 18 Jul, 5 Sep, 27 Oct, 5 Dec 2026 (and 16 Jan 2027); Advanced Course — 15 Aug, 20 Oct, 15 Dec 2026 (and later). Each exam is a ~4-hour slot on the date. To sit an exam you need ≥25% of exercise points per part beforehand; to pass, ≥50% of exam points.

### HACK THE BOX ACADEMY

| Item | Detail (July 2026) |
|---|---|
| Student plan | **$96/year (~$8/month)** — "opens Tier I and II modules"; HTB Academy only |
| Silver Annual | $490/year; access to all modules up to and including Tier II; includes one exam voucher (CPTS / CWES / CDSA) valid 365 days, plus one extra CJCA voucher |
| Gold Annual | $1,260/year; Tier III access (93 modules); adds specialized paths (e.g. Senior Web Penetration Tester); one exam voucher |
| CPTS exam voucher (standalone) | **$210** (taxes included); includes **2 attempts** |
| Cube system | Still in use; sign-up grants 30 free Cubes; Tier 0 modules effectively free (10 Cubes, all refunded on completion); completing modules returns partial Cubes |
| Student eligibility & verification | Add institutional email as a *verified secondary* email; if the domain is already in HTB's database the Student plan unlocks instantly. Otherwise open a support ticket for domain validation (institution name, email, website, country). With no academic email, submit proof of enrolment (student ID with expiry/current year, registration/tuition receipt, or a signed enrolment letter). **No SheerID** is referenced in current HTB docs — verification is HTB's own support process |
| Croatian email | @unist.hr / @fesb.hr / @studenti.unist.hr should qualify if the domain is registered; if greyed out, a support ticket will validate it |

**CPTS "Penetration Tester" job-role path:** **28 modules** (~1,970 Cubes à la carte, ~450 Cubes returned on completion; also grants ~70% progress toward the Web Penetration Tester path). You must complete **100% of the path, including every module's hands-on skills assessment,** before you can sit the exam. Exam format: black-box enterprise environment (~8 machines, ~14 flags), **10 days of hands-on testing + 10 days to submit a professional pentest report**; passing is contingent on the report meeting professional standards, and results are released in batches. Recent learners (anecdotal — Medium/blog reviews, 2025–2026) consistently report a 3–6 month completion timeline at part-time study and emphasize not skipping modules. **Total realistic cost to CPTS via the Student plan: ~$242** (student subscription over 3–4 months + the $210 voucher).

*Named modules — general confirmation only.* HTB Academy still structures content as Paths → Modules → Sections under the Tier 0/I/II/III system. The named modules a 2025 roadmap cites — "Introduction to Python 3," "Linux Fundamentals," "Setting Up," "Web Requests," "Introduction to Web Applications," "Web Attacks," "Session Security," "API Attacks," "Security Monitoring & SIEM Fundamentals," and "Understanding Log Sources & Investigating with Splunk" — are consistent with the current catalog and tiering model. **Exact per-module section counts, hour estimates, and each module's precise tier sit behind the Academy login and were not individually verified this session** — confirm them on the module pages once subscribed rather than trusting a stale roadmap.

### SOFTWARE ENGINEERING TOOLING

| Resource | Current URL | Cost | Status/version (2026) | Notes |
|---|---|---|---|---|
| GitHub Skills "Introduction to GitHub" | https://github.com/skills/introduction-to-github | Free | Active | Completes in <1 hour; interactive via Issues + Actions; use a **public** repo to avoid consuming Actions minutes. GitHub Skills catalog expanded (Copilot, secure-code-game, agentic-workflows exercises) |
| Pro Git book | https://git-scm.com/book/en/v2 | Free online | 2nd edition | Chapters 1–3 = getting started, Git basics, branching |
| uv (Astral) | https://docs.astral.sh/uv/ | Free / OSS | Mainstream (0.11.x line in early 2026) | Now the default recommendation over pip/venv/poetry; drop-in pip replacement; 10–100× faster. Astral acquisition by OpenAI announced 19 Mar 2026 |
| Ruff (Astral) | https://docs.astral.sh/ruff/tutorial/ | Free / OSS | 0.15.x (0.15.22, 16 Jul 2026) | Linter + formatter; de-facto standard; replaces Black/Flake8/isort |
| ty (Astral type checker) | https://docs.astral.sh/ty/ | Free / OSS | **Beta** (1.0 targeted 2026) | Formerly "red-knot"; alternative to mypy/Pyright/Pylance; 10–100× faster but still beta |
| pytest | https://docs.pytest.org/ | Free / OSS | **Major version 9.x** | pytest 9 added a terminal progress feature (disabled by default on some terminals) |
| mypy vs Pyright vs ty | https://mypy.readthedocs.io/ | Free / OSS | mypy 1.20.x | **For a beginner SignalContract project in 2026, use mypy or Pyright** (mature, stable); treat ty as promising-but-beta and defer it until 1.0 |
| Typer | https://typer.tiangolo.com/tutorial/ | Free / OSS | Active | CLI framework; pair with the Python Packaging User Guide's command-line-tools guidance |
| Pydantic | https://docs.pydantic.dev/latest/ | Free / OSS | **v2 (v2.13.x); no v3 released** | Rust core (pydantic-core); v3 will be edge-case fixes, not an API rewrite — v2 model syntax will remain current |
| FastAPI | https://fastapi.tiangolo.com/tutorial/ | Free / OSS | 0.136.1 (Apr 2026) | Requires Python 3.10+; dropped 3.8/3.9; Pydantic v2 native; OpenAPI 3.1 output |
| HTTPX | https://www.python-httpx.org/ | Free / OSS | Active | Current version not freshly verified this session |
| Hypothesis | https://hypothesis.readthedocs.io/ | Free / OSS | Active | Property-based testing; status not freshly verified this session |
| Docker Desktop (Windows, student) | https://www.docker.com/ | Free for personal use / education (enrolled students) / small business | Paid tiers Pro $9, Team $15, Business $24 per user/mo (annual) | Free tier requires **<250 employees AND <$10M revenue**; since Dec 2024 SSA, educational free use is limited to *enrolled students* for academic use — which fits this learner. **Podman Desktop** (Apache 2.0, free at any scale, rootless) is the drop-in alternative |
| GitHub Actions free tier | https://github.com/ | Free | Public repos: effectively unlimited minutes; private repos: capped monthly minutes | Exact 2026 private-repo minute allowance not freshly verified — keep CI on a public repo for SignalContract to stay free |

### SECURITY REFERENCES

| Resource | Current URL | Status (2026) |
|---|---|---|
| OWASP Top 10 2025 | https://owasp.org/Top10/2025/ | **Final** (Jan 2026). List: A01 Broken Access Control (now absorbs SSRF); A02 Security Misconfiguration; **A03 Software Supply Chain Failures (new)**; A04 Cryptographic Failures; A05 Injection; A06 Insecure Design; A07 Authentication Failures; A08 Software & Data Integrity Failures; **A09 Security Logging & Alerting Failures (renamed)**; **A10 Mishandling of Exceptional Conditions (new)** |
| OWASP API Security Top 10 | https://owasp.org/API-Security/editions/2023/en/0x00-header/ | **2023 edition is current** (no newer edition); top item remains API1:2023 Broken Object Level Authorization |
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ | v5.0 line current (5.0 RC materials referenced on OWASP site); exact point release not freshly verified |
| OWASP Logging Cheat Sheet | https://cheatsheetseries.owasp.org/ | Active; exact cheat-sheet slug not freshly verified this session |
| OpenTelemetry | https://opentelemetry.io/ | **Logs are a stable signal in the OpenTelemetry specification.** Collector ~v0.157 (Jul 2026). Python: tracing/metrics stable; the Python `opentelemetry-instrumentation-logging` package is still **Beta** (verified on PyPI) |
| SARIF 2.1.0 / GitHub | https://docs.github.com/en/code-security/code-scanning | GitHub code scanning still **requires SARIF version 2.1.0** (a supported subset); uploadable via Actions, the code-scanning API, or CodeQL CLI |

**A09 URL flag:** the category *name* the roadmap cites is correct. Confirm the exact A09 page slug against the live index at owasp.org/Top10/2025/ (category pages live under that path); do not assume a hard-coded 2025 sub-path without checking, since the final release reorganized several entries.

### FREE / LOW-COST & CROATIAN CONTEXT

- **GitHub Student Developer Pack** (https://education.github.com/pack): free for verified students; a Croatian university email or an uploaded student document qualifies. High-value contents for this learner in 2026: full **JetBrains suite (PyCharm)**, **GitHub Pro**, **GitHub Copilot** student access (repackaged under a new student Copilot arrangement as of 12 March 2026 — free access continues but is managed differently), **$200 DigitalOcean credit**, **$100 Azure credit**, a free domain, and learning-platform trials. Copilot free access ends when student verification lapses.
- **TryHackMe** (https://tryhackme.com/): freemium. **Premium is $16.99/month or ~$126/year;** the **verified-student discount is 20% off annual → ~$100/year (~$8.33/month)**; a permanent free tier exists. A reasonable lower-cost complement or fallback to HTB Academy, with its own Jr Penetration Tester path.
- **Croatian resources (anecdotal community value, not structured courses):** **Split Tech City** (en.split-techcity.com) runs regular meetups, workshops and conferences, several hosted at **FESB**; **Python Hrvatska** (meetup.com/python-hrvatska) runs monthly Python meetups (mostly Zagreb, with a summer break); **Split Tech Mixer** socials run in Split. These are networking/learning supplements rather than graded coursework.

## Recommendations
1. **Weeks 1–6 — Python foundations (free):** Begin the **Helsinki MOOC Parts 1–7** (register with the Croatian university email; note the ECTS path needs the online exam, next Intro sittings 5 Sep / 27 Oct / 5 Dec 2026) and reinforce with **Exercism** (146 exercises). Add **CS50P** if you prefer lecture-driven learning. **Claim the GitHub Student Developer Pack now** (free PyCharm + Copilot). Stand up the SignalContract repo on **uv + Ruff + pytest 9** from day one.
2. **Weeks 4–8 — tooling for SignalContract:** Use **uv** (env/deps), **Ruff** (lint/format), **pytest** (tests) + **Hypothesis** (property tests), **Typer** (CLI), **Pydantic v2 + FastAPI 0.136 + HTTPX** (API/client), and **mypy or Pyright** for typing (defer **ty** until its 1.0). Target **Python 3.13 or 3.14** as the runtime. Wire **GitHub Actions** CI on a **public** repo (free minutes) and add **SARIF 2.1.0** upload for code scanning. Use **Docker Desktop** under the student free tier, or **Podman** if you want to avoid licensing questions entirely.
3. **Weeks 6+ — security + CPTS:** After verifying the university email, buy the **HTB Academy Student plan ($96/yr)** and start the **CPTS Penetration Tester path (28 modules)**. Budget the **$210 CPTS voucher** only when you are near 100% path completion (vouchers are 365-day, 2-attempt). Map SignalContract's logging/alerting design to **OWASP Top 10 2025 A09** and the **OWASP Logging Cheat Sheet**; adopt **OpenTelemetry** for structured logs but treat the Python logging SDK as **beta**. Reference **OWASP API Security Top 10 (2023)** and **ASVS 5.0** for the API surface.
4. **Thresholds that change the plan:** If HTB student verification stalls, subscribe to **TryHackMe's student annual (~$100/yr)** as a stopgap while HTB support validates your domain. If the CPTS timeline slips, hold the voucher purchase until the path hits 100%. If a proctored Helsinki exam date doesn't fit your August start, you can still complete all exercises free and sit a later 2026 exam — the material stays open to end-of-year 2026.

## Caveats
- Prices are in USD as published on vendor/third-party pages verified January–July 2026; EUR conversions are approximate (Croatia is in the eurozone). Verify live prices at checkout, since HTB and TryHackMe change pricing periodically and run seasonal discounts (~25% around Black Friday/year-end).
- **HTB per-module section counts, hour estimates, and the exact live Student-plan price sit behind the Academy login and were not individually verified** — confirm on the module/billing pages once subscribed rather than trusting a 2025 roadmap.
- HTTPX and Hypothesis exact versions, the GitHub Actions 2026 private-repo minute allowance, the OWASP ASVS point release, and the OWASP Logging Cheat Sheet exact URL were **not freshly verified** this session — check them directly before hard-coding into the schedule.
- Third-party pricing/review pages (HackerDNA, EthicalHacking.ai, Capterra) and Medium/Reddit/blog CPTS write-ups are **anecdotal**; where they agree with official HTB help-center pages (student plan mechanics, voucher terms, tiering) I have prioritized the official source, and the HTB Student Subscription and Academy Subscriptions help-center articles are the authoritative references used above.
- The Helsinki MOOC's exact final exercise-completion deadline for the specific January-2026 cohort should be reconfirmed on the live course page; the material itself remains open to the end of 2026.