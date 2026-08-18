export const EventEmailTemplate = {
  ANNOUNCEMENT: "announcement.html",
  DEADLINE_REMINDER: "deadline_reminder.html",
  EVENT_REMINDER: "event_reminder.html",
  EXAM_REMINDER: "exam_reminder.html",
  REGISTRATION_CLOSING: "registration_closing.html",
  REGISTRATION_OPEN: "registration_open.html",
  REGISTRATION_REMINDER: "registration_reminder.html",
  RESULTS_PUBLISHED: "results_published.html",
  RESULTS_PUBLISHED_REMINDER: "results_published_reminder.html",
  UPCOMING_EVENT_REMINDER: "upcoming_event_reminder.html",
  VAC_RE_OPENING_REMINDER: "vac-re-opening_reminder.html",
} as const;

// This extracts the values into a reusable TypeScript type
export type EventEmailTemplate =
  (typeof EventEmailTemplate)[keyof typeof EventEmailTemplate];

export interface Subscriber {
  email: string;
  name: string;
  program: string;
  surname: string;
  other_names: string;
}

export interface Event {
  id: number;
  title: string;
  body: string;
  start_date: string;
  end_date?: string;
  notification_days_before?: number;
  notification_offsets?: number[];
  email_template: EventEmailTemplate;
  is_active: boolean;
}

export type EventCreate = Omit<Event, "id">;

// --- School management types ---

export type StudentStatus =
  | "active"
  | "deferred"
  | "suspended"
  | "graduated"
  | "withdrawn";
export type EnrollmentStatus = "enrolled" | "dropped" | "completed";
export type AttendanceStatus = "present" | "absent" | "late" | "excused";
export type AssessmentKind =
  | "quiz"
  | "assignment"
  | "midterm"
  | "project"
  | "exam";
export type InvoiceStatus = "unpaid" | "partial" | "paid" | "void";
export type PaymentMethod =
  | "cash"
  | "bank_transfer"
  | "mobile_money"
  | "card"
  | "scholarship";

export const DAY_NAMES = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
] as const;

export interface Term {
  id: number;
  name: string;
  academic_year: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
}

export type TermCreate = Omit<Term, "id">;

export interface Student {
  id: string;
  index_number: string;
  email: string;
  subscriber_email: string | null;
  first_name: string;
  middle_name: string | null;
  last_name: string;
  full_name: string;
  phone_number: string | null;
  program: string;
  level: number;
  gender: string | null;
  date_of_birth: string | null;
  status: StudentStatus;
  enrolled_on: string;
}

export interface StudentCreate {
  index_number: string;
  email: string;
  first_name: string;
  middle_name?: string | null;
  last_name: string;
  phone_number?: string | null;
  program: string;
  level: number;
  gender?: string | null;
  date_of_birth?: string | null;
  status?: StudentStatus;
}

export interface Course {
  id: number;
  code: string;
  title: string;
  description: string | null;
  credit_hours: number;
  department: string | null;
  level: number | null;
  lecturer_name: string | null;
  is_active: boolean;
}

export type CourseCreate = Omit<Course, "id">;

export interface Enrollment {
  id: string;
  student_id: string;
  course_id: number;
  term_id: number;
  status: EnrollmentStatus;
  enrolled_at: string | null;
  student_name: string | null;
  student_index_number: string | null;
  course_code: string | null;
  course_title: string | null;
  term_name: string | null;
}

export interface ClassSession {
  id: number;
  course_id: number;
  term_id: number;
  day_of_week: number;
  start_time: string;
  end_time: string;
  room: string | null;
  lecturer_name: string | null;
  course_code: string | null;
  course_title: string | null;
}

export type ClassSessionCreate = Omit<
  ClassSession,
  "id" | "course_code" | "course_title"
>;

export interface AttendanceEntry {
  enrollment_id: string;
  status: AttendanceStatus;
  remarks?: string | null;
}

export interface AttendanceMark {
  course_id: number;
  term_id: number;
  session_date: string;
  class_session_id?: number | null;
  entries: AttendanceEntry[];
}

export interface AttendanceSummary {
  student_id: string;
  student_name: string;
  student_index_number: string;
  course_id: number;
  course_code: string;
  sessions_held: number;
  present: number;
  late: number;
  excused: number;
  absent: number;
  attendance_rate: number;
}

export interface Assessment {
  id: number;
  course_id: number;
  term_id: number;
  title: string;
  kind: AssessmentKind;
  max_score: string;
  weight: string;
  due_date: string | null;
  course_code: string | null;
}

export interface AssessmentCreate {
  course_id: number;
  term_id: number;
  title: string;
  kind: AssessmentKind;
  max_score: number;
  weight: number;
  due_date?: string | null;
}

