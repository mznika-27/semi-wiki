"""新增詞條的骨架：複製 templates/term.html 到 wiki/<slug>.html，並在 data/terms.json 登記。

用法：
    python tools/new_term.py <slug> <中文名稱> <英文名稱> <分類代碼> <一句話說明>
例：
    python tools/new_term.py probe-card 探針卡 "Probe Card" test "晶圓切割前，用來一顆一顆測晶片好壞的針頭。"

跑完之後還要手動把 wiki/<slug>.html 裡五個段落寫完，相關詞條填進 terms.json 的 related，最後跑 tools/check.py。
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)
    slug, name, en, cat, oneliner = sys.argv[1:]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit("slug 只能用小寫英文、數字和連字號，例如 probe-card")

    data_path = ROOT / "data" / "terms.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if cat not in data["categories"]:
        sys.exit(f"沒有這個分類：{cat}。可用：{', '.join(data['categories'])}")
    if any(t["slug"] == slug for t in data["terms"]):
        sys.exit(f"{slug} 已經存在")

    page = ROOT / "wiki" / f"{slug}.html"
    today = date.today().isoformat()
    html = (ROOT / "templates" / "term.html").read_text(encoding="utf-8")
    for key, val in {"SLUG": slug, "NAME": name, "EN": en, "CATEGORY": cat,
                     "CATEGORY_LABEL": data["categories"][cat]["label"],
                     "ONELINER": oneliner, "UPDATED": today}.items():
        html = html.replace("{{" + key + "}}", val)
    page.write_text(html, encoding="utf-8")

    data["terms"].append({"slug": slug, "name": name, "en": en, "category": cat,
                          "oneliner": oneliner, "related": [], "updated": today})
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已建立 wiki/{slug}.html，並登記到 data/terms.json。接著把五個段落寫完。")


if __name__ == "__main__":
    main()
