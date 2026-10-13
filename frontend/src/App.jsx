import { useEffect, useRef, useState } from "react";
import "./App.css";

 function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);

  const messagesEndRef = useRef(null);

  // Create a new conversation ID
  const [conversationId, setConversationId] = useState(() => {
    return crypto.randomUUID();
  });

  // Scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isThinking]);

  const formatReply = (reply) => {
    if (typeof reply === "string") {
      return reply;
    }

    if (reply?.reply) {
      return reply.reply;
    }

    if (reply?.intent) {
      let result = `Intent: ${reply.intent}`;

      if (reply.destination) {
        result += `\nDestination: ${reply.destination}`;
      }

      if (reply.date) {
        result += `\nDate: ${reply.date}`;
      }

      return result;
    }

    return JSON.stringify(reply);
  };

  const handleSend = async () => {
    if (!message.trim() || isThinking) return;

    const userMessage = message.trim();

    // Add user message
    setMessages((previous) => [
      ...previous,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");
    setIsThinking(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend returned an error");
      }

      const data = await response.json();

      // Add Sah-AI response
      setMessages((previous) => [
        ...previous,
        {
          sender: "ai",
          text: formatReply(data.reply),
        },
      ]);
    } catch (error) {
      console.error("Error communicating with Sah-AI:", error);

      setMessages((previous) => [
        ...previous,
        {
          sender: "ai",
          text: "Sorry, I couldn't connect to Sah-AI.",
        },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  const useExample = (example) => {
    setMessage(example);
  };

  // Start a completely new conversation
  const handleNewChat = () => {
    setMessages([]);
    setMessage("");
    setConversationId(crypto.randomUUID());
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">S</div>

          <div>
            <h1>Sah-AI</h1>
            <p>Your AI companion</p>
          </div>
        </div>

        <button className="new-chat-button" onClick={handleNewChat}>
          ＋ New Chat
        </button>
      </header>

      <main className="chat-container">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">✦</div>

            <h2>Namaste! I'm Sah-AI.</h2>

            <p>
              Tell me what you want to do, and I'll help you get it done.
            </p>

            <div className="examples">
              <button
                onClick={() =>
                  useExample("Repu Hyderabad ki train chudu")
                }
              >
                🚆 Search for a train
              </button>

              <button
                onClick={() =>
                  useExample("Movie ticket book cheyyali")
                }
              >
                🎬 Book a movie ticket
              </button>

              <button
                onClick={() =>
                  useExample("Hyderabad lo hotel kavali")
                }
              >
                🏨 Find a hotel
              </button>
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((item, index) => (
              <div
                key={index}
                className={`message-row ${
                  item.sender === "user"
                    ? "user-row"
                    : "ai-row"
                }`}
              >
                <div
                  className={`message-bubble ${
                    item.sender === "user"
                      ? "user-bubble"
                      : "ai-bubble"
                  }`}
                >
                  {item.text.split("\n").map((line, lineIndex) => (
                    <div key={lineIndex}>{line}</div>
                  ))}
                </div>
              </div>
            ))}

            {isThinking && (
              <div className="message-row ai-row">
                <div className="message-bubble ai-bubble thinking">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}

        <div className="input-area">
          <input
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
            disabled={isThinking}
          />

          <button
            className="send-button"
            onClick={handleSend}
            disabled={isThinking}
          >
            ➤
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;