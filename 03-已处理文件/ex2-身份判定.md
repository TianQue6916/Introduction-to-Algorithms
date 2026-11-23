# 6.006_EX2 身份判定：它是 Final 的官方解答，不是 Review 课材料

> **判定对象**：`04-题目/考试/6.006_EX2.md`（806 行，标题自称「Final Exam Review 1」）与其源 PDF `04-题目/考试/6.006_EX2.pdf`（351596 B）。
> **判定日期**：2026-11-23。**判定人**：补译与研判 worker（delegationDepth = 1）。
> **本文性质**：证据与结论，不是译文。文中「英文原句 + 中文对照」以表格并排出现，是为了让原句可逐字核对，不构成译文正体。
> **来源等级**（按本仓库技能铁律 29）：A 级 = 一手材料（PDF 字节、PDF 元数据、PDF 文字层、OCW 官方直链）可直接核对；B 级 = 二手推断（本机 grep 统计、页数对照）；未标注者一律视为「未经检验的结论」。

---

## 一句话结论

`6.006_EX2.md` 所译的 PDF 是 MIT 6.006 Spring 2020 的 **Final Exam Solutions（期末考官方解答）**，不是任何「Final Exam Review（期末复习课）」材料。md 标题里的「Final Exam Review 1」是一处孤立误标：**全文只有标题那一行出现 "Review"，正文零处**。因此处置方式是**改标题，不重译**。

---

## 证据一（A 级）：与 OCW 的 `final_sol.pdf` 字节级等同

本次直接从 MIT OpenCourseWare（麻省理工学院开放课件）把原件重新下载了一遍再比，不依赖任何转述。

| 文件 | 字节 | MD5 |
|---|---|---|
| 本机 `04-题目/考试/6.006_EX2.pdf` | 351596 | `8fa8ce1d657e9fd75b41ca8592aab9b3` |
| OCW 原件 `MIT6_006S20_final_sol.pdf` | 351596 | `8fa8ce1d657e9fd75b41ca8592aab9b3` |

- 字节数相同、MD5 相同，`cmp -s` 返回 **IDENTICAL-BYTES**（零输出即逐字节一致）——这比 MD5 相同更强一层，因为 `cmp` 是比较实际字节而不是摘要。
- 下载直链（2026-11-23 实测 200，351596 字节）：
  `https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/e882f34a3f46aa9862953616f6de1c57_MIT6_006S20_final_sol.pdf`
- 文件名 `..._final_sol.pdf` 是 OCW 自己的命名（`sol` = solution），不是本仓库的命名。

## 证据二（A 级）：PDF 元数据自述其身份

`pdfinfo` 读出的文档属性（不是正文，是 PDF 的 `/Info` 字典）：

```text
Title:          6.006 Introduction to Algorithms, Final Exam Solutions
Author:         Erik Demaine, Jason Ku, Justin Solomon
Creator:        TeX
Producer:       pdfTeX-1.40.20
CreationDate:   Sun May 24 00:30:29 2020 中国标准时间
Pages:          21
Page size:      612 x 792 pts (letter)
```

标题里写的是 **Final Exam Solutions（期末考解答）**。作者三人与 6.006 Spring 2020 的授课教师一致。21 页这个数字后面还要用到（md 的页标记正好覆盖到第 21 页）。

## 证据三（A 级）：PDF 前 3 页原文片段

以下英文原句均由 `pdftotext -layout -enc UTF-8 -f N -l N` 抽自 PDF 文字层，逐字照录；中文对照只为核对用。

| 页 | 英文原句（PDF 文字层原文） | 中文对照 |
|---|---|---|
| 1 | `Introduction to Algorithms  6.006 Spring 2020` | 算法导论，6.006，2020 春季学期 |
| 1 | `Massachusetts Institute of Technology  Solution: Final` | 麻省理工学院，**解答：期末考** |
| 1 | `Instructors: Erik Demaine, Jason Ku, and Justin Solomon` | 授课教师：Erik Demaine、Jason Ku、Justin Solomon |
| 1 | `You have 180 minutes to earn a maximum of 180 points.` | 你有 180 分钟，满分 180 分。 |
| 1 | `If you need more space, write "Continued on S1" (or S2, S3, S4, S5, S6, S7)` | 若需更多空间，写 "Continued on S1"（或 S2–S7） |
| 1 | `Problem  Parts Points` / `2: Decision Problems 10 40` / `10: A Feast for Crowns 1 18` / `Total  180` | 计分表：共 10 题，合计 180 分（第 2 题 10 个小题 40 分，第 10 题 18 分） |
| 2 | `Problem 1. [2 points] Information (2 parts)` | 第 1 题［2 分］信息（2 小题） |
| 2 | `(a) [1 point] Write your name and email address on the cover page.  Solution: OK!` | (a)［1 分］在封面写上姓名与邮箱。解答：OK！ |
| 3 | `Problem 2. [40 points] Decision Problems (10 parts)` | 第 2 题［40 分］判定问题（10 小题） |
| 3 | `For each of the following questions, circle either T (True) or F (False), and briefly justify your answer in the box provided` | 对下列各问圈选 T（真）或 F（假），并在方框内简述理由 |
| 3 | `(a) T F  2^{2n} ∈ Θ(2^n).` / `Solution: False. This statement is equivalent to saying k^2 ∈ O(k) for k = 2^n. Constants in exponents matter asymptotically!` | (a) $2^{2n} \in \Theta(2^n)$。解答：假。该命题等价于「取 $k = 2^n$ 时有 $k^2 \in O(k)$」。指数上的常数在渐近意义上是要紧的！ |
| 3 | `Solution: False. This is an example of Case II of Master Theorem, since a = 4/9, b = 3/2, f(n) = n^2 …` | 解答：假。这是主定理（Master Theorem）情形 II 的例子：$a = 4/9$，$b = 3/2$，$f(n) = n^2$，于是 $T(n) = \Theta(n^2 \log n)$，不是 $O(n^2)$。 |
| 3 | `(c) T F  Performing an O(1) amortized operation n times on an initially empty data structure takes worst-case O(n) time.` / `Solution: True. This is the definition of amortization.` | (c) 对一个初始为空的数据结构执行 $n$ 次 amortized $O(1)$（摊还常数时间）的操作，最坏情况耗时 $O(n)$。解答：真。这就是 amortization（摊还分析）的定义。 |

