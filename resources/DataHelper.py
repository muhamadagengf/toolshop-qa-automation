import time
import json
import os

class DataHelper:
    """Helper library for generating unique test data and reading test data files."""

    def generate_unique_user(self):
        timestamp = int(time.time() * 1000)
        return {
            "first_name": "Ageng",
            "last_name": f"Tester{timestamp % 10000}",
            "dob": "1992-06-18",
            "street": "Jalan Otomasi No. 42",
            "house_number": "42",
            "postal_code": "12345",
            "city": "Jakarta",
            "state": "DKI Jakarta",
            "country": "ID",
            "phone": f"0812{timestamp % 100000000:08d}",
            "email": f"ageng_qa_{timestamp}@toolshop-test.org",
            "password": f"Logique{timestamp}!Zx9"
        }

    def load_json_data(self, relative_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
