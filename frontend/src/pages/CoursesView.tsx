import { useEffect, useState, type FormEvent } from "react";
import { school, type Course, type CourseCreate } from "../api";
import {
  Banner,
  Card,
  PageHeader,
  StatusPill,
  Table,
  buttonClasses,
  inputClasses,
} from "../components/ui";

const emptyForm: CourseCreate = {
  code: "",
  title: "",
  description: "",
  credit_hours: 3,
  department: "",
  level: null,
  lecturer_name: "",
  is_active: true,
};

export default function CoursesView() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<CourseCreate>(emptyForm);
  const [error, setError] = useState<string | null>(null);

  const load = () =>
    school.getCourses().then(setCourses).catch((e) => setError(e.message));

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await school.createCourse({
        ...form,
        credit_hours: Number(form.credit_hours),
        level: form.level ? Number(form.level) : null,
        description: form.description || null,
        department: form.department || null,
        lecturer_name: form.lecturer_name || null,
      });
      setForm(emptyForm);
      setShowForm(false);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const toggleActive = async (course: Course) => {
    setError(null);
    try {
      await school.setCourseActive(course.id, !course.is_active);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const handleDelete = async (course: Course) => {
    if (!window.confirm(`Delete ${course.code}?`)) return;
    setError(null);
    try {
      await school.deleteCourse(course.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Courses"
        description="The course catalogue students are enrolled into."
      >
        <button onClick={() => setShowForm(!showForm)} className={buttonClasses}>
          {showForm ? "Cancel" : "Add Course"}
        </button>
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}

      {showForm && (
        <Card>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                required
                placeholder="Code (e.g. CS101)"
                className={inputClasses}
                value={form.code}
                onChange={(e) => setForm({ ...form, code: e.target.value })}
              />
              <input
                required
                placeholder="Title"
                className={`${inputClasses} md:col-span-2`}
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
              <input
                required
                type="number"
                min={0}
                placeholder="Credit hours"
                className={inputClasses}
                value={form.credit_hours}
                onChange={(e) =>
                  setForm({ ...form, credit_hours: Number(e.target.value) })
                }
              />
              <input
                placeholder="Department"
                className={inputClasses}
                value={form.department ?? ""}
                onChange={(e) =>
                  setForm({ ...form, department: e.target.value })
                }
              />
              <input
                type="number"
                min={0}
                step={100}
                placeholder="Level (optional)"
                className={inputClasses}
                value={form.level ?? ""}
                onChange={(e) =>
                  setForm({
                    ...form,
                    level: e.target.value ? Number(e.target.value) : null,
                  })
                }
              />
              <input
                placeholder="Lecturer"
                className={inputClasses}
                value={form.lecturer_name ?? ""}
                onChange={(e) =>
                  setForm({ ...form, lecturer_name: e.target.value })
                }
              />
              <textarea
                placeholder="Description (optional)"
                className={`${inputClasses} md:col-span-2`}
                value={form.description ?? ""}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>
            <button type="submit" className={buttonClasses}>
              Create Course
            </button>
          </form>
        </Card>
      )}

      <Table
        headers={[
          "Code",
          "Title",
          "Credits",
          "Department",
          "Level",
          "Lecturer",
          "Status",
          "Actions",
        ]}
        isEmpty={courses.length === 0}
        empty="No courses yet."
      >
        {courses.map((course) => (
          <tr key={course.id} className="hover:bg-app-border/10 transition-colors">
            <td className="p-4 text-app-text-h font-medium">{course.code}</td>
            <td className="p-4 text-app-text">{course.title}</td>
            <td className="p-4 text-app-text">{course.credit_hours}</td>
            <td className="p-4 text-app-text">{course.department ?? "—"}</td>
            <td className="p-4 text-app-text">{course.level ?? "—"}</td>
            <td className="p-4 text-app-text">{course.lecturer_name ?? "—"}</td>
            <td className="p-4">
              <StatusPill status={course.is_active ? "active" : "inactive"} />
            </td>
            <td className="p-4 space-x-4 whitespace-nowrap">
              <button
                onClick={() => toggleActive(course)}
                className="text-app-accent hover:underline font-medium text-sm"
              >
                {course.is_active ? "Deactivate" : "Activate"}
              </button>
              <button
                onClick={() => handleDelete(course)}
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
