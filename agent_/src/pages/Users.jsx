import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CareerAdvisor() {
  const navigate = useNavigate();

  const [skills, setSkills] = useState([]);

  const fetchAdvice = async () => {
    try {
      const email = localStorage.getItem("email");

      const response = await fetch(
        `http://localhost:8000/career_advisor?email=${email}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (data.error) {
        alert(data.error);
      } else {
        setSkills(data.skills);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to fetch career advice");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <button
        onClick={() => navigate("/dashboard")}
        className="bg-slate-800 px-4 py-2 rounded-lg mb-6"
      >
        ← Back
      </button>

      <div className="max-w-3xl mx-auto bg-slate-900 p-8 rounded-2xl border border-slate-800">

        <h1 className="text-3xl font-bold text-cyan-400 mb-6">
          Career Advisor
        </h1>

        <button
          onClick={fetchAdvice}
          className="w-full bg-cyan-500 text-black font-bold py-3 rounded-xl"
        >
          Get Career Advice
        </button>

        {skills.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">
              Your Skills
            </h2>

            <div className="flex flex-wrap gap-3">
              {skills.map((skill, index) => (
                <span
                  key={index}
                  className="bg-cyan-500 text-black px-4 py-2 rounded-full"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}