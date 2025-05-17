import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(console_handler)
    return logger