export interface Score {
  id: string;
  assessment_id: number;
  enrollment_id: string;
  score: string;
  remarks: string | null;
  graded_at: string | null;
  student_name: string | null;
  student_index_number: string | null;
  assessment_title: string | null;
  max_score: string | null;
}

export interface CourseResult {
  enrollment_id: string;
  student_id: string;
  student_name: string;
  student_index_number: string;
  course_id: number;
  course_code: string;
  course_title: string;
  credit_hours: number;
  weighted_score: number;
  graded_weight: number;
  letter_grade: string;
  grade_point: number;
}

export interface StudentResults {
  student_id: string;
  student_name: string;
  student_index_number: string;
  term_id: number;
  term_name: string;
  results: CourseResult[];
  total_credits: number;
  gpa: number;
}

export interface FeeStructure {
  id: number;
  term_id: number;
  name: string;
  description: string | null;
  amount: string;
  program: string | null;
  level: number | null;
  due_date: string;
  term_name: string | null;
}

export interface FeeStructureCreate {
  term_id: number;
  name: string;
  description?: string | null;
  amount: number;
  program?: string | null;
  level?: number | null;
  due_date: string;
}

export interface Invoice {
  id: string;
  student_id: string;
  term_id: number;
  fee_structure_id: number | null;
  description: string;
  amount: string;
  issued_on: string;
  due_date: string;
  status: InvoiceStatus;
  amount_paid: string;
  balance: string;
  student_name: string | null;
  student_index_number: string | null;
}

export interface Payment {
  id: string;
  invoice_id: string;
  amount: string;
  method: PaymentMethod;
  reference: string | null;
  paid_on: string;
  recorded_at: string | null;
}

export interface BillingRun {
  fee_structure_id: number;
  invoices_created: number;
  students_skipped: number;
}

export interface StudentBalance {
  student_id: string;
  student_name: string;
  student_index_number: string;
  total_billed: string;
  total_paid: string;
  balance: string;
  invoices: Invoice[];
}

// --- API Client ---
const API_BASE = "/";

/** Throws the API's `detail` message so forms can surface 404/409 reasons. */
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: init?.body
      ? { "Content-Type": "application/json", ...init?.headers }
      : init?.headers,
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") detail = body.detail;
      else if (Array.isArray(body?.detail)) detail = body.detail[0]?.msg ?? detail;
    } catch {
      // Non-JSON error body; keep the status-based message.
    }
    throw new Error(detail);
  }
  return res.status === 204 ? (undefined as T) : res.json();
}

const query = (params: Record<string, string | number | undefined | null>) => {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      search.set(key, String(value));
    }
  }
  const encoded = search.toString();
  return encoded ? `?${encoded}` : "";
};

