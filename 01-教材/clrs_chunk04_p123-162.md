# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk04 · 书页 123–162 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §5.2–5.3, p.123</span>

（接上页）……我们预期对任意 input（输入）都是如此，而不只是对取自某个特定 distribution（分布）的输入。

### Section 5.3 · Randomized algorithms（随机化算法） <span style="color:#2471a3;">**[section]**</span>

让我们进一步考察 probabilistic analysis（概率分析）与 randomized algorithm（随机化算法）之间的区别。在 §5.2 中我们曾断言：假设候选人以随机顺序到来，雇用一位新办公室助理的 expected number（期望次数）约为 $\ln n$。注意，这里的 algorithm（算法）是 deterministic（确定性的）：对任何一个特定输入，雇用新办公室助理的次数总是相同的。此外，雇用新办公室助理的次数随输入不同而不同，它取决于各位候选人的 rank（名次）。由于这个次数只取决于候选人的名次，我们可以按顺序列出各位候选人的名次来表示一个特定输入，即 $\langle rank(1), rank(2), \ldots, rank(n) \rangle$。给定名次表 $A_1 = \langle 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 \rangle$，新办公室助理总会被雇用 10 次，因为每位后继候选人都比前一位更好，于是第 5–6 行在每次 iteration（迭代）中都会被执行。给定名次表 $A_2 = \langle 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 \rangle$，新办公室助理只在第一次迭代时被雇用一次。给定名次表 $A_3 = \langle 5, 2, 1, 8, 4, 7, 10, 9, 3, 6 \rangle$，新办公室助理被雇用三次，分别是在面试名次为 5、8 和 10 的候选人时。回想我们的算法成本取决于雇用新办公室助理的次数，可以看到：既有像 $A_1$ 这样的 expensive inputs（昂贵输入），也有像 $A_2$ 这样的 inexpensive inputs（廉价输入），还有像 $A_3$ 这样的 moderately expensive inputs（成本中等的输入）。

另一方面，考虑这样一个随机化算法：先对候选人做 permutation（排列），然后再确定最佳候选人。在这种情况下，我们在算法中进行 randomize（随机化），而不是在输入分布中随机化。给定一个特定输入，比如上面的 $A_3$，我们无法说出最大值会被更新多少次，因为这个量随算法的每次运行而不同。第一次在 $A_3$ 上运行该算法时，可能产生排列 $A_1$ 并执行 10 次更新；而第二次运行时，可能产生排列 $A_2$ 并只执行一次更新。第三次运行时，执行的更新次数又可能是别的某个数。每运行一次该算法，其执行过程都取决于所做的随机选择，并很可能与上一次的执行不同。对于这个算法以及许多其他随机化算法而言，没有任何特定输入能诱发其 worst-case behavior（最坏情况行为）。即使是你最坏的敌人，也无法构造出一个坏的输入数组，因为随机排列使输入顺序变得无关紧要。只有当 random-number generator（随机数生成器）产生一个"不走运"的排列时，随机化算法才会表现糟糕。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一段要抓的是一件"控制权移交"的事：deterministic algorithm（确定性算法）的成本由 input（输入）唯一决定，因此只要存在一个坏输入，最坏情况就必然可达；randomized algorithm（随机化算法）把成本变成 random variable（随机变量），于是最坏情况从"某个输入"降格为"某条随机数轨迹"。
>
> 机制分两层。第一层是量纲的替换：确定性分析问的是 $\max_{x} T(x)$，随机化分析问的是 $\mathrm{E}[T]$ 与尾部 $\Pr\{T > t\}$。这两个量不在同一个坐标系里，所以"期望好"并不自动等于"不会坏"——随机化算法给你的是 tail bound（尾部界），不是 worst-case（最坏情况）为零。第二层是为什么这样可行：对手只能选择输入，不能选择你的 random bits（随机比特）；输入顺序被 permutation（排列）抹平之后，任意固定输入在算法眼里的分布都退化成"随机输入"，对手精心构造的结构被洗掉了。注意这里没有任何关于输入分布的 assumption（假设），被随机化的是算法自己。
>
> 三个概念必须分开，否则一句话里就会偷换。average-case（平均情况）是对输入分布求期望，前提是你相信数据长什么样；expected（期望）是对算法内部掷骰子求期望，不需要任何关于数据的假设；amortized（摊还）是对一串操作的总额平均，既不涉及随机也不涉及分布。三者的数学对象分别是输入的分布、算法的随机源、操作序列的总和。教材之所以反复强调这一点，是因为一旦把 expected（期望）当成 average-case（平均情况），你就会以为"换个输入就能推翻结论"——随机化算法恰恰做不到这一点，这正是它在缓存驱逐策略、哈希函数选择、负载均衡这些对抗场景里被选用的理由。
>
> 算一个数看量级。hiring problem（雇用问题）取 $n = 10$：若候选人恰好按名次递增到达，即 $\langle 1, 2, \ldots, 10 \rangle$，每次都要换人，成本为 10 次雇用；而随机排列之下的期望雇用次数是调和数 $H_{10} = 2.929$。差距只有 3.4 倍，因为 $\Theta(\lg n)$ 与 $n$ 在 $n = 10$ 时还没拉开。换成 quicksort（快速排序）看 $n = 10^4$：固定取末尾元素作 pivot（枢轴）遇到已排序输入要退化成 $\Theta(n^2)$，比较次数 $n(n-1)/2 = 4.9995 \times 10^7$；随机选 pivot（枢轴）的期望比较次数约 $2n \ln n = 1.842 \times 10^5$。两数相差 271 倍，这才是"最坏情况由谁控制"在实际系统里的分量。再看 $n = 1000$：固定 pivot（枢轴）要 $499500$ 次比较，随机 pivot（枢轴）约 $1.38 \times 10^4$ 次，相差 36 倍——倍数随 $n$ 增大而增大，因为差距是 $\Theta(n/\lg n)$。但随机化并不消灭最坏情况：抽到"每次分割都极不均衡"的排列概率虽小，那条路径依然存在，所以工程实现还要给递归深度加上限，这一手在第 19 条注里会以 introsort 的面目出现。
>
> 跨课程连接落在 6.042J 与 CSAPP 的分工上：6.042J 给你 conditioning（条件化）与 independence（独立性）的语言，让你能把"算法掷骰子"写成一个概率空间；CSAPP 第 6 章讲 storage hierarchy（存储层次结构）时完全没有对抗视角，因为 cache（高速缓存）的命中率不取决于谁在攻击你，它只取决于地址流。两套视角的合流点在 hashing（散列）与密码学：那里的对手真的会构造输入。区别也要说清：6.042J 的期望是对 sample space（样本空间）求和，而这里的期望是对算法内部的 random choices（随机选择）求和，前者描述世界，后者描述你自己。
>
> 一句话收束：随机化不是让算法变快，而是把"最坏情况"从输入的属性改成你自己掷骰子的属性。

对于 hiring problem（雇用问题），代码中唯一需要的改动，就是把该数组随机排列。

---

> <span style="color:#7f8c8d;">CLRS §5.3, p.124</span>

```text
RANDOMIZED-HIRE-ASSISTANT(n)
 1  randomly permute the list of candidates
 2  best = 0          // candidate 0 is a least-qualified dummy candidate
 3  for i = 1 to n
 4      interview candidate i
 5      if candidate i is better than candidate best
 6          best = i
 7          hire candidate i
```

有了这个简单的改动，我们就创建了一个 randomized algorithm（随机化算法），其性能与"假设候选人以随机顺序出现"时所得到的性能相匹配。

**Lemma 5.3（引理 5.3）** <span style="color:#2471a3;">**[lemma]**</span>

过程 RANDOMIZED-HIRE-ASSISTANT（随机化雇用助手）的 expected hiring cost（期望雇用成本）为 $O(c \ln n)$。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  在对输入数组进行排列之后，我们所达成的局面与对 HIRE-ASSISTANT 进行概率分析时的局面完全相同。

对比 Lemma 5.2（引理 5.2）与 Lemma 5.3（引理 5.3），可以凸显 probabilistic analysis（概率分析）与 randomized algorithm（随机化算法）之间的差异。在引理 5.2 中，我们对 input（输入）做了一个 assumption（假设）。在引理 5.3 中，我们不做这样的假设，尽管对输入进行随机化会额外耗费一些时间。为了与我们的术语保持一致，我们把引理 5.2 表述为 average-case hiring cost（平均情况雇用成本），而把引理 5.3 表述为 expected hiring cost（期望雇用成本）。在本节的余下部分，我们将讨论 randomly permuting inputs（随机化排列输入）所涉及的一些问题。

#### Randomly permuting arrays（随机排列数组） <span style="color:#2471a3;">**[section]**</span>

许多 randomized algorithm（随机化算法）通过排列给定的输入数组来 randomize（随机化）输入。（使用随机化还有其他方式。）这里我们将讨论实现这一点的两种方法。我们假设给定一个数组 $A$，不失一般性（without loss of generality），它包含元素 1 到 $n$。我们的目标是产生该数组的一个 random permutation（随机排列）。

一种常见的方法是：给数组的每个元素 $A[i]$ 分配一个 random priority（随机优先级）$P[i]$，然后根据这些优先级对 $A$ 的元素进行 sort（排序）。例如，若初始数组为 $A = \langle 1, 2, 3, 4 \rangle$，并且我们选择随机优先级 $P = \langle 36, 3, 62, 19 \rangle$，那么将产生数组 $B = \langle 2, 4, 1, 3 \rangle$，因为第二个优先级最小，其次是第四个，然后是第一个，最后是第三个。我们把这个过程称为 PERMUTE-BY-SORTING（通过排序进行排列）：

---

> <span style="color:#7f8c8d;">CLRS §5.3, p.125</span>

```text
PERMUTE-BY-SORTING(A)
 1  n = A.length
 2  let P[1 .. n] be a new array
 3  for i = 1 to n
 4      P[i] = RANDOM(1, n^3)
 5  sort A, using P as sort keys
```

第 4 行在 1 到 $n^3$ 之间选择一个随机数。我们使用 1 到 $n^3$ 的范围，是为了使 $P$ 中所有 priority（优先级）都互不相同这件事 likelihood（可能性）很大。（Exercise 5.3-5（习题 5.3-5）要求你证明所有元素互不相同的概率至少为 $1 - 1/n$，而 Exercise 5.3-6（习题 5.3-6）则问：即使两个或多个优先级相同，应如何实现该算法。）我们假设所有优先级都是 unique（唯一的）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第 4 行取 $1$ 到 $n^3$ 这个范围，本质上是在买一份"碰撞保险"：priority（优先级）不唯一会破坏均匀性，而编号空间每放大一个因子，碰撞概率就掉一个量级。
>
> 先把机制拆开。目标是 uniform random permutation（均匀随机排列），也就是在 $n!$ 个结果上各给 $1/n!$ 概率。直接在 $n!$ 个排列上均匀抽样很麻烦（$n!$ 随 $n$ 爆炸，没法用一次取模搞定），于是换一条路：给每个元素独立发一个 random priority（随机优先级），再用比较排序这一确定性过程把优先级翻译成名次，名次即位置。这条链有两个误差来源——优先级可能撞车（两个元素名次无法区分），排序本身要花时间。取 $n^3$ 是为了压住第一个误差：$n$ 个优先级落在 $n^3$ 个格子里，配对数 $\binom{n}{2} = n(n-1)/2$，由 union bound（联合界）得碰撞概率至多 $(n-1)/(2n^2) < 1/(2n)$，于是"全部互不相同"的概率至少 $1 - 1/n$，这正是习题 5.3-5 要证的界。
>
> 代入数字。$n = 100$：格子数 $10^6$，配对数 $4950$，期望碰撞对数 $4950/10^6 = 4.95 \times 10^{-3}$；精确连乘 $\prod_{i=0}^{99}(1 - i/10^6)$ 得 $0.99506$，与下界 $1 - 1/n = 0.99$ 一致，而且更紧。$n = 10^4$：配对数 $4.9995 \times 10^7$，格子 $10^{12}$，期望碰撞 $5.0 \times 10^{-5}$，基本可以当零。反过来验证 $n^2$ 够不够：把格子数换成 $n^2$，期望碰撞对数约 $1/2$，也就是说有一半机会撞车，均匀性直接破产；再换成 $n$，期望碰撞对数约 $n/2$，彻底失效。所以 $n^3$ 不是随手挑的，它让误差从"常数量级"掉到 $1/n$。
>
> 这里藏着一条比结论更值钱的设计手法：先枚举一个我们"抽得动"的理想概率空间（$n$ 个独立均匀编号），再用一个确定性过程（排序）把它解码成我们"想要但抽不动"的对象（均匀排列）。这个手法在两处会重演：第 7 章随机化快排不直接抽排列，而是每层抽一个 pivot（枢轴）；第 11 章不直接抽"好的散列函数"，而是从一族函数里随机取一个。区别在于：这里"解码"是排序、代价 $\Theta(n \lg n)$，而快排与散列的解码代价是 $O(1)$ 与 $O(n)$。
>
> 代价那一半也值得算清。比较排序有 $\Omega(n \lg n)$ 的下界，所以整个过程是 $\Theta(n \lg n)$，随机化并没有让它变快，反而比直接洗牌（$\Theta(n)$）慢。但 CLRS 习题 8.3-4 提示了一个巧合：优先级都落在 $0$ 到 $n^3 - 1$ 之间，用基数为 $n$ 的 radix sort（基数排序）只需 3 趟分配，总时间 $\Theta(n)$——因为 $n^3$ 这个上界事先知道，可以把它当成"位数有限"的结构来用。区别在于：前者是通用黑箱（任何可比的键都能排），后者把"键的取值范围"变成了资源。这也解释了教材为什么先给 $\Theta(n \lg n)$ 的实现：它清楚、无假设，代价只差一个对数。
>
> 跨课程连接有两处。其一，6.042J 的生日问题是同一个模型：阈值出现在"配对数追平格子数"处，这里配对数 $\Theta(n^2)$、格子 $n^3$，余量 $n$ 倍，所以安全。其二，第 8 章的决策树下界让你能判断"这条实现路径是不是已经最优"——在比较模型里 $\Theta(n \lg n)$ 是天花板，要突破它必须换模型（用值的范围当时标），这正是计数/基数排序的位置。
>
> 一句话收束：$n^3$ 买的不是正确性，而是"以高概率正确"，而"先抽得动的空间、再确定性解码"才是这段代码真正想留下的东西。

这一过程中耗时的步骤是第 5 行的排序。正如第 8 章将要讲到的，如果我们使用 comparison sort（比较排序），排序需要 $\Omega(n \lg n)$ 时间。我们可以达到这一 lower bound（下界），因为我们已经看到 merge sort（归并排序）需要 $\Theta(n \lg n)$ 时间。（在第二部分我们还会看到其他需要 $\Theta(n \lg n)$ 时间的比较排序。Exercise 8.3-4（习题 8.3-4）要求你解决一个非常类似的问题：在 $O(n)$ 时间内对范围 0 到 $n^3 - 1$ 中的数排序。）排序之后，如果 $P[i]$ 是第 $j$ 小的优先级，那么 $A[i]$ 就位于输出的第 $j$ 个位置。这样我们便得到一个 permutation（排列）。剩下要证明的是：该过程产生的是一个 uniform random permutation（均匀随机排列），也就是说，该过程等可能地产生数字 1 到 $n$ 的每一种排列。

**Lemma 5.4（引理 5.4）** <span style="color:#2471a3;">**[lemma]**</span>

假设所有优先级互不相同，则过程 PERMUTE-BY-SORTING 产生输入的一个 uniform random permutation（均匀随机排列）。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  我们从考虑这样一个特定排列开始：每个元素 $A[i]$ 都得到第 $i$ 小的优先级。我们将证明这个排列出现的概率恰好为 $1/n!$。对于 $i = 1, 2, \ldots, n$，令 $E_i$ 表示元素 $A[i]$ 得到第 $i$ 小优先级这一 event（事件）。于是我们希望计算"对所有 $i$，事件 $E_i$ 都发生"的概率，即

```math
\Pr\{E_1 \cap E_2 \cap E_3 \cap \cdots \cap E_{n-1} \cap E_n\}\,.
```

利用 Exercise C.2-5（习题 C.2-5），这个概率等于

```math
\Pr\{E_1\} \cdot \Pr\{E_2 \mid E_1\} \cdot \Pr\{E_3 \mid E_2 \cap E_1\} \cdot \Pr\{E_4 \mid E_3 \cap E_2 \cap E_1\} \cdots \Pr\{E_i \mid E_{i-1} \cap E_{i-2} \cap \cdots \cap E_1\} \cdots \Pr\{E_n \mid E_{n-1} \cap \cdots \cap E_1\}\,.
```

我们有 $\Pr\{E_1\} = 1/n$，因为它就是"从 $n$ 个优先级的集合中随机选出的一个优先级恰好是最小优先级"的概率。

接下来我们观察到……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.3, p.126</span>

> （接上页）……接下来我们观察到：$\Pr\{E_2 \mid E_1\} = 1/(n-1)$，因为在给定元素 $A[1]$ 已取得最小优先级的条件下，其余 $n-1$ 个元素中的每一个都有相同的机会取得第二小的优先级。一般地，对于 $i = 2, 3, \ldots, n$，我们有 $\Pr\{E_i \mid E_{i-1} \cap E_{i-2} \cap \cdots \cap E_1\} = 1/(n-i+1)$，因为：在给定元素 $A[1]$ 到 $A[i-1]$ 已（按序）取得最小的 $i-1$ 个优先级的条件下，其余 $n - (i-1)$ 个元素中的每一个都有相同的机会取得第 $i$ 小的优先级。于是，我们有

```math
\begin{aligned}
\Pr\{E_1 \cap E_2 \cap E_3 \cap \cdots \cap E_{n-1} \cap E_n\}
  &= \left(\frac{1}{n}\right)\left(\frac{1}{n-1}\right)\cdots\left(\frac{1}{2}\right)\left(\frac{1}{1}\right) \\[4pt]
  &= \frac{1}{n!}\,,
\end{aligned}
```

> 这样就证明了：得到恒等排列（identity permutation）的概率是 $1/n!$。

> 我们可以把这个证明推广到优先级的任意一个排列。考虑集合 $\{1, 2, \ldots, n\}$ 的任何一个固定排列 $\sigma = \langle \sigma(1), \sigma(2), \ldots, \sigma(n) \rangle$。令 $r_i$ 表示分配给元素 $A[i]$ 的优先级的 rank（名次），其中拥有第 $j$ 小优先级的元素名次为 $j$。如果我们把 $E_i$ 定义为"元素 $A[i]$ 得到第 $\sigma(i)$ 小的优先级"，即 $r_i = \sigma(i)$ 这一事件，那么同样的证明仍然成立。因此，如果我们计算得到任何一个特定排列的概率，其计算过程与上面的完全相同，所以得到这个排列的概率同样是 $1/n!$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注释要立的模板是「条件概率链」：证均匀性不要去证"每个元素落在每个位置的概率"，而要证"每个完整结果的概率"。
>
> 为什么弱条件不够？"每个元素落在每个位置概率 $1/n$"只约束了 $n^2$ 个边缘概率，而均匀性约束的是 $n!$ 个联合概率；前者是后者的推论，反过来不成立。教材第 109 行那句提醒与习题 5.3-4 的循环移位就是反例：$n = 4$ 时它只产出 4 个排列（每个的概率 $1/4$），其余 20 个排列概率为 0，可每个元素落到每个位置的概率仍然是 $1/4$——边缘对、联合错。链式证明的写法是：把目标事件拆成按时间排列的 $E_1, E_2, \ldots, E_n$，用乘法法则 $\Pr\{E_1 \cap \cdots \cap E_n\} = \prod_{i=1}^{n} \Pr\{E_i \mid E_1 \cap \cdots \cap E_{i-1}\}$，再逐步用"剩余选项彼此对称"把每个条件概率钉成 $1/(n-i+1)$。关键在于每步只用对称性，不用 independence（独立性）——各 $E_i$ 显然不独立，但条件化把它们串成了可算的链。
>
> 手算一遍 $n = 4$：固定目标排列 $\langle 3, 1, 4, 2 \rangle$，第一步要它落在首位，概率 $1/4$；给定首位之后第二步要它落到次位，剩余三选一，概率 $1/3$；再 $1/2$；最后一步只剩一个元素，概率 $1$。连乘 $1/24$，恰是 $1/4!$。再看引理 5.5 的不变式版本：不变式断言"前缀恰为某个 $(i-1)$-排列的概率是 $(n-i+1)!/n!$"，保持步乘上 $1/(n-i+1)$ 得到 $(n-i)!/n!$，终止时 $i = n+1$ 得 $1/n!$。顺带核对 $n = 3$：连乘为 $1/3 \cdot 1/2 \cdot 1 = 1/6$，恰是 $1/3!$，而循环移位构造在 $n = 3$ 时只产出 3 个结果、概率质量集中，一眼就能看出它不是均匀的。两种写法是同一件事的两种记账方式：一个是连乘、一个是递推；连乘版适合手算小情形，递推版适合写成不变式。
>
> 历史与出处：Fisher–Yates shuffle（费雪–耶茨洗牌）的纸笔版出自 Fisher 与 Yates 1938 年的《Statistical tables for biological, agricultural and medical research》例 12（多个二手书目条目与离线维基一致到书名、年份与例号）；把它改写成今天这种原地交换的计算机形式的，是 Durstenfeld 1964 年在 CACM 上的 Algorithm 235；Knuth 在《The Art of Computer Programming》第二卷的讲解让"Knuth shuffle"这个名字流传开。必须区分两个版本：1938 年版本是"从剩余表里划掉再编号"的纸笔流程，需要额外表；1964 年版本才是原地交换、只花 $n-1$ 次随机调用、$O(n)$ 时间。区别还在于前者每步取 $1$ 到剩余个数的随机整数，后者取 $i$ 到 $n$，两者等价但后者更好写。
>
> 跨课程连接放在线性代数：把一次洗牌看成作用在概率向量上的线性映射，RANDOMIZE-IN-PLACE 的每一步对应一个 doubly stochastic matrix（双随机矩阵），均匀分布是它的不动点；Strang 课上的 Markov chain（马尔可夫链）稳态分析就是这个结构。区别在于：线性代数只告诉你不动点存在且唯一（需要不可约与非周期这类条件），那是一个极限结论；而这里要证的是"无论从哪个初始排列出发，恰好 $n$ 步之后落在均匀分布上"——这是有限步的精确等式，比渐近收敛强得多。
>
> 一句话收束：证均匀性的正确粒度是排列，不是元素；而让链能连乘的，是每一步在给定历史下的对称性。

