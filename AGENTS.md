# AGENTS.md

這個專案的完整規則寫在 [CLAUDE.md](CLAUDE.md)，不管用哪一個 AI 工具，開工前都先讀那一份。

最常用的三件事：

- 新增詞條：`python tools/new_term.py <slug> <中文名稱> <英文名稱> <分類代碼> <瓶頸代碼> <一句話說明>`，再把六個段落寫完
- 檢查全站：`python tools/check.py`，看到「全部通過」才 commit
- 本機預覽：`python -m http.server 8000`，打開 http://localhost:8000
- Windows 中文亂碼時，Python 指令加 `-X utf8`
