# Introduction to Algorithms: 6.006

## <span style="color:#2471a3;">**[lecture]**</span> <span style="color:#c0392b">Lecture 8: Binary Heaps（二叉堆）</span>

Massachusetts Institute of Technology
Instructors: Erik Demaine, Jason Ku, and Justin Solomon

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Lecture 8 译注（对应视频：Binary Heaps）</span>

> 本讲主题：**Binary Heaps（二叉堆）**。从**Priority Queue（优先队列）** 接口出发，把「数组」重新解读为「complete binary tree（完全二叉树）」，引入**Max-Heap Property（最大堆性质）** 与向上/向下的 `max_heapify` 操作，实现 $O(\log n)$ 的插入与删除最大元；再把它套进「优先队列排序」框架得到**Heap Sort（堆排序）**，并用「Linear Build Heap（自底向上的线性建堆）」把建堆降到 $O(n)$，最后与 Sequence AVL Tree 对比。

---

## 1. Priority Queue Interface 优先队列接口
- **跟踪大量项，快速访问 / 删除「最重要的」那一个。**
- 例：带宽有限的路由器（router），必须给某些类型的报文更高的优先级；
- 例：操作系统内核里的**process scheduling（进程调度）**；
- 例：**discrete-event simulation（离散事件模拟）**——下一个要发生的事件是什么？
- 例：图算法（graph algorithms，本课程后面会讲）。
- 按 `key = priority`（键 = 优先级）给项排序，因此是 **Set interface（集合接口）**，而不是 **Sequence interface（序列接口）**。
- 针对 Set 操作的某个子集做了优化：
| 操作 | 含义 |
|---|---|
| `build(X)` | 从可迭代对象 X 构建优先队列 |
| `insert(x)` | 把项 x 加入数据结构 |
| `delete_max()` | 删除并返回键最大的那个项 |
| `find_max()` | 返回键最大的那个项 |
- （通常只为「最大」或「最小」之一做优化，很少同时两者。）
- **重点放在 `insert` 与 `delete_max` 两个操作上**：`build` 可以靠反复 `insert` 实现；`find_max()` 也可以由 `insert(delete_max())` 实现（删了再放回去）。

  这里的关键是 `delete_max()` 的返回值语义：它是「删除**并返回**」那个键最大的项。因此 `insert(delete_max())` 的完整意思是——先由 `delete_max()` 把最大项从队列中取出、**并把它的值交回给你**，随即 `insert` 再把这个返回值原样放回队列。净效果是队列内容不变，但你借这一步拿到了「最大项的值」，这恰好就是 `find_max()` 要返回的东西。换句话说，`delete_max()` 的返回值被当成了 `find_max()` 的输出，而 `insert` 的作用只是把被删的项归位、不破坏队列。所以「删了再放回」并非无意义的空操作：**删除不是目的，取出那个值才是**，插回只是为了让「没有真正少元素」的查询语义成立。需要强调的是，这只是说明 `find_max` 能由更基础的 `insert` 与 `delete_max` **复合出来**（正如 `build` 能由反复 `insert` 复合出来），并不代表实际会这样实现——它要真的删、再插，比直接实现的 `find_max` 多付出一倍代价，所以「可以实现」不等于「推荐这样实现」。

### 核心概念定义
> **定义（priority queue，优先队列）**：一种集合型数据结构，每次操作只关心「键值最大（或最小）」的那个元素，支持插入、删除最大/最小元、查询最大/最小元。可判定标准：它暴露的是 `insert` / `delete_max`（或 `find_max`）这类「按优先级取元素」的接口，而不是「按下标随机访问」的接口。
> **定义（interface，接口）**：一个数据结构对外承诺支持的一组操作（方法签名 + 各自的时间复杂度语义）。Set interface 只关心「元素是否在集合里、按键比较」，不关心元素间的先后次序；Sequence interface 才关心元素的顺序。这是贯穿 6.006 的分类视角。

设 $T(k)$ 为从某节点向下修复、且该节点到其子树最深叶子的距离为 $k$ 时，`delete_max` 的修复过程所花的时间。向下修复每向下走一层，都做常数次比较与交换（常数时间）；最坏情况下修复会一路走到叶子，沿途共走 $k$ 层，所以 $T(k)=O(k)$。又因为整棵树的高度 $h$ 满足 $k\le h$，且 $h=O(\log n)$（$n$ 为元素个数），于是 $T(k)=O(\log n)$——这给出的是**上界**。

