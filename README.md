# 依存ライブラリのインストール
python -m pip install -r requirements.txt

# インデックス作成
python mycli.py index C:\docs

# キーワード検索
python mycli.py search "売上"

# 正規表現検索
python mycli.py search "売上|契約" --regex

# 大文字小文字無視
python mycli.py search "sales" --ignore-case