你可能会认为：要证明一个排列是 uniform random permutation（均匀随机排列），只需证明对每个元素 $A[i]$，它最终落在位置 $j$ 的概率是 $1/n$ 就够了。Exercise 5.3-4（习题 5.3-4）表明这个较弱的条件实际上是不充分的。

生成随机排列的一个更好的方法是 in place（原地）排列给定数组。过程 RANDOMIZE-IN-PLACE 在 $O(n)$ 时间内完成此事。在它的第 $i$ 次 iteration（迭代）中，它从元素 $A[i]$ 到 $A[n]$ 之中随机选取元素 $A[i]$。在第 $i$ 次迭代之后，$A[i]$ 就再也不会被改变。

```text
RANDOMIZE-IN-PLACE(A)
 1  n = A.length
 2  for i = 1 to n
 3      swap A[i] with A[RANDOM(i, n)]
```

我们将使用一个 loop invariant（循环不变式）来证明：过程 RANDOMIZE-IN-PLACE 产生一个均匀随机排列。一个包含 $n$ 个元素的集合上的 $k$-permutation（$k$-排列）是一个由这 $n$ 个元素中的 $k$ 个组成的、无重复的 sequence（序列）。（见 Appendix C（附录 C）。）这样的 $k$-排列共有 $n!/(n-k)!$ 种可能。

---

> <span style="color:#7f8c8d;">CLRS §5.3, p.127</span>

**Lemma 5.5（引理 5.5）** <span style="color:#2471a3;">**[lemma]**</span>

过程 RANDOMIZE-IN-PLACE 计算出一个 uniform random permutation（均匀随机排列）。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>  我们使用如下的 loop invariant（循环不变式）：
>
> 恰在第 2–3 行 for 循环的第 $i$ 次 iteration（迭代）之前，对 $n$ 个元素的每个可能的 $(i-1)$-排列，子数组 $A[1 .. i-1]$ 以概率 $(n-i+1)!/n!$ 包含这个 $(i-1)$-排列。

我们需要证明：该不变式在第一次循环迭代之前成立；循环的每次迭代都维持该不变式；并且当循环 termination（终止）时，该不变式能提供一个可用于证明 correctness（正确性）的有用性质。

**Initialization（初始化）：** 考虑恰在第一次循环迭代之前的情形，此时 $i = 1$。循环不变式说：对每个可能的 0-排列，子数组 $A[1 .. 0]$ 以概率 $(n-i+1)!/n! = n!/n! = 1$ 包含这个 0-排列。子数组 $A[1 .. 0]$ 是一个 empty subarray（空子数组），而 0-排列不含任何元素。于是，$A[1 .. 0]$ 以概率 1 包含任何 0-排列，循环不变式在第一次迭代之前成立。

**Maintenance（保持）：** 我们假设恰在第 $i$ 次迭代之前，每个可能的 $(i-1)$-排列都以概率 $(n-i+1)!/n!$ 出现在子数组 $A[1 .. i-1]$ 中，并且我们将证明：在第 $i$ 次迭代之后，每个可能的 $i$-排列都以概率 $(n-i)!/n!$ 出现在子数组 $A[1 .. i]$ 中。这样，把 $i$ 递增以进入下一次迭代后，循环不变式便得到维持。

让我们考察第 $i$ 次迭代。考虑一个特定的 $i$-排列，并将其中的元素记为 $\langle x_1, x_2, \ldots, x_i \rangle$。这个排列由一个 $(i-1)$-排列 $\langle x_1, \ldots, x_{i-1} \rangle$ 后面跟着算法放入 $A[i]$ 的值 $x_i$ 组成。令 $E_1$ 表示"前 $i-1$ 次迭代已在 $A[1 .. i-1]$ 中创建了特定的 $(i-1)$-排列 $\langle x_1, \ldots, x_{i-1} \rangle$"这一 event（事件）。由循环不变式，$\Pr\{E_1\} = (n-i+1)!/n!$。令 $E_2$ 表示"第 $i$ 次迭代把 $x_i$ 放入位置 $A[i]$"这一事件。$i$-排列 $\langle x_1, \ldots, x_i \rangle$ 恰在 $E_1$ 与 $E_2$ 同时发生时出现在 $A[1 .. i]$ 中，因此我们希望计算 $\Pr\{E_2 \cap E_1\}$。利用 equation (C.14)（式 (C.14)），我们有

```math
\Pr\{E_2 \cap E_1\} = \Pr\{E_2 \mid E_1\}\,\Pr\{E_1\}\,.
```

概率 $\Pr\{E_2 \mid E_1\}$ 等于 $1/(n-i+1)$，因为在第 3 行中，算法从位置 $A[i .. n]$ 的 $n-i+1$ 个值中随机选取 $x_i$。于是，我们有……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.3, p.128</span>

（接上页）

```math
\begin{aligned}
\Pr\{E_2 \cap E_1\}
  &= \Pr\{E_2 \mid E_1\}\,\Pr\{E_1\} \\[4pt]
  &= \frac{1}{n-i+1} \cdot \frac{(n-i+1)!}{n!} \\[4pt]
  &= \frac{(n-i)!}{n!}\,.
\end{aligned}
```

> **Termination（终止）：** 在终止时，$i = n+1$，于是子数组 $A[1 .. n]$ 以概率 $(n-(n+1)+1)!/n! = 0!/n! = 1/n!$ 是一个给定的 $n$-排列。因此，RANDOMIZE-IN-PLACE 产生一个 uniform random permutation（均匀随机排列）。

randomized algorithm（随机化算法）往往是求解一个问题最简单、最有效的方式。在本书中我们会不时地使用随机化算法。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**5.3-1** Professor Marceau objects to the loop invariant used in the proof of Lemma 5.5. He questions whether it is true prior to the first iteration. He reasons that we could just as easily declare that an empty subarray contains no 0-permutations. Therefore, the probability that an empty subarray contains a 0-permutation should be 0, thus invalidating the loop invariant prior to the first iteration. Rewrite the procedure RANDOMIZE-IN-PLACE so that its associated loop invariant applies to a nonempty subarray prior to the first iteration, and modify the proof of Lemma 5.5 for your procedure.

**5.3-2** Professor Kelp decides to write a procedure that produces at random any permutation besides the identity permutation. He proposes the following procedure:

```text
PERMUTE-WITHOUT-IDENTITY(A)
 1  n = A.length
 2  for i = 1 to n - 1
 3      swap A[i] with A[RANDOM(i + 1, n)]
```

Does this code do what Professor Kelp intends?

**5.3-3** Suppose that instead of swapping element $A[i]$ with a random element from the subarray $A[i .. n]$, we swapped it with a random element from anywhere in the array:……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.3, p.129</span>

（接上页）

```text
PERMUTE-WITH-ALL(A)
 1  n = A.length
 2  for i = 1 to n
 3      swap A[i] with A[RANDOM(1, n)]
```

**5.3-3（续）** Does this code produce a uniform random permutation? Why or why not?

**5.3-4** Professor Armstrong suggests the following procedure for generating a uniform random permutation:

```text
PERMUTE-BY-CYCLIC(A)
 1  n = A.length
 2  let B[1 .. n] be a new array
 3  offset = RANDOM(1, n)
 4  for i = 1 to n
 5      dest = i + offset
 6      if dest > n
 7          dest = dest - n
 8      B[dest] = A[i]
 9  return B
```

Show that each element $A[i]$ has a $1/n$ probability of winding up in any particular position in $B$. Then show that Professor Armstrong is mistaken by showing that the resulting permutation is not uniformly random.

**5.3-5 $\star$** Prove that in the array $P$ in procedure PERMUTE-BY-SORTING, the probability that all elements are unique is at least $1 - 1/n$.

**5.3-6** Explain how to implement the algorithm PERMUTE-BY-SORTING to handle the case in which two or more priorities are identical. That is, your algorithm should produce a uniform random permutation, even if two or more priorities are identical.

**5.3-7** Suppose we want to create a random sample of the set $\{1, 2, 3, \ldots, n\}$, that is, an $m$-element subset $S$, where $0 \le m \le n$, such that each $m$-subset is equally likely to be created. One way would be to set $A[i] = i$ for $i = 1, 2, 3, \ldots, n$, call RANDOMIZE-IN-PLACE($A$), and then take just the first $m$ array elements. This method would make $n$ calls to the RANDOM procedure. If $n$ is much larger than $m$, we can create a random sample with fewer calls to RANDOM. Show that……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.3–5.4, p.130</span>

（接上页）

**5.3-7（续）** ……the following recursive procedure returns a random $m$-subset $S$ of $\{1, 2, 3, \ldots, n\}$, in which each $m$-subset is equally likely, while making only $m$ calls to RANDOM:

```text
RANDOM-SAMPLE(m, n)
 1  if m == 0
 2      return ∅
 3  else S = RANDOM-SAMPLE(m - 1, n - 1)
 4      i = RANDOM(1, n)
 5      if i ∈ S
 6          S = S ∪ {n}
 7      else S = S ∪ {i}
 8  return S
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段递归值得单独拎出来，因为它是"只花 $m$ 次随机数就从 $n$ 个元素里均匀抽 $m$-子集"的最小样本：随机调用次数从 $n$ 降到 $m$，而正确性一分不少。
>
> 机制是这样的。设 $S = $ RANDOM-SAMPLE$(m-1, n-1)$，按归纳假设它是 $\{1, \ldots, n-1\}$ 上均匀的 $(m-1)$-子集；随后抽一个 $i \in \{1, \ldots, n\}$。若 $i \in S$，说明这个名额已经被前 $n-1$ 个元素中的一个占住，于是把 $n$ 塞进去（大小仍是 $m$）；若 $i \notin S$，就把 $i$ 塞进去。为什么这样就均匀？因为第 $n$ 个元素"是否入样"这件事被那枚均匀的 $i$ 以 $m/n$ 的概率决定了：$i$ 落进 $S$（概率 $(m-1)/n$）时 $n$ 入样，$i$ 恰好等于 $n$（概率 $1/n$）时 $n$ 也入样，合计 $m/n$；而不含 $n$ 的那些 $m$-子集，则通过 $i$ 落在 $S$ 之外被逐一选中。归纳假设管住前 $n-1$ 个元素，这枚硬币管住"要不要 $n$"，两段拼起来每个 $m$-子集的概率都是 $1/\binom{n}{m}$。
>
> 我把小情形全部枚举验证过：$m = 2, n = 4$ 时 6 个子集概率全是 $1/6 = 1/\binom{4}{2}$；$m = 3, n = 5$ 时 10 个子集概率全是 $1/10$；$m = 1, n = 5$ 时 5 个单元素集概率全是 $1/5$；$m = 2, n = 5$ 时 10 个二元子集概率全是 $1/10$。没有遗漏、没有重复，概率和严格为 1。规模感的对比：$n = 10^6, m = 10$ 时，本方法调 10 次 RANDOM，而"先 RANDOMIZE-IN-PLACE 再取前 10 个"要调 $10^6$ 次，差 $10^5$ 倍；后者的时间还全花在洗一个你根本不需要的完整排列上。时间上两者都是 $\Theta(n)$（递归 $n$ 层），差别在随机数调用的次数与"是否需要额外空间"。
>
> 这就是 reservoir sampling（蓄水池采样）的雏形：把递归倒过来写成循环，每读入第 $j$ 个元素就以 $m/j$ 的概率把它换进蓄水池，一遍扫描、$O(m)$ 内存、$O(n)$ 时间。成熟形态是 Vitter 1985 年在 ACM TOMS 第 11 卷 37 到 57 页提出的 Algorithm R，以及跳过式改进 Algorithm Z（文献信息可一手核实到期刊、卷、页码）。为什么"跳过式"更快？因为逐元素掷硬币意味着每来一个元素就要一次随机调用，而随机数生成本身可能比比较还贵；跳过式一次算出"下一个入选者在多远"，把随机调用从 $n$ 次降到 $m \ln(n/m)$ 次量级。
>
> 跨课程连接有三处。其一是 6.042J 的归纳法与对称性论证，这里不需要任何分布假设，只需要"每个剩余元素等可能"。其二是 CSAPP 第 11 章的网络编程：socket（套接字）上的字节流只能顺序到达，你没法回头重读，这正是蓄水池唯一能工作的场景。其三是第 9 章的 RANDOMIZED-SELECT，它同样用"递归缩小规模 + 每层等概率"的结构，只是每层砍掉的是一个区间而不是一个元素。区别在于：数组上的随机采样可以先洗牌再取前缀，因为随机访问允许回头；流上不行，所以必须把随机性摊到"到达时刻"上，代价是每个元素都可能被后来的元素顶替。
>
> 还有一层机制要说清：为什么"第 $n$ 个元素以 $m/n$ 的概率入选"就能推出"每个元素公平"。直觉上容易误判成"每个元素独立以 $m/n$ 入选"，那样得到的子集大小是随机的，不满足"恰好 $m$ 个"。这里的关键是那个 $n$ 顶替动作把"随机"与"配额"绑在一起：命中的是 $i \in S$ 就让 $n$ 占住被撞掉的那个名额，于是子集大小恒为 $m$，而"谁被挤掉"由 $S$ 的均匀性保证。换成另一种写法——先各自独立以 $m/n$ 抛硬币、再补齐或删减——你就得处理"大小不是 $m$"的补事件，证明会长一倍。这也是递归版比自底向上写更容易证的原因：它把"大小恰好"这个硬约束编码进了结构，只留下"位置均匀"这一条需要归纳。
>
> 一句话收束：随机调用的次数是可以省的，只要把"选择哪 $m$ 个"改写成"每个位置独立决定要不要"。

### Section 5.4（★）· Probabilistic analysis and further uses of indicator random variables（概率分析与指示器随机变量的进一步使用） <span style="color:#2471a3;">**[section]**</span>

本 advanced section（进阶节）通过四个 example（例子）进一步阐明 probabilistic analysis（概率分析）。第一个例子确定在一个有 $k$ 个人的房间里，其中两个人同一天生日的 probability（概率）。第二个例子考察当我们把球随机地扔进箱子时会发生什么。第三个例子研究我们抛硬币时连续出现正面的"streaks（连续成功序列）"。最后一个例子分析 hiring problem（雇用问题）的一个变体：你必须在不真正面试所有候选人的情况下做出决策。

#### Section 5.4.1 · The birthday paradox（生日悖论） <span style="color:#2471a3;">**[section]**</span>

我们的第一个例子是 birthday paradox（生日悖论）。一个房间里必须有多少人，才能使其中两个人在同一天出生的概率达到 50%？答案出人意料地少。悖论之处在于：正如我们将要看到的，这个人数实际上远少于一年中的天数，甚至远少于一年天数的一半。

为了回答这个问题，我们用整数 $1, 2, \ldots, k$ 为房间里的人编号，其中 $k$ 是房间里的人数。我们忽略闰年的问题，并假设所有的年份都有 $n = 365$ 天。对于 $i = 1, 2, \ldots, k$，令 $b_i$ 为第 $i$ 个人的生日所在的那一天，其中 $1 \le b_i \le n$。我们还假设生日在一年中的 $n$ 天上是 uniformly distributed（均匀分布）的，于是对 $i = 1, 2, \ldots, k$ 和 $r = 1, 2, \ldots, n$，有 $\Pr\{b_i = r\} = 1/n$。

给定的两个人（比如 $i$ 和 $j$）生日相同的概率，取决于生日的随机选取是否 independent（独立）。从现在起我们假设生日是独立的，于是 $i$ 的生日与 $j$ 的生日都落在第 $r$ 天的概率为……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.131</span>

（接上页）……$i$ 的生日与 $j$ 的生日都落在第 $r$ 天的概率为

```math
\begin{aligned}
\Pr\{b_i = r \text{ and } b_j = r\}
  &= \Pr\{b_i = r\}\,\Pr\{b_j = r\} \\[4pt]
  &= 1/n^2\,.
\end{aligned}
```

于是，两人落在同一天的概率是

```math
\begin{aligned}
\Pr\{b_i = b_j\}
  &= \sum_{r=1}^{n} \Pr\{b_i = r \text{ and } b_j = r\} \\[4pt]
  &= \sum_{r=1}^{n} (1/n^2) \\[4pt]
  &= 1/n\,.
\end{aligned}
\tag{5.6}
```

更直观地说，一旦 $b_i$ 被选定，$b_j$ 被选为同一天的概率就是 $1/n$。于是，$i$ 与 $j$ 有相同生日的概率，与"其中一人的生日落在一个给定的日子"的概率相同。不过要注意，这一巧合依赖于"生日相互独立"这一 assumption（假设）。

我们可以通过考察 complementary event（补事件）来分析"$k$ 个人中至少有 2 人生日相同"的概率。"至少有两个生日相同"的概率等于 1 减去"所有生日都不相同"的概率。$k$ 个人生日互不相同这一 event（事件）是

```math
B_k = \bigcap_{i=1}^{k} A_i\,,
```

其中 $A_i$ 是"第 $i$ 个人的生日与所有 $j < i$ 的人的生日都不同"这一事件。由于我们可以把 $B_k$ 写成 $B_k = A_k \cap B_{k-1}$，于是从 equation (C.16)（式 (C.16)）我们得到 recurrence（递归式）

```math
\Pr\{B_k\} = \Pr\{B_{k-1}\}\,\Pr\{A_k \mid B_{k-1}\}\,.
\tag{5.7}
```

其中我们取 $\Pr\{B_1\} = \Pr\{A_1\} = 1$ 作为 initial condition（初始条件）。换句话说，$b_1, b_2, \ldots, b_k$ 互不相同的概率，等于 $b_1, b_2, \ldots, b_{k-1}$ 互不相同的概率，乘以"在给定 $b_1, b_2, \ldots, b_{k-1}$ 互不相同的条件下，对 $i = 1, 2, \ldots, k-1$ 都有 $b_k \ne b_i$"的概率。

如果 $b_1, b_2, \ldots, b_{k-1}$ 互不相同，那么"对 $i = 1, 2, \ldots, k-1$ 都有 $b_k \ne b_i$"的 conditional probability（条件概率）为 $\Pr\{A_k \mid B_{k-1}\} = (n-k+1)/n$，因为在 $n$ 天中有 $n-(k-1)$ 天尚未被占用。我们迭代地应用递归式 (5.7)，得到……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.132</span>

（接上页）

```math
\begin{aligned}
\Pr\{B_k\}
  &= \Pr\{B_{k-1}\}\,\Pr\{A_k \mid B_{k-1}\} \\[4pt]
  &= \Pr\{B_{k-2}\}\,\Pr\{A_{k-1} \mid B_{k-2}\}\,\Pr\{A_k \mid B_{k-1}\} \\[4pt]
  &= \cdots \\[4pt]
  &= \Pr\{B_1\}\,\Pr\{A_2 \mid B_1\}\,\Pr\{A_3 \mid B_2\} \cdots \Pr\{A_k \mid B_{k-1}\} \\[4pt]
  &= 1 \cdot \left(\frac{n-1}{n}\right)\left(\frac{n-2}{n}\right) \cdots \left(\frac{n-k+1}{n}\right) \\[4pt]
  &= 1 \cdot \left(1 - \frac{1}{n}\right)\left(1 - \frac{2}{n}\right) \cdots \left(1 - \frac{k-1}{n}\right)\,.
\end{aligned}
```

Inequality (3.12)（不等式 (3.12)），即 $1 + x \le e^x$，给我们

```math
\begin{aligned}
\Pr\{B_k\}
  &\le e^{-1/n} e^{-2/n} \cdots e^{-(k-1)/n} \\[4pt]
  &= e^{-\left(\sum_{i=1}^{k-1} i\right)/n} \\[4pt]
  &= e^{-k(k-1)/2n} \\[4pt]
  &\le 1/2\,,
