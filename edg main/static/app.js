const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");
const resultContent = document.getElementById("resultContent");
const errorBox = document.getElementById("error");
const statusBox = document.getElementById("status");

const placeholders = {
  qa: "Example: Which is the largest ocean?",
  explain: "Example: Explain the Pythagoras theorem in simple terms.",
  quiz: "Paste a topic or educational passage here.",
  summarize: "Paste a long educational passage here.",
  learn: "Example: SQL"
};

task.addEventListener("change", () => {
  inputText.placeholder = placeholders[task.value];
});

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    statusBox.textContent = data.gemini_configured
      ? "API ready"
      : "Gemini key not configured";
  } catch {
    statusBox.textContent = "API unavailable";
  }
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function clearError() {
  errorBox.textContent = "";
  errorBox.classList.add("hidden");
}

function renderText(answer) {
  resultContent.innerHTML = `<div class="answer"></div>`;
  resultContent.querySelector(".answer").textContent = answer;
}

function renderQuiz(data) {
  resultContent.innerHTML = "";
  data.questions.forEach((q, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "quiz-question";

    const title = document.createElement("h3");
    title.textContent = `${index + 1}. ${q.question}`;
    wrapper.appendChild(title);

    q.options.forEach(option => {
      const button = document.createElement("button");
      button.className = "option";
      button.textContent = option;
      button.addEventListener("click", () => {
        wrapper.querySelectorAll(".option").forEach(b => b.disabled = true);
        const feedback = document.createElement("p");
        feedback.className = "feedback";
        if (option === q.correct_answer) {
          button.classList.add("correct");
          feedback.textContent = `Correct. ${q.explanation}`;
        } else {
          button.classList.add("wrong");
          wrapper.querySelectorAll(".option").forEach(b => {
            if (b.textContent === q.correct_answer) b.classList.add("correct");
          });
          feedback.textContent = `Not quite. Correct answer: ${q.correct_answer}. ${q.explanation}`;
        }
        wrapper.appendChild(feedback);
      });
      wrapper.appendChild(button);
    });

    resultContent.appendChild(wrapper);
  });
}

function renderLearningPath(data) {
  resultContent.innerHTML = `<h3></h3><p class="answer"></p>`;
  resultContent.querySelector("h3").textContent = data.title;
  resultContent.querySelector("p").textContent = data.overview;

  data.steps.forEach((step, index) => {
    const div = document.createElement("div");
    div.className = "step";
    const resources = step.resources.length
      ? `<ul>${step.resources.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul>`
      : "";
    div.innerHTML = `
      <strong>Step ${index + 1}: ${escapeHtml(step.level)} — ${escapeHtml(step.topic)}</strong>
      <p>${escapeHtml(step.description)}</p>
      ${resources}
    `;
    resultContent.appendChild(div);
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[c]));
}

async function runTask() {
  clearError();
  const text = inputText.value.trim();

  if (!text) {
    showError("Please enter some text first.");
    return;
  }

  const routes = {
    qa: "/api/qa",
    explain: "/api/explain",
    quiz: "/api/quiz",
    summarize: "/api/summarize",
    learn: "/api/learn/recommendations"
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "Generating…";
  result.classList.add("hidden");

  try {
    const body = task.value === "qa"
      ? { question: text }
      : { text };

    const response = await fetch(routes[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    if (task.value === "quiz") {
      renderQuiz(data);
    } else if (task.value === "learn") {
      renderLearningPath(data);
    } else {
      renderText(data.answer);
    }

    result.classList.remove("hidden");
    result.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    showError(error.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Generate Answer";
  }
}

submitBtn.addEventListener("click", runTask);
checkHealth();
