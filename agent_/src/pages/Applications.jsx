import { useEffect, useState } from "react";

export default function Applications() {
  const [applications, setApplications] = useState([]);

  const email = localStorage.getItem("email");

  const fetchApplications = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/applications/${email}`
      );

      const data = await res.json();
      setApplications(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <h1 className="text-3xl font-bold text-cyan-400 mb-6">
        Application Tracker
      </h1>

      {applications.length === 0 ? (
        <p className="text-slate-400">No applications found</p>
      ) : (
        <div className="space-y-4">
          {applications.map((app) => (
            <div
              key={app.id}
              className="bg-slate-900 p-5 rounded-xl border border-slate-800"
            >
              <h2 className="text-xl text-cyan-400 font-bold">
                {app.company}
              </h2>

              <p className="text-slate-300">{app.role}</p>

              <p className="text-sm text-slate-500">
                Status: {app.status || "Applied"}
              </p>

              {app.apply_link && (
                <a
                  href={app.apply_link}
                  target="_blank"
                  className="text-green-400 underline"
                >
                  View Job
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}