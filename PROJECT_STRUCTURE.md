polymarket-ai-lab/
├─ archetypes/
│  └─ default.md
├─ content/
│  ├─ posts/                # 每日實驗日誌
│  │  └─ okc-experiment-2025-01-01.md
│  ├─ notes/                # 教學 / 指南 / 工具分享
│  │  └─ polymarket-strategy-guide.md
│  └─ _index.md             # 用於首頁或目錄描述（可選）
├─ data/                    # 可存 JSON/CSV（例如計算結果快取）
│  └─ experiments.json
├─ layouts/                 # Hugo 模板（如需自訂）
│  ├─ _default/
│  │  ├─ baseof.html
│  │  ├─ list.html
│  │  └─ single.html
│  ├─ posts/
│  │  └─ single.html        # 文章頁自訂模板（展示 PnL / 勝率等指標）
│  └─ partials/
│     └─ stats.html         # 指標區塊 partial
├─ static/                  # 圖檔、JSON、其他靜態資源
│  ├─ images/
│  │  └─ logo.png
│  └─ samples/
│     └─ post-template.json
├─ assets/                  # 若採用 Hugo Pipes 處理 CSS/JS（可選）
│  └─ css/
│     └─ main.css
├─ themes/                  # 主題（可用官方 theme 或自製）
│  └─ polymarket-ai-lab/
│     ├─ layouts/...
│     └─ assets/...
├─ .github/
│  └─ workflows/
│     └─ deploy.yml         # GitHub Actions: build & deploy 到 Pages
├─ hugo.toml                # Hugo 主設定檔（用 TOML）
├─ README.md