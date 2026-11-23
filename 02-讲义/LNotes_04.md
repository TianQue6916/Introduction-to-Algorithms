# Lecture 4: Hashing（哈希）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Review（回顾）

上一讲结束时我们手上有两张表。Array 的 `find` 是 $n$，Sorted Array 的 `find` 是 $\log n$，这就是当时的全部家当。

| Data Structure | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Sorted Array | $n\log n$ | $\log n$ | $n$ | $n$ | $1$ | $1$ | $\log n$ | $\log n$ |

- Idea！我们想要更快的 search 与 dynamic operations。能不能让 `find(k)` 比 $\Theta(\log n)$ 更快？
- 在 comparison model 下答案是「不能」，这是 lower bound（下界）。但换个 model，答案是「能」——本讲就干这件事。

## Comparison Model（比较模型）

- 在这个 model 里，假设 algorithm 只能通过 comparison（比较）来区分 items。
- Comparable items（可比较元素）就是黑盒：只支持两两之间的比较。
- 允许的 comparisons 是 $<, \le, >, \ge, =, \ne$，输出是二值：True 或 False。
- 目标：存储 $n$ 个 comparable items 构成的 set，支持 `find(k)`。
- Running time 被比较次数从下方界定，所以**数比较次数**就等于在算时间。

## Decision Tree（判定树）

- 任何 algorithm 都可以看成一棵由所执行 operations 构成的 decision tree。
- internal node（内部节点）代表一次 binary comparison（二元比较），分成 True 与 False 两枝。
- 对 comparison algorithm 而言，decision tree 一定是 binary 的（原文此处配图，见 [Figure 1]）。
- leaf（叶子）代表 algorithm 终止，并产出对应的 output。
- 一条 root-to-leaf path（根到叶路径）代表 algorithm 在某个 input 上的一次完整执行。
- 每个可能的 output 至少要有一个 leaf，所以一次 search 需要至少 $n + 1$ 个 leaves（$n$ 个「命中」加一个「未命中」）。

[Figure 1：原文此处为示意图，展示一棵 binary decision tree 的形状：内部节点是 $\le$ 比较，向下分成两枝，叶子是最终的 find 结果。原 PDF 为矢量插图，文字层无内容，此处以文字描述保留其结构]

## Comparison Search 的 Lower Bound（下界）

- 一个 comparison search algorithm 的 worst-case running time 是多少？
- 由于 running time $\ge$ 比较次数 $\ge$ 任何 root-to-leaf path 的最大长度 $\ge$ tree 的高度。
- 那么，含 $\ge n$ 个节点的 binary tree，最小高度是多少？
- 最小高度出现在 tree 是 complete（完全）的时候：除最后一行外每一行都填满。
- 此时高度 $\ge \lceil \lg(n+1)\rceil - 1 = \Omega(\log n)$，所以任何 comparison sort 的 running time 都是 $\Omega(\log n)$。
- Sorted array 恰好达到这个 bound！太好了。
- 更一般地：若 tree 有 $\Theta(n)$ 个 leaves、最大 branching factor 为 $b$，则高度是 $\Omega(\log_b n)$。
- 要想更快，就必须有一个能让 branching factor 达到 super-constant（超常数）即 $\omega(1)$ 的 operation。怎么做到？

## Direct Access Array（直接访问数组）

