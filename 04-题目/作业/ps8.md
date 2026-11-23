<!-- page 1/3 -->
# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Set 8（习题集 8）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Set 8 Questions（习题集 8 题卷）· 主题：Dynamic Programming（动态规划）· 对应 Lecture 15 之后的 DP 内容与 CLRS 第 15 章（动态规划）</span>

---

**Problem Set 8（习题集 8）**

请在提供的 LATEX（排版系统）template（模板）中写出你的解答。追求 concise（简洁）的解答；convoluted and obtuse（复杂晦涩）的描述即使正确也可能得低分。本次没有需要提交的 coding（编程）部分。

请用 dynamic programming（动态规划）求解下列每一个问题。对每个问题，务必：定义一组 subproblems（子问题）、递归地建立 subproblem（子问题）之间的 relate（关系）、论证该 relation（关系）是 acyclic（无环）的、给出 base cases（基本情况）、由 subproblems（子问题）构造出原问题的解、并分析 running time（运行时间）。正确但低效的 dynamic program（动态规划）会获得可观的 partial credit（部分分）。

对下面每个问题，请标出所要求的 running time（运行时间）属于哪一种：(1) polynomial（多项式）、(2) pseudopolynomial（伪多项式）、(3) 关于 input size（输入规模）的 exponential（指数）。这项 categorization（分类）每题值 3 分。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 整卷四题共享同一条隐藏考点：running time（运行时间）的 "polynomial（多项式）" 只在一种口径下有意义，就是**关于输入的编码长度**，而不是关于输入里出现的那些数值本身。这条口径决定了本卷每题最后那 3 分怎么拿。
>
> 先把两种口径摆清楚。输入是一个 bit string（位串），它的长度记作 $L$；算法在 RAM（随机存取机）上跑的步数记作 $T(L)$。说 $T$ 是 polynomial（多项式）的，意思是存在常数 $k$ 使 $T(L) = O(L^k)$。麻烦在于题目里的参数有两种身份：$n$ 是"有多少个东西"，编码长度约 $\log n$ 位；$m$ 是"多大一个数"，编码长度约 $\log m$ 位。一个耗时 $O(nm)$ 的 program（程序）对 $n$、$m$ 都是多项式，但对 $L$ 是 $O(2^{L})$ 量级 —— 因为它把 $m$ 的**数值**当成了循环上界。
>
> 三类标签的判据因此钉死：polynomial（多项式）要求 $T = O(L^k)$，例 8-2 的 $O(n^3)$；pseudopolynomial（伪多项式）要求 $T$ 关于数值多项式、关于 $L$ 指数，例 8-1 的 $O(nm)$ 与 8-3 的 $O(m^3 n)$；exponential（指数）要求连数值口径也救不回来，典型是枚举 $2^n$ 个子集。8-4 属于容易被误判的一类：它写作 $O(m^3 n)$，看似与 8-3 同形，但输入里明写着 $O(m^2 n)$ 份、每份至多 $m$ 个字符的日志，字符总数本身就已达 $O(m^3 n)$，所以这个上界关于 $L$ 是线性的，属 polynomial（多项式）。
>
> 数量级差多少，用一组数看清。取 $n = 100$、$m = 10^3$，则 $nm = 10^5$ 步，而 $m$ 只占约 $\log_2 10^3 \approx 9.97$ 位；把 $m$ 抬到 $10^6$（编码只多约 $10$ 位），步数立刻变成 $10^8$，涨了 $1000$ 倍。位数加十、工作量涨千倍 —— 这就是 pseudopolynomial（伪多项式）这个标签要提醒的事：它在小 $m$ 上跑得像多项式，在 $m$ 的位数上是指数。
>
> 跨课程连接：6.042J 的 asymptotic notation（渐进记号）一节给了 $O(\cdot)$ 的严格定义，那里自变量默认是"问题规模"，本卷把"规模"具体化成 bit length（位长），两者是同一套符号的两种代入方式。CLRS 第 34 章讲 NP-completeness（即 NP 完全性），其中 subset sum（子集和）的 $O(nW)$ 动态规划就是伪多项式的标准例子：$W$ 是数值，编码只要 $\log W$ 位，所以那个动态规划并不证明 subset sum（子集和）属于 polynomial（多项式）可解。CSAPP 第 2 章的 integer representation（整数表示）解释了为什么"位数"才是真实成本：一个 `int` 固定占 4 字节、32 位，硬件不会因为数值小就少读几位，算法层面的位数记账与硬件层面的字长在这里是同一件事。
>
> 落到做法上：每写完一题的 running time（运行时间），先问一句"我的循环上界里有没有哪个变量是数值、而它的编码只有对数位"。有，就标 pseudopolynomial（伪多项式）；没有，才考虑 polynomial（多项式）。8-4 还要多问一句"输入里已经明写了多少字符"——上界被输入自身的大小兜住时，标签会从伪多项式翻成多项式。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-1. Oil Well that Ends Well（善始善终的油井）</span>

大亨 Ron Jockefeller（罗恩·洛克菲勒）的 oil wells（油井）本月将产出 $m$ 桶石油。Ron 手里有一份来自潜在买家的 $n$ 张 order（订单）的清单，其中第 $i$ 张 order（订单）表示买家愿意买 $a_i$ 桶，总价为 $p_i$（不是每桶单价），这个总价可能为负。<sup>1</sup> 每张 order（订单）必须整单完成，否则完全不完成，并且每张 order（订单）只能被完成一次。Ron 不必卖掉他全部的石油，但每桶未售出的石油他要付 $s$ 美元的 storage cost（存储成本）。请描述一个 $O(nm)$ 时间的 algorithm（算法），用来确定要完成哪些 order（订单），使得 Ron 的 profit（利润，可能为负）最大化。

