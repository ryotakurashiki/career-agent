from jobs.providers.base import JobProvider
from jobs.models import Job


# 固定のダミー求人データ。
# 実際のProviderではここをAPIコールに置き換える。
_JOBS = [
    Job(
        id="dummy-001",
        title="プロダクトマネージャー / PdM",
        company="Tech Startup Vietnam",
        location="ホーチミン（フルリモート可）",
        employment_type="fulltime",
        salary="〜1,200万円",
        description="BtoB SaaSプロダクトのPMを担当。東南アジア市場への展開をリード。英語・日本語話者歓迎。",
        url="https://example.com/jobs/001",
        source="dummy",
    ),
    Job(
        id="dummy-002",
        title="経営企画マネージャー",
        company="Japan Global Ventures",
        location="フルリモート（海外在住可）",
        employment_type="fulltime",
        salary="900〜1,400万円",
        description="海外拠点の経営管理・KPI設計・戦略立案を担当。スタートアップ経験者歓迎。",
        url="https://example.com/jobs/002",
        source="dummy",
    ),
    Job(
        id="dummy-003",
        title="業務改善コンサルタント（改善職）",
        company="Ops Consulting Asia",
        location="ホーチミン",
        employment_type="contract",
        salary="月80〜120万円",
        description="クライアント企業の業務プロセス分析・改善提案・実行支援。PdM経験者優遇。",
        url="https://example.com/jobs/003",
        source="dummy",
    ),
    Job(
        id="dummy-004",
        title="プロダクトマネージャー（副業・業務委託）",
        company="Remote SaaS Inc.",
        location="フルリモート",
        employment_type="contract",
        salary="時給8,000〜12,000円",
        description="新機能のロードマップ策定からリリースまでを担当。週20時間〜相談可。",
        url="https://example.com/jobs/004",
        source="dummy",
    ),
    Job(
        id="dummy-005",
        title="事業開発・経営企画",
        company="Southeast Asia Holdings",
        location="ホーチミン",
        employment_type="fulltime",
        salary="〜1,000万円",
        description="ベトナム現地法人の事業戦略策定・新規事業立ち上げ。現地チームのマネジメントも担当。",
        url="https://example.com/jobs/005",
        source="dummy",
    ),
]


class DummyProvider(JobProvider):
    def search(self, query: str, location: str, employment_type: str, limit: int) -> list[Job]:
        results = _JOBS

        # queryでフィルタ（titleとdescriptionを対象に部分一致）
        if query:
            q = query.lower()
            results = [
                j for j in results
                if q in j.title.lower() or q in j.description.lower()
            ]

        # locationでフィルタ（部分一致）
        if location:
            results = [j for j in results if location in j.location]

        # employment_typeでフィルタ
        if employment_type and employment_type != "any":
            results = [j for j in results if j.employment_type == employment_type]

        return results[:limit]
