#!/bin/bash

RESULT_DIR="reports/allure-results"
DATE=$(date +%F)
TIME=$(date +%H%M%S)
REPORT_DEST="reports/$DATE/run-$TIME"

mkdir -p "$REPORT_DEST"

if [ "$(ls -A "$RESULT_DIR")" ]; then
    allure generate "$RESULT_DIR" -o "$REPORT_DEST/allure-report" --clean
    echo "✅ Report generated at $REPORT_DEST/allure-report/index.html"
else
    echo "❌ No Allure results found."
fi
#How to use, run this query after run test
#./sh_scripts/generate_report.sh