下界同样成立：存在一种最坏输入，使修复路径确实走满 $k$ 层（例如删掉根之后，新的根要一路下沉到叶子才满足堆性质）。这时每向下一层至少也要做常数次操作，故 $T(k)=\Omega(k)$。上下界都以 $k$ 为界，合起来即 $T(k)=\Theta(k)$。而在高度平衡的实现里，树高既不超过 $\Theta(\log n)$、也能达到 $\Theta(\log n)$，即 $k=\Theta(\log n)$，代入得 $T(k)=\Theta(\log n)$。

因此 `delete_max` 的运行时间**与树的高度成正比**——「运行时间是树的高度」这一表述并不严谨，因为时间是时间、高度是长度，二者量纲不同，准确说法是时间**正比于**高度。在高度平衡的实现中，这个高度为 $\Theta(\log n)$，故 `delete_max` 的运行时间是 $\Theta(\log n)$。

## 2. Priority Queue Sort 优先队列排序
- 任何一个优先队列数据结构都能「翻译」成一个排序算法：
- `build(A)`——例如按输入顺序一个一个 `insert`；
- 反复 `delete_min()`（或 `delete_max()`）来确定（反向的）有序顺序。
- 所有「难活」都藏在数据结构内部。
- 运行时间是 $T_{\text{build}} + n \cdot T_{\text{delete\_max}} \le n \cdot T_{\text{insert}} + n \cdot T_{\text{delete\_max}}$。
  - 这里 $T_{\text{build}}$ 指把 $n$ 个元素构造成优先队列（执行 `build(A)`）的总代价，$T_{\text{insert}}$ 指一次 `insert` 的代价，$T_{\text{delete\_max}}$ 指一次 `delete_max()` 的代价。
  - 不等式中间那一步 $T_{\text{build}} \le n \cdot T_{\text{insert}}$ 成立，是因为 `build` 的实现方式就是「按输入顺序把 $n$ 个元素逐个 `insert` 进去」，于是建队总代价不会超过做 $n$ 次 `insert` 的代价。
- 我们已经见过的很多排序算法，都可以看成一种「优先队列排序」：
| Priority Queue 优先队列 | Operations $O(\cdot)$ | | | Priority Queue Sort 优先队列排序 | |
|---|---|---|---|---|---|
| Data Structure 数据结构 | `build(A)` | `insert(x)` | `delete_max()` | Time 时间 | In-place? 原地？ |
| Dynamic Array 动态数组 | $n$ | $1^{(a)}$ | $n$ | $n^2$ | Y |
| Sorted Dynamic Array 有序动态数组 | $n\log n$ | $n$ | $1^{(a)}$ | $n^2$ | Y |
| Set AVL Tree 集合 AVL 树 | $n\log n$ | $\log n$ | $\log n$ | $n\log n$ | N |
| **Goal 目标** | $n$ | $\log n^{(a)}$ | $\log n^{(a)}$ | $n\log n$ | Y |
> 上表是打散后的原文表格重建。四行分别对应四种「优先队列排序」：动态数组 → **Selection Sort（选择排序）**；有序动态数组 → **Insertion Sort（插入排序）**；集合 AVL 树 → **AVL Sort（AVL 排序）**；而最后一行是我们要达成的目标——`build` $O(n)$、`insert`/`delete_max` 平摊 $O(\log n)$、总时间 $O(n\log n)$ 且原地（In-place），这正好是 **堆排序（Heap Sort）** 的性能。
>
> 表中 `(a)` 表示平摊（amortized）代价：动态数组 `insert` 靠扩容均摊为 $O(1)$，有序动态数组 `delete_max` 靠从尾部删为 $O(1)$。`n^2` 的来源：$n \cdot T_{\text{insert}} + n \cdot T_{\text{delete\_max}}$，对动态数组是 $n\cdot 1 + n\cdot n = O(n^2)$，对有序动态数组是 $n\cdot n + n\cdot 1 = O(n^2)$。
---

