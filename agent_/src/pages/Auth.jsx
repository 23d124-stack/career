import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Auth() {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = async () => {
    try {
      const endpoint = isLogin ? "/login" : "/register";

      const body = isLogin
        ? {
            email,
            password,
          }
        : {
            name,
            email,
            password,
            skills: "",
          };

      const response = await fetch(
        `http://localhost:8000${endpoint}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      const data = await response.json();

      alert(data.message);

      if (
        data.message === "Login Success" ||
        data.message === "User Registered Successfully"
      ) {
        // Save email for future requests
        localStorage.setItem("email", email);

        // Redirect to Profile Page
        navigate("/profile");
      }
    } catch (error) {
      console.error(error);
      alert("Something went wrong");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950 flex items-center justify-center px-4">

      <div className="w-full max-w-md bg-slate-900/80 backdrop-blur-lg border border-slate-800 rounded-3xl shadow-2xl p-8">

        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-cyan-400">
            CareerAI
          </h1>

          <p className="text-slate-400 mt-2">
            Smart AI Career Guidance Platform
          </p>
        </div>

        <h2 className="text-2xl font-semibold text-white mb-6 text-center">
          {isLogin ? "Welcome Back" : "Create Account"}
        </h2>

        {!isLogin && (
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full mb-4 px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white outline-none focus:border-cyan-400"
          />
        )}

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white outline-none focus:border-cyan-400"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-6 px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white outline-none focus:border-cyan-400"
        />

        <button
          onClick={handleAuth}
          className="w-full bg-cyan-500 hover:bg-cyan-400 text-black font-bold py-3 rounded-xl transition"
        >
          {isLogin ? "Sign In" : "Create Account"}
        </button>

        <div className="mt-6 text-center">
          <span className="text-slate-400">
            {isLogin
              ? "Don't have an account?"
              : "Already have an account?"}
          </span>

          <button
            onClick={() => setIsLogin(!isLogin)}
            className="ml-2 text-cyan-400 font-semibold"
          >
            {isLogin ? "Register" : "Login"}
          </button>
        </div>

      </div>

    </div>
  );
}