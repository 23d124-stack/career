import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Jobs() {
  const navigate = useNavigate();

  const [role, setRole] = useState("AI Engineer");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchJobs = async () => {
    try {
      setLoading(true);

      const response = await fetch(
        `http://localhost:8000/live_jobs/${role}`
      );

      const data = await response.json();

      setJobs(data || []);

    } catch (error) {
      console.error(error);
      alert("Failed to load jobs");
    } finally {
      setLoading(false);
    }
  };
  const autoApply = async (job) => {
  const email = localStorage.getItem("email");

  if (!email) {
    alert("Please login first");
    return;
  }

  try {
    const response = await fetch(
      `http://localhost:8000/apply_job?email=${email}&company=${encodeURIComponent(
        job.company
      )}&role=${encodeURIComponent(
        job.title || job.role
      )}&apply_link=${encodeURIComponent(
        job.apply_link ||
        job.link ||
        job.url ||
        job.apply_url ||
        ""
      )}`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    alert(data.message);
  } catch (error) {
    console.error(error);
    alert("Auto apply failed");
  }
};

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      {/* Back */}
      <button
        onClick={() => navigate("/dashboard")}
        className="mb-6 bg-slate-800 px-4 py-2 rounded-lg"
      >
        ← Back
      </button>

      <div className="max-w-4xl mx-auto bg-slate-900 p-8 rounded-2xl border border-slate-800">

        <h1 className="text-3xl font-bold text-cyan-400 mb-6">
          Live Job Recommendations
        </h1>

        {/* Role Input */}
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full p-3 rounded-lg bg-slate-800 border border-slate-700 mb-6"
        >
          <option>AI Engineer</option>
          <option>Data Scientist</option>
          <option>Frontend Developer</option>
        </select>

        {/* Button */}
        <button
          onClick={fetchJobs}
          disabled={loading}
          className="w-full bg-cyan-500 text-black font-bold py-3 rounded-xl hover:bg-cyan-400"
        >
          {loading ? "Fetching Jobs..." : "Find Jobs"}
        </button>

        {/* Jobs List */}
        <div className="mt-8 space-y-4">

          {jobs.length === 0 && !loading && (
            <p className="text-slate-400 text-center">
              No jobs loaded yet
            </p>
          )}

          {jobs.map((job, index) => (
            <div
              key={index}
              className="bg-slate-800 border border-slate-700 p-5 rounded-xl hover:border-cyan-400 transition"
            >

              <h2 className="text-xl font-bold text-cyan-400">
                {job.title || job.role}
              </h2>

              <p className="text-slate-300 mt-1">
                {job.company}
              </p>

              <p className="text-slate-400 text-sm mt-1">
                {job.location}
              </p>

            <div className="mt-4 flex gap-3 flex-wrap">

  {(job.apply_link || job.link || job.url || job.apply_url) && (
    <a
      href={
        job.apply_link ||
        job.link ||
        job.url ||
        job.apply_url
      }
      target="_blank"
      rel="noreferrer"
      className="bg-green-500 text-black px-4 py-2 rounded-lg font-semibold"
    >
      Apply Now →
    </a>
  )}

  <button
    onClick={() => autoApply(job)}
    className="bg-cyan-500 text-black px-4 py-2 rounded-lg font-semibold"
  >
    Auto Apply
  </button>

</div>

            </div>
          ))}

        </div>

      </div>
    </div>
  );
}