import logging 

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,  # Set log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Log format
    )
    return logging.getLogger(__name__)
