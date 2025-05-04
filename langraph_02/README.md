# AI Support Agent with LangGraph

## Project Overview

This project implements an AI support agent using LangGraph that can interact with users and hand off complex queries to a human support team. The agent uses Google's Gemini model as its foundation and implements an interrupt pattern with MongoDB for state persistence.

## Architecture

The system consists of these key components:

1. **LangGraph Agent Flow**: A directed graph that manages conversation flow between:
   - User input
   - AI model (Gemini 2.0 Flash)
   - Tool handling
   - Human support team handoff

2. **MongoDB Checkpointing**: Persists conversation state between interactions, allowing for:
   - Conversation history preservation
   - Agent state recovery after interrupts
   - Thread management across sessions

3. **Human Interrupt Pattern**: A specialized pattern that:
   - Detects when AI needs human assistance
   - Pauses execution and stores state in MongoDB
   - Resumes conversation when human support provides input

## How It Works

1. User submits a question to the AI agent
2. The agent processes the request using the Gemini model
3. If the request is complex or requires human judgment, the agent:
   - Triggers the `human_assistant_tool`
   - Stores conversation state in MongoDB
   - Waits for human support team input
4. When human support responds, the conversation resumes with that input
5. The agent continues the conversation or completes the request

## Key Files

- `graph.py`: Defines the LangGraph conversation flow and tools
- `main.py`: Entry point for direct user conversations
- `support.py`: Interface for human support team to view and respond to requests 
- `docker-compose.yml`: Sets up MongoDB container for state persistence

## Technologies Used

- **LangGraph**: Framework for building stateful, multi-step AI agents
- **MongoDB**: Database for state persistence and checkpointing
- **Google Gemini 2.0 Flash**: LLM powering the agent's responses
- **Docker**: Container for MongoDB instance

## Setup and Usage

1. Start the MongoDB container:
   ```
   docker-compose up -d
   ```

2. Run the main application for user interaction:
   ```
   python main.py
   ```

3. For support team members, run the support interface:
   ```
   python support.py
   ```

## Environment Variables

Create a `.env` file with:
```
GEMINI_API_KEY=your_key_here
```