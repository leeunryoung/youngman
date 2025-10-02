# Gemini Code Assistant Context

## Project Overview

This project is a Korean chatbot designed to provide information about youth policies. It's built with Python and utilizes a combination of a web framework, a large language model, and a vector database to deliver answers.

- **Backend:** The core of the application is a FastAPI server that exposes an API for asking questions.
- **Language Model:** It uses LangChain with OpenAI's `gpt-4o-mini` to understand and respond to user queries in Korean.
- **Data Store:** Policy documents are stored and retrieved using ChromaDB, a vector store, which allows for efficient semantic search.
- **Frontend:** A simple HTML page with JavaScript provides a user interface for interacting with the chatbot.

The chatbot is designed to be an expert on youth policies, capable of answering questions and classifying them into relevant categories like "jobs," "housing," and "education."

## Building and Running

This project has two main ways to run: as a web server or as a command-line application.

### Running the Web Server

To start the web server, you'll need to run the `main.py` file located in the `api` directory. This will start a `uvicorn` server.

```bash
# Navigate to the api directory
cd api

# Run the uvicorn server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Once the server is running, you can access the chatbot's user interface by opening the `templates/index.html` file in your web browser.

### Running the Command-Line Interface

To interact with the chatbot directly from your terminal, you can run the `main.py` file in the project's root directory.

```bash
python main.py
```

This will start an interactive session where you can type your questions and receive answers from the chatbot.

## Development Conventions

- **Language:** The primary language for both the code and the user-facing content is Korean.
- **Agent-based Architecture:** The project uses a LangChain agent to process user input. This agent is equipped with custom tools for question-answering and classification.
- **RAG for QA:** The question-answering tool is based on the Retrieval-Augmented Generation (RAG) pattern. It retrieves relevant policy documents from the ChromaDB vector store and uses them to generate an informed answer.
- **Modular Structure:** The code is organized into several modules, each with a specific responsibility:
    - `policy_data_loader.py`: Handles loading and processing of policy documents.
    - `agent_setup.py`: Creates and configures the LangChain agent.
    - `tools.py`: Defines the custom tools used by the agent.
    - `api/main.py`: Contains the web server and API logic.
    - `main.py`: Provides the command-line interface.
- **Environment Variables:** The project uses a `.env` file to manage environment variables, such as the OpenAI API key. Make sure to create a `.env` file and add your API key before running the application.
