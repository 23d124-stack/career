import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ResumeUpload() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF resume");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await fetch(
        "http://localhost:8000/upload_resume",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setSkills(data.skills || []);

      // Save extracted skills
      localStorage.setItem(
        "skills",
        JSON.stringify(data.skills || [])
      );

    } catch (error) {
      console.error(error);
      alert("Resume upload failed");
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

      <div className="max-w-2xl mx-auto bg-slate-900 p-8 rounded-2xl border border-slate-800">

        <h1 className="text-3xl font-bold text-cyan-400 mb-6">
          Resume Upload
        </h1>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full mb-6"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full bg-cyan-500 text-black font-bold py-3 rounded-xl hover:bg-cyan-400"
        >
          {loading ? "Uploading..." : "Upload Resume"}
        </button>

        {skills.length > 0 && (
          <div className="mt-8">

            <h2 className="text-xl font-semibold mb-4">
              Extracted Skills
            </h2>

            <div className="flex flex-wrap gap-3">

              {skills.map((skill, index) => (
                <span
                  key={index}
                  className="bg-cyan-500 text-black px-4 py-2 rounded-full font-medium"
                >
                  {skill}
                </span>
              ))}

            </div>

            <button
              onClick={() => navigate("/resume-score")}
              className="mt-8 bg-green-500 px-6 py-3 rounded-xl font-semibold"
            >
              Continue →
            </button>

          </div>
        )}

      </div>

    </div>
  );
}