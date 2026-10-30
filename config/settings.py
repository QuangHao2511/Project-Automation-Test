# D:\download\Project Automation Test\config\settings.py
from pathlib import Path
import os
from dotenv import load_dotenv
from pathlib import Path

# Path(__file__) = D:\download\Project Automation Test\config\settings.py
# .parent        = D:\download\Project Automation Test\config
# .parent.parent = D:\download\Project Automation Test (GỐC DỰ ÁN)
BASE_DIR = Path(__file__).resolve().parent.parent

# Tải cấu hình từ file .env tại thư mục gốc
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

# --- CÁC ĐƯỜNG DẪN TỪNG TẦNG ---
DATA_DIR = BASE_DIR / "data"
TEST_DATA_JSON = DATA_DIR / "test_data.json"

REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
AUTH_STATE_FILE = REPORTS_DIR / "state" / "auth_state.json"

# Biến môi trường
BASE_URL = os.getenv("BASE_URL", "https://example.com")
USERNAME = os.getenv("TEST_USER", "standard_user")
PASSWORD = os.getenv("TEST_PASSWORD", "secret_pass")


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DATA_JSON = BASE_DIR / "data" / "test_data.json"