## 3. Priority Queue: Set AVL Tree 用集合 AVL 树实现优先队列
- **Set AVL 树**支持 `insert(x)`、`find_min()`、`find_max()`、`delete_min()`、`delete_max()`，每操作 $O(\log n)$ 时间。
- 因此优先队列排序运行时间为 $O(n\log n)$。
- 这（本质上）就是第 7 讲的 AVL 排序。
- 可以通过**subtree augmentation（子树增强）** 把 `find_min()` / `find_max()` 加速到 $O(1)$ 时间。
- 但这个数据结构很复杂，而且得到的排序是 **in-place（原地）** 的。
- 有没有一个更简单、专为优先队列设计、并且是原地 $O(n\lg n)$ 排序的数据结构？
- **有的——binary heap（二叉堆）和堆排序（heap sort）。**
- 本质做法：**在一个 Sequence 数据结构（数组）之上实现一个 Set 数据结构**，用我们学过的二叉树知识。
### Priority Queue: Array 用数组实现优先队列
- 把元素存在一个**unordered（无序）动态数组**里。
- `insert(x)`：把 x 追加到末尾，平摊 $O(1)$ 时间。
- `delete_max()`：花 $O(n)$ 找最大，把它换到末尾再删掉。
- `insert` 很快，但 `delete_max` 很慢。
- 这种优先队列排序就是**选择排序**！（外加一些拷贝。）
### Priority Queue: Sorted Array 用有序数组实现优先队列
- 把元素存在一个**sorted（有序）动态数组**里。
- `insert(x)`：把 x 追加到末尾，再向下换到有序位置，$O(n)$ 时间。
- `delete_max()`：从末尾删，平摊 $O(1)$。
- `delete_max` 很快，但 `insert` 很慢。
- 这种优先队列排序就是**插入排序**！（外加一些拷贝。）
- **能否在这两种「数组优先队列」的两个极端之间找到一个折中？**
---

## 4. Array as a Complete Binary Tree 把数组看成完全二叉树

- **Idea（一句话本质）**：把一个数组解释成一颗**完全二叉树（complete binary tree）**——除最大深度那层外，第 $i$ 层至多有 $2^i$ 个节点；最大深度那层的所有节点都**left-aligned（左对齐）**。
- 等价地说：完全树是「按阅读顺序（root to leaves, left to right，从根到叶、从左到右）稠密填满」的。
- 视角：**数组与完全二叉树之间存在双射（bijection）**。
- 例：$Q = [0,1,2,3,4,5,6,7,8,9]$，按下标从 0 起按层填充：

| 深度 | 下标 | 对应节点 |
|---|---|---|
| $d_0$ | 0 | 0 |
| $d_1$ | 1, 2 | 1, 2 |
| $d_2$ | 3, 4, 5, 6 | 3, 4, 5, 6 |
| $d_3$ | 7, 8, 9 | 7, 8, 9 |

![图 3-1：完全二叉树按层填充的节点位（d0 起四层）](data:image/png;base64,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)
**图 3-1**：第 $i$ 层恰好容纳 $2^i$ 个节点位（$d_0$ 一个、$d_1$ 两个、$d_2$ 四个、$d_3$ 从八个起始位），而且只有在最深层才允许缺位，且缺的位必在右侧——所以「left-aligned（左对齐）」不是排版约定，而是「数组下标连续」这一算术事实的几何投影。Layer $i$ holds exactly $2^i$ slots, and the last level is filled from the left only.

![图 3-2：$Q=[0,1,\dots,9]$ 按层读出即得树形](_assets/lec08_fig_3_2.png)
**图 3-2**：把 $Q=[0,1,\dots,9]$ 按层（$d_0\to d_3$，层内从左到右）依次读出，就得到「$0$ 为根、$1,2$ 为其左右孩子、$3$–$6$ 为下一层、$7$–$9$ 为最深层」的唯一一棵树——即 $\mathrm{left}(i)=2i+1$、$\mathrm{right}(i)=2i+2$ 不是额外约定，而是「按层读数」这一条规则的必然推论。Reading the array level by level uniquely determines the tree, and hence the index arithmetic.

- $n$ 个项的数组，其「完全树视角」的高度是 $\lceil \lg n \rceil$，因此是一颗**balanced binary tree（平衡二叉树）**。

### Implicit Complete Tree 隐式完全树

- 完全二叉树的结构可以是**implicit（隐式的）**，不必存指针。
- 根在下标 0。
- 用下标算术计算邻居：

```math
\text{left}(i) = 2i + 1,\qquad \text{right}(i) = 2i + 2,\qquad \text{parent}(i) = \left\lfloor \frac{i-1}{2} \right\rfloor
```