> <sup>1</sup> 今年早些时候，oil futures contract（石油期货合约）的价格变成了负数：人们在付钱以求**不**接收石油的交割，因为石油的需求大幅下降，而能储存石油的地方不够用了。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-2. Splits Bowling（分裂保龄球）</span>

在 Lecture 15 中，我们引入了 Bowling（保龄球）：这是一个单人游戏，在一列 $n$ 个 pin（球瓶）上进行，其中第 $i$ 个 pin（球瓶）的取值为整数 $v_i$（可能为负）。玩家反复用两种方式击倒 pin（球瓶）：

- 击倒单个 pin（球瓶），得 $v_i$ 分；或者
- 击倒相邻的两个 pin（球瓶）$i$ 与 $i + 1$，得 $v_i \cdot v_{i+1}$ 分。

pin（球瓶）至多被击倒一次，不过玩家可以选择不击倒某些 pin（球瓶）。Bowling（保龄球）的一个变体 Split Bowling（分裂保龄球）增加了第三种击倒两个 pin（球瓶）的方式，也就是让这两个 pin（球瓶）构成一个 split（分裂），具体是：

- 若两个 pin（球瓶）$i$ 与 $j > i + 1$ 之间的所有 pin（球瓶）$\{i + 1, \ldots, j - 1\}$ 在此之前已被击倒，则可以击倒这两个 pin（球瓶）$i$ 与 $j$，得 $v_i \cdot v_j$ 分。

请描述一个 $O(n^3)$ 时间的 algorithm（算法），对给定的 $n$ 个 pin（球瓶）的输入序列，确定玩 Split Bowling（分裂保龄球）所能取得的 maximum score（最高得分）。

---

<!-- page 2/3 -->
### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-3. Quarter Partition（四等分划分）</span>

给定一个 set（集合）$A = \{a_0, \ldots, a_{n-1}\}$，它包含 $n$ 个互不相同的正整数，令 $m = \sum_{a_i \in A} a_i$，请描述一个 $O(m^3 n)$ 时间的 algorithm（算法），返回 $A$ 的一个 partition（划分）：把 $A$ 分成四个 subset（子集）$A_1, A_2, A_3, A_4 \subseteq A$（其中 $A_1 \sqcup A_2 \sqcup A_3 \sqcup A_4 = A$，符号 $\sqcup$ 表示互不相交的并），使得它们各自的和之中最大的那个尽可能小，也就是使下面这个量最小化：

```math
\max\Big\{\sum_{a_i \in A_j} a_i \ \Big|\ j \in \{1, 2, 3, 4\}\Big\}
```

> 〔原抽取串：`A1  A2  A3  A4 n= A` 与 `max aiAj ai | j  {1, 2, 3, 4}`；`n=` 是 `⊔=`（或 `∪̇ =`，即 disjoint union（互不相交的并））的错位抽取，`aiAj` 是 $\sum_{a_i \in A_j}$ 的碎片，包含符号 `⊆`、求和号 $\sum$ 与花括号均丢失，此处按 partition（划分）的数学含义重建〕

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 8-4. Corrupt Chronicles（损坏的航海日志）</span>

Kimmy Jerk（金米·杰克）是 USS Exitcost（「出局成本」号）的 captain（舰长），这艘 starship（星际飞船）的任务是探索新的世界。每天，Capt. Jerk（杰克舰长）都要往飞船的计算机上传一份 captain's log（舰长日志）：一个由至多 $m$ 个小写英文字母与空格构成的 string（字符串），其中日志里的一个 word（词）指的是任何不包含空格的 maximal substring（极大子串）。

有一天，Capt. Jerk（杰克舰长）被绑架了，communications officer（通信官）Uhota Nyura（乌霍塔·纽拉）去翻 captain's log（舰长日志）寻找证据。不幸的是，日志上传系统出了故障，它把最近 $n$ 份 log（日志）里的所有空格都丢掉了，从而损坏了每一份 log（日志）。Nyura 军官希望依据 Capt. Jerk（杰克舰长）在以往 log（日志）中表现出的 speech patterns（说话习惯）来复原这些空格。给定一个由这 $n$ 份 corrupted logs（损坏日志）构成的 list（列表）$L_c$，以及一个由故障发生前的 $O(m^2 n)$ 份 uncorrupted logs（未损坏日志）构成的 list（列表）$L_u$，Nyura 军官想要：

- 对出现在 $L_u$ 中任何一份 log（日志）里的每个 word（词）$w$，计算 $f(w)$：即 word（词）$w$ 在 $L_u$ 中出现的次数，这是一个正整数（注意，对任何不出现在 $L_u$ 中的 word（词）$w$，$f(w)$ 为零）；并且
- 对每份 log（日志）$\ell_i \in L_c$，返回 $\ell_i$ 的一个 restoration（复原）$R_i$（也就是一个由 word（词）构成的 sequence（序列）$R_i$，其按序 concatenation（拼接）等于 $\ell_i$），使得 $\sum_{w \in R_i} f(w)$ 在所有可能的 restoration（复原）中最大。

请描述一个 $O(m^3 n)$ 时间的 algorithm（算法），依据上述 protocol（协议）复原 Capt. Jerk（杰克舰长）的 log（日志）。

---

<!-- page 3/3 -->
> <span style="color:#7f8c8d;">MIT OpenCourseWare · 6.006 Introduction to Algorithms, Spring 2020 · https://ocw.mit.edu · 引用本材料或使用条款的信息见 https://ocw.mit.edu/terms</span>
