# utils/file_reader.py
import json
from pathlib import Path

def load_json(file_path: Path) -> dict:
    """Đọc và parse file JSON theo đường dẫn chỉ định."""
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)