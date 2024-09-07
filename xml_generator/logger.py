import logging


def setup_logger(name, level=logging.DEBUG, format='%(asctime)s - %(name)-14s - %(levelname)-8s - %(message)s'):
    """
    Setup a logger with the given name, level, and format.
    
    :param name: Name of the logger.
    :param level: Logging level (e.g., logging.DEBUG, logging.INFO).
    :param format: Log message format string.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a console handler with the specified log level and format
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(format)
    ch.setFormatter(formatter)
    
    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)
    
    return logger


def log_message(logger, level, message):
    """
    Log a message with the specified logging level.
    
    :param level: Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    :param message: Message to log.
    """
    
    if isinstance(level, int):
        # Convert integer level to corresponding string level
        level = logging.getLevelName(level)
    elif isinstance(level, str):
        # Ensure level is in uppercase
        level = level.upper()
        
    log_func = getattr(logger, level.lower(), None)
    if log_func:
        log_func(message)
    else:
        raise ValueError(f"Invalid log level: {level}")

