# Introduction to Algorithms: 6.006

## <span style="color:#2471a3;">**[lecture]**</span> <span style="color:#c0392b">Lecture 19: Complexity（复杂度——决策问题、可判定性与 P/NP/EXP）</span>

Massachusetts Institute of Technology
Instructors: Erik Demaine, Jason Ku, and Justin Solomon

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Lecture 19 讲义（对应视频：Complexity）——动态规划四讲（L16-L18）之后的独立收束讲：从"怎么设计快算法"转向"哪些问题根本不可能有快算法"。</span>

🎥 *Demaine 开场如此定位本讲*："Today we're going to, in one lecture, cover an entire field, which is computational complexity... algorithms is mostly about showing how to solve problems well... And computational complexity is more about the lower bound side, proving that you can't solve a problem very well."（翻译：今天我们要用一节课覆盖一整个领域——computational complexity（计算复杂性）。算法课主要是展示如何把问题解决好；而计算复杂性更关心下界那一侧——证明你没法把某个问题解得很好。）

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Decision Problems（决策问题）</span>

- **Decision problem（决策问题）**：把每个 input（输入）指派为 YES（是，记 $1$）或 NO（否，记 $0$）的任务
- 每个输入要么是 NO input（NO 输入），要么是 YES input（YES 输入）

| Problem | Decision（对应决策） |
|---------|---------------------|
| **s-t Shortest Path**（$s$-$t$ 最短路径） | 给定 $G$ 中是否存在一条从 $s$ 到 $t$、weight（权重）至多为 $d$ 的 path（路径）？ |
| **Negative Cycle**（负环） | 给定 $G$ 中是否存在一个 negative weight cycle（负权环）？ |
| **Longest Simple Path**（最长简单路径） | 给定 $G$ 中是否存在一条 weight 至少为 $d$ 的 simple path（简单路径）？ |
| **Subset Sum**（子集和） | 给定整数集合 $A$，是否存在一个 sum（和）为 $S$ 的 subset（子集）？ |
| **Tetris**（俄罗斯方块） | 给定 board（游戏板）与方块出现序列，能否逐一放置 pieces（方块）坚持到序列结束而不堆顶？ |
| **Chess**（国际象棋） | 在给定局面中，某方能否 forced win（逼出胜局）？ |
| **Halting problem**（停机问题） | 给定 computer program（计算机程序）对给定输入是否会终止？ |

![图 1-1：七个问题及其决策版本的对照表（原书排版）](_assets/lec19_fig_1_1.png)

**图 1-1**：七行里只有前两行（s-t Shortest Path、Negative Cycle）的决策版属于 P；第三行 Longest Simple Path 与第一行只差 `simple` 一词，判定就从多项式可解跳到 NP-complete；最后一行 Halting problem 连 decidability 都没有 —— 这张表的七行恰好横跨 P、NP-complete、EXP-complete、undecidable 四个层级。*Adding the word `simple` moves shortest path out of P, and the bottom row is not even decidable: seven rows span four complexity levels.*

- **Algorithm/Program（算法/程序）**：一段 constant-length code（定长代码）——运行在 word size 为 $\Omega(\log n)$ bits 的 word-RAM 上——用来求解某个问题；即它对**每一个**输入都产生正确输出，且代码的长度与实例大小无关
- 若存在某个 program 能在 finite time（有限时间）内求解该问题，则称该问题是 **decidable（可判定的）**

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注要回答的设计问题是：整个 complexity theory（计算复杂性理论）为什么把舞台收缩到 **decision problem（决策问题）** 上，却不因此丢掉 optimization problem（优化问题）的难度？答案不是「图省事」，而是一条可证明的等价：在 polynomial time（多项式时间）归约下，一个优化问题与它的 decision version（判定版本）难度相同。这条等价一旦立住，后面关于 NP 与 NP-complete 的全部难度分层才有一个共同的坐标系。
>
> 机制要从「输出是什么」问起。任何程序能吐出来的东西都是一串有限 bit；既然答案是一串 bit，那么「求答案」就可以拆成「逐位问」——把「第 $k$ 位是 1 吗」当成一次独立的一问。若答案的 bit 长度是 $\mathrm{poly}(n)$，那么 $\mathrm{poly}(n)$ 次判定查询就足以逐位把答案拼回来，这就是 self-reducibility（自归约）。反方向是平凡的：判定版是优化版的特例，只问「有没有不超过阈值 $d$ 的解」。两个方向合起来，优化版与判定版互相归约，落在同一个 polynomial time（多项式时间）等价类里。NP 只对判定版定义还有一层技术原因：verifier（验证器）的 certificate（证书）必须是有限串，而优化版的最优解常常「有无穷多个同样好的解」，量化结构写不干净；压成「是/否」，存在量词与全称量词才各就各位。
>
> 把代价算一遍。设图有 $n = 10000$ 个顶点、$m = 50000$ 条边，权重取 $1$ 到 $1000$ 的整数。任何 simple path（简单路径）至多 $9999$ 条边，所以 $s$ 到 $t$ 的距离不超过 $9999 \times 1000 \approx 10^{7}$。对阈值 $d$ 做二分，需要 $\lceil \log_2 10^{7} \rceil = 24$ 次判定。每次判定跑一遍 Dijkstra 并在距离超过 $d$ 时剪枝，约 $m \log n = 50000 \times 14 \approx 7 \times 10^{5}$ 次基本操作；$24$ 次合计约 $1.7 \times 10^{7}$ 次，而一次完整 Dijkstra 只要 $7 \times 10^{5}$ 次——开销正好 $24$ 倍，也就是值域的 log 倍。若精度从整数换成 $\varepsilon = 0.001$ 的实数，次数变成 $\log_2 10^{10} \approx 34$ 次，仍然是多项式。这个 $24$ 与 $34$ 就是判定查询的账单：它只取决于答案有多少 bit，不取决于问题本身有多难。
>
> 跨课程连接：CLRS 第 34 章 §34.1 干的是同一件事，但它把「优化转判定」写成三条约定（对应该节开头几道练习），并强调这是 formal-language framework（形式语言框架）的入口：一个 problem（问题）就是一个 language（语言），也就是全体 YES input（YES 输入）构成的串集合。区别在关注点：CLRS 更在意「怎么把具体问题写成语言」以便后面写归约，本讲更在意「判定版是否忠实承载难度」这个前提本身。再往前接 6.042J：那里「函数 $f: A \to B$」与「关系 $R \subseteq A \times B$」是同一种对象的两种写法，判定问题只是把陪域取成 $\{0,1\}$ 的那种函数——把答案压到两个元素，等价于把集合隶属写成布尔函数。区别在追问的层次：6.042J 只问「这样的函数存不存在」，复杂度理论还要问「它能不能在 $\mathrm{poly}(n)$ 步内被算出来」，后者才是全部难度的来源。
>
> 所以 L0036 说的「升格」不是术语搬家，而是一次坐标变换：把「求最优值」换成「问阈值」，难度不变而量化结构变干净，NP 的「存在一条短证书」才有地方写。附带一个容易忽略的推论：既然查询次数只与答案长度有关，一个优化问题只要答案是多项式位长，它的判定版与优化版就落在同一个难度类里——这也解释了为什么后面所有 hardness（难度）证明都只需要对判定版做。

