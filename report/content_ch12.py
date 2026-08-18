"""Chapter One: Introduction. Chapter Two: Literature Review."""

CHAPTER_ONE = [
    ("chapter", "CHAPTER ONE", "INTRODUCTION"),

    ("h2", "1.1", "Background of the Study"),
    ("p", "The administration of a tertiary institution rests on a small number of "
          "records that must remain mutually consistent: who the students are, what "
          "courses exist, who is registered for what in a given semester, who attended "
          "which class, what marks were earned, and what fees are owed and paid. These "
          "records are not independent. A mark is meaningless without the registration "
          "it belongs to; an invoice is meaningless without the student and the "
          "semester it was raised against; an attendance rate is meaningless unless the "
          "register is tied to a specific class sitting. In principle, therefore, the "
          "administration of an institution is a single connected information problem."),
    ("p", "In practice it is rarely treated as one. Departments commonly maintain "
          "student biodata in one place, class registers on paper, continuous "
          "assessment marks in individual lecturers' spreadsheets, and fee accounts in "
          "a separate accounting package or ledger. Each of these artefacts is "
          "internally reasonable, but the boundaries between them are maintained by "
          "human effort. A student who defers, changes programme or is billed at the "
          "wrong level must be corrected in several places, and there is no mechanism "
          "that notices when one of those corrections is forgotten. [SOURCE NEEDED: a "
          "study documenting fragmented or manual record-keeping practice in Ghanaian "
          "or West African tertiary institutions]"),
    ("p", "Communication with students exhibits the same fragmentation. Registration "
          "windows, examination timetables, fee deadlines and resumption dates are "
          "typically announced through notice boards, departmental social-media groups "
          "and word of mouth. These channels are not systematic: they depend on a member "
          "of staff remembering to post at the right moment, and on the student "
          "happening to look. A reminder that arrives after the deadline it concerns has "
          "no value, and a reminder that is never sent at all is indistinguishable, from "
          "the student's point of view, from an institution that did not care to send "
          "it. [SOURCE NEEDED: evidence on students missing academic deadlines owing to "
          "poor institutional communication]"),
    ("p", "Software addressing parts of this problem is not scarce. Learning management "
          "systems such as Moodle organise course content and assessment; commercial "
          "student information systems handle admissions and records; accounting "
          "packages handle billing. What is less common, particularly at a scale and "
          "cost that a single department or a small institution can absorb, is a system "
          "in which these concerns share one data model, so that billing knows what "
          "programme and level a student is in, grading knows which registration a mark "
          "belongs to, and the notification mechanism knows which students exist at all. "
          "Where such integration is absent, institutions substitute manual "
          "reconciliation, and manual reconciliation is precisely where errors and "
          "delays originate."),
    ("p", "This project was undertaken against that background. It set out to build a "
          "single system in which the academic term is the organising concept, so that "
          "enrolment, timetabling, attendance, assessment and billing are all scoped to "
          "a semester and can be run independently each semester without the records of "
          "one term contaminating another; and in which the correctness rules that "
          "administrators presently enforce by vigilance are instead enforced by the "
          "software itself."),

    ("h2", "1.2", "Statement of the Problem"),
    ("p", "Tertiary institutions manage student records, course enrolment, attendance, "
          "assessment and fee accounts through disconnected manual and semi-automated "
          "processes that do not share a common data model, resulting in duplicated "
          "data entry, inconsistent and unverifiable results computation, avoidable "
          "billing errors, and the failure of time-critical academic announcements to "
          "reach students before the deadlines they concern."),
    ("p", "The seriousness of this problem lies in the fact that its costs are silent. "
          "When a lecturer computes a continuous-assessment mark in a spreadsheet whose "
          "weightings sum to more than one hundred percent, nothing objects; the error "
          "surfaces only if someone recomputes it by hand. When a bursary runs a billing "
          "cycle twice, the second run produces a second invoice for every student, and "
          "the duplicates must be located and reversed individually. When two lecturers "
          "are allocated the same lecture room at overlapping times, the clash is "
          "discovered by the students who arrive to find the room occupied. When a "
          "reminder about a registration deadline is posted three days late, no error "
          "message is generated anywhere; there are simply students who did not register."),
    ("p", "These failures share a structure. In each case a rule exists that everybody "
          "involved knows and agrees with, but the rule lives only in the heads of the "
          "people operating the process. It is never checked mechanically, and so it is "
          "violated whenever attention lapses. The need to solve this problem is "
          "therefore not merely a need for digitisation. Transferring the same "
          "unenforced rules from paper into a spreadsheet, or into a database with no "
          "constraints, reproduces the identical failure mode at greater speed. What is "
          "required is a system that holds these rules explicitly, refuses operations "
          "that would violate them, and performs the time-dependent communication tasks "
          "on a schedule that does not depend on anybody remembering."),

    ("h2", "1.3", "Aim of the Study"),
    ("p", "The aim of this study is to design, implement and evaluate an integrated "
          "web-based school management and automated notification system that maintains "
          "student, course, enrolment, timetable, attendance, assessment and fee records "
          "within a single term-scoped data model, enforces institutional correctness "
          "rules in software, and dispatches academic reminders to students "
          "automatically and without duplication."),

    ("h2", "1.4", "Objectives of the Study"),
    ("p", "In pursuit of the stated aim, the specific objectives of this study are:"),
    ("num", "To analyse the record-keeping and communication processes of a tertiary "
            "institution and derive from them a set of functional and non-functional "
            "requirements for an integrated management system."),
    ("num", "To design a normalised, term-scoped relational data model and a layered "
            "software architecture in which the academic, attendance, grading and "
            "financial domains share a single source of truth."),
    ("num", "To implement the designed system as a web application comprising a "
            "RESTful application programming interface and an administrative dashboard, "
            "with the institutional correctness rules encoded as enforced invariants."),
    ("num", "To implement an automated notification subsystem that evaluates "
            "configurable reminder offsets before each academic event and dispatches "
            "templated messages exactly once per subscriber, per event, per offset."),
    ("num", "To test and evaluate the implemented system against the requirements "
            "established in the first objective, verifying in particular that each "
            "encoded invariant rejects the operations it is intended to reject."),

    ("h2", "1.5", "Research Questions"),
    ("p", "The study was guided by the following questions:"),
    ("num", "Which correctness rules governing academic and financial records in a "
            "tertiary institution can be expressed as machine-enforceable invariants, "
            "and where in a layered architecture should each be enforced?"),
    ("num", "How can a relational data model be structured so that academic operations "
            "remain independently repeatable across successive academic terms?"),
    ("num", "What scheduling and record-keeping mechanism guarantees that an automated "
            "reminder is delivered to a subscriber exactly once for a given event and "
            "reminder offset, notwithstanding restarts of the application or repeated "
            "execution of the scheduled job?"),
    ("num", "To what extent does the implemented system satisfy the functional and "
            "non-functional requirements derived from institutional practice?"),

    ("h2", "1.6", "Significance of the Study"),
    ("p", "The direct beneficiaries of this study are the administrative and academic "
          "staff of the institution in which such a system is deployed. For "
          "administrators, the elimination of duplicated data entry between the student "
          "register, the enrolment record and the billing ledger removes a recurring "
          "source of clerical work and of error. For lecturers, weighted assessment "
          "definitions and automatic result computation remove the need to maintain "
          "private spreadsheets whose formulas nobody else can audit. For finance "
          "officers, an idempotent billing run and an invoice that refuses to be "
          "overpaid or voided after payment remove two of the most common and most "
          "time-consuming reconciliation tasks."),
    ("p", "Students benefit less visibly but more consequentially. A reminder that "
          "arrives seven days, three days, one day and on the morning of a registration "
          "deadline is a materially different service from an announcement pinned to a "
          "notice board, and it is delivered without any member of staff having to act. "
          "Students also gain a defensible account of their own standing: an attendance "
          "rate computed from recorded sittings and a grade computed from declared "
          "weightings are both auditable in a way that a handwritten register and a "
          "private spreadsheet are not."),
    ("p", "In terms of contribution to practice, the study offers a reference design in "
          "which institutional rules are expressed once, in a service layer, rather than "
          "being re-implemented in each user interface that touches the data. This is a "
          "modest but practically significant architectural claim: it is the difference "
          "between a system whose correctness survives the addition of a mobile "
          "application or a bulk import script, and one whose correctness does not. The "
          "system was further built entirely on open-source components, which is "
          "relevant to institutions for which the licensing cost of commercial student "
          "information systems is prohibitive."),

    ("h2", "1.7", "Scope of the Study"),
    ("p", "The study covers the design, implementation and functional evaluation of a "
          "web-based system providing the following capabilities: management of academic "
          "terms; management of student records keyed by index number and electronic "
          "mail address; maintenance of a course catalogue; enrolment of students in "
          "courses for a specified term; definition of recurring weekly timetable slots "
          "with room-clash detection; marking of attendance registers against class "
          "sittings and computation of attendance rates; definition of weighted "
          "assessments, entry of scores, and computation of course results and grade "
          "point averages; definition of fee structures, issuing of invoices through a "
          "billing run, recording of payments and computation of outstanding balances; "
          "and the creation of academic events with automated, offset-based electronic "
          "mail reminders to registered subscribers."),
    ("p", "The following are explicitly outside the scope of the study. The system does "
          "not implement a student-facing self-service portal; students are recipients "
          "of notifications and subjects of records rather than interactive users. It "
          "does not implement online payment processing; payments are recorded after "
          "they have been received through channels external to the system. It does not "
          "implement learning-content delivery, assignment submission or plagiarism "
          "detection, these being the province of a learning management system. It does "
          "not implement admissions processing, hostel allocation, library circulation "
          "or human-resource management. Notification delivery is implemented for "
          "electronic mail only; the channel abstraction admits short-message and push "
          "delivery, but no such channel was implemented."),
    ("p", "The intended users of the system are the administrative staff, lecturers and "
          "finance officers of a tertiary department or small institution. The study was "
          "conducted within the Computer Science Department, Kumasi Technical "
          "University, over the course of one academic year, and the requirements were "
          "drawn from the practices of that environment."),

    ("h2", "1.8", "Limitations of the Study"),
    ("p", "Several limitations qualify the findings reported here and should be borne in "
          "mind when interpreting them."),
    ("p", "First, the system was evaluated functionally rather than in live "
          "institutional operation. Test data were constructed to exercise the system's "
          "rules, including deliberately invalid operations, but the system was not run "
          "for a complete semester with real student records. Consequently the study can "
          "report that the implemented invariants behave as designed, but it cannot "
          "report on the administrative burden of sustained data entry, on staff "
          "adoption, or on behaviour at the scale of several thousand concurrent records."),
    ("p", "Second, the evaluation of the notification subsystem was necessarily "
          "compressed. Reminder offsets are expressed in days, and verifying the full "
          "seven-day, three-day, one-day and same-day sequence in real time would "
          "require a week of elapsed time per test case. The subsystem was therefore "
          "tested by invoking the processing cycle directly with controlled event dates, "
          "which verifies the dispatch logic and the duplicate-suppression guarantee but "
          "does not exercise the scheduler over a genuine multi-week period."),
    ("p", "Third, authentication and role-based authorisation are present in the "
          "codebase in a preliminary form, based on JSON Web Tokens and Argon2 password "
          "hashing, but the school-management endpoints were not placed behind "
          "per-role authorisation within the period of the study. The system is "
          "therefore suitable for deployment on a trusted internal network but would "
          "require the completion of that work before exposure to a public network."),
    ("p", "Fourth, the grading scale implemented in the system is a single configurable "
          "tuple, and the results reported here reflect that particular scale. "
          "Institutions operating a different scale would obtain different letter grades "
          "and grade points from the same raw scores, although the computation itself is "
          "unaffected."),
    ("p", "Fifth, the requirements were elicited from a single institutional context. "
          "Practices that are near-universal in that context, such as the use of index "
          "numbers as the primary student identifier, are embedded in the data model and "
          "would require adaptation elsewhere."),

    ("h2", "1.9", "Organisation of the Report"),
    ("p", "This report is organised into five chapters."),
    ("p", "Chapter One introduces the study. It establishes the administrative and "
          "communication context from which the problem arises, states the problem, and "
          "sets out the aim, objectives, research questions, significance, scope and "
          "limitations of the work."),
    ("p", "Chapter Two reviews the relevant literature. It clarifies the key concepts on "
          "which the system rests, examines existing school management and notification "
          "systems, reviews the technologies and architectural patterns available for "
          "building such a system, identifies the gaps that this project addresses, and "
          "summarises the position the study takes."),
    ("p", "Chapter Three presents the methodology and system design. It justifies the "
          "Design Science Research approach and the iterative development process "
          "adopted, presents the functional and non-functional requirements, describes "
          "the tools and technologies selected, and sets out the system architecture, "
          "use cases, database design and principal algorithms, together with the "
          "testing plan and the ethical considerations governing the work."),
    ("p", "Chapter Four documents the implementation of the system and its evaluation. "
          "It describes the development environment, the database implementation, each "
          "of the system modules and the user interface, explains the key code modules, "
          "and presents the test plan, test cases, test results and an evaluation of the "
          "system against its requirements."),
    ("p", "Chapter Five discusses the findings, draws conclusions and makes "
          "recommendations. It summarises what was achieved, assesses each objective "
          "against the evidence, compares the system with the existing systems reviewed "
          "in Chapter Two, states the contribution of the project and the challenges "
          "encountered, and recommends directions for further work."),
]


