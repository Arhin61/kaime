import { useCallback, useEffect, useState, type FormEvent } from "react";
import {
  school,
  type FeeStructure,
  type FeeStructureCreate,
  type Invoice,
  type PaymentMethod,
} from "../api";
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

const METHODS: PaymentMethod[] = [
  "cash",
  "bank_transfer",
  "mobile_money",
  "card",
  "scholarship",
];

const emptyStructure = {
  name: "",
  amount: 0,
  program: "",
  level: "",
  due_date: "",
};

export default function FeesView() {
  const { terms, termId, setTermId } = useTerms();
  const [structures, setStructures] = useState<FeeStructure[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [form, setForm] = useState(emptyStructure);
  const [payingInvoice, setPayingInvoice] = useState<Invoice | null>(null);
  const [paymentAmount, setPaymentAmount] = useState("");
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>("cash");
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const load = useCallback(() => {
    if (!termId) {
      setStructures([]);
      setInvoices([]);
      return;
    }
    school
      .getFeeStructures(termId)
      .then(setStructures)
      .catch((e) => setError((e as Error).message));
    school
      .getInvoices({ term_id: termId })
      .then(setInvoices)
      .catch((e) => setError((e as Error).message));
  }, [termId]);

  useEffect(() => {
    load();
  }, [load]);

  const createStructure = async (event: FormEvent) => {
    event.preventDefault();
    if (!termId) return;
    setError(null);
    try {
      const payload: FeeStructureCreate = {
        term_id: termId,
        name: form.name,
        amount: Number(form.amount),
        program: form.program || null,
        level: form.level ? Number(form.level) : null,
        due_date: form.due_date,
      };
      await school.createFeeStructure(payload);
      setForm(emptyStructure);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const runBilling = async (structure: FeeStructure) => {
    setError(null);
    setNotice(null);
    try {
      const run = await school.runBilling(structure.id);
      setNotice(
        `${structure.name}: ${run.invoices_created} invoice(s) issued, ${run.students_skipped} already billed.`,
      );
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const deleteStructure = async (structure: FeeStructure) => {
    if (!window.confirm(`Delete ${structure.name}?`)) return;
    setError(null);
    try {
      await school.deleteFeeStructure(structure.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const submitPayment = async (event: FormEvent) => {
    event.preventDefault();
    if (!payingInvoice) return;
    setError(null);
    setNotice(null);
    try {
      await school.recordPayment({
        invoice_id: payingInvoice.id,
        amount: Number(paymentAmount),
        method: paymentMethod,
      });
      setNotice(`Payment recorded for ${payingInvoice.student_name}.`);
      setPayingInvoice(null);
      setPaymentAmount("");
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const voidInvoice = async (invoice: Invoice) => {
    if (!window.confirm(`Void the ${invoice.description} invoice?`)) return;
    setError(null);
    try {
      await school.voidInvoice(invoice.id);
      load();
    } catch (e) {
      setError((e as Error).message);
    }
  };

  const outstanding = invoices
    .filter((invoice) => invoice.status !== "void")
    .reduce((sum, invoice) => sum + Number(invoice.balance), 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Fees"
        description="Fee structures, issued invoices and payments."
      >
        <TermSelect terms={terms} value={termId} onChange={setTermId} />
      </PageHeader>

      {error && <Banner message={error} onDismiss={() => setError(null)} />}
      {notice && (
        <Banner
          message={notice}
          tone="success"
          onDismiss={() => setNotice(null)}
        />
      )}

      <Card>
        <form
          onSubmit={createStructure}
          className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end"
        >
          <label className="text-sm text-app-text md:col-span-2">
            Fee name
            <input
              required
              placeholder="e.g. Semester tuition"
              className={inputClasses}
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </label>
          <label className="text-sm text-app-text">
            Amount
            <input
              required
              type="number"
              min={0}
              step="0.01"
              className={inputClasses}
              value={form.amount}
              onChange={(e) =>
                setForm({ ...form, amount: Number(e.target.value) })
              }
            />
          </label>
          <label className="text-sm text-app-text">
            Program (optional)
            <input
              placeholder="All programs"
              className={inputClasses}
              value={form.program}
              onChange={(e) => setForm({ ...form, program: e.target.value })}
            />
          </label>
          <label className="text-sm text-app-text">
            Level (optional)
            <input
              type="number"
              min={0}
              step={100}
              placeholder="All levels"
              className={inputClasses}
              value={form.level}
              onChange={(e) => setForm({ ...form, level: e.target.value })}
            />
          </label>
          <label className="text-sm text-app-text md:col-span-2">
            Due date
            <input
              required
              type="date"
              className={inputClasses}
              value={form.due_date}
              onChange={(e) => setForm({ ...form, due_date: e.target.value })}
            />
          </label>
          <button type="submit" className={buttonClasses} disabled={!termId}>
            Add Fee Structure
          </button>
        </form>
      </Card>

      <Table
        headers={["Fee", "Amount", "Applies to", "Due", "Actions"]}
        isEmpty={structures.length === 0}
        empty={termId ? "No fee structures for this term." : "Select a term."}
      >
        {structures.map((structure) => (
          <tr
            key={structure.id}
            className="hover:bg-app-border/10 transition-colors"
          >
            <td className="p-4 text-app-text-h font-medium">{structure.name}</td>
            <td className="p-4 text-app-text">{structure.amount}</td>
            <td className="p-4 text-app-text">
              {structure.program ?? "All programs"}
              {structure.level ? ` · Level ${structure.level}` : ""}
            </td>
            <td className="p-4 text-app-text">{structure.due_date}</td>
            <td className="p-4 space-x-4 whitespace-nowrap">
              <button
                onClick={() => runBilling(structure)}
                className="text-app-accent hover:underline font-medium text-sm"
              >
                Bill students
              </button>
              <button
                onClick={() => deleteStructure(structure)}
                className="text-red-500 hover:underline font-medium text-sm"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </Table>

      {payingInvoice && (
        <Card>
          <h3 className="text-lg font-bold text-app-text-h mb-4">
            Record payment — {payingInvoice.student_name} (
            {payingInvoice.balance} outstanding)
          </h3>
          <form
            onSubmit={submitPayment}
            className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end"
          >
            <label className="text-sm text-app-text">
              Amount
              <input
                required
                autoFocus
                type="number"
                min={0.01}
                step="0.01"
                max={Number(payingInvoice.balance)}
                className={inputClasses}
                value={paymentAmount}
                onChange={(e) => setPaymentAmount(e.target.value)}
              />
            </label>
            <label className="text-sm text-app-text">
              Method
              <select
                className={inputClasses}
                value={paymentMethod}
                onChange={(e) =>
                  setPaymentMethod(e.target.value as PaymentMethod)
                }
              >
                {METHODS.map((method) => (
                  <option key={method} value={method}>
                    {method.replace("_", " ")}
                  </option>
                ))}
              </select>
            </label>
            <button type="submit" className={buttonClasses}>
              Save Payment
            </button>
            <button
              type="button"
              onClick={() => setPayingInvoice(null)}
              className="text-app-text hover:text-app-accent text-sm"
            >
              Cancel
            </button>
          </form>
        </Card>
      )}

      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-bold text-app-text-h">Invoices</h3>
          <span className="text-sm text-app-text">
            Outstanding this term:{" "}
            <span className="font-semibold text-app-text-h">
              {outstanding.toFixed(2)}
            </span>
          </span>
        </div>
        <Table
          headers={[
            "Index",
            "Student",
            "Description",
            "Amount",
            "Paid",
            "Balance",
            "Due",
            "Status",
            "Actions",
          ]}
          isEmpty={invoices.length === 0}
          empty="No invoices issued for this term yet."
        >
          {invoices.map((invoice) => (
            <tr
              key={invoice.id}
              className="hover:bg-app-border/10 transition-colors"
            >
              <td className="p-4 text-app-text-h font-medium">
                {invoice.student_index_number}
              </td>
              <td className="p-4 text-app-text">{invoice.student_name}</td>
              <td className="p-4 text-app-text">{invoice.description}</td>
              <td className="p-4 text-app-text">{invoice.amount}</td>
              <td className="p-4 text-app-text">{invoice.amount_paid}</td>
              <td className="p-4 text-app-text">{invoice.balance}</td>
              <td className="p-4 text-app-text">{invoice.due_date}</td>
              <td className="p-4">
                <StatusPill status={invoice.status} />
              </td>
              <td className="p-4 space-x-4 whitespace-nowrap">
                {invoice.status !== "paid" && invoice.status !== "void" && (
                  <>
                    <button
                      onClick={() => {
                        setPayingInvoice(invoice);
                        setPaymentAmount(invoice.balance);
                      }}
                      className="text-app-accent hover:underline font-medium text-sm"
                    >
                      Pay
                    </button>
                    {invoice.status === "unpaid" && (
                      <button
                        onClick={() => voidInvoice(invoice)}
                        className="text-red-500 hover:underline font-medium text-sm"
                      >
                        Void
                      </button>
                    )}
                  </>
                )}
              </td>
            </tr>
          ))}
        </Table>
      </div>
    </div>
  );
}