> 注意表格里最后三个问题（Tetris、Chess、Halting）故意**不是**来自算法课，而是来自现实游戏与逻辑：它们把"计算"从数组、图扩展到方块、棋盘与任意程序。表格的对角线信息是——**问题越"自由"，求解越难**：最短路径（受限的图结构）易解，Chess（几乎无结构的棋盘状态空间）极难，Halting（对任意程序推理）不可判定。直觉上，一个问题的输入**结构越丰富**（图、数组、网格），越容易找到高效算法；输入越"混沌"（任意代码、任意局面），越难。本讲后面会把这个直觉精确化：**结构 = 可归约性（reducibility）**。
>
> 逐行读这张表还能得到一张"难度光谱预览"：s-t Shortest Path 是 P 的（Dijkstra，本课已证）；Negative Cycle 是 P 的（Bellman-Ford 或 Floyd-Warshall 检测负环，L12/L14）；Longest Simple Path 是 NP-complete 的（第 4 页正式登场）——注意它与 Shortest Path 只有 simple 一词之差，却从易解跳到极难；Subset Sum 是 weakly NP-complete 的（L18 的伪多项式 DP 是它最后的温柔）；Tetris 是 NP-complete 的（判定版为"给定方块序列能否活下来"，Breukelaar–Demaine–Hohenberger 等 2003/2004 年证明，见 "Tetris is Hard, Even to Approximate"）；Chess 是 EXP-complete 的——注意是推广到 $n \times n$ 棋盘才算 EXP-complete，普通 8×8 棋盘是常数规模、理论上可蛮力穷举；Halting 根本**不可判定**——连"给够时间总能算完"都做不到。从 P 一路滑到不可判定，这张表就是本讲后三页内容的缩略地图，建议学完本讲后回来看一眼这张表，逐个确认每个问题的最终归属。
>
> 讲义里 "Algorithm = constant-length code（定长代码）"这个限定也值得停下来想一层：为什么要求**代码长度与实例无关**？因为在可判定性论证里，程序要能被"枚举"——如果允许程序随实例变长（比如把整个输入硬编码进程序），那么"每个输入配一个专属程序"会让"程序可数"的论证崩塌——输入（无穷 bit 串）不可数，而"输入 → 专属程序"的映射会把不可数多个输入映射成不可数多个求解器，计数论证随即失效。定长代码保证**一份代码处理无穷多个输入**，这才是"算法"的本义。而 decidable（可判定）的定义——"存在程序在有限时间内求解"——注意它**不要求时间上界**：跑 $2^{2^n}$ 年也算 decidable。这与你习惯的"高效"（polynomial time）是两回事：decidable 只管"能不能算完"，P/EXP 才管"算多久"。本讲接下来的路线就是逐级加资源约束，按"集合从小到大"排列为 $P \subseteq NP \subseteq EXP \subsetneq R$：P（多项式内算完）⊆ NP（证书可在多项式内验证）⊆ EXP（指数内算完）⊊ R（有限时间内算完）。注意方向：**P 是 NP 的子集**（能快解 ⟹ 能快验证），NP 又含于 EXP，R 最大——资源预算逐级放宽。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Decidability（可判定性）</span>

- 每个 program 都是一段 finite（有限的）、定长的 bit（比特）串，即一个非负整数 $\in \mathbb{N}$
- 每个 problem 是一个函数 $p : \mathbb{N} \to \{0, 1\}$，即一个 infinite（无穷的）bit 串
- （program 的个数 $\mathbb{N}$，**countably infinite（可数无穷）**）小于（problem 的个数 $\mathbb{R}$，**uncountably infinite（不可数无穷）**）

🎥 *Demaine 用"无穷的大小不一样"点破这一步的直觉*："There are also infinitely many integers. So that maybe doesn't seem that deep. But there's a difference in infinitude... infinite strings of bits are what's called uncountable. I think the most intuitive way to see this is... if I put a decimal or a binary point in front, this encodes a real number between 0 and 1."（翻译：整数也有无穷多个，所以这看起来也许没什么了不起。但无穷与无穷之间有大小之分……无穷 bit 串被称为不可数无穷。最直观的理解方式是——在无穷 bit 串前面加一个小数点，它就编码了 0 到 1 之间的一个实数。）
- （证明用 Cantor's diagonalization argument（康托对角线论证），6.042 应该讲过）
- 这证明了：**大多数决策问题不能被任何程序求解（即 undecidable，不可判定）**

🎥 *Demaine 称这是本讲最令人吃惊的结论*："One result we'll prove today is that most problems actually have no algorithm, which is kind of shocking."（翻译：我们今天要证明的一个结论是——大多数问题实际上根本没有算法，这有点令人震惊。）
- 例如 Halting problem（停机问题）就不可判定（6.045 里有很多精彩的证明）
- 好在：我们通常思考的大多数问题在结构上都是 algorithmic（算法的），因而是可判定的

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页是全讲最重要的"数数"论证，值得用你在 6.042J 学过的集合基数（cardinality）概念重新走一遍——它本质上是一个 **Pigeonhole Principle（鸽巢原理）**的极限版本：要把不可数多个问题塞进可数个程序里，必然有大量问题没有对应程序。程序是有限 bit 串，全体有限 bit 串可以按长度排成 $\epsilon, 0, 1, 00, 01, \ldots$，与 $\mathbb{N}$ 一一对应——可数无穷。每个问题 $p : \mathbb{N} \to \{0,1\}$ 等价于一个"第 $i$ 位是 $p(i)$"的**无穷 bit 串**；全体无穷 $0/1$ 串的集合与实数集等势（把第 $i$ 位当作 $0.b_1 b_2 b_3 \ldots$ 的二进制小数，即得从无穷串到 $[0,1]$ 的满射；虽因 $0.0111\ldots = 0.1000\ldots$ 之类在可数多处重复而非单射，但等势结论不受影响，$\mathbb{R}$ 仍不可数）。于是"问题比程序多"——程序可数、问题不可数。**Cantor's diagonalization（康托对角线法）**正是你在 6.042J 见过的"实数不可数"证明的同一把刀：假定把全体无穷 $0/1$ 串排成列表，构造一个新串，其第 $i$ 位取反第 $i$ 个串的第 $i$ 位——它不在列表中任何位置，矛盾。这里"第 $i$ 个程序跑在第 $i$ 个输入上并取反其结果"是同一对角线的计算版本，它先给出一个具体的不可判定集合 $K$（第 $i$ 个程序在第 $i$ 个输入上不停机的那些 $i$）；停机问题另有自己的对角论证（见下句 $H$ 与 $D$），两者同源但并非同一证明：若存在程序 $H$ 判定停机，则构造 $D$：输入程序 $P$ 时，若 $H(P, P)$ 说"会停"就死循环、说"不停"就停机——$D(D)$ 无论 $H$ 怎么答都自相矛盾。这是 6.045 的核心内容，本讲只取结论：**对角线法的本质是"自我指涉 + 取反"**，与 6.042J 里证明 $\mathbb{N}$ 与 $\mathbb{R}$ 不等势、以及 Russell's paradox（罗素悖论，即"由所有不属于自身的集合构成的集合"是否属于自身——怎么答都矛盾）用的是同一个思想模板。直觉锚点：**"可数"意味着能逐个枚举（哪怕永不停歇），"不可数"意味着连枚举都做不到**——绝大多数问题是后者，它们连"等待答案"的资格都没有，更遑论多项式时间。
>
> 这个论证里有两个容易滑过的细节值得点出。**细节一：程序为什么能枚举？** "程序是有限 bit 串"不是一句废话——它排除了"程序库"里混入无限长代码的可能，保证了全体程序与自然数同势。所有你写过的 C/Python 程序、所有算法课的伪代码，落盘后都是有限字节串，都在这个可数集合里。**细节二：为什么停机问题"重要"？** 不可判定的问题有无穷多个（大多数问题都不可判定），但停机问题是其中**对人类最有用的一个**——编译器要判断程序是否死循环、操作系统要判断任务是否卡死、静态分析工具要证明程序终止性，全都绕不开它。它不可判定意味着：**不存在一个通用算法能对"所有程序 + 所有输入"判定是否停机**——注意是"通用"，单个具体程序是否停机往往可以人工证明（比如你的循环程序显然会停），难的是一把钥匙开所有锁。这正是"可判定性"研究的现实意义：**知道什么问题根本不可能自动化，与知道什么问题可以自动化，同等重要**——你不会再浪费时间写一个理论上不可能存在的调试器。而本讲接下来关心的是可判定但未必高效的那一层（R）内部——从下一节的 R/EXP/P 开始，问题的问法从「能不能算完」变成「要多少资源才能算完」，复杂度理论的主舞台就此拉开。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Decidable Decision Problems（可判定的决策问题）</span>

- **R**：能在 finite time 内判定的问题（'R' 来自 recursive languages，递归语言）
- **EXP**：能在 exponential time（指数时间）$2^{n^{O(1)}}$ 内判定的问题（**我们日常考虑的大多数问题都在这里**）
- **P**：能在 polynomial time（多项式时间）$n^{O(1)}$ 内判定的问题（efficient algorithms（高效算法），本课焦点）

