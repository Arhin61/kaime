import { useCallback, useEffect, useState, type FormEvent } from "react";
import {
  school,
  type Student,
  type StudentCreate,
  type StudentStatus,
} from "../api";
import {
  Banner,
  Card,
  PageHeader,
  StatusPill,
  Table,
  buttonClasses,
  inputClasses,
} from "../components/ui";

const STATUSES: StudentStatus[] = [
  "active",
  "deferred",
  "suspended",
  "graduated",
  "withdrawn",
];

const emptyForm: StudentCreate = {
  index_number: "",
  email: "",
  first_name: "",
  middle_name: "",
  last_name: "",
  phone_number: "",
  program: "",
  level: 100,
};

export default function StudentsView() {
  const [students, setStudents] = useState<Student[]>([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<StudentCreate>(emptyForm);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    school
      .getStudents({ search: search || undefined, status: statusFilter || undefined })
      .then(setStudents)
      .catch((e) => setError((e as Error).message));
  }, [search, statusFilter]);

  useEffect(() => {
    const timer = setTimeout(load, 250);
    return () => clearTimeout(timer);
  }, [load]);

  const handleCreate = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await school.createStudent({
        ...form,
        level: Number(form.level),
        middle_name: form.middle_name || null,
        phone_number: form.phone_number || null,
      });
      setForm(emptyForm);
      setShowForm(false);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const changeStatus = async (student: Student, status: StudentStatus) => {
    setError(null);
    try {
      await school.updateStudent(student.id, { status });
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const handleDelete = async (student: Student) => {
    if (!window.confirm(`Delete ${student.full_name}?`)) return;
    setError(null);
    try {
      await school.deleteStudent(student.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Students"
        description="Student records. Matching subscriber emails are linked automatically."
      >
        <input
          placeholder="Search name, index or email…"
          className={`${inputClasses} py-2 w-auto`}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className={`${inputClasses} py-2 w-auto`}
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All statuses</option>
          {STATUSES.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
        <button onClick={() => setShowForm(!showForm)} className={buttonClasses}>
          {showForm ? "Cancel" : "Add Student"}
        </button>
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}

      {showForm && (
        <Card>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                required
                placeholder="Index number"
                className={inputClasses}
                value={form.index_number}
                onChange={(e) =>
                  setForm({ ...form, index_number: e.target.value })
                }
              />
              <input
                required
                type="email"
                placeholder="Email"
                className={inputClasses}
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
              <input
                placeholder="Phone number"
                className={inputClasses}
                value={form.phone_number ?? ""}
                onChange={(e) =>
                  setForm({ ...form, phone_number: e.target.value })
                }
              />
              <input
                required
                placeholder="First name"
                className={inputClasses}
                value={form.first_name}
                onChange={(e) => setForm({ ...form, first_name: e.target.value })}
              />
              <input
                placeholder="Middle name (optional)"
                className={inputClasses}
                value={form.middle_name ?? ""}
                onChange={(e) =>
                  setForm({ ...form, middle_name: e.target.value })
                }
              />
              <input
                required
                placeholder="Last name"
                className={inputClasses}
                value={form.last_name}
                onChange={(e) => setForm({ ...form, last_name: e.target.value })}
              />
              <input
                required
                placeholder="Program"
                className={`${inputClasses} md:col-span-2`}
                value={form.program}
                onChange={(e) => setForm({ ...form, program: e.target.value })}
              />
              <input
                required
                type="number"
                min={0}
                step={100}
                placeholder="Level"
                className={inputClasses}
                value={form.level}
                onChange={(e) =>
                  setForm({ ...form, level: Number(e.target.value) })
                }
              />
            </div>
            <button type="submit" className={buttonClasses}>
              Create Student
            </button>
          </form>
        </Card>
      )}

      <Table
        headers={["Index", "Name", "Email", "Program", "Level", "Status", "Actions"]}
        isEmpty={students.length === 0}
        empty="No students match the current filters."
      >
        {students.map((student) => (
          <tr
            key={student.id}
            className="hover:bg-app-border/10 transition-colors"
          >
            <td className="p-4 text-app-text-h font-medium">
              {student.index_number}
            </td>
            <td className="p-4 text-app-text">{student.full_name}</td>
            <td className="p-4 text-app-text">
              {student.email}
              {student.subscriber_email && (
                <span className="ml-2 text-xs text-app-accent">subscribed</span>
              )}
            </td>
            <td className="p-4 text-app-text">{student.program}</td>
            <td className="p-4 text-app-text">{student.level}</td>
            <td className="p-4">
              <StatusPill status={student.status} />
            </td>
            <td className="p-4 whitespace-nowrap">
              <select
                className="bg-app-bg border border-app-border rounded px-2 py-1 text-sm text-app-text mr-3"
                value={student.status}
                onChange={(e) =>
                  changeStatus(student, e.target.value as StudentStatus)
                }
              >
                {STATUSES.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
              <button
                onClick={() => handleDelete(student)}
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
