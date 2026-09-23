# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk05 · 书页 163–202 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §6.5, p.163</span>

（接上页）

在第 23 章和第 24 章中，我们还将看到 min-priority queue（最小优先队列）的诸多其他用途，重点是 DECREASE-KEY 操作。

不出所料，我们也可以用 heap（堆）来实现 priority queue（优先队列）。在某个给定的 application（应用）中，例如 job scheduling（作业调度）或 event-driven simulation（事件驱动模拟），优先队列中的 elements（元素）对应于该应用中的 objects（对象）。我们经常需要确定是哪一个应用对象对应于某个给定的优先队列元素，反之亦然。因此，当我们用堆来实现优先队列时，常常需要在每个堆元素中存储一个指向相应应用对象的 handle（句柄）。句柄的确切构成（例如是一个 pointer（指针）还是一个整数）取决于具体应用。类似地，我们也需要在每个应用对象中存储一个指向相应堆元素的句柄，这里的句柄通常是一个 array index（数组下标）。由于堆元素在堆操作过程中会改变它们在数组中的位置，一个实际的实现在重新定位某个堆元素时，还必须更新相应应用对象中的数组下标。因为访问应用对象的细节高度依赖于具体应用及其实现，我们在此不打算深入这些细节，只是指出：在实践中，这些句柄确实需要得到正确的维护。

现在我们讨论如何实现 max-priority queue（最大优先队列）的各种操作。过程 HEAP-MAXIMUM 用 $\Theta(1)$ 时间实现了 MAXIMUM 操作：

```text
HEAP-MAXIMUM(A)
1  return A[1]
```

过程 HEAP-EXTRACT-MAX 实现 EXTRACT-MAX 操作。它与 HEAPSORT 过程的 for 循环体（第 3–5 行）很相似：

```text
HEAP-EXTRACT-MAX(A)
1  if A.heap-size < 1
2      error "heap underflow"
3  max = A[1]
4  A[1] = A[A.heap-size]
5  A.heap-size = A.heap-size - 1
6  MAX-HEAPIFY(A, 1)
7  return max
```

HEAP-EXTRACT-MAX 的 running time（运行时间）为 $O(\lg n)$，因为它在 MAX-HEAPIFY 的 $O(\lg n)$ 时间之上，只执行了 constant amount of work（常数量的工作）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把 HEAP-EXTRACT-MAX 与第 162 页的 HEAPSORT 循环体对照着看：两者做的是同一件事——"取走根上最大元、把最后一个叶子搬到根、再让 MAX-HEAPIFY 把它沉下去"。HEAPSORT 正是把这个动作循环 $n-1$ 次，才把整个数组从后往前"倒"成有序的。另外注意第 5 行 `A.heap-size = A.heap-size - 1` 是"缩小堆"而非"删除数组元素"：被抽取的最大值只是退出了堆的管理范围，仍留在数组的尾部——堆排序正是利用这一点让有序后缀与无序前缀共存于同一个数组中，不花额外空间。这种"逻辑尺寸与物理尺寸分离"的技巧（本书用属性 $A.\text{heap-size}$ 与 $A.\text{length}$ 区分）在后面第 10 章还会反复出现。

过程 HEAP-INCREASE-KEY 实现 INCREASE-KEY 操作。指向数组的一个 index（下标）$i$ 标识了我们想要增大其关键字的那个优先队列元素。该过程首先把元素 $A[i]$ 的关键字更新为它的 new value（新值）。因为增大 $A[i]$ 的关键字可能会违背 max-heap property（最大堆性质），……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.5, p.164</span>

（接上页）

该过程随后——颇令人回想起 Section 2.1 中 INSERTION-SORT 的 insertion loop（插入循环）（第 5–7 行）——从这个结点出发，沿一条 simple path（简单路径）向 root（根结点）遍历，为新近增大了的关键字寻找一个合适的位置。在 HEAP-INCREASE-KEY 沿这条路径上行的过程中，它反复地把一个元素与其 parent（父结点）比较：若该元素的关键字较大，则交换二者的关键字并继续上行；若该元素的关键字较小（即父结点更大），则终止——因为此时 max-heap property（最大堆性质）已经成立。（精确的 loop invariant（循环不变式）见 Exercise 6.5-5。）

```text
HEAP-INCREASE-KEY(A, i, key)
1  if key < A[i]
2      error "new key is smaller than current key"
3  A[i] = key
4  while i > 1 and A[PARENT(i)] < A[i]
5      exchange A[i] with A[PARENT(i)]
6      i = PARENT(i)
```

Figure 6.5（图 6.5）展示了一个 HEAP-INCREASE-KEY 操作的例子。在一个含 $n$ 个元素的堆上运行 HEAP-INCREASE-KEY 的 running time（运行时间）为 $O(\lg n)$，因为第 3 行所更新结点向上通往根结点的这条路径的长度为 $O(\lg n)$。

过程 MAX-HEAP-INSERT 实现 INSERT 操作。它的 input（输入）是要插入到 max-heap（最大堆）$A$ 中的那个新元素的 key（关键字）。该过程首先通过向树中添加一个新的 leaf（叶结点）来扩展最大堆，这个新叶子的关键字是 $-\infty$；然后它调用 HEAP-INCREASE-KEY，把这个新结点的关键字设置到正确的值，并维护最大堆性质。

```text
MAX-HEAP-INSERT(A, key)
1  A.heap-size = A.heap-size + 1
2  A[A.heap-size] = -∞
3  HEAP-INCREASE-KEY(A, A.heap-size, key)
```

在一个含 $n$ 个元素的堆上运行 MAX-HEAP-INSERT 的运行时间为 $O(\lg n)$。

总而言之，heap（堆）可以在 $O(\lg n)$ 时间内支持对规模为 $n$ 的集合的任何一种 priority-queue（优先队列）操作。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "先置 $-\infty$ 再增大"并非画蛇添足：第 2 行把新叶子设为 $-\infty$，是让这棵加了一个叶子的树立刻满足最大堆性质——$-\infty$ 不可能大于任何父结点；随后 HEAP-INCREASE-KEY 的第 1 行检查 `key < A[i]` 时，$-\infty$ 恰好保证任何合法的 key 都能通过（这正是 Exercise 6.5-4 追问的用意）。反过来看，"把过大值沿树下行"本应由 DECREASE-KEY（对最小堆）或 MAX-HEAPIFY 类过程完成；在最大堆上只靠"上行"就能恢复性质，是因为只有"增大"才会破坏最大堆序。INSERT 与 INCREASE-KEY 同为 $O(\lg n)$，代价都花在与树高同阶的路径上——这正是 Exercise 6.5-6 让你把上行路径上的三次赋值（exchange）优化为一次赋值（insertion-sort 式的"挖坑后移"）的原因。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**6.5-1**

Illustrate the operation of HEAP-EXTRACT-MAX on the heap $A = \langle 15, 13, 9, 5, 12, 8, 7, 4, 0, 6, 2, 1 \rangle$.

---

> <span style="color:#7f8c8d;">CLRS §6.5 + Figure 6.5, p.165</span>

> <span style="color:#7f8c8d;">[note] 本页为整页插图：图 6.5 用四棵二叉树 (a)–(d) 展示 HEAP-INCREASE-KEY 在图 6.4(a) 的最大堆 $A = \langle 16, 14, 10, 8, 7, 9, 3, 2, 4, 1 \rangle$ 上的操作，下标为 $i$ 的结点（关键值为 4 的叶子）以深色阴影标出；(b) 中该叶子的关键值被增大为 15；(c)、(d) 中 15 沿父结点路径逐级上浮，直到其父结点不小于它为止。箭头旁标注的是当前 $i$ 的位置。</span>

```text
(a) 初始配置（i = 9，A[i] = 4）         (b) 关键值增大为 15（i = 9）

            16                                    16
        /        \                            /        \
      14          10                        14          10
    /    \      /    \                    /    \      /    \
   8      7    9      3                  8      7    9      3
  / \    /                              / \    /
 2   4   1                             2  15   1
    (i)                                   (i)

(c) 第 4–6 行 while 循环一次迭代后      (d) 再一次迭代后（i = 2，
    （15 与父结点 8 交换，i = 4）            A[PARENT(i)] = 16 ≥ 15，终止）

            16                                    16
        /        \                            /        \
      14          10                      15(i)         10
    /    \      /    \                    /    \      /    \
 15(i)    7    9      3                 14      7    9      3
  / \    /                              / \    /
 2   8   1                             2   8   1
```

**Figure 6.5（图 6.5）** HEAP-INCREASE-KEY 的操作。(a) 图 6.4(a) 的 max-heap（最大堆），其中下标为 $i$ 的结点用深色阴影标出。(b) 该结点的关键值被增大到 15。(c) 在第 4–6 行 while 循环的一次迭代之后，该结点与其父结点交换了关键值，下标 $i$ 上移到父结点。(d) 再经过一次 while 循环迭代之后的最大堆。此时 $A[\mathrm{PARENT}(i)] \ge A[i]$，max-heap property（最大堆性质）成立，过程随之终止。

（接上页）

**6.5-2**

Illustrate the operation of MAX-HEAP-INSERT(A, 10) on the heap $A = \langle 15, 13, 9, 5, 12, 8, 7, 4, 0, 6, 2, 1 \rangle$.

**6.5-3**

Write pseudocode for the procedures HEAP-MINIMUM, HEAP-EXTRACT-MIN, HEAP-DECREASE-KEY, and MIN-HEAP-INSERT that implement a min-priority queue with a min-heap.

**6.5-4**

Why do we bother setting the key of the inserted node to $-\infty$ in line 2 of MAX-HEAP-INSERT when the next thing we do is increase its key to the desired value?

---

> <span style="color:#7f8c8d;">CLRS §6.5 / Problems, p.166</span>

**6.5-5**

Argue the correctness of HEAP-INCREASE-KEY using the following loop invariant:

> At the start of each iteration of the while loop of lines 4–6, $A[\mathrm{PARENT}(i)] \ge A[\mathrm{LEFT}(i)]$ and $A[\mathrm{PARENT}(i)] \ge A[\mathrm{RIGHT}(i)]$, if these nodes exist, and the subarray $A[1 .. A.\text{heap-size}]$ satisfies the max-heap property, except that there may be one violation: $A[i]$ may be larger than $A[\mathrm{PARENT}(i)]$.

You may assume that the subarray $A[1 .. A.\text{heap-size}]$ satisfies the max-heap property at the time HEAP-INCREASE-KEY is called.

**6.5-6**

Each exchange operation on line 5 of HEAP-INCREASE-KEY typically requires three assignments. Show how to use the idea of the inner loop of INSERTION-SORT to reduce the three assignments down to just one assignment.

**6.5-7**

Show how to implement a first-in, first-out queue with a priority queue. Show how to implement a stack with a priority queue. (Queues and stacks are defined in Section 10.1.)

**6.5-8**

The operation HEAP-DELETE(A, i) deletes the item in node $i$ from heap $A$. Give an implementation of HEAP-DELETE that runs in $O(\lg n)$ time for an $n$-element max-heap.

**6.5-9**

Give an $O(n \lg k)$-time algorithm to merge $k$ sorted lists into one sorted list, where $n$ is the total number of elements in all the input lists. (Hint: Use a min-heap for $k$-way merging.)

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这三道题合起来是一份"优先队列是万能积木"的宣言。6.5-7 要你用优先队列实现 stack（栈）与 queue（队列）：给每个元素配一个单调递增（栈）或递减（队列）的时间戳 key，压入与弹出就退化为 INSERT 与 EXTRACT-MAX，可见第 10 章的线性结构只是优先队列在 key 取值退化时的特例。6.5-8 的 HEAP-DELETE(A, i) 无需新机制：先把 $A[i]$ 增大到 $+\infty$ 让它浮上堆顶，再照搬 HEAP-EXTRACT-MAX 的"末位补顶 + 下沉"，两次 $O(\lg n)$ 操作串联即可。6.5-9 则是后续章节的预热：把 $k$ 个链表的当前队头放进一个大小为 $k$ 的最小堆，每次 EXTRACT-MIN 输出全局最小、再从该链表补入下一个元素，$n$ 次堆操作各花 $O(\lg k)$，总计 $O(n \lg k)$。这正是外部排序中 multiway merge（多路归并）的标准引擎，也是第 24 章最短路算法"用堆维护 frontier（前沿候选集）"的雏形——"用堆维护候选集、每次取最优"这个骨架，你后面至少还要遇到三次。

## Problems for Chapter 6（第 6 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 6-1 · Building a heap using insertion（用插入法建堆） <span style="color:#2471a3;">**[problem]**</span>

We can build a heap by repeatedly calling MAX-HEAP-INSERT to insert the elements into the heap. Consider the following variation on the BUILD-MAX-HEAP procedure:……（接下页）

---

> <span style="color:#7f8c8d;">CLRS Problems 6-1 / 6-2 / 6-3, p.167</span>

（接上页）

```text
BUILD-MAX-HEAP′(A)
1  A.heap-size = 1
2  for i = 2 to A.length
3      MAX-HEAP-INSERT(A, A[i])
```

a. Do the procedures BUILD-MAX-HEAP and BUILD-MAX-HEAP′ always create the same heap when run on the same input array? Prove that they do, or provide a counterexample.

b. Show that in the worst case, BUILD-MAX-HEAP′ requires $\Theta(n \lg n)$ time to build an $n$-element heap.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题逼你正视"同样的输出、不同的代价"。b 问的账本很清楚：BUILD-MAX-HEAP′ 逐个调用 MAX-HEAP-INSERT，最坏情况（输入已按增序排好）下每个新元素都要一路浮到根，单次代价 $\Theta(\lg n)$，$n$ 次累加即 $\Theta(n \lg n)$。这与 6.3 节 BUILD-MAX-HEAP 的 $O(n)$ 上界形成鲜明对照：自底向上建堆时绝大多数结点位于底层、下沉路径极短，总代价 $\sum_{h} \lceil n/2^{h+1} \rceil \cdot O(h)$ 按几何级数收敛。a 问的答案是否定的：例如 $A = \langle 1, 2, 3 \rangle$，插入法得到的堆与自底向上建堆法得到的堆形状并不相同——"上浮"与"下沉"走的是不同的路径，造出的堆不必同构。深层教训是：复杂度由算法对输入执行的操作序列决定，而不由最终输出决定——两个算法产出"同样合法"的结果，代价却可以差一个 $\lg n$ 因子。

### Problem 6-2 · Analysis of d-ary heaps（d 叉堆分析） <span style="color:#2471a3;">**[problem]**</span>

A $d$-ary heap is like a binary heap, but (with one possible exception) non-leaf nodes have $d$ children instead of 2 children.

a. How would you represent a $d$-ary heap in an array?

b. What is the height of a $d$-ary heap of $n$ elements in terms of $n$ and $d$?

c. Give an efficient implementation of EXTRACT-MAX in a $d$-ary max-heap. Analyze its running time in terms of $d$ and $n$.

d. Give an efficient implementation of INSERT in a $d$-ary max-heap. Analyze its running time in terms of $d$ and $n$.

e. Give an efficient implementation of INCREASE-KEY(A, i, k), which flags an error if $k < A[i]$, but otherwise sets $A[i] = k$ and then updates the $d$-ary max-heap structure appropriately. Analyze its running time in terms of $d$ and $n$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> d 叉堆是检验你是否真把"堆 = 完全 $d$ 叉树 + 序性质"内化的试金石，全部小问靠第一性原理算账即可。$n$ 个结点的 $d$ 叉树高为 $\Theta(\log_d n)$：$d$ 越大树越矮，故 b 问答案是 $\lfloor \log_d n \rfloor$；INSERT 与 INCREASE-KEY 沿单一路径上浮，代价降为 $\Theta(\log_d n)$。但 EXTRACT-MAX 每层要先在 $d$ 个孩子里挑最大者，每层花 $O(d)$，总代价 $\Theta(d \log_d n)$；a 问的数组表示把二叉堆的 $\text{PARENT}(i) = \lfloor i/2 \rfloor$ 推广为 $\text{PARENT}(i) = \lfloor (i-2)/d \rfloor + 1$。两相比照可见：你只是在"树高"与"每层宽度"之间搬运代价，$d$ 并不消除对数因子。$d$ 也不是越大越好——$d = \lg n$ 附近达到平衡（两者同为 $\Theta(\lg n)$），$d = n$ 则退化为线性扫描；实践中 $d$ 的选取还要顾及 cache（缓存）：$d$ 个孩子连续存放，才能吃满一次 cache line（缓存行）加载的红利。

### Problem 6-3 · Young tableaus（Young 氏矩阵） <span style="color:#2471a3;">**[problem]**</span>

An $m \times n$ Young tableau is an $m \times n$ matrix such that the entries of each row are in sorted order from left to right and the entries of each column are in sorted order from top to bottom. Some of the entries of a Young tableau may be $\infty$, which we treat as nonexistent elements. Thus, a Young tableau can be used to hold $r \le mn$ finite numbers.

a. Draw a $4 \times 4$ Young tableau containing the elements $\{9, 16, 3, 2, 4, 8, 5, 14, 12\}$.