![图 1-2：R / EXP / P 三个可判定类及其定义（原书排版）](_assets/lec19_fig_1_2.png)

**图 1-2**：EXP 的指数 $2^{n^{O(1)}}$ 与 P 的多项式 $n^{O(1)}$ 用的是**同一个** $O(1)$ 记号 —— 差别只在谁被指数化：$n$ 作底得多项式，$2$ 作底、$n^{O(1)}$ 作指数得指数。因此 $P \subsetneq EXP$ 不是「量」的差别（不是某个常数更大），而是 time hierarchy theorem 保证的严格分层；右列括号注把三个类的用途钉死：EXP 是「日常思考的问题所在」，P 才是本课的目标。*P and EXP share the same $O(1)$ exponent; only the base differs, and the time hierarchy theorem makes the gap strict rather than quantitative.*

🎥 *Demaine 定义 P 与 EXP 时点明本课视角*："P is the set of all problems solvable in polynomial time. OK. So these are the problems that are efficiently solvable. P is set of all of them. And for contrast, EXP is the set of all problems solvable in exponential time. Exponential here means something like 2 to the n to the constant."（翻译：P 是所有能在多项式时间内求解的问题的集合——也就是能被高效求解的那些问题。作为对照，EXP 是所有能在指数时间内求解的问题的集合；这里的指数大致是 $2^{n^{O(1)}}$ 的意思。）
- 这些集合两两不同：$P \subsetneq EXP \subsetneq R$（由 time hierarchy theorems（时间谱系定理）保证，见 6.045）
- 例如 Chess 属于 $EXP \setminus P$

![复杂度类谱系：P ⊆ NP ⊆ EXP ⊊ R ⊊ 全体判定问题（虚线=未证猜想）](assets/lec19-classes-hierarchy.svg)

> <span style="color:#7f8c8d;">类谱系示意（自绘）：P ⊊ NP ⊊ EXP ⊊ R ⊊ 全体判定问题；其中 P ⊊ EXP 与 EXP ⊊ R 已被证明，P ⊊ NP 悬而未决（$P \ne NP$ 仅是普遍猜想）。</span>

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 三层蛋糕回答的不是「哪个问题在哪一层」，而是「资源预算凭什么这样切」。这条注的核心：R、EXP、P 三个边界的形状都由同一个事实决定——候选解的个数是 $2$ 的「答案长度」次方。
>
> 为什么日常问题都落在 EXP？因为任何问题都能用「枚举候选解再加逐个检查」的方式暴力求解。候选解是长度 $\mathrm{poly}(n)$ 的 bit 串，共 $2^{\mathrm{poly}(n)}$ 个；对每个候选跑一个 $\mathrm{poly}(n)$ 时间的检查器，总时间 $2^{\mathrm{poly}(n)} \cdot \mathrm{poly}(n) \subseteq 2^{n^{O(1)}}$。所以「能快速验证」自动蕴含「能在指数时间求解」，这就是 $NP \subseteq EXP$ 的证明，也是 Demaine 说 EXP 装着日常世界的机制原因：不是巧合，是「答案必须是一串有限 bit」这条事实的推论。
>
> 拿 Subset Sum（子集和）数一遍。$n = 50$ 时子集总数 $2^{50} = 1125899906842624 \approx 1.13 \times 10^{15}$。若每秒能检查 $10^{9}$ 个子集（已经很乐观），需要 $1.13 \times 10^{6}$ 秒 $\approx 13$ 天。$n = 60$：$2^{60} \approx 1.15 \times 10^{18}$，需 $1.15 \times 10^{9}$ 秒 $\approx 36.5$ 年。$n = 100$：$2^{100} \approx 1.27 \times 10^{30}$，需 $1.27 \times 10^{21}$ 秒 $\approx 4.0 \times 10^{22}$ 年，而宇宙年龄约 $1.38 \times 10^{10}$ 年，相差 $12$ 个数量级。再看 P 那一侧：$n = 10^{6}$ 时 $n^{2} = 10^{12}$ 次操作，每秒 $10^{9}$ 次只需 $1000$ 秒。输入从 $50$ 涨到 $100$（翻一倍），耗时从 $13$ 天涨到 $4 \times 10^{22}$ 年，涨了 $24$ 个数量级——这种「输入翻倍、代价涨成天文数字」的响应，就是 exponential（指数）的定义性特征，也是渐近分析在这里不是学究气的原因：任何多项式算法与指数算法的交叉点之后，指数永远输，而交叉点可能只有几十。
>
> 跨课程连接：6.042J 的 counting（计数）给这里两件现成工具。一是幂集计数，$X$ 有 $k$ 个元素则子集恰有 $2^{k}$ 个，子集枚举的规模就是这一条的直译。二是二进制表示的位数是 log，而输入规模 $n$ 数的是位数——所以「值 $10^{7}$」在 bit 长度上只有 $24$，这个错位正是后面 weakly NP-complete（弱 NP 完全）与 pseudo-polynomial（伪多项式）那道裂缝的来源。CLRS 第 34 章 §34.1 的类包含链与本讲一致，只是多摆了一层 PSPACE（多项式空间可解的问题）；区别在表述语言：CLRS 用「某台 machine（机器）在 $n^{k}$ 步内判定」的机器模型写法，便于写定理；讲义用「问题集合」的写法，便于建立直觉。
>
> EXP 内部也不是一块铁板。time hierarchy theorem（时间谱系定理）的定量版本说，只要两个预算相差一个 $\log$ 因子以上（严格条件是 $T_2 \log T_2 = o(T_1)$），就能对角化出一个落在两者之间的问题，于是 $n$、$n^{2}$、$n^{7}$ 各自是不同的 time class（时间类），$2^{n}$ 与 $2^{n^{2}}$ 也各自不同，EXP 内部有无穷多级，R 更是一座越往上越高的塔，最高处是 $2^{2^{n}}$、$2^{2^{2^{n}}}$ 这样的双重、三重指数。那 P 为什么看上去扁平？因为它把任意次数的多项式一次性收进来——扁平是取并集的结果，不是谱系定理在那里失灵。而 P 与 EXP 之间那道缝由 NP 占着，NP 究竟把缝填满多少（即 $NP$ 是否真等于 EXP）至今开放，已被钉死的只有两头之一：$P \subsetneq EXP$。这种「类与类的边界不是画上去的、是被谱系定理一级一级分出来的」分辨率意识，才是三层蛋糕真正要教的技术内容——记住它，就不会把「P 在 EXP 里面」误读成「P 只是小一点的 EXP」，两者中间还隔着无穷多级。
>
> 严格性不靠直觉：$P \subsetneq EXP$ 是 Hartmanis–Stearns 1965 的 time hierarchy theorem（时间谱系定理）的推论，证明仍是 diagonalization（对角化），但没有停机问题那么粗糙——先取一个可构造的时间界，造一台机器在输入 $x$ 上模拟第 $|x|$ 台机器、只花 $2^{|x|}$ 步预算就取反，得到的问题落在 EXP 而不在 P。补一句反面对照：同一把刀砍不动 P 与 NP 的分离，原因写在讲 NP 的那条注里。于是三层蛋糕的正确读法是「资源预算的刻度尺」，不是「难度排行榜」——排行榜要等 NP 出场才排得起来。

