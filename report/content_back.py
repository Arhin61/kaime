"""References and Appendices."""

REFERENCES = [
    ("chapter_single", "REFERENCES"),
    ("note", "NOTE TO THE AUTHOR — DELETE THIS BOX BEFORE SUBMISSION. The works below "
             "are real and checkable. Verify every entry against the actual publication "
             "before submitting, and remove any work you have not read enough of to "
             "defend in the viva. Chapters One, Two and Five additionally contain "
             "[SOURCE NEEDED] markers where an empirical claim about institutional "
             "practice requires a citation that you must find yourself. Do not invent "
             "references to fill those markers; either locate a genuine source or soften "
             "the claim until it no longer needs one."),
    ("ref", "Beck, K., Beedle, M., van Bennekum, A., Cockburn, A., Cunningham, W., "
            "Fowler, M., Grenning, J., Highsmith, J., Hunt, A., Jeffries, R., Kern, J., "
            "Marick, B., Martin, R. C., Mellor, S., Schwaber, K., Sutherland, J., & "
            "Thomas, D. (2001). Manifesto for agile software development. "
            "https://agilemanifesto.org"),
    ("ref", "Chen, P. P.-S. (1976). The entity-relationship model: Toward a unified view "
            "of data. ACM Transactions on Database Systems, 1(1), 9-36. "
            "https://doi.org/10.1145/320434.320440"),
    ("ref", "Codd, E. F. (1970). A relational model of data for large shared data banks. "
            "Communications of the ACM, 13(6), 377-387. "
            "https://doi.org/10.1145/362384.362685"),
    ("ref", "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user "
            "acceptance of information technology. MIS Quarterly, 13(3), 319-340. "
            "https://doi.org/10.2307/249008"),
    ("ref", "Evans, E. (2003). Domain-driven design: Tackling complexity in the heart of "
            "software. Addison-Wesley."),
    ("ref", "Fielding, R. T. (2000). Architectural styles and the design of "
            "network-based software architectures [Doctoral dissertation, University of "
            "California, Irvine]. "
            "https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm"),
    ("ref", "Fowler, M. (2002). Patterns of enterprise application architecture. "
            "Addison-Wesley."),
    ("ref", "Helland, P. (2012). Idempotence is not a medical condition. ACM Queue, "
            "10(4), 30-46. https://doi.org/10.1145/2181796.2187821"),
    ("ref", "Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in "
            "information systems research. MIS Quarterly, 28(1), 75-105. "
            "https://doi.org/10.2307/25148625"),
    ("ref", "Meta Open Source. (2024). React documentation. https://react.dev"),
    ("ref", "Nielsen, J. (1994). Usability engineering. Morgan Kaufmann."),
    ("ref", "Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A "
            "design science research methodology for information systems research. "
            "Journal of Management Information Systems, 24(3), 45-77. "
            "https://doi.org/10.2753/MIS0742-1222240302"),
    ("ref", "PostgreSQL Global Development Group. (2024). PostgreSQL documentation. "
            "https://www.postgresql.org/docs/"),
    ("ref", "Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A "
            "practitioner's approach (9th ed.). McGraw-Hill Education."),
    ("ref", "Ramirez, S. (2024). FastAPI documentation. https://fastapi.tiangolo.com"),
    ("ref", "Ramirez, S. (2024). SQLModel documentation. https://sqlmodel.tiangolo.com"),
    ("ref", "Richardson, C. (2018). Microservices patterns: With examples in Java. "
            "Manning Publications."),
    ("ref", "Sommerville, I. (2016). Software engineering (10th ed.). Pearson Education."),
    ("ref", "Grondahl Larsen, A. (2024). APScheduler documentation. "
            "https://apscheduler.readthedocs.io"),
    ("note", "ADD YOUR OWN SOURCES HERE. At minimum you should add: (a) one or more "
             "studies on school or student management information systems and their "
             "adoption, cited in Section 2.2.1; (b) evidence on record-keeping practice "
             "in Ghanaian or West African tertiary institutions, cited in Section 1.1; "
             "(c) evidence on students missing deadlines through poor institutional "
             "communication, cited in Section 1.1; (d) a comparative evaluation of "
             "open-source student information systems, cited in Section 2.3.2; (e) a "
             "study of institutional communication channels, cited in Section 2.3.4; and "
             "(f) evidence on mobile telephone versus electronic mail reach among "
             "students, cited in Section 5.11. Order the complete list alphabetically by "
             "author surname and apply a hanging indent throughout."),
]


