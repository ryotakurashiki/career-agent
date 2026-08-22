import json
import os
from openai import OpenAI
from config import DEFAULT_MODEL, EXTRACTION_PROMPT, PROFILE_PATH
from resume_loader import load_all_docs


def extract_profile() -> dict:
    """
    profile/docs/ 内のファイルを読み込み、LLMでプロフィールを抽出して
    profile/profile.json に保存する。
    """
    print("ドキュメントを読み込んでいます...")
    raw_text = load_all_docs()

    print("プロフィールを抽出しています...")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        # JSONのみを返すようにOpenAIに指示する
        response_format={"type": "json_object"},
    )

    profile = json.loads(response.choices[0].message.content)

    # profile/ ディレクトリがなければ作る
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)

    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(f"プロフィールを {PROFILE_PATH} に保存しました。")
    return profile
