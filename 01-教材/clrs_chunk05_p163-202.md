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
> 这对公式的读法：最深叶由大侧比例决定，它控制总深度，也就是总代价；最浅叶由小侧比例决定，它决定"最先落位"的那些元素何时逃出递归。两个深度相差 $\log_{1/\alpha} / \log_{1/(1-\alpha)}$ 倍，$\alpha$ 越小时差距越悬殊——$1/100$ 时相差四百多倍。
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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 先说这条注要解决的设计问题：HOARE-PARTITION 与本章 Lomuto 版 PARTITION 的差别不在谁更快，而在分区不变式的形状——Lomuto 版有一个主元的最终位置，Hoare 版没有。
>
> Lomuto 版维护三段不变式：A[p..i] 中每个元素都 ≤ 主元值、A[i+1..j-1] 中每个元素都 > 主元值、A[r] 恰好是主元本身；循环结束时把 A[i+1] 与 A[r] 交换，主元便落到最终位置 q，于是 q 既不属于左子问题也不属于右子问题，递归必须在 A[p..q-1] 与 A[q+1..r] 上各做一次。Hoare 版把主元只当一把标尺：令 x = A[p]，i 从 p-1 出发向右、j 从 r+1 出发向左，两个 repeat 循环各自先移动一步再判断，直到 A[j] ≤ x 与 A[i] ≥ x 才停下；当 i < j 就交换这两个站错边的元素，当 i ≥ j 就返回 j。返回值 j 只是左右两块的分界线，主元值本身可能早已被换到右半区，因此它不需要、也无法归位。
>
> 两个 repeat 的写法不是风格问题，而是正确性的一部分：循环体先让 j 减一、i 加一，再检查条件，保证每一轮至少推进一个下标。若改成先判断后移动，当 A[p] 恰好等于 x 时 i 会停在原地，两个指针可能再也不靠近，外层 while 变成死循环；初值取 p-1 与 r+1 也是同一个道理，第一个被检查的位置必须正好是 p 与 r。CLRS 在 Lomuto 版里用哨兵把内层循环的边界判断省掉，思想相同：预先保证某个位置一定能停住，内层就只剩比较与交换。
>
> 为什么这样设计能成立——Problem 7-1 的 b、c、d 三问可以一次答完。循环不变式是 A[p..i] 的每个元素 ≤ x 且 A[j..r] 的每个元素 ≥ x，并且交换前后始终 i < j。初始化时两段都是空的，成立；交换把左侧一个 ≥ x 的元素与右侧一个 ≤ x 的元素对调，两段性质保持。终止时 i ≥ j，于是 A[p..j] 被 A[p..i] 包含、全部 ≤ x，A[j+1..r] 被 A[j..r] 包含、全部 ≥ x，从而左块每个元素 ≤ 右块每个元素，这就是 d 问。越界即 b 问由 A[p] = x 保证：i 最远在 p 处就停，因为 A[p] ≥ x；j 最远也在 p 处就停，因为 A[p] ≤ x；两个下标都出不了 A[p..r]。至于 j < r 即 c 问，来自第一轮：若 A[r] > x 则 j 已 ≤ r-1；若 A[r] ≤ x 则 j = r，此时 i 停在 p < r，i < j 迫使交换继续进行，之后 j 每轮至少再减一，故返回时 j ≤ r-1。
>
> 现在手算一遍。取 A = ⟨13,19,9,5,12,8,7,4,11,2,6,21⟩，p = 1、r = 12、x = 13。第一轮 j 退到 11 停下，因为 A[11] = 6 ≤ 13；i 进到 1 停下，因为 A[1] = 13 ≥ 13；交换得 ⟨6,19,9,5,12,8,7,4,11,2,13,21⟩。第二轮 j 退到 10 停下，A[10] = 2；i 进到 2 停下，A[2] = 19；交换得 ⟨6,2,9,5,12,8,7,4,11,19,13,21⟩。第三轮 j 退到 9 停下，A[9] = 11；i 一路进到 10 才停，A[10] = 19 ≥ 13；此时 i = 10 > j = 9，返回 j = 9。左块 9 个元素最大为 12，右块最小为 13，划分成立，注意 13 本身留在了右块。
>
> 一个诚实的对比：这趟 Hoare 划分做了 14 次比较、2 次交换，而同规模 Lomuto 划分固定做 11 次比较、最多 11 次交换。比较次数并不更少，Hoare 的优势在交换次数与等值元素处理。这直接对应机器代价：CSAPP 第 6 章 的 cache（缓存）以 64 字节 line 为单位搬运，每次交换是两次读加两次写，交换次数少意味着写回流量少；在内存带宽成为瓶颈的排序里，写流量往往比比较次数更贵。
>
> 跨课程连接 6.042J 的归纳法：Hoare 版的正确性证明是标准的三段式——证明初始化成立、证明每一步保持、证明终止时结论成立，与证图论里可达性、证二分搜索区间不变式完全同构。区别在于这里的归纳变量是循环轮数而不是递归深度，所以不需要强归纳，只用普通归纳；而快排整体的正确性才需要对子问题规模做强归纳。
>
> 收束一句：Hoare 版返回的是分界点而非主元位置，读任何先递归左半再递归右半的写法时，边界取 j 与 j+1 而不是 q-1 与 q+1，根源就在这里；median-of-3（三者取中）的价值也只是让 j 更可能落在中间，改变的是常数而不是量级。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题要回答的是一个假设的边界：7.4.2 节的期望分析为什么必须先假定元素互不相同，去掉这条假设后分析要怎么改。
>
> 机制上，退化来自 Lomuto 版 PARTITION 的比较方向。它把 A[j] ≤ x 的元素都往左边搬，而所有元素都等于 x 时这个条件永远成立，于是 i 每一步都自增、每次都在交换，循环结束时 q = r，切出的子问题规模是 0 与 n-1。递推变成 T(n) = T(n-1) + (n-1)，解出 T(n) = n(n-1)/2。更关键的是随机化救不了：随机选主元仍会选到某个等于全部元素的值，划分依旧是 0 与 n-1，期望与最坏同为 Θ(n²)。随机化能打散的是元素互异时的极端次序，打不散值本身的重复。
>
> 算一下量级。n = 10^5 时比较次数是 4,999,950,000，按每秒 10^9 次比较约 5 秒；而同样规模下 2n ln n ≈ 2.3×10^6 次比较约 2.3 毫秒，差两千倍。同时递归深度是 10^5 层，按每帧 48 字节算要 4.8 MB 栈，已经超过 Windows 的默认线程栈，所以全等输入在工程上是既慢又爆栈，这一点回接 Problem 7-4 对栈深的讨论。
>
> PARTITION′ 的改法是把不变式从两段扩成三段：A[p..q-1] 全部小于 x、A[q..t] 全部等于 x、A[t+1..r] 全部大于 x，返回两个下标 q 与 t，递归只在 A[p..q-1] 与 A[t+1..r] 上进行。全等输入时一趟扫描直接得到 q = p、t = r，两个子问题都为空，总代价 Θ(n)。一般输入下它把等于主元的元素一次剔除，重复率越高收益越大；而 Lomuto 版每次都把等值元素留一半在子问题里，重复率高时它们会被反复划分。
>
> 具体实现是三指针扫描，不变式是四个区：A[p..q-1] 小于 x、A[q..t] 等于 x、A[t+1..u-1] 大于 x、A[u..r] 尚未检查。每读一个 A[u]，按它和 x 的大小关系把它换进前三个区之一：等于 x 时只把 u 加一；小于 x 时把它换到 q 处，并把等于区的左端与大于区的左端各右移一格；大于 x 时只把 u 加一。三种情形各摊还 O(1)，整趟仍是 Θ(r-p)，满足题目对 PARTITION′ 的代价要求。
>
> 手算 n = 8 的全等数组：Lomuto 版每层做 k-1 次比较，共 7+6+5+4+3+2+1 = 28 次，交换次数与之同阶；三路版一趟 8 次比较就返回 q = 1、t = 8，两个子问题为空。28 与 8 的差距随 n 拉大：n = 1000 时是 499500 与 1000，比例约 500 倍；n = 10^6 时是两个数量级以上的差距。这就是为什么「元素取值受限或大量重复」的输入上，三路划分不是优化而是必需。
>
> 跨课程连接 6.042J 的等价关系：R = {(a,b) : a = b} 把输入按值分成等价类，三路划分就是一次显式的按等价类分块。区别在于等价关系只告诉你同类，不告诉你类之间谁大，所以算法还要靠小于关系把等价类排好序——这也解释了为什么三路划分需要同时维护三条边界而不是两条，第三条边界承担的是把等价类整体切出来的职责。
>
> 工程上这条思想落到了 Java 的 DualPivotQuicksort 与多数标准库的 introsort：检测到大量重复就切到三路划分或直接转计数排序。收束一句：7.4.2 的假设不是数学洁癖，去掉它要付 Θ(n²) 的代价，而恢复它只需多维护一条边界。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题的价值在于换一种记账单位：7.4.2 节数的是哪些元素对发生了比较，这里数的是每次递归调用的期望代价，两条路线殊途同归。
>
> 先看 (7.5) 怎么变成 (7.6)。由 a 问，第 q 小的元素被选为主元的概率是 1/n，指示器 X_q 的期望也是 1/n。把求和的每一项展开：$\sum_{q=1}^{n}$ (T(q-1) + T(n-q)) 中，每个 T(k) 恰好出现两次——一次在 q = k+1 处作为 T(q-1)，一次在 q = n-k 处作为 T(n-q)；k = 0 与 k = 1 的项为 0，于是这一和等于 2·$\sum_{q=2}^{n-1}$ T(q)。再除以 n 得 (2/n)·$\sum_{q=2}^{n-1}$ E[T(q)]，而两个边界 q = 1、q = n 只贡献空子问题，与 Θ(n) 的划分代价合并进 Θ(n) 项，这就是 (7.6)。
>
> 为什么 X_q 的期望是 1/n：RANDOMIZED-PARTITION 是从 r-p+1 个下标里均匀抽一个，每个元素被抽中的概率相同，与它的值多大无关。这一点值得停一下：它说明随机化作用在位置上，而不是作用在值的分布上，所以后面的期望只依赖排列的均匀性，不需要对输入分布做任何假设——这正是 5.4 节 randomized algorithm（随机化算法）的标准套路。
>
> 为什么不能拿主方法直接解 (7.6)：它右边拖着 T(2)、T(3)、一直到 T(n-1) 的全部历史项，属于全历史递推，而主方法只认常数个同规模子问题。正确工具是代入法：猜 E[T(n)] ≤ a·n·lg n，回代后右边出现 (2/n)·Σ a·q·lg q，用 (7.7) 把那个求和压到 (1/2)·n²·lg n 减去 n²/8 的量级，再配平常数 a 即可。
>
> 把 (7.5) 再展开一层可以看清常数：设 E[T(k)] ≈ a·k·ln k，把求和换成积分 ∫_0^n a·x·ln x dx，值为 a·(n²·ln n / 2 - n²/4)；乘上前面的 2/n 得 a·n·ln n - a·n/2。要它与左边的 a·n·ln n 配平，必须有 -a·n/2 + c·n = 0，即 a = 2c。取 c = 1 得 E[T(n)] ≈ 2n·ln n ≈ 2.885·n·lg n，这正是 7.4.2 节 2(n+1)H_n - 4n 在同一个量级上的另一种写法，两个系数并不矛盾，只是记账对象不同：一个记比较，一个记调用。
>
> 可算的核对：用程序递推 (7.6)，把 Θ(n) 项取成 n，得 E[T(1000)]/(1000·lg 1000) ≈ 1.169，n = 2000 时是 1.188，说明常数 a 很小而且在缓慢收敛。同时验 (7.7)：n = 1024 时左边 Σ k·lg k = 4,859,567，右边 5,111,808，比值 0.9507；n = 16 时比值 0.809。界成立，但对小 n 偏松，这正是提示要求按 n/2 拆成两段分别放缩的结果——拆得越细，界越紧。
>
> 跨课程连接 6.042J 的求和放缩：把 $\sum_{k=2}^{n-1}$ k·lg k 在 k = ⌈n/2⌉ 处切成两段，前半段用 lg k ≤ lg(n/2) = lg n - 1 放大，后半段用 k ≤ n 放大，两步都只用到单调性。这与证调和级数 Θ(log n) 时用积分比较的手法同源：区别在于那里关心一条曲线的面积，这里关心按大小把求和项分档——同一套放缩技术在不同尺度上的应用。
>
> 还有一个容易被跳过的细节：为什么 (7.5) 里那笔划分代价可以写成与 X_q 无关的 Θ(n)。原因是每次调用 PARTITION 都恰好做 r-p 次比较，与选中的是哪个元素无关——主元只影响子问题的规模，不影响本层的扫描代价。正因为这一项对每个 q 都相同，取期望时它原样留在外面，成为 (7.6) 末尾的 Θ(n)；若划分代价依赖主元，期望就要对 X_q 再做一次加权，式子立刻复杂一层，代入法也就不再干净。
>
> 收束：(7.6) 这种按子问题规模求和的形态，比 7.4.2 的元素对求和更容易推广。子问题个数从两个变成三个时，元素对论证要整段重写，而规模求和只需改系数，这也是三路划分的分析能沿用同一条路的原因；同一条路还直接通向第 9 章 quickselect 的期望线性时间证明。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Problem 7-4 的问题是：递归版 quicksort 的栈深由什么决定，尾递归能把最坏栈深改到多少。
>
> 先算清楚一次调用占多少栈空间。按书里的假设，数组参数以指针传递，所以每层栈帧只占常量空间：返回地址、两三个参数、被调用者保存的寄存器与局部变量。栈帧在调用时压入、返回时弹出，栈深就是任意时刻同时活着的帧数。原始 QUICKSORT 有两次递归调用，先排左半再排右半；第二次调用返回之后函数立刻返回、什么都不做，这就是 tail call（尾调用）。把它的参数改写成 p = q+1 并放回 while 循环，就省掉一层帧，这正是 TAIL-RECURSIVE-QUICKSORT 第 4、5 行的来历。
>
> 要看清它省掉的只是第二次调用，第一次调用照样压栈。所以 b 问的答案很直接：只要每层的左子问题都很大，递归就像一条长链往下叠。构造这种输入不难——把数组按严格递减排好，Lomuto 版每次取 A[r] 作主元，而递减数组的 A[r] 恰好是当前子数组的最小值，划分结果是左半 n-1 个元素、右半 0 个，于是第 4 行每层都递归在规模 n-1 的子数组上，栈深为 n。反过来，若输入递增，左半为空、右半 n-1，第 4 行递归规模为 0、第 5 行的循环接管其余部分，栈深只有 1。同一个算法对两种几乎对称的输入给出完全不同的栈深，这就是为什么最坏情况必须单独分析。
>
> 算一下具体数字：n = 10^6 时最坏栈深 10^6 帧，每帧按 48 字节估（64 位下返回地址 8 字节、两个参数 16 字节、保存的寄存器与对齐填充约 24 字节），合计约 48 MB。Windows 上主线程默认栈 8 MB、新建线程默认 1 MB，按 1 MB 算只能承受约 21845 帧，也就是 n 超过两万就会撞上保护页并触发 stack overflow（栈溢出）。改成 c 问的写法后，栈深是 20 帧，约 1 KB，因为 lg 10^6 ≈ 19.93。
>
> c 问的修复为什么有效：每轮先比较两个子问题的规模，把小的那个交给递归、大的那个交给迭代，即把 p 或 r 更新成新的边界。于是下一次递归的参数规模不超过当前的一半，深度不超过 lg n；同时划分的总次数没有变，递归树还是那棵树，只是遍历次序改了，期望运行时间仍是 Θ(n lg n)。关键不是少递归一次，而是递归的永远是小的那一半。
>
> 跨课程连接 CSAPP 第 3 章 的栈帧与第 9 章 的虚拟内存：栈向低地址增长，每次 call 把返回地址压栈并调整栈指针，越界会撞上操作系统放在栈底的保护页，进程收到 SIGSEGV 而不是优雅失败。gcc 在 -O2 下会做尾调用优化，把真正的尾调用编译成 jmp；但先处理小的一半这条改写编译器做不到，因为它需要比较两个候选子问题的规模，属于算法层决策，不是调用约定层能推断的信息。
>
> 收束一句：tail recursion（尾递归）只把常数降下来，真正把最坏栈深从 Θ(n) 压到 Θ(lg n) 的是小的递归、大的迭代，这条改写与手写显式栈本质上是同一件事的两种写法。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Problem 7-5 与 Problem 7-6 是两条不同的改进路线：一条改主元的选择方式，一条改问题的划分方式。
>
> 先看 median-of-3（三者取中）的概率分布。从 n 个元素里随机取三个不同下标，按值排序后取中间那个作主元。若要主元恰好是第 i 小的元素 A′[i]，另两个元素必须一个取自比它小的 i-1 个、一个取自比它大的 n-i 个，共 (i-1)(n-i) 种搭配。三元组的总数是 C(n,3) = n(n-1)(n-2)/6，于是 p_i = 6(i-1)(n-i) / [n(n-1)(n-2)]，且 p_1 = p_n = 0：三元组的中位数不可能取到最小或最大元素。
>
> 自己验一遍归一化：令 k = i-1，求和变成 $\sum_{k=1}^{n-2}$ k(n-1-k) = (n-1)·Σk - Σk²，代入 Σk = (n-2)(n-1)/2 与 Σk² = (n-2)(n-1)(2n-3)/6，得 (n-2)(n-1)n/6，再乘 6/[n(n-1)(n-2)] 恰为 1。数值上也一致：n = 10^6 时把 p_i 全部加起来仍是 1，误差在双精度舍入范围内。
>
> b、c 两问的数字：n = 10 时 p 序列是 0.0667、0.1167、0.15、0.1667、0.1667、0.15、0.1167、0.0667，而均匀随机是 1/n = 0.1，中间元素被选中的概率涨到 1.667 倍；n 趋于无穷时这个比值趋于 3/2，因为 p_i 近似为 6x(1-x)/n，x = i/n，在 x = 1/2 处取值 1.5/n。好分割的概率是 Σ p_i 在 n/3 与 2n/3 之间的部分：n = 3000 的数值求和给 0.4821，连续近似 ∫ 6x(1-x) dx 在 [1/3, 2/3] 上等于 39/81 ≈ 0.4815，而均匀随机只有 1/3，提高约 44%。
>
> d 问的要点是这些改善只作用在常数因子上：比较排序的下界由决策树的叶子数决定，第 8 章会证明它，而主元怎么挑都改变不了 n! 这个叶子规模，只能把坏分割的概率压低、把期望比较次数的系数从约 1.39 拉下来。把 median-of-3 看成一次采样估计中位数，它用三次比较换来更集中的划分，是典型的用常数换分布。
>
> Problem 7-6 走得更远：它把相等的概念从值推广到区间。若一个区间的左端点不大于某个值 x、右端点不小于 x，则它与 x 相交，这一族区间的先后可以任意排（取所有 c_j = x 就能满足单调要求），于是它们天然构成三路划分的中间一块。算法骨架仍是 quicksort：随机挑一个区间、取它的某个端点作 x，把区间分成完全在左、与 x 相交、完全在右三族，只对左右两族递归。交叠越多中间那块越大、递归越浅，全部交叠时一趟 Θ(n) 结束，而且不需要显式检测这种情形。
>
> 从估计的角度看，median-of-3 是用样本中位数估计真实中位数：样本量 3 时估计的方差已明显小于单个随机样本，把主元落在中间三分之一的概率从 1/3 抬到 0.48；继续加大样本量的边际收益迅速递减——取 5 个数求中位数，选出中位数本身的代价就从 3 次比较涨到 6 次（这是已知的下界），而好分割概率只再涨几个百分点，所以主流实现停在 3，或者干脆放弃采样、改用均匀随机。这是采样精度与采样代价之间的权衡，不是数学上的最优问题。
>
> 跨课程连接 6.042J 的组合计数：p_i 的推导只用从两组元素各选一个的乘法原理，与证二项式系数恒等式是同一套工具；区别在于分母是 C(n,3) 而不是 2^n，因为三元组不关心顺序。收束：median-of-3 改的是选谁，fuzzy sort 改的是什么叫相等，后者对问题结构的利用更深一层。

