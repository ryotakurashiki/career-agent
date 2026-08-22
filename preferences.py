import json
import os
from openai import OpenAI
from config import DEFAULT_MODEL, PREFERENCES_EXTRACTION_PROMPT, PREFERENCES_PATH, PREFERENCES_QUESTIONS


def collect_preferences() -> dict:
    """
    希望条件をヒアリングして preferences.json に保存する。
    質問は固定テキスト（LLM不要）、回答の構造化のみLLMを使う。
    """
    print(f"\nAgent: {PREFERENCES_QUESTIONS}")
    user_response = input("あなた: ").strip()

    if not user_response:
        print("入力がなかったため、希望条件の設定をスキップします。")
        return {}

    print("\n希望条件を整理しています...")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": PREFERENCES_EXTRACTION_PROMPT},
            {"role": "user", "content": user_response},
        ],
        response_format={"type": "json_object"},
    )

    preferences = json.loads(response.choices[0].message.content)
    _save(preferences)
    print(f"希望条件を {PREFERENCES_PATH} に保存しました。")
    return preferences


def load_preferences() -> dict | None:
    """
    preferences.json が存在すれば読み込んで返す。なければ None を返す。
    """
    if not os.path.exists(PREFERENCES_PATH):
        return None
    with open(PREFERENCES_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save(preferences: dict):
    os.makedirs(os.path.dirname(PREFERENCES_PATH), exist_ok=True)
    with open(PREFERENCES_PATH, "w", encoding="utf-8") as f:
        json.dump(preferences, f, ensure_ascii=False, indent=2)
