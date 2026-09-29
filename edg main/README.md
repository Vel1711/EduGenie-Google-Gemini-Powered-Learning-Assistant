# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project documentation.

## Features
- Q&A
- Simplified concept explanation
- 3-question MCQ quiz generation
- Long-text summarization
- Beginner-to-advanced learning paths
- Structured JSON validation for quizzes and learning paths
- Health/status endpoint
- Optional local LaMini-Flan-T5 explanation provider
- Gemini fallback for explanations when the local model is unavailable

## Architecture

Browser
  -> FastAPI
      -> module router
          -> Gemini service
          -> optional local LaMini-Flan-T5
  -> validated response
  -> browser

## Important implementation note

The original documentation names Gemini 1.5 Pro. The code keeps the documented role of Gemini for Q&A, quiz, summarization and learning paths, but makes the model configurable through `.env`. The default is `gemini-2.5-flash`, a currently supported Gemini model suitable for this lightweight application.

The original documentation also specifies LaMini-Flan-T5-783M for concept explanation. This implementation supports that provider through `EXPLANATION_PROVIDER=local`, while `auto` (the default) uses the local model when available and falls back to Gemini when it is not. This avoids making the application unusable on machines that cannot load a local Transformer model.

## Quick start

### 1. Create a virtual environment

Windows PowerShell:
```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Optional local LaMini support:
```bash
pip install -r requirements-local.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and put your Gemini API key in it.

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
EXPLANATION_PROVIDER=auto
```

### 4. Run

```bash
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

### 5. Test

```bash
python -m pytest
```

Or use the browser interface.

## API endpoints

- `GET /health`
- `POST /api/qa`
- `POST /api/explain`
- `POST /api/quiz`
- `POST /api/summarize`
- `POST /api/learn/recommendations`

The legacy documentation names the endpoints `/qa`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`. This implementation exposes those exact routes as well as `/api/...` aliases.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   ├── prompts.py
│   ├── dependencies.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py
│   │   └── local_explanation.py
│   └── modules/
│       ├── __init__.py
│       ├── qna.py
│       ├── explanation_module.py
│       ├── quiz_module.py
│       ├── summary_module.py
│       └── learning_path.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── __init__.py
    └── test_api.py
```

## Security

Never commit `.env` or a real Gemini API key. The browser never receives the API key; calls to Gemini are made by the FastAPI backend.
