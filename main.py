import json
import os
from dotenv import load_dotenv
from agent import CareerAgent
from extractor import extract_profile
from preferences import collect_preferences, load_preferences
from config import PROFILE_PATH

# .envファイルからAPIキーを環境変数に読み込む
load_dotenv()


def load_profile() -> dict:
    """
    profile.json が存在すればそれを返す。
    なければ抽出を実行して保存・返す。
    """
    if os.path.exists(PROFILE_PATH):
        print(f"プロフィールを読み込みました: {PROFILE_PATH}")
        with open(PROFILE_PATH, encoding="utf-8") as f:
            return json.load(f)
    else:
        print("プロフィールが見つかりません。ドキュメントから抽出します。")
        return extract_profile()


def setup_preferences() -> dict:
    """
    preferences.json が存在すれば読み込む。
    なければヒアリングを実行して保存・返す。
    既存の場合は更新するか確認する。
    """
    existing = load_preferences()
    if existing:
        answer = input("\n前回の希望条件が見つかりました。更新しますか？ (y/N): ").strip().lower()
        if answer == "y":
            return collect_preferences()
        return existing
    else:
        print("\n希望条件をヒアリングします。")
        return collect_preferences()


def main():
    profile = load_profile()
    preferences = setup_preferences()
    agent = CareerAgent(profile, preferences)

    print("\nCareer Agent へようこそ。")
    print("転職に関して何でも聞いてください。")
    print("終了するには 'exit' または 'quit' と入力してください。")
    print("-" * 50)

    while True:
        user_input = input("\nあなた: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("終了します。")
            break

        if not user_input:
            continue

        reply, usage = agent.chat(user_input)

        print(f"\nAgent: {reply}")
        print(f"\n[tokens] input: {usage.prompt_tokens}, output: {usage.completion_tokens}, total: {usage.total_tokens}")


if __name__ == "__main__":
    main()
