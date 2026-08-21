import os
from openai import OpenAI
from config import DEFAULT_MODEL, SYSTEM_PROMPT


class CareerAgent:
    def __init__(self):
        # APIキーは環境変数から読む（.envからpython-dotenvが展開済み）
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = DEFAULT_MODEL

        # 会話履歴。ここにuserとassistantのやり取りを蓄積していく。
        # LLM自体は前の会話を覚えていないので、毎回この全履歴を送る。
        self.messages = []

    def chat(self, user_input: str) -> tuple[str, object]:
        # 1. ユーザーの発言を履歴に追加
        self.messages.append({"role": "user", "content": user_input})

        # 2. APIを呼ぶ
        #    systemはmessagesリストの最初に "role": "system" として渡す
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + self.messages,
        )

        # 3. LLMの返答を取り出す
        reply = response.choices[0].message.content

        # 4. LLMの返答も履歴に追加（次の会話で文脈として使う）
        self.messages.append({"role": "assistant", "content": reply})

        return reply, response.usage