---

> <span style="color:#7f8c8d;">CLRS Notes for Chapter 7, p.190</span>

## Chapter notes（第 7 章注释） <span style="color:#2471a3;">**[reference]**</span>

> <span style="color:#7f8c8d;">[note] 按规范，本章 notes（注释/参考文献）保留英文原文，不作翻译；文中受损的数学记号已按原书恢复。</span>

The quicksort procedure was invented by Hoare [170]; Hoare's version appears in Problem 7-1. The PARTITION procedure given in Section 7.1 is due to N. Lomuto. The analysis in Section 7.4 is due to Avrim Blum. Sedgewick [305] and Bentley [43] provide a good reference on the details of implementation and how they matter.

McIlroy [248] showed how to engineer a "killer adversary" that produces an array on which virtually any implementation of quicksort takes $\Theta(n^2)$ time. If the implementation is randomized, the adversary produces the array after seeing the random choices of the quicksort algorithm.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这两段 notes 是第 7 章的史实与工程索引，值得把每一句还原成当时要解决的具体问题。
>
> Hoare 的原始论文是 Quicksort，发表在 The Computer Journal 5(1):10–16，1962 年，DOI 10.1093/comjnl/5.1.10；本章的 PARTITION 不是他的版本，而是 Lomuto 的。Lomuto 版进教材的通行说法是 Bentley 在 Programming Pearls 里介绍了它、并归功于 Nico Lomuto，CLRS 只写姓氏；Lomuto 本人的原始文献我在公开检索里没有找到，这一条只能标为未能一手核实。7.4 节的期望分析 CLRS 明确归给 Avrim Blum。Sedgewick 的 Implementing Quicksort Programs 发表在 Communications of the ACM 21(10):847–857，1978 年 10 月，主题正是实现细节如何影响性能。
>
> McIlroy 的 A Killer Adversary for Quicksort 发表在 Software—Practice and Experience 29(4):341–344，1999 年。构造比名字更值得看：比较函数不返回两个元素的大小关系，而是根据一个动态维护的候选值当场决定答案，于是输入数组是在排序过程中被喂出来的，而不是事先给定。任何只靠比较获取信息的排序都逃不掉，因为对手可以保证每次划分都切出 1 与 n-2。
>
> 算一下代价差异：n = 10^5 时随机化 quicksort 的期望比较次数是 2n·ln n ≈ 2.30×10^6，最坏是 n²/2 = 5×10^9，差 2171 倍；n = 10^6 时这个比值涨到 18096 倍。对手只需要在 O(n log n) 次比较里做决定就能锁定这种退化，也就是说它的信息成本与正常排序同阶。
>
> 方法论意义在于：随机化保证的是对任何固定输入期望代价小，而对手模型允许输入依赖随机选择，两个前提不同。5.4 节的分析默认输入先于随机选择存在，McIlroy 的构造恰好打破这个顺序。工程上的对策不是更聪明的随机，而是给最坏情况兜底——introsort 在递归深度超过约 2·lg n 时切换到 heapsort，把最坏情况锁在 O(n log n)。
>
> 跨课程连接 CSAPP 第 5 章 的程序优化：对手需要一个带可变状态的比较函数，通常用全局变量实现，这就破坏了比较是纯函数的假设。编译器若把比较函数内联并假设它无副作用，可能把两次相同参数的调用合并成一次，对手随之失效——同一段代码在 -O0 与 -O2 下行为不同，这是优化假设与语言语义冲突的经典例子。
>
> 另一个常被混淆的点：CLRS 正文说 PARTITION 归 N. Lomuto，但很多教材与实现把以最后一个元素为主元、单向扫描的写法笼统称作 Lomuto，而 Bentley 转述的细节与 CLRS 的伪码并不完全一致；引用时应当以伪码为准，而不是凭名字回忆。至于 Sedgewick 那篇论文的具体贡献，它系统比较了划分方案、小数组阈值、三数取中与递归消除四件事对实际耗时的影响，并给出按规模选策略的经验规则——渐近分析管不到这些，但它们决定了同一个 Θ(n lg n) 算法在实际机器上能快几倍。
>
> 再补一句出处层面的提醒：这两段里的 [170]、[305]、[43]、[248] 是 CLRS 自己参考文献表的编号，换版本就会变，检索时应按作者与年份去查，而不是按编号；这也解释了为什么同一篇论文在不同版本里编号不同。
>
> 收束：这段 notes 真正想说的是，quicksort 的性能由算法、实现、输入分布三者共同决定，任何一环的假设被打破，结论都会变。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注做两件事：把第 7 章的骨架收拢，并说清下一章要接什么。
>
> 三大要点。第一是 PARTITION 的循环不变式：Lomuto 版维护 A[p..i] 全部 ≤ 主元、A[i+1..j-1] 全部 > 主元，整段正确性由三段式证明撑起。第二是划分比例决定递推：最好情况 T(n) = 2T(n/2) + Θ(n) 得 Θ(n lg n)，最坏情况 T(n) = T(n-1) + Θ(n) 得 Θ(n²)，而总是 1/10 与 9/10 这种常比例划分仍然是 Θ(n lg n)——递归树每层代价 Θ(n)、深度 Θ(lg n)，比例常数只进入系数。第三是期望分析：随机主元下第 i 小与第 j 小的元素发生比较的概率是 2/(j-i+1)，求和得 2(n+1)H_n - 4n。
>
> 把第三个结论算成数：n = 10^6 时 H_n ≈ 14.39，2(n+1)H_n - 4n ≈ 2.48×10^7 次比较；而 lg(n!) ≈ 1.849×10^7 比特。两个数同阶，说明 quicksort 的期望比较次数离信息论下界只差一个不大的常数，这就是快排常数小的定量版本。
>
> 下一章证明的是另一件事：任何 comparison sort（比较排序）在最坏情况下都要做 Ω(n lg n) 次比较。论证只用到一个计数事实——n 个元素的排列有 n! 种，每次比较只给一个二值答案，所以决策树至少要有 n! 个叶子，高度至少为 lg(n!)。由此 merge sort 与 heapsort 的 O(n lg n) 上界与这个下界吻合，称为渐近最优；quicksort 的期望也是同阶，只是最坏情况没有保证。
>
> 跨课程连接 Cover 的信息论：一次比较最多提供 1 比特信息，要区分 n! 种等可能结果，至少需要 log2(n!) 比特，这与信源编码里平均码长不小于熵是同一个论证的两个化身。区别很关键：信源编码关心平均码长，允许变长码；决策树关心最坏情况树高，约束是每一个叶子都不能太深，所以更强，也因此拿不到 Huffman 编码那种平均意义下的最优性。
>
> 再补一个概率论视角：期望比较次数 2(n+1)H_n - 4n 的推导只用指示器与线性性，不需要各元素对之间相互独立，这与 5.4 节生日问题的技巧同源，也说明独立性在期望分析里往往是多余的假设。但若要问集中性，也就是以高概率不超过两倍期望，光有一阶矩不够，还需要二阶矩或 Chernoff 型的偏差界，本章不展开；这正是随机化算法分析从一阶走向二阶的自然分界。
>
> 把三章的线索连起来看更清楚：第 6 章 heapsort 的 O(n lg n) 上界、第 7 章 quicksort 的期望同阶、第 8 章的 Ω(n lg n) 下界，三者合起来说明 n lg n 是比较排序这一模型的天花板；而打破天花板不需要更聪明的算法，只需要换模型。这个"换模型"的思路在后面还会反复出现：散列表换掉比较模型得到平均 O(1) 的查找，位图换掉比较模型得到 O(n) 的集合运算。
>
> 还可以连接 6.042J 的偏序：排序算法做的事是用比较逐步确定输入的线性次序，输入本身是一个全序，算法要输出这个全序；n! 就是 n 个元素上全序的个数，决策树的叶子与之对应。收束：第 7 章讲怎么做，第 8 章讲最多能好到什么程度，两章合起来才是排序问题的完整答案。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本章的论证结构是先立靶子再射箭：先把 comparison sort（比较排序）的能力边界算清楚，再给三条绕开它的路线。
>
> 比较排序的定义要点是信息通道的宽度：给定两个元素，你只能问一个是非问题。书里列的五种测试 $a_i < a_j$、$a_i \le a_j$、$a_i = a_j$、$a_i \ge a_j$、$a_i > a_j$ 看起来是五种操作，实际只携带两档信息——$a_i \le a_j$ 与 $a_i > a_j$。
>
> 在互异假设下 $a_i = a_j$ 永不成立，可以删掉；而小于等于、大于等于、大于、小于之间只差操作数的次序，问 $a_i \ge a_j$ 等价于问 $a_j \le a_i$。所以模型可以简化成每次比较有两个结果，决策树是二叉树而不是五叉树。这一步是整章下界证明的技术前提：如果一次比较能给出三种以上答案，$2^h$ 就得换成 $3^h$，高度的下界会小一些。
>
> 把多给几个答案能省多少算出来：若允许三路比较，每次最多 $\log_2 3 \approx 1.585$ 比特，下界从 $\log_2(n!)$ 变成 $\log_3(n!)$。$n = 10^6$ 时 $\log_2(n!) \approx 1.849\times 10^7$，$\log_3(n!) \approx 1.166\times 10^7$，只降 37%。增加分支数改变不了 $n\lg n$ 这个量级，只能省常数，这也是为什么没人去发明四路比较。
>
> 还有一件容易被忽略的事：决策树模型里比较是唯一被允许的操作，读数组元素的值本身不算操作。这条约定看似技术性，实际很要紧——若允许直接读值，counting sort 就合法了，下界立刻失效。换句话说，$\Omega(n\lg n)$ 是模型的性质，不是排序问题本身的性质。
>
> 把这一点想清楚，后面三节读起来就顺了：counting sort 假设值是 $0$ 到 $k$ 的整数，于是值可以当数组下标，一次读写就定位；radix sort 假设值可以拆成若干位，于是位可以当排序的轮次；bucket sort 假设值落在 $[0,1)$ 且近似均匀，于是区间可以当桶。三个假设一个比一个弱，代价一个比一个大：分别需要 $\Theta(n+k)$ 的额外空间、$d$ 趟全量扫描、以及一个无法在 $O(n)$ 内验证的分布前提。
>
> 代价也要说清：一旦元素可能相等，等号就可能成立，五种测试不再互相等价，简化失效。这正是 Problem 7-2 的处境，也是三路划分存在的理由；counting sort 能突破下界，不是靠加宽通道，而是靠换掉通道。
>
> 跨课程连接 Cover 的信息论：把输入看成 $n!$ 个等可能消息之一，熵就是 $\log_2(n!)$ 比特；一次比较是容量 1 比特的二元信道，所以至少需要 $\log_2(n!)$ 次才能唯一定位消息。这与信源编码定理结构相同，区别在于编码允许变长、允许对高频符号用短码，而排序必须对每个输入都正确，取的是最坏情况。
>
> 还可以连到 CSAPP 第 3 章：x86 的 cmp 只设置条件码，本质是二值；硬件层面没有一次比较多比特的指令，SIMD 的并行比较只是把多个二元比较打包，通道数变多但每次仍是二值。
>
> 最后提醒一句读法：这三节里的线性时间算法都不是比较排序的反例，它们在比较排序的模型之外。把模型边界记清楚，后面的每一处仿佛矛盾的地方都会自动消解。
>
> 收束：绕开 $\Omega(n\lg n)$ 的唯一办法是不做比较——用值当下标、用数字位、用区间，三条路分别在 8.2、8.3、8.4 节。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注处理两个容易踩的坑：full binary tree 的译名，以及决策树为什么必须忠实复刻算法的动态。
>
> 书里的 full binary tree 指每个结点有 0 个或 2 个孩子的二叉树，没有独生子结点；中文教材常把每层都填满的树叫满二叉树，那是 perfect binary tree（完美二叉树），两者不是一回事。区别在计数上很关键：perfect 树的叶子数被高度唯一确定为 $2^h$；full 树只保证内部结点数等于叶子数减一，叶子数可以在 1 到 $2^h$ 之间任意取值。
>
> 决策树为什么必须复刻算法：内部结点标 $i{:}j$ 表示此刻比较 $a_i$ 与 $a_j$，左右子树分别是小于等于与大于之后继续做的比较，叶子标的是此刻已经确定的排列。算法在某个具体输入上的执行，就是从根沿一条路径走到叶子的过程；控制流、数据移动统统被抹掉，只留下比较与分支。
>
> 叶子标注的是排列而不是排序后的数组，这一点也有讲究：排序算法只改变元素的位置、不改变元素集合，把叶子标成排列就等于说输出只取决于相对次序，与具体数值无关。于是决策树只依赖 $n$，不依赖输入里那些数到底是几，同一棵树的结论对整类输入都成立。
>
> 数一数图 8.1 那棵树：高度 3 的二叉树最多 $2^3 = 8$ 个叶子，而 3 个元素有 $3! = 6$ 种排列，$6 \le 8$ 富余两个位置，所以树不必是 perfect 的。反过来 $2^2 = 4 < 6$，高度 2 装不下 6 个排列，故 $h \ge 3$；图 8.1 恰好高 3，达到下界，于是插入排序在 3 个元素上的最坏比较次数就是 3，与表 2.1 给出的 3 一致。
>
> 再看叶子与排列的对应：同一片叶子不能对应两个排列，否则算法走到这里无法区分它们，输出必然错一个；所以每片叶子最多承载一个排列，$n!$ 个排列需要 $n!$ 片可达叶子。可达这个词也不能省：决策树里可以有不可达的空位，比如某两个分支在算法上根本走不到，下界只能用可达叶子的数量。
>
> 图 8.1 的阴影路径值得手跟一遍：输入 $\langle 6, 8, 5 \rangle$，先比 $1{:}2$，$6 \le 8$ 走左；再比 $2{:}3$，$8 > 5$ 走右；最后比 $1{:}3$，$6 > 5$ 走右，落到叶子 $\langle 3,1,2 \rangle$，读作 $a_3 \le a_1 \le a_2$，即 $5 \le 6 \le 8$。三步正好对应插入排序处理第三个元素时做的比较，决策树与算法逐句对应。
>
> 顺带说清一个常见误读：决策树的叶子数不必恰好等于 $n!$。插入排序在 3 个元素上有 6 片叶子、高度 3，而最多可容纳 8 片，富余的两片并不是浪费——它们对应某些输入下多走的比较。下界证明只用叶子数不少于 $n!$，所以富余不影响结论。
>
> 跨课程连接 6.042J 的树计数：那里证明 full binary tree 满足叶子数等于内部结点数加一，用的是对结点数的归纳；这里要的是高度 $h$ 的二叉树叶子不超过 $2^h$，用的是对层数的归纳。同一棵树的两种计数方式回答两个不同问题：前者给守恒关系，后者给高度的指数上界，下界证明要的是后者。
>
> 收束：读懂图的形状之后，下一页那串不等式就只是在把这张图的两个计数事实写成数学。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 定理 8.1 的证明只有三行，但每一步都值得追问一句凭什么。
>
> 第一个不等式 $n! \le l$ 来自正确性要求。若某个排列没有对应的可达叶子，就存在一种输入，算法走到不了任何叶子或者走到别人的叶子，输出必然错；所以可达叶子数 $l$ 至少是 $n!$。这一步把算法语义翻译成了计数。
>
> 第二个不等式 $l \le 2^h$ 是组合事实。高度为 $h$ 的二叉树叶子不超过 $2^h$，对 $h$ 归纳最干净：$h = 0$ 时只有一片叶子，等于 $2^0$；$h+1$ 时根的两个子树高度都不超过 $h$，各自叶子不超过 $2^h$，合起来不超过 $2^{h+1}$。这一步把树的形状翻译成了计数。
>
> 把高度与最坏比较次数等同起来还需要一个小前提：每次比较沿一条边下降一层，所以从根到叶的路径长度就是该次执行做的比较次数；最坏情况取最长路径，即树高。若算法在某些输入上提前终止，那片叶子就在较浅的位置，但这只影响最浅叶子，不影响下界。
>
> 两边取 $\lg$（单调增，方向不变）得 $h \ge \lg(n!)$，再用 equation (3.19) 的 Stirling 界 $\lg(n!) = n\lg n - 1.4427n + O(\lg n) = \Omega(n\lg n)$。三步合起来：任何比较排序的决策树高度都是 $\Omega(n\lg n)$，而高度就是最坏情况比较次数，定理得证。
>
> Stirling 那个常数值得单独记住：$1.4427 = 1/\ln 2$，即从自然对数换到以 2 为底。误差项 $O(\lg n)$ 也不能丢——它决定了下界与 $n\lg n$ 的差是线性还是对数。$n = 10^6$ 时 $1.4427n \approx 1.44\times 10^6$，占 $n\lg n = 1.99\times 10^7$ 的 7.2%，正好解释了为什么实际下界比 $n\lg n$ 小一截。
>
> 代入数字看这个界紧不紧：$n = 10$ 时 $\lg(10!) = 21.79$，故 $h \ge 22$；归并排序的最坏比较数是 $n\lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1 = 40 - 16 + 1 = 25$，与下界差 3。$n = 20$ 时 $\lg(20!) = 61.08$，故 $h \ge 62$，而 $20\lg 20 = 86.4$，比值 0.707；$n = 10^6$ 时比值为 0.928。比值随 $n$ 缓慢升向 1，说明 $n\lg n$ 这个记号在渐近意义上没有浪费，但在有限 $n$ 上确实偏松。
>
> 推论 8.2 把上下界拼起来：heapsort 与 merge sort 的 $O(n\lg n)$ 与这里的 $\Omega(n\lg n)$ 吻合，所以渐近最优。注意最优是就最坏比较次数而言的，不排除某些输入上更快，也不排除换个模型突破；同一个算法在别的机器模型上还可能有完全不同的评价，比如 radix sort 在字长固定的机器上能做到 $\Theta(n)$。
>
> 还有一个细节要澄清：定理说的是比较次数，不是时间。如果比较本身很贵（比如比较两个长字符串），常数因子会变得比比较次数更重要；反过来若比较极便宜，模型就非常贴合实际——这也是为什么下界结论在实践中常常被验证得很准。
>
> 跨课程连接 6.042J 与实分析里的夹逼：这里的手法与上下极限的夹逼同构——用两条不等式把未知量卡在中间，再用已知渐近式确定量级。区别在于这里全是不等式的整数运算，不取极限，所以不需要任何收敛性论证，比实分析里的版本干净得多。
>
> 收束一句：$n! \le l \le 2^h$ 这条链之所以有力，是因为左端来自正确性、右端来自树的形状，两个完全不同的来源被同一棵树联系起来；这也是决策树模型最值得记住的一点。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 三道练习是把定理 8.1 当工具用的三种方式：换估计法、换比例、换问题。
>
> 8.1-2 要求不用 Stirling 而直接估 $\sum_{k=1}^{n}\lg k$。手法是 Appendix A.2 的积分比较：$\lg x$ 单调增，故 $\int_1^n \lg x\,dx \le \sum_{k=1}^n \lg k \le \int_1^{n+1}\lg x\,dx$。下界算出 $n\lg n - 1.4427n + 1.44$，与 Stirling 的主项只差常数项。
>
> 核对精度：$n = 1000$ 时积分下界 8524.5，真值 $\lg(1000!) = 8529.4$，相对误差万分之六；若改用梯形法则加一项端点修正，误差还能再降一个量级。这说明积分估阶在 $n$ 上千时已经够用，也说明为什么教材敢不带 Stirling 就用积分。
>
> 8.1-3 问能不能对一部分输入做到线性，答案比直觉更强：不行。理由是把同一套计数搬到部分输入上。若有 $f\cdot n!$ 个输入能在 $cn$ 次比较内排好，决策树就必须在深度 $cn$ 内放 $f\cdot n!$ 片叶子，于是 $2^{cn} \ge f\cdot n!$，取对数得 $cn \ge \lg(n!) + \lg f$。
>
> 代入三种比例：$f = 1/2$ 时 $\lg f = -1$；$f = 1/n$ 时 $\lg f = -\lg n$；$f = 1/2^n$ 时 $\lg f = -n$。$n = 10^6$ 时 $\lg(n!) = 1.849\times 10^7$，而这三项分别只有 $-1$、$-19.9$、$-10^6$，全被主项吞掉，左端仍要求 $c$ 达到千万量级，不是常数。也就是说，任何占比固定的输入族都不可能线性，指数级小的比例也不行——常数必须随 $\lg n$ 一起长大。
>
> 这个结论的强度值得单独说：定理 8.1 只说最坏输入需要 $\Omega(n\lg n)$，而 8.1-3 说能快速处理的输入占比趋于零，也就是几乎所有输入都慢。下界从最坏情况推到几乎处处，这在算法分析里是更强的命题。
>
> 8.1-4 换问题：输入由 $n/k$ 个长度 $k$ 的块组成，块间已按大小分离，只需块内排序。把 $n!$ 换成 $(k!)^{n/k}$，取对数得 $(n/k)\lg(k!) \ge (n/k)(k\lg k - 1.4427k) = n\lg k - 1.4427n$，于是下界是 $\Omega(n\lg k)$。
>
> 核对数字：$n = 10^6$、$k = 8$ 时 $n\lg k = 3\times 10^6$，而 $(n/k)\lg(k!) = 1.912\times 10^6$。后者更小，是因为 $\lg(8!) = 15.30$ 比 $8\lg 8 - 1.4427\times 8 = 12.46$ 更紧，说明用 Stirling 下界放缩是有代价的，直接算阶乘的对数更准。
>
> 为什么不能简单把各块的下界相加：各块的决策树在真实算法里是同一棵全局树的不同子树，叶子数是 $(k!)^{n/k}$ 而不是每块独立取最坏再相加；提示原文说不严格，正是指这一点。把每块的界加起来得到的是 $n\lg k$ 的量级，恰好对，但推理是错的——结论对不等于论证对。
>
> 三道题还有一个共同的方法论：把下界当成可以搬运的对象。8.1-2 搬的是估计工具（积分换 Stirling），8.1-3 搬的是计数不等式的一边（把 $n!$ 换成 $f\cdot n!$），8.1-4 搬的是结果空间的大小（把 $n!$ 换成 $(k!)^{n/k}$）。搬运时唯一要守的规矩是：新模型的叶子数仍要被 $2^h$ 卡住。
>
> 把三题的答案并排放好便于对照：8.1-2 的结论是 $\Theta(n\lg n)$，下界 $n\lg n - 1.4427n$、上界 $n\lg n + \lg n$；8.1-3 的结论是三种比例都不行，且要求的常数随 $\lg n$ 增长；8.1-4 的结论是 $\Omega(n\lg k)$。形式各异，用的都是叶子数被 $2^h$ 卡住这一条。
>
> 再补一个读法上的提醒：这三题都在回答同一个元问题——下界的证明只需要两样东西，一个"结果空间有多大"的计数，一个"每次操作能排除多少可能"的计数。只要这两样能写出来，夹逼就自动成立，具体是排序、查找还是别的什么问题都无关。
>
> 跨课程连接 6.042J 的计数与积分比较：三道题分别用到乘法原理、对数估计、以及把界套在指数上的手法，都是 6.042J 与 3.2 节已有的工具，没有新数学。收束：下一步进入第一个线性时间算法 counting sort，它的前提不再是只许比较，而是元素是 0 到 k 的整数。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 图 8.2 值得逐格跟踪一遍：counting sort 只有四个循环，每个循环的职责与代价都不同，而稳定性藏在最后一个循环的遍历方向里。
>
> 第一个循环（第 2–3 行）把 C 清零，代价 $\Theta(k)$；第二个（第 4–5 行）扫描 A，对每个 A[j] 把 C[A[j]] 加一，代价 $\Theta(n)$，结束后 C[i] 是值为 i 的元素个数；第三个（第 7–8 行）求前缀和，代价 $\Theta(k)$，结束后 C[i] 是值不超过 i 的元素个数；第四个（第 10–12 行）从后往前扫描 A，把 A[j] 写进 B[C[A[j]]] 再把 C[A[j]] 减一，代价 $\Theta(n)$。合计 $\Theta(n+k)$，全程没有比较两个元素。
>
> 以 A = $\langle 2,5,3,0,2,3,0,3 \rangle$、$k = 5$ 为例。计数后 C = $\langle 2,0,2,3,0,1 \rangle$：0 出现两次、2 出现两次、3 出现三次、5 出现一次。前缀和后 C = $\langle 2,2,4,7,7,8 \rangle$，读作不超过 0 的有 2 个、不超过 2 的有 4 个、不超过 3 的有 7 个、全部 8 个都不超过 5。
>
> 第一次迭代取 $j = 8$，A[8] = 3，C[3] = 7 表示不超过 3 的有 7 个，所以这个 3 该落在第 7 位；写入 B[7] = 3，再把 C[3] 减为 6。接着 $j = 7$，A[7] = 0，C[0] = 2，写入 B[2] = 0，C[0] 变成 1。八次迭代依次写入 B[7]、B[2]、B[6]、B[4]、B[1]、B[5]、B[8]、B[3]，最终 B = $\langle 0,0,2,2,3,3,3,5 \rangle$，排序完成。
>
> 边放边减一的理由：三个 3 分别落在位置 7、6、5，是递减的；而扫描方向是从后往前，所以最后出现的 3 先落位、最先出现的 3 最后落位，输出里三个 3 的相对次序与输入完全一致。稳定性不是巧合，它是遍历方向与减一这两件事合作的结果。
>
> 把第 10 行改成 $j$ 从 1 到 A.length 会怎样：算法仍然正确，每个元素依旧落在它该在的区间里，Exercise 8.2-3 的第一问就是这个；但同值元素的相对次序被翻了过来，稳定性被破坏。这说明稳定性是遍历方向带来的附加性质，与排序正确性是两件事，可以单独丢失。
>
> 跨课程连接 CSAPP 第 6 章：B[C[A[j]]] 是一次按值定位的散乱写，$n = 10^6$ 个四字节整数、64 字节 line，几乎每次写都换一个新 line，写放大极重；而 quicksort 的就地交换在缓存里来回走同一小片区域。这解释了为什么渐近更优的 counting sort 在实际机器上未必更快，8.3 节末尾的工程讨论说的正是这件事。
>
> 再补一个容易漏掉的点：每个元素的目标位置只取决于 C[A[j]] 与它在同值元素中的名次，与输入顺序之外的任何东西无关。所以 counting sort 天然可以分批处理——先统计，再把放位的活分给多个线程，因为位置是预先确定的。这种位置可预先确定的性质，是它比 quicksort 更容易并行化的原因，也是 GPU 上基数排序常用它作内层引擎的理由。
>
> 还有一点术语上的澄清：第 7–8 行的前缀和本质上就是离散的累积分布函数，它把"值等于 i 的个数"变成"值不超过 i 的个数"。这两个量在概率论里分别叫概率质量与累积概率，名字不同、算法相同，看见"前缀和"就该想到"离散积分"。
>
> 最后一个不算小的代价：counting sort 需要能对值取整。若键不是整数，就必须先做一次保序的量化，而量化本身会丢掉信息，排序结果只能在量化后的序上正确。这条限制在下一节会被放大成"每一位也只允许有限个取值"。
>
> 收束：counting sort 的全部技巧就是用值当数组下标，代价是需要一块大小为 k 的工作区；换来的是线性时间，前提是 k 与 n 同阶，而且元素可以当整数索引。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页有三个考点：时间 $\Theta(n+k)$、为什么逃得过下界、稳定性到底有什么用。
>
> 时间：四个循环分别是 $\Theta(k)$、$\Theta(n)$、$\Theta(k)$、$\Theta(n)$，合起来 $\Theta(n+k)$。注意这是精确的界而不是最坏情况的界——counting sort 没有基于数据的分支，任何输入都走同样的路径，所以最坏等于平均，这在线性时间算法里是难得的性质。
>
> 算两个极端：$n = 10^6$、$k = 10^3$ 时总操作约 $1.001\times 10^6$ 次，是线性的；$n = 10^6$、$k = 10^9$（比如要排序 32 位整数）时总操作约 $1.001\times 10^9$ 次，而且 C 数组要 4 GB（每项 4 字节），在 8 GB 机器上会触发交换。所以 $k = O(n)$ 不是修辞，是能不能用的分界线。
>
> 逃得过下界的原因：第 8 章的下界只对 comparison sort（比较排序）成立，前提是只通过比较获取顺序信息。counting sort 从头到尾没有比较两个元素，它做的是把元素的值当数组下标这个映射，本质是直接寻址而不是比较。模型的适用范围被打破，结论自然不适用。
>
> 稳定性有两层用途。表面一层是卫星数据：元素往往带着键之外的负载，同值元素的先后不能随意打乱，否则每次排序都要重排负载。更深一层是 radix sort：它把多趟稳定排序串起来，靠的正是上一趟的相对次序被下一趟保留，没有稳定性整个算法就错。
>
> 举个会翻车的例子：A = $\langle (2,a),(2,b) \rangle$，键相同。正向扫描时先处理 $(2,a)$，写成 B[C[2]]，C[2] 减一；再处理 $(2,b)$，它落到前一个位置，输出变成 $(2,b)$、$(2,a)$，次序反了。反向扫描则恰好相反，保序。
>
> 跨课程连接 CSAPP 第 6 章与第 9 章：k 决定工作集大小。$k = 10^9$ 时 C 数组 4 GB，比 LLC 大三个数量级，每次 C[A[j]] 加一都可能是一次主存访问甚至一次缺页；渐近式里的 $\Theta(k)$ 在常数上被 miss penalty 放大，实测时间会差出好几个数量级。
>
> 再补两个适用边界的例子。若元素是负数，只需先扫一遍求最小值做平移，代价多 $\Theta(n)$；若元素是浮点数但可以按位重新解释成整数，也能做类似处理，只是要额外处理符号位，否则负数会排到正数后面。这类把值映射到非负整数的预处理，是工程实现里绕不过去的一步。
>
> 另一点值得对比：counting sort 的时间与元素分布无关，只要 k 固定；quicksort 的时间依赖分布，最坏会退化。前者的确定性是优点，代价是 $\Theta(k)$ 的空间；后者的空间只要 $O(\lg n)$ 栈，时间却只有期望保证。选哪一种，取决于 k 是否小、以及是否接受随机化。
>
> 最后一个细节：counting sort 的空间是 $\Theta(n+k)$ 而不是 $\Theta(k)$，因为输出数组 B 另需 n 个位置。若强行改成原地版本，可以省掉 B，但稳定性会一并失去——这也是标准实现都选择非原地的原因。
>
> 顺带把三个循环的分工记牢：计数、前缀和、放置。三者顺序不能换，因为前缀和依赖计数，放置依赖前缀和；而放置循环的方向决定稳定性，与正确性无关。记住这个分工，后面 radix 的每一趟就是这三步的重复。
>
> 收束：counting sort 的适用面很窄——整数、范围小、非负——但在这个窄面上它无可替代，因为它是 radix sort 每一趟的引擎。

