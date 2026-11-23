# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Set 8（习题集 8）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Set 8（习题集 8 题卷）· 主题：Dynamic Programming（动态规划）· 对应 Lecture 15 前后的 DP 内容与 CLRS §15</span>

---

**Problem Set 8（习题集 8）**

请在提供的 LATEX（排版系统）template（模板）中写出你的解答。追求 concise（简洁）的解答；convoluted and obtuse（复杂晦涩）的描述即使正确也可能得低分。本次没有需要提交的 coding（编程）部分。

请用 dynamic programming（动态规划）求解下列每一个问题。对每个问题，务必：定义一组 subproblems（子问题）、递归地建立子问题之间的 relate（关系）、论证该关系是 acyclic（无环）的、给出 base cases（基本情况）、由子问题构造出原问题的解、并分析 running time（运行时间）。正确但低效的动态规划会获得可观的 partial credit（部分分）。

对下面每个问题，请标出所要求的 running time（运行时间）属于哪一种：(1) polynomial（多项式）、(2) pseudopolynomial（伪多项式）、(3) 关于 input size（输入规模）的 exponential（指数）。这项分类每题值 3 分。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-1. Oil Well that Ends Well（善始善终的油井）</span>

大亨 Ron Jockefeller（罗恩·洛克菲勒）的 oil wells（油井）本月将产出 $m$ 桶石油。Ron 手里有一份来自潜在买家的 $n$ 张订单的清单，其中第 $i$ 张订单表示买家愿意买 $a_i$ 桶，总价为 $p_i$（不是每桶单价），这个总价可能为负。<sup>1</sup> 每张订单必须整单完成，否则完全不完成，并且每张订单只能被完成一次。Ron 不必卖掉他全部的石油，但每桶未售出的石油他要付 $s$ 美元的 storage costs（存储成本）。请描述一个 $O(nm)$ 时间的 algorithm（算法），用来确定要完成哪些订单，使得 Ron 的 profit（利润，可能为负）最大化。

> <sup>1</sup> 今年早些时候，oil futures contract（石油期货合约）的价格变成了负数：人们在付钱以求**不**接收石油的交割，因为石油的需求大幅下降，而能储存石油的地方不够用了。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-2. Splits Bowling（分裂保龄球）</span>

在 Lecture 15 中，我们引入了 Bowling（保龄球）：这是一个单人游戏，在一列 $n$ 个 pins（球瓶）上进行，其中第 $i$ 个球瓶的取值为整数 $v_i$（可能为负）。玩家反复用两种方式击倒球瓶：

- 击倒单个球瓶，得 $v_i$ 分；或者
- 击倒相邻的两个球瓶 $i$ 与 $i + 1$，得 $v_i \cdot v_{i+1}$ 分。

球瓶至多被击倒一次，不过玩家可以选择不击倒某些球瓶。Bowling（保龄球）的一个变体 Split Bowling（分裂保龄球）增加了第三种击倒两个球瓶的方式，也就是让这两个球瓶构成一个 split（分裂），具体是：

- 若两个球瓶 $i$ 与 $j > i + 1$ 之间的所有球瓶 $\{i + 1, \ldots, j - 1\}$ 在此之前已被击倒，则可以击倒这两个球瓶 $i$ 与 $j$，得 $v_i \cdot v_j$ 分。

请描述一个 $O(n^3)$ 时间的 algorithm（算法），对给定的 $n$ 个球瓶的输入序列，确定玩 Split Bowling（分裂保龄球）所能取得的 maximum score（最高得分）。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-3. Quarter Partition（四等分划分）</span>

给定一个集合 $A = \{a_0, \ldots, a_{n-1}\}$，它包含 $n$ 个互不相同的正整数，令 $m = \sum_{a_i \in A} a_i$，请描述一个 $O(m^3 n)$ 时间的 algorithm（算法），返回 $A$ 的一个 partition（划分）：把 $A$ 分成四个 subsets（子集）$A_1, A_2, A_3, A_4 \subseteq A$（其中 $A_1 \sqcup A_2 \sqcup A_3 \sqcup A_4 = A$，$\sqcup$ 表示互不相交的并），使得它们各自的和之中最大的那个尽可能小，也就是使
$$\max\Big\{\sum_{a_i \in A_j} a_i \ \Big|\ j \in \{1, 2, 3, 4\}\Big\}$$
最小化。

> 〔原抽取串：`A1  A2  A3  A4 n= A` 与 `max aiAj ai | j  {1, 2, 3, 4}`；`n=` 为 `⊔=`（或 `∪̇ =`，disjoint union）的错位抽取，`aiAj` 为 $\sum_{a_i \in A_j}$ 的碎片，集合包含符号 `⊆`、求和号 $\sum$ 与花括号均丢失，此处按 partition（划分）的数学含义重建〕

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-4. Corrupt Chronicles（损坏的航海日志）</span>

Kimmy Jerk（金米·杰克）是 USS Exitcost（「出局成本」号）的舰长，这艘 starship（星际飞船）的任务是探索新的世界。每天，Jerk 舰长都要往飞船的计算机上传一份 captain's log（舰长日志）：一个由至多 $m$ 个小写英文字母与空格构成的 string（字符串），其中日志里的一个 word（词）指的是任何不包含空格的 maximal substring（极大子串）。

有一天，Jerk 舰长被绑架了，communications officer（通信官）Uhota Nyura（乌霍塔·纽拉）去翻舰长日志寻找证据。不幸的是，日志上传系统出了故障，它把最近 $n$ 份日志里的所有空格都丢掉了，从而损坏了每一份日志。Nyura 军官希望依据 Jerk 舰长在以往日志中表现出的 speech patterns（说话习惯）来复原这些空格。给定一个由这 $n$ 份 corrupted logs（损坏日志）构成的列表 $L_c$，以及一个由故障发生前的 $O(m^2 n)$ 份 uncorrupted logs（未损坏日志）构成的列表 $L_u$，Nyura 军官想要：

- 对出现在 $L_u$ 中任何一份日志里的每个 word（词）$w$，计算 $f(w)$：即 word（词）$w$ 在 $L_u$ 中出现的次数，这是一个正整数（注意，对任何不出现在 $L_u$ 中的 word（词）$w$，$f(w)$ 为零）；并且
- 对每份日志 $\ell_i \in L_c$，返回 $\ell_i$ 的一个 restoration（复原）$R_i$（也就是一个由 word（词）构成的序列 $R_i$，其按序 concatenation（拼接）等于 $\ell_i$），使得 $\sum_{w \in R_i} f(w)$ 在所有可能的 restoration（复原）中最大。

请描述一个 $O(m^3 n)$ 时间的 algorithm（算法），依据上述协议复原 Jerk 舰长的日志。

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare · 6.006 Introduction to Algorithms, Spring 2020 · https://ocw.mit.edu · 引用本材料或使用条款的信息见 https://ocw.mit.edu/terms</span>
