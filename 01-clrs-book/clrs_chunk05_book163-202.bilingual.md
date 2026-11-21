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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> `HEAP-EXTRACT-MAX` 与 `HEAPSORT` 的循环体是同一段机械动作的两种封装：取走根上的最大元，把最后一个叶子搬到根的位置，把 `A.heap-size` 减一，再让 `MAX-HEAPIFY` 把新根沉到它该在的深度。`HEAPSORT` 只是把这个动作重复 $n-1$ 次，每抽走一个最大元，数组末尾就多出一个已经定序的位置。
>
> 为什么必须搬最后一个叶子，而不是随便挑一个内部结点上来？因为 array（数组）表示法的整套下标公式只对 complete binary tree（完全二叉树）成立：父结点是 $\lfloor i/2 \rfloor$，左右孩子是 $2i$ 与 $2i+1$，这三条公式的成立前提是"前 $n$ 个位置恰好填满一棵完全二叉树"。删掉根之后，唯一一个"删掉它、剩余前缀仍然是完全二叉树"的结点就是最后一个叶子；换任何别的结点上来，数组中间会留下空洞，父子下标关系立刻失效，整个隐式结构随之崩塌。
>
> 为什么搬完之后必须调用 `MAX-HEAPIFY`？因为被搬上来的叶子携带的是任意值，它只可能破坏"根与它的两个孩子"这一处关系；根的两棵子树在抽取之前各自合法，抽取动作没有碰过它们。所以违规范围被压缩到一条从根出发的 simple path（简单路径）上：每层先比较两个孩子选出大者，再拿当前结点与它比较并决定是否 exchange（交换），代价与树高同阶。
>
> 拿具体数字过一遍：$n = 1024$ 的堆高为 $10$，抽空整个堆需要 $1023$ 次抽取，每次至多 $10$ 层、每层至多 $2$ 次比较，总比较次数不超过 $20460$；而自底向上建堆只花不超过 $2n = 2048$ 次比较。两笔账合起来正是 $n \lg n$ 的排序总账，其中建堆那部分小到可以忽略——这也是堆排序的成本几乎全部记在抽取阶段的原因。
>
> `HEAPSORT` 把抽出的最大值写到刚空出来的尾位，于是有序后缀从右向左生长，与左侧尚未处理的堆前缀共用同一个数组。这就是 `A.length`（物理容量）与 `A.heap-size`（逻辑尺寸）分离的用处：前者说这个数组有多少格，后者说前多少格还归堆管；缩小堆只是把逻辑边界左移一格，数组元素一个都没删，被抽走的最大值仍然躺在尾部。这套技巧在第 10 章用数组实现 stack（栈）与 queue（队列）时会再出现一次，那里的 `top` 指针与 `head`、`tail` 下标同样是"物理容量 + 逻辑尺寸"的两层记法。
>
> 跨课程连接：CSAPP 第 6 章 cache（缓存）层次给出的成本模型解释了堆排序的强弱两面。堆是隐式结构，数据就躺在原数组里，一条 $64$ 字节的 cache line（缓存行）能装 $16$ 个 $32$ 位整数，抽取阶段既不额外分配、也不搬大块内存，内存流量近乎最小；但下沉时每层要跳到 $2i$ 或 $2i+1$，跨 cache line 的概率高，命中率反而不如顺序扫描的算法。区别在于两个模型计量对象不同：cache 模型数的是字节搬运与缺失次数，渐近记号数的是比较次数，两者就在常数因子上分道扬镳。
>
> 一句话收束：抽取是"把根摘走、用末尾补位、再下沉修复"的三段式，`HEAPSORT` 是它的 $n-1$ 次迭代，而"逻辑尺寸与物理尺寸分离"才是让有序后缀与无序前缀同居一个数组、零额外空间的那把钥匙。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> `MAX-HEAP-INSERT` 的两步不是画蛇添足：第 1 行把堆尺寸加一，第 2 行把新叶子置为 $-\infty$，第 3 行才调用 `HEAP-INCREASE-KEY` 把真正的 key（关键字）写进去。先把新位置填成"最小可能值"再抬高，是为了让整个插入过程只走一条单调的上行路径。
>
> 第一性原理：$-\infty$ 是取大运算的 identity element（单位元），即 $\max(-\infty, x) = x$ 对一切 $x$ 成立，正如 $0$ 是加法的单位元、$+\infty$ 是取小的单位元。把一个 $-\infty$ 叶子挂到树上之后，新增的唯一一对父子关系是"新叶子与其父"，而父结点的值恒 $\ge -\infty$，所以这棵变大的树立刻满足 max-heap property（最大堆性质），扩展这一步不需要任何修复。
>
> 第二步的关键在于 `HEAP-INCREASE-KEY` 只肯"增大"：它的第 1 行 `if key < A[i]` 就报错。这个限制并非偷懒，而是因为"增大"与"减小"破坏的是两种不同的关系。增大一个结点，只可能让"父不小于子"这一条在它到根的路径上失效，于是修复只需沿路径上行，即 sift-up（上浮），代价与树高同阶；减小一个结点，破坏的是它与两个孩子的关系，修复必须下行，即 sift-down（下沉），也就是 `MAX-HEAPIFY` 干的事。用 $-\infty$ 起手，就把"插入任意 key"化归成"纯增大"，从而只复用唯一一个已有的修复过程。Exercise 6.5-4 追问的正是这个前提条件为什么总能被满足。
>
> 代价与数字：$n = 1024$ 时树高 $10$，单次插入至多 $10$ 次比较；每次 exchange（交换）要三次赋值，所以最坏 $30$ 次赋值；若按 Exercise 6.5-6 的挖坑改法，路径上只保留一次最终写入，赋值数降到至多 $11$ 次。逐个插入建堆的总比较数复算为 $\sum_{k=2}^{1024} \lfloor \lg k \rfloor = 8204$，与 $n \lg n = 10240$ 同量级；自底向上的 `BUILD-MAX-HEAP` 只要不超过 $2n = 2048$。差距出在这里：浅层结点数量少但每次要付满深度，深层结点数量多却每次都便宜。
>
> 跨课程连接：CSAPP 第 3 章机器级表示的存储模型可以直接给"三次赋值与一次赋值"定价——交换是 $3$ 次 load（读取）加 $3$ 次 store（写入），挖坑法是把父结点写进子结点位置后继续上行，最后一次性落座，减少的是写流量而不是比较次数。这与 insertion-sort（插入排序）内层循环的"先挪位、最后落座"是同一手法，CLRS 在 2.1 节和 6.5-6 题里刻意让两处照面，区别仅在于插入排序挪的是有序前缀的尾部，堆上浮挪的是一条祖先链。
>
> 工程上还有一个细节：$-\infty$ 不是可表示的数值。整数键用类型的最小值当哨兵，浮点键用负无穷常量；若键是无下界的任意精度整数，就得额外加一个"尚未赋值"的标志位，否则"先置最小值"这一步无法落地。哨兵是否合法，取决于键的类型有没有下界——这是把数学记号翻译成代码时最容易漏掉的一处。
>
> 严格说，新叶子没有孩子，直接写入任意 key 也只需要上浮；$-\infty$ 的真正作用在于让"插入"能原样复用 `HEAP-INCREASE-KEY`，而不必放宽它的前置条件、也不必另写一个"允许任意初值"的过程。一个假值换掉一整条分支路径，这就是哨兵的全部价值。
>
> 收束：插入 = 扩一个哨兵叶子 + 一次单纯的上浮，代价 $O(\lg n)$ 全部花在那条长度为树高的路径上；真正省下的是代码路径数量，你不需要再写一个双向修补的插入版本。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这三道题合起来是一份宣言：priority queue（优先队列）是比 stack（栈）与 queue（队列）更原始的积木，线性结构只是它在 key（关键字）取值退化时的特例。6.5-7 要你亲手把这个退化做出来，6.5-8 要你补一个删除操作，6.5-9 则是后面十几章反复出现的引擎。
>
> 6.5-7 的做法是给每个元素配一个单调的 time stamp（时间戳）当 key。实现 stack（栈）时让时间戳随插入严格递增，则最后压入者 key 最大，`EXTRACT-MAX` 取出的正是栈顶，后进先出自然成立；实现 queue（队列）时让时间戳递减，则最早入队者 key 最大，取出即队头，先进先出成立。代价也一目了然：本来是 $O(1)$ 的两个操作，现在都变成 $O(\lg n)$。你换到的不是速度，而是"一套代码同时扮演两种结构"的通用性——这正是优先队列值得单独成为 ADT（抽象数据类型）的理由。
>
> 6.5-8 的 `HEAP-DELETE(A, i)` 不需要新机制：先把 $A[i]$ 增大到 $+\infty$，它会沿祖先链一路浮到堆顶，再照搬 `HEAP-EXTRACT-MAX` 的"末位补顶 + 下沉"，两次 $O(\lg n)$ 串联即为 $O(\lg n)$。更省的做法只有一次对数：把末位元素搬到 $A[i]$ 上，若它比父结点大就上浮、比某个孩子小就下沉，二者只会发生一个，代价仍是 $O(\lg n)$ 但少一半常数。两版都合法，差别在于前者靠一个假的极大值把"删除"归约成"增大 + 抽取"，后者直接对"位置 $i$ 处唯一的违规"做定向修复。
>
> 6.5-9 是 $k$ 路归并：把 $k$ 个已排序序列的当前队头放进一个大小为 $k$ 的 min-heap（最小堆），每次 `EXTRACT-MIN` 输出全局最小并从该序列补入下一个元素。$n$ 次堆操作各花 $O(\lg k)$，总计 $O(n \lg k)$。代数字：$n = 10^{6}$、$k = 100$ 时 $\lg k \approx 6.64$，总比较数约 $6.6 \times 10^{6}$；而每输出一个元素就线性扫一遍 $k$ 个队头的笨办法要 $n k = 10^{8}$ 次，差出约 $15$ 倍。$k$ 越大优势越明显，但堆本身也要占内存，实际系统里 $k$ 常取到几百。
>
> 跨课程连接：这条"用堆维护候选集、每次取最优"的骨架，你后面至少还要撞见三次。第 24 章 Dijkstra 最短路用 min-heap（最小堆）维护 frontier（前沿候选集），每次取出当前距离最小的未定标结点；第 23 章 Prim 最小生成树同理；第 16 章 Huffman 编码每次合并权值最小的两棵树。它们的共同前提都是"候选集只增不减、每次只要最优的一个"，而这正是优先队列的接口。外部排序里的 multiway merge（多路归并）也是同一件事，只是把内存层次换了舞台：CSAPP 第 6 章告诉你一次归并的路数越多，需要写的 pass（趟）数越少，磁盘 I/O 的总量就按对数下降。
>
> 把通用性的价格算清：$n = 10^{6}$ 次压栈若改用优先队列实现，每次 $\lg n \approx 20$ 层、每层一次比较加可能的交换，总计约 $2 \times 10^{7}$ 次比较；真正的栈只需一次下标自增加一次 store（写入）。"一套结构通吃"换来的，是把 $10^{6}$ 次常数操作放大成 $2 \times 10^{7}$ 次比较。工程上还有一处边界：用递减时间戳实现队列依赖计数器单调，$64$ 位无符号整数按每秒 $10^{9}$ 次递增要约 $584$ 年才回绕，溢出不是现实威胁，但严谨实现仍要显式处理回绕。
>
> 收束：这三道练习的真实分量不在技巧，而在于它们把"结构"还原成"操作"——只要你有一个能反复取最优的容器，栈、队列、删除、归并都只是它的调用序列。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题逼你正视一句话：同样的输出，可以有不同的代价。`BUILD-MAX-HEAP` 与 `BUILD-MAX-HEAP'` 都把同一个数组变成合法的 max-heap（最大堆），a 问却要你说清它们是否造出同一个堆；b 问则把这笔代价差算成一个完整的对数因子。
>
> b 问的账本很清楚：`BUILD-MAX-HEAP'` 逐个调用 `MAX-HEAP-INSERT`，最坏输入是已按增序排好的数组——每个新元素都是当前最大值，于是每次插入都要从叶子一路浮到根。第 $k$ 个元素上浮的层数正好是它插入后所在的深度 $\lfloor \lg k \rfloor$，总代价精确等于 $\sum_{k=2}^{n} \lfloor \lg k \rfloor = (n+1)\lfloor \lg n \rfloor - 2^{\lfloor \lg n \rfloor + 1} + 2$，代 $n = 1024$ 得 $8204$，与 $n \lg n = 10240$ 同量级。
>
> 对照 6.3 节的自底向上建堆：它从 $\lfloor n/2 \rfloor$ 号结点往前逐个下沉，总代价是 $\sum_{h} \lceil n/2^{h+1} \rceil \cdot O(h)$，按几何级数收敛到不超过 $2n = 2048$。两个求和差在哪里？差在"按什么给结点分组"。下沉法的代价与该结点的高度成正比，而大多数结点位于底层、高度很小，所以按高度分组后高 $h$ 组只有 $n/2^{h+1}$ 个结点，权重衰减得比数量增长更快；上浮法的代价与深度成正比，底层结点数量最多，于是数量与权重同时变大，求和退化成 $n \lg n$。
>
> a 问的答案是否定的，反例给最小规模即可：输入 $A = \langle 1, 2, 3 \rangle$。插入法先得 $[1]$，插入 $2$ 后上浮成 $[2, 1]$，插入 $3$ 后上浮成 $[3, 1, 2]$；自底向上法则从 $1$ 号结点开始，孩子的较大者是 $3$，交换得 $[3, 2, 1]$。两个结果都是合法最大堆，却不是同一个堆——上浮走的是"新元素向根爬"，下沉走的是"老元素向叶落"，路径不同，形状自然不必相同。
>
> 跨课程连接：6.042J 的反例法在这里就是全部工具——要推翻"总是相同"这种全称命题，一个三点输入足够，不必去构造一般性的论证。更值得带走的是那句话：running time（运行时间）由算法对输入执行的操作序列决定，而不由它吐出的输出决定。这与排序里"归并排序与插入排序输出同一个有序数组、代价却差一个量级"是同一个道理。
>
> 别以为渐近差距在小 $n$ 上也成立，方向恰好相反：$n = 8$ 时插入法总比较数精确为 $13$，而自底向上法在全部 $8! = 40320$ 个排列上暴力枚举，比较数落在 $7$ 与 $11$ 之间，最坏也只要 $11$。这个例子里插入法已经更贵，只贵两次比较；$n \lg n$ 与 $2n$ 的差距要到大 $n$ 才显出一个对数因子。渐近记号描述趋势，不描述小规模常数。
>
> 还有一层容易被忽略的取舍：`BUILD-MAX-HEAP'` 是增量构造，允许数据一边到达一边查询——第 $k$ 步之后，前 $k$ 个元素已经构成一个合法堆，最坏 $\Theta(n \lg n)$ 就是"随时可用"的价钱；`BUILD-MAX-HEAP` 是批量构造，必须先拿到全部 $n$ 个元素才谈得上 $O(n)$。这与在线算法与离线算法的分野是同一件事，也是流式场景里插入法没有被淘汰的原因。补一句平均情况：随机输入下每个新元素平均只浮一两层，总代价与 $n$ 同阶，单调输入才是那个把 $\Theta(n \lg n)$ 兑现出来的最坏情形。
>
> 收束：`BUILD-MAX-HEAP` 的 $O(n)$ 不是技巧上的小聪明，而是"把代价记在高度上"这一分组方式的必然结果；换成把代价记在深度上，$n \lg n$ 立刻回来。

