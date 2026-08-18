# Kaime

Kaime is an academic platform with two halves: a **notification service** that
keeps students informed about university events, exams, and deadlines without
manual effort, and a **school management system** covering student records,
courses, enrollment, timetabling, attendance, grading, and fees.

The project has two parts:

- **Backend** — a FastAPI service (Python) that stores subscribers/events and
  school records in PostgreSQL and runs a background scheduler that dispatches
  notifications.
- **Frontend** — a React + Vite dashboard for managing everything above, built
  and served as static files by the backend.

## How it works

1. Staff create **events** (e.g. exam dates, registration deadlines) with a
   title, body, date range, and one or more notification offsets (how many
   days before the event a reminder should go out).
2. **Subscribers** (students) are registered with contact details.
3. A background scheduler periodically checks for due notifications, renders
   the appropriate Jinja2 email template, and dispatches it through a
   pluggable notification channel (email today; SMS/push can be added later).
4. Each dispatch is recorded to guarantee idempotency — a subscriber won't be
   notified twice for the same event/offset.

## School management

Everything in this module is scoped to an **academic term**, so the same course
can be run, graded and billed independently each semester.

- **Students** — records keyed by index number and email. When a student's email
  matches an existing subscriber, the record is automatically linked to that
  subscriber so notifications and academic records stay in step.
- **Courses & enrollment** — a course catalogue, plus enrollments that tie a
  student to a course for a term (one enrollment per student/course/term).
- **Timetable** — recurring weekly class slots per course. Booking the same room
  for overlapping times on the same day is rejected.
- **Attendance** — bulk register marking against a course sitting. Re-marking a
  sitting updates the earlier entry rather than duplicating it. Present, late
  and excused all count towards the attendance rate; absent does not.
- **Grades** — weighted assessments (quiz/assignment/midterm/project/exam) whose
  weights may not exceed 100% per course-term. Results normalise over the weight
  actually graded, so partial-term standings are still meaningful. The grade
  scale lives in `app/services/grading_service.py` (`GRADE_SCALE`) — edit that
  tuple to match your institution's scale.
- **Fees** — fee structures per term that can target a program and/or level.
  Running billing on a structure issues one invoice to every matching active
  student and is idempotent. Payments accumulate against an invoice and move it
  through unpaid → partial → paid; overpayment is rejected.

Records that other rows depend on cannot be deleted out from under them — a
student with enrollments or invoices, or a course with enrollments, assessments
or timetable slots, returns `409` until the dependents are cleared. Deleting an
enrollment does remove its attendance and scores.

### Layout

- `app/models.py` — all tables, including the school domain.
- `app/repositories/school_repository.py` — data access for the school domain.
- `app/services/school_service.py` — terms, students, courses, enrollment,
  timetable.
- `app/services/attendance_service.py` — register marking and summaries.
- `app/services/grading_service.py` — assessments, scores, results and GPA.
- `app/services/finance_service.py` — fee structures, invoices, payments.
- `app/services/exceptions.py` — shared `ResourceNotFoundError` /
  `ResourceConflictError`, mapped to `404` / `409` by handlers in `app/main.py`.

## Why APScheduler here?

APScheduler is the best fit for this service because reminders are time-based,
lightweight, and run inside the FastAPI process with no extra broker. It keeps
deployment simple while still supporting interval/cron jobs, concurrency
controls, and misfire handling.

For horizontal scaling or heavy queue workloads, migrate the
`NotificationChannel` pipeline to Celery workers later without changing the
orchestration contract.

## Tech stack

- **Backend**: FastAPI, SQLModel/SQLAlchemy, PostgreSQL, Alembic migrations,
  APScheduler, Jinja2 templates, fastapi-mail.
- **Frontend**: React 19, React Router, TypeScript, Vite, Tailwind CSS.

## Quick start

1. Copy config:

   ```bash
   cp .env.example ./.env
   ```

2. Start the API (backend):

   ```bash
   uv run fastapi dev
   ```

