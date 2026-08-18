import type { ReactNode } from "react";

export const inputClasses =
  "w-full p-3 rounded-lg border border-app-border bg-app-bg text-app-text focus:ring-2 focus:ring-app-accent outline-none";

export const buttonClasses =
  "bg-app-accent text-white px-5 py-2 rounded-lg font-medium hover:opacity-90 transition shadow-sm disabled:opacity-50 disabled:cursor-not-allowed";

export function PageHeader({
  title,
  description,
  children,
}: {
  title: string;
  description?: string;
  children?: ReactNode;
}) {
  return (
    <div className="flex flex-wrap gap-4 justify-between items-center">
      <div>
        <h2 className="text-2xl font-bold text-app-text-h">{title}</h2>
        {description && (
          <p className="text-sm text-app-text mt-1">{description}</p>
        )}
      </div>
      <div className="flex items-center gap-3">{children}</div>
    </div>
  );
}

export function Banner({
  message,
  tone = "error",
  onDismiss,
}: {
  message: string;
  tone?: "error" | "success";
  onDismiss?: () => void;
}) {
  const tones = {
    error: "border-red-500/40 bg-red-500/10 text-red-600",
    success: "border-green-500/40 bg-green-500/10 text-green-600",
  };
  return (
    <div
      className={`flex justify-between items-start gap-4 rounded-lg border p-3 text-sm ${tones[tone]}`}
    >
      <span>{message}</span>
      {onDismiss && (
        <button onClick={onDismiss} className="font-bold shrink-0">
          ×
        </button>
      )}
    </div>
  );
}

export function Card({ children }: { children: ReactNode }) {
  return (
    <div className="bg-app-bg p-6 rounded-xl border border-app-border shadow-app-shadow">
      {children}
    </div>
  );
}

export function Table({
  headers,
  children,
  empty,
  isEmpty,
}: {
  headers: string[];
  children: ReactNode;
  empty: string;
  isEmpty: boolean;
}) {
  return (
    <div className="bg-app-bg rounded-xl border border-app-border overflow-x-auto">
      <table className="w-full text-left min-w-max">
        <thead className="bg-app-bg border-b border-app-border">
          <tr>
            {headers.map((header) => (
              <th
                key={header}
                className="p-4 text-app-text-h font-semibold text-sm whitespace-nowrap"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-app-border">
          {isEmpty ? (
            <tr>
              <td
                colSpan={headers.length}
                className="p-8 text-center text-app-text"
              >
                {empty}
              </td>
            </tr>
          ) : (
            children
          )}
        </tbody>
      </table>
    </div>
  );
}

export function Pill({ label, tone }: { label: string; tone: string }) {
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${tone}`}
    >
      {label}
    </span>
  );
}

const STATUS_TONES: Record<string, string> = {
  active: "bg-green-500/15 text-green-600",
  enrolled: "bg-green-500/15 text-green-600",
  paid: "bg-green-500/15 text-green-600",
  present: "bg-green-500/15 text-green-600",
  completed: "bg-blue-500/15 text-blue-600",
  partial: "bg-amber-500/15 text-amber-600",
  late: "bg-amber-500/15 text-amber-600",
  deferred: "bg-amber-500/15 text-amber-600",
  suspended: "bg-red-500/15 text-red-600",
  absent: "bg-red-500/15 text-red-600",
  withdrawn: "bg-red-500/15 text-red-600",
  dropped: "bg-red-500/15 text-red-600",
  unpaid: "bg-red-500/15 text-red-600",
};

export function StatusPill({ status }: { status: string }) {
  const tone = STATUS_TONES[status] ?? "bg-app-accent/10 text-app-accent";
  return <Pill label={status} tone={tone} />;
}

/** Shared term selector — nearly every school view is scoped to a term. */
export function TermSelect({
  terms,
  value,
  onChange,
  allowAll = false,
}: {
  terms: { id: number; name: string; is_current: boolean }[];
  value: number | undefined;
  onChange: (termId: number | undefined) => void;
  allowAll?: boolean;
}) {
  return (
    <select
      className={`${inputClasses} py-2 w-auto`}
      value={value ?? ""}
      onChange={(e) =>
        onChange(e.target.value ? Number(e.target.value) : undefined)
      }
    >
      {allowAll && <option value="">All terms</option>}
      {!allowAll && !value && <option value="">Select a term…</option>}
      {terms.map((term) => (
        <option key={term.id} value={term.id}>
          {term.name}
          {term.is_current ? " (current)" : ""}
        </option>
      ))}
    </select>
  );
}
