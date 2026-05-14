SHELL := bash
.ONESHELL:
.SHELLFLAGS := -ecx
PYTHON := python3
PORT := 8001

# Call this only if you need to enter shell and work interactive there
env:
	pipenv install --dev
	pipenv shell

# You can call this directly to install dependencies defined in Pipfile in the virtual env
# You could call this also after you have added new dependencies in Pipfile
setup:
	pipenv install --dev

# Call this if you want to run the app in virtual env. This will also install all dependencies in defined pipfile in the virtual env
run: setup
	pipenv run uvicorn app.main:app --reload --log-config log_settings.yaml --host 0.0.0.0 --port $(PORT)

# Install as systemd service (requires sudo)
install-service:
	sudo cp agent-ui.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable agent-ui.service
	@echo "Service installed. Start with: sudo systemctl start agent-ui"

# Uninstall systemd service (requires sudo)
uninstall-service:
	sudo systemctl stop agent-ui.service || true
	sudo systemctl disable agent-ui.service || true
	sudo rm -f /etc/systemd/system/agent-ui.service
	sudo systemctl daemon-reload
	@echo "Service uninstalled"

# Virtual env is created here: ~/.local/share/virtualenvs
# Call this when you want to free up space or reset all dependencies
# pipenv --rm should remove the virtual env 
clean:
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf .pytest_cache
	rm -rf ./app.log
	pipenv --rm

# Call this to do a complete clean including removing the Pipfile.lock
clean-all: clean
	rm -rf Pipfile.lock
