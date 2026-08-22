from jobs.models import Job
from jobs.providers.base import JobProvider


class JobRegistry:
    """
    複数のProviderを管理し、横断検索・重複除去を行う。

    Agentからは search() だけを呼ぶ。
    新しいProviderを追加するときは register() するだけでよく、Agent側は変更不要。
    """

    def __init__(self):
        self._providers: list[JobProvider] = []

    def register(self, provider: JobProvider):
        self._providers.append(provider)

    def search(self, query: str, location: str, employment_type: str, limit: int) -> list[Job]:
        results = []
        seen_ids: set[str] = set()

        for provider in self._providers:
            for job in provider.search(query, location, employment_type, limit):
                # 同じidの求人が複数Providerから来ても1件だけ使う
                if job.id not in seen_ids:
                    seen_ids.add(job.id)
                    results.append(job)

        return results[:limit]

    def fetch_all(self, limit: int = 200) -> list[Job]:
        """フィルタなしで全Providerから求人を取得する。パイプラインの最初のステップで使う。"""
        return self.search("", "", "any", limit)
