# AI 供應鏈技術筆記

追 AI 伺服器供應鏈時碰到的新技術，一個技術一頁：跟舊做法差在哪、卡在哪、研究時看什麼。

網站：https://mznika-27.github.io/semi-wiki/

## 這個專案的重點

網站本身很簡單，重點是 [CLAUDE.md](CLAUDE.md)：裡面寫好了什麼技術值得開一頁、詞條頁的固定格式、命名方式、分類、寫作規則和新增步驟。之後要加新技術，只要叫 AI 先讀 CLAUDE.md，再說「新增一個 OOO 的詞條」，它就能照同一套方式做完，最後用 `tools/check.py` 檢查有沒有漏。

## 本機預覽

```
python -m http.server
```

打開 http://localhost:8000

政大 財管三 周孟臻・生成式 AI 課第九週作業