### Problem 6-2 · Analysis of d-ary heaps（d 叉堆分析） <span style="color:#2471a3;">**[problem]**</span>

A $d$-ary heap is like a binary heap, but (with one possible exception) non-leaf nodes have $d$ children instead of 2 children.

a. How would you represent a $d$-ary heap in an array?

b. What is the height of a $d$-ary heap of $n$ elements in terms of $n$ and $d$?

c. Give an efficient implementation of EXTRACT-MAX in a $d$-ary max-heap. Analyze its running time in terms of $d$ and $n$.

d. Give an efficient implementation of INSERT in a $d$-ary max-heap. Analyze its running time in terms of $d$ and $n$.

e. Give an efficient implementation of INCREASE-KEY(A, i, k), which flags an error if $k < A[i]$, but otherwise sets $A[i] = k$ and then updates the $d$-ary max-heap structure appropriately. Analyze its running time in terms of $d$ and $n$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> d 叉堆考的是你有没有真把"堆 = 完全 $d$ 叉树 + 序性质"这件事内化。题目四个小问看似各自独立，其实全部可以靠同一句话推完：数组下标给出一棵树，树高给出一条路径，路径长度就是一个操作的代价。
>
> a 问的表示法：结点 $i$ 的孩子是 $d(i-1)+2$ 到 $d(i-1)+d+1$ 这连续 $d$ 个下标，父结点是 $\lfloor (i-2)/d \rfloor + 1$。验算 $d = 2$ 时它退化成熟悉的 $\lfloor i/2 \rfloor$；取 $d = 4$、$i = 1$，孩子应为 $2, 3, 4, 5$，公式给出 $4(0)+2$ 到 $4(0)+5$，正确。之所以父结点公式要减 $2$，是因为根结点没有父亲、占了一个额外的偏移量。
>
> b 问：$n$ 个结点的完全 $d$ 叉树高为 $\lfloor \log_d n \rfloor$。代数字体会一下宽度换高度的效果：$n = 10^{6}$ 时 $\log_2 n \approx 19.93$，$\log_4 n \approx 9.97$，$\log_{16} n \approx 4.98$。$d$ 从 $2$ 提到 $16$，树高直接砍到四分之一。
>
> c 问 `EXTRACT-MAX` 的账要分两笔：末位元素搬到根之后，每层必须在 $d$ 个孩子里挑出最大者，这需要 $d-1$ 次比较；挑完再与当前结点比较一次。于是每层 $\Theta(d)$，总代价 $\Theta(d \log_d n)$。d 与 e 两问相反，`INSERT` 与 `HEAP-INCREASE-KEY` 都只沿单条祖先路径上行，每层只做一次父子比较，所以代价降到 $\Theta(\log_d n)$——孩子多不多与它们无关。
>
> 把两个代价放一起看，就能回答"$d$ 取多大最好"。比较次数正比于 $d \log_d n = d \ln n / \ln d$，与 $n$ 无关的系数是 $d/\ln d$。这个函数在 $d = e \approx 2.718$ 处取最小，离散地看：$d = 2$ 时系数 $2.885$，$d = 3$ 时 $2.731$，$d = 4$ 时 $2.885$，$d = 16$ 时 $5.771$。所以纯按比较次数，$d = 3$ 最优，$d = 2$ 与 $d = 4$ 恰好并列。
>
> 但真机不看比较次数，看 cache（缓存）。这一层要接 CSAPP 第 6 章：一条 $64$ 字节的 cache line（缓存行）装 $16$ 个 $32$ 位整数，$d = 16$ 时所有孩子正好挤在一行内，取最大者只需一次缺失；$d = 4$ 时四个孩子只占 $16$ 字节，通常与父结点同处一行，而下沉到下一层时新的四个孩子也往往还在同一行附近。$d = 2$ 则每层要么左要么右，跳跃距离以 $2$ 的幂增长，cache line 的复用率低。LaMarca 与 Ladner 1996 年发表于 ACM Journal of Experimental Algorithmics 第 1 卷第 4 篇的实测给出：$4$ 叉堆的缓存缺失数约为二叉堆的一半。
>
> 这也解释了工程实现的常见选择：标准库与竞赛代码里 $4$ 叉堆最流行，它的比较次数与二叉堆持平，却因树高减半而少了大约一半的 cache miss（缓存缺失）；$d = 16$ 在大规模数据上偶有胜出，代价是比较次数翻倍。
>
> 把四个小问写成一张统一的账本会更清楚：读一个结点是 $O(1)$，上浮一层要 $1$ 次比较加 $1$ 次写入，下沉一层要 $d$ 次比较（孩子里选大者）加 $1$ 次写入。于是任何操作的代价都等于"路径长度乘以每层单价"，路径长度由树高给出，每层单价由"要不要看孩子"给出。a 到 e 五问只是在这一张账本上换行。
>
> 为什么理论上最优的 $d = 3$ 在实践中少见？两个工程原因。一是 $d$ 取 $2$ 的幂时 $\lfloor (i-2)/d \rfloor$ 可以写成移位，$d = 3$ 则要做真正的整除，除法指令比移位慢一个数量级；二是四个孩子占 $16$ 字节、常常与父结点落在同一条 cache line（缓存行）里，三个孩子则容易跨行，边界对齐反而变差。数学上最优与机器上最优之间隔着一条指令集。
>
> 收束：$d$ 叉堆是"代价在树高与每层宽度之间搬运"的教科书例子——你把 $\log_d n$ 压低，就必须在每层多付 $d$ 次比较，$d$ 不消除对数因子，只调整它的底与前面的常数；$d = n$ 时堆退化成一个线性扫描的数组，对数因子以最昂贵的方式被"消除"。

### Problem 6-3 · Young tableaus（Young 氏矩阵） <span style="color:#2471a3;">**[problem]**</span>

An $m \times n$ Young tableau is an $m \times n$ matrix such that the entries of each row are in sorted order from left to right and the entries of each column are in sorted order from top to bottom. Some of the entries of a Young tableau may be $\infty$, which we treat as nonexistent elements. Thus, a Young tableau can be used to hold $r \le mn$ finite numbers.

a. Draw a $4 \times 4$ Young tableau containing the elements $\{9, 16, 3, 2, 4, 8, 5, 14, 12\}$.

