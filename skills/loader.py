from pathlib import Path


def load_skill(skill_name: str) -> str:
    """
    skills/<skill_name>/SKILL.md を読み込んで文字列として返す。

    使い方:
        skill = load_skill("job-evaluation")
        # -> SKILL.md の内容がそのまま返る
    """
    path = Path(__file__).parent / skill_name / "SKILL.md"
    return path.read_text(encoding="utf-8")
