# SignalContract: learning and build roadmap

This is the practical order of work. Do **not** try to learn all of Python, observability, Docker, and security engineering before writing code. Learn only the material needed for the next small release, build it, test it, and then continue.

Assumptions: **no previous tool-development experience**, 8–12 focused hours per week, Windows laptop with 16 GB RAM, and approximately 12 months available. The original 10–12 week prototype estimate assumed some basic programming comfort. Starting from zero, a credible first prototype is more likely to take **14–18 weeks**. That is not failure; it is a more honest plan.

## Read this first: what kind of roadmap this is

This document is a curriculum and sequencing guide. It does not try to replace the courses by teaching their code. For each skill it tells you:

1. why SignalContract needs the skill;
2. what exact concepts you need and what you may ignore;
3. which resource should be your main course;
4. which HTB module adds security context;
5. how many focused hours to budget;
6. how to study instead of only watching;
7. what evidence shows that you are ready to continue.

There are four kinds of resources in this roadmap:

- **Primary course:** complete it in order and do its exercises. Use only one primary Python course.
- **HTB security module:** complete the named module or sections for practical security context.
- **Reference documentation:** do not read it cover to cover. Search it when the roadmap tells you to use a particular feature.
- **Practice source:** use a limited number of exercises to test recall. Do not disappear into hundreds of unrelated exercises.

## Set up your learning notebook before Phase 0

Use two connected systems:

1. **Local Markdown notes in this repository are the permanent record.** They are searchable, versioned with Git, portable and remain yours if you stop using an AI product.
2. **NotebookLM is the study assistant.** Upload the roadmap and notes so it can quiz you, produce study guides and answer questions grounded in your material.

Do not keep the only copy of important notes inside a chat. Chat history is useful conversation, but it is not a well-organized learning record.

### Files and folders

This repository contains a starter structure under `learning-notes/`:

```text
learning-notes/
├── README.md                 # instructions and index
├── 00-baseline-and-goals.md  # complete before studying
├── 01-python/
├── 02-git-and-tooling/
├── 03-testing/
├── 04-http-and-apis/
├── 05-security-logging/
├── 06-data-models-and-cli/
├── 07-fastapi/
├── 08-opentelemetry/
├── 09-docker-and-ci/
├── 10-research-methods/
├── decisions.md              # important project choices and reasons
├── questions.md              # unresolved questions
├── weekly-review-template.md
└── lesson-note-template.md
```

Do not create one enormous unstructured file. Create one note for each meaningful lesson or study session, using names such as:

```text
learning-notes/01-python/2026-07-24-htb-functions.md
learning-notes/01-python/2026-07-26-helsinki-lists.md
learning-notes/04-http-and-apis/2026-09-03-http-status-codes.md
```

### Complete the baseline note first

Before opening the first course, complete `learning-notes/00-baseline-and-goals.md`. Record:

- why you want to build SignalContract;
- how many hours you can consistently study;
- your current ability with terminal, Git, Python, HTTP and testing;
- what “successful after three months” means;
- topics that currently confuse you;
- constraints such as university work and CPTS study;
- the date of your first monthly review.

This makes progress measurable. Do not write what you think you *should* know; write what you can currently do without help.

## How to take notes during every lesson

Copy `lesson-note-template.md` into the relevant subject folder. Complete it in this order:

1. **Before the lesson:** write its title, URL, section and two questions you expect it to answer.
2. **During the lesson:** use short bullets. Record concepts, not a transcript.
3. **After the lesson:** close the source and explain the main idea in your own words.
4. **Evidence:** describe the exercise you completed and what happened.
5. **Mistakes:** record the error, your incorrect assumption and the corrected mental model.
6. **Open questions:** move unresolved questions to `questions.md`.
7. **Next review:** schedule a short recall check for the next day and one week later.

A useful lesson note answers:

- What problem does this concept solve?
- How does it behave?
- When will SignalContract need it?
- What is one example I completed myself?
- What mistake did I make?
- Could I explain it without the source?

Avoid copying entire paragraphs or code listings from courses. The act of rewriting a concept is part of learning, and copying course material may also create copyright problems if the repository later becomes public.

## How to use NotebookLM with this roadmap

### Initial NotebookLM setup

1. Open NotebookLM in a desktop browser.
2. Create one notebook named `SignalContract Learning and Thesis`.
3. Upload `SIGNALCONTRACT-LEARNING-AND-BUILD-ROADMAP.md` as the first source.
4. Upload the thesis proposal, idea matrix and recommendation deck as supporting sources.
5. Add the course page you are **currently using** as a separate web source. Links written inside the roadmap are not automatically imported as complete webpages.
6. Add your current subject notes. Do not upload every future resource at once; inactive material makes answers less focused.