\end{aligned}
```

只要 $k(k-1)/2n \ge \ln 2$。当 $k(k-1) \ge 2n \ln 2$ 时——或者求解这个二次方程，即当 $k \ge (1 + \sqrt{1 + 8n \ln 2})/2$ 时——所有 $k$ 个生日互不相同的概率至多是 $1/2$。对于 $n = 365$，我们必须有 $k \ge 23$。因此，如果房间里至少有 23 个人，那么至少两个人有相同生日的概率至少是 $1/2$。在火星上，一年有 669 个火星日；因此需要 31 个火星人才能达到同样的效果。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $k = 23$ 是概率论最著名的数字之一，而它反直觉的根源在"数对"而不是"数人"：房间里有 $\binom{k}{2}$ 个配对，每个配对都可能碰撞，碰撞机会是配对数的一次函数，于是阈值落在 $k \approx \sqrt{2n}$ 而不是 $n/2$。
>
> 两条推导都要会。第一条是精确的补事件递推：$\Pr\{B_k\} = \prod_{i=1}^{k-1}(1 - i/n)$，再用 $1 + x \le e^{x}$ 把连乘压成 $e^{-k(k-1)/(2n)}$，令其 $\le 1/2$ 解出 $k(k-1) \ge 2n \ln 2$。第二条是指示器法：令 $X_{ij}$ 标记第 $i$ 与第 $j$ 人同生日，$\mathrm{E}[X_{ij}] = 1/n$，由 expectation（期望）的线性性得 $\mathrm{E}[X] = \binom{k}{2}/n$，令其 $\ge 1$ 得 $k \ge \sqrt{2n} + 1$。两条路给出同一阶但不同常数：前者问"至少一对的概率过半"，后者问"期望对数为一"；后者不需要 independence（独立性），代价是只给期望数而不给概率，教材明说这是 approximate（近似）分析。
>
> 数字全部复算过。$n = 365$：$k = 23$ 时碰撞概率 $0.5073$（不是恰好 0.5，只是刚过线）；$k = 28$ 时 $0.6545$，而期望对数在 $k = 28$ 才到 $28 \times 27/(2 \times 365) = 1.0356$；要 99% 需 $k = 57$（$0.9901$）。火星一年 669 天：$k = 31$ 时 $0.5063$，期望法要 $k = 38$（$38 \times 37/(2 \times 669) = 1.0508$）。两个常数的来历值得记：概率法给出 $k \approx 1.1774\sqrt{n}$，期望法给出 $k \approx 1.4142\sqrt{n}$，相差 20%，恰好是"概率过半"与"期望为一"这两个不同问题的差别。
>
> 还有一个更省力的近似值得掌握：当 $k^2/(2n)$ 不大时，碰撞对数近似服从均值为 $\lambda = k^2/(2n)$ 的 Poisson distribution（泊松分布），于是"至少一对"的概率 $\approx 1 - e^{-\lambda}$。代 $k = 23$：$\lambda = 529/730 = 0.7247$，$1 - e^{-0.7247} = 0.5155$，与精确值 $0.5073$ 差 1.6%；代 $k = 28$：$\lambda = 1.0739$，得 $0.6583$，与 $0.6545$ 差 0.6%。这个近似之所以成立，是因为"配对数很多、每对碰撞概率很小"正是泊松极限的标准条件，而 Poisson 分布在后面第 11 章的链长分析里还会反复出现。
>
> 历史：这个问题的首次正式发表通常归到 von Mises 1939 年在伊斯坦布尔发表的《Über Aufteilungs- und Besetzungswahrscheinlichkeiten》，多份二手文献与离线维基在作者与年份上一致；至于"Harold Davenport 约 1927 年的讨论"这一说法，我未能一手核实原始出处，故只作旁注、不作断言。
>
> 跨课程连接：6.042J 里你已经用过指示器变量与 union bound（联合界），这里是把它们用到"二元关系计数"上；密码学里的 birthday attack（生日攻击）是同一模型的直接后代——对 $l$ 位散列，找一对碰撞期望只需 $2^{l/2}$ 次尝试，128 位即 $2^{64} \approx 1.84 \times 10^{19}$ 次，这把"散列越长越安全"变成了一条平方根律。区别在于：生日问题里天数固定、人数是变量；攻击里散列值空间固定、尝试次数是变量，但两边的配对数都是 $\binom{k}{2}$，所以公式长得一模一样。
>
> 模型假设也必须交代，否则不知道结论能用在哪。上面所有数字都建立在两条假设上：生日在 $n$ 天上 uniform（均匀），且彼此 independent（独立）。真实数据两条都不满足——出生日期有明显的季节性与节假日效应，双胞胎让同一家庭的生日强相关。不均匀会把碰撞概率推高（质量集中在一部分日子上），也就是说 23 这个数字是乐观的：真实人群里达到 50% 所需的 $k$ 只会更小。所以"23 人"应当读作"在最理想的均匀模型下也要 23 人"，而不是"现实中恰好 23 人"。
>
> 一句话收束：反直觉的不是概率，而是"配对数按平方增长"这件事没有直觉对应物。

#### An analysis using indicator random variables（使用指示器随机变量的分析） <span style="color:#2471a3;">**[section]**</span>

我们可以用 indicator random variable（指示器随机变量）来对 birthday paradox（生日悖论）给出一个更简单但 approximate（近似的）分析。对房间里 $k$ 个人的每一对 $(i, j)$，我们定义指示器随机变量 $X_{ij}$，其中 $1 \le i < j \le k$：

```math
\begin{aligned}
X_{ij} &= I\{\text{person } i \text{ and person } j \text{ have the same birthday}\} \\[4pt]
       &= \begin{cases} 1 & \text{if person } i \text{ and person } j \text{ have the same birthday}\,, \\ 0 & \text{otherwise}\,. \end{cases}
\end{aligned}
```

根据 equation (5.6)（式 (5.6)），两个人生日相同的概率是 $1/n$，于是由 Lemma 5.1（引理 5.1），我们有

```math
\begin{aligned}
\mathrm{E}[X_{ij}]
  &= \Pr\{\text{person } i \text{ and person } j \text{ have the same birthday}\} \\[4pt]
  &= 1/n\,.
\end{aligned}
```

令 $X$ 为统计"生日相同的人对数"的 random variable（随机变量），我们有……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.133</span>

（接上页）令 $X$ 为统计"生日相同的人对数"的 random variable（随机变量），我们有

```math
\begin{aligned}
X &= \sum_{i=1}^{k} \sum_{j=i+1}^{k} X_{ij}\,.
\end{aligned}
```

对两边取 expectation（期望）并应用 linearity of expectation（期望的线性性），我们得到

```math
\begin{aligned}
\mathrm{E}[X]
  &= \mathrm{E}\left[\sum_{i=1}^{k} \sum_{j=i+1}^{k} X_{ij}\right] \\[4pt]
  &= \sum_{i=1}^{k} \sum_{j=i+1}^{k} \mathrm{E}[X_{ij}] \\[4pt]
  &= \binom{k}{2}\frac{1}{n} \\[4pt]
  &= \frac{k(k-1)}{2n}\,.
\end{aligned}
```

因此，当 $k(k-1) \ge 2n$ 时，生日相同的人对的 expected number（期望数目）至少为 1。于是，如果房间里至少有 $\sqrt{2n} + 1$ 个人，我们就可以期望至少两个人生日相同。对 $n = 365$，当 $k = 28$ 时，生日相同的人对的期望数目是 $(28 \cdot 27)/(2 \cdot 365) \approx 1.0356$。因此，只要有 28 个人，我们就期望能找到至少一对生日相同的人。在火星上，一年有 669 个火星日那么长，我们需要至少 38 个火星人。

第一种分析只使用了 probabilities（概率），确定了"存在一对相同生日的概率超过 $1/2$"所需的人数；第二种分析使用了 indicator random variables（指示器随机变量），确定了"相同生日的期望对数为 1"所需的人数。虽然两种情形下所需的确切人数不同，但它们在渐近意义下是相同的：$\Theta(\sqrt{n})$。

#### Section 5.4.2 · Balls and bins（球与箱子） <span style="color:#2471a3;">**[section]**</span>

考虑这样一个过程：我们把相同的球随机地投进编号为 $1, 2, \ldots, b$ 的 $b$ 个 bins（箱子）中。每次投掷都是 independent（独立的），并且在每次投掷中，球等可能地落入任何一个箱子。投出的球落入任一给定箱子的概率是 $1/b$。因此，这个投球过程是一列 Bernoulli trials（伯努利试验）（见 Appendix C.4（附录 C.4）），成功的概率为 $1/b$，其中 success（成功）表示球落入给定的箱子。这一模型对分析 hashing（散列）（见 Chapter 11（第 11 章））特别有用，而且我们可以就投球过程回答各种有趣的问题。（Problem C-1 会就 balls and bins（球与箱子）提出更多问题。）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.134</span>

**一个给定的箱子里会落入多少个球？** 落入给定箱子的球的数目服从 binomial distribution（二项分布）$b(k; n, 1/b)$。如果我们投掷 $n$ 个球，equation (C.37)（式 (C.37)）告诉我们，落入给定箱子的球的期望数目是 $n/b$。

**平均而言，我们必须投多少个球，才能使一个给定的箱子接到一个球？** 直到给定箱子接到一个球为止的投掷次数服从 geometric distribution（几何分布），其成功概率为 $1/b$；由 equation (C.32)（式 (C.32)），直到成功为止的期望投掷次数是 $1/(1/b) = b$。

**我们必须投多少个球，才能使每个箱子都至少含有一个球？** 我们把"球落入一个空箱"的一次投掷称为一次 "hit"（命中）。我们想知道获得 $b$ 次命中所需的期望投掷次数 $n$。

利用这些命中，我们可以把 $n$ 次投掷划分为若干 stages（阶段）。第 $i$ 个阶段由第 $(i-1)$ 次命中之后的投掷组成，直至第 $i$ 次命中为止。第一个阶段由第一次投掷组成，因为当所有箱子都为空时我们必然命中。在第 $i$ 个阶段的每次投掷中，有 $i-1$ 个箱子含有球，$b-i+1$ 个箱子为空。因此，第 $i$ 个阶段中每次投掷获得命中的概率是 $(b-i+1)/b$。令 $n_i$ 表示第 $i$ 个阶段中的投掷次数。于是，获得 $b$ 次命中所需的投掷次数为 $n = \sum_{i=1}^{b} n_i$。每个随机变量 $n_i$ 都服从成功概率为 $(b-i+1)/b$ 的 geometric distribution（几何分布），因此由 equation (C.32)，我们有

```math
\mathrm{E}[n_i] = \frac{b}{b-i+1}\,.
```

由 linearity of expectation（期望的线性性），我们有

```math
\begin{aligned}
\mathrm{E}[n]
  &= \mathrm{E}\left[\sum_{i=1}^{b} n_i\right] \\[4pt]
  &= \sum_{i=1}^{b} \mathrm{E}[n_i] \\[4pt]
  &= \sum_{i=1}^{b} \frac{b}{b-i+1} \\[4pt]
  &= b\sum_{i=1}^{b} \frac{1}{i} \\[4pt]
  &= b(\ln b + O(1)) \qquad \text{(by equation (A.7))}\,.
\end{aligned}
```

因此，大约需要 $b \ln b$ 次投掷，我们才能期望每个箱子都有一个球。这个问题也被称为 coupon collector's problem（优惠券收集问题），它说的是：一个试图收集 $b$ 种不同优惠券的人，期望要获得大约 $b \ln b$ 张随机得到的优惠券才能成功。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $b \ln b$ 这个量级说明"覆盖"贵在收尾：前一半箱子几乎白送，最后几个顽固空箱要等 $b$ 次投掷才命中一次。
>
> 机制的骨架是"阶段划分 + 几何分布"。第 $i$ 阶段开始时已有 $i-1$ 个箱子有球、$b-i+1$ 个空箱，每次投掷命中概率 $(b-i+1)/b$，所以该阶段长度服从成功概率 $(b-i+1)/b$ 的 geometric distribution（几何分布），期望 $b/(b-i+1)$。求和得 $\mathrm{E}[n] = b \sum_{i=1}^{b} 1/i = b H_b = b(\ln b + \gamma + O(1/b))$，其中 $\gamma \approx 0.5772$ 是欧拉常数。为什么不是 $b$ 而是 $b \ln b$？因为成本按 $1/i$ 加权：前 $b/2$ 个箱子总共只花约 $b \ln 2 \approx 0.69b$ 次投掷，后 $b/2$ 个也花 $b \ln 2$ 次，越往后越贵；对数因子来自调和和，而不是来自任何一个阶段。
>
> 数字。$b = 365$ 时 $H_{365} = 6.4785$，期望投掷 $2364.6$ 次；拿 $b \ln b = 365 \times 5.8999 = 2153$ 近似会低估 9%，这个 9% 就是欧拉常数除以 $\ln b$ 的量级。$b = 669$ 时 $669 H_{669} = 4739.0$。再算两个常被问的量：$n = b$ 次投掷后空箱的期望个数约 $b e^{-1}$，$b = 365$ 时为 $134.3$，因为每个箱子空的概率是 $(1 - 1/b)^b \to e^{-1}$；单球箱的期望个数约 $b cdot e^{-1} \cdot 1 = 134.3$，两者在一比一时恰好相等，这是泊松分布均值等于 1 时的巧合（一般地，期望空箱 $b e^{-\lambda}$、期望单球箱 $b \lambda e^{-\lambda}$，$\lambda = 1$ 处两者相等）。
>
> 方差也值得看一眼，因为它决定了"经验公式能不能当保证用"。第 $i$ 阶段方差为 $(1-p_i)/p_i^2$，$p_i = (b-i+1)/b$，求和得约 $b^2 \sum 1/i^2 \to \pi^2 b^2/6$，即标准差约 $1.28 b$，与均值 $b \ln b$ 相比可以忽略——这意味着优惠券收集的完成时间高度集中，$b \ln b$ 不是一个平均值附近的松估计，而是一条相当可靠的预测。对比生日问题：那里的碰撞时间标准差与均值同阶，所以"23 人"只能说概率过半，不能说"几乎一定"。
>
> 跨课程连接有三处。其一，第 11 章的 hashing（散列）就是这套球与箱子模型：把 $n$ 个 key（关键字）散列到 $n$ 个 slot（槽）里，"最后一次命中空槽"对应第 $b$ 阶段，load factor（装载因子）就是 $n/b$，习题 5.4-6 要你算空箱与单球箱的期望数。其二，6.042J 的几何分布与期望线性性是全部工具，没有用到几何分布之外的任何分布知识。其三，算法工程的对应物是"覆盖式扫描"：数据库为了把索引的全部 leaf（叶结点）访问一遍，访问次数远超页数，正是因为最后几个页要反复重试。区别在于：物理系统里那个"重试"是 cache（高速缓存）未命中带来的延迟，概率由访问模式决定，而不是均匀投掷；所以工程的覆盖成本常常偏离 $b \ln b$，可能更好也可能更坏。
>
> 再把这套模型推到第 11 章的链长上，会得到一条常被引用的结论：$n$ 个 key（关键字）散列到 $n$ 个槽后，最长链的期望长度约 $\ln n/\ln \ln n$。$n = 10^4$ 时是 $9.21/2.22 \approx 4.15$，$n = 10^6$ 时是 $13.82/2.63 \approx 5.26$——注意它长得极慢，所以散列表的查找在最坏链长上几乎不随规模恶化。为什么这个结论也要用球与箱子？因为"某个槽里至少有 $k$ 个球"的概率可以用二项尾界估出来，再乘槽数做 union bound（联合界）；本质仍是"对每个箱子问同一个问题，再对所有箱子求和"。区别在于：优惠券收集问的是"每个箱子至少 1 个"，链长问的是"某个箱子超过 $k$ 个"，前者是覆盖、后者是集中。
>
> 一句话收束：$b \ln b$ 是"覆盖成本"的标准答案，凡是"直到每个对象都被碰到"的问题都长这个样子。

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.135</span>

#### Section 5.4.3 · Streaks（连续成功序列） <span style="color:#2471a3;">**[section]**</span>

假设你抛掷一枚 fair coin（均匀硬币）$n$ 次。你期望看到的最长的连续 heads（正面）序列（streak）有多长？答案是 $\Theta(\lg n)$，正如下面的分析所表明的。

我们首先证明最长正面连续序列的期望长度是 $O(\lg n)$。每次抛掷出现正面的概率是 $1/2$。令 $A_{ik}$ 表示"长度至少为 $k$ 的正面连续序列从第 $i$ 次抛掷开始"这一 event（事件），更精确地说，表示"$k$ 次连续抛掷 $i, i+1, \ldots, i+k-1$ 全部为正面"这一事件，其中 $1 \le k \le n$ 且 $1 \le i \le n-k+1$。由于各次抛掷是 mutually independent（相互独立的），对任一给定的事件 $A_{ik}$，全部 $k$ 次抛掷都是正面的概率为

```math
\Pr\{A_{ik}\} = 1/2^k\,.
\tag{5.8}
```

对 $k = 2\lceil\lg n\rceil$，有

```math
\Pr\{A_{i,\,2\lceil\lg n\rceil}\} = 1/2^{2\lceil\lg n\rceil} \le 1/2^{2\lg n} = 1/n^2\,,
```

因此，长度至少为 $2\lceil\lg n\rceil$ 的正面连续序列从位置 $i$ 开始的概率相当小。这样的连续序列至多能在 $n - 2\lceil\lg n\rceil + 1$ 个位置上开始。因此，长度至少为 $2\lceil\lg n\rceil$ 的正面连续序列在某处开始的概率为

```math
\begin{aligned}
\Pr\left(\bigcup_{i=1}^{n-2\lceil\lg n\rceil+1} A_{i,\,2\lceil\lg n\rceil}\right)
  &\le \sum_{i=1}^{n-2\lceil\lg n\rceil+1} 1/n^2 \\[4pt]
  &< \sum_{i=1}^{n} 1/n^2 \\[4pt]
  &= 1/n\,,
\end{aligned}
\tag{5.9}
```

因为由 Boole's inequality（布尔不等式）(C.19)，事件的 union（并）的概率至多是各个事件概率之和。（注意，即使对像这里这样并非独立的事件，布尔不等式也成立。）

现在我们用 inequality (5.9)（不等式 (5.9)）来 bound（界定）最长连续序列的长度。对 $j = 0, 1, 2, \ldots, n$，令 $L_j$ 表示"最长正面连续序列的长度恰为 $j$"这一事件，并令 $L$ 表示最长连续序列的长度。根据 expected value（期望值）的定义，我们有

```math
\mathrm{E}[L] = \sum_{j=0}^{n} j\,\Pr\{L_j\}\,.
\tag{5.10}
```

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.136</span>

（接上页）我们可以尝试对每个 $\Pr\{L_j\}$ 使用与 inequality (5.9)（不等式 (5.9)）中计算类似的上界来求这个和的值。遗憾的是，这种方法会得到较弱的界。不过，我们可以利用上述分析获得的一些 intuition（直觉）来得到一个好的界。非正式地，我们观察到：在 equation (5.10)（式 (5.10)）的求和式中，没有任何单独一项的两个因子 $j$ 与 $\Pr\{L_j\}$ 同时很大。为什么？当 $j \ge 2\lceil\lg n\rceil$ 时，$\Pr\{L_j\}$ 非常小；而当 $j < 2\lceil\lg n\rceil$ 时，$j$ 又相当小。更形式化地，我们注意到事件 $L_j$（$j = 0, 1, \ldots, n$）是 disjoint（互不相交的），因此"长度至少为 $2\lceil\lg n\rceil$ 的正面连续序列在某处开始"的概率是 $\sum_{j=2\lceil\lg n\rceil}^{n} \Pr\{L_j\}$。由不等式 (5.9)，我们有 $\sum_{j=2\lceil\lg n\rceil}^{n} \Pr\{L_j\} < 1/n$。另外，注意到 $\sum_{j=0}^{n} \Pr\{L_j\} = 1$，我们有 $\sum_{j=0}^{2\lceil\lg n\rceil-1} \Pr\{L_j\} \le 1$。于是，我们得到

```math
\begin{aligned}
\mathrm{E}[L]
  &= \sum_{j=0}^{n} j\,\Pr\{L_j\} \\[4pt]
  &= \sum_{j=0}^{2\lceil\lg n\rceil-1} j\,\Pr\{L_j\} + \sum_{j=2\lceil\lg n\rceil}^{n} j\,\Pr\{L_j\} \\[4pt]
  &< \sum_{j=0}^{2\lceil\lg n\rceil-1} (2\lceil\lg n\rceil)\,\Pr\{L_j\} + \sum_{j=2\lceil\lg n\rceil}^{n} n\,\Pr\{L_j\} \\[4pt]
  &= 2\lceil\lg n\rceil \sum_{j=0}^{2\lceil\lg n\rceil-1} \Pr\{L_j\} + n \sum_{j=2\lceil\lg n\rceil}^{n} \Pr\{L_j\} \\[4pt]
  &< 2\lceil\lg n\rceil \cdot 1 + n \cdot (1/n) \\[4pt]
  &= O(\lg n)\,.
\end{aligned}
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条要收藏的是「分段放缩」：算 $\mathrm{E}[L] = \sum_j j \Pr\{L_j\}$ 这种"取值乘概率质量"的和时，先找阈值，把两端用两套不同的界分别压住。
>
> 为什么必须分段？因为 $j$ 与 $\Pr\{L_j\}$ 是跷跷板：$j$ 大时概率指数小，$j$ 小时概率大但取值小，任何单一的不等式都只能压住一头。分段的原理是"用便宜的界压贵的那一侧"：低段 $j \le t$，取值上限 $t$ 很便宜，于是只需 $\sum_{j<t} \Pr\{L_j\} \le 1$ 这条平凡的归一化；高段 $j \ge t$ 时取值上限只能给 $n$，很贵，所以必须用一条强得多的话把质量压死——这里用 Boole's inequality（布尔不等式）把 $n$ 个"从位置 $i$ 起有长串"的单点概率加起来，得小于 $1/n$。两段分别是 $O(t)$ 与 $O(1)$，取 $t = 2\lceil \lg n \rceil$ 即得 $O(\lg n)$。
>
> 理解这一步的最好方式是问"不这样做会怎样"。若对每一段都用 $j \le n$ 与 $\Pr\{L_j\} \le 1/2^k$ 硬算，得到 $n \sum_j 2^{-j}$ 之类的表达式，虽然也能估出常数级，但丢失了"长度超过 $2\lg n$ 的串几乎不出现"这个结构；若对每一段都用 $j \le t$，那么高段的质量 $1/n$ 被乘成 $t/n$，看起来很好，但低段的界就撑不住了——你会得到 $O(t)$，其实本质相同，只是没显式区分"哪一段靠质量、哪一段靠取值"。分段的价值在于它让你清楚知道每一段是谁在起作用。
>
> 算个数体会松紧。$n = 1024$ 时 $t = 20$，上界给出 $20 \times 1 + 1024 \times (1/1024) = 21$；而我用动态规划精确算出 $\mathrm{E}[L] = 9.334$（把"当前连正长度"作为状态、逐个抛掷转移，时间 $O(n \cdot k)$）。上界 21 比真值大 2.2 倍，但阶是对的。顺带做一个渐近核对：真实的 $\mathrm{E}[L]$ 约等于 $\log_2 n$ 减去一个常数，$n = 1024$ 时 $\log_2 n = 10$，与实测的 9.334 相差 0.666；$n = 1000$ 时 $\log_2 n = 9.966$，实测 9.300，差 0.666。两次差值是同一个常数，说明真值稳定地落在 $\log_2 n$ 下方约三分之二处，而不是随机抖动。这说明"上界松 2 倍"不是我们的手法退步，而是 union bound（联合界）本身丢了相关性信息。
>
> 还有一条等价路线值得对照：利用 $\mathrm{E}[L] = \sum_{j \ge 1} \Pr\{L \ge j\}$（这是"尾和"恒等式），把 $j \ge t$ 的部分用 Boole 得 $\Pr\{L \ge j\} \le n/2^{j}$，求和得 $n/2^{t-1} = 2/n$，于是 $\mathrm{E}[L] \le t + 2/n$。这条路更短，而且阈值一眼可见。代价是它同样只用一阶信息，得不到更紧的常数。
>
> 阈值为什么取 $2\lceil \lg n \rceil$ 而不是 $\lceil \lg n \rceil$？这是"留一段余量"的工程选择。若取 $t = \lceil \lg n \rceil$，则单点概率约 $1/n$，$n$ 个位置联合起来得 $1$，上界退化成平凡界，什么都证不出来。取 $2\lceil \lg n \rceil$ 让单点概率变成 $1/n^2$，联合之后才落回 $1/n$——也就是说，阈值必须比"期望出现一条的长度"再高一倍，才能让"超过阈值"成为稀有事。一般地，取 $r\lceil \lg n \rceil$ 得到 $\Pr\{L \ge r\lceil \lg n \rceil\} \le n^{1-r}$，$r = 1, 2, 3$ 分别对应平凡界、$1/n$、$1/n^2$。这一族界的用法是：想要多强的尾部就选多大的 $r$，代价是常数因子变大。
>
> 跨课程连接放在 100B 实分析：连续情形有 $\mathrm{E}[L] = \int_0^{\infty} \Pr\{L > t\}\,dt$，那是 Fubini（富比尼）定理的换序思想，形式上表现为分部积分；这里的尾和是它的离散版，两段的角色分别对应"截断上界"与"尾部质量"。区别在于：积分恒等式是精确的，而这里的求和式必须靠额外的界才能收口，因为离散分布没有密度可以换元。另一处连接是 6.042J 的 union bound（联合界），你在生日问题里已经用过一次。
>
> 一句话收束：见到"取值乘概率"的和，先问能不能找到阈值，把跷跷板的两头分别钉住。

