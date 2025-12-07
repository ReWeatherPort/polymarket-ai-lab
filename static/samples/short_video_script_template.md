# Shorts 腳本 - {{ $json.date }}

【開場 2s】
旁白：OKC x Polymarket 今日實驗速覽！

【數據 5s】
旁白：PnL：$ {{ $json.pnl }}，勝率：{{ $json.win_rate * 100 }}%，最大回撤：$ {{ $json.max_drawdown }}。

【策略 7s】
旁白：今日策略重點：低價買入 + 風險控制；觀察賽中波動，避免追高。

【風險 5s】
旁白：注意流動性與滑點，單筆倉位不超過 2%，回撤達閾值即停損。

【結尾 3s】
旁白：更多數據與教學，見 Polymarket AI Lab。