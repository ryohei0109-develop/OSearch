"""
mycli - ドキュメント検索CLIツール

使い方:
  python mycli.py index <ディレクトリ>          インデックス作成
  python mycli.py search "<キーワード>"         キーワード検索
  python mycli.py search "<キーワード>" --regex  正規表現検索
  python mycli.py search "<キーワード>" --ignore-case  大文字小文字無視
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="mycli",
        description="Office ドキュメント（.docx/.xlsx/.pptx）の内容を検索するCLIツール",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="コマンド")
    subparsers.required = True

    # --- index サブコマンド ---
    index_parser = subparsers.add_parser(
        "index",
        help="指定ディレクトリのドキュメントをインデックス化する",
    )
    index_parser.add_argument(
        "target_directory",
        help="インデックス対象のディレクトリパス",
    )
    index_parser.add_argument(
        "--output", "-o",
        default=None,
        help="インデックスファイルの出力先（デフォルト: data/index.json）",
    )

    # --- search サブコマンド ---
    search_parser = subparsers.add_parser(
        "search",
        help="インデックスからキーワード検索する",
    )
    search_parser.add_argument(
        "keyword",
        help="検索キーワード",
    )
    search_parser.add_argument(
        "--regex",
        action="store_true",
        help="正規表現検索を有効にする",
    )
    search_parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="大文字小文字を無視して検索する",
    )
    search_parser.add_argument(
        "--index", "-i",
        default=None,
        help="インデックスファイルのパス（デフォルト: data/index.json）",
    )

    args = parser.parse_args()

    if args.command == "index":
        from cli.index import run
        run(args)
    elif args.command == "search":
        from cli.search import run
        run(args)


if __name__ == "__main__":
    main()