b. Argue that an $m \times n$ Young tableau $Y$ is empty if $Y[1, 1] = \infty$. Argue that $Y$ is full (contains $mn$ elements) if $Y[m, n] < \infty$.……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Young tableau（Young 氏矩阵）把堆的树序换成了行列双单调：每行从左到右递增，每列从上到下递增。它不是堆的推广，而是把"一个方向上的偏序"换成"两个方向上的偏序"，代价与收益都由此而来。
>
> 定义里那句"某些元素可以是 $+\infty$，视作不存在的元素"是理解全局的钥匙。$+\infty$ 是一个吸收元：任何比较与它相遇都不会破坏单调性，因为"不小于任何数"这一条对一切有限值都成立。于是"未填满"与"已填满"可以用同一套单调性语言描述，不必为空格子写特例。
>
> b 问的第一个论断：若 $Y[1,1] = +\infty$，则整张表为空。证明只需两行单调性：对任意 $j$，行单调给 $Y[1,j] \ge Y[1,1] = +\infty$；对任意 $i$，列单调给 $Y[i,1] \ge Y[1,1]$。而 $+\infty$ 已是最大可能值，所以表里每个格子都是 $+\infty$，也就是一个有限元素都没有。
>
> 第二个论断反过来：若 $Y[m,n] < +\infty$，则表是满的。对任意 $i$ 有 $Y[i,n] \le Y[m,n]$（列单调，越靠下越大），对任意 $j$ 有 $Y[i,j] \le Y[i,n]$（行单调），合起来每个格子都不超过 $Y[m,n]$，于是全部有限，共 $m n$ 个元素。
>
> 这两个论断的实质是一条更一般的事实：单调函数在偏序集的两个端点取到极值。$Y[1,1]$ 是 product order（积偏序）下的最小元，$Y[m,n]$ 是最大元；把 matrix（矩阵）看成从有序对集合到实数集的单调映射，最小值必然落在最小元上，最大值必然落在最大元上，问 a、b 只是这条事实的两个特例。
>
> 用 6.042J 的语言重述一遍：把下标集合 $\{1, \dots, m\} \times \{1, \dots, n\}$ 装上积偏序，即 $(i,j) \preceq (i',j')$ 当且仅当 $i \le i'$ 且 $j \le j'$。这张偏序集里每条行、每条列都是一条 chain（链），而"行列双单调"正好是说 $Y$ 是从这个偏序集到实数的单调映射。注意它比全序弱得多：$(i,j)$ 与 $(i',j')$ 若一个下标大一个下标小，两者根本不可比，这正是下一注里"一次比较排除一整行或一整列"能成立的结构性原因。
>
> a 问的填法给一个：把 $\{2,3,4,5,8,9,12,14,16\}$ 按行排成三行——第一行 $2, 3, 4, 5$，第二行 $8, 9, 12, 14$，第三行第一个格子 $16$、其余七个留空。逐列检查 $2 \le 8 \le 16$、$3 \le 9$、$4 \le 12$、$5 \le 14$，逐行检查自然成立，所以这是一张合法的 $4 \times 4$ 表。填空位的顺序恰好是"从右上向左下"的阶梯，下一注会把它变成算法。
>
> 历史一句带过：这类填法由剑桥的 Alfred Young 在 1900 年引入，$1903$ 年起被 Frobenius 用于研究排列的对称结构，此后在代数里有独立的研究脉络。本书只借用它的偏序结构，那段代数背景与这里的问题无关。
>
> 值得对比一下"极值在哪里"。堆的最大元位置确定（就在根），最小元却要扫一遍叶子；Young 氏矩阵两头都确定：最小元在左上角、最大元在右下角。这份对称来自偏序的两个端点都存在于格子里，而堆的树叶有 $\lceil n/2 \rceil$ 个，最小值只能在其中某个叶子上。
>
> 用 $+\infty$ 占位还有一个实现上的好处：比较函数不必带"这个格子是否为空"的分支，单调性检查与下沉循环里没有特例，代码与满表完全一致。把"缺失"编码成"极大值"，是用一个值把两种状态压成一种——与上一章把"未使用的数组尾部"隐去是同一类做法。
>
> 收束：Young 氏矩阵是"二维的堆"——堆沿一条路径比较，它沿两个方向比较；堆的高度是 $\lg n$，它的"深度"是行列之和 $m+n$，下一页的 $O(m+n)$ 算法与 $O(n^{3})$ 排序全部由这个类比推出来。

---

> <span style="color:#7f8c8d;">CLRS Problem 6-3 / Notes for Chapter 6, p.168</span>

（接上页）

c. Give an algorithm to implement EXTRACT-MIN on a nonempty $m \times n$ Young tableau that runs in $O(m + n)$ time. Your algorithm should use a recursive subroutine that solves an $m \times n$ problem by recursively solving either an $(m - 1) \times n$ or an $m \times (n - 1)$ subproblem. (Hint: Think about MAX-HEAPIFY.) Define $T(p)$, where $p = m + n$, to be the maximum running time of EXTRACT-MIN on any $m \times n$ Young tableau. Give and solve a recurrence for $T(p)$ that yields the $O(m + n)$ time bound.

d. Show how to insert a new element into a nonfull $m \times n$ Young tableau in $O(m + n)$ time.

e. Using no other sorting method as a subroutine, show how to use an $n \times n$ Young tableau to sort $n^2$ numbers in $O(n^3)$ time.

f. Give an $O(m + n)$-time algorithm to determine whether a given number is stored in a given $m \times n$ Young tableau.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> c 问与 f 问是同一条路径的两种写法，可以给它起个名字叫"阶梯下潜"：从右上角 $Y[1,n]$ 出发，当前元素比目标大就左移一列，比目标小就下移一行。整条路径像下楼梯，每走一步都永久排除一整行或一整列。
>
> 为什么一次比较能排除一整条链？关键在两个方向单调的"方向相反"。站在 $(i,j)$：若 $Y[i,j] > x$，则该列中它下方的每个元素都不小于它、因而都大于 $x$，这一列从第 $i$ 行往下全部作废；若 $Y[i,j] < x$，则该行中它左侧的每个元素都不大于它、因而都小于 $x$，这一行从第 $j$ 列往左全部作废。两种情形合起来，每步恰好删掉一条 chain（链）。
>
> 代价立刻算得出：行最多走 $m-1$ 步，列最多走 $n-1$ 步，总步数不超过 $m+n-1$。$4 \times 4$ 的表最多 $7$ 步，$1000 \times 1000$ 的表最多 $1999$ 步；而逐格扫描要 $10^{6}$ 次比较。这是 saddleback search（鞍点搜索）的常见版本。
>
> 与二分搜索对照，差别来自序结构：一维数组是全序，一次比较把候选劈成两半，于是有 $\lg n$；二维偏序里 $(i,j)$ 与 $(i',j')$ 常常不可比，"比它小的都在左上、比它大的都在右下"只对一个象限成立，所以每步只能扔掉一条链，得到 $m+n$ 而不是 $\lg(mn)$。维度换了，能保住的对数就没了——这是"可比较性决定下界"的一个干净例子。
>
> c 问要的是同一路径的递归记账：抽走 $Y[1,1]$ 后把 $+\infty$ 填进去，然后让这个洞下沉。下沉规则是"与右邻、下邻中较小的那个交换"。为什么不与较大的交换？取较小的那个才不会破坏另一条链的单调性。
>
> 把这一步写清楚：洞在 $(i,j)$，右邻 $R = Y[i,j+1]$，下邻 $D = Y[i+1,j]$，设 $R \le D$，于是把 $R$ 搬进洞里。行方向：$R$ 原本右边不小于它，洞移到 $(i,j+1)$ 后新右邻是 $+\infty$，不成问题。列方向：新填进 $(i,j)$ 的 $R$ 必须不小于上邻，而 $Y[i-1,j] \le Y[i-1,j+1] \le Y[i,j+1] = R$，第一个不等号来自行单调、第二个来自列单调，链就接上了。若改成搬较大的 $D$，这一串不等号立刻断掉。
>
> 记账用的规模变量不是 $(m,n)$ 两个数，而是 $p = m+n$：每下沉一步，洞沿行或沿列各前进一格，可用的行数加列数之和恰好减 $1$，所以 $T(p) = T(p-1) + O(1)$，解得 $O(m+n)$。抓住一个不变量比分别追踪两个变量省事得多。
>
> d 问的 `INSERT` 是镜像动作：把新元素放进右下角那个 $+\infty$ 的位置，然后沿"上邻、左邻中较大的那个"上浮，规则与堆的 sift-up（上浮）完全同构，只是把"父结点"换成了两个可比较的邻居；代价同样是 $O(m+n)$。若表已满，则要先把最大元取出（一次 `EXTRACT-MIN` 式的下潜），腾出右下角。
>
> e 问的 $O(n^{3})$ 是直和：$n^{2}$ 个元素逐个插入、每次 $O(n)$，得到 $n^{3}$。代数字：$n = 100$ 时约 $10^{6}$ 次基本操作。这个界比任何 $O(n^{2} \lg n)$ 的比较排序都差，题面之所以要求"不得调用其它排序"，就是要你看清这一点——它是用空间结构换"不许用现成工具"的产物，工程上没人会这样做。
>
> 收束：Young 氏矩阵这一组题的价值在于给出两个可复用的模板。其一是"沿两条链下潜、每步删一条链"的 `saddleback search`；其二是"用一个 $+\infty$ 洞在二维格子上滚动"的下沉与上浮，它们与堆的 `MAX-HEAPIFY`、`HEAP-INCREASE-KEY` 是一一对应的动作，只是把一维路径换成了二维阶梯。

## Notes for Chapter 6（第 6 章注释） <span style="color:#2471a3;">**[reference]**</span>

> <span style="color:#7f8c8d;">[note] 按规范，本章 notes（注释/参考文献）保留英文原文，不作翻译；文中受损的数学记号已按原书恢复。</span>

