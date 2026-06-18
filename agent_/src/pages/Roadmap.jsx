import { useState } from "react";

export default function Roadmap() {
  const [role, setRole] = useState("");
  const [roadmap, setRoadmap] = useState([]);

  const fetchRoadmap = async () => {
    const res = await fetch("http://localhost:8000/roadmap", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        target_role: role,
      }),
    });

    const data = await res.json();
    setRoadmap(data.roadmap);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <h1 className="text-3xl font-bold text-cyan-400 mb-6">
        Roadmap Generator
      </h1>

      <input
        value={role}
        onChange={(e) => setRole(e.target.value)}
        placeholder="Enter role (AI Engineer)"
        className="w-full p-3 rounded bg-slate-800 mb-4"
      />

      <button
        onClick={fetchRoadmap}
        className="bg-cyan-500 text-black px-6 py-2 rounded"
      >
        Generate Roadmap
      </button>

      <div className="mt-6 space-y-2">
        {roadmap.map((step, index) => (
          <div
            key={index}
            className="bg-slate-800 p-3 rounded border border-slate-700"
          >
            {step}
          </div>
        ))}
      </div>

    </div>
  );
}