# Career Agent Project

## Goal

自分専用のCLI型AI転職エージェントを作る。

最終的には `$ career` から自然言語で転職活動を進められるようにする。

## Learning goals

このプロジェクトは完成品を最速で作ることだけが目的ではない。

以下を実装しながら理解することを重視する。

1. LLM API
2. Conversation
3. Tool Calling
4. Memory
5. Skills
6. MCP
7. Agent architecture

## Development principles

- 一度に複数の新しい概念を導入しない
- 必要になるまで複雑なframeworkを使わない
- 実装前に「なぜ必要か」を説明する
- 初心者がコードを理解できるシンプルさを優先する
- 可能な処理は通常のPythonで行い、LLMが必要な部分だけLLMを使う
- 各ステップで動作確認してから次へ進む

## Current phase

Career Agent v0

現在の目的:

User
→ CLI
→ LLM API
→ Response

まだ実装しないもの:

- Job Search
- Tool Calling
- Memory
- Skills
- MCP
- Database
- Web UI
- Multi-agent

## Product vision

将来的には以下を実現する。

- 履歴書・職務経歴書からプロフィールを理解
- 希望条件に合う求人を探す
- 求人を評価・ランキング
- ユーザーのフィードバックから好みを学習
- 企業調査
- 応募書類作成
- 面接準備
- 応募状況管理
- 必要に応じてGmailやCalendarなどを操作