b. Argue that an $m \times n$ Young tableau $Y$ is empty if $Y[1, 1] = \infty$. Argue that $Y$ is full (contains $mn$ elements) if $Y[m, n] < \infty$.……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Young 氏矩阵把堆的"树序"换成了"行列双单调"：每行从左到右有序、每列从上到下有序。用 6.042J 的语言说，每行、每列各自是一条 chain（链），整张矩阵是两个方向上的偏序（即积偏序 product order：$(i,j) \preceq (i',j')$ 当且仅当 $i \le i'$ 且 $j \le j'$）下的单调填充——$Y[1,1]$ 是最小元、$Y[m,n]$ 是最大元，这正是 b 问两个论断的偏序解释。这些对象由英国数学家 Alfred Young 于 1900 年引入（据离线维基百科），最初服务于对称群的表示论，1903 年起被 Frobenius 用于研究对称群表示——在数据结构语境下，它就是一枚"二维的堆"。与堆一样，$\infty$ 占位符让"未填满"不破坏单调性：把 $\infty$ 看成"比一切都大的空元素"，任何比较都与它兼容。c~f 问将反复使用同一个引擎：与 $Y[i,j]$ 的一次比较能排除一整行或一整列，下一页的 $O(m+n)$ 算法全部由此而来。

---

> <span style="color:#7f8c8d;">CLRS Problem 6-3 / Notes for Chapter 6, p.168</span>

（接上页）

c. Give an algorithm to implement EXTRACT-MIN on a nonempty $m \times n$ Young tableau that runs in $O(m + n)$ time. Your algorithm should use a recursive subroutine that solves an $m \times n$ problem by recursively solving either an $(m - 1) \times n$ or an $m \times (n - 1)$ subproblem. (Hint: Think about MAX-HEAPIFY.) Define $T(p)$, where $p = m + n$, to be the maximum running time of EXTRACT-MIN on any $m \times n$ Young tableau. Give and solve a recurrence for $T(p)$ that yields the $O(m + n)$ time bound.

d. Show how to insert a new element into a nonfull $m \times n$ Young tableau in $O(m + n)$ time.

e. Using no other sorting method as a subroutine, show how to use an $n \times n$ Young tableau to sort $n^2$ numbers in $O(n^3)$ time.

f. Give an $O(m + n)$-time algorithm to determine whether a given number is stored in a given $m \times n$ Young tableau.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> c 问与 f 问是同一证明策略模板的两副面孔，不妨命名为「阶梯下潜」：从右上角 $Y[1,n]$ 出发，当前元素比目标大就左移一列、比目标小就下移一行，每步永久排除一行或一列，至多 $m + n - 1$ 步——这就是经典的 saddleback search（鞍点搜索）。c 问要求的是同一路径的递归记账法：抽走 $Y[1,1]$ 后用 $\infty$ 补位，让坏点像 MAX-HEAPIFY 一样在"向下或向右"中二选一下沉，以 $p = m + n$ 记规模，每步恰减 1，故 $T(p) = T(p-1) + O(1) = O(m+n)$。注意这里的技巧：不必用 $m, n$ 两个变量分别追踪，抓住"每步代价 $O(1)$、总深度 $p$"这一个不变量即可——堆把代价花在"树高"上，Young 氏矩阵把代价花在"行列之和"上，二者是同一主题的变奏。d 问的插入沿"向左或向上"上浮，与堆的 sift-up 完全同构；e 问的 $O(n^3)$ 不过是 $n^2$ 次插入、每次 $O(n)$ 的直和。

## Notes for Chapter 6（第 6 章注释） <span style="color:#2471a3;">**[reference]**</span>

> <span style="color:#7f8c8d;">[note] 按规范，本章 notes（注释/参考文献）保留英文原文，不作翻译；文中受损的数学记号已按原书恢复。</span>

The heapsort algorithm was invented by Williams [357], who also described how to implement a priority queue with a heap. The BUILD-MAX-HEAP procedure was suggested by Floyd [106].

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这两句话是堆的"出生证明"，值得用核实过的细节展开：heapsort 与 binary heap 由在英国 Elliot Bros（伦敦）工作的 J. W. J. Williams 于 1964 年发表（据离线维基百科，其思想形成于 1963 年前后），同一篇论文首次把二叉堆当作独立的数据结构加以阐述，而不只是排序的附庸。同年 Robert W. Floyd 发表了原位（in-place）改进版，延续他此前 treesort（树排序）系列的研究——BUILD-MAX-HEAP 正出自 Floyd 之手。Williams 的动机来自系统调度与离散事件模拟对 priority queue（优先队列）的迫切需求，此后六十年堆成为 Dijkstra 最短路、Prim 最小生成树、任务调度器的共同地基。本页下文 Fredman–Willard 与 Thorup 的 $O(\lg \lg n)$ 上界，以及第 19 章 Fibonacci heap（斐波那契堆）、第 20 章 van Emde Boas 树，都是这场持续至今的"优先队列军备竞赛"的战报——数据结构的历史，很大程度上就是优先队列的历史。

We use min-heaps to implement min-priority queues in Chapters 16, 23, and 24. We also give an implementation with improved time bounds for certain operations in Chapter 19 and, assuming that the keys are drawn from a bounded set of nonnegative integers, Chapter 20.

If the data are $b$-bit integers, and the computer memory consists of addressable $b$-bit words, Fredman and Willard [115] showed how to implement MINIMUM in $O(1)$ time and INSERT and EXTRACT-MIN in $O(\sqrt{\lg n})$ time. Thorup [337] has improved the $O(\sqrt{\lg n})$ bound to $O(\lg \lg n)$ time. This bound uses an amount of space unbounded in $n$, but it can be implemented in linear space by using randomized hashing.

An important special case of priority queues occurs when the sequence of EXTRACT-MIN operations is monotone, that is, the values returned by successive EXTRACT-MIN operations are monotonically increasing over time. This case arises in several important applications, such as Dijkstra's single-source shortest-paths algorithm, which we discuss in Chapter 24, and in discrete-event simulation. For Dijkstra's algorithm it is particularly important that the DECREASE-KEY operation be implemented efficiently. For the monotone case, if the data are integers in the range $1, 2, \ldots, C$, Ahuja, Mehlhorn, Orlin, and Tarjan [8] describe……（接下页）

---

> <span style="color:#7f8c8d;">CLRS Notes for Chapter 6, p.169</span>

（接上页）how to implement EXTRACT-MIN and INSERT in $O(\lg C)$ amortized time (see Chapter 17 for more on amortized analysis) and DECREASE-KEY in $O(1)$ time, using a data structure called a radix heap. The $O(\lg C)$ bound can be improved to $O(\sqrt{\lg C})$ using Fibonacci heaps (see Chapter 19) in conjunction with radix heaps. Cherkassky, Goldberg, and Silverstein [65] further improved the bound to $O(\lg^{1/3+\varepsilon} C)$ expected time by combining the multilevel bucketing structure of Denardo and Fox [85] with the heap of Thorup mentioned earlier. Raman [291] further improved these results to obtain a bound of $O(\min(\lg^{1/4+\varepsilon} C,\ \lg^{1/3+\varepsilon} n))$, for any fixed $\varepsilon > 0$.

---

> <span style="color:#7f8c8d;">CLRS Chapter 7 / §7.1, p.170</span>

## Chapter 7（第 7 章）· Quicksort（快速排序） <span style="color:#2471a3;">**[section]**</span>

quicksort（快速排序）算法的最坏情况 running time（运行时间）是 $\Theta(n^2)$——对一个含 $n$ 个数的 input array（输入数组）而言。尽管这个最坏情况的运行时间很慢，但 quicksort 往往仍是排序问题在实践中的最佳选择：它在平均情况下表现极为出色，其 expected running time（期望运行时间）是 $\Theta(n \lg n)$，而且隐藏在 $\Theta(n \lg n)$ 这个记号背后的 constant factors（常数因子）相当小。quicksort 还有另外两个优点：它采用 sort in place（原地排序）（见第 17 页），并且在 virtual-memory environments（虚拟存储环境）下也能工作得很好。

Section 7.1 描述这个算法，以及 quicksort 用来对子数组做 partitioning（划分）的一个重要 subroutine（子程序）。由于 quicksort 的行为颇为复杂，我们先在 Section 7.2 中以直观的方式讨论它的性能，而把它的精确分析留到本章的末尾。Section 7.3 给出了一个使用 random sampling（随机取样）技术的 quicksort 版本。该算法具有良好的期望运行时间，而且没有任何特定的输入能够引发它的最坏情况行为。Section 7.4 分析了 randomized algorithm（随机化算法），证明它在最坏情况下需要 $\Theta(n^2)$ 时间，并且（在元素互异的假定下）其期望运行时间为 $O(n \lg n)$。

### Section 7.1 · Description of quicksort（快速排序的描述） <span style="color:#2471a3;">**[section]**</span>

quicksort 与 merge sort（归并排序）一样，采用的也是 Section 2.3.1 中引入的 divide-and-conquer paradigm（分治范式）。下面是对一个典型 subarray（子数组）$A[p .. r]$ 排序的三步 divide-and-conquer process（分治过程）：

**Divide（分解）：** 把数组 $A[p .. r]$ Partition（划分，即重新排列）成两个（可能为空的）子数组 $A[p .. q-1]$ 与 $A[q+1 .. r]$，使得 $A[p .. q-1]$ 中的每个元素都 $\le A[q]$，而 $A[q]$ 又 $\le A[q+1 .. r]$ 中的每个元素。在这个划分过程中一并计算出 index（下标）$q$。

**Conquer（解决）：** 通过对 $A[p .. q-1]$ 和 $A[q+1 .. r]$ 递归调用 quicksort，把这两个子数组分别排序。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第 170 页开篇这段话值得逐句读：快排与堆排序渐近同为 $O(n \lg n)$，快排胜出的秘密不在大 $O$ 里，而在三个"常数级"的细节上——划分循环对数组的顺序双向扫描极契合 cache（缓存）预取、内层循环极简、原位排序不搬内存；上一章译者注里提到的 introsort 正是拿快排当主力、堆排序当保镖。同时请留意一个与归并排序的深刻对照：归并的"分解"是平凡的（中点一劈）、"合并"要苦干 $\Theta(n)$；快排恰好反过来——"合并"是免费的（子数组各自有序，整体即有序），全部工作量被前移进了"划分"这一步。分治的代价放在哪一步，是设计这类算法时最核心的取舍；本章后续的分析（7.2 节的直观论证与 7.4 节的精确期望分析）都是在为"划分划得平均"这件事定价。

---

> <span style="color:#7f8c8d;">CLRS §7.1, p.171</span>

（接上页）

**Combine（合并）：** 由于两个子数组已经各自排好序，所以不需要任何工作来 combine（合并）它们：整个数组 $A[p .. r]$ 现在就已经是有序的了。

下面的过程实现了 quicksort：

```text
QUICKSORT(A, p, r)
1  if p < r
2      q = PARTITION(A, p, r)
3      QUICKSORT(A, p, q - 1)
4      QUICKSORT(A, q + 1, r)
```

要对整个数组 $A$ 排序，初始调用为 QUICKSORT(A, 1, A.length)。

#### Partitioning the array（数组的划分） <span style="color:#2471a3;">**[section]**</span>

这个算法的关键是 PARTITION 过程，它对 subarray（子数组）$A[p .. r]$ 进行 in-place（原地）的重新排列：

```text
PARTITION(A, p, r)
1  x = A[r]
2  i = p - 1
3  for j = p to r - 1
4      if A[j] ≤ x
5          i = i + 1
6          exchange A[i] with A[j]
7  exchange A[i + 1] with A[r]
8  return i + 1
```

Figure 7.1（图 7.1）展示了 PARTITION 在一个 8 元素数组上的工作过程。PARTITION 总是选择 $x = A[r]$ 作为一个 pivot element（主元元素），并围绕这个主元来划分子数组 $A[p .. r]$。随着过程的运行，它把数组划分成四个（可能为空的）regions（区域）。在第 3–6 行 for 循环的每一次迭代的开始时刻，这四个区域都满足某些性质——图 7.2 展示了这些性质。我们把这些性质表述为一个 loop invariant（循环不变式）：

> 在第 3–6 行循环的每次迭代的开始时刻，对于任何一个 array index（数组下标）$k$：
>
> 1. 如果 $p \le k \le i$，则 $A[k] \le x$。
> 2. 如果 $i + 1 \le k \le j - 1$，则 $A[k] > x$。
> 3. 如果 $k = r$，则 $A[k] = x$。

……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> PARTITION 的不变式描述的是"四个区域"而非"两个"：$A[p..i]$ 存放 $\le x$ 的元素，$A[i+1..j-1]$ 存放 $> x$ 的元素，$A[j..r-1]$ 是尚未检视的未知区，$A[r]$ 是主元。这种"已处理区 + 未知区"的不变式写法与第 2.1 节插入排序的"已排序前缀"同源，但更胜一筹——维护成本是 $O(1)$/轮且总共只需 $r-p$ 轮，故 PARTITION 本身是 $\Theta(n)$ 的。请特别留意变量 $i$ 与 $j$ 的分工：$j$ 是"探路者"，随循环每轮无条件前移；$i$ 是"边界记录者"，只在发现 $\le x$ 的元素时前移一格——因此 $i$ 始终指向 $\le x$ 区域的最后一个元素，第 7 行 `exchange A[i+1] with A[r]` 才能把主元恰好嵌进两个区域之间。看懂图 7.2 中四区域随 $i$、$j$ 移动的演化，是理解整个第 7 章的钥匙；习题 7.1-1 与 7.1-2 马上会让你亲手在样例数组上走一遍。

---

> <span style="color:#7f8c8d;">CLRS §7.1 + Figure 7.1, p.172</span>

> <span style="color:#7f8c8d;">[note] 本页为整页插图：图 7.1 用九个面板 (a)–(i) 展示 PARTITION 在样本数组 $\langle 2, 8, 7, 1, 3, 5, 6, 4 \rangle$（$p = 1$，$r = 8$，主元 $x = A[8] = 4$）上的完整操作。下标 $i$ 标记"$\le x$"区域的右端，$j$ 标记当前检视位置；每行中用竖线示意两个划分的边界——竖线左侧（浅色）元素均 $\le 4$，其后（深色）元素均 $> 4$，无阴影元素尚未检视，末尾白色元素为主元 4。</span>

```text
(a) 初始设置：i = p-1 = 0，j = p = 1
    [ | 2  8  7  1  3  5  6 | 4 ]
    p,j                      r          （尚无元素进入两个划分）

(b) j = 1：A[1] = 2 ≤ x，i 增至 1，A[1] 与自身交换
    [ 2 | 8  7  1  3  5  6 | 4 ]
    p,i      j               r

(c) j = 2：A[2] = 8 > x，j 前移
    [ 2 | 8  7  1  3  5  6 | 4 ]
    p,i         j            r

(d) j = 3：A[3] = 7 > x，j 前移
    [ 2 | 8  7  1  3  5  6 | 4 ]
    p,i            j         r

(e) j = 4：A[4] = 1 ≤ x，i 增至 2，交换 A[2] 与 A[4]（1 与 8）
    [ 2  1 | 7  8  3  5  6 | 4 ]
    p,  i               j    r

(f) j = 5：A[5] = 3 ≤ x，i 增至 3，交换 A[3] 与 A[5]（3 与 7）
    [ 2  1  3 | 8  7  5  6 | 4 ]
    p     i            j     r

(g) j = 6：A[6] = 5 > x，j 前移
    [ 2  1  3 | 8  7  5  6 | 4 ]
    p     i               j  r

(h) j = 7：A[7] = 6 > x，j 前移，循环终止
    [ 2  1  3 | 8  7  5  6 | 4 ]
    p     i                  r,j

(i) 第 7–8 行：交换 A[i+1] = A[4] 与 A[8]（主元 4 入位），返回 i + 1 = 4
    [ 2  1  3 | 4 | 7  5  6  8 ]
    p     i                r
```

**Figure 7.1（图 7.1）** PARTITION 在一个样本数组上的操作。数组元素 $A[r]$ 成为 pivot element（主元元素）$x$。浅色阴影的数组元素全部位于第一个划分之中，其值都不大于 $x$；深色阴影的元素位于第二个划分中，其值都大于 $x$；unshaded（无阴影）的元素尚未被放入前两个划分中的任何一个，而最后一个白色元素是主元 $x$。(a) 初始数组与变量设置；此时还没有任何元素被放入前两个划分中的任何一个。(b) 值 2 "与自身交换"，从而被放入较小值的那一划分中。(c)–(d) 值 8 和 7 被加入较大值的划分中。(e) 值 1 与 8 交换，较小的划分扩大。(f) 值 3 与 7 交换，较小的划分继续扩大。(g)–(h) 较大的划分扩大到包含 5 和 6，循环终止。(i) 在第 7–8 行中，主元元素被交换到位，恰好处在两个划分之间。

（接上页）

在 $j$ 与 $r - 1$ 之间的那些下标不被上述三种情形中的任何一种所覆盖，这些位置上的值与主元 $x$ 之间没有任何特定的关系。

我们需要证明：这个 loop invariant（循环不变式）在第一次迭代之前为真，循环的每一次迭代都维持该不变式，并且当循环终止时，该不变式能提供一个用于证明 correctness（正确性）的有用性质。……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §7.1 + Figure 7.2, p.173</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 7.2 的示意图：子数组 $A[p..r]$ 被维护成四个 region（区域）——$A[p..i]$ 中的值全部 $\le x$，$A[i+1..j-1]$ 中的值全部 $> x$，$A[r] = x$（主元），而 $A[j..r-1]$ 中的值不受限制（unrestricted）。</span>

```text
p          i               j               r
[  ≤ x  ][  > x  ][ unrestricted（任意值） ][ x ]
   A[p..i]  A[i+1..j-1]     A[j..r-1]       A[r]
```

**Figure 7.2（图 7.2）** 过程 PARTITION 在子数组 $A[p..r]$ 上所维护的四个区域。$A[p..i]$ 中的值都小于或等于 $x$，$A[i+1..j-1]$ 中的值都大于 $x$，且 $A[r] = x$。子数组 $A[j..r-1]$ 可以取任意值。

