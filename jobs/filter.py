import re
from jobs.models import Job


class HardFilter:
    """
    ③ Python Hard Filter

    LLMを使わず、ハードルールで求人を除外する。
    「絶対に合わない」求人をここで落とすことで、
    後段のLLM評価のコストと精度を守る。
    """

    def run(self, jobs: list[Job], preferences: dict) -> list[Job]:
        jobs = self._filter_location(jobs, preferences)
        jobs = self._filter_employment_type(jobs, preferences)
        return jobs

    def _filter_location(self, jobs: list[Job], preferences: dict) -> list[Job]:
        locations = preferences.get("希望勤務地", [])
        if not locations:
            return jobs

        # preferencesの勤務地文字列から検索キーワードを抽出する
        # 例: "ホーチミン(ベトナム)" → "ホーチミン"
        #     "海外からのフルリモート" → "フルリモート"
        key_terms = [self._extract_location_key(loc) for loc in locations]

        return [
            job for job in jobs
            if any(term in job.location for term in key_terms)
        ]

    def _filter_employment_type(self, jobs: list[Job], preferences: dict) -> list[Job]:
        pref_types = preferences.get("雇用形態", [])
        if not pref_types:
            return jobs

        mapping = {"正社員": "fulltime", "業務委託": "contract"}
        allowed = {mapping[t] for t in pref_types if t in mapping}
        if not allowed:
            return jobs

        return [job for job in jobs if job.employment_type in allowed]

    def _extract_location_key(self, location: str) -> str:
        # 括弧とその中身を削除: "ホーチミン(ベトナム)" → "ホーチミン"
        location = re.sub(r'[（(][^)）]*[)）]', '', location).strip()
        # "〜からの〜" パターンは末尾の語を取る: "海外からのフルリモート" → "フルリモート"
        if 'からの' in location:
            location = location.split('からの')[-1]
        return location
