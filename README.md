# Azure DevOps Pull Request Analyzer

An intelligent agent that analyzes Pull Requests in Azure DevOps and provides AI-powered reviews.

## Features
- **Automated PR Review**: Analyzes code changes using Azure OpenAI.
- **Smart Filtering**: Only reviews PRs targeting `main`, `master`, or `develop` branches.
- **Persistence**: Saves analysis results to Azure Cosmos DB.
- **Graceful Error Handling**: Continues analysis even if diff retrieval fails.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in `.env` (see `src/config.py`).

## Running the Application
To start the web server locally:
```bash
python main.py
```
The server will start at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Running Tests
To run the unit tests:
```bash
$env:PYTHONPATH="."; python -m pytest tests/ -v
```