> 关键论断是**包含关系严格**：$P \subsetneq EXP \subsetneq R$。P ⊊ EXP 与 EXP ⊊ R 都是**已证明的定理**（time hierarchy theorems（时间谱系定理）：给你更多时间，就能严格判定更多问题——证明思路是"给足时间后对角线化"，与上页停机问题的对角线同源，但要用可构造时间函数避开停机陷阱，细节在 6.045）。**注意：P ⊊ EXP 已被证明，但 P ⊊ NP 未被证明**——NP 夹在两者之间，它是不是真的比 P 大、比 EXP 小，就是 $P \stackrel{?}{=} NP$ 这个 open problem（开放问题），下一节会正式展开。**Chess 属于 $EXP \setminus P$ 是确定的定理而非猜想**：Chess（推广到 $n \times n$ 棋盘）已证 EXP-complete，即 EXP 中每个问题都能归约到它；又 $P \subsetneq EXP$ 已被时间谱系定理证明，故 EXP-complete 问题不可能在 P 中（否则 $P = EXP$，矛盾）——这条推论不依赖 $P \ne NP$，与 NP-complete 问题"是否在 P 中悬而未决"的情形形成鲜明对比。复杂度谱系常被画成同心圆（见上配图），记忆口诀：**P 内是"能快解"，EXP 内是"能暴力解"，R 内是"能解"，之外是"永不可解"**。你从 L18 带来的 Subset Sum 此刻有了精确坐标：它在 EXP 内（暴力枚举 $2^n$ 个子集）、确实在 NP 内（证书就是那个凑出目标和的子集 $A'$，验证器 $O(n)$ 求和即可）、若 $P \ne NP$ 则不在 P 内——下两页把 NP 的定义补齐。
>
> 这张谱系图里每个类都能在你已学的问题中找到"代表"：P 的代表满课都是——排序、Dijkstra、Bellman-Ford、Floyd-Warshall、LCS、所有 DP（L15-L18）；EXP 的代表是"暴力搜索版"——枚举所有子集的 Subset Sum、枚举所有顶点排列的 TSP；R 的代表是"任何有限时间算法"——包括那些要跑 $2^{2^n}$ 年的理论算法；R 之外的代表是停机问题。把类想成**资源预算**：P 的预算是最抠门的（多项式步数），EXP 的预算是"指数步数也认了"（$2^{n^{O(1)}}$ 里那个 $O(1)$ 常数可以是 2、3、任意大——所以 EXP 内部还分 $2^n, 2^{n^2}, 2^{n^3}, \ldots$ 无穷层级，时间谱系定理保证它们严格递增），R 的预算是"不限时间但必须停机"（连 $2^{2^n}$ 这样的双重指数也在 R 内，但已不属于 EXP）。**资源越多，能解的问题越多**——这就是时间谱系定理的直观内容，也解释了为什么包含关系是"一层套一层"而不是"互不重叠"：多给资源只会让你解更多，不会让你解更少。
>
> "Chess 是 EXP-complete"，这里有个值得拆开的词：**complete（完全）** 意味着它在 EXP 内部"最难"——EXP 里每个问题都能归约到它。类比 NP-complete：complete 类问题是一类中的"扛把子"，搞定一个就搞定整类。注意讲义对 Chess 的表述（$EXP \setminus P$）与对 Longest Simple Path/Tetris 的表述（"若 NP 中存在问题不属于 P，那么它们也不在 P 中"）语气不同——前者是**确定的**（EXP-complete + $P \subsetneq EXP$ 已证 ⇒ Chess $\notin P$ 无条件成立），后者是**条件性的**（依赖 $P \ne NP$）。这个细微差别值得记住：**凡是依赖 $P \ne NP$ 的结论都要加"若"字**，而依赖时间谱系定理的结论可以理直气壮。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Nondeterministic Polynomial Time（NP，非确定性多项式时间）</span>

- **P** 是满足如下条件的决策问题集合：存在 algorithm $A$，使得对每个 size 为 $n$ 的 input $I$，$A$ 在 $I$ 上运行 $\mathrm{poly}(n)$ 时间并正确求解 $I$

- **NP** 是满足如下条件的决策问题集合：存在一个 **verification algorithm（验证算法）** $V$，它以问题的 input $I$ 和一条长度关于 $I$ 的 size 呈多项式关系的 certificate（证书）bit 串作为输入，使得：

  - $V$ 的运行时间总是关于 $I$ 的 size 呈多项式；
  - 若 $I$ 是 YES input，则存在某个 certificate $c$，使 $V$ 在输入 $(I, c)$ 上输出 YES；
  - 若 $I$ 是 NO input，则无论选哪个 certificate $c$，$V$ 在输入 $(I, c)$ 上总是输出 NO

- 你可以把 certificate 想成"$I$ 是 YES input"的 proof（证明）：若 $I$ 实际上是 NO input，则任何 proof 都不应该奏效

| Problem | Certificate（证书） | Verifier（验证器） |
|---------|----------------------|--------------------|
| **s-t Shortest Path** | 一条从 $s$ 到 $t$ 的 path $P$ | 把 $P$ 上的 weights 加起来，检查是否 $\le d$ |
| **Negative Cycle** | 一个 cycle $C$ | 把 $C$ 上的 weights 加起来，检查是否 $< 0$ |
| **Longest Simple Path** | 一条 path $P$ | 检查 $P$ 是否为 weight $\ge d$ 的 simple path |
| **Subset Sum** | 一个 items 集合 $A'$ | 检查 $A'$ 是否 $\subseteq A$，且其元素和是否为 $S$ |
| **Tetris** | 一串 moves（走法） | 检查这些 moves 是否允许 survival（存活） |

![图 2-1：五个 NP 问题的 certificate 与 verifier 对照表（原书排版）](_assets/lec19_fig_2_1.png)

**图 2-1**：Certificate 一列全部是多项式长度的 witness（一条路径、一个环、一个子集 $A'$、一串 moves），Verifier 一列做的事全部是「求和 + 与阈值比较」或「检查 $\subseteq$ / $\in$」，即 $O(n)$ 到 $O(n^2)$ 的死算，没有一行需要「聪明」。这张表就是 NP 定义 $\exists$ 短证书 $+$ 多项式验证的字面物证；也说明为什么「验证」不构成求解 —— 表格给了答案，验证器只需核对，它并不产生答案。*Every certificate is a polynomial-size witness and every verifier is plain sum-and-compare: the $\exists$ + poly-check definition written out row by row.*

- **$P \subseteq NP$**：verifier $V$ 可以忽略 certificate 直接求解该实例
- **$NP \subseteq EXP$**：把所有可能的 certificates 都试一遍！至多 $2^{n^{O(1)}}$ 个，对每个都运行 verifier $V$
- **Open（未解）**：$P \stackrel{?}{=} NP$？$NP \stackrel{?}{=} EXP$？
- 大多数人认为 $P \subsetneq NP$（而 $NP$ 与 $EXP$ 的关系同样是开放问题），即 **generating（生成）解比 checking（检查）解更难**

