import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Ensure the logger is initialized only once
        if not hasattr(self, 'initialized'):

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            self.logger = logging.getLogger("logger")

            # Get log level from environment variable
            log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
            self.loglevel = getattr(logging, log_level_str, logging.INFO)

            # Set log level
            self.logger.setLevel(self.loglevel)

            # Check if logging to file is enabled
            write_to_file = os.getenv("WRITE_TO_FILE", "false").lower() == "true"

            # Avoid adding handlers multiple times
            if not self.logger.handlers:
                if write_to_file:
                    # Create log directory if it doesn't exist
                    log_dir = Path(__file__).parent / 'log'
                    log_dir.mkdir(exist_ok=True)

                    # File handler - overwrites on each restart
                    log_file = log_dir / 'chat.log'
                    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
                    file_handler.setFormatter(formatter)
                    file_handler.setLevel(self.loglevel)
                    self.logger.addHandler(file_handler)
                else:
                    # Console handler
                    stdout_handler = logging.StreamHandler(sys.stdout)
                    stdout_handler.setFormatter(formatter)
                    stdout_handler.setLevel(self.loglevel)
                    self.logger.addHandler(stdout_handler)

            self.initialized = True

    def info(self, message):
        """Logs an info message"""
        self.logger.info("%s", message)

    def debug(self, message):
        """Logs a debug message"""
        self.logger.debug("%s", message)

    def warning(self, message):
        """Logs an warning message"""
        self.logger.warning("%s", message)

    def error(self, message):
        """Logs an error message"""
        self.logger.error("%s", message)

# Example of how to use the Logger class
if __name__ == "__main__":
    logger = Logger()
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
