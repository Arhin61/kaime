import { useCallback, useEffect, useState } from "react";
import {
  school,
  type AttendanceStatus,
  type AttendanceSummary,
  type Course,
  type Enrollment,
} from "../api";
import { useTerms } from "../hooks/useTerms";
import {
  Banner,
  Card,
  PageHeader,
  Table,
  TermSelect,
  buttonClasses,
  inputClasses,
} from "../components/ui";

const STATUSES: AttendanceStatus[] = ["present", "absent", "late", "excused"];

const today = () => new Date().toISOString().slice(0, 10);

export default function AttendanceView() {
  const { terms, termId, setTermId } = useTerms();
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState("");
  const [sessionDate, setSessionDate] = useState(today);
  const [roster, setRoster] = useState<Enrollment[]>([]);
  const [marks, setMarks] = useState<Record<string, AttendanceStatus>>({});
  const [summary, setSummary] = useState<AttendanceSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    school.getCourses().then(setCourses).catch(() => {});
  }, []);

  const loadRoster = useCallback(() => {
    if (!termId || !courseId) {
      setRoster([]);
      setSummary([]);
      return;
    }
    const course = Number(courseId);
    school
      .getCourseRoster(course, termId)
      .then((rows) => {
        const active = rows.filter((row) => row.status !== "dropped");
        setRoster(active);
        setMarks(
          Object.fromEntries(
            active.map((row) => [row.id, "present" as AttendanceStatus]),
          ),
        );
      })
      .catch((e) => setError((e as Error).message));
    school
      .getAttendanceSummary(course, termId)
      .then(setSummary)
      .catch((e) => setError((e as Error).message));
  }, [termId, courseId]);

  useEffect(() => {
    loadRoster();
  }, [loadRoster]);

  const submit = async () => {
    if (!termId || !courseId || roster.length === 0) return;
    setError(null);
    setNotice(null);
    setSaving(true);
    try {
      await school.markAttendance({
        course_id: Number(courseId),
        term_id: termId,
        session_date: sessionDate,
        entries: roster.map((row) => ({
          enrollment_id: row.id,
          status: marks[row.id] ?? "present",
        })),
      });
      setNotice(`Register saved for ${sessionDate}.`);
      loadRoster();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  const markAll = (status: AttendanceStatus) =>
    setMarks(Object.fromEntries(roster.map((row) => [row.id, status])));

  return (
    <div className="space-y-6">
      <PageHeader
        title="Attendance"
        description="Mark the register for a sitting, then review the term summary."
      >
        <TermSelect terms={terms} value={termId} onChange={setTermId} />
        <select
          className={`${inputClasses} py-2 w-auto`}
          value={courseId}
          onChange={(e) => setCourseId(e.target.value)}
        >
          <option value="">Select a course…</option>
          {courses.map((course) => (
            <option key={course.id} value={course.id}>
              {course.code}
            </option>
          ))}
        </select>
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}
      {notice && (
        <Banner
          message={notice}
          tone="success"
          onDismiss={() => setNotice(null)}
        />
      )}

      {roster.length > 0 && (
        <Card>
          <div className="flex flex-wrap gap-4 items-end justify-between mb-4">
            <label className="text-sm text-app-text">
              Session date
              <input
                type="date"
                className={inputClasses}
                value={sessionDate}
                onChange={(e) => setSessionDate(e.target.value)}
              />
            </label>
            <div className="flex gap-3">
              <button
                onClick={() => markAll("present")}
                className="text-app-accent hover:underline text-sm font-medium"
              >
                Mark all present
              </button>
              <button
                onClick={() => markAll("absent")}
                className="text-red-500 hover:underline text-sm font-medium"
              >
                Mark all absent
              </button>
            </div>
          </div>

          <div className="divide-y divide-app-border">
            {roster.map((row) => (
              <div
                key={row.id}
                className="flex flex-wrap items-center justify-between gap-3 py-3"
              >
                <div>
                  <span className="text-app-text-h font-medium">
                    {row.student_index_number}
                  </span>
                  <span className="text-app-text ml-3">{row.student_name}</span>
                </div>
                <div className="flex gap-1">
                  {STATUSES.map((status) => (
                    <button
                      key={status}
                      onClick={() => setMarks({ ...marks, [row.id]: status })}
                      className={`px-3 py-1 rounded-lg text-sm capitalize transition ${
                        marks[row.id] === status
                          ? "bg-app-accent text-white"
                          : "border border-app-border text-app-text hover:border-app-accent"
                      }`}
                    >
                      {status}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={submit}
            disabled={saving}
            className={`${buttonClasses} mt-6`}
          >
            {saving ? "Saving…" : "Save Register"}
          </button>
        </Card>
      )}

      <div className="space-y-3">
        <h3 className="text-lg font-bold text-app-text-h">Term summary</h3>
        <Table
          headers={[
            "Index",
            "Student",
            "Sessions",
            "Present",
            "Late",
            "Excused",
            "Absent",
            "Rate",
          ]}
          isEmpty={summary.length === 0}
          empty="No attendance recorded for this course and term yet."
        >
          {summary.map((row) => (
            <tr
              key={row.student_id}
              className="hover:bg-app-border/10 transition-colors"
            >
              <td className="p-4 text-app-text-h font-medium">
                {row.student_index_number}
              </td>
              <td className="p-4 text-app-text">{row.student_name}</td>
              <td className="p-4 text-app-text">{row.sessions_held}</td>
              <td className="p-4 text-app-text">{row.present}</td>
              <td className="p-4 text-app-text">{row.late}</td>
              <td className="p-4 text-app-text">{row.excused}</td>
              <td className="p-4 text-app-text">{row.absent}</td>
              <td
                className={`p-4 font-semibold ${
                  row.attendance_rate >= 75
                    ? "text-green-600"
                    : row.attendance_rate >= 50
                      ? "text-amber-600"
                      : "text-red-500"
                }`}
              >
                {row.attendance_rate}%
              </td>
            </tr>
          ))}
        </Table>
      </div>
    </div>
  );
}
