document.addEventListener("DOMContentLoaded", () => {
  const socket = io("/julia", {
    withCredentials: true,
    
  });

  socket.on("connect", () => console.log("Connected to WebSocket server"));

  socket.on("error", (error) => {
    console.error("WebSocket error:", error);
    alert("Server error: " + (error?.error || "Unknown error"));
  });

  socket.on("response", (data) => {
    try {
      console.log("Server response:", data);
      const resultsBox = document.getElementById("results");
      if (resultsBox) {
        resultsBox.innerHTML = "";
        data.results.forEach(result => {
          const div = document.createElement("div");
          div.innerHTML = `
            <h3>${result.title}</h3>
            <a href="${result.url}" target="_blank">${result.url}</a>
            <pre>${JSON.stringify(result.ai_insight || {}, null, 2)}</pre>
          `;
          resultsBox.appendChild(div);
        });
      }
    } catch (err) {
      console.error("Error handling server response:", err);
    }
  });

  const submitBtn = document.querySelector(".submit");
  const micBtn = document.querySelector(".mic");
  const chatboxIcon = document.getElementById("chatbox-icon");

  if (submitBtn) {
    submitBtn.addEventListener("click", sendMessage);
  }

  if (micBtn) {
    micBtn.addEventListener("click", startSpeechToText);
  }

  if (chatboxIcon) {
    chatboxIcon.addEventListener("click", () => {
      const box = document.getElementById("chatbox");
      if (box) {
        box.style.display = box.style.display === "flex" ? "none" : "flex";
      } else {
        console.error("#chatbox not found");
      }
    });
  }

  function sendMessage() {
    const textarea = document.getElementById("messageInput");
    if (!textarea) return;

    const message = textarea.value.trim();
    if (message) {
      socket.emit("message", { q: message });
      textarea.value = "";

      if (message.startsWith("http://") || message.startsWith("https://")) {
        axios.get(message)
          .then(() => console.log("URL fetched"))
          .catch(err => console.error("URL fetch failed:", err));
      }
    }
  }

  function startSpeechToText() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      const messageInput = document.getElementById("messageInput");
      if (messageInput) {
        messageInput.value = transcript;
      }
    };

    recognition.onerror = function(event) {
      console.error("Speech recognition error:", event.error);
    };

    recognition.start();
  }
});

