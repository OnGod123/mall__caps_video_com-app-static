const socket = io("/julia", {
    query: { token: "your_jwt_token" }
  });


socket.onopen = () => console.log("Connected to WebSocket server");
socket.onerror = (error) => console.error("WebSocket error:", error);

function toggleChatbox() {
  const box = document.getElementById("chatbox");
  box.style.display = box.style.display === "flex" ? "none" : "flex";
}

function sendMessage() {
  const textarea = document.getElementById("messageInput");
  const message = textarea.value.trim();

  if (message) {
    socket.send(message);
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
