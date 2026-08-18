import { NavLink } from "react-router";
import { Link } from "react-router"

export default function Sidebar() {
  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    `px-4 py-2 rounded-lg transition-colors duration-200 ${
      isActive
        ? "bg-blue-100 text-blue-700 font-semibold"
        : "text-gray-600 hover:bg-gray-100"
    }`;

  return (
    <aside className="w-64 min-h-screen bg-white border-r border-gray-200 p-6 flex flex-col gap-8">
      <Link to="/" className="flex items-center gap-2">
        <span className="text-xl font-bold text-gray-900">Kaime</span>
      </Link>

      <nav className="flex flex-col gap-2">
        <p className="px-4 text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
          Notifications
        </p>
        <NavLink to="events" className={linkClasses}>
          Events
        </NavLink>
        <NavLink to="subscribers" className={linkClasses}>
          Subscribers
        </NavLink>

        <p className="px-4 mt-4 text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">
          School
        </p>
        <NavLink to="students" className={linkClasses}>
          Students
        </NavLink>
        <NavLink to="courses" className={linkClasses}>
          Courses
        </NavLink>
        <NavLink to="enrollments" className={linkClasses}>
          Enrollments
        </NavLink>
        <NavLink to="timetable" className={linkClasses}>
          Timetable
        </NavLink>
        <NavLink to="attendance" className={linkClasses}>
          Attendance
        </NavLink>
        <NavLink to="grades" className={linkClasses}>
          Grades
        </NavLink>
        <NavLink to="fees" className={linkClasses}>
          Fees
        </NavLink>
        <NavLink to="terms" className={linkClasses}>
          Academic Terms
        </NavLink>
      </nav>
    </aside>
  );
}
