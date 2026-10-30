# Playwright Python Test Automation Framework

Framework kiểm thử tự động toàn diện xây dựng trên nền tảng **Playwright (Python)** kết hợp **PyTest**, áp dụng mô hình **Page Object Model (POM)**.

## 🛠️ Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.11+
- **Thư viện kiểm thử:** Playwright, PyTest
- **Báo cáo:** Allure Report
- **Mô hình kiến trúc:** Page Object Model (POM)
- **CI/CD:** GitHub Actions

## 📁 Cấu trúc thư mục
- `pages/`: Chứa các Page Object quản lý locator và thao tác giao diện.
- `tests/`: Kịch bản kiểm thử, fixtures (`conftest.py`) và hooks.
- `data/`: Dữ liệu kiểm thử phục vụ Data-Driven Testing (`test_data.json`).
- `config/`: Cấu hình đường dẫn động (`settings.py`) và biến môi trường.
- `utils/`: Các hàm tiện ích bổ trợ (đọc file, format, logger).

## 🚀 Hướng dẫn cài đặt & Thực thi

1. **Cài đặt thư viện phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
