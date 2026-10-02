import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { LogOut, Menu, X, UserRound } from 'lucide-react'
import { useState } from 'react'
import Logo from './Logo'
import HookSidebar from './animated/HookSidebar'
import NotificationBell from './animated/NotificationBell'

const links = [
  {href:'/app/dashboard',label:'Dashboard'},
  {href:'/app/courses',label:'Courses'},
  {href:'/app/progress',label:'Progress'},
  {href:'/app/recommendations',label:'Recommendations'},
  {href:'/app/tutor',label:'Tutor'},
  {href:'/app/assessment',label:'Assessments'},
  {href:'/app/resources',label:'Resources'},
  {href:'/app/history',label:'History'},
]

export default function AppLayout(){
 const [open,setOpen]=useState(false); const loc=useLocation()
 const crumb=loc.pathname.split('/').filter(Boolean).slice(-1)[0]?.replaceAll('-',' ')||'Dashboard'
 return <div className="app-shell">
   <aside className={`sidebar ${open?'mobile-open':''}`}>
    <div className="sidebar-top"><Logo/><button className="icon-btn mobile-only" onClick={()=>setOpen(false)} aria-label="Close navigation"><X size={18}/></button></div>
    <div className="learner-pill"><span className="pulse-dot"/> <span>Adaptive engine</span><strong>LIVE</strong></div>
    <HookSidebar items={links} label="Workspace" color="#6E5BFF"/>
    <div className="sidebar-bottom">
      <NavLink to="/app/profile" onClick={()=>setOpen(false)} className={({isActive})=>`nav-item ${isActive?'active':''}`}><UserRound size={18}/><span>Profile</span></NavLink>
      <button className="nav-item"><LogOut size={18}/><span>Sign out</span></button>
    </div>
   </aside>
   {open && <div className="mobile-overlay" onClick={()=>setOpen(false)}/>} 
   <main className="main-shell">
     <header className="topbar"><button className="icon-btn mobile-only" onClick={()=>setOpen(true)} aria-label="Open navigation"><Menu size={20}/></button><div className="breadcrumb">{crumb}</div><div className="topbar-right"><NotificationBell count={3}/><div className="state-chip"><span className="pulse-dot"/> Focus flow</div><div className="avatar">AR</div></div></header>
     <div className="page"><Outlet/></div>
   </main>
 </div>
}
