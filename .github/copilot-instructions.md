# ReachRich – Project Instructions for GitHub Copilot

## 1. Project Overview

**ReachRich** is an AI-powered personal finance management application.

The name combines:
- **Reach** – achieving financial goals.
- **Rich** – financial well-being and growth.

The main goal is to help users understand, organize, and analyze their financial activity using intelligent automation and AI.

The application will allow users to import financial transactions from bank Excel files, categorize income and expenses, add transactions manually, and receive useful financial insights.

## 2. Product Vision

ReachRich aims to provide:

- Automatic import of bank transactions from Excel files.
- Identification and categorization of income and expenses.
- Manual creation and editing of transactions.
- Intelligent transaction classification using AI.
- Financial summaries and visual reports.
- Analysis of spending patterns.
- AI-powered insights and suggestions for better financial management.

The initial focus is building a reliable MVP before expanding into advanced features.

## 3. Core Product Principles

### AI as an assistant, not the source of truth

- AI should assist with classification, analysis, and recommendations.
- Financial records must be stored and managed by the application.
- AI must never invent financial data.
- AI-generated classifications must be validated.
- Uncertain classifications should be flagged for user review.
- Users should be able to correct AI decisions manually.

### Data reliability

- Preserve original transaction information.
- Avoid duplicate transaction imports.
- Validate dates, amounts, descriptions, and transaction types.
- Handle missing or unexpected Excel data safely.
- Never silently discard transactions that cannot be processed.

### Separation of concerns

Keep the application modular and maintainable.

Separate:
- API endpoints.
- Business logic.
- Database operations.
- Data models and validation schemas.
- Excel import and parsing.
- AI integrations.

Avoid putting unrelated responsibilities in a single file.

## 4. Technology Stack

### Initial technology decisions

| Component | Technology |
|---|---|
| Backend | Python |
| API Framework | FastAPI |
| Excel Processing | Pandas / OpenPyXL |
| AI Integration | OpenAI API |
| Initial Database | SQLite |
| Configuration | python-dotenv |
| Development Server | Uvicorn |

The frontend technology and production database have not yet been finalized.

Do not introduce additional frameworks or technologies without discussing their advantages and disadvantages first.

## 5. Suggested Project Structure

```text
ReachRich/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── excel_import.py
│   │   └── transaction_classifier.py
│   │
│   ├── database/
│   │
│   └── core/
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

This is a suggested structure. Adapt it according to actual project requirements without creating unnecessary abstractions.

## 6. Development Roadmap

Develop the application incrementally.

### Phase 1 – Backend Foundation
- Set up FastAPI.
- Configure Uvicorn.
- Create the main application entry point.
- Add a health-check endpoint.
- Configure the database connection.

### Phase 2 – Transaction Management
- Define transaction models.
- Create validation schemas.
- Implement transaction creation and editing.
- Implement database persistence.

### Phase 3 – Excel Import
- Support bank Excel files.
- Parse transaction data.
- Normalize dates, amounts, and descriptions.
- Handle different Excel formats.
- Prevent duplicate imports.
- Report invalid or unsupported rows.

### Phase 4 – AI Integration
- Integrate OpenAI API.
- Implement automatic transaction categorization.
- Validate AI responses.
- Support manual correction of classifications.

### Phase 5 – Financial Analysis
- Calculate income and expenses.
- Generate monthly and yearly summaries.
- Identify spending patterns.
- Add AI-powered financial insights.

### Phase 6 – Frontend
- Choose the frontend technology.
- Build a clear and intuitive user interface.
- Connect the frontend to the backend API.
- Present financial data visually.

Do not skip foundational phases to implement advanced features prematurely.

## 7. Coding Standards

When generating or modifying code:

- Prefer clean, readable, and maintainable Python.
- Use meaningful variable and function names.
- Use type hints.
- Follow FastAPI and Pydantic conventions.
- Keep functions focused on a single responsibility.
- Handle exceptions explicitly.
- Avoid unnecessary dependencies.
- Avoid duplicated code.
- Write reusable components where appropriate.
- Add tests for important business logic.
- Follow existing project conventions.

Do not refactor unrelated code when implementing a specific feature.

## 8. Security and Privacy

Financial information is sensitive.

- Never hardcode API keys or credentials.
- Store secrets in environment variables.
- Never commit `.env` to Git.
- Provide `.env.example` with placeholder values.
- Avoid logging sensitive financial information.
- Send only the minimum necessary information to external AI services.
- Validate all external inputs.
- Keep financial records separate from AI-generated content.

## 9. GitHub Copilot Working Guidelines

Before implementing a feature:

1. Inspect the existing project structure.
2. Understand the current implementation.
3. Identify which files need modification.
4. Follow the existing architecture.
5. Avoid introducing unnecessary complexity.

When requirements are unclear:
- Ask for clarification.
- Do not invent business rules.
- Explain important technical decisions.
- Present alternatives when architecture decisions are involved.

When implementing a feature:
- Make focused changes.
- Keep the application runnable.
- Add or update relevant tests.
- Explain what was changed.
- Explain how to run and verify the implementation.

Never claim that a command or test was executed unless it actually was.

## 10. General Development Philosophy

ReachRich should be developed as a real, maintainable software product — not just a quick prototype.

Prioritize:

1. Correctness and data reliability.
2. Clear architecture.
3. Security and privacy.
4. Maintainability.
5. Good user experience.
6. Useful AI capabilities.

Always prefer a simple, reliable solution over unnecessary complexity.