> 上面三式是打散后的公式重建。`left(i) = 2i+1`、`right(i) = 2i+2`、`parent(i) = (i-1)/2`（向下取整，原文的 $\lfloor \cdot \rfloor$ 与换行被 PDF 拆散，此处按「根为 0、左孩子 $2i+1$」的标准 0 基下标约定还原）。**自检**：代入 $i=0$，`left(0)=1`、`right(0)=2`，`parent(1)=⌊0/2⌋=0`、`parent(2)=⌊1/2⌋=0`，三者衔接一致——孩子 $1,2$ 的父正是根 $0$。

---

## 5. Binary Heaps 二叉堆

- **Idea（一句话本质）**：让较大的元素在树中**位置更高**，但只要求「局部」满足即可。
- **Max-Heap Property（最大堆性质）在节点 i 处**：$Q[i] \ge Q[j]$，对所有 $j \in \{\text{left}(i), \text{right}(i)\}$。
- **max-heap（最大堆）** 是一个在所有节点处都满足最大堆性质的数组。
- **Claim（命题）**：在最大堆中，每个节点 i 满足 $Q[i] \ge Q[j]$，对所有位于 $\text{subtree}(i)$ 中的节点 j。
- **Proof（证明）**：
  - 对 $d = \text{depth}(j) - \text{depth}(i)$ 做归纳。
  - 基例：$d = 0$ 意味着 $i = j$，于是 $Q[i] \ge Q[j]$（事实上相等）。
  - 归纳步：$\text{depth}(\text{parent}(j)) - \text{depth}(i) = d - 1 \lt  d$，由归纳假设得 $Q[i] \ge Q[\text{parent}(j)]$；
  - 再由 $\text{parent}(j)$ 处的最大堆性质得 $Q[\text{parent}(j)] \ge Q[j]$。
- 特别地，最大元素在最大堆的根处。

### 核心概念定义

> **定义（Max-Heap Property，最大堆性质）**：对每个节点 $i$，其键值不小于它的每一个孩子。可判定标准：逐个检查所有非叶节点，看是否「父 ≥ 子」恒成立。它是「全局最大在根」这一结论的充分条件，而非对任意节点都「比所有后代大」的直接要求——那是上面 Claim 推出的推论。

> **定义（invariant，不变式 / 循环不变式）**：在算法执行过程中始终成立、且能用来证明正确性的一个性质。可判定标准：它在进入循环前成立、每一轮迭代后仍成立、循环结束时蕴含目标结论。下文 `max_heapify_up` / `max_heapify_down` 的正确性正是靠「堆性质在其余节点处始终成立」这一不变式。

---

## 6. Heap Insert 堆插入

- **Idea（一句话本质）**：把新元素放到数组末尾（下一个叶子位），再沿「向上」方向与父节点比较、必要时交换，直到最大堆性质恢复。

- 把新项 x 追加到数组末尾（平摊 $O(1)$），让它成为阅读顺序里的下一个叶子 i。
- `max_heapify_up(i)`：与父节点交换，直到最大堆性质成立。
  - 检查 $Q[\text{parent}(i)] \ge Q[i]$ 是否成立（这是 $\text{parent}(i)$ 处最大堆性质的一部分）；
  - 若不成立，交换 $Q[i]$ 与 $Q[\text{parent}(i)]$，然后递归调用 `max_heapify_up(parent(i))`。

### Pseudocode（伪代码）

```math
\begin{aligned}
&\textbf{def}\;\text{max\_heapify\_up}(A, i):\\
&\qquad p \leftarrow \text{parent}(i) = \left\lfloor \frac{i-1}{2} \right\rfloor\\
&\qquad \textbf{if}\;\; i > 0 \;\;\textbf{and}\;\; A[i] > A[p]:\\
&\qquad\qquad \text{swap}\; A[i],\, A[p]\\
&\qquad\qquad \text{max\_heapify\_up}(A, p)
\end{aligned}
```

### 正确性论证（循环不变式 / 归纳假设）

