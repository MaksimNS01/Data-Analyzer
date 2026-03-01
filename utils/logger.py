# Import necessary libraries
import logging  # Standard Python library for logging
import os  # Library for working with the operating system and files
from datetime import datetime  # Library for working with date and time

class AppLogger:
    """
    A class for logging application activity with the option to enable/disable it.

    Provides:
        - Saving logs to files with the date in the name
        - Outputting logs to the console
        - Different logging levels (debug, info, warning, error)
        - Formatting messages with timestamps
        - Ability to enable/disable logging
    """

    def __init__(self, logs_dir: str = None, enabled: bool = True):
        """
        Initialization of the logging system.

        Configures:
            - Directory for storing logs
            - Message formatting
            - Handlers for file and console
            - Logging levels
            - Logging on/off status

        Args:
            logs_dir (str): Path to the directory for logs. If None, "logs" in the current directory is used.
            enabled (bool): Flag to enable/disable logging (default True)
        """
        self._enabled = enabled

        if not self._enabled:
            return  # If logging is disabled, do not initialize handlers

        # Use the passed directory or create a default one
        if logs_dir is None:
            self.logs_dir = "logs"
        else:
            self.logs_dir = logs_dir

        # Create a directory to store log files
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # Generate a log file name with the current date
        # Format: chat_app_YYYY-MM-DD.log
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"{current_date}.log")

        # Setting the log message format
        # Format: YYYY-MM-DD HH:MM:SS - LEVEL - Message
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',  # Message template
            datefmt='%Y-%m-%d %H:%M:%S'                   # Date and time
        )

        # Create and configure a handler for writing to a file
        file_handler = logging.FileHandler(
            log_file,           # Path to the log file
            encoding='utf-8'    # Encoding for Unicode support
        )
        file_handler.setFormatter(formatter)  # Set formatting

        # Create and configure a handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)  # Set the same formatting

        # Configure the main application logger
        self.logger = logging.getLogger('ParserApp')  # Создание логгера с именем
        self.logger.setLevel(logging.DEBUG)      # Set the logging level
        self.logger.addHandler(file_handler)     # Add a file handler
        self.logger.addHandler(console_handler)  # Add a console handler

    def enable(self):
        """
        Enable logging.
        """
        self._enabled = True
        if not hasattr(self, 'logger'):
            # If the logger has not been initialized, initialize it.
            self._init_logger()

    def disable(self):
        """
        Disable logging.
        """
        self._enabled = False

    def is_enabled(self) -> bool:
        """
        Check whether logging is enabled.

        Returns:
            bool: True if logging is enabled, False if disabled
        """
        return self._enabled

    def _init_logger(self):
        """
        Initialize the logger (called when logging is enabled).
        """
        # Generate log file name with current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"{current_date}.log")

        # Setting the log message format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

         # Creating and configuring a handler for writing to a file
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Create and configure a handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Configure the main application logger
        self.logger = logging.getLogger('ParserApp')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """
        Logging an informational message.

        Used to record important information about the application's operation:
            - Successful operations
            - Execution status
            - Status information

        Args:
            message (str): Text of the informational message
        """
        if not self._enabled:
            return
        self.logger.info(message)

    def error(self, message: str, exc_info=None):
        """
        Logging an error.

        Used to record information about errors:
            - Exceptions
            - Failures
            - Critical errors

        Args:
            message (str): Error message text
            exc_info: Exception information (default None)
        """
        if not self._enabled:
            return
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str):
        """
        Logging debug information.

        Used to record detailed information for debugging:
            - Variable values
            - Intermediate results
            - Execution details

        Args:
            message (str): Debug message text
        """
        if not self._enabled:
            return
        self.logger.debug(message)

    def warning(self, message: str):
        """
        Warning logging.

        Used to record warnings:
            - Potential problems
            - Undesirable situations
            - Status warnings

        Args:
            message (str): Warning text
        """
        if not self._enabled:
            return
        self.logger.warning(message)


# Functions for convenient logger creation
def create_logger(logs_dir: str = None, enabled: bool = True) -> AppLogger:
    """
    Create a logger instance..

    Args:
        logs_dir (str): Path to the directory for logs
        enabled (bool): Flag to enable/disable logging

    Returns:
        AppLogger: Logger instance
    """
    return AppLogger(logs_dir, enabled)


def create_enabled_logger(logs_dir: str = None) -> AppLogger:
    """
    Create an enabled logger.

    Args:
        logs_dir (str): Path to the directory for logs

    Returns:
        AppLogger: Instance of an enabled logger
    """
    return AppLogger(logs_dir, enabled=True)


def create_disabled_logger(logs_dir: str = None) -> AppLogger:
    """
    Create a disabled logger.

    Args:
        logs_dir (str): Path to the directory for logs

    Returns:
        AppLogger: Instance of a disabled logger
    """
    return AppLogger(logs_dir, enabled=False)


# Пример использования
if __name__ == "__main__":
    # Example 1: Creating an enabled logger
    logger_enabled = create_enabled_logger()
    logger_enabled.info("This message will be recorded in the log")
    logger_enabled.error("This error message will be recorded in the log")

    # Example 2: Creating a disabled logger
    logger_disabled = create_disabled_logger()
    logger_disabled.info("This message will NOT be recorded in the log")
    logger_disabled.error("This error message will NOT be recorded in the log")

    # Example 3: Dynamic enable/disable
    logger_dynamic = AppLogger(enabled=False)  # Create disabled
    logger_dynamic.info("This message will NOT appear in the log")

    logger_dynamic.enable()  # Enable logging
    logger_dynamic.info("This message will now be recorded in the log")

    logger_dynamic.disable()  # Disable logging
    logger_dynamic.info("This message will NOT be recorded in the log again")

    # Checking the status
    print(f"Logger enabled: {logger_dynamic.is_enabled()}")

    # Example with a flag from an external source (e.g., command line arguments)
    import sys
    log_enabled = "--debug" in sys.argv or "--verbose" in sys.argv
    dynamic_logger = AppLogger(enabled=log_enabled)

    if log_enabled:
        dynamic_logger.info("Logging enabled via command line arguments")
    else:
        dynamic_logger.info("Logging disabled")
