# ADHD AI Assistant

An AI-powered assistant specifically designed to help individuals with ADHD manage their tasks, routines, and daily life. Built with LangChain and OpenAI's GPT-4.

## Features

- Task Management

  - Create and track tasks
  - Set reminders
  - Update task status
  - Break down complex tasks into manageable steps

- ADHD-Specific Support

  - Clear, concise communication
  - Visual task organization
  - Time-blocking assistance
  - Positive reinforcement
  - Routine building

- User Profile Management
  - Track ADHD traits and preferences
  - Customize reminder times
  - Store task preferences

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd adhd-ai-assistant
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the CLI interface:

```bash
python -m adhd_assistant.cli
```

The assistant will help you:

- Create and manage tasks
- Set reminders
- Update task status
- Get your task list
- Update your profile
- Chat about your day and get ADHD-friendly advice

## Example Interactions

```
🧠 ADHD AI Assistant: Hello! I'm here to help you manage your tasks and daily life.

You: I need to write a report for work but I'm feeling overwhelmed

🧠 AI: Let's break this down into smaller steps! First, let's create a task for your report.
I'll help you set up a structured approach with clear deadlines.

You: Can you create a task for my report?

🧠 AI: I'll help you create a task. Let's break it down:
1. What's the title of your report?
2. When is it due?
3. Would you like me to set up some checkpoints along the way?
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
