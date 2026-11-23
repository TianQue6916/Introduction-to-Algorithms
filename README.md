# Introduction to Algorithms · MIT 6.006

算法导论课程的双语学习资料库。

- 教材：Cormen / Leiserson / Rivest / Stein《Introduction to Algorithms》（CLRS）
- 课程：MIT 6.006 Introduction to Algorithms, Spring 2020
- 视频本体因体积未收录，字幕见 `05-subtitles/`

## 目录结构

| 目录 | 内容 |
|---|---|
| `01-clrs-book/` | CLRS 教材逐段双语翻译，按页分块（`chunk01`–`chunk06`，覆盖 book p005–p242） |
| `02-lecture-notes/` | 课堂讲义双语翻译（lec15–lec19：递归算法、动态规划、伪多项式、复杂性）+ `LNotes/` 官方讲义 1–20 |
| `03-problem-sets/` | 官方原卷与解答（`prob7sol`、`prob8sol`、`ps6sol`、`ps7sol`、`r15`–`r17`）+ 对应双语译本（`*.bilingual.md`）+ 6.006 PS6 中文版 |
| `04-exams/` | Exams 1–14 原卷 + 课程进度表 |
| `05-subtitles/` | 全部讲次的中英双语字幕（`.srt` 英文原轨 + `.zho-hans.srt` 中文轨） |
| `06-notes/` | 个人推导笔记：动态规划（DP）判定、LCS 最优子结构、编辑距离贪心反例、Bellman-Ford/Johnson 等 |

## 双语规范

正文以中文为主体，英文术语以 `English term（中文）` 形式行内嵌入；公式与 LaTeX 环境保留英文原样。

## 学习定位

对应方舟计划的**算法主线**，与 `Design-and-Analysis-of-Algorithms-6.046J`（进阶）构成两级算法训练。

> 早期混入的 C/C++ 入门练习已于 2026-09-23 移至独立仓库 [`Introduction-to-Algorithms-codetry`](https://github.com/TianQue6916/Introduction-to-Algorithms-codetry)。
---

> 图片已按技能铁律 42 base64 内嵌进 md；56 个源文件（54 png + 2 svg）逐个按「字节数 + 前 64 字节 md5」核对命中后，源资产目录 `02-讲义/_assets/`、`02-讲义/assets/` 已删除，图片只存在于 md 的 data URI 里。

## 目录结构

> 本节描述 **2026-11 目录归一化后**的结构；上文同名节为归一化前的历史记录，按「原有内容不动」原则保留。

| 目录 | 内容 |
|---|---|
| `01-教材/` | CLRS 教材逐段双语翻译，平铺 6 个分块 `clrs_chunk01`–`clrs_chunk06`（覆盖 book p005–p242） |
| `02-讲义/` | 课堂讲义 lec01–lec20：PDF 原件 + 译文 md（平铺）；`_assets/`、`assets/` 源资产目录已删除（图片全部 base64 内嵌在 md 中） |
| `视频/` | 全部讲次与 Problem Session 的中英双语字幕（英文原轨 `.srt` + 中文轨 `.zho-hans.srt`／`.zh-CN.srt`）；视频本体因体积未收录 |
| `03-已处理文件/` | 疑问驱动的 AI 资料：原 `06-笔记/` 全部个人推导笔记 + `06-notes/clrs_toc.txt` |
| `04-题目/作业/` | 官方作业原件与译本（`MIT-6.006-Problem-Set-6-Chinese.docx`）+ Recitation 15–17 习题课材料（`r15`–`r17`） |
| `04-题目/考试/` | Exams 1–14 原卷与译本（`6.006_EX1`–`6.006_EX14`，每份 `.pdf` + `.md`） |
| `04-题目/题解/` | 官方题目解答（`prob7sol`、`prob8sol`、`ps6_sol`、`ps7_sol`、`q2_sol`、`review2_sol`） |
| `05-代码/` | 课程附带代码与自有编程（本轮无内容） |
| `06-工具/` | 脚本、Lean 验证、给模型读的索引（本轮无内容） |
| `_superseded/` | 历史被替换版本，原地保留不动 |
| 仓根 | `README.md`、`llms.txt`、`LICENSE`、`NOTICE` |

## 6.006 现状（2026-11-23 审计）

| 项 | 现状 |
|---|---|
| 讲义 | 20 讲齐全：lec v2 主版本 + LNotes v1 紧凑版，两版内容已融合（每讲 `.pdf` 原件 + `.md` 译文） |
| 教材 | CLRS book p005–p242，共 6 片（`clrs_chunk01`–`clrs_chunk06`），36 张原书插图已补 |
| 题目 | Recitation 15–17（`r15`–`r17`）+ Exams 1–14（`EX1`–`EX14`，每份 `.pdf` + `.md`）；EX10–EX12 已按「每次带括号」重做 |
| 清理 | lec18 重复 PDF（`lec18-pseudopolynomial-LNotes18.pdf`，8 页，与 `lec18-pseudopolynomial.pdf` 同源）已删除；归一化残留的空目录 `01-clrs-book/`、`03-problem-sets/`、`04-exams/`、`02-lecture-notes/LNotes/` 已清空并移除 |

**已知缺失（本仓范围内做不了或未做）**

- Problem Set 题目：PS1–PS5、PS7、PS8（仅存 PS6 中文版与 `ps6_sol`、`ps7_sol` 等解答）
- 官方解答：Quiz 1、Quiz 3、Final（官方未公开解答）
- Recitation 1–20：课程本身无译本（仅 r15–r17 有材料）
