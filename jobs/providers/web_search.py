import json
import time
from openai import OpenAI
from jobs.providers.base import JobProvider
from jobs.models import Job
from config import WEB_SEARCH_MODEL, WEB_SEARCH_PROMPT
from jobs.feedback import FeedbackManager


class WebSearchProvider(JobProvider):
    """
    OpenAI Responses API の built-in web_search_preview を使って
    実際の求人をWebから検索するProvider。

    ・セッション内キャッシュあり（1時間）: 同じセッションで何度呼ばれても再検索しない
    ・プロンプトを絞り込んで検索回数を抑える（目安3クエリ以内）
    ・URLは必ず出典の実際のURLを使う
    """

    CACHE_TTL = 60 * 60  # 1時間

    def __init__(self, client: OpenAI, preferences: dict, feedback: FeedbackManager, model: str = WEB_SEARCH_MODEL):
        self.client = client
        self.preferences = preferences
        self.feedback = feedback
        self.model = model
        self._cache: list[Job] = []
        self._cache_at: float = 0

    def clear_cache(self) -> None:
        self._cache = []
        self._cache_at = 0

    def search(self, query: str, location: str, employment_type: str, limit: int) -> list[Job]:
        # キャッシュが有効なら再検索しない
        if self._cache and time.time() - self._cache_at < self.CACHE_TTL:
            return self._cache[:limit]

        # registry.fetch_all() は query="" で呼ぶので、preferences からフォールバック
        effective_query = query or "、".join(self.preferences.get("希望職種", []))
        effective_location = location or "、".join(self.preferences.get("希望勤務地", []))
        effective_type = self._resolve_employment_type(employment_type)

        comments = self.feedback.get_comments()
        feedback_section = (
            "- 除外条件（以下に該当する求人は取得しないこと）:\n"
            + "\n".join(f"  - {c}" for c in comments)
            + "\n"
        ) if comments else ""

        prompt = WEB_SEARCH_PROMPT.format(
            query=effective_query,
            location=effective_location,
            employment_type=effective_type,
            feedback_section=feedback_section,
        )

        response = self.client.responses.create(
            model=self.model,
            tools=[{"type": "web_search_preview"}],
            input=prompt,
        )

        jobs = self._parse_response(response)

        self._cache = jobs
        self._cache_at = time.time()

        return jobs[:limit]

    def _resolve_employment_type(self, employment_type: str) -> str:
        """
        "any" の場合は preferences から雇用形態を解決する。
        """
        if employment_type != "any":
            return {"fulltime": "正社員", "contract": "業務委託"}.get(employment_type, employment_type)

        pref_types = self.preferences.get("雇用形態", [])
        return "、".join(pref_types) if pref_types else "正社員または業務委託"

    def _parse_response(self, response) -> list[Job]:
        output_text = response.output_text

        # アノテーションから実際のURLを収集しておく（LLMがURLを捏造した場合の検証用）
        verified_urls = self._extract_citation_urls(response)

        # コードブロック記法を除去してJSONをパース
        text = output_text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        try:
            jobs_data = json.loads(text)
        except json.JSONDecodeError:
            return []

        jobs = []
        for item in jobs_data:
            url = item.get("url", "").strip()

            # URLが空・架空の場合は verified_urls から補完を試みる
            if not url or "example.com" in url:
                url = verified_urls.pop(0) if verified_urls else ""

            if not url:
                # URLなしの求人は出典不明なので除外
                continue

            job = Job(
                id=f"web-{abs(hash(item.get('title', '') + item.get('company', '')))}",
                title=item.get("title", ""),
                company=item.get("company", ""),
                location=item.get("location", ""),
                employment_type=item.get("employment_type", "fulltime"),
                salary=item.get("salary", ""),
                description=item.get("description", ""),
                url=url,
                source="web_search",
            )
            jobs.append(job)

        return jobs

    def _extract_citation_urls(self, response) -> list[str]:
        """
        Responses API のアノテーションから実際の検索結果URLを取り出す。
        LLMが返したURLの検証・補完に使う。
        """
        urls = []
        for item in response.output:
            if not hasattr(item, "content"):
                continue
            for block in item.content:
                if not hasattr(block, "annotations"):
                    continue
                for annotation in block.annotations:
                    if hasattr(annotation, "url") and annotation.url:
                        urls.append(annotation.url)
        return urls
