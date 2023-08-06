import argparse
import sys
import logging

from . import __version__

REQUIRED_PYTHON = (3, 10)

LOG_FORMAT = '%(asctime)-15s %(levelname)-8s %(name)-15s %(message)s'


def validate_python():
    """Validate that the right Python version is running."""
    if sys.version_info[:2] < REQUIRED_PYTHON:
        print(f"Error: {__package__} requires at least Python "
              f"v{REQUIRED_PYTHON}")
        sys.exit(1)


def log_setup(loglevel='INFO'):
    """Start logging write version"""
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    logger = logging.getLogger(__package__)
    logger.info(f"Starting {__package__} v{__version__}")
    logger.info(f'Changing log level to: {loglevel}')
    logger.setLevel(loglevel)


def get_parser():
    parser = argparse.ArgumentParser(description="Remotely access to your PLC, with auto discover feature", prog=__package__)
    parser.add_argument("--version", action="version", version=f'{__package__} v{__version__}')
    parser.add_argument('--loglevel', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set log level, Defaults to INFO')
    return parser


if __name__ == '__main__':
    validate_python()
    args = get_parser().parse_args()
    log_setup(args.loglevel)
