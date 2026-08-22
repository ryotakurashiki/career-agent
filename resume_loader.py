import os
from pypdf import PdfReader
from config import DOCS_DIR


def load_all_docs() -> str:
    """
    DOCS_DIR 内の全ファイルを読み込み、結合したテキストを返す。
    対応フォーマット: PDF, TXT
    """
    if not os.path.exists(DOCS_DIR):
        raise FileNotFoundError(f"{DOCS_DIR} が見つかりません。ディレクトリを作成してファイルを置いてください。")

    texts = []
    for filename in sorted(os.listdir(DOCS_DIR)):
        file_path = os.path.join(DOCS_DIR, filename)
        if filename.endswith(".pdf"):
            texts.append(f"=== {filename} ===\n{_load_pdf(file_path)}")
        elif filename.endswith(".txt"):
            texts.append(f"=== {filename} ===\n{_load_txt(file_path)}")
        # 未対応の拡張子はスキップ

    if not texts:
        raise FileNotFoundError(f"{DOCS_DIR} に対応ファイル（PDF, TXT）が見つかりません。")

    return "\n\n".join(texts)


def _load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages = [page.extract_text() for page in reader.pages]
    return "\n".join(pages)


def _load_txt(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        return f.read()
