"""サーチャー：index.jsonを読み込んでキーワード検索する"""

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    """検索結果の1件を表すデータクラス"""
    file: str
    file_type: str
    location: dict
    content: str


def search(
    index_path: str,
    keyword: str,
    use_regex: bool = False,
    ignore_case: bool = False,
) -> list[SearchResult]:
    """
    index.json を読み込んでキーワード検索し、ヒットした結果一覧を返す。
    """
    index_file = Path(index_path)
    if not index_file.exists():
        raise FileNotFoundError(
            f"インデックスファイルが見つかりません: {index_path}\n"
            "先に `mycli index <ディレクトリ>` を実行してください。"
        )

    with open(index_file, "r", encoding="utf-8") as f:
        index = json.load(f)

    # 検索パターンを構築
    flags = re.IGNORECASE if ignore_case else 0
    if use_regex:
        try:
            pattern = re.compile(keyword, flags)
        except re.error as e:
            raise ValueError(f"正規表現が不正です: {e}")
    else:
        # 通常検索はキーワードをエスケープして正規表現に変換
        pattern = re.compile(re.escape(keyword), flags)

    results = []
    for entry in index:
        for item in entry.get("contents", []):
            content = item.get("content", "")
            if pattern.search(content):
                results.append(SearchResult(
                    file=entry["file"],
                    file_type=entry["type"],
                    location=item.get("location", {}),
                    content=content,
                ))

    return results


def format_location(file_type: str, location: dict) -> str:
    """ロケーション情報を人間が読みやすい形式に変換する。"""
    parts = []
    if location.get("sheet"):
        parts.append(f"Sheet: {location['sheet']}")
    if location.get("cell"):
        parts.append(f"Cell: {location['cell']}")
    if location.get("shape_id") and not location.get("sheet"):
        parts.append(f"Shape: {location['shape_id']}")
    if location.get("slide") is not None:
        parts.append(f"Slide: {location['slide']}")
    if location.get("page") is not None:
        parts.append(f"Page: {location['page']}")
    if location.get("paragraph_index") is not None:
        parts.append(f"Para: {location['paragraph_index']}")
    return ", ".join(parts) if parts else ""
