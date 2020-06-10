import os
from .message import bot

# Shared logging import for both client and default.py (for headless)
RSE_LOG_LEVEL = os.environ.get("RSE_LOG_LEVEL", "INFO")
RSE_LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "QUIET", "FATAL"]
if RSE_LOG_LEVEL not in RSE_LOG_LEVELS:
    RSE_LOG_LEVEL = "INFO"
