# Coding agent 

This coding agent was created by following this course: https://www.boot.dev/courses/build-ai-agent-python
## Setup

To set up the project, run the following commands:

```bash
uv init --no-package
uv add openai==2.44.0
uv add python-dotenv==1.1.0
```

Create a file .env in the project root folder:
```
OPENROUTER_API_KEY='<<add_your_key_here>>'
```

## Usage

```bash
uv run main.py "write a test file in current dir, named hello_world.txt, with content: hello world!"
```


