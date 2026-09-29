# EduGenie API

## Health

`GET /health`

Example response:

```json
{
  "status": "ok",
  "app": "EduGenie",
  "gemini_configured": true,
  "explanation_provider": "auto"
}
```

## Q&A

`POST /qa`

```json
{"question": "What is an array?"}
```

Response:

```json
{"answer": "..."}
```

## Explanation

`POST /explain`

```json
{"text": "Explain binary search simply."}
```

## Quiz

`POST /quiz`

```json
{"text": "Binary search works on sorted arrays..."}
```

Response contains exactly three questions, each with four options, a correct answer and explanation.

## Summary

`POST /summarize`

```json
{"text": "Long educational passage..."}
```

## Learning recommendations

`POST /learn/recommendations`

```json
{"text": "Python programming"}
```

All documented endpoints also have `/api/...` aliases for frontend use.