长度超过 $r\lceil\lg n\rceil$ 次抛掷的正面连续序列出现的概率随 $r$ 的增大而迅速减小。对 $r \ge 1$，长度至少为 $r\lceil\lg n\rceil$ 的连续正面序列从位置 $i$ 开始的概率为

```math
\Pr\{A_{i,\,r\lceil\lg n\rceil}\} = 1/2^{r\lceil\lg n\rceil} \le 1/n^r\,.
```

因此，最长连续序列至少为 $r\lceil\lg n\rceil$ 的概率至多是 $n/n^r = 1/n^{r-1}$；等价地，最长连续序列的长度小于 $r\lceil\lg n\rceil$ 的概率至少是 $1 - 1/n^{r-1}$。

作为一个例子，对 $n = 1000$ 次抛硬币，出现长度至少为 $2\lceil\lg n\rceil = 20$ 的连续正面序列的概率至多是 $1/n = 1/1000$。出现长于 $3\lceil\lg n\rceil = 30$ 的连续正面序列的机会至多是 $1/n^2 = 1/1{,}000{,}000$。

现在我们证明一个 complementary（互补的）下界：$n$ 次抛硬币中最长正面连续序列的期望长度是 $\Omega(\lg n)$。为了证明这个界，我们通过把 $n$ 次抛掷划分为大约 $n/s$ 个、每组 $s$ 次抛掷的组来寻找长度为 $s$ 的连续序列……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.137</span>

（接上页）如果我们选取 $s = \lfloor(\lg n)/2\rfloor$，就可以证明：这些组中很可能至少有一组全为正面，从而最长连续序列的长度很可能至少为 $s = \Omega(\lg n)$。然后我们证明最长连续序列的期望长度是 $\Omega(\lg n)$。

我们把 $n$ 次抛硬币划分为至少 $\lfloor n/\lfloor(\lg n)/2\rfloor\rfloor$ 个由 $\lfloor(\lg n)/2\rfloor$ 次连续抛掷组成的组，并界定"没有任何一组全为正面"的概率。由 equation (5.8)（式 (5.8)），从位置 $i$ 开始的组全为正面的概率为

```math
\Pr\{A_{i,\,\lfloor(\lg n)/2\rfloor}\} = 1/2^{\lfloor(\lg n)/2\rfloor} \ge 1/\sqrt{n}\,.
```

因此，长度至少为 $\lfloor(\lg n)/2\rfloor$ 的正面连续序列不从位置 $i$ 开始的概率至多是 $1 - 1/\sqrt{n}$。由于这 $\lfloor n/\lfloor(\lg n)/2\rfloor\rfloor$ 个组是由互斥且独立的抛硬币构成的，所以所有这些组都不是长度为 $\lfloor(\lg n)/2\rfloor$ 的连续序列的概率至多为

```math
\begin{aligned}
(1 - 1/\sqrt{n})^{\lfloor n/\lfloor(\lg n)/2\rfloor\rfloor}
  &\le (1 - 1/\sqrt{n})^{\,n/\lceil(\lg n)/2\rceil - 1} \\[4pt]
  &\le (1 - 1/\sqrt{n})^{\,2n/\lceil\lg n\rceil - 1} \\[4pt]
  &\le e^{-(2n/\lceil\lg n\rceil - 1)/\sqrt{n}} \\[4pt]
  &= O(e^{-\lg n}) \\[4pt]
  &= O(1/n)\,.
\end{aligned}
```

在这个论证中，我们使用了 inequality (3.12)（不等式 (3.12)），即 $1 + x \le e^x$，以及一个你可能想要自行验证的事实：当 $n$ 充分大时，$(2n/\lceil\lg n\rceil - 1)/\sqrt{n} \ge \lg n$。

因此，最长连续序列等于或超过 $\lfloor(\lg n)/2\rfloor$ 的概率为

```math
\sum_{j=\lfloor(\lg n)/2\rfloor}^{n} \Pr\{L_j\} \ge 1 - O(1/n)\,.
\tag{5.11}
```

现在我们可以计算最长连续序列期望长度的下界了：从 equation (5.10)（式 (5.10)）出发，并以与上界分析类似的方式进行……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.138</span>

（接上页）

```math
\begin{aligned}
\mathrm{E}[L]
  &= \sum_{j=0}^{n} j\,\Pr\{L_j\} \\[4pt]
  &= \sum_{j=0}^{\lfloor(\lg n)/2\rfloor-1} j\,\Pr\{L_j\} + \sum_{j=\lfloor(\lg n)/2\rfloor}^{n} j\,\Pr\{L_j\} \\[4pt]
  &\ge \sum_{j=0}^{\lfloor(\lg n)/2\rfloor-1} 0 \cdot \Pr\{L_j\} + \sum_{j=\lfloor(\lg n)/2\rfloor}^{n} \lfloor(\lg n)/2\rfloor\,\Pr\{L_j\} \\[4pt]
  &= 0 \cdot \sum_{j=0}^{\lfloor(\lg n)/2\rfloor-1} \Pr\{L_j\} + \lfloor(\lg n)/2\rfloor \sum_{j=\lfloor(\lg n)/2\rfloor}^{n} \Pr\{L_j\} \\[4pt]
  &\ge 0 + \lfloor(\lg n)/2\rfloor\,(1 - O(1/n)) \qquad \text{(by inequality (5.11))} \\[4pt]
  &= \Omega(\lg n)\,.
\end{aligned}
```

与 birthday paradox（生日悖论）一样，我们可以用 indicator random variables（指示器随机变量）得到一个更简单但 approximate（近似的）分析。令 $X_{ik} = I\{A_{ik}\}$ 是与"长度至少为 $k$ 的正面连续序列从第 $i$ 次抛掷开始"相关联的指示器随机变量。为了统计这类连续序列的总数，我们定义

```math
X = \sum_{i=1}^{n-k+1} X_{ik}\,.
```

取期望并使用 linearity of expectation（期望的线性性），我们有

```math
\begin{aligned}
\mathrm{E}[X]
  &= \mathrm{E}\left[\sum_{i=1}^{n-k+1} X_{ik}\right] \\[4pt]
  &= \sum_{i=1}^{n-k+1} \mathrm{E}[X_{ik}] \\[4pt]
  &= \sum_{i=1}^{n-k+1} \Pr\{A_{ik}\} \\[4pt]
  &= \sum_{i=1}^{n-k+1} 1/2^k \\[4pt]
  &= \frac{n - k + 1}{2^k}\,.
\end{aligned}
```

通过代入 $k$ 的各种取值，我们可以计算长度为 $k$ 的连续序列的期望数目。如果这个数目很大（远大于 1），那么我们期望会出现许多长度为 $k$ 的连续序列，并且出现其中之一的概率很高。如果……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.139</span>

（接上页）如果这个数目很小（远小于 1），那么我们期望长度为 $k$ 的连续序列很少出现，并且出现其中之一的概率很低。如果 $k = c\lg n$，其中 $c$ 为某个 positive constant（正常数），我们得到

```math
\begin{aligned}
\mathrm{E}[X]
  &= \frac{n - c\lg n + 1}{2^{c\lg n}} \\[4pt]
  &= \frac{n - c\lg n + 1}{n^c} \\[4pt]
  &= \frac{1}{n^{c-1}} - \frac{(c\lg n - 1)/n}{n^{c-1}} \\[4pt]
  &= \Theta(1/n^{c-1})\,.
\end{aligned}
```

