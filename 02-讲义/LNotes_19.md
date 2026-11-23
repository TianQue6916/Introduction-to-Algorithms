# Lecture 19: Complexity（复杂度）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Decision Problems（判定问题）

- Decision problem（判定问题）：把 inputs 归为 YES（1）或 NO（0）。
- Inputs 要么是 NO inputs，要么是 YES inputs。

| Problem（问题） | 判定内容 |
|---|---|
| s-t Shortest Path | 给定的 $G$ 中是否存在一条从 $s$ 到 $t$、weight 至多为 $d$ 的 path？ |
| Negative Cycle | 给定的 $G$ 中是否存在 negative weight cycle？ |
| Longest Simple Path | 给定的 $G$ 中是否存在一条 weight 至少为 $d$ 的 simple path？ |
| Subset Sum | 给定的整数集合 $A$ 中是否存在一个 subset，其和为 $S$？ |
| Tetris | 在给定的 board（棋盘）上，你能否在给定的 pieces 序列下存活？ |
| Chess | 给定棋局下，某一 player 能否 force a win（强制获胜）？ |
| Halting problem | 给定 computer program 对给定 input 是否会 terminate（停机）？ |

## Decision（判定）

- Algorithm / Program：长度固定的 code（运行在 word-RAM 上，word 为 $\Omega(\log n)$ bits），用来求解一个问题。
- 也就是：它对每个 input 都产出 correct output。
- 并且 code 的长度与 instance size 无关。
- 若存在一个 program 能在 finite time（有限时间）内求解该问题，则称该问题 decidable（可判定的）。

## Decidability（可判定性）

- Program 是有限的（常数的）bit string，也就是一个非负整数 $\in \mathbb{N}$。
- Problem 是一个 function $p : \mathbb{N} \to \{0, 1\}$，也就是一个无限的 bit string。
- 程序的数量为 $|\mathbb{N}|$，即 countably infinite（可数无限）。
- 问题的数量为 $|\mathbb{R}|$，即 uncountably infinite（不可数无限）。
- 所以（# of programs）$\ll$（# of problems）。
- （用 Cantor's diagonalization argument（康托对角线论证）证明，大概在 6.042 中讲过。）
- 这证明了：大多数 decision problems 无法被任何 program 求解（undecidable，不可判定）。
- 例如 Halting problem 是不可判定的（6.045 中有许多精彩的证明）。
- 幸运的是，我们能想到的多数 problem 在结构上都是 algorithmic 的，因而可判定。

## Decidable Decision Problems（可判定的判定问题）

| 集合 | 含义 |
|---|---|
| $\mathbb{R}$ | 可在有限时间内判定的问题（'R' 来自 recursive languages） |
| $\mathbb{EXP}$ | 可在指数时间 $2^{n^{O(1)}}$ 内判定的问题（我们想到的多数问题都在这里） |
| $\mathbb{P}$ | 可在多项式时间 $n^{O(1)}$ 内判定的问题（efficient algorithms，本课的重点） |

- 这些集合互不相同，即 $\mathbb{P} \subsetneq \mathbb{EXP} \subsetneq \mathbb{R}$。
- 该结论由 time hierarchy theorems（时间层次定理）得到，见 6.045。
- 例如 Chess 在 $\mathbb{EXP} \setminus \mathbb{P}$ 中。

## Nondeterministic Polynomial Time (NP)（非确定性多项式时间）

- $\mathbb{P}$ 是这样一类 decision problems 的集合：存在 algorithm $A$，使对每个规模为 $n$ 的 input $I$，$A$ 在 $I$ 上运行 poly$(n)$ 时间并正确求解 $I$。
- $\mathbb{NP}$ 是这样一类 decision problems 的集合：存在 verification algorithm（验证算法）$V$，它以问题的 input $I$ 与一个长度为 $I$ 的规模的多项式的 certificate bit string（证书比特串）为输入，使得：
  - $V$ 的运行时间总是 $I$ 的规模的多项式；
  - 若 $I$ 是 YES input，则存在某个 certificate $c$，使 $V$ 在 input $(I, c)$ 上输出 YES；并且
  - 若 $I$ 是 NO input，则无论选什么 certificate $c$，$V$ 在 input $(I, c)$ 上总是输出 NO。
- 可以把 certificate 理解为「$I$ 是 YES input」的一个 proof（证明）。
- 若 $I$ 其实是 NO input，那么任何 proof 都不该 work。

| Problem | Certificate（证书） | Verifier（验证器） |
|---|---|---|
| s-t Shortest Path | 一条从 $s$ 到 $t$ 的 path $P$ | 把 $P$ 上的 weights 相加，检验是否 $\le d$ |
| Negative Cycle | 一个 cycle $C$ | 把 $C$ 上的 weights 相加，检验是否 $< 0$ |
| Longest Simple Path | 一条 path $P$ | 检验 $P$ 是否是 weight $\ge d$ 的 simple path |
| Subset Sum | 一个 items 集合 $A'$ | 检验 $A' \subseteq A$ 且其和为 $S$ |
| Tetris | 一串 moves（操作） | 检验这些 moves 是否能让你存活 |

