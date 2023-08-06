import logging

from seleniumbot.core import SeleniumBot, SeleniumClient, Action

# Output seleniumwire logs only if it's WARNING level.
# Reason: Seleniumwire outputs a lot of INFO level logs.
logger = logging.getLogger('seleniumwire')
logger.setLevel(logging.WARNING)
