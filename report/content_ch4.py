"""Chapter Four: System Implementation, Testing and Results."""

CHAPTER_FOUR = [
    ("chapter", "CHAPTER FOUR", "SYSTEM IMPLEMENTATION, TESTING AND RESULTS"),

    ("h2", "4.1", "Introduction"),
    ("p", "This chapter documents how the design presented in Chapter Three was "
          "realised and how the resulting system was evaluated. Sections 4.2 to 4.4 "
          "describe the development environment, the languages and frameworks used, and "
          "the implementation of the database. Section 4.5 describes each module of the "
          "system. Section 4.6 presents the user interface. Section 4.7 explains the key "
          "code modules. Sections 4.8 and 4.9 present the test plan, the test cases and "
          "the results obtained. Sections 4.10 and 4.11 report the performance measured "
          "and evaluate the system against the requirements of Section 3.3."),

    ("h2", "4.2", "Development Environment"),
    ("p", "Table 4.1 records the environment in which the system was developed and "
          "tested. The specification of the development machine is stated because the "
          "performance figures reported in Section 4.10 were obtained on it and are not "
          "meaningful without it."),
    ("table", "4.1", "Development environment",
     ["Item", "Specification"],
     [
         ["Operating system", "Linux (kernel 7.0)"],
         ["Processor", "<<Processor model and speed>>"],
         ["Memory", "<<Installed RAM>>"],
         ["Storage", "<<Storage type and capacity>>"],
         ["Code editor", "Visual Studio Code"],
         ["Server runtime", "Python 3.14"],
         ["Server package manager", "uv"],
         ["Client runtime", "Node.js 24"],
         ["Client package manager", "npm"],
         ["Database server", "PostgreSQL"],
         ["Version control", "Git"],
         ["Interface testing", "Scalar interactive documentation; curl"],
         ["Browser", "<<Browser and version used for dashboard testing>>"],
     ],
     [2.0, 4.0]),

    ("h2", "4.3", "Programming Languages, Tools and Frameworks"),
    ("p", "The server was implemented in Python 3.14 and the dashboard in TypeScript. "
          "The grounds on which each framework was selected were given in Section 2.4 "
          "and the complete inventory in Table 3.4; this section records how each was "
          "actually used."),
    ("p", "FastAPI provides the routing, request validation and dependency injection of "
          "the application tier. Each domain has its own router module carrying a common "
          "path prefix and a tag, so that the generated interface specification is "
          "organised by domain. Request and response models are declared as Pydantic "
          "schemas, from which the framework derives validation, serialisation and "
          "documentation, so that no endpoint contains hand-written validation code. The "
          "dependency-injection mechanism is used to construct the entire layer stack "
          "for each request: an endpoint declares that it requires a service, the "
          "framework constructs that service with a repository, and the repository with "
          "a session whose lifetime ends with the request."),
    ("p", "SQLModel is used to declare each table once, the declaration serving both as "
          "the mapped table and as the validated model. Alembic maintains the schema as "
          "a sequence of versioned migration scripts. APScheduler provides the "
          "asynchronous scheduler that drives the notification cycle. Jinja2 renders the "
          "message templates held in the templates directory, and fastapi-mail performs "
          "the transport. Argon2 hashing is provided through pwdlib and token handling "
          "through PyJWT. Scalar presents the generated interface specification "
          "interactively at the documentation path."),
    ("p", "On the client, React 19 provides the component model and React Router the "
          "navigation between views. Vite provides the development server and the "
          "production build. Tailwind CSS provides the styling, applied through a small "
          "set of shared presentational components so that the modules are visually "
          "consistent. The production build emits static assets that the server process "
          "itself serves, so that the whole system is deployed as a single process."),

    ("h2", "4.4", "Database Implementation"),
    ("p", "The fifteen tables of Figure 3.4 were implemented as SQLModel classes in a "
          "single module, and the schema was evolved through Alembic migrations. Seven "
          "migrations were applied over the course of the project, the last of which "
          "introduced the ten tables of the school-management domain in one revision. "
          "Maintaining the schema as migrations rather than by direct alteration means "
          "that the schema of any past state of the project can be reproduced exactly, "
          "and that the deployment procedure is the application of migrations rather "
          "than the manual execution of statements."),
    ("p", "The constraints identified in Section 3.5.3 were implemented as table "
          "constraints rather than being left to application logic. Table 4.2 records "
          "each uniqueness constraint, the requirement it implements and the behaviour "
          "it produces."),
    ("table", "4.2", "Uniqueness constraints and the guarantees they provide",
     ["Table", "Constraint columns", "Requirement", "Effect"],
     [
         ["enrollments", "student_id, course_id, term_id", "FR-05", "A student cannot be registered twice for the same course in the same term."],
         ["attendance_records", "enrollment_id, session_date, class_session_id", "FR-09", "Re-marking a sitting updates the existing entry instead of creating a second one."],
         ["assessment_scores", "assessment_id, enrollment_id", "FR-13", "Re-entering a mark updates the existing score."],
         ["notification_dispatches", "event_id, recipient_email, channel, days_before, scheduled_for, status", "FR-24", "A subscriber cannot be notified twice for the same event and offset."],
         ["students", "index_number (and, separately, email)", "FR-02", "Index numbers and electronic mail addresses are unique across the register."],
         ["courses", "code", "FR-04", "Course codes are unique across the catalogue."],
         ["academic_terms", "name", "FR-01", "Term names are unique."],
     ],
     [1.1, 1.6, 0.9, 2.4]),
    ("p", "Referential integrity is enforced by foreign keys throughout, and the "
          "deletion rules of FR-21 are implemented in the service layer above them: a "
          "term with enrolments, a student with enrolments or invoices, and a course "
          "with enrolments, assessments or timetable slots each refuse deletion with a "
          "conflict response. The single deliberate exception is the deletion of an "
          "enrolment, which cascades to the attendance records and scores belonging to "
          "it, on the grounds that those records have no meaning once the registration "
          "they describe is gone."),
    ("p", "Columns holding monetary amounts are declared as exact decimals with "
          "specified precision and scale rather than as floating-point numbers. Columns "
          "used as query predicates, principally the foreign keys, the student index "
          "number, the course code, the student and enrolment statuses and the attendance "
          "session date, are indexed."),

    ("h2", "4.5", "System Modules"),
    ("p", "The system comprises eleven functional modules. Each is implemented as a "
          "vertical slice through the layers, and each is described below in terms of "
          "what it does and which rules it enforces."),

    ("h3", "4.5.1", "Academic Terms Module"),
    ("p", "Provides the creation, listing, retrieval, amendment and deletion of academic "
          "terms, together with retrieval of the term currently in force. It rejects a "
          "term whose end date precedes its start date, rejects a duplicate term name, "
          "and refuses to delete a term that has enrolments recorded against it. Because "
          "every other academic entity carries a term identifier, this module is the "
          "foundation of the term scoping described in Section 3.5.3."),

    ("h3", "4.5.2", "Student Records Module"),
    ("p", "Provides the student register, keyed by index number and electronic mail "
          "address, both of which are unique. Students may be listed with filters on "
          "programme, level and status, and searched by name or index number. When a "
          "student is registered whose electronic mail address matches an existing "
          "notification subscriber, the record is linked to that subscriber "
          "automatically, implementing FR-03 and keeping the academic register and the "
          "notification audience in step. The module refuses to delete a student who has "
          "enrolments or invoices."),

    ("h3", "4.5.3", "Course Catalogue Module"),
    ("p", "Provides the course catalogue, each course carrying a unique code, a title, "
          "credit hours, an owning department, a level and an active state. Courses may "
          "be deactivated rather than deleted, which is the correct treatment for a "
          "course no longer offered but present in historical records. The module "
          "refuses to delete a course with enrolments, assessments or timetable slots, "
          "and exposes the roster of students registered for a course in a given term."),

    ("h3", "4.5.4", "Enrolment Module"),
    ("p", "Binds a student to a course within a term, at most once, enforcing FR-05 "
          "through the uniqueness constraint of Table 4.2. It refuses to enrol a student "
          "in an inactive course and refuses to enrol a student who is not active. An "
          "enrolment carries a status of enrolled, dropped or completed; dropped "
          "enrolments are excluded from results computation, which is why a student who "
          "withdraws from a course does not receive a failing grade in it."),

    ("h3", "4.5.5", "Timetable Module"),
    ("p", "Provides recurring weekly class sessions for a course within a term, each "
          "carrying a day of the week, a start and end time, a room and a lecturer. It "
          "rejects a session whose end time does not follow its start time, and rejects "
          "any session that would double-book a room, implementing FR-07 through the "
          "interval overlap test of Section 3.6.4. The rejection message names the "
          "conflicting booking and its times, so that the operator can resolve the clash "
          "without searching for it."),

    ("h3", "4.5.6", "Attendance Module"),
    ("p", "Provides bulk marking of the register for a course sitting, implementing "
          "FR-08. Every entry in a submission is validated before any part of it is "
          "persisted, so a submission naming an enrolment that does not belong to the "
          "course is rejected in its entirety. Re-marking a sitting updates the existing "
          "entries rather than duplicating them, implementing FR-09. The module computes "
          "the per-student summary of Section 3.6.6, reporting sittings held, the count "
          "of each status and the attendance rate."),

    ("h3", "4.5.7", "Grading Module"),
    ("p", "Provides weighted assessment definitions of five kinds, bulk score entry and "
          "result computation. It enforces the weight budget of FR-12, rejects a score "
          "exceeding an assessment's maximum, rejects a submission naming an enrolment "
          "belonging to a different course or term, and rejects a submission naming the "
          "same enrolment more than once. Results are computed by the normalising "
          "algorithm of Section 3.6.2 and reported both per course and as a "
          "credit-weighted grade point average for a student in a term."),

    ("h3", "4.5.8", "Fees and Billing Module"),
    ("p", "Provides fee structures scoped to a term and optionally targeted at a "
          "programme, a level or both; an idempotent billing run implementing FR-17; "
          "manual invoice creation; payment recording; and the computation of a "
          "student's balance. It refuses an overpayment, refuses payment against a "
          "voided invoice, and refuses to void an invoice against which any payment has "
          "been recorded. The billing run reports the number of invoices created and the "
          "number of students skipped, which makes the effect of a repeated run visible "
          "to the operator."),

    ("h3", "4.5.9", "Subscriber and Event Modules"),
    ("p", "Provide the audience and the subject matter of the notification subsystem. "
          "Subscribers are contact records keyed by electronic mail address. Events carry "
          "a title, a body, a date range, a message template drawn from the fixed "
          "enumeration, one or more reminder offsets, and an active flag by which an "
          "event may be suspended without being deleted."),

    ("h3", "4.5.10", "Notification Module"),
    ("p", "Implements the dispatch cycle of Section 3.6.1. The scheduler starts with "
          "the application and fires at the configured interval, currently thirty "
          "minutes; each firing examines events beginning within the configured "
          "lookahead of fourteen days, determines whether the number of days remaining "
          "matches one of the event's offsets, and for each subscriber not already "
          "notified for that combination renders the template and dispatches the message, "
          "retrying up to three times with a linearly increasing delay before recording "
          "the attempt as failed. Every attempt is recorded. The cycle is additionally "
          "exposed as an internal endpoint for on-demand execution during testing."),

    ("h3", "4.5.11", "Dashboard Module"),
    ("p", "Provides the administrative interface described in Section 4.6, comprising a "
          "view for each of the modules above, built on a shared set of presentational "
          "components and a shared client for the server interface."),

    ("h2", "4.6", "Interface Design"),
    ("p", "The dashboard presents each module through a consistent layout: a sidebar "
          "for navigation between modules, a filter region above a data table, and modal "
          "forms for creation and amendment. Where a module is term-scoped, a term "
          "selector is present and its selection persists across views, so that an "
          "operator working within a semester does not reselect it in every module. "
          "Errors returned by the server are displayed verbatim, since the service layer "
          "composes them to be meaningful to an operator: a rejected timetable slot "
          "names the conflicting booking, and a rejected assessment states the total "
          "weight that would have resulted."),
    ("p", "The figures below present the principal views of the dashboard. They are to "
          "be captured from the running system and inserted here."),
    ("figure_placeholder", "4.1", "Dashboard landing view"),
    ("figure_placeholder", "4.2", "Academic terms view, showing the current term"),
    ("figure_placeholder", "4.3", "Student register with programme and level filters"),
    ("figure_placeholder", "4.4", "Student registration form"),
    ("figure_placeholder", "4.5", "Course catalogue view"),
    ("figure_placeholder", "4.6", "Enrolment view for a selected term"),
    ("figure_placeholder", "4.7", "Timetable view showing weekly class sessions"),
    ("figure_placeholder", "4.8", "Room clash rejection message"),
    ("figure_placeholder", "4.9", "Attendance register marking view"),
    ("figure_placeholder", "4.10", "Attendance summary showing rates per student"),
    ("figure_placeholder", "4.11", "Assessment definition view showing the weight budget"),
    ("figure_placeholder", "4.12", "Bulk score entry view"),
    ("figure_placeholder", "4.13", "Course results with letter grades and grade points"),
    ("figure_placeholder", "4.14", "Student transcript view showing the grade point average"),
    ("figure_placeholder", "4.15", "Fee structure definition view"),
    ("figure_placeholder", "4.16", "Billing run result showing invoices created and students skipped"),
    ("figure_placeholder", "4.17", "Invoice and payment recording view"),
    ("figure_placeholder", "4.18", "Event creation form showing reminder offsets"),
    ("figure_placeholder", "4.19", "Rendered notification email as received"),
    ("figure_placeholder", "4.20", "Interactive interface documentation"),

    ("h2", "4.7", "Explanation of Key Code Modules"),

    ("h3", "4.7.1", "Layer Composition through Dependency Injection"),
    ("p", "The dependency module composes the layer stack for every request. A factory "
          "function constructs a repository from a request-scoped database session, and a "
          "second constructs each service from that repository. These are bound to "
          "annotated type aliases, so that an endpoint declares its dependency by type "
          "and the framework supplies the fully composed object. Listing 4.1 shows the "
          "pattern for the school service."),
    ("code", "Listing 4.1", "Composition of the layer stack (app/dependencies.py)",
     """def get_school_repository(
    session: Session = Depends(get_session),
) -> SchoolRepository:
    return SchoolRepository(session=session)


def get_school_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> SchoolService:
    return SchoolService(repository=repository)


SchoolServiceDep = Annotated[SchoolService, Depends(get_school_service)]"""),
    ("p", "The consequence is visible in the router. Listing 4.2 shows two endpoints in "
          "full; each declares its dependency, delegates, and returns. There is no "
          "session handling, no validation and no error handling, because each of those "
          "belongs to a different layer. This is what makes the claim of NFR-04 concrete: "
          "there is no rule in the router that a second client could bypass, because "
          "there is no rule in the router at all."),
    ("code", "Listing 4.2", "Router endpoints delegating to the service (app/routers/students.py)",
     """@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, service: SchoolServiceDep):
    return service.create_student(payload)


@router.get("", response_model=list[StudentRead])
def list_students(
    service: SchoolServiceDep,
    program: str | None = None,
    level: int | None = None,
    student_status: StudentStatus | None = Query(default=None, alias="status"),
    search: str | None = None,
):
    return service.list_students(
        program=program, level=level, status=student_status, search=search
    )"""),

    ("h3", "4.7.2", "Domain Exceptions and Status Code Mapping"),
    ("p", "The services signal refusal by raising one of two domain exceptions, which "
          "carry no knowledge of the transport. Two application-wide handlers translate "
          "them, as shown in Listing 4.3. This implements NFR-03 in nine lines for the "
          "entire system: every endpoint of every module returns 404 for a missing "
          "resource and 409 for a rule violation, without any endpoint containing "
          "status-code logic, and a service may be exercised in a unit test without a "
          "web context."),
    ("code", "Listing 4.3", "Domain exception handlers (app/main.py)",
     """@app.exception_handler(ResourceNotFoundError)
async def handle_resource_not_found(_request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(ResourceConflictError)
async def handle_resource_conflict(_request: Request, exc: ResourceConflictError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )"""),

    ("h3", "4.7.3", "The Idempotency Guard in the Notification Cycle"),
    ("p", "Listing 4.4 shows the core of the dispatch loop. The guard is the first "
          "statement inside the loop over subscribers, before any rendering or "
          "transport, so a duplicate costs a single indexed lookup. Because the dispatch "
          "record is written after each attempt, and because the uniqueness constraint of "
          "Table 4.2 backs the check at the database level, the guarantee of FR-24 holds "
          "across restarts of the application and would hold even if the check in the "
          "service were removed."),
    ("code", "Listing 4.4", "Idempotency guard and dispatch recording "
                            "(app/services/notification_service.py)",
     """for subscriber in subscribers:
    if self.repository.has_dispatch(
        event_id=event.id,
        recipient_email=subscriber.email,
        channel=self.email_channel.channel_name,
        days_before=days_remaining,
        scheduled_for=event_date,
    ):
        continue

    context = {
        "student_name": subscriber.full_name,
        "event_title": event.title,
        "body": event.body,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "days_remaining": days_remaining,
    }
    html_body = self.renderer.render(event.email_template, context)
    subject = self._build_subject(event.title, days_remaining)

    try:
        await self._send_with_retry(
            subject=subject, recipient=subscriber.email, html_body=html_body
        )
    except Exception as exc:
        logger.exception(...)
        self.repository.record_dispatch(..., status="failed",
                                        error_message=str(exc))
        continue

    self.repository.record_dispatch(..., status="sent")"""),

    ("h3", "4.7.4", "The Weighted Result Computation"),
    ("p", "Listing 4.5 shows the accumulation and normalisation described in Section "
          "3.6.2. Two accumulators are maintained per enrolment: the weighted marks "
          "earned, and the assessment weight those marks account for. Assessments with a "
          "non-positive maximum or weight are skipped, which prevents a division by zero "
          "and excludes an assessment that has been defined but not weighted."),
    ("code", "Listing 4.5", "Weighted result computation (app/services/grading_service.py)",
     """earned: dict[UUID, float] = {}
graded_weight: dict[UUID, float] = {}
for score, assessment in scored:
    if assessment.max_score <= 0 or assessment.weight <= 0:
        continue
    fraction = float(score.score) / float(assessment.max_score)
    weight = float(assessment.weight)
    earned[score.enrollment_id] = (
        earned.get(score.enrollment_id, 0.0) + fraction * weight
    )
    graded_weight[score.enrollment_id] = (
        graded_weight.get(score.enrollment_id, 0.0) + weight
    )

for enrollment, student, course, _term in rows:
    covered = graded_weight.get(enrollment.id, 0.0)
    points = earned.get(enrollment.id, 0.0)
    # Normalise over the weight actually graded so partial terms still rank.
    percentage = round(points / covered * 100, 2) if covered else 0.0
    letter, grade_point = grade_for(percentage)"""),

    ("h3", "4.7.5", "The Channel Abstraction"),
    ("p", "The delivery channel is declared as an interface with a name and an "
          "asynchronous send operation, and the orchestrator is constructed with an "
          "instance of it rather than with a concrete mail client. This implements "
          "NFR-05: adding a short-message channel requires a new implementation of the "
          "interface and a change to composition, and no change to the logic that "
          "decides what is sent and to whom. It also makes the orchestrator testable, "
          "since a test may supply a channel that records its calls instead of "
          "transmitting."),

    ("h3", "4.7.6", "Application Lifespan and Scheduler Management"),
    ("p", "The scheduler is bound to the application lifespan, as shown in Listing 4.6, "
          "so that it starts when the application starts and is shut down when the "
          "application stops. The job is configured to permit at most one concurrent "
          "instance, to coalesce executions missed while the application was stopped "
          "into a single execution, and to allow a grace period within which a delayed "
          "execution may still run. The first of these prevents a slow cycle from "
          "overlapping the next; the second prevents a backlog of executions after a "
          "restart; and the idempotency guard of Section 4.7.3 makes all three safe."),
    ("code", "Listing 4.6", "Scheduler lifecycle bound to the application (app/main.py)",
     """@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = SchedulerService(
        notification_job=run_notification_cycle,
        settings=notification_settings,
    )
    scheduler.start()
    app.state.scheduler = scheduler
    logger.info("Application startup complete")
    yield
    scheduler.shutdown()
    logger.info("Application shutdown complete")"""),

    ("h2", "4.8", "Test Plan and Test Cases"),
    ("p", "The test cases below implement the plan of Section 3.8. They are grouped by "
          "module, and each is traced to the requirement it verifies. Cases whose "
          "identifier is marked with an asterisk supply deliberately invalid input; a "
          "pass for such a case means that the system correctly refused the operation "
          "and persisted no part of it."),
    ("p", "The Result column of each table is to be completed from the observed "
          "behaviour of the running system, and the evidence of execution reproduced in "
          "Appendix E."),

    ("h3", "4.8.1", "Academic Term, Student and Course Test Cases"),
    ("test_table", "4.3", "Test cases for the term, student and course modules",
     [
         ["TC-01", "FR-01", "Create a term with valid dates and mark it current", "Term created; HTTP 201; retrievable as the current term"],
         ["TC-02*", "FR-01", "Create a term whose end date precedes its start date", "Rejected; HTTP 409; no term created"],
         ["TC-03*", "FR-01", "Create a term with a name already in use", "Rejected; HTTP 409"],
         ["TC-04*", "FR-21", "Delete a term that has enrolments", "Rejected; HTTP 409; term and enrolments intact"],
         ["TC-05", "FR-02", "Register a student with a unique index number and email", "Student created; HTTP 201"],
         ["TC-06*", "FR-02", "Register a second student with an index number already in use", "Rejected; HTTP 409"],
         ["TC-07*", "FR-02", "Register a second student with an email already in use", "Rejected; HTTP 409"],
         ["TC-08", "FR-03", "Register a student whose email matches an existing subscriber", "Student created and automatically linked to that subscriber"],
         ["TC-09", "FR-02", "List students filtered by programme and level", "Only students matching both filters returned"],
         ["TC-10*", "FR-21", "Delete a student who has enrolments", "Rejected; HTTP 409"],
         ["TC-11*", "FR-21", "Delete a student who has invoices", "Rejected; HTTP 409"],
         ["TC-12", "FR-04", "Create a course with a unique code", "Course created; HTTP 201"],
         ["TC-13*", "FR-04", "Create a course with a code already in use", "Rejected; HTTP 409"],
         ["TC-14", "FR-04", "Deactivate a course", "Course marked inactive; record retained"],
         ["TC-15*", "FR-21", "Delete a course that has enrolments", "Rejected; HTTP 409"],
     ]),

    ("h3", "4.8.2", "Enrolment and Timetable Test Cases"),
    ("test_table", "4.4", "Test cases for the enrolment and timetable modules",
     [
         ["TC-16", "FR-05", "Enrol an active student in an active course for a term", "Enrolment created; HTTP 201"],
         ["TC-17*", "FR-05", "Enrol the same student in the same course and term again", "Rejected; HTTP 409; exactly one enrolment remains"],
         ["TC-18", "FR-05", "Enrol the same student in the same course in a different term", "Second enrolment created; both retained"],
         ["TC-19*", "FR-05", "Enrol a student in an inactive course", "Rejected; HTTP 409"],
         ["TC-20", "FR-05", "Set an enrolment status to dropped", "Status updated; enrolment excluded from results"],
         ["TC-21", "FR-06", "Create a class session with valid times and a free room", "Session created; HTTP 201"],
         ["TC-22*", "FR-06", "Create a class session whose end time precedes its start time", "Rejected; HTTP 409"],
         ["TC-23*", "FR-07", "Book a room already occupied for an overlapping period on the same day", "Rejected; HTTP 409; message names the conflicting booking and its times"],
         ["TC-24", "FR-07", "Book a room immediately after an existing booking ends", "Accepted; adjacent sessions permitted"],
         ["TC-25", "FR-07", "Book the same room at the same time on a different day", "Accepted"],
         ["TC-26", "FR-07", "Create a session with no room specified overlapping another", "Accepted; unallocated sessions cannot clash"],
     ]),

    ("h3", "4.8.3", "Attendance Test Cases"),
    ("test_table", "4.5", "Test cases for the attendance module",
     [
         ["TC-27", "FR-08", "Mark a full register for a sitting in one submission", "All entries recorded; HTTP 201"],
         ["TC-28", "FR-09", "Re-mark the same sitting with corrected statuses", "Existing entries updated; entry count unchanged"],
         ["TC-29*", "FR-08", "Submit a register naming an enrolment from another course", "Whole submission rejected; HTTP 409; no entry persisted"],
         ["TC-30*", "FR-08", "Submit a register naming the same enrolment twice", "Rejected; HTTP 409"],
         ["TC-31*", "FR-08", "Submit an empty register", "Rejected; HTTP 409"],
         ["TC-32", "FR-10", "Compute the summary for a student marked present, late and excused across sittings", "Attendance rate of 100 percent; all three statuses credited"],
         ["TC-33", "FR-10", "Compute the summary for a student marked absent for half of the sittings", "Attendance rate of 50 percent"],
         ["TC-34", "FR-10", "Compute the summary for a course with no register marked", "Empty summary; no division-by-zero error"],
     ]),

    ("h3", "4.8.4", "Grading Test Cases"),
    ("test_table", "4.6", "Test cases for the grading module",
     [
         ["TC-35", "FR-11", "Define assessments of 10, 20, 20 and 50 percent for a course-term", "All four created; total weight 100 percent"],
         ["TC-36*", "FR-12", "Define a further assessment of 10 percent for the same course-term", "Rejected; HTTP 409; message states the resulting total of 110 percent"],
         ["TC-37", "FR-12", "Amend an existing assessment's weight within the budget", "Accepted; the assessment's own weight not double-counted"],
         ["TC-38", "FR-13", "Record scores for a whole class in one submission", "All scores recorded; HTTP 201"],
         ["TC-39*", "FR-13", "Record a score exceeding the assessment maximum", "Rejected; HTTP 409; no score persisted"],
         ["TC-40", "FR-13", "Re-record a score for an enrolment already scored", "Existing score updated; no duplicate created"],
         ["TC-41*", "FR-13", "Record a score for an enrolment in a different course", "Rejected; HTTP 409"],
         ["TC-42", "FR-14", "Compute results when all assessments are graded", "Weighted percentage equals the conventional weighted average"],
         ["TC-43", "FR-14", "Compute results with only the 10 and 20 percent assessments graded, both at full marks", "Percentage of 100.00; graded weight reported as 30.00"],
         ["TC-44", "FR-14", "Compute results for a student with no scores recorded", "Percentage of 0.00; graded weight of 0.00; no error"],
         ["TC-45", "FR-14", "Verify grade boundaries at 80, 75, 70, 65, 60, 55 and 50 percent", "Letters A, B+, B, C+, C, D+ and D respectively"],
         ["TC-46", "FR-14", "Verify a percentage below 50", "Letter F; grade point 0.0"],
         ["TC-47", "FR-15", "Compute the grade point average for a student in a term", "Credit-weighted mean of the grade points of the courses taken"],
         ["TC-48", "FR-14", "Compute results for a course in which one enrolment is dropped", "Dropped enrolment excluded from the result set"],
     ]),

    ("h3", "4.8.5", "Fees and Billing Test Cases"),
    ("test_table", "4.7", "Test cases for the fees and billing module",
     [
         ["TC-49", "FR-16", "Define a fee structure targeted at a programme and level", "Structure created; HTTP 201"],
         ["TC-50", "FR-17", "Run billing on that structure", "One invoice issued to each matching active student; counts reported"],
         ["TC-51", "FR-17", "Run billing on the same structure a second time", "No new invoice created; every student reported as skipped"],
         ["TC-52", "FR-17", "Run billing on a structure targeted at a level only", "Invoices issued to matching students across all programmes at that level"],
         ["TC-53", "FR-17", "Verify that non-active students are not billed", "Deferred, suspended, graduated and withdrawn students receive no invoice"],
         ["TC-54", "FR-18", "Record a partial payment against an invoice", "Payment recorded; invoice status becomes partial"],
         ["TC-55", "FR-18", "Record the balancing payment", "Invoice status becomes paid"],
         ["TC-56*", "FR-18", "Record a payment exceeding the outstanding balance", "Rejected; HTTP 409; no payment persisted"],
         ["TC-57*", "FR-19", "Void an invoice against which a payment has been recorded", "Rejected; HTTP 409"],
         ["TC-58", "FR-19", "Void an invoice with no payments", "Invoice status becomes void"],
         ["TC-59*", "FR-19", "Record a payment against a voided invoice", "Rejected; HTTP 409"],
         ["TC-60", "FR-20", "Compute a student's balance across several invoices and payments", "Total invoiced, total paid and outstanding amount all correct"],
     ]),

    ("h3", "4.8.6", "Notification Test Cases"),
    ("test_table", "4.8", "Test cases for the notification module",
     [
         ["TC-61", "FR-22", "Create an event with offsets of 7, 3, 1 and 0 days", "Event created; HTTP 201"],
         ["TC-62*", "FR-22", "Create an event naming a template outside the permitted set", "Rejected; HTTP 422"],
         ["TC-63", "FR-23", "Run the cycle with an event exactly 7 days away", "Reminder dispatched to every subscriber"],
         ["TC-64", "FR-23", "Run the cycle with an event 5 days away and no matching offset", "No reminder dispatched"],
         ["TC-65", "FR-24", "Run the cycle a second time with the same event 7 days away", "No further reminder dispatched; dispatch count unchanged"],
         ["TC-66", "FR-23", "Run the cycle with the same event 3 days away", "A new reminder dispatched for the 3-day offset"],
         ["TC-67", "FR-23", "Run the cycle with an event whose start date has passed", "No reminder dispatched"],
         ["TC-68", "FR-23", "Run the cycle with an event beyond the 14-day lookahead", "Event not considered"],
         ["TC-69", "FR-22", "Run the cycle with an event that has no offsets configured", "Institutional default offsets of 7, 3, 1 and 0 applied"],
         ["TC-70", "FR-23", "Run the cycle with a deactivated event", "No reminder dispatched"],
         ["TC-71", "FR-25", "Run the cycle with the mail transport unreachable", "Dispatch recorded with status failed and the error message retained"],
         ["TC-72", "FR-26", "Observe behaviour on a transport failure", "Three attempts made with increasing delay before the failure is recorded"],
         ["TC-73", "FR-23", "Inspect a delivered message", "Recipient name, event title, body, dates and days remaining correctly rendered"],
         ["TC-74", "FR-23", "Verify the subject line at 0, 1 and several days remaining", "Subject reads 'Happening Today', 'starts tomorrow' and 'starts in N days' respectively"],
     ]),

    ("h3", "4.8.7", "Cross-Cutting and Interface Test Cases"),
    ("test_table", "4.9", "Cross-cutting test cases",
     [
         ["TC-75", "NFR-03", "Request a resource that does not exist in each module", "HTTP 404 with a descriptive message in every case"],
         ["TC-76", "NFR-03", "Submit a structurally invalid request body", "HTTP 422 with the offending field identified"],
         ["TC-77", "NFR-03", "Submit a request violating a domain rule in each module", "HTTP 409 with a descriptive message in every case"],
         ["TC-78", "NFR-01", "Execute every idempotent operation twice", "State after the second execution identical to that after the first"],
         ["TC-79", "NFR-02", "Attempt a duplicate insertion bypassing the service check", "Database constraint rejects the insertion"],
         ["TC-80", "NFR-08", "Inspect the stored representation of a user password", "Only an Argon2 hash present; no plain text; hash absent from all responses"],
         ["TC-81", "NFR-06", "Attempt a rejected operation through the dashboard", "Reason displayed to the operator in intelligible terms"],
         ["TC-82", "NFR-09", "Build the dashboard and serve it from the application process", "Dashboard served correctly by the single process"],
     ]),

    ("h2", "4.9", "Test Results"),
    ("p", "The tables in this section record the outcome of executing the test cases of "
          "Section 4.8. Each is to be completed with the behaviour actually observed."),
    ("results_table", "4.10", "Test results by module",
     [
         ["Academic terms", "TC-01 to TC-04", "4", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Student records", "TC-05 to TC-11", "7", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Course catalogue", "TC-12 to TC-15", "4", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Enrolment", "TC-16 to TC-20", "5", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Timetable", "TC-21 to TC-26", "6", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Attendance", "TC-27 to TC-34", "8", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Grading", "TC-35 to TC-48", "14", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Fees and billing", "TC-49 to TC-60", "12", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Notifications", "TC-61 to TC-74", "14", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Cross-cutting", "TC-75 to TC-82", "8", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
         ["Total", "TC-01 to TC-82", "82", "[FILL IN]", "[FILL IN]", "[FILL IN]"],
     ]),
    ("p", "The outcome of each individual test case is recorded in the Result column of "
          "Tables 4.3 to 4.9. Evidence of execution is reproduced in Appendix E."),
    ("p", "Any test case that failed on first execution should be discussed here, "
          "stating the defect it revealed, the change made in response, and the outcome "
          "on re-execution. A report in which every case passed at the first attempt "
          "invites the question of whether the tests were capable of failing; the "
          "defects found and fixed are evidence that they were."),

    ("h2", "4.10", "System Performance Results"),
    ("p", "Response times were measured on the development machine specified in Table "
          "4.1, against the synthetic dataset of Section 3.7, with the database on the "
          "same host. The figures below therefore exclude network latency and represent "
          "server processing time. Each measurement is to be taken as the mean of ten "
          "consecutive executions after an initial warm-up execution."),
    ("perf_table", "4.12", "Measured response times for representative operations",
     [
         ["Register a student", "FR-02", "[FILL IN]"],
         ["List 100 students with filters applied", "FR-02", "[FILL IN]"],
         ["Enrol a student in a course", "FR-05", "[FILL IN]"],
         ["Create a class session with clash detection", "FR-07", "[FILL IN]"],
         ["Mark a register of 50 students", "FR-08", "[FILL IN]"],
         ["Compute the attendance summary for a course of 50 students", "FR-10", "[FILL IN]"],
         ["Record 50 scores in one submission", "FR-13", "[FILL IN]"],
         ["Compute course results for 50 students across 4 assessments", "FR-14", "[FILL IN]"],
         ["Compute a student transcript and grade point average", "FR-15", "[FILL IN]"],
         ["Run billing across 100 matching students", "FR-17", "[FILL IN]"],
         ["Re-run the same billing (all skipped)", "FR-17", "[FILL IN]"],
         ["Record a payment", "FR-18", "[FILL IN]"],
         ["Execute one notification cycle over 100 subscribers", "FR-23", "[FILL IN]"],
         ["Re-execute the same cycle (all suppressed)", "FR-24", "[FILL IN]"],
     ]),
    ("p", "Two comparisons in this table carry analytical weight and should be "
          "commented on once the figures are obtained. The first is the difference "
          "between the initial billing run and its repetition, which shows the cost of "
          "the idempotency check relative to the cost of the work it avoids. The second "
          "is the same comparison for the notification cycle, where the suppressed run "
          "performs an indexed lookup per subscriber and no rendering or transport at "
          "all, and should therefore be substantially faster than the run that "
          "dispatches."),

    ("h2", "4.11", "Evaluation of the System"),
    ("p", "The system was evaluated against the requirements of Section 3.3. Table 4.13 "
          "records, for each functional requirement, the module implementing it and the "
          "test cases verifying it, and is to be completed with the status observed."),
    ("traceability_table", "4.13", "Requirements traceability and verification status"),
    ("p", "Table 4.14 records the assessment of the non-functional requirements, which "
          "are evaluated by inspection and measurement rather than by discrete test "
          "cases."),
    ("nfr_table", "4.14", "Assessment of non-functional requirements",
     [
         ["NFR-01", "Idempotency of repeated operations", "TC-51, TC-28, TC-40, TC-65, TC-78", "[FILL IN]"],
         ["NFR-02", "Invariants enforced in service and database", "TC-79 and all cases marked with an asterisk", "[FILL IN]"],
         ["NFR-03", "Correct status code semantics", "TC-75, TC-76, TC-77", "[FILL IN]"],
         ["NFR-04", "Rules implemented once in the service layer", "Code inspection: routers contain no domain logic", "[FILL IN]"],
         ["NFR-05", "Channel extensibility", "Code inspection: orchestrator depends on the channel interface only", "[FILL IN]"],
         ["NFR-06", "Usability of the dashboard", "TC-81; user acceptance testing", "[FILL IN]"],
         ["NFR-07", "Interactive operations within two seconds", "Table 4.12", "[FILL IN]"],
         ["NFR-08", "Credential and secret handling", "TC-80; inspection of the repository for secrets", "[FILL IN]"],
         ["NFR-09", "Single-process deployment", "TC-82", "[FILL IN]"],
         ["NFR-10", "Auditability of dispatches and payments", "TC-71, TC-60", "[FILL IN]"],
     ]),
    ("p", "Beyond the requirement-by-requirement assessment, the system was evaluated "
          "against the four gaps identified in Section 2.6. The integration of academic "
          "and financial concerns is realised in the billing run, which targets students "
          "by the academic attributes of programme and level held in the same database "
          "as their enrolments and results, and therefore requires no reconciliation "
          "between an academic and a financial system. The treatment of notification as "
          "an automated rather than a manual act is realised in the scheduled cycle and "
          "evidenced by the dispatch history, which records what was sent to whom and "
          "when. The single-sourcing of validation logic is realised in the service "
          "layer and evidenced by the routers, which contain no domain logic and could "
          "not therefore be bypassed by a second client. Term scoping is realised in the "
          "data model and evidenced by test case TC-18, in which the same student is "
          "enrolled in the same course in two terms and both records are retained and "
          "independently gradeable."),
    ("p", "The evaluation also identified where the system falls short. The limitations "
          "of Section 1.8 remain: authorisation is not yet enforced per role on the "
          "school-management endpoints; the system has not been operated over a complete "
          "semester with real data; and the notification subsystem was exercised through "
          "controlled invocation rather than over a genuine multi-week period. These are "
          "discussed further in Chapter Five."),
]
