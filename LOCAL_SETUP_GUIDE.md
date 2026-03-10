# Azure AI DevOps Agent - Local Setup Guide

This guide provides step-by-step instructions on how to set up, configure, and run the Azure AI DevOps Agent and its accompanying dashboards on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your laptop/local machine:
- **Python 3.9+** (Ensure `python` and `pip` are added to your system PATH)
- **Git** (for cloning the repository)

---

## Step 1: Clone the Repository

First, download the source code from GitHub to your local machine:

```powershell
git clone https://github.com/Srk-1974/ai_devops_agent_calude.git
cd ai_devops_agent_calude
```

## Step 2: Configure Environment Variables

The application requires certain credentials (like Azure DevOps tokens and OpenAI keys) to function. **These should never be committed to GitHub.** 

1. In the root directory, locate the `.env.example` file.
2. Create a new file named exactly `.env` in the same directory.
3. Copy the contents of `.env.example` into your new `.env` file.
4. Fill in the required values. For local testing without connecting to real Azure services, you can use placeholder values:

```env
# Example .env file for local testing
ADO_ORGANIZATION=test-org
ADO_PROJECT=test-project
ADO_PAT=test-pat

AZURE_OPENAI_ENDPOINT=https://test.openai.azure.com/
AZURE_OPENAI_API_KEY=test-key

# General
ENVIRONMENT=development
```

## Step 3: Install Dependencies

Install all the required Python libraries needed to run the backend and the dashboards:

```powershell
pip install -r requirements.txt
```

---

## Step 4: Running the Dashboards

This project provides two different dashboards you can use. You can run one or both.

### Option A: The Modern HTML/FastAPI Dashboard (Recommended)

This is the primary dashboard served directly by the backend API.

1. **Start the server:**
   ```powershell
   python main.py
   ```
2. **Access the Application:**
   Open your web browser and navigate to: **http://localhost:8000/**

You will see the "AI PR Analyzer" dashboard indicating that "Services are Online" in green. 
- *Note: Leave the terminal window open to keep the server running.*
- To view interactive API documentation and test webhooks, visit **http://localhost:8000/docs**

### Option B: The Streamlit Management Console

If you want to use the alternative Streamlit data dashboard:

1. Ensure your backend API is already running using the `python main.py` command (from Option A).
2. Open a **new**, separate terminal window.
3. Navigate to the project directory:
   ```powershell
   cd path/to/ai_devops_agent_calude
   ```
4. **Start the Streamlit app:**
   ```powershell
   streamlit run app_streamlit.py
   ```
5. Your browser will automatically open to **http://localhost:8501/**.
6. The dashboard should connect to your local backend and show "Backend: Online".

---

## Troubleshooting

- **"Backend: Offline" in Streamlit:** Ensure that `python main.py` is actively running in another terminal. The Streamlit app relies on the `main.py` server to fetch its data.
- **Port already in use error:** If you get an error saying port 8000 or 8501 is in use, you likely have another instance of the application running. Close your old terminals or use Task Manager / Activity Monitor to stop old Python processes.