（接上页）

**Initialization（初始化）：** 在循环的第一次迭代之前，$i = p - 1$ 且 $j = p$。由于 $p$ 与 $i$ 之间不存在任何值，且 $i+1$ 与 $j-1$ 之间也不存在任何值，循环不变式的前两个条件平凡地（trivially）得到满足。第 1 行中的 assignment（赋值）满足了第三个条件。

**Maintenance（保持）：** 如图 7.3 所示，我们考虑两种情况，取决于第 4 行中测试的 outcome（结果）。图 7.3(a) 展示了当 $A[j] > x$ 时会发生什么：循环中唯一的动作是递增 $j$。在 $j$ 递增之后，条件 2 对 $A[j-1]$ 成立，而所有其他项保持不变。图 7.3(b) 展示了当 $A[j] \le x$ 时会发生什么：循环递增 $i$，交换 $A[i]$ 与 $A[j]$，然后递增 $j$。由于这次交换，我们现在有 $A[i] \le x$，条件 1 得到满足。类似地，我们也有 $A[j-1] > x$，因为被交换到 $A[j-1]$ 中的那一项，依循环不变式所述，是大于 $x$ 的。

**Termination（终止）：** 终止时，$j = r$。因此，数组中的每一项都位于不变式所描述的三个集合之一中，于是我们已把数组中的值 partition（划分）成了三个集合：小于或等于 $x$ 的那些、大于 $x$ 的那些，以及一个包含 $x$ 的 singleton set（单元素集合）。

PARTITION 的最后两行收尾工作是这样的：把 pivot element（主元元素）与左侧最靠左的大于 $x$ 的元素交换，从而把主元移动到它在已划分数组中的正确位置上，然后返回主元的新的 index（下标）。至此，PARTITION 的 output（输出）满足了 divide step（分解步骤）所要求的规定。事实上，它还满足一个稍强一点的条件：在 QUICKSORT 的第 2 行之后，$A[q]$ 严格小于 $A[q+1..r]$ 中的每一个元素。

PARTITION 在子数组 $A[p..r]$ 上的 running time（运行时间）为 $\Theta(n)$，其中 $n = r - p + 1$（见 Exercise 7.1-3）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段不变式论证里最精妙的是 Maintenance 的第二种情况：交换后 $A[j-1] > x$ 并非"显然"，它依赖"被换进来的那一项原本属于 $> x$ 区域"这一不变式保证。这正是循环不变式方法的价值——每一步的新状态都从旧状态"继承"合法性，而不必重新全局检查。另外注意结论中的一个常见误区：PARTITION 之后主元只是"就位"了，$A[p..q-1]$ 与 $A[q+1..r]$ 内部仍然无序——quicksort 的"合并"步骤之所以免费，代价全部预付在了这里的划分之中。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**7.1-1**

Using Figure 7.1 as a model, illustrate the operation of PARTITION on the array $A = \langle 13, 19, 9, 5, 12, 8, 7, 4, 21, 2, 6, 11 \rangle$.……（接下页）

---

> <span style="color:#7f8c8d;">CLRS Figure 7.3 / Exercises 7.1-2~4 / §7.2, p.174</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 7.3 的示意图：(a) 中 $A[j] > x$，$j$ 直接右移一格，四个区域形状不变；(b) 中 $A[j] \le x$，$i$ 先右移一格，然后交换 $A[i]$ 与 $A[j]$，再右移 $j$——"$\le x$"区域随之扩大一格。</span>

```text
(a) A[j] > x：                      (b) A[j] ≤ x：
p      i        j       r           p        i      j       r
[ ≤ x ][  > x  ][ ? ][x]            [ ≤ x   ][ > x ][ ?  ][x]
                    j ← j+1              i ← i+1，交换 A[i]↔A[j]，j ← j+1
```

**Figure 7.3（图 7.3）** 过程 PARTITION 一次迭代的两种情况。(a) 若 $A[j] > x$，唯一的动作就是递增 $j$，循环不变式得以维持。(b) 若 $A[j] \le x$，下标 $i$ 被递增，$A[i]$ 与 $A[j]$ 被交换，然后 $j$ 被递增。同样，循环不变式得以维持。

**7.1-2**

What value of $q$ does PARTITION return when all elements in the array $A[p..r]$ have the same value? Modify PARTITION so that $q = \lfloor (p+r)/2 \rfloor$ when all elements in the array $A[p..r]$ have the same value.

**7.1-3**

Give a brief argument that the running time of PARTITION on a subarray of size $n$ is $\Theta(n)$.

**7.1-4**

How would you modify QUICKSORT to sort into nonincreasing order?

### Section 7.2 · Performance of quicksort（快速排序的性能） <span style="color:#2471a3;">**[section]**</span>

quicksort 的 running time（运行时间）取决于 partitioning（划分）是 balanced（平衡的）还是 unbalanced（不平衡的），而这又取决于划分时使用了哪些元素。如果划分是平衡的，该算法的运行速度就渐近地与 merge……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §7.2, p.175</span>

（接上页）sort（归并排序）一样快。然而，如果划分是不平衡的，它可能运行得渐近地如 insertion sort（插入排序）一样慢。在本节中，我们将以非形式的方式考察 quicksort 在平衡划分与不平衡划分这两种假定下的性能表现。

#### Worst-case partitioning（最坏情况划分） <span style="color:#2471a3;">**[section]**</span>

quicksort 的 worst-case behavior（最坏情况行为）发生在 partitioning routine（划分例程）产生一个包含 $n-1$ 个元素的 subproblem（子问题）和一个包含 $0$ 个元素的子问题的时候。（我们将在 Section 7.4.1 中证明这一论断。）让我们假定这种不平衡划分出现在每一次 recursive call（递归调用）中。划分本身需要 $\Theta(n)$ 时间。由于对大小为 $0$ 的数组进行的递归调用直接返回，故 $T(0) = \Theta(1)$，于是运行时间的 recurrence（递归式）为

```math
\begin{aligned}
T(n) &= T(n-1) + T(0) + \Theta(n) \\
     &= T(n-1) + \Theta(n).
\end{aligned}
```

直观地看，如果我们将递归的每一层上发生的代价累加起来，就得到一个 arithmetic series（算术级数，见 equation (A.2)），其值为 $\Theta(n^2)$。事实上，直接用 substitution method（代换法）就可以证明递归式 $T(n) = T(n-1) + \Theta(n)$ 的解为 $T(n) = \Theta(n^2)$。（见 Exercise 7.2-1。）

于是，如果在该算法的每一递归层上划分都是极不平衡的，运行时间就是 $\Theta(n^2)$。因此，quicksort 最坏情况运行时间并不比插入排序更好。此外，$\Theta(n^2)$ 的运行时间出现在输入数组已经完全排好序的情况——这是一种常见情形，而插入排序在这种情形下恰好在 $O(n)$ 时间内运行。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "对已排序输入反而最慢"是 Lomuto 划分（固定取 $A[r]$ 为主元）的标志性弱点：输入越有序，$q$ 越贴近端点，递归树越退化成一条长度为 $n$ 的"链"，$\sum_{k=1}^{n} k = \Theta(n^2)$。工程中的数组常常"基本有序"，这正是 7.3 节引入随机化主元的动机，也是 7.2-4 题让插入排序与快排赛跑的背景。

#### Best-case partitioning（最好情况划分） <span style="color:#2471a3;">**[section]**</span>

在尽可能最平均的 split（分割）中，PARTITION 产生两个子问题，每一个的规模都不超过 $n/2$，因为一个的规模是 $\lfloor n/2 \rfloor$，另一个的规模是 $\lceil n/2 \rceil - 1$。在这种情况下，quicksort 运行得快得多。此时运行时间的递归式为

```math
T(n) = 2T(n/2) + \Theta(n),
```

其中我们容忍了一定的 sloppiness（不严谨）：既忽略了 floor（下取整）与 ceiling（上取整），也减去了 $1$。根据 master theorem（主方法）的情形 2（Theorem 4.1），该递归式的解为 $T(n) = \Theta(n \lg n)$。通过在递归的每一层上都均等地平衡划分的两侧，我们得到了一个渐近意义上更快的算法。

#### Balanced partitioning（平衡划分） <span style="color:#2471a3;">**[section]**</span>

quicksort 的 average-case running time（平均情况运行时间）更加接近最好情况而非最坏情况——Section 7.4 中的分析将展示这一点。理解其中缘由的关键，在于理解划分的平衡程度是如何反映在刻画运行时间的递归式之中的。

……（接下页）

---

> <span style="color:#7f8c8d;">CLRS Figure 7.4 + §7.2, p.176</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 7.4 的示意图：PARTITION 每次都按 9 比 1 的比例分割，子问题规模沿树逐层缩小，右侧为每层总代价。为对照原书排版，下图以文本示意重绘。</span>

```text
层 0 :                    n                     ← 代价 cn
层 1 :          n/10          9n/10             ← 代价 cn
层 2 :     n/100   9n/100   9n/100   81n/100     ← 代价 cn
  ⋮          ⋮        ⋮        ⋮        ⋮
深度 log₁₀ n 处达到边界条件（代价 ≤ cn），递归于深度 log₁₀⁄₉ n = Θ(lg n) 处终止
```

**Figure 7.4（图 7.4）** QUICKSORT 的一棵 recursion tree（递归树），其中 PARTITION 总是产生一个 9-to-1 split（9 比 1 的分割），由此得到的 running time（运行时间）为 $O(n \lg n)$。结点中显示的是 subproblem sizes（子问题规模），右侧为每层的代价。每层的代价包含隐含在 $\Theta(n)$ 项中的常数 $c$。

（接上页）例如，假定划分算法总是产生一个 9-to-1 proportional split（9 比 1 的比例分割），乍一看这似乎相当不平衡。于是我们得到关于 quicksort 运行时间的递归式

```math
T(n) = T(9n/10) + T(n/10) + cn,
```

