<script>
const socket = io("/julia", {
  query: { token: "your_jwt_token" }
});

// ✅ Corrected: Socket.IO uses "connect", not onopen
socket.on("connect", () => console.log("Connected to WebSocket server"));

// ✅ Corrected: Socket.IO uses "error" event, not socket.onerror
socket.on("error", (error) => {
  console.error("WebSocket error:", error);
  alert("Server error: " + (error?.error || "Unknown error"));
});

// ✅ Added: Handle server "response" events
socket.on("response", (data) => {
  console.log("Server response:", data);
  // Optional: render to UI if you have a div with id="results"
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
});

function toggleChatbox() {
  const box = document.getElementById("chatbox");
  box.style.display = box.style.display === "flex" ? "none" : "flex";
}

function sendMessage() {
  const textarea = document.getElementById("messageInput");
  const message = textarea.value.trim();

  if (message) {
    // ✅ Corrected: Use socket.emit instead of socket.send
    socket.emit("message", { q: message });
    textarea.value = "";

    // Auto-fetch if URL
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
    document.getElementById("messageInput").value = transcript;
  };

  recognition.onerror = function(event) {
    console.error("Speech recognition error:", event.error);
  };

  recognition.start();
}
</script>

