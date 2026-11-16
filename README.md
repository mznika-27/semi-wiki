# 半導體產業小百科

用白話解釋 AI 晶片供應鏈上的名詞，一個名詞一頁，頁面之間互相連結。

網站：https://mznika-27.github.io/semi-wiki/

## 這個專案的重點

網站本身很簡單，重點是 [CLAUDE.md](CLAUDE.md)：裡面寫好了詞條頁的固定格式、命名方式、分類、寫作規則和新增步驟。之後要加新名詞，只要叫 AI 先讀 CLAUDE.md，再說「新增一個 OOO 的詞條」，它就能照同一套方式做完，最後用 `tools/check.py` 檢查有沒有漏。

## 本機預覽

```
python -m http.server
```

打開 http://localhost:8000

政大 財管三 周孟臻・生成式 AI 課第九週作業
