import os
import sys

def get_install_dir():
    """Returns the base directory where the app is installed."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

INSTALL_DIR = get_install_dir()

SCREENSHOT_DIR = os.path.join(INSTALL_DIR, "screenshots")
TEMPLATE_DIR = os.path.join(INSTALL_DIR, "templates")
CLAIMER_EXE_PATH = os.path.join(INSTALL_DIR, "daily_claim_runner.exe")

# Create screenshots folder at runtime
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