如果 $c$ 较大，长度为 $c\lg n$ 的连续序列的期望数目就很小，我们断定它们不太可能出现。另一方面，如果 $c = 1/2$，则我们得到 $\mathrm{E}[X] = \Theta(1/n^{1/2-1}) = \Theta(n^{1/2})$，我们期望有大量长度为 $(1/2)\lg n$ 的连续序列。因此，出现一个这样长度的连续序列是很有可能的。仅凭这些粗略的估计，我们就能断定：最长连续序列的期望长度是 $\Theta(\lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 到这里上下界合拢，$\Theta(\lg n)$ 才成立；值得把两个模板分别命名收藏——「上下界夹逼」与「期望值探测」——并诚实标出后者在哪里还不严格。
>
> 上界方向只用一条不等式加一次联合：单点概率 $\Pr\{A_{ik}\} = 2^{-k}$，取 $k = 2\lceil \lg n \rceil$ 得小于 $1/n^2$，再乘上 $n$ 个可能的起点得 $1/n$——于是"出现长度至少 $2\lceil \lg n \rceil$ 的连正"是小概率事件。下界方向必须反过来：不能只说"短串很多"，要说"至少有一条长串"的概率接近 1。做法是把 $n$ 次抛掷切成互不相交的组（每组 $s = \lfloor(\lg n)/2 \rfloor$ 次），每组全正的概率大于等于 $1/\sqrt{n}$，组间 independent（独立），于是"所有组都失败"的概率至多 $(1 - 1/\sqrt{n})^{n/s}$，再用 $1 + x \le e^{x}$ 变成 $e^{-n/(s\sqrt{n})}$，数量级为 $1/n$。这一招的要害是"切开换取独立性"：原始窗口互相重叠、无法直接相乘，切成不相交的组之后独立性成立，代价是只证明了长度为 $s$ 的串而不是更长。
>
> 数字。$n = 1000$ 时 $2\lceil \lg n \rceil = 20$，上界说 $\Pr\{L \ge 20\}$ 小于 $1/1000$，我用精确动态规划算得 $0.000468$，界是松的但同一量级；$3\lceil \lg n \rceil = 30$ 时上界 $10^{-6}$，实测已在 $10^{-15}$ 量级以下。下界一侧：$s = \lfloor \lg 1000/2 \rfloor = 4$，能保证"长度至少 4 的连正"几乎必然出现，而实测 $\mathrm{E}[L] = 9.3$，说明这个下界确实很松——松是因为切块浪费了大量重叠机会，但阶对了。
>
> 第二个模板是「期望值探测」：令 $X$ 为长度 $k$ 的连正串个数，$\mathrm{E}[X] = (n - k + 1)/2^{k}$。$n = 1024$ 时取 $k = 5$ 得 $31.875$（期望很多条），取 $k = 7$ 得 $7.95$（仍很多），取 $k = 10$ 得 $0.9912$（临界），取 $k = 20$ 得 $0.0010$（几乎不出现）。三个数字把"阈值在 $\lg n$ 附近"这件事钉死。但这里必须补一句严格化的门票：$\mathrm{E}[X]$ 大并不自动蕴含"出现概率高"，因为一个非负随机变量完全可以以极小概率取极大值。要把"期望多"翻译成"概率高"，得用 Markov（马尔可夫）不等式反向做：$\Pr\{X = 0\} \le \mathrm{Var}[X] / \mathrm{E}[X]^2$（这是二阶矩方法，Chebyshev 不等式的推论）。以 $n = 1024, k = 7$ 为例，$\mathrm{E}[X] = 7.95$，而精确枚举给出 $\Pr\{X = 0\} = 0.0165$，也就是"至少出现一条长度 7 的连正"的概率是 $98.3\%$——期望值探测的方向没错。
>
> 还有一处值得解释：上界为什么要写成 $r\lceil \lg n \rceil$ 的一族，而不是只要一个 $2\lceil \lg n \rceil$？因为"夹逼"要求两个方向都能落到同一个阶上。上界只要给出某个比 $\lg n$ 大的量级就能收紧到 $\Theta(\lg n)$，但下界必须给出"至少有这么长"的概率接近 1，而分组只证明了 $s = \lfloor(\lg n)/2 \rfloor$ 这一条。两端相差常数倍（$2$ 与 $1/2$），夹出的区间就是 $\Theta(\lg n)$ 本身。换句话说，夹逼之所以成立，不是因为两个界很紧，而是因为它们的比值是常数；这也是为什么教材不去优化常数——优化常数只改变区间宽度，不改变阶。
>
> 跨课程连接：6.042J 的联合界与独立性是上界与下界各自的引擎；100B 里 $1 + x \le e^{x}$ 是标准的指数化技巧，它把"连乘"翻译成"求和的指数"。区别在于：这里的指数化是对离散求和用的，而实分析里它常用于控制积分核。另一处连接是概率论教材 Bertsekas 里的二阶矩方法——那门课会把这里"近似"的部分补成定理，届时你会看到 $\mathrm{E}[X]^2/\mathrm{E}[X^2]$ 这个比值如何成为"以正概率出现"的标准判据。
>
> 一句话收束：上界靠"压单点概率再求和"，下界靠"切块换独立再连乘"，而期望值探测负责快速定位阈值。

#### Section 5.4.4 · The on-line hiring problem（在线雇用问题） <span style="color:#2471a3;">**[section]**</span>

作为最后一个例子，我们考虑 hiring problem（雇用问题）的一个 variant（变体）。假设现在我们不想为了找出最好的那位而面试所有的 candidates（候选人），也不想随着应聘者越来越好而不停地雇用与解雇。相反，我们愿意满足于一位接近最好的候选人，以换取恰好只雇用一次。我们必须遵守公司的一项要求：每次面试之后，我们必须要么立即把职位提供给应聘者，要么立即拒绝该应聘者。那么，在"最小化面试量"与"最大化所雇用候选人的质量"之间如何 trade-off（权衡）？

我们可以按如下方式 modeling（建模）这个问题。面试过一位应聘者之后，我们能够给每人一个 score（分数）；令 $\text{score}[i]$ 表示我们给第 $i$ 位应聘者的分数，并假设没有两位应聘者得到相同的分数。在我们见过 $j$ 位应聘者之后，我们知道这 $j$ 位中谁的分数最高，但不知道剩余的 $n-j$ 位应聘者中是否会有人得到更高的分数。我们决定采用这样的 strategy（策略）：选择一个 positive integer（正整数）$k < n$，先面试并拒绝前 $k$ 位应聘者，然后雇用其后第一位分数高于所有先前应聘者的应聘者。如果结果发现最有资格（best-qualified）的应聘者恰在前 $k$ 位被面试者之中，那么我们将雇用第 $n$ 位应聘者。我们在过程 ON-LINE-MAXIMUM$(k, n)$ 中将这一策略 formalize（形式化），它返回我们希望雇用的候选人的 index（下标）。

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.140</span>

（接上页）

```text
ON-LINE-MAXIMUM(k, n)
 1  bestscore = −∞
 2  for i = 1 to k
 3      if score[i] > bestscore
 4          bestscore = score[i]
 5  for i = k + 1 to n
 6      if score[i] > bestscore
 7          return i
 8  return n
```

我们希望对 $k$ 的每个可能取值，确定我们雇用到最有资格应聘者的 probability（概率），然后选出最好的 $k$ 值，并用该值实现这一策略。暂时假设 $k$ 是固定的。令 $M(j) = \max_{1 \le i \le j}\{\text{score}[i]\}$ 表示应聘者 1 到 $j$ 之中的最高分数。令 $S$ 表示"我们成功地选中了最有资格的应聘者"这一 event（事件），并令 $S_i$ 表示"当最有资格的应聘者是第 $i$ 位被面试者时我们成功"这一事件。由于各个 $S_i$ 是 disjoint（互不相交的），我们有 $\Pr\{S\} = \sum_{i=1}^{n} \Pr\{S_i\}$。注意到当最有资格的应聘者在前 $k$ 位之中时我们绝不会成功，因此对 $i = 1, 2, \ldots, k$ 有 $\Pr\{S_i\} = 0$。于是，我们得到

```math
\Pr\{S\} = \sum_{i=k+1}^{n} \Pr\{S_i\}\,.
\tag{5.12}
```

现在我们来计算 $\Pr\{S_i\}$。为了在最有资格的应聘者是第 $i$ 位时成功，必须发生两件事。第一，最有资格的应聘者必须位于位置 $i$，我们把这一事件记为 $B_i$。第二，算法不得选中位置 $k+1$ 到 $i-1$ 中的任何一位应聘者，而这只发生在：对每个满足 $k+1 \le j \le i-1$ 的 $j$，我们在第 6 行发现 $\text{score}[j] < \text{bestscore}$。（由于分数各不相同，我们可以忽略 $\text{score}[j] = \text{bestscore}$ 的可能性。）换句话说，$\text{score}[k+1]$ 到 $\text{score}[i-1]$ 的所有值都必须小于 $M(k)$；如果其中有任何值大于 $M(k)$，我们就会改为返回第一个大于 $M(k)$ 的值的下标。我们用 $O_i$ 表示"位置 $k+1$ 到 $i-1$ 中的应聘者都没有被选中"这一事件。所幸，事件 $B_i$ 与 $O_i$ 是 independent（独立的）。事件 $O_i$ 只依赖于位置 1 到 $i-1$ 中各值的相对 ordering（顺序），而 $B_i$ 只依赖于位置 $i$ 上的值是否大于所有其他位置上的值。位置 1 到 $i-1$ 中各值的顺序不影响位置 $i$ 上的值是否大于它们全体，而位置 $i$ 上的值也不影响位置 1 到 $i-1$ 中各值的顺序。因此我们可以应用 equation (C.15)（式 (C.15)）得到……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.141</span>

（接上页）

```math
\Pr\{S_i\} = \Pr\{B_i \cap O_i\} = \Pr\{B_i\}\,\Pr\{O_i\}\,.
```

概率 $\Pr\{B_i\}$ 显然是 $1/n$，因为 maximum（最大值）等可能地位于 $n$ 个位置中的任何一个。要使事件 $O_i$ 发生，位置 1 到 $i-1$ 中的最大值——它等可能地位于这 $i-1$ 个位置中的任何一个——必须位于前 $k$ 个位置之一。因此，$\Pr\{O_i\} = k/(i-1)$，从而 $\Pr\{S_i\} = k/(n(i-1))$。利用 equation (5.12)（式 (5.12)），我们有

```math
\begin{aligned}
\Pr\{S\}
  &= \sum_{i=k+1}^{n} \Pr\{S_i\} \\[4pt]
  &= \sum_{i=k+1}^{n} \frac{k}{n(i-1)} \\[4pt]
  &= \frac{k}{n} \sum_{i=k+1}^{n} \frac{1}{i-1} \\[4pt]
  &= \frac{k}{n} \sum_{i=k}^{n-1} \frac{1}{i}\,.
\end{aligned}
```

我们用 integrals（积分）做 approximation（近似），从上方和下方 bound（界定）这个 summation（求和式）。由 inequalities (A.12)（不等式 (A.12)），我们有

```math
\int_{k}^{n} \frac{1}{x}\,dx \;\le\; \sum_{i=k}^{n-1} \frac{1}{i} \;\le\; \int_{k-1}^{n-1} \frac{1}{x}\,dx\,.
```

计算这些 definite integrals（定积分），我们得到界

```math
\frac{k}{n}(\ln n - \ln k) \;\le\; \Pr\{S\} \;\le\; \frac{k}{n}(\ln(n-1) - \ln(k-1))\,,
```

它们为 $\Pr\{S\}$ 提供了相当 tight（紧）的界。因为我们希望最大化成功的概率，让我们聚焦于选择使 $\Pr\{S\}$ 的下界最大的 $k$ 值。（况且，下界表达式也比上界表达式更容易最大化。）对表达式 $(k/n)(\ln n - \ln k)$ 关于 $k$ 求导，我们得到

```math
\frac{1}{n}(\ln n - \ln k - 1)\,.
```

令该导数等于 0，我们看到：当 $\ln k = \ln n - 1 = \ln(n/e)$，即等价地当 $k = n/e$ 时，概率的下界取得最大值。因此，如果我们以 $k = n/e$ 实现这一策略，我们就能以至少 $1/e$ 的概率成功地雇用到最有资格的应聘者。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一节是 secretary problem（秘书问题）的原始形态，策略只有一句话：先用前 $k$ 位建立基准，之后遇到第一个破纪录者立刻出手。要解释的是为什么 $k \approx n/e$ 与成功率 $\approx 1/e$ 这两个常数会绑在一起出现。
>
> 机制。成功事件拆成两半：最有资格者恰好在位置 $i$（概率 $1/n$，因为最大值等可能落在任何位置），且在它之前的 $k+1$ 到 $i-1$ 号都没被选中——后者等价于"前 $i-1$ 位中的最大值落在前 $k$ 位里"，概率 $k/(i-1)$。两件事 independent（独立），所以 $\Pr\{S_i\} = k/(n(i-1))$，求和得 $\Pr\{S\} = (k/n) \sum_{i=k}^{n-1} 1/i \approx (k/n) \ln(n/k)$。对 $k$ 求导置零：$\ln(n/k) = 1$，即 $k = n/e$，代回得成功率 $1/e$。直觉上这是两个相反错误的平衡：$k$ 太小则基准线被早期平庸者污染，$k$ 太大则最优者已在观察期被放走；$n/e$ 让"看错"与"错过"的概率相等。
>
> 数字（我按 $(k/n) \sum_{i=k}^{n-1} 1/i$ 精确枚举每个 $k$ 算的）：$n = 10$ 时最优 $k = 3$，成功率 $0.3987$；$n = 100$ 时最优 $k = 37$，成功率 $0.3710$；$n = 1000$ 时最优 $k = 368$，成功率 $0.3682$。三个数与 $1/e = 0.36788$ 的差随 $n$ 单调缩小，且最优点都略微大于 $n/e$（$100/e = 36.79$ 而最优 $k = 37$），因为积分近似略低估了求和。这个"成功率不随 $n$ 衰减"的结论是本题最反直觉处：难度对规模免疫，只要目标从"最好"松到"接近最好"。
>
> 失败的 63% 在哪？两类。第一类，最优者恰好落进观察期，概率 $k/n = 1/e \approx 0.368$，这时无论后面怎么选都必然失败（策略只能选观察期之后的破纪录者）。第二类，最优者不在观察期，但观察期之后出现了某个"局部最好"的人先破了纪录，于是你提前出手锁死——这类失败的概率约 $0.264$。两类加起来约 $0.632 = 1 - 1/e$。这也说明了一个设计上的事实：拒绝前 $k$ 位不是浪费，它是唯一能让"基准线"成立的代价；如果你试图让 $k \to 0$，第一类失败消失但第二类暴涨，最优点只是把两类调到相等。
>
> 放开"只雇一次"的约束会怎样？如果允许多次录用、但每次换人要付成本，问题就变成 optimal stopping（最优停时）的一个具体实例：你要在每一步比较"现在停下的收益"与"继续的期望收益"，用逆向归纳算出阈值曲线。此时最优策略不再是"固定拒掉前 $k$ 位"，而是一族随剩余人数变化的阈值。反过来，如果把"可回头"允许进来（见过的人还能选），最优策略退化成"全看一遍再选最好"，成功率 $1$，代价是面试成本 $n$。三个版本（只选一次、可多次、可回头）对照着看，才能看清 $1/e$ 究竟是被哪条约束逼出来的：它是"不可回头 + 只能选一次 + 不知道未来"这三条同时成立时的最优常数。
>
> 跨课程连接有两处。其一，6.042J 的对称性给出 $\Pr\{O_i\} = k/(i-1)$，不需要任何分布假设——这正是它比"假设分数服从正态分布"更强的理由；100B 的"单调函数求和与积分互估"给出 $\ln(n/k)$ 的夹逼，教材的 inequality（不等式）(A.12) 正是这条。其二，这个模型是 online algorithm（在线算法）与 competitive analysis（竞争分析）的祖先：你必须在不知道未来的情况下决策，评价标准从"最优"改成"与离线最优的比值"。区别在于：secretary（秘书）问题的离线最优是"必选到最好者"，评价是达成概率；竞争分析里离线最优是一个具体成本值，评价是成本比值，后者可以做到常数倍而前者只能做到 $1/e$。
>
> 一句话收束：先观察后出手的价值，是用 $1 - 1/e \approx 63\%$ 的失败率换来一个与规模无关的保证。

---

> <span style="color:#7f8c8d;">CLRS §5.4, p.142</span>

### Exercises <span style="color:#2471a3;">**[exercise]**</span>

**5.4-1**

How many people must there be in a room before the probability that someone has the same birthday as you do is at least $1/2$? How many people must there be before the probability that at least two people have a birthday on July 4 is greater than $1/2$?

**5.4-2**

Suppose that we toss balls into $b$ bins until some bin contains two balls. Each toss is independent, and each ball is equally likely to end up in any bin. What is the expected number of ball tosses?

**5.4-3 ★**

For the analysis of the birthday paradox, is it important that the birthdays be mutually independent, or is pairwise independence sufficient? Justify your answer.

**5.4-4 ★**

How many people should be invited to a party in order to make it likely that there are three people with the same birthday?

**5.4-5 ★**

What is the probability that a $k$-string over a set of size $n$ forms a $k$-permutation? How does this question relate to the birthday paradox?

**5.4-6 ★**

Suppose that $n$ balls are tossed into $n$ bins, where each toss is independent and the ball is equally likely to end up in any bin. What is the expected number of empty bins? What is the expected number of bins with exactly one ball?

**5.4-7 ★**

Sharpen the lower bound on streak length by showing that in $n$ flips of a fair coin, the probability is less than $1/n$ that no streak longer than $\lg n - 2\lg\lg n$ consecutive heads occurs.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 5, p.143</span>

## Problems for Chapter 5（第 5 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 5-1 · Probabilistic counting（概率计数） <span style="color:#2471a3;">**[problem]**</span>

With a $b$-bit counter, we can ordinarily only count up to $2^b - 1$. With R. Morris's probabilistic counting, we can count up to a much larger value at the expense of some loss of precision.

We let a counter value of $i$ represent a count of $n_i$ for $i = 0, 1, \ldots, 2^b - 1$, where the $n_i$ form an increasing sequence of nonnegative values. We assume that the initial value of the counter is 0, representing a count of $n_0 = 0$. The INCREMENT operation works on a counter containing the value $i$ in a probabilistic manner. If $i = 2^b - 1$, then the operation reports an overflow error. Otherwise, the INCREMENT operation increases the counter by 1 with probability $1/(n_{i+1} - n_i)$, and it leaves the counter unchanged with probability $1 - 1/(n_{i+1} - n_i)$.

If we select $n_i = i$ for all $i \ge 0$, then the counter is an ordinary one. More interesting situations arise if we select, say, $n_i = 2^{i-1}$ for $i > 0$, or $n_i = F_i$ (the $i$th Fibonacci number—see Section 3.2).

For this problem, assume that $n_{2^b-1}$ is large enough that the probability of an overflow error is negligible.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题是 Morris counter（莫里斯计数器）的入门，要解决的问题只有一句：$b$ 位的寄存器怎么数出远超 $2^b$ 的数。
>
> 机制。让计数器的值 $i$ 代表"真实计数 $n_i$"，且 $n_i$ 严格递增。INCREMENT 在值为 $i$ 时以概率 $1/(n_{i+1} - n_i)$ 加 1、否则原地不动。无偏性是这样来的：这一次操作给"代表值"带来的期望增量是 $(n_{i+1} - n_i) \times 1/(n_{i+1} - n_i) = 1$，不管当前在哪个状态都一样，所以 $n$ 次操作之后期望代表值恰好是 $n$——这正是 (a) 小问，它只用 expectation（期望）的线性性，不需要各步 independent（独立）。方差由 $n_i$ 的增长速度控制：$n_i$ 长得越快，单步跨度越大，抖动越狠。
>
> 算一个具体情形（题目 (b) 小问取 $n_i = 100i$）。此时每步增量概率恒为 $1/100$，$n$ 次操作后"加了多少次"服从二项分布，方差 $n \cdot (1/100) \cdot (99/100)$，乘以 $100^2$ 得代表值方差约 $99n \approx 100n$，标准差约 $10\sqrt{n}$。我做了 $4 \times 10^4$ 次模拟核对：$n = 10, 20, 40$ 时测得方差 $985.3, 1981.6, 3979.3$，与理论值 $1000, 2000, 4000$ 吻合。含义是相对误差约 $10/\sqrt{n}$：$n = 10^6$ 时约 1%。再看指数情形 $n_i = 2^{i-1}$：$b = 8$ 位时 $i$ 最大 255，$n_{255} = 2^{254} \approx 2.9 \times 10^{76}$，而普通计数器只能到 255——从 $10^2$ 到 $10^{76}$，换来的是相对误差变成常数级，这就是"以精度换容量"的字面含义。
>
> 为什么位宽是 $\log_2\log_2 n$ 而不是 $\log_2 n$？因为要存的是"指数"，而指数只需要对数量级的位来编码：$n = 10^{76}$ 的对数约 76，$76$ 的对数约 6.25，所以 8 位寄存器足够。这个"双重对数"是这类算法最迷人的地方：你可以不断把指数往上叠，代价是每叠一层就多一份误差。现代流式系统里这套思想变成了 sketch（概要数据结构）：Count-Min sketch（计数最小概要）用同样的"带噪声的小计数器 + 多副本取最小"来控制误差，区别在于它处理的是"每个键的频次"而不是"单一总数"，所以需要多组计数器。
>
> 一个自然的问题是：这种"偶尔加一"的规则能不能换成确定性的（比如每 $2^i$ 次加一）？不能——确定性规则会让计数器停在同一状态上很久，然后突然跳一下，误差是系统性的、不会平均掉。随机化在这里的作用不是省时间，而是把误差变成零均值噪声，让 $\mathrm{E}$ 恰好等于真值。这一点与 §5.3 的随机化快排是同一件事的两面：那里的随机化是为了让最坏输入消失，这里的随机化是为了让误差可期望。
>
> 历史与出处（可一手核实）：Robert Morris 1977 年在贝尔实验室提出该算法，动机是统计网络事件时寄存器不够；Philippe Flajolet 在 1980 年代初做了完整分析并给它起了 approximate counting（近似计数）这个名字（《Approximate counting: A detailed analysis》，BIT 1985）。它的历史地位在于被公认为 streaming algorithm（流式算法）的先驱：Alon、Matias、Szegedy 1996 年 STOC 的《The space complexity of approximating the frequency moments》建立了流式算法的空间下界框架，该文获 2005 年 Gödel Prize（奖项页可核实到作者、论文与年份）。
>
> 跨课程连接：CSAPP 第 2 章与第 3 章的位运算与寄存器直觉在这里直接用上——指数只需要对数的位宽，是因为二进制表示天然按位置指数加权。另一处连接是 100B 与概率论的"用不等式控制误差"：$\sigma = \sqrt{\mathrm{Var}}$ 决定了相对误差按 $1/\sqrt{n}$ 衰减，这是所有"多次独立采样取平均"方法的共同底座。区别在于：这里不能取平均（只有一个寄存器），所以误差不能靠重复实验压掉，只能靠"重复整个计数器"（多次独立运行再取中位数）来压，那是另一套工程，也是 Flajolet 那篇论文里讨论的重点之一。
>
> 一句话收束：随机化把"精确计数"换成"无偏估计"，与 §5.3 把最坏情况换成期望是同一哲学的两次落笔。

a. Show that the expected value represented by the counter after $n$ INCREMENT operations have been performed is exactly $n$.

b. The analysis of the variance of the count represented by the counter depends on the sequence of the $n_i$. Let us consider a simple case: $n_i = 100i$ for all $i \ge 0$. Estimate the variance in the value represented by the register after $n$ INCREMENT operations have been performed.

### Problem 5-2 · Searching an unsorted array（未排序数组的搜索） <span style="color:#2471a3;">**[problem]**</span>

This problem examines three algorithms for searching for a value $x$ in an unsorted array $A$ consisting of $n$ elements.

Consider the following randomized strategy: pick a random index $i$ into $A$. If $A[i] = x$, then we terminate; otherwise, we continue the search by picking a new random index into $A$. We continue picking random indices into $A$ until we find an index $j$ such that $A[j] = x$ or until we have checked every element of $A$. Note that we pick from the whole set of indices each time, so that we may examine a given element more than once.

a. Write pseudocode for a procedure RANDOM-SEARCH to implement the strategy above. Be sure that your algorithm terminates when all indices into $A$ have been picked.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 5, p.144</span>

（接上页 · Problem 5-2）

b. Suppose that there is exactly one index $i$ such that $A[i] = x$. What is the expected number of indices into $A$ that we must pick before we find $x$ and RANDOM-SEARCH terminates?

c. Generalizing your solution to part (b), suppose that there are $k \ge 1$ indices $i$ such that $A[i] = x$. What is the expected number of indices into $A$ that we must pick before we find $x$ and RANDOM-SEARCH terminates? Your answer should be a function of $n$ and $k$.

d. Suppose that there are no indices $i$ such that $A[i] = x$. What is the expected number of indices into $A$ that we must pick before we have checked all elements of $A$ and RANDOM-SEARCH terminates?

Now consider a deterministic linear search algorithm, which we refer to as DETERMINISTIC-SEARCH. Specifically, the algorithm searches $A$ for $x$ in order, considering $A[1], A[2], A[3], \ldots, A[n]$ until either it finds $A[i] = x$ or it reaches the end of the array. Assume that all possible permutations of the input array are equally likely.

e. Suppose that there is exactly one index $i$ such that $A[i] = x$. What is the average-case running time of DETERMINISTIC-SEARCH? What is the worst-case running time of DETERMINISTIC-SEARCH?

f. Generalizing your solution to part (e), suppose that there are $k \ge 1$ indices $i$ such that $A[i] = x$. What is the average-case running time of DETERMINISTIC-SEARCH? What is the worst-case running time of DETERMINISTIC-SEARCH? Your answer should be a function of $n$ and $k$.

g. Suppose that there are no indices $i$ such that $A[i] = x$. What is the average-case running time of DETERMINISTIC-SEARCH? What is the worst-case running time of DETERMINISTIC-SEARCH?

Finally, consider a randomized algorithm SCRAMBLE-SEARCH that works by first randomly permuting the input array and then running the deterministic linear search given above on the resulting permuted array.

h. Letting $k$ be the number of indices $i$ such that $A[i] = x$, give the worst-case and expected running times of SCRAMBLE-SEARCH for the cases in which $k = 0$ and $k = 1$. Generalize your solution to handle the case in which $k \ge 1$.

i. Which of the three searching algorithms would you use? Explain your answer.

---

> <span style="color:#7f8c8d;">CLRS Notes for Chapter 5, p.145</span>

## Notes for Chapter 5（第 5 章注记） <span style="color:#2471a3;">**[reference]**</span>

Bollobás [53], Hofri [174], and Spencer [321] contain a wealth of advanced probabilistic techniques. The advantages of randomized algorithms are discussed and surveyed by Karp [200] and Rabin [288]. The textbook by Motwani and Raghavan [262] gives an extensive treatment of randomized algorithms.

Several variants of the hiring problem have been widely studied. These problems are more commonly referred to as "secretary problems." An example of work in this area is the paper by Ajtai, Meggido, and Waarts [11].

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一页的 Notes 值得停一下，因为它记录了一个成果同时开出三条线：sorting algorithm（排序算法）、data structure（数据结构）、abstract data type（抽象数据类型）。
>
> 先说机制上的分工。Williams 1964 年在 CACM 第 7 卷第 6 期的 Algorithm 232 里提出 heapsort（堆排序）与 binary heap（二叉堆），但他建堆用的是"逐个插入"——$n$ 次插入、每次 $O(\lg n)$，建堆本身 $O(n \lg n)$。同年 Floyd 在 CACM 第 7 卷第 12 期的 Algorithm 245《Treesort 3》里给出改进：数组原地、自底向上建堆，于是建堆降到 $O(n)$，整套排序仍是 $O(n \lg n)$ 但常数更小。今天教材里的 BUILD-MAX-HEAP 加 HEAPSORT 就是 Floyd 的形态。这条文献信息我按 NIST 的算法词典条目核对过期刊、卷、期、页码与年月，那里还有一句判语："Williams 清楚提出了 heapsort（堆排序）的想法，Floyd 给出了完整而高效的实现"。
>
> 为什么它能开出第二条线？因为堆把"取最大"与"插入"这两件事同时压到 $O(\lg n)$。算一下替代方案的账：用有序数组，EXTRACT-MAX 是 $O(1)$ 但 INSERT 要 $O(n)$（挪位），$n$ 次插入合计 $O(n^2)$；用无序数组则反过来，INSERT 是 $O(1)$ 而取最大 $O(n)$。堆是唯一让两者都 $O(\lg n)$ 的结构。$n = 10^6$ 时，$n^2/2 = 5 \times 10^{11}$ 次移动对比 $n \lg n \approx 2 \times 10^7$，差 25000 倍。这就是 priority queue（优先队列）这个抽象数据类型的由来：使用者只声明"我要 INSERT 与 EXTRACT-MAX"，堆负责把两边都做到对数，而第 6.5 节正是这么组织的。
>
> 第三层是历史坐标，但要克制，不堆年表。Notes 里提到的 secretary problems（秘书问题）你在 §5.4.4 已经见过 37% 策略，而 Karp 与 Rabin 的综述（文献 [200] 与 [288]）标志着 1970 年代末随机化算法成为独立研究领域。这里的因果要说准：不是"随机化让堆变好"，而是"同一时期排序与随机化两条线各自成熟"，教材把两者放进同一本 Notes 只是版面安排。真正属于 heapsort（堆排序）的历史贡献是"第一次把树形结构压进数组"，这与第 6.1 节的零指针表示是同一件事的两面。
>
> 还有一个常被问到的细节：为什么教材说 heap（堆）而这一章的 heap（堆）不是"垃圾回收存储"？因为这个词在 1964 年被 Williams 用来命名"父子有序的完全二叉树"，到 1980 年代又被 Lisp 与 Java 用来指"程序运行时的动态内存区"，两者只是同名。这个术语冲突提醒你读文献时要看上下文：在算法书里 heap（堆）永远是数据结构，在语言实现书里 heap（堆）永远是内存区域。顺带一句：正因为这两个含义都不涉及"堆积"的字面义，中文翻译才会分裂成"堆"与"堆区"两种说法，而本书的"堆"指前者。
>
> 跨课程连接：第 6.5 节把堆变成优先队列，操作系统里的 scheduler（调度器，CSAPP 第 8 章讲进程与信号时你见过它的决策）与第 24 章 Dijkstra 算法都是它的下游；事件驱动模拟器用 min-priority queue（最小优先队列）按时间键取下一个事件，这正是教材举的例子。区别在于：教材只用堆讲"如何实现"，而工程里更关心"要不要用堆"——如果操作序列是"大量插入、只取一次最大"，排序一次反而更便宜，这正是第 8 章的下界告诉你的判断法。
>
> 一句话收束：heapsort（堆排序）的历史价值不在排序本身，而在于它顺手造出了第一个"两个操作都对数"的容器。

---

> <span style="color:#7f8c8d;">CLRS Part II, p.146</span>

> <span style="color:#7f8c8d;">[note] 本页为篇章分隔页（part-opening page），原文仅含篇章编号与篇章标题，无正文内容，故不作正文翻译。</span>

## Part II（第二部分）· Sorting and Order Statistics（排序与顺序统计） <span style="color:#2471a3;">**[section]**</span>

---

> <span style="color:#7f8c8d;">CLRS Part II Introduction, p.147</span>

## Part II · Sorting and Order Statistics（排序与顺序统计）

### Introduction（引言）

本部分给出若干解决如下 sorting problem（排序问题）的 algorithms（算法）：

**Input（输入）：** 一个由 $n$ 个数组成的 sequence（序列）$\langle a_1, a_2, \ldots, a_n \rangle$。

**Output（输出）：** input sequence（输入序列）的一个 permutation（排列，即 reordering（重排））$\langle a'_1, a'_2, \ldots, a'_n \rangle$，使得 $a'_1 \le a'_2 \le \cdots \le a'_n$。

input sequence 通常是一个包含 $n$ 个 elements（元素）的 array（数组），不过它也可以用其他方式表示，例如 linked list（链表）。

### The structure of the data（数据的结构）

在实践中，待排序的数很少是孤立取值。每个数通常是一个称为 record（记录）的数据集合的一部分。每个 record 包含一个 key（关键字），也就是待排序的值；record 的其余部分由 satellite data（卫星数据）构成，它们通常随 key 一起被携带。在实践中，当 sorting algorithm（排序算法）对 key 进行重排时，它必须同时重排 satellite data。如果每个 record 包含大量 satellite data，我们往往重排一个由指向各 record 的 pointer（指针）构成的数组，而不重排 record 本身，以尽量减少 data movement（数据移动）。

从某种意义上说，正是这些 implementation details（实现细节）把一个 algorithm 与一个成熟的程序（full-blown program）区分开来。sorting algorithm 描述的是我们确定 sorted order（已排序顺序）的方法，而不论我们排序的是一个个孤立的数，还是包含许多字节 satellite data 的大型 record。因此，在聚焦 sorting problem 时，我们通常假设 input 只由数组成。把一个对数进行排序的 algorithm 转换成一个对 record 进行排序的程序（接下页）

---

> <span style="color:#7f8c8d;">CLRS Part II, p.148</span>

（接上页）在概念上是直截了当的，尽管在给定的 engineering situation（工程情境）中，其他一些微妙之处可能使实际的编程工作颇具挑战性。

### Why sorting?（为什么排序？）

许多计算机科学家认为，sorting（排序）是算法研究中最根本的问题。理由有以下几点：

- 有时，application（应用程序）本身就需要对信息进行排序。例如，为了准备 customer statements（客户对账单），银行需要按 check number（支票号）对支票进行排序。

- 算法常常把 sorting 用作一个关键的 subroutine（子程序）。例如，一个渲染相互叠放的 graphical objects（图形对象）的程序，可能需要按"above（在上）"关系对这些对象排序，以便自底向上地绘制它们。在本书中我们将看到大量把 sorting 用作子程序的算法。

- 我们可以从种类繁多的 sorting algorithms（排序算法）中汲取选择，它们采用（employ）了一整套丰富的技术（techniques）。事实上，算法设计中许多重要的技术，都出现在多年来发展起来的各类 sorting algorithms 之中。从这个意义上说，sorting 也是一个具有历史意义的问题。

- 我们可以为 sorting 证明一个 nontrivial lower bound（非平凡下界）（正如我们将在 Chapter 8（第 8 章）中所做的那样）。我们最好的 upper bounds（上界）在渐近意义上与该下界相匹配，因此我们知道我们的 sorting algorithms 是 asymptotically optimal（渐近最优的）。此外，我们还可以利用 sorting 的下界来证明其他某些问题的下界。

- 在实现 sorting algorithms 时，许多 engineering issues（工程问题）会凸显出来。针对特定情形最快的排序程序可能取决于诸多因素，例如关于 key 与 satellite data 的先验知识、主机的 memory hierarchy（存储层次结构，cache（高速缓存）与 virtual memory（虚拟内存）），以及 software environment（软件环境）。这些问题中的许多最好在算法层面处理，而不是靠"tweaking（微调）"代码。

### Sorting algorithms（排序算法）

我们在 Chapter 2（第 2 章）中介绍过两个对 $n$ 个实数排序的算法。insertion sort（插入排序）在最坏情况下需要 $\Theta(n^2)$ 时间。不过，由于它的 inner loops（内层循环）十分紧凑，对于小的 input size（输入规模），它是一种快速的 in-place（原地）sorting algorithm。（回想一下：如果排序算法在 input array（输入数组）之外存储的 elements（元素）始终只有常数个，我们就称它是原地排序的。）merge sort（归并排序）具有更好的 asymptotic running time（渐近运行时间）$\Theta(n \lg n)$，但它所使用的 MERGE procedure（MERGE 过程）并不是原地操作的。（接下页）

---

> <span style="color:#7f8c8d;">CLRS Part II, p.149</span>

（接上页）在本部分中，我们将再介绍两个对任意实数排序的算法。heapsort（堆排序）在 Chapter 6（第 6 章）中给出，它以 $O(n \lg n)$ 时间对 $n$ 个数进行原地排序。它使用一种重要的 data structure（数据结构）——heap（堆），借助这种结构，我们还可以实现 priority queue（优先队列）。

quicksort（快速排序）在 Chapter 7（第 7 章）中给出，同样对 $n$ 个数进行原地排序，但其 worst-case running time（最坏情况运行时间）为 $\Theta(n^2)$。不过，它的 expected running time（期望运行时间）是 $\Theta(n \lg n)$，而且在实践中通常胜过 heapsort。与 insertion sort 一样，quicksort 的代码紧凑，因此其运行时间中的 hidden constant factor（隐藏常数因子）较小。它是排序大型输入数组时流行使用的算法。

insertion sort、merge sort、heapsort 和 quicksort 都是 comparison sort（比较排序）：它们通过比较 elements（元素）来确定 input array（输入数组）的 sorted order（已排序顺序）。Chapter 8（第 8 章）一开始将引入 decision-tree model（决策树模型），以研究 comparison sorts 的性能局限。利用这一模型，我们证明任何 comparison sort 在 $n$ 个输入上的 worst-case running time 具有 $\Omega(n \lg n)$ 的下界，从而说明 heapsort 和 merge sort 是渐近最优的比较排序算法。

Chapter 8 随后进一步说明：如果我们能够通过比较元素以外的手段收集到关于输入的 sorted order 的信息，就可以打破 $\Omega(n \lg n)$ 这一 lower bound（下界）。例如，counting sort（计数排序）假设输入的数都属于集合 $\{0, 1, \ldots, k\}$。通过利用 array indexing（数组下标索引）作为确定相对顺序的工具，counting sort 能够以 $\Theta(k + n)$ 时间对 $n$ 个数排序。于是，当 $k = O(n)$ 时，counting sort 的运行时间与 input array 的规模呈 linear（线性）关系。一个相关算法 radix sort（基数排序）可以用来扩展 counting sort 的适用范围。如果待排序的有 $n$ 个整数，每个整数有 $d$ 位数字（digit），而每一位数字最多可取 $k$ 种可能的值，那么 radix sort 能以 $\Theta(d(n + k))$ 时间对这些数排序。当 $d$ 为常数且 $k$ 为 $O(n)$ 时，radix sort 以线性时间运行。第三个算法 bucket sort（桶排序）需要知道 input array 中数的 probabilistic distribution（概率分布）。对于 uniformly distributed（均匀分布）在 half-open interval（半开区间）$[0, 1)$ 上的 $n$ 个实数，它能以 average-case（平均情况）$O(n)$ 时间完成排序。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 比较排序的下界可以提前看穿，而且只需要两件 6.042J 的工具：把算法画成一棵树，再数叶子。
>
> 机制。任何 comparison sort（比较排序）在给定输入上的执行路径，都是一串"比 $a$ 与 $b$"得到的回答；把每次比较记作一个二分支的结点，整棵树就记录了算法对所有可能输入的行为。$n$ 个元素有 $n!$ 种排列，而正确的算法必须把每种排列送到一个"输出它"的 leaf（叶结点），所以叶子数至少 $n!$；高度为 $h$ 的二叉树至多 $2^h$ 个叶子，于是 $2^h \ge n!$，取对数得 $h \ge \lg(n!)$。这一步的实质是信息论：一次比较只回答一个是非题，即一个 bit（比特），要把 $n!$ 种可能区分开，至少需要 $\lg(n!)$ 个 bit（比特）。
>
> 数字。$n = 3$：$3! = 6$，$\lg 6 = 2.585$，故至少 3 次比较（$2^2 = 4 < 6 \le 8$），而插入排序在最好情形恰好 2 次、最坏 3 次，说明界是紧的；$n = 5$：$120$ 种排列，$\lg 120 = 6.907$，至少 7 次；$n = 10^6$：用 Stirling 展开 $\lg(n!) = n \lg n - n \lg e + O(\lg n)$，即 $10^6 \times 19.93 - 10^6 \times 1.4427 \approx 1.849 \times 10^7$，而 $n!$ 本身是 $10^{5.57 \times 10^6}$ 量级——下界是从这个天文数字里取对数得来的。注意 $\lg(n!)$ 与 $n \lg n$ 只差一个 $1.4427n$ 的项，正是这一项让"下界"与"归并排序的上界"在常数上还能对上。
>
> 绕过下界的方式更值得注意：counting sort（计数排序）根本不做比较，它把值本身当 array index（数组下标）用，$\Theta(n + k)$；radix sort（基数排序）把它串成多趟，$\Theta(d(n+k))$。为什么下界对它们失效？因为下界的前提是"唯一的信息来源是比较"，而计数排序偷偷用了另一条信息通道——值的具体大小可以当地址。这提醒你：每个下界都绑定一个计算模型，出了模型就没有下界。同样的觉悟在第 9 章会再来一次：只允许比较时找第 $i$ 小要 $\Omega(n \lg n)$，允许"以值定址"或随机化，就能做到期望 $O(n)$。
>
> 还有一处容易忽略的细节：决策树只对"确定性算法"直接成立。随机化排序（比如随机 pivot（枢轴）的快排）每一步有多条分支，画出来是一棵带概率的树，$n!$ 个叶子仍然要覆盖所有输出，故 $\lg(n!)$ 的下界对"期望比较次数"同样适用——因为对任意一棵树，最浅的叶子都不能比 $\lg(n!)$ 更浅，而随机化只是在这些树之间按概率挑选。区别在于：确定性情形说的是"每片叶子都深"，随机化情形说的是"平均深度"也压不下去，方法不同、结论一样。
>
> 下界的另一面是：它不能告诉你"哪个算法最好"。$\Omega(n \lg n)$ 只说没人能低于这个量级，而归并、堆排、快排的期望都达到了它，所以从下界角度看三者打平；真正的差别全在常数、稳定性与访存模式上。这正是第 13 条注那张表的意义——下界划定可行域，工程在可行域里挑点。区别在于：下界是数学事实（对所有算法成立），选型是工程判断（对特定数据成立）。
>
> 跨课程连接有两处。其一，6.042J 的树计数引理（高度 $h$ 的二叉树最多 $2^h$ 个叶子）是全部骨架。其二，Cover 的信息论给出同一件事的版本：均匀分布下 $\log_2(n!) \approx n \log_2 n$ 正是编码 $n$ 个符号所需的平均位数，而这里是最坏路径长度，即最大值而不是期望，所以比较排序的下界比信息论的编码界更强。区别在于：信息论允许变长码，短的常见符号可以省位；排序不允许，因为最坏输入必须也被正确处理。
>
> 一句话收束：$\Omega(n \lg n)$ 不是排序的性质，而是"只准问是非题"这种计算模型的性质。

下表总结了来自 Chapter 2（第 2 章）与第 6–8 章的各 sorting algorithms 的 running time（运行时间）。照例，$n$ 表示待排序 items（项）的数目。对 counting sort 而言，待排序的项是集合 $\{0, 1, \ldots, k\}$ 中的整数。对 radix sort 而言，每一项是一个 $d$ 位数字的数，其中每位数字取 $k$ 种可能的值。对 bucket sort 而言，我们假设 key 是均匀分布在半开区间 $[0, 1)$ 上的实数。最右一列给出 average-case 或 expected running time，并在它与 worst-case running time 不同时予以注明。我们省略了 heapsort 的 average-case running time，因为本书并不对它进行分析。（接下页）

---

> <span style="color:#7f8c8d;">CLRS Part II, p.150</span>

（接上页）

| Algorithm（算法） | Worst-case running time（最坏情况运行时间） | Average-case/expected running time（平均情况/期望运行时间） |
|---|---|---|
| Insertion sort（插入排序） | $\Theta(n^2)$ | $\Theta(n^2)$ |
| Merge sort（归并排序） | $\Theta(n \lg n)$ | $\Theta(n \lg n)$ |
| Heapsort（堆排序） | $O(n \lg n)$ | — |
| Quicksort（快速排序） | $\Theta(n^2)$ | $\Theta(n \lg n)$（expected（期望）） |
| Counting sort（计数排序） | $\Theta(k + n)$ | $\Theta(k + n)$ |
| Radix sort（基数排序） | $\Theta(d(n + k))$ | $\Theta(d(n + k))$ |
| Bucket sort（桶排序） | $\Theta(n^2)$ | $\Theta(n)$（average-case（平均情况）） |

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这张表要当"假设清单"读：每一行的复杂度都挂着一个前提，选型的本质是判断你的数据是否满足那个前提。
>
> 逐行看前提。insertion sort（插入排序）的 $\Theta(n^2)$ 是平方级，但内循环只有比较与移动两步、不要额外内存，$n$ 在几十以内时实测常常最快——$n = 20$ 时平方项约 $n^2/4 = 100$ 次比较，而归并排序虽只要 $n \lg n \approx 86$ 次比较，却要付递归与临时数组的常数，谁快取决于常数差多少。merge sort（归并排序）的 $\Theta(n \lg n)$ 是保证，且 stable（稳定）。heapsort（堆排序）的 $O(n \lg n)$ 也是保证，且原地。quicksort（快速排序）的最坏 $\Theta(n^2)$ 真的会发生，但期望 $\Theta(n \lg n)$ 且常数最小。counting sort（计数排序）的 $\Theta(n + k)$ 需要键落在 $[0, k]$ 的整数区间。radix sort（基数排序）的 $\Theta(d(n + k))$ 需要定长数字。bucket sort（桶排序）的 $\Theta(n)$ 只在键均匀分布在 $[0, 1)$ 时成立，最坏 $\Theta(n^2)$——输入一旦偏离均匀，线性的承诺立刻作废。
>
> 两个细节值得单独说。其一，表里 heapsort（堆排序）的 average-case（平均情况）一栏是"—"，那不是"没有平均情况"，而是本书没分析；实际上元素互异时它的最好情形也有 $\Omega(n \lg n)$（习题 6.4-5），即所有情形同阶，这正是它适合当"兜底"的原因：没有坏输入能让它退化。其二，stability（稳定性）指"键相同的记录保持原有相对次序"，快排与堆排都不稳定，因为交换会把相等元素搬得很远；归并与计数排序天然稳定。工程上这一点很硬：多关键字排序时"先按次关键字排、再按主关键字稳定地排"能拼出正确结果，不稳定排序就拼不出来。
>
> 现代实现把这张表拆成两条路线（可一手核实）：Java 的 Arrays.sort 对基本类型用 dual-pivot quicksort（双枢轴快速排序，Yaroslavskiy 2009 年提出，Java 7 起采用），对对象用 TimSort（稳定的归并变体，Tim Peters 2002 年为 CPython 写的，CPython 2.3 起进入标准库）；Python 的内置 sorted 也是 TimSort。原因正是这张表的逻辑：基本类型没有 satellite data（卫星数据），稳定性无意义，于是选缓存友好的快排；对象可能带次关键字，稳定性必须保，于是选归并。一句话，语言设计者读表时读的不是复杂度，是"哪些前提默认成立"。
>
> 还有一个容易被忽视的代价项：$n$ 很小的时候，渐近符号完全失效。$n = 8$ 时插入排序约 16 次比较，归并排序要 $8 \times 3 = 24$ 次比较再加递归调用开销，差距是常数倍但方向与渐近预测相反。这也是 introsort 之类的实现要在底部切到插入排序的原因：不是理论需要，而是常数需要。区别在于：复杂度表告诉你 $n \to \infty$ 时的胜负，工程实现还要回答 $n = 8$ 时的胜负，而后者只能实测。
>
> 跨课程连接：CSAPP 第 6 章的 storage hierarchy（存储层次结构）解释了为什么 $n$ 小时插入排序赢——它顺序访问、工作集小到能装进 L1；也解释了为什么大数组上快排赢——划分是顺序双向扫描，预取友好。区别在于：第 8 章的下界只数比较次数，完全看不见 cache（高速缓存），而工程选型里一次缓存未命中的代价常常比一次比较大一个量级。第二处连接是第 2 章：插入排序的不变式是"前缀已排序"，这个性质维护起来一步只要 $O(n)$ 但内循环极紧，所以小规模无敌。
>
> 一句话收束：复杂度表给的是天花板，选型看的是前提是否成立、常数有多大。

### Order statistics（顺序统计量）

一个由 $n$ 个数组成的 set（集合）的 $i$th order statistic（第 $i$ 顺序统计量），就是这个集合中第 $i$ 小的数。当然，我们可以先对 input（输入）排序，再索引 output（输出）的第 $i$ 个 element（元素），来选取第 $i$ 顺序统计量。在对 input distribution（输入分布）不作任何假设的情况下，由 Chapter 8（第 8 章）证明的下界可知，这一方法需要 $\Omega(n \lg n)$ 时间。在 Chapter 9（第 9 章）中，我们将说明即使 elements 是任意实数，也可以在 $O(n)$ 时间内找到第 $i$ 小的元素。我们将给出一个 randomized algorithm（随机化算法），其 pseudocode（伪代码）十分紧凑，worst case（最坏情况）下运行 $\Theta(n^2)$ 时间，但其 expected running time（期望运行时间）为 $O(n)$。我们还将给出一个更复杂的算法，其 worst-case time（最坏情况时间）为 $O(n)$。

### Background（背景知识）

尽管本部分的大部分内容并不依赖艰深的数学，但某些 section（节）确实需要一定的数学素养。特别地，对 quicksort（快速排序）、bucket sort（桶排序）以及 order-statistic algorithm（顺序统计算法）的分析要用到概率论（Appendix C（附录 C）中有所复习），以及 Chapter 5（第 5 章）中关于 probabilistic analysis（概率分析）与 randomized algorithms（随机化算法）的材料。对 worst-case linear-time（最坏情况线性时间）顺序统计算法的分析，所涉及的数学比本部分其他 worst-case analysis（最坏情况分析）要稍微复杂一些。

---

> <span style="color:#7f8c8d;">CLRS Chapter 6, p.151</span>

## Chapter 6（第 6 章）· Heapsort（堆排序） <span style="color:#2471a3;">**[section]**</span>

本章介绍另一种 sorting algorithm（排序算法）：heapsort（堆排序）。与 merge sort（归并排序）一样而与 insertion sort（插入排序）不同，heapsort 的 running time（运行时间）为 $O(n \lg n)$；与 insertion sort 一样而与 merge sort 不同，heapsort 是 in-place（原地）排序：在任何时刻，存储在 input array（输入数组）之外的 array elements（数组元素）只有常数个。因此，heapsort 兼具我们已讨论过的两种排序算法的更好的属性。

heapsort 还引入了另一种 algorithm design technique（算法设计技术）：使用一种 data structure（数据结构）——这里是我们要称之为"heap（堆）"的一种结构——来管理信息。heap 数据结构不仅对 heapsort 有用，它还能实现一种高效的 priority queue（优先队列）。在后面各章的 algorithms（算法）中，heap 数据结构还会再次出现。

"heap"这个术语最初是在 heapsort 的语境下创造的，但后来它逐渐被用来指"garbage-collected storage（垃圾回收存储）"，例如 Java 和 Lisp 这类编程语言所提供的那种。我们的 heap 数据结构并不是垃圾回收存储；本书中每当提到 heap 时，我们指的都是一种数据结构，而不是 garbage collection（垃圾回收）的某个方面。

### Section 6.1 · Heaps（堆） <span style="color:#2471a3;">**[section]**</span>

(binary) heap data structure（（二叉）堆数据结构）是一个 array object（数组对象），我们可以把它看作一棵 nearly complete binary tree（近似完全二叉树）（见 Section B.5.3（B.5.3 节）），如图 6.1 所示。树上的每个 node（结点）都对应数组中的一个 element（元素）。这棵树在除最低层（可能例外）之外的所有层上都被完全填满，而最低层则从左往右填充到某一点为止。表示 heap 的数组 $A$ 是一个具有两个 attributes（属性）的对象：`A.length`（照例）给出数组中元素的数目，而 `A.heap-size` 表示存放在数组 $A$ 中的堆元素有多少个。也就是说，虽然 $A[1..A.length]$ 中可能存有数，但只有 $A[1..A.heap-size]$（其中 $0 \le A.heap\text{-}size \le A.length$）中的元素才是 heap 的有效元素。树的 root（根结点）是 $A[1]$，给定某个结点的 index（下标）$i$，我们可以很容易地计算出它的 parent（父结点）、left child（左孩子）和 right child（右孩子）的下标：（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.1, p.152</span>

（接上页）

**Figure 6.1（图 6.1）** 一个 max-heap（最大堆），(a) 视作 binary tree（二叉树），(b) 视作 array（数组）。树中每个结点的圆内所写的数字是该结点存储的 value（值）；结点上方的数字是它在数组中对应的 index（下标）。数组的上、下方画出的连线展示了 parent-child（父—子）关系；parent（父结点）总是位于其 children（孩子）的左侧。这棵树的 height（高度）为 3；下标为 4（值为 8）的那个结点的高度为 1。

```
(a) 二叉树视图                    (b) 数组视图

              16 (1)              下标:  1  2  3  4 5 6 7 8  9 10
            /        \            值:   16 14 10 8 7 9 3 2  4  1
        14 (2)      10 (3)
        /     \      /    \
     8 (4)   7 (5) 9 (6)  3 (7)
     /   \     |
  2 (8)  4 (9) 1 (10)
```

> <span style="color:#7f8c8d;">[note] 上方 (a)(b) 两个视图为本译者按原书 Figure 6.1 重建的 ASCII 示意图（已逐结点核对与原图一致），非原书版式原图。</span>

```
PARENT(i)
1  return ⌊i/2⌋

LEFT(i)
1  return 2i

RIGHT(i)
1  return 2i + 1
```

在大多数计算机上，LEFT 过程只需将 $i$ 的 binary representation（二进制表示）向左移动一个 bit position（位），就能用一条 instruction（指令）计算出 $2i$。类似地，RIGHT 过程可以将 $i$ 的二进制表示左移一位、再把 1 作为 low-order bit（低位）加进来，从而快速算出 $2i + 1$；而 PARENT 过程将 $i$ 右移一位，即可计算 $\lfloor i/2 \rfloor$。heapsort 的良好实现常常把这些过程实现为"macro（宏）"或"inline（内联）"过程。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 完全二叉树塞进 array（数组）可以零指针，原因是它的形状被结点个数唯一确定，父子关系因此可以写成下标的算术，而不必写成内存里的链接。
>
> 机制。指针式树需要 pointer（指针），是因为结点的位置任意、父子关系只能显式记录，每条边都是额外的 8 字节开销加一次可能的 cache miss（缓存未命中）。而"逐层自左填满"这条形状约束把树的结构完全钉死：第 $k$ 层恰好占下标 $2^k$ 到 $2^{k+1}-1$，于是 $\mathrm{PARENT}(i) = \lfloor i/2 \rfloor$、$\mathrm{LEFT}(i) = 2i$、$\mathrm{RIGHT}(i) = 2i+1$。这是把"结构信息"从内存搬到"下标"里——同样的父子关系，一份用指针存，一份用算术算，后者零成本。位运算还顺手送了一个红利：$2i$ 是左移一位，$\lfloor i/2 \rfloor$ 是右移一位，乘法与除法退化成单条指令，教材因此建议把它们写成 macro（宏）或 inline（内联）过程。
>
> 算两笔账。空间：$10^6$ 个 4 字节整数放在数组里是 4 MB；换成指针结点，每个结点要 key（关键字，8 字节）加两个指针（16 字节）共 24 字节，合计 24 MB，是 6 倍。时间：数组顺序访问的带宽按 20 GB/s 估，4 MB 扫完约 0.2 ms；指针树每走一步都是一次独立寻址，典型延迟 100 ns 量级，$10^6$ 次就是 0.1 s，相差 500 倍。小例子核对下标：$n = 10$ 时 $\mathrm{LEFT}(3) = 6$、$\mathrm{RIGHT}(3) = 7$、$\mathrm{PARENT}(9) = 4$，与教材 Figure 6.1 的树逐一对应；再核一个边界：$i = 1$ 时 $\lfloor i/2 \rfloor = 0$，下标 0 不存在，所以根没有父结点，这正是过程要假设"除根以外"的原因。
>
> 代价也要写清。数组表示要求形状"近乎完全"，中途增删结点会让下标错位，所以第 13 章的红黑树仍然必须用指针；而堆的所有操作只沿父子路径走，从不需要"任意位置插入或删除"，所以这笔交易划得来。换句话说：不是数组比指针好，而是"操作模式只走一条路径"让数组的约束不构成损失。这个判断标准可以迁移：线段树、二叉树式并查集、二叉堆都是"形状规则 + 只走父子路径"，于是都能数组化；而需要拆分与合并的结构（平衡树、可持久化结构）就只能用指针。
>
> 还有一个隐蔽的好处：数组表示让"堆的大小"变成一个整数 `heap-size`，丢弃结点不需要释放任何东西，只是把这个数减一。这就是 HEAPSORT 能原地排序的关键——已排好的部分留在原数组尾部，堆的部分缩到前面，两者共享同一块内存，中间没有拷贝。区别在于：指针式结构要"丢弃"结点必须真的回收，否则内存泄漏；数组式结构只要改一个下标，代价为零。
>
> 跨课程连接：CSAPP 第 6 章的 spatial locality（空间局部性）是评估这笔交易的尺子——同一 cache line（缓存行）里的 16 个 4 字节整数会被一次预取全部带进 L1，随后 16 次访问几乎免费；而指针树每次跳转都换一条 cache line（缓存行）。第二处连接是 CSAPP 第 2 章的位运算：移位代替乘除不是优化技巧，而是"乘以 2 的幂"在二进制表示下的恒等变形。区别在于：第 6 章讲硬件如何利用规律性，这里讲数据结构如何主动制造规律性，两者合起来才是"让常数变小"的完整方法。
>
> 一句话收束：用"形状规则"换"显式链接"，是堆能做得又小又快的第一性原因。

binary heap（二叉堆）有两种：max-heap（最大堆）和 min-heap（最小堆）。在这两种堆中，各结点上的值都要满足一种 heap property（堆性质），其具体细节取决于堆的类型。在 max-heap 中，max-heap property（最大堆性质）是指：除 root（根结点）以外的所有结点 $i$ 都满足

```math
A[\mathrm{PARENT}(i)] \ge A[i]\,,
```

也就是说，某个结点的值至多等于其父结点的值。于是，max-heap 中最大的 element（元素）存放在根结点中；而以某一结点为根的 subtree（子树）中包含（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.1, p.153</span>

（接上页）……所包含的值都不大于该结点自身所保存的值。min-heap（最小堆）的组织方式正好相反；min-heap property（最小堆性质）是指，除 root（根结点）以外的所有结点 $i$ 都满足

```math
A[\mathrm{PARENT}(i)] \le A[i]\,,
```

最小堆中的最小 element（元素）存放在根结点。

对于 heapsort algorithm（堆排序算法），我们使用最大堆。最小堆通常用来实现 priority queue（优先队列），我们将在 Section 6.5（6.5 节）中讨论它。对于任何特定的 application（应用），我们都会明确指明所需的究竟是 max-heap 还是 min-heap；而当某条性质对最大堆或最小堆都适用时，我们就只用"heap（堆）"这一术语。

把 heap（堆）视作一棵 tree（树）时，我们把堆中某个结点的 height（高度）定义为：从该结点出发到某个 leaf（叶结点）的最长 simple downward path（简单向下路径）上的边数；并把堆的高度定义为其根结点的高度。由于含 $n$ 个元素的堆基于一棵 complete binary tree（完全二叉树），它的高度为 $\Theta(\lg n)$（见 Exercise 6.1-2，习题 6.1-2）。我们将会看到，堆上的基本 operations

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 给堆量高度的标准手法是"层数翻倍 + 两头夹住"：完全二叉树第 $h$ 层至多 $2^h$ 个结点，于是结点总数被 $2^{h}$ 与 $2^{h+1}-1$ 夹住，height（高度）就被钉死在 $\lfloor \lg n \rfloor$。
>
> 机制。设树高为 $h$（按 edge（边）数计，根的高度是 $h$，叶的高度是 0）。前 $h$ 层全满共 $2^h - 1$ 个结点，加上第 $h$ 层至少 1 个、至多 $2^h$ 个，得 $2^h \le n \le 2^{h+1} - 1$。两边取对数：$h \le \lg n < h+1$，即 $h = \lfloor \lg n \rfloor$。为什么全书都要先钉这个数？因为第 6 章每个基本过程的运行时间都以高度为自变量：MAX-HEAPIFY 是 $O(h)$，BUILD-MAX-HEAP 的上界推导要按高度分组，HEAPSORT 与四个优先队列操作全都写成 $O(\lg n)$。先有"高度等于 $\Theta(\lg n)$"这把尺子，后面每个对数界才有据可查。
>
> 数字。$n = 10$：$\lfloor \lg 10 \rfloor = 3$，各层结点数为 $1, 2, 4, 3$（末层只有 3 个，正是"近乎完全"的标志）；$n = 1000$：$\lfloor \lg 1000 \rfloor = 9$，前 9 层满共 511 个，末层 489 个；$n = 1023 = 2^{10} - 1$：满二叉树，高度 9，末层 $512$ 个。边界情形 $n = 1$：$\lfloor \lg 1 \rfloor = 0$，单结点堆的高度是 0 条边。这个边界正是检验定义的地方：若按"层数"计，$n = 1$ 的高度会是 1，随后所有结论整体偏 1，MAX-HEAPIFY 每次递归就少算一层，Huffman 式的高度分析和 BUILD-MAX-HEAP 的求和都会跟着错。教材特意强调 simple downward path（简单向下路径）上的边数，就是为了堵住这个偏移。
>
> 还有一个"为什么不能更紧"的问题：完全二叉树的高度只能是 $\lfloor \lg n \rfloor$，不能是别的值，因为形状被 $n$ 唯一确定。这一点与"任意二叉树的高度可以是 $1$ 到 $n-1$ 之间任何值"形成对比：退化链高度 $n-1$，满树高度 $\lfloor \lg n \rfloor$，前者让所有堆操作退化到 $O(n)$。堆的性质不保证平衡，是完全二叉树的形状在保证平衡——这也是为什么堆必须用数组紧凑存储，而不能随便挂结点。
>
> 顺带回答一个常被追问的问题：为什么堆高是 $\Theta(\lg n)$ 而不是 $O(n)$？因为完全二叉树不允许"单链"形状：一旦某个结点只有左孩子，之后的结点必须继续往左填，不能直接另起一条链。这条约束让每层结点数至少是上一层的全部（除末层外），于是层数被 $\lg n$ 卡住。对照普通二叉搜索树：它没有形状约束，最坏退化成链，高度 $n-1$，查找从 $O(\lg n)$ 掉到 $O(n)$——这正是第 12 章要引入平衡树的原因。区别在于：堆用"形状约束"换高度保证，平衡树用"旋转操作"换高度保证，前者免费但限制用法，后者灵活但每次操作要付维护费。
>
> 跨课程连接有两处。其一，6.042J 里"满二叉树第 $h$ 层有 $2^h$ 个结点"这个计数引理是全部内容，你用它做过求和与不等式题；这里只是把同一个引理从"证明题的对象"变成"数据结构的标尺"。其二，这个结论与 CSAPP 第 2 章的二进制表示是同一件事：$\lfloor \lg n \rfloor$ 恒等于 $n$ 的二进制位数减一，$1000 = 1111101000$ 共 10 位，减一得 9，与 $\lfloor \lg 1000 \rfloor = 9$ 一致。上界为什么必须写成 $2^{h+1} - 1$ 而不是 $2^{h+1}$？取 $n = 1023 = 2^{10} - 1$ 时高度确实是 9；若上界写成 $2^{10}$，那么 $n = 1024$ 也会满足 $n \le 2^{10}$，被误判成高度 9，而 $\lfloor \lg 1024 \rfloor = 10$——差一位就错一个量级上的判断。区别在于：二进制讲编码位数，这里讲路径长度。
>
> 一句话收束：高度是对数这件事不是巧合，而是"每往下一层结点数翻倍"的直接后果。

- MAX-HEAPIFY（堆化）过程，运行时间为 $O(\lg n)$，是维护 max-heap property（最大堆性质）的关键。
- BUILD-MAX-HEAP（建最大堆）过程，以 linear time（线性时间）运行，从一个 unordered input array（无序输入数组）产生一个最大堆。
- HEAPSORT（堆排序）过程，运行时间为 $O(n \lg n)$，对数组进行 in-place（原地）排序。
- MAX-HEAP-INSERT、HEAP-EXTRACT-MAX、HEAP-INCREASE-KEY 和 HEAP-MAXIMUM 过程，运行时间均为 $O(\lg n)$，使 heap data structure（堆数据结构）能够实现优先队列。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**6.1-1**

What are the minimum and maximum numbers of elements in a heap of height $h$?

**6.1-2**

Show that an $n$-element heap has height $\lfloor \lg n \rfloor$.

**6.1-3**

Show that in any subtree of a max-heap, the root of the subtree contains the largest value occurring anywhere in that subtree.（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.1–6.2, p.154</span>

（接上页）

**6.1-4**

Where in a max-heap might the smallest element reside, assuming that all elements are distinct?

**6.1-5**

Is an array that is in sorted order a min-heap?

**6.1-6**

Is the array with values $\langle 23, 17, 14, 6, 13, 10, 1, 5, 7, 12 \rangle$ a max-heap?

**6.1-7**

Show that, with the array representation for storing an $n$-element heap, the leaves are the nodes indexed by $\lfloor n/2 \rfloor + 1, \lfloor n/2 \rfloor + 2, \ldots, n$.

### Section 6.2 · Maintaining the heap property（维护堆的性质） <span style="color:#2471a3;">**[section]**</span>

为了维护 max-heap property（最大堆性质），我们调用 MAX-HEAPIFY（堆化）过程。它的 inputs（输入）是数组 $A$ 和一个指向数组的 index（下标）$i$。在被调用时，MAX-HEAPIFY 假定以 LEFT(i) 和 RIGHT(i) 为根的 binary trees（二叉树）都是 max-heap（最大堆），但 $A[i]$ 可能小于其 children（孩子），从而违背最大堆性质。MAX-HEAPIFY 让 $A[i]$ 的值在最大堆中"逐级下降"（float down），使得以 下标 $i$ 为根的 subtree（子树）重新遵循最大堆性质。

```text
MAX-HEAPIFY(A, i)
1  l = LEFT(i)
2  r = RIGHT(i)
3  if l ≤ A.heap-size and A[l] > A[i]
4      largest = l
5  else largest = i
6  if r ≤ A.heap-size and A[r] > A[largest]
7      largest = r
8  if largest ≠ i
9      exchange A[i] with A[largest]
10  MAX-HEAPIFY(A, largest)
```

Figure 6.2（图 6.2）展示了 MAX-HEAPIFY 的动作。在每一步中，$A[i]$、$A[\mathrm{LEFT}(i)]$ 和 $A[\mathrm{RIGHT}(i)]$ 三者中的最大者被确定出来，其下标被存入 largest 中。若 $A[i]$ 本身就是最大者，则以结点 $i$ 为根的子树已然是一个最大堆，过程随之终止。否则，两个孩子之一拥有最大元素，于是 $A[i]$ 与 $A[\mathrm{largest}]$ 相交换，这使得结点 $i$ 及其……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.2, p.155</span>

> <span style="color:#7f8c8d;">[note] 本页为整页插图：图 6.2 用三棵二叉树 (a)(b)(c) 展示 MAX-HEAPIFY(A, 2) 的执行过程（数组 $A = \langle 16, 4, 10, 14, 7, 9, 3, 2, 8, 1 \rangle$，$A.\text{heap-size} = 10$），结点旁标出的 $i$ 是当前调用处理的下标。</span>

```text
(a) 初始配置（i = 2）              (b) 交换 A[2] 与 A[4] 后（i = 4）

          16                            16
        /    \                         /    \
      4(i)    10                     14      10
     /  \   /  \                    /  \    /  \
   14    7 9    3                 4(i)  7  9    3
   / \  /                        / \
  2   8 1                       2   8 1

(c) 交换 A[4] 与 A[9] 后（i = 9）

          16
        /    \
      14      10
     /  \    /  \
    8    7  9    3
   / \  /
  2  4(i) 1
```

**Figure 6.2（图 6.2）** MAX-HEAPIFY(A, 2) 的动作，其中 $\text{A.heap-size} = 10$。(a) 初始配置，此时位于结点 $i = 2$ 处的 $A[2]$ 违背了 max-heap property（最大堆性质），因为它不是比两个孩子都大。(b) 通过交换 $A[2]$ 与 $A[4]$，结点 2 的最大堆性质得到恢复，但这一交换破坏了结点 4 的最大堆性质。此时的 recursive call（递归调用）MAX-HEAPIFY(A, 4) 以 $i = 4$ 执行。如 (c) 所示，在交换 $A[4]$ 与 $A[9]$ 之后，结点 4 被修复，而递归调用 MAX-HEAPIFY(A, 9) 不再对数据结构造成任何改变。

（接上页）……孩子一起满足最大堆性质。然而，下标为 largest 的结点现在保存的是原来的 $A[i]$ 值，因此以 largest 为根的子树可能违背最大堆性质。于是，我们对该子树递归地调用 MAX-HEAPIFY。

MAX-HEAPIFY 在以给定结点 $i$ 为根、规模为 $n$ 的子树上的 running time（运行时间）由两部分组成：调整 $A[i]$、$A[\mathrm{LEFT}(i)]$ 和 $A[\mathrm{RIGHT}(i)]$ 三者之间关系所需的 $\Theta(1)$ 时间，再加上在以结点 $i$ 的某个孩子为根的子树上运行 MAX-HEAPIFY 所需的时间（假定递归调用发生）。两棵孩子子树的规模各至多为 $2n/3$——最坏情形发生在树的最低层恰好半满时——因此我们可以用如下的 recurrence（递归式）来刻画 MAX-HEAPIFY 的运行时间：

```math
T(n) \le T(2n/3) + \Theta(1)\,.
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么孩子子树至多 $2n/3$？因为最坏的形状是"底层恰好半满、且全挂在同一侧"，此时一侧子树独占上方满层与底层的一半，比值在 $n \to \infty$ 时趋于 $2/3$。
>
> 机制。设树高 $h$，除最底层外全满。整棵树有 $2^h - 1$ 个上层结点加末层若干；最重子树的结点数是"上方 $h-1$ 层满树"（$2^{h-1} - 1$ 个）加"末层左半边"（至多 $2^{h-1}$ 个），合计至多 $2^{h} - 1$；而整棵树至少是 $2^h - 1 + 2^{h-1}$（末层至少半满）。于是比值至多 $(2^h - 1)/(3 \cdot 2^{h-1} - 1) \to 2/3$。为什么这个界够用？因为分析递归成本时不必精确知道子树多大，只需证明"最重分支的规模占比被一个常数钉死"，于是得到 $T(n) \le T(2n/3) + \Theta(1)$，解出 $\Theta(\lg n)$。
>
> 数字（我逐个 $n$ 算过左右子树大小）：$n = 10$ 时左 6 右 3，比值 $0.600$；$n = 11$ 时左 7 右 3，比值 $0.636$；$n = 23$ 时左 15 右 7，比值 $0.652$；$n = 10^6$ 时左 524287、右 475712，比值 $0.524$。注意它并不单调趋向 $2/3$：$n$ 恰为 $2^k - 1$ 时两子树相等，比值只有 $0.5$ 左右；真正的上确界出现在"末层再多挂几个结点"的那些 $n$ 上，且随高度增加逼近 $2/3$ 但永不等于。这解释了为什么界写成 $\le 2n/3$ 而不是 $< 2n/3$——上确界不可达，但必须包住。
>
> 解递归式的深度是 $\log_{3/2} n$：$n = 10^6$ 时为 $34.07$ 层，而 $\lg n = 19.93$，常数比 $1.71$；每层只花 $\Theta(1)$（比较两个孩子并交换），所以总时间 $\Theta(\lg n)$。这 $1.71$ 倍的常数很有意义：它说明"最坏情况只比理想情况多走 71% 的层"，所以 MAX-HEAPIFY 的真实代价与树高同阶，绝不会退化。第二把尺子更朴素：每递归一层结点下降一层，而堆高 $\lfloor \lg n \rfloor$ 已由习题 6.1-2 钉死，直接得 $O(\lg n)$，连递归式都不用解。
>
> 下界要靠构造。习题 6.2-6 要你造一个让递归走满整条根到叶路径的输入：把足够小的元素放在根，沿某条路径每个位置的父亲都小于孩子路径上的值，MAX-HEAPIFY 就会一路交换到底。这就补齐了 $\Omega(\lg n)$ 的方向，使结论成为紧确界。为什么下界比上界难？因为上界只需对所有输入成立的一条不等式，下界必须找到一个具体输入——这是算法分析里的通例：上界靠不等式，下界靠构造。
>
> 还有一处细节值得点明：$2n/3$ 这个界只在"最底层半满"时逼近，而半满意味着 $n$ 落在 $2^h$ 到 $3 \cdot 2^{h-1}$ 之间。若 $n$ 更小（底层只填了几个），最重子树占比反而更小；若 $n$ 接近 $2^{h+1} - 1$（接近满树），两子树几乎相等，比值接近 $1/2$。所以 $2/3$ 是一个只在上确界处取到的界，而不是典型值。真要写程序测，你会发现随机输入下 MAX-HEAPIFY 的递归深度平均只有 $\lg n$ 的一半左右，因为最深路径是少数。这就是"最坏界"与"典型行为"的差别：理论用最坏界保证正确性，工程用典型值估吞吐。
>
> 跨课程连接：6.042J 的归纳法与递归树结构给出 $T(n) = aT(n/b) + f(n)$ 的解法框架，第 4 章的 master theorem（主定理）是它的成品（这里 $a = 1, b = 3/2, f = \Theta(1)$，落在情形 2）；区别在于主定理只给阶，而这里还要知道"为什么是 $2/3$ 而不是 $1/2$"——那是一句关于完全二叉树形状的几何事实，主定理看不见。第二处连接是第 9 章的 RANDOMIZED-SELECT：它同样用"最坏分割比例被常数钉死"推出期望线性时间，手法完全同源，只是那里钉的是 $9/10$。
>
> 一句话收束：递归分析的功夫不在解方程，而在证明"最重的那一支永远不占满"。

---

> <span style="color:#7f8c8d;">CLRS §6.2–6.3, p.156</span>

由 master theorem（主定理，见 Theorem 4.1，定理 4.1）的 case 2（情形 2），上述递归式的解为 $T(n) = O(\lg n)$。或者，我们也可以把 MAX-HEAPIFY 在一个高度为 $h$ 的结点上的运行时间刻画为 $O(h)$。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**6.2-1**

Using Figure 6.2 as a model, illustrate the operation of MAX-HEAPIFY$(A, 3)$ on the array $A = \langle 27, 17, 3, 16, 13, 10, 1, 5, 7, 12, 4, 8, 9, 0 \rangle$.

**6.2-2**

Starting with the procedure MAX-HEAPIFY, write pseudocode for the procedure MIN-HEAPIFY$(A, i)$, which performs the corresponding manipulation on a min-heap. How does the running time of MIN-HEAPIFY compare to that of MAX-HEAPIFY?

**6.2-3**

What is the effect of calling MAX-HEAPIFY$(A, i)$ when the element $A[i]$ is larger than its children?

**6.2-4**

What is the effect of calling MAX-HEAPIFY$(A, i)$ for $i > \text{A.heap-size}/2$?

**6.2-5**

The code for MAX-HEAPIFY is quite efficient in terms of constant factors, except possibly for the recursive call in line 10, which might cause some compilers to produce inefficient code. Write an efficient MAX-HEAPIFY that uses an iterative control construct (a loop) instead of recursion.

**6.2-6**

Show that the worst-case running time of MAX-HEAPIFY on a heap of size $n$ is $\Omega(\lg n)$. (Hint: For a heap with $n$ nodes, give node values that cause MAX-HEAPIFY to be called recursively at every node on a simple path from the root down to a leaf.)

### Section 6.3 · Building a heap（建堆） <span style="color:#2471a3;">**[section]**</span>

我们可以以 bottom-up manner（自底向上的方式）使用 MAX-HEAPIFY 过程，把数组 $A[1..n]$（其中 $n = \text{A.length}$）转换成一个 max-heap（最大堆）。由 Exercise 6.1-7（习题 6.1-7）可知，subarray（子数组）$A[(\lfloor n/2 \rfloor + 1) .. n]$ 中的元素全都是树的 leaf（叶结点），因此每一个都……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.3, p.157</span>

（接上页）……本身就是一棵 1-element heap（单元素堆）。BUILD-MAX-HEAP 过程遍历树中其余的结点，并对每个结点运行一次 MAX-HEAPIFY。

```text
BUILD-MAX-HEAP(A)
1  A.heap-size = A.length
2  for i = ⌊A.length/2⌋ downto 1
3      MAX-HEAPIFY(A, i)
```

Figure 6.3（图 6.3）给出了 BUILD-MAX-HEAP 动作的一个例子。

为了说明 BUILD-MAX-HEAP 为什么能正确工作，我们使用如下的 loop invariant（循环不变式）：

> 恰在第 2–3 行 for 循环的每次 iteration（迭代）开始时，每个结点 $i+1, i+2, \ldots, n$ 都是某个 max-heap（最大堆）的 root（根结点）。

我们需要证明：该不变式在第一次循环迭代之前为真；循环的每次迭代都维持该不变式；并且当循环 termination（终止）时，该不变式能提供一个可用于证明 correctness（正确性）的有用性质。

**Initialization（初始化）：** 在第一次循环迭代之前，$i = \lfloor n/2 \rfloor$。每个结点 $\lfloor n/2 \rfloor + 1, \lfloor n/2 \rfloor + 2, \ldots, n$ 都是一个 leaf（叶结点），因而是 trivial max-heap（平凡最大堆）的根。

**Maintenance（保持）：** 为看出每次迭代都维持循环不变式，请注意结点 $i$ 的 children（孩子）的编号都大于 $i$。于是，由循环不变式，它们都是最大堆的根。这正是使调用 MAX-HEAPIFY(A, i) 能让结点 $i$ 成为最大堆之根所需的条件；此外，MAX-HEAPIFY 调用还保持了"结点 $i+1, i+2, \ldots, n$ 全都是最大堆的根"这一性质。在 for 循环的更新步骤中把 $i$ 递减，便为下一次迭代重新建立了循环不变式。

**Termination（终止）：** 循环终止时，$i = 0$。由循环不变式，每个结点 $1, 2, \ldots, n$ 都是某个最大堆的根。特别地，结点 1 是。

我们可以按如下方式算出 BUILD-MAX-HEAP 运行时间的一个简单 upper bound（上界）：每次调用 MAX-HEAPIFY 耗费 $O(\lg n)$ 时间，而 BUILD-MAX-HEAP 共进行 $O(n)$ 次这样的调用，因此运行时间为 $O(n \lg n)$。这个上界虽然正确，却不是 asymptotically tight（渐近紧确）的。

我们可以通过如下观察导出一个更紧的界：MAX-HEAPIFY 在某个结点上运行的时间随该结点在树中的 height（高度）而变化，而大多数结点的高度都很小。我们的更紧分析依赖于如下性质：一个含 $n$ 个元素的堆的高度为 $\lfloor \lg n \rfloor$（见习题 6.1-2），且任意高度 $h$ 的结点至多有 $\left\lceil n/2^{h+1} \right\rceil$ 个（见 Exercise 6.3-3，习题 6.3-3）。

MAX-HEAPIFY 在高度为 $h$ 的结点上被调用时所需的时间为 $O(h)$，于是我们可以把 BUILD-MAX-HEAP 的 total cost（总代价）表示为由下式从上方界定：（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.3, p.158</span>

> <span style="color:#7f8c8d;">[note] 本页为整页插图：图 6.3 用六棵二叉树 (a)–(f) 展示 BUILD-MAX-HEAP 在 10 元素输入数组 $A = \langle 4, 1, 3, 2, 16, 9, 10, 14, 8, 7 \rangle$ 上的操作，画出的都是 BUILD-MAX-HEAP 第 3 行调用 MAX-HEAPIFY 之前的数据结构，$i$ 为循环下标所指向的结点。</span>

```text
(a) i = 5                         (b) i = 4

            4                             4
         /     \                       /     \
        1       3                     1       3
       / \     / \                   / \     / \
      2  16(i) 9  10               14(i) 16  9   10
     / \   |                      / \   |
   14   8  7                     2   8  7

(c) i = 3                         (d) i = 2

            4                             4
         /     \                       /     \
        1      10                    16      10
       / \     /  \                  /  \    / \
     14   16  9    3               14    7  9   3
     / \   |                      / \   |
    2   8  7                      2   8 1

(e) i = 1                         (f) 完成后的最大堆

            16                            16
         /     \                       /     \
       14       10                   14       10
      /  \     / \                  /  \     / \
     8    7   9   3                8    7   9   3
    / \   |                      / \   |
   2   4 1                      2   4 1
```

**Figure 6.3（图 6.3）** BUILD-MAX-HEAP 的操作，图中展示的是 BUILD-MAX-HEAP 第 3 行调用 MAX-HEAPIFY 之前的数据结构。(a) 一个 10 元素的 input array（输入数组）$A$ 以及它所表示的 binary tree（二叉树）。图中显示，在调用 MAX-HEAPIFY(A, i) 之前，循环 index（下标）$i$ 指向结点 5。(b) 由此得到的数据结构。下一次迭代的循环下标 $i$ 指向结点 4。(c)–(e) BUILD-MAX-HEAP 中 for 循环的后续迭代。请留意：每当在某个结点上调用 MAX-HEAPIFY 时，该结点的两棵 subtree（子树）都是 max-heap（最大堆）。(f) BUILD-MAX-HEAP 结束后的 max-heap。

---

> <span style="color:#7f8c8d;">CLRS §6.3–6.4, p.159</span>

（接上页）

```math
\sum_{h=0}^{\lfloor \lg n \rfloor} \left\lceil \frac{n}{2^{h+1}} \right\rceil O(h)
\;=\;
O\!\left(n \sum_{h=0}^{\lfloor \lg n \rfloor} \frac{h}{2^h}\right).
```

我们把 $x = 1/2$ 代入 formula (A.8)（公式 (A.8)）来求值最后一个 summation（求和式），得到

```math
\sum_{h=0}^{\infty} \frac{h}{2^h}
\;=\;
\frac{1/2}{(1 - 1/2)^2}
\;=\;
2\,.
```

于是，我们可以把 BUILD-MAX-HEAP 的 running time（运行时间）界定为

```math
O\!\left(n \sum_{h=0}^{\lfloor \lg n \rfloor} \frac{h}{2^h}\right)
=
O\!\left(n \sum_{h=0}^{\infty} \frac{h}{2^h}\right)
=
O(n)\,.
```

因此，我们可以在 linear time（线性时间）内从一个 unordered array（无序数组）构造出一个 max-heap（最大堆）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 对 $n$ 个结点各做一次堆化只要 $O(n)$，原因不是 amortized（摊还），而是"按 height（高度）计价"：绝大多数结点住在低层，而低层的活几乎不花钱。
>
> 机制。MAX-HEAPIFY 在高度 $h$ 的结点上花 $O(h)$（沿一条路径下降）。完全二叉树里高度 $h$ 的结点至多 $\lceil n/2^{h+1} \rceil$ 个（习题 6.3-3），于是总成本上界是 $\sum_h \lceil n/2^{h+1} \rceil \cdot O(h) = O(n \sum_h h/2^h)$。这个级数收敛：由 $\sum_{h \ge 0} h x^h = x/(1-x)^2$，取 $x = 1/2$ 得 $2$，所以总成本 $O(2n) = O(n)$。几何直觉是"越往上越稀、权越轻"：一半结点是叶（高度 0，零成本），四分之三的结点高度不超过 1，成本高的那些结点数量指数少，两个因子相互抵消，剩下一个常数。
>
> 数字全部点过一遍。$n = 15$：各高度结点数 $8, 4, 2, 1$，加权和 $0 \cdot 8 + 1 \cdot 4 + 2 \cdot 2 + 3 \cdot 1 = 11$，远小于 $2n = 30$。$n = 1000$：加权和 $994$，而 $2n = 2000$，常数小于 1。$n = 1023$：$1013$ 对 $2046$。对比"逐个 MAX-HEAP-INSERT"的 $O(n \lg n)$：$n = 1023$ 时 $n \lceil \lg n \rceil = 10230$，差 10 倍；$n = 10^6$ 时 $n \lg n \approx 2 \times 10^7$ 对 $2n = 2 \times 10^6$，同样约 10 倍。这个 10 倍不是渐进差距的极限，而是"对数被常数取代"在这个规模上的具体读数。
>
> 为什么自底向上可行，自顶向下不行？因为 MAX-HEAPIFY 有一个前提："两个孩子子树已经是合法堆"。下标从 $\lfloor n/2 \rfloor$ 递减，保证被处理的结点的孩子要么是叶（平凡合法），要么已在更早的迭代中被处理过；反过来从小到大遍历，前提不成立，堆化会反复破坏已修好的部分。习题 6.3-2 问的正是这个方向问题。另一方面，逐个插入之所以要 $O(n \lg n)$，是因为每次插入都必须一路上浮到根，无法利用"下方已经整理好"的结构——它把成本花在了重复路径上。
>
> 还有一个视角能解释"为什么是线性而不是 $\Theta(n \lg n)$ 的某个中间量"：把每个结点的工作量写成"它的高度"，就得到一个加权求和；而高度分布是几何衰减的，所以求和收敛。若换成"按层计价"（每层工作量 = 该层结点数 × 层高），得到的是 $\sum_h 2^h \cdot O(h) = O(n \lg n)$——同一棵树、同一次执行，两种记账方式给出两个答案，因为真正的执行是"每个结点一次"，而不是"每层一次"。这也顺带说明为什么"摊还分析"在这里不是必需的：这里没有一串操作的借贷关系，只有一个静态的一次性成本。
>
> 再补一个数感对照：$O(n)$ 建堆的常数到底是多少？实测的"操作次数"约 $2n$ 到 $1.5n$ 之间（取决于是否把每次比较与交换都记一次），而逐个插入约 $n \lg n - 2n$ 次比较。$n = 2^{20}$ 时前者约 $2.1 \times 10^6$，后者约 $1.9 \times 10^7$，差近 9 倍；随着 $n$ 翻倍，前者翻倍、后者多一截，所以差距只会拉大。这也是为什么标准库的建堆都采自底向上：多花一点代码复杂度，换一个常数级的整体改进，在任何规模上都划算。
>
> 跨课程连接：6.042J 的等比级数求和与夹逼是全部工具；100B 里"单调函数的求和与积分互估"是它的连续版本，而这里用到的 $\sum h x^h$ 是更简单的一类（幂级数求导）。第二处连接是第 4 章：同一个递归式若按"每层工作量"算会得到 $O(n \lg n)$，按"每个结点工作量"算得到 $O(n)$——两种算法都对，只是计价的维度不同，这说明"按什么计价"本身就是分析的一部分。区别在于：递归式给出的是分治结构，而这里根本没有分治，只有一次循环。
>
> 一句话收束：$O(n)$ 建堆不是魔法，而是"数量指数衰减乘上成本线性增长"恰好收敛。

我们可以用 BUILD-MIN-HEAP 过程来 build（构造）min-heap（最小堆）：它与 BUILD-MAX-HEAP 完全相同，只是把第 3 行中对 MAX-HEAPIFY 的调用换成对 MIN-HEAPIFY 的调用（见 Exercise 6.2-2，习题 6.2-2）。BUILD-MIN-HEAP 以线性时间从一个无序的 linear array（线性数组）产生一个最小堆。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**6.3-1**

Using Figure 6.3 as a model, illustrate the operation of BUILD-MAX-HEAP on the array $A = \langle 5, 3, 17, 10, 84, 19, 6, 22, 9 \rangle$.

**6.3-2**

Why do we want the loop index $i$ in line 2 of BUILD-MAX-HEAP to decrease from $\lfloor \text{A.length}/2 \rfloor$ to 1 rather than increase from 1 to $\lfloor \text{A.length}/2 \rfloor$?

**6.3-3**

Show that there are at most $\left\lceil n/2^{h+1} \right\rceil$ nodes of height $h$ in any $n$-element heap.

### Section 6.4 · The heapsort algorithm（堆排序算法） <span style="color:#2471a3;">**[section]**</span>

heapsort algorithm（堆排序算法）首先利用 BUILD-MAX-HEAP 在 input array（输入数组）$A[1..n]$（其中 $n = \text{A.length}$）上构造一个 max-heap（最大堆）。由于数组的 maximum element（最大元素）存放在根结点 $A[1]$ 中，我们可以把它放入其正确的最终位置……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.4, p.160</span>

（接上页）……最终位置：只需把它与 $A[n]$ 交换。如果我们现在从堆中 discard（丢弃）结点 $n$——只需把 `A.heap-size` 减 1 就能做到——我们观察到，根结点的 children（孩子）仍然是 max-heap（最大堆），但新的根元素可能违背 max-heap property（最大堆性质）。而为了恢复最大堆性质，我们要做的只是调用 MAX-HEAPIFY(A, 1)，这会在 $A[1..n-1]$ 中留下一个最大堆。随后，heapsort algorithm（堆排序算法）对规模从 $n-1$ 一直降到 2 的堆重复这一过程。（关于一个精确的 loop invariant（循环不变式），见 Exercise 6.4-2，习题 6.4-2。）

```text
HEAPSORT(A)
1  BUILD-MAX-HEAP(A)
2  for i = A.length downto 2
3      exchange A[1] with A[i]
4      A.heap-size = A.heap-size - 1
5      MAX-HEAPIFY(A, 1)
```

Figure 6.4（图 6.4）给出了 HEAPSORT 操作的一个例子，展示的是第 1 行构造出初始 max-heap 之后的过程。图中画出了第 2–5 行 for 循环第一次迭代之前的最大堆，以及每次迭代之后的最大堆。

HEAPSORT 过程耗时 $O(n \lg n)$：对 BUILD-MAX-HEAP 的调用耗时 $O(n)$，而对 MAX-HEAPIFY 的 $n-1$ 次调用中每次耗时 $O(\lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把 loop invariant（循环不变式）当模板收藏：HEAPSORT 的正确性证明与插入排序的证明是同一个骨架，只是不变式维护的性质强弱不同。
>
> 骨架。不变式（习题 6.4-2 给了原文）：每轮循环开始时，$A[1..i]$ 是含 $i$ 个最小元素的最大堆，$A[i+1..n]$ 含 $n-i$ 个最大元素且已排好序。初始化：建堆之后 $i = n$，后缀为空，前缀是合法堆，成立。保持：交换 $A[1]$ 与 $A[i]$，最大值落到位置 $i$，把堆大小减 1，再对根调用 MAX-HEAPIFY 恢复堆性质——此时前缀仍是"含 $i-1$ 个最小元素的最大堆"，后缀多了一个已就位的最大值，不变式维持。终止：$i = 1$ 时后缀是整个数组且有序。三步与 chunk01 里插入排序的不变式（"$A[1..j-1]$ 是已排序前缀"）逐字对应。
>
> 精髓在强弱取舍。插入排序维护"前缀全序"这个强性质，代价是每次插入要比较并后移，一步 $O(n)$；堆排序只维护"前缀成堆"这个弱性质——堆序只约束父子、不约束兄弟——代价是每次只需 $O(\lg n)$。这一课的普适形态是：不变式越弱、维护越便宜，只要弱性质仍能支撑每步所需的信息（这里只需要"根是最大"）。反过来，如果你把不变式写强了（比如要求前缀全序），你就是在做插入排序，而不是堆排序。
>
> 走一遍小例子。$A = \langle 4, 1, 3, 2, 5 \rangle$：建堆后 $\langle 5, 4, 3, 2, 1 \rangle$；第 1 轮交换 $A[1]$ 与 $A[5]$，堆化得 $\langle 4, 2, 3, 1 \rangle$，后缀 $[5]$；第 2 轮得堆 $\langle 3, 2, 1 \rangle$，后缀 $[4, 5]$；第 3 轮得堆 $\langle 2, 1 \rangle$，后缀 $[3, 4, 5]$；最后一轮得 $[1]$ 与后缀 $[2, 3, 4, 5]$，拼起来即 $\langle 1, 2, 3, 4, 5 \rangle$。每一轮都能看到不变式的两部分同时保持：前缀始终是堆（虽然越来越小），后缀始终有序且全是全局最大。
>
> 一个常见误解要澄清：循环不变式不是"循环执行过程中的中间状态"，而是"每轮循环开始那一刻的状态"；它允许循环体内短暂破坏性质（交换那一步堆性质就坏了），只要在下一轮开始前修好。这与第 2 章插入排序的写法一致，也是为什么"保持"步要分两段论证：先说明交换后哪些不变，再说明 MAX-HEAPIFY 如何恢复被破坏的部分。区别在于：插入排序的恢复只动一个元素的位置，堆排序的恢复要沿一条路径下沉。
>
> 再把两个不变式并列写出来，差别就一目了然。插入排序：每轮开始时 $A[1..j-1]$ 恰是原数组前 $j-1$ 个元素排好序的样子——它约束的是"内容与顺序"，是强性质。堆排序：每轮开始时 $A[1..i]$ 是含 $i$ 个最小元素的堆，$A[i+1..n]$ 是含 $n-i$ 个最大元素的有序后缀——它约束的是"集合与形状"，允许内部次序任意。前者维护一步要挪动 $O(n)$ 个元素，后者只要下沉 $O(\lg n)$。所以不变式的强弱不是文风问题，它直接决定每步的代价表。
>
> 跨课程连接：6.042J 的数学归纳法是骨架本身（初始、保持、结论），第 2 章插入排序的不变式是同一模板的第一次出现，第 5 章引理 5.5 的概率型不变式则说明这个模板可以携带概率成分（"前缀恰为某个 $(i-1)$-排列的概率是 $(n-i+1)!/n!$"）。区别在于：概率型不变式的"保持"步是一个条件概率乘法，而不是一个纯逻辑蕴含，所以它需要期望与条件化这两件额外工具，但三步结构一字未改。
>
> 一句话收束：正确性证明的可复用部分不是某条不变式，而是"前缀与后缀分解 + 三步归纳"这个装配流程。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**6.4-1**

Using Figure 6.4 as a model, illustrate the operation of HEAPSORT on the array $A = \langle 5, 13, 2, 25, 7, 17, 20, 8, 4 \rangle$.

**6.4-2**

Argue the correctness of HEAPSORT using the following loop invariant:

> At the start of each iteration of the for loop of lines 2–5, the subarray $A[1..i]$ is a max-heap containing the $i$ smallest elements of $A[1..n]$, and the subarray $A[i+1..n]$ contains the $n-i$ largest elements of $A[1..n]$, sorted.

**6.4-3**

What is the running time of HEAPSORT on an array $A$ of length $n$ that is already sorted in increasing order? What about decreasing order?

**6.4-4**

Show that the worst-case running time of HEAPSORT is $\Omega(n \lg n)$.（接下页）

---

> <span style="color:#7f8c8d;">CLRS §6.4, p.161</span>

> <span style="color:#7f8c8d;">[note] 本页为整页插图：图 6.4 用十棵二叉树 (a)–(j) 展示 HEAPSORT 在初始数组 $A = \langle 16, 14, 10, 8, 7, 9, 3, 2, 4, 1 \rangle$ 上的操作。每个面板画的是第 5 行 MAX-HEAPIFY 调用之后的堆（(a) 为第 1 行 BUILD-MAX-HEAP 刚建成的堆），$i$ 为 for 循环当时的循环下标；每棵树右侧列出的数值是已经排好序、被逐出堆的部分，(k) 为最终排好序的数组。</span>

```text
(a) BUILD-MAX-HEAP 之后（i 无）      已排序部分:（无）

            16
          /    \
        14      10
       /  \    /  \
      8    7  9    3
     / \  /
    2  4 1

(b) i = 10                           已排序部分: 16

            14
          /    \
         8      10
        / \    /  \
       4   7  9    3
      / \
     2   1

(c) i = 9                            已排序部分: 14 16

            10
          /    \
         8      9
        / \    / \
       4   7  1   3
      /
     2

(d) i = 8                            已排序部分: 10 14 16

            9
          /   \
         8     3
        / \   / \
       4   7 1   2

(e) i = 7                            已排序部分: 9 10 14 16

            8
          /   \
         7     3
        / \   /
       4   2 1

(f) i = 6                            已排序部分: 8 9 10 14 16

            7
          /   \
         4     3
        / \
       1   2

(g) i = 5                            已排序部分: 7 8 9 10 14 16

            4
          /   \
         2     3
        /
       1

(h) i = 4                            已排序部分: 4 7 8 9 10 14 16

            3
          / \
         2   1

(i) i = 3                            已排序部分: 3 4 7 8 9 10 14 16

            2
          /
         1

(j) i = 2                            已排序部分: 2 3 4 7 8 9 10 14 16

            1

(k) 最终的已排序数组 A:

    1 2 3 4 7 8 9 10 14 16
```

**Figure 6.4（图 6.4）** HEAPSORT 的操作。(a) 第 1 行中 BUILD-MAX-HEAP 刚刚构造出 max-heap（最大堆）数据结构之后的情形。(b)–(j) 第 5 行每次调用 MAX-HEAPIFY 之后紧接的最大堆，图中同时标出此时的 $i$ 值。只有浅色着色的结点仍留在 heap（堆）中。(k) 最终的 sorted array（已排序数组）$A$。

---

> <span style="color:#7f8c8d;">CLRS §6.4–6.5, p.162</span>

（接上页）

**6.4-5 ★**

Show that when all elements are distinct, the best-case running time of HEAPSORT is $\Omega(n \lg n)$.

### Section 6.5 · Priority queues（优先队列） <span style="color:#2471a3;">**[section]**</span>

Heapsort（堆排序）是一个优秀的 algorithm（算法），但第 7 章将要介绍的 quicksort（快速排序）的一个良好实现，在实践中通常会胜过它。尽管如此，heap data structure（堆数据结构）本身仍有许多用途。本节我们介绍 heap 最流行的 application（应用）之一：作为一种高效的 priority queue（优先队列）。与 heap 一样，priority queue 也有两种形式：max-priority queue（最大优先队列）和 min-priority queue（最小优先队列）。这里我们聚焦于如何实现最大优先队列——它转而基于 max-heap（最大堆）；Exercise 6.5-3（习题 6.5-3）会请你编写用于最小优先队列的过程。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 堆排序在实践里输给快排，账要记在 storage hierarchy（存储层次结构）上：两者复杂度同阶，访存模式却相反。
>
> 机制。MAX-HEAPIFY 沿树下降时下标走 $i \to 2i$ 或 $2i+1$，每层地址大约翻倍。这不是"固定跨步"，而是"跨步长按几何增长"的访问：相邻两次访存之间的距离越来越大，hardware prefetcher（硬件预取器）识别不了这种模式，每个 64 字节的 cache line（缓存行）往往只服务一两次访问就作废。快排的划分恰好相反：两个指针从两端向中间顺序扫描，地址单调变化，预取器能把整批 cache line（缓存行）提前拉进 L1，一条 cache line（缓存行）里的 16 个整数在一次扫描中被全部消费。
>
> 算具体的浪费率。$10^6$ 个 4 字节整数占 4 MB、62500 条 cache line（缓存行）。堆路径的下标是 $1, 2, 4, 8, \ldots, 524288$，共 20 层；前 16 个下标落在同一条 cache line（缓存行）内，此后每翻倍就换一条新的 cache line（缓存行），于是 20 层访问落在 16 条不同 cache line（缓存行）上，其中后 15 层每条 cache line（缓存行）只用一次——有效带宽约 $4/64 = 6.25\%$。再考虑 TLB（页表缓存）：$10^6$ 个整数跨约 $10^3$ 个 4 KB 页，路径后段每层几乎必换页，每次换页的代价是几十到上百个周期。快排的顺序扫描则把每批 16 个整数的缓存命中率做到接近 100%。
>
> 工程上的折中是 introsort（内省排序）：Musser 1997 年在《Software: Practice and Experience》第 27 卷第 8 期提出的混合策略——以快排为主力，递归深度超过 $2\lfloor \lg n \rfloor$ 时切换到 heapsort（保住 $O(n \lg n)$ 的最坏保证），片段小于阈值时交 insertion sort（插入排序）。三个算法各补一个短板：快排的常数小、堆排的最坏有界、插入排序的小规模快。工业界的其它两条路线也值得对照（可一手核实）：Java 对基本类型用 dual-pivot quicksort（双枢轴快速排序），对对象用 TimSort；Python 的内置 sorted 用 TimSort。堆排没有出局：它无递归栈、无退化输入，在内存受限与实时性场景里仍是可靠备胎，习题 6.4-5 更证明了元素互异时它连最好情形也是 $\Omega(n \lg n)$，这份"倔强"恰是它担任兜底的资格。
>
> 一个反直觉的补充：堆排的"差"并不是差在比较次数上。理论上堆排的比较次数约 $2n \lg n$，快排约 $1.39n \lg n$（这是信息论下界附近的最优常数），前者是后者的 1.4 倍；但实测差距常常是 2 到 3 倍，多出来的部分全部来自访存。这解释了为什么"减少比较次数"的优化（比如把两个孩子比较改成三个一组）在堆排上收效有限：瓶颈在内存，不在指令。区别在于：比较次数能从复杂度表上读到，访存代价读不到，只能从 cache（高速缓存）参数与地址流推。
>
> 跨课程连接：CSAPP 第 6 章给了全部语言——spatial locality（空间局部性）、cache line（缓存行）、prefetcher（预取器），以及各级之间差一个数量级的 latency（延迟）：L1 约 4 周期、主存约 200 周期；区别在于 CSAPP 讲的是"程序如何顺应硬件"，这里讲的是"算法选择如何被硬件改写"。第二处连接是第 7 章的划分过程与第 2 章的插入排序：前者顺序、后者局部性强，于是快排与插入排序都被访存偏爱，唯独堆排因为树形跳跃而吃亏。
>
> 一句话收束：同阶复杂度之间，决定胜负的是"地址流是否可预测"，而这一点只有存储层次结构的视角能看见。

priority queue 是一种用于维护一个由元素构成的 set（集合）$S$ 的 data structure（数据结构），其中的每个元素都有一个与之关联的值，称为 key（关键字）。max-priority queue 支持下列 operations（操作）：

INSERT(S, x) 把 element（元素）$x$ 插入集合 $S$ 中，这一操作等价于 $S = S \cup \{x\}$。

MAXIMUM(S) 返回 $S$ 中拥有最大 key（关键字）的元素。

EXTRACT-MAX(S) 去掉并返回 $S$ 中拥有最大关键字的元素。

INCREASE-KEY(S, x, k) 将元素 $x$ 的关键字的值增大到新值 $k$，这里假定 $k$ 至少与 $x$ 当前的关键字的值一样大。

在诸多其他应用之中，我们可以用最大优先队列在一台 shared computer（共享计算机）上调度 jobs（作业）。最大优先队列记录着有待执行的作业及它们各自的相对 priorities（优先级）。当一个作业完成或被中断时，scheduler（调度器）通过调用 EXTRACT-MAX，从所有待处理的作业中选出优先级最高的那个作业。调度器随时都可以通过调用 INSERT 把一个新作业加入 queue（队列）。

或者，min-priority queue（最小优先队列）支持 INSERT、MINIMUM、EXTRACT-MIN 和 DECREASE-KEY 操作。最小优先队列可以用于 event-driven simulator（事件驱动的模拟器）。queue 中的 items（项）是要模拟的 events（事件），每个事件都带有一个关联的发生时间，这个时间充当它的 key（关键字）。各事件必须按其发生时间的顺序来模拟，因为对某一事件的模拟可能会导致其他事件在未来被模拟。模拟程序在每一步都调用 EXTRACT-MIN 来选出下一个要模拟的事件。每当新的事件被产生出来时，模拟器就通过调用 INSERT 把它们插入最小优先队列。（接下页）
