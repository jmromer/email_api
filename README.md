# Email API

## Dependencies

- Python 3.9
- [Poetry](https://python-poetry.org/docs/1.2) for dependency & package
  management

Python dependencies outlined in [`pyproject.toml`](pyproject.toml)

## Installation

```shell
poetry install
```

## Environment Configuration

To run the service locally, populate the `.env` or the environment with the
required env vars:

```shell
cp .env.example .env
```

## Usage

```shell
% poetry run start

INFO:     Started server process [4205]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Tests

```shell
% poetry run test

................                     [100%]
================== mypy ===================
Success: no issues found in 3 source files
16 passed in 1.22s
```

## Implementation time

`03:28`
