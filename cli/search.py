"""search サブコマンドのハンドラ"""

import sys
from core.searcher import search, format_location


# デフォルトのインデックスパス
DEFAULT_INDEX_PATH = "data/index.json"


def run(args):
    """search コマンドを実行する。"""
    keyword = args.keyword
    index_path = args.index or DEFAULT_INDEX_PATH
    use_regex = args.regex
    ignore_case = args.ignore_case

    try:
        results = search(
            index_path=index_path,
            keyword=keyword,
            use_regex=use_regex,
            ignore_case=ignore_case,
        )
    except FileNotFoundError as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("該当する結果が見つかりませんでした。")
        return

    print(f"{len(results)} 件見つかりました。\n")
    for i, result in enumerate(results, start=1):
        loc_str = format_location(result.file_type, result.location)
        if loc_str:
            print(f"[{i}] {result.file} ({loc_str})")
        else:
            print(f"[{i}] {result.file}")

        # コンテンツのプレビュー（長い場合は先頭80文字）
        preview = result.content.replace("\n", " ")
        if len(preview) > 80:
            preview = preview[:80] + "..."
        print(f"    {preview}")
        print()
