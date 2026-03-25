"""インデクサー：ディレクトリを走査してindex.jsonを生成する"""

import json
import os
from pathlib import Path

from parser.excel import parse as parse_excel
from parser.word import parse as parse_word
from parser.ppt import parse as parse_ppt


# 対応拡張子とパーサーのマッピング
_PARSERS = {
    ".xlsx": ("excel", parse_excel),
    ".docx": ("word", parse_word),
    ".pptx": ("powerpoint", parse_ppt),
}


def build_index(target_dir: str, output_path: str) -> int:
    """
    target_dir 配下を再帰走査してindex.jsonを生成する。
    戻り値: インデックス登録ファイル数
    """
    target = Path(target_dir)
    if not target.is_dir():
        raise ValueError(f"指定されたパスはディレクトリではありません: {target_dir}")

    index = []
    file_count = 0

    for file_path in target.rglob("*"):
        ext = file_path.suffix.lower()
        if ext not in _PARSERS:
            continue

        # 一時ファイル（~$ プレフィックス）はスキップ
        if file_path.name.startswith("~$"):
            continue

        file_type, parser_fn = _PARSERS[ext]
        print(f"  解析中: {file_path}")

        try:
            contents = parser_fn(str(file_path))
        except Exception as e:
            print(f"  [エラー] スキップします: {file_path} ({e})")
            continue

        if contents:
            index.append({
                "file": str(file_path),
                "type": file_type,
                "contents": contents,
            })
            file_count += 1

    # 出力ディレクトリを作成してJSON書き込み
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return file_count