APPENDICES = [
    ("chapter_single", "APPENDICES"),

    ("h1", "APPENDIX A: SYSTEM SOURCE CODE"),
    ("p", "The complete source code of the system is available in the accompanying "
          "repository. This appendix reproduces the modules most directly supporting the "
          "claims made in Chapters Three and Four. Listings 4.1 to 4.6 in the body of "
          "the report are not repeated here."),
    ("appendix_code_list", "", "", [
        ["app/models.py", "All fifteen table definitions, including the uniqueness constraints of Table 4.2."],
        ["app/schemas.py", "Request and response models, including the enumerations restricting status, kind, method and template values."],
        ["app/dependencies.py", "Composition of the router, service and repository layers through dependency injection."],
        ["app/main.py", "Application assembly, domain exception handlers, scheduler lifespan and dashboard mounting."],
        ["app/repositories/school_repository.py", "Data access for the school-management domain."],
        ["app/services/school_service.py", "Terms, students, courses, enrolment and timetabling, including room clash detection."],
        ["app/services/attendance_service.py", "Register marking and attendance rate computation."],
        ["app/services/grading_service.py", "Assessments, scores, weighted results, the grade scale and grade point average."],
        ["app/services/finance_service.py", "Fee structures, the idempotent billing run, invoices and payments."],
        ["app/services/notification_service.py", "The dispatch cycle, offset resolution, retry policy and idempotency guard."],
        ["app/services/scheduler_service.py", "APScheduler configuration and lifecycle."],
        ["app/services/channels/base.py", "The notification channel interface."],
        ["app/services/channels/email.py", "The electronic mail channel implementation."],
        ["app/services/exceptions.py", "The two domain exceptions."],
        ["alembic/versions/", "The seven migration scripts recording the evolution of the schema."],
        ["frontend/src/pages/", "The dashboard views, one per module."],
    ]),
    ("note", "Insert the source listings you wish to reproduce after this table, or "
             "state here where the complete repository may be obtained. Include at "
             "minimum app/models.py and the four school-domain service modules, since "
             "these carry the invariants the report claims. Set all code in a monospaced "
             "font and reduce the point size if necessary to preserve line breaks."),

    ("h1", "APPENDIX B: APPLICATION PROGRAMMING INTERFACE ENDPOINTS"),
    ("p", "The endpoints exposed by the system are listed below by module. Interactive "
          "documentation generated from the interface specification is available at the "
          "documentation path of a running instance."),
    ("api_table", "", "", [
        ["Subscribers", "POST /dashboard/subscribers\nGET /dashboard/subscribers\nGET /dashboard/subscribers/{email}\nPATCH /dashboard/subscribers/{email}\nDELETE /dashboard/subscribers/{email}"],
        ["Events", "POST /dashboard/events\nGET /dashboard/events\nGET /dashboard/events/{event_id}\nPATCH /dashboard/events/{event_id}\nPATCH /dashboard/events/{event_id}/activate\nPATCH /dashboard/events/{event_id}/deactivate\nDELETE /dashboard/events/{event_id}"],
        ["Academic terms", "POST /dashboard/terms\nGET /dashboard/terms\nGET /dashboard/terms/current\nGET /dashboard/terms/{term_id}\nPATCH /dashboard/terms/{term_id}\nDELETE /dashboard/terms/{term_id}"],
        ["Students", "POST /dashboard/students\nGET /dashboard/students\nGET /dashboard/students/by-index/{index_number}\nGET /dashboard/students/{student_id}\nPATCH /dashboard/students/{student_id}\nDELETE /dashboard/students/{student_id}\nGET /dashboard/students/{student_id}/enrollments\nGET /dashboard/students/{student_id}/results?term_id=\nGET /dashboard/students/{student_id}/balance"],
        ["Courses", "POST /dashboard/courses\nGET /dashboard/courses\nGET /dashboard/courses/{course_id}\nPATCH /dashboard/courses/{course_id}\nDELETE /dashboard/courses/{course_id}\nPATCH /dashboard/courses/{course_id}/activate\nPATCH /dashboard/courses/{course_id}/deactivate\nGET /dashboard/courses/{course_id}/roster\nGET /dashboard/courses/{course_id}/results?term_id="],
        ["Enrolments", "POST /dashboard/enrollments\nGET /dashboard/enrollments\nPATCH /dashboard/enrollments/{enrollment_id}\nDELETE /dashboard/enrollments/{enrollment_id}"],
        ["Timetable", "POST /dashboard/timetable\nGET /dashboard/timetable\nPATCH /dashboard/timetable/{session_id}\nDELETE /dashboard/timetable/{session_id}"],
        ["Attendance", "POST /dashboard/attendance\nGET /dashboard/attendance\nGET /dashboard/attendance/summary?course_id=&term_id=\nDELETE /dashboard/attendance/{record_id}"],
        ["Grades", "POST /dashboard/grades/assessments\nGET /dashboard/grades/assessments\nPATCH /dashboard/grades/assessments/{assessment_id}\nDELETE /dashboard/grades/assessments/{assessment_id}\nPOST /dashboard/grades/scores\nGET /dashboard/grades/assessments/{assessment_id}/scores"],
        ["Fees", "POST /dashboard/fees/structures\nGET /dashboard/fees/structures\nPATCH /dashboard/fees/structures/{structure_id}\nDELETE /dashboard/fees/structures/{structure_id}\nPOST /dashboard/fees/structures/{structure_id}/bill\nPOST /dashboard/fees/invoices\nGET /dashboard/fees/invoices\nGET /dashboard/fees/invoices/{invoice_id}\nDELETE /dashboard/fees/invoices/{invoice_id}\nPATCH /dashboard/fees/invoices/{invoice_id}/void\nPOST /dashboard/fees/payments\nGET /dashboard/fees/invoices/{invoice_id}/payments"],
        ["Internal", "POST /internal/notifications/run"],
    ]),

    ("h1", "APPENDIX C: CONFIGURATION PARAMETERS"),
    ("p", "The behaviour of the notification subsystem is governed by the configuration "
          "parameters listed below, supplied through environment variables. The default "
          "values are those in force during the evaluation reported in Chapter Four."),
    ("config_table", "", "", [
        ["NOTIFICATION_SCAN_INTERVAL_MINUTES", "30", "Interval at which the scheduler executes the dispatch cycle."],
        ["NOTIFICATION_LOOKAHEAD_DAYS", "14", "How far ahead the cycle looks for events warranting a reminder."],
        ["NOTIFICATION_DEFAULT_OFFSETS", "7, 3, 1, 0", "Reminder offsets applied to an event declaring none of its own."],
        ["NOTIFICATION_MAX_RETRIES", "3", "Attempts made before a dispatch is recorded as failed."],
        ["NOTIFICATION_RETRY_BACKOFF_SECONDS", "3", "Base delay between attempts; the delay increases linearly with the attempt number."],
        ["NOTIFICATION_TIMEZONE", "UTC", "Time zone in which the scheduler operates."],
        ["MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_FROM_NAME", "Site-specific", "Mail transport configuration."],
        ["MAIL_STARTTLS, MAIL_SSL_TLS, USE_CREDENTIALS, VALIDATE_CERTS", "true, false, true, true", "Transport security settings."],
        ["POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB", "Site-specific", "Database connection parameters."],
        ["JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES", "Site-specific", "Token signing and expiry configuration."],
    ]),
    ("p", "No secret value is committed to the source repository; all are supplied at "
          "deployment through the environment, as stated in Section 3.9.3."),

    ("h1", "APPENDIX D: WORK PLAN"),
    ("p", "The project was executed over one academic year according to the schedule "
          "below. Completed periods are to be shaded in the Gantt chart accompanying "
          "this table."),
    ("gantt_table", "", "", [
        ["Problem identification and topic approval", "<<Month>>", "<<Month>>", "Consultation with supervisor; scope agreed"],
        ["Literature review", "<<Month>>", "<<Month>>", "Chapter Two drafted"],
        ["Requirements elicitation", "<<Month>>", "<<Month>>", "Tables 3.1 to 3.3 produced"],
        ["System design", "<<Month>>", "<<Month>>", "Architecture, entity relationship diagram and algorithms"],
        ["Proposal submission and defence", "<<Month>>", "<<Month>>", "Proposal approved"],
        ["Increments 1 to 3: terms, students, courses", "<<Month>>", "<<Month>>", "Core register operational"],
        ["Increments 4 to 6: enrolment, timetable, attendance", "<<Month>>", "<<Month>>", "Clash detection and register marking operational"],
        ["Increments 7 to 8: grading, fees and billing", "<<Month>>", "<<Month>>", "Results computation and billing operational"],
        ["Increment 9: notification subsystem", "<<Month>>", "<<Month>>", "Scheduled dispatch operational"],
        ["Increment 10: dashboard integration", "<<Month>>", "<<Month>>", "All modules exposed through the interface"],
        ["Testing and evaluation", "<<Month>>", "<<Month>>", "Eighty-two test cases executed; defects resolved"],
        ["Report writing", "<<Month>>", "<<Month>>", "Chapters One to Five completed"],
        ["Similarity and AI checks; revision", "<<Month>>", "<<Month>>", "Thresholds satisfied"],
        ["Submission and oral defence", "<<Month>>", "<<Month>>", "Final submission"],
    ]),
    ("note", "Insert your Gantt chart here. The guidelines call for one explicitly. A "
             "horizontal bar chart with the fourteen activities above on the vertical "
             "axis and the months of the academic year on the horizontal axis is "
             "sufficient; it may be produced in a spreadsheet application and inserted "
             "as an image."),

    ("h1", "APPENDIX E: TEST CASE EXECUTION RECORD"),
    ("p", "The full record of test case execution, giving for each case the input "
          "supplied, the response received and the resulting database state, is "
          "reproduced here. Test cases and expected outcomes are stated in Section 4.8 "
          "and summarised results in Section 4.9."),
    ("note", "Insert your execution evidence here: screenshots of responses from the "
             "interactive interface documentation, terminal transcripts of requests made "
             "with curl, or a tabulated log. Evidence for the cases marked with an "
             "asterisk in Section 4.8 matters most, since these are the cases that "
             "demonstrate the invariants actually refusing invalid operations, which is "
             "the central claim of the report."),

    ("h1", "APPENDIX F: USER MANUAL"),
    ("p", "This appendix describes the installation and operation of the system."),
    ("h2", "F.1", "Installation"),
    ("code", "", "Installation and startup", """# 1. Obtain the source and copy the configuration template
cp .env.example ./.env
# Edit .env to supply database, mail and token settings

# 2. Apply the database migrations
uv run alembic upgrade head

# 3. Start the application server
uv run fastapi dev

# 4. Build the dashboard (served by the application process)
cd frontend
npm install
npm run build

# During development the dashboard may instead be run separately:
npm run dev

# 5. Trigger a notification cycle manually, without waiting for the scheduler
curl -X POST http://localhost:8000/internal/notifications/run"""),
    ("h2", "F.2", "Order of Operations"),
    ("p", "Because every academic record is scoped to a term, the system must be "
          "populated in dependency order. Create the academic term first and mark it "
          "current. Register students and create courses next; these are independent of "
          "each other. Enrol students in courses for the term, since enrolment requires "
          "all three. Timetable class sessions, define assessments and define fee "
          "structures, each of which requires a course or a term. Only then may "
          "registers be marked, scores recorded and billing run, since each of these "
          "requires an enrolment or a fee structure to exist. Subscribers and events may "
          "be created at any point, independently of the academic records."),
    ("h2", "F.3", "Operating Notes"),
    ("p", "A student whose electronic mail address matches an existing subscriber is "
          "linked to that subscriber automatically at registration; to have a student "
          "receive notifications, ensure the subscriber record exists first or that the "
          "addresses match."),
    ("p", "A course that is no longer offered should be deactivated rather than deleted, "
          "which preserves the historical records that depend on it. The same applies to "
          "an event that should stop generating reminders."),
    ("p", "A billing run may be repeated safely. Students already invoiced against the "
          "structure are skipped, and the response reports how many invoices were created "
          "and how many students were skipped."),
    ("p", "A register that was marked incorrectly should be re-submitted for the same "
          "sitting; the existing entries are updated rather than duplicated. The same "
          "applies to assessment scores."),
    ("p", "Where an operation is refused, the message returned states the reason. A "
          "refused timetable slot names the conflicting booking and its times; a refused "
          "assessment states the total weight that would have resulted; a refused "
          "deletion names the dependent records that must be cleared first."),
]
