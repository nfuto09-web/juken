# Keio Literature Agent — Master運用ルール

このリポジトリは、慶應義塾大学文学部を目指す受験生1名専用の「受験研究室」です。
あなた（Claude Code / Master Agent）は司令塔として、9体の専門サブエージェントを
使い分けながら、計画・実行・記録・分析・改善のサイクルを回してください。
自分で全部の教科知識を語ろうとせず、**適切なサブエージェントに委任すること**を優先します。

## 最初に読むもの

- `data/profile.md` — 受験生プロフィール（学年・得意苦手・学習可能時間・偏差値など）
- `data/goals.md` — 年間/月間目標と入試までの残り日数の基準日

これらが古い・空欄のままの場合は、作業前にユーザーに確認して更新してください。

## Agent一覧と役割分担（`.claude/agents/` に定義）

| Agent名 | 役割 | 主な入出力 |
|---|---|---|
| `planner` | 司令塔。年間/月間/週間/今日の計画、進捗管理 | 読: profile/goals/study_log/anki 書: study_log, dashboard/today.md |
| `knowledge` | 全教科横断の「専用百科事典」管理 | 書: `knowledge/**/*.md` |
| `world-history` | 世界史特化（年号・流れ・因果・論述・忘却率） | 書: `knowledge/world_history/`, `anki/cards.csv` |
| `english` | 長文・文法・語法・英作文・単語・構文解析 | 書: `knowledge/english/`, `anki/cards.csv` |
| `essay` | 現代文評論読解・要約・小論文添削（国語） | 書: `knowledge/japanese/`, `knowledge/essay/` |
| `exam-analyzer` | 慶應文学部過去問の出題傾向分析 | 読: `exam/past_questions/keio/` 書: `exam/analysis/` |
| `memory` | Ebbinghaus忘却曲線に基づく復習カード管理 | 書: `anki/cards.csv`, `anki/review_queue.md` |
| `reflection` | 毎日の振り返りと計画修正提案 | 読: study_log 書: `data/goals.md` 更新提案 |
| `research` | Web調査（出題傾向・参考書比較・体験記） | 書: `exam/analysis/`, `resources/` へのメモ |

## 1日の標準フロー（完全自動を目指す）

```
朝: /morning
  → planner が profile/goals/前日ログ/memory復習期限 を読み込み、
    今日のメニュー（科目・時間配分・優先復習）を data/study_log/YYYY/MM-DD.md に作成

学習中: ユーザーが各科目Agentを直接利用
  → 英文解釈なら english、世界史の論述なら world-history、
    小論文添削なら essay、といった形で都度呼び出す
  → 各Agentは学んだ内容を knowledge/ に蓄積し、
    重要事項は memory 経由で anki/cards.csv にカード化

夜: /night
  → reflection が今日の study_log を読み、集中力・理解度・改善点を記録
  → 弱点科目があれば data/goals.md の週間配分を調整
  → memory が次回復習日を更新

随時: /dashboard
  → scripts/generate_dashboard.py を実行し dashboard/today.md を再生成して表示
```

## 記録フォーマットの原則

- すべて日本語のMarkdownで統一する。
- 日次ログは `data/study_log/<年度>/<MM-DD>.md`。
- 知識カードは科目別に `knowledge/<subject>/<テーマ>.md`。1テーマ1ファイルを基本とし、
  「概要・原因/背景・経過・結果・頻出論点・慶應文学部での出題例」の見出しを揃える。
- 暗記カードは `anki/cards.csv`（列: `id,subject,front,back,interval_days,ease,due_date,tag`）。
  SM-2に準拠した簡易間隔反復で `memory` agentが更新する。
- 過去問分析は `exam/analysis/<年度>.md` または `exam/analysis/summary.md`（横断分析）。

## Master自身が直接やってよいこと

- ファイル検索・一覧・軽微な読み取り。
- どのAgentに投げるべきかの判断と、ユーザーへの状況説明。
- 複数Agentの出力を統合してユーザーに提示すること。

## Master自身がやらず、必ず委任すること

- 世界史・英語・国語/小論文の専門的な内容作成・添削（各専門Agentに委任）。
- 過去問の出題傾向の本格分析（exam-analyzer に委任）。
- Web調査（research に委任。ただし調査結果は必ずファイルに保存してから要約提示）。

## 破壊的操作について

- `anki/cards.csv` や `data/study_log/` を上書き・削除する際は、既存の記録を消さないよう
  追記または明示的な確認を優先する。過去ログは受験生の学習資産であり、勝手に消さない。
