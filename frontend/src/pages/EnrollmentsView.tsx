import { useCallback, useEffect, useState, type FormEvent } from "react";
import { school, type Course, type Enrollment, type Student } from "../api";
import { useTerms } from "../hooks/useTerms";
import {
  Banner,
  Card,
  PageHeader,
  StatusPill,
  Table,
  TermSelect,
  buttonClasses,
  inputClasses,
} from "../components/ui";

export default function EnrollmentsView() {
  const { terms, termId, setTermId } = useTerms();
  const [students, setStudents] = useState<Student[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [studentId, setStudentId] = useState("");
  const [courseId, setCourseId] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    school.getStudents({ status: "active" }).then(setStudents).catch(() => {});
    school.getCourses().then(setCourses).catch(() => {});
  }, []);

  const load = useCallback(() => {
    if (!termId) {
      setEnrollments([]);
      return;
    }
    school
      .getEnrollments({ term_id: termId })
      .then(setEnrollments)
      .catch((e) => setError((e as Error).message));
  }, [termId]);

  useEffect(() => {
    load();
  }, [load]);

  const handleEnroll = async (event: FormEvent) => {
    event.preventDefault();
    if (!termId) return;
    setError(null);
    try {
      await school.enroll({
        student_id: studentId,
        course_id: Number(courseId),
        term_id: termId,
      });
      setStudentId("");
      setCourseId("");
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const drop = async (enrollment: Enrollment) => {
    setError(null);
    try {
      await school.setEnrollmentStatus(enrollment.id, "dropped");
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const handleDelete = async (enrollment: Enrollment) => {
    if (
      !window.confirm(
        `Remove ${enrollment.student_name} from ${enrollment.course_code}? Their attendance and scores for it will be deleted.`,
      )
    )
      return;
    setError(null);
    try {
      await school.deleteEnrollment(enrollment.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Enrollments"
        description="Register students onto courses for a term."
      >
        <TermSelect terms={terms} value={termId} onChange={setTermId} />
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}

      <Card>
        <form
          onSubmit={handleEnroll}
          className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end"
        >
          <label className="text-sm text-app-text">
            Student
            <select
              required
              className={inputClasses}
              value={studentId}
              onChange={(e) => setStudentId(e.target.value)}
            >
              <option value="">Select a student…</option>
              {students.map((student) => (
                <option key={student.id} value={student.id}>
                  {student.index_number} — {student.full_name}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm text-app-text">
            Course
            <select
              required
              className={inputClasses}
              value={courseId}
              onChange={(e) => setCourseId(e.target.value)}
            >
              <option value="">Select a course…</option>
              {courses
                .filter((course) => course.is_active)
                .map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.code} — {course.title}
                  </option>
                ))}
            </select>
          </label>
          <button type="submit" className={buttonClasses} disabled={!termId}>
            Enroll Student
          </button>
        </form>
      </Card>

      <Table
        headers={["Index", "Student", "Course", "Term", "Status", "Actions"]}
        isEmpty={enrollments.length === 0}
        empty={termId ? "No enrollments for this term yet." : "Select a term."}
      >
        {enrollments.map((enrollment) => (
          <tr
            key={enrollment.id}
            className="hover:bg-app-border/10 transition-colors"
          >
            <td className="p-4 text-app-text-h font-medium">
              {enrollment.student_index_number}
            </td>
            <td className="p-4 text-app-text">{enrollment.student_name}</td>
            <td className="p-4 text-app-text">
              {enrollment.course_code} — {enrollment.course_title}
            </td>
            <td className="p-4 text-app-text">{enrollment.term_name}</td>
            <td className="p-4">
              <StatusPill status={enrollment.status} />
            </td>
            <td className="p-4 space-x-4 whitespace-nowrap">
              {enrollment.status === "enrolled" && (
                <button
                  onClick={() => drop(enrollment)}
                  className="text-app-accent hover:underline font-medium text-sm"
                >
                  Drop
                </button>
              )}
              <button
                onClick={() => handleDelete(enrollment)}
                className="text-red-500 hover:underline font-medium text-sm"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </Table>
    </div>
  );
}