---

> <span style="color:#7f8c8d;">CLRS §8.2–8.3, p.197</span>

**8.2-4**

Describe an algorithm that, given $n$ integers in the range $0$ to $k$, preprocesses its input and then answers any query about how many of the $n$ integers fall into a range $[a..b]$ in $O(1)$ time. Your algorithm should use $\Theta(n + k)$ preprocessing time.

### Section 8.3 · Radix sort（基数排序） <span style="color:#2471a3;">**[section]**</span>

Radix sort（基数排序）是一种如今只能在计算机博物馆里见到的 card-sorting machine（卡片排序机）所使用的算法。这种卡片有 80 列（columns），机器可以在每列的 12 个位置之一打一个孔。sorter（分拣机）可以被机械地"编程"（"programmed"），以检查一副卡片（deck）中每张卡片的给定列，并根据打孔的位置把卡片分到 12 个箱（bins）之一。操作员随后可以逐箱收集卡片，使得第 1 个位置打孔的卡片叠放在第 2 个位置打孔的卡片之上，依此类推。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 原书这段博物馆式的描述背后有真实的历史人物和一套可以核算的数字。
>
> 卡片制表机出自 Herman Hollerith（1860–1929）。据 Britannica 与常见教学资料，1880 年美国普查的完整制表拖了七年（1887 年才收尾），而 1890 年的人口已达 62,979,766，比 1880 年的 50,189,209 增长 25.5%；当时有人估计按人工办法，1890 年的数据要拖到 1900 年前后才能算完。Hollerith 在 1884 年取得打孔卡制表机专利，1890 年投入使用；他创办的公司 1911 年并入 Computing-Tabulating-Recording Company，1924 年改名 IBM。
>
> 算一下机械化的量级：62,979,766 张卡片，机器按每分钟 60 张计（文献给的范围是每分钟 50 到 80 张），单机 24 小时不停需要 62979766 除以 86400 约等于 729 天；若同时开 100 台，约 7.3 天。把七年压到几个月的算术就在这里——不是算法变聪明了，而是吞吐率与并行度同时上去了。
>
> 为什么硬件形态决定算法形态：分拣机一次只看一列，也就是一个十进制位，所以逐位排序、每趟稳定是机械结构的必然，而不是设计者的偏好。想按高位优先排，就得在每一层维护十个箱子并记住它们的次序，箱子数随位数指数膨胀；按低位优先排，只需要十一个箱子，一趟一趟过即可。
>
> 这张卡片本身也有数据结构上的意义：80 列乘 12 行的固定布局就是定长记录，每列一位数字，等于把字段这个概念物化了。radix sort 里的 d 位数字，正是这 80 列的抽象；一张卡就是一条记录，一列就是一个关键字分量。
>
> 跨课程连接 CSAPP 第 1 章与第 6 章：吞吐率与延迟是两个量。单张卡片处理要几十到上百毫秒，这是延迟；机器可以不停喂卡片，这是吞吐。把 100 台机器并行，墙钟时间近似除以 100，这是理想的线性加速端点；Amdahl 定律提醒的是另一头——只要有串行段（比如人工整理卡片顺序、核对异常卡片），加速就有上限。
>
> 还可以连到 CSAPP 的位图思想：一列上打三个孔就是三位编码，两张卡片对应同一列的不同孔位组合，这就是最早的位并行索引。counting sort 的 C 数组与它是同一思路的现代版本：用位置编码信息，而不是用比较提取信息。
>
> 补一句人物背景：Hollerith 是哥伦比亚大学矿业学院的毕业生，1879 年毕业，随后参与 1880 年普查，正是在那次经历里看清了人工制表的瓶颈。他受列车检票员在车票不同位置打孔以记录乘客特征的启发，把打孔位置当成编码——这个想法比机器本身更重要，因为它把信息与物理位置绑定，读取就退化成检测孔位。
>
> 顺带说清一个常被夸大的说法：1890 年普查并不是一年内全部算完，人口总数这类主要统计量出得快，交叉制表仍需要更长时间；机械化带来的是数量级的改善，而不是瞬间完成。
>
> 收束一句：原书说这机器如今只能在博物馆见到，恰恰提醒我们算法依附的硬件会过时，但它利用键的内部结构绕开比较的思想不会——今天它在内存里以 counting sort 与 radix sort 的面目继续存在。

