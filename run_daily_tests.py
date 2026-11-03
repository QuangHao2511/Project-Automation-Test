# run_daily_tests.py
import subprocess
import sys
import os

def run_daily_regression():
    print("=" * 60)
    print("🚀 BẮT ĐẦU CHU TRÌNH KIỂM THỬ HẰNG NGÀY (DAILY HEALTH CHECK)")
    print("=" * 60)

    # Bước 1: Khởi tạo Storage State (Phiên đăng nhập)
    print("\n[BƯỚC 1/2] Đang nạp session và lưu cookie đăng nhập...")
    auth_cmd = [sys.executable, "-m", "pytest", "tests/test_setup_auth.py", "-q"]
    auth_result = subprocess.run(auth_cmd)
    
    if auth_result.returncode != 0:
        print("❌ LỖI: Không thể khởi tạo phiên đăng nhập! Dừng quy trình kiểm thử.")
        sys.exit(1)

    # Bước 2: Chạy toàn bộ kịch bản nghiệp vụ (trừ file setup)
    print("\n[BƯỚC 2/2] Đang thực thi toàn bộ kịch bản kiểm thử nghiệp vụ...")
    test_cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--ignore=tests/test_setup_auth.py",
        "-v", "-s",
        "--alluredir=reports/allure-results",
        "--clean-alluredir"
    ]
    test_result = subprocess.run(test_cmd)

    print("\n" + "=" * 60)
    if test_result.returncode == 0:
        print("✅ TẤT CẢ KỊCH BẢN ĐÃ PASS! HỆ THỐNG HOẠT ĐỘNG ỔN ĐỊNH.")
    else:
        print("⚠️ CÓ KỊCH BẢN BỊ FAIL! Vui lòng kiểm tra báo cáo chi tiết.")
    print("=" * 60)

if __name__ == "__main__":
    run_daily_regression()