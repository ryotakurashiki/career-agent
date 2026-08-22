import json
import os
from datetime import datetime
from config import FEEDBACK_PATH


class FeedbackManager:
    """
    ユーザーの求人フィードバックを保存・管理する。

    save()  : フィードバックを feedback.json に追記する
    get_summary() : 過去のフィードバックをまとめてランカーに渡せる文字列にする
    """

    def __init__(self):
        self.path = FEEDBACK_PATH

    def save(self, liked_job_ids: list, disliked_job_ids: list, comments: list) -> None:
        data = self._load_raw()
        data["history"].append({
            "timestamp": datetime.now().isoformat(),
            "liked_job_ids": liked_job_ids,
            "disliked_job_ids": disliked_job_ids,
            "comments": comments,
        })
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_summary(self) -> str:
        """
        過去のフィードバック全体をテキストにまとめて返す。
        パイプラインのランカーがプロンプトに追加して使う。
        """
        data = self._load_raw()
        if not data["history"]:
            return ""

        lines = ["ユーザーの過去のフィードバック（次の評価に反映すること）:"]

        all_comments = [
            comment
            for entry in data["history"]
            for comment in entry.get("comments", [])
        ]
        for comment in all_comments:
            lines.append(f"  - {comment}")

        liked_ids = [
            job_id
            for entry in data["history"]
            for job_id in entry.get("liked_job_ids", [])
        ]
        if liked_ids:
            lines.append(f"過去に気に入った求人ID: {', '.join(liked_ids)}")

        disliked_ids = [
            job_id
            for entry in data["history"]
            for job_id in entry.get("disliked_job_ids", [])
        ]
        if disliked_ids:
            lines.append(f"過去に気に入らなかった求人ID: {', '.join(disliked_ids)}")

        return "\n".join(lines)

    def _load_raw(self) -> dict:
        if not os.path.exists(self.path):
            return {"history": []}
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)
