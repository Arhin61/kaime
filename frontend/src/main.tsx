import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'

import './index.css'
import App from './App.tsx'
import Events from './pages/EventsView.tsx'
import Subscribers from './pages/SubscribersView.tsx'
import Dashboard from './pages/Dashboard.tsx'
import Terms from './pages/TermsView.tsx'
import Students from './pages/StudentsView.tsx'
import Courses from './pages/CoursesView.tsx'
import Enrollments from './pages/EnrollmentsView.tsx'
import Timetable from './pages/TimetableView.tsx'
import Attendance from './pages/AttendanceView.tsx'
import Grades from './pages/GradesView.tsx'
import Fees from './pages/FeesView.tsx'
import { ThemeProvider } from './components/ThemeContext.tsx'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="dashboard" element={<Dashboard />}>
            <Route path="events" element={<Events />} />
            <Route path="subscribers" element={<Subscribers />} />
            <Route path="terms" element={<Terms />} />
            <Route path="students" element={<Students />} />
            <Route path="courses" element={<Courses />} />
            <Route path="enrollments" element={<Enrollments />} />
            <Route path="timetable" element={<Timetable />} />
            <Route path="attendance" element={<Attendance />} />
            <Route path="grades" element={<Grades />} />
            <Route path="fees" element={<Fees />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  </StrictMode>,
)
