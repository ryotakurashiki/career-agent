# Career Agent

自分専用のCLI型AI転職エージェント。

プロフィール・希望条件をもとに求人をWeb検索し、AIが評価・提案する。
フィードバックを伝えると次回の検索に反映される。

## セットアップ

```bash
git clone <repo>
cd career-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.env` を作成してAPIキーを設定する。

```
OPENAI_API_KEY=sk-...
```

## 使い方

### 1. 職務経歴書・履歴書を置く

`profile/docs/` にPDFを入れる。

```
profile/docs/
  職務経歴書.pdf
  履歴書.pdf
```

### 2. 起動する

```bash
python main.py
```

初回起動時に以下が自動で実行される。

- `profile/docs/` のPDFを読み込んでプロフィールを抽出 → `profile/profile.json` に保存
- 希望条件（職種・勤務地・年収など）をヒアリング → `profile/preferences.json` に保存

2回目以降は保存済みのデータを読み込む。希望条件を更新したい場合は起動時に `y` を入力する。

### 3. 会話する

```
Career Agent へようこそ。
転職に関して何でも聞いてください。
--------------------------------------------------

あなた: 求人を探してください
```

エージェントが自動で求人をWeb検索し、Top5を提案する。

### 4. フィードバックを伝える

```
あなた: 〇〇必須の求人は避けたい。提案の中では〇〇社は良さそう。
```

フィードバックは `profile/feedback.json` に保存され、次回の検索から反映される。

- 「避けたい条件」は **Web検索の時点** から除外される
- 「気に入った/気に入らない」はランキングスコアに反映される

### 5. 終了する

```
あなた: exit
```

## ファイル構成

```
main.py              # エントリポイント
agent.py             # キャリアエージェント本体（会話・Tool Calling）
config.py            # モデル・パス・プロンプト設定

jobs/
  models.py          # 共通 Job データモデル
  registry.py        # Provider の管理・横断検索
  filter.py          # Python による Hard Filter（勤務地・雇用形態）
  ranker.py          # LLM による一次評価・詳細評価
  pipeline.py        # 検索パイプライン全体の制御
  feedback.py        # フィードバックの保存・読み込み
  providers/
    base.py          # Provider の基底クラス
    dummy.py         # ダミーデータ（動作確認用）
    web_search.py    # OpenAI Responses API による Web 検索

skills/
  loader.py          # SKILL.md を読み込むユーティリティ
  job-evaluation/
    SKILL.md         # 求人評価の知識・評価観点・スコアの考え方

profile/
  docs/              # 職務経歴書・履歴書（PDF）を置く場所
  profile.json       # 抽出済みプロフィール（自動生成）
  preferences.json   # 希望条件（自動生成）
  feedback.json      # フィードバック履歴（自動生成）
```

## 求人検索パイプライン

```
① Web検索    : 希望条件＋フィードバックをもとに最大50件取得
② Hard Filter: 勤務地・雇用形態でNGを除外（Python）
③ 一次評価   : 安いLLMでスコアリング → 上位15件に絞る
④ 詳細評価   : 強いLLMで精密にランキング → Top5を返す
```