🎥 *Demaine 说明这只是猜想而非定理*："People conjecture that P does not equal NP. It's sort of a standard conjecture in theoretical computer science. But we don't know how to prove whether P equals NP or does not equal NP."（翻译：人们猜想 $P \ne NP$。这是理论计算机科学里的一个标准猜想，但我们并不知道如何证明 $P = NP$ 还是 $P \ne NP$。）
- 你若能证明其中任何一个方向，人们会给你很多钱（$1M Millennium Prize（百万美元千禧年大奖））
- **我们为什么关心？** 若能证明某问题是 NP 中最难的问题，则当 $P \ne NP$ 时，该问题不可能在 polynomial time 内求解
- **如何比较问题的难度？Reductions（归约）！**

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> verifier（验证器）定义的价值不在于换一种说法，而在于它把「一个问题有多难」翻译成两个可数的量：YES 证据有多短、查它有多快。这条注把这种翻译提炼成一个可复用的模板，并说明为什么同一个模板推不动 $P$ 与 $NP$ 的分离。
>
> 先把三个条件写成一行逻辑：$I$ 是 YES input（YES 输入）当且仅当存在 $c$，满足 $|c| \le p(|I|)$ 且 $V(I, c)$ 输出 YES。注意「当且仅当」的两半各管一件事：从右到左是 completeness（完备性，真命题有证书），从左到右是 soundness（可靠性，假命题骗不过验证器）。写成逻辑式后 NP 的本质一眼可见：它是一个存在量词加一个多项式谓词。这也解释了为什么 NP 只对判定问题定义——存在量词需要一个「候选物」的论域，而只有判定版的答案是单点，候选物才好写成证书。
>
> 给这套模板起个名字：短证书加快验证。用它证明 membership（隶属）时走三步：① 指认证书的类型（一条路径、一个环、一个子集、一串 moves（走法））；② 算出证书的 bit 长度并证明它是 $\mathrm{poly}(n)$；③ 写验证器并证明它 $\mathrm{poly}(n)$ 且两个方向都对——YES 时存在证书，NO 时任何证书都过不了。用它做 hardness（难度）时也走三步，但方向整个翻过来：① 从已知难问题的实例构造目标问题的实例；② 证明构造只要 $\mathrm{poly}(n)$ 时间；③ 证明答案保持，YES 映 YES、NO 映 NO。两者的区别只在「谁答谁」：membership 证的是「答案短」，hardness 证的是「难度传得过去」；把三步显式写出来，归约证明就不会漏步。
>
> 看一个具体例子。取 $n = 40$ 个 $20$ bit 的整数，输入规模约 $800$ bit。证书是 $40$ bit 的子集指示串——$40$ bit 恰好能区分 $2^{40} \approx 1.1 \times 10^{12}$ 种可能的子集，也就是说证书的信息量正好等于搜索空间的对数。验证器做 $40$ 次加法，每次两个 $20$ bit 数相加，约 $800$ 次 bit 操作。求解侧呢：$2^{40}$ 次检查乘以 $800$ 次 bit 操作 $\approx 8.8 \times 10^{14}$ 次，按每秒 $10^{9}$ 次要 $8.8 \times 10^{5}$ 秒 $\approx 10.2$ 天。两个数并排放：「证书 $40$ bit、验证 $800$ 步」对「穷举 $10$ 天」。这个落差就是 NP 与 P 的全部张力——证据的信息量是搜索空间的对数，而找到它要线性扫过搜索空间。
>
> 为什么五十年推不动？因为对角线法在这里失效，而失效的原因不是技巧不够，是有定理说它不可能。要讲清楚得先引入一个概念：oracle（谕示）是一台「一步就能回答某个问题、不管它多难」的黑盒；配上这种黑盒的图灵机叫 oracle machine（谕示机）；它的用处是检验「一个证明技巧会不会被黑盒搞坏」——若某技巧在有黑盒时推出某个结论，去掉黑盒后就不该得出相反的结论。Baker–Gill–Solovay 1975 证明了：存在一个 oracle $A$ 使 $P^{A} = NP^{A}$，也存在另一个 oracle $B$ 使 $P^{B} \ne NP^{B}$。于是任何 relativizing（可相对化）的证明技巧，也就是在有黑盒时照常成立的技巧，都不可能证明 $P \ne NP$，因为它对 $A$ 与 $B$ 会给出同一个结论，而事实是两个方向各有一个真。对角线法正是可相对化的，所以「像证 $P \subsetneq EXP$ 那样用对角线证 $P \ne NP$」这条路被定理封死。
>
> 后面还有两道同类的墙：Razborov–Rudich 1994 的 natural proofs（自然证明）说明，一大类组合式的电路下界证明若成立，就会顺带造出破解伪随机函数的算法，与密码学的通行假设冲突；Aaronson–Wigderson 2008 的 algebrization（代数化）把封堵扩展到算术化的技巧。三道墙合起来的意思是：$P$ 与 $NP$ 的分离需要的不是更聪明的对角线，而是一类至今没人想到的证明技术。回到讲义：CLRS 第 34 章 §34.2 把 NP 定义为「多项式时间可验证的关系」，与本条的量词写法是同一件事；区别是 CLRS 面向判卷，要求你把证书和验证器都写成显式算法，而 6.006 面向建立直觉，只要求你能一眼看出证据是短的。

> 注意三个认知陷阱：**陷阱一**：NP 不是"非多项式时间"的缩写！NP 里的问题目前**不知道**是否能在多项式时间内求解，但"不知道能不能快解"与"一定不能快解"是两回事——NP 只承诺"验证快"，不承诺"求解慢"。**陷阱二**：$P \subseteq NP$ 是**平凡的**（trivial）：求解器本身就是验证器——拿到证书不看，直接算出答案，答案对则输出 YES。这行包含关系不需要任何聪明证明。**陷阱三**：$NP \subseteq EXP$ 也几乎是平凡的：把所有可能的证书（至多 $2^{n^{O(1)}}$ 个）全部喂给多项式验证器，总时间仍是指数。**唯一不平凡、悬而未决的**是反方向 $P \supseteq NP$ 是否成立，即 $P = NP$？本页"大多数人认为 $P \subsetneq NP$"是一个**猜想**（conjecture），不是定理——这是计算机科学最重要、也最尴尬的开放问题（千禧年大奖问题之一，证明或证伪任一方向都值 100 万美元，且会天翻地覆：$P = NP$ 意味着所有"验证容易"的问题都能"快速求解"，密码学、优化、AI 全部重写）。一个连接点：你在 L18 学的 Subset Sum 正是 NP 的**明星成员**——它的验证器就是表里那行"检查候选子集是否 $\subseteq A$ 且元素和是否为 $S$"；而 L18 的核心结论"Subset Sum 的 DP 是伪多项式"此刻获得新解读：伪多项式算法只说明它在"数值大小"维度上可解，若 $P \ne NP$ 则不存在真正的多项式算法——下两页会看到 Subset Sum 其实是 NP-complete 的（weakly NP-complete），这条线索把 L18 与本讲焊在一起。
>
> 再补一层"为什么验证视角好用"的直觉：验证器把"难题"拆成了"容易的部分"——真正难的部分（找证书）被外包给了那个不存在的"魔法猜手"，剩下的（查证书）人人都会。这像极了你平时核对别人的证明：判断"这个证明对不对"（验证）通常远比自己"想出这个证明"（求解）容易。NP 的定义正是把这个日常经验提炼成数学：**若一个问题连"别人给答案后核对"都做不到多项式时间，它就连 NP 的门都进不去**（那些问题落在更难的类里，比如 EXP 中连验证都难的问题）。这张 5 问题验证表（最短路径/负环/最长简单路径/Subset Sum/Tetris）值得逐行默读一遍：每个验证器都是 $O(n)$ 或 $O(n^2)$ 的"死算"——没有任何一个需要"聪明"，这就是 NP 成员资格的典型画像：**问题本身可能极难，但它的 YES 证据总是"短且好查"**。对比之下，"证明一个实例是 NO"往往没有捷径（没有证书可查）——这正是 NO 侧与 YES 侧的本质不对称，也是 $NP$ 与 $coNP$（补类，本课不展开）分野的种子。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Reductions（归约）</span>

🎥 *Demaine 强调归约是全课反复使用的老朋友*："What does as hard as mean? This is our good friend reductions. We talk about reductions a lot in this class. Reductions are the easy way to use algorithms. You just take your problem, and you reduce it to a problem you already know how to solve."（翻译："至少一样难"是什么意思？就是我们这位老朋友 reductions（归约）。本课我们经常提到归约——归约是用算法的省力方式：把你的问题拿过来，归约成一个你已知怎么解的问题。）

- 假设你想求解 problem $A$
- 一个办法是把 $A$ 转化成某个你知道怎么求解的 problem $B$
- 用解 $B$ 的算法求解，再用它算出 $A$ 的解
- 这叫做从 problem $A$ 到 problem $B$ 的 **reduction（归约）**（$A \to B$）
- 因为 $B$ 可以用来解 $A$，所以 **$B$ 至少和 $A$ 一样难**（$A \le B$，读作"$A$ 不比 $B$ 难"）
- 通用算法策略：**归约到一个你知道怎么解的问题**

| Problem $A$ | Conversion（转化） | Problem $B$ |
|-------------|--------------------|-------------|
| Unweighted Shortest Path（无权最短路径） | 给所有边赋相等权重 | Weighted Shortest Path（带权最短路径） |
| Integer-weighted Shortest Path（整数权最短路径） | 细分每条边 | Unweighted Shortest Path（无权最短路径） |
| Longest Simple Path（最长简单路径） | 把权重取负 | Shortest Path（最短路径） |

![图 3-1：三种归约 A → B 的对照表（原书排版）](_assets/lec19_fig_3_1.png)

**图 3-1**：三行都朝「右边那个问题」归约，但方向信息各不相同 —— 无权→带权是**加一般性**（赋等权）；整数权→无权是反过来，用一个**更特殊**的模型去解更一般的模型（把权 $w$ 细分成 $w$ 条单位边，把权重编码进结构，前提是 $w$ 多项式有界）；最长→最短是**取负权**，仅当无负环时保持答案。第二行是这张表的反直觉点：归约的难度偏序允许特例解一般。*Each row moves right along the difficulty order, and the integer to unweighted row shows a special case solving a general one by encoding weights into structure.*