The heapsort algorithm was invented by Williams [357], who also described how to implement a priority queue with a heap. The BUILD-MAX-HEAP procedure was suggested by Floyd [106].

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这两句话是堆的出生证明。我把能核实的部分留下，把传言剔掉：heapsort（堆排序）与 binary heap（二叉堆）出自 J. W. J. Williams 的 Algorithm 232，发表于 Communications of the ACM 第 7 卷第 6 期（1964 年 6 月），页码 347–348；他当时在英国伦敦的 Elliott Bros. 公司工作，思想形成于 1963 年前后。
>
> 值得强调的不是年份，而是那篇短文同时给两样东西：一个排序算法，和一个可以独立使用的数据结构。此前的排序算法都把辅助结构当成私有细节，Williams 把"能反复取最大值的容器"单独拎出来描述，priority queue（优先队列）从此有了标准实现。NIST 的算法词典条目也是这么记的。
>
> Floyd 的贡献是 Algorithm 245 Treesort 3，同年第 7 卷第 12 期、第 701 页。它把建堆改成原地、自底向上，也就是今天的 `BUILD-MAX-HEAP`；CLRS 引用 Floyd 的正是这一步。两个版本的功能相同，代价却差了整整一个对数因子：逐个插入建堆最坏 $\Theta(n \lg n)$，自底向上是 $O(n)$。上一注里那道 Problem 6-1 就是在让你亲手复算这个差距。
>
> 为什么当时需要它？1960 年代初的批处理系统要按优先级挑下一个任务，离散事件模拟要按时间戳挑下一个事件，两者都是"反复取最小或最大"的负载。用有序数组每次都 $O(n)$ 插入，用无序数组每次 $O(n)$ 找最小，堆把两个操作都压到 $O(\lg n)$，第一次让"既快插入、又快取极值"同时成立。动机是调度，不是排序——这一点常被忽略。
>
> 后续的影响可以只看一条主线：优先队列的每次提速都直接改写图算法的界。Dijkstra 与 Prim 用二叉堆得到 $O((V+E)\lg V)$；Fredman 与 Tarjan 的 Fibonacci heap（斐波那契堆）把 `DECREASE-KEY` 摊还到 $O(1)$，Dijkstra 降到 $O(E + V \lg V)$；van Emde Boas 树与 Thorup 的整数堆进一步压到 $O(\lg \lg n)$ 量级。这里不列年表，只记结论：图的算法复杂度长期就是被"优先队列能做到多快"牵着走的。
>
> 跨课程连接：CSAPP 第 6 章解释了为什么理论优雅的堆在实机上常常跑不过 quicksort（快速排序）。堆排序的比较次数已经接近最优，但下沉时的访问模式在数组里跳跃，cache（缓存）不友好，分支也不可预测；快速排序顺序扫描，预取器能跟上。工程上的折中是 introsort（内省排序，Musser 1997）：平时用快速排序，递归深度超过 $\Theta(\lg n)$ 就切到堆排序兜底，于是平均快、最坏仍然是 $O(n \lg n)$。堆在这里的角色是"最坏情况的保险"。
>
> Floyd 在 treesort（树排序）这个名下发表过一系列算法，Treesort 3 是其中的第三个；同系列早期的那些编号与卷期我未能一手核实，这里就不写死。可以确定的是本书正文把 `BUILD-MAX-HEAP` 明确署给 Floyd（参考文献编号 106），这条归属没有争议。
>
> 今天 heapsort 的用武之地不在通用排序，而在三个场合：额外空间极紧（只要 $O(1)$，数据全在已给的数组里）、必须给出最坏情况的硬性保证（$\Theta(n \lg n)$ 是确定性上界，随机化算法只能承诺期望）、以及实时系统里按截止时间排序的就绪队列。它慢在常数，赢在确定性与空间，这个取舍六十年没变。
>
> 收束：Williams 给了结构与算法，Floyd 给了线性建堆与原位性，此后六十年的工作都在同一件事上加码——把"取极值"的代价再压低一点。数据结构的历史，很大一部分就是优先队列的历史。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第 170 页开篇这段话说了一件反直觉的事：quicksort（快速排序）的最坏情况是 $\Theta(n^{2})$，比 heapsort（堆排序）的 $\Theta(n \lg n)$ 差，可实践中它常常是最快的通用排序。答案不在渐近记号里，而在三处常数级的细节上，以及一处结构性的取舍上。
>
> 先说取舍。归并排序与快速排序都是 divide-and-conquer（分治）：把数组切开、递归排好、再拼起来。区别在于重活放在哪一步。归并的"分"是平凡的（中点一劈），"合"要苦干 $\Theta(n)$，而且必须有第二块缓冲区；快排恰好相反，划分时苦干 $\Theta(n)$，但两个子数组各自有序之后，整体自动有序，"合"是免费的、不需要任何动作。
>
> 这个差别决定了内存行为。归并每层都要把 $n$ 个元素搬进缓冲区再搬回来，快排只在划分时原地交换，一个字节都不额外申请。$n = 10^{6}$ 个 $4$ 字节整数时，归并需要额外的 $4$ MB 缓冲，$\lg n \approx 20$ 层下来累计搬运约 $2 \times 10^{7}$ 个字；快排的额外空间是递归栈，深度约 $20$。
>
> 再说三个常数细节。第一，划分是对子数组的一次顺序扫描，地址严格递增，硬件预取器能完整跟上：一条 $64$ 字节的 cache line（缓存行）装 $16$ 个整数，$10^{6}$ 个元素一趟只产生约 $6.25 \times 10^{4}$ 次必需的缺失。第二，内层循环体极简——一次比较、一次自增、偶尔一次交换，没有函数调用、没有额外数据结构操作。第三，in-place（原位）排序让整个工作集就是原数组本身，不会因为第二块数组而与原数组争抢 cache 与 TLB 表项；CLRS 特意提到它在 virtual-memory environments（虚拟存储环境）下也表现良好，说的正是这一层。
>
> 代价也有：递归深度是 $\Theta(\lg n)$ 的期望值，但最坏到 $n$，栈可能溢出；等值元素多时 Lomuto 划分会退化；已排序输入配固定主元更是直接落到 $\Theta(n^{2})$。工程实现因此叠了三层补丁：三数取中或随机主元打散最坏输入、小区间（十来个元素以内）改用 insertion-sort（插入排序）以减少递归开销、递归深度超限则切到 heapsort（堆排序）兜底。最后这一招就是 introsort（内省排序）。
>
> 跨课程连接：CSAPP 第 6 章的 cache（缓存）模型给出了"为什么顺序扫描值钱"的定量答案——缺失代价按百 cycle 计，而一次命中的比较只要一两个 cycle，所以"少缺失"比"少比较"更影响墙钟时间；第 3 章的分支预测则解释了内层循环的隐藏成本：`if A[j] <= x` 的走向由数据决定、随机输入下几乎不可预测，每次误预测要十几个 cycle。6.042J 那边给的是另一件工具：把"每层 $\Theta(n)$、共 $\Theta(\lg n)$ 层"写成递归式再解，是这套分析的骨架。
>
> 还有一个常被忽略的对比维度：稳定与适应。归并排序是 stable（稳定）的，能保留相等元素的原始次序，也容易改成利用已有有序性的多路归并；快速排序两者都不满足，代价是它对随机输入的常数最小。选型时应先问输入分布与是否需要稳定排序，再谈谁更快——脱离输入分布问"哪个排序最好"没有答案。
>
> 收束：快排赢的不是渐近，而是"把全部代价集中在一次顺序扫描上"这个结构选择。分治的代价放在分解还是合并，是设计这类算法时最核心的一问；本章后面的 7.2 与 7.4 全部在为"划分划得平均"这件事定价。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> `PARTITION` 的 loop invariant（循环不变式）描述的是四个区域而不是两个，这一点值得停下来想清楚：$A[p..i]$ 放已确认不大于 $x$ 的元素，$A[i+1..j-1]$ 放已确认大于 $x$ 的元素，$A[j..r-1]$ 是尚未检视的未知区，$A[r]$ 是 pivot element（主元）本身。
>
> 两个指针的分工是这套机制的骨架：$j$ 是探路者，每轮无条件前移一格，把未知区最左边那个元素"消费"掉；$i$ 是边界记录者，只在发现一个不大于 $x$ 的元素时才前移一格。于是 $i$ 永远指向"不大于 $x$ 区域"的最后一个位置，循环结束时 $A[i+1]$ 正是"大于 $x$ 区域"的最左元素，最后一步交换 `A[i+1]` 与 `A[r]` 就能把主元恰好嵌进两个区域中间。
>
> 为什么必须四块，不能把未知区并进"大于 $x$"区？因为未知区里的元素还没看过，随时可能跳出一个不大于 $x$ 的；若把它们预先算作"大于"，每遇到一个小的就得在整段里挪位置，代价从 $O(1)$ 涨到 $O(n)$。把"已确认"与"未检视"分开，是让每轮只付常数代价的唯一办法。主元留在 $r$ 不动，也是为了最后一刻一次到位。
>
> 代价算得干净：$j$ 从 $p$ 走到 $r-1$，共 $r-p$ 轮，每轮至多一次比较加一次交换（三次赋值），所以整体 $\Theta(n)$。$n = 1000$ 时就是 $999$ 轮、至多 $999$ 次比较。
>
> 拿 Figure 7.1 的数组走一遍：$A = \langle 2, 8, 7, 1, 3, 5, 6, 4 \rangle$，$x = 4$，初始 $i = 0$。$j = 1$ 时 $2 \le 4$，$i$ 增到 $1$，与自身交换；$j = 2, 3$ 时 $8$ 与 $7$ 都大于 $4$，$i$ 不动；$j = 4$ 时 $1 \le 4$，$i = 2$，交换 $A[2]$ 与 $A[4]$ 得 $\langle 2, 1, 7, 8, 3, 5, 6, 4 \rangle$；$j = 5$ 时 $3 \le 4$，$i = 3$，交换 $A[3]$ 与 $A[5]$ 得 $\langle 2, 1, 3, 8, 7, 5, 6, 4 \rangle$；$j = 6, 7$ 都大于 $4$。循环结束时 $i = 3$，交换 $A[4]$ 与 $A[8]$，得 $\langle 2, 1, 3, 4, 7, 5, 6, 8 \rangle$，返回下标 $4$。左边三个都不大于 $4$，右边四个都大于 $4$。
>
> trace 里藏着一个真实机器才在乎的细节：当 $i+1 = j$ 时（比如 $j = 1$ 那轮），交换其实是元素与自身交换，语义上什么也没做，真机却仍要三次读写。加一个 `if (i+1 != j)` 判断能省掉它，但判断本身也要一次比较与一次分支，通常并不划算——这类"优化"必须先量化再动手。
>
> 跨课程连接：初始化、保持、终止三段式，就是 6.042J 里数学归纳法的 base、step 与"归纳变量走到终点"。三段式真正省力的地方在于它把"整段程序正确"降级为"一步转移正确"：你只需检查 $A[j]$ 这一格被处理后的局部状态，不必在每轮重新扫描全数组。这与证明一个递推关系时只验证 $T(n)$ 与 $T(n-1)$ 的关系是同一种思维。
>
> 最后一句工程注：划分内层那个数据相关的分支是快速排序常数里不小的一块。Hoare 版划分把主元放在两端、双向夹逼，交换次数约为 Lomuto 版的一半，内层循环也更短，这是许多标准库选它的原因。
>
> 再补一个自检点：循环终止时未知区必须是空的，也就是 $j$ 恰好走到 $r$，这是"三段归纳"能收尾的前提。若边界写错、提前退出，未知区会被静默当成"大于 $x$"处理，划分结果表面上仍像是对的，错误要等到最终排序出现局部乱序才暴露——不变式写得清楚，正是为了让这种静默错误无处藏身。
>
> 收束：把图 7.2 的四区域与 $i$、$j$ 的移动对应起来看，第 7 章后面的每个结论都只是这四块区域在不同输入下的演化。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段不变式论证里最需要盯住的是 Maintenance（保持）的第二种情况：当 $A[j] \le x$ 时，循环递增 $i$、交换 $A[i]$ 与 $A[j]$、再递增 $j$；交换之后要成立的是 $A[j-1] > x$。这一步并不是"看上去显然"，它是被不变式本身保证的。
>
> 把交换看清楚。执行交换前，$i$ 是"不大于 $x$ 区域"的右端，所以 $A[i+1]$ 是"大于 $x$ 区域"的最左元素；交换把 $A[i+1]$ 搬到 $A[j-1]$ 的位置上。如果"大于 $x$ 区域"非空，那么这个被搬过去的元素按不变式的第二条本来就大于 $x$，于是 $A[j-1] > x$ 立刻成立。
>
> 如果"大于 $x$ 区域"是空的呢？那就意味着 $i+1 = j$，交换的两端是同一个位置，元素与自己交换，$A[j-1]$ 仍然是原来那个不大于 $x$ 的元素——而这一轮恰恰是被判为 $A[j] \le x$ 才进来的，所以 $A[j-1] > x$ 这条断言在空区情形下根本不适用，因为此时 $A[j-1]$ 已经被划入"不大于 $x$"的一侧。两种子情形合起来，才覆盖全部可能。
>
> 这正是循环不变式方法的用处：每一轮的新状态都能从旧状态"继承"合法性，你不需要在每轮重新扫描整个数组去确认性质。局部改动只影响局部的几条断言，其余由归纳假设兜住。与 6.042J 里的数学归纳对照，初始化是 base case，保持是 inductive step，终止是"归纳变量走到终点"——三段一一对应。
>
> 顺带纠正一个常见误解：`PARTITION` 结束时只是主元就位，$A[p..q-1]$ 与 $A[q+1..r]$ 内部依旧无序。快速排序的"合并"之所以免费，是因为划分已经把全局的相对次序信息压缩进了下标 $q$ 里；真正的工作全部预付在这一步。
>
> 还有一个更强的性质值得记住：划分之后主元严格小于右侧每个元素，而不是"不大于"。原因是"大于 $x$ 区域"的判据是严格的 $> x$，等于 $x$ 的元素全部被留在左侧。于是有重复元素时，与主元相等的元素会聚在左边，`QUICKSORT` 递归右子数组时不会再把它们拿来比较——这一点在第 7.4 节的期望分析里是隐含前提。
>
> 把代价数量化：一次 `PARTITION` 的交换次数不超过元素个数 $r-p+1$，每次交换三次赋值，$n = 1000$ 时至多约 $3000$ 次写入；而整个排序的写入总量由递归树的每一层累加，正是 $\Theta(n \lg n)$ 层的乘积。循环里那个数据相关的分支不可预测，每次误预测要十几个 cycle，这部分成本在渐近记号里完全看不见。
>
> 补一句终止时的收敛：循环结束时 $j = r$，四个区域塌缩成三块——$A[p..i]$ 都不大于 $x$、$A[i+1..r-1]$ 都大于 $x$、$A[r] = x$。"划分成三个集合"这句话的严格来源就在这里，图 7.2 画的是过程，终止式才是结论。
>
> 一个可复核的自检办法：把不变式写成谓词 $P(i,j)$，每轮代码执行完立刻验证 $P(i',j')$。这就是把证明机械化，也是写 `assert` 的思路——测试版本里把不变式写成运行期断言，绝大多数边界错误会当场暴露，而不是等到结果乱序。
>
> 收束：$A[j-1] > x$ 这条细节是整段证明的承重点——它告诉你"继承"从哪来。看懂了它，循环不变式就不再是背下来的三段模板，而是可以随时自己重写的一件工具。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 最坏情况出现在划分产生 $n-1$ 与 $0$ 两个子问题的时候。`PARTITION` 固定取 $A[r]$ 当 pivot element（主元），于是"输入已经升序"这件在工程中极其常见的事，恰好把最坏情况兑现出来：每层的 $A[r]$ 都是当前子数组的最大值，所有元素都不大于它，划分结果退化成"$n-1$ 个元素"加"一个空"。
>
> 递归然后写成 $T(n) = T(n-1) + T(0) + \Theta(n) = T(n-1) + \Theta(n)$：规模每次只减一，而划分照旧收 $\Theta(n)$。把每层代价加起来就是算术级数 $n + (n-1) + \cdots + 1 = n(n+1)/2$。$n = 1000$ 时是 $500500$ 次比较，而 $n \lg n \approx 9966$，相差约 $50$ 倍；$n = 10^{5}$ 时相差约 $5000$ 倍。
>
> 这条链还有比时间更早致命的问题：递归深度等于 $n$。假设每层 stack frame（栈帧）约 $48$ 字节，$n = 10^{6}$ 就需要约 $48$ MB 栈空间，而 CSAPP 第 9 章讲过，进程主线程的栈默认只有 $8$ MB 左右——程序在超时之前就先因栈溢出而崩掉。
>
> 为什么"退化成长链"必然导致二次代价？因为快速排序的总代价等于"每个元素在所参与的每一层里被比较一次"，而每个元素参与的层数就是它在递归树里的深度。平衡时深度是 $\lg n$，总和 $n \lg n$；退化时深度是 $1, 2, \dots, n$，总和 $n^{2}/2$。递归树的形状就是代价的全部来源。
>
> 对策有四层，作用点各不相同。随机选主元（第 7.3 节）让"最坏输入"这个概念失效；三数取中降低遇到坏划分的频率但不能消除；算法层检测递归深度、超过 $\Theta(\lg n)$ 就切 heapsort（堆排序）兜底，这就是 introsort（内省排序）；实现层则可以只对较小子数组递归、较大者用循环迭代，把栈深度硬性压到 $\Theta(\lg n)$。
>
> 第四层值得单独说，因为它与主元选择无关、纯粹是控制流技巧。递归时先处理较小的那一半，较大的那一半用 while 循环继续，则栈上永远只压着"不超过当前规模一半"的子问题，深度自动被 $\lg n$ 封顶。代价不变，鲁棒性却从"看运气"变成"有保证"。
>
> 跨课程连接：这里用到三块现成脚手架。6.042J 的级数求和给出 $n(n+1)/2$ 的封闭形式；CLRS 第 4 章的 substitution method（代换法）给出 $T(n) = T(n-1) + \Theta(n)$ 的解为 $\Theta(n^{2})$；CSAPP 第 9 章的虚拟内存给出栈大小这一物理约束。三者叠起来才是完整的判断：不是"慢了 50 倍"，而是"根本跑不完"。
>
> 再补一笔工程量化：$n = 10^{4}$ 时退化情形的比较次数约 $5 \times 10^{7}$，平衡情形约 $1.3 \times 10^{5}$，相差近四百倍；在每秒能跑 $10^{9}$ 次比较的机器上，前者是几十毫秒，后者是微秒级。所谓最坏情况不是理论上的尾巴，而是银行流水、日志时间戳这类几乎有序的输入会直接撞上来的现实。
>
> 最后提醒量纲：这里说的是比较次数的 $\Theta(n^{2})$，而退化情形的交换次数同样是 $\Theta(n^{2})$——几乎每次比较都伴随一次交换，所以它不是"只慢在比较上"的软退化，而是时间与写入一起崩。
>
> 收束：已排序输入最慢，是"固定主元加单侧划分"这个组合的直接后果，不是快速排序的固有属性。7.3 节的随机化正是把这条确定性缺陷换成一次概率极低的事故；Exercise 7.2-4 让你拿插入排序与它赛跑，赛的正是"几乎有序"这一类输入。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段论证悄悄做了一次视角转换：不再追问"递归树有多少层、每层省了多少"，而是问"代价被谁吃掉了"。9 比 1 的分割乍看很不平衡，可它给出的答案与从正中间切开完全同阶。
>
> 机制是这样展开的。递归式为 $T(n) = T(9n/10) + T(n/10) + c n$，其中显式写出的 $c n$ 是划分代价。在树的第 $d$ 层，各结点的规模之和不超过 $n$，因为 $9/10 + 1/10 = 1$；所以只要这一层的所有结点都还在递归（没触到边界条件），该层总代价就是 $c n$，与层的深浅无关。
>
> 层数由两条路径夹住。沿着"每次取较小的那一半"往下，规模按 $1/10$ 收缩，$\log_{10} n$ 层之后降到常数，这是最浅的叶子；沿着"每次取较大的那一半"往下，规模按 $9/10$ 收缩，能撑 $\log_{10/9} n$ 层，这是最深的叶子。所以前 $\log_{10} n$ 层每层付满 $c n$，之后各层代价不超过 $c n$，总计不超过 $c n \cdot \log_{10/9} n$，即 $O(n \lg n)$。
>
> 代数字体会一下常数有多贵：$n = 10^{9}$ 时 $\log_{10} n = 9$，$\log_{10/9} n \approx 196.7$，而 $\lg n \approx 29.9$，常数因子约 $6.6$ 倍。如果把比例换成 99 比 1，最深深度变成 $\log_{100/99} n \approx 2061.9$，约是 $\lg n$ 的 $69$ 倍。阶没变，常数变得很难看。
>
> 一般化成一个可套用的结论：若每层按 $\alpha$ 与 $1-\alpha$ 分割且 $0 < \alpha \le 1/2$，则深度约为 $\ln n / \ln(1/(1-\alpha)) \approx \ln n / \alpha$，总代价约为 $n \ln n / \alpha$。$\alpha$ 越小常数越大，但只要 $\alpha$ 是不依赖 $n$ 的常数，对数阶就保住。
>
> 那什么样的分割才真的致命？只有"一个子问题规模为 0"这一类，因为它不缩小问题，递归树退化成一条链，深度从 $\Theta(\lg n)$ 变成 $n$。换句话说，毁灭性的不是"分得不均"，而是"完全没分"。任何正比例的划分都把规模按几何级数缩小，而几何级数收敛得比任何多项式都快。
>
> 跨课程连接：这套"每层代价相同、层数由缩放因子决定"的算法就是 6.042J 里的等比级数加对数换底；把它与归并排序的递归树并排放，形状完全一样，只是分叉处从 $(1/2, 1/2)$ 换成了 $(9/10, 1/10)$。这也解释了为什么归并排序的 $\Theta(n \lg n)$ 与快速排序的期望 $\Theta(n \lg n)$ 是同一个量级，而两者的常数因子相差一个依赖分割比例的因子。
>
> 这里得到的是上界而不是紧界。上界只需两句话："每层不超过 $c n$、层数不超过 $\log_{10/9} n$"，粗糙一点也无妨；要拿到 $\Omega(n \lg n)$ 还得另证每一层至少付 $c n$。Exercise 7.2-2 做的正是这件事——最好情况下递归树每层仍要付 $\Theta(n)$ 的划分费，所以 $n \lg n$ 不只是上界，也是最好情况的紧界。上界与下界分开证，是第 4 章传下来的标准分工。
>
> 数值校验一次：$n = 10$ 时 $\log_{10/9} 10 \approx 21.85$，手画 9 比 1 的递归树深度确实落在二十上下，公式与实验一致。
>
> 还有一个实践含义：既然代价对 $\alpha$ 如此不敏感，就不值得为"完美对半分"付出高昂的主元选择代价。取三个数求中位数能把 $\alpha$ 压到 $0.4$ 附近，额外成本只是常数次比较；真正糟糕的是 $\alpha$ 逼近 $0$，那时 $1/\alpha$ 会爆炸——7.2 节的退化分割正是 $\alpha = 0$ 的极限。
>
> 收束：结论一句话——任何常数比例的分割都保住 $O(n \lg n)$，真正致命的只有退化为零的分割；这一观察在 7.4.2 节的期望分析里会以"好分割与坏分割混合"的形式再出现一次。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里悄悄立起了一个概率模型，值得用第一性原理拆开：我们凭什么可以假定"输入的所有排列等可能"？先看这个假设为什么是允许的，再看它强在哪、弱在哪。
>
> 第一步是化简：快速排序的行为只取决于元素的 relative ordering（相对次序），不取决于具体数值。`PARTITION` 只做比较、从不看数值的绝对大小，所以把数组里每个元素都换成 $2x_i$、或换成它的排名，运行轨迹分毫不动。用 6.042J 的语言说，输入空间被"保序变换"这个等价关系商掉了，剩下的自由度只有排列，共 $n!$ 个等价类。
>
> 第二步是假设："每个排列等可能"正是 5.2 节雇用问题用过的同一假设，那里说的是候选人次序均匀随机，这里说的是输入次序均匀随机。有了它，才能谈"平均情况"——否则"平均"这个词没有定义。
>
> 这个假设的力量在于量纲：最坏的排列只占全部输入的 $1/n!$。$n = 20$ 时 $20! \approx 2.43 \times 10^{18}$，最坏排列的概率是 $4.1 \times 10^{-19}$；$n = 100$ 时这个数小到没有任何现实意义。于是"坏输入"从确定性的威胁降格成一个概率极低的事件。
>
> 它的弱点同样明显：真实数据几乎从不均匀。银行流水按时间排序、日志按写入顺序递增、数据库主键自增——这些都是"基本有序"，恰好落在均匀分布的极端外侧。7.3 节的随机化正是要根治这一点：不再假设输入随机，而是让算法自己掷骰子。
>
> Exercise 7.2-6 的 80% 与 20% 可以从这个模型直接算出来：主元均匀落在 $n$ 个位置之一，分割不劣于 9 比 1 当且仅当主元的排名落在中间 $80%$ 的位置区间里，于是概率是 $0.8$；剩下 $0.2$ 的概率分割更差。这两句话合起来就是本节结尾"好分割与坏分割随机混合、整体仍是 $O(n \lg n)$"的定量版本。
>
> 跨课程连接：三个现成脚手架。5.2 节雇用问题提供了 indicator random variable（指示器随机变量）的用法；概率论课程里（教材是 Bertsekas）"均匀分布加期望线性性"是同一套工具；6.042J 的等价类与商集给出"为什么可以只数排列"的严格依据。区别在于：雇用问题里随机性来自现实（候选人顺序），这里随机性是我们主动装进算法的。
>
> 再补一个量纲对照：$n!$ 增长得比任何指数都快——Stirling 公式给出 $n! \approx \sqrt{2 \pi n}(n/e)^{n}$——所以这个均匀模型对越大的输入越宽容——大输入下最坏排列几乎不可能被随机抽到；而小输入（$n \le 10$）时所有排列都可能出现，讨论平均情况的意义有限。
>
> 顺带记一条对称性：均匀假设下每个元素成为主元的概率都是 $1/n$，所以"哪一段被切在左边"完全随机。这条对称性是 7.4.1 节最坏情况分析与 7.4.2 节期望分析的共同起点，后面反复要用。
>
> 收束：这个假设不是数学上的偷懒，而是把"输入分布"这个无法掌控的东西换成"算法内部随机"这个可以掌控的东西的第一步；严格版本在 7.4.2 节，那里连"排列等可能"都不再需要。

