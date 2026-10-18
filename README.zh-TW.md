# wheel-coding

> English: [README.md](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**先找輪子，再動手造。** 這裡只放一個 skill：`wheel` —— 動手前查三軸 prior-art（官方文件／社群共識／成熟開源輪子），出一張輪子卡裁決，並在需要時從閉源產物反推它用了什麼。

編碼行為紀律（動手前紀律、研究優先、停損、驗收、派工）已獨立到 [royalskynet/ether-code](https://github.com/royalskynet/ether-code)，`coding-hermes` 的 Layer 2 指向本 repo 的 `wheel`。

**技能類型：** 純文檔紀律，無 runtime 依賴；附一個只用標準庫的登記簿 CLI。

## 安裝

```bash
npx skills add https://github.com/royalskynet/wheel-coding --skill wheel
```

安裝到 `~/.hermes/skills/wheel/`。**開新 session** 才會進索引生效。

## `/wheel` 預設做三件事

| # | 做什麼 | 何時 |
|---|---|---|
| 1. 決策 | 官方文檔＋社群共識＋成熟輪子一起收，支持「做／不做／用誰」的 7 級裁決 | 每次 |
| 2. 輪子 | 成熟方案與開源輪子的清單、採用量、授權、維護狀況，供膠水或採用 | 每次（Quick 只跑這一軸） |
| 3. 逆向 | 目標是閉源產物（Electron／APK／binary／私有 registry 包）時，從產物反推依賴與設計 | 情境需要或使用者要求，不是每次 |

逆向只到「事實與清單」：列 asar／包成員、`otool -L`、`codesign -dv`、strings、sourcemap。不整份反編譯、不碰 DRM。全量 rea（Ghidra／IDA 深層反編譯）不在本 skill 範圍。

## 功能

- **重述問題**：先問「不做會怎樣」，能刪就裁決成 `不做`；真問題是別的 → `換題`。
- **定深度**：Quick／Standard／Full／Full＋逆向，不是每次都全跑。
- **三軸＋閉源軸**：gh issues、HN、Stack Overflow 做社群共識；`gh search repos`／npm／pip／brew 找輪子；deps.dev＋下載量判龍頭；閉源軸用只讀工具。
- **評分**：活躍度、授權、成本、可逆性、採用量、社群抱怨；stars 只排序不計分。
- **7 級裁決**：不做／換題／設定／採用／改用／借鏡／自造，自造是最後一格。
- **不對稱閘**：自造或帶警示才要第二意見。
- **輪子卡**：≤12 行，plan 的「輪子：」行就是卡片首行。
- **登記簿**：每張卡記一行，`review_by` 依領域變化速度（30／90／180 天）過期。

## 登記簿

```bash
python3 skills/wheel/scripts/wheel_registry.py find "<關鍵字>" "<英文說法>"   # 第 0 步
python3 skills/wheel/scripts/wheel_registry.py add "設定｜借鏡" "<問題>" "<首選>" 90
python3 skills/wheel/scripts/wheel_registry.py check
```

五欄 TSV：date、verdict、problem、choice、review_by；檔案在 `~/.wheel/registry.tsv`（可用 `WHEEL_REGISTRY` 覆寫）。純標準庫、無網路。腳本不在時 skill 有 `grep`／`printf` 的等價寫法，`scripts/test_skill.py` 會直接執行那段原文驗證兩邊一致。

## 測試

```bash
python3 skills/wheel/scripts/test_wheel_registry.py   # 144 項：文法、過期判定、exit code
python3 skills/wheel/scripts/test_skill.py            # 30 項：SKILL.md 與 CLI 契約、fallback 可跑
```

## 觸發條件

**觸發：** 要自造、選型、「該用哪個／有沒有現成／最好的做法／最新版是多少」、新增依賴或子系統、寫超過膠水量的新程式、同一解法連敗 2 次。

**不觸發：** typo、純改既有程式、概念解釋、已有未過期輪子卡的續做。

## 血緣

`wheel` 的概念取自 deja-vu（裁決＋不對稱閘）與 dont-reinvent（授權／維護檢查），由 `coding-hermes` 的 Layer 2 於 v2.4.0 抽出成獨立 skill。沿革與各版差異見 [HISTORY.md](HISTORY.md)。

## License

MIT。Copyright (c) 2026 royalskynet。
