# Keio Literature Agent — 慶應義塾大学文学部 受験研究室

「質問に答えるAI」ではなく、**2年間の学習を管理する受験研究室**として設計された
Claude Code プロジェクトです。9体の専門Agentが Planner を司令塔として連携し、
計画・実行・記録・分析・改善のサイクルを継続的に回します。

## 使い方（毎日の流れ）

| タイミング | コマンド | やること |
|---|---|---|
| 朝 | `/morning` | 今日の学習メニューを生成（前日の理解度・復習期限を反映） |
| 学習中 | 各科目Agentを直接呼び出し | 例:「japanese-history agentで明治維新を解説して」 |
| 学習後 | `data/study_log/` に記録 | Planner/Reflectionが読み取り理解度を更新 |
| 夜 | `/night` | 今日の反省会 → 明日以降の計画を自動修正 |
| いつでも | `/dashboard` | 進捗ダッシュボードを表示 |

## ディレクトリ構成

```
juken/
├── CLAUDE.md                # Master Agent（司令塔）の運用ルール
├── .claude/
│   ├── agents/               # 9体の専門サブエージェント定義
│   └── commands/              # /morning /night /dashboard などのスラッシュコマンド
├── data/
│   ├── profile.md             # 受験生プロフィール
│   ├── goals.md                # 年間・月間目標
│   └── study_log/              # 日次学習ログ（年度別）
├── knowledge/                 # 教科別「専用百科事典」（Markdown知識DB）
│   ├── english/
│   ├── japanese_history/
│   ├── japanese/
│   └── essay/
├── anki/                       # 忘却曲線に基づく復習カード（Memory Agent管理）
├── exam/
│   ├── past_questions/keio/    # 過去問本文・設問メモ
│   └── analysis/                # 出題傾向分析（Exam Analyzer出力）
├── resources/                  # 参考書・PDF等の教材管理
├── scripts/                    # ダッシュボード生成などの補助スクリプト
└── dashboard/                  # 生成済みダッシュボード（today.md）
```

## Agent一覧

1. **Planner** — 年間/月間/週間/今日の計画、進捗管理（司令塔）
2. **Knowledge** — 全教科の知識をMarkdown化する専用百科事典管理者
3. **Japanese History** — 日本史特化（年号・流れ・因果・論述・忘却率管理）
4. **English** — 長文・文法・語法・英作文・単語・構文解析
5. **Essay（国語/小論文）** — 評論読解・要約・小論文添削
6. **Exam Analyzer** — 慶應文学部過去問の出題傾向分析
7. **Memory** — Ebbinghaus忘却曲線に基づく復習カード管理（Anki的役割）
8. **Reflection** — 毎日の振り返りと計画修正
9. **Research** — Web調査（出題傾向・参考書比較・合格者体験記など）

詳細な運用ルールは `CLAUDE.md` を参照してください。まずは `data/profile.md` を
確認・更新してから `/morning` を実行してください。
