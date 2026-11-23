# Lecture 8: Binary Heaps（二叉堆）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Priority Queue Interface（优先队列接口）

- 目标：跟踪大量 items，并能快速访问 / 移除其中最重要的那个。
  - 例子：带宽受限的 router（路由器），必须对某几类 message 优先处理。
  - 例子：operating system kernel 里的 process scheduling（进程调度）。
  - 例子：discrete-event simulation（离散事件模拟）——下一个发生的事件是哪个？
  - 例子：graph algorithms（图算法，本课后半段会用到）。
- 用 key = priority（优先级）给 items 排序，所以这是一个 Set interface，而非 Sequence interface。
- 它只针对 Set operations 的一个特定子集做优化：

| Operation | 语义 |
|---|---|
| `build(X)` | 用 iterable $X$ 构造出这个 priority queue |
| `insert(x)` | 把 item $x$ 加入 data structure |
| `delete_max()` | 移除并返回 key 最大的 stored item |
| `find_max()` | 返回 key 最大的 stored item |

- 通常只针对 max 或 min 之一做优化，而不是两者同时。
- 本讲聚焦在 `insert` 与 `delete_max` 上：`build` 可以反复 `insert` 实现；`find_max()` 可以用 `insert(delete_min())` 的写法绕过去。

## Priority Queue Sort（优先队列排序）

- 任何 priority queue data structure 都能翻译成一个 sorting algorithm：
  - `build(A)`，例如按 input order 一个个 `insert`。
  - 反复 `delete_min()`（或 `delete_max()`），由此确定（逆序的）sorted order。
- 所有难活在 data structure 内部完成。
- Running time 是 $T_{\text{build}} + n\cdot T_{\text{delete\_max}} \le n\cdot T_{\text{insert}} + n\cdot T_{\text{delete\_max}}$。
- 我们此前见过的很多 sorting algorithms 都能看成 priority queue sort：

| Priority Queue Data Structure | `build(A)` | `insert(x)` | `delete_max()` | Sort 的 Time | In-place? | 对应的 Sort |
|---|---|---|---|---|---|---|
| Dynamic Array | $n$ | $1^{(a)}$ | $n$ | $n^2$ | 是 | Selection Sort |
| Sorted Dynamic Array | $n\log n$ | $n$ | $1^{(a)}$ | $n^2$ | 是 | Insertion Sort |
| Set AVL Tree | $n\log n$ | $\log n$ | $\log n$ | $n\log n$ | 否 | AVL Sort |
| Goal | $n$ | $\log n^{(a)}$ | $\log n^{(a)}$ | $n\log n$ | 是 | Heap Sort |

> 表注：$(a)$ = amortized。原 PDF 为合并单元格排版，文字层把 $n^2$ 拆成 `2` 与 `n` 两行、把四个 Sort 名字另起一列；上表按语义合并成完整行。「对应的 Sort」一列原文在表下方单独列出（Selection Sort / Insertion Sort / AVL Sort / Heap Sort），这里按行对齐填入，标 `†` 的对应关系为推定。

## Priority Queue: Set AVL Tree（用 Set AVL tree 做优先队列）

- Set AVL tree 支持 `insert(x)`、`find_min()`、`find_max()`、`delete_min()`、`delete_max()`，每个 operation 都是 $O(\log n)$。
- 于是 priority queue sort 跑 $O(n\log n)$ 时间。
  - 这（基本上）就是 Lecture 7 的 AVL Sort。
- 还能靠 subtree augmentation 把 `find_min()` 与 `find_max()` 加速到 $O(1)$。
- 但这个 data structure 太复杂，而且得到的 sort 不是 in-place 的。
- 那么，有没有一个只服务 priority queue 的更简单结构，同时能给出 in-place 的 $O(n\lg n)$ sort？
- 有：binary heap（二叉堆）与 heap sort。
- 它的本质是：在一个 Sequence data structure（array）之上，借用我们已经学过的 binary tree 知识，去实现一个 Set data structure。

## Priority Queue: Array（用无序 array 做优先队列）

- 把 elements 存在一个 unordered dynamic array 里。
- `insert(x)`：把 $x$ append 到末尾，amortized $O(1)$。
- `delete_max()`：$O(n)$ 找出 max，把 max swap 到末尾再删掉。
- `insert` 快，但 `delete_max` 慢。
- 此时的 priority queue sort 就是 selection sort！（外加一些 copying）

## Priority Queue: Sorted Array（用有序 array 做优先队列）

- 把 elements 存在一个 sorted dynamic array 里。
- `insert(x)`：append 到末尾，再反复 swap 下移到 sorted position，$O(n)$。
- `delete_max()`：从末尾删除，$O(1)$ amortized。
- `delete_max` 快，但 `insert` 慢。
- 此时的 priority queue sort 就是 insertion sort！（外加一些 copying）
- 那么，能不能在这两个 array 极端之间找到一个折中？

