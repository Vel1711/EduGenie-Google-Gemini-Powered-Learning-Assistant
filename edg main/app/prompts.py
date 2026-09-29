def qa_prompt(question: str) -> str:
    return f"""
You are EduGenie, an educational AI assistant.
Answer the student's question accurately and clearly.

Rules:
- Prefer simple language.
- Give the direct answer first.
- Add a short explanation or example when useful.
- If the question is ambiguous, state the assumption.
- Do not invent citations, sources, statistics, or facts.
- If you are uncertain, say so.

Student question:
{question}
""".strip()


def explanation_prompt(topic: str) -> str:
    return f"""
Explain the following educational topic for a beginner.

Topic: {topic}

Requirements:
- Start with a simple definition.
- Explain the main idea step by step.
- Give one simple example.
- Avoid unnecessary jargon.
- Keep it concise but useful.
""".strip()


def summary_prompt(text: str) -> str:
    return f"""
Summarize the following educational passage for quick revision.

Requirements:
- Preserve the important facts and meaning.
- Remove repetition and unnecessary wording.
- Use clear headings or bullet points when helpful.
- Do not add facts that are not supported by the passage.

Passage:
{text}
""".strip()


def quiz_prompt(text: str) -> str:
    return f"""
Create exactly 3 multiple-choice questions from the educational text below.

Requirements:
- Exactly 3 questions.
- Exactly 4 options per question.
- Exactly one correct answer per question.
- correct_answer must exactly match one of the four options.
- Add a short explanation for each answer.
- Questions must be answerable from the supplied text.
- Avoid trick questions and ambiguous options.

Source text:
{text}
""".strip()


def learning_path_prompt(topic: str) -> str:
    return f"""
Create a structured learning path for the topic below.

Topic: {topic}

Requirements:
- Start at beginner level and progress toward advanced level.
- Give at least 3 learning steps.
- For every step provide level, topic, description and useful resource suggestions.
- Resources may be general resource types or well-known learning sites/books, but do not invent URLs.
- Make the sequence practical and suitable for a self-learner.
""".strip()
