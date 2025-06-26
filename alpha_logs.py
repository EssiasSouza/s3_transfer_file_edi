version = "3.0.0"

import logging
from logging.handlers import TimedRotatingFileHandler
import os

def checking_logs_folder(logs_path):
    message = ""
    if logs_path:
        if not os.path.exists(logs_path):
            message = f"The directory {logs_path} does not exist. Creating it..."
            os.mkdir(logs_path)
    else:
        logs_path = './logs'
        os.mkdir(logs_path)
        message = "logs_path is missing in the settings.json"
    return message

def setup_logger(log_full_path):
    """Setup and return a logger for the specified log_name."""
    full_log_path = os.path.join(log_full_path)
    logger = logging.getLogger(log_full_path)
    if logger.hasHandlers():
        logger.handlers.clear()
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = TimedRotatingFileHandler(full_log_path, when="midnight", interval=1, backupCount=7, encoding='utf-8')
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S -')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_print(level, log_full_path, message):
    """Log a message with the specified log level and log file."""
    logger = setup_logger(log_full_path)
    print(message)
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'debug':
        logger.debug(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)
    else:
        logger.log(logging.NOTSET, message)


def log_SQL_message(message, log_name):
    def treating_message(message):
        if message == "OK":
            message = "Task completed succesfully"
            type_return = "info"
            return message, type_return
        else:
            type_return = "error"
            return message, type_return
    returning, type_return = treating_message(message)
    log_print(type_return, log_name, returning)