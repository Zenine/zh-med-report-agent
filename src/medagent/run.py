"""CLI entry point: run the agent on a task from the dataset."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _load_dotenv() -> None:
    """Minimal .env loader — no extra dependency."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    _load_dotenv()

    parser = argparse.ArgumentParser(description="运行医疗 Agent 单例分析")
    parser.add_argument("--task", required=True, help="任务文件路径 (JSONL)")
    parser.add_argument("--case", type=int, default=0, help="任务编号 (0-indexed)")
    parser.add_argument("--model", default=None, help="LLM 模型名称（默认读 MEDAGENT_MODEL 环境变量）")
    parser.add_argument("--dry-run", action="store_true", help="只打印任务内容，不调用 LLM")
    args = parser.parse_args()

    task_path = Path(args.task)
    if not task_path.exists():
        print(f"错误：任务文件不存在 {task_path}", file=sys.stderr)
        sys.exit(1)

    tasks = [json.loads(line) for line in task_path.read_text().splitlines() if line.strip()]
    if args.case >= len(tasks):
        print(f"错误：任务编号 {args.case} 超出范围（共 {len(tasks)} 条）", file=sys.stderr)
        sys.exit(1)

    task = tasks[args.case]
    print(f"=== 任务 #{args.case}: {task.get('title', 'untitled')} ===")
    print(f"风险标签: {task.get('risk_labels', [])}")
    print(f"---输入---")
    print(task["input"])
    print()

    if args.dry_run:
        print("(dry-run 模式，跳过 LLM 调用)")
        print(f"---期望行为---")
        for b in task.get("expected_behaviors", []):
            print(f"  - {b}")
        return

    from medagent.agent import run_case

    if args.model:
        os.environ["MEDAGENT_MODEL"] = args.model

    result = run_case(task["input"])
    print("---Agent 输出---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