CHAPTER_TWO = [
    ("chapter", "CHAPTER TWO", "LITERATURE REVIEW"),

    ("h2", "2.1", "Introduction"),
    ("p", "This chapter reviews the body of work relevant to the design of an integrated "
          "school management and automated notification system. It proceeds from "
          "concepts to artefacts to techniques. Section 2.2 clarifies the key terms and "
          "ideas on which the system rests. Section 2.3 examines existing systems in the "
          "problem space and the design decisions embodied in them. Section 2.4 reviews "
          "the technologies available for constructing such a system and the grounds on "
          "which a selection can be made. Section 2.5 reviews the architectural patterns, "
          "methods and models drawn upon in the design. Section 2.6 identifies the gaps "
          "in the reviewed work that this project addresses, and Section 2.7 summarises "
          "the chapter."),

    ("h2", "2.2", "Conceptual Review"),

    ("h3", "2.2.1", "School Management Information Systems"),
    ("p", "A school management information system is an application that collects, "
          "stores, processes and reports the administrative and academic data of an "
          "educational institution. Its characteristic feature, distinguishing it from a "
          "general database application, is that its entities are bound by a "
          "well-established set of institutional rules: a student belongs to a "
          "programme and a level, a course carries credit hours, a registration binds a "
          "student to a course within a defined period, and a result is derived from "
          "assessments belonging to that registration. The value of such a system lies "
          "less in the storage of these records than in the consistency it maintains "
          "among them. [SOURCE NEEDED: a scholarly definition or review of school "
          "management information systems and their adoption]"),

    ("h3", "2.2.2", "Term Scoping and Temporal Data"),
    ("p", "Academic data are inherently periodic. The same course is offered repeatedly, "
          "to different cohorts, with different assessments and different fees, and each "
          "offering must be recorded and reported separately while the underlying course "
          "definition persists. This is a recognised problem in temporal data modelling: "
          "an entity possesses attributes that are stable across time and attributes that "
          "are valid only within a defined interval. The conventional resolution is to "
          "separate the durable entity from the time-bound association, so that the "
          "course catalogue is stable while enrolment, timetabling, assessment and "
          "billing are all keyed to an academic term. Failure to make this separation "
          "produces the familiar pathology in which historical results become "
          "unretrievable after a course definition is edited."),

    ("h3", "2.2.3", "Idempotency"),
    ("p", "An operation is idempotent when performing it more than once produces the "
          "same system state as performing it once. Helland (2012) argues that "
          "idempotency is not an optional refinement in distributed and long-running "
          "systems but a precondition for reliable operation, because in the presence of "
          "retries, timeouts and restarts an operation will eventually be attempted "
          "twice whether or not the designer intended it. The property is directly "
          "relevant in the present domain. A billing run that is not idempotent produces "
          "duplicate invoices when a network timeout prompts the operator to retry. A "
          "notification job that is not idempotent sends a student the same reminder on "
          "every scan interval. In each case the standard implementation technique is "
          "the same: before performing the effect, record or check a key that uniquely "
          "identifies the intended effect, and enforce that key's uniqueness in the "
          "database rather than in application logic alone."),

    ("h3", "2.2.4", "Invariants and Defensive Data Design"),
    ("p", "An invariant is a condition that must hold of the data at all times, "
          "regardless of the operations applied. Evans (2003) locates the enforcement of "
          "invariants at the boundary of the aggregate: the object responsible for a "
          "cluster of related data is also responsible for refusing any operation that "
          "would leave that cluster in an invalid state. In an institutional records "
          "system the relevant invariants are readily enumerated, since they are the "
          "rules administrators already apply informally, and include such conditions as "
          "the total weighting of the assessments of a course not exceeding one hundred "
          "percent, a room not being allocated to two classes at overlapping times, the "
          "sum of payments against an invoice not exceeding the invoiced amount, and a "
          "record with live dependants not being deletable. The design question is not "
          "whether these rules exist but where they are enforced, and the argument "
          "developed in this study is that enforcing them in a shared service layer, "
          "rather than in each user interface, is what makes them durable."),

    ("h3", "2.2.5", "Automated Notification and Scheduling"),
    ("p", "An automated notification system dispatches messages in response to the "
          "passage of time rather than in response to a user action. Its essential "
          "components are a definition of the events that warrant notification, a rule "
          "determining when relative to each event a message should be sent, a "
          "mechanism that periodically evaluates that rule, a rendering step that "
          "produces the message body, a delivery channel, and a record of what has "
          "already been delivered. The design difficulty concentrates in the last of "
          "these. Because the evaluating mechanism runs repeatedly and may run more "
          "often than the granularity of the rule it evaluates, correctness depends on "
          "the system's ability to distinguish a notification that is due from one that "
          "is due and has already been sent."),

    ("h3", "2.2.6", "Representational State Transfer"),
    ("p", "Fielding (2000) introduced Representational State Transfer as an "
          "architectural style for network-based applications, characterised by a "
          "uniform interface, stateless interaction, addressable resources and the "
          "manipulation of those resources through representations. In practical terms "
          "the style prescribes that application entities be exposed as resources "
          "identified by uniform resource identifiers, that the semantics of an "
          "operation be carried by the request method, and that the outcome be reported "
          "through the response status code. The last of these is significant for the "
          "present work: a well-designed interface distinguishes an operation that "
          "failed because the resource does not exist from one that failed because it "
          "would violate a rule, and reports these as distinct conditions rather than "
          "as a single generic error."),

    ("h2", "2.3", "Review of Existing Systems"),

    ("h3", "2.3.1", "Learning Management Systems"),
    ("p", "Moodle is the most widely deployed open-source learning management system and "
          "is used extensively in African tertiary institutions. It organises courses, "
          "distributes materials, collects assignment submissions, administers quizzes "
          "and maintains a gradebook whose categories and weightings are configurable. "
          "Its strengths are its maturity, its plugin ecosystem and the absence of "
          "licensing cost. Its limitation with respect to the present problem is one of "
          "orientation rather than capability: Moodle is designed around the delivery of "
          "teaching, and treats institutional administration as peripheral. It has no "
          "native concept of a fee structure, an invoice or a payment, no room-allocation "
          "or timetabling model, and its notion of enrolment is enrolment in a Moodle "
          "course rather than registration for a credit-bearing course in a specified "
          "academic term. An institution using Moodle therefore continues to maintain "
          "its authoritative student and financial records elsewhere, which reproduces "
          "the fragmentation the present project seeks to remove."),

    ("h3", "2.3.2", "Student Information Systems"),
    ("p", "Dedicated student information systems address administration directly. "
          "Commercial products in this category maintain admissions, biodata, "
          "registration, transcripts and billing within one product, and are the "
          "reference point against which any new system in this space must be assessed. "
          "Their principal barrier is cost and organisational weight: licensing, "
          "implementation and training costs are calibrated for institutions with a "
          "dedicated information-technology directorate, and configuration to local "
          "practice is a project in itself. Open-source alternatives such as Fedena and "
          "openSIS reduce the licensing barrier and cover student records, attendance "
          "and fees, but they are typically built around the assumptions of primary and "
          "secondary schooling, in which a pupil belongs to a class for a year rather "
          "than registering for an individually chosen set of credit-bearing courses "
          "each semester. Adapting that model to tertiary practice is not a matter of "
          "configuration. [SOURCE NEEDED: a comparative study or evaluation of open-source "
          "student information systems]"),

    ("h3", "2.3.3", "Institutional Portals and In-House Systems"),
    ("p", "Many institutions operate an in-house student portal, typically supporting "
          "course registration and the publication of results. These systems are "
          "well-adapted to local practice by construction, but they are commonly built "
          "as a user interface directly over a database, with validation logic embedded "
          "in the pages that perform data entry. The consequence is that the same rule "
          "is implemented several times over, once in each page that can modify the "
          "relevant data, and diverges as the system is maintained. A bulk import or an "
          "administrative correction applied outside those pages bypasses the rules "
          "entirely. This observation is one of the principal motivations for the "
          "architecture adopted in the present study."),

    ("h3", "2.3.4", "Communication and Notification Practice"),
    ("p", "Institutional communication with students is at present dominated by "
          "notice boards, bulk short-message services and social-media groups. Bulk "
          "messaging services deliver reliably but are triggered manually, which means "
          "the timing of a reminder depends on a member of staff acting on the correct "
          "day; they also maintain their own recipient lists, which diverge from the "
          "authoritative student register as students are admitted, defer or graduate. "
          "Social-media groups are timely when active but are neither auditable nor "
          "universal. Neither mechanism maintains a record of what was sent to whom, "
          "which means neither can guarantee that a given student was actually informed. "
          "[SOURCE NEEDED: a study of institutional communication channels and their "
          "effectiveness in reaching students]"),

    ("h2", "2.4", "Review of Related Technologies"),

    ("h3", "2.4.1", "Server-Side Frameworks"),
    ("p", "The candidate frameworks for the application server were the established "
          "general-purpose web frameworks and the newer asynchronous application "
          "programming interface frameworks. Django offers the most complete package, "
          "including an object-relational mapper, an authentication system and an "
          "automatically generated administrative interface, and would have delivered a "
          "working system quickly; its administrative interface, however, is generated "
          "from the data model and is therefore poorly suited to operations such as a "
          "billing run or bulk register marking that do not correspond to the editing of "
          "a single row. Flask offers minimalism at the cost of assembling request "
          "validation, serialisation and documentation from third-party extensions. "
          "FastAPI derives request validation, response serialisation and interface "
          "documentation from Python type annotations, provides first-class asynchronous "
          "request handling, and includes a dependency-injection mechanism that supports "
          "the layered construction adopted in this project. The type-driven validation "
          "is directly relevant to the aims of the study, since it removes an entire "
          "class of input-validation errors before any domain rule is evaluated."),

    ("h3", "2.4.2", "Client-Side Technologies"),
    ("p", "For the administrative dashboard the alternatives were server-rendered "
          "templates and a single-page application. Server-rendered templates are simpler "
          "to deploy and require no separate build step, but they couple the presentation "
          "to the server framework and require a full page round trip for each "
          "interaction, which is unsatisfactory for tasks such as marking a register of "
          "sixty students. A single-page application built with React maintains "
          "interface state on the client and communicates with the server through the "
          "same programming interface that any other client would use, which "
          "additionally validates the claim that the interface is not a privileged path "
          "into the data. TypeScript was preferred to plain JavaScript for the static "
          "guarantees it provides across the boundary between the client and the "
          "interface it consumes."),

    ("h3", "2.4.3", "Database Systems and Object-Relational Mapping"),
    ("p", "The data of this domain are highly relational and rich in constraints, which "
          "argues for a relational database management system. Codd (1970) established "
          "the relational model, and the normalisation theory built upon it remains the "
          "basis for eliminating the update anomalies that the fragmented spreadsheets "
          "described in Chapter One exhibit. Among relational systems, PostgreSQL was "
          "considered against MySQL and SQLite. SQLite is unsuited to concurrent "
          "multi-user write access. MySQL is capable but historically less strict in its "
          "constraint handling. PostgreSQL provides rigorous constraint enforcement, "
          "exact numeric types appropriate to monetary amounts, native support for "
          "universally unique identifiers and structured document columns, and is "
          "released under a permissive open-source licence."),
    ("p", "Object-relational mapping mediates between the relational store and the "
          "application's object model. SQLModel builds on SQLAlchemy and Pydantic so "
          "that a single class definition serves both as the table definition and as the "
          "validated data model, which reduces the duplication that otherwise arises "
          "between persistence models and request or response schemas. Schema evolution "
          "was managed with Alembic, which records each change as a versioned, reversible "
          "migration script rather than allowing the schema to be altered ad hoc."),

    ("h3", "2.4.4", "Task Scheduling"),
    ("p", "Three mechanisms were considered for periodic execution of the notification "
          "cycle. The operating-system scheduler, cron, is universally available and "
          "external to the application, but it invokes a separate process that must "
          "independently establish configuration and database connections, and it is "
          "invisible to the application's own logging and lifecycle. A distributed task "
          "queue such as Celery provides durable queuing, worker scaling and retry "
          "policies, at the cost of introducing a message broker and at least one "
          "additional deployed process. APScheduler runs within the application process "
          "and supports interval and cron triggers together with the concurrency and "
          "misfire controls needed here, namely a limit of one concurrent instance of "
          "the job, coalescing of missed executions, and a grace period within which a "
          "delayed execution is still permitted to run. For a workload consisting of a "
          "periodic scan of a modest number of rows, the operational simplicity of an "
          "in-process scheduler was judged decisive; the channel abstraction described "
          "in Chapter Three deliberately preserves the option of migrating to a "
          "distributed queue should the workload change."),

    ("h2", "2.5", "Review of Methods, Algorithms and Models"),

    ("h3", "2.5.1", "Layered Architecture and the Repository Pattern"),
    ("p", "Fowler (2002) catalogues the layered organisation of enterprise applications, "
          "in which presentation, domain logic and data access are separated so that each "
          "may vary independently, and describes the Repository pattern, in which data "
          "access is mediated by an object presenting a collection-like interface over "
          "the persistence mechanism. The benefit relevant to this study is that the "
          "domain layer expresses rules in terms of the domain rather than in terms of "
          "queries, and that those rules become reachable from any entry point into the "
          "system. Evans (2003) develops the complementary argument that the service "
          "layer is the correct home for operations that span several entities, which is "
          "the case for every non-trivial operation in this domain: a billing run touches "
          "fee structures, students and invoices; a result computation touches "
          "enrolments, assessments, scores and courses."),

    ("h3", "2.5.2", "Dependency Injection"),
    ("p", "Dependency injection supplies a component's collaborators from outside rather "
          "than having the component construct them. In the present system the "
          "consequence is that a request handler declares that it requires a service, "
          "the framework constructs that service with a repository, and the repository "
          "is constructed with a database session whose lifetime is bound to the "
          "request. Neither the handler nor the service contains any code concerned with "
          "obtaining or closing a connection, and either may be exercised in a test with "
          "a substituted collaborator."),

    ("h3", "2.5.3", "Weighted Assessment and Grade Point Computation"),
    ("p", "The computation of a course result from component assessments is a weighted "
          "aggregation in which each assessment contributes its declared weight in "
          "proportion to the fraction of its maximum score that the student attained. "
          "The design question that arises in practice is the treatment of assessments "
          "that have not yet been graded. Aggregating over the full declared weight "
          "treats an ungraded assessment as a score of zero, which renders every "
          "mid-semester standing meaningless and misleading. Normalising instead over "
          "the weight actually graded reports the student's standing among the "
          "assessments so far completed, which is both defensible and useful during the "
          "semester and converges on the same value as the conventional computation once "
          "all assessments have been graded. The latter approach was adopted. Grade "
          "points are then obtained by mapping the resulting percentage onto an ordered "
          "scale, and the grade point average is the credit-weighted mean of the grade "
          "points of the courses taken in the term."),

    ("h3", "2.5.4", "Interval Overlap Detection"),
    ("p", "Detection of a timetable clash reduces to the classical test for the overlap "
          "of two half-open intervals. Two bookings of the same room on the same day of "
          "the week conflict precisely when the start of each precedes the end of the "
          "other. Expressing the condition in this form, rather than through an "
          "enumeration of the cases in which two intervals may be arranged, avoids the "
          "boundary errors that such enumerations characteristically contain, and "
          "correctly permits one class to begin at the exact moment another ends."),

    ("h3", "2.5.5", "Software Development Process Models"),
    ("p", "Sommerville (2016) and Pressman and Maxim (2020) survey the principal process "
          "models. The waterfall model presumes that requirements can be established "
          "completely before design begins, which was not the case here, since the "
          "domain rules were discovered progressively as the model was built and tested. "
          "Iterative and incremental development, in the spirit of the Agile Manifesto "
          "(Beck et al., 2001), delivers the system as a sequence of working increments "
          "and accommodates the refinement of requirements as understanding develops. "
          "This was the process adopted, structured so that each increment delivered one "
          "complete vertical slice of the system, from database table through repository "
          "and service to interface endpoint and dashboard view."),

    ("h3", "2.5.6", "Design Science Research"),
    ("p", "Hevner et al. (2004) characterise design science research in information "
          "systems as the construction and evaluation of an artefact that addresses an "
          "identified organisational problem, and Peffers et al. (2007) provide the "
          "procedural model consisting of problem identification, definition of "
          "objectives, design and development, demonstration, evaluation and "
          "communication. This paradigm fits the present study exactly, in which the "
          "contribution is a working system and the evaluation is an assessment of that "
          "system against the requirements derived from the problem."),

    ("h2", "2.6", "Identification of Gaps in Existing Systems"),
    ("p", "Four gaps emerge from the foregoing review and together define the "
          "contribution attempted in this project."),
    ("p", "The first is the separation of academic and financial concerns. Learning "
          "management systems handle teaching and grading but not billing; accounting "
          "systems handle billing but hold no notion of programme, level or academic "
          "term. Because fee liability is in practice determined by exactly those "
          "academic attributes, the separation forces a manual reconciliation that is "
          "both laborious and error-prone. A system in which a fee structure may be "
          "targeted at a programme and level, and billed directly against the student "
          "register, closes this gap."),
    ("p", "The second is the treatment of notification as a manual act. In the systems "
          "reviewed, a reminder is sent because a member of staff decides to send it. A "
          "system in which the reminder schedule is declared once, as a property of the "
          "event, and thereafter executed by the system, changes the failure mode from "
          "silent omission to a recorded and inspectable dispatch history."),
    ("p", "The third is the placement of validation logic. Where rules are implemented "
          "in the user interface, they are absent from every other path into the data "
          "and are duplicated among the interfaces that do implement them. Consolidating "
          "them into a service layer through which all mutations pass makes the rules "
          "single-sourced and testable in isolation."),
    ("p", "The fourth is the absence of term scoping in systems adapted from primary and "
          "secondary education. Where a pupil belongs to a class for a year, term "
          "scoping is unnecessary; where a student registers for an individually chosen "
          "set of courses each semester, its absence makes the accurate reconstruction "
          "of historical records impossible."),

    ("h2", "2.7", "Summary of the Literature"),
    ("p", "The review establishes that the individual capabilities required of the "
          "proposed system are all well understood in isolation. Learning management "
          "systems handle course delivery and grading; student information systems "
          "handle records and billing; scheduling libraries handle periodic execution; "
          "relational databases and object-relational mappers handle persistence and "
          "constraint enforcement. What the review does not find is a system, available "
          "at a cost and complexity appropriate to a single department or small "
          "tertiary institution, that unifies these capabilities within one term-scoped "
          "data model and enforces institutional correctness rules at a single "
          "architectural boundary."),
    ("p", "The literature also supplies the methodological and architectural resources "
          "for constructing such a system: design science research as the paradigm, "
          "iterative and incremental development as the process, layered architecture "
          "with a repository and service separation as the structure, idempotency keys "
          "enforced by database constraints as the mechanism for reliable repeated "
          "execution, and Representational State Transfer as the interface style. "
          "Chapter Three sets out how these resources were applied in the design of the "
          "system."),
]
