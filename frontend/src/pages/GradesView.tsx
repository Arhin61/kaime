import { useCallback, useEffect, useState, type FormEvent } from "react";
import {
  school,
  type Assessment,
  type AssessmentKind,
  type Course,
  type CourseResult,
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

const KINDS: AssessmentKind[] = [
  "quiz",
  "assignment",
  "midterm",
  "project",
  "exam",
];

export default function GradesView() {
  const { terms, termId, setTermId } = useTerms();
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState("");
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [results, setResults] = useState<CourseResult[]>([]);
  const [roster, setRoster] = useState<Enrollment[]>([]);
  const [activeAssessment, setActiveAssessment] = useState<Assessment | null>(
    null,
  );
  const [scores, setScores] = useState<Record<string, string>>({});
  const [form, setForm] = useState({
    title: "",
    kind: "assignment" as AssessmentKind,
    max_score: 100,
    weight: 20,
  });
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    school.getCourses().then(setCourses).catch(() => {});
  }, []);

  const load = useCallback(() => {
    if (!termId || !courseId) {
      setAssessments([]);
      setResults([]);
      setRoster([]);
      setActiveAssessment(null);
      return;
    }
    const course = Number(courseId);
    school
      .getAssessments({ course_id: course, term_id: termId })
      .then(setAssessments)
      .catch((e) => setError((e as Error).message));
    school
      .getCourseResults(course, termId)
      .then(setResults)
      .catch((e) => setError((e as Error).message));
    school
      .getCourseRoster(course, termId)
      .then((rows) => setRoster(rows.filter((row) => row.status !== "dropped")))
      .catch((e) => setError((e as Error).message));
  }, [termId, courseId]);

  useEffect(() => {
    load();
  }, [load]);

  const createAssessment = async (event: FormEvent) => {
    event.preventDefault();
    if (!termId || !courseId) return;
    setError(null);
    try {
      await school.createAssessment({
        course_id: Number(courseId),
        term_id: termId,
        title: form.title,
        kind: form.kind,
        max_score: Number(form.max_score),
        weight: Number(form.weight),
      });
      setForm({ ...form, title: "" });
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const openScoreEntry = async (assessment: Assessment) => {
    setError(null);
    setActiveAssessment(assessment);
    try {
      const existing = await school.getScores(assessment.id);
      setScores(
        Object.fromEntries(
          existing.map((score) => [score.enrollment_id, score.score]),
        ),
      );
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const saveScores = async () => {
    if (!activeAssessment) return;
    setError(null);
    setNotice(null);
    const entries = roster
      .filter((row) => scores[row.id] !== undefined && scores[row.id] !== "")
      .map((row) => ({ enrollment_id: row.id, score: Number(scores[row.id]) }));
    if (entries.length === 0) {
      setError("Enter at least one score.");
      return;
    }
    try {
      await school.recordScores(activeAssessment.id, entries);
      setNotice(`Scores saved for ${activeAssessment.title}.`);
      setActiveAssessment(null);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const deleteAssessment = async (assessment: Assessment) => {
    if (
      !window.confirm(`Delete ${assessment.title} and all its recorded scores?`)
    )
      return;
    setError(null);
    try {
      await school.deleteAssessment(assessment.id);
      if (activeAssessment?.id === assessment.id) setActiveAssessment(null);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const totalWeight = assessments.reduce(
    (sum, assessment) => sum + Number(assessment.weight),
    0,
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Grades"
        description="Weighted assessments, score entry and computed results."
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

      {termId && courseId && (
        <Card>
          <form
            onSubmit={createAssessment}
            className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end"
          >
            <label className="text-sm text-app-text md:col-span-2">
              Assessment title
              <input
                required
                placeholder="e.g. Mid-semester exam"
                className={inputClasses}
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </label>
            <label className="text-sm text-app-text">
              Kind
              <select
                className={inputClasses}
                value={form.kind}
                onChange={(e) =>
                  setForm({ ...form, kind: e.target.value as AssessmentKind })
                }
              >
                {KINDS.map((kind) => (
                  <option key={kind} value={kind}>
                    {kind}
                  </option>
                ))}
              </select>
            </label>
            <label className="text-sm text-app-text">
              Max score
              <input
                required
                type="number"
                min={1}
                className={inputClasses}
                value={form.max_score}
                onChange={(e) =>
                  setForm({ ...form, max_score: Number(e.target.value) })
                }
              />
            </label>
            <label className="text-sm text-app-text">
              Weight (%)
              <input
                required
                type="number"
                min={0}
                max={100}
                className={inputClasses}
                value={form.weight}
                onChange={(e) =>
                  setForm({ ...form, weight: Number(e.target.value) })
                }
              />
            </label>
            <button type="submit" className={`${buttonClasses} md:col-span-5`}>
              Add Assessment ({totalWeight}% of 100% allocated)
            </button>
          </form>
        </Card>
      )}

      <Table
        headers={["Title", "Kind", "Max", "Weight", "Actions"]}
        isEmpty={assessments.length === 0}
        empty={
          courseId ? "No assessments for this course yet." : "Select a course."
        }
      >
        {assessments.map((assessment) => (
          <tr
            key={assessment.id}
            className="hover:bg-app-border/10 transition-colors"
          >
            <td className="p-4 text-app-text-h font-medium">
              {assessment.title}
            </td>
            <td className="p-4 text-app-text capitalize">{assessment.kind}</td>
            <td className="p-4 text-app-text">{assessment.max_score}</td>
            <td className="p-4 text-app-text">{assessment.weight}%</td>
            <td className="p-4 space-x-4 whitespace-nowrap">
              <button
                onClick={() => openScoreEntry(assessment)}
                className="text-app-accent hover:underline font-medium text-sm"
              >
                Enter scores
              </button>
              <button
                onClick={() => deleteAssessment(assessment)}
                className="text-red-500 hover:underline font-medium text-sm"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </Table>

      {activeAssessment && (
        <Card>
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-app-text-h">
              Scores — {activeAssessment.title}{" "}
              <span className="text-sm font-normal text-app-text">
                (out of {activeAssessment.max_score})
              </span>
            </h3>
            <button
              onClick={() => setActiveAssessment(null)}
              className="text-app-text hover:text-app-accent text-sm"
            >
              Close
            </button>
          </div>
          <div className="divide-y divide-app-border">
            {roster.map((row) => (
              <div
                key={row.id}
                className="flex items-center justify-between gap-4 py-3"
              >
                <div>
                  <span className="text-app-text-h font-medium">
                    {row.student_index_number}
                  </span>
                  <span className="text-app-text ml-3">{row.student_name}</span>
                </div>
                <input
                  type="number"
                  min={0}
                  max={Number(activeAssessment.max_score)}
                  step="0.01"
                  className="w-28 p-2 rounded-lg border border-app-border bg-app-bg text-app-text focus:ring-2 focus:ring-app-accent outline-none"
                  value={scores[row.id] ?? ""}
                  onChange={(e) =>
                    setScores({ ...scores, [row.id]: e.target.value })
                  }
                />
              </div>
            ))}
          </div>
          <button onClick={saveScores} className={`${buttonClasses} mt-6`}>
            Save Scores
          </button>
        </Card>
      )}

      <div className="space-y-3">
        <h3 className="text-lg font-bold text-app-text-h">Results</h3>
        <Table
          headers={["Index", "Student", "Weighted score", "Graded", "Grade", "Points"]}
          isEmpty={results.length === 0}
          empty="No results yet — record some scores first."
        >
          {results.map((result) => (
            <tr
              key={result.enrollment_id}
              className="hover:bg-app-border/10 transition-colors"
            >
              <td className="p-4 text-app-text-h font-medium">
                {result.student_index_number}
              </td>
              <td className="p-4 text-app-text">{result.student_name}</td>
              <td className="p-4 text-app-text">{result.weighted_score}%</td>
              <td className="p-4 text-app-text">{result.graded_weight}%</td>
              <td className="p-4 font-bold text-app-text-h">
                {result.letter_grade}
              </td>
              <td className="p-4 text-app-text">
                {result.grade_point.toFixed(1)}
              </td>
            </tr>
          ))}
        </Table>
      </div>
    </div>
  );
}
