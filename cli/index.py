"""index サブコマンドのハンドラ"""

import sys
from core.indexer import build_index


# デフォルトのインデックス保存先
DEFAULT_INDEX_PATH = "data/index.json"


def run(args):
    """index コマンドを実行する。"""
    target_dir = args.target_directory
    output_path = args.output or DEFAULT_INDEX_PATH

    print(f"インデックス作成開始: {target_dir}")
    print(f"出力先: {output_path}")
    print("-" * 40)

    try:
        count = build_index(target_dir, output_path)
    except ValueError as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)

    print("-" * 40)
    print(f"完了: {count} ファイルをインデックスに登録しました。")
    print(f"インデックスファイル: {output_path}")
