import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Chat() {
  const navigate = useNavigate();

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message) return;

    const userMsg = { role: "user", text: message };
    setChat((prev) => [...prev, userMsg]);

    try {
      setLoading(true);

     const response = await fetch("http://localhost:8000/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    message: message
  }),
});

      const data = await response.json();

      const aiMsg = {
        role: "ai",
        text: data.response,
      };

      setChat((prev) => [...prev, aiMsg]);

      setMessage("");
    } catch (error) {
      console.error(error);
      alert("Chat failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">

      <button
        onClick={() => navigate("/dashboard")}
        className="mb-4 bg-slate-800 px-4 py-2 rounded"
      >
        ← Back
      </button>

      <h1 className="text-3xl font-bold text-cyan-400 mb-6">
        AI Career Chat
      </h1>

      {/* Chat Box */}
      <div className="bg-slate-900 p-4 rounded-xl h-[500px] overflow-y-auto mb-4 border border-slate-800">

        {chat.map((c, i) => (
          <div
            key={i}
            className={
              c.role === "user"
                ? "text-right mb-3"
                : "text-left mb-3"
            }
          >
            <div
              className={
                c.role === "user"
                  ? "bg-cyan-500 text-black inline-block px-3 py-2 rounded-lg"
                  : "bg-slate-800 inline-block px-3 py-2 rounded-lg"
              }
            >
              {c.text}
            </div>
          </div>
        ))}

      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask career questions..."
          className="flex-1 p-3 rounded bg-slate-800 border border-slate-700"
        />

        <button
          onClick={sendMessage}
          className="bg-cyan-500 text-black px-4 rounded font-bold"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>

    </div>
  );
}