对于 decimal digits（十进制数字），每列只使用其中的 10 个位置（其余两个位置留给编码非数字字符）。于是一个 $d$-digit number（$d$ 位数字）将占据一个由 $d$ 列组成的 field（字段）。由于卡片分拣机一次只能看一列，按一个 $d$ 位数字对 $n$ 张卡片排序的问题就需要一个 sorting algorithm（排序算法）来解决。

直观上，你可能会按 most significant digit（最高有效位）对数字排序，对得到的各个箱递归地排序，然后按顺序合并各副卡片。遗憾的是，由于在排序每个箱时必须把 10 个箱中 9 个箱的卡片先放到一边，这一过程会产生许多你必须记录在案的中间卡片堆。（见 Exercise 8.3-5。）

Radix sort 解决卡片排序问题的方法——与直觉相反（counterintuitively）——是先按 least significant digit（最低有效位）排序。算法随后把各箱卡片合并成单副卡片：0 号箱中的卡片排在 1 号箱的卡片之前，1 号箱的排在 2 号箱的之前，依此类推。然后它再按次最低有效位对整副卡片重新排序，并以同样的方式重新合并。这一过程一直持续到卡片按全部 $d$ 位数字排完序为止。令人惊叹的是，此时这些卡片已经按这个 $d$ 位数字完全排好序了。因此，只需对卡片做 $d$ 趟（passes）处理即可完成排序。图 8.3 展示了 radix sort 作用于"一副" 7 个 3 位数的过程。

