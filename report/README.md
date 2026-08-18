# Project Report — Kaime

**The deliverable is [`Kaime_Project_Report.docx`](Kaime_Project_Report.docx)** — a
complete five-chapter KTU Computer Science project report, formatted to the
departmental guidelines and with all nine design diagrams embedded.

## What is in the document

| Section | Contents |
|---|---|
| Preliminaries (roman numerals) | Title page, Declaration, Certification, Acknowledgements, Abstract (298 words), auto Table of Contents, List of Figures, List of Tables |
| Chapter One | Background, problem statement, aim, 5 objectives, 4 research questions, significance, scope, limitations, organisation |
| Chapter Two | Conceptual review, existing systems, related technologies, methods and models, 4 identified gaps, summary |
| Chapter Three | Design Science methodology, 27 functional + 10 non-functional requirements, 14 user stories, tools, architecture, use cases, ERD, class/sequence/activity/state diagrams, 6 pseudocode algorithms, data description, testing plan, ethics |
| Chapter Four | Development environment, database implementation, 11 modules, interface design, 6 annotated code listings, 82 test cases, results tables, performance tables, evaluation |
| Chapter Five | Findings, interpretation, objectives assessment, comparison table, advantages, challenges, implications, contribution, conclusion, 9 recommendations |
| References | 20 verified APA 7th entries |
| Appendices | A source code, B API endpoints, C configuration, D work plan, E test evidence, F user manual |

Roughly 96 pages before you add screenshots.

## READ THIS FIRST — four things you must do

### 1. The 20% AI-content rule

The guidelines cap AI-generated content at 20% and require you to *explain and defend
every part of the work*. This draft was produced with AI assistance, so **you cannot
submit it as-is**. Work through it in this order:

- **Safe with light editing** — Chapters Three and Four. These describe *your own code*:
  your tables, your service boundaries, your grade scale, your conflict rules. The facts
  are yours; only the sentences came from a draft. Rewrite in your own voice anyway —
  detectors flag phrasing, not facts.
- **Rewrite substantially** — Chapters One, Two and Five. These are argument and prose.
  Rewrite paragraph by paragraph from the ideas, not by paraphrasing the sentences.
- **Replace yourself** — every `[SOURCE NEEDED]` marker. See below.

Run the department's similarity and AI checkers *before* the deadline, not on the day.

### 2. Citations — no sources were invented for you

The reference list contains **real, checkable works** (Fowler, Fielding, Hevner,
Peffers, Chen, Codd, Helland, Sommerville, Pressman, Evans, Beck et al., plus official
FastAPI/React/PostgreSQL/APScheduler documentation). Verify each against the actual
publication and drop any you have not read enough of to defend in the viva.

Six places in the text carry a **`[SOURCE NEEDED]`** marker instead of a citation —
every point where the text makes an empirical claim about institutional practice in
Ghana or West Africa (fragmented record-keeping, students missing deadlines,
communication channels, open-source SIS evaluations, mobile vs. email reach).
**Do not guess a citation to fill these.** A fabricated reference is misconduct and is
trivially caught. Find real sources in Google Scholar, AJOL, ResearchGate or the
university library, or soften the claim until it needs no source. A note in the
References section lists exactly what to look for — delete that note before submitting.

### 3. Placeholders to fill in

Search the document for `<<` and for `[FILL IN]`:

- `<<Your name>>`, `<<Student number>>`, `<<Your programme of study>>`, `<<Month, Year>>`
- `<<Supervisor's name>>`, `<<Head of Department's name>>`
- Table 4.1 — your machine's processor, RAM, storage, browser
- **Every `[FILL IN]` in the test-result and performance tables — run the tests and
  record what actually happened.** Do not copy the Expected column into the Result
  column. The report explicitly says that a run in which nothing ever failed invites the
  question of whether the tests could fail; if you found and fixed defects, say so.
- Appendix D — the months of your work plan, plus a Gantt chart image
- 20 screenshot placeholders in Section 4.6, marked `[ INSERT SCREENSHOT HERE ]`

Three yellow-shaded italic **author notes** are embedded in the References and
Appendices. Delete them before submitting.

### 4. Update the automatic fields in Word

The Table of Contents, List of Figures and List of Tables are live Word fields and
currently show placeholder text. Open the document and press **Ctrl+A then F9**, or
right-click each and choose *Update Field*, then choose "update entire table". Do this
**last**, after all your edits, so the page numbers are correct.

## Formatting already applied

Times New Roman 12 pt · 1.5 line spacing · justified body · centred bold major headings ·
left-aligned bold numbered sub-headings, max three levels · chapter page breaks ·
roman numerals for preliminaries, arabic from Chapter One · repeating table header rows ·
consistent figure and table captions.

Check it opens correctly in Word before you rely on it; it was verified through
LibreOffice.

## Regenerating the document

The `.docx` is generated from the Python sources here, so edits to content can be
re-rendered rather than re-typed:

```bash
uv run --with python-docx python report/build_docx.py
```

| File | Contents |
|---|---|
| `build_docx.py` | Formatting engine: styles, sections, page numbering, tables, figures |
| `content_front.py` | Title page, declaration, acknowledgements, abstract |
| `content_ch12.py` | Chapters One and Two |
| `content_ch3.py` | Chapter Three |
| `content_ch4.py` | Chapter Four |
| `content_ch5.py` | Chapter Five |
| `content_back.py` | References and appendices |
| `diagrams/*.mmd` | Mermaid source for the nine figures |
| `diagrams/png/` | Rendered figures embedded in the document |

Once you start editing in Word, stop regenerating — you would overwrite your edits.

## Regenerating the diagrams

```bash
npm install @mermaid-js/mermaid-cli
cd report/diagrams
for f in *.mmd; do
  npx mmdc -i "$f" -o "png/${f%.mmd}.png" -b white -s 2 -w 1700 -c mermaid-config.json
done
```

The `-w 1700` and the `wrappingWidth` in `mermaid-config.json` matter: without them the
flowcharts render as narrow columns too tall to fit a page.
