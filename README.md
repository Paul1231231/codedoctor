# CodeDoctor

AI-powered debugging and regression testing platform.

## Problem

Developers frequently spend significant time diagnosing runtime
errors and understanding unfamiliar code failures.

CodeDoctor analyzes source code and error information to identify
likely root causes and propose fixes.

## Architecture

TODO

## Tech Stack

- Python
- FastAPI
- Pydantic
- Alibaba Cloud Model Studio
- Qwen
- uv

## Development

```bash
uv sync
uv run fastapi dev src/codedoctor/main.py