为使 radix sort 正确工作，各位数字上的排序必须是稳定的（stable）。卡片分拣机所执行的排序是稳定的，但操作员必须小心，不要改变卡片从箱中取出时的顺序——即使箱中的所有卡片在所选列上的数字都相同。……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> LSD 为什么必须先低位、每一趟为什么必须稳定，这两件事是同一个归纳的两面。
>
> 不变式：做完第 t 趟（按第 t 低位）之后，序列按最低 t 位有序，且最低 t 位相同的元素保持输入中的相对次序。基线 t = 0 是输入本身；归纳步是：第 t+1 趟按第 t+1 位稳定排序——若两个数第 t+1 位不同，本趟直接把它们排对；若相同，本趟不改变它们的相对次序，而由归纳假设它们已按低 t 位有序，于是整体按低 t+1 位有序。
>
> 稳定性的必要性可以这样看：本趟只按一位排序，它没有能力知道低 t 位的信息；低 t 位的信息完全存放在上一趟留下的次序里。若本趟把次序打乱，信息就丢了，后面多少趟都补不回来。
>
> 举一个会错的例子：两个两位数 15 与 12。按个位排（5 与 2）得 $\langle 12,15 \rangle$；再按十位排，两者十位都是 1，属于持平，若这一趟不稳定，输出可能是 $\langle 15,12 \rangle$，结果错。反过来若十位不同（比如 21 与 12），第二趟按十位就能直接定序，第一趟稳不稳定都无所谓——所以稳定性只在高位持平时才真正起作用，而它必须每一趟都具备，因为你无法预知哪些高位会持平。
>
> 对照 MSD：先按最高位分箱，再对每个箱递归按次高位排。它需要维护的中间堆数是 10 的幂次级别，8.3-5 会算出 d = 4 时最坏要 1111 趟；而 LSD 只需 d 趟，也就是 4 趟。差距来自递归展开：MSD 把一次分箱展开成一棵十叉树，叶子数就是 10 的 d 次方量级。
>
> 跨课程连接 CSAPP 第 6 章：LSD 的每一趟都是一次全量顺序扫描，d 趟就是 d 遍 n 个元素的读写。在内存里这很便宜，顺序访问吃得下预取；但在磁盘上就是 d 倍 I/O，而外部排序的多路归并只需 O(log(n/M)) 趟，所以大数据集上 radix 往往输给外部归并。
>
> 再补一个容易被忽略的代价：LSD 需要额外空间。counting sort 作为每趟的引擎，本身需要 O(n+k) 的输出缓冲与计数数组；而 quicksort 是原地的。所以 radix sort 与 quicksort 的取舍不只是趟数，还包括空间与缓存行为。
>
> 再补一个实现细节：LSD 必须知道每个数字位的取值范围。十进制位是 0 到 9，$k = 10$；二进制按 r 位一组，$k = 2^r$。若位数切不整齐（比如 32 位切成三个 11 位），最后一组要按实际位宽处理，否则 k 会被高估，白扫一遍数组。
>
> 还有一点正确性之外的代价：LSD 要求每一趟都稳定，而稳定的 counting sort 是非原地的，所以 radix sort 整体也要 $\Theta(n+k)$ 的额外空间与额外一遍拷贝。这与排序是原地操作的直觉相违，工程上必须算进内存预算；原地版本存在，但代价是更复杂的交换与更差的缓存行为。
>
> 收束：LSD 的聪明之处在于把多关键字排序化归为多次单关键字稳定排序，代价是 d 趟扫描，收益是每趟都极其简单、可以交给最快的底层实现。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 图 8.3 用七个数把 radix sort 讲透了，而引理 8.3 给它配了一个可以拆开算的时间式子。
>
> 先逐趟走一遍。输入是 $\langle 329,457,657,839,436,720,355 \rangle$。按个位稳定排序，键依次是 9、7、7、9、6、0、5，稳定排完得 $\langle 720,355,436,457,657,329,839 \rangle$。再按十位稳定排序，键是 2、5、3、5、5、2、3，排完得 $\langle 720,329,436,839,355,457,657 \rangle$。最后按百位稳定排序，键是 7、3、4、8、3、4、6，得 $\langle 329,355,436,457,657,720,839 \rangle$，完全有序。
>
> 请重点盯住 457 与 657 这一对。它们的个位都是 7，第一趟不改变相对次序，457 仍在 657 之前；它们的十位都是 5，第二趟同样不改变次序；直到第三趟百位 4 小于 6，才把它们分开。两个数最终的正确次序，是靠前两趟保持不动攒下来的。
>
> 这正是稳定性的作用形式：稳定不是不交换，而是在键相等时不交换。一旦某一趟在相等键上做了交换，被丢掉的次序就无法从后续任何一趟恢复，因为后续各趟只看更高的位，对低位当年发生过什么一无所知。
>
> 多关键字排序是同一件事的直接应用。要按年、月、日三个关键字排日期，写法是先按日排、再按月排、最后按年排，三趟都用稳定排序。理由与 457 和 657 一样：最后排的关键字最重要，前面的趟只负责在高位持平时充当决胜依据。若顺序反了，先按年排的结果会被后两趟彻底覆盖，等于白排。
>
> 引理 8.3 的时间式子把两个因子分开：d 趟，每趟 $\Theta(n+k)$，合起来 $\Theta(d(n+k))$。式子本身没有信息量，价值在于它把趟数与每趟代价解耦，下一节的引理 8.4 就是靠调整 r 在这两个因子之间做权衡。
>
> 代入数字：$n = 10^6$、$d = 3$、$k = 10$ 时总代价约 $3.00003\times 10^6$，与比较排序的 $2n\ln n \approx 2.8\times 10^7$ 相比少了一个数量级。若把一个 32 位字按 8 位一组切开，则 $d = 4$、$k = 256$，代价 $4.001\times 10^6$，仍然线性。
>
> 跨课程连接数据库：SQL 的 ORDER BY 多列排序与这里的多趟稳定排序是同一个算法，区别在于数据库可能直接走索引跳过排序，也可能因为数据量大而改用外部归并。理解这一层，就能明白为什么加索引能省掉的往往正是这几趟扫描。
>
> 还要记住引理 8.3 的一个隐含前提：每一趟的稳定排序必须是 counting sort 这一类的线性算法。若每趟改用比较排序，总代价变成 $d\cdot n\lg n$，radix sort 就毫无优势了——它快，是因为内层足够快。
>
> 再补一个常被问到的实现问题：为什么每趟都用计数排序而不用比较排序？理由是 k 很小——十进制位只有十个取值，计数数组只要十一个格子，每趟的 $\Theta(n+k)$ 几乎就是 $\Theta(n)$。若改成比较排序，每趟至少 $\Theta(n\lg n)$，d 趟下来线性优势全赔进去。反过来说，若每一位的取值范围很大（比如按整个 32 位字当一位），计数排序就不划算，这正是引理 8.4 要平衡的东西。
>
> 收束：radix sort 的力量来自把多关键字问题拆成 d 个单关键字问题，而它的正确性完全押在每一趟的稳定性上。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 引理 8.4 的全部内容是一个自由度的选择：把一个 b 位的字切成每段几位。
>
> 设每段 r 位，则段数 $d = \lceil b/r \rceil$，每段取值范围是 $0$ 到 $2^r - 1$，正好交给计数排序处理，$k = 2^r$。于是总时间 $\Theta(d(n+2^r))$，也就是 $\Theta((b/r)(n+2^r))$。
>
> 两个因子朝相反方向走：r 变大，趟数 $b/r$ 变小；但每趟的 $2^r$ 指数膨胀。求平衡点就是对 $(b/r)(n+2^r)$ 关于 r 求导并令其为零。
>
> 把 r 当连续变量，导数等于零给出 $2^r(r\ln 2 - 1) = n$。这个方程没有初等解，但可以数值求：$n = 10^6$ 时解出 $r \approx 16.54$。
>
> 书上的结论是取 $r = \lfloor \lg n \rfloor$（这里约 19）在常数因子意义下最优。我自己复算之后发现精确最小并不在 19 附近，原因有两条：一是 d 是 $\lceil b/r \rceil$ 这个阶梯函数，不是光滑的 $b/r$；二是 r 恰好整除 b 时会白拿一次便宜。
>
> 把 $b = 32$、$n = 10^6$ 的整数点算一遍：$r = 8$ 时 $d = 4$，代价约 $4.001\times 10^6$；$r = 11$ 时 $d = 3$，代价约 $3.006\times 10^6$；$r = 16$ 时 $d = 2$，代价约 $2.131\times 10^6$；$r = 19$ 时 $d = 2$，代价约 $3.049\times 10^6$；$r = 20$ 时 $d = 2$，代价约 $4.097\times 10^6$。
>
> 所以在这一组具体参数下，最优是 $r = 16$，它恰好整除 32，比 19 少付了 $524288 - 65536 = 458752$ 项的开销。书上给 19 并不错，它保证的是常数因子意义下最优，不是逐点最小；工程实现应当按实际的 b、n 与缓存容量去试，而不是照抄公式。
>
> 另一个极端也值得记住：若 $b < \lfloor \lg n \rfloor$，则对任何 $r \le b$ 都有 $n + 2^r = \Theta(n)$，此时直接取 $r = b$，一趟计数排序就完成，总时间 $\Theta(n)$。
>
> 缓存层面的账更实际：$r = 16$ 时计数数组有 $2^{16}$ 项，每项四字节就是 256 KB，正好卡在常见 L2 的容量上；$r = 19$ 时是 2 MB，超出 L2 一个数量级，每趟的随机访问会把趟数省下来的收益吃回去。这条经验比渐近式更贴近实测。
>
> 跨课程连接高数的极值问题与 CSAPP 第 6 章：前者给两个反向因子相乘时求驻点的通用手法，后者给工作集决定 miss 率的判据；两者合起来，才是 r 取多少的完整答案。
>
> 还有一个前提容易被忽略：$\lceil b/r \rceil$ 意味着最后一段可能不满 r 位，取值范围只有 $2^{b - r(d-1)}$，计数排序的实际 k 比 $2^r$ 小。书上为了表述简洁统一写 $2^r$，那是一个上界；工程上按实际位宽分配数组，能省下可观的初始化时间，尤其当 n 不大时这一项甚至主导总耗时。
>
> 把整个讨论翻译成一句话：radix sort 的时间是趟数乘每趟代价，而每趟代价主要由计数数组的大小决定。于是取多大的 r 本质上是在问愿意让计数数组多大，答案由缓存容量而不是渐近式决定。这也解释了为什么实际库里的 radix sort 常用 8 位或 11 位一段——它们让计数数组落在几十 KB 到几百 KB，能整块装进 L1 或 L2。
>
> 实践里还有一条经验：当 b 不大（比如 16 位或 32 位整数）时，把 r 取成能整除 b 的值，趟数正好是 $b/r$，不会多出半趟；这种整除性往往比接近 $\lg n$ 更能决定实际耗时，因为它直接减少一次全量扫描。
>
> 收束：引理 8.4 是把理论最优与工程最优分开看的绝好例子——公式给数量级，实测给常数，两者都不能省。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 8.3-5 的星标不是随便标的：它要求把 MSD 递归的代价算成具体数字，而这个数字会大到让人放弃这条路线。
>
> 最坏情形是输入在每一位上都扎堆：所有 d 位数的第一位相同，于是第一趟只分出一个非空箱，剩下的工作递归到低一位；依次类推，每层都只有一个箱要处理，但分箱的趟数按十的幂次累积。
>
> 趟数算出来是 $10^0 + 10^1 + \cdots + 10^{d-1} = (10^d - 1)/9$。$d = 4$ 时是 1111 趟，$d = 6$ 时是 111111 趟。
>
> 操作员要跟踪的卡片堆数是同一量级：最深层有 $10^d$ 个箱，$d = 4$ 时是一万个堆。这就是中间卡片堆噩梦的精确刻画——不是算不完，是摆不下。
>
> 对照 LSD：同样的问题只要 d 趟，$d = 4$ 时四趟，与 1111 趟相差 278 倍。这个对比说明为什么工程上几乎只用 LSD，MSD 只在字典序、前缀查询这类场景里以 trie 的形式出现。
>
> bucket sort 走的是另一条路：不按数字位切，而按值域切。它把 $[0,1)$ 均分成 n 个等长子区间，把元素扔进对应的桶，对每个桶内部排序，最后按桶序拼接。
>
> 两者的假设性质完全不同。counting sort 假设值域小，这是结构性假设，扫一遍求最大值就能验证；bucket sort 假设值近似均匀独立，这是概率性假设，无法在 $O(n)$ 内验证，只能靠先验知识或采样估计。
>
> 把退化的代价算出来：$n = 10^3$ 个均匀分布的数配 $n$ 个桶，每桶期望 1 个元素，桶内插入排序总代价 $\Theta(n)$。若输入全落在 $[0,0.01)$ 内，则全部挤进前 10 个桶，每桶约 100 个元素，插入排序代价 $\sum n_i(n_i-1)/2 = 10 \times 4950 = 49500$，已接近 $n^2/2$ 的量级，线性承诺当场失效。
>
> 跨课程连接 6.431 的均匀分布与独立性：bucket sort 的分析要对输入分布取期望，而均匀独立正是让每个桶的占用服从多项分布的关键条件；一旦元素之间相关（比如按时间戳排序、数据有聚簇），均匀性假象立刻破裂。
>
> 补一句 MSD 的优点，免得把它说得一无是处：它天然支持前缀查询与字典序，因为最高位分完箱之后每个箱内部就是一个独立子问题，可以在需要时才递归。LSD 做不到这一点，它必须把所有趟跑完才能确定任何一个元素的位置。所以在字符串排序、路由表查找这类场景里，MSD 的 trie 形式反而是主流。
>
> 再补一个 bucket sort 的实现细节：桶通常用链表串起来，插入是 $O(1)$；桶内用插入排序，因为平均桶长是 1，插入排序在极短序列上的常数最小，换成快排光是递归开销就比比较本身贵。这与第 2 章小数组切插入排序的经验是同一条。
>
> 顺带一句：桶数不一定取 n，取 n 只是让期望桶长为 1、常数最舒服；取 $2n$ 或 $n/2$ 都合法，只是常数与空间跟着变。这个自由度和引理 8.4 里选 r 的自由度是同一类问题。
>
> 收束：counting sort 与 bucket sort 都在用结构换时间，区别是前者用值的范围、后者用值的分布；范围的假设可以检验，分布的假设只能相信。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第 6 行的 $\lfloor nA[i] \rfloor$ 是全算法的灵魂：它把一个连续值域映射成离散的桶号，而且映射本身保序。
>
> 先验证映射：若 x 落在 $[k/n, (k+1)/n)$ 内，则 $nx$ 落在 $[k, k+1)$ 内，取整恰为 k；反过来 $\lfloor nx \rfloor = k$ 也意味着 x 落在同一区间。所以值与桶号是一一对应的划分，中间没有任何近似。
>
> 正确性论证只有三句。设 $A[i] \le A[j]$，则 $\lfloor nA[i] \rfloor \le \lfloor nA[j] \rfloor$，因为取整是单调不减的；若两者相等，它们同桶，桶内的插入排序会把次序排对；若前者更小，它们落进不同桶，第 9 行的按序拼接保证小桶整体在前。
>
> 取图 8.4 的十个数走一遍：0.78 落桶 7、0.17 落桶 1、0.39 落桶 3、0.26 落桶 2、0.72 落桶 7、0.94 落桶 9、0.21 落桶 2、0.12 落桶 1、0.23 落桶 2、0.68 落桶 6。桶 2 有 3 个元素、桶 7 有 2 个、其余五个桶各 1 个，桶 4、5、8 为空。
>
> 桶内插入排序的总比较数是 $3 + 1 = 4$ 次，而把这十个数整体交给比较排序要约 $n\lg n \approx 33$ 次。差距来自分工：一次线性扫描完成了大部分排序工作，插入排序只处理桶里那几个元素。
>
> 为什么桶内平均只有常数个元素：n 个数独立均匀地落进 n 个桶，每个桶的期望占用是 1。这条直觉下一页会被精确化成 $\mathrm{E}[n_i^2] = 2 - 1/n$，而二阶矩正是桶内插入排序代价的量度。
>
> 与 counting sort 的区别值得摆清楚：counting sort 按每一个可能取值分格，格数是 k 加一；bucket sort 按值域切成 n 个连续区间，桶数固定为 n，与值域大小无关。前者要求值是整数且范围小，后者要求值落在 $[0,1)$ 且分布均匀——前者的限制更硬，后者退化的风险更大。
>
> 空间上也有区别：counting sort 的计数数组要 k 加一格，bucket sort 的桶数组只要 n 格，但桶内链表还要额外的指针空间。若元素本身很大（比如结构体），链表结点的开销不可忽略，这也是工程上常改成"两趟计数"的原因。
>
> 跨课程连接散列：$\lfloor nx \rfloor$ 本质上是一个 hash function（散列函数），把键映射到桶号；均匀分布保证碰撞的期望是常数，与散列表的平均 $O(1)$ 查找是同一个分析。区别在于散列函数要处理任意类型的键并抵抗对抗性输入，而这里的映射是恒等缩放的确定性函数，对任何非均匀分布都可能退化。
>
> 还有一个实现细节：$\lfloor nA[i] \rfloor$ 在 $A[i]$ 取到 1 时会越界，所以算法明确假设 $0 \le A[i] < 1$。若输入允许取 1，实现里要么把它归进最后一个桶，要么把桶数改成 n 加一，否则就写坏内存。这类边界检查在标准库里往往只有一行，但它属于正确性的一部分。
>
> 另外，桶号计算用浮点乘法加取整，这一步有精度风险：n 很大时 $nA[i]$ 可能超出双精度能精确表示整数的范围，取整就会错位。工程上要么限制桶数，要么改用定点运算，把映射写成整数乘加而不是浮点乘。
>
> 收束：bucket sort 的正确性只依赖映射的单调性，性能只依赖分布的均匀性；前者恒真，后者是赌注。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (8.2) 是整个 bucket sort 分析的核心，它的骨架是 5.4.2 节的 balls and bins（球与箱）。
>
> 把 n 个元素看成 n 个球、n 个桶看成 n 个箱子，每个球独立均匀地落进某个箱子，概率是 $1/n$。要算的是 $\mathrm{E}[n_i^2]$，也就是某个指定箱子里球数的平方的期望。
>
> 为什么盯住平方而不是别的：桶内用插入排序，代价是 $\Theta(n_i^2)$ 量级，所以二阶矩直接就是代价。这也是本节不像生日问题那样只问有没有碰撞、而要问碰撞总量的原因。
>
> 把 $n_i$ 写成指示器之和：$n_i = \sum_j X_{ij}$，其中 $X_{ij}$ 表示第 j 个元素落进桶 i。平方之后展开成双重和，对角项与交叉项就自然分开了。
>
> 对角项有 n 个，每个是 $X_{ij}^2$，而指示器的平方等于它自己，期望是 $1/n$，合计 1。交叉项有 $n(n-1)$ 个，两个不同元素同时落进同一个指定桶的概率是 $1/n^2$，合计 $(n-1)/n$。两者相加正好是 $2 - 1/n$。
>
> 核对数字：$n = 10$ 时公式给 1.9，两万次随机模拟得 1.8969；$n = 100$ 时公式给 1.99，模拟得 1.9901。n 越大越接近 2，因为对角项恒为 1、交叉项趋于 1。
>
> 独立性只用在哪里：只在交叉项，两个不同元素落桶才是独立事件。对角项不需要独立性，指示器与自己是完全相关的。而整个论证只用到期望的线性性，它对任意相关结构都成立，所以这个式子甚至不要求各元素独立，只要求边缘分布均匀。
>
> 与生日问题的对照：生日问题问至少有一对碰撞的概率，n 个球进 n 个箱时约等于 $1 - e^{-1/2} \approx 0.39$；这里问碰撞对数的期望，恰好约等于 1。同一个场景、两个统计量，前者是指示型的、要独立性才能算，后者是计数型的、只要线性性。
>
> 跨课程连接 6.431 的指示器随机变量与线性性：这套手法在期望分析里几乎万能，代价是它只给一阶矩信息，给不出集中性。若要知道桶长不超过某阈值的概率，就得用 Chernoff 型的偏差界。
>
> 再换一个视角：二阶矩可以拆成均值平方加方差，而 $\mathrm{E}[n_i] = 1$、$\mathrm{Var}(n_i) = 1 - 1/n$，两项各贡献 1。这个分解比展开双重和更直观——一个桶的平均负载是 1，波动也大约是 1，两者叠加才是 $2 - 1/n$。
>
> 顺带说清 $n_i$ 的分布：它服从参数为 n 与 $1/n$ 的二项分布，均值 1、方差 $1 - 1/n$。二项分布在均值附近的集中性由 Chernoff 界给出，可以证明桶长超过常数倍的概率指数小，这是桶内平均只有常数个元素这句话的严格版本。
>
> 还有一点值得记住：n 个球投进 n 个箱，期望的最大桶长是 $\Theta(\log n / \log \log n)$，比常数大。所以桶内代价并非逐桶都是 $O(1)$；总期望之所以仍是线性的，靠的是总额被 $\sum n_i^2$ 控制，而不是被最大桶控制。
>
> 最后补一句用法上的提醒：$2 - 1/n$ 与 n 无关的部分只有那个 2，所以桶内代价的总量是 $\Theta(n)$ 而不是 $\Theta(n^2)$；这个 2 与桶数无关，只与每个桶的期望负载有关，换成 $m$ 个桶就是 $1 + n/m$。
>
> 收束：$2 - 1/n$ 这个数几乎全部来自自己配自己的对角项，真正的碰撞只贡献不到 1——桶排序线性的秘密就藏在这一行。