export const school = {
  // Terms
  getTerms: () => request<Term[]>("dashboard/terms"),
  createTerm: (data: TermCreate) =>
    request<Term>("dashboard/terms", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateTerm: (id: number, data: Partial<TermCreate>) =>
    request<Term>(`dashboard/terms/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  deleteTerm: (id: number) =>
    request<void>(`dashboard/terms/${id}`, { method: "DELETE" }),

  // Students
  getStudents: (filters: { search?: string; program?: string; status?: string } = {}) =>
    request<Student[]>(`dashboard/students${query(filters)}`),
  createStudent: (data: StudentCreate) =>
    request<Student>("dashboard/students", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateStudent: (id: string, data: Partial<StudentCreate>) =>
    request<Student>(`dashboard/students/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  deleteStudent: (id: string) =>
    request<void>(`dashboard/students/${id}`, { method: "DELETE" }),
  getStudentResults: (id: string, termId: number) =>
    request<StudentResults>(`dashboard/students/${id}/results${query({ term_id: termId })}`),
  getStudentBalance: (id: string, termId?: number) =>
    request<StudentBalance>(`dashboard/students/${id}/balance${query({ term_id: termId })}`),

  // Courses
  getCourses: () => request<Course[]>("dashboard/courses"),
  createCourse: (data: CourseCreate) =>
    request<Course>("dashboard/courses", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  setCourseActive: (id: number, active: boolean) =>
    request<Course>(
      `dashboard/courses/${id}/${active ? "activate" : "deactivate"}`,
      { method: "PATCH" },
    ),
  deleteCourse: (id: number) =>
    request<void>(`dashboard/courses/${id}`, { method: "DELETE" }),
  getCourseRoster: (id: number, termId?: number) =>
    request<Enrollment[]>(`dashboard/courses/${id}/roster${query({ term_id: termId })}`),
  getCourseResults: (id: number, termId: number) =>
    request<CourseResult[]>(`dashboard/courses/${id}/results${query({ term_id: termId })}`),

  // Enrollments
  getEnrollments: (
    filters: { student_id?: string; course_id?: number; term_id?: number } = {},
  ) => request<Enrollment[]>(`dashboard/enrollments${query(filters)}`),
  enroll: (data: { student_id: string; course_id: number; term_id: number }) =>
    request<Enrollment>("dashboard/enrollments", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  setEnrollmentStatus: (id: string, status: EnrollmentStatus) =>
    request<Enrollment>(`dashboard/enrollments/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),
  deleteEnrollment: (id: string) =>
    request<void>(`dashboard/enrollments/${id}`, { method: "DELETE" }),

  // Timetable
  getTimetable: (filters: { term_id?: number; course_id?: number } = {}) =>
    request<ClassSession[]>(`dashboard/timetable${query(filters)}`),
  createClassSession: (data: ClassSessionCreate) =>
    request<ClassSession>("dashboard/timetable", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  deleteClassSession: (id: number) =>
    request<void>(`dashboard/timetable/${id}`, { method: "DELETE" }),

  // Attendance
  markAttendance: (data: AttendanceMark) =>
    request<unknown[]>("dashboard/attendance", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getAttendanceSummary: (courseId: number, termId: number) =>
    request<AttendanceSummary[]>(
      `dashboard/attendance/summary${query({ course_id: courseId, term_id: termId })}`,
    ),

  // Grades
  getAssessments: (filters: { course_id?: number; term_id?: number } = {}) =>
    request<Assessment[]>(`dashboard/grades/assessments${query(filters)}`),
  createAssessment: (data: AssessmentCreate) =>
    request<Assessment>("dashboard/grades/assessments", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  deleteAssessment: (id: number) =>
    request<void>(`dashboard/grades/assessments/${id}`, { method: "DELETE" }),
  getScores: (assessmentId: number) =>
    request<Score[]>(`dashboard/grades/assessments/${assessmentId}/scores`),
  recordScores: (
    assessmentId: number,
    entries: { enrollment_id: string; score: number }[],
  ) =>
    request<Score[]>("dashboard/grades/scores", {
      method: "POST",
      body: JSON.stringify({ assessment_id: assessmentId, entries }),
    }),

  // Fees
  getFeeStructures: (termId?: number) =>
    request<FeeStructure[]>(`dashboard/fees/structures${query({ term_id: termId })}`),
  createFeeStructure: (data: FeeStructureCreate) =>
    request<FeeStructure>("dashboard/fees/structures", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  deleteFeeStructure: (id: number) =>
    request<void>(`dashboard/fees/structures/${id}`, { method: "DELETE" }),
  runBilling: (id: number) =>
    request<BillingRun>(`dashboard/fees/structures/${id}/bill`, { method: "POST" }),
  getInvoices: (filters: { student_id?: string; term_id?: number; status?: string } = {}) =>
    request<Invoice[]>(`dashboard/fees/invoices${query(filters)}`),
  voidInvoice: (id: string) =>
    request<Invoice>(`dashboard/fees/invoices/${id}/void`, { method: "PATCH" }),
  deleteInvoice: (id: string) =>
    request<void>(`dashboard/fees/invoices/${id}`, { method: "DELETE" }),
  recordPayment: (data: {
    invoice_id: string;
    amount: number;
    method: PaymentMethod;
    reference?: string | null;
  }) =>
    request<Payment>("dashboard/fees/payments", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

export const api = {
  // Subscribers
  getSubscribers: async (): Promise<Subscriber[]> => {
    const res = await fetch(`${API_BASE}dashboard/subscribers`);
    return res.json();
  },
  createSubscriber: async (data: Subscriber): Promise<Subscriber> => {
    const res = await fetch(`${API_BASE}dashboard/subscribers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create subscriber");
    return res.json();
  },
  deleteSubscriber: async (email: string): Promise<void> => {
    await fetch(`${API_BASE}dashboard/subscribers/${email}`, { method: "DELETE" });
  },

  // Events
  getEvents: async (): Promise<Event[]> => {
    const res = await fetch(`${API_BASE}dashboard/events`);
    return res.json();
  },
  createEvent: async (data: EventCreate): Promise<Event> => {
    const res = await fetch(`${API_BASE}dashboard/events`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create event");
    return res.json();
  },
  toggleEventStatus: async (id: number, activate: boolean): Promise<Event> => {
    const action = activate ? "activate" : "deactivate";
    const res = await fetch(`${API_BASE}dashboard/events/${id}/${action}`, {
      method: "PATCH",
    });
    return res.json();
  },
  deleteEvent: async (id: number): Promise<void> => {
    await fetch(`${API_BASE}dashboard/events/${id}`, { method: "DELETE" });
  },
};
