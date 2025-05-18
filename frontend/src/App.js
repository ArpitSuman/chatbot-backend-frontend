import React, { useState, useRef, useEffect } from "react";
import "./App.css";

const backendUrl = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat]);

  const sendMessage = async () => {
    if (!message.trim()) return;
    setLoading(true);

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      setChat((prev) => [
        ...prev,
        { user: message, bot: data.reply || data.error || "Error from bot." },
    ]);

    } catch (err) {
      setChat((prev) => [
        ...prev,
        { user: message, bot: "Error contacting server." },
      ]);
    } finally {
      setMessage("");
      setLoading(false);
    }
  };

  const resetChat = async () => {
    await fetch(`${backendUrl}/reset`, {
      method: "POST",
    });
    setChat([]);
    setMessage("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="App">
      <h1>🤖 AI Chatbot</h1>

      <div className="chat-window">
        {chat.map((c, i) => (
          <div key={i} className="chat-bubble">
            <p><b>You:</b> {c.user}</p>
            <p><b>Bot:</b> {c.bot}</p>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <div className="input-area">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          rows={2}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
        <button onClick={resetChat} className="reset-button">
          Reset
        </button>
      </div>
    </div>
  );
}

export default App;
