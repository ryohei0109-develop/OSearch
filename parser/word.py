"""Word ファイルのパーサー（本文＋図形）"""

import zipfile
from lxml import etree
from docx import Document


# XML 名前空間
_NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def parse(file_path: str) -> list[dict]:
    """
    .docx ファイルを解析してコンテンツリストを返す。
    本文段落と図形内テキストの両方を対象とする。
    ページ番号は段落インデックスから推定（簡易実装）。
    """
    contents = []

    # --- 本文段落 ---
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"[警告] Wordファイルの読み込みに失敗しました: {file_path} ({e})")
        return contents

    for para_idx, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        contents.append({
            "location": {
                "page": None,          # python-docx ではページ番号の正確な取得が困難
                "paragraph_index": para_idx,
                "sheet": None,
                "cell": None,
                "slide": None,
                "shape_id": None,
            },
            "content": text,
        })

    # --- 図形内テキスト（XML解析）---
    try:
        contents.extend(_parse_shapes(file_path))
    except Exception as e:
        print(f"[警告] Word図形テキスト解析に失敗しました: {file_path} ({e})")

    return contents


def _parse_shapes(file_path: str) -> list[dict]:
    """word/document.xml から w:t タグのテキストを抽出する（図形内）。"""
    results = []
    with zipfile.ZipFile(file_path, "r") as zf:
        if "word/document.xml" not in zf.namelist():
            return results
        xml_data = zf.read("word/document.xml")
        root = etree.fromstring(xml_data)

        # w:drawing 要素配下にある a:t タグ（DrawingML）を対象とする
        ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
        for drawing in root.iter(f"{{{_NS_W}}}drawing"):
            for t_elem in drawing.iter(f"{{{ns_a}}}t"):
                text = (t_elem.text or "").strip()
                if not text:
                    continue
                results.append({
                    "location": {
                        "page": None,
                        "paragraph_index": None,
                        "sheet": None,
                        "cell": None,
                        "slide": None,
                        "shape_id": "drawing",
                    },
                    "content": text,
                })

    return results
