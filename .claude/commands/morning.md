---
description: 今日の学習メニューを生成する朝のルーチン
---

朝のルーチンを実行してください。

1. `planner` agentを起動し、`data/profile.md` / `data/goals.md` / 直近の
   `data/study_log/` を読み込ませ、今日の学習メニューを
   `data/study_log/<年度>/<MM-DD>.md` に作成させる。
2. `memory` agentを起動し、`anki/cards.csv` から本日期限の復習カードを抽出させ、
   `anki/review_queue.md` を更新させる。件数を1で作成した計画に反映する。
3. `scripts/generate_dashboard.py` を実行して `dashboard/today.md` を再生成する。
4. 最終的に、今日のメニューと復習件数、ダッシュボードの要点をユーザーに簡潔に提示する。
