from jobs.providers.base import JobProvider
from jobs.models import Job


# 20件のダミー求人。関連度がバラバラになるよう設計している。
# 実際のProviderではAPIコールに置き換える。
_JOBS = [

    # ===== 職種・勤務地ともに希望に近い（High relevance）=====

    Job(id="dummy-001", title="プロダクトマネージャー / PdM",
        company="Tech Startup Vietnam", location="ホーチミン（フルリモート可）",
        employment_type="fulltime", salary="〜1,200万円",
        description="BtoB SaaSプロダクトのPMを担当。東南アジア市場への展開をリード。英語・日本語話者歓迎。",
        url="https://example.com/jobs/001", source="dummy"),

    Job(id="dummy-002", title="経営企画マネージャー",
        company="Japan Global Ventures", location="フルリモート（海外在住可）",
        employment_type="fulltime", salary="900〜1,400万円",
        description="海外拠点の経営管理・KPI設計・戦略立案を担当。スタートアップ経験者歓迎。",
        url="https://example.com/jobs/002", source="dummy"),

    Job(id="dummy-003", title="業務改善コンサルタント",
        company="Ops Consulting Asia", location="ホーチミン",
        employment_type="contract", salary="月80〜120万円",
        description="クライアント企業の業務プロセス分析・改善提案・実行支援。PdM経験者優遇。",
        url="https://example.com/jobs/003", source="dummy"),

    Job(id="dummy-004", title="プロダクトマネージャー（業務委託）",
        company="Remote SaaS Inc.", location="フルリモート",
        employment_type="contract", salary="時給8,000〜12,000円",
        description="新機能のロードマップ策定からリリースまでを担当。週20時間〜相談可。",
        url="https://example.com/jobs/004", source="dummy"),

    Job(id="dummy-005", title="事業開発・経営企画",
        company="Southeast Asia Holdings", location="ホーチミン",
        employment_type="fulltime", salary="〜1,000万円",
        description="ベトナム現地法人の事業戦略策定・新規事業立ち上げ。現地チームのマネジメントも担当。",
        url="https://example.com/jobs/005", source="dummy"),

    Job(id="dummy-006", title="シニアPdM / プロダクトリード",
        company="Global EdTech Co.", location="フルリモート（アジア時間帯）",
        employment_type="fulltime", salary="1,200〜1,600万円",
        description="教育系SaaSのプロダクトロードマップ主導。グローバルチームのプロダクトリード。",
        url="https://example.com/jobs/006", source="dummy"),

    Job(id="dummy-007", title="グロースPM / Growth PM",
        company="Vietnam FinTech", location="ホーチミン（一部リモート）",
        employment_type="fulltime", salary="〜1,100万円",
        description="ユーザー獲得・リテンション施策の企画・実行。データドリブンなプロダクト改善。",
        url="https://example.com/jobs/007", source="dummy"),

    Job(id="dummy-008", title="新規事業企画・事業開発",
        company="Asia Ventures", location="ホーチミン",
        employment_type="fulltime", salary="800〜1,200万円",
        description="新規事業の立ち上げから事業化まで一貫担当。現地パートナーとの折衝も含む。",
        url="https://example.com/jobs/008", source="dummy"),

    # ===== 勤務地は合うが職種が低関連（Low relevance）=====

    Job(id="dummy-009", title="スクラムマスター / アジャイルコーチ",
        company="Dev Agency Vietnam", location="フルリモート",
        employment_type="contract", salary="月60〜90万円",
        description="開発チームのスクラム導入・運営支援。プロセス改善のファシリテーション。",
        url="https://example.com/jobs/009", source="dummy"),

    Job(id="dummy-010", title="カスタマーサクセスマネージャー",
        company="SaaS Vietnam", location="ホーチミン",
        employment_type="fulltime", salary="600〜900万円",
        description="エンタープライズ顧客のオンボーディング・活用促進・チャーン防止を担当。",
        url="https://example.com/jobs/010", source="dummy"),

    Job(id="dummy-011", title="マーケティングマネージャー",
        company="Consumer Tech Asia", location="フルリモート",
        employment_type="fulltime", salary="700〜1,000万円",
        description="東南アジア向けデジタルマーケティング戦略の立案・実行。SEO/SEM/SNS運用。",
        url="https://example.com/jobs/011", source="dummy"),

    Job(id="dummy-012", title="データアナリスト",
        company="Analytics Vietnam", location="ホーチミン",
        employment_type="contract", salary="月50〜70万円",
        description="ユーザー行動データの分析・可視化・レポーティング。SQL/BIツール必須。",
        url="https://example.com/jobs/012", source="dummy"),

    Job(id="dummy-020", title="人事・採用マネージャー",
        company="HR Tech Vietnam", location="ホーチミン",
        employment_type="fulltime", salary="500〜700万円",
        description="エンジニア・ビジネス職の採用戦略立案・実行。現地と日本の採用を担当。",
        url="https://example.com/jobs/020", source="dummy"),

    # ===== 希望勤務地外（Hard Filterで除外される）=====

    Job(id="dummy-013", title="プロダクトマネージャー",
        company="Tokyo Tech Corp", location="東京（出社必須）",
        employment_type="fulltime", salary="〜1,000万円",
        description="自社サービスのPM。渋谷オフィス勤務。週5日出社。",
        url="https://example.com/jobs/013", source="dummy"),

    Job(id="dummy-014", title="経営企画・IR担当",
        company="大阪製造業", location="大阪",
        employment_type="fulltime", salary="700〜900万円",
        description="経営会議資料作成・IR対応・中期経営計画策定。製造業経験者優遇。",
        url="https://example.com/jobs/014", source="dummy"),

    Job(id="dummy-015", title="Senior Product Manager",
        company="Singapore Startup", location="シンガポール（出社必須）",
        employment_type="fulltime", salary="SGD 8,000〜12,000",
        description="Consumer app PM. Build and lead product strategy for SEA market.",
        url="https://example.com/jobs/015", source="dummy"),

    Job(id="dummy-016", title="事業企画マネージャー",
        company="名古屋メーカー", location="名古屋",
        employment_type="fulltime", salary="600〜800万円",
        description="新規事業企画・推進。製造業のDX推進プロジェクト。",
        url="https://example.com/jobs/016", source="dummy"),

    Job(id="dummy-017", title="PdM / プロダクトオーナー",
        company="Fukuoka SaaS", location="福岡（ハイブリッド）",
        employment_type="fulltime", salary="600〜900万円",
        description="週3出社・週2リモート。福岡オフィス中心のプロダクト開発。",
        url="https://example.com/jobs/017", source="dummy"),

    Job(id="dummy-018", title="コンサルタント（経営・IT）",
        company="Big4系ファーム", location="東京",
        employment_type="fulltime", salary="800〜1,500万円",
        description="大手クライアントの経営改革・DX支援。東京オフィス勤務ベース。",
        url="https://example.com/jobs/018", source="dummy"),

    Job(id="dummy-019", title="エンジニアリングマネージャー",
        company="Tokyo Internet Co.", location="東京（リモート週2可）",
        employment_type="fulltime", salary="〜1,200万円",
        description="バックエンドチームのマネジメント。技術戦略の立案・実行。東京本社勤務。",
        url="https://example.com/jobs/019", source="dummy"),
]


class DummyProvider(JobProvider):
    def search(self, query: str, location: str, employment_type: str, limit: int) -> list[Job]:
        results = _JOBS

        if query:
            q = query.lower()
            results = [
                j for j in results
                if q in j.title.lower() or q in j.description.lower()
            ]

        if location:
            results = [j for j in results if location in j.location]

        if employment_type and employment_type != "any":
            results = [j for j in results if j.employment_type == employment_type]

        return results[:limit]
