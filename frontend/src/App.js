import React, { useState } from "react";
import "./App.css";
const backendUrl = process.env.REACT_APP_BACKEND_URL;
function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    console.log("Backend URL:", backendUrl);
    const response = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    setChat([...chat, { user: message, bot: data.reply }]);
    setMessage("");
  };

  return (
    <div className="App">
      <h1>AI Chatbot</h1>
      <div className="chat-window">
        {chat.map((c, i) => (
          <div key={i}>
            <p><b>You:</b> {c.user}</p>
            <p><b>Bot:</b> {c.bot}</p>
          </div>
        ))}
      </div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