- $\mathbb{P} \subseteq \mathbb{NP}$：验证器 $V$ 直接忽略 certificate 求解该 instance 即可。
- $\mathbb{NP} \subseteq \mathbb{EXP}$：把所有可能的 certificates 都试一遍！至多 $2^{n^{O(1)}}$ 个，对每个都运行验证器 $V$。
- Open（未决问题）：$\mathbb{P} = \mathbb{NP}$ 吗？$\mathbb{NP} = \mathbb{EXP}$ 吗？
- 多数人认为 $\mathbb{P} \subsetneq \mathbb{NP} \subsetneq \mathbb{EXP}$，即生成 solution 比检验 solution 更难。
- 无论你往哪个方向证明出来，人们都会给你很多钱（100 万美元的 Millennium Prize，千禧年大奖）。
- 为什么我们在意这个？
- 若能证明某问题是 $\mathbb{NP}$ 中最难的问题，那么在 $\mathbb{P} \ne \mathbb{NP}$ 的前提下，它就无法在多项式时间内求解。
- 如何关联问题的难易？Reductions（归约）！

## Reductions

- 假设你想求解问题 $A$。
- 一种解法是把 $A$ 转换成你已会求解的问题 $B$。
- 用 $B$ 的 algorithm 求解，再用它算出 $A$ 的 solution。
- 这称为从问题 $A$ 到问题 $B$ 的 reduction（$A \to B$）。
- 因为 $B$ 可用来求解 $A$，所以 $B$ 至少和 $A$ 一样难（$A \le B$）。
- 一般的 algorithmic strategy：归约到你已会求解的问题。

| 从 $A$ | Conversion（转换） | 到 $B$ |
|---|---|---|
| Unweighted Shortest Path | 给所有 edges 相同的 weights | Weighted Shortest Path |
| Integer-weighted Shortest Path | Subdivide edges（细分边） | Unweighted Shortest Path |
| Longest Path | Negate weights（取负权） | Shortest Path |

- 若 $\mathbb{NP}$ 中每个问题都能 polynomial-time reducible（多项式归约）到 $A$，则称 $A$ 是 NP-hard。
- 也就是：$A$ 至少和 $\mathbb{NP}$ 中每个问题一样难（可用来求解它们），即对 $X \in \mathbb{NP}$ 有 $X \le A$。
- NP-complete $= \mathbb{NP} \cap$ NP-hard。
- 所有 NP-complete problems 彼此等价，即互相可归约。
- 第一个 NP-complete problem 是什么？
- 每个 decision problem 都可归约到「满足一个 logical circuit（逻辑电路）」。
- 这个问题称为 “Circuit SAT”。
- Longest Simple Path 与 Tetris 是 NP-complete。
- 所以若有任何问题落在 $\mathbb{NP} \setminus \mathbb{P}$ 中，它们就是（这样的问题）。
- Chess 是 EXP-complete：在 $\mathbb{EXP}$ 中，且 $\mathbb{EXP}$ 中每个问题都可归约到它（因此它 $\notin \mathbb{P}$）。

## Examples of NP-complete Problems（NP 完全问题的例子）

- Subset Sum（来自 L18）：属于 “weakly NP-complete”（弱 NP 完全），这正是它能有 pseudopolynomial-time algorithm 的原因；但除非 $\mathbb{P} = \mathbb{NP}$，不存在 polynomial algorithm。
- 3-Partition：给定 $n$ 个 integers，能否把它们分成若干个 sum 相等的 triple（三元组）？属于 “strongly NP-complete”（强 NP 完全）：除非 $\mathbb{P} = \mathbb{NP}$，不存在 pseudopolynomial-time algorithm。
- Rectangle Packing（矩形装箱）：给定 $n$ 个 rectangles 与一个目标 rectangle，后者的面积等于这 $n$ 个 rectangle 面积之和，要求不重叠地装进去。
  - 从 3-Partition 到 Rectangle Packing 的 reduction：把 integer $a_i$ 变成 $1 \times a_i$ 的 rectangle；把目标 rectangle 设为 $n/3 \times (\sum_i a_i)/3$。
- Jigsaw puzzles（拼图）：给定 $n$ 个 pieces，其 tabs / pockets（凸起 / 凹槽）可能有歧义，要求把它们拼起来。
  - 从 Rectangle Packing 的 reduction：用唯一匹配的 tabs / pockets 强迫拼出 rectangles 与矩形边界；对所有其它边界使用一个带歧义的 tab / pocket。
- $n$ 个 strings 的 longest common subsequence。
- graph 中的 longest simple path。
- Traveling Salesman Problem（旅行商问题）：访问给定 graph 的所有 vertices 的最短 path（或判定版本：minimum weight 是否 $\le d$）。
- 3D 中在 obstacles（障碍物）之间的 shortest path。
- 给定 graph 的 3-coloring（但 2-coloring $\in \mathbb{P}$）。
- 给定 graph 中最大的 clique（团）。
- SAT：给定 Boolean formula（用 AND、OR、NOT 构成），它是否恒为 true？
  - 例如 $x \ \text{AND} \ \text{NOT}\ x$ 是 NO input。
- Minesweeper、Sudoku，以及多数 puzzles。
- Super Mario Bros.、Legend of Zelda、Pokémon，以及多数 video games 都是 NP-hard（很多还更难）。