> **译注（文字层丢上标）**：第 3 页 (a)(b) 两小题的公式在 PDF 文字层里被压平（$2^{2n}$ 抽成 `22n`，$2^n$ 抽成 `2n`，$(3/2)n$ 抽成 `3 � 2 n`）。上表已按课程上下文与主定理（Master Theorem）的标准形式还原；还原结果属于译注级重建，不是文字层原文。

## 证据四（B 级）：md 正文与这份 PDF 一一对应

| 检查项 | 结果 |
|---|---|
| PDF 总页数 | 21（`pdfinfo`） |
| `6.006_EX2.md` 的页标记 | 15 个 `## 第 N 页`，最后一个为第 21 页 |
| md 第 1 页的计分表 | 10 题、180 分、第 2 题 10 小题 40 分，与 PDF 第 1 页逐项相同 |
| md 第 3 页起的判断题 | 题号 (a)–(j)、每题「解答：False/True + 理由」，与 PDF 第 3–6 页对应 |
| 全文出现 "Review" 的次数 | **1** 次，位置：第 1 行标题；正文 0 次 |

正文既没有 review session（复习课）的题目清单，也没有「把已考内容重讲一遍」的结构——它就是一份逐题解答的答案册。**「Final Exam Review 1」这个副标题在正文里没有任何支撑。**

## 结论

1. `6.006_EX2.pdf` = OCW `MIT6_006S20_final_sol.pdf`，字节级相同（A 级）。
2. 该 PDF 的身份 = **6.006 Spring 2020 的 Final 官方解答**，21 页，10 道题共 180 分（A 级：PDF 元数据 + 第 1 页正文）。
3. `6.006_EX2.md` 的正文忠实于这份 PDF（B 级：页数与题项对照）。
4. 所以「它是 Final 的官方解答还是 Final 的 Review 课材料」这个二选一里，答案是**官方解答**，且**不是** Review 材料。

## 建议：只改标题，不重译

**改什么**（一处，第 1 行）：

```text
现在：# 6.006 Introduction to Algorithms · Exams 2 双语译注（Final Exam Review 1）
建议：# 6.006 Introduction to Algorithms · Exams 2 双语译注（Solution: Final 期末考官方解答）
```

**为什么不重译**：

1. 正文与 PDF 逐页对齐、页数覆盖完整（21/21），题目分值、题号、解答结构都在，重译不会带来新信息。
2. 真正的问题不在「译得对不对」，而在标题里那三个英文词——改一行就解决，重译是拿几十倍成本换零收益。
3. 重译还会把现有的术语瑕疵原样再犯一遍（见下条），等于白做。

**另有一件独立的事（不属本次判定，交后续审稿）**：

`6.006_EX2.md` 的术语是「首现加注、之后裸用」的旧规范，并且夹着少量「中文（English）」倒挂与破折号解释式写法，例如「merge sort（归并排序）」之后裸用 `merge`、「directed acyclic graph——即不含任何有向环的有向图」。这与现行铁律 3（术语 `English（中文）`、**每次出现都带括号**）不符，也与同目录 `6.006_EX14.md` 第 5–9 页的现行写法不一致。这需要一次术语规范化审稿，不是重译。

**若真有「Final Exam Review」材料**（例如 6.006 期末复习课的视频或讲义），那是**另一个**待译对象，不应借用 `6.006_EX2` 这个编号与这份 PDF 的位置。本判定未检索 OCW 是否存在这类材料——这一句属于**未经检验的结论**，需要时另行核实。

---

## 复现命令

```bash
# 1) 本机 PDF 的 MD5 与字节数
md5sum "D:/gh-publish/算法导论 6.006/04-题目/考试/6.006_EX2.pdf"
# 2) 重新下载 OCW 原件并比对（逐字节，不是只比摘要）
curl -sSL -o ocw_final_sol.pdf \
  "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/e882f34a3f46aa9862953616f6de1c57_MIT6_006S20_final_sol.pdf"
md5sum ocw_final_sol.pdf
cmp -s ocw_final_sol.pdf "D:/gh-publish/算法导论 6.006/04-题目/考试/6.006_EX2.pdf" && echo IDENTICAL-BYTES
# 3) PDF 自述身份与前 3 页文字层
pdfinfo "D:/gh-publish/算法导论 6.006/04-题目/考试/6.006_EX2.pdf" | grep -E "^Title|^Pages"
pdftotext -layout -enc UTF-8 -f 1 -l 3 "D:/gh-publish/算法导论 6.006/04-题目/考试/6.006_EX2.pdf" -
# 4) md 里 "Review" 只出现一次（标题）
grep -c "Review" "D:/gh-publish/算法导论 6.006/04-题目/考试/6.006_EX2.md"
```
