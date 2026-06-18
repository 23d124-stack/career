import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ResumeScore() {
  const navigate = useNavigate();

  const skills = JSON.parse(
    localStorage.getItem("skills") || "[]"
  );

  const [targetRole, setTargetRole] = useState("AI Engineer");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScore = async () => {
    try {
      setLoading(true);

      const response = await fetch(
        "http://localhost:8000/resume_score",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            target_role: targetRole,
            skills: skills,
          }),
        }
      );

      const data = await response.json();

      setResult(data);

    } catch (error) {
      console.error(error);
      alert("Failed to calculate score");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <button
        onClick={() => navigate("/dashboard")}
        className="mb-6 bg-slate-800 px-4 py-2 rounded-lg"
      >
        ← Back
      </button>

      <div className="max-w-3xl mx-auto bg-slate-900 p-8 rounded-2xl border border-slate-800">

        <h1 className="text-3xl font-bold text-cyan-400 mb-6">
          Resume Score
        </h1>

        <p className="mb-4 text-slate-300">
          Extracted Skills:
        </p>

        <div className="flex flex-wrap gap-2 mb-6">
          {skills.map((skill, index) => (
            <span
              key={index}
              className="bg-cyan-500 text-black px-3 py-1 rounded-full"
            >
              {skill}
            </span>
          ))}
        </div>

        <select
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          className="w-full p-3 rounded-lg bg-slate-800 border border-slate-700 mb-6"
        >
          <option>AI Engineer</option>
          <option>Data Scientist</option>
          <option>Frontend Developer</option>
        </select>

        <button
          onClick={handleScore}
          disabled={loading}
          className="w-full bg-cyan-500 text-black font-bold py-3 rounded-xl hover:bg-cyan-400"
        >
          {loading ? "Calculating..." : "Calculate Resume Score"}
        </button>

        {result && (
          <div className="mt-8">

            <h2 className="text-2xl font-bold mb-4">
              Resume Score
            </h2>

            <div className="w-full bg-slate-800 rounded-full h-6 mb-4">
              <div
                className="bg-green-500 h-6 rounded-full text-center text-black font-bold"
                style={{
                  width: `${result.resume_score}%`,
                }}
              >
                {result.resume_score}%
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-green-400 font-bold mb-2">
                Matched Skills
              </h3>

              <div className="flex flex-wrap gap-2">
                {result.matched_skills.map((skill, index) => (
                  <span
                    key={index}
                    className="bg-green-500 text-black px-3 py-1 rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-red-400 font-bold mb-2">
                Missing Skills
              </h3>

              <div className="flex flex-wrap gap-2">
                {result.missing_skills.map((skill, index) => (
                  <span
                    key={index}
                    className="bg-red-500 text-black px-3 py-1 rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

          </div>
        )}

      </div>

    </div>
  );
}