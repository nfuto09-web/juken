#!/usr/bin/env python3
"""dashboard/today.md を data/goals.md, data/study_log/, anki/cards.csv から生成する。

使い方: python3 scripts/generate_dashboard.py
"""
import csv
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOALS = ROOT / "data" / "goals.md"
STUDY_LOG = ROOT / "data" / "study_log"
CARDS = ROOT / "anki" / "cards.csv"
DASHBOARD = ROOT / "dashboard" / "today.md"

BAR_WIDTH = 10


def bar(ratio: float) -> str:
    ratio = max(0.0, min(1.0, ratio))
    filled = round(ratio * BAR_WIDTH)
    return "█" * filled + "░" * (BAR_WIDTH - filled) + f" {round(ratio * 100)}%"


def find_base_date() -> date | None:
    if not GOALS.exists():
        return None
    text = GOALS.read_text(encoding="utf-8")
    m = re.search(r"仮基準日:\s*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y-%m-%d").date()


def find_today_log() -> Path | None:
    today = date.today()
    candidate = STUDY_LOG / str(today.year) / f"{today.month:02d}-{today.day:02d}.md"
    return candidate if candidate.exists() else None


SUBJECT_LINE = re.compile(r"^-\s*([^:：]+)[:：]\s*(\d+)\s*分")


def parse_minutes(section_text: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in section_text.splitlines():
        m = SUBJECT_LINE.match(line.strip())
        if m:
            subject = m.group(1).strip()
            result[subject] = result.get(subject, 0) + int(m.group(2))
    return result


def extract_section(text: str, heading_prefix: str) -> str:
    lines = text.splitlines()
    out = []
    capturing = False
    for line in lines:
        if line.strip().startswith("## "):
            capturing = line.strip().startswith(heading_prefix)
            continue
        if capturing:
            out.append(line)
    return "\n".join(out)


def subject_progress() -> dict[str, tuple[int, int]]:
    """科目名 -> (実施分, 予定分)"""
    log_path = find_today_log()
    if not log_path:
        return {}
    text = log_path.read_text(encoding="utf-8")
    planned = parse_minutes(extract_section(text, "今日のメニュー"))
    actual = parse_minutes(extract_section(text, "実施記録"))
    subjects = {}
    for subject, mins in planned.items():
        subjects[subject] = (actual.get(subject, 0), mins)
    return subjects


def review_count() -> int:
    if not CARDS.exists():
        return 0
    today = date.today()
    count = 0
    with CARDS.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            due = row.get("due_date", "").strip()
            if not due:
                continue
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
            except ValueError:
                continue
            if due_date <= today:
                count += 1
    return count


def total_study_hours() -> float:
    subjects = subject_progress()
    total_minutes = sum(actual for actual, _ in subjects.values())
    return round(total_minutes / 60, 1)


def days_remaining() -> int | None:
    base = find_base_date()
    if base is None:
        return None
    return (base - date.today()).days


def render() -> str:
    today = date.today()
    subjects = subject_progress()
    reviews = review_count()
    hours = total_study_hours()
    remaining = days_remaining()

    lines = []
    lines.append(f"# {today.isoformat()} ダッシュボード")
    lines.append("")
    lines.append("```")
    lines.append("=====================")
    lines.append("")
    if subjects:
        for subject, (actual, planned) in subjects.items():
            ratio = (actual / planned) if planned else 0
            lines.append(f"{subject}")
            lines.append(bar(ratio))
            lines.append("")
    else:
        lines.append("(今日の学習計画が未作成です。/morning を実行してください)")
        lines.append("")
    lines.append("復習")
    lines.append(f"{reviews}件")
    lines.append("")
    if remaining is not None:
        lines.append("残り")
        lines.append(f"{remaining}日")
        lines.append("")
    lines.append("今日の勉強時間")
    lines.append(f"{hours}h")
    lines.append("")
    lines.append("=====================")
    lines.append("```")
    return "\n".join(lines) + "\n"


def main() -> None:
    DASHBOARD.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD.write_text(render(), encoding="utf-8")
    print(f"generated: {DASHBOARD}")


if __name__ == "__main__":
    main()
