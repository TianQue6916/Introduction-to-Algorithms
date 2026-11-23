# 04-题目 · MIT 6.006 习题与考试译注索引

三个子目录：

- `作业/` —— Problem Set（`ps*.md`）与 Recitation（`r*.md`）译注，源 PDF 与 `.md` 同目录同名。
- `题解/` —— Problem Session / Problem Set 的官方解答译注（`prob*sol.md`、`ps*_sol.md`）。
- `考试/` —— Quiz / Final 试卷与官方解答（`6.006_*.md/.pdf`），本页对照表即针对此目录。

## OCW 原名 ↔ 仓内文件名对照

2026-11-23 起，`考试/` 下原名 `6.006_EX<n>.*` 的 9 组文件按 OCW 原件身份改为语义名（`git mv`，历史保留）。md5 为改名前旧文件的实测值前 8 位（`git mv` 不改内容，改名后数值不变）。

| 仓内新名 | OCW 材料 | 原 EX 名 | md md5 | pdf md5 |
|---|---|---|---|---|
| `6.006_final.md` / `.pdf` | Final Exam（期末试卷，21 页） | `6.006_EX1` | `90e1116c` | `a7a62614` |
| `6.006_final_sol.md` / `.pdf` | Final Exam Solutions（官方解答） | `6.006_EX2` | `1ddd87cc` | `8fa8ce1d` |
| `6.006_q2.md` / `.pdf` | Quiz 2（第二次小测） | `6.006_EX7` | `c1c8244e` | `a5272b15` |
| `6.006_q2_sol.md` / `.pdf` | Quiz 2 Solutions | `6.006_EX10` | `ab69ff5c` | `d9e0848f` |
| `6.006_q3.md` / `.pdf` | Quiz 3 | `6.006_EX11` | `9303e13d` | `df6fa93f` |
| `6.006_q3_sol.md` / `.pdf` | Quiz 3 Solutions | `6.006_EX14` | `2b5c1429` | `cfa0ce66` |
| `6.006_review2_sol.md` / `.pdf` | Quiz 2 Review Solutions（复习课解答） | `6.006_EX9` | `68133306` | `f26b3093` |
| `6.006_review3.md` / `.pdf` | Quiz 3 Review（复习课） | `6.006_EX12` | `09a15e69` | `dac04d9e` |
| `6.006_review3_sol.md` / `.pdf` | Quiz 3 Review Solutions | `6.006_EX13` | `ae1a52b9` | `3955f42e` |

证据等级（按仓库技能的来源分级）：

- `6.006_EX2 → 6.006_final_sol` 是 **A 级**：重新从 MIT OCW 下载 `final_sol.pdf` 后与其做字节级与 MD5 比对，完全一致。推理全文见 `../03-已处理文件/ex2-身份判定.md`（该 md 标题自称「Final Exam Review 1」，是孤立误标：全文只有标题那一行出现 "Review"）。
- 其余 8 条为 **B 级**：由卷面内容、页数、题号与「题目 / 解答」配对关系归类，未逐字节比对 OCW 原件。

## 身份待定（未改名）

`6.006_EX3`、`EX4`、`EX5`、`EX6`、`EX8` 五组保留原 EX 编号：卷面内容与 OCW 具体文件尚未对上（其中 EX3/EX6 体量最大，疑为多材料合订），在对上之前不改名，避免把错的身份固化成文件名。
