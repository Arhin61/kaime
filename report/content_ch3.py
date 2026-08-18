"""Chapter Three: Methodology and System Design."""

CHAPTER_THREE = [
    ("chapter", "CHAPTER THREE", "METHODOLOGY AND SYSTEM DESIGN"),

    ("h2", "3.1", "Introduction"),
    ("p", "This chapter sets out how the study was conducted and how the resulting "
          "system was designed. Section 3.2 states and justifies the research approach, "
          "the methods used to gather requirements, and the development process "
          "followed. Section 3.3 presents the requirements themselves. Section 3.4 "
          "documents the tools and technologies selected and the grounds for selecting "
          "them. Section 3.5 presents the design of the system: its architecture, its "
          "use cases, its database schema and its principal object structure and "
          "behaviour. Section 3.6 specifies the algorithms that implement the "
          "non-trivial domain rules. Section 3.7 describes the data used. Section 3.8 "
          "presents the validation and testing plan, and Section 3.9 discusses the "
          "ethical considerations governing the work."),

    ("h2", "3.2", "Research Methodology"),

    ("h3", "3.2.1", "Research Approach"),
    ("p", "This study adopted the Design Science Research paradigm as articulated by "
          "Hevner et al. (2004) and operationalised by Peffers et al. (2007). The "
          "paradigm is appropriate because the object of the study is not a hypothesis "
          "about an existing phenomenon but an artefact constructed to address an "
          "identified organisational problem, and because its criterion of success is "
          "the utility of that artefact rather than the statistical significance of an "
          "observation. The six activities of the Peffers model map onto the present "
          "work as follows."),
    ("p", "Problem identification and motivation consisted of examining how student "
          "records, registration, attendance, results and fees are presently handled, "
          "and establishing the failure modes documented in Chapter One. Definition of "
          "the objectives of a solution produced the functional and non-functional "
          "requirements presented in Section 3.3, expressed as capabilities the artefact "
          "must possess and invariants it must enforce. Design and development produced "
          "the data model, architecture and algorithms presented in this chapter and the "
          "implementation reported in Chapter Four. Demonstration consisted of "
          "exercising each module of the working system against representative data. "
          "Evaluation consisted of the systematic testing reported in Chapter Four, in "
          "which each requirement and each declared invariant was tested with both "
          "valid and deliberately invalid input. Communication is effected by this "
          "report and by the oral defence accompanying it."),

    ("h3", "3.2.2", "Data Collection Methods"),
    ("p", "Requirements were established from three sources. The first was "
          "documentary analysis of the artefacts the institution presently uses: the "
          "structure of student registers, the layout of continuous-assessment "
          "spreadsheets, the composition of examination results sheets, the format of "
          "fee schedules and the calendar of academic events. These artefacts encode the "
          "institution's working data model, and reading them established the attributes "
          "each entity must carry, the identifiers in actual use, and the grading scale "
          "and assessment categories to be supported."),
    ("p", "The second was unstructured interviews with administrative staff, lecturers "
          "and finance staff, directed at establishing not what data are recorded but "
          "where the present processes fail. These conversations produced the "
          "invariants: the duplicate invoices that follow an interrupted billing run, "
          "the assessment weightings that do not sum correctly, the room double-bookings "
          "discovered only when a class arrives, and the difficulty of correcting a "
          "student record on which other records already depend."),
    ("p", "The third was observation of the existing systems reviewed in Chapter Two, "
          "which established the baseline of expected functionality and the interface "
          "conventions with which prospective users are already familiar."),
    ("p", "No personal data belonging to identifiable students were collected. All "
          "records used during development and testing were synthetic, as described in "
          "Section 3.7."),

    ("h3", "3.2.3", "System Development Methodology"),
    ("p", "The system was developed using an iterative and incremental process in the "
          "Agile tradition (Beck et al., 2001). A waterfall process was rejected because "
          "it presumes that requirements are fully known before design commences, "
          "whereas several of the domain rules that this system's design turns upon "
          "were discovered only in the course of modelling the domain and testing early "
          "increments. The treatment of ungraded assessments in the results computation, "
          "discussed in Section 3.6.2, is a case in point: the requirement became clear "
          "only when the first implementation produced obviously wrong mid-semester "
          "standings."),
    ("p", "Each increment delivered one complete vertical slice of the system, "
          "comprising the database table and its migration, the repository methods "
          "providing access to it, the service methods enforcing its rules, the "
          "endpoints exposing those methods, and the dashboard view consuming them. "
          "Delivering vertically rather than by layer meant that every increment ended "
          "in a system that could be exercised end to end, and that integration "
          "difficulties surfaced within the increment that caused them rather than "
          "accumulating to the end of the project."),
    ("p", "The increments were sequenced by dependency. Academic terms were built first, "
          "since every other academic entity is scoped by a term; then students and "
          "courses; then enrolment, which binds the two within a term; then timetabling "
          "and attendance, which depend on enrolment; then assessment and grading, which "
          "also depend on enrolment; then fees and billing, which depend on the student "
          "register; and finally the notification subsystem, which depends on the "
          "subscriber and event records. Version control was maintained throughout with "
          "Git, with each increment developed and reviewed before being merged."),
    ("figure", "3.1", "Iterative and incremental development cycle applied in the study",
     "fig3-9-process.png"),

    ("h2", "3.3", "Requirements Analysis"),

    ("h3", "3.3.1", "Functional Requirements"),
    ("p", "The functional requirements of the system are enumerated in Table 3.1. Each "
          "is identified by a code used subsequently to trace the requirement to its "
          "implementation in Chapter Four and to the test cases that verify it."),
    ("table", "3.1", "Functional requirements of the system",
     ["ID", "Requirement"],
     [
         ["FR-01", "The system shall allow an administrator to create, view, update and delete academic terms, and to designate one term as the current term."],
         ["FR-02", "The system shall allow an administrator to register a student with a unique index number and a unique electronic mail address, together with programme, level, contact and status information."],
         ["FR-03", "The system shall automatically link a newly registered student to an existing notification subscriber where their electronic mail addresses match."],
         ["FR-04", "The system shall allow an administrator to maintain a course catalogue in which each course carries a unique code, a title, credit hours and an active or inactive state."],
         ["FR-05", "The system shall allow an administrator to enrol a student in a course for a specified academic term, permitting at most one enrolment per student, course and term."],
         ["FR-06", "The system shall allow an administrator to define recurring weekly class sessions for a course within a term, specifying day, start time, end time and room."],
         ["FR-07", "The system shall reject any class session that would allocate a room already booked for an overlapping period on the same day of the same term."],
         ["FR-08", "The system shall allow a lecturer to mark an attendance register in bulk for a course sitting, recording each student as present, absent, late or excused."],
         ["FR-09", "The system shall update rather than duplicate attendance entries when a sitting is marked again."],
         ["FR-10", "The system shall compute, for each student in a course and term, the number of sittings held and the attendance rate, counting present, late and excused as attendance and absent as non-attendance."],
         ["FR-11", "The system shall allow a lecturer to define weighted assessments of a specified kind for a course within a term."],
         ["FR-12", "The system shall reject any assessment definition that would cause the total assessment weight for a course within a term to exceed one hundred percent."],
         ["FR-13", "The system shall allow a lecturer to record scores in bulk against an assessment, rejecting any score exceeding the assessment's maximum."],
         ["FR-14", "The system shall compute course results by weighted aggregation, normalising over the assessment weight actually graded, and map the resulting percentage to a letter grade and grade point."],
         ["FR-15", "The system shall compute a student's credit-weighted grade point average for a term."],
         ["FR-16", "The system shall allow a finance officer to define fee structures for a term, optionally targeted at a programme, a level, or both."],
         ["FR-17", "The system shall issue, on request, one invoice against a fee structure to every active student matching that structure, skipping students already invoiced for it."],
         ["FR-18", "The system shall allow a finance officer to record payments against an invoice, rejecting any payment that would cause the total paid to exceed the invoiced amount."],
         ["FR-19", "The system shall maintain the status of an invoice as unpaid, partially paid or paid according to the payments recorded against it, and shall permit an invoice to be voided only while no payment has been recorded against it."],
         ["FR-20", "The system shall compute a student's outstanding balance from the invoices and payments recorded."],
         ["FR-21", "The system shall prevent the deletion of any record on which other records depend, and shall report the attempt as a conflict."],
         ["FR-22", "The system shall allow an administrator to create academic events carrying a title, body, date range, message template and one or more reminder offsets."],
         ["FR-23", "The system shall periodically and without user intervention evaluate all active events and dispatch reminders to subscribers on the days indicated by the configured offsets."],
         ["FR-24", "The system shall dispatch at most one reminder per subscriber, per event, per offset, irrespective of how often the evaluation cycle is executed."],
         ["FR-25", "The system shall record the outcome of every dispatch attempt, including failures and their causes."],
         ["FR-26", "The system shall retry a failed dispatch attempt a configured number of times with an increasing delay before recording it as failed."],
         ["FR-27", "The system shall provide an administrative dashboard through which all of the above operations may be performed."],
     ],
     [0.8, 5.2]),

    ("h3", "3.3.2", "Non-Functional Requirements"),
    ("p", "Table 3.2 states the non-functional requirements, which constrain how the "
          "system provides the functionality above rather than what functionality it "
          "provides."),
    ("table", "3.2", "Non-functional requirements of the system",
     ["ID", "Category", "Requirement"],
     [
         ["NFR-01", "Reliability", "Repeated execution of any bulk operation, whether a billing run, a register marking or a notification cycle, shall leave the system in the same state as a single execution."],
         ["NFR-02", "Data integrity", "Every domain invariant shall be enforced in the service layer and, where it is expressible as a uniqueness or referential condition, reinforced by a database constraint."],
         ["NFR-03", "Correctness of interface", "The interface shall report a request for a non-existent resource as HTTP 404, a request violating a domain rule as HTTP 409, and a structurally invalid request as HTTP 422."],
         ["NFR-04", "Maintainability", "Domain rules shall be implemented once, in the service layer, and shall not be duplicated in the user interface or in any other client."],
         ["NFR-05", "Extensibility", "The notification delivery mechanism shall be defined by an interface, so that additional channels may be added without modification to the orchestration logic."],
         ["NFR-06", "Usability", "The dashboard shall present each module through a consistent layout, and shall report the reason for a rejected operation in terms meaningful to the operator."],
         ["NFR-07", "Performance", "Interactive dashboard operations shall complete within two seconds under representative departmental data volumes."],
         ["NFR-08", "Security", "Passwords shall be stored only as Argon2 hashes; configuration secrets shall be supplied by environment variables and shall not appear in the source repository."],
         ["NFR-09", "Portability", "The system shall run on any platform supporting Python 3.14 and PostgreSQL, and shall be deployable as a single application process serving both the interface and the compiled dashboard."],
         ["NFR-10", "Auditability", "Every notification dispatch and every payment shall carry a timestamp and be retrievable after the fact."],
     ],
     [0.7, 1.35, 3.95]),

    ("h3", "3.3.3", "User Requirements and User Stories"),
    ("p", "The requirements above were derived from the user stories set out in Table "
          "3.3, which express the needs of each class of user in that user's own terms."),
    ("table", "3.3", "User stories by actor",
     ["Actor", "User story"],
     [
         ["Administrator", "As an administrator, I want to open a new academic term and mark it as current, so that all subsequent registrations and billing are recorded against the correct semester."],
         ["Administrator", "As an administrator, I want to register a student once and have that record serve enrolment, grading, billing and notification, so that I do not maintain the same person in four places."],
         ["Administrator", "As an administrator, I want to be prevented from deleting a student who has enrolments or invoices, so that I do not silently destroy academic or financial history."],
         ["Administrator", "As an administrator, I want to schedule the weekly timetable and be told immediately if a room is already taken, so that clashes are resolved before the semester begins."],
         ["Administrator", "As an administrator, I want to declare an event and its reminder schedule once, so that students are reminded without my having to remember."],
         ["Lecturer", "As a lecturer, I want to mark a whole class register in one operation, so that taking attendance does not consume teaching time."],
         ["Lecturer", "As a lecturer, I want to correct a register I marked wrongly without creating duplicate entries, so that the attendance rate remains accurate."],
         ["Lecturer", "As a lecturer, I want the system to refuse assessment weightings that exceed one hundred percent, so that my continuous assessment scheme is arithmetically sound."],
         ["Lecturer", "As a lecturer, I want to see class standings before all assessments are graded, so that I can identify struggling students during the semester."],
         ["Finance officer", "As a finance officer, I want to bill an entire programme and level in one operation, so that invoicing does not require me to process students individually."],
         ["Finance officer", "As a finance officer, I want a repeated billing run to skip students already invoiced, so that an interrupted run can be safely restarted."],
         ["Finance officer", "As a finance officer, I want the system to refuse an overpayment, so that a keying error is caught at the point of entry rather than at reconciliation."],
         ["Student", "As a student, I want reminders of registration and examination deadlines to reach me in advance, so that I do not miss them."],
         ["Student", "As a student, I want to receive each reminder once, so that the messages remain worth reading."],
     ],
     [1.1, 4.9]),

    ("h2", "3.4", "Tools and Technologies"),
    ("p", "Table 3.4 records the tools and technologies selected for the project "
          "together with the role each plays. The comparative grounds for the principal "
          "selections were set out in Section 2.4."),
    ("table", "3.4", "Tools and technologies used in the project",
     ["Category", "Technology", "Role in the system"],
     [
         ["Programming language (server)", "Python 3.14", "Implementation of the application server, domain services and background scheduler."],
         ["Programming language (client)", "TypeScript", "Implementation of the administrative dashboard with static type checking across the interface boundary."],
         ["Server framework", "FastAPI", "Routing, request validation, response serialisation, dependency injection and generation of the interface specification."],
         ["Object-relational mapper", "SQLModel (over SQLAlchemy and Pydantic)", "Definition of tables and validated data models from single class declarations."],
         ["Database", "PostgreSQL", "Persistent storage with referential integrity, uniqueness constraints and exact numeric types for monetary amounts."],
         ["Database driver", "psycopg 3", "Connectivity between the application and PostgreSQL."],
         ["Migration tool", "Alembic", "Versioned, reversible evolution of the database schema."],
         ["Scheduler", "APScheduler", "In-process periodic execution of the notification cycle with concurrency and misfire control."],
         ["Template engine", "Jinja2", "Rendering of notification message bodies from templates and event context."],
         ["Mail transport", "fastapi-mail", "Asynchronous dispatch of rendered messages over SMTP."],
         ["Password hashing", "pwdlib with Argon2", "One-way hashing of user credentials."],
         ["Token handling", "PyJWT", "Issuing and verification of JSON Web Tokens for authentication."],
         ["Interface documentation", "Scalar", "Interactive presentation of the generated interface specification."],
         ["Client framework", "React 19", "Component-based construction of the dashboard."],
         ["Client routing", "React Router", "Navigation between dashboard views without full page reloads."],
         ["Build tool", "Vite", "Development server and production bundling of the dashboard."],
         ["Styling", "Tailwind CSS", "Consistent presentation through utility-based styling."],
         ["Package management", "uv (server), npm (client)", "Reproducible dependency resolution and installation."],
         ["Version control", "Git", "Source history and incremental development."],
         ["Development environment", "Visual Studio Code", "Editing, debugging and integrated terminal use."],
     ],
     [1.5, 1.5, 3.0]),

    ("h2", "3.5", "System Design"),

    ("h3", "3.5.1", "System Architecture"),
    ("p", "The system is organised as a three-tier application with a strict internal "
          "layering within the application tier, as shown in Figure 3.2. The "
          "presentation tier is a single-page application executing in the browser. The "
          "application tier is a FastAPI process divided into a router layer, a service "
          "layer and a repository layer, together with a background scheduler operating "
          "alongside the request-handling path. The data tier is a PostgreSQL database."),
    ("figure", "3.2", "Layered architecture of the Kaime system",
     "fig3-1-architecture.png"),
    ("p", "The responsibilities of each layer are deliberately narrow. The router layer "
          "translates between the transport and the domain: it declares the shape of "
          "each request and response, delegates to a service, and contains no domain "
          "logic whatever. The service layer owns the domain rules; it is the only layer "
          "that decides whether an operation is permissible, and it signals refusal by "
          "raising one of two domain exceptions rather than by constructing a transport "
          "response. The repository layer owns data access; it contains the queries and "
          "the session handling, and makes no decisions. The database itself carries the "
          "constraints that must hold irrespective of the path by which data arrive."),
    ("p", "This arrangement is what delivers requirement NFR-04. Because the router "
          "layer holds no rules, a second client, a bulk import script or an "
          "administrative tool reaches the same rules by the same route, and no rule can "
          "be bypassed by entering the system at a different point. It also delivers "
          "requirement NFR-03 economically: the two domain exceptions, "
          "ResourceNotFoundError and ResourceConflictError, are registered once as "
          "application-wide handlers that translate them into the 404 and 409 responses "
          "respectively, so no individual endpoint contains status-code logic."),
    ("p", "The background path is separate. The scheduler is started when the "
          "application starts and stopped when it stops, using the framework's lifespan "
          "mechanism. On each firing it constructs the notification orchestrator with "
          "its own database session, distinct from any request session, and executes one "
          "processing cycle. The same cycle is additionally exposed as an internal "
          "endpoint so that it may be invoked on demand during testing without waiting "
          "for the scheduler interval, which is the mechanism referred to in Section "
          "1.8."),

    ("h3", "3.5.2", "Use Case Design"),
    ("p", "Figure 3.3 presents the use cases of the system and the actors that "
          "initiate them. Four human actors are distinguished by function rather than "
          "by enforced privilege: the administrator, responsible for terms, students, "
          "courses, enrolment, timetabling and events; the lecturer, responsible for "
          "attendance and assessment; the finance officer, responsible for fee "
          "structures, billing and payments; and the student, who is a recipient of "
          "notifications rather than an operator of the system. A fifth, non-human "
          "actor, the scheduler, initiates the dispatch of due notifications and is "
          "shown as a system actor because it acts on the passage of time rather than "
          "at any person's instigation."),
    ("figure", "3.3", "Use case diagram of the Kaime system", "fig3-2-usecase.png"),

    ("h3", "3.5.3", "Database Design"),
    ("p", "The database comprises fifteen tables, normalised to third normal form. "
          "Figure 3.4 presents the entity relationship diagram. The design turns on "
          "three decisions."),
    ("figure", "3.4", "Entity relationship diagram of the Kaime database",
     "fig3-3-erd.png"),
    ("p", "The first is the separation of durable entities from term-bound "
          "associations. Students and courses are durable: a course exists whether or "
          "not it is running this semester. Enrolments, class sessions, assessments, fee "
          "structures and invoices all carry a term identifier, which is what allows the "
          "same course to be run, graded and billed independently each semester and "
          "allows any past semester to be reconstructed exactly. This realises the term "
          "scoping identified as a gap in Section 2.6."),
    ("p", "The second is that the enrolment is the hinge of the academic model. "
          "Attendance records and assessment scores refer to an enrolment, not to a "
          "student and a course separately. This makes it structurally impossible to "
          "record a mark for a student who is not registered for the course, or to mark "
          "a register for a student who is not in the class, and it means that removing "
          "an enrolment removes precisely the dependent records that ought to go with it."),
    ("p", "The third is the use of uniqueness constraints as idempotency keys, "
          "implementing NFR-01 and NFR-02. Four such constraints carry particular "
          "weight. The enrolment table is unique on the combination of student, course "
          "and term, which enforces FR-05. The attendance table is unique on the "
          "combination of enrolment, session date and class session, which is what "
          "permits FR-09 to be implemented as an update rather than an insertion. The "
          "assessment score table is unique on the combination of assessment and "
          "enrolment, which gives the same guarantee for score entry. The notification "
          "dispatch table is unique on the combination of event, recipient, channel, "
          "offset, scheduled date and status, which is the mechanism that delivers "
          "FR-24. In each case the constraint is declared in the schema, so the "
          "guarantee holds even if a defect were introduced into the service layer."),
    ("p", "Monetary amounts are stored as exact decimal values rather than as "
          "floating-point numbers, since the accumulation of representation error across "
          "a term's invoices and payments would otherwise render balances unreliable. "
          "Identifiers of records that may be created concurrently or in bulk, namely "
          "students, enrolments, attendance records, scores, invoices, payments and "
          "dispatches, are universally unique identifiers rather than sequential "
          "integers, which permits such records to be generated without coordinating on "
          "a shared sequence. Reference data with a natural ordering and a small "
          "cardinality, namely terms, courses, class sessions, assessments and fee "
          "structures, retain sequential integer keys."),
    ("p", "Table 3.5 summarises the tables of the database and their purpose."),
    ("table", "3.5", "Summary of database tables",
     ["Table", "Purpose", "Key constraints"],
     [
         ["users", "System operator accounts.", "Unique email; password stored as Argon2 hash."],
         ["subscribers", "Recipients of notifications.", "Email as primary key."],
         ["events", "Academic events warranting reminders.", "Reminder offsets stored as a document column; active flag."],
         ["notification_dispatches", "Record of every dispatch attempt.", "Unique on event, recipient, channel, offset, date and status."],
         ["academic_terms", "Semesters against which all academic activity is scoped.", "Unique name; one term flagged as current."],
         ["students", "Student register.", "Unique index number; unique email; optional link to a subscriber."],
         ["courses", "Course catalogue.", "Unique course code; active flag."],
         ["enrollments", "Registration of a student for a course in a term.", "Unique on student, course and term."],
         ["class_sessions", "Recurring weekly timetable slots.", "Day of week constrained to 0-6; room clash rejected in the service layer."],
         ["attendance_records", "Register marks against a sitting.", "Unique on enrolment, session date and class session."],
         ["assessments", "Weighted assessment definitions.", "Total weight per course and term constrained to 100 percent."],
         ["assessment_scores", "Scores recorded against an assessment.", "Unique on assessment and enrolment; score bounded by the maximum."],
         ["fee_structures", "Fee definitions targeted at a programme and level.", "Scoped to a term."],
         ["invoices", "Amounts billed to a student.", "At most one invoice per student per fee structure."],
         ["payments", "Amounts received against an invoice.", "Sum of payments constrained not to exceed the invoiced amount."],
     ],
     [1.25, 2.25, 2.5]),

    ("h3", "3.5.4", "Class Design"),
    ("p", "Figure 3.5 presents the principal classes of the application tier and the "
          "relationships among them. Each service holds a repository and no other "
          "dependency, which is what makes a service testable with a substituted "
          "repository. The notification orchestrator additionally holds a renderer, a "
          "delivery channel and its configuration."),
    ("figure", "3.5", "Class diagram of the service and repository layers",
     "fig3-4-class.png"),
    ("p", "The delivery channel is declared as an interface rather than as a concrete "
          "class, which implements NFR-05. The orchestrator refers only to the "
          "interface, so the addition of a short-message or push channel requires a new "
          "implementation of that interface and a change to the composition of the "
          "orchestrator, but no change to the logic that determines what should be sent "
          "and to whom. The two domain exceptions are shown because they constitute the "
          "vocabulary in which every service reports a refusal."),

    ("h3", "3.5.5", "Process Design"),
    ("p", "Figure 3.6 traces one execution of the notification cycle, which is the "
          "system's principal autonomous behaviour. The diagram makes visible the point "
          "at which FR-24 is enforced: before any message is rendered or sent, the "
          "orchestrator asks the repository whether a dispatch already exists for that "
          "combination of event, recipient, channel, offset and date, and abandons the "
          "recipient if one does. Because the dispatch record is written after each "
          "attempt, successful or otherwise, the guarantee survives a restart of the "
          "application mid-cycle."),
    ("figure", "3.6", "Sequence diagram of one notification dispatch cycle",
     "fig3-5-sequence.png"),
    ("p", "Figure 3.7 presents the billing run as an activity diagram, showing the "
          "point at which the existence check makes the operation idempotent in "
          "satisfaction of FR-17 and NFR-01, and the summary of invoices created and "
          "students skipped that is returned to the operator so that the effect of a "
          "repeated run is visible rather than silent."),
    ("figure", "3.7", "Activity diagram of the idempotent fee billing run",
     "fig3-6-activity-billing.png"),
    ("p", "Figure 3.8 presents the lifecycle of an invoice as a state transition "
          "diagram, showing the permitted transitions among the unpaid, partially paid, "
          "paid and void states and the two transitions that the system refuses in "
          "satisfaction of FR-18 and FR-19."),
    ("figure", "3.8", "State transition diagram for an invoice",
     "fig3-8-state-invoice.png"),

    ("h3", "3.5.6", "Input Design"),
    ("p", "Input to the system is received through forms in the dashboard and validated "
          "at three successive points. The first is the browser, where field types and "
          "required-field markers prevent the most obvious errors before a request is "
          "made. The second is the server's request model, where declared types, "
          "enumerations and bounds reject structurally invalid input with a 422 response "
          "before any domain code executes; enumerations are used for every value drawn "
          "from a fixed set, namely student status, enrolment status, attendance status, "
          "assessment kind, invoice status, payment method and message template, which "
          "makes an invalid value in these fields unrepresentable. The third is the "
          "service layer, which evaluates the domain rules that cannot be expressed as "
          "properties of a single request, such as whether a room is free or whether an "
          "assessment weight budget remains."),
    ("p", "Two input forms depart from single-record entry because the corresponding "
          "task does. The attendance register accepts an entire class in one submission, "
          "as required by FR-08, since marking sixty students individually would make "
          "the system unusable during a lecture. Score entry accepts an entire "
          "assessment's marks in one submission for the same reason. Both submissions "
          "are validated in full before any part is persisted, so a single invalid entry "
          "rejects the whole submission rather than leaving a partially recorded "
          "register."),

    ("h3", "3.5.7", "Output Design"),
    ("p", "Output takes three forms. Tabular views present lists of records with the "
          "filters appropriate to each module, such as programme, level and status for "
          "students, or term and course for enrolments. Computed views present derived "
          "figures rather than stored ones: the attendance summary reports sittings "
          "held, the counts of each status and the resulting rate; the results view "
          "reports the weighted percentage, the proportion of the assessment weight so "
          "far graded, the letter grade and the grade point; the balance view reports "
          "the total invoiced, the total paid and the outstanding amount. Reporting the "
          "graded proportion alongside the percentage is a deliberate design decision "
          "arising from Section 3.6.2, since it tells the reader how much of the "
          "semester's assessment the reported standing is based on."),
    ("p", "The third form of output is the notification message itself, rendered from a "
          "Jinja2 template selected per event from a fixed set of institutional "
          "templates, and populated with the recipient's name, the event title and body, "
          "the event dates and the number of days remaining. Restricting the template to "
          "a defined set rather than accepting an arbitrary path is both a usability and "
          "a security decision, since it makes it impossible for a template reference to "
          "address an arbitrary file on the server."),

    ("h2", "3.6", "Algorithm Descriptions"),

    ("h3", "3.6.1", "Notification Dispatch Algorithm"),
    ("p", "The notification cycle determines which reminders are due and dispatches "
          "those not already sent. Its correctness rests on the distinction between a "
          "reminder being due and a reminder being due and unsent, which is evaluated "
          "per recipient rather than per event. Pseudocode 3.1 states the algorithm."),
    ("code", "Pseudocode 3.1", "Notification dispatch cycle", """PROCEDURE process_due_notifications(now)
    lookahead  <- configured lookahead in days
    events     <- repository.get_upcoming_events(now, now + lookahead)
    subscribers<- repository.get_subscribers()

    FOR EACH event IN events DO
        event_date     <- date part of event.start_date
        days_remaining <- event_date - date part of now

        IF days_remaining < 0 THEN CONTINUE          // event already past

        offsets <- resolve_offsets(event)
        IF days_remaining NOT IN offsets THEN CONTINUE

        FOR EACH subscriber IN subscribers DO
            IF repository.has_dispatch(event.id, subscriber.email,
                                       channel, days_remaining, event_date)
            THEN CONTINUE                            // idempotency guard, FR-24

            context <- { student_name, event_title, body,
                         start_date, end_date, days_remaining }
            html    <- renderer.render(event.email_template, context)
            subject <- build_subject(event.title, days_remaining)

            TRY
                send_with_retry(subject, subscriber.email, html)
            CATCH error
                repository.record_dispatch(..., status <- "failed",
                                           error_message <- error)
                CONTINUE
            END TRY

            repository.record_dispatch(..., status <- "sent")
        END FOR
    END FOR
END PROCEDURE

FUNCTION resolve_offsets(event)
    IF event.notification_offsets is non-empty THEN
        RETURN non-negative values of event.notification_offsets
    ELSE IF event.notification_days_before is set and non-negative THEN
        RETURN { event.notification_days_before }
    ELSE
        RETURN configured default offsets
    END IF
END FUNCTION

PROCEDURE send_with_retry(subject, recipient, html)
    max_retries <- configured maximum, at least 1
    backoff     <- configured backoff in seconds, at least 1
    FOR attempt <- 1 TO max_retries DO
        TRY
            channel.send(subject, recipient, html)
            RETURN
        CATCH error
            IF attempt = max_retries THEN RAISE error
            WAIT backoff x attempt seconds            // linear backoff, FR-26
        END TRY
    END FOR
END PROCEDURE"""),
    ("p", "Three properties of this algorithm are worth remarking. The offset "
          "resolution is a three-level fallback, which allows an event to declare an "
          "explicit reminder schedule, or a single reminder, or to inherit the "
          "institutional default. The retry is applied to the transport failure only, "
          "so a rendering error is not retried pointlessly. The dispatch record is "
          "written for failures as well as successes, which satisfies FR-25 and makes a "
          "silent delivery failure impossible."),

    ("h3", "3.6.2", "Weighted Result Computation Algorithm"),
    ("p", "The computation of a course result aggregates the scores of the graded "
          "assessments in proportion to their declared weights. Pseudocode 3.2 states "
          "the algorithm; Figure 3.9 presents it as a flowchart."),
    ("code", "Pseudocode 3.2", "Weighted result and grade point average computation",
     """FUNCTION compute_results(enrollments)
    enrollments <- enrollments WHERE status != "dropped"
    scores      <- repository.list_scores_for_enrollments(enrollments)

    earned        <- empty map, default 0
    graded_weight <- empty map, default 0

    FOR EACH (score, assessment) IN scores DO
        IF assessment.max_score <= 0 OR assessment.weight <= 0 THEN CONTINUE
        fraction <- score.score / assessment.max_score
        earned[score.enrollment_id]        += fraction x assessment.weight
        graded_weight[score.enrollment_id] += assessment.weight
    END FOR

    results <- empty list
    FOR EACH enrollment IN enrollments DO
        covered <- graded_weight[enrollment.id]
        points  <- earned[enrollment.id]
        IF covered > 0 THEN
            percentage <- points / covered x 100      // normalise over graded weight
        ELSE
            percentage <- 0.0
        END IF
        (letter, grade_point) <- grade_for(percentage)
        APPEND (enrollment, percentage, covered, letter, grade_point) TO results
    END FOR
    RETURN results
END FUNCTION

FUNCTION grade_for(percentage)
    FOR EACH (floor, letter, point) IN GRADE_SCALE DO   // descending by floor
        IF percentage >= floor THEN RETURN (letter, point)
    END FOR
    RETURN ("F", 0.0)
END FUNCTION

FUNCTION compute_gpa(results)
    total_credits   <- sum of credit_hours over results
    weighted_points <- sum of (grade_point x credit_hours) over results
    IF total_credits > 0 THEN
        RETURN round(weighted_points / total_credits, 2)
    ELSE
        RETURN 0.0
    END IF
END FUNCTION"""),
    ("figure", "3.9", "Flowchart of the weighted result computation algorithm",
     "fig3-7-flowchart-grading.png"),
    ("p", "The decisive line is the normalisation over the weight actually graded "
          "rather than over the full declared weight. Consider a course whose assessment "
          "scheme is a quiz of ten percent, an assignment of twenty percent, a midterm "
          "of twenty percent and an examination of fifty percent, and a student who has "
          "so far scored full marks in the quiz and the assignment, the midterm and "
          "examination being ungraded. Aggregating over the full weight yields thirty "
          "percent and a failing grade, which is not merely unhelpful but false: the "
          "student has failed nothing. Normalising over the thirty percent actually "
          "graded yields one hundred percent, which correctly reports that the student "
          "has full marks in everything assessed so far. Once every assessment is "
          "graded, the graded weight equals the declared total and the two computations "
          "coincide. The proportion of weight graded is reported alongside the "
          "percentage so that a reader can see the basis of the figure."),
    ("p", "The grade scale used by the system is given in Table 3.6. It is defined as a "
          "single ordered structure in the grading service, so an institution operating "
          "a different scale changes one declaration and no logic."),
    ("table", "3.6", "Grade scale implemented in the system",
     ["Percentage range", "Letter grade", "Grade point"],
     [
         ["80.00 and above", "A", "4.0"],
         ["75.00 to 79.99", "B+", "3.5"],
         ["70.00 to 74.99", "B", "3.0"],
         ["65.00 to 69.99", "C+", "2.5"],
         ["60.00 to 64.99", "C", "2.0"],
         ["55.00 to 59.99", "D+", "1.5"],
         ["50.00 to 54.99", "D", "1.0"],
         ["Below 50.00", "F", "0.0"],
     ],
     [2.4, 1.8, 1.8]),

    ("h3", "3.6.3", "Assessment Weight Budget Check"),
    ("p", "Before an assessment is created or its weight amended, the service verifies "
          "that the total weight declared for the course within the term will not exceed "
          "one hundred percent, implementing FR-12. When an existing assessment is being "
          "amended, that assessment is excluded from the existing total so that its own "
          "current weight is not counted twice."),
    ("code", "Pseudocode 3.3", "Assessment weight budget check",
     """PROCEDURE assert_weight_budget(course_id, term_id, added_weight, exclude_id)
    existing <- sum of assessment.weight
                FOR assessments OF course_id AND term_id
                WHERE assessment.id != exclude_id
    IF existing + added_weight > 100 THEN
        RAISE ResourceConflictError(
            "Total assessment weight would be " + (existing + added_weight) +
            "%, which exceeds 100%.")
    END IF
END PROCEDURE"""),

    ("h3", "3.6.4", "Room Clash Detection"),
    ("p", "A proposed class session is rejected if the room it requests is already "
          "booked for an overlapping period on the same day of the same term, "
          "implementing FR-07. Two half-open intervals overlap precisely when each "
          "begins before the other ends, which is the condition tested. Sessions with no "
          "room specified are exempt, since an unallocated session cannot clash."),
    ("code", "Pseudocode 3.4", "Room clash detection",
     """PROCEDURE assert_no_room_clash(term_id, day_of_week, room, start, end, exclude_id)
    IF room is empty THEN RETURN                 // no room, no clash possible

    candidates <- repository.find_room_clashes(term_id, day_of_week,
                                               room, exclude_id)
    FOR EACH other IN candidates DO
        IF start < other.end_time AND other.start_time < end THEN
            RAISE ResourceConflictError(
                "Room " + room + " is already booked " +
                other.start_time + "-" + other.end_time + " on that day.")
        END IF
    END FOR
END PROCEDURE"""),
    ("p", "The strict inequalities are deliberate. A session ending at 10:00 and a "
          "session beginning at 10:00 do not overlap and are permitted, which matches "
          "the way a timetable is actually read."),

    ("h3", "3.6.5", "Idempotent Billing and Payment Application"),
    ("p", "The billing run issues one invoice to each active student matching the fee "
          "structure's programme and level, skipping any student already invoiced "
          "against that structure, and reports both counts. Payment application "
          "recomputes the invoice status from the total received and refuses any payment "
          "that would exceed the invoiced amount."),
    ("code", "Pseudocode 3.5", "Idempotent billing run and payment application",
     """PROCEDURE run_billing(structure_id)
    structure <- get_fee_structure(structure_id)          // 404 if absent
    students  <- repository.list_students(program <- structure.program,
                                          level   <- structure.level,
                                          status  <- "active")
    created <- 0 ; skipped <- 0
    FOR EACH student IN students DO
        IF repository.get_invoice_for_structure(student.id, structure_id) EXISTS
        THEN
            skipped <- skipped + 1                        // idempotency, FR-17
        ELSE
            create Invoice(student, structure.term, structure,
                           amount   <- structure.amount,
                           due_date <- structure.due_date,
                           status   <- "unpaid")
            created <- created + 1
        END IF
    END FOR
    COMMIT
    RETURN (created, skipped)
END PROCEDURE

PROCEDURE record_payment(invoice_id, amount)
    invoice <- get_invoice(invoice_id)                    // 404 if absent
    IF invoice.status = "void" THEN
        RAISE ResourceConflictError("Cannot pay a voided invoice.")
    END IF
    already_paid <- sum of payments against invoice
    IF already_paid + amount > invoice.amount THEN
        RAISE ResourceConflictError("Payment exceeds the outstanding balance.")
    END IF
    persist Payment(invoice, amount, method, reference, paid_on)
    invoice.status <- status_for(invoice.amount, already_paid + amount)
    COMMIT
END PROCEDURE

FUNCTION status_for(amount, paid)
    IF paid >= amount THEN RETURN "paid"
    ELSE IF paid > 0  THEN RETURN "partial"
    ELSE                   RETURN "unpaid"
    END IF
END FUNCTION"""),

    ("h3", "3.6.6", "Attendance Rate Computation"),
    ("p", "The attendance summary tallies the register entries of each student in a "
          "course and term and expresses attendance as the proportion of recorded "
          "sittings at which the student was credited. Present, late and excused are "
          "credited; absent is not. Crediting an excused absence reflects institutional "
          "practice, in which a student with documented leave is not penalised."),
    ("code", "Pseudocode 3.6", "Attendance rate computation",
     """FUNCTION course_summary(course_id, term_id)
    records <- repository.list_attendance(course_id, term_id)
    tallies <- empty map keyed by student

    FOR EACH (record, enrollment, student) IN records DO
        t <- tallies[enrollment.student_id]   // created with all counts at 0
        t.sessions_held      <- t.sessions_held + 1
        t[record.status]     <- t[record.status] + 1
    END FOR

    summaries <- empty list
    FOR EACH (student_id, t) IN tallies DO
        credited <- t.present + t.late + t.excused         // FR-10
        IF t.sessions_held > 0 THEN
            rate <- round(credited / t.sessions_held x 100, 2)
        ELSE
            rate <- 0.0
        END IF
        APPEND summary(student, sessions_held, present, late,
                       excused, absent, rate) TO summaries
    END FOR
    RETURN summaries sorted by student name
END FUNCTION"""),

    ("h2", "3.7", "Data Description"),
    ("p", "The system does not consume an external dataset; it generates and maintains "
          "its own records. Two categories of data were nonetheless required during "
          "development and evaluation."),
    ("p", "The first is reference data drawn from institutional practice: the "
          "structure of index numbers, the names and credit values of courses, the "
          "programme and level designations in use, the assessment categories and their "
          "customary weightings, the grade scale reproduced in Table 3.6, and the "
          "calendar of academic events. These were obtained from the documentary sources "
          "described in Section 3.2.2 and determine the shape of the model rather than "
          "its contents."),
    ("p", "The second is the synthetic test dataset used for demonstration and "
          "evaluation. No real student data were used at any point. The dataset "
          "comprised two academic terms, a set of courses spanning several levels and "
          "credit values, a cohort of students distributed across programmes and levels "
          "and including students in non-active statuses, enrolments connecting them, a "
          "weekly timetable containing both compatible and deliberately clashing room "
          "allocations, attendance registers over several sittings including all four "
          "attendance statuses, assessment schemes both within and deliberately "
          "exceeding the weight budget, scores both within and deliberately exceeding "
          "assessment maxima, fee structures targeted variously at a programme, a level "
          "and both, and payments constituting under-payment, exact payment and "
          "deliberate over-payment. Names and electronic mail addresses were fabricated; "
          "index numbers followed the institutional format without corresponding to any "
          "real student."),
    ("p", "The dataset was constructed specifically so that the invalid cases are "
          "present, since a dataset containing only valid records would exercise none of "
          "the invariants that constitute the substance of the design. The mail "
          "transport was directed to a capture mailbox during testing so that no message "
          "was delivered to any real address."),

    ("h2", "3.8", "Validation and Testing Plan"),

    ("h3", "3.8.1", "Testing Approach"),
    ("p", "Testing followed the requirements. Each functional requirement of Table 3.1 "
          "was traced to at least one test case, and each requirement expressing a "
          "prohibition was tested with input that violates it, on the principle that an "
          "invariant that has never rejected anything has not been shown to work. "
          "Testing was conducted incrementally, each increment being tested as it was "
          "completed, with the earlier increments re-exercised after each subsequent one "
          "to detect regressions."),

    ("h3", "3.8.2", "Types of Testing"),
    ("p", "Four types of testing were planned. Unit testing exercises the service-layer "
          "computations in isolation, and is directed at the algorithms of Section 3.6: "
          "the weight budget check, the interval overlap test, the grade mapping, the "
          "weighted normalisation, the attendance rate and the invoice status "
          "determination. Integration testing exercises complete paths from endpoint "
          "through service and repository to database and back, confirming both that "
          "records are correctly persisted and that the domain exceptions surface as the "
          "correct status codes. System testing exercises whole workflows end to end, "
          "such as opening a term, registering students, enrolling them, timetabling, "
          "marking registers, defining and scoring assessments, computing results, "
          "billing, taking payment and dispatching notifications. User acceptance "
          "testing places the dashboard before prospective users who attempt the tasks "
          "of Table 3.3 and report where the system obstructs or misleads them."),
    ("p", "Idempotency is tested as a distinct concern cutting across the above, since "
          "it is the property most easily lost and least visible when lost. Every "
          "operation claiming idempotency, namely the billing run, register marking, "
          "score entry and the notification cycle, is executed twice against identical "
          "input, and the state after the second execution is compared with the state "
          "after the first."),

    ("h3", "3.8.3", "Test Environment and Criteria"),
    ("p", "Testing was carried out in the development environment documented in Section "
          "4.1, against a PostgreSQL database populated with the synthetic dataset of "
          "Section 3.7 and reset between runs so that each test began from a known "
          "state. A test case passes when the observed outcome matches the expected "
          "outcome in full, including the status code returned and, for rejected "
          "operations, the fact that no partial change was persisted. The test cases and "
          "their results are reported in Sections 4.8 and 4.9."),

    ("h2", "3.9", "Ethical Considerations"),

    ("h3", "3.9.1", "Data Privacy"),
    ("p", "The system by its nature holds personal data: names, electronic mail "
          "addresses, telephone numbers, dates of birth, academic performance and "
          "financial liability. Academic and financial records are among the more "
          "sensitive categories an institution holds, since disclosure can affect a "
          "student's standing, employment prospects and reputation. Three measures "
          "govern this. No real student data were used at any point in development or "
          "testing; the dataset described in Section 3.7 is wholly synthetic. The system "
          "collects only attributes with an identified administrative purpose, and "
          "attributes that are not required for an operation the system performs, such "
          "as identity-document numbers or next-of-kin details, were deliberately "
          "excluded from the model. Access to the deployed system is confined to "
          "authenticated operators."),

    ("h3", "3.9.2", "Consent"),
    ("p", "No human participants were the subject of experimentation. The staff "
          "consulted during requirements gathering participated voluntarily, were "
          "informed of the purpose of the discussion, and are not identified in this "
          "report. Where a system of this kind is deployed with real data, the "
          "institution's own data-protection obligations apply, and the notification "
          "subscriber record is designed so that a subscriber may be removed "
          "independently of the student record, which is the mechanism by which a "
          "withdrawal of consent to receive messages would be honoured without "
          "destroying the academic record."),

    ("h3", "3.9.3", "Security Considerations"),
    ("p", "Passwords are never stored in recoverable form; only Argon2 hashes are "
          "persisted, and the password field is excluded from every response model so "
          "that a hash cannot be disclosed by an interface response. Configuration "
          "secrets, comprising database credentials, mail credentials and the token "
          "signing key, are supplied through environment variables and are excluded from "
          "the source repository. Database access is confined to the repository layer "
          "and mediated by the object-relational mapper, which parameterises queries and "
          "thereby closes the injection vector. The set of message templates is a fixed "
          "enumeration rather than a caller-supplied path, which prevents a template "
          "reference from addressing an arbitrary file. The limitations of the present "
          "authorisation arrangement are stated frankly in Section 1.8 and revisited in "
          "Section 5.10."),

    ("h3", "3.9.4", "Academic Integrity"),
    ("p", "All third-party components used in this project are open-source software "
          "used in accordance with their licences and acknowledged in Section 3.4 and in "
          "the references. All sources consulted are cited. Where artificial-intelligence "
          "tools were used in the preparation of this report, their use was confined to "
          "drafting assistance and language refinement, and is disclosed in the "
          "declaration; the system design, the implementation and the conclusions are "
          "the author's own work."),
]