- 若 **NP 中的每个问题**都能多项式归约到 problem $A$，则称 $A$ 是 **NP-hard（NP 难）** 的
- 即 $A$ 至少和 NP 中每个问题一样难（对每个 $X \in NP$ 有 $X \le A$，即 $A$ 可以用来解每个 NP 问题）
- **NP-complete（NP 完全）** $= NP \cap NP\text{-hard}$
- 所有 NP-complete 问题彼此等价，即可以互相归约
- 第一个 NP-complete 问题？**NP 中的每个决策问题都能多项式归约到"判定一个逻辑电路是否可满足"**——这个问题叫 **Circuit SAT（电路可满足性）**
- Longest Simple Path 与 Tetris 都是 NP-complete 的，所以只要 $P \ne NP$（NP 中存在问题不属于 P），它们就不在 P 中
- **Chess 是 EXP-complete 的**：属于 EXP，且 EXP 中每个问题都能归约到它（所以 $\notin P$）

![图 3-2：P / NP / EXP / R 与 NP-hard / EXP-hard 的难度数轴（原书彩色图）](_assets/lec19_fig_3_2.png)

**图 3-2**：数轴自左向右是 P ⊂ NP ⊂ EXP ⊂ R，而 NP-hard / EXP-hard 的箭头指向右端 —— 「hard」不是某个位置，而是**从该点向右的整条射线段**。于是 NP-complete（$NP \cap NP$-hard）恰好落在 NP 区间的右端点：它既是 NP 的成员（所以可以验证），又已经能编码 NP 里所有问题（所以最右）。EXP-complete 同理落在 EXP 右端。图上 P 与 NP 之间、NP 与 EXP 之间的位置关系是**示意**（原文标注 informal），因为 $P \stackrel{?}{=} NP$ 至今未解。*`Hard` denotes a rightward half-line, not a point; NP-complete therefore sits exactly at the right endpoint of NP, and the diagram is explicitly informal because $P$ vs $NP$ is open.*

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> reduction（归约）在这一页从「技巧」升级成「序」：它给问题集合装上一个 $\le$ 关系，hardness（难度）这个词才有精确含义。
>
> 形式化：$A \le B$ 指存在一个 $\mathrm{poly}(n)$ 时间可计算的映射 $f$，使 $x \in A$ 当且仅当 $f(x) \in B$。两条性质值得单独说。一是传递性：若 $A \le B$ 且 $B \le C$，把两个映射复合起来仍是多项式时间，故 $A \le C$——于是所有问题被组织成一个 preorder（预序）。二是它缺反对称性：两个问题可以互相归约而彼此不是同一个问题（同一对象的不同编码、多项式时间内的重新编码都算），所以 $\le$ 不是 partial order（偏序），商掉「互相可归约」才得到等价类，NP-complete 就是这样一个类——若 $P \ne NP$，它与 P 那个类不相交。这一步正好落在 6.042J 的等价关系上：那边学的是自反、对称、传递三条件定一个划分，这里的 $\le$ 只满足自反与传递，商出来的划分更粗——同类成员「难度相同但问题不同」，这正是复杂度理论需要的粒度。
>
> 算一下细分归约的真实账单。$n = 1000$ 个顶点、$m = 5000$ 条边、权重是 $1$ 到 $W$ 的整数，细分成单位边后边数变成 $\sum w \le mW = 5000W$。取 $W = 10^{6}$：$5 \times 10^{9}$ 条边，一次 BFS 要 $O(V+E) \approx 5 \times 10^{9}$ 步，每秒 $10^{9}$ 步约 $5$ 秒，还撑得住。取 $W = 10^{9}$：$5 \times 10^{12}$ 条边，BFS 要 $5000$ 秒 $\approx 83$ 分钟，而按每条边 $8$ 字节存图需要 $40$ TB，内存先爆。理论上这仍然合法——$W$ 的 bit 长度只有 $30$，边数 $5 \times 10^{12}$ 是输入规模的 $3 \times 10^{7}$ 倍，是多项式关系；但次数大到不可用。这就是 polynomial time（多项式时间）与实际可行之间那道真实裂缝，也是 pseudo-polynomial（伪多项式）概念的来源：只有当 $W$ 多项式有界时，细分才不会指数膨胀。
>
> 跨课程连接：CLRS 第 34 章 §34.3 对归约证明有书写规范，要求把「给定 $A$ 的实例、构造 $B$ 的实例」写成显式算法并双向证明；本讲用表格给直觉，三行对应三种形态：restriction（限制，无权最短路径是带权的特例）、encoding（编码，把权重写进图结构）、以及一条反例警示（取负权只在无负环时保答案）。CSAPP 第 5 章讲常数因子为什么在工程里不可忽略，正好是同一件事的另一面：O 记号丢掉常数、归约丢掉多项式的次数，两者都是渐近抽象的代价，代价有多大要回到具体数上才知道。
>
> 把 gadget（小装置）归约抽象成三要素：① 每个结构单元里放一个「必须选固定个数」的选择装置；② 用边或约束编码「违反」——两件不能同时为真的东西之间连一条冲突边；③ 全局配额对齐单元数，使「选满」等价于「全部满足」。用 3-SAT 到 Independent Set（独立集）走一遍微型实例：子句集 $(x \lor y) \land (\lnot x \lor \lnot y)$，每个子句放两个顶点、子句内两顶点连边使同子句不能选两个，跨子句给互补文字连边，配额取 $2$。赋值 $x = 1, y = 0$ 使两个子句都真，对应选 $x$ 与 $\lnot y$——两者不互补、之间无边，独立集大小恰为 $2$，通过。反之任何大小为 $2$ 的独立集都必须每子句取一个，取法读回来就是一个一致赋值。三要素齐了，证明只剩验算。
>
> 所以本页三行表格不是三个小技巧，而是同一个序的三次落地；而方向感是这个序最容易读反的地方——想证 $A$ 难，要把已知难的问题归约到 $A$，写成 $X \le A$，不是把 $A$ 归约出去。记住这一条，后面所有 hardness 证明的骨架都在这里。

> NP-hard 与 NP-complete 的定义是层层加码：**NP-hard** = "能用来解 NP 中所有问题"（即对每个 $X \in NP$，$X \le A$）——它是 NP 难度的"上端"；**NP-complete** = NP-hard 且本身在 NP 中。于是若 $A$ 是 NP-complete 且你能找到 $A$ 的多项式算法，则把每个 NP 问题先归约到 $A$ 再解，就得到 $P = NP$——这就是"证明某问题是 NP-complete 等价于宣称它代表了整个 NP 类的难度"的含义。**为什么这有用？** 你若在现实中遇到一个 NP-complete 问题（下页的清单会告诉你这种问题到处都是），就知道不要浪费生命找它的多项式算法——转而接受指数/伪多项式/近似解。**归约的方向感**是新手最容易搞反的：想证明"我的问题 $A$ 难"，必须把**已知的难问题 $X$ 归约到 $A$**（$X \le A$，即 $A$ 至少和 $X$ 一样难）；反方向 $A \le X$（把 $A$ 归约到已知难问题）只说明"A 不比 $X$ 难"——这当然成立、却**证不出 $A$ 难**（正如任何可判定问题——包括所有 NP 问题——都能归约到停机问题，但那不说明它难）。想证明"我的问题 $A$ 容易"，则把 $A$ 归约到已知的易问题 $B$（$A \le B$）。归约的三种典型形态（以后在 6.045/6.046 会系统学）：**限制（restriction）**——$A$ 是 $B$ 的特例（无权最短路径是带权的特例）；**局部替换（gadget）**——把 $A$ 的结构单元替换成 $B$ 的小装置（$A \le B$ 是把 $A$ 实例翻译成 $B$ 实例；如把 3-SAT 归约到独立集时，把 $A$ 的每个子句替换成 $B$ 里的"三角形装置"）；**编码（encoding）**——把 $A$ 的语义编码进 $B$ 的输入（下页 Rectangle Packing 把整数 $a_i$ 编码成 $1 \times a_i$ 的矩形，就是编码型归约的绝佳例子）。
>
> 归约还是你判断"新问题能不能用老算法"的日常思维工具，只是本课以前没给它起名字：本页表格里把最长路径用负权化到最短路径（注意无负环才成立）、L18 把 Subset Sum 作为判定问题用伪多项式 DP 求解并讨论其 self-reducibility（自归约：反复调用判定 oracle 还原具体子集）、甚至分治法里"把大问题化到更小同类问题"都带归约的影子——区别只在于：**算法设计中的归约要求转换本身高效且保持最优解**，而复杂度理论中的归约只要求**保持 YES/NO 答案**（连解都不用恢复）。后者的要求更弱，所以能做更大胆的编码——这也是为什么复杂度归约能证明"看起来毫不相干的问题"难度相同（比如把整数划分编码成矩形装箱）。归约的复杂度预算也要记住：**归约转换本身必须是多项式时间的**，否则"用 B 的多项式算法解 A"的总时间可能不再是多项式（转换就要指数时间）。最后，一条把本页与 L18 接起来的暗线：Subset Sum $\le$ Knapsack（L18 recitation 提到背包是 Subset Sum 的推广——每个物品可带价值），而 3-Partition $\le$ Rectangle Packing $\le$ Jigsaw（下页的归约链）——NP-complete 问题之间织成一张网，证明一个等于证明一片，这正是"所有 NP-complete 问题彼此等价"的实际威力。

