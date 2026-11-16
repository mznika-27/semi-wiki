"""檢查整個網站有沒有照 CLAUDE.md 的規則。每次新增或修改詞條後都要跑：

    python tools/check.py

全部通過才可以 commit。檢查項目：
1. terms.json 每個詞條都有對應的 wiki/<slug>.html，反過來也一樣
2. 必填欄位都有填，分類代碼存在，slug 格式正確，一句話說明 40 字以內
3. 每頁五個段落（what / chain / companies / myth / related）都在，而且照順序
4. 沒有留下 {{ }} 佔位符或範本註解
5. 頁面標題、一句話說明跟 terms.json 一致
6. 相關詞條：每頁至少 2 個，連到的頁面存在，而且 A 連 B 時 B 也要連回 A
7. 不准出現的字眼（股價、目標價、買進、賣出、推薦買）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ["what", "chain", "companies", "myth", "related"]
BANNED = ["目標價", "股價", "買進", "賣出", "推薦買", "加碼", "減碼"]
REQUIRED = ["slug", "name", "en", "category", "oneliner", "related", "updated"]


def main():
    errors = []
    data = json.loads((ROOT / "data" / "terms.json").read_text(encoding="utf-8"))
    cats = data["categories"]
    terms = {t["slug"]: t for t in data["terms"]}
    pages = {p.stem for p in (ROOT / "wiki").glob("*.html")}

    for slug in sorted(set(terms) - pages):
        errors.append(f"{slug}: terms.json 有登記，但 wiki/{slug}.html 不存在")
    for slug in sorted(pages - set(terms)):
        errors.append(f"{slug}: 有 wiki/{slug}.html，但 terms.json 沒登記")

    for slug, t in terms.items():
        miss = [k for k in REQUIRED if not t.get(k) and k != "related"]
        if miss:
            errors.append(f"{slug}: terms.json 缺欄位 {miss}")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            errors.append(f"{slug}: slug 格式不對，只能用小寫英文、數字、連字號")
        if t.get("category") not in cats:
            errors.append(f"{slug}: 分類 {t.get('category')} 不存在")
        if len(t.get("oneliner", "")) > 40:
            errors.append(f"{slug}: 一句話說明超過 40 字（{len(t['oneliner'])} 字）")
        rel = t.get("related", [])
        if len(rel) < 2:
            errors.append(f"{slug}: 相關詞條少於 2 個")
        for r in rel:
            if r not in terms:
                errors.append(f"{slug}: 相關詞條 {r} 不存在")
            elif slug not in terms[r].get("related", []):
                errors.append(f"{slug}: 連到 {r}，但 {r} 沒有連回來")

        path = ROOT / "wiki" / f"{slug}.html"
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        found = re.findall(r'<section id="([a-z]+)"', html)
        if found != SECTIONS:
            errors.append(f"{slug}: 段落應為 {SECTIONS}，實際為 {found}")
        if "{{" in html or "<!--" in html:
            errors.append(f"{slug}: 還有沒填的佔位符或範本註解")
        if f"<h1>{t.get('name')}</h1>" not in html:
            errors.append(f"{slug}: 頁面 <h1> 跟 terms.json 的 name 不一致")
        if f'<div class="oneliner">{t.get("oneliner")}</div>' not in html:
            errors.append(f"{slug}: 頁面一句話說明跟 terms.json 不一致")
        if f'class="tag cat-{t.get("category")}"' not in html:
            errors.append(f"{slug}: 分類標籤跟 terms.json 不一致")
        page_links = set(re.findall(r'<a href="([a-z0-9-]+)\.html">', html))
        if page_links != set(rel):
            errors.append(f"{slug}: 頁面相關詞條 {sorted(page_links)} 跟 terms.json {sorted(rel)} 不一致")
        for sec in ["what", "myth"]:
            m = re.search(rf'<section id="{sec}">(.*?)</section>', html, re.S)
            if m and "<p>" not in m.group(1):
                errors.append(f"{slug}: {sec} 段落沒有內容")
        m = re.search(r'<section id="companies">(.*?)</section>', html, re.S)
        if m and m.group(1).count("<tr>") < 2:
            errors.append(f"{slug}: 相關公司表格沒有內容")
        text = re.sub(r"<[^>]+>", "", html)
        for w in BANNED:
            if w in text:
                errors.append(f"{slug}: 出現不准用的字眼「{w}」")

    if errors:
        print(f"沒通過，共 {len(errors)} 個問題：")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"全部通過：{len(terms)} 個詞條、{len(cats)} 個分類。")


if __name__ == "__main__":
    main()