> **不变式**：除了「可能破坏性质的那一个节点」外，树的其余所有节点都满足最大堆性质。
>
> - 初始（刚 `append` 完）：新节点 i 是叶子，它插入前原数组是合法最大堆；现在只有 i 可能「比它的祖先大」，其余节点性质不变。不变式成立。
> - 归纳步：假设当前只有节点 $v$ 可能大于它的祖先。若 $A[\text{parent}(v)] \ge A[v]$，则 $v$ 处性质也恢复，全树合法，结束；否则交换 $A[v]$ 与 $A[\text{parent}(v)]$。交换后，$v$ 的原位置拿到的是「比原 $v$ 更大」的父元素，故 $v$ 的孩子仍被它支配；而「可能大于祖先」的节点从 $v$ 变成了 $\text{parent}(v)$——不变式随之推进到上一层。
> - 终止：当 $v$ 成为根，或 $A[\text{parent}(v)] \ge A[v]$ 时，全树满足最大堆性质。归纳得证。

### 复杂度分析

每次递归最多向上走一层，递归深度不超过树高 $h = \lceil \lg n \rceil$（完全二叉树的平衡性保证）。设 $T(k)$ 为从深度 $k$ 的节点向上修复的代价，则递推式：

```math
T(k) \;=\; T(k-1) + O(1),\qquad T(0) = O(1)
```

直接展开：$T(k) = T(0) + k\cdot O(1) = O(k)$。而 $k \le h = O(\log n)$，故：

```math
T(n) = O(\log n) = \Theta(\log n)
```

所以 `insert` 的运行时间是**树的高度**，即 $\Theta(\log n)$！

---

## 7. Heap Delete Max 堆删除最大元
- **Idea（一句话本质）**：最大键在根，但动态数组只能方便地删「最后一个元素」——于是把根与末元素交换、删掉末尾，再把「换下来的元素」（即原在末尾、被移到根的那个元素）沿向下方向与较大的孩子交换，直到最大堆性质恢复。
- 动态数组只能方便地删最后一个元素，但最大键在树的根。
- 所以把根节点 $i = 0$ 处的项，与堆数组中最后一个节点 $n-1$ 处的项交换。
- `max_heapify_down(i)`：把根与较大的孩子交换，直到最大堆性质成立。
- 检查 $Q[i] \ge Q[j]$ 是否对 $j \in \{\text{left}(i), \text{right}(i)\}$ 都成立（$i$ 处的最大堆性质）；
- 若不成立，把 $Q[i]$ 与键最大的那个孩子 $Q[j]$（$j \in \{\text{left}(i), \text{right}(i)\}$）交换，然后递归调用 `max_heapify_down(j)`。
### Pseudocode（伪代码）
```math
\begin{aligned}
&\textbf{def}\;\text{max\_heapify\_down}(A, i, n):\\
&\qquad l \leftarrow 2i+1,\quad r \leftarrow 2i+2\\
&\qquad \textbf{if}\;\; l < n \;\;\textbf{and}\;\; A[l] > A[i]:\\
&\qquad\qquad j \leftarrow l\\
&\qquad \textbf{else:}\;\; j \leftarrow i\\
&\qquad \textbf{if}\;\; r < n \;\;\textbf{and}\;\; A[r] > A[j]:\\
&\qquad\qquad j \leftarrow r\\
&\qquad \textbf{if}\;\; j \neq i:\\
&\qquad\qquad \text{swap}\; A[i],\, A[j]\\
&\qquad\qquad \text{max\_heapify\_down}(A, j, n)
\end{aligned}
```
### 正确性论证（循环不变式 / 归纳假设）
> **不变式**：除了「可能被下移的那个节点」外，树的其余节点都满足最大堆性质。
>
> 这里「可能被下移的那个节点」指的就是 Idea 里说的「换下来的元素」——即根与末元素交换后、从原来根的位置开始一路往下换的那个元素。它和被删除的根的关系是：被删除的是原来就在根上的最大键，交换后随末元素一起移到数组末尾、离开堆；而「换下来的元素」本是数组末尾的项，交换后被移到了根，成为这棵树上唯一可能比后代小的元素。整棵树上唯一可能违反最大堆性质的，始终只是这个元素当前所在的那一个节点。
>
> - 初始（把根与末元素交换后）：「换下来的元素」此刻在根处，只有它可能比自己的某些后代小；删去的末元素（即原来的最大键）已离开堆。不变式成立。
> - 归纳步：设当前只有节点 $i$ 可能小于它的后代。若 $Q[i] \ge Q[\text{left}(i)], Q[\text{right}(i)]$，则 $i$ 处性质恢复，结束；否则设 $j$ 是 $i$ 的键最大的孩子，交换 $Q[i]$ 与 $Q[j]$。交换后，$i$ 拿到的是「比原 $Q[i]$ 更大的孩子」，故 $i$ 处性质恢复；而「可能小于后代」的节点变成了 $j$，不变式推进到下一层。
> - 终止：当 $i$ 是叶子，或 $Q[i]$ 已不小于两个孩子时，全树满足最大堆性质。归纳得证。
### 复杂度分析
每次递归最多向下走一层，深度不超过树高 $h = O(\log n)$。设 $T(k)$ 为从某节点向下修复（其下方还有 $k$ 层）的代价，递推式：
```math
T(k) \;=\; T(k-1) + O(1),\qquad T(0) = O(1)
```
展开得 $T(k) = O(k)$，而 $k \le h = O(\log n)$，故：
```math
T(n) = O(\log n) = \Theta(\log n)
```
所以 `delete_max` 的运行时间是**树的高度**，即 $\Theta(\log n)$！

