import os
import json
from dotenv import load_dotenv

load_dotenv(".env.testAcc")

ENV = os.getenv("ENV", "dev")

def load_config():
    with open(f"configs/{ENV}.json") as f:
        return json.load(f)

config = load_config()

BASE_URL = config["base_url"]
TIMEOUT = config["timeout"]

EMAIL = os.getenv("USER_NAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")
BOOK_CATEGORY_LIST = ['Bình tĩnh sống', 'Phương Nam', 'Test', 'Adventure', 'Advertisement',
                          'Bền bỉ sẽ thành công thui nè', 'Blogger', 'Category 1', 'Category not exist', 'Chậm 1 chút',
                          'Chuột Book Store', 'Có chí ắt thành công', 'Default Category 1', 'Default Category 2',
                          'Đoàn Giỏi', 'Đón', 'Đón tết 2026', 'Đón tết 25122025', 'Đón tết nao cả nhà ưi',
                          'Đón tết thui cả nhà ưi', 'Early Book', 'engineering', 'Entertainmance', 'Fiction',
                          'Last Minute', 'Ngày 25122025', 'Ngày 2512202501', 'Ngày 2512202502', 'Ngày 2512202503',
                          'Normal book', 'novel', 'Phương Nam', 'PROMO_2gG1y', 'Sách thực tế 22122025 lần 1',
                          'std Slytherin L', 'Story', 'Tây Nam Bộ', 'Test', 'tham4', 'Truyện not exist',
                          'Truyện, Entertainmance']
PROMOTION_LIST = ["COCHI241220250123456789","COCHI24122025012345678","COCHI241220250123456","COCHI2412202501234567"]
PICTURE_LIST = ["VJ703_13-01-2026.png","616194573_3384053701750492_4966226566346009925_n.jpg","download.jpeg"]
LOGIN_INCORRECT_PASSWORD = "abcdhs"
LOGIN_FAIL_ALERT = "Authentication failed!"

TASK_STATUSES = ["To do", "In progress", "Done"]

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PICTURE_TEST_DATA_DIR = (
    PROJECT_ROOT / "data" / "picture_test_data"
)

def resource_path(*paths):
    return PROJECT_ROOT / "resources" / Path(*paths)

UPLOAD_FILE_PATH = resource_path("images", "scrence.jpeg")
UPLOAD_FILE_NAME = UPLOAD_FILE_PATH.name