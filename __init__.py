#!/usr/bin/env python
import dotenv
import logging
import os

# Load .env file into os.environ from a directory above
dotenv.load_dotenv(dotenv.find_dotenv())

def create_logger(name:str, logging_level:str, logging_format:str):
    # create console handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(logging_format)
    # set logging formatter
    handler.setFormatter(formatter)
    # create named logger
    logger=logging.getLogger(name)
    # set logging level
    logger.setLevel(logging_level)
    logger.addHandler(handler)
    logging.info("Initialized logging level to: '%s'", logging_level)
    logging.info("Initialized logging format to: '%s'", logging_format)
    logging.info("Successfully initiated ConsoleHandler logger")
    return logger

def modify_logger(logger, logging_level, logging_format):
    # create console handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(logging_format)
    # set logging formatter
    handler.setFormatter(formatter)
    handlers = logger.handlers.copy()
    for handler in handlers:
        # Copied from `logging.shutdown`.
        try:
            handler.acquire()
            handler.flush()
            handler.close()
        except (OSError, ValueError):
            pass
        finally:
            handler.release()
        logger.removeHandler(handler)
    logger.addHandler(handler)
    if not logging_level in {'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'}:
        raise ValueError('Could not interpret "LOG_LEVEL" environment value "' + logging_level + '" as a valid logging level name. Accepted values (case insensitive):\n * CRITICAL\n * FATAL\n * ERROR\n * WARNING\n * WARN\n * INFO\n * DEBUG\n * NOTSET')
    logger.setLevel(logging_level)
    logging.info("Initialized logging level to: '%s'", logging_level)
    logging.info("Initialized logging format to: '%s'", logging_format)
    logging.info("Successfully initiated ConsoleHandler logger")
    
def retry_infinite(func):
    def retry(*args,**kwargs):
        try:
            pass
        except Exception as error:    
            pass

if __name__ == "__main__":
    global DEFAULT_LOG_LEVEL
    global DEFAULT_LOG_FORMAT
    DEFAULT_LOG_FORMAT='[%(asctime)s] %(levelname)-8s (%(name)s) <%(module)s.py>.%(funcName)s: %(message)s'
    DEFAULT_LOG_LEVEL='WARNING'
    logger=create_logger('root', DEFAULT_LOG_LEVEL, DEFAULT_LOG_FORMAT)
    # ===================
    # LOG_LEVEL
    # ===================
    try:
        global LOG_LEVEL
        global LOG_LEVEL_UPPER
        LOG_LEVEL = os.environ.get("LOG_LEVEL")
        if isinstance(LOG_LEVEL,str):
            LOG_LEVEL_UPPER=LOG_LEVEL.upper()
        elif LOG_LEVEL is None:
            raise TypeError('Undefined environment variable LOG_LEVEL.')
        else:
            raise TypeError('Environment variable LOG_LEVEL is not a string.')
    except Exception as exc:
        logging.warning("Failed to initialize logging level by using \"LOG_LEVEL\" environment variable: '%s'.", LOG_LEVEL)
        LOG_LEVEL_UPPER=DEFAULT_LOG_LEVEL
        logging.info("Using default logging level: '%s'", DEFAULT_LOG_LEVEL)
    try:
        global LOG_FORMAT
        LOG_FORMAT = os.environ.get("LOG_FORMAT")
        if LOG_FORMAT is None:
            raise TypeError('Undefined environment variable LOG_FORMAT.')
        elif not isinstance(LOG_FORMAT,str):
            raise TypeError('Environment variable LOG_FORMAT is not a string.')
    except Exception as exc:
        logging.warning("Failed to initialize logging format by using \"LOG_FORMAT\" environment variable: '%s'", LOG_FORMAT)
        LOG_FORMAT=DEFAULT_LOG_FORMAT
        logging.info("Using default logging format '%s'", DEFAULT_LOG_FORMAT)

    if not LOG_LEVEL_UPPER in {'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'}:
        logging.warning('Could not interpret "LOG_LEVEL" environment value "' + LOG_LEVEL + '" as a valid logging level name. Accepted values (case insensitive):\n * CRITICAL\n * FATAL\n * ERROR\n * WARNING\n * WARN\n * INFO\n * DEBUG\n * NOTSET')
        LOG_LEVEL_UPPER=DEFAULT_LOG_LEVEL
    modify_logger(logger=logger, logging_level=LOG_LEVEL_UPPER,logging_format=LOG_FORMAT)
