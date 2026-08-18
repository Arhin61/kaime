import { Link, Outlet } from "react-router";
import ThemeToggler from "./components/ThemeToggler";

export default function App() {
  return (
    <div className="min-h-screen bg-app-bg text-app-text font-sans">
      {/* Navigation */}
      <nav className="border-b border-app-border sticky top-0 z-50 bg-app-bg/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-app-text-h">Kaime</span>
          </div>
          <div className="flex items-center gap-6">
            <a
              href="#features"
              className="text-app-text hover:text-app-accent transition-colors font-medium"
            >
              Features
            </a>
            <ThemeToggler />
            <Link
              to="/dashboard"
              className="bg-app-accent text-white px-5 py-2 rounded-lg font-medium hover:bg-blue-700 transition shadow-sm"
            >
              Dashboard
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-16">
        {/* Hero */}
        <section className="text-center mb-24">
          <h1 className="text-6xl md:text-7xl font-extrabold text-app-text-h mb-6 leading-tight tracking-tight">
            Run Your School, <br />
            <span className="text-app-accent">End to End</span>
          </h1>
          <p className="text-xl text-app-text max-w-2xl mx-auto mb-10">
            Kaime pairs a full school management system — students, courses,
            enrollment, timetabling, attendance, grading, and fees — with
            automated notifications, so every deadline reminder and academic
            update reaches students without manual effort.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/dashboard"
              className="bg-app-accent text-white px-8 py-3 rounded-xl font-semibold text-lg hover:bg-blue-700 transition shadow-lg"
            >
              Launch Dashboard
            </Link>
          </div>
        </section>

        {/* Features Grid */}
        <section id="features" className="py-12">
          <div className="mb-10">
            <h2 className="text-sm font-bold text-app-accent uppercase tracking-wider mb-6">
              School Management
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: "🧑‍🎓",
                  title: "Students & Terms",
                  desc: "Keep student records and academic terms in sync, with every course run scoped to its own term.",
                },
                {
                  icon: "📚",
                  title: "Courses & Enrollment",
                  desc: "Maintain a course catalogue and enroll students per term, one enrollment per student/course.",
                },
                {
                  icon: "🗓️",
                  title: "Timetable & Attendance",
                  desc: "Schedule weekly class slots without room clashes, then mark attendance sitting by sitting.",
                },
                {
                  icon: "📝",
                  title: "Grading",
                  desc: "Weight assessments, record scores, and compute results and GPA automatically.",
                },
                {
                  icon: "💳",
                  title: "Fees & Billing",
                  desc: "Bill fee structures to matching students and track invoices from unpaid to paid.",
                },
                {
                  icon: "⚡",
                  title: "Smart Automation",
                  desc: "Reduce manual admin overhead with idempotent billing, attendance, and enrollment safeguards.",
                },
              ].map((feat, i) => (
                <div
                  key={i}
                  className="p-8 rounded-2xl border border-app-border bg-app-bg shadow-app-shadow hover:border-app-accent/50 transition-colors"
                >
                  <div className="text-app-accent mb-4 text-3xl">{feat.icon}</div>
                  <h3 className="text-xl font-bold mb-3 text-app-text-h">
                    {feat.title}
                  </h3>
                  <p className="text-app-text">{feat.desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-sm font-bold text-app-accent uppercase tracking-wider mb-6">
              Notifications
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: "📅",
                  title: "Event Scheduling",
                  desc: "Create events once and let Kaime handle the notification timeline automatically.",
                },
                {
                  icon: "🎓",
                  title: "Targeted Alerts",
                  desc: "Ensure the right information reaches the right students at the perfect time.",
                },
                {
                  icon: "🔗",
                  title: "Linked to School Records",
                  desc: "Subscribers automatically link to matching student records, keeping alerts and academics in step.",
                },
              ].map((feat, i) => (
                <div
                  key={i}
                  className="p-8 rounded-2xl border border-app-border bg-app-bg shadow-app-shadow hover:border-app-accent/50 transition-colors"
                >
                  <div className="text-app-accent mb-4 text-3xl">{feat.icon}</div>
                  <h3 className="text-xl font-bold mb-3 text-app-text-h">
                    {feat.title}
                  </h3>
                  <p className="text-app-text">{feat.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <div className="mt-12">
          <Outlet />
        </div>
      </main>

      <footer className="border-t border-app-border py-12">
        <div className="max-w-7xl mx-auto px-6 text-center text-app-text">
          <p>
            &copy; {new Date().getFullYear()} Kaime Academic Solutions. All
            rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
