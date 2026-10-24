# 股票觀察清單 Stock Tracker

一個使用 Django 開發的股票觀察清單網站，支援台股與美股，具備即時股價與 K 線圖功能。

## 功能

- 使用者註冊／登入／登出
- 新增、編輯、刪除股票
- 顯示即時股價（串接 Yahoo Finance）
- 互動式 K 線圖（支援 1 個月、3 個月、6 個月、1 年）
- MA5、MA20、MA60 均線顯示
- 自動判斷台股（加上 .TW）與美股格式
- RWD 響應式設計（Bootstrap 5）

## 使用工具

- **後端**：Python 3.14、Django 6.0
- **前端**：Bootstrap 5、Plotly
- **資料來源**：yfinance（Yahoo Finance）
- **資料庫**：SQLite
- **版本控制**：Git／GitHub