## 8. Heap Sort 堆排序

- 把最大堆塞进「优先队列排序」框架，就得到一个新的排序算法。
- 运行时间是 $O(n\log n)$，因为每次 `insert` 和 `delete_max` 都只要 $O(\log n)$。
- 但通常会加入两个改进：

### In-place Priority Queue Sort 原地优先队列排序

- 最大堆 Q 是更大数组 A 的一个**prefix（前缀）**，用一个变量 $|Q|$ 记住有多少项属于堆。
- $|Q|$ 初始为 0，`insert` 后最终到 $|A|$，`delete` 后又回到 0。
- `insert()`：把数组中下标 $|Q|$ 处的下一项吸收进堆。
- `delete_max()`：把最大项移到末尾，然后通过 `|Q|` 减 1 把它「放弃」。
- 用「数组」做原地优先队列排序，恰是**选择排序**；
- 用「有序数组」做原地优先队列排序，恰是**插入排序**；
- 用「二叉最大堆」做原地优先队列排序，就是**堆排序**。

### Idea（算法思路）

> **Idea（一句话本质）**：不另开数组，而是把「待排序的数组 A」自己分成两段——前缀是堆、后缀是已排好的最大值区。`insert` 就是把前缀边界右移并 `max_heapify_up`；`delete_max` 就是把根换到前缀末尾、边界左移并 `max_heapify_down`。一遍「建堆 + 反复删最大」即可原地完成排序。

### Pseudocode（伪代码）

```python
def heap_sort(A):
    n = len(A)
    build_max_heap(A)            # 见下一节，O(n) 线性建堆
    for k in range(n - 1, 0, -1):
        swap(A[0], A[k])         # 把当前最大移到末尾
        max_heapify_down(A, 0, k)  # 对缩小的堆[0, k) 修复根，O(log n)
```

### 复杂度分析（含递推式）

设 $n$ 为元素个数。建堆 $T_{\text{build}} = O(n)$（下节证明），随后 $n-1$ 次 `delete_max`，每次 `max_heapify_down` 从根下潜、代价不超过树高 $O(\log n)$。总时间：

```math
T(n) \;=\; T_{\text{build}}(n) + \sum_{k=1}^{n-1} O(\log k) \;=\; O(n) + O(n\log n) \;=\; O(n\log n)
```

其中求和式由「每个 $k \le n$，故 $\log k \le \log n$」放大为 $(n-1)\cdot O(\log n) = O(n\log n)$。空间上只用 $O(1)$ 额外变量（前缀技巧），故**原地（in-place）**。

---

## 9. Linear Build Heap 线性建堆

- **Idea（一句话本质）**：不要「从空堆开始一个个向上插入」（那是 $O(n\log n)$），而是把整个数组从一开始就当作完全二叉树，然后从最后一个节点到根、自底向上地对每个节点做 `max_heapify_down`——叶子天然满足堆性质，只有内部节点需要下沉，而「下沉次数按高度计」的总和是线性的。

- 逐个 `insert` n 个项，会对 $i$ 从 $0$ 到 $n-1$（从根往下）调用 `max_heapify_up(i)`。最坏交换次数约为：

```math
\sum_{i=0}^{n-1} \text{depth}(i) \;=\; \sum_{i=0}^{n-1} \lg i \;=\; \lg(n!) \;\ge\; \frac{n}{2}\lg\frac{n}{2} \;=\; \Omega(n\lg n)
```

- **Idea（核心改进）**！从一开始就把整个数组当作完全二叉树，然后对 $i$ 从 $n-1$ 到 $0$（从叶往上）调用 `max_heapify_down(i)`。最坏交换次数约为：