其中我们显式地写出了隐藏在 $\Theta(n)$ 项中的常数 $c$。图 7.4 展示了该递归式的递归树。注意，递归树的每一层的代价都是 $cn$，直到递归在深度 $\log_{10} n = \Theta(\lg n)$ 处达到 boundary condition（边界条件）为止，此后各层的代价至多为 $cn$。递归在深度 $\log_{10/9} n = \Theta(\lg n)$ 处终止。因此，quicksort 的总代价是 $O(n \lg n)$。于是，即便在递归的每一层上都以 9 比 1 的比例分割——直观上这似乎相当不平衡——quicksort 的运行时间也是 $O(n \lg n)$：渐近意义上与从正中间分开的分割完全一样。事实上，即使是 99 比 1 的分割，得到的运行时间也是 $O(n \lg n)$。进一步说，任何具有常数比例（constant proportionality）的分割都会产生一棵深度为 $\Theta(\lg n)$ 的递归树，且每层代价为 $O(n)$。因此，只要分割具有常数比例，运行时间就是 $O(n \lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段论证悄悄完成了一次"视角转换"：我们不再追问"递归树有多少层、每层省了多少"，而是问"代价被谁吃掉了"。9:1 分割中，规模 $9n/10$ 的子树每层贡献 $(9/10)n$，指数衰减 $(9/10)^d n \to 1$ 给出树高 $\log_{10/9} n = \Theta(\lg n)$——底数从 $2$ 换成 $10/9$ 只改变常数因子，不改对数的量级。记住这个结论：**任何常数比例的分割都保住 $O(n \lg n)$**；真正致命的只有 7.2 节那种"一个子问题规模为 0"的退化分割。这一观察将在 7.4.2 节的期望分析中扮演关键角色。

---

> <span style="color:#7f8c8d;">CLRS Figure 7.5 + §7.2, p.177</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 7.5 的示意图：(a) 展示递归树中连续两层——根处一次"坏"分割（子数组规模 $0$ 与 $n-1$），下一层对规模 $n-1$ 的子数组做"好"分割（$(n-1)/2-1$ 与 $(n-1)/2$）；(b) 展示单层非常平衡的分割（两个 $(n-1)/2$）。(a) 中两次分割的总代价 $\Theta(n) + \Theta(n-1) = \Theta(n)$，与 (b) 中单层代价 $\Theta(n)$ 相当，但两层之后两侧余留的子问题规模反而更小。</span>

```text
(a) 坏分割 → 好分割（两层）：          (b) 一层很平衡的分割：
         n                                    n
        / \        代价 Θ(n)                 / \
       0   n-1                              (n-1)/2   (n-1)/2
          / \          代价 Θ(n)                 代价 Θ(n)
    (n-1)/2-1  (n-1)/2
```

**Figure 7.5（图 7.5）** (a) quicksort 递归树的两层。根结点处划分的代价为 $n$，产生一个 "bad" split（坏分割）：两个规模分别为 $0$ 和 $n-1$ 的子数组。规模为 $n-1$ 的子数组的划分代价为 $n-1$，产生一个 "good" split（好分割）：规模分别为 $(n-1)/2 - 1$ 和 $(n-1)/2$ 的子数组。(b) 递归树中非常平衡的一层。在这两个部分中，以椭圆形阴影标出的子问题的划分代价都是 $\Theta(n)$。然而 (a) 中尚待求解的子问题（以方形阴影标出）并不大于 (b) 中对应的尚待求解的子问题。

#### Intuition for the average case（平均情况的直观认识） <span style="color:#2471a3;">**[section]**</span>

为了对 quicksort 的 randomized behavior（随机化行为）建立一个清晰的认识，我们必须对"预期会在怎样的频率上遇到各种输入"做出假设。quicksort 的行为取决于作为输入给出的数组元素中值的相对次序（relative ordering），而不取决于数组中的具体值。正如 Section 5.2 中对 hiring problem（雇用问题）的概率分析那样，我们暂时假定输入数的所有 permutation（排列）都是等可能的。

当我们在一个随机输入数组上运行 quicksort 时，划分极不可能在每一层都以相同的方式发生，而我们此前的非正式分析却做了这样的假定。我们预期某些分割会相当平衡，而另一些则会相当不平衡。例如，Exercise 7.2-6 要求你证明：大约 80% 的时间 PARTITION 产生比 9 比 1 更平衡的分割，大约 20% 的时间它产生比 9 比 1 更不平衡的分割。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里悄悄立起了一个概率模型，值得用第一性原理拆开看。quicksort 的运行时间只取决于元素的 relative ordering（相对次序）：PARTITION 只做比较、从不利用数值的绝对大小，把数组里每个元素都换成 $2x_i$，运行轨迹分毫不变。既然绝对值无关紧要，可能影响算法的输入自由度只剩 $n!$ 种排列，而"假定所有排列等可能"正是 5.2 节雇用问题用过的同一假设（那里是"候选人次序均匀随机"）。这个假设强在把"坏输入"从确定性威胁降格为概率事件：最坏排列只占 $1/n!$，小到几乎碰不到；但它也弱在真实数据未必均匀——银行流水这类"基本有序"的输入远离均匀分布，这正是 7.3 节随机化要根治的对象。Exercise 7.2-6 的 80%/20% 数字则预告了本节结尾的论证方式：好坏分割随机混合、整体仍可 $O(n \lg n)$，下一页的"交替论证"是它的最保守版本。

在平均情况下，PARTITION 产生 "good" split（好分割）与 "bad" split（坏分割）的混合。在平均情况下一次 PARTITION 执行的递归树中，好分割与坏分割随机地分布在整个树中。为了获得直观认识，不妨假定好分割与坏分割在树中交替地出现在各层上，且好分割是最好情况的分割，坏分割是最坏情况的分割。图 7.5(a) 展示了递归树中连续两层上的分割。在树的根结点处，划分的代价为 $n$，产生的子数组规模为 $n-1$ 和 $0$：这是最坏情况。在下一层，规模为 $n-1$ 的子数组经历最好情况的划分，产生规模为 $(n-1)/2 - 1$ 和 $(n-1)/2$ 的子数组。让我们假定规模为 $0$ 的子数组的 boundary-condition cost（边界条件代价）为 $1$。……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §7.2 + Exercises 7.2-1~5, p.178</span>

（接上页）坏分割与随后的好分割的组合，产生了三个规模分别为 $0$、$(n-1)/2 - 1$ 和 $(n-1)/2$ 的子数组，其划分代价合计为 $\Theta(n) + \Theta(n-1) = \Theta(n)$。毫无疑问，这一局面并不比图 7.5(b) 中的局面更差——后者即单层划分产生两个规模为 $(n-1)/2$ 的子数组、代价为 $\Theta(n)$ 的情形。然而，后一种情形可是 balanced（平衡的）！直观上，坏分割的 $\Theta(n-1)$ 代价可以被吸收进好分割的 $\Theta(n)$ 代价之中，而得到的分割是一个好分割。因此，当各层在好分割与坏分割之间交替时，quicksort 的 running time（运行时间）就如同只有好分割时的运行时间一样：仍然是 $O(n \lg n)$，只不过是 $O$ 记号背后隐藏了一个稍大一点的常数。

我们将在 Section 7.4.2 中对一个 randomized version（随机化版本）的 quicksort 的 expected running time（期望运行时间）给出严格的分析。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "坏分割的代价可以被好分割吸收"是本节最重要的一句话：$n-1$ 那次"白付"的划分费，换来的是把问题直接推近了一层最好情况分割，之后余留的子问题（$(n-1)/2-1$ 与 $(n-1)/2$）比单层平衡分割（两个 $(n-1)/2$）还小。换句话说，只要坏分割不连续出现，它就只是让 $O(n \lg n)$ 的常数因子变大，而不改变增长阶数。这一"局部坏、整体好"的直觉，正是 7.4.2 节用指示器随机变量做精确期望分析的导火索。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**7.2-1**

Use the substitution method to prove that the recurrence $T(n) = T(n-1) + \Theta(n)$ has the solution $T(n) = \Theta(n^2)$, as claimed at the beginning of Section 7.2.

**7.2-2**

What is the running time of QUICKSORT when all elements of array $A$ have the same value?

**7.2-3**

Show that the running time of QUICKSORT is $\Theta(n^2)$ when the array $A$ contains distinct elements and is sorted in decreasing order.

**7.2-4**

Banks often record transactions on an account in order of the times of the transactions, but many people like to receive their bank statements with checks listed in order by check number. People usually write checks in order by check number, and merchants usually cash them with reasonable dispatch. The problem of converting time-of-transaction ordering to check-number ordering is therefore the problem of sorting almost-sorted input. Argue that the procedure INSERTION-SORT would tend to beat the procedure QUICKSORT on this problem.

**7.2-5**

Suppose that the splits at every level of quicksort are in the proportion $1 - \alpha$ to $\alpha$, where $0 < \alpha \le 1/2$ is a constant. Show that the minimum depth of a leaf in the recursion tree is approximately $-\lg n / \lg \alpha$ and the maximum depth is approximately $-\lg n / \lg(1 - \alpha)$. (Don't worry about integer round-off.)……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 7.2-5 的两个深度公式是「比例衰减递归树」模板的精确化。若每层按 $1-\alpha : \alpha$ 分割，小侧规模逐层乘 $\alpha$，衰减到常数需 $-\lg n / \lg \alpha$ 层，大侧同理需 $-\lg n / \lg(1-\alpha)$ 层——代入 $\alpha = 1/10$ 就还原出 7.2.2 节的 $\log_{10/9} n$，代入 $\alpha = 1/2$ 两式合一即 $\lg n$。这对公式有个漂亮的读法：**最深叶由大侧比例决定（它控制总深度），最浅叶由小侧比例决定（它决定"最先落位"的元素何时逃出生天）**。做一次极限自查：当 $\alpha \to 0$ 时 $-\lg \alpha \to \infty$，深度趋于无穷——公式精确复现了"退化成链"的最坏情况，渐近式在极限处也不说谎。这条公式还会在 7.4.2 节以另一种面貌回归：只要每层分割在期望意义下以某个常数比例"甩掉"元素，递归深度就仍是 $\Theta(\lg n)$——比例常数只改对数的底，改不了对数的量级。

---

> <span style="color:#7f8c8d;">CLRS Exercise 7.2-6 + §7.3, p.179</span>

（接上页）

**7.2-6**

?

Argue that for any constant $0 < \alpha \le 1/2$, the probability is approximately $1 - 2\alpha$ that on a random input array, PARTITION produces a split more balanced than $1 - \alpha$ to $\alpha$.

### Section 7.3 · A randomized version of quicksort（快速排序的随机化版本） <span style="color:#2471a3;">**[section]**</span>

在探索 quicksort 的 average-case behavior（平均情况行为）时，我们做了一个假设：输入数的所有排列都是等可能的。然而在工程实践中，我们不能总是指望这个假设成立。（见 Exercise 7.2-4。）正如 Section 5.3 中所看到的，我们有时可以给一个 algorithm（算法）加入 randomization（随机化），以便在所有输入上都获得良好的 expected performance（期望性能）。许多人把由此得到的 randomized version of quicksort（快速排序的随机化版本）视为对足够大的输入而言 sorting algorithm of choice（首选的排序算法）。

在 Section 5.3 中，我们是通过显式地 permutation（排列）输入来随机化算法的。对 quicksort 我们也可以这样做，但另一种随机化技术——称为 random sampling（随机取样）——能给出更简单的分析。我们不再总是使用 $A[r]$ 作为主元，而是从子数组 $A[p..r]$ 中随机选出一个元素。做法是：先把 $A[r]$ 与从 $A[p..r]$ 中随机选出的一个元素 exchange（交换）。通过随机取样范围 $p, \ldots, r$，我们保证了 pivot element（主元元素）$x = A[r]$ 等可能地是子数组中 $r - p + 1$ 个元素中的任何一个。因为我们随机地选择主元元素，我们预期输入数组的分割在平均意义上会得到相当好的平衡。

对 PARTITION 和 QUICKSORT 的改动很小。在新的划分过程中，我们只需在真正进行划分之前实现这个交换：

```text
RANDOMIZED-PARTITION(A, p, r)
1  i = RANDOM(p, r)
2  exchange A[r] with A[i]
3  return PARTITION(A, p, r)
```

新的 quicksort 调用 RANDOMIZED-PARTITION 来代替 PARTITION：

```text
RANDOMIZED-QUICKSORT(A, p, r)
1  if p < r
2      q = RANDOMIZED-PARTITION(A, p, r)
3      RANDOMIZED-QUICKSORT(A, p, q - 1)
4      RANDOMIZED-QUICKSORT(A, q + 1, r)
```

我们将在下一节中分析这个算法。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 随机化的落脚点小得惊人：只在划分前加一次 `RANDOM(p, r)` 取样加一次交换，最坏情况输入就"失效"了——不再存在一个固定数组能让算法必然退化，因为主元的选择已由随机数发生器接管。注意代价的两面性：算法自身的最坏情况运行时间仍是 $\Theta(n^2)$（某个极端倒霉的取样序列依然可能），但那是"概率极小的事故"而非"确定性的缺陷"；下一节要证明的正是其期望运行时间为 $\Theta(n \lg n)$。这与 5.3 节"随机化雇用助手"是同一个策略：把性能 guarantee（保证）从"对输入"搬到"对随机数"。

---

> <span style="color:#7f8c8d;">CLRS Exercises 7.3-1~2 + §7.4, p.180</span>

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**7.3-1**

Why do we analyze the expected running time of a randomized algorithm and not its worst-case running time?

**7.3-2**

When RANDOMIZED-QUICKSORT runs, how many calls are made to the random-number generator RANDOM in the worst case? How about in the best case? Give your answer in terms of $\Theta$-notation.

### Section 7.4 · Analysis of quicksort（快速排序的分析） <span style="color:#2471a3;">**[section]**</span>

Section 7.2 为 quicksort 的 worst-case behavior（最坏情况行为）以及"我们为何预期它运行得快"提供了一些直观认识。在本节中，我们将更严格地分析 quicksort 的行为。我们首先进行 worst-case analysis（最坏情况分析）——它既适用于 QUICKSORT 也适用于 RANDOMIZED-QUICKSORT——最后以对 RANDOMIZED-QUICKSORT 的 expected running time（期望运行时间）的分析作结。

#### 7.4.1 Worst-case analysis（最坏情况分析） <span style="color:#2471a3;">**[section]**</span>

我们在 Section 7.2 中看到，quicksort 中每一递归层上的最坏情况分割产生 $\Theta(n^2)$ 的运行时间；直观上，这就是该算法的最坏情况运行时间。我们现在证明这一论断。

使用 substitution method（代换法，见 Section 4.3），我们可以证明 quicksort 的运行时间为 $O(n^2)$。令 $T(n)$ 为过程 QUICKSORT 在规模为 $n$ 的输入上的最坏情况时间。我们有递归式

```math
T(n) = \max_{0 \le q \le n-1} \left( T(q) + T(n-q-1) \right) + \Theta(n), \tag{7.1}
```

其中参数 $q$ 的取值范围从 $0$ 到 $n-1$，这是因为过程 PARTITION 产生两个总规模为 $n-1$ 的子问题。我们猜测 $T(n) \le cn^2$（$c$ 为某个常数）。把这个猜测代入递归式 (7.1)，得到

```math
\begin{aligned}
T(n) &\le \max_{0 \le q \le n-1} \left( cq^2 + c(n-q-1)^2 \right) + \Theta(n) \\
     &= c \cdot \max_{0 \le q \le n-1} \left( q^2 + (n-q-1)^2 \right) + \Theta(n).
\end{aligned}
```

表达式 $q^2 + (n-q-1)^2$ 在参数的取值范围 $0 \le q \le n-1$ 上的某端点处取得最大值。为验证这一论断，注意该表达式关于 $q$ 的二阶导数为正（见 Exercise 7.4-3）。这一……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 递归式 (7.1) 里的 $\max$ 是最坏情况分析的"对手机制"：我们不预设任何具体输入，而想象一个 adversary（对手）在每层递归挑出最能拖慢你的划分点 $q$——最坏情况就是这场博弈的估值。这一"内建对手"也解释了 Exercise 7.3-1 的答案。随机化算法之所以分析期望而非最坏，是因为量词次序变了：$\mathrm{E}[T]$ 是对随机数取期望、对每个固定输入都成立（$\forall x\ \mathrm{E}$），而最坏情况分析是对随机序列取最坏（$\exists$ 随机序列）——前者承诺"没有任何输入能让算法平均变慢"，后者只被极小概率的倒霉序列触发。7.3-2 还有个反直觉的小结论：RANDOM 的调用次数在最好与最坏情况下都是 $\Theta(n)$，因为每次 PARTITION 恰好掷一次骰子，而 PARTITION 的调用次数至多 $n$ 次——运气好坏体现在"掷出的点"上，而非"掷的次数"上。下一小节将把这个 $\max$ 放缩到端点值，完成 $O(n^2)$ 的代换证明。

---

> <span style="color:#7f8c8d;">CLRS §7.4, p.181</span>

（接上页）观察给了我们不等式 $\max_{0 \le q \le n-1} \left( q^2 + (n-q-1)^2 \right) \le (n-1)^2 = n^2 - 2n + 1$。继续对 $T(n)$ 进行放缩，我们得到

```math
\begin{aligned}
T(n) &\le cn^2 - c(2n - 1) + \Theta(n) \\
     &\le cn^2,
\end{aligned}
```

因为我们可以把常数 $c$ 选得足够大，使得 $c(2n-1)$ 项支配 $\Theta(n)$ 项。于是，$T(n) = O(n^2)$。我们在 Section 7.2 中看到过 quicksort 耗费 $\Omega(n^2)$ 时间的一个具体情况：划分不平衡的时候。另外，Exercise 7.4-1 要求你证明递归式 (7.1) 有一个解 $T(n) = \Omega(n^2)$。因此，quicksort 的（最坏情况）运行时间为 $\Theta(n^2)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页藏着一个值得命名的论证模板，可称为「凸性端点极大化」：$q^2 + (n-q-1)^2$ 在两端之和固定为 $n-1$ 的约束下，被分配到端点时最大、平分时最小。代数一眼看穿：令两端为 $a, b$，则 $a^2 + b^2 = (a+b)^2 - 2ab$——固定和时 $ab$ 在 $a = b$ 处最大、在端点处趋零，故平方和被"不平均"放大。这同时解释了两件事：快排最坏情况必然出现在极端不平衡的划分（平方代价天然惩罚不均），而平衡划分（$q \approx (n-1)/2$）使平方和最小、运行最快。以后凡是遇到"总和固定、比较平方和"的场合，先写出这个恒等式，它比求二阶导数（Exercise 7.4-3 的路线）更快也更透明，两者正好互相印证。最后留意证明的收尾手法：选足够大的 $c$ 让 $c(2n-1)$ 支配 $\Theta(n)$ 项，这是代换法里"常数吸收"的标准动作，与 4.3 节如出一辙。

#### 7.4.2 Expected running time（期望运行时间） <span style="color:#2471a3;">**[section]**</span>

我们已经见过 RANDOMIZED-QUICKSORT 的 expected running time（期望运行时间）为 $O(n \lg n)$ 背后的直观理由：如果在递归的每一层中，RANDOMIZED-PARTITION 所诱导的分割都把某个 constant fraction（常数比例）的元素放到分割的某一侧，那么 recursion tree（递归树）的深度就是 $\Theta(\lg n)$，且每一层上执行 $O(n)$ 的工作量。即便我们在这些层之间再加上若干新的层，且其分割是可能的最不平衡分割，总时间仍保持为 $O(n \lg n)$。我们可以精确地分析 RANDOMIZED-QUICKSORT 的期望运行时间：首先理解划分过程是如何运作的，然后利用这一理解推导出期望运行时间的 $O(n \lg n)$ 界。这一期望运行时间的 upper bound（上界），与我们在 Section 7.2 中见到的 $\Theta(n \lg n)$ 的最好情况界相结合，给出 $\Theta(n \lg n)$ 的期望运行时间。我们在全节中都假定被排序的各元素的值是互异的（distinct）。

#### Running time and comparisons（运行时间与比较） <span style="color:#2471a3;">**[section]**</span>

QUICKSORT 与 RANDOMIZED-QUICKSORT 这两个过程只在如何选取 pivot element（主元元素）上有所不同；在所有其他方面它们都是一样的。因此，我们可以这样来组织对 RANDOMIZED-QUICKSORT 的分析：讨论 QUICKSORT 与 PARTITION 这两个过程，但附带一个假设——主元元素是从传给 RANDOMIZED-PARTITION 的子数组中随机选取的。

QUICKSORT 的运行时间由花费在 PARTITION 过程中的时间所支配。每次调用 PARTITION，它都会选取一个主元元素，而这个元素不会再被包含在任何后续对 QUICKSORT 和 PARTITION 的 recursive call（递归调用）中。因此，在 quicksort 算法的整个执行过程中，对 PARTITION 的调用至多有 $n$ 次。对 PARTITION 的一次调用需要 $O(1)$ 时间，再加上一段与第 3–6 行 for 循环的 iteration（迭代）次数成正比的时间。该 for 循环的每次迭代都在第 4 行执行一次比较（comparison），把主元元素与数组 $A$ 的另一个元素相比较。因此，……（接下页）

---

> <span style="color:#7f8c8d;">CLRS Lemma 7.1, p.182</span>

（接上页）如果我们能够统计出第 4 行被执行的总次数，我们就能够界定在 QUICKSORT 的整个执行期间花费在该 for 循环中的总时间。

#### Lemma 7.1（引理 7.1） <span style="color:#2471a3;">**[lemma]**</span>

令 $X$ 是在 QUICKSORT 对一个含 $n$ 个元素的数组的整个执行过程中，PARTITION 的第 4 行所执行的比较（comparisons）次数。那么 QUICKSORT 的 running time（运行时间）为 $O(n + X)$。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  根据上面的讨论，该算法对 PARTITION 的调用至多有 $n$ 次，其中每一次调用都先做常数量的工作，然后执行 for 循环若干次。for 循环的每一次迭代都执行第 4 行。

因此，我们的目标是计算 $X$，即在所有对 PARTITION 的调用中执行的比较总数。我们并不试图分析每一次对 PARTITION 的调用中执行了多少次比较；相反，我们将推导出比较总数的一个总体上的界。为此，我们必须理解算法何时比较数组中的两个元素、何时不比较。为便于分析，我们把数组 $A$ 的元素重命名为 $z_1, z_2, \ldots, z_n$，其中 $z_i$ 是第 $i$ 小的元素。我们还定义集合 $Z_{ij} = \{ z_i, z_{i+1}, \ldots, z_j \}$ 为介于 $z_i$ 与 $z_j$ 之间（含端点）的元素集合。

算法何时比较 $z_i$ 与 $z_j$？为了回答这个问题，我们首先观察到：每一对元素至多被比较一次。为什么？元素只与主元元素比较，而且当某次 PARTITION 调用结束后，该次调用所用的主元元素再也不会与任何其他元素比较。

我们的分析使用 indicator random variables（指示器随机变量，见 Section 5.2）。我们定义

```math
X_{ij} = I\, \{\, z_i \text{ is compared to } z_j \,\},
```

这里我们考察的是这一比较是否在算法执行的任何时刻发生，而不仅仅是在某一次迭代或某一次 PARTITION 调用期间发生。由于每一对至多被比较一次，我们可以轻松地刻画该算法执行的比较总数：

```math
X = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{ij}.
```

对两边取 expectation（期望），然后利用 linearity of expectation（期望的线性性）和 Lemma 5.1（引理 5.1），我们得到

```math
\mathrm{E}[X] = \mathrm{E}\left[ \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{ij} \right]
```

……（接下页，期望的推导在第 183 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "每对元素至多比较一次"是全章期望分析得以成立的枢纽。原因在 PARTITION 的结构里：某元素要么是主元（一经定序、永久退场），要么与主元比较后被分到某一侧、与主元分道扬镳。于是比较次数 $X$ 不必逐次调用地追踪，而可按"元素对"全局记账：$X = \sum X_{ij}$，把"何时比较 $z_i$ 与 $z_j$"这一事件当作指示器随机变量求和。这种"换一个记账维度"的手法——从调用维度切到配对维度——是随机化算法期望分析中的常用套路，5.2 节的雇用问题（按候选人记账）与下一页按 $Z_{ij}$ 中"排名"记账的推导一脉相承。

---

> <span style="color:#7f8c8d;">CLRS §7.4.2, p.183</span>

（接上页）对上式两边取 expectation（期望），利用 indicator random variable（指示器随机变量）的定义（equation (5.10)）与 linearity of expectation（期望的线性性），我们得到

```math
\begin{aligned}
\mathrm{E}[X] = \mathrm{E}\left[ \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{ij} \right]
  &= \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \mathrm{E}[X_{ij}] \\
  &= \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \Pr\,\{\, z_i \text{ is compared to } z_j \,\}. \tag{7.2}
\end{aligned}
```

剩下的工作就是计算 $\Pr\,\{\, z_i \text{ is compared to } z_j \,\}$。我们的分析假定 RANDOMIZED-PARTITION 过程是随机且独立地（randomly and independently）选取每个 pivot（主元）的。

不妨想一想两个元素何时不被比较。考虑 quicksort 的一个输入：数字 $1$ 到 $10$（以任意顺序排列），并假定第一个主元元素（pivot element）是 $7$。那么第一次对 PARTITION 的调用就把这些数分成两个集合：$\{1, 2, 3, 4, 5, 6\}$ 与 $\{8, 9, 10\}$。在此过程中，主元元素 $7$ 与所有其他元素都进行了比较，但第一个集合中的任何数（例如 $2$）都不会、也永远不会与第二个集合中的任何数（例如 $9$）进行比较。

一般来说，因为我们假定元素值互不相同（distinct），一旦选取了某个主元 $x$ 满足 $z_i < x < z_j$，我们就知道 $z_i$ 与 $z_j$ 在此后的任何时刻都不可能再被比较。反过来，如果 $z_i$ 在 $Z_{ij}$ 中的任何其他元素之前被选为主元，那么 $z_i$ 将与 $Z_{ij}$ 中除自身之外的每个元素都比较。类似地，如果 $z_j$ 在 $Z_{ij}$ 中的任何其他元素之前被选为主元，那么 $z_j$ 也将与 $Z_{ij}$ 中除自身之外的每个元素比较。在前面那个例子里，$7$ 与 $9$ 之所以被比较，是因为 $7$ 是 $Z_{7,9}$ 中第一个被选为主元的元素；相反，$2$ 与 $9$ 永远不会被比较，因为从 $Z_{2,9}$ 中选出的第一个主元是 $7$。于是，$z_i$ 与 $z_j$ 被比较，当且仅当从 $Z_{ij}$ 中第一个被选为主元的元素是 $z_i$ 或者 $z_j$。

我们现在来计算这一事件发生的 probability（概率）。在 $Z_{ij}$ 中的某个元素被选为主元之前，整个集合 $Z_{ij}$ 都还处在同一个 partition（划分）之中。因此，$Z_{ij}$ 中的任何元素都等可能（equally likely）地成为第一个被选出的主元。由于集合 $Z_{ij}$ 含有 $j - i + 1$ 个元素，而且主元是随机且独立地选取的，任何一个给定元素成为第一个被选主元的概率都是 $1/(j - i + 1)$。于是我们有

```math
\begin{aligned}
\Pr\,\{\, z_i \text{ is compared to } z_j \,\}
  &= \Pr\,\{\, z_i \text{ or } z_j \text{ is first pivot chosen from } Z_{ij} \,\} \\
  &= \Pr\,\{\, z_i \text{ is first pivot chosen from } Z_{ij} \,\} + \Pr\,\{\, z_j \text{ is first pivot chosen from } Z_{ij} \,\} \\
  &= \frac{1}{j-i+1} + \frac{1}{j-i+1} \\
  &= \frac{2}{j-i+1}. \tag{7.3}
\end{aligned}
```

……（接下页，式 (7.2) 与 (7.3) 的合并及求和估计在第 184 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (7.3) 是整个期望分析的"点睛之笔"。它把"两个元素是否比较"这一全局事件，归结为"$Z_{ij}$ 中第一个被选为主元的是谁"这一局部事件——因为一旦有第三方元素（值介于 $z_i$ 与 $z_j$ 之间者）先当上主元，$z_i$ 与 $z_j$ 就会被分进不同的划分而永别。而"第一个被选出的主元"在 $Z_{ij}$ 的 $j-i+1$ 个候选中均匀分布，于是每对的比较概率恰为 $2/(j-i+1)$。下一页把这个概率代回式 (7.2) 后，只需一步变量替换 $k = j - i$，就能用调和级数的界收出 $O(n \lg n)$。

---

> <span style="color:#7f8c8d;">CLRS §7.4.2 + Exercises 7.4-1~4, p.184</span>

（接上页）式 (7.3) 的第二行成立，是因为这两个事件是 mutually exclusive（互斥）的。把 equation (7.2) 与 equation (7.3) 结合起来，我们得到

```math
\mathrm{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \frac{2}{j-i+1}.
```

我们可以用 change of variables（变量替换，$k = j - i$）以及 equation (A.7) 中关于 harmonic series（调和级数）的界来求这个和的值：

```math
\begin{aligned}
\mathrm{E}[X] &= \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \frac{2}{j-i+1}
   = \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k+1}
   < \sum_{i=1}^{n-1} \sum_{k=1}^{n} \frac{2}{k} \\
   &= \sum_{i=1}^{n-1} O(\lg n) \\
   &= O(n \lg n). \tag{7.4}
\end{aligned}
```

于是我们得出结论：使用 RANDOMIZED-PARTITION 时，当元素值互不相同，quicksort 的 expected running time（期望运行时间）为 $O(n \lg n)$。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**7.4-1**

Show that in the recurrence

```math
T(n) = \max_{0 \le q \le n-1} \left( T(q) + T(n-q-1) \right) + \Theta(n),
```

$T(n) = \Omega(n^2)$.

**7.4-2**

Show that quicksort's best-case running time is $\Omega(n \lg n)$.

**7.4-3**

Show that the expression $q^2 + (n - q - 1)^2$ achieves a maximum over $q = 0, 1, \ldots, n - 1$ when $q = 0$ or $q = n - 1$.

**7.4-4**

Show that RANDOMIZED-QUICKSORT's expected running time is $\Omega(n \lg n)$.

……（接下页，习题 7.4-5~6 与 Problems 在第 185 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (7.4) 的三步变换值得细品：第一步变量替换 $k = j - i$ 把"内层起点随 $i$ 变化"的求和标准化；第二步把 $2/(k+1)$ 放宽为 $2/k$（分母变小、值变大），从而把一截一截的"部分调和级数"统一成完整的调和级数——其部分和为 $\Theta(\lg n)$（Appendix A 的式 (A.7)）；第三步注意到内层和不再依赖 $i$，直接乘上外层的 $n-1$ 项。这与 7.2.1 节最坏情况分析中"代换法"的收尾手法互为镜像：那里证上界 $O(n^2)$，这里证期望上界 $O(n \lg n)$；习题 7.4-1 与 7.4-4 恰好让你补出对应的下界，合起来即 $\Theta$ 界。

---

> <span style="color:#7f8c8d;">CLRS Exercises 7.4-5~6 + Problems 7-1, p.185</span>

（接上页）

**7.4-5**

We can improve the running time of quicksort in practice by taking advantage of the fast running time of insertion sort when its input is "nearly" sorted. Upon calling quicksort on a subarray with fewer than $k$ elements, let it simply return without sorting the subarray. After the top-level call to quicksort returns, run insertion sort on the entire array to finish the sorting process. Argue that this sorting algorithm runs in $O(nk + n \lg(n/k))$ expected time. How should we pick $k$, both in theory and in practice?

**7.4-6 ★**

Consider modifying the PARTITION procedure by randomly picking three elements from array $A$ and partitioning about their median (the middle value of the three elements). Approximate the probability of getting at worst an $\alpha$-to-$(1-\alpha)$ split, as a function of $\alpha$ in the range $0 < \alpha < 1$.

## Problems for Chapter 7（第 7 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 7-1 · Hoare partition correctness（Hoare 划分的正确性） <span style="color:#2471a3;">**[problem]**</span>

The version of PARTITION given in this chapter is not the original partitioning algorithm. Here is the original partition algorithm, which is due to C. A. R. Hoare:

```text
HOARE-PARTITION(A, p, r)
 1  x = A[p]
 2  i = p - 1
 3  j = r + 1
 4  while TRUE
 5      repeat
 6          j = j - 1
 7      until A[j] ≤ x
 8      repeat
 9          i = i + 1
10      until A[i] ≥ x
11      if i < j
12          exchange A[i] with A[j]
13      else return j
```

a. Demonstrate the operation of HOARE-PARTITION on the array $A = \langle 13, 19, 9, 5, 12, 8, 7, 4, 11, 2, 6, 21 \rangle$, showing the values of the array and auxiliary values after each iteration of the while loop in lines 4–13.

……（接下页，Problem 7-1 的 b–e 小问在第 186 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> HOARE-PARTITION 与本章的 Lomuto 版 PARTITION 有两点不同：其一，主元取的是子数组**第一个**元素 $A[p]$（而非 $A[r]$），且两个下标 $i$、$j$ 分别从两端向中间**相向扫描**（$j$ 自右向左找 $\le x$ 的元素，$i$ 自左向右找 $\ge x$ 的元素）；其二，当 $i \ge j$ 时返回切分点 $j$，主元本身留在左半划分里而不做"归位交换"。习题 7.4-6 的"三者取中"（median-of-3）思路与 Problem 7-5 呼应，它通过降低极端分割的概率来改进 RANDOMIZED-QUICKSORT 的常数因子。

---

> <span style="color:#7f8c8d;">CLRS Problems 7-1 / 7-2, p.186</span>

（接上页）

The next three questions ask you to give a careful argument that the procedure HOARE-PARTITION is correct. Assuming that the subarray $A[p..r]$ contains at least two elements, prove the following:

b. The indices $i$ and $j$ are such that we never access an element of $A$ outside the subarray $A[p..r]$.

c. When HOARE-PARTITION terminates, it returns a value $j$ such that $p \le j < r$.

d. Every element of $A[p..j]$ is less than or equal to every element of $A[j+1..r]$ when HOARE-PARTITION terminates.

The PARTITION procedure in Section 7.1 separates the pivot value (originally in $A[r]$) from the two partitions it forms. The HOARE-PARTITION procedure, on the other hand, always places the pivot value (originally in $A[p]$) into one of the two partitions $A[p..j]$ and $A[j+1..r]$. Since $p \le j < r$, this split is always nontrivial.

e. Rewrite the QUICKSORT procedure to use HOARE-PARTITION.

### Problem 7-2 · Quicksort with equal element values（元素取值相等时的快速排序） <span style="color:#2471a3;">**[problem]**</span>

The analysis of the expected running time of randomized quicksort in Section 7.4.2 assumes that all element values are distinct. In this problem, we examine what happens when they are not.

a. Suppose that all element values are equal. What would be randomized quicksort's running time in this case?

b. The PARTITION procedure returns an index $q$ such that each element of $A[p..q-1]$ is less than or equal to $A[q]$ and each element of $A[q+1..r]$ is greater than $A[q]$. Modify the PARTITION procedure to produce a procedure PARTITION′(A, p, r), which permutes the elements of $A[p..r]$ and returns two indices $q$ and $t$, where $p \le q \le t \le r$, such that

- all elements of $A[q..t]$ are equal,
- each element of $A[p..q-1]$ is less than $A[q]$, and
- each element of $A[t+1..r]$ is greater than $A[q]$.

Like PARTITION, your PARTITION′ procedure should take $\Theta(r - p)$ time.

c. Modify the RANDOMIZED-PARTITION procedure to call PARTITION′, and name the new procedure RANDOMIZED-PARTITION′. Then modify the QUICKSORT procedure to produce a procedure QUICKSORT′(A, p, r) that calls ……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题直指 7.4.2 节分析的一个软肋——"元素值互不相同"这一假设。当所有元素相等时，Lomuto 型 PARTITION 每次都产生 $0$ 与 $n-1$ 规模的最坏分割，quicksort 退化为 $\Theta(n^2)$（见 a 问）；而 PARTITION′ 把"与主元相等"的元素聚成一块 $A[q..t]$ 并从递归中剔除（见 c 问），输入全等时甚至一趟即完成。这种"三路划分"（3-way partition）思想在实践中是处理大量重复关键字的标准手段。

---

> <span style="color:#7f8c8d;">CLRS Problems 7-2 / 7-3, p.187</span>

（接上页）RANDOMIZED-PARTITION′ and recurses only on partitions of elements not known to be equal to each other.

d. Using QUICKSORT′, how would you adjust the analysis in Section 7.4.2 to avoid the assumption that all elements are distinct?

### Problem 7-3 · Alternative quicksort analysis（快速排序的另一种分析） <span style="color:#2471a3;">**[problem]**</span>

An alternative analysis of the running time of randomized quicksort focuses on the expected running time of each individual recursive call to RANDOMIZED-QUICKSORT, rather than on the number of comparisons performed.

a. Argue that, given an array of size $n$, the probability that any particular element is chosen as the pivot is $1/n$. Use this to define indicator random variables $X_q = I\,\{\text{the $q$th smallest element is chosen as the pivot}\}$. What is $\mathrm{E}[X_q]$?

b. Let $T(n)$ be a random variable denoting the running time of quicksort on an array of size $n$. Argue that

```math
\mathrm{E}[T(n)] = \mathrm{E}\left[ \sum_{q=1}^{n} X_q \left( T(q-1) + T(n-q) + \Theta(n) \right) \right]. \tag{7.5}
```

c. Show that we can rewrite equation (7.5) as

```math
\mathrm{E}[T(n)] = \frac{2}{n} \sum_{q=2}^{n-1} \mathrm{E}[T(q)] + \Theta(n). \tag{7.6}
```

d. Show that

```math
\sum_{k=2}^{n-1} k \lg k \le \frac{1}{2} n^2 \lg n - \frac{1}{8} n^2. \tag{7.7}
```

(Hint: Split the summation into two parts, one for $k = 2, 3, \ldots, \lceil n/2 \rceil - 1$ and one for $k = \lceil n/2 \rceil, \ldots, n-1$.)

e. Using the bound from equation (7.7), show that the recurrence in equation (7.6) has the solution $\mathrm{E}[T(n)] = \Theta(n \lg n)$.

(Hint: Show, by substitution, that $\mathrm{E}[T(n)] \le a n \lg n$ for sufficiently large $n$ and for some positive constant $a$.)

……（接下页，Problem 7-4 在第 188 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题给出了 7.4.2 节之外的另一条分析路线：不再数"比较对"，而是直接对**每次递归调用**的期望代价记账。注意 $\mathrm{E}[X_q] = 1/n$（a 问）之后，式 (7.5) 中规模为 $q-1$ 与 $n-q$ 的两个子问题各以 $1/n$ 的概率出现，把 $q=1$、$q=n$ 两个边界情形（子问题规模为 $0$）与 $\Theta(n)$ 的划分代价合并进 $\Theta(n)$ 项，并对称合并 $\mathrm{E}[T(q-1)]$ 与 $\mathrm{E}[T(n-q)]$ 的系数，即得式 (7.6)——它与 7.4.2 节式 (7.2) 形似而神不同：那里是对"元素对"求和，这里是对"子问题规模"求和。d 问的不等式 (7.7) 则是主方法思想（一半贡献一半，各约 $n^2 \lg n / 2$ 减去修正项）在求和上的翻版。

---

> <span style="color:#7f8c8d;">CLRS Problems 7-4 / 7-5, p.188</span>

（接上页）

### Problem 7-4 · Stack depth for quicksort（快速排序的栈深） <span style="color:#2471a3;">**[problem]**</span>

The QUICKSORT algorithm of Section 7.1 contains two recursive calls to itself. After QUICKSORT calls PARTITION, it recursively sorts the left subarray and then it recursively sorts the right subarray. The second recursive call in QUICKSORT is not really necessary; we can avoid it by using an iterative control structure. This technique, called tail recursion, is provided automatically by good compilers. Consider the following version of quicksort, which simulates tail recursion:

```text
TAIL-RECURSIVE-QUICKSORT(A, p, r)
 1  while p < r
 2      // Partition and sort left subarray.
 3      q = PARTITION(A, p, r)
 4      TAIL-RECURSIVE-QUICKSORT(A, p, q - 1)
 5      p = q + 1
```

a. Argue that TAIL-RECURSIVE-QUICKSORT(A, 1, A.length) correctly sorts the array $A$.

Compilers usually execute recursive procedures by using a stack that contains pertinent information, including the parameter values, for each recursive call. The information for the most recent call is at the top of the stack, and the information for the initial call is at the bottom. Upon calling a procedure, its information is pushed onto the stack; when it terminates, its information is popped. Since we assume that array parameters are represented by pointers, the information for each procedure call on the stack requires $O(1)$ stack space. The stack depth is the maximum amount of stack space used at any time during a computation.

b. Describe a scenario in which TAIL-RECURSIVE-QUICKSORT's stack depth is $\Theta(n)$ on an $n$-element input array.

c. Modify the code for TAIL-RECURSIVE-QUICKSORT so that the worst-case stack depth is $\Theta(\lg n)$. Maintain the $O(n \lg n)$ expected running time of the algorithm.

### Problem 7-5 · Median-of-3 partition（三者取中划分） <span style="color:#2471a3;">**[problem]**</span>

One way to improve the RANDOMIZED-QUICKSORT procedure is to partition around a pivot that is chosen more carefully than by picking a random element from the subarray. One common approach is the median-of-3 method: choose the pivot as the median (middle element) of a set of 3 elements randomly selected from the subarray. (See Exercise 7.4-6.) For this problem, let us assume that the elements in the input array $A[1..n]$ are distinct and that $n \ge 3$. We denote the ……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题的核心观察是：TAIL-RECURSIVE-QUICKSORT 把"对右半数组的递归调用"改写成了 while 循环里的参数更新（第 5 行），省掉了一次栈帧的压入与弹出；但若左子数组总是很大（例如输入已排好序时 PARTITION 每次切出规模 $n-2$ 与 $0$ 的两半），第 4 行的递归就会层层嵌套，栈深达 $\Theta(n)$（b 问）。c 问的修复办法简单而经典：**先对较小的子数组递归，对较大的子数组循环**（把第 4–5 行改为"若 $q - p < r - q$ 则递归左半、令 $p = q + 1$，否则递归右半、令 $r = q - 1$"）。由于每次至少把一半规模的子问题交给迭代，栈深不超过 $\lg n$，而期望运行时间不变。"尾递归"（tail recursion）只是把最坏栈深从 $\Theta(n)$ 改善到 $\Theta(\lg n)$ 的必要铺垫，靠它自身并不够。

---

> <span style="color:#7f8c8d;">CLRS Problems 7-5 / 7-6, p.189</span>

（接上页）sorted output array by $A'[1..n]$. Using the median-of-3 method to choose the pivot element $x$, define $p_i = \Pr\,\{ x = A'[i] \}$.

a. Give an exact formula for $p_i$ as a function of $n$ and $i$ for $i = 2, 3, \ldots, n-1$. (Note that $p_1 = p_n = 0$.)

b. By what amount have we increased the likelihood of choosing the pivot as $x = A'[\lfloor (n+1)/2 \rfloor]$, the median of $A[1..n]$, compared with the ordinary implementation? Assume that $n \rightarrow \infty$, and give the limiting ratio of these probabilities.

c. If we define a "good" split to mean choosing the pivot as $x = A'[i]$, where $n/3 \le i \le 2n/3$, by what amount have we increased the likelihood of getting a good split compared with the ordinary implementation? (Hint: Approximate the sum by an integral.)

d. Argue that in the $\Omega(n \lg n)$ running time of quicksort, the median-of-3 method affects only the constant factor.

### Problem 7-6 · Fuzzy sorting of intervals（区间的模糊排序） <span style="color:#2471a3;">**[problem]**</span>

Consider a sorting problem in which we do not know the numbers exactly. Instead, for each number, we know an interval on the real line to which it belongs. That is, we are given $n$ closed intervals of the form $[a_i, b_i]$, where $a_i \le b_i$. We wish to fuzzy-sort these intervals, i.e., to produce a permutation $\langle i_1, i_2, \ldots, i_n \rangle$ of the intervals such that for $j = 1, 2, \ldots, n$, there exist $c_j \in [a_{i_j}, b_{i_j}]$ satisfying

```math
c_1 \le c_2 \le \cdots \le c_n.
```

a. Design a randomized algorithm for fuzzy-sorting $n$ intervals. Your algorithm should have the general structure of an algorithm that quicksorts the left endpoints (the $a_i$ values), but it should take advantage of overlapping intervals to improve the running time. (As the intervals overlap more and more, the problem of fuzzy-sorting the intervals becomes progressively easier. Your algorithm should take advantage of such overlapping, to the extent that it exists.)

b. Argue that your algorithm runs in expected time $\Theta(n \lg n)$ in general, but runs in expected time $\Theta(n)$ when all of the intervals overlap (i.e., when there exists a value $x$ such that $x \in [a_i, b_i]$ for all $i$). Your algorithm should not be checking for this case explicitly; rather, its performance should naturally improve as the amount of overlap increases.

……（接下页，Chapter notes 在第 190 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Problem 7-5 的四个小问层层递进：a 问枚举"三元组的中位数恰为第 $i$ 小元素"的组合数，得 $p_i = \dfrac{2(i-1)(n-i)}{n(n-1)(n-2)}$（注意 $p_1 = p_n = 0$：三元组的中位数不可能是最小或最大元素）；b、c 两问把 median-of-3 与"均匀随机取主元"的概率分布 $1/n$ 相除、取极限（c 问用积分近似求和 $\int_{n/3}^{2n/3} p_i \,\mathrm{d}i$）；d 问点破要害——median-of-3 改变的只是"好分割"的概率常数，而 quicksort 的 $\Omega(n \lg n)$ 下界由比较次数决定，故只能影响常数因子。Problem 7-6 则是分治思想的绝妙练习：当区间大量交叠时，"取一个公共点 $x$ 作主元、把与 $x$ 相交的区间聚为一组"即可让问题规模骤减，全交叠时退化为线性扫描——算法无需显式检测该情形，性能随交叠程度自然提升。

---

> <span style="color:#7f8c8d;">CLRS Notes for Chapter 7, p.190</span>

## Chapter notes（第 7 章注释） <span style="color:#2471a3;">**[reference]**</span>

> <span style="color:#7f8c8d;">[note] 按规范，本章 notes（注释/参考文献）保留英文原文，不作翻译；文中受损的数学记号已按原书恢复。</span>

The quicksort procedure was invented by Hoare [170]; Hoare's version appears in Problem 7-1. The PARTITION procedure given in Section 7.1 is due to N. Lomuto. The analysis in Section 7.4 is due to Avrim Blum. Sedgewick [305] and Bentley [43] provide a good reference on the details of implementation and how they matter.

McIlroy [248] showed how to engineer a "killer adversary" that produces an array on which virtually any implementation of quicksort takes $\Theta(n^2)$ time. If the implementation is randomized, the adversary produces the array after seeing the random choices of the quicksort algorithm.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这两段 notes 浓缩了快速排序六十余年的工程史：quicksort 由 C. A. R. Hoare 于 1962 年发表（文献 [170]，即 Problem 7-1 中的 HOARE-PARTITION 所本），本章正文使用的 PARTITION 版本出自 N. Lomuto；7.4 节的期望分析归功于 Avrim Blum。Sedgewick [305] 与 Bentley [43] 是实现细节（如小数组改用插入排序，即习题 7.4-5 的思路）对性能影响的经典参考。McIlroy [248] 构造的 "killer adversary"（杀手对手）尤其值得一提：它能对几乎任何 quicksort 实现动态喂出使其退化为 $\Theta(n^2)$ 的输入——即使实现是随机化的，对手也能在看到随机选择后再产出数组。这一结果提醒我们：随机化的好处依赖于随机数不被对手预测，这与第 5 章 randomized algorithm（随机化算法）的概率分析前提一脉相承。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 顺带一提，第 7 章至此收官。本章三大要点：PARTITION 的循环不变式、最坏情况 $\Theta(n^2)$ 与最好情况 $\Theta(n \lg n)$ 的划分分析、以及基于"元素对比较概率 $2/(j-i+1)$"的期望分析。下一章将证明：任何 comparison sort（比较排序）在最坏情况下都必须做 $\Omega(n \lg n)$ 次比较——quicksort（平均意义）与归并排序、堆排序在渐近意义上已是比较排序的天花板。

---

> <span style="color:#7f8c8d;">CLRS Chapter 8 + §8.1, p.191</span>

## Chapter 8（第 8 章）· Sorting in Linear Time（线性时间排序） <span style="color:#2471a3;">**[section]**</span>

至此，我们已经介绍了好几种能够在 $O(n \lg n)$ 时间内对 $n$ 个数进行排序的 algorithm（算法）。merge sort（归并排序）与 heapsort（堆排序）在最坏情况下达到这一 upper bound（上界）；quicksort（快速排序）则在平均意义上达到它。此外，对其中每一种算法，我们都能构造出一个由 $n$ 个输入数组成的 sequence（序列），使得该算法的 running time（运行时间）达到 $\Omega(n \lg n)$。

这些算法共享一个有趣的性质：它们所确定的 sorted order（排序顺序）**仅仅基于输入元素之间的比较**。我们把这类排序算法称为 comparison sorts（比较排序）。迄今介绍的所有排序算法都是 comparison sorts。

在 Section 8.1 中，我们将证明：任何 comparison sort 为了对 $n$ 个元素排序，在最坏情况下都必须进行 $\Omega(n \lg n)$ 次 comparison（比较）。因此，merge sort 与 heapsort 是渐近最优的（asymptotically optimal），不存在比它们快过常数因子以上的 comparison sort。

Section 8.2、Section 8.3 与 Section 8.4 将考察三种能够在线性时间（linear time）内运行的排序算法——counting sort（计数排序）、radix sort（基数排序）与 bucket sort（桶排序）。当然，这些算法之所以能突破，是因为它们使用比较之外的操作来确定排序顺序。因此，$\Omega(n \lg n)$ 的 lower bound（下界）对它们并不适用。

### Section 8.1 · Lower bounds for sorting（排序的下界） <span style="color:#2471a3;">**[section]**</span>

在一个 comparison sort 中，我们仅使用元素之间的比较来获取输入序列 $\langle a_1, a_2, \ldots, a_n \rangle$ 中元素之间的 order information（顺序信息）。也就是说，给定两个元素 $a_i$ 与 $a_j$，我们执行下列测试之一：

```math
a_i < a_j, \quad a_i \le a_j, \quad a_i = a_j, \quad a_i \ge a_j, \quad a_i > a_j,
```

以此确定它们的相对顺序。我们不可以检视这些元素的取值，也不可以用任何其他方式获取关于它们的顺序信息。

在本节中，我们不失一般性地（without loss of generality）假定所有输入元素互不相同（distinct）。有了这一假设，形如 $a_i = a_j$ 的比较便毫无用处，于是我们可以假定不做这类比较。我们还注意到，比较 $a_i \le a_j$、$a_i \ge a_j$、$a_i > a_j$ 与 $a_i < a_j$ 全都是等价的，因为它们 ……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本章开篇先立"靶子"再射箭：既然此前所有 $O(n \lg n)$ 的排序算法都只靠比较来定序，那就先证明**任何**只靠比较的排序在最坏情况下都逃不掉 $\Omega(n \lg n)$ 次比较（Section 8.1 的决策树论证），随后（Section 8.2–8.4）再展示三种绕开比较、利用关键字内部结构的线性时间算法。本页末句的"等价性"观察是下界证明的第一块铺路石：五种比较测试在信息量上只有两档——"≤"与">"，下一页将据此把模型彻底简化为"每次比较只有两种结果"。

---

> <span style="color:#7f8c8d;">CLRS §8.1 + Figure 8.1, p.192</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 8.1 的示意图：对三个元素做插入排序的 decision tree（决策树）。每个内部结点标注一次比较（如 $1{:}2$ 表示比较 $a_1$ 与 $a_2$），"≤"走左分支、">"走右分支；六个叶子恰为三种元素的全部 $3! = 6$ 种排列。深色阴影路径对应输入 $\langle a_1 = 6,\ a_2 = 8,\ a_3 = 5 \rangle$ 的排序过程：先比较 $1{:}2$（$6 \le 8$，走左），再比较 $2{:}3$（$8 > 5$，走右），最后比较 $1{:}3$（$6 > 5$，走右），到达叶子 $\langle 3, 1, 2 \rangle$，给出排序结果 $a_3 = 5 \le a_1 = 6 \le a_2 = 8$。为对照原书排版，下图以文本示意重绘。</span>

```text
                         1:2
                      ≤ /    \ >
                2:3                1:3
              ≤ /  \ >            ≤ /  \ >
       〈1,2,3〉      1:3      〈2,1,3〉      2:3
                ≤ /  \ >        ≤ /  \ >
         〈1,3,2〉    〈3,1,2〉  〈2,3,1〉   〈3,2,1〉
```

**Figure 8.1（图 8.1）** 对三个元素执行插入排序的 decision tree（决策树）。标注为 $i{:}j$ 的 internal node（内部结点）表示一次 $a_i$ 与 $a_j$ 之间的比较；标注为排列 $\langle \pi(1), \pi(2), \ldots, \pi(n) \rangle$ 的叶结点表示顺序 $a_{\pi(1)} \le a_{\pi(2)} \le \cdots \le a_{\pi(n)}$。阴影路径给出排序输入序列 $\langle a_1 = 6, a_2 = 8, a_3 = 5 \rangle$ 时所作的判定；叶子处的排列 $\langle 3, 1, 2 \rangle$ 表明排序后的顺序为 $a_3 = 5 \le a_1 = 6 \le a_2 = 8$。输入元素共有 $3! = 6$ 种可能的排列，因此该决策树必须至少有 6 个叶子。

（接上页）……它们给出关于 $a_i$ 与 $a_j$ 的相对顺序的完全相同的信息。因此，我们假定所有比较都具有 $a_i \le a_j$ 的形式。

#### The decision-tree model（决策树模型） <span style="color:#2471a3;">**[section]**</span>

我们可以抽象地用 decision trees（决策树）来审视 comparison sorts（比较排序）。一个 decision tree（决策树）是一棵 full binary tree（满二叉树），它表示某个特定排序算法在处理给定规模的输入时，所执行的元素之间的比较。控制、数据移动以及算法的其他方面一律忽略。图 8.1 展示了 Section 2.1 的 insertion sort（插入排序）算法作用于三元素输入序列时对应的决策树。

在一棵决策树中，我们把每个 internal node（内部结点）标注为 $i{:}j$，其中 $i$、$j$ 满足 $1 \le i, j \le n$，而 $n$ 是输入序列中的元素个数。我们还把每个 leaf（叶结点）标注为一个 permutation（排列）$\langle \pi(1), \pi(2), \ldots, \pi(n) \rangle$。（排列的背景知识见 Section C.1。）排序算法的执行对应于沿着一条 simple path（简单路径）从决策树的根（root）走向某个叶结点。每个内部结点表示一次比较 $a_i \le a_j$：一旦知道 $a_i \le a_j$，左子树（left subtree）便决定后续的比较；而知道 $a_i > a_j$ 后，右子树（right subtree）决定后续的比较。当我们到达一个叶结点时，排序算法已经确立了顺序 $a_{\pi(1)} \le a_{\pi(2)} \le \cdots \le a_{\pi(n)}$。因为任何一个正确的排序算法都必须能够产生其输入的每一种排列，所以 $n$ 个元素上的 $n!$ 种排列中的每一种，都必须作为该 comparison sort 的决策树的某个叶子出现，排序算法才是正确的。此外，这些叶子中的每一个都必须可以从根出发、经由一条对应于某次真实执行的下向路径到达。……（接下页，定理 8.1 的证明在第 193 页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "full binary tree（满二叉树）"在此书中指**每个结点都有 0 个或 2 个孩子**的二叉树（即没有"独生子"结点），切勿与中文教材里"每层都满"的满二叉树概念混淆。图 8.1 值得逐枝玩味：插入排序在 $a_1 \le a_2$ 时还要再比较 $2{:}3$ 才能分辨 $\langle 1,2,3 \rangle$ 与 $\langle 3,1,2 \rangle$ 或 $\langle 1,3,2 \rangle$，这说明决策树的结构忠实复刻了算法"每次比较、按结果走分支"的动态过程。下一页将从这个"必须至少有 $n!$ 个可达叶子"的计数论证出发，用二叉树高度的下界 $\lg(n!)$（配合 Stirling 近似）一举得到定理 8.1：任何比较排序最坏情况下的比较次数为 $\Omega(n \lg n)$。

---

> <span style="color:#7f8c8d;">CLRS §8.1, p.193</span>

（接上页）……这次 comparison sort（比较排序）的 execution（执行）。（我们把这样的叶子称为 "reachable"（可达的）。）因此，我们只考虑每一种 permutation（排列）都作为一个可达叶结点出现的 decision trees（决策树）。

#### A lower bound for the worst case（最坏情况下的下界） <span style="color:#2471a3;">**[section]**</span>

从一棵 decision tree（决策树）的 root（根）到它的任一可达叶结点的最长 simple path（简单路径）的 length（长度），代表对应的 sorting algorithm（排序算法）在最坏情况下执行的比较次数。因此，对一个给定的 comparison sort algorithm（比较排序算法）而言，其 worst-case number of comparisons（最坏情况比较次数）就等于它的决策树的 height（高度）。于是，对"每一种排列都作为可达叶结点出现"的所有决策树的高度取一个 lower bound（下界），就是对任何 comparison sort algorithm 运行时间的下界。下面的定理给出了这样一个下界。

#### Theorem 8.1（定理 8.1） <span style="color:#2471a3;">**[theorem]**</span>

任何 comparison sort algorithm 都需要 $\Omega(n \lg n)$ 次比较。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  由前面的讨论可知，只需确定一棵"每一种排列都作为可达叶结点出现"的决策树的高度。考虑一棵高度为 $h$、有 $l$ 个可达叶结点的决策树，它对应于对 $n$ 个元素的一个 comparison sort。因为输入的 $n!$ 种 permutation 中的每一种都作为某个叶结点出现，所以有 $n! \le l$。又因为一棵高度为 $h$ 的 binary tree（二叉树）的叶结点不超过 $2^h$ 个，故有

```math
n! \le l \le 2^h,
```

对其取对数，即得

```math
\begin{aligned}
h &\ge \lg(n!) \quad &\text{(since the $\lg$ function is monotonically increasing)} \\
  &= \Omega(n \lg n). \quad &\text{(by equation (3.19))}
\end{aligned}
```

#### Corollary 8.2（推论 8.2） <span style="color:#2471a3;">**[corollary]**</span>

Heapsort（堆排序）与 merge sort（归并排序）是渐近最优的（asymptotically optimal）comparison sorts（比较排序）。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  Heapsort 与 merge sort 运行时间的 $O(n \lg n)$ upper bound（上界），与 Theorem 8.1 给出的 $\Omega(n \lg n)$ worst-case（最坏情况）lower bound（下界）恰好吻合。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**8.1-1**

What is the smallest possible depth of a leaf in a decision tree for a comparison sort?……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 定理 8.1 的证明是全章的"承重墙"：$n! \le l \le 2^h$ 三个量排成一串后，一次取对数就完成了全部工作——左边是必须出现的排列数（正确性要求），右边是高度 $h$ 所能容纳的叶子数上限（二叉树的组合性质），夹逼之下 $h \ge \lg(n!) = \Omega(n \lg n)$。其中 $\lg(n!) = \Omega(n \lg n)$ 直接引用 equation (3.19)（由 Stirling 近似导出），无需重新证明。推论 8.2 则把第 2 章的 $O(n \lg n)$ 上界与这里的 $\Omega(n \lg n)$ 下界合在一起，说明 heapsort 与 merge sort 在渐近意义上已经"无提升空间"（就比较次数而言）。

---

> <span style="color:#7f8c8d;">CLRS §8.1–8.2, p.194</span>

**8.1-2**

Obtain asymptotically tight bounds on $\lg(n!)$ without using Stirling's approximation. Instead, evaluate the summation $\sum_{k=1}^{n} \lg k$ using techniques from Section A.2.

**8.1-3**

Show that there is no comparison sort whose running time is linear for at least half of the $n!$ inputs of length $n$. What about a fraction of $1/n$ of the inputs of length $n$? What about a fraction $1/2^n$?

**8.1-4**

Suppose that you are given a sequence of $n$ elements to sort. The input sequence consists of $n/k$ subsequences, each containing $k$ elements. The elements in a given subsequence are all smaller than the elements in the succeeding subsequence and larger than the elements in the preceding subsequence. Thus, all that is needed to sort the whole sequence of length $n$ is to sort the $k$ elements in each of the $n/k$ subsequences. Show an $\Omega(n \lg k)$ lower bound on the number of comparisons needed to solve this variant of the sorting problem. (Hint: It is not rigorous to simply combine the lower bounds for the individual subsequences.)

### Section 8.2 · Counting sort（计数排序） <span style="color:#2471a3;">**[section]**</span>

Counting sort（计数排序）假定 $n$ 个 input elements（输入元素）中的每一个都是 $0$ 到 $k$ 区间内的一个 integer（整数），其中 $k$ 为某个整数。当 $k = O(n)$ 时，该排序的运行时间为 $\Theta(n)$。

Counting sort 对每个输入元素 $x$，确定小于 $x$ 的元素个数。它利用这一信息，直接把元素 $x$ 放到输出数组中的相应位置上。例如，如果有 17 个元素小于 $x$，那么 $x$ 就应当属于输出位置 18。当若干元素具有相同值时，我们必须对这个方案稍作修改，因为我们不想把它们全都放进同一个位置。

在 counting sort 的代码中，我们假定输入是一个数组 $A[1..n]$，因此 $A.\text{length} = n$。我们还需要另外两个数组：数组 $B[1..n]$ 存放排序后的 output（输出），数组 $C[0..k]$ 提供临时工作存储（temporary working storage）。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 练习 8.1-2~8.1-4 是把定理 8.1 的下界"用到刀刃上"的三道题：8.1-2 练习不用 Stirling 近似、改用 Appendix A.2 的求和技术直接估计 $\lg(n!)$；8.1-3 探讨这一下界对"多少比例的输入"成立——结论相当反直觉：哪怕只对 $n!$ 个输入中的一半达到线性时间都不可能，而可以线性时间的输入比例最多只有 $1/2^n$ 这个量级；8.1-4 是一个"分块有序"的变体，把定理的证明思路中的 $n!$ 换成 $(k!)^{n/k}$，即可得到 $\Omega(n \lg k)$。下一页起进入第一个线性时间排序算法：counting sort。

---

> <span style="color:#7f8c8d;">CLRS §8.2 + Figure 8.2, p.195</span>

> <span style="color:#7f8c8d;">[note] 本页主体为图 8.2 的示意图：COUNTING-SORT 在输入数组 $A[1..8]$ 上的运行过程，其中 $A$ 的每个元素都是不超过 $k = 5$ 的非负整数。(a) 为执行到第 5 行后数组 $A = \langle 2, 5, 3, 0, 2, 3, 0, 3 \rangle$ 与辅助数组 $C$ 的状态（$C[i]$ 记录值为 $i$ 的元素个数）；(b) 为执行到第 8 行后的 $C$（前缀和）；(c)–(e) 为第 10–12 行循环分别执行一、二、三次后的输出数组 $B$ 与辅助数组 $C$——每次迭代从 $A$ 中取一个元素放入 $B$，并把对应的计数减 1；数组 $B$ 中只有浅色阴影的元素已被填入。(f) 为最终排好序的输出数组 $B$。为对照原书排版，下图以文本示意重绘（"·"表示尚未填入的位置）。</span>

```text
(a)  A: 索引  1 2 3 4 5 6 7 8      C: 索引  0 1 2 3 4 5
     值      2 5 3 0 2 3 0 3      值      2 0 2 3 0 1

(b)  C: 索引  0 1 2 3 4 5
     值      2 2 4 7 7 8

(c)  B: 索引  1 2 3 4 5 6 7 8      C: 索引  0 1 2 3 4 5
     值      · · · · · · · 3      值      2 2 4 6 7 8

(d)  B: 索引  1 2 3 4 5 6 7 8      C: 索引  0 1 2 3 4 5
     值      · · 0 · · · · 3      值      1 2 4 6 7 8

(e)  B: 索引  1 2 3 4 5 6 7 8      C: 索引  0 1 2 3 4 5
     值      · · 0 · · 3 3 3      值      1 2 4 5 7 8

(f)  B: 索引  1 2 3 4 5 6 7 8
     值      0 0 2 2 3 3 3 5
```

**Figure 8.2（图 8.2）** COUNTING-SORT 在输入数组 $A[1..8]$ 上的 operation（运行过程），其中 $A$ 的每个元素都是不大于 $k = 5$ 的 nonnegative integer（非负整数）。(a) 执行到第 5 行后的数组 $A$ 与辅助数组 $C$。(b) 执行到第 8 行后的数组 $C$。(c)–(e) 分别是第 10–12 行的循环执行一、二、三次之后的 output array（输出数组）$B$ 与辅助数组 $C$。数组 $B$ 中只有浅色阴影的元素已被填入。(f) 最终排好序的输出数组 $B$。

```text
COUNTING-SORT(A, B, k)
 1  let C[0..k] be a new array
 2  for i = 0 to k
 3      C[i] = 0
 4  for j = 1 to A.length
 5      C[A[j]] = C[A[j]] + 1
 6  // C[i] now contains the number of elements equal to i.
 7  for i = 1 to k
 8      C[i] = C[i] + C[i − 1]
 9  // C[i] now contains the number of elements less than or equal to i.
10  for j = A.length downto 1
11      B[C[A[j]]] = A[j]
12      C[A[j]] = C[A[j]] − 1
```

图 8.2 展示了 counting sort 的运行过程。第 2–3 行的 for 循环把数组 $C$ 初始化为全零之后，第 4–5 行的 for 循环检查每个 input element（输入元素）：如果某个输入元素的值为 $i$，我们就把 $C[i]$ 加 1。因此，在第 5 行之后，对每个整数 $i = 0, 1, \ldots, k$，$C[i]$ 中保存的正是值等于 $i$ 的输入元素的个数。第 7–8 行通过对数组 $C$ 求前缀和（running sum），对每个 $i = 0, 1, \ldots, k$ 确定有多少输入元素小于或等于 $i$。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 图 8.2 值得逐格跟踪一遍：以 $j = 8$ 的第一次迭代为例，$A[8] = 3$，此刻 $C[3] = 7$ 表示"值 $\le 3$ 的元素共 7 个"，于是 $A[8]$ 被放入 $B[7]$，随后 $C[3]$ 减为 6——下次再遇到值为 3 的元素就会被放到位置 6，恰好紧跟其后。这个"边放边减一"的技巧让相等的元素各得其所、互不踩踏。另外请特别留意第 10 行循环的方向是 **downto**（从后往前扫描 $A$）：方向反了算法仍能正确排序（见 Exercise 8.2-3），但稳定性（stability）会被破坏。

---

> <span style="color:#7f8c8d;">CLRS §8.2, p.196</span>

（接上页）最后，第 10–12 行的 for 循环把每个元素 $A[j]$ 放到输出数组 $B$ 中它应在的已排序位置上。如果所有 $n$ 个元素互不相同（distinct），那么当我们第一次进入第 10 行时，对每个 $A[j]$ 而言，$C[A[j]]$ 的值正是 $A[j]$ 在输出数组中的最终正确位置，因为有 $C[A[j]]$ 个元素小于或等于 $A[j]$。由于元素可能并不互异，我们在每把一个值 $A[j]$ 放入 $B$ 数组时，就把 $C[A[j]]$ 减 1。将 $C[A[j]]$ 减 1，会使得下一个值等于 $A[j]$ 的输入元素（如果存在的话）被放到输出数组中紧挨在 $A[j]$ 之前的位置上。

Counting sort 需要多少时间？第 2–3 行的 for 循环耗时 $\Theta(k)$，第 4–5 行的 for 循环耗时 $\Theta(n)$，第 7–8 行的 for 循环耗时 $\Theta(k)$，第 10–12 行的 for 循环耗时 $\Theta(n)$。因此，总时间为 $\Theta(k + n)$。在实践中，当 $k = O(n)$ 时我们通常采用 counting sort，此时它的 running time（运行时间）为 $\Theta(n)$。

Counting sort 之所以能够胜过 Section 8.1 中证明的 $\Omega(n \lg n)$ lower bound（下界），是因为它并不是一个 comparison sort（比较排序）。事实上，代码中任何地方都没有出现输入元素之间的比较。相反，counting sort 利用元素的实际值来索引（index into）一个数组。当我们脱离 comparison sort 模型时，$\Omega(n \lg n)$ 的排序下界便不再适用。

Counting sort 的一个重要性质是它是稳定的（stable）：具有相同值的数在输出数组中的先后次序，与它们在输入数组中的先后次序相同。也就是说，对于值相同的两个数，它按"输入数组中先出现的数在输出数组中也先出现"的规则来打破平局（breaks ties）。通常，只有当被排序的元素还携带着 satellite data（卫星数据）时，稳定性这一性质才显得重要。Counting sort 的稳定性之所以重要，还有另一个原因：counting sort 常被用作 radix sort（基数排序）的 subroutine（子过程）。正如下一节我们将看到的，为使 radix sort 正确工作，counting sort 必须是稳定的。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**8.2-1**

Using Figure 8.2 as a model, illustrate the operation of COUNTING-SORT on the array $A = \langle 6, 0, 2, 0, 1, 3, 4, 6, 1, 3, 2 \rangle$.

**8.2-2**

Prove that COUNTING-SORT is stable.

**8.2-3**

Suppose that we were to rewrite the for loop header in line 10 of the COUNTING-SORT as

```text
10  for j = 1 to A.length
```

Show that the algorithm still works properly. Is the modified algorithm stable?……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本页有三处是考点："总时间 $\Theta(k+n)$"是四个循环耗时之和，$k = O(n)$ 时才是线性；"为何能逃过 $\Omega(n \lg n)$ 下界"——因为下界只在 comparison sort 模型内成立，counting sort 压根不比较元素，而是用元素值当数组下标；"稳定性"——注意它是**从后往前**扫描输入才获得的（Exercise 8.2-3 会让你发现顺序扫描会破坏它），而这一性质将在 §8.3 中成为 radix sort 正确性的基石。

---

> <span style="color:#7f8c8d;">CLRS §8.2–8.3, p.197</span>

**8.2-4**

Describe an algorithm that, given $n$ integers in the range $0$ to $k$, preprocesses its input and then answers any query about how many of the $n$ integers fall into a range $[a..b]$ in $O(1)$ time. Your algorithm should use $\Theta(n + k)$ preprocessing time.

### Section 8.3 · Radix sort（基数排序） <span style="color:#2471a3;">**[section]**</span>

Radix sort（基数排序）是一种如今只能在计算机博物馆里见到的 card-sorting machine（卡片排序机）所使用的算法。这种卡片有 80 列（columns），机器可以在每列的 12 个位置之一打一个孔。sorter（分拣机）可以被机械地"编程"（"programmed"），以检查一副卡片（deck）中每张卡片的给定列，并根据打孔的位置把卡片分到 12 个箱（bins）之一。操作员随后可以逐箱收集卡片，使得第 1 个位置打孔的卡片叠放在第 2 个位置打孔的卡片之上，依此类推。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 原书这段"博物馆展品"式的描述背后有真实的历史人物：卡片排序机制出自 Herman Hollerith（1860–1929）之手（据离线维基百科），他受列车检票员在车票不同位置打孔以记录乘客特征的启发，于 1884 年获得打孔卡制表机专利，并为 1890 年美国人口普查制造了成套设备——1880 年的人口数据靠人工处理花了 8 年，Hollerith 的机器把 1890 年的统计大幅提速，完成了数据处理史上第一次"机械化批处理"。他创办的公司于 1911 年并入 Computing-Tabulating-Recording Company，1924 年更名为 IBM。理解这段历史还能帮你记住 radix sort 的硬件根源：分拣机一次只看一列（一个数字位），所以"逐位排序、每趟必须稳定"是机械结构的必然，而非算法设计的随意选择。原书称它为"如今只能在博物馆见到的机器"，这恰恰提醒我们：算法所依附的硬件形态会过时，但它利用"键的内部结构绕开比较"的思想不会。

对于 decimal digits（十进制数字），每列只使用其中的 10 个位置（其余两个位置留给编码非数字字符）。于是一个 $d$-digit number（$d$ 位数字）将占据一个由 $d$ 列组成的 field（字段）。由于卡片分拣机一次只能看一列，按一个 $d$ 位数字对 $n$ 张卡片排序的问题就需要一个 sorting algorithm（排序算法）来解决。

直观上，你可能会按 most significant digit（最高有效位）对数字排序，对得到的各个箱递归地排序，然后按顺序合并各副卡片。遗憾的是，由于在排序每个箱时必须把 10 个箱中 9 个箱的卡片先放到一边，这一过程会产生许多你必须记录在案的中间卡片堆。（见 Exercise 8.3-5。）

Radix sort 解决卡片排序问题的方法——与直觉相反（counterintuitively）——是先按 least significant digit（最低有效位）排序。算法随后把各箱卡片合并成单副卡片：0 号箱中的卡片排在 1 号箱的卡片之前，1 号箱的排在 2 号箱的之前，依此类推。然后它再按次最低有效位对整副卡片重新排序，并以同样的方式重新合并。这一过程一直持续到卡片按全部 $d$ 位数字排完序为止。令人惊叹的是，此时这些卡片已经按这个 $d$ 位数字完全排好序了。因此，只需对卡片做 $d$ 趟（passes）处理即可完成排序。图 8.3 展示了 radix sort 作用于"一副" 7 个 3 位数的过程。

为使 radix sort 正确工作，各位数字上的排序必须是稳定的（stable）。卡片分拣机所执行的排序是稳定的，但操作员必须小心，不要改变卡片从箱中取出时的顺序——即使箱中的所有卡片在所选列上的数字都相同。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本页的"历史包袱"正是理解 radix sort 的钥匙：先按高位排序再递归（MSD，most-significant-digit）看似自然，却要维护大量中间卡片堆；反其道而行的 LSD（least-significant-digit）——从最低位开始、逐位稳定排序——只需 $d$ 趟扫描就能完成，而且**每位上的排序必须稳定**这一要求，正是上一页 counting sort 稳定性大显身手的地方。想一想：按个位排好后，两个数若十位相同，则它们按个位的相对次序必须保留——这就是稳定的意义所在。

---

> <span style="color:#7f8c8d;">CLRS §8.3 + Figure 8.3, p.198</span>

> <span style="color:#7f8c8d;">[note] 本页上部为图 8.3 的示意图：radix sort 作用于 7 个 3 位数的列表。最左一列为输入 ⟨329, 457, 657, 839, 436, 720, 355⟩；其后各列依次为按个位（第 1 位数字）、十位（第 2 位数字）、百位（第 3 位数字）做稳定排序后的列表：按个位排序得 ⟨720, 355, 436, 457, 657, 329, 839⟩，再按十位排序得 ⟨720, 329, 436, 839, 355, 457, 657⟩，最后按百位排序得 ⟨329, 355, 436, 457, 657, 720, 839⟩，即为完全排好序的结果。阴影标出的是为从上一列得到当前列表而据以排序的数字位。为对照原书排版，下图以文本示意重绘（加粗者为该趟据以排序的数字位）。</span>

```text
输入       按个位排序   按十位排序   按百位排序
3**2**9    7**2**0     7**2**0     **3**29
4**5**7    3**5**5     3**2**9     **3**55
6**5**7    4**3**6     4**3**6     **4**36
8**3**9    4**5**7     8**3**9     **4**57
4**3**6    6**5**7     3**5**5     **6**57
7**2**0    3**2**9     4**5**7     **7**20
3**5**5    8**3**9     6**5**7     **8**39
```

**Figure 8.3（图 8.3）** Radix sort 作用于 7 个 3 位数的列表的运行过程。最左一列是 input（输入）。其余各列展示的是依次按重要性递增的数字位（increasingly significant digit positions）排序后的列表。阴影标出的是为从上一列得到当前列表而据以排序的数字位。

在一个典型的 sequential random-access machine（顺序随机访问计算机）中，我们有时用 radix sort 来对以多个字段（multiple fields）为 key（关键字）的 information records（信息记录）排序。例如，我们可能希望按三个关键字（year（年）、month（月）、day（日））对 dates（日期）排序。我们可以用一个比较函数来运行排序算法：给定两个日期，先比较年份；若持平（tie），再比较月份；若再次持平，则比较日期。另一种做法是，用一个稳定排序对该信息排三次序：先按日，再按月，最后按年。

Radix sort 的代码很直接。下面的过程假定 $n$ 个元素组成的数组 $A$ 中的每个元素都有 $d$ 位数字，其中第 1 位是最低有效位，第 $d$ 位是最高有效位。

```text
RADIX-SORT(A, d)
 1  for i = 1 to d
 2      use a stable sort to sort array A on digit i
```

#### Lemma 8.3（引理 8.3） <span style="color:#2471a3;">**[lemma]**</span>

给定 $n$ 个 $d$ 位数，其中每个数字位可以取 $k$ 个可能的值，如果 RADIX-SORT 所用的 stable sort（稳定排序）耗时 $\Theta(n + k)$，则 RADIX-SORT 能在 $\Theta(d(n + k))$ 时间内正确排好这些数。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  Radix sort 的 correctness（正确性）通过对当前所排序的数字列做 induction（归纳）来证明（见 Exercise 8.3-3）。运行时间的分析则取决于用哪一个稳定排序作为 intermediate sorting algorithm（中间排序算法）。当每个数字位都在 $0$ 到 $k-1$ 区间内（即它可以取 $k$ 个可能的值），且 $k$ 不太大时，counting sort（计数排序）是显然的选择。这样，对 $n$ 个 $d$ 位数的每一趟处理耗时 $\Theta(n + k)$；共有 $d$ 趟，故 radix sort 的总时间为 $\Theta(d(n + k))$。

当 $d$ 为常数且 $k = O(n)$ 时，我们可以让 radix sort 以 linear time（线性时间）运行。更一般地，在如何把每个关键字分解成若干数字位这一点上，我们有一定的灵活性。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 图 8.3 请重点盯住"457 / 657"这对数：按个位排序后 457 在 657 前（个位 7 持平，保持输入次序——稳定性），按十位排序后仍是 457 在 657 前（十位 5 持平，**再次**保持次序），最终按百位排序才分出高下。多关键字日期排序（先日、再月、最后年）是同一思想的直接应用——最后排的关键字最"重要"，先排的关键字在高位持平时充当"决胜依据"。引理 8.3 的运行时间 $\Theta(d(n+k))$ 则把"趟数 $d$"与"每趟代价 $n+k$"两个因子明确分开，为下页的引理 8.4（把一个 $b$ 位字拆成若干个 $r$ 位"数字"）铺路。

---

> <span style="color:#7f8c8d;">CLRS §8.3, p.199</span>

#### Lemma 8.4（引理 8.4） <span style="color:#2471a3;">**[lemma]**</span>

给定 $n$ 个 $b$ 位数以及任何正整数 $r \le b$，如果 RADIX-SORT 所用的稳定排序对处于 $0$ 到 $k$ 区间内的输入耗时 $\Theta(n + k)$，则 RADIX-SORT 能在 $\Theta((b/r)(n + 2^r))$ 时间内正确排好这些数。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  对于一个值 $r \le b$，我们把每个关键字看作具有 $d = \lceil b/r \rceil$ 位数字，每位数字有 $r$ 个比特。每位数字都是 $0$ 到 $2^r - 1$ 区间内的整数，于是我们可以使用 $k = 2^r - 1$ 的 counting sort。（例如，我们可以把一个 32 比特的字看作有 4 个 8 比特的数字位，于是 $b = 32$，$r = 8$，$k = 2^r - 1 = 255$，$d = b/r = 4$。）counting sort 的每一趟耗时 $\Theta(n + k) = \Theta(n + 2^r)$，共 $d$ 趟，故总运行时间为 $\Theta(d(n + 2^r)) = \Theta((b/r)(n + 2^r))$。

对于给定的 $n$ 和 $b$ 的值，我们希望在 $r \le b$ 的条件下选取使表达式 $(b/r)(n + 2^r)$ 最小的 $r$ 值。如果 $b < \lfloor \lg n \rfloor$，那么对任何 $r \le b$，都有 $(n + 2^r) = \Theta(n)$。因此，选 $r = b$ 给出运行时间 $(b/b)(n + 2^b) = \Theta(n)$，这在渐近意义上是最优的。如果 $b \ge \lfloor \lg n \rfloor$，那么选 $r = \lfloor \lg n \rfloor$ 就给出了在常数因子意义下最好的时间，这可以如下看出。选 $r = \lfloor \lg n \rfloor$ 给出的运行时间为 $\Theta(bn / \lg n)$。当把 $r$ 增大到 $\lfloor \lg n \rfloor$ 以上时，分子中的 $2^r$ 项比分母中的 $r$ 项增长得更快，因此把 $r$ 增大到 $\lfloor \lg n \rfloor$ 以上将给出 $\Omega(bn / \lg n)$ 的运行时间。反之，如果把 $r$ 减小到 $\lfloor \lg n \rfloor$ 以下，那么 $b/r$ 项增大，而 $n + 2^r$ 项仍保持在 $\Theta(n)$。

Radix sort 是否优于以比较为基础的 sorting algorithm（排序算法），例如 quicksort（快速排序）？如果 $b = O(\lg n)$（这常常是实际情况），且我们选 $r \approx \lg n$，那么 radix sort 的运行时间是 $\Theta(n)$，看起来比 quicksort 的期望运行时间 $\Theta(n \lg n)$ 要好。然而，隐藏在 Θ-notation（Θ 记号）中的 constant factors（常数因子）是不同的。虽然 radix sort 对 $n$ 个关键字的处理趟数可能比 quicksort 少，但 radix sort 的每一趟可能显著耗时更长。我们偏爱哪种排序算法，取决于 implementations（实现）的特性、underlying machine（底层机器）的特性（例如，quicksort 通常比 radix sort 更有效地利用 hardware caches（硬件缓存）），以及 input data（输入数据）的特性。此外，以 counting sort 作为中间稳定排序的这个 radix sort 版本并非 in place（原地的），而许多耗时 $\Theta(n \lg n)$ 的 comparison sorts 都是原地的。因此，当主存空间非常宝贵时，我们可能更偏爱像 quicksort 这样的 in-place algorithm（原地算法）。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**8.3-1**

Using Figure 8.3 as a model, illustrate the operation of RADIX-SORT on the following list of English words: COW, DOG, SEA, RUG, ROW, MOB, BOX, TAB, BAR, EAR, TAR, DIG, BIG, TEA, NOW, FOX.……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 引理 8.4 的精髓在"把一个 $b$ 比特关键字看作 $\lceil b/r \rceil$ 个 $r$ 比特的数字"这个自由度：每位数字的取值范围是 $0 \sim 2^r - 1$，所以 counting sort 的 $k = 2^r - 1$，每趟代价 $n + 2^r$；$r$ 越大趟数 $\lceil b/r \rceil$ 越少，但每趟代价 $2^r$ 指数膨胀——求导平衡后最优取 $r = \lfloor \lg n \rfloor$（当 $b \ge \lfloor \lg n \rfloor$ 时），总时间 $\Theta(bn/\lg n)$；当 $b < \lg n$ 时干脆 $r = b$，一次到位得 $\Theta(n)$。页末的工程讨论同样重要：渐近胜出 $\ne$ 实际更快——常数因子、缓存友好性、是否原地，都是实战中绕不开的账。

---

> <span style="color:#7f8c8d;">CLRS §8.3–8.4, p.200</span>

**8.3-2**

Which of the following sorting algorithms are stable: insertion sort, merge sort, heapsort, and quicksort? Give a simple scheme that makes any sorting algorithm stable. How much additional time and space does your scheme entail?

**8.3-3**

Use induction to prove that radix sort works. Where does your proof need the assumption that the intermediate sort is stable?

**8.3-4**

Show how to sort $n$ integers in the range $0$ to $n^3 - 1$ in $O(n)$ time.

**8.3-5** $(\star)$

In the first card-sorting algorithm in this section, exactly how many sorting passes are needed to sort $d$-digit decimal numbers in the worst case? How many piles of cards would an operator need to keep track of in the worst case?

### Section 8.4 · Bucket sort（桶排序） <span style="color:#2471a3;">**[section]**</span>

Bucket sort（桶排序）假定输入是由一个 uniform distribution（均匀分布）中抽取（drawn）出来的，并且具有 $O(n)$ 的 average-case running time（平均情况运行时间）。与 counting sort 一样，bucket sort 之所以快，是因为它对输入做出了某种假定：counting sort 假定输入由一个小范围内的整数组成，而 bucket sort 则假定输入是由一个随机过程生成的，该过程将元素均匀、独立地分布（uniformly and independently distributed）在区间 $[0, 1)$ 上。（uniform distribution 的定义见 Section C.2。）

Bucket sort 把区间 $[0, 1)$ 划分成 $n$ 个相同大小的子区间（equal-sized subintervals），或称 buckets（桶），然后把 $n$ 个输入数分散到各个桶中。由于输入是均匀、独立地分布在 $[0, 1)$ 上的，我们并不指望有很多数落入同一个桶。为了产生输出，我们只需把每个桶中的数排序，然后按顺序遍历各个桶，依次列出每个桶中的元素即可。

我们的 bucket sort 代码假定输入是一个含 $n$ 个元素的数组 $A$，且数组中的每个元素 $A[i]$ 都满足 $0 \le A[i] < 1$。代码需要一个由 linked lists（链表）（即各桶）组成的辅助数组 $B[0..n-1]$，并假定存在某种维护这类链表的机制。（Section 10.2 描述了如何实现链表上的基本操作。）……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 注意原书中 8.3-5 题号前有星标（$\star$），表示这是一道较难的题：MSD 递归排序 $d$ 位十进制数，最坏情况下（输入已按位全相同地堆在一起）需要 $10^0 + 10^1 + \cdots + 10^{d-1} = (10^d - 1)/9$ 趟排序，操作员要跟踪的卡片堆数目也达同一量级——这正是"中间卡片堆"噩梦的精确刻画。而接下来登场的 bucket sort 走的是另一条线性时间路线：不按"数字位"切分，而按"值域区间"切分，其 $O(n)$ 平均性能的赌注押在输入的均匀分布上，下一页将用期望分析精确兑现这个赌注。

---

> <span style="color:#7f8c8d;">CLRS §8.4 + Figure 8.4, p.201</span>

> <span style="color:#7f8c8d;">[note] 本页上部为图 8.4 的示意图：BUCKET-SORT 在 $n = 10$ 时的运行过程。(a) 为输入数组 $A[1..10] = \langle .78, .17, .39, .26, .72, .94, .21, .12, .23, .68 \rangle$；(b) 为算法第 8 行执行后由已排序链表（桶）组成的数组 $B[0..9]$：值 $.12$ 落入桶 $B[0]$，$.17$ 落入 $B[1]$，$.21, .23, .26$ 落入 $B[2]$，$.39$ 落入 $B[3]$，$.68$ 落入 $B[6]$，$.72, .78$ 落入 $B[7]$，$.94$ 落入 $B[9]$（桶 $B[4]$、$B[5]$、$B[8]$ 为空）。桶 $i$ 存放半开区间 $[i/10, (i+1)/10)$ 中的值。排好序的输出就是按次序连接（concatenation）$B[0], B[1], \ldots, B[9]$ 各链表的结果。为对照原书排版，下图以文本示意重绘。</span>

```text
(a)  A: 索引  1    2    3    4    5    6    7    8    9    10
     值      .78  .17  .39  .26  .72  .94  .21  .12  .23  .68

(b)  B:  0    1    2              3    4    5    6    7           8    9
         .12  .17  .21 → .23 → .26 .39  ∅    ∅    .68  .72 → .78   ∅    .94
```

**Figure 8.4（图 8.4）** $n = 10$ 时 BUCKET-SORT 的 operation（运行过程）。(a) 输入数组 $A[1..10]$。(b) 算法第 8 行执行后由已排序链表（buckets（桶））组成的数组 $B[0..9]$。桶 $i$ 存放半开区间（half-open interval）$[i/10, (i+1)/10)$ 中的值。排好序的输出由按次序连接列表 $B[0], B[1], \ldots, B[9]$ 构成。

```text
BUCKET-SORT(A)
 1  n = A.length
 2  let B[0..n − 1] be a new array
 3  for i = 0 to n − 1
 4      make B[i] an empty list
 5  for i = 1 to n
 6      insert A[i] into list B[⌊nA[i]⌋]
 7  for i = 0 to n − 1
 8      sort list B[i] with insertion sort
 9  concatenate the lists B[0], B[1], …, B[n − 1] together in order
```

图 8.4 展示了 bucket sort 作用于一个含 10 个数的输入数组的运行过程。为了说明该算法是正确的，考虑两个元素 $A[i]$ 与 $A[j]$。不失一般性（without loss of generality），设 $A[i] \le A[j]$。由于 $\lfloor nA[i] \rfloor \le \lfloor nA[j] \rfloor$，要么元素 $A[i]$ 与 $A[j]$ 进入同一个桶，要么 $A[i]$ 进入一个下标更小的桶。如果 $A[i]$ 与 $A[j]$ 进入同一个桶，那么第 7–8 行的 for 循环会把它们排成正确的次序。如果 $A[i]$ 与 $A[j]$ 进入不同的桶，那么第 9 行会把它们排成正确的次序。因此，bucket sort 是正确的。

要分析运行时间，请注意除第 8 行之外的所有行在最坏情况下都耗时 $O(n)$。我们还需要分析第 8 行中 $n$ 次调用 insertion sort（插入排序）所耗费的总时间。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第 6 行的下标计算 $\lfloor nA[i] \rfloor$ 是全算法的灵魂：把值域 $[0,1)$ 均匀切成 $n$ 份后，一个落在半开区间 $[k/n, (k+1)/n)$ 中的值恰好映射到桶号 $\lfloor nA[i] \rfloor = k$——"值本身告诉你它该去哪个桶"，完全不需要比较。正确性论证也极简：$\lfloor nA[i] \rfloor \le \lfloor nA[j] \rfloor$ 保证 $A[i]$ 不会落到比 $A[j]$ 更靠后的桶，桶内交给 insertion sort 收拾，桶间靠第 9 行的按序拼接。但"桶内用插入排序"为何平均不慢？因为均匀分布下每桶只有约 $O(1)$ 个元素——这正是下一页期望分析要量化的直觉。

---

> <span style="color:#7f8c8d;">CLRS §8.4, p.202</span>

（接上页）为了分析这些 insertion sort 调用的代价，令 $n_i$ 为 random variable（随机变量），表示放入桶 $B[i]$ 中的元素个数。由于 insertion sort 以二次时间（quadratic time）运行（见 Section 2.2），bucket sort 的 running time（运行时间）为

```math
T(n) = \Theta(n) + \sum_{i=0}^{n-1} O(n_i^2).
```

我们现在来分析 bucket sort 的 average-case running time（平均情况运行时间），方法是计算运行时间的 expected value（期望值），其中我们对 input distribution（输入分布）取期望。对上式两边取期望，并利用 linearity of expectation（期望的线性性），得到

```math
\begin{aligned}
\mathrm{E}[T(n)]
  &= \mathrm{E}\left[ \Theta(n) + \sum_{i=0}^{n-1} O(n_i^2) \right] \\
  &= \Theta(n) + \sum_{i=0}^{n-1} \mathrm{E}\big[\, O(n_i^2) \,\big] \qquad\quad \text{(by linearity of expectation)} \\
  &= \Theta(n) + \sum_{i=0}^{n-1} O\big(\, \mathrm{E}[n_i^2] \,\big). \qquad \text{(by equation (C.22))} \tag{8.1}
\end{aligned}
```

我们断言

```math
\mathrm{E}[n_i^2] = 2 - 1/n \tag{8.2}
```

对 $i = 0, 1, \ldots, n-1$ 成立。每个桶 $i$ 的 $\mathrm{E}[n_i^2]$ 都取相同的值并不令人意外，因为输入数组 $A$ 中的每个值落入任何桶的可能性都是相同的（equally likely）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (8.2) 的推导马上展开，先把它的"球与箱"骨架搭好：$n$ 个元素独立均匀地落进 $n$ 个桶，正是 5.4.2 节 balls and bins（球与箱）的场景——与生日问题（5.4.1 节）同族，那里问"是否存在一对碰撞"，这里问"碰撞对的总期望"。指示器 $X_{ij}$ 把"元素 $j$ 落入桶 $i$"变成 0-1 变量，$n_i^2 = \sum_j \sum_k X_{ij}X_{ik}$ 恰好把平方拆成两类：$j = k$ 的对角项（自己配自己，贡献恒为 1）与 $j \ne k$ 的非对角项（两元素同桶，概率 $1/n^2$）。于是 $\mathrm{E}[n_i^2] = 1 + n(n-1)/n^2 = 2 - 1/n$：期望的平方里几乎全是"自己配自己"，真正的碰撞对期望不足 1——插入排序在桶内平均只面对常数个工作量，桶排序 $O(n)$ 的全部秘密就在这一行。注意整个论证只靠期望的线性性，从不需要各 $X_{ij}$ 相互独立——线性性让你不必关心"对与对之间"的相关性，这是生日问题分析的同款技巧。

为了证明 equation (8.2)，我们定义 indicator random variables（指示器随机变量，见 Section 5.2）

```math
X_{ij} = I\, \{\, A[j] \text{ falls in bucket } i \,\}
```

其中 $i = 0, 1, \ldots, n-1$ 且 $j = 1, 2, \ldots, n$。于是，

```math
n_i = \sum_{j=1}^{n} X_{ij}.
```

为了计算 $\mathrm{E}[n_i^2]$，我们展开平方并重新组合各项：……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页是"期望分析三步曲"的舞台：先把总时间分解为 $\Theta(n)$ 的固定开销加上各桶内部排序代价之和；再利用期望的线性性把期望"拆"进求和号内（注意 $\mathrm{E}[\Theta(n)] = \Theta(n)$、$O$ 与 $\mathrm{E}$ 的交换引用了 equation (C.22)——期望意义下的渐近记号运算法则）；最后把每个桶的平方项 $n_i^2$ 用指示器随机变量 $X_{ij}$ 表示出来。本页结尾的"展开平方"（$n_i^2 = \sum_{j}\sum_{k} X_{ij}X_{ik}$）将在下一页分为 $j = k$ 与 $j \ne k$ 两部分处理，其中 $\mathrm{E}[n_i^2] = 2 - 1/n$ 与 $\sum_{i=0}^{n-1} \mathrm{E}[n_i^2] = 2n - 1 = \Theta(n)$ 一同收出 bucket sort 的期望运行时间 $O(n)$。
