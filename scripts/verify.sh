#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0

echo "=== verify.sh ==="

# 1. Python 语法检查
echo "[1/4] Python 语法检查..."
find src -name '*.py' -print0 | xargs -0 python3 -m py_compile 2>&1 || FAIL=1

# 2. 核心文件存在性
echo "[2/4] 核心文件检查..."
for f in README.md pyproject.toml datasets/lab_report_tasks.jsonl rubrics/lab_report_rubrics.yaml src/medagent/__init__.py; do
    if [ ! -f "$f" ]; then
        echo "  缺失: $f"
        FAIL=1
    fi
done

# 3. 数据集完整性：至少 10 条任务
echo "[3/4] 数据集完整性..."
TASK_COUNT=$(wc -l < datasets/lab_report_tasks.jsonl | tr -d ' ')
if [ "$TASK_COUNT" -lt 10 ]; then
    echo "  任务数不足: $TASK_COUNT < 10"
    FAIL=1
else
    echo "  任务数: $TASK_COUNT"
fi

# 4. pytest（如果有测试）
if [ -d tests ] && find tests -name 'test_*.py' | grep -q .; then
    echo "[4/4] 运行测试..."
    python3 -m pytest tests -q || FAIL=1
else
    echo "[4/4] 跳过测试（tests/ 目录为空或不存在）"
fi

if [ "$FAIL" -ne 0 ]; then
    echo "=== FAIL ==="
    exit 1
fi
echo "=== PASS ==="
