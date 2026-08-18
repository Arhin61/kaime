import { useCallback, useEffect, useState, type FormEvent } from "react";
import { DAY_NAMES, school, type ClassSession, type Course } from "../api";
import { useTerms } from "../hooks/useTerms";
import {
  Banner,
  Card,
  PageHeader,
  TermSelect,
  buttonClasses,
  inputClasses,
} from "../components/ui";

export default function TimetableView() {
  const { terms, termId, setTermId } = useTerms();
  const [courses, setCourses] = useState<Course[]>([]);
  const [sessions, setSessions] = useState<ClassSession[]>([]);
  const [courseId, setCourseId] = useState("");
  const [day, setDay] = useState(0);
  const [startTime, setStartTime] = useState("08:00");
  const [endTime, setEndTime] = useState("10:00");
  const [room, setRoom] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    school.getCourses().then(setCourses).catch(() => {});
  }, []);

  const load = useCallback(() => {
    if (!termId) {
      setSessions([]);
      return;
    }
    school
      .getTimetable({ term_id: termId })
      .then(setSessions)
      .catch((e) => setError((e as Error).message));
  }, [termId]);

  useEffect(() => {
    load();
  }, [load]);

  const handleCreate = async (event: FormEvent) => {
    event.preventDefault();
    if (!termId) return;
    setError(null);
    try {
      await school.createClassSession({
        course_id: Number(courseId),
        term_id: termId,
        day_of_week: day,
        start_time: `${startTime}:00`,
        end_time: `${endTime}:00`,
        room: room || null,
        lecturer_name: null,
      });
      setRoom("");
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const handleDelete = async (session: ClassSession) => {
    if (!window.confirm(`Remove ${session.course_code} from the timetable?`))
      return;
    setError(null);
    try {
      await school.deleteClassSession(session.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Timetable"
        description="Weekly class slots. Room double-bookings are rejected."
      >
        <TermSelect terms={terms} value={termId} onChange={setTermId} />
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}

      <Card>
        <form
          onSubmit={handleCreate}
          className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end"
        >
          <label className="text-sm text-app-text md:col-span-2">
            Course
            <select
              required
              className={inputClasses}
              value={courseId}
              onChange={(e) => setCourseId(e.target.value)}
            >
              <option value="">Select a course…</option>
              {courses.map((course) => (
                <option key={course.id} value={course.id}>
                  {course.code} — {course.title}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm text-app-text">
            Day
            <select
              className={inputClasses}
              value={day}
              onChange={(e) => setDay(Number(e.target.value))}
            >
              {DAY_NAMES.map((name, index) => (
                <option key={name} value={index}>
                  {name}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm text-app-text">
            Start
            <input
              required
              type="time"
              className={inputClasses}
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
            />
          </label>
          <label className="text-sm text-app-text">
            End
            <input
              required
              type="time"
              className={inputClasses}
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
            />
          </label>
          <label className="text-sm text-app-text md:col-span-2">
            Room
            <input
              placeholder="e.g. NB Block 12"
              className={inputClasses}
              value={room}
              onChange={(e) => setRoom(e.target.value)}
            />
          </label>
          <button type="submit" className={buttonClasses} disabled={!termId}>
            Add Slot
          </button>
        </form>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {DAY_NAMES.map((name, index) => {
          const daySessions = sessions.filter(
            (session) => session.day_of_week === index,
          );
          return (
            <div
              key={name}
              className="rounded-xl border border-app-border p-4 space-y-3"
            >
              <h3 className="font-bold text-app-text-h">{name}</h3>
              {daySessions.length === 0 ? (
                <p className="text-sm text-app-text">No classes.</p>
              ) : (
                daySessions.map((session) => (
                  <div
                    key={session.id}
                    className="rounded-lg bg-app-accent/5 border border-app-accent/20 p-3"
                  >
                    <div className="font-semibold text-app-text-h text-sm">
                      {session.course_code}
                    </div>
                    <div className="text-xs text-app-text">
                      {session.start_time.slice(0, 5)}–
                      {session.end_time.slice(0, 5)}
                      {session.room ? ` · ${session.room}` : ""}
                    </div>
                    <button
                      onClick={() => handleDelete(session)}
                      className="mt-2 text-red-500 hover:underline text-xs font-medium"
                    >
                      Remove
                    </button>
                  </div>
                ))
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