为了证明 equation (8.2)，我们定义 indicator random variables（指示器随机变量，见 Section 5.2）

```math
X_{ij} = I\, \{\, A[j] \text{ falls in bucket } i \,\}
```

其中 $i = 0, 1, \ldots, n-1$ 且 $j = 1, 2, \ldots, n$。于是，

```math
n_i = \sum_{j=1}^{n} X_{ij}.
```

为了计算 $\mathrm{E}[n_i^2]$，我们展开平方并重新组合各项：……（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页是期望分析三步曲的舞台：分解、取期望、展开平方。
>
> 第一步分解：总时间等于固定开销加上各桶内部排序代价之和，即 $T(n) = \Theta(n) + \sum_{i=0}^{n-1} O(n_i^2)$。固定开销包括建桶、投放、拼接，都是 $\Theta(n)$。
>
> 第二步取期望：两边同时取期望，把期望推进求和号。这一步需要两个许可，一是期望的线性性，它不要求各项独立；二是确定性项可以直接出去，$\mathrm{E}[\Theta(n)] = \Theta(n)$。
>
> 关于 $O$ 与 $\mathrm{E}$ 的交换，书里引了 equation (C.22)。严格说这是对渐近记号的一种约定，使用时要知道它的条件：随机变量的规模要有界，否则 $\mathrm{E}[O(X)]$ 与 $O(\mathrm{E}[X])$ 的意义会变得含糊。
>
> 第三步代入式 (8.2)：$\mathrm{E}[T(n)] = \Theta(n) + \sum_i O(2 - 1/n) = \Theta(n) + O(2n - 1) = \Theta(n)$。$n = 10^4$ 时 $\mathrm{E}[\sum n_i^2] = 19999$，而最坏情况（全部落进一个桶）是 $10^8$，相差 5000 倍。
>
> 这个对比说明期望与最坏的差距不是常数而是量级：线性对平方。所以 bucket sort 的所有承诺都挂在分布均匀这一条上，一旦数据聚簇，它直接掉到 $\Theta(n^2)$，比 quicksort 的最坏还差——后者至少有随机化兜底，前者连兜底都没有。
>
> 为什么必须独立均匀：若元素之间存在相关，桶的占用不再是多项分布，二阶矩可能变成 $\Theta(n^2)$。极端的例子是所有元素相等，全部落进一个桶，某个 $n_i$ 等于 n，平方和就是 $n^2$。
>
> 再看第 8 行为什么选插入排序：桶的平均长度是 1，插入排序在极短序列上常数最小，而快排的递归开销反而更贵。这是第 2 章那条经验的直接延续，也是"算法选择要看子问题规模"的具体体现。
>
> 跨课程连接 CSAPP 第 6 章：桶通常用链表实现，每次插入是一次随机地址的写，$n = 10^6$ 时链表结点散布在堆上，局部性极差；若改成两趟计数加数组，就退化成 counting sort，局部性变好但要求值域小。工程上的选择往往是这两者的折中。
>
> 还有一件容易忽略的事：$\mathrm{E}[T(n)] = \Theta(n)$ 里的常数很小。因为桶内插入排序的比较次数是 $n_i(n_i-1)/2$，而 $\mathrm{E}[n_i(n_i-1)] = \mathrm{E}[n_i^2] - \mathrm{E}[n_i] = 1 - 1/n$，全部桶加起来约 $n - 1$ 次比较，与投放的 n 次同级。这解释了为什么 bucket sort 在均匀数据上实测极快。
>
> 把三个线性时间算法放在一起看，共同点就清楚了：它们都放弃比较模型，各自换上一个关于输入的假设。counting sort 用值的范围，radix sort 用值的位数结构，bucket sort 用值的分布。第 9 章会回到比较模型，但换一个更弱的问题——只求第 i 小的元素，不做全排序。
>
> 最后一个提醒：均匀独立这个假设在真实数据上几乎从不严格成立。实用的做法是先采样估计分布，再按经验分位数而不是等宽区间分桶，这就是基于分位数的桶排序；代价是多一次采样与一趟映射，收益是在偏斜数据上仍能接近线性。
>
> 收束：bucket sort 的期望线性是分布假设、期望线性、二阶矩三件事的合成品，缺一件都不成立；这也是它常被当作知道数据分布时才用的算法的原因。