在平均情况下，PARTITION 产生 "good" split（好分割）与 "bad" split（坏分割）的混合。在平均情况下一次 PARTITION 执行的递归树中，好分割与坏分割随机地分布在整个树中。为了获得直观认识，不妨假定好分割与坏分割在树中交替地出现在各层上，且好分割是最好情况的分割，坏分割是最坏情况的分割。图 7.5(a) 展示了递归树中连续两层上的分割。在树的根结点处，划分的代价为 $n$，产生的子数组规模为 $n-1$ 和 $0$：这是最坏情况。在下一层，规模为 $n-1$ 的子数组经历最好情况的划分，产生规模为 $(n-1)/2 - 1$ 和 $(n-1)/2$ 的子数组。让我们假定规模为 $0$ 的子数组的 boundary-condition cost（边界条件代价）为 $1$。……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §7.2 + Exercises 7.2-1~5, p.178</span>

（接上页）坏分割与随后的好分割的组合，产生了三个规模分别为 $0$、$(n-1)/2 - 1$ 和 $(n-1)/2$ 的子数组，其划分代价合计为 $\Theta(n) + \Theta(n-1) = \Theta(n)$。毫无疑问，这一局面并不比图 7.5(b) 中的局面更差——后者即单层划分产生两个规模为 $(n-1)/2$ 的子数组、代价为 $\Theta(n)$ 的情形。然而，后一种情形可是 balanced（平衡的）！直观上，坏分割的 $\Theta(n-1)$ 代价可以被吸收进好分割的 $\Theta(n)$ 代价之中，而得到的分割是一个好分割。因此，当各层在好分割与坏分割之间交替时，quicksort 的 running time（运行时间）就如同只有好分割时的运行时间一样：仍然是 $O(n \lg n)$，只不过是 $O$ 记号背后隐藏了一个稍大一点的常数。