3. Run the dashboard (frontend), in a separate shell:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   build the frontend (`npm run build`) — the FastAPI app
   serves the resulting `frontend/dist` directory directly (see
   `app/main.py`).

## Notification architecture

- `app/services/notification_service.py` orchestrates due checks, rendering,
  retries, and idempotency.
- `app/services/scheduler_service.py` manages periodic execution with
  APScheduler.
- `app/services/channels/base.py` defines the channel contract for
  email/SMS/push extensibility.
- `app/services/channels/email.py` sends email notifications.
- `app/services/template_renderer.py` renders Jinja2 templates from
  `app/templates/`.
- `app/repositories/notification_repository.py` isolates data access and
  dispatch tracking.
- `app/main.py` wires scheduler startup/shutdown using FastAPI lifespan, and
  mounts the built frontend.

## Running a manual cycle

Use the internal endpoint to trigger processing immediately:

```bash
curl -X POST http://localhost:8000/internal/notifications/run
```

## API endpoints

- Subscribers:
  - `POST /dashboard/subscribers`
  - `GET /dashboard/subscribers`
  - `GET /dashboard/subscribers/{email}`
  - `PATCH /dashboard/subscribers/{email}`
  - `DELETE /dashboard/subscribers/{email}`
- Events:
  - `POST /dashboard/events`
  - `GET /dashboard/events`
  - `GET /dashboard/events/{event_id}`
  - `PATCH /dashboard/events/{event_id}`
  - `PATCH /dashboard/events/{event_id}/activate`
  - `PATCH /dashboard/events/{event_id}/deactivate`
  - `DELETE /dashboard/events/{event_id}`

- Academic terms:
  - `POST|GET /dashboard/terms`, `GET /dashboard/terms/current`
  - `GET|PATCH|DELETE /dashboard/terms/{term_id}`
- Students:
  - `POST|GET /dashboard/students`
  - `GET /dashboard/students/by-index/{index_number}`
  - `GET|PATCH|DELETE /dashboard/students/{student_id}`
  - `GET /dashboard/students/{student_id}/enrollments`
  - `GET /dashboard/students/{student_id}/results?term_id=`
  - `GET /dashboard/students/{student_id}/balance`
- Courses:
  - `POST|GET /dashboard/courses`
  - `GET|PATCH|DELETE /dashboard/courses/{course_id}`
  - `PATCH /dashboard/courses/{course_id}/activate|deactivate`
  - `GET /dashboard/courses/{course_id}/roster`
  - `GET /dashboard/courses/{course_id}/results?term_id=`
- Enrollments:
  - `POST|GET /dashboard/enrollments`
  - `PATCH|DELETE /dashboard/enrollments/{enrollment_id}`
- Timetable:
  - `POST|GET /dashboard/timetable`
  - `PATCH|DELETE /dashboard/timetable/{session_id}`
- Attendance:
  - `POST|GET /dashboard/attendance`
  - `GET /dashboard/attendance/summary?course_id=&term_id=`
  - `DELETE /dashboard/attendance/{record_id}`
- Grades:
  - `POST|GET /dashboard/grades/assessments`
  - `PATCH|DELETE /dashboard/grades/assessments/{assessment_id}`
  - `POST /dashboard/grades/scores`
  - `GET /dashboard/grades/assessments/{assessment_id}/scores`
- Fees:
  - `POST|GET /dashboard/fees/structures`
  - `PATCH|DELETE /dashboard/fees/structures/{structure_id}`
  - `POST /dashboard/fees/structures/{structure_id}/bill`
  - `POST|GET /dashboard/fees/invoices`
  - `GET|DELETE /dashboard/fees/invoices/{invoice_id}`
  - `PATCH /dashboard/fees/invoices/{invoice_id}/void`
  - `POST /dashboard/fees/payments`
  - `GET /dashboard/fees/invoices/{invoice_id}/payments`

When creating or updating events, `email_template` is restricted to the
built-in template enum values (for example `event_reminder.html`,
`exam_reminder.html`, `deadline_reminder.html`, `registration_open.html`).

Interactive API docs are available at `/docs` once the backend is running.
