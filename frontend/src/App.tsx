import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './components/AppLayout'
import { Login, Register } from './pages/Auth'
import { Assessment, Concept, CourseOverview, Courses, Dashboard, Feedback, History, Profile, Progress, Recommendations, Resources, Tutor, WeakAreas } from './pages/AppPages'

export default function App(){return <Routes>
  <Route path="/" element={<Navigate to="/login" replace/>}/>
  <Route path="/login" element={<Login/>}/><Route path="/register" element={<Register/>}/>
  <Route path="/app" element={<AppLayout/>}>
    <Route index element={<Navigate to="dashboard" replace/>}/><Route path="dashboard" element={<Dashboard/>}/><Route path="courses" element={<Courses/>}/><Route path="courses/python" element={<CourseOverview/>}/><Route path="concepts/functions" element={<Concept/>}/><Route path="tutor" element={<Tutor/>}/><Route path="tutor/:sessionId" element={<Tutor/>}/><Route path="assessment" element={<Assessment/>}/><Route path="assessment/feedback" element={<Feedback/>}/><Route path="progress" element={<Progress/>}/><Route path="weak-areas" element={<WeakAreas/>}/><Route path="recommendations" element={<Recommendations/>}/><Route path="resources" element={<Resources/>}/><Route path="resources/:resourceId" element={<Resources/>}/><Route path="history" element={<History/>}/><Route path="profile" element={<Profile/>}/>
  </Route>
  <Route path="*" element={<Navigate to="/login" replace/>}/>
</Routes>}
