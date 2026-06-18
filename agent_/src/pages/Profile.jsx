import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

export default function Profile() {
  const navigate = useNavigate();

  const email = localStorage.getItem("email") || "";

  const [formData, setFormData] = useState({
    email: email,
    degree: "",
    college: "",
    graduation_year: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      const response = await api.post("/profile", formData);

      alert(response.data.message);

      navigate("/Dashboard");
    } catch (error) {
      alert(
        error.response?.data?.message ||
        "Profile update failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">

        <h2 className="text-2xl font-bold text-center mb-6">
          Complete Your Profile
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="email"
            name="email"
            value={formData.email}
            readOnly
            className="w-full border rounded-lg px-4 py-3 bg-gray-100"
          />

          <input
            type="text"
            name="degree"
            placeholder="Degree"
            value={formData.degree}
            onChange={handleChange}
            required
            className="w-full border rounded-lg px-4 py-3"
          />

          <input
            type="text"
            name="college"
            placeholder="College Name"
            value={formData.college}
            onChange={handleChange}
            required
            className="w-full border rounded-lg px-4 py-3"
          />

          <input
            type="number"
            name="graduation_year"
            placeholder="Graduation Year"
            value={formData.graduation_year}
            onChange={handleChange}
            required
            className="w-full border rounded-lg px-4 py-3"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700"
          >
            {loading ? "Saving..." : "Save Profile"}
          </button>

        </form>
      </div>
    </div>
  );
}