## Array as a Complete Binary Tree（把 array 看成完全二叉树）

- Idea：把 array 解释成一棵 complete binary tree（完全二叉树），第 $i$ 层最多有 $2^i$ 个 node，只有最大那一层的 nodes 是左对齐（left-aligned）的。
- 等价说法：complete tree 是按 reading order（阅读序）密集填满的——从 root 到 leaves、从左到右。
- 这是一个视角转换：arrays 与 complete binary trees 之间存在 bijection（双射）。

```text
Q = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   对应树形：
              0            <- d0
            /   \
           1     2         <- d1
          / \   / \
         3   4 5   6       <- d2
        / \
       7   8 ... 9（9 是 4 的左子）
```

[Figure 1：array 下标与 complete binary tree 的对应。原文用 ASCII 画法分四行给出 d0..d3 各层的 nodes，并在左侧标出 `Q = [0,1,2,3,4,5,6,7,8,9]` 与每层在 array 中的区间（d0 是 `0`；d1 是 `1 2`；d2 是 `3 4 5 6`；d3 是 `7 8 9`）。树形按 left-to-right reading order 填充，因此最后一层只有三个 node 且靠左]

- 从 complete tree 这个视角看，含 $n$ 个 item 的 array 的 height 是 $\lceil \lg n\rceil$，所以它就是一棵 balanced binary tree。

## Implicit Complete Tree（隐式完全二叉树）

- complete binary tree 的结构可以完全是 implicit（隐式）的，不必存 pointers。
- root 在 index 0。
- 用 index arithmetic（下标算术）就能算出邻居：
  - `left(i) = 2i + 1`
  - `right(i) = 2i + 2`
  - `parent(i) = floor((i - 1) / 2)`

```math
\mathrm{parent}(i) = \left\lfloor \frac{i-1}{2} \right\rfloor
```

- 这是本讲所有魔法的来源：**指针被下标算术替代了**，于是「树形结构」不花任何存储代价，而且父子关系可在 $O(1)$ 内算出。

## Binary Heaps（二叉堆）

- Idea：让较大的 elements 待在 tree 中较高的位置，但只要求 locally（局部地）成立。
- Max-Heap Property（最大堆性质）在 node $i$ 上：对所有 $j \in \{\mathrm{left}(i), \mathrm{right}(i)\}$ 都有 $Q[i] \ge Q[j]$。
- Max-heap（最大堆）就是「在所有 nodes 上都满足 max-heap property」的一个 array。
- Claim：在一个 max-heap 中，每个 node $i$ 都满足：对 `subtree(i)` 里所有 nodes $j$ 有 $Q[i] \ge Q[j]$。
- Proof：
  - 对 $d = \mathrm{depth}(j) - \mathrm{depth}(i)$ 做 induction。
  - Base case：$d = 0$ 意味着 $i = j$，于是 $Q[i] \ge Q[j]$（其实相等）。
  - 因为 $\mathrm{depth}(\mathrm{parent}(j)) - \mathrm{depth}(i) = d-1 < d$，由 induction 得 $Q[i] \ge Q[\mathrm{parent}(j)]$。
  - 又由 $\mathrm{parent}(j)$ 处的 Max-Heap Property 得 $Q[\mathrm{parent}(j)] \ge Q[j]$。
- 特别地，max item 一定在 max-heap 的 root 处。

## Heap Insert（堆插入）

- 花 amortized $O(1)$ 把新 item $x$ append 到 array 末尾，使它成为 reading order 里的下一个 leaf $i$。
- `max_heapify_up(i)`：与 parent 反复 swap，直到满足 Max-Heap Property。
  - 检查是否有 $Q[\mathrm{parent}(i)] \ge Q[i]$（这是 $\mathrm{parent}(i)$ 处 Max-Heap Property 的一部分）。
  - 若不成立，就 swap $Q[i]$ 与 $Q[\mathrm{parent}(i)]$，然后递归 `max_heapify_up(parent(i))`。
- Correctness：
  - Max-Heap Property 保证所有 nodes $\ge$ 其 descendants，唯一可能被破坏的是 $Q[i]$ 可能大于它的某些 ancestors（除非 $i$ 就是 root，那就已经完事了）。
  - 若需要 swap，同一个保证在把 $Q[i]$ 换成 $Q[\mathrm{parent}(i)]$ 之后依然成立。
- Running time：tree 的 height，所以是 $\Theta(\log n)$！

## Heap Delete Max（堆删除最大值）

- dynamic array 只能轻易移除最后一个 element，但 max key 在 tree 的 root 上。
- 所以先把 root node $i = 0$ 的 item 与 heap array 里 node $n-1$ 的最后一个 item 交换。
- `max_heapify_down(i)`：把 root 与更大的那个 child 反复 swap，直到满足 Max-Heap Property。
  - 检查是否有 $Q[i] \ge Q[j]$ 对所有 $j \in \{\mathrm{left}(i), \mathrm{right}(i)\}$（即 $i$ 处的 Max-Heap Property）。
  - 若不成立，就在 $\{\mathrm{left}(i), \mathrm{right}(i)\}$ 里挑 key 最大的那个 child $j$，swap $Q[i]$ 与 $Q[j]$，然后递归 `max_heapify_down(j)`。
