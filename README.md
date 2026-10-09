
# CodeDoctor

**An LLM-powered code analysis and debugging assistant with structured outputs and safety guardrails.**

CodeDoctor is a personal software engineering project that explores how to build a more reliable LLM-powered developer tool. It analyzes source code and error information to help identify potential root causes and suggest fixes.

Rather than relying on an LLM response alone, the project explores structured output validation and security checks to make model interactions more predictable and safer to handle.

## Overview

Debugging unfamiliar code can be time-consuming. Developers often need to understand error messages, trace potential causes, and determine what changes might resolve a problem.

CodeDoctor aims to streamline this process by combining an LLM with application-level validation and safeguards.

### Key Features

- **LLM-powered code analysis** — Analyze source code and error information to identify potential causes of failures and suggest fixes.
- **Structured outputs** — Use Pydantic models to define and validate the expected shape of model responses.
- **LLM guardrails** — Explore Guardrails AI to validate model outputs against defined requirements.
- **Security checks** — Add checks for potentially malicious prompt instructions and sensitive information, such as personally identifiable information (PII).
- **API-based architecture** — Use FastAPI to expose application functionality.
- **Configurable LLM integration** — Use LiteLLM and model-provider configuration to connect to supported LLMs.

> Note: Guardrails and security checks provide additional protection, not a guarantee that every unsafe input or output will be detected. CodeDoctor should not be considered a production-grade secure execution environment.

## Architecture

At a high level, the intended request flow is:

```text
User / Client
      |
      v
   FastAPI
      |
      v
Code Analysis Service
      |
      v
  LLM Client
      |
      v
Configured LLM Provider
      |
      v
Structured Output Validation
      |
      v
Guardrails and Security Checks
      |
      v
Validated Response
```

The diagram describes the conceptual workflow. The exact execution order depends on the implementation of each component.

### Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Main programming language |
| FastAPI | API framework |
| Pydantic | Data models and structured validation |
| LiteLLM | LLM integration |
| Guardrails AI | Output validation and guardrails |
| Qwen / Alibaba Cloud Model Studio | Model and provider used in development |
| uv | Dependency and project management |
| pytest | Automated testing |

## Project Structure

```text
codedoctor/
├── litellm/               # LLM-related configuration or resources
├── src/
│   └── codedoctor/        # Application source code
├── tests/                 # Automated tests
├── .env.example           # Environment variable template
├── .gitignore
├── .python-version
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependency versions
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- An API key and access to a compatible LLM provider, if required by your configuration

### 1. Clone the repository

```bash
git clone https://github.com/Paul1231231/codedoctor.git
cd codedoctor
```

### 2. Install dependencies

```bash
uv sync --group dev
```

This installs the project dependencies and development dependencies defined in `pyproject.toml`.

### 3. Configure environment variables

Copy the example environment file:

**macOS / Linux**

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

Configure the required model-provider credentials and settings using the variable names defined in `.env.example`.

Do not commit `.env` or expose API keys in source code.

### 4. Start the application

```bash
uv run fastapi dev src/codedoctor/main.py
```

When the server starts successfully, open the local API documentation at:

http://127.0.0.1:8000/docs

The available endpoints and request schemas can be explored through the interactive API documentation.

## Running Tests

Run the test suite with:

```bash
uv run pytest
```

To run a particular test file:

```bash
uv run pytest tests/unit/test_analyzer.py
```

The second command assumes that the test file exists at that location. Adjust the path to match the current test structure.

## Design Considerations

### 1. Structured Output

LLM responses are not inherently guaranteed to follow a required schema.

CodeDoctor uses structured data models and validation to make responses easier for the application to consume. Invalid responses should be handled explicitly rather than blindly passed to downstream components.

### 2. Guardrails and Security

LLM applications must account for untrusted inputs and potentially unsafe outputs.

CodeDoctor explores checks for:

- Prompt injection and attempts to override intended instructions.
- Potential exposure of personally identifiable information.
- Responses that do not conform to the expected structure.
- Invalid or unexpected model outputs.

These checks are defense-in-depth measures. They require testing against realistic attack cases and should not be treated as a complete security boundary.

### 3. Separation of Responsibilities

Separating API handling, analysis logic, model integration, validation, and security checks makes the codebase easier to test and maintain.

It also helps keep model-specific behavior separate from the application's core logic.

## Current Status

CodeDoctor is an undergraduate personal project focused on learning and applying LLM application engineering.

The current scope emphasizes code analysis, structured responses, and safety checks. The project can be extended in the future with additional execution isolation, broader language support, and more comprehensive security testing.

## Limitations

- LLM-generated explanations and fixes may be incorrect.
- Output validation does not guarantee the semantic correctness of a response.
- Prompt-injection and PII detection may produce false positives or miss certain cases.
- Running untrusted code requires a separate, properly isolated execution environment.

CodeDoctor should be treated as a development and learning tool, not as a replacement for code review, automated testing, or dedicated security analysis.

## Future Work

Possible future improvements include:

- [ ] Add a reproducible end-to-end demonstration.
- [ ] Expand unit and integration test coverage.
- [ ] Evaluate guardrails against a collection of adversarial inputs.
- [ ] Add a sandbox for executing untrusted code with appropriate isolation and resource limits.
- [ ] Explore support for multiple programming languages.
- [ ] Add continuous integration to run tests automatically.

## Learning Objectives

This project has helped me explore:

- Building APIs with FastAPI.
- Integrating LLM providers into Python applications.
- Defining and validating structured model outputs.
- Applying guardrails to LLM inputs and outputs.
- Thinking about prompt injection, PII, and defense-in-depth security.
- Organizing a Python project for testing and maintainability.

## Author

**Paul Li**

GitHub: [@Paul1231231](https://github.com/Paul1231231)

---

This project is developed for educational purposes.
