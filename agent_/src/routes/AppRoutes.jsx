import { BrowserRouter, Routes, Route } from "react-router-dom";

import Auth from "../pages/Auth";
import Profile from "../pages/Profile";   // Add this import
import Dashboard from "../pages/Dashboard";
import ResumeUpload from "../pages/ResumeUpload";
import ResumeScore from "../pages/ResumeScore";
import SkillGap from "../pages/SkillGap";
import Roadmap from "../pages/Roadmap";
import Jobs from "../pages/Jobs";
import Interview from "../pages/Interview";
import Chat from "../pages/Chat";
import Applications from "../pages/Applications";
import CareerAdvisor from "../pages/CareerAdvisor";
import Users from "../pages/Users";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login/Register Page */}
        <Route path="/" element={<Auth />} />

        {/* Profile Creation */}
        <Route path="/profile" element={<Profile />} />

        {/* Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Feature Pages */}
        <Route path="/resume" element={<ResumeUpload />} />
        <Route path="/resume-score" element={<ResumeScore />} />
        <Route path="/skill-gap" element={<SkillGap />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/applications" element={<Applications />} />
        <Route path="/career-advisor" element={<CareerAdvisor />} />
        <Route path="/users" element={<Users />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/chat" element={<Chat />} />
        

      </Routes>
    </BrowserRouter>
  );
}