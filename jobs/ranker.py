import json
from dataclasses import asdict
from openai import OpenAI
from jobs.models import Job
from config import FAST_RANK_PROMPT, DEEP_RANK_PROMPT
from skills.loader import load_skill

_JOB_EVALUATION_SKILL = load_skill("job-evaluation")


class FastRanker:
    """
    ④ 安いLLMで一次評価

    全件を1回のAPIコールでスコアリングする。
    タイトルと概要だけを送ってトークンを節約し、上位N件を残す。
    """

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    def rank(self, jobs: list[Job], profile: dict, preferences: dict, top_n: int, feedback_summary: str = "") -> list[Job]:
        if not jobs:
            return jobs

        # タイトルと概要だけ送る（トークン節約）
        jobs_text = json.dumps(
            [{"id": j.id, "title": j.title, "description": j.description} for j in jobs],
            ensure_ascii=False,
        )
        user_content = (
            f"プロフィール:\n{json.dumps(profile, ensure_ascii=False)}\n\n"
            f"希望条件:\n{json.dumps(preferences, ensure_ascii=False)}\n\n"
            + (f"{feedback_summary}\n\n" if feedback_summary else "")
            + f"求人リスト:\n{jobs_text}"
        )

        system_prompt = _JOB_EVALUATION_SKILL + "\n\n" + FAST_RANK_PROMPT

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
        )

        scores_data = json.loads(response.choices[0].message.content)
        score_map = {s["id"]: s["score"] for s in scores_data.get("scores", [])}

        # スコアの高い順にソートして上位N件を返す
        ranked = sorted(jobs, key=lambda j: score_map.get(j.id, 0), reverse=True)
        return ranked[:top_n]


class DeepRanker:
    """
    ⑤ 強いLLMで詳細評価

    FastRankerで残った件数を全フィールド込みで詳細に評価する。
    マッチング理由（match_reason）も生成してJobに付与する。
    """

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    def rank(self, jobs: list[Job], profile: dict, preferences: dict, top_n: int, feedback_summary: str = "") -> list[Job]:
        if not jobs:
            return jobs

        # 全フィールドを送る（match_reasonは除く）
        jobs_data = [
            {k: v for k, v in asdict(j).items() if k != "match_reason"}
            for j in jobs
        ]
        user_content = (
            f"プロフィール:\n{json.dumps(profile, ensure_ascii=False)}\n\n"
            f"希望条件:\n{json.dumps(preferences, ensure_ascii=False)}\n\n"
            + (f"{feedback_summary}\n\n" if feedback_summary else "")
            + f"求人リスト:\n{json.dumps(jobs_data, ensure_ascii=False)}"
        )

        system_prompt = _JOB_EVALUATION_SKILL + "\n\n" + DEEP_RANK_PROMPT

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
        )

        ranking_data = json.loads(response.choices[0].message.content)
        ranking = ranking_data.get("ranking", [])

        # idをキーにしてscore・reasonを取り出せるようにする
        rank_map = {r["id"]: r for r in ranking}

        # スコアの高い順にソートしてmatch_reasonを付与する
        ranked = sorted(
            jobs,
            key=lambda j: rank_map.get(j.id, {}).get("score", 0),
            reverse=True,
        )
        for job in ranked:
            job.match_reason = rank_map.get(job.id, {}).get("reason", "")

        return ranked[:top_n]
