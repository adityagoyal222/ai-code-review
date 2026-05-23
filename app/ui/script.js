const form = document.getElementById("review-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.textContent = "Running review...";

  const payload = {
    code: document.getElementById("code").value,
    language: document.getElementById("language").value || null,
  };

  try {
    const response = await fetch("/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      result.textContent = `Request failed: ${response.status}`;
      return;
    }

    const data = await response.json();
    result.textContent = data.review || "No review returned.";
  } catch (error) {
    result.textContent = `Error: ${error}`;
  }
});