```math
\sum_{i=0}^{n-1} \text{height}(i) \;=\; \sum_{i=0}^{n-1} (\lg n - \lg i) \;=\; \lg\!\left(\frac{n^n}{n!}\right) \;=\; \Theta\!\left(\lg\frac{n^n}{(n/e)^n}\right) \;=\; O(n)
```

- 所以可以 $O(n)$ 时间建堆。
- （但这并不会加速堆排序的 $O(n\lg n)$ 总性能。）

### 公式重建与自检

> 上面的两个求和式是 PDF 打散后的重建，按数学意义还原如下：
>
> 1. **自顶向下逐个插入**（`max_heapify_up`）：第 $i$ 个节点上浮的代价正比于它的深度 $\text{depth}(i)$。求和 $\sum_{i=0}^{n-1}\text{depth}(i)$ 由完全二叉树的结构给出 $\approx \sum \lg i = \lg(n!)$（因为深度约等于 $\lg i$）。用「后半因子」放缩：$n!$ 中后 $n/2$ 个因子都 $\ge n/2$，故 $n! \ge (n/2)^{n/2}$，于是 $\lg(n!) \ge \frac{n}{2}\lg\frac{n}{2} = \Omega(n\lg n)$。
>
> 2. **自底向上建堆**（`max_heapify_down`）：第 $i$ 个节点下沉的代价正比于它的高度 $\text{height}(i) = h - \text{depth}(i) \approx \lg n - \lg i$。求和：
>
> ```math
> \sum_{i=0}^{n-1}\text{height}(i) \;=\; \sum_{i=0}^{n-1}(\lg n - \lg i) \;=\; n\lg n - \lg(n!) \;=\; \lg\!\left(\frac{n^n}{n!}\right)
> ```
>
> 用 Stirling 近似 $n! \approx (n/e)^n$ 代入：$\lg(n^n/n!) \approx \lg(n^n/(n/e)^n) = \lg(e^n) = n\lg e = O(n)$。这正是原文 $\Theta(\lg\sqrt{\cdot})$ 碎片对应的含义（根号是打散造成的 $\lg$ 指数表示混乱，本质是 $\lg(n^n/n!)$）。
>
> **自检（代入边界验证两段衔接）**：$i$ 从根到叶，$\text{height}(i)$ 从 $h$ 递减到 $0$；$\lg n - \lg i$ 在 $i=1$ 时取 $\lg n$、在 $i=n-1$ 时取 $\lg(n/(n-1))\to 0$，与「根高度 $h=\lg n$、叶高度 0」的几何意义两端衔接一致。故重建无误，结论 $O(n)$ 成立。

---

## 10. Sequence AVL Tree Priority Queue 序列 AVL 树实现优先队列
- 我们还在哪里见过「一个对数级数据结构却拥有线性建堆时间」？**Sequence AVL Tree！**
- 把优先队列的项按任意顺序（插入顺序）存在 Sequence AVL Tree 里。
- 维护 **max（和/或 min）augmentation（增强）**：
- `node.max` = 指向「node 的子树中**键最大的节点**」的**指针**（注意：这个字段存的是指向该节点的指针，不是键值本身；要取最大键值时再通过该指针取 `node.max.key`）。
- 这是一个**subtree property（子树性质）**，因此只需常数因子的额外开销来维护。
- `find_min()` 与 `find_max()` 在 $O(1)$ 时间。
- `delete_min()` 与 `delete_max()` 在 $O(\log n)$ 时间。
- `build(A)` 在 $O(n)$ 时间。
- **与二叉堆有同样的界，而且更快地拿到极值：`find_min()`/`find_max()` 只需 $O(1)$（二叉堆同样 $O(1)$），而 `delete_min()`/`delete_max()`、`build(A)` 的界也与二叉堆一致；额外的收益是 Sequence AVL Tree 还能按位置做插入、删除、split、join 等序列操作，这是二叉堆做不到的。**
### 核心概念定义
> **定义（subtree augmentation，子树增强）**：给树的每个节点额外存一个「可由其子树信息递推算出的量」（这里是子树最大键的指针），插入/删除时只需沿根到该节点的路径 $O(\log n)$ 时间更新即可维持。可判定标准：该量只依赖节点的键与两个孩子的对应量，不依赖子树之外的信息。

