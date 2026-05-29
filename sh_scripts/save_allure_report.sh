#!/usr/bin/env bash
set -e

RESULT_DIR_RAW="reports/allure-results"
DATE=$(date +%F)
TIME=$(date +%H%M%S)
REPORT_DEST="reports/$DATE/run-$TIME"

echo "🚀 Bắt đầu quy trình Test & Report..."

mkdir -p "$RESULT_DIR_RAW"
mkdir -p "$REPORT_DEST"

rm -rf "$RESULT_DIR_RAW"/* 2>/dev/null || true
echo "🧹 Đã dọn dẹp thư mục kết quả cũ."

MARKER=${1:-smoke}

echo "🧪 Đang chạy automation test với marker: $MARKER ..."
pytest -m "$MARKER" -n 3 --alluredir="$RESULT_DIR_RAW" || true

if [ -d "$RESULT_DIR_RAW" ] && [ "$(find "$RESULT_DIR_RAW" -type f | wc -l)" -gt 0 ]; then
    echo "📊 Đang khởi tạo Allure Report..."
    allure generate "$RESULT_DIR_RAW" -o "$REPORT_DEST/allure-report" --clean

    echo "---"
    echo "✅ Hoàn thành!"
    echo "🔗 Report: $REPORT_DEST/allure-report/index.html"

    # Auto open (Mac)
    open "$REPORT_DEST/allure-report/index.html" 2>/dev/null || true
else
    echo "❌ Lỗi: Không có dữ liệu Allure được sinh ra."
    exit 1
fi

# Including run test by marker - default is smoke and generate report
#5. How to run file
#./sh_scripts/save_allure_report.sh