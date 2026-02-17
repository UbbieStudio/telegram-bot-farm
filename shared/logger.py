import logging
import sys

def get_logger(name: str):
    """
    Creates a standardized logger for all bots in the farm.
    Outputs to the console (STDOUT) so Docker can capture the logs.
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(name)