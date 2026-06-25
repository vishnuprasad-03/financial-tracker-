"""
Logging configuration for Finance Tracker.
"""

import logging
import logging.config
import yaml


with open("logging.yaml", "r") as file:
    config = yaml.safe_load(file)

logging.config.dictConfig(config)

logger = logging.getLogger(__name__)