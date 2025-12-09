
# Chat with OpenAI

A simple web app example using FastAPI and Semantic Kernel. User is able to talk to AI about anything using prompts. AI is able to understand state of lights introduced in lights_plugin.py and control them on request.

## Quick Start

To run this app, open terminal in the `semantic-kernel-test` folder and run:

Create .env file and edit it. You need to give your OpenAI API key and the used AI model.
cp .env.example .env

```bash
make run
```

The server will start listening on **port 8080**. You can change the port in the `main.py file`.

This command will also automatically install all dependencies defined in the `Pipfile`.

## Available Make Commands

### `make env`
Enter the pipenv shell for interactive work.  
Only needed if you want to run commands interactively in the virtual environment.

### `make setup`
Install dependencies defined in the `Pipfile` into the virtual environment.  
Use this after adding new dependencies to `Pipfile`.

### `make run`
Run the application. This also installs all dependencies when needed.
Then open a web page: http://localhost:8080

### `install-service`
Install as systemd service (requires sudo). Service expects that code is located here: /opt/my/semantic-kernel-test

### `uninstall-service`
Uninstall systemd service (requires sudo)

### `make clean`
Remove cache files and delete the virtual environment to free up space.

### `make clean-all`
Complete clean including removal of `Pipfile.lock`.

**Note:** Virtual environment is created at `~/.local/share/virtualenvs`

The location varies by operating system:
- **Linux/macOS:** `~/.local/share/virtualenvs/`
- **Windows:** `%USERPROFILE%\.virtualenvs\`

To create the virtual environment inside the project folder instead (as `.venv`), set:
```bash
export PIPENV_VENV_IN_PROJECT=1
```

### Getting started with Semantic Kernel
https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide?pivots=programming-language-python

### Examples in Github
https://github.com/microsoft/semantic-kernel