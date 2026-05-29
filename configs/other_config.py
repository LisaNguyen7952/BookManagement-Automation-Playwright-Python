import os


from utils.string_helper import DateFormat

# BASE_URL = os.getenv("URL")
# USER_NAME = os.getenv("USER_NAME")
# LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
INVALID_EMAIL = "liisa@gmail.com"
INVALID_PASSWORD ="123456"
STORAGE_DIR = "./auth"
STORAGE_STATE = os.path.join(STORAGE_DIR, "storage_state.json")

DEFAULT_HEADLESS = False
DEFAULT_SLOW_MO = "500"

SCREENSHOT_DIR = "screenshots"
LOG_DIR = "logs"
VIEWTRACE_DIR = "traceview"
DIALOG_ACTIONS = {"accept", "dismiss", "prompt"}


DEFAULT_SCREEN_PARTIAL_URL = "dashboard"
CLIENT_PARTIAL_URL = "client"
LEAD_PARTIAL_URL = "lead"

UI_DATE_FORMAT = DateFormat.MMDDYYYY