NotebookLM currently supports Markdown, DOCX, CSV, PPTX, PDF, copied text, Google Drive sources and web URLs. A locally uploaded file is a snapshot. If the local note changes, replace or re-upload that source. A Google Doc imported from Drive can be synchronized, so that is an alternative for a continuously updated learning journal.

### Recommended source organization

Keep these sources selected most of the time:

- the master roadmap;
- the notes for the current phase;
- the current primary-course webpage or exported material;
- one relevant official reference;
- the weekly review when preparing the next week.

Deselect the idea matrix, presentation and unrelated future-phase sources during ordinary Python study. NotebookLM can answer more precisely when only relevant sources are active.

### Adding your notes to NotebookLM

At the end of each study session:

1. Finish the local Markdown lesson note.
2. Commit it to Git with a message such as `notes: review Python functions`.
3. In NotebookLM, remove the older version of that lesson-note source if one exists.
4. Upload the updated Markdown file, or paste it as a new source with a clear title.
5. Ask NotebookLM to find misconceptions or missing explanations using the course source and your note.
6. Correct the local note yourself; then upload the corrected version.

Do not let NotebookLM silently rewrite the permanent note. Review suggested corrections and change the local Markdown source so Git retains the history.

If managing many individual files becomes inconvenient, maintain a Google Doc named `SignalContract Learning Journal`, import it from Drive and synchronize it. Still export or copy a backup into this repository at least monthly.

### NotebookLM prompts for the beginning

```text
Using the roadmap and my baseline note, create a realistic first-week schedule for 10 hours.
Use only Phase 0 and the beginning of the Python foundation.
Explain why each resource is included and do not introduce later topics.
```

```text
Read my baseline note. Ask me one diagnostic question at a time about terminal use,
Git and Python. At the end, map my gaps to the roadmap. Do not assume that confidence
means competence; ask for examples of things I can do unaided.
```

### NotebookLM prompts after a lesson

```text
Compare my lesson note with the selected course source.
Identify: (1) misconceptions, (2) important missing concepts,
(3) statements that are too vague, and (4) three recall questions.
Do not write code for me.
```

```text
Quiz me on this lesson one question at a time.
Require me to explain the concept in my own words and give an example.
Do not reveal the answer until I attempt it.
```

```text
Using my lesson note, create five flashcards.
Prefer why/when/failure questions over syntax memorization.
Mark any card whose answer is not directly supported by the selected sources.
```

### NotebookLM prompts for weekly review

```text
Using this week's lesson notes and the roadmap, produce a weekly review with:
completed objectives, concepts demonstrated, unresolved gaps, overdue recall items,
and the smallest next-week objective. Do not advance me based only on completed videos.
```

```text
Test the exit criteria for my current roadmap block.
Ask for evidence from my exercises and notes.
Return READY, NEEDS PRACTICE, or MISSING FOUNDATION with reasons.
```

### NotebookLM limitations to remember

- It can confidently produce an incorrect explanation; verify technical disputes against official documentation.
- A link inside an uploaded Markdown file is not the same as importing that webpage as a source.
- Uploaded local files do not automatically follow later Git changes.
- Generated flashcards and summaries are study aids, not proof of competence.
- Do not upload real credentials, personal data, employer data or sensitive HTB target information.
- NotebookLM should quiz and organize you; it should not decide that unreviewed generated code is correct.

## Review rhythm for notes throughout the project

### After every session — 5 to 10 minutes

- Finish the lesson note.
- Record one mistake and one unanswered question.
- Commit the note and any exercise.
- State the next smallest action.

### The following day — 10 minutes

Without opening the source, answer the note's recall questions. Mark each answer:

- `2 — can explain and apply`;
- `1 — recognize but cannot independently apply`;
- `0 — cannot recall`.

Restudy items scored 0. Create a new example for items scored 1. Do not spend time reviewing items repeatedly scored 2 unless they are used incorrectly later.

### Every week — 30 to 45 minutes

Copy `weekly-review-template.md`, summarize completed work, calculate actual study time, review unresolved questions and check the current exit gate. Upload that weekly review to NotebookLM and use the weekly-review prompt above.

### At the end of every phase — 60 to 90 minutes

Create a phase summary containing:

- concepts you can now explain;
- evidence you can produce;
- the most important mistakes and corrections;
- remaining gaps;
- resources completed and deliberately skipped;
- readiness-gate result;
- changes required to the next phase's schedule.

Then demonstrate the phase from a clean environment. Notes are not proof that the skill works; the demonstration and tests are the proof.

### During implementation

Continue lesson notes, but also update:

- `decisions.md` when choosing a library, schema rule or scope boundary;
- `questions.md` when a technical or research question is unresolved;
- the project issue tracker for actionable implementation work;
- code comments only when the code cannot clearly express the reason.

