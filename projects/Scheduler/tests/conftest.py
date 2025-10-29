
import logging
import os
import pytest
import sys

curr_dir = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(curr_dir):
    for dir in dirs:
        sys.path.append(os.path.join(root, dir))

sys.path.append(curr_dir)


@pytest.fixture(scope='session')
def logger():
    """
    Returns a logger that streams to stdout and a file.
    """
    # DEBUG - pipeline artifact
    logging.getLogger().setLevel(logging.DEBUG)

    # INFO - console logs
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)-15s [%(levelname)-8s] [%(funcName)-40s]  %(message)s"
    )
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    return logging.getLogger("__name__")