---

## <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Examples of NP-complete Problems（NP 完全问题举例）</span>

- **Subset Sum**（来自 L18）："weakly NP-complete（弱 NP 完全）"——正是这一点允许伪多项式时间算法存在，但除非 $P = NP$，否则不存在多项式算法
- **3-Partition（3-划分）**：给定 $n$ 个整数（$n$ 为 3 的倍数），能否把它们分成 $\frac{n}{3}$ 个和相等的三元组？（"strongly NP-complete（强 NP 完全）"：除非 $P = NP$，否则不存在伪多项式时间算法）
- **Rectangle Packing（矩形装箱）**：给定 $n$ 个矩形和一个 target rectangle（目标矩形），其中 target 的面积等于 $n$ 个矩形面积之和，问能否无重叠地装入
  - 从 **3-Partition 到 Rectangle Packing 的归约**：把整数 $a_i$ 转化为 $1 \times a_i$ 的矩形；把 target 矩形设为 $\frac{n}{3} \times \frac{\sum_i a_i}{3}$
- **Jigsaw puzzles（拼图）**：给定 $n$ 块可能有 ambiguous tabs/pockets（可互换的同形凸榫/凹槽）的拼图块，问能否拼合
  - 从 Rectangle Packing 归约：用唯一匹配的凸榫/凹槽强制拼出矩形与矩形边界；其余边界用同一个 ambiguous 凸榫/凹槽
- **n 个字符串的 Longest Common Subsequence（最长公共子序列）**
- **图中的 Longest Simple Path（最长简单路径）**
- **Traveling Salesman Problem（旅行商问题，TSP）**：访问给定图所有顶点（且回到起点）的最短路径（判定版：最小权重是否 $\le d$）
- **3D 中绕过障碍物的最短路径**
- **给定图的 3-coloring（3-着色）**（但 2-coloring 属于 P）
- **给定图中的最大 clique（团）**
- **SAT（可满足性问题）**：给定一个由 AND、OR、NOT 构成的 Boolean formula（布尔公式），是否存在赋值使其为真？例如 $x \land \lnot x$ 是 NO input
- **Minesweeper（扫雷）、Sudoku（数独）以及大多数 puzzle（谜题）**
- **Super Mario Bros.（超级马里奥）、Legend of Zelda（塞尔达传说）、Pokémon（宝可梦）以及大多数视频游戏都是 NP-hard 的（很多还更难）**

🎥 *Demaine 提到视频游戏其实落在更高的复杂度类*："Super Mario Brothers is NP-hard. Legend of Zelda is NP-hard. Pokemon is NP-hard. These problems are actually all a little bit harder than NP in a different class called PSPACE, which I won't go into."（翻译：超级马里奥是 NP-hard，塞尔达传说是 NP-hard，宝可梦是 NP-hard。这些问题其实比 NP 还要再难一点，落在另一个叫 PSPACE 的类里——这个我就不展开了。）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这张清单是 NP-complete 问题的"名人堂"，也揭示了 complexity theory 最反直觉的事实：**NP 完全性不是病态理论的专利，而是日常世界的常态**。逐类拆解：
>
> ① **数值型**：Subset Sum 与 3-Partition 的对照是 L18 的直接延续。两者都是"分一堆数"，但 NP 完全性的**强弱**不同：Subset Sum 是 weakly NP-complete——它的困难全部来自那个可能指数大的目标值 $T$，若把输入整数写成 unary（一元编码），伪多项式 DP $O(nT)$ 就变成输入规模的多项式（L18 已详述）；3-Partition 是 strongly NP-complete——即使输入全用 unary 编码依然 NP-complete，不存在任何伪多项式算法（除非 $P = NP$）。直觉差别：Subset Sum 的"数字大小"是唯一的困难来源（数字小时问题平凡），3-Partition 的困难是**组合性**的（三个一组和相等，即使数字都很小也很难），所以 3-Partition 更"硬核"。这正是伪多项式算法只对 weakly NP-complete 问题有效的理论根据——L18 的 DP 能解 Subset Sum 是因为它恰好是 weak 的。
>
> ② **几何型**：从 3-Partition 到 Rectangle Packing 的归约（讲义 Reductions 表下方那行，方向是 3-Partition $\le$ Rectangle Packing）是"编码型归约"的范本：整数 $a_i$ 变成 $1 \times a_i$ 的矩形条。⚠️ **讲义此处尺寸有笔误，需勘误**：讲义写 target 为 $\frac{n}{3} \times \frac{\sum_i a_i}{3}$，但这个矩形的面积是 $\frac{n \sum_i a_i}{9}$，并不等于 $n$ 个矩形条的总面积 $\sum_i a_i$（除非 $n = 9$），与问题陈述"target 面积 = 各矩形面积之和"矛盾。**正确的构造**是：3-Partition 把 $n$ 个整数分成 $\frac{n}{3}$ 个三元组、每组和同为 $B = \frac{3\sum_i a_i}{n}$（由面积守恒反解：$\frac{n}{3}$ 组 × 每组和 $B$ = $\sum_i a_i$ ⟹ $B = \frac{3\sum_i a_i}{n}$）；把每个三元组的三根条**首尾相接排成一行**（行长 = 三元组和 = $B$），$\frac{n}{3}$ 行上下堆叠成 target = $\frac{n}{3}$（高）× $B$（宽）——面积 $= \frac{n}{3} \cdot \frac{3\sum_i a_i}{n} = \sum_i a_i$ ✓ 守恒。若存在 3-划分，每行放一个三元组即得无重叠装箱；反过来，任何装箱都必须排成恰好 $\frac{n}{3}$ 行（行高为 1、面积守恒强制行数固定），每行三条的和必须相等（否则行宽超出 $B$ 或留缝），于是答案保持。（3-Partition 标准定义还要求 $B/4 < a_i < B/2$——每个数大于四分之一 B 且小于一半 B，正是为强制"每组恰三条"；讲义省略了此条件，严谨的归约论证需要它。）**Rectangle Packing 到 Jigsaw** 的归约（方向是 Rectangle Packing $\le$ Jigsaw）展示"gadget"思想：唯一匹配的凸榫/凹槽强制拼图块拼成指定矩形（任何偏离都被榫槽结构否决），ambiguous 榫槽给其余自由度——用物理结构编码约束，是归约设计的艺术。
>
> ③ **图上**：Longest Simple Path、最大 clique、3-coloring、TSP 都在清单里。它们与你在本课学过的多项式图算法形成**精确对照**：最短路径（多项式）vs 最长简单路径（NP-complete）——差别只在"简单"二字——但"允许重复"并不会让问题变容易：在 DAG 中（无环，简单性自动满足）最长路径负权化后多项式可解；一般有环图里，允许重复的"最长 walk"遇到正环就无界、去掉正环又回到简单路径的难度。禁止重复的简单路径版本则要枚举顶点排列；2-coloring（多项式，BFS 二分图判定）vs 3-coloring（NP-complete）；"找最小生成树"（多项式）vs"找最大团"（NP-complete）。**同一个图，不同的问题难度天差地别**——难度不在图里，而在问题问的是什么。
>
> ④ **"视频游戏都是 NP-hard"**不是玩笑：2000 年代起研究者系统证明了 Tetris、Super Mario Bros.、Legend of Zelda、Pokémon 等游戏的判定版本是 NP-complete 甚至 PSPACE-complete（多项式空间可解的问题类；PSPACE 包含 NP，但"是否严格更难"与 P vs NP 一样未证，见 6.045）——方法就是把 SAT 或 3-Partition 的实例"编码"成游戏关卡（用关卡中的敌人、机关模拟逻辑门与计数）。这条研究方向叫游戏与谜题的复杂度分析（NP-hardness of games），有严肃的学术论文（如 Giovanni Viglietta 的 "Gaming is a hard job, but someone has to do it!"，Theory of Computing Systems 2014；Tetris 的 NP-完全性见 Demaine 等 2004 年 "Tetris is Hard, Even to Approximate"）。**它对你的意义**：NP 完全性是一种"结构诊断"，一旦你把自己面对的问题识别为 NP-complete（或 NP-hard），就该立刻转换策略——找近似算法、参数化算法、伪多项式算法（若 weakly NP-complete）、启发式、或约束求解器（SAT solver，现代工业界处理这类问题的实际主力，见下注）。
>
> ⑤ 清单最后一行"很多还更难"呼应第 3 页 Chess 的 EXP-complete：NP-complete 之上还有更难的类（PSPACE、EXP、不可判定），游戏恰好横跨全部层级——Tetris 是 NP-complete（其"能否活过给定方块序列"判定版），Chess 是 EXP-complete（讲义第 3 页，且已证 $\in EXP \setminus P$），围棋也在 EXP 级，而"给定规则能否让任意程序停下"（即做游戏 AI 的终极形态：判定对手程序是否停机）不可判定。**复杂度类不是一条线，而是一座越往上越陡的山。**

