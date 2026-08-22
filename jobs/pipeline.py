from openai import OpenAI
from jobs.models import Job
from jobs.registry import JobRegistry
from jobs.filter import HardFilter
from jobs.ranker import FastRanker, DeepRanker
from config import FETCH_LIMIT, FAST_RANK_TOP_N, DEEP_RANK_TOP_N, FAST_RANKER_MODEL, DEEP_RANKER_MODEL


class JobPipeline:
    """
    求人検索パイプライン。

    ② 取得      : 全Providerから多めに取得
    ③ フィルタ  : Pythonのハードルールで除外
    ④ 一次評価  : 安いLLMでスコアリング
    ⑤ 詳細評価  : 強いLLMで精密にランキング
    """

    def __init__(self, registry: JobRegistry, client: OpenAI):
        self.registry = registry
        self.hard_filter = HardFilter()
        self.fast_ranker = FastRanker(client, FAST_RANKER_MODEL)
        self.deep_ranker = DeepRanker(client, DEEP_RANKER_MODEL)

    def run(self, profile: dict, preferences: dict, feedback_summary: str = "") -> list[Job]:
        # ② 取得
        jobs = self.registry.fetch_all(limit=FETCH_LIMIT)
        print(f"[pipeline] 取得: {len(jobs)}件")

        # ③ Python Hard Filter
        jobs = self.hard_filter.run(jobs, preferences)
        print(f"[pipeline] フィルタ後: {len(jobs)}件")

        if not jobs:
            return []

        # ④ 安いLLMで一次評価（フィードバック反映）
        jobs = self.fast_ranker.rank(jobs, profile, preferences, top_n=FAST_RANK_TOP_N, feedback_summary=feedback_summary)
        print(f"[pipeline] 一次評価後: {len(jobs)}件")

        # ⑤ 強いLLMで詳細評価（フィードバック反映）
        jobs = self.deep_ranker.rank(jobs, profile, preferences, top_n=DEEP_RANK_TOP_N, feedback_summary=feedback_summary)
        print(f"[pipeline] 詳細評価後: {len(jobs)}件")

        return jobs
