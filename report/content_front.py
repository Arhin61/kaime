"""Preliminary pages: title, declaration, certification, acknowledgements, abstract."""

TITLE_PAGE = [
    ("title_big", "KUMASI TECHNICAL UNIVERSITY"),
    ("title_mid", "FACULTY OF APPLIED SCIENCES AND TECHNOLOGY"),
    ("title_mid", "COMPUTER SCIENCE DEPARTMENT"),
    ("spacer", 3),
    ("title_topic", "DESIGN AND IMPLEMENTATION OF AN INTEGRATED SCHOOL "
                    "MANAGEMENT AND AUTOMATED NOTIFICATION SYSTEM"),
    ("spacer", 3),
    ("title_mid", "A PROJECT SUBMITTED TO THE COMPUTER SCIENCE DEPARTMENT"),
    ("title_mid", "IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR THE AWARD"),
    ("title_mid_bold_tail", ("OF ", "<<YOUR PROGRAMME OF STUDY>>")),
    ("spacer", 3),
    ("title_bold", "<<Your name (First name, middle name and Surname)>>"),
    ("title_bold", "(<<Student number>>)"),
    ("spacer", 3),
    ("title_bold", "<<MONTH, YEAR>>"),
]

DECLARATION = [
    ("h1", "DECLARATION"),
    ("p", "I hereby declare that this project report is the result of my own original "
          "effort, carried out under the supervision of <<Supervisor's name>> in the "
          "Computer Science Department, Kumasi Technical University. All sources of "
          "information consulted in the course of this work have been duly acknowledged "
          "and referenced in accordance with the American Psychological Association "
          "(APA, 7th edition) style. To the best of my knowledge, this work has not "
          "been submitted, either in whole or in part, for the award of any other "
          "degree, diploma or qualification in this or any other institution."),
    ("spacer", 1),
    ("p_left", "Where artificial-intelligence tools were used in the preparation of this "
               "report, their use was limited to drafting assistance and language "
               "refinement; the design decisions, the implemented system and the "
               "conclusions drawn are my own, and I am able to explain and defend every "
               "part of this work."),
    ("spacer", 2),
    ("sig", "<<Your name (First name, middle name and Surname)>>", "Student"),
    ("spacer", 2),
    ("h1", "CERTIFICATION"),
    ("p", "I hereby certify that this project report was prepared by the above-named "
          "student under my supervision, in accordance with the guidelines for the "
          "writing of undergraduate project reports laid down by the Computer Science "
          "Department, Kumasi Technical University. I confirm that the work meets the "
          "required academic standards and I approve it for submission."),
    ("spacer", 2),
    ("sig", "<<Supervisor's name>>", "Project Supervisor"),
    ("spacer", 2),
    ("sig", "<<Head of Department's name>>", "Head of Department"),
]

ACKNOWLEDGEMENTS = [
    ("h1", "ACKNOWLEDGEMENTS"),
    ("p", "My first and deepest gratitude goes to the Almighty God, whose grace and "
          "provision sustained me throughout the period of this project."),
    ("p", "I am profoundly grateful to my supervisor, <<Supervisor's name>>, for the "
          "patience, technical insight and steady direction offered at every stage of "
          "this work. The critiques offered during our review sessions shaped both the "
          "architecture of the system and the argument of this report, and any clarity "
          "the reader finds in the pages that follow owes a great deal to that guidance."),
    ("p", "I acknowledge the Head of Department, <<Head of Department's name>>, and the "
          "entire teaching staff of the Computer Science Department, Kumasi Technical "
          "University, whose instruction over the course of my programme furnished the "
          "foundation on which this project was built. I am grateful in particular to "
          "the lecturers of the database systems, software engineering and web "
          "technologies courses, whose material I drew on directly."),
    ("p", "I thank the administrative and academic staff who gave their time to discuss "
          "how student records, class registers, results and fees are handled in "
          "practice. Their candour about where the existing manual processes break down "
          "gave this project its problem statement and kept its requirements honest."),
    ("p", "Finally, I thank my family for their unfailing material and moral support, "
          "and my colleagues in the department for the many hours of discussion, "
          "testing and encouragement. Whatever shortcomings remain in this work are "
          "entirely my own."),
]

ABSTRACT = [
    ("h1", "ABSTRACT"),
    ("p", "Tertiary institutions maintain student records, course registrations, class "
          "registers, examination results and fee accounts as loosely coupled "
          "activities supported by paper registers, spreadsheets and ad-hoc messaging. "
          "The resulting fragmentation produces duplicated data entry, inconsistent "
          "results computation, avoidable billing errors, and students who miss "
          "registration and examination deadlines because announcements reach them too "
          "late. This project addressed that fragmentation by designing and implementing "
          "Kaime, an integrated web-based school management and automated notification "
          "system. The work followed a Design Science Research approach executed through "
          "iterative and incremental development, in which requirements elicited from "
          "institutional practice were translated into a domain model and realised as a "
          "working artefact evaluated against those requirements. The system comprises a "
          "React and TypeScript single-page dashboard, a Python FastAPI server organised "
          "into router, service and repository layers, and a PostgreSQL database of "
          "fifteen tables under Alembic migrations. Every academic operation is scoped "
          "to an academic term, so a course may be run, graded and billed independently "
          "each semester. Domain invariants are enforced in the service layer and "
          "reinforced by database constraints: assessment weights may not exceed one "
          "hundred percent per course-term, a room may not be double-booked, records "
          "with live dependants may not be deleted, invoices may not be overpaid, and "
          "repeated billing or register marking updates rather than duplicates existing "
          "rows. An APScheduler background job evaluates configurable day offsets before "
          "each event, renders a Jinja2 template, and writes a dispatch record whose "
          "unique constraint guarantees that no subscriber is notified twice for the "
          "same event and offset. Testing across the modules confirmed that the system "
          "enforces its stated invariants and returns the correct status semantics for "
          "conflicting and missing resources. The study contributes a term-scoped, "
          "invariant-driven reference design in which correctness rules are expressed "
          "once in a service layer rather than repeated across user interfaces."),
    ("spacer", 1),
    ("p_left_italic", "Keywords: school management system, automated notification, "
                      "FastAPI, PostgreSQL, idempotency, design science research, "
                      "academic records."),
]