Do not use lesson notes as a substitute for issues, tests or documentation. Each has a different role.

## Important correction: the best Python route for a complete beginner

HTB Academy's Introduction to Python 3 is a good security-oriented beginning, but it is not by itself enough preparation for designing and maintaining a thesis-quality Python package. Use the following route.

### Step A — confidence-building introduction: HTB Academy (10–20 hours)

Complete [HTB Academy: Introduction to Python 3](https://academy.hackthebox.com/course/preview/introduction-to-python-3). It has 14 sections and covers variables, data structures, control flow, functions, classes, modules and libraries.

How to use it:

- Work in 60–90 minute sessions.
- Type every example instead of pasting it.
- After each section, close the lesson and recreate the important example from memory.
- Change at least two things in each example and predict the result before running it.
- Complete every exercise and the skills assessment.
- Keep a `python-learning` repository containing your rewritten exercises and one-sentence notes about mistakes.

Do not move on merely because every page is marked complete. You should be able to write a small function using a list and dictionary, read a file, import a module and explain an exception without reopening the lesson.

### Step B — real programming foundation: choose exactly one main course (70–130 hours)

**Recommended option: University of Helsinki Python Programming MOOC 2026.** Complete [Parts 1–7](https://programming-26.mooc.fi/) of Introduction to Programming, including the exercises. The university identifies Parts 1–7 as a full 5-ECTS introductory course. For a beginner studying 8–12 hours per week, reserve roughly 8–12 weeks. Then complete Part 8 (classes and objects); use Parts 9–10 selectively when the roadmap reaches object-oriented design and a larger application.

Why this is the recommendation: it is exercise-heavy, gives much more programming repetition than reading documentation, begins at zero, and progresses through modules and data processing—the parts directly relevant to SignalContract.

**Alternative: [Harvard CS50P](https://cs50.harvard.edu/python/).** Choose this instead if you learn substantially better from lectures. Complete the lectures and all required problem sets; watching videos without submitting problems does not count. Budget approximately 8–10 weeks at 8–12 hours per week.

Do **not** complete Helsinki and CS50P simultaneously. That creates duplicate lessons and delays the project. If the chosen course's explanation does not click, consult the equivalent lesson in the other course once, then return to the primary course.

### Step C — Python reference, not another course

Use [The Python Tutorial](https://docs.python.org/3/tutorial/) after you have seen a topic in the primary course. It is the authoritative language reference, but it is not the best first teacher for every beginner.

Read only these sections during the foundation:

- sections 3–5 for basic syntax, control flow and data structures;
- section 4.9 for functions;
- section 6 for modules and packages;
- section 7 for file input/output;
- section 8 for exceptions;
- section 9 for classes, after the primary course introduces them;
- section 12 for virtual environments and packages.

### Step D — limited practice

Use [Exercism's Python track](https://exercism.org/tracks/python) only for 15–25 beginner exercises spread across the course. Select exercises involving strings, collections, files and validation. Stop once you can solve ordinary problems without needing a video walkthrough. Competitive programming, algorithms puzzles and advanced mathematics are not prerequisites for v0.1.

### Python readiness checklist

You are ready to start the real v0.1 code only when all of these are true:

- You completed HTB Introduction to Python 3 and Parts 1–7 of Helsinki **or** all required CS50P work.
- You can use strings, numbers, booleans, lists, dictionaries, sets and tuples.
- You can write and call functions and explain parameters, return values and scope.
- You can split a program into modules and import them.
- You can read/write UTF-8 text and parse JSON.
- You can raise, catch and describe exceptions without hiding unexpected errors.
- You understand a class well enough to model an event, but you do not need advanced inheritance.
- You can create a virtual environment and install dependencies.
- You can debug a traceback from its final line upward.
- You can solve a small new problem without copying the structure of a tutorial.

If two or more items are false, spend another week on exercises. Do not compensate by asking an AI to generate the missing program; the purpose of this stage is to build your own ability to reason about it.

## Complete curriculum map: learn in this order

The times below are focused learning and practice estimates, not deadlines. They include exercises but not the later thesis experiment.

| Order | Knowledge area | Why it is needed | Main learning source | HTB source | Focused time | Stop/continue criterion |
|---:|---|---|---|---|---:|---|
| 1 | Terminal and files | Run tools, manage environments and understand paths | Linux Fundamentals or Microsoft command-line basics | Linux Fundamentals; Setting Up | 10–20 h | Navigate, create/move files, run programs, understand paths and environment variables |
| 2 | Git and GitHub | Preserve work and show professional development history | GitHub Skills + Pro Git chapters 1–3 | No dedicated HTB Git course is required | 6–10 h | Branch, commit, merge, resolve a simple conflict and open a PR without a video |
| 3 | Python foundations | Implement every core component | Helsinki Parts 1–7 or CS50P | Introduction to Python 3 | 80–150 h including HTB | Pass the Python checklist above |
| 4 | Python project practices | Make maintainable rather than one-file scripts | PyPA, `uv`, typing and Ruff documentation | None; this is software engineering | 15–25 h | Installable `src/` package with types, linting and a CLI entry point |
| 5 | Automated testing | Prove matcher correctness and prevent regressions | pytest docs; Hypothesis later | HTB exercises demonstrate practice, not unit-test design | 20–30 h initially | Independently test success, edge cases and expected failures |
| 6 | HTTP and REST APIs | Execute security scenarios | MDN HTTP + HTTPX documentation | Web Requests; Introduction to Web Applications | 20–30 h | Explain and generate requests, status codes, headers, JSON and timeouts |
| 7 | Application security scenarios | Define meaningful actions and expected denials | OWASP API Top 10 and ASVS | Web Attacks; Session Security; API Attacks later | 20–35 h | Write safe setup/action/cleanup and authorization expectation for eight scenarios |
| 8 | Security logging and privacy | Define what SignalContract must prove | OWASP Logging Cheat Sheet and A09 | Security Monitoring & SIEM Fundamentals | 20–30 h | Justify required fields, alert criteria and forbidden data for each scenario |
| 9 | Data modelling and schemas | Create a stable contract language | Pydantic + JSON Schema introduction | No HTB module is needed | 15–25 h | Validate versioned contracts and give clear errors |
| 10 | CLI design and packaging | Make the project usable by employers and CI | PyPA CLI guide + Typer | None | 12–20 h | A clean clone can install and run `--help`, `validate` and `verify` |
| 11 | FastAPI and local services | Build the first controlled fixture application | FastAPI tutorial | Web Requests knowledge is prerequisite | 20–35 h | Implement/test local endpoints and structured logs without following a full tutorial |
| 12 | Timing, correlation and safe cleanup | Avoid flaky or misleading verification | HTTPX, pytest fixtures, Python time documentation | SIEM use-case sections provide context | 15–25 h | Distinguish app, capture, timeout and verifier failures deterministically |
| 13 | OpenTelemetry | Accept a standard log pipeline | OTel logs specification, Python instrumentation and Collector quick start | Optional SIEM module reinforcement | 25–45 h | Explain app → SDK → Collector → receiver flow and run it locally |
| 14 | Docker Compose | Reproduce the demonstration | Docker Get Started and Compose tutorial | None required | 15–25 h | Rebuild and run the lab on a clean machine with documented commands |
| 15 | CI, JUnit and SARIF | Integrate with employer workflows | GitHub Actions docs, pytest JUnit and SARIF docs | None | 15–25 h | One internal result produces equivalent terminal/JSON/JUnit/SARIF reports |
| 16 | Mutation testing and experiments | Produce the thesis contribution | mutmut/PIT concepts plus research-method guidance | None | 30–50 h before experiments | Classify meaningful versus equivalent mutations and freeze an evaluation plan |
| 17 | Basic statistics and reproducibility | Defend conclusions honestly | SciPy/Jupyter tutorials and supervisor guidance | None | 20–40 h | Calculate and explain chosen metrics without overstating results |
| 18 | Minimal JavaScript/Express | Provide a second implementation ecosystem | MDN JavaScript guide + Express starter | Secure Coding 101: JavaScript is optional | 25–45 h | Recreate equivalent scenarios; do not attempt frontend development |

This totals several hundred hours because the outcome is both a software project and a research project. At 8–12 hours per week over a year, it is feasible only if optional topics remain optional and the v0.1 scope stays small.

## How to learn each kind of subject

### For programming courses

Use a **learn → recall → modify → apply** cycle:

1. Study one short lesson.
2. Type its example.
3. Close the material and recreate the idea from memory.
4. Modify the example so that it handles a different input or failure.
5. The following day, solve one small related problem without notes.
6. At the end of the week, use the concept in a tiny SignalContract-related exercise.

A two-hour session should usually contain no more than 45–60 minutes of video/reading. The remainder should be keyboard work and debugging.

### For documentation

Documentation is a reference, not a course. First write a one-sentence question such as “How does pytest supply temporary files?” Then find the relevant official page, run the smallest example, change it and record the answer. Do not read hundreds of API pages in advance.

### For HTB modules

Before starting, write three questions the module should answer. During the module, keep notes under `concept`, `example`, `SignalContract relevance` and `remaining question`. Complete the exercises yourself. After the module, create a one-page mapping from what you learned to the tool—for example, `failed login → expected application event → possible alert`.

### For books and long references

Read only assigned chapters. Pro Git chapters 1–3 are needed early; the rest is reference material. OWASP ASVS is a requirements catalogue, not a book to memorize. The OpenTelemetry specification should be read selectively only when v0.4 begins.

## Weekly schedule for 8–12 hours

Use four or five sessions instead of one weekend marathon:

| Session | Activity | Typical time |
|---|---|---:|
| 1 | Primary course lesson and exercises | 2 h |
| 2 | Continue exercises; redo one item from memory | 2 h |
| 3 | HTB module or official security reading | 1.5–2 h |
| 4 | Small project-related exercise using this week's concepts | 2–3 h |
| 5 | Tests, Git commits, dev log and review | 1–2 h |

At the end of every week, record:

- hours actually spent;
- lessons/exercises completed;
- three concepts you can explain without notes;
- one thing you still cannot do;
- one working artifact or test;
- the next smallest task.

If you study for ten hours but produce no exercise, test, note or working artifact, count that as passive exposure—not a completed week.

## Tool setup curriculum—not just an installation list

Learn setup in this order:

1. **Files and terminal:** use HTB Linux Fundamentals until paths, current directory, file operations, processes and permissions make sense. On Windows, use PowerShell locally but learn basic Linux shell because containers and most security labs use Linux.
2. **Editor:** learn only opening a folder, integrated terminal, Python interpreter selection, search, rename, debugger breakpoints and source control view. Do not spend days customizing VS Code.
3. **Python environment:** learn why projects isolate dependencies, then practice creating/deleting/recreating a virtual environment. Use `uv` or `venv`, not global package installation.
4. **Git locally:** learn working tree, staging area, commit and branch. Make ten small commits in the learning repository.
5. **GitHub:** complete [Introduction to GitHub](https://github.com/skills/introduction-to-github), which is designed to take under an hour and covers branches, commits, pull requests and merges. Then repeat that workflow in your own repository.
6. **Quality commands:** only after Python basics, add pytest, Ruff and a type checker. Understand what each checks before enabling many rules.
7. **Docker:** install it early to confirm the laptop supports it, but postpone learning it until the offline CLI works.

Setup is complete when you can delete your local learning repository, clone it again, recreate its environment from documented commands and run its tests. Do this destructive rehearsal only with the disposable learning repository—not with important work.

## Exact concepts to learn—and concepts to postpone

### Python: required before v0.1

Required: values and types; collections; conditions and loops; functions; modules; file handling; JSON; exceptions; classes/dataclasses; type hints; paths; basic iterators; dependency environments; unit testing.

Postpone: metaclasses, descriptors, advanced decorators, multiprocessing, GUI programming, data science libraries, machine learning, clever one-liners and deep inheritance hierarchies.

### Software engineering: required during v0.1

Required: separation of concerns; small functions; immutable input/result thinking; explicit errors; deterministic output; dependency pinning; semantic versioning; changelog; code review; tests near behavior.

Postpone: microservices, distributed systems, Kubernetes, elaborate design-pattern catalogues and performance optimization without measurements.

### Web: required before v0.2

Required: HTTP request/response; methods and status codes; headers; JSON; cookies and bearer tokens conceptually; REST; authentication versus authorization; timeouts; retries; idempotency; correlation IDs; local server/client model.

Postpone: browser frontend frameworks, WebSockets, GraphQL, HTTP/3 internals and production reverse-proxy administration.

### Logging: required before security assertions

Required: structured events; timestamps; severity; actor/action/target/outcome/reason; correlation; sensitive-data minimization; CR/LF injection; event versus alert; delivery deadline; missing/duplicate/reordered events.

Postpone: becoming an Elastic/Splunk administrator, enterprise retention engineering and proprietary SIEM integrations.

### Research: required before mutation experiments

Required: research question; hypotheses; baselines; ground truth; precision/recall/false-positive rate; mutation score; equivalent mutants; repeated runs; threats to validity; reproducible environment.

Postpone: advanced statistics until the supervisor confirms which tests the experiment actually needs.

## When to use AI assistance

Use AI to explain error messages, quiz you, review code you wrote, compare two approaches and identify missing tests. Do not use it to generate an entire milestone that you cannot explain. A good rule is: never merge code until you can explain its control flow, data model, failure behavior and tests without the conversation that produced it.

## Monthly mentor/self-assessment checkpoint

Every four weeks, demonstrate the current artifact from a clean terminal and answer:

1. What did I learn rather than merely use?
2. Which part can I rebuild without notes?
3. What failure cases do my tests cover?
4. What did I deliberately postpone?
5. Does the next topic directly unlock the next milestone?
6. Is the 8–12 hour schedule sustainable?

If the answer to question 5 is no, do not begin that topic. If a learning block takes twice its estimate, reduce project scope rather than skipping the foundation.

## The rule for every week

Use roughly:

- 35% guided learning and note-taking;
- 45% writing SignalContract or a small preparatory exercise;
- 15% automated tests and debugging;
- 5% README/dev-log updates.

For every resource, type the examples yourself. A topic is “learned enough” when you can produce the weekly deliverable without copying a tutorial.

## Phase 0 — prepare the environment (2–3 days)

### Install

1. Python 3.12 or newer.
2. Git and a GitHub account.
3. VS Code with the Python and Ruff extensions, or PyCharm Community.
4. Docker Desktop, but do not use Docker in the first implementation.
5. `uv` or Python's built-in `venv` for isolated environments.

Learn how to create a folder, virtual environment, install a package, run a Python file, run `pytest`, make a Git commit, create a branch, and open a pull request.

Resources:

- HTB Academy: [Linux Fundamentals](https://academy.hackthebox.com/course/preview/linux-fundamentals) — terminal, files, permissions and processes. Do this if shell usage is not comfortable.
- HTB Academy: [Setting Up](https://academy.hackthebox.com/course/preview/setting-up) — useful workstation preparation.
- [Python setup and usage](https://docs.python.org/3/using/index.html)
- [GitHub Skills: Introduction to GitHub](https://github.com/skills/introduction-to-github)
- [Pro Git, chapters 1–3](https://git-scm.com/book/en/v2)
- [uv installation and first project](https://docs.astral.sh/uv/getting-started/)

Deliverable: a private `signalcontract-lab` repository containing `README.md`, `.gitignore`, `pyproject.toml`, `src/`, `tests/`, and one passing test. Do not publish the main project until its name, licence and scope are reviewed.

## Phase 1 — learn enough Python to build a CLI (weeks 1–4)

### Week 1: values, control flow and files

Learn strings, integers, booleans, lists, dictionaries, `if`, loops, functions, exceptions, `pathlib`, and reading UTF-8 text files.

- HTB Academy: [Introduction to Python 3](https://academy.hackthebox.com/course/preview/introduction-to-python-3) — complete through functions and libraries; ideally complete the whole module.
- Primary reference: [The Python Tutorial](https://docs.python.org/3/tutorial/)
- Extra practice: [Exercism Python track](https://exercism.org/tracks/python) — do 10–15 easy exercises, not the entire track.

Build exercise: read a `.jsonl` file, parse each line with `json.loads`, and print the `event_type`. Bad JSON must produce a clear line-numbered error.

Exit gate: you can explain the difference between a list and dictionary, write a function, handle an exception, and read a file without a tutorial.

### Week 2: modules, classes and type hints

Learn imports, packages, dataclasses, enums, type hints, `None`, iterators, and separating parsing from business logic.

- [Python modules](https://docs.python.org/3/tutorial/modules.html)
- [Python typing](https://docs.python.org/3/library/typing.html)
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [mypy getting started](https://mypy.readthedocs.io/en/stable/getting_started.html)

Build exercise: create `SecurityEvent`, `Contract`, and `VerificationResult` models. Convert JSON dictionaries into models and reject missing required data.

Exit gate: `mypy` or Pyright finds no errors in the exercise, and parsing code does not contain CLI printing.

### Week 3: testing

Learn arrange/act/assert, fixtures, parametrization, temporary files, exception assertions, and coverage. Then learn property-based testing only after ordinary unit tests are comfortable.

- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [Hypothesis introduction](https://hypothesis.readthedocs.io/en/latest/quickstart.html)

Build exercise: tests for empty files, malformed JSON, missing fields, Unicode, duplicate events and very long values. Aim for meaningful branch coverage, not a vanity percentage.

Exit gate: `pytest` passes from a clean clone and tests do not depend on execution order.

### Week 4: CLI and packaging

Learn command-line arguments, exit codes, stdout versus stderr, package layout, dependency groups and semantic versioning.

- [Python Packaging: creating command-line tools](https://packaging.python.org/en/latest/guides/creating-command-line-tools/)
- [Typer tutorial](https://typer.tiangolo.com/tutorial/)
- [Python packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)

Build exercise: `signalcontract validate example.yml` loads a contract and returns exit code 0 or a useful validation error. Add `--version` and `--help`.

Exit gate: another person can clone the repository, install it, run the CLI and see one passing and one failing example.

## Phase 2 — learn the web and security-event problem (weeks 5–7)

### Week 5: HTTP and APIs

Learn URLs, methods, status codes, headers, JSON bodies, authentication headers, timeouts, redirects and the difference between a transport failure and application failure.

- HTB Academy: [Web Requests](https://academy.hackthebox.com/course/preview/web-requests) — the most directly relevant HTB module.
- HTB Academy: [Introduction to Web Applications](https://academy.hackthebox.com/course/preview/introduction-to-web-applications)
- [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [HTTPX quickstart](https://www.python-httpx.org/quickstart/)

Build exercise: a script sends requests to a local test server, records start/end time, status, body and correlation ID, and distinguishes timeout, connection and HTTP errors.

Exit gate: you can explain why `401`, `403`, `404`, `429` and `500` are different and why a `200` response does not prove correct security logging.

### Week 6: web-security scenarios

Learn authentication failure, authorization denial, IDOR/BOLA, cross-tenant access, validation failure, log injection and secure cleanup. Learn these to design safe test scenarios—not to scan strangers' systems.

- HTB Academy: [Web Attacks](https://academy.hackthebox.com/course/preview/web-attacks/introduction-to-web-attacks) — especially IDOR and HTTP verb behavior.
- HTB Academy: [Session Security](https://academy.hackthebox.com/course/preview/session-security)
- Optional later: [API Attacks](https://academy.hackthebox.com/course/preview/api-attacks)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [OWASP ASVS](https://github.com/OWASP/ASVS)

Build exercise: write eight scenario descriptions before implementing a runner: login success/failure, denied object access, denied admin action, cross-tenant attempt, high-value transaction, invalid input, dependency failure and log-injection attempt.

Exit gate: every scenario states setup, action, expected HTTP result, expected event, cleanup and authorization boundary.

### Week 7: security logging and privacy

Learn what should be logged, event semantics, actor/action/target/outcome/reason, correlation identifiers, timestamps, sensitive-data exclusion, CR/LF injection and alerting.

- HTB Academy: [Security Monitoring & SIEM Fundamentals](https://academy.hackthebox.com/course/preview/security-monitoring--siem-fundamentals) — complete the SIEM definition and use-case-development sections first.
- Optional HTB follow-up: [Understanding Log Sources & Investigating with Splunk](https://academy.hackthebox.com/course/preview/understanding-log-sources--investigating-with-splunk)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OWASP A09:2025](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/)
- [OpenTelemetry guidance for sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/)

Build exercise: design 10 good and 10 deliberately bad JSONL events. Bad variants should include a missing actor, wrong outcome, broken correlation, raw token, email canary and newline injection.

Exit gate: you can justify every required and forbidden field using a scenario or published guidance.

## Phase 3 — build SignalContract v0.1 (weeks 8–12)

Use this initial structure:

```text
signalcontract/
├── pyproject.toml
├── README.md
├── src/signalcontract/
│   ├── cli.py
│   ├── contract.py
│   ├── events.py
│   ├── matcher.py
│   ├── privacy.py
│   ├── results.py
│   └── errors.py
├── tests/
│   ├── unit/
│   └── fixtures/
├── examples/
└── docs/
```

### Week 8: contract schema

Define version `0.1` with only: contract ID, expected event type, time window, required fields, exact assertions, absent-field assertions and forbidden canary strings.

- [JSON Schema tutorial](https://json-schema.org/learn/getting-started-step-by-step)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)

Do not add regex, wildcards, HTTP scenarios or OpenTelemetry yet.

### Week 9: JSONL event ingestion

Implement streaming input, source line numbers, timestamp normalization, input-size limits and separate parse/validation errors. Never silently skip malformed events.

Tests: empty, malformed, missing, duplicate, reordered, non-UTF-8 and oversized inputs.

### Week 10: deterministic matching

Implement candidate selection and exact/absent/membership checks. Define how zero, one and multiple matching events behave. Sort diagnostics so repeated runs are byte-for-byte stable.

Tests: missing event, ambiguous match, wrong actor/action/target/outcome/reason, broken correlation and events outside the time window.

### Week 11: privacy assertions and diagnostics

Implement synthetic token/PII canaries, control-character detection and allow-list/redaction rules. A failure must say: contract, assertion, expected value, safe observed summary and source line—without echoing secrets.

### Week 12: release v0.1

Implement:

```text
signalcontract validate CONTRACT
signalcontract verify CONTRACT --events EVENTS.jsonl
```

Add CI for Python versions, Ruff, type checking and pytest. Publish example contracts, a two-minute terminal demo and architecture/limitations documentation.

- [Ruff tutorial](https://docs.astral.sh/ruff/tutorial/)
- [GitHub Actions: build and test Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

**v0.1 acceptance gate:** from a clean clone, one command installs the package; the examples demonstrate pass, missing event, wrong semantics and leaked canary; output is deterministic; no network, Docker, SIEM or real data is required. If this is not working after 12 weeks, keep the thesis focused on the offline verifier and ask the mentor to reduce scope.

## Phase 4 — v0.2 HTTP scenario runner (months 4–5)

1. Learn FastAPI and create a tiny reference application.
2. Implement setup → action → cleanup with strict base-URL allow-listing.
3. Generate a unique correlation ID per run.
4. Capture local JSONL logs.
5. Separate scenario failure, application failure, capture failure and verification failure.

Resources:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [HTTPX advanced clients](https://www.python-httpx.org/advanced/clients/)
- [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

Acceptance gate: `docker compose up` is **not** required yet. A local FastAPI app demonstrates all eight scenarios, and cleanup runs safely even when an assertion fails.

## Phase 5 — v0.3 advanced assertions and alerts (month 6)

Add wildcard/regex assertions only with limits, cross-event correlation, duplicate/reordering policy, deadline-aware matching, and a local mock webhook for alert delivery.

Learn:

- [Python regular expressions](https://docs.python.org/3/howto/regex.html)
- [FastAPI background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

Acceptance gate: automated tests cover delayed/suppressed alerts, ambiguous events, webhook failure, injection and redaction. Tests use a controllable clock where possible instead of real sleeping.

## Phase 6 — v0.4 interoperability (month 7)

Only now learn OpenTelemetry. Understand the data model and Collector pipeline before writing an adapter.

- [OpenTelemetry logs specification](https://opentelemetry.io/docs/specs/otel/logs/)
- [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/languages/python/instrumentation/)
- [OpenTelemetry Collector quick start](https://opentelemetry.io/docs/collector/quick-start/)
- [JUnit XML output in pytest](https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files)
- [SARIF 2.1.0 standard](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [GitHub SARIF support](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)

Implement JSON, JUnit, SARIF and Markdown reporters from one internal result model. Add a local Collector input without removing JSONL support.

Acceptance gate: every format reports the same failure identifiers and severity, and the entire demo remains local.

## Phase 7 — mutation engine and second fixture (month 8)

Learn mutation-testing principles, but implement deterministic event/logging mutations rather than arbitrary Python source rewriting.

- [Mutation testing overview and terminology](https://pitest.org/quickstart/mutators/)
- [mutmut documentation](https://mutmut.readthedocs.io/)
- [Express getting started](https://expressjs.com/en/starter/installing.html)
- [Node.js test runner](https://nodejs.org/api/test.html)

Implement deletion, missing field, semantic substitution, broken correlation, delay/suppression, canary/control character, duplicate/reorder and sink-unavailable mutations. Record seed, mutation ID and expected classification.

Acceptance gate: at least 20 manually reviewed non-equivalent mutations work on FastAPI and Express before expanding to 60.

## Phase 8 — reproducible experiment (months 9–10)

Freeze the contract corpus before comparing:

1. HTTP assertions only.
2. Event presence only.
3. JSON Schema only.
4. Full SignalContract.

Measure mutant kill rate, precision, recall, false-positive rate, runtime, memory, writing effort and diagnostic localization. Mark equivalent/doubtful mutations separately.

- [Docker getting started](https://docs.docker.com/get-started/)
- [Docker Compose introduction](https://docs.docker.com/compose/gettingstarted/)
- [SciPy statistical tests](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Jupyter documentation](https://docs.jupyter.org/en/latest/)
- [ACM artifact review and badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)

Acceptance gate: a clean machine can reproduce tables from pinned inputs with one documented command, and repeated runs produce explainable variance.

## Phase 9 — thesis and public release (months 10–12)

1. Conduct 5–10 practitioner interviews only after mentor/ethics guidance.
2. Ask external testers to follow the installation guide without live help.
3. Publish threat model, limitations, SECURITY.md, CONTRIBUTING.md, code of conduct and support policy.
4. Pin dependencies and container images; archive the evaluation corpus and results.
5. Release v1.0, demonstration video, technical article and defense deck.

- [GitHub: setting up a project for healthy contributions](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [OpenSSF Scorecard](https://scorecard.dev/)
- [Python security considerations](https://docs.python.org/3/library/security_warnings.html)
- [Zenodo GitHub integration](https://help.zenodo.org/docs/github/)

## What not to learn yet

Do not delay v0.1 to learn Kubernetes, Elastic/Splunk administration, malware analysis, Active Directory internals, frontend frameworks, LLM APIs, cloud IAM or production SIEM integrations. They are interesting but do not unblock the offline verifier.

## Recommended first seven days

1. Create the private lab repository and Python virtual environment.
2. Begin HTB's **Introduction to Python 3** and type every example.
3. Complete Python Tutorial sections 3–5.
4. Write the 20-line JSONL reader exercise.
5. Add five pytest cases for that reader.
6. Commit each working step with a clear message.
7. Write a one-page dev log: what you learned, what broke, and the exact next task.

Your first target is not “build SignalContract.” It is: **by the end of week 4, produce a small installable Python CLI with tests; by week 12, make that CLI reliably prove four kinds of JSONL security-event failure.**
