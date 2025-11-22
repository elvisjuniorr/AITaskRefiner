import { useState } from "react";
import { motion } from "framer-motion";
import { Send, Sparkles } from "lucide-react";
import './App.css';

const Card = ({ children, className = "" }) => (
  <div className={`bg-slate-950 border border-slate-700 rounded-2xl shadow-2xl ${className}`}>
    {children}
  </div>
);

const CardContent = ({ children, className = "" }) => (
  <div className={`p-6 ${className}`}>{children}</div>
);

const Button = ({ children, onClick }) => (
  <button
    onClick={onClick}
    className="rounded-2xl bg-indigo-600 hover:bg-indigo-700 transition-all px-5 py-3 shadow-lg flex items-center justify-center"
  >
    {children}
  </button>
);

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "bot",
      content:
        "Welcome to AITaskRefiner. Paste your software prompt and I will refine it using advanced Prompt Engineering techniques."
    }
  ]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:8000/processar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          mensagem: input,
          session_id: "user-001"
        })
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: data.resposta
        }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: "❌ Erro ao conectar com o servidor Python."
        }
      ]);
    }

    setInput("");
  };

  return (
    <div className="app-wrapper">
      <div className="chat-card">
        <div className="chat-content">

          <div className="chat-header">
            <h1>
              <Sparkles className="text-indigo-400" />
              AITaskRefiner
            </h1>
            <p>Intelligent Prompt Engineering Assistant</p>
          </div>

          <div className="chat-box">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.role === "user" ? "user" : "bot"}`}
              >
                {msg.content}
              </div>
            ))}
          </div>

          <div className="input-area">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Paste your unstructured prompt here..."
              className="text-input"
              rows={2}
            />
            <button className="send-button" onClick={handleSend}>
              <Send className="w-5 h-5 text-white" />
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}