- 关键工具：Word-RAM model 里的 $O(1)$ time random access indexing（随机访问索引）。这等于拿到了 linear branching factor（线性分支因子）！
- Idea！给每个 item 一个唯一整数 key $k \in \{0, \dots, u-1\}$，然后把 item 存在 array 的 index $k$ 处。
- 这等于给 array 的每一个 index 都赋予了一个 meaning（语义）。
- 若 keys 能塞进一个 machine word（机器字），即 $u \le 2^w$，则 worst-case 下 `find` 与 dynamic operations 都是 $O(1)$！太好了。
- 6.006 的约定：除非长度被显式参数化，否则假设 input 的 number / string 都能塞进一个 word。
- 理由是：计算机内存里的任何东西都是 binary integer，或者是内存中一个 (static) 64-bit address。
- 但 space 是 $O(u)$，若 $n \ll u$ 就非常糟 :(
- 例子：若 keys 是十个字母的姓名，要一位一 bit，就需要 $26^{10} \approx 17.6$ TB 空间。
- 怎么才能用更少的空间？

## Hashing（哈希）

- Idea！若 $n \ll u$，就把 keys 映射到一个更小的 range $m = \Theta(n)$，用小一号的 direct access array。
- Hash function（哈希函数）：$h(k) : \{0, \dots, u-1\} \to \{0, \dots, m-1\}$，这套结构也叫 hash map。
- 此时 direct access array 称为 hash table（哈希表），$h(k)$ 称为 key $k$ 的 hash。
- 若 $m \ll u$，由 pigeonhole principle（鸽巢原理），**没有任何** hash function 是 injective（单射）的。

## Collision（碰撞）

- 因此必然存在 keys $a, b$ 使 $h(a) = h(b)$，这就是 collision :(
- 两个 items 不能存在同一个 index 上，那存哪儿？两种选择：
  - 存到 array 的别处（open addressing，开放寻址）
    - analysis 较复杂，但在工程上很常见、很实用。
  - 存进另一个支持 dynamic set interface 的 data structure（chaining，链式法）。

## Chaining（链式法）

- Idea！把 collisions 存进另一个 data structure，也就是一条 chain。
- 若 keys 大致均匀分布在各个 indices 上，chain 长度是 $n/m = n/\Omega(n) = O(1)$！
- 若 chain 长度是 $O(1)$，则所有 operations 都花 $O(1)$ 时间！太好了。
- 若不然，大量 items 可能映射到同一个位置，例如 $h(k) = \text{constant}$，那 chain 长度就是 $\Theta(n)$ :(
- 所以需要一个好的 hash function。那什么算好的 hash function？

## Hash Functions（哈希函数）

### Division method（除法法，坏的）

```math
h(k) = (k \bmod m)
```

- 这是一个 heuristic（启发式），在 keys 均匀分布时表现好。
- $m$ 应当避开 stored keys 的对称性。
- 取远离 $2$ 的幂与 $10$ 的幂的大素数，通常比较合理。
- Python 用的是这个方法的一个变体，外加一些额外的 mixing（混洗）。
- 但要注意：若 $u \gg n$，**任何** hash function 都存在某个 input set，使它造出一条 $O(n)$ 长度的 chain。
- Idea！那就别用固定的 hash function，而是随机地（但要小心地）挑一个。

### Universal method（全域法，理论上好的）

```math
h_{ab}(k) = (((ak + b) \bmod p) \bmod m)
```

- Hash family（哈希函数族）$\mathcal{H}(p, m) = \{h_{ab} \mid a, b \in \{0, \dots, p-1\},\ a \ne 0\}$。
- 由一个固定的素数 $p > u$ 参数化，$a$ 与 $b$ 从 $\{0, \dots, p-1\}$ 中选取。
- $\mathcal{H}$ 是一个 universal family（全域族），即对所有 $k_i \ne k_j \in \{0, \dots, u-1\}$ 都有

```math
\Pr_{h \in \mathcal{H}}\{h(k_i) = h(k_j)\} \le \frac{1}{m}
```

- 全域性为什么有用？它直接推出 chain 长度短——是在 expectation（期望）意义下短。
- 对 $h \in \mathcal{H}$ 定义 indicator random variable（指示随机变量）$X_{ij}$：
  - 若 $h(k_i) = h(k_j)$ 则 $X_{ij} = 1$，否则 $X_{ij} = 0$。
- index $h(k_i)$ 处 chain 的长度是 random variable $X_i = \sum_j X_{ij}$。
- 求 index $h(k_i)$ 处 chain 的 expected size：

```math
\mathbb{E}\{X_i\} = \mathbb{E}\left\{\sum_j X_{ij}\right\} = \sum_j \mathbb{E}\{X_{ij}\} = 1 + \sum_{j \ne i} \mathbb{E}\{X_{ij}\}
```

- 其中那个单独的 $1$ 来自 $j = i$（自己一定和自己碰撞，$X_{ii} = 1$）；继续展开 $j \ne i$ 的每一项：

```math
\mathbb{E}\{X_{ij}\} = (1)\Pr_{h \in \mathcal{H}}\{h(k_i) = h(k_j)\} + (0)\Pr_{h \in \mathcal{H}}\{h(k_i) \ne h(k_j)\}
```

- 代入全域性得 $\mathbb{E}\{X_{ij}\} \le 1/m$，于是

```math
\mathbb{E}\{X_i\} \le 1 + \sum_{j \ne i} \frac{1}{m} = 1 + \frac{n-1}{m}
```

- 又因为 $m = \Omega(n)$，所以 load factor（装载因子）$\alpha = n/m = O(1)$，故期望意义下是 $O(1)$！

## Dynamic（动态性）

- 若 $n/m$ 离 $1$ 很远，就用新随机选出的 hash function、按新 size $m$ 重建整张表。
- 这与 dynamic array 的 analysis 一样，重建的代价可以 amortize（摊还）到大量 dynamic operations 上。
- 于是 hash table 能在 expected amortized（期望摊还）$O(1)$ 时间内实现 dynamic set operations :) 

## 复杂度收尾对照表

原 PDF 的这张表同样是合并单元格排版，文字层只抽出部分数值。缺失格子按各结构的语义补全，并用 `†` 标注为推定值（不作原始断言）。

| Data Structure | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Sorted Array | $n\log n$ | $\log n$ | $n$ | $n$ | $1$ | $1$ | $\log n$ | $\log n$ |
| Direct Access Array | $u$ | $1$ | $1$ | $1^†$ | $u$ | $u$ | $u^†$ | $u^†$ |
| Hash Table | $n^{(e)}$ | $1^{(e)}$ | $1^{(a)(e)}$ | $1^{(a)(e)†}$ | $n$ | $n$ | $n^†$ | $n^†$ |

- 上标含义：$(e)$ = expected（期望意义下），$(a)$ = amortized（摊还意义下）。
- 关键结论：hash table 把「search 比 $\Theta(\log n)$ 更快」这件在 comparison model 下不可能的事做到了，代价是放弃 order 操作——`find_min` / `find_max` / `find_prev` / `find_next` 退化成 $\Theta(n)$ 的线性扫描。
- 这就是 set interface 里 Order 那一层的真实边界：一旦上了 hashing，键序信息就彻底丢了。
