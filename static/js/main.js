// main.js
const generateBtn = document.getElementById("generateBtn");
const topicInput = document.getElementById("topic");
const contentTypeSelect = document.getElementById("contentType");
const lengthSelect = document.getElementById("length");
const resultPre = document.getElementById("result");
const loadingDiv = document.getElementById("loading");
const copyBtn = document.getElementById("copyBtn");
const clearBtn = document.getElementById("clearBtn");

generateBtn.addEventListener("click", async () => {
  const topic = topicInput.value.trim();
  const content_type = contentTypeSelect.value;
  const length = lengthSelect.value;

  if (!topic) {
    alert("Please enter a topic.");
    return;
  }

  generateBtn.disabled = true;
  loadingDiv.classList.remove("hidden");
  resultPre.textContent = "";

  try {
    const resp = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, content_type, length })
    });

    const data = await resp.json();
    if (resp.ok) {
      resultPre.textContent = data.result;
    } else {
      resultPre.textContent = "Error: " + (data.error || "Unknown error");
    }
  } catch (err) {
    resultPre.textContent = "Network error: " + err.message;
  } finally {
    loadingDiv.classList.add("hidden");
    generateBtn.disabled = false;
  }
});

copyBtn.addEventListener("click", async () => {
  const text = resultPre.textContent;
  if (!text) return alert("No text to copy.");
  await navigator.clipboard.writeText(text);
  alert("Copied to clipboard!");
});

clearBtn.addEventListener("click", () => {
  resultPre.textContent = "";
});
