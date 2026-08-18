import { useEffect, useState, type FormEvent } from "react";
import { school, type Term, type TermCreate } from "../api";
import {
  Banner,
  Card,
  PageHeader,
  StatusPill,
  Table,
  buttonClasses,
  inputClasses,
} from "../components/ui";

const emptyForm: TermCreate = {
  name: "",
  academic_year: "",
  start_date: "",
  end_date: "",
  is_current: false,
};

export default function TermsView() {
  const [terms, setTerms] = useState<Term[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<TermCreate>(emptyForm);
  const [error, setError] = useState<string | null>(null);

  const load = () => school.getTerms().then(setTerms).catch((e) => setError(e.message));

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await school.createTerm(form);
      setForm(emptyForm);
      setShowForm(false);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const makeCurrent = async (term: Term) => {
    setError(null);
    try {
      await school.updateTerm(term.id, { is_current: true });
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const handleDelete = async (term: Term) => {
    if (!window.confirm(`Delete ${term.name}?`)) return;
    setError(null);
    try {
      await school.deleteTerm(term.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Academic Terms"
        description="Semesters that enrollment, grading and billing are scoped to."
      >
        <button onClick={() => setShowForm(!showForm)} className={buttonClasses}>
          {showForm ? "Cancel" : "Add Term"}
        </button>
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}

      {showForm && (
        <Card>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                required
                placeholder="Name (e.g. 2025/2026 Semester 1)"
                className={inputClasses}
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
              <input
                required
                placeholder="Academic year (e.g. 2025/2026)"
                className={inputClasses}
                value={form.academic_year}
                onChange={(e) =>
                  setForm({ ...form, academic_year: e.target.value })
                }
              />
              <label className="text-sm text-app-text">
                Start date
                <input
                  required
                  type="date"
                  className={inputClasses}
                  value={form.start_date}
                  onChange={(e) =>
                    setForm({ ...form, start_date: e.target.value })
                  }
                />
              </label>
              <label className="text-sm text-app-text">
                End date
                <input
                  required
                  type="date"
                  className={inputClasses}
                  value={form.end_date}
                  onChange={(e) => setForm({ ...form, end_date: e.target.value })}
                />
              </label>
            </div>
            <label className="flex items-center gap-2 text-app-text">
              <input
                type="checkbox"
                checked={form.is_current}
                onChange={(e) =>
                  setForm({ ...form, is_current: e.target.checked })
                }
              />
              Mark as the current term
            </label>
            <button type="submit" className={buttonClasses}>
              Create Term
            </button>
          </form>
        </Card>
      )}

      <Table
        headers={["Name", "Academic year", "Start", "End", "Status", "Actions"]}
        isEmpty={terms.length === 0}
        empty="No terms yet. Add one to get started."
      >
        {terms.map((term) => (
          <tr key={term.id} className="hover:bg-app-border/10 transition-colors">
            <td className="p-4 text-app-text-h font-medium">{term.name}</td>
            <td className="p-4 text-app-text">{term.academic_year}</td>
            <td className="p-4 text-app-text">{term.start_date}</td>
            <td className="p-4 text-app-text">{term.end_date}</td>
            <td className="p-4">
              {term.is_current ? (
                <StatusPill status="current" />
              ) : (
                <span className="text-app-text text-sm">—</span>
              )}
            </td>
            <td className="p-4 space-x-4 whitespace-nowrap">
              {!term.is_current && (
                <button
                  onClick={() => makeCurrent(term)}
                  className="text-app-accent hover:underline font-medium text-sm"
                >
                  Set current
                </button>
              )}
              <button
                onClick={() => handleDelete(term)}
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
