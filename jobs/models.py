from dataclasses import dataclass, field


@dataclass
class Job:
    id: str
    title: str
    company: str
    location: str
    employment_type: str  # "fulltime" or "contract"
    salary: str           # 表示用の文字列に統一（例: "〜1,200万円"）
    description: str
    url: str
    source: str           # どのProviderから来たか（例: "dummy", "jooble"）
    match_reason: str = field(default="")  # DeepRankerがマッチング理由を設定する