## 11. Set vs. Multiset 集合与多重集
- 我们的 Set 接口假定**键不重复**，但可以用这些 Set 来实现允许重复键的 **Multiset（多重集）**：
- Set 中的每个项是一个 **Sequence（例如链表 linked list）**，用来存「键相同的那些 Multiset 项」，而该 Sequence 的键就是这一组项的键。
- 事实上，不做这个归约，二叉堆和 AVL 树也能**直接**处理重复键的项（例如 `delete_max` 删除「某个」最大键的项），只需注意用 $\le$ 约束（而不是 Set AVL 树里的 $\lt $）。
  - 这里的「Set AVL 树里的 $\lt$」指它作为二叉搜索树时的**二叉搜索树性质（BST property）**中的严格比较：对任意节点 $x$，左孩子键 $<$ $x$ 的键 $<$ 右孩子键，且整棵树**不允许出现键相等的两个节点**。这个严格小于是在 `insert` 和 `delete` 定位节点位置（判断该往左还是往右走）时用的比较约束。当要直接支持重复键时，就得把其中一侧的比较放宽成 $\le$（例如允许「键 $\le$ 父键」的项归到左子树），让相等的键也能被放进树里，`delete_max` 时只删掉其中一个即可。
### 核心概念定义
> **定义（multiset，多重集）**：允许同一元素出现多次的集合，元素按「键值」而非「身份」归类。可判定标准：`insert` 两个键相等的项后，两者都在结构里，`delete_max` 只删掉其中一个最大键的项。Set 到 Multiset 的归约，就是把「同一键的多个项」打包成一条 Sequence 挂在 Set 的一个槽位上。

## 附：本讲核心概念速查（首次出现的英文原名 + 中文 + 定义）

| 英文原名 | 中文 | 一句可判定的定义 |
|---|---|---|
| priority queue | 优先队列 | 只按键值大小取/删「最大（或最小）元」的集合型数据结构 |
| interface | 接口 | 数据结构对外承诺的一组操作及其时间复杂度语义 |
| Set interface | 集合接口 | 只关心元素存在性与按键比较、不关心先后次序的接口 |
| Sequence interface | 序列接口 | 关心元素先后次序（下标/顺序）的接口 |
| build | 建堆/构建 | 从可迭代输入一次性构造数据结构的操作 |
| process scheduling | 进程调度 | 操作系统按优先级决定 CPU 给哪个进程运行 |
| discrete-event simulation | 离散事件模拟 | 按时间戳维护事件队列、依次处理最早事件的模拟方法 |
| selection sort | 选择排序 | 反复选最大/最小元放到末尾的原地 $O(n^2)$ 排序 |
| insertion sort | 插入排序 | 反复把元素插入有序前缀的原地 $O(n^2)$ 排序 |
| subtree augmentation | 子树增强 | 给节点存一个可由子树信息递推算出的量并沿途维护 |
| complete binary tree | 完全二叉树 | 除最底层外每层满、最底层节点左对齐的二叉树 |
| bijection | 双射 | 两个集合元素间的一一对应关系 |
| balanced binary tree | 平衡二叉树 | 高度为 $O(\log n)$ 的二叉树 |
| implicit | 隐式的 | 用下标算术而非指针表示树结构的方式 |
| Max-Heap Property | 最大堆性质 | 每个节点键值不小于其所有孩子的性质 |
| max-heap | 最大堆 | 所有节点都满足最大堆性质的数组 |
| invariant | 不变式/循环不变式 | 算法执行中始终成立、可用来证正确性的性质 |
| max_heapify_up | 向上堆化 | 让节点与父比较交换、向上恢复堆性质 |
| max_heapify_down | 向下堆化 | 让节点与较大孩子交换、向下恢复堆性质 |
| heap sort | 堆排序 | 建最大堆后反复删最大元的原地 $O(n\log n)$ 排序 |
| prefix | 前缀 | 数组前 $|Q|$ 个元素构成的、充当堆的那一段 |
| linear build heap | 线性建堆 | 自底向上逐节点下潜、$O(n)$ 时间建堆 |
| height | 高度 | 节点到其子树最深叶的边数 |
| depth | 深度 | 根到节点的边数 |
| multiset | 多重集 | 允许元素重复、按键归类的集合 |

---

*MIT OpenCourseWare · https://ocw.mit.edu · 6.006 Introduction to Algorithms, Spring 2020*