---

> <span style="color:#1e8449;">**[note] Note（译者注，Circuit SAT 与第一个 NP-complete 问题）:**</span> "第一个 NP-complete 问题"为什么是 Circuit SAT 而不是别的？这需要一点历史与机制。1971 年 Stephen Cook 发表 "The Complexity of Theorem-Proving Procedures"，证明了 **Circuit SAT / SAT 是 NP-complete**；次年 Richard Karp 发表 "Reducibility Among Combinatorial Problems"，把 Cook 的结果推广到 21 个问题（包括 clique、vertex cover、Hamiltonian cycle、TSP 等），从此 NP-completeness 成为一门"归约工业"。为什么 Circuit SAT 是自然的"第一个"？因为**任何 NP 问题的验证过程本身就是一个逻辑电路**：验证器 $V$ 在输入 $(I, c)$ 上运行多项式时间，而"多项式时间计算"可以被展平成多项式大小的布尔电路（电路模拟图灵机/程序的基本结论，CLRS §34.3 有构造（Lemma 34.6））；于是"$I$ 是 YES 实例"等价于"存在证书 $c$ 使电路输出 1"，即该电路可满足（satisfiable）。**每个 NP 问题都归约到 Circuit SAT，不需要任何问题特异的技巧**——归约就是"把验证器编译成电路"。这正是"第一个"的本质：它不是靠逐个构造归约拼出来的，而是**一次性覆盖所有 NP 问题**的通用论证。从 Circuit SAT 到 SAT 再到 3-SAT 只需局部改写（把电路门展开成子句、再把长句切成每句恰含三个文字的析取子句（整个公式是这些子句的合取）），于是 3-SAT 成为后续所有归约的"起点"（6.046/6.045 会把 3-SAT 归约到独立集、clique、vertex cover、Hamiltonian cycle……形成一张互相可达的归约网）。Cook 1971 与 Karp 1972 的论文动机都来自 logic（逻辑）与 automated theorem proving（自动定理证明）——Cook 想回答"定理证明能否高效机械化"，意外把 SAT 置于 NP 的核心，奠定了整个 NP 理论。**记忆锚点**：Circuit SAT 是 NP-complete 的**种子**，SAT/3-SAT 是归约的**枢纽**，Subset Sum/TSP/clique 等是**终端消费者**——归约方向永远从枢纽指向终端。
>
> 把 Cook 的证明再往深挖一层，你会看到"多项式时间计算 = 电路"这个等式的威力。验证器 V 在输入 $(I, c)$ 上跑 $T = n^{O(1)}$ 步；每一步（读内存、算术、跳转）都可以用一个小电路模拟（在 bit 级模型上每步 $O(1)$ 个门；在 word-RAM 上每步操作 $w$ 位字需 $\mathrm{poly}(w)$ 个门），把 $T$ 步串起来就得到总大小多项式于 $T$ 的电路，其输入是证书 $c$ 的各位。于是"存在使 V 输出 YES 的 $c$" = "存在使电路输出 1 的输入赋值" = 电路可满足。**注意这个归约不需要知道 V 内部在算什么**——任何多项式时间的 V 都能被"编译"成电路，这就是通用性（universality）的由来：一次证明，覆盖所有 NP 问题。Circuit SAT → SAT → 3-SAT 的链条把电路门（与/或/非）翻译成布尔子句：每个门变成若干子句约束其输入输出关系，再把长子句用辅助变量切成三个一组的短子句——翻译保持可满足性，且规模只多项式增长。3-SAT 之所以成为归约枢纽，是因为"三个文字一组"的形态足够刚性，方便后续归约构造 gadget（6.046 会把 3-SAT 归约到 Independent Set：每个子句放三个顶点、同子句内两两连边、跨子句连"互为否定"的边，求大小为 $m$（子句数）的独立集——可满足赋值 ↔ 大小 $m$ 的独立集一一对应）。
>
> 对你有实际价值的一点：**SAT 不只是理论玩具**。现代 SAT solver（CDCL 算法：冲突驱动子句学习 + 回溯，见 6.046 尾段或专门课程）能在秒到分钟级求解含数百万变量的工业实例——硬件验证（芯片等价性检查）、软件测试（符号执行）、调度、密码分析都把它当引擎用。理论说 SAT 是 NP-complete（最坏情况指数），实践却说"大多数实例其实好解"——两者不矛盾：NP-complete 保证的是**最坏情形**，真实世界的实例常有结构（稀疏、层次化）可被 CDCL 利用。这也是学习本讲最重要的心态校正：**"NP-complete"不是"别做了"的墓碑，而是"别找多项式最坏情况算法了，换武器"的路标**——伪多项式（Subset Sum）、参数化（固定参数 $k$、把指数限制在 $k$ 上）、近似、SAT 或整数线性规划（ILP）solver、启发式，都是武器库里的备选项。CLRS 第 34 章（NP-Completeness）对归约证明的书写规范有系统示范，适合作为本讲的延伸阅读。
>
> 一个具体的"证书 + 验证器"例子帮你看清 Circuit SAT 的机制：给定电路 $C$（由与/或/非门组成），YES 实例的证书就是一组让 $C$ 输出 1 的输入赋值；验证器只需按门逐层求值、$O(电路大小)$ 时间即可核对——证书"短且好查"，完美符合 NP 的画像。3-SAT 到 Independent Set 的归约也可配微型实例走一遍：子句 $(x \lor y) \land (\bar x \lor \bar y)$ 对应两个"三角形"（每条边两端分别来自两个子句、标互为否定的文字），$m = 2$；可满足赋值 $x=1, y=0$ 给出独立集 $\{x, \bar y\}$，大小恰为 2——每个子句恰贡献一个顶点。最坏情况指数 vs 工业可解，与快排最坏 $O(n^2)$ 却实际常用是同一类现象：**复杂度分析给最坏保证，工程实践吃平均/结构红利**。

---

> <span style="color:#7f8c8d;">MIT OpenCourseWare — 6.006 Introduction to Algorithms, Spring 2020. Lecture 19 讲义翻译版。原文：https://ocw.mit.edu（Terms of Use 见 https://ocw.mit.edu/terms）</span>
