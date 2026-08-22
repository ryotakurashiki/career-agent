import json
import os
from dataclasses import asdict
from openai import OpenAI
from config import DEFAULT_MODEL, SYSTEM_PROMPT, TOOLS
from jobs.registry import JobRegistry
from jobs.providers.dummy import DummyProvider
from jobs.pipeline import JobPipeline
from jobs.feedback import FeedbackManager


class CareerAgent:
    def __init__(self, profile: dict, preferences: dict):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = DEFAULT_MODEL
        self.profile = profile
        self.preferences = preferences

        # プロフィールと希望条件をシステムプロンプトに埋め込む
        profile_text = json.dumps(profile, ensure_ascii=False, indent=2)
        preferences_text = json.dumps(preferences, ensure_ascii=False, indent=2)
        self.system_prompt = (
            SYSTEM_PROMPT
            + f"\n\n## 求職者のプロフィール\n\n```json\n{profile_text}\n```"
            + f"\n\n## 希望条件\n\n```json\n{preferences_text}\n```"
        )

        # 会話履歴
        self.messages = []

        # Providerを登録。将来ここに実APIのProviderを追加する。
        registry = JobRegistry()
        registry.register(DummyProvider())

        # パイプライン初期化
        self.pipeline = JobPipeline(registry, self.client)
        self.feedback = FeedbackManager()

    def chat(self, user_input: str) -> tuple[str, object]:
        self.messages.append({"role": "user", "content": user_input})

        # LLMがtool_callsを返すかぎりループする。
        # 通常の返答が来たらループを抜けてユーザーに返す。
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": self.system_prompt}] + self.messages,
                tools=TOOLS,
            )

            message = response.choices[0].message

            # LLMがToolを呼びたい場合
            if response.choices[0].finish_reason == "tool_calls":
                # assistantのメッセージ（tool_calls情報を含む）を履歴に追加
                self.messages.append(message)

                # 各tool callを実行し、結果をtoolメッセージとして履歴に追加
                for tool_call in message.tool_calls:
                    result = self._execute_tool(tool_call)
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
                # ループを続け、tool結果を受け取ったLLMに再度返答させる

            # LLMが通常の返答をした場合
            else:
                reply = message.content
                self.messages.append({"role": "assistant", "content": reply})
                return reply, response.usage

    def _execute_tool(self, tool_call) -> str:
        name = tool_call.function.name

        if name == "search_jobs":
            return self._search_jobs()

        if name == "save_feedback":
            args = json.loads(tool_call.function.arguments)
            return self._save_feedback(**args)

        return json.dumps({"error": f"unknown tool: {name}"}, ensure_ascii=False)

    def _search_jobs(self) -> str:
        """パイプラインを実行して求人を検索し、JSON文字列で返す。"""
        feedback_summary = self.feedback.get_summary()
        jobs = self.pipeline.run(self.profile, self.preferences, feedback_summary)

        if not jobs:
            return json.dumps({"message": "条件に合う求人が見つかりませんでした。"}, ensure_ascii=False)

        return json.dumps([asdict(job) for job in jobs], ensure_ascii=False, indent=2)

    def _save_feedback(self, liked_job_ids=None, disliked_job_ids=None, comments=None) -> str:
        """フィードバックを保存する。次回の search_jobs 呼び出し時に自動で反映される。"""
        self.feedback.save(
            liked_job_ids=liked_job_ids or [],
            disliked_job_ids=disliked_job_ids or [],
            comments=comments or [],
        )
        return json.dumps({"message": "フィードバックを保存しました。次回の求人検索に反映されます。"}, ensure_ascii=False)
