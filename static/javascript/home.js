const text = "stream";
const container = document.getElementById("stream-container");

[...text].forEach((char, i) => {
  const span = document.createElement("span");
  span.textContent = char;
  span.classList.add("letter");
  container.appendChild(span);

  setTimeout(() => {
    span.classList.add("show");
  }, i * 300); // Delay between letters
});