我们将在 Section 7.4.2 中对一个 randomized version（随机化版本）的 quicksort 的 expected running time（期望运行时间）给出严格的分析。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本节最重要的一句话是"坏分割的代价可以被好分割吸收"，其余段落都是它的展开。先把机制拆开：坏分割本身并没有浪费时间，它买到了一层进展。
>
> 看连续两层的账。根结点处划分付 $n$ 的代价，产生规模 $n-1$ 与 $0$ 两个子问题——这是最坏情况。紧接着在规模 $n-1$ 的那个子问题上做一次最好情况的划分，付 $n-1$ 的代价，产生规模 $(n-1)/2-1$ 与 $(n-1)/2$ 两个子问题。两层合计付出 $\Theta(n) + \Theta(n-1) = \Theta(n)$。
>
> 把它与"两层都是好分割"并排放：后者的代价是 $n + n = 2n$，余留子问题各为 $(n-1)/2$；前者是 $n + (n-1) \approx 2n$，余留子问题为 $(n-1)/2-1$ 与 $(n-1)/2$，反而更小。$n = 1000$ 时前者 $1999$、后者 $2000$，子问题规模 $498$ 与 $499$、$500$ 与 $500$——差别小到可以当作噪声。
>
> 于是结论成立：只要坏分割不连续出现，它只是把常数因子推大，不改增长阶。量化一下——每两层至少推进一次"规模减半"，所以递归树深度不超过 $2 \lg n$，总代价 $O(n \lg n)$，$O$ 背后的常数是 $2$ 而不是 $1$。
>
> 这条论证的适用边界必须说清。它假定坏分割与好分割在树中交替出现；若坏分割连续出现 $n$ 次（已排序输入配固定主元就是这种情形），"交替"这个假设当场破产，结论立刻退回 $\Theta(n^{2})$。所以交替只是"最保守的混合假设"，不是定理。
>
> 把它严格化需要概率语言：7.4.2 节用 indicator random variable（指示器随机变量）证明期望意义下每一层都会甩掉一个常数比例的元素，从而递归树深度在期望意义下为 $\Theta(\lg n)$。交替论证是那个证明的直觉版本——它告诉你"混合"为什么足够，只是不肯花力气算概率。
>
> 跨课程连接：这是 amortized analysis（摊还分析）的思维方式——单次操作贵不贵不重要，关键是那次昂贵是否买到了实质进展。第 17 章会用 potential method（势能法）把这种"记账"变成形式化工具。另一个连接在 CSAPP 第 6 章：评价 cache（缓存）性能看的是平均每指令缺失数，而不是某一次缺失有多惨；两者的共同点是"看统计量而非最坏单点"。
>
> 把"吸收"写成不等式会更硬。设坏分割在规模 $n$ 上的代价是 $\Theta(n)$，随后在规模 $n-1$ 上的好分割也是 $\Theta(n-1)$，两者之和 $\Theta(n)$；而"连续两次好分割"同样是 $\Theta(n)$。所以从代价看，坏分割只在常数项上体现，不进增长阶。
>
> 反过来看，这条论证也说明了最坏情况为什么必须"连续坏"才致命：单次坏分割至多浪费一个 $n$ 的常数倍，要累积成 $n^{2}$ 需要大约 $n$ 次连续坏分割。随机化的作用正是把"连续"这个前提打散。
>
> 给一个可算的对照：若每 $k$ 层里只有一层是坏的，总代价约是 $\Theta(n \lg n)$ 的 $1 + 1/k$ 倍；$k = 2$ 时就是本节的交替情形，常数约 $1.5$ 上下，$k = 10$ 时几乎看不出来。这回答了"要多好才算够"——常数比例的混合就够。
>
> 收束：坏分割与好分割交替时，快速排序的 running time（运行时间）与只有好分割时同阶，只是常数更大。这句话既是直觉，也是后面精确分析要兑现的承诺。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 7.2-5 的两个深度公式是"按比例衰减的递归树"这一模板的精确版本，值得背下来，也要会现场推。
>
> 推导只有一步。若每层都按 $1-\alpha$ 比 $\alpha$ 分割（$0 < \alpha \le 1/2$），那么沿"较小那一侧"往下走，规模每层乘 $\alpha$，从 $n$ 衰减到常数需要 $d$ 满足 $\alpha^{d} n = 1$，即 $d = \log_{1/\alpha} n = -\lg n / \lg \alpha$ 层，这是最浅的叶子；沿"较大那一侧"往下走，规模每层乘 $1-\alpha$，得 $d = -\lg n / \lg(1-\alpha)$ 层，这是最深的叶子。
>
> 符号不用担心：$0 < \alpha < 1$ 时 $\lg \alpha < 0$，所以 $-\lg n / \lg \alpha$ 是正数；$\alpha = 1/2$ 时两式相等，都等于 $\lg n$，正是完美对半分。
>
> 代数字。$\alpha = 1/10$、$n = 10^{9}$：最浅 $\log_{10} 10^{9} = 9$ 层，最深 $\log_{10/9} 10^{9} \approx 196.7$ 层。$\alpha = 1/100$：最浅 $4.5$ 层，最深约 $2062$ 层——小侧衰减越快，最浅叶越浅，但大侧几乎没变，最深受制于 $1-\alpha \approx 1$。$\alpha = 1/2$ 时两式都是 $29.9$ 层。
>
> 这对公式的读法：最深叶由大侧比例决定，它控制总深度，也就是总代价；最浅叶由小侧比例决定，它决定"最先落位"的那些元素何时逃出递归。两个深度相差 $\log_{1/lpha} / \log_{1/(1-lpha)}$ 倍，$lpha$ 越小时差距越悬殊——$1/100$ 时相差四百多倍。
>
> 做一次极限自查，确认公式在边界处不说谎。$\alpha \to 0$ 时 $\lg(1-\alpha) \to 0$，最深深度趋于无穷，公式精确复现了"退化成链"的最坏情况；$\alpha = 1/2$ 时两式合一为 $\lg n$，回到最好的平衡情形。渐近式在两端都对，说明它抓对了机制。
>
> 与 7.2.2 节的呼应：那里 9 比 1 的分割对应 $\alpha = 1/10$、$1-\alpha = 9/10$，最深深度正是 $\log_{10/9} n$，两处完全一致，只是那里用了具体数值、这里给出一族公式。
>
> 跨课程连接：排序的 decision tree（决策树）下界给出另一个"必须有 $\lg$ 那么深"的理由——$n$ 个元素的可能次序有 $n!$ 种，任何基于比较的算法都要有至少 $\lg(n!) \approx n \lg n - 1.44 n$ 个叶子，树深因而不小于 $\lg n$ 量级。递归树的"深度乘每层代价"与决策树的"深度"是同一枚硬币的两面：前者算时间，后者证下界。6.042J 的对数换底公式在这里天天要用。
>
> 题目只问深度，但深度与代价只差一个乘数：每层代价不超过 $c n$，于是总代价上界等于最深深度乘以 $c n$，仍是 $O(n \lg n)$。深度公式因此是整套分析的骨架，代价只是给它乘上一个系数。
>
> 有个容易混淆的点：最浅叶的深度不是"排序完成所需的层数"，而是"某个元素最早被确定最终位置时的层数"。快速排序每层恰好让一个主元就位，所以最浅叶对应最早落位的那个元素，它逃得最快。
>
> 把公式反过来用也是一类常考题：已知最深深度为 $d$，问比例能差到什么程度。由 $d = -\lg n / \lg(1-\alpha)$ 解出 $1-\alpha = n^{-1/d}$。取 $n = 10^{9}$、$d = 100$，得 $1-\alpha \approx 0.8128$，即分割不能差于 81 比 19 左右；若把 $d$ 压到 $50$，则要求 $1-\alpha \approx 0.66$，即 66 比 34。
>
> 最小规模的一致性检查：$n = 2$ 时两式都给出 $1$，因为只剩一层递归；$n = 3$ 且 $\alpha = 1/3$ 时最浅 $1$、最深 $2$，手画递归树也对得上。
>
> 最后一处实现层面的对应：把尾递归消掉、只对较小一侧递归之后，栈深上界就等于最浅叶深度；所以这两个公式同时也回答了"栈会不会溢出"——它给的是最坏情况下的递归层数，而不是平均值。
>
> 收束：比例常数只改对数的底，改不了对数的量级；这条结论将在 7.4.2 节以"期望意义下每层甩掉常数比例"的面貌回归。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 随机化的落脚点小得惊人：`RANDOMIZED-PARTITION` 只是在划分之前多做两件事——在 $A[p..r]$ 里均匀随机取一个下标，把它与 $A[r]$ 交换，然后照旧调用 `PARTITION`。整个算法的其余部分一个字都没改。
>
> 机制上要看清"随机的是谁"。原版里主元由数据决定（固定取最右元素），随机化后主元由随机数发生器决定，与数据的排列无关。于是"存在一个固定数组让算法必然退化"这件事不再可能：任何具体的输入都可能被抽到好主元，也都可能被抽到坏主元。
>
> 为什么这一点足够？因为 7.4 节的期望分析只需要一条性质：对任意固定的输入，集合 $Z_{ij}$（值介于第 $i$ 小与第 $j$ 小之间的那些元素）中"第一个被选为主元的是谁"是均匀分布的。随机选下标恰好保证了这条——每个位置被先选中的机会相同，与它在数组里原本排第几无关。
>
> 代价可以精确记账。每次划分多一次随机数抽取与一次交换，二者都是常数代价；划分恰被调用 $n$ 次（每层确定一个主元的最终位置），所以总共抽 $n$ 次随机数。$n = 10^{6}$ 时是 $10^{6}$ 次抽取、每次几纳秒，相对 $2 \times 10^{7}$ 次比较可以忽略。
>
> 最坏情况并没有消失。若每次都恰好抽到最大或最小元素，递归仍退化成链，最坏时间仍是 $\Theta(n^{2})$。但这条路径要求连续 $n$ 次都抽到两端的极端位置，概率约为 $2^{n-1}/n!$：$n = 20$ 时是 $2.2 \times 10^{-13}$，$n = 100$ 时小到无法书写。
>
> 这就把"确定性缺陷"换成了"概率极小的事故"，性质上完全不同。术语上这叫 Las Vegas algorithm（拉斯维加斯算法）：输出永远正确，运行时间随机；与之对照的是 Monte Carlo algorithm（蒙特卡罗算法），时间确定但输出可能错。快速排序属于前者——它从不出错，只是有时慢。
>
> 与 5.3 节的随机化雇用助手是同一个策略：把性能 guarantee（保证）从"对输入"搬到"对随机数"。区别在于雇用问题里随机性是现实自带的（候选人顺序），这里是我们主动注入的，代价只是一次 `RANDOM` 调用。
>
> 工程上还有两个细节。随机数发生器要够快：每次都调系统熵源会让随机化本身变成瓶颈，实用实现用 xorshift（移位异或发生器）或 PCG（置换同余发生器）这类廉价发生器；另一个是种子——固定种子便于复现与调试，但那等于把随机化换成确定的伪随机序列，理论上又可能出现被针对的输入，所以只应出现在测试环境。
>
> 跨课程连接：数学侧用全期望公式，$\mathrm{E}[T] = \sum_{q} \Pr{\text{切在} q} \cdot (\mathrm{E}[T(q)] + \mathrm{E}[T(n-q-1)] + c n)$，其中概率来自主元的均匀性；6.042J 的条件期望与全期望公式是它的直接工具。系统侧的对照是 CSAPP 里"用随机化抵御最坏输入"的思路（例如哈希表加随机种子防碰撞攻击），两者都在把对手的攻击面从数据挪到概率上。
>
> 收束：随机化版本的算法本身仍然可能 $\Theta(n^{2})$，但它不再有"专为它准备的输入"；下一节要证的正是它的期望运行时间为 $\Theta(n \lg n)$。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 递归式 (7.1) 里的 $\max$ 是"内建对手"的记号：我们不预设任何具体输入，而是想象一个 adversary（对手）在每一层递归替我们挑出最能拖慢算法的划分点 $q$，最坏情况就是这场博弈的估值。
>
> 把量词摆清楚是理解一切的关键。最坏情况时间可以写成对输入的取上确界：$T(n) = \sup_{x} T(x)$；而划分点 $q$ 完全由输入决定，能取到 $0$ 到 $n-1$ 的任何值，所以对输入的 $\sup$ 就化成对 $q$ 的 $\max$，于是有 $T(n) = \max_{0 \le q \le n-1}(T(q) + T(n-q-1)) + \Theta(n)$。
>
> 随机化算法之所以分析期望而非最坏，是因为量词次序变了。期望写出来是"对每个固定输入，先对随机数取期望"：$\sup_{x} \mathrm{E}_{\text{随机数}}[T(x)]$；而最坏随机化分析要的是"存在一条倒霉随机序列"，即 $\mathrm{E}$ 之外的 $\exists$。前者的承诺强得多——没有任何输入能让算法平均变慢。
>
> 这两个量词不能交换，换了结论就错。一个直观类比：$\forall$ 输入 $\exists$ 好主元 与 $\exists$ 主元 $\forall$ 输入 是两件事。分析里最常见的错误就是在期望式子里偷偷把"对随机数求平均"换成"对输入求最坏"。
>
> 用这个递归式做上界很直接：猜 $T(n) \le c n^{2}$，代入得 $T(n) \le c \cdot \max_{q}(q^{2} + (n-q-1)^{2}) + \Theta(n)$，而括号里的表达式最大不过 $(n-1)^{2} = n^{2} - 2n + 1$；于是 $T(n) \le c n^{2} - c(2n-1) + \Theta(n) \le c n^{2}$，只要 $c$ 取够大让 $c(2n-1)$ 压住 $\Theta(n)$。这就是下一注要收的尾。
>
> 顺带解决 Exercise 7.3-2 的疑惑：`RANDOM` 被调用的次数在最好与最坏情况下都是 $\Theta(n)$。因为每次 `PARTITION` 恰好掷一次骰子，而 `PARTITION` 的调用次数至多 $n$ 次——每调用一次就有一个元素被固定到最终位置，递归不会重复处理它。运气好坏体现在"掷出的点数"上，不在"掷的次数"上。
>
> 拿个数字对比"最坏"与"平均"差多少：均匀随机的划分点给出 $\Theta(n \lg n)$ 的期望，退化划分给出 $\Theta(n^{2})$ 的最坏，比值约为 $n/(2.8 \lg n)$。$n = 10^{6}$ 时约 $25000$ 倍——这就是为什么必须把最坏情况单独拿出来处理，而不是说"通常很快"。
>
> 跨课程连接：这套"算法选策略、对手选输入"的结构就是 minimax（极小极大）思想，与博弈论里的估值同型；数学上的工具则是 6.042J 反复强调的量词顺序。写证明时把 $\forall$ 与 $\exists$ 的位置先标出来，比事后检查一步吐槽要省事得多。
>
> 还有一个更细的观察：$\max$ 与"取平均"的选择，就是"最坏"与"平均"的分野。若把式中的 $\max$ 换成对 $q$ 取均匀平均（每个 $q$ 概率 $1/n$），得到的解是 $\Theta(n \lg n)$；两式只差一个符号，结论差一个 $n / \lg n$ 的因子。分析时用错符号，结果是灾难性的。
>
> Exercise 7.4-3 要你验证 $q^{2} + (n-q-1)^{2}$ 在端点取最大：对 $q$ 求二阶导得常数 $4 > 0$，函数是凸的，而凸函数在闭区间上的最大值必在端点。下一注会给出更快的代数证明，两条路线互相印证。
>
> 工程上的对应：真实实现不会去解这个递归式，而是直接压测。但最坏情况的存在意味着压力测试必须包含"已排序、完全逆序、所有元素相等"三类输入，否则测出来的常数只反映了随机分布下的行为。
>
> 收束：$\max$ 是"最坏情况"的形式化，它把"哪个输入最糟"这个问题变成一个可以代数的极值问题；下一小节把 $\max$ 放缩到端点值，就完成了 $O(n^{2})$ 的代换法证明。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页藏着一个值得命名的论证模板，可称为「凸性端点极大化」：在"两端之和固定"的约束下，平方和这类凸函数在端点取最大、在等分点取最小。以后凡是遇到"总和固定、比较平方和"的场合，先把这个恒等式写出来。
>
> 代数一眼看穿。令两端为 $a$ 与 $b$，则 $a^{2} + b^{2} = (a+b)^{2} - 2ab$。固定和 $a+b = s$ 时，$a^{2} + b^{2}$ 随 $ab$ 反向变化；而 $ab$ 在 $a = b$ 处取最大、在端点处趋零。于是平方和在 $a = b$ 处最小、在端点处最大。在本节的约束里 $a+b = n-1$，所以最大值是 $(n-1)^{2}$，最小值是 $(n-1)^{2}/2$。
>
> 这条结论不依赖具体数值。$n = 100$ 时，端点给出 $99^{2} = 9801$，中点给出 $2 \times 49.5^{2} = 4900.5$，恰好是前者的一半。也就是说平衡划分的平方代价只有极端划分的一半——这正是"分得越均匀，代换法的界越紧"的代数根源。
>
> 微积分版本是 Exercise 7.4-3 的路线：把表达式看成 $q$ 的函数，求二阶导得常数 $4 > 0$，于是它是 convex（凸）的；凸函数在闭区间上的最大值必落在端点。两条路线互为印证，但恒等式法更快也更透明——它直接告诉你极值的比值，而不是只说"在端点"。
>
> 证明的收尾手法在这里。代入上界 $T(n) \le c(n-1)^{2} + \Theta(n) = c n^{2} - c(2n-1) + \Theta(n)$；只要 $c(2n-1)$ 能压住 $\Theta(n)$ 那一项的常数 $d$，即 $c \ge d$ 左右，就有 $T(n) \le c n^{2}$。这就是 substitution method（代换法）里的"常数吸收"标准动作，与 4.3 节的做法完全一致：先猜一个带待定常数的界，再靠"减去的那一项足够大"把低阶项吃掉。
>
> 下一步是另一半：Exercise 7.4-1 要求证明 $T(n) = \Omega(n^{2})$，思路是构造一条具体的坏输入（已排序）走到底，或用代入法猜 $T(n) \ge c' n^{2}$。上下界合起来才是 $\Theta(n^{2})$。只证上界就说"最坏是平方"是不完整的。
>
> 为什么"平衡最快、极端最慢"能直接从凸性读出来？因为划分的代价是 $\Theta(n)$ 均匀分摊到每一层，而层数由最慢的那条路径决定；平方和衡量的是"两个子问题规模的不均衡程度"，不均衡度越大，最深路径越长，层数越多。凸性把这个直觉变成了可以计算的极值问题。
>
> 跨课程连接：几何图像在 Strang 的线性代数里。把 $(q, n-q-1)$ 看成平面上的向量 $v$，目标函数就是 $v^{T} v$，约束是一条直线 $\mathbf{1}^{T} v = n-1$；在这个约束下最小化范数得到"投影到直线上"的那一点，也就是均分点，最大化则跑到直线的两个端点。更高一层的普遍事实是：凸函数在紧凸集上的极值出现在极点，这是线性规划与凸分析的基本定理，而这里的一维线段只是最简单的情形。
>
> 不等式版本也顺手可得：$(a+b)^{2}/2 \le a^{2} + b^{2}$，等号仅在 $a = b$ 时成立。这条与均值不等式同族，本质都是"凸性 + 固定和"。把它与前一句的几何图像并排看，同一个事实有三种语言：代数恒等式、微积分凸性、几何投影。
>
> 这个极值同时解释了"快排最坏必在极端"：平方代价天然惩罚不均衡，所以 $q$ 越靠端点，代换法给出的上界越松，真实代价越大——两者说的是同一件事的两面。
>
> 收束：看到"固定总和、比较平方和"，先写 $(a+b)^{2} - 2ab$，极值立刻现形；这条模板在分析最坏情况、估计方差、设计损失函数时都会反复出现。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 全章期望分析能成立，枢纽是一句话：每一对元素至多被比较一次。这句话为什么成立，要看 `PARTITION` 的结构——某个元素要么被选为主元（一经定序、永久退场），要么与主元比较之后被分到某一侧，此后与另一侧的元素再也不会见面。
>
> 把"永不再见"说清：一次划分之后，左子数组的所有元素都不大于主元，右子数组的所有元素都大于主元；两个不同子数组里的元素在后续递归中属于互不相交的子问题，不会再被放进同一个 `PARTITION`。所以只要一对元素被分开过一次，它们的比较历史就永久结束了。
>
> 于是比较次数 $X$ 不必逐次调用去追踪，可以按"元素对"全局记账：$X = \sum_{i<j} X_{ij}$，其中 $X_{ij}$ 是指示器随机变量，表示"第 $i$ 小与第 $j$ 小的元素是否被比较过"。这一步是把记账维度从"调用"换成"配对"——数量相同，但可加性变好了。
>
> 量纲感受一下：$n$ 个元素共有 $n(n-1)/2$ 对，$n = 1000$ 时是 $499500$ 个指示器；而实际的期望比较次数只有约 $10986$（下一注算），平均每个指示器的期望不到 $0.022$。也就是说绝大多数元素对根本不会被比较——这也解释了为什么快速排序的比较次数远少于"每对都比一次"。
>
> 关键是期望的线性性：$\mathrm{E}[X] = \sum_{i<j} \mathrm{E}[X_{ij}] = \sum_{i<j} \Pr\{ z_i \text{与} z_j \text{被比较} \}$。这一步不需要任何独立性假设，对任意的联合分布都成立——这正是它好用的原因。若换成需要独立性的公式，就得算 $n(n-1)/2$ 个事件的交集概率，那条路走不通。
>
> 把"不需要独立"再强调一次，因为这是初学者最容易误解的地方：$\mathrm{E}[A+B] = \mathrm{E}[A] + \mathrm{E}[B]$ 是无条件成立的恒等式，与 $A$、$B$ 是否相关无关。相关的信息全部被吞进了各自的边际概率里，代价是每个概率都要单独算——而这里的 $\Pr{\, z_i \text{与} z_j \text{比较} \,}$ 恰好有极简洁的形式。
>
> 跨课程连接：这套"换个维度计数"的手法与组合数学里的 double counting（双重计数）同源——同一个量按行数一次、按列数一次，两种算法必须相等。它也直接继承 5.2 节雇用问题的指示器技巧：那里按候选人记账，这里按元素对记账，共同点是"把复杂事件拆成大量简单事件的求和"。系统层面还有一个类比：性能分析工具统计的是"按事件分类的计数"而不是"逐条指令重放"，同一个道理——选对计数维度，问题就塌缩了。
>
> 再记一个容易读错的记号：$z_i$ 指"第 $i$ 小"的那个元素，不是原数组第 $i$ 个位置上的元素。后面全部按 rank（秩）编号，与物理位置无关——这正是"算法只依赖相对次序"这条事实的记账方式。
>
> 与最坏情况对照能看出这个变量的弹性：最坏情况下 $X$ 会走到 $499500$（每对都比一次），而期望只有约 $10986$，相差约 $45$ 倍。同一个计数变量，在不同输入下可以走满，也可以几乎不走。
>
> 收束：$X = \sum X_{ij}$ 是把"什么时候比较"这个动态问题，变成"哪一对会被比较"这个静态问题的开关；打开它之后，剩下的全部工作就是算一个概率。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (7.3) 是整个期望分析的点睛之笔：它把"两个元素是否被比较"这个全局事件，归结为"$Z_{ij}$ 里第一个被选为主元的是谁"这个局部事件。归约一旦成立，概率就只剩数数。
>
> 先看归约为什么合法。在 $Z_{ij}$ 中的任何元素被选为主元之前，整个集合 $Z_{ij}$ 都还处在同一个划分里——因为它们之间没有别的主元把它们切开。所以"第一个从 $Z_{ij}$ 里被选出的主元"这个概念有定义，而且此时 $Z_{ij}$ 的每个元素都等可能地成为那个第一名。
>
> 再看为什么"第一个"决定一切。若第一个被选中的是某个中间元素 $z_k$（$i < k < j$），那么这一轮划分之后 $z_i$ 落在左子数组、$z_j$ 落在右子数组，二者从此属于互不相交的子问题，永远不会再被比较；若第一个被选中的是 $z_i$ 或 $z_j$ 本身，那么它当主元时必然与另一个比较一次。于是"被比较"与"第一个是两端之一"是同一个事件，不多不少。
>
> 概率立刻可算：$Z_{ij}$ 有 $j-i+1$ 个元素，第一个被选中者是其中任意一个的概率都是 $1/(j-i+1)$；两个端点是互斥事件，概率可以直接相加。
>
> $\Pr\{ z_i \text{与} z_j \text{被比较} \} = \frac{1}{j-i+1} + \frac{1}{j-i+1} = \frac{2}{j-i+1}.$
>
> 这就是式 (7.3)。均匀性来自随机化：主元在当前位置上均匀抽取，所以集合里每个元素"抢到第一"的机会相同，与它在数组中原本排第几无关。
>
> 做两个端点自检，确认公式没算错。相邻秩 $j = i+1$ 时概率是 $2/2 = 1$——相邻的两个元素一定被比较过，这条结论可以独立验证：它们之间没有任何元素能先把它们分开。最远的一对 $j-i+1 = n$ 时概率是 $2/n$，与"两端之一恰是全局第一个主元"的概率一致。
>
> 这两个自检比公式本身更有用：它们说明比较概率随秩距离单调下降，且下降速度是 $1/$距离。距离为 $d$ 的一对，比较概率约 $2/d$；所以每个元素只与近邻频繁比较，与远处的元素几乎从不照面——这正是"快速排序的比较次数远少于每对都比一次"的定量说法。
>
> 有个常见的错误直觉要纠正：以为比较概率取决于两个元素在数组里相隔多远。其实它与物理距离无关，只与 rank（秩）距离有关，因为划分是按值分侧、不是按位置。把数组随机打乱，任何一对的比较概率都不变。
>
> 跨课程连接：这套推理是"对称性加首次命中"的标准套路，6.042J 的条件概率与全概率公式就够用——把"第一个主元是谁"当作划分样本空间的方式，再在每个格子里算条件概率。它与抽签公平的论证同型：无论抽签顺序如何，每个人抽中的概率都是 $1/n$，因为对称性没有被破坏。
>
> 分母里那个加一常被漏掉：$Z_{ij}$ 包含两端共 $j-i+1$ 个元素；漏掉会写成 $2/(j-i)$，相邻时算出 $2$，与"概率不可能超过 $1$"当场矛盾，这个自检很灵。
>
> 收束：下一页把这个概率代回式 (7.2)，只需一步变量替换 $k = j-i$，再用调和级数的界，就能收出 $O(n \lg n)$。整章的技术含量几乎全部压在这一步归约上。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (7.4) 的三步变换值得逐步拆开，因为它是一个可以复用的"求和标准化"模板：先换元对齐下标，再放宽被加项，最后利用内层和与外层变量无关。
>
> 第一步是变量替换。原式是双重和，内层起点随 $i$ 变化，直接估计很别扭；令 $k = j-i$，$j$ 从 $i+1$ 走到 $n$ 对应 $k$ 从 $1$ 走到 $n-i$，内层变成 $\sum_{k=1}^{n-i} 2/(k+1)$。下标对齐之后，被加项里不再出现 $i$。
>
> 第二步是放宽。把 $2/(k+1)$ 放大成 $2/k$：分母变小、值变大，方向正确，因为我们要的是上界。放大的代价只在 $k = 1$ 那一项：真实值 $1$、放成 $2$，多算了一倍；其余各项相差不到一个因子 $(k+1)/k \le 2$，无关紧要。于是内层不超过 $2 H_{n-i}$。
>
> 第三步是乘外层。内层和满足 $2 H_{n-i} \le 2 H_{n-1}$，已经不依赖 $i$，而外层共有 $n-1$ 项，所以 $\mathrm{E}[X] \le 2(n-1)H_{n-1} = O(n \lg n)$。最后一步用到 $H_{m} = \Theta(\lg m)$，即 Appendix A 的式 (A.7)。三步都没有精细技巧，全部是"把难算的东西换成好算的上界"。
>
> 还有一处隐含前提值得点明：期望与有限求和的交换是合法的，因为指示器只有 $n(n-1)/2$ 个，是有限项之和。若换成无穷级数，交换次序需要额外的收敛条件；这里不需要任何附加假设。
>
> 界松不松是读者最关心的问题。代 $n = 1000$：$H_{999} \approx 7.4855$，界给出 $2 \times 999 \times 7.4855 \approx 14956$；而精确的期望值是 $10986$，界松了约 $1.36$ 倍。松的部分主要来自第二步的放宽与"用 $H_{n-1}$ 替代 $H_{n-i}$"这两处。
>
> 再对照渐近常数：期望的极限是 $2 n \ln n$，换成以 $2$ 为底就是 $2 \ln 2 \cdot n \lg n \approx 1.386 n \lg n$。$n = 1000$ 时精确值 $10986$ 除以 $n \lg n \approx 9966$ 得 $1.102$，比极限常数小——因为在 $n = 1000$ 这个尺度上，低阶项还在往下拽。
>
> 与最坏情况并排：最坏是 $\Theta(n^{2})$，期望是 $\Theta(n \lg n)$，$n = 1000$ 时 $500500$ 对 $10986$，相差约 $46$ 倍。这就是随机化买到的东西——不是把最坏改好，而是让最坏变成极小概率事件。
>
> 下界那一半由 Exercise 7.4-4 补：即使随机化，递归树每一层仍要付 $\Theta(n)$，且最好情况的深度也是 $\Theta(\lg n)$，故期望运行时间是 $\Omega(n \lg n)$。上下界合起来才是 $\Theta(n \lg n)$；正文里直接说"期望运行时间为 $\Theta(n \lg n)$"，指的就是这条双向结论。
>
> 跨课程连接：数学侧用到调和级数的两条基本事实，$H_n = \ln n + \gamma + O(1/n)$（$\gamma \approx 0.5772$ 是欧拉常数）与积分界 $\sum_{k=1}^{n} 1/k \le 1 + \ln n$，后者是 6.042J 里"用积分夹住求和"的原型。意义侧值得与比较排序的下界对比：任何比较排序至少要 $\lg(n!) \approx n \lg n - 1.44 n$ 次比较，而快速排序的期望约 $1.386 n \lg n$，只多出约三成九。它并不最优，但已很接近下界，这才是"实践中最佳选择"的定量含义。
>
> 模板可以推广：这个"换元、放宽、乘出"的三步在别处同样好用——随机化选择算法的期望比较次数、均匀哈希下链表的平均查找长度、随机图的连通分支数，都是先找指示器、再把求和标准化。认出这个骨架，比记住任何单个结论都值钱。
>
> 这里只求上界，因为最终要的是"期望运行时间不超过 $O(n \lg n)$"；若还想要方差或高概率界，第三步之后就不能停，得回到 $X_{ij}$ 的协方差上去算。
>
> 收束：三步变换、一个调和级数、一次双向论证——整章分析在这里闭合。以后写类似的期望分析，照这个骨架走：先找指示器，再算单个概率，最后把求和标准化并放宽。

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

a. Argue that, given an array of size $n$, the probability that any particular element is chosen as the pivot is $1/n$. Use this to define indicator random variables $X_q = I\,\{\text{the }q\text{th smallest element is chosen as the pivot}\}$. What is $\mathrm{E}[X_q]$?

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