- Correctness：
  - Max-Heap Property 保证所有 nodes $\ge$ 其 descendants，唯一可能被破坏的是 $Q[i]$ 可能小于它的某些 descendants（除非 $i$ 是 leaf，那就已经完事了）。
  - 若需要 swap，同一个保证在把 $Q[i]$ 换成 $Q[j]$ 之后依然成立。
- Running time：tree 的 height，所以是 $\Theta(\log n)$！

## Heap Sort（堆排序）

- 把 max-heap 插进 priority queue sort，就得到一个新的 sorting algorithm。
- Running time 是 $O(n\log n)$，因为每次 `insert` 与 `delete_max` 都花 $O(\log n)$。
- 但这个算法通常还会带上两处改进：

### In-place Priority Queue Sort（原地优先队列排序）

- Max-heap $Q$ 是更大 array $A$ 的一个 prefix，另外记住有多少 items $|Q|$ 属于 heap。
- $|Q|$ 初始为 0；`insert` 阶段结束后变成 $|A|$；`delete` 阶段结束后又回到 0。
- `insert()` 把 array 中 index $|Q|$ 处的下一个 item 吸收进 heap。
- `delete_max()` 把 max item 挪到末尾，然后通过递减 $|Q|$ 把它「放弃」掉。
- 用 Array 做 in-place priority queue sort，恰好就是 Selection Sort。
- 用 Sorted Array 做 in-place priority queue sort，恰好就是 Insertion Sort。
- 用 binary Max Heap 做 in-place priority queue sort，就是 Heap Sort。
- 这条对应关系很值得记住：**三个 sort 的差别只在 priority queue 的实现**，排序骨架完全一样。

## Linear Build Heap（线性建堆）

- 把 $n$ 个 items 逐个 `insert` 进 heap，会对 $i$ 从 0 到 $n-1$（从 root 往下）调用 `max_heapify_up(i)`：

```math
\text{worst-case swaps} \approx \sum_{i=0}^{n-1}\mathrm{depth}(i) = \sum_{i=0}^{n-1}\lg i = \lg(n!) \ge (n/2)\lg(n/2) = \Omega(n\lg n)
```

- Idea！一开始就把整个 array 当成一棵 complete binary tree，然后对 $i$ 从 $n-1$ 到 0（从 leaves 往上）调用 `max_heapify_down(i)`：

```math
\text{worst-case swaps} \approx \sum_{i=0}^{n-1}\mathrm{height}(i) = \sum_{i=0}^{n-1}(\lg n - \lg i) = \lg\frac{n^n}{n!} = \Theta\left(\lg\frac{n^n}{n(n/e)^n}\right) = O(n)
```

- 所以 heap 可以在 $O(n)$ 时间内建好。
- （但这并不会改善 heap sort 的 $O(n\lg n)$ 总体性能。）
- 两个求和式的差别值得看清：按 depth 求和时绝大多数 nodes 都在深层、每个贡献 $\lg n$；按 height 求和时绝大多数 nodes 都在浅层、每个贡献小常数。**求和方向决定了总和的两个不同量级**，这是线性建堆的全部内容。

## Sequence AVL Tree Priority Queue（用 Sequence AVL tree 做优先队列）

- 在线性 build time 这件事上，我们还在别处见过另一个「原本是 logarithmic 的 data structure」吧？
- 就是 Sequence AVL Tree！
- 把 priority queue 的 items 按 arbitrary order（也就是 insertion order）存进 Sequence AVL Tree。
- 维护一个 max（和 / 或 min）augmentation：

```text
node.max = 指向 node 的 subtree 中 key 最大的那个 node 的指针
```

- 这是一个 subtree property，所以维护它只增加常数因子开销。
- `find_min()` 与 `find_max()` 于是花 $O(1)$ 时间。
- `delete_min()` 与 `delete_max()` 花 $O(\log n)$ 时间。
- `build(A)` 花 $O(n)$ 时间。
- 与 binary heaps 的 bounds 完全一样（而且还多给了别的 operation）。

## Set vs. Multiset（集合与多重集）

- 我们的 Set interface 假设没有 duplicate keys，但可以用这些 Sets 去实现允许 duplicate keys 的 Multiset：
  - Set 里每个 item 是一个 Sequence（例如 linked list），这个 Sequence 存放 Multiset 中 key 相同的那些 items，而 Sequence 的 key 就是那个共享的 key。
- 事实上，不做这层归约，binary heaps 与 AVL trees 也能直接处理 duplicate-key items（此时 `delete_max` 删掉「某个」key 最大的 item），只要注意把约束写成 $\le$ 而不是 Set AVL Tree 里的 $<$。
