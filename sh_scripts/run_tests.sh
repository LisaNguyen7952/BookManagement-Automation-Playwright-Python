#!/bin/bash

MARK=${1:-smoke}
THREAD=${2:-3}

echo "🧪 Running tests with marker: $MARK"
pytest -m "$MARK" -n "$THREAD" --alluredir="reports/allure-results"

#How ro use - example
#./sh_scripts/run_tests.sh smoke
#./sh_scripts/run_tests.sh regression 5
