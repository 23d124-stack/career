import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();

  const email = localStorage.getItem("email");

  const features = [
    { title: "Resume Upload", path: "/resume", description: "Upload resume & extract skills" },
    { title: "Resume Score", path: "/resume-score", description: "Check ATS score" },
    { title: "Skill Gap", path: "/skill-gap", description: "Find missing skills" },
    { title: "Roadmap", path: "/roadmap", description: "Learning path generator" },
    { title: "Jobs", path: "/jobs", description: "Recommended jobs" },
    { title: "Interview", path: "/interview", description: "AI interview practice" },
    { title: "Chat", path: "/chat", description: "Career AI assistant" },
    { title: "Applications", path: "/applications", description: "Track applications" },
    {title: "Career Advisor",description: "Get personalized career guidance",path: "/career-advisor"},
    {title: "Users",description: "View registered users",path: "/users",}
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* HEADER */}
      <div className="flex justify-between items-center p-6 bg-slate-900 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-bold text-cyan-400">
            CareerAI Dashboard
          </h1>
          <p className="text-slate-400 text-sm">
            Logged in: {email}
          </p>
        </div>

        <button
          onClick={() => {
            localStorage.clear();
            navigate("/");
          }}
          className="bg-red-500 px-4 py-2 rounded-lg font-semibold"
        >
          Logout
        </button>
      </div>

      {/* CARDS SECTION (FIXED NAVIGATION HERE) */}
      <div className="p-8 grid gap-6 md:grid-cols-2 lg:grid-cols-4">

        {features.map((item, index) => (
          <div
            key={index}
            onClick={() => navigate(item.path)}
            className="bg-slate-900 border border-slate-800 p-6 rounded-2xl cursor-pointer hover:border-cyan-400 hover:scale-105 transition"
          >
            <h2 className="text-xl font-bold text-cyan-400 mb-2">
              {item.title}
            </h2>

            <p className="text-slate-400 text-sm">
              {item.description}
            </p>

            <p className="text-xs text-slate-600 mt-3">
              {item.path}
            </p>
          </div>
        ))}

      </div>
    </div>
  );
}