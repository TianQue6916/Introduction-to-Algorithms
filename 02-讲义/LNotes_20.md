# Lecture 20: Course Review（课程回顾）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## 6.006: Introduction to Algorithms（算法导论）

- Goals（目标）：
  1. 求解 hard computational problems（输入规模非常数的计算问题）。
  2. 论证 algorithm 是 correct 的（Induction、Recursion）。
  3. 论证 algorithm 是 “good” 的（Asymptotics、Model of Computation，计算模型）。
  - （并把以上三点 effectively communicate 给人类或计算机。）
- “good” algorithms 总是存在吗？
  - 多数 problems 无法被高效求解，但我们想到的许多问题可以！
  - Polynomial 指的是 input 规模的多项式。
  - Pseudopolynomial 指的是 input 规模、以及 input 中数字大小的多项式。
  - NP：Nondeterministic Polynomial time，certificates 可在多项式时间内被检验。
  - NP-hard：这样一类 problems 的集合 —— 它们可用来在 poly-time 内求解 NP 中任何问题。
  - NP-complete：NP-hard 与 NP 的交集。

## How to solve an algorithms problem?（如何求解算法问题？）

- 归约到你已会求解的问题：
  - Search / Sort（Q1）：
    - Search：Extrinsic（外在，Sequence）与 Intrinsic（内在，Set）Data Structures。
    - Sort：Comparison Model（比较模型）、Stability（稳定性）、In-place（原地）。
  - Graphs（Q2）：
    - Reachability（可达性）、Connected Components（连通分量）、Cycle Detection（环检测）、Topological Sort（拓扑排序）。
    - Single-Source / All-Pairs Shortest Paths。
- 设计新的 recursive algorithm：
  - Brute Force。
  - Divide & Conquer。
  - Dynamic Programming（Q3）。
  - Greedy / Incremental。

## Next Steps（后续课程）

- (U) 6.046: Design & Analysis of Algorithms。
- (G) 6.851: Advanced Data Structures。
- (G) 6.854: Advanced Algorithms。

## 6.046（后续课程延伸）

- 6.006 的延伸：
  - Data Structures：Union-Find、通过 potential analysis（势能分析）做 Amortization（摊还分析）。
  - Graphs：Minimum Spanning Trees（最小生成树）、Network Flows / Cuts（网络流 / 割）。
  - Algorithm Design（Paradigms，范式）：Divide & Conquer、Dynamic Programming、Greedy。
  - Complexity：Reductions。
- Relax Problem（放宽问题：改变 correct / efficient 的定义）：
  - Randomized Algorithms（随机算法）：
    - 6.006 大多只讲 deterministic 的（hashing 例外）。
    - Las Vegas：always correct，probably fast（像 hashing）。
    - Monte Carlo：always fast，probably correct。
    - 在 structured data 上通常能拿到更快的 randomized algorithms。
  - Numerical Algorithms / Continuous Optimization（数值算法 / 连续优化）：
    - 6.006 只处理 integers。
    - Approximate real numbers（近似实数）！为 precision（精度）付出时间。
  - Approximation Algorithms（近似算法）：
    - Input 是 optimization problem（在 weighted outputs 上求 min / max）。
    - 许多 optimization problems 是 NP-hard。
    - 在 polynomial time 内能逼近 optimal solution 到什么程度？
- Change Model of Computation（改变计算模型）：
  - Cache Models（缓存模型，memory hierarchy cost model，存储层次代价模型）。
  - Quantum Computer（量子计算机，利用量子性质）。
  - Parallel Processors（并行处理器，用多个 CPUs 而不是一个）：
    - Multicore、large shared memory（大共享内存）。
    - Distributed cores、message passing（消息传递）。

## Future Courses（后续课程）

| Model（模型） | Application（应用） |
|---|---|
| Computation / Complexity | 6.045, 6.840, 6.841 |
| Biology | 6.047 |
| Randomness | 6.842 |
| Game Theory | 6.853 |
| Quantum | 6.845 |
| Cryptography | 6.875 |
| Distributed / message passing | 6.852 |
| Vision | 6.819 |
| Multicore / shared memory | 6.816, 6.846 |
| Graphics | 6.837 |
| Graph and Matrix | 6.890 |
| Geometry | 6.850 |
| Constant Factors / Performance | 6.172 |
| Folding | 6.849 |

† 原 PDF 该表为两列并排的合并单元格，「Model」与「Application」的逐行对应关系在文字层中被打散为两个独立列表；上表的配对按 6.xxx 课程编号的实际主题推定重建。
