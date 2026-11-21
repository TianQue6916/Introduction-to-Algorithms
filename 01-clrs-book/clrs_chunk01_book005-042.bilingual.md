# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk01 · 书页 5–42（第 1 章 + 第 2 章） · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §1.1, p.5</span>

## Chapter 1 · The Role of Algorithms in Computing（算法在计算中的作用）

什么是算法（algorithm）？为什么研究算法是有价值的？相对于计算机所使用的其他技术，算法又扮演着什么角色？在本章中，我们将回答这些问题。

### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

非正式地说，算法是任何定义良好的计算过程（computational procedure），它以某个值或一组值作为输入（input），并产生某个值或一组值作为输出（output）。因此，算法就是一系列计算步骤（computational steps），把输入转换为输出。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 别放过 well-defined（定义良好）这个限定词——它是整个学科的第一性原理：只有它，才能让“计算”变成一个可以被证明的对象。
>
> 先把对象说清。一个 computational problem（计算问题）的本质，是输入集合与输出集合之间的一条 relation（关系）；algorithm（算法）则是这条关系的有限、无歧义、可执行的描述。所谓 well-defined（定义良好），含义很窄也很硬：给定同样的输入、同样的中间状态，下一步做什么只有唯一的答案。这一条要求就是 determinism（确定性）的全部来源。没有它，同一个输入可以走出多条执行路径、给出不同输出，输出就不再是输入的函数；“该 algorithm（算法）对所有输入都给出满足 spec（规约）的答案”这句话连主语都立不住。
>
> 给一个能数出来的例子。sorting problem（排序问题）的 spec（规约）只要求 key（关键字）非递减，没有规定相等 key 的相对次序。取三条记录 $(2,\text{a})$, $(1,\text{b})$, $(2,\text{c})$，只按 key（关键字）排，输出必须是 $(1,\text{b})$ 后跟两个含 2 的记录，而这两条记录的先后有两种排法，于是恰好有 $2!=2$ 个输出都满足 spec（规约）。一般地，若输入里有 $k$ 个相等的 key（关键字），合格输出就有 $k!$ 个。想让“正确”变成唯一结论，必须在 spec（规约）里追加 stable（稳定）条件——相等 key 保持原始相对次序；追加之后合格输出从 2 个降到 1 个。这就是 spec（规约）的精度直接决定 correctness（正确性）命题强度的具体形态。
>
> 与 6.042J 的连接。你在 6.042J 里养成的次序是“先把命题陈述写精确，再动笔证明”，这里完全同构：spec（规约）是命题的陈述，algorithm（算法）是构造性证明，correctness（正确性）证明是把两者接起来的那一步。区别在于，数学命题的真假是客观的，而 spec（规约）是人选的：写宽了（“任何排列都算对”）correctness（正确性）容易满足却毫无信息量；写窄了（要求相等元素也按某个特定次序落位）可能根本无解，或者逼出你不需要付的代价。
>
> 还有两个必须分开的条件。termination（终止）与 partial correctness（部分正确性）是两件事：CLRS 第 2 章的 loop invariant（循环不变式）只覆盖后者，必须再证循环必然终止，二者合起来才是 total correctness（完全正确性）。反例很便宜：把 while 的守卫改成恒真，loop invariant（循环不变式）照旧成立，但 algorithm（算法）永不停机，“对所有输入都停机并输出满足 spec（规约）的结果”立刻为假。
>
> 所以第一性原理可以压成一句判据：动手设计之前先问 spec（规约）写清了没有。写清了才有 theorem（定理）可证；写不清，最多只是 demo（演示）。
>
> 还有一个常被忽略的点：well-defined（定义良好）是相对于“状态”说的，不是相对于“实现”说的。同一个 algorithm（算法）可以用 array（数组）实现，也可以用 linked list（链表）实现，只要每一步的操作语义唯一，它在 pseudocode（伪代码）层面仍然是 well-defined（定义良好）的；反过来，一条“随机选一个未排序元素”的指令就不是 well-defined（定义良好）的，因为它没有指定选哪个——这正是 randomized algorithm（随机化算法）必须显式引入随机源、并把结论改写成 expected running time（期望运行时间）的原因。
>
> 给一条能用的检验判据：拿两个故意写坏的实现去套你的 spec（规约），看它能不能把它们判错。若两个行为不同、甚至一个死循环的实现都能通过，spec（规约）太松；若连教科书上的标准 algorithm（算法）都过不了，spec（规约）太紧。能一句话说清“谁不合格”的 spec（规约），才是能支撑证明的 spec（规约）。

我们也可以把算法看作解决一个规定明确的计算问题（computational problem）的工具。问题的陈述用一般性的语言规定了所期望的输入/输出关系（input/output relationship）；算法则描述了实现这一输入/输出关系的具体计算过程。

例如，我们可能需要把一个数字序列按非递减顺序（nondecreasing order）排序。这个问题在实践中频繁出现，也为引入许多标准的设计技巧（design techniques）和分析工具（analysis tools）提供了丰富的素材。下面我们正式定义排序问题（sorting problem）：

**输入（Input）**：由 $n$ 个数字组成的序列 $\langle a_1, a_2, \ldots, a_n \rangle$。

**输出（Output）**：输入序列的一个排列（reordering）$\langle a'_1, a'_2, \ldots, a'_n \rangle$，使得 $a'_1 \le a'_2 \le \cdots \le a'_n$。

例如，给定输入序列 $\langle 31, 41, 59, 26, 41, 58 \rangle$，一个排序算法返回的输出序列为 $\langle 26, 31, 41, 41, 58, 59 \rangle$。这样的输入序列被称为排序问题的一个实例（instance）。一般而言，问题的实例由为计算该问题的一个解所需的输入构成（这些输入满足问题陈述中施加的一切约束）。

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.6</span>


### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

因为许多程序把它用作中间步骤，所以排序（sorting）是计算机科学（computer science）中的一种基本操作（fundamental operation）。因此，我们有大量优秀的排序算法可供使用。对给定的应用而言，哪个算法最好取决于——除其他因素外——待排序项（item）的数目、各项已部分有序的程度、对项值的可能限制、计算机的体系结构，以及所使用的存储设备类型：主存（main memory）、磁盘（disk）甚至磁带（tape）。

如果一个算法对每个输入实例都以正确的输出停机（halt），我们就说该算法是正确的（correct）。我们说一个正确的算法解决了给定的计算问题。一个不正确的算法可能在某些输入实例上根本不停止，也可能以错误的答案停止。与你可能预期的相反，如果能够控制错误率（error rate），不正确的算法有时也可能是有用的。在第 31 章研究寻找大素数的算法时，我们将看到一个错误率可控制的算法的例子。不过，通常我们只关心正确的算法。

算法可以用英语、计算机程序，甚至硬件设计（hardware design）来描述。唯一的要求是，这种描述必须对所遵循的计算过程给出精确的描述。

算法能解决哪些种类的问题？

排序绝不是人们为其开发过算法的唯一计算问题。（看到这本书的厚度，你大概也早已猜到了。）算法的实际应用无处不在，下面是一些例子：

- **人类基因组计划（Human Genome Project）**已在下列目标上取得巨大进展：识别人类 DNA 中全部 100,000 个基因，确定组成人类 DNA 的 30 亿个化学碱基对（base pairs）的序列，将这些信息存储在数据库中，并开发数据分析工具。其中每一步都需要复杂的算法。虽然这些问题的解法超出了本书的范围，但许多解决这些生物学问题的方法都借助了本书若干章节中的思想，从而使科学家能够在高效利用资源的同时完成任务。节省下来的既有人的时间也有机器的时间，还有金钱，因为从实验技术中可以提取出更多的信息。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 历史与算法的分工在这里最清楚：Human Genome Project（人类基因组计划）提供了问题规模，algorithm（算法）决定了这个问题在给定算力下是否可解。
>
> 先把史实钉住。该计划 1990 年正式启动，由美国 NIH 与 DOE 主导、多国实验室参与；2003 年 4 月宣布完成，比原定时间表提前两年，公开口径是覆盖了基因区约 99%。书中“100,000 个基因”是 1990 年代的流行估计；2004 年 10 月 International Human Genome Sequencing Consortium（国际人类基因组测序联盟）在 Nature 上把基因数下修到 20,000–25,000。这不是书错了，而是“输入规模”这个量本身在十年里被实验技术与 algorithm（算法）一起改写了两三倍。
>
> algorithm（算法）在其中做了三件事：fragment assembly（片段拼接）、gene finding（基因识别）、similarity search（相似性检索）。拼接的规模用一个乘法就能感受：常染色质约 $2.88\times10^{9}$ 个碱基对，测序深度 30 倍、每段读长 700 个碱基，读段条数约 $2.88\times10^{9}\times30/700\approx1.2\times10^{8}$，即一亿两千万条。任何两两比较的策略，配对数是 $(1.2\times10^{8})^{2}\approx1.4\times10^{16}$ 量级，就算每次比较只花一个时钟周期，也远超任何机器的寿命；实际系统靠 k-mer（长度为 k 的子串）索引把候选配对压到近似线性。
>
> longest common subsequence（最长公共子序列）在这里的位置值得单独算一遍：两条长度各 1000 的序列，各自有 $2^{1000}$ 个子序列，逐对枚举是 $2^{2000}$ 量级的配对；而 dynamic programming（动态规划）只填 $1000\times1000=10^{6}$ 个格子，每格常数工作。$10^{6}$ 与 $2^{2000}$ 之间的差距不是常数倍，也不是多项式倍，而是“能不能做完”的分界。
>
> 为什么 CLRS 第三版（2009 年）把它排在第一例：基因组数据在 2003 年之后进入爆炸期，它是当时少数“algorithm（算法）直接决定科学可行性”的公开案例，而不是实验室里的玩具。相比之下 shortest path（最短路径）这类例子在工业界早已成熟，缺的正是公众可见的规模感。
>
> 收束：硬件让测序变便宜，algorithm（算法）让数据变得可读。前者给的是常数倍，后者给的是可行性本身——这正是第 1 章把它放在第一位的理由。
>
> 再补一个规模感的对照：100,000 与 20,000 之间差五倍，而碱基对数是 $3\times10^{9}$ 量级——即便“基因”的计数变了五倍，底层的序列规模只由测序技术决定。这说明 computational problem（计算问题）的输入规模不随你对问题理解的深化而缩小，algorithm（算法）必须按最坏情况下的真实规模设计，而不是按某一版注释里的估计设计。
>
> 一个可复核的章节对照：CLRS 说这些问题的解法超出本书范围，但同时说许多方法借用了本书若干章节的思想。具体到章节：fragment assembly（片段拼接）用到第 15 章的 dynamic programming（动态规划）与第 32 章的 string matching（字符串匹配）；序列检索用到第 11 章的 hash table（散列表）；相似度度量落在第 15 章的 longest common subsequence（最长公共子序列）。一个基因组项目横跨本书三到四个部分，这就是“基础技术适用于问题领域”的字面含义。
>
> 最后提醒一句：书中写“100,000 个基因”时并没有错，它对应的是当时的共识。读旧教材时要习惯把“数字”和“问题结构”分开看——数字会更新，结构不会。
>
> 这类“数字随研究推进而变”的现象在算法书里很常见：input size（输入规模）的定义跟着对问题的理解走，而 complexity（复杂度）结论只依赖结构。所以被推翻的总是估计值，不是增长阶。

- **互联网（Internet）**使全世界的人们能够快速访问和检索大量信息。借助巧妙的算法，互联网上的站点得以管理和操纵如此庞大的数据量。基本离不开算法的典型问题包括：为数据寻找良好的传输路由（解决此类问题的技术出现在第 24 章），以及利用搜索引擎快速找到承载特定信息的页面（相关技术在第 11 章和第 32 章）。

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.7</span>


### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

- **电子商务（electronic commerce）**使商品和服务得以通过电子方式进行磋商与交换，它依赖于信用卡号、密码、银行对账单等个人信息的私密性。电子商务所采用的核心技术包括公钥密码学（public-key cryptography）和数字签名（digital signatures）（见第 31 章），它们建立在数值算法和数论（number theory）的基础之上。

- **制造业及其他商业企业**常常需要以最有利的方式来分配稀缺资源。石油公司可能想知道把油井布置在何处才能使其期望利润（expected profit）最大化；政治候选人可能想知道把钱花在哪里购买竞选广告，才能使赢得选举的机会最大化；航空公司可能想以尽可能低的成本为航班安排机组人员，同时确保每个航班都有人覆盖并符合政府对机组排班的法规；互联网服务提供商可能想知道在哪里部署额外资源，才能更有效地服务其客户。所有这些都是可以用线性规划（linear programming）解决的问题的例子，我们将在第 29 章中学习线性规划。

虽然这些例子中的某些细节超出了本书的范围，但我们确实给出了适用于这些问题及问题领域的基础技术。我们还将展示如何解决许多具体的问题，包括下面这些：

- 给定一张道路图，图上标出了每对相邻交叉路口之间的距离，我们希望确定从一个交叉路口到另一个交叉路口的最短路线。即使不允许路线自我交叉，可能的路线的数目也可能极其庞大。我们怎样才能在所有可能的路线中选出最短的那条？这里，我们把道路图（它本身就是对实际道路的一种建模）抽象为一个图（graph）（我们将在第六部分和附录 B 中遇到图），并希望在图中找到从一个顶点到另一个顶点的最短路径（shortest path）。我们将在第 24 章看到如何高效地解决这个问题。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 跨课程连接：把道路网抽象成 graph（图）$G=(V,E)$，这一步的信息损失正是建模的本质——留下“顶点 + 连接”，丢掉城市名与路面宽度。
>
> 6.042J 的图论部分已经给足了原材料：path（路径）、simple path（简单路径），以及 $n$ 个顶点的 graph（图）中 simple path（简单路径）长度至多 $n-1$。后者值得追问一句为什么：simple path（简单路径）不允许重复顶点，最多用尽 $n$ 个顶点，所以边数上界是 $n-1$。这条结构性质把“路径集合”从潜在的无限压成了有限——注意是有限，不是小。
>
> shortest path（最短路径）问的是带权版本：在所有从 $s$ 到 $t$ 的路径中，让边权之和最小。暴力枚举行不通，因为路线数随顶点数呈组合爆炸。算两个数：$10\times10$ 的网格路网，从左上角到右下角若只许向右、向上走，路线数是 $\binom{18}{9}=48620$，还能硬算；把网格放大到 $20\times20$，路线数变成 $\binom{38}{19}\approx3.5\times10^{10}$，按每秒一亿次枚举要三百多秒，而真实路网还允许绕行，简单路径数还要再乘上组合因子，很快超出任何算力。
>
> 第 24 章的 Dijkstra algorithm（迪杰斯特拉算法）为什么能绕过枚举：它不枚举路径，而是按“离源点由近到远”的次序一次性确定每个顶点，每条边只松弛常数次。稠密表示是 $O(V^{2})$；配上 binary heap（二叉堆）是 $O((V+E)\log V)$。还是那个网格：$V=100$、$E\approx180$，堆操作量约 $2.8\times10^{2}\times6.6\approx2\times10^{3}$ 次，与 48620 条路线相差一个数量级以上；网格放大到 $20\times20$ 时，$V=400$、$E\approx760$，堆操作约 $7\times10^{3}$ 次，而路线数是 $3.5\times10^{10}$——量级差别从十倍变成七位数。
>
> 类比成立之处：两者讨论的是同一对象——带权 graph（图）中的路径。区别在于 6.042J 关心路径的存在性与结构（有没有、有多长、能不能覆盖所有边），shortest path（最短路径）关心的是在全体路径上最优化一个可加的量。
>
> 顺着这个区分看习题 1.1-4 就清楚了：shortest path（最短路径）与 traveling-salesman problem（旅行商问题）问的是“同对象、不同目标”。前者要从 $s$ 到 $t$，去掉末段后剩下的仍是从 $s$ 到中间点的 shortest path（最短路径），optimal substructure（最优子结构）成立；后者要求一条经过所有顶点恰好一次并回到起点的回路，去掉一段之后起点与“已访问集合”都变了，剩下的不是同类型子问题，于是只好去证 NP-complete（NP 完全）。
>
> 带这个区分去读第六部分，你会发现 Dijkstra algorithm（迪杰斯特拉算法）的正确性论证之所以干净，全靠“边权非负”这一个结构假设：它把“已确定集合”与“未确定集合”之间的边界钉死，让贪心选择不再需要回看。
>
> 补一个“非负边权为什么是硬条件”的可算反例。三点：$s\to a$ 权 2，$s\to b$ 权 3，$b\to a$ 权 $-2$。Dijkstra algorithm（迪杰斯特拉算法）第一轮会先确定 $a$（距离 2），但真实最短路是 $s\to b\to a$，长度 1。非负假设一破，“已确定集合”就不再封闭，贪心选择的正确性论证整条断掉。
>
> 与这组数字对应的工程量级：$V=400$ 的网格上，$O(V^{2})$ 是 $1.6\times10^{5}$ 次操作，$O((V+E)\log V)$ 约 $7\times10^{3}$ 次，差二十倍——说明“同一个 algorithm（算法）、不同的 data structure（数据结构）”本身就是一个常数级战场，而 CSAPP 第 6 章的 cache（缓存）局部性决定这两者谁真正跑得快。

- 给定两个有序符号序列 $X = \langle x_1, x_2, \ldots, x_m \rangle$ 和 $Y = \langle y_1, y_2, \ldots, y_n \rangle$，我们希望找出 $X$ 和 $Y$ 的一个最长公共子序列（longest common subsequence）。$X$ 的子序列就是把 $X$ 中的某些元素（也可能是全部或没有）删去后所得的结果。例如，$\langle A, B, C, D, E, F, G \rangle$ 的一个子序列可以是 $\langle B, C, E, G \rangle$。$X$ 和 $Y$ 的最长公共子序列的长度给出了这两个序列相似程度的一种度量。例如，如果这两个序列是 DNA 链上的碱基对，那么当它们有一个很长的公共子序列时，我们就可以认为它们是相似的。如果 $X$ 有 $m$ 个符号而 $Y$ 有 $n$ 个符号，那么 $X$ 和 $Y$ 分别有 $2^m$ 和 $2^n$ 个可能的子序列；除非 $m$ 和 $n$ 都非常小，否则选出 $X$ 和 $Y$ 的所有可能子序列并逐一匹配，可能要耗费长得无法接受的时间。我们将在第 15 章看到，如何用一种称为动态规划（dynamic programming）的通用技术来高效地解决这个问题。

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.8</span>


### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

> <span style="color:#7f8c8d;">**[note]** 本页开头的 longest common subsequence（最长公共子序列）示例收尾两句（"respectively. Selecting all possible subsequences…"）已并入第 7 页对应段落，此处直接接续下一示例。</span>

- 给定一个用零件库表示的机械设计，其中每个零件可能包含其他零件的实例，我们需要按顺序列出这些零件，使得每个零件都出现在使用它的任何零件之前。如果设计包含 $n$ 个零件，那么可能有 $n!$ 种顺序，其中 $n!$ 表示阶乘函数（factorial function）。由于阶乘函数的增长速度甚至比指数函数还快，我们不可能（除非零件很少）逐一生成每种可能的顺序，再验证在该顺序中每个零件是否出现在使用它的零件之前。这个问题是拓扑排序（topological sorting）的一个实例，我们将在第 22 章看到如何高效地解决它。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 跨课程连接：这个“零件必须排在使用它的零件之前”的约束，就是 6.042J 里 partial order（偏序）的工程化身；topological sorting（拓扑排序）要做的，是给它一个 linear extension（线性扩张）。
>
> 先把结构说清。“零件 $A$ 必须先于零件 $B$”定义了零件集合上的一个二元关系。它满足 partial order（偏序）的几条要求：reflexive（自反）这一条在工程里通常弱化成严格序（自己不必先于自己）；antisymmetric（反对称）禁止“$A$ 先于 $B$”与“$B$ 先于 $A$”同时成立；transitive（传递）保证链条闭合——$A$ 先于 $B$、$B$ 先于 $C$，则 $A$ 必须先于 $C$，否则约束体系自相矛盾。
>
> 6.042J 里你画过 Hasse diagram（哈斯图）：只画 cover relation（覆盖关系），去掉由自反与传递必然推出的边。Hasse diagram（哈斯图）是 partial order（偏序）的可视化；topological sorting（拓扑排序）是对同一个 partial order（偏序）做线性化。
>
> 算一下候选规模，别只信“$n!$ 很大”这句话。4 个零件，约束只有 $A$ 先于 $C$ 与 $B$ 先于 $C$，则 $4!=24$ 个排列里合法的有 8 个；再加一条 $D$ 先于 $A$，合法数掉到 3 个。也就是说，“$n!$ 个候选里合法的那些恰好是全部 linear extension（线性扩张）”不是修辞：$n=4$ 时是 24 里挑 3；$n=10$ 时 $10!=3628800$，逐排列检查的代价随 $n$ 阶乘式爆炸，而真正的检查算法只要 $O(V+E)$。
>
> 共同的结构不变量是 acyclicity（无环性）。一旦出现循环依赖（$A$ 依赖 $B$、$B$ 又依赖 $A$），antisymmetry（反对称性）被破坏，linear extension（线性扩张）根本不存在。用 graph（图）的语言说，partial order（偏序）的 cover relation（覆盖关系）图必须是 DAG（有向无环图）。第 22 章的算法每轮取一个入度为 0 的顶点剥离；若某一轮一个也取不出来，就说明剩下的子图有环——algorithm（算法）的失败模式，直接对应数学上的不存在性，这是本注最值得记住的一处对应。
>
> 区别也要说清：Hasse diagram（哈斯图）不区分同一层元素之间的次序，topological sorting（拓扑排序）必须给出一条具体序列；而且同一个 partial order（偏序）通常有多个 linear extension（线性扩张），所以“拓扑序”永远不是唯一答案。这一点在工程上很实用：它说明合法的构建顺序是一族而不是一个，你可以在这族里按其他目标（例如并行度、缓存局部性）再挑。
>
> 收束：第 22 章那个 $O(V+E)$ 的算法，本质是把 partial order（偏序）按 cover relation（覆盖关系）做一次逐层剥离；它和 $n!$ 枚举之间不是快慢之差，而是“可算”与“不可算”之差。
>
> 把“$n!$ 里合法的那些”再推一步：数出 linear extension（线性扩张）的总数是计数问题，属于 #P 完全那一类；而“存在性 + 构造一个”只要 $O(V+E)$。判定与构造可以很容易，计数很难——同一族结构上，三种问法能差出好几个量级，这一点在组合数学里反复出现。
>
> 工程侧的推论：既然合法序不唯一，build system（构建系统，例如 make 与包管理器）通常只保证“存在一条被选中的 linear extension（线性扩张）”，不保证它最短。想要更短的构建时间，就得在 partial order（偏序）之外再引入代价模型，那已经变成 scheduling（调度）问题；而 scheduling（调度）一旦带上资源约束，常常掉进 NP-complete（NP 完全）那一类。

- 给定平面上的 $n$ 个点，我们希望找出这些点的凸包（convex hull）。凸包是包含这些点的最小的凸多边形（convex polygon）。直观上，我们可以把每个点想象成钉在木板上的一个钉子，凸包则由一根紧紧环绕所有这些钉子的橡皮筋来表示。橡皮筋在其上转弯的每个钉子都是凸包的一个顶点。（例子见图 33.6，第 1029 页。）这 $n$ 个点的 $2^n$ 个子集中的任何一个都有可能成为凸包的顶点集。即使知道哪些点是凸包的顶点也还不够，因为我们还需要知道它们出现的顺序。因此，凸包的顶点有非常多的可能选择。第 33 章给出了寻找凸包的两种好方法。

上面这些清单远非详尽（看到这本书的分量，你大概也又猜到了），但它们表现出许多有趣的算法问题所共有的两个特征：

1. 它们有大量的候选解（candidate solutions），其中绝大多数都不能解决手头的问题。要找出一个能解决问题的解，或者一个"最佳"的解，可能相当具有挑战性。

2. 它们都有实际应用。在上述问题中，寻找最短路径提供了最简单的例子。一家运输公司——例如卡车运输公司或铁路公司——在穿越公路或铁路网络的最短路径寻找上有直接的经济利益，因为走更短的路意味着更低的人力和燃料成本。互联网上的一个路由节点也可能需要找到穿过网络的最短路径，以便快速转发一条消息。又如，一个想开车从纽约去波士顿的人，可能希望从一个合适的网站上获取驾驶路线，也可能在开车时使用自己的 GPS。

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.9</span>


### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

并非每个由算法解决的问题都有一组容易识别的候选解。例如，假设给定一组表示信号采样（samples of a signal）的数值，我们希望计算这些采样的离散傅里叶变换（discrete Fourier transform）。离散傅里叶变换把时域（time domain）转换到频域（frequency domain），产生一组数值系数，从而我们可以确定被采样信号中各个频率的强度。离散傅里叶变换除了处于信号处理（signal processing）的核心位置之外，还在数据压缩以及大多项式和大整数相乘方面有应用。第 30 章针对该问题给出了一个高效算法——快速傅里叶变换（fast Fourier transform，通常简称 FFT），该章还勾勒了一个用于计算 FFT 的硬件电路的设计。

#### Data Structures（数据结构） <span style="color:#2471a3;">**[section]**</span>

本书还包含若干数据结构（data structure）。数据结构是一种存储和组织数据的方式，以便于对数据的访问和修改。没有任何单一的数据结构能对所有用途都表现良好，因此了解其中若干种数据结构的优点和局限是很重要的。

#### Technique（技术） <span style="color:#2471a3;">**[section]**</span>

虽然你可以把这本书当作算法的"菜谱"（cookbook）来用，但说不定某天你会遇到一个无法轻易找到现成已发表算法的问题（例如本书中的许多习题和问题）。本书将教你算法设计与分析的技术，使你能自己开发算法、证明它们给出正确的答案，并理解它们的效率。不同的章节处理算法问题求解的不同方面。有些章节处理具体问题，例如第 9 章寻找中位数和顺序统计量（order statistics）、第 23 章计算最小生成树（minimum spanning tree）、第 26 章确定网络中的最大流（maximum flow）。另一些章节处理技术，例如第 4 章的分治法（divide-and-conquer）、第 15 章的动态规划（dynamic programming）和第 17 章的摊还分析（amortized analysis）。

#### Hard Problems（难题） <span style="color:#2471a3;">**[section]**</span>

本书的大部分内容是关于高效算法的。我们衡量效率的通常标准是速度，即算法产生结果需要多长时间。然而，有些问题目前还不知道有高效的解法。第 34 章研究这些问题的有趣子集，它们被称为 NP 完全（NP-complete）问题。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 拓展注：要把“没人找到多项式算法、也没人证明它不存在”这句读准，需要 P（多项式时间可解）与 NP（多项式时间可验证）这个框架。
>
> 两个类的差别只有一个词：解与验证。给一张填好的数独，验证合法性只要扫一遍棋盘，$9\times9$ 个格子每格常数检查，总共约 729 次比较；面对空盘找一个填法，合法终盘总数约 $6.7\times10^{21}$ 个，靠回溯搜索在最坏情况下要在这片空间里走很远。这就是“验证容易、求解未必容易”的最小可视化例子。
>
> 严格一点的定义：P 是所有存在 polynomial-time（多项式时间）deterministic（确定性）algorithm（算法）的判定问题；NP 是所有“给定候选解后能在 polynomial-time（多项式时间）内验证”的判定问题。NP-complete（NP 完全）的含义更强：它们属于 NP，而且任何 NP 问题都能在 polynomial-time（多项式时间）内 reduction（归约）到它们。于是“一荣俱荣”：其中任何一个有了 polynomial-time（多项式时间）algorithm（算法），全体 NP 问题就都有了。
>
> 史实部分（已查一手线索）：NP 完全性的概念由 Stephen Cook 在 1971 年明确定义，并证明 propositional satisfiability（命题可满足性）是 NP-complete（NP 完全）的；Richard Karp 在 1972 年把这套方法扩展到一批组合问题；2000 年 Clay Mathematics Institute（克雷数学研究所）把“P 是否等于 NP”列入七个 Millennium Prize Problems（千禧年大奖难题），悬赏一百万美元。至今未决。
>
> 一个可复算的规模感来自习题 1.2-3：最小的 $n$ 使 $100n^{2}$ 快于 $2^{n}$。代入：$n=14$ 时 $100n^{2}=19600$ 大于 $2^{14}=16384$；$n=15$ 时 $22500$ 小于 $32768$。所以指数 algorithm（算法）在极小规模上并不吃亏，痛点全在规模增长之后：$n=50$ 时 $2^{50}\approx1.1\times10^{15}$，按每秒 $10^{9}$ 次运算要 $1.1\times10^{6}$ 秒，约 13 天。
>
> traveling-salesman problem（旅行商问题）是这条界线的样板：$n$ 个城市的巡回路线有 $(n-1)!/2$ 条，$n=15$ 时约 $4.4\times10^{10}$，$n=20$ 时约 $6.1\times10^{16}$。第 35 章的 approximation algorithm（近似算法）不争最优，而是保证“解不超过最优值的某个固定倍数”——把不可算，换成可算加可证的误差。
>
> 三条出路怎么选：问题有可证明的近似比，走 approximation algorithm（近似算法）；输入分布已知或可采样，走 heuristic（启发式）与 randomization（随机化）；真实输入带额外结构（城市都沿一条公路），就挖结构把问题拉回可算区。识别出它是 NP-complete（NP 完全）本身就是成果——它替你省下的是几个月，而不是几个常数。
>
> 收束：这一段的价值不在“难题很难”，而在于它给了一个二分类器。把问题分成“结构上可算”与“结构上大概不可算”，你的设计精力应当按这个分类分配，而不是按题目是否眼熟分配。
>
> 把 P 与 NP 的关系再说死一点：P 含于 NP 是显然的——能解当然能验证，解出来直接比就行。是否真包含，是全部难点所在。若 P 等于 NP，则“找一个证明”与“验证一个证明”一样容易，公钥密码学的安全性基础会被整体改写；这也是这个问题对工程界而不只对数学界重要的原因。
>
> reduction（归约）的方向最容易记反。标准记法是从难归到易：把已知难问题 X 的每个实例在 polynomial-time（多项式时间）内改写成 Y 的一个实例，于是“Y 有解则 X 有解”。所以只要 Y 拿到 polynomial-time（多项式时间）algorithm（算法），X 也就有了；反过来不成立。把方向记成“难→易”，整套论证的方向就不会翻。

为什么 NP 完全问题有趣？首先，虽然人们从未找到过任何一个 NP 完全问题的高效算法，但也从未有人证明过……

> <span style="color:#7f8c8d;">*（本节未完，续见第 10 页）*</span>

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.10</span>


### Section 1.1（Algorithms，算法）<span style="color:#2471a3;">**[section]**</span>（续上页）

……即某个问题的高效算法不可能存在。换言之，没有人知道 NP-complete（NP 完全）问题是否存在高效的算法。

其次，NP-complete 问题集合具有一个显著性质：如果其中任何一个问题存在高效算法，那么所有这些问题都存在高效算法。NP-complete 问题之间的这种相互关联，使得高效解的缺失更显耐人寻味。

第三，若干 NP-complete 问题与一些我们已经知道高效算法的问题相似、但并不相同。计算机科学家们对这样一个事实深感兴趣：对问题描述的一点点改动，竟能引发已知最优算法效率的巨大变化。

你应该了解 NP-complete 问题，因为其中一些问题在实际应用中出现的频率高得惊人。如果有人让你为一个 NP-complete 问题设计高效算法，你很可能会在徒劳的搜索上耗费大量时间。但如果你能证明该问题是 NP-complete 的，就可以把时间转而用来开发能给出很好（但并非最优）解的算法。

举一个具体的例子：考虑一家设有 central depot（中心仓库）的快递公司。每天，它都在仓库为每辆送货卡车装货，然后派车前往多个地址送货。一天结束时，每辆卡车都必须回到仓库，以便为第二天装货做好准备。为了降低成本，公司希望选择一种送货停靠点的顺序，使每辆卡车行驶的总距离最短。这个问题就是著名的 traveling-salesman problem（旅行商问题），它是 NP-complete 的，目前没有已知的高效算法。不过，在某些假设下，我们确实知道一些能给出总距离的高效算法，其总距离并不会比最小可能值高出太多。第 35 章将讨论这类 approximation algorithms（近似算法）。

#### Parallelism（并行性） <span style="color:#2471a3;">**[section]**</span>

多年来，我们可以指望处理器时钟速度以稳定的速率持续提升。然而，物理限制为不断攀升的时钟速度设置了一道根本性的路障：由于 power density（功率密度）随时钟速度超线性（superlinearly）增长，一旦时钟速度足够高，芯片就有熔化的风险。因此，为了每秒执行更多的计算，芯片被设计为不只包含一个、而是包含多个处理 core（核）。我们可以把这些 multicore（多核）计算机比作单块芯片上的多台 sequential（串行）计算机；换句话说，它们是一种 parallel computer（并行计算机）。为了从多核计算机中获得最佳性能，我们需要在设计算法时就考虑并行性。第 27 章将介绍 multithreaded（多线程）算法的模型，这类算法充分利用多个核。该模型从理论角度看具有优势，并且构成了若干成功计算机程序的基础，其中包括一个国际象棋冠军程序。

---

> <span style="color:#7f8c8d;">CLRS §1.1–1.2, p.11</span>


### Exercises <span style="color:#2471a3;">**[exercise]**</span>

**1.1-1**
Give a real-world example that requires sorting or a real-world example that requires computing a convex hull.

**1.1-2**
Other than speed, what other measures of efficiency might one use in a real-world setting?

**1.1-3**
Select a data structure that you have seen previously, and discuss its strengths and limitations.

**1.1-4**
How are the shortest-path and traveling-salesman problems given above similar? How are they different?

**1.1-5**
Come up with a real-world problem in which only the best solution will do. Then come up with one in which a solution that is "approximately" the best is good enough.

### Section 1.2（Algorithms as a technology，算法作为技术）<span style="color:#2471a3;">**[section]**</span>

假设计算机无限快，computer memory（计算机内存）完全免费，你还有理由学习算法吗？答案是肯定的，哪怕仅仅因为你仍然希望证明：你的求解方法能够终止（terminate），并且能以正确的答案终止。

如果计算机无限快，那么任何求解问题的正确方法都行得通。你或许希望自己的实现符合良好的软件工程实践（例如，实现应当设计良好并有充分的文档），但大多数时候你会选择最容易实现的方法。

当然，计算机可能很快，但并非无限快；内存可能很便宜，但并非免费。因此，计算时间是一种 bounded resource（有界资源），内存空间同样如此。你应该明智地使用这些资源，而时间或空间上高效的算法将帮助你做到这一点。

---

> <span style="color:#7f8c8d;">CLRS §1.2, p.12</span>


### Section 1.2（Algorithms as a technology，算法作为技术）<span style="color:#2471a3;">**[section]**</span>

#### Efficiency（效率） <span style="color:#2471a3;">**[section]**</span>

为解决同一问题而设计的不同算法，其效率往往有天壤之别。这些差异可能比硬件和软件造成的差异重要得多。

例如，在第 2 章中我们将看到两种 sorting（排序）算法。第一种是 insertion sort（插入排序），对 $n$ 个项排序所需时间约为 $c_1 n^2$，其中 $c_1$ 是一个不依赖于 $n$ 的常数；也就是说，它的时间大致正比于 $n^2$。第二种是 merge sort（归并排序），所需时间约为 $c_2 n \lg n$，其中 $\lg n$ 表示 $\log_2 n$，$c_2$ 是另一个同样不依赖于 $n$ 的常数。insertion sort 的 constant factor（常数因子）通常比 merge sort 小，因此 $c_1 < c_2$。

我们将会看到，常数因子对 running time（运行时间）的影响远小于对 input size（输入规模）$n$ 的依赖。我们把 insertion sort 的运行时间写成 $c_1 n \cdot n$，把 merge sort 的运行时间写成 $c_2 n \cdot \lg n$。于是可以看出，insertion sort 的运行时间中有一个因子 $n$，而 merge sort 相应位置是 $\lg n$，后者要小得多。（例如，当 $n = 1000$ 时，$\lg n$ 约为 10；当 $n$ 等于一百万时，$\lg n$ 大约也只有 20。）虽然对于较小的输入规模，insertion sort 通常比 merge sort 运行得更快，但一旦输入规模 $n$ 足够大，merge sort 用 $\lg n$ 对抗 $n$ 的优势将足以弥补常数因子上的差异。无论 $c_1$ 比 $c_2$ 小多少，总存在一个 crossover point（交叉点），超过该点之后 merge sort 会更快。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第一性原理：为什么区区 constant factor（常数因子）会被 growth rate（增长率）吞没？答案藏在一个单调无界的函数里。
>
> 先把方程写开：令交叉点处 $c_1 n^{2}=c_2 n\lg n$，两边除以 $n$ 得 $c_1 n=c_2\lg n$，再除以 $c_1\lg n$ 得 $n/\lg n=c_2/c_1$。于是“交叉点存在”这件事，等价于“函数 $n/\lg n$ 无上界”。它确实单调递增且无界：$n=10^{3}$ 时约 100，$n=10^{6}$ 时约 $5.0\times10^{4}$，$n=10^{9}$ 时约 $3.3\times10^{7}$。
>
> 反解一次最有说服力：设 $c_1$ 比 $c_2$ 小一千倍，即 $c_2/c_1=1000$，解 $n/\lg n=1000$ 得 $n\approx13747$。也就是说，哪怕 insertion sort（插入排序）的单步代价只有 merge sort（归并排序）的千分之一，从第 13748 个元素起 merge sort（归并排序）就开始赢。这个数是解方程得到的，不是估的。
>
> 为什么 constant factor（常数因子）只能挪动交叉点的位置、不能改变结论：$c_1$ 与 $c_2$ 是固定的一次效应，而交叉点 $n^{*}$ 随比值 $c_2/c_1$ 增长得极慢（近似对数级），$n$ 却可以任意大。对任何固定的比值，总有一个 $n$ 超过 $n^{*}$。asymptotic（渐近）论证的力量就在这里：它不告诉你“多大算大”，只告诉你“一定存在那么大”。
>
> CSAPP 第 5 章的程序优化（消除循环低效、减少过程调用、提高 cache（缓存）局部性）确实能把 constant factor（常数因子）压低几倍到几十倍，这是真实的、值得做的工程。但它改变的是“每一步的代价”，改变不了“步数随 $n$ 增长的方式”。$c$ 的回报有界，增长率之差不有界。
>
> 分工因此很清楚：performance tuning（性能调优）决定 $c$，algorithm design（算法设计）决定 growth rate（增长率）。前者的上限是硬件与编译器的物理极限，后者没有上限。工程判断很具体：数据规模还会涨时，先换 algorithm（算法），再谈调优。
>
> 一个诚实的反面提醒：若你的输入永远停在 $n=10^{3}$，交叉点可能永远不来，此时 constant factor（常数因子）才是胜负手——这正是 Problem 2-1 用 insertion sort（插入排序）处理小子数组、把 merge sort（归并排序）递归的叶子加粗的现实依据。
>
> 收束：$c_1<c_2$ 这个不等式在代数上毫无分量，它只是两边的一个系数；把它放进 $n\to\infty$ 的极限里，它连“决定胜负”的资格都没有。真正决定胜负的是 $n$ 与 $\lg n$ 谁在指数位置上。
>
> 顺手把 $\lg$ 的含义固定住：本书的 $\lg n$ 指 $\log_{2} n$，于是 $\lg 10^{6}\approx19.93$、$\lg 10^{7}\approx23.25$。换底只差一个常数因子 $1/\log_{2}e\approx1.4427$，而 $\Theta$ 记号本就把常数因子吸收掉，所以底数取 2、取 10 还是取 $e$，增长阶的结论都一样——这也解释了为什么第 3 章可以只写 $\Theta(\log n)$ 而不写底数。
>
> 再给一个“constant factor（常数因子）到底能差多少”的现实刻度：同一段数组求和，编译器 -O2 与 -O0 之间常差两三倍；把顺序访问换成跨步访问，cache（缓存）未命中率上升，常再差五到十倍；换语言（解释器与编译型之间）还能再差几十倍。这些叠起来最多把 $c$ 拉开两个数量级。
>
> 而 $n/\lg n$ 从 $n=10^{3}$ 到 $n=10^{9}$ 拉开了五个数量级：前者的乘积有界，后者无界。所以读这类论证时先别问“哪个更快”，要问“在什么规模区间内更快”——前一个问题需要常数，后一个问题只需要增长率与交叉点位置。
>
> 一句话记住这个分工：交叉点的位置由常数的比值决定，交叉点之后的胜负由增长阶决定。前者可以靠工程改进挪动，后者只能靠换算法改变。

举一个具体的例子，我们让一台较快的计算机（计算机 A）运行 insertion sort，与一台较慢的计算机（计算机 B）运行 merge sort 一较高下。它们各自都要对由 1000 万个数字组成的数组（array）排序。（虽然 1000 万个数字看起来很多，但如果这些数字是 8 字节整数，那么输入约占 80 兆字节，即使一台廉价笔记本电脑的内存也能容纳很多遍。）假设计算机 A 每秒执行 100 亿条指令（比本书写作时的任何单台串行计算机都快），而计算机 B 每秒只执行 1000 万条指令，因此计算机 A 在原始计算能力上比计算机 B 快 1000 倍。为了让差异更加戏剧化，假设世界上最巧妙的程序员用机器语言为计算机 A 编写 insertion sort，结果代码对 $n$ 个数字排序需要 $2n^2$ 条指令。再假设只是一位普通程序员用高级语言和效率低下的编译器实现 merge sort，结果代码需要 $50 n \lg n$ 条指令。要对 1000 万个数字排序，计算机 A 需要

```math
\frac{2 \cdot (10^7)^2\ \text{instructions}}{10^{10}\ \text{instructions/second}} = 20{,}000\ \text{seconds}（超过 5.5 小时），
```

而计算机 B 需要

---

> <span style="color:#7f8c8d;">CLRS §1.2, p.13</span>


### Section 1.2（Algorithms as a technology，算法作为技术）<span style="color:#2471a3;">**[section]**</span>

（接上页）计算机 B 需要

```math
\frac{50 \cdot 10^7 \lg 10^7\ \text{instructions}}{10^7\ \text{instructions/second}} \approx 1163\ \text{seconds}（不到 20 分钟）。
```

凭借一个 running time（运行时间）增长得更慢的算法，即使编译器很差，计算机 B 的运行速度也比计算机 A 快 17 倍以上！当我们对 1 亿个数字排序时，merge sort 的优势更加明显：insertion sort 需要 23 天以上，而 merge sort 不到 4 小时。一般来说，随着 problem size（问题规模）增大，merge sort 的相对优势也在增大。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 跨课程连接：计算机 A/B 这组数字的本质，是 asymptotic improvement（渐近改进）可以碾压硬件一千倍的劣势。
>
> 先复算两个数。A 需要 $2\cdot(10^{7})^{2}/10^{10}=2\times10^{4}$ 秒，约 5.6 小时；B 需要 $50\cdot10^{7}\cdot\lg10^{7}/10^{7}=50\times23.253\approx1163$ 秒，约 19.4 分钟。运行时间之比是 $20000/1163\approx17.2$。
>
> 但真正干净的那个数是指令数之比，它不含硬件差异：$\frac{2n^{2}}{50n\lg n}=\frac{n}{25\lg n}$，代入 $n=10^{7}$ 得 $\frac{10^{7}}{25\times23.253}\approx1.72\times10^{4}$。两个数必须分清——指令数之比 $1.7\times10^{4}$ 是纯 algorithm（算法）效应，运行时间之比 17.2 是把这个效应除以了一千倍硬件优势。
>
> CSAPP 的机制恰好解释为什么硬件优势只能给常数级：pipeline（流水线）让多条指令重叠执行、cache（缓存）命中把访存从几十个周期压到几个周期、superscalar（超标量）每周期多发射几条。这些机制全都在压缩 constant factor（常数因子）的取值范围，压不到 $n^{2}$ 与 $n\lg n$ 的结构差别上。
>
> 再放大一档验证同一个规律：$n=10^{8}$ 时指令数之比为 $10^{8}/(25\times26.575)\approx1.5\times10^{5}$，比上一档又大了近十倍。书里说这时 A 需要 23 天以上、B 不到 4 小时，与这个比例一致——规模每乘十，优势就再乘一个接近十的因子。
>
> 工程结论：换硬件给出的是有上界的常数倍回报，换 algorithm（算法）给出的是随 $n$ 无界增长的回报。所以“等机器变快”永远替代不了“换更好的 algorithm（算法）”，两者的函数形式不同，不是同一类投入。
>
> 一个诚实的边界：这条结论依赖“规模真的会变大”。若输入永远停在 $n=10^{3}$ 量级，constant factor（常数因子，包括语言、编译器、cache（缓存）行为）才是胜负手，此时把 merge sort（归并排序）换成 insertion sort（插入排序）反而更快，这也是 Problem 2-1 的出发点。
>
> 收束：硬件买的是系数，algorithm（算法）买的是指数。系数可以买很多次，指数只能靠想出来——这是第 1 章把 algorithm（算法）称为 technology（技术）的确切含义。
>
> 把这组数字换个方向读：要让 A 追上 B，需要把硬件再快 17 倍；要让 B 追上 A，只需换一个增长阶更低的 algorithm（算法）。两种改法的成本完全不对称——前者受制于工艺与功耗墙，后者是一次性的智力投入。
>
> 再把手算过程摊开，避免量级说糊：$\lg10^{7}=7\log_{2}10\approx23.25$，所以 $50n\lg n$ 在 $n=10^{7}$ 时是 $50\times10^{7}\times23.25\approx1.16\times10^{10}$ 条指令，除以每秒 $10^{7}$ 条得 1163 秒；而 $2n^{2}$ 是 $2\times10^{14}$ 条指令，除以每秒 $10^{10}$ 条得 $2\times10^{4}$ 秒。指令数差 $1.7\times10^{4}$ 倍，时间只差 17 倍，账就是这么平的。
>
> 这条算术还解释了一个常见误判：看到“A 每秒一百亿条、B 每秒一千万条”就认定 A 必胜，那是只比了硬件参数。运行时间是指令数除以速率，两个因子一起决定胜负；要比就得比最终的商，不能只比其中一个因子。
>
> 最后落到可操作的判断上：做性能决策前先估 $n$ 的未来取值。若 $n$ 还会涨两个数量级，增长率就是唯一该优化的量；若 $n$ 已经封顶，才轮到 constant factor（常数因子）与 cache（缓存）行为说话。
>
> 顺手把书里那两个时间换算核一遍：$2\times10^{4}$ 秒除以 3600 是 5.56 小时，所以写“超过 5.5 小时”；1163 秒除以 60 是 19.4 分钟，所以写“不到 20 分钟”。$10^{8}$ 那一档同理：$2\times10^{16}/10^{10}=2\times10^{6}$ 秒约 23.1 天，$50\times10^{8}\times26.575/10^{7}\approx1.33\times10^{4}$ 秒约 3.7 小时。

#### Algorithms and other technologies（算法与其他技术） <span style="color:#2471a3;">**[section]**</span>

上面的例子表明，我们应该像看待计算机硬件一样，把算法视为一种 technology（技术）。系统的整体性能既取决于选择高效的算法，也取决于选择快速的硬件。正如其他计算机技术正在飞速发展，算法领域也在飞速发展。

鉴于还有其他先进技术，你可能会怀疑算法在当代计算机上是否真的如此重要，这些技术包括：

- advanced computer architectures and fabrication technologies（先进的计算机体系结构与制造技术），
- easy-to-use, intuitive, graphical user interfaces (GUIs)（易用、直观的图形用户界面（GUIs）），
- object-oriented systems（面向对象系统），
- integrated Web technologies（集成化的 Web 技术），以及
- fast networking, both wired and wireless（有线和无线的高速网络）。

答案是肯定的。虽然有些应用在 application level（应用层）并不显式需要算法内容（例如某些简单的 Web 应用），但很多应用需要。例如，考虑一种基于 Web 的服务，它负责确定如何从一地旅行到另一地。其实现将依赖快速硬件、图形用户界面、广域网（wide-area networking），或许还会用到面向对象技术。但它同样需要针对某些操作的算法，例如寻找路线（很可能使用 shortest-path（最短路径）算法）、渲染（rendering）地图，以及 interpolating（插值）地址。

此外，即使一个应用在应用层不需要算法内容，它也严重依赖算法。该应用依赖快速硬件吗？硬件的设计就用到了算法。该应用依赖图形用户界面吗？任何 GUI 的设计都依赖算法。该应用依赖网络吗？网络中的 routing（路由）就严重依赖算法。该应用是用机器码（machine code）之外的语言编写的吗？那么它必然经过 compiler（编译器）、interpreter（解释器）或 assembler（汇编器）的处理，而这三者都大量使用算法。

---

> <span style="color:#7f8c8d;">CLRS §1.2, p.14</span>


### Section 1.2（Algorithms as a technology，算法作为技术）<span style="color:#2471a3;">**[section]**</span>

（接上页）算法是当代计算机所用大多数技术的核心。此外，随着计算机能力的不断提升，我们用它解决比以往任何时候都更大的问题。正如我们在上面 insertion sort 与 merge sort 的对比中看到的，正是面对较大的问题规模时，算法之间的效率差异才变得尤为突出。

拥有扎实的算法知识与技术基础，是把真正熟练的程序员与新手区分开来的一个特征。借助现代计算技术，你可以在不太了解算法的情况下完成某些任务；但有了良好的算法背景，你能做的事情会多得多，多得多。

### Exercises <span style="color:#2471a3;">**[exercise]**</span>

**1.2-1**
Give an example of an application that requires algorithmic content at the application level, and discuss the function of the algorithms involved.

**1.2-2**
Suppose we are comparing implementations of insertion sort and merge sort on the same machine. For inputs of size $n$, insertion sort runs in $8n^2$ steps, while merge sort runs in $64n \lg n$ steps. For which values of $n$ does insertion sort beat merge sort?

**1.2-3**
What is the smallest value of $n$ such that an algorithm whose running time is $100n^2$ runs faster than an algorithm whose running time is $2^n$ on the same machine?

### Problems <span style="color:#2471a3;">**[problem]**</span>

**1-1** Comparison of running times（运行时间的比较）

For each function $f(n)$ and time $t$ in the following table, determine the largest size $n$ of a problem that can be solved in time $t$, assuming that the algorithm to solve the problem takes $f(n)$ microseconds.

---

> <span style="color:#7f8c8d;">CLRS §1.2, p.15 (Notes & Problems)</span>


### Problems <span style="color:#2471a3;">**[problem]**</span>（续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 以下为译者根据原文 Problem 1-1 补全的数值表（原文表格各格留空，要求读者自填），每格给出单位时间内可解的最大 n。
>
> 先把题目读准：给定运行时间函数 $f(n)$，且 $f(n)$ 以 microsecond（微秒）为单位，问在时间 $t$ 内能解出的最大问题规模 $n$。换算基准为：1 秒 $=10^{6}$ 微秒，1 分钟 $=6\times10^{7}$，1 小时 $=3.6\times10^{9}$，1 天 $=8.64\times10^{10}$，1 个月按 30 天取 $2.592\times10^{12}$，1 年按 365 天取 $3.1536\times10^{13}$，1 世纪取 $3.1536\times10^{15}$。
>
> | $f(n)$ | 1 秒 | 1 分钟 | 1 小时 | 1 天 | 1 个月 | 1 年 | 1 世纪 |
> |--------|------|--------|--------|------|--------|------|--------|
> | $\lg n$ | $2^{10^{6}}$ | $2^{6\times10^{7}}$ | $2^{3.6\times10^{9}}$ | $2^{8.6\times10^{10}}$ | $2^{2.6\times10^{12}}$ | $2^{3.2\times10^{13}}$ | $2^{3.2\times10^{15}}$ |
> | $\sqrt{n}$ | 1000 | 7745 | 60000 | 293938 | 1609968 | 5615692 | 56156922 |
> | $n$ | $10^{6}$ | $6\times10^{7}$ | $3.6\times10^{9}$ | $8.6\times10^{10}$ | $2.6\times10^{12}$ | $3.2\times10^{13}$ | $3.2\times10^{15}$ |
> | $n\lg n$ | 62746 | 2801417 | 133378058 | 2755147513 | $7.2\times10^{10}$ | $8.0\times10^{11}$ | $6.9\times10^{13}$ |
> | $n^{2}$ | 1000 | 7745 | 60000 | 293938 | 1609968 | 5615692 | 56156922 |
> | $n^{3}$ | 100 | 391 | 1532 | 4420 | 13736 | 31593 | 146645 |
> | $2^{n}$ | 19 | 25 | 31 | 36 | 41 | 44 | 51 |
> | $n!$ | 9 | 11 | 12 | 13 | 15 | 16 | 17 |
>
> 读表方法一：看行内增长。$n!$ 那一行从 1 秒到 1 世纪只从 9 涨到 17，涨了不到一倍；$\sqrt{n}$ 那一行从 $10^{3}$ 涨到 $5.6\times10^{7}$，涨了五万多倍。同样的时间预算翻 $10^{9}$ 倍，对不同 $f(n)$ 的收益天差地别——阶乘级算法几乎买不到规模，平方根级算法能买到五个数量级。
>
> 读表方法二：看列内比较。1 世纪那一列里，$n$ 可以到 $3.2\times10^{15}$，而 $2^{n}$ 只到 51。也就是说，一个世纪的计算时间买到的指数级算法规模只有 51 个元素——这就是为什么在 NP-complete（NP 完全）问题上“等硬件”没有意义，硬件给的是常数倍，而这里的差距是阶。
>
> 手算校验两格，确认这张表不是抄来的。第一格：$n\lg n$ 在 1 秒（$10^{6}$ 微秒）时解 $n\log_{2}n=10^{6}$，取 $n=62746$ 得 $62746\times15.94\approx1.0\times10^{6}$，正好卡在预算上。第二格：$n!$ 在 1 秒时，$9!=362880\le10^{6}$ 而 $10!=3628800>10^{6}$，所以是 9，不是 10。
>
> $\lg n$ 那一行为什么是天文数字：解 $\lg n\le t$ 就是 $n\le2^{t}$，而 $t$ 本身从 $10^{6}$ 到 $3\times10^{15}$，所以 $n$ 落在 $2^{10^{6}}$ 这种量级。这不是造表时偷懒，而是对数增长的真实含义：输入每翻一倍，只多花一步，于是时间预算的一点点增长就能换来规模的爆炸式扩张。
>
> 还有一个单位陷阱：题目说 $f(n)$ 以微秒计，所以 $f(n)=n^{2}$ 在 1 秒内可解 $n=1000$，因为 $1000^{2}=10^{6}$ 微秒恰好是 1 秒。若误以为以秒计，同一格会错成 $n=1$。这类题最常见的失分点不是解方程，而是单位错位。
>
> 末两行的对比值得单独记：$2^{n}$ 与 $n!$ 都是指数级，但 $n!$ 的底数随 $n$ 增长，所以撞墙更快——1 世纪列上 $2^{n}$ 给 51，$n!$ 只给 17。同样的时间预算，阶乘级算法拿到的规模只有指数级的三分之一。
>
> 这张表的用途不是背数字，而是建立“规模预算”的直觉：给定时间预算与增长阶，立刻估出可解规模；给定必须处理的规模，立刻判断哪个阶还活得下去。这是分析 algorithm（算法）时最先要用的一次心算。
>
> 还有一类容易被忽略的读法：把行与列看成“预算”的两种分配方式。行是选定增长阶之后看预算能给多少规模，列是选定预算之后看哪种增长阶还活得下去。真正做工程决策时，顺序通常是先定列（你手上有多少时间），再在行里挑一个能覆盖目标规模的增长阶——这就是选 algorithm（算法）的正确顺序。
>
> 关于 $n\lg n$ 这一行再补一个实用刻度：62746 这个数在真实系统里很有名，它大约就是“一秒钟能排序的元素数”的量级，很多工程直觉都围绕它建立。记住这一个数，比记住七列全部数字更有用。

| $f(n)$ | 1 second | 1 minute | 1 hour | 1 day | 1 month | 1 year | 1 century |
|--------|----------|----------|--------|-------|---------|--------|-----------|
| $\lg n$ | | | | | | | |
| $\sqrt{n}$ | | | | | | | |
| $n$ | | | | | | | |
| $n \lg n$ | | | | | | | |
| $n^2$ | | | | | | | |
| $n^3$ | | | | | | | |
| $2^n$ | | | | | | | |
| $n!$ | | | | | | | |

### Notes for Chapter 1 <span style="color:#2471a3;">**[reference]**</span>

**Chapter notes**

There are many excellent texts on the general topic of algorithms, including those by Aho, Hopcroft, and Ullman [5, 6]; Baase and Van Gelder [28]; Brassard and Bratley [54]; Dasgupta, Papadimitriou, and Vazirani [82]; Goodrich and Tamassia [148]; Hofri [175]; Horowitz, Sahni, and Rajasekaran [181]; Johnsonbaugh and Schaefer [193]; Kingston [205]; Kleinberg and Tardos [208]; Knuth [209, 210, 211]; Kozen [220]; Levitin [235]; Manber [242]; Mehlhorn [249, 250, 251]; Purdom and Brown [287]; Reingold, Nievergelt, and Deo [293]; Sedgewick [306]; Sedgewick and Flajolet [307]; Skiena [318]; and Wilf [356]. Some of the more practical aspects of algorithm design are discussed by Bentley [42, 43] and Gonnet [145]. Surveys of the field of algorithms can also be found in the Handbook of Theoretical Computer Science, Volume A [342] and the CRC Algorithms and Theory of Computation Handbook [25]. Overviews of the algorithms used in computational biology can be found in textbooks by Gusfield [156], Pevzner [275], Setubal and Meidanis [310], and Waterman [350].

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 历史注：文献列表里的 Knuth 三卷即《The Art of Computer Programming》，而 algorithm（算法）这个词本身，来自一位 9 世纪学者的名字。
>
> 先把书目事实钉住（已查一手线索）：Donald Knuth 生于 1938 年，1962 年动手写这套书，原计划一本十二章；第一卷 Fundamental Algorithms 于 1968 年由 Addison-Wesley 出版，第二卷 1969 年、第三卷 1973 年；此后长期停顿，2011 年出版第四卷 A 册，之后又出第四卷 B 册。他 1974 年获 ACM Turing Award（图灵奖），同年图灵奖演讲题为 Computer Programming as an Art。业界称他为 the father of the analysis of algorithms（算法分析之父）。
>
> 为什么这套书记载的是方法而不是一堆 algorithm（算法）：它第一次把“算法描述 + 正确性证明 + 精确的运行时间分析”当作一个整体来写。精确到什么程度？insertion sort（插入排序）的比较次数不只写 $\Theta(n^{2})$，而是给出带系数的表达式，例如平均情况约 $\frac{1}{4}n^{2}$ 量级再加上低阶修正。正是这种“连系数都要算清”的习惯，让 average-case analysis（平均情况分析）成为可能。
>
> 名字的来路也值得记：al-Khwārizmī（约 780–850）在巴格达的 House of Wisdom（智慧宫）任职，约 820 年写成《Al-Jabr》，书名正是 algebra（代数）一词的来源；他的名字拉丁化为 Algoritmi，12 世纪随译本进入欧洲后写成 algorism，一度专指十进制算术的逐步计算程序，最后演变成 algorithm（算法）。所以“算法”与“代数”是同一位学者的两份遗产。
>
> 一个反直觉的点：在 20 世纪之前，algorithm（算法）并不指“抽象的计算过程”，而指“用阿拉伯数字做算术的具体手法”，接近今天的“口诀”。它从口诀升级为概念，靠的是 20 世纪把“有限步、无歧义、可执行”形式化的努力——也就是第 1 章那段定义的全部内容。词义的变迁本身就是学科成熟度的刻度。
>
> 与 CSAPP 的连接：Knuth 的精确分析必须先绑定一台假想机器，他为此设计了 MIX；CSAPP 第 3、4 章给你的是一台真实的 x86-64。两者的思路完全一致——把 program（程序）落到机器级动作上再计数；区别在于 MIX 追求可移植的分析结论，x86-64 追求可执行的现实行为。
>
> 阅读建议也要说清：TAOCP 不是通读材料，是查阅工具。想知道某个 sorting algorithm（排序算法）的全部变体与精确常数，去 Knuth 对应小节；想建立框架、学证明模板，留在 CLRS。两者不是替代关系，而是“查数”与“搭骨架”的分工。
>
> 收束：CLRS 第 2 章末尾的 Chapter notes 又提了一次“algorithm（算法）来自 al-Khowârizmî”，说明作者把它当成术语的正式出处，而不是逸闻。术语的来历一旦清楚，你对“什么叫算法”的判断标准也会跟着变严。
>
> 还有一层容易被忽略：TeX 也是他为这套书造的。1970 年代末，出版社的排版质量达不到他的要求，他放下写作去写排版程序，结果意外催生了今天科学出版的事实标准。这件事是他那种“连系数与字形间距都要算清”的性格的延伸，不是岔路。
>
> 所以读这套书的正确姿势是查而不是背：把它当成一张带精确数字的表，遇到具体的 sorting algorithm（排序算法）再去翻对应小节，不要企图线性通读。

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.16</span>

## Chapter 2（第 2 章）· Getting Started（入门）

本章将使你熟悉一个 framework（框架），我们将用它来贯穿全书地思考 algorithms（算法）的 design（设计）与 analysis（分析）。本章 self-contained（自成一体），不过确实包含了对第 3 章和第 4 章所引入内容的若干 references（引用）。（它还包含几个 summations（求和式），Appendix A（附录 A）会说明如何求解它们。）

我们首先考察 insertion sort algorithm（插入排序算法），用它来解决第 1 章引入的 sorting problem（排序问题）。我们定义一个 pseudocode（伪代码）——如果你做过 computer programming（计算机编程），应该对它很熟悉——并用它来展示我们将如何 specify（描述）自己的 algorithms。在描述了 insertion sort algorithm 之后，我们再论证它确实能正确排序，并分析它的 running time（运行时间）。该 analysis 会引入一种 notation（记号），它关注的是该时间如何随待排序 items（项）的数量而增长。

在讨论完 insertion sort 之后，我们引入算法设计中的 divide-and-conquer（分治法），并用它来开发一个名为 merge sort（归并排序）的 algorithm。最后，我们对 merge sort 的 running time 进行分析。

### Section 2.1 · Insertion Sort（插入排序） <span style="color:#2471a3;">**[section]**</span>

我们的第一个 algorithm，insertion sort（插入排序），解决的是第 1 章引入的 sorting problem：

**Input（输入）：** 一个包含 $n$ 个数的 sequence（序列）$\langle a_1, a_2, \ldots, a_n \rangle$。

**Output（输出）：** input sequence（输入序列）的一个 permutation（排列，即 reordering（重排））$\langle a'_1, a'_2, \ldots, a'_n \rangle$，使得 $a'_1 \le a'_2 \le \cdots \le a'_n$。

我们想要排序的这些数也称为 keys（关键字）。虽然在概念上我们排序的是一个 sequence，但 input（输入）是以一个包含 $n$ 个 elements（元素）的 array（数组）形式到达我们手中的。

在本书中，我们通常会把 algorithms 描述成用 pseudocode（伪代码）编写的 programs（程序）；这种 pseudocode 在许多方面与 C、C++、Java、Python 或 Pascal 相似。如果你接触过其中任何一种语言，那么 reading（阅读）我们的 algorithms 应该几乎毫无困难。

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.17</span>

**Figure 2.1（图 2.1）：** 使用 insertion sort（插入排序）对一手 playing cards（扑克牌）进行排序。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 以下是对图面的文字描述（原文图注仅一句），并把它与 pseudocode（伪代码）的每一行动作对上，图才算是读完了。
>
> 图面内容：左侧桌上是一堆牌面朝下的 cards（牌），右侧是左手里已经理好的牌，牌面朝上、从左到右按 sorted order（已排序顺序）排列。取牌的动作是从牌堆顶部取一张，再从右到左与手中的每一张比较，一旦遇到第一张不大于它的牌就停下，插到那张牌的右边。
>
> 与 INSERTION-SORT 的对应关系逐条是：手中那一段就是 subarray（子数组）$A[1..j-1]$，桌上牌堆是 $A[j+1..n]$，取出的那张牌是 key（关键字），从右到左的比较是 while 循环，把较大的牌向右挪一格是 $A[i+1]=A[i]$，最后落位是 $A[i+1]=key$。一张牌都没挪动时，第 8 行仍要执行一次，这是“每次迭代恰一次落位”的来源。
>
> 图里最重要的不是动作，而是那条不变量：任何时刻左手里的牌，都是“原先在牌堆顶部的那 $j-1$ 张”，并且已经按 sorted order（已排序顺序）排列。这句话同时说了两件事——元素的集合没变（还是原来那些），顺序变好了（成了有序前缀）。后面第 19 页的 loop invariant（循环不变式）就是这句话去掉口语之后的版本。
>
> 算一下规模：$n=6$ 的牌，最坏情况（牌堆正好逆序）比较次数是 $\sum_{j=2}^{6}(j-1)=15$，最好情况（牌堆已经有序）是 5 次；等概率随机排列时，平均比较次数约 $7.5+5=12.5$ 次，落在两者之间偏上。这组数字说明“平均”并不等于“最好与最坏的中点”，而是接近最坏那一端。
>
> 为什么拿手排扑克当比喻不是凑趣：它把 algorithm（算法）的三个部件同时落在手上。data（数据）是牌；loop invariant（循环不变式）是“左手永远有序”；代价模型是“一次比较、一次移动都算一个常数”。三者齐了，才能从比喻走到分析。
>
> 比喻的边界也要划清：人手能一眼看清手里一整段牌，机器不能，所以机器必须逐格移动而不是“整体插入”。这一条差别正好解释了为什么 insertion sort（插入排序）的代价是移动次数而不是“插入一次”。凡是比喻，都要能说出它在哪失效——这也是用类比学习的最低门槛。
>
> 图的六张牌（5,2,4,6,1,3）与后面图 2.2 的状态表是同一条轨道的两个视角：图 2.1 给直觉，图 2.2 给逐次迭代后的数据。两者对照着看，你就能把“手上的动作”翻译成“array（数组）下标的变化”。
>
> 收束：读任何插图都问三个问题——画了什么对象、对应哪几行、哪条不变量在图上看得见。三问答完，图才算读完；否则你只是看了一张漂亮的画。
>
> 补一个常被问到的细节：为什么图中的牌是牌面朝下的？因为“牌堆里还剩哪些牌”对后续分析没有用，看不见反而更贴近 algorithm（算法）的真实处境——未处理部分只有规模，没有内容。一个小设定就把建模的取舍摆了出来。

那么，pseudocode（伪代码）与 “real” code（真正的代码）之间的区别在于：在 pseudocode 中，为了 specify（描述）一个给定的 algorithm，我们采用最清晰、最简洁的 expressive method（表达方式）。有时候，最清晰的表达方式是 English（英语），所以如果你在“真正的”代码段落中碰到嵌入的英文短语或句子，不必感到惊讶。pseudocode 与 real code 的另一个区别是：pseudocode 通常不关心 software engineering（软件工程）方面的问题。data abstraction（数据抽象）、modularity（模块化）和 error handling（错误处理）等问题往往会被忽略，目的是更简洁地传达 algorithm 的 essence（精髓）。

我们从 insertion sort 入手，它是针对少量 elements 进行排序的一种高效 algorithm。insertion sort 的工作方式与许多人整理一手 playing cards 的方式相同：我们从一只空的 left hand（左手）以及桌上牌面朝下的 cards 开始，然后一次从桌上取出一张 card（扑克牌），把它插入 left hand 中正确的位置。为了找到一张 card 的正确位置，我们把它与手中已有的每一张 card 从右到左逐一比较，如图 2.1（Figure 2.1）所示。在任何时刻，left hand 中持有的 cards 都是已排序的，而且这些 cards 原本正是桌上 pile 顶部的 cards。

我们把 insertion sort 的 pseudocode 表示为一个名为 INSERTION-SORT 的 procedure（过程），它以 array（数组）$A[1..n]$ 作为参数，该 array 包含一个长度为 $n$、待排序的 sequence（序列）。（在代码中，$A$ 中 elements 的个数 $n$ 记作 $A.length$。）该 algorithm 对输入的数进行 in place（原地）排序：它在 array $A$ 内部重新排列这些数，任意时刻存储在 array 之外的数至多只有 constant（常数）个。当 INSERTION-SORT procedure 结束时，input array（输入数组）$A$ 中就包含了已排序的 output sequence（输出序列）。

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.18</span>

**Figure 2.2（图 2.2）：** 对 array（数组）$A = \langle 5, 2, 4, 6, 1, 3 \rangle$ 执行 INSERTION-SORT 的操作过程。array indices（数组下标）显示在矩形上方，存储在 array 各位置中的 values（值）显示在矩形内部。(a)–(e) 为第 1–8 行 for loop（for 循环）的各次 iterations（迭代）。在每次 iteration 中，black rectangle（黑色矩形）存放取自 $A[j]$ 的 key（关键字），它会在第 5 行的 test（测试）中与它左侧 shaded rectangles（阴影矩形）中的 values 进行比较。shaded arrows（阴影箭头）表示第 6 行中 array values 向右移动一个位置，black arrows（黑色箭头）表示第 8 行中 key 所移动到的位置。(f) 为最终的 sorted array（已排序数组）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 以下为根据图 2.2 重构的逐次状态表（原文为插图，无此表格），并附上可复核的计数统计——这张表的用途是让你不必相信任何文字描述，只看表就能重算 $T(n)$ 的每一项。
>
> 读法先说清：方括号里是当前的 key（关键字）$A[j]$，方括号左边是已排好序的 $A[1..j-1]$，右边是尚未处理的 $A[j+1..n]$。每一行对应 for 循环的一次迭代，因此这张表一共有 $n-1=5$ 行。
>
> | 迭代 | $j$ | key | 迭代结束时的 array（数组）状态 | 第 5 行测试次数 $t_j$ |
> |------|-----|-----|------------------------------|------------------------|
> | (a) | 2 | 2 | 2, 5, 4, 6, 1, 3 | 2 |
> | (b) | 3 | 4 | 2, 4, 5, 6, 1, 3 | 2 |
> | (c) | 4 | 6 | 2, 4, 5, 6, 1, 3 | 1 |
> | (d) | 5 | 1 | 1, 2, 4, 5, 6, 3 | 5 |
> | (e) | 6 | 3 | 1, 2, 3, 4, 5, 6 | 4 |
>
> 统计结果：$t_2=2$、$t_3=2$、$t_4=1$、$t_5=5$、$t_6=4$，合计 14 次测试；其中判定为真、真正发生移位的次数是 9。9 这个数不是巧合，它等于输入序列的 inversion（逆序对）个数，也等于元素移动的总次数——习题 2-4 会把这件事讲成一般结论。
>
> 逐格验证两次，确认表不是编的。$t_2=2$：$j=2$、key 为 2，第一次测试“$i=1>0$ 且 $A[1]=5>2$”为真，移位、$i$ 降到 0；第二次测试“$i>0$”为假，退出。两次测试、一次移位。$t_4=1$：$j=4$、key 为 6，第一次测试 $A[3]=5>6$ 就为假，一次移位都没有，这是最省的形态。
>
> 表里最能看出最好与最坏的形状。输入若已经有序，每个 $j$ 都只花一次测试，合计 $n-1=5$ 次；输入若逆序，则 $t_j=j$，合计 $\sum_{j=2}^{6}j=20$ 次。这条 6 元素的输入花了 14 次，落在区间 $[5,20]$ 的上半段，离最坏只差 6 次。
>
> 竖着读也有信息：$i$ 每轮只往左移动 $t_j-1$ 格，$j$ 每轮固定加 1，所以 $i$ 的总行程正好等于移位数 9。把 $i$ 的行程看成“inversion（逆序对）被逐个消掉”的过程，第 5 行的每一次判真都在消掉一个 inversion（逆序对）——这张表因此也是一份逆序对计数的现场记录。
>
> 还有一层用途：把 $t_j$ 当成输入的函数而不是常数。$t_j$ 随输入形状变化，正是 best-case（最好情况）与 worst-case（最坏情况）分析的起点；若 $t_j$ 恒等于 $j$，三种情况的区分就不需要了，$T(n)$ 也就只剩一个公式。
>
> 与图 2.1 的连接：2.1 给的是手上的动作，2.2 给的是 array（数组）里的下标变化，两者是同一个 loop invariant（循环不变式）的两个投影。看图 2.2 时若只盯数字，就丢掉了不变量；盯住不变量，数字自然会长出来。
>
> 收束：这类状态表的价值在可核对性。任何“$T(n)$ 是多少”的结论，都可以回到这张表上逐项相加；能被表格复核的论证，才不是背下来的论证。
>
> 还有一个容易被跳过的地方：这张表里 $j$ 从 2 走到 6，正好是 for 循环的 5 次迭代，没有 $j=1$ 那一行。原因是长度为 1 的前缀自动有序，不需要插入。这个“少一轮”的细节在写 loop invariant（循环不变式）时很关键——base case（基例）是 $j=2$ 而不是 $j=1$，差一轮就会让整个证明错位。
>
> 把表与自己手算的结果对照一遍，是掌握 insertion sort（插入排序）最省时间的方式：手算一遍大约五分钟，而它能把“移动次数等于 inversion（逆序对）数”这件事从记忆变成经验。看表是被动的，重算一遍才是主动的。
>
> 一句话记住这张表：14 是测试次数、9 是移位次数，两个数就把这条输入上 insertion sort（插入排序）的全部代价说完了。

```text
     下标 j:  1   2   3   4   5   6
(a)         5  [2]  4   6   1   3     j = 2，黑色方格 = key = 2
(b)         2   5  [4]  6   1   3     j = 3，黑色方格 = key = 4
(c)         2   4   5  [6]  1   3     j = 4，黑色方格 = key = 6
(d)         2   4   5   6  [1]  3     j = 5，黑色方格 = key = 1
(e)         1   2   4   5   6  [3]    j = 6，黑色方格 = key = 3
(f)         1   2   3   4   5   6     最终已排序数组
```

INSERTION-SORT 的 pseudocode（伪代码）如下所示：

```text
INSERTION-SORT(A)
1  for j = 2 to A.length
2      key = A[j]
3      // Insert A[j] into the sorted sequence A[1..j-1].
4      i = j - 1
5      while i > 0 and A[i] > key
6          A[i + 1] = A[i]
7          i = i - 1
8      A[i + 1] = key
```

#### Loop Invariants and the Correctness of Insertion Sort（循环不变式与插入排序的正确性） <span style="color:#2471a3;">**[section]**</span>

这里，Figure 2.2（图 2.2）展示了该 algorithm 对 $A = \langle 5, 2, 4, 6, 1, 3 \rangle$ 的工作过程。index（下标）$j$ 指示当前正在插入手中的 “current card”（当前扑克牌）。在以 $j$ 为 index 的 for loop 的每次 iteration 开始时，由 elements（元素）$A[1..j-1]$ 构成的 subarray（子数组）构成了当前已排序的 hand（手中的牌），而剩下的 subarray（子数组）$A[j+1..n]$ 则对应仍放在桌上的 pile of cards（牌堆）。事实上，elements $A[1..j-1]$ 就是原先位于位置 $1$ 到 $j-1$ 的那些 elements，只不过现在处于 sorted order（已排序顺序）。我们把关于 $A[1..j-1]$ 的这些性质形式化地表述为一条 loop invariant（循环不变式）：

> 在第 1–8 行的 for loop 的每次 iteration 开始时，subarray $A[1..j-1]$ 由原先位于 $A[1..j-1]$ 的 elements 组成，但现在已按 sorted order（已排序顺序）排列。

我们使用 loop invariants（循环不变式）来帮助理解一个 algorithm 为什么是正确的。关于一条 loop invariant，我们必须证明三件事：

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.19</span>

**Initialization（初始化）：** 在 loop（循环）的第一次 iteration（迭代）之前它为真。

**Maintenance（保持）：** 如果它在 loop 的某次 iteration 之前为真，那么在下一次 iteration 之前它仍然为真。

**Termination（终止）：** 当 loop 终止时，invariant（不变式）会为我们提供一个有用的 property（性质），它有助于证明 algorithm（算法）是正确的。

当前两个 properties（性质）成立时，loop invariant（循环不变式）在 loop 的每一次 iteration 之前都为真。（当然，除了 loop invariant 本身之外，我们也可以自由地利用其他已确立的事实，来证明 loop invariant 在每次 iteration 之前仍然为真。）

注意这与 mathematical induction（数学归纳法）的相似之处：要证明某个 property 成立，你要证明一个 base case（基本情况）和一个 inductive step（归纳步骤）。在这里，证明 invariant 在第一次 iteration 之前成立对应着 base case，而证明 invariant 在一次 iteration 到下一次 iteration 之间保持成立则对应着 inductive step。

第三个 property 也许是最重要的一个，因为我们正是利用 loop invariant 来证明 correctness（正确性）。通常，我们把 loop invariant 与导致 loop 终止的 condition（条件）结合起来使用。termination property 不同于我们通常使用 mathematical induction 的方式——在 mathematical induction 中我们无限地应用 inductive step；而在这里，当 loop 终止时我们就停止这种 “induction”（归纳）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一论证结构值得命名为「循环不变式论证」模板，它可以与 6.042J 的 mathematical induction（数学归纳法）逐条对齐，而且对齐之后你会发现第三条性质是归纳法里根本没有的东西。
>
> 逐条对齐：Initialization（初始化）对应 base case（基例），在 INSERTION-SORT 里就是证明 $j=2$ 时的命题 $P(2)$；Maintenance（保持）对应 inductive step（归纳步），即证明“$P(j)$ 为真则 $P(j+1)$ 为真”；Termination（终止）不属于归纳，它是归纳结束之后的推论——把终止时的 $j$ 值代进 $P$。
>
> 为什么前两条只保证“永远为真”，第三条才兑换出 correctness（正确性）：$P(j)$ 说的是“$A[1..j-1]$ 由原先位于该段的元素组成、且已按 sorted order（已排序顺序）排列”。这是一条对 $j$ 的全称陈述，只要循环还在跑它就成立，但它不告诉你循环停在哪。把终止条件 $j>n$ 与“每轮 $j$ 加 1”合起来得 $j=n+1$，代入即得“$A[1..n]$ 有序”——目标结论这才落袋。
>
> 反例检验法：缺 Initialization，起点可能已错，比如“$A[1..0]$ 有序”这种空真命题会把初始化缺陷掩盖掉；缺 Maintenance，链条在中途断掉，你无法排除某个 $k$ 处为假；缺 Termination，即便不变式恒真，你也说不出它退化成了哪一句。三条各自对应一种失败模式，所以叫三件套，不叫三条建议。
>
> 与纯归纳法的区别原文点破过：mathematical induction（数学归纳法）里 inductive step 可以无限应用，没有“终点”这个概念；而循环必然终止，终止那一刻是额外信息。正是这条额外信息，把“对所有 $j$ 成立”兑换成“整个 array（数组）有序”。换句话说，归纳给你一条无限长的链，循环给你一条有限长的链加一个端点。
>
> 名字与出处值得记一笔（已查一手线索）：把 loop invariant（循环不变式）作为证明方法系统提出的，是 Robert Floyd 1967 年的论文 Assigning Meanings to Programs（发表于 Applied Mathematics 会议论文集第 19 卷）。CLRS 第 2 章末的 Chapter notes 沿的正是这条脉络，并指出程序正确性证明领域最早的文章出自 P. Naur。
>
> 给一份能直接用的清单，写 loop invariant（循环不变式）时问三句：陈述里出现的变量（这里是 $j$ 与 $A$）在终止时是否都有确定取值？终止时的退化形式是否恰好是你要证的结论？它是否强到足以推出结论、又弱到能在每轮维持？三问全过，证明就是填空。
>
> 收束：模板的名字不重要，那两问才重要——不变式是什么？终止时它退化成什么？这两问答完，整条证明的骨架就已经站在那里了。
>
> 还有一个反直觉之处：loop invariant（循环不变式）不是“循环结束后成立的性质”，而是“每轮开始时都成立的性质”。前者叫 postcondition（后置条件），后者才叫不变式。把两者混同，就会写出“循环结束后数组有序”这种根本无法逐轮验证的陈述。
>
> 具体差别在于检验次数：postcondition（后置条件）只在一处被检验，不变式要在每一处被维持，所以它必须写得足够“本地”——只涉及当轮可观测的变量。这也是为什么 CLRS 的不变式里只出现 $j$ 与 $A[1..j-1]$，而不出现“已经消掉了多少个 inversion（逆序对）”这种全局量。

下面我们来看看这些 properties 对 insertion sort（插入排序）是如何成立的。

**Initialization（初始化）：** 我们首先证明当 $j = 2$ [1] 时，loop invariant 在第一次 loop iteration 之前成立。因此，subarray（子数组）$A[1..j-1]$ 只包含单独一个 element（元素）$A[1]$，它事实上正是原先位于 $A[1]$ 的 element。此外，这个 subarray 是已排序的（当然，这是平凡的），这就证明了 loop invariant 在 loop 的第一次 iteration 之前成立。

**Maintenance（保持）：** 接下来，我们处理第二个 property：证明每次 iteration 都维持 loop invariant。非形式地说，for loop 的 body（循环体）是这样工作的：把 $A[j-1]$、$A[j-2]$、$A[j-3]$ 等等依次向右移动一个 position（位置），直到为 $A[j]$ 找到合适的 position 为止（第 4–7 行），在那一刻它把 $A[j]$ 的 value（值）插入该 position（第 8 行）。于是 subarray $A[1..j]$ 就由原先位于 $A[1..j]$ 的 elements 组成，但处于 sorted order（已排序顺序）。随后为 for loop 的下一次 iteration 把 $j$ 递增 1，这样就保持了 loop invariant。

对第二个 property 进行更形式化的处理，需要我们为第 5–7 行的 while loop（while 循环）陈述并证明一条 loop invariant。然而，在目前这个阶段，

> <span style="color:#7f8c8d;">**[1]** 当 loop 是 for loop 时，我们在第一次 iteration 之前检查 loop invariant 的时刻，恰好在 loop-counter variable（循环计数器变量）的 initial assignment（初始赋值）之后、loop header（循环头）中第一次 test 之前。就 INSERTION-SORT 而言，这个时刻是在把 2 赋给 variable（变量）$j$ 之后、第一次 test 是否 $j \le A.length$ 之前。</span>

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.20</span>

我们宁可不要陷入这种 formalism（形式化）的细节之中；因此，我们依靠 informal analysis（非形式化的分析）来证明第二个 property（性质）对外层 loop（循环）成立。

**Termination（终止）：** 最后，我们考察 loop 终止时会发生什么。导致 for loop 终止的 condition（条件）是 $j > A.length = n$。因为 loop 的每次 iteration（迭代）都会使 $j$ 增加 1，所以在那个时刻必定有 $j = n + 1$。把 $n + 1$ 代入 loop invariant（循环不变式）表述中的 $j$，我们得到：subarray（子数组）$A[1..n]$ 由原先位于 $A[1..n]$ 的 elements（元素）组成，但处于 sorted order（已排序顺序）。注意到 subarray $A[1..n]$ 就是整个 array（数组），我们得出结论：整个 array 是已排序的。因此，该 algorithm（算法）是正确的。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这份证明里藏着一个递进逻辑：为什么只需“初始化 + 保持 + 终止条件”三样东西，就足以推出 correctness（正确性）？答案是一次最小反例论证。
>
> 关键在于不变式是对一个有限索引集的全称命题，这里的索引集是 $\{2,3,\ldots,n+1\}$。有限集合上的全称命题可以用最小反例法证：假设存在某一轮开始时不变式为假，取其中最早的那一轮 $k$。$k$ 不能是 2，因为 Initialization（初始化）已经排除了它；$k$ 也不能大于 2，因为 Maintenance（保持）说“若第 $k-1$ 轮为真则第 $k$ 轮为真”，而 $k-1$ 轮为真，矛盾。于是不存在反例。
>
> 三条性质各提供一台机器：Maintenance（保持）提供沿时间轴的传递性，Initialization（初始化）提供链条的第一环，Termination（终止）提供把链条末端接回目标命题的那一下。三台机器合起来才构成一条完整推理，缺任何一台，链条要么没有起点，要么中途断开，要么末端悬空。
>
> 用反例拆解看得更清楚。没有 Initialization（初始化），起点可能已经错了，最小反例法立刻失效；没有 Maintenance（保持），中间可以断，某个 $k$ 处的假无法被排除；没有 Termination（终止），你只证明了“每条前缀都有序”，却没有把它接到“整个 array（数组）有序”这个目标上——局部全对，结论不落地。
>
> 一个容易忽略的技术细节藏在脚注 1 里：for 循环的情形下，“第一次迭代之前”精确指循环计数器初始赋值之后、循环头第一次测试之前。对 INSERTION-SORT 就是“$j$ 已经是 2，但还没测 $j\le A.length$”。若把检查时刻挪到赋值之前，$j$ 无定义，命题根本不可陈述。形式化的严谨往往就藏在这种时刻选择里，而不是藏在公式里。
>
> 与 6.042J 的连接：这套结构就是“归纳 + 终点推论”，只是归纳对象从自然数换成了迭代轮数。区别在于数学归纳的步数无界，而这里的步数被终止条件钉死，所以多出一条 Termination（终止）；这也解释了为什么数学归纳里没有“第三条性质”这个东西。
>
> 一种可以照抄的写法：先把 loop invariant（循环不变式）写成含参数 $j$ 的命题 $P(j)$，再写出循环停止时 $j$ 的取值，最后把该值代进 $P$ 化简。三步做完，剩下全是填空题；反过来，若你写不出 $P(j)$ 的参数化形式，说明你还没找到真正的不变式。
>
> 收束：证明的强度不来自三条性质的名字，而来自“最小反例 + 终点实例化”这两台机器。名字只是标签，机器才是能搬去下一题的东西。
>
> 顺带一个术语区分：这套三件套给出的其实是 total correctness（完全正确性），其中 Termination（终止）那一步同时承担了“循环真的会停”的举证责任。若 algorithm（算法）可能不终止，你证到的只是“若它停，则答案正确”——那叫 partial correctness（部分正确性），是弱一档的结论。
>
> 一句话收口：三件套证明的命题是“循环会停，而且停下时对”，那个“会停”不能靠默认，必须单独举证。

在本章稍后以及在其他章节中，我们都会使用这种 loop invariants 的方法来证明 correctness（正确性）。

### <span style="color:#c0392b;">Pseudocode Conventions（伪代码约定）</span>

我们在 pseudocode（伪代码）中使用以下 conventions（约定）。

- **Indentation（缩进）表示 block structure（块结构）。** 例如，从第 1 行开始的 for loop 的 body（循环体）由第 2–8 行组成，而从第 5 行开始的 while loop 的 body 包含第 6–7 行，但不包含第 8 行。我们的 indentation 风格同样适用于 if-else statements [2]。使用 indentation 而非 begin 和 end statements 等常规的 block structure 指示符，能大大减少杂乱，同时保持甚至增强 clarity（清晰度）[3]。

- **while、for 和 repeat-until 等 looping constructs（循环结构），以及 if-else conditional construct（条件结构），其含义与 C、C++、Java、Python 和 Pascal 中的相应结构类似 [4]。** 在本书中，loop counter（循环计数器）在退出 loop 后仍保留其 value（值），这与 C++、Java 和 Pascal 中出现的某些情形不同。因此，在 for loop 刚结束后，loop counter 的 value 就是第一个超过 for loop bound（循环边界）的 value。我们在对 insertion sort（插入排序）的 correctness argument（正确性论证）中就用到了这个 property。第 1 行的 for loop header（循环头）是 `for j = 2 to A.length`，所以当该 loop 终止时，$j = A.length + 1$（等价地，$j = n + 1$，因为 $n = A.length$）。当 for loop 在每次 iteration 中递增其 loop counter 时，我们使用 keyword（关键字）`to`；

> <span style="color:#7f8c8d;">**[2]** 在 if-else statement 中，我们把 `else` 缩进到与它所匹配的 `if` 相同的层级。尽管我们省略了 keyword（关键字）`then`，但偶尔会把当 `if` 之后的 test 为真时所执行的那部分称为 then clause（then 子句）。对于 multiway tests（多路测试），在第一个 test 之后我们用 `elseif` 来表示其余 test。</span>

> <span style="color:#7f8c8d;">**[3]** 本书中的每个 pseudocode procedure（过程）都出现在同一页上，这样你就不必去辨认那些跨页拆分的 code（代码）的 indentation（缩进）层级。</span>

> <span style="color:#7f8c8d;">**[4]** 大多数 block-structured（块结构）languages 都有等价的结构，不过具体 syntax（语法）可能有所差异。Python 缺少 repeat-until loops，而且它的 for loops 与本书中的 for loops 工作方式略有不同。</span>

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.21</span>

（接上页 for loop 的 loop counter 讨论）当 for loop 递减其 loop counter（循环计数器）时，我们使用 keyword（关键字）`downto`。当 loop counter 的变化量大于 1 时，变化量跟在 optional（可选的）keyword `by` 之后。

- 符号 `//` 表示该行剩余部分是 comment（注释）。

- 形如 $i = j = e$ 的 multiple assignment（多重赋值）会把 expression（表达式）$e$ 的 value（值）同时赋给 variables（变量）$i$ 和 $j$；它应被视为等同于先执行 assignment（赋值）$j = e$、再执行 assignment $i = j$。

- variables（变量）（如 $i$、$j$ 和 key）是给定 procedure（过程）的 local（局部）variables。除非明确说明，否则我们不会使用 global variables（全局变量）。

- 我们通过给出 array name（数组名）后跟 square brackets（方括号）中的 index（下标）来访问 array elements（数组元素）。例如，$A[i]$ 表示 array（数组）$A$ 的第 $i$ 个 element（元素）。notation（记号）`..` 用来表示 array 内的一段 values 取值范围。因此，$A[1..j]$ 表示 $A$ 的 subarray（子数组），它由 $j$ 个 elements $A[1], A[2], \ldots, A[j]$ 组成。

- 我们通常把 compound data（复合数据）组织成 objects（对象），objects 由 attributes（属性）组成。我们使用许多 object-oriented programming languages（面向对象编程语言）中常见的 syntax（语法）来访问某个特定 attribute：object name（对象名），后跟一个 dot（点），再后跟 attribute name（属性名）。例如，我们把 array 视为一个 object，其 attribute length 表示它包含多少个 elements。要指定 array $A$ 中的 elements 个数，我们写作 $A.length$。

我们把表示 array 或 object 的 variable 视为指向该 array 或 object 所对应 data（数据）的一个 pointer（指针）。对于 object $x$ 的所有 attributes $f$，执行 assignment $y = x$ 会使得 $y.f$ 等于 $x.f$。此外，如果我们现在设置 $x.f = 3$，那么之后不仅 $x.f$ 等于 3，$y.f$ 也等于 3。换句话说，在执行 assignment $y = x$ 之后，$x$ 和 $y$ 指向同一个 object。

我们的 attribute notation 可以 “cascade”（级联）。例如，假设 attribute $f$ 本身是指向某种具有 attribute $g$ 的 object 的 pointer。那么 notation $x.f.g$ 会隐式地加括号为 $(x.f).g$。换句话说，如果我们已经执行了 assignment $y = x.f$，那么 $x.f.g$ 与 $y.g$ 是相同的。

有时候，pointer 可能不指向任何 object。在这种情况下，我们给它一个 special value（特殊值）NIL。

- 我们按 by value（按值传递）方式把 parameters（参数）传递给 procedure：被调用的 procedure（called procedure）收到的是 parameters 自身的一份 copy（副本），如果它给某个 parameter 赋值，这个更改不会被调用它的 procedure（calling procedure）看到。当传递 objects 时，指向该 object 所对应 data 的 pointer 会被复制，但 object 的 attributes 不会被复制。例如，如果 $x$ 是被调用 procedure 的一个 parameter，那么在被调用 procedure 内部执行的 assignment $x = y$ 对 calling procedure 是不可见的。然而，assignment $x.f = 3$ 却是可见的。类似地，arrays 是按 pointer（指针）传递的，因此

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.22</span>


### Section 2.1 Insertion sort（插入排序）· 续 <span style="color:#2471a3;">**[section]**</span>

当数组作为参数传递给过程时，传递的是指向数组的指针（a pointer to the array）而非整个数组，因此对单个数组元素（array elements）的修改在调用过程（calling procedure）中是可见的。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里“传递的是指向 array（数组）的 pointer（指针）”值得接回 CSAPP 第 3 章的机器级图景：所谓传参，复制的永远是一个机器字。
>
> 机器级事实先摆清：调用一个 procedure（过程）时，实参被放进 register（寄存器）或调用者的 stack frame（栈帧），被调用者拿到的是那份 copy（副本）。若实参是 scalar（标量），copy（副本）就是值本身；若实参是 array（数组）或 object（对象），copy（副本）是一个地址。所以 CLRS 的“按值传递 + 对象按指针传递”不是两条规则，而是一条规则加两种被复制的对象。
>
> 算一下选址过程：设 base（基址）已在寄存器里、每个元素占 4 字节，则 $A[3]$ 的地址是 base 加 12。一次访存就是“寄存器内容加立即数”的一条指令，代价常数。这就是“通过地址改写共享内存”的具体形态——所谓“看得见”，指的是写到了调用者的那块内存上。
>
> 为什么改 $A[3]$ 调用者看得见、改参数 $A$ 本身却看不见：前者是往那个地址写数据，动的是共享内存；后者是改写栈帧里那份地址 copy（副本），只改了本地那张标签。类比成立的原因是两边共享同一套“值即位模式”的表示语义；区别只在于 pseudocode（伪代码）抹掉了栈帧分配与寄存器传参的细节。
>
> CSAPP 第 3 章还能把这句话再精确一层：x86-64 上前六个整数参数走寄存器，第七个起才压栈，所以“抄进栈帧”在参数很少时并不字面成立。这不影响结论——无论放在寄存器还是栈里，传的都只是一个机器字。
>
> 一个真实陷阱：array（数组）作参数时 $A.length$ 不会自动带过去，因为被调用者只拿到地址。这正是 C 里必须另传长度的原因，也是 CSAPP 缓冲区实验里大量越界 bug 的来源。CLRS 用 $A.length$ 这个 attribute（属性）notation（记号）回避了它，但机器上没人替你记录长度。
>
> 与 6.042J 的连接：这相当于“两个名字指向同一个对象”在集合论里的影子——判等不能只比名字，要比指向的目标。区别在于数学里没有可变状态，所以“别名”这套区分只在程序语义里才有意义；一旦某个对象可被原地修改，名字与对象就必须分开谈。
>
> 收束：想通“复制的只是一个机器字”这一点，本章的 pseudocode（伪代码）与你在 CSAPP 实验里读的汇编就能逐行对照，不必再把它当成两套互不相干的约定。
>
> 再补一个下标细节：CLRS 的 array（数组）从 1 开始编号，机器上的 array（数组）从 0 开始，$A[i]$ 的真实地址是 base 加 $(i-1)\times4$。这层偏移由编译器代劳，但它解释了为什么越界写 $A[0]$ 在 pseudocode（伪代码）里是“下标 0”，在机器上却是“基址前一个元素”。
>
> 这类约定差异正是 pseudocode（伪代码）与机器码之间唯一需要翻译的东西，其余部分一一对应，不必另立一套心智模型。
>
> 记住这条区别：被复制的永远是机器字，不是对象本身；所谓“引用”，只是那个字恰好装着地址。

返回语句（return statement）会立即将控制权转移回调用过程中的调用点（the point of call）。大多数返回语句还会携带一个要返回给调用者的值。我们的伪代码与许多编程语言不同之处在于：我们允许在一条 return 语句中返回多个值（multiple values）。

布尔运算符（boolean operators）“and”和“or”是短路求值的（short circuiting）。也就是说，当对表达式“$x$ and $y$”求值时，我们先求值 $x$；若 $x$ 的值为 FALSE，则整个表达式不可能为 TRUE，因此我们不再求值 $y$。反之，若 $x$ 的值为 TRUE，则必须求值 $y$ 才能确定整个表达式的值。类似地，在表达式“$x$ or $y$”中，只有当 $x$ 的值为 FALSE 时才求值 $y$。短路运算符使我们能够写出诸如“$x \ne \text{NIL}$ and $x.f = y$”这样的布尔表达式，而不必担心当 $x$ 为 NIL 时求值 $x.f$ 会发生什么。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> short-circuit evaluation（短路求值）不只是语法便利，它是把控制流编码进布尔表达式的一招——而它管的是 correctness（正确性），不只是效率。
>
> 机器级图景：$x$ and $y$ 编译出来是“求值 $x$，测试，若为假则直接跳到整体为假”，本质上是一条条件分支指令，而不是把两个布尔值都算出来再做按位与。CSAPP 第 3 章讲条件跳转与条件传送时给过同一套图景，区别只在于这里的分支由语言语义强制，编译器无权把它换成“两边都算”。
>
> 为什么它关乎 correctness（正确性）：若 $x=\text{NIL}$，$x.f$ 在真实机器上就是对非法地址的解引用，会触发 SIGSEGV。短路恰好保证这次解引用永不执行。同样的道理落在 INSERTION-SORT 第 5 行：$i>0$ and $A[i]>key$，当 $i=0$ 时若第二个操作数被求值，就会访问 $A[0]$，在 1 起始的下标约定下已经越界。
>
> 算一下这层保护值多少钱：$n=10^{6}$ 的已有序输入，每个 $j$ 只有一次“$i>0$ 为假”的机会，共 $n-1$ 次，省下的比较也是 $n-1$ 次——量级微不足道。但省掉的是越界访问的风险，不是几次比较；把这两件事混为一谈，就会误判这条语言特性的重要性。
>
> 语义后果值得一提：短路让布尔表达式不再可交换。$x$ and $y$ 与 $y$ and $x$ 在 $x=\text{NIL}$ 时行为完全不同，所以任何优化都不能把它重排成“先算 $y$”。这条约束在编译器里是硬的，不是风格问题。
>
> C 语言里的惯用法 `if (p && p->next)` 就是同一模式在字节级的重演；而 `&` 与 `&&` 的区别正在这里——按位与会把两边都算完，指针为空时立刻炸。写代码时把“守卫”与“运算”分开，是这套语义给的最实用的一条纪律。
>
> 与 6.042J 的连接：布尔代数里的 and 是对称的，程序里的 and 不是。区别在于程序的操作数带副作用与求值代价，数学命题没有；一旦把“求值”这件事本身放进语义，交换律就要重新谈条件。
>
> 收束：读 CLRS 的长条件时，默认那是“安全卫兵”式写法——前面的条件先给后面的条件发放求值许可证。作者靠这一机制，免费换来了边界安全；你也该在自己的代码里照抄这个习惯。
>
> 还有一处值得对照的写法：$x \ne \text{NIL}$ and $x.f = y$。若把 and 换成数学里的合取，这个式子根本不合法，因为第二个合取项在 $x$ 为空时没有真值；short-circuit evaluation（短路求值）把“有没有真值”推迟到运行期决定，于是它重新成为一条合法表达式。
>
> 反过来看，这也划出了真值表法的边界：真值表假定每个子表达式都有真值，而短路语义恰恰在破坏这个前提。凡带副作用或可能失败的操作，都不能直接套真值表。
>
> 工程习惯上还有一条：把最便宜、最能排除的守卫放在最前面，因为它的失败概率最高、提前退出的收益最大。这是这套语义附带的一点性能红利，虽远小于它在 correctness（正确性）上的价值。

关键字 error 表示发生了错误，原因是调用该过程时的条件不正确。调用过程负责处理这一错误，因此我们并不规定应采取何种行动。

### Exercises <span style="color:#2471a3;">**[exercise]**</span>

**2.1-1**
Using Figure 2.2 as a model, illustrate the operation of INSERTION-SORT on the array $A = \langle 31, 41, 59, 26, 41, 58\rangle$.

**2.1-2**
Rewrite the INSERTION-SORT procedure to sort into nonincreasing instead of nondecreasing order.

**2.1-3**
Consider the searching problem:

*Input:* A sequence of $n$ numbers $A = \langle a_1, a_2, \ldots, a_n\rangle$ and a value $v$.
*Output:* An index $i$ such that $v = A[i]$ or the special value NIL if $v$ does not appear in $A$.

Write pseudocode for linear search, which scans through the sequence, looking for $v$. Using a loop invariant, prove that your algorithm is correct. Make sure that your loop invariant fulfills the three necessary properties.

**2.1-4**
Consider the problem of adding two $n$-bit binary integers, stored in two $n$-element arrays $A$ and $B$. The sum of the two integers should be stored in binary form in an $(n+1)$-element array $C$. State the problem formally and write pseudocode for adding the two integers.

---

> <span style="color:#7f8c8d;">CLRS §2.2, p.23</span>

### Section 2.2 Analyzing algorithms（分析算法）<span style="color:#2471a3;">**[section]**</span>

分析算法（analyzing an algorithm）如今意味着预测算法所需的资源（resources）。偶尔，内存、通信带宽（communication bandwidth）或计算机硬件等资源是首要关注点，但大多数时候我们想要度量的是计算时间（computational time）。一般而言，通过分析一个问题的若干个候选算法，我们能够找出其中最有效率的一个。这样的分析可能会指出不止一个可行的候选，但在此过程中我们常常能淘汰若干较差的算法。

在分析算法之前，我们必须拥有一个所用实现技术（implementation technology）的模型，包括该技术的资源模型及其代价（costs）。在本书的大部分内容中，我们将假设一个通用的单处理器随机访问机器（random-access machine，RAM）计算模型作为实现技术，并理解我们的算法将被实现为计算机程序。在 RAM 模型中，指令（instructions）一条接一条地执行，没有并发操作（concurrent operations）。

严格来说，我们应当精确定义 RAM 模型的指令及其代价。然而这样做既繁琐，又对算法设计与分析的洞察力帮助甚微。但我们仍需小心，不要滥用 RAM 模型。例如，如果一台 RAM 有一条能够排序的指令会怎样？那我们只需一条指令就能完成排序。这样的 RAM 是不现实的，因为真实计算机并没有这样的指令。因此，我们的准则是以真实计算机的设计方式为依据。RAM 模型包含真实计算机中常见的指令：算术运算（arithmetic，如加、减、乘、除、取余、下取整（floor）、上取整（ceiling））、数据移动（data movement，加载（load）、存储（store）、复制（copy）），以及控制（control，条件与无条件转移、子程序调用与返回）。每一条这样的指令都花费一段常量时间（constant amount of time）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 追问一层：为什么分析 algorithm（算法）之前，要先立“每条指令花费常数时间”这条假设？因为不立它，“运行时间”就不是一个 well-defined（定义良好）的量。
>
> 同一段代码在解释器、带多级 cache（缓存）的 x86、GPU 上可以差几个数量级，没有公共标尺就无法比较 algorithm（算法）本身。RAM model（随机访问机模型）的做法是先抽掉全部实现差异，把“步数”当作与机器无关的代理变量——于是比较的对象从“某台机器上的某段代码”变成“两个计数函数”。
>
> 它丢掉了什么？cache（缓存）层级、pipeline（流水线）、分支预测、virtual memory（虚拟内存）——恰是 CSAPP 第 5、6 章优化的全部舞台。同一次顺序遍历与一次跨步遍历，仅因 cache（缓存）友好与否就能差数倍，而这些全被抹进 $c_i$ 里。
>
> 为什么抹平之后结论仍然有用：对足够大的 $n$，由 algorithm（算法）结构决定的主项会压倒常数级差异；而且“$n^{2}$ 次比较”这类计数结论在任何机器上都成立。代价是：当两个 algorithm（算法）的增长阶相同时，被抹掉的 constant factor（常数因子）与 cache（缓存）行为反而成为胜负手——那是 CSAPP 教你的战场。
>
> 一条必须守住的边界：model（模型）不能强到不现实。书里举的反例是“若这台 RAM 有一条能排序的指令会怎样”——那只需一条指令就能完成排序，模型立刻失去意义。所以准则是照着真实机器的设计方式造模型，指令集只含 arithmetic（算术）、data movement（数据移动）与 control（控制）三类。
>
> 字长假设也是一条边界：处理规模为 $n$ 的输入时，假定整数用 $c\lg n$ 位表示，$c\ge1$ 且为常数。$c\ge1$ 保证一个字能装下 $n$、从而能索引单个输入元素；$c$ 是常数则禁止字长任意增长——否则一个字能装海量信息并一步处理完，排序都能变成常数时间。
>
> 灰色地带值得单独记：求幂 $x^{y}$ 一般不是常数时间操作；但 $2^{k}$ 在 $k$ 不超过字长时，可以用一条左移指令完成，所以被当作常数时间。CLRS 明说会尽量避开这类灰色地带，但保留这一条便利，因为它让“数组长度上界”这类论证写起来干净。
>
> 与 6.042J 的连接：这就是“先固定公理系统、再谈定理”的工程版。model（模型）是公理，$T(n)$ 是定理；换一组公理，结论的形状会变，但证明的方法不变。
>
> 收束：RAM model（随机访问机模型）不是对现实的描述，而是一份可检验的约定。它的全部价值在于：让“$n^{2}$ 与 $n\lg n$ 哪个更好”这个问题，有一个不依赖具体机器的答案。
>
> 还有一条常被忽略的推论：既然 model（模型）里的“步”与机器无关，$T(n)$ 的常数项就不能跨机器比较，只有增长阶能跨机器比较。这解释了为什么讨论 algorithm（算法）时几乎只用 $\Theta$，而报告程序性能时才给带单位的绝对时间——两者说的不是同一层次的量。
>
> 还有一个实践后果：因为 model（模型）抹平了存储层次，同一 algorithm（算法）在“工作集放得下”与“放不下”两种情形下的实测差距可以到两个数量级。这不是模型错了，而是模型的适用范围到了边界；判据是：若工作集远超 cache（缓存）容量，就得换用带层次的外部存储模型重新分析。

RAM 模型中的数据类型（data types）是整数（integer）和浮点数（floating point，用于存储实数）。虽然本书中我们通常不关心精度，但在某些应用中精度至关重要。我们还假设每个数据字（word）的大小有一个上限。例如，当处理规模为 $n$ 的输入时，我们通常假设整数用 $c\lg n$ 位表示，其中 $c \ge 1$ 为某个常量。我们要求 $c \ge 1$，这样每个字都能容纳 $n$ 的值，从而能够对单个输入元素进行索引；我们又把 $c$ 限制为常量，这样字长就不会任意增长。（如果字长可以任意增长，我们就能在一个字中存储海量数据，并以常量时间全部处理——这显然是不现实的场景。）

---

> <span style="color:#7f8c8d;">CLRS §2.2, p.24</span>

真实计算机还包含上述未列出的指令，这类指令在 RAM 模型中代表一个灰色地带（gray area）。例如，求幂（exponentiation）是否是一条常量时间指令？在一般情况下不是：当 $x$ 和 $y$ 是实数时，计算 $x^y$ 需要若干条指令。然而在某些受限情形下，求幂是常量时间操作。许多计算机有一条“左移”（shift left）指令，能在常量时间内把整数的各位向左移动 $k$ 个位置。在大多数计算机上，把整数各位向左移动一个位置等价于乘以 2，因此向左移动 $k$ 个位置等价于乘以 $2^k$。于是，只要 $k$ 不超过计算机字中的位数，这类计算机就可以通过把整数 1 向左移动 $k$ 个位置这一条常量时间指令来计算 $2^k$。我们将尽力避免 RAM 模型中的这类灰色地带，但当 $k$ 是足够小的正整数时，我们会把计算 $2^k$ 视为常量时间操作。

在 RAM 模型中，我们并不试图对当代计算机中常见的内存层次结构（memory hierarchy）建模。也就是说，我们不建立缓存（caches）或虚拟内存（virtual memory）的模型。有若干计算模型试图考虑内存层次结构的影响，这些影响在真实机器上运行真实程序时有时相当显著。本书中有少量问题考察内存层次结构的影响，但大多数情况下，本书中的分析不会考虑它们。包含内存层次结构的模型比 RAM 模型复杂得多，因此可能难以使用。此外，RAM 模型的分析通常是实际机器上性能的极佳预测。

即使在 RAM 模型中分析一个简单算法也可能颇具挑战。所需的数学工具可能包括组合学（combinatorics）、概率论（probability theory）、代数技巧（algebraic dexterity），以及识别公式中最显著项的能力。由于算法的行为可能随每个可能的输入而不同，我们需要一种手段把这些行为概括为简单、易理解的公式。

尽管我们通常只为给定算法选择一个机器模型进行分析，但在决定如何表达分析结果时仍面临许多选择。我们希望有一种既易于书写和操作、又能展现算法资源需求的重要特征、同时抑制繁琐细节的表达方式。

#### Analysis of insertion sort（插入排序的分析）<span style="color:#2471a3;">**[section]**</span>

INSERTION-SORT 过程所花费的时间取决于输入：排序一千个数比排序三个数耗时更长。此外，对于两个规模相同但已排序程度不同的输入序列，INSERTION-SORT 所花费的时间也可能不同。一般而言，算法花费的时间随输入规模（input size）的增长而增长，因此传统上把程序的运行时间（running time）描述为输入规模的函数。要做到这一点，我们需要更仔细地定义“运行时间”和“输入规模”这两个术语。

---

> <span style="color:#7f8c8d;">CLRS §2.2, p.25</span>

输入规模的最佳度量取决于所研究的问题。对许多问题而言，例如排序或计算离散傅里叶变换（discrete Fourier transforms），最自然的度量是输入中项的数目——例如排序时的数组规模 $n$。对许多其他问题，例如两个整数相乘，输入规模的最佳度量是用普通二进制记法表示该输入所需的总位数。有时，用两个数而非一个数来描述输入规模更合适。例如，若算法的输入是一个图，则输入规模可以用图中的顶点数和边数来描述。我们将针对所研究的每个问题说明所采用的输入规模度量。

算法在某个特定输入上的运行时间（running time）是所执行基本操作（primitive operations）或“步”（steps）的数目。把“步”的概念定义得尽可能与机器无关是方便的。眼下，让我们采用以下观点：执行伪代码的每一行需要一段常量时间。一行与另一行所花费的时间可能不同，但我们假设第 $i$ 行的每次执行花费时间 $c_i$，其中 $c_i$ 是常量。这一观点与 RAM 模型一致，也反映了伪代码在大多数实际计算机上会如何实现。

> <span style="color:#7f8c8d;">脚注 5：</span>这里存在一些微妙之处。我们用英语描述的计算步（computational steps）常常是需要超过常量时间的过程的变体。例如，本书后面可能会说“按 x 坐标对点排序”，正如我们将看到的，这需要超过常量时间。此外，请注意一条调用子程序的语句本身花费常量时间，尽管子程序一旦被调用可能花费更多时间。也就是说，我们把调用子程序的过程——向其传递参数等——与执行子程序的过程区分开来。

在接下来的讨论中，我们对 INSERTION-SORT 运行时间的表达式会从一个使用全部语句代价 $c_i$ 的杂乱公式，演化为一种更简洁、更易于操作的记号。这种更简单的记号也会使我们易于判断一个算法是否比另一个更有效率。

我们从给出 INSERTION-SORT 过程开始，列出每条语句的时间“代价”（cost）以及每条语句的执行次数（number of times executed）。对每个 $j = 2, 3, \ldots, n$（其中 $n = A.length$），我们令 $t_j$ 表示对于该 $j$ 值，第 5 行中 while 循环测试被执行的次数。当一个 for 或 while 循环以通常方式退出（即由于循环头中的测试）时，测试比循环体多执行一次。我们假设注释不是可执行语句，因此它们不花费时间。

---

> <span style="color:#7f8c8d;">CLRS §2.2, p.26</span>

| 行 | INSERTION-SORT(A) | cost（代价） | times（次数） |
|----|-------------------|------|-------|
| 1 | `for j = 2 to A.length` | $c_1$ | $n$ |
| 2 | `key = A[j]` | $c_2$ | $n - 1$ |
| 3 | `// Insert A[j] into the sorted sequence A[1..j-1].` | 0 | $n - 1$ |
| 4 | `i = j - 1` | $c_4$ | $n - 1$ |
| 5 | `while i > 0 and A[i] > key` | $c_5$ | $\sum_{j=2}^{n} t_j$ |
| 6 | `A[i + 1] = A[i]` | $c_6$ | $\sum_{j=2}^{n} (t_j - 1)$ |
| 7 | `i = i - 1` | $c_7$ | $\sum_{j=2}^{n} (t_j - 1)$ |
| 8 | `A[i + 1] = key` | $c_8$ | $n - 1$ |

算法的运行时间是各条已执行语句的运行时间之和；一条以 $c_i$ 步执行并执行 $n$ 次的语句，将对总运行时间贡献 $c_i n$。为了计算 $T(n)$，即 INSERTION-SORT 在包含 $n$ 个值的输入上的运行时间，我们将代价列与次数列相乘后求和，得到：

```math
T(n) = c_1 n + c_2(n-1) + c_4(n-1) + c_5 \sum_{j=2}^{n} t_j + c_6 \sum_{j=2}^{n} (t_j - 1) + c_7 \sum_{j=2}^{n} (t_j - 1) + c_8(n-1).
```

> <span style="color:#7f8c8d;">脚注 6：</span>这一特征对内存之类的资源并不一定成立。一条引用 $m$ 个字的内存、被执行 $n$ 次的语句，并不一定引用 $mn$ 个不同的内存字。

即使对于给定规模的输入，算法的运行时间也可能取决于该规模下的具体输入。例如，在 INSERTION-SORT 中，若数组已排序，则出现最好情况（best case）。对每个 $j = 2, 3, \ldots, n$，当 $i$ 取初始值 $j - 1$ 时，我们在第 5 行发现 $A[i] \le$ key。因此对 $j = 2, 3, \ldots, n$ 有 $t_j = 1$，最好情况运行时间（best-case running time）为：

```math
T(n) = c_1 n + c_2(n-1) + c_4(n-1) + c_5(n-1) + c_8(n-1) = (c_1 + c_2 + c_4 + c_5 + c_8)n - (c_2 + c_4 + c_5 + c_8).
```

我们可以把这一运行时间表示为 $an + b$，其中常量 $a$ 和 $b$ 依赖于语句代价 $c_i$；因此它是 $n$ 的线性函数（linear function）。

若数组处于逆序排序（reverse sorted order）——即递减顺序（decreasing order）——则出现最坏情况（worst case）。我们必须将每个元素 $A[j]$ 与整个已排序子数组 $A[1..j-1]$ 中的每个元素进行比较，因此对 $j = 2, 3, \ldots, n$ 有 $t_j = j$。

---

> <span style="color:#7f8c8d;">CLRS §2.2, p.27</span>

由于

```math
\sum_{j=2}^{n} j = \frac{n(n+1)}{2} - 1
```

且

```math
\sum_{j=2}^{n} (j-1) = \frac{n(n-1)}{2}
```

（参见附录 A 复习如何求解这些求和式），我们发现最坏情况下 INSERTION-SORT 的运行时间为：

```math
\begin{aligned}
T(n) &= c_1 n + c_2(n-1) + c_4(n-1) + c_5\left(\frac{n(n+1)}{2} - 1\right) + c_6\left(\frac{n(n-1)}{2}\right) + c_7\left(\frac{n(n-1)}{2}\right) + c_8(n-1) \\
&= \left(\frac{c_5}{2} + \frac{c_6}{2} + \frac{c_7}{2}\right)n^2 + \left(c_1 + c_2 + c_4 + \frac{c_5}{2} - \frac{c_6}{2} - \frac{c_7}{2} + c_8\right)n - (c_2 + c_4 + c_5 + c_8).
\end{aligned}
```

我们可以把这一最坏情况运行时间表示为 $an^2 + bn + c$，其中常量 $a$、$b$、$c$ 同样依赖于语句代价 $c_i$；因此它是 $n$ 的二次函数（quadratic function）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里把从 $t_j=j$ 到 $an^{2}+bn+c$ 的推演重演一遍，沉淀成可复用的三步模板：枚举形状、逐行乘积求和、合并同类项。
>
> 第一步，分情形枚举输入的“形状”：已排序给 $t_j=1$，逆序给 $t_j=j$。这一步的实质是把“输入”这个无穷维对象压成一个参数化的族——这正是 best-case（最好情况）、worst-case（最坏情况）、average-case（平均情况）三分法的来源。没有这一步，$T(n)$ 只是一个说不出口的函数。
>
> 第二步，逐行“代价乘次数”再求和。唯一要下功夫的是两个求和：$\sum_{j=2}^{n}j=n(n+1)/2-1$ 与 $\sum_{j=2}^{n}(j-1)=n(n-1)/2$。前者用 6.042J 的配对法（首尾相加）立得；后者其实是 $\sum_{j=1}^{n-1}j$，换个下标就是同一个公式，不必另记。
>
> 第三步，合并同类项。$c_5\cdot n(n+1)/2$ 贡献 $n^{2}$ 项与 $n$ 项；$c_6$ 与 $c_7$ 各贡献 $n(n-1)/2$，同样只到 $n^{2}$；其余各行的 $n-1$ 只贡献 $n$ 项与常数项。于是 $an^{2}+bn+c$ 自然浮现，其中 $a=(c_5+c_6+c_7)/2$。
>
> 关键读法：$n^{2}$ 的系数只含 $c_5,c_6,c_7$，恰是 while 循环体的那三行。这不是巧合，而是“内层循环决定增长阶”的直接证据——外层每轮只做常数工作，内层每轮做与 $n$ 成正比的工作，谁进平方项一目了然。
>
> 用具体数字校验一遍：令所有 $c_i=1$、$n=100$。此时 $\sum t_j=5049$、$\sum(t_j-1)=4950$，逐行代入得总和 $100+99+99+5049+4950+4950+99=15346$；再用合并后的公式算，$a=1.5$、$b=3.5$、$c=-4$，得 $1.5\times10^{4}+350-4=15346$。两条路给出同一个数，说明合并没有漏项。
>
> 模板的适用范围要说清：它只适用于“每行代价是常数、执行次数可由输入参数刻画”的 pseudocode（伪代码）。一旦某行本身调用一个需要 $\Theta(n)$ 的子过程（例如“给这部分排序”），常数时间假设就破了，模板必须改成“代价也是 $n$ 的函数”，否则低估一个量级。
>
> 与 CSAPP 的连接：这套逐行计价正是 CSAPP 第 5 章优化的第一步——先数清每条指令执行多少次，再谈 pipeline（流水线）与 cache（缓存）。区别在于 CLRS 只关心次数的增长阶，CSAPP 关心次数乘上每次的周期数。
>
> 收束：模板只有三步，但三步的顺序不能乱——先枚举形状才有次数，有了次数才能乘积求和，求完和才能合并。顺序一乱，你就只能对着公式发呆。
>
> 一个细节值得盯住：$c_3$ 去哪了？表里第 3 行是注释，代价记为 0。这一步不是偷懒，而是把“注释不算可执行语句”这条约定显式化；若不写这一行，读者会怀疑你漏了一项。
>
> 另一个细节：第 1 行 `for j = 2 to A.length` 的测试次数记成 $n$ 而不是 $n-1$，因为 for 循环头在最后一次失败时也要测一次。这个“多一次”正是后面能取到 $j=n+1$ 的原因，也是 loop invariant（循环不变式）里 Termination（终止）那一步的依据。
>
> 把两个细节合起来看，计数的准确性不是为了好看：每一个加一或减一，后面都被某个论证用到。表不是装饰，它是证明的原料。
>
> 再补一个适用范围的反例：如果某行是“调用 MERGE”，它的代价就不是常数 $c_i$，而是 $\Theta(n)$。此时逐行乘积的模板会低估一个量级，必须先把子过程的代价展开再求和——模板能用，但前提是每行的代价确实是常数。

通常，如同插入排序一样，算法的运行时间对给定输入是固定的，尽管在后面的章节中我们会看到一些有趣的“随机化”（randomized）算法，其行为即使对固定输入也可能变化。

#### Worst-case and average-case analysis（最坏情况与平均情况分析）<span style="color:#2471a3;">**[section]**</span>

在我们对插入排序的分析中，我们既考察了最好情况——输入数组已排序，也考察了最坏情况——输入数组为逆序排序。不过，在本书其余部分，我们通常只专注于求出最坏情况运行时间（worst-case running time），即规模为 $n$ 的任何输入中最长的运行时间。我们给出这样做的三个理由。

- 算法的最坏情况运行时间给出了它对任何输入的运行时间的上界（upper bound）。知道这一点就提供了一种保证：算法绝不会花费更长的时间。我们无需对运行时间作某种有根据的猜测，然后期望它不会糟糕太多。
- 对某些算法而言，最坏情况出现得相当频繁。例如，在数据库中搜索某条特定信息时，当该信息不在数据库中时，搜索算法的最坏情况常常出现。在某些应用中，对不存在信息的搜索可能相当频繁。

---

> <span style="color:#7f8c8d;">CLRS §2.2, p.28</span>

- “平均情况”（average case）往往与最坏情况差不多糟糕。假设我们随机选择 $n$ 个数并应用插入排序。要确定把元素 $A[j]$ 插入子数组 $A[1..j-1]$ 中的什么位置需要多长时间？平均而言，$A[1..j-1]$ 中一半的元素小于 $A[j]$，一半的元素大于它。因此平均而言，我们检查子数组 $A[1..j-1]$ 的一半，于是 $t_j$ 约为 $j/2$。结果表明，平均情况运行时间（average-case running time）是输入规模的二次函数，正如最坏情况运行时间一样。

在某些特定情形下，我们会关注算法的平均情况运行时间；在本书中我们将看到概率分析（probabilistic analysis）技术应用于各种算法。平均情况分析的范围是有限的，因为对某个特定问题而言，“平均”输入究竟是什么可能并不明显。通常我们会假设给定规模的所有输入等可能（equally likely）。在实践中，这一假设可能被违反，但有时我们可以使用随机化算法（randomized algorithm），它做出随机选择，从而允许进行概率分析并给出期望运行时间（expected running time）。我们将在第 5 章以及随后的若干章节中更深入地探讨随机化算法。

#### Order of growth（增长阶数）<span style="color:#2471a3;">**[section]**</span>

我们使用了一些简化抽象（simplifying abstractions）来简化对 INSERTION-SORT 过程的分析。首先，我们忽略了每条语句的实际代价，用常量 $c_i$ 来表示这些代价。然后，我们观察到即便是这些常量，也给了我们超出实际需要的细节：我们把最坏情况运行时间表示为 $an^2 + bn + c$，其中常量 $a$、$b$、$c$ 依赖于语句代价 $c_i$。这样我们不仅忽略了实际的语句代价，也忽略了抽象的代价 $c_i$。

现在我们再做一次简化抽象：真正让我们感兴趣的是运行时间的增长速率（rate of growth），即增长阶数（order of growth）。因此我们只考虑公式的首项（leading term）（例如 $an^2$），因为对大的 $n$ 而言，低阶项相对无关紧要。我们也忽略首项的常量系数（constant coefficient），因为在大输入下确定计算效率时，常量因子（constant factors）不如增长阶数显著。对插入排序而言，当我们忽略低阶项和首项的常量系数后，剩下的就是来自首项的因子 $n^2$。我们称插入排序的最坏情况运行时间为 $\Theta(n^2)$（读作 “theta of n-squared”，即“$n$ 平方的 theta”）。本章中我们将非正式地使用 $\Theta$-记号（$\Theta$-notation），并在第 3 章中给出它的精确定义。

我们通常认为，若一个算法的最坏情况运行时间具有更低的增长阶数，那么它比另一个算法更有效率。由于常量因子和低阶项的存在，一个运行时间具有较高增长阶数的算法，对小的输入可能比运行时间具有较低增长阶数的算法花费更少的时间。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> “只保留首项”不是偷懒，而是刻意的信息压缩。用数字感受一下量级，你才会知道它在什么时候成立、什么时候不成立。
>
> 代典型常数 $a=1/2$、$b=20$、$c=50$：$n=100$ 时首项 5000、低阶项 2050，低阶项占 29%；$n=10^{6}$ 时首项 $5\times10^{11}$、低阶项约 $2\times10^{7}$，占比降到十万分之四。低阶项并没有消失，它只是被首项按多项式比例碾压过去了。
>
> 小规模时结论会直接翻转：$n=20$ 时首项 200、低阶项 450，低阶项占 69%；$n=10$ 时首项 50、低阶项 250，占 83%。所以“只留首项”是一个随 $n$ 增大才逐渐成立的近似，不是一个恒等式。Problem 2-1 的混合策略——小子数组用 insertion sort（插入排序）——正源于此。
>
> 为什么可以心安理得地丢：首项与低阶项的比值是 $\Theta(n)$ 量级，随 $n$ 单调放大；而 $\Theta$ 记号问的本来就是“$n$ 充分大时形状如何”，不是“$n=100$ 时谁快”。问法一换，答案就跟着换。
>
> 同理可以丢系数：$n^{2}/2$ 与 $n^{2}/3$ 只差一个常数倍，$\Theta$ 记号把它们归为同一类。这与线性代数里分析矩阵幂 $A^{k}$ 只看主导特征值的逻辑同构——主导项决定形状，其余项只决定常数与瞬态。
>
> 两个世界的分工要分清：CSAPP 给你 constant factor（常数因子）的世界（一次访存与一次乘法差几十个周期），Strang 给你结构主导项的世界（特征值、秩、条件数），而 $\Theta$ 记号是后者的极端形式：只留增长阶，连系数也不要。
>
> 一个诚实的提醒：$\Theta$ 记号在 $n$ 很大时才是真理。若你的输入规模固定在 $10^{3}$ 量级，被丢掉的那 2050 项可能正是胜负手，此时应当回到带系数的表达式——也就是第 3 章之前的写法。能否正确切换这两种视角，是“会用记号”与“被记号骗”的分界线。
>
> 收束：信息压缩的代价与收益要一起算。丢掉低阶项与系数，换来一个与机器无关、可比较的结论；这笔交易在 $n\to\infty$ 时稳赚，在 $n$ 固定时可能亏。判断属于哪种情形，正是 analyze（分析）这一步真正在做的事。
>
> 还有容易被忽略的第三层简化：从 $c_i$ 到 $a$、$b$、$c$ 是一次抽象，从 $an^{2}+bn+c$ 到 $\Theta(n^{2})$ 是第二次抽象。两次抽象各有适用边界，混为一谈就会在“要不要保留系数”上犹豫不决。
>
> 一个具体场合：若两个 algorithm（算法）都是 $\Theta(n\log n)$，$\Theta$ 记号已经用尽，你必须回到带系数的表达式去比。merge sort（归并排序）与 heapsort（堆排序）就属于这种情形，胜负由 constant factor（常数因子）与 cache（缓存）行为决定。
>
> 反过来，若两个 algorithm（算法）的阶不同，任何系数比较都没有意义：$1000n^{2}$ 永远追不上 $n^{3}/1000$，只要 $n$ 足够大。先比阶、再比系数，这是选 algorithm（算法）时唯一不会错的次序。
>
> 最后给一条记号纪律：$\Theta$ 是等价类，不是数值。写 $\Theta(n^{2})=\Theta(n^{2})$ 没问题，写 $\Theta(n^{2})\le\Theta(n^{3})$ 就没有意义——不等号在等价类上没有定义。看到 $T(n)=\Theta(n^{2})$ 时，正确读法是“$T$ 属于这个类”，而不是“$T$ 等于某个数”。
>
> 顺带一提：这道题完整的答案还要说明“为什么丢掉系数不影响结论”，那正是第 3 章渐近记号定义所做的事——把“被丢掉的东西有多小”写成一条可检验的不等式。

---

> <span style="color:#7f8c8d;">CLRS §2.2–2.3, p.29</span>

……增长阶数（order of growth）。不过，只要输入足够大，例如一个 $\Theta(n^2)$ 算法在最坏情况下就会比一个 $\Theta(n^3)$ 算法运行得更快。

### Exercises <span style="color:#2471a3;">**[exercise]**</span>

**2.2-1**
Express the function $n^3/1000 - 100n^2 - 100n + 3$ in terms of $\Theta$-notation.

**2.2-2**
Consider sorting $n$ numbers stored in array $A$ by first finding the smallest element of $A$ and exchanging it with the element in $A[1]$. Then find the second smallest element of $A$, and exchange it with $A[2]$. Continue in this manner for the first $n - 1$ elements of $A$. Write pseudocode for this algorithm, which is known as selection sort. What loop invariant does this algorithm maintain? Why does it need to run for only the first $n - 1$ elements, rather than for all $n$ elements? Give the best-case and worst-case running times of selection sort in $\Theta$-notation.

**2.2-3**
Consider linear search again (see Exercise 2.1-3). How many elements of the input sequence need to be checked on the average, assuming that the element being searched for is equally likely to be any element in the array? How about in the worst case? What are the average-case and worst-case running times of linear search in $\Theta$-notation? Justify your answers.

**2.2-4**
How can we modify almost any algorithm to have a good best-case running time?

### Section 2.3 Designing algorithms（设计算法）<span style="color:#2471a3;">**[section]**</span>

我们可以从范围广泛的算法设计技术（algorithm design techniques）中进行选择。对插入排序（insertion sort）而言，我们采用的是增量方法（incremental approach）：在将子数组 $A[1..j-1]$ 排好序之后，我们再把单个元素 $A[j]$ 插入到它的正确位置，从而得到已排序的子数组 $A[1..j]$。

在本节中，我们考察另一种设计方法，即众所周知的 divide-and-conquer（分治法），我们将在第 4 章中对它进行更详细的探讨。我们将用分治法来设计一种排序算法，其最坏情况运行时间（worst-case running time）远小于插入排序。分治法算法的一个优点是，其运行时间常常可以利用我们将在第 4 章中看到的技巧而容易地确定下来。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.30</span>

#### 2.3.1 The divide-and-conquer approach（分治法）<span style="color:#2471a3;">**[section]**</span>

许多有用的算法在结构上是递归的（recursive）：为了求解给定的问题，它们会递归地调用自身一次或多次，以处理密切相关但规模更小的子问题（subproblems）。这些算法通常遵循 divide-and-conquer（分治法）方法：把问题分解为若干个与原问题相似但规模更小的子问题，递归地求解这些子问题，然后把得到的解合并（combine）起来，形成原问题的解。

分治法范式（divide-and-conquer paradigm）在递归的每一层都包含三个步骤：

- **Divide（分解）**：把问题分解为若干个子问题，它们是同一问题的更小实例（smaller instances）。
- **Conquer（解决）**：通过递归地求解来“解决”子问题。不过，如果子问题的规模足够小，就直接以直截了当的方式求解子问题。
- **Combine（合并）**：把子问题的解合并成原问题的解。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把 divide/conquer/combine 记成一个可复用的设计模板，而不只是 merge sort（归并排序）的描述——模板一旦可复用，你就能把它搬到别的问题上。
>
> 模板的受力点有两处。其一，“子问题与原问题相似”保证递归良构——$T(n)$ 的定义里可以合法出现 $T(n/b)$，这是 recurrence（递归式）写得出来的前提。其二，成本核算被模板切成三笔账 $D(n)+aT(n/b)+C(n)$，其中 $D$ 与 $C$ 通常是多项式，递归项是唯一的难点。
>
> 增量法与分治怎么取舍：若“新增一个元素”能借助已有结构以较低代价吸收，incremental approach（增量法）常数小、空间省，insertion sort（插入排序）就是这种形态；若问题能对半劈且合并代价不高于两半之和，divide-and-conquer（分治法）能把你带进更低的增长阶。
>
> 主 theorem（定理）是这三步账的定量结算器：给定 $a$、$b$ 与 $D(n)+C(n)$ 的增长阶，直接读出 $T(n)$ 的阶，不必每次画树。它的标准表述出自 Bentley、Haken 与 Saxe 1980 年发表于 SIGACT News 第 12 卷第 3 期的文章，CLRS 第 4 章把它整理成今天通用的三分情形。
>
> 一个能算出差别的例子：Strassen 矩阵乘法把 $a$ 从 8 降到 7、$b$ 仍为 2，指数从 3 变成 $\log_{2}7\approx2.807$。$n=1024$ 时 $n^{3}=1.07\times10^{9}$，而 $n^{2.807}\approx2.8\times10^{8}$，差 3.8 倍。指数上只少 0.19，规模一大就变成数倍——这是“指数上的小改动能换大收益”的最干净例子。
>
> 三个同类实例摆在一起看更清楚：binary search（二分搜索）是 $a=1$、$b=2$、$C(n)=\Theta(1)$，得 $\Theta(\log n)$；merge sort（归并排序）是 $a=2$、$b=2$、$C(n)=\Theta(n)$，得 $\Theta(n\log n)$；朴素矩阵乘法是 $a=8$、$b=2$、$C(n)=\Theta(n^{2})$，得 $\Theta(n^{3})$。三者的差别全在 $a$、$b$ 与 $C$ 的搭配上，而模板的形状一模一样。
>
> 与 6.042J 的连接：这套“拆—递归—合”的结构，与集合论里做递归定义时“基础情形 + 递归构造”的结构同构。区别在于递归定义关心对象是否合法（造出来的东西属于不属于那个集合），divide-and-conquer（分治法）关心代价如何累加。同一个形状，两种用途。
>
> 收束：看见一个 algorithm（算法）能写成 $D(n)+aT(n/b)+C(n)$，你其实已经拿到了它的增长阶入口；剩下的事只是把 $a$、$b$、$C$ 数清楚，别把模板当结论。
>
> 模板还有一个容易忽略的前提：子问题的“类型”必须与原问题一致。若分解后得到的是另一种问题（比如把排序拆成“找第 k 小”），递归式 $aT(n/b)$ 就写不出来，得换别的方法——这也是好的分解往往保留问题“签名”的原因。
>
> 另一个前提：合并必须从子问题的解出发，不能回头修改子问题。merge sort（归并排序）满足这一点：MERGE 只读 $L$ 与 $R$），而某些原地算法不满足，代价分析就复杂得多。
>
> 最后一点：分治的收益上限由 $a$ 与 $b$ 的比值决定。$a$ 越小、$b$ 越大，指数 $\log_{b}a$ 才越低。这也是 Strassen 死磕“把 8 次乘法降到 7 次”而不在意加法变多的原因——只有乘法次数进指数。
>
> 再补一个模板失效的边界：若 $a$ 或 $b$ 不是常数（例如每次把规模开平方），递归式就超出了主 theorem（定理）的适用范围，得回到递归树或代入法。模板的前提是每层以固定比例缩小；比例一变，结论的形状就变。
>
> 再补一个同族例子，把收益算出来：Karatsuba 大整数乘法把四次子乘法降到三次，a 取三、b 取二，指数变成以二为底三的对数，约一点五八五。规模到一百万位时，平方量级是十的十二次方，而一点五八五次方只有约三点二乘以十的九次方，差三百多倍。指数上更小的差别，在规模上换成更狠的倍数。

归并排序（merge sort）算法密切遵循分治法范式。直观上，它的运作方式如下。

- **Divide（分解）**：把待排序的 $n$ 元素序列分解为两个各含 $n/2$ 个元素的子序列。
- **Conquer（解决）**：用归并排序递归地对这两个子序列排序。
- **Combine（合并）**：合并（merge）两个已排序的子序列，产生已排序的答案。

当待排序的序列长度为 1 时，递归就“触底”（bottoms out）了；此时无需做任何工作，因为每个长度为 1 的序列都已经是已排序顺序（sorted order）的了。

归并排序算法的关键操作，是“合并”（combine）步骤中把两个已排序序列合并（merge）在一起的过程。我们通过调用辅助过程（auxiliary procedure）MERGE(A, p, q, r) 来执行合并，其中 $A$ 是一个数组，$p$、$q$、$r$ 是数组下标，满足 $p \le q < r$。该过程假定子数组 $A[p..q]$ 和 $A[q+1..r]$ 已处于已排序顺序，并把它们合并成一个已排序的子数组，用以替换当前的子数组 $A[p..r]$。

我们的 MERGE 过程花费 $\Theta(n)$ 时间，其中 $n = r - p + 1$ 是被合并的元素总数，它按如下方式工作。回到我们打牌的比喻：假设桌上正面朝上放着两摞牌，每摞都已排好序，最小的牌在最上面。我们希望把这两摞牌合并成单独一摞已排序的输出牌堆，这摞输出牌要正面朝下放在桌上。我们的基本步骤是：选择两摞正面朝上的牌堆顶端两张中较小的一张，把它从所在牌堆中取出（这会翻露出新的顶牌），然后把它正面朝下放到输出牌堆上。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.31</span>

我们重复这一步骤，直到某个输入牌堆为空；此时我们只需把剩下的输入牌堆整摞正面朝下放到输出牌堆上。在计算上，每个基本步骤花费常量时间（constant time），因为我们只需比较两张顶牌。由于我们至多执行 $n$ 个基本步骤，因此合并（merge）花费 $\Theta(n)$ 时间。

下面的伪代码（pseudocode）实现了上述想法，但附加了一个小技巧，从而避免了在每个基本步骤中都要检查某一摞牌是否为空。我们在每摞牌的底部放一张哨兵（sentinel）牌，它包含一个特殊值，我们用这个值来简化代码。这里我们使用 $\infty$ 作为哨兵值，因此无论何时翻出一张值为 $\infty$ 的牌，它都不可能是较小的那张牌，除非两摞牌都翻露出了各自的哨兵牌。不过一旦发生这种情况，所有非哨兵牌就都已经放到了输出牌堆上。因为我们预先知道恰好会有 $r - p + 1$ 张牌被放到输出牌堆上，所以一旦执行了这么多次基本步骤，就可以停下来。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> sentinel（哨兵）是“用存储换分支”的典型交易，值得从第一性原理拆开：它把边界检查从控制流里搬进了数据里。
>
> 不加 sentinel（哨兵）时，合并循环每次迭代都必须回答两个问题：$L$ 空了吗？$R$ 空了吗？两次边界检查在真实处理器上并不免费——分支预测失败一次要十几个周期（见 CSAPP 第 3 章的条件跳转、第 5 章的 pipeline（流水线）），而且让循环体多出两条出口，代码路径翻倍。
>
> 放入 $\infty$ 之后，两个 array（数组）“永远取不完”：$\infty$ 与任何真实元素比较都判负，于是每个非 sentinel（哨兵）元素仍按正确顺序被取走；仅当两堆都只剩 sentinel（哨兵）时才会“取到” $\infty$，而此时循环已经做满 $r-p+1$ 次迭代，靠 for 循环的计数器自然终止。
>
> 两个边界检查就这样被一个数学事实消掉了：$\infty$ 是全序集合中的最大元。代价是每个 array（数组）多一个槽位、多两次赋值——用两格存储，换掉每次迭代的两次比较。
>
> 算一下这笔交易的规模：合并 $n=10^{6}$ 个元素，省下 $2\times10^{6}$ 次边界检查；若其中一半预测失败、每次失败约 17 个周期，就是 $1.7\times10^{7}$ 个周期，按 3 GHz 算约 5.7 毫秒。绝对数不大，但它是白拿的——没有增加任何算法复杂度。
>
> 一个必须守住的细节：$\infty$ 必须是“比任何可能出现的 key（关键字）都大”的标记，而机器上没有真的无穷。真实实现常用“类型最大值”或在比较里加分支，前者在浮点下会撞上 NaN 的坑——NaN 与任何值比较都为假，会让 sentinel（哨兵）判定失效。
>
> 与第 10 章的呼应：同一个思想在 linked list（链表）里重现——NIL sentinel（哨兵）让“空链表”不再是特例，插入与删除都不必先判空。这类“让边界条件自然失效”的技巧在 data structure（数据结构）里反复出现，值得当成一条通用手法记住。
>
> 与 6.042J 的连接：这就是“把 case analysis 转成代数运算”的手法——你不去分类讨论“哪边空了”，而是让比较运算本身自动处理边界。收益不只在速度上，还在于正确性证明里少掉两个分支，证明长度直接减半。
>
> 收束：sentinel（哨兵）不是小聪明，它是一次结构重构：把“检查边界”换成“让边界没有意义”。代价可见、收益可算，这种交易值得养成习惯去识别。
>
> 一个实现层面的取舍：sentinel（哨兵）要求元素类型存在“比所有合法值都大”的表示。整数可以取类型最大值，浮点却可能没有，因为 NaN 的比较语义会让判定失效），字符串则需要额外约定。选 sentinel（哨兵）值之前，先确认这个前提在类型上成立。
>
> 另一条纪律：sentinel（哨兵）是“看不见的数据”，调试时容易被误统计成真实元素，所以打印或统计长度时要显式扣掉它。这类小坑在真实项目里比性能收益更常被踩到。
>
> 一句话收口：sentinel（哨兵）把“检查”从代码搬进数据，代价可见、收益可算，这是重构里最划算的一类交易。
>
> 再给一个失败边界：若 sentinel（哨兵）值可能出现在合法数据里，正确性立刻崩塌。例如用零当 sentinel（哨兵）、而零本身是合法关键字，合并时就会把真实元素当成“取完了”的信号，后半段数据被整段丢弃。选 sentinel（哨兵）值，等于在证明里加一条前置条件：它在数据域之外。这条前置条件没人替你检查，只能靠设计时自己守住。

```
MERGE(A, p, q, r)
 1  n1 = q - p + 1
 2  n2 = r - q
 3  let L[1..n1 + 1] and R[1..n2 + 1] be new arrays
 4  for i = 1 to n1
 5      L[i] = A[p + i - 1]
 6  for j = 1 to n2
 7      R[j] = A[q + j]
 8  L[n1 + 1] = ∞
 9  R[n2 + 1] = ∞
10  i = 1
11  j = 1
12  for k = p to r
13      if L[i] ≤ R[j]
14          A[k] = L[i]
15          i = i + 1
16      else A[k] = R[j]
17          j = j + 1
```

具体来说，MERGE 过程的工作方式如下。第 1 行计算子数组 $A[p..q]$ 的长度 $n_1$，第 2 行计算子数组 $A[q+1..r]$ 的长度 $n_2$。在第 3 行，我们创建长度分别为 $n_1 + 1$ 和 $n_2 + 1$ 的数组 $L$ 和 $R$（“left”（左）和 “right”（右））；每个数组中多出来的那个位置将用来存放哨兵。第 4–5 行的 for 循环把子数组 $A[p..q]$ 复制到 $L[1..n_1]$，第 6–7 行的 for 循环把子数组 $A[q+1..r]$ 复制到 $R[1..n_2]$。第 8–9 行把哨兵放到数组 $L$ 和 $R$ 的末端。第 10–17 行，如图 2.3 所示……

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.32</span>

**Figure 2.3（图 2.3）**：调用 MERGE(A, 9, 12, 16) 时第 10–17 行的运行过程，此时子数组 $A[9..16]$ 包含序列 $\langle 2, 4, 5, 7, 1, 2, 3, 6 \rangle$。在复制并插入哨兵之后，数组 $L$ 包含 $\langle 2, 4, 5, 7, \infty \rangle$，数组 $R$ 包含 $\langle 1, 2, 3, 6, \infty \rangle$。$A$ 中浅色阴影（lightly shaded）的位置包含它们的最终值，而 $L$ 和 $R$ 中浅色阴影的位置包含尚未复制回 $A$ 的值。综合起来，浅色阴影的位置始终构成 $A[9..16]$ 中原来的那些值，连同两个哨兵。$A$ 中深色阴影（heavily shaded）的位置包含将被复制覆盖的值，而 $L$ 和 $R$ 中深色阴影的位置包含已经复制回 $A$ 的值。(a)–(h) 为在第 12–17 行循环每次迭代之前，数组 $A$、$L$、$R$ 以及它们各自的下标 $k$、$i$、$j$ 的状态。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 下表为根据图 2.3 的八个分图重构的状态表（原文只有插图，无此表格），用于逐迭代跟踪第 12–17 行的动作。
>
> 读法先说清：$k$ 是写入位置，$i$ 与 $j$ 是两个 array（数组）的游标，每一行给出的是 for 循环一次迭代“之前”的状态；动作一栏写的是该次迭代把谁写进 $A[k]$，以及哪个游标随后前进。
>
> | 步骤 | $k$ | $i$ | $j$ | $L[i]$ | $R[j]$ | 动作 |
> |------|-----|-----|-----|--------|--------|------|
> | (a) | 9 | 1 | 1 | 2 | 1 | $A[9]\leftarrow1$，$j\leftarrow2$ |
> | (b) | 10 | 1 | 2 | 2 | 2 | $A[10]\leftarrow2$，$i\leftarrow2$ |
> | (c) | 11 | 2 | 2 | 4 | 2 | $A[11]\leftarrow2$，$j\leftarrow3$ |
> | (d) | 12 | 2 | 3 | 4 | 3 | $A[12]\leftarrow3$，$j\leftarrow4$ |
> | (e) | 13 | 2 | 4 | 4 | 6 | $A[13]\leftarrow4$，$i\leftarrow3$ |
> | (f) | 14 | 3 | 4 | 5 | 6 | $A[14]\leftarrow5$，$i\leftarrow4$ |
> | (g) | 15 | 4 | 4 | 7 | 6 | $A[15]\leftarrow6$，$j\leftarrow5$ |
> | (h) | 16 | 4 | 5 | 7 | $\infty$ | $A[16]\leftarrow7$，$i\leftarrow5$ |
>
> 统计一遍：共 8 次迭代，8 个元素每个恰好被写入一次；$i$ 从 1 走到 5、$j$ 从 1 走到 5，合计前进 8 步，与迭代次数相等——因为每次迭代恰好消耗一个元素。最后停在 $(i,j)=(5,5)$，两个游标都指向 sentinel（哨兵），正对应“两个 sentinel（哨兵）是唯一没有被写回的元素”。
>
> 有一处必须对照代码看：第 (b) 行 $L[i]=R[j]=2$ 相等，代码走的是 $L[i]\le R[j]$ 这条分支，取的是 $L$ 里的那个 2。这个选择决定了 merge sort（归并排序）的 stability（稳定性）——相等时先取左边，左边元素就保持在前。若把判定改成严格小于，稳定性立刻丢失，而且从这张表上就能看出来。
>
> 再算一个数：8 个元素、8 次比较，说明 MERGE 的比较次数不超过 $n_1+n_2$，即 $\Theta(n)$。它与逐元素复制的代价同阶，所以合并步骤的 constant factor（常数因子）很小——这也是 merge sort（归并排序）在真实机器上表现稳定的原因之一。
>
> 表里每行都满足的那句话，就是第 33 页的不变式：$A[p..k-1]$ 已按序包含最小的 $k-p$ 个元素，而 $L[i]$ 与 $R[j]$ 分别是各自剩余部分的最小者。把这两句合起来看，你就能明白为什么它被称为复合不变式——它同时说了两个 array（数组）的状态。
>
> 与 insertion sort（插入排序）对比着看更有意思：那边是“逐个插入”的增量视角，每步移动一整段；这边是“两个有序流归并”的视角，每步只写一格。同样是 $\Theta(n)$ 的工作量，形态完全不同，代码复杂度也不同。
>
> 收束：这类表的价值是把“证明”降级成“核对”。八行看完，正确性论证里每一步该拿什么当理由，你都已经亲眼见过一次；剩下的事只是把它按模板写成三段。
>
> 有一处可以自己验证：把八行的 $k$ 值连起来是 9 到 16，正好覆盖 $A[p..r]$ 的八个位置，一个不漏、一个不重。这是“每个元素恰写一次”的直接证据，比任何文字论证都硬。
>
> 另一个观察：$i$ 与 $j$ 从不后退，两者之和从 2 单调增长到 10。这条单调性正是 MERGE 为 $\Theta(n)$ 的结构原因——游标总行程是 $2n$，不会出现重复扫描。
>
> 还能读出稳定性：第 (b) 行相等时取左，第 (c) 行才轮到右，于是左段的 2 落在右段的 2 之前。这张表既是状态记录，也是 stability（稳定性）的证据。
>
> 还有一个细节能对上代码：第 12 行的循环变量 $k$ 从 $p$ 走到 $r$，共 $r-p+1=8$ 次，而表里正好八行。若表多一行或少一行，说明你把“读取哨兵”那一次误算进了循环——那是循环结束之后的动作，不在表内。
>
> 一句话：表里每一行都能在代码里找到对应的三条赋值语句，找不到就说明你看漏了一次迭代。
>
> 还有一个对照：CSAPP 第 3 章讲循环展开时，关心的正是这种“每次迭代做固定几件事”的循环体。表里每行只写一格、比较一次、推进一个游标，正好三件固定工作；循环展开一次写两格，就是把两行合并成一行。看清这一点，你就知道这段代码在编译器优化后为什么能跑到接近内存带宽——它每读一次内存就写一次结果，没有冗余访问。

| 步骤 | $k$ | $i$ | $j$ | $L[i]$ | $R[j]$ | 动作 |
|------|-----|-----|-----|--------|--------|------|
| (a) | 9 | 1 | 1 | 2 | 1 | $A[9] \leftarrow 1$（取自 $R$），$j \leftarrow 2$ |
| (b) | 10 | 1 | 2 | 2 | 2 | $A[10] \leftarrow 2$（取自 $L$），$i \leftarrow 2$ |
| (c) | 11 | 2 | 2 | 4 | 2 | $A[11] \leftarrow 2$（取自 $R$），$j \leftarrow 3$ |
| (d) | 12 | 2 | 3 | 4 | 3 | $A[12] \leftarrow 3$（取自 $R$），$j \leftarrow 4$ |
| (e) | 13 | 2 | 4 | 4 | 6 | $A[13] \leftarrow 4$（取自 $L$），$i \leftarrow 3$ |
| (f) | 14 | 3 | 4 | 5 | 6 | $A[14] \leftarrow 5$（取自 $L$），$i \leftarrow 4$ |
| (g) | 15 | 4 | 4 | 7 | 6 | $A[15] \leftarrow 6$（取自 $R$），$j \leftarrow 5$ |
| (h) | 16 | 4 | 5 | 7 | $\infty$ | $A[16] \leftarrow 7$（取自 $L$），$i \leftarrow 5$ |

……即第 10–17 行执行 $r - p + 1$ 个基本步骤，同时维持下面的循环不变式（loop invariant）：

> <span style="color:#00838f;">**循环不变式（loop invariant）**：在第 12–17 行 for 循环的每次迭代开始时，子数组 $A[p..k-1]$ 按已排序顺序包含 $L[1..n_1+1]$ 和 $R[1..n_2+1]$ 中最小的 $k - p$ 个元素。此外，$L[i]$ 和 $R[j]$ 分别是各自数组中尚未复制回 $A$ 的最小元素。</span>

我们必须证明：该循环不变式在第 12–17 行 for 循环的第一次迭代之前成立，循环的每次迭代都维持该不变式，并且当循环终止时，该不变式能提供一个有用的性质来证明正确性（correctness）。

> **Initialization（初始化）**：在循环的第一次迭代之前，我们有 $k = p$，因此子数组 $A[p..k-1]$ 为空。这个空子数组包含 $L$ 和 $R$ 中最小的 $k - p = 0$ 个元素，并且由于 $i = j = 1$，$L[i]$ 和 $R[j]$ 都是各自数组中尚未复制回 $A$ 的最小元素。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.33</span>

**Figure 2.3, continued（图 2.3 续）**：(i) 终止时数组与下标的状态。此时 $A[9..16]$ 中的子数组已经排好序，而 $L$ 和 $R$ 中的两个哨兵，是这两个数组中仅有的尚未复制到 $A$ 中的两个元素。

> **Maintenance（保持）**：要看出每次迭代都维持循环不变式，我们首先假定 $L[i] \le R[j]$。那么 $L[i]$ 就是尚未复制回 $A$ 的最小元素。由于 $A[p..k-1]$ 包含最小的 $k - p$ 个元素，所以在第 14 行把 $L[i]$ 复制到 $A[k]$ 之后，子数组 $A[p..k]$ 将包含最小的 $k - p + 1$ 个元素。将 $k$ 递增（在 for 循环的更新中）并将 $i$ 递增（在第 15 行），就为下一次迭代重新建立了循环不变式。反之，如果 $L[i] > R[j]$，那么第 16–17 行会执行适当的动作来维持循环不变式。

> **Termination（终止）**：终止时 $k = r + 1$。根据循环不变式，子数组 $A[p..k-1]$（即 $A[p..r]$）按已排序顺序包含 $L[1..n_1+1]$ 和 $R[1..n_2+1]$ 中最小的 $k - p = r - p + 1$ 个元素。数组 $L$ 和 $R$ 合起来包含 $n_1 + n_2 + 2 = r - p + 3$ 个元素。除了两个最大的元素之外，其余都已被复制回 $A$，而这两个最大的元素正是哨兵。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这份证明复用了第 19 页的「循环不变式论证」模板。要看到的不只是“又证了一遍”，而是模板的可移植性——换掉命题，方法一字不改。
>
> 起跳：Initialization（初始化）用“$k=p$ 时 $A[p..k-1]$ 为空、含最小的 0 个元素”作为 base case（基例）。注意“含 0 个元素”不算废话——它把“空”与“最小的 0 个”接上了，归纳才能从这里接出去；否则你只能说“什么都没做”，推不动下一步。
>
> 保持：Maintenance（保持）分 $L[i]\le R[j]$ 与 $L[i]>R[j]$ 两个对称分支各自推进。左分支：$L[i]$ 是尚未复制的最小元素，复制到 $A[k]$ 后前缀含最小的 $k-p+1$ 个，再把 $i$ 与 $k$ 各加 1，不变量重建；右分支完全对称，无需重写论证，只需写“同理”。
>
> 终止：Termination（终止）把 $k=r+1$ 代回，得 $A[p..r]$ 已按序含最小的 $r-p+1$ 个元素。再算一次元素数：$n_1+n_2+2=(q-p+1)+(r-q)+2=r-p+3$，其中 $r-p+1$ 个已写回，剩下两个正是 sentinel（哨兵）。这一步把“剩下的只有哨兵”从直觉变成算术。
>
> 装进骨架的变量换了：从“数组前缀是否有序”换成“$A[p..k-1]$ 是否恰含最小的 $k-p$ 个元素”，而三段式的结构、每段要回答的问题，一个字都没改。这就是模板的可移植性——你换的是命题，不是方法。
>
> 这里的不变式比 insertion sort（插入排序）的更强：它同时约束“已复制部分”与“两个游标所指元素”，是复合不变式。设计不变式的诀窍，是让它恰好覆盖终止时你要用的全部信息，不多不少。
>
> 一个反例说明“不多不少”有多重要：若只写前半句（前缀含最小的那些），终止时你无法排除“剩余元素被悄悄扔掉”的可能；只有再加上“两个游标指向各自剩余部分的最小者”，才能推出“剩下的两个必然是 sentinel（哨兵）”。少一条约束，结论就悬空。
>
> 与 6.042J 的连接：这与归纳证明里“加强归纳假设”是同一个动作——想推出更强的结论，就得假设更强的命题。区别在于这里是“设计”不变式（你可以自定义），而不是“发现”一个已给定的定理。
>
> 收束：CLRS 在小 algorithm（算法）上反复演练三段式，正如你在 6.042J 先把归纳练成肌肉记忆、再去证图论与数论的命题——练的从来不是题目，是骨架。
>
> 还有一个细节值得核对：终止那一步要用到“$L$ 与 $R$ 合起来有 $n_1+n_2+2$ 个元素”，而 $n_1+n_2=r-p+1$。也就是说，源子数组恰好有 $r-p+1$ 个真实元素，加上两个 sentinel（哨兵），正好比写回的多两个。这两格差，就是“sentinel（哨兵）没有被复制”的全部内容。
>
> 再说清“复合”二字的代价：不变式里每多一个合取项，初始化就要多验一项、保持就要多推一项。所以设计时要问：这一项在终止时真被用到吗？用不到就删掉，用得到就留着——这是唯一标准，而不是越强越好。
>
> 最后一句：这套证明读完之后，你应当能在不看原文的情况下把三段重新写一遍，并且每一步都说得出理由；做到了，才算真把模板搬走，而不只是读过。
>
> 再补一个反例，说明强度不够会导致什么：若把不变式写成“前缀长度等于 k 减 p”，它当然每轮都成立，却完全不含顺序信息，终止时只能得到“长度为 r 减 p 加一”，推不出有序。可见不变式必须约束内容，不能只约束规模。这条判据对写代码断言同样适用：只检查长度的断言，抓不到真实故障。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.34</span>

要看出 MERGE 过程在 $\Theta(n)$ 时间内运行（其中 $n = r - p + 1$），请注意第 1–3 行和第 8–11 行各自都花费常量时间，第 4–7 行的 for 循环花费 $\Theta(n_1 + n_2) = \Theta(n)$ 时间，7 而第 12–17 行的 for 循环有 $n$ 次迭代，每次迭代花费常量时间。

> <span style="color:#7f8c8d;">脚注 7：</span>我们将在第 3 章中看到如何形式化地解释包含 $\Theta$-记号的方程。

现在我们可以把 MERGE 过程作为子过程（subroutine）用在归并排序算法中。过程 MERGE-SORT(A, p, r) 对子数组 $A[p..r]$ 中的元素排序。如果 $p \ge r$，该子数组至多有一个元素，因此已经排好序。否则，分解（divide）步骤只需计算一个把 $A[p..r]$ 划分成两个子数组的下标 $q$：$A[p..q]$ 包含 $\lceil n/2 \rceil$ 个元素，$A[q+1..r]$ 包含 $\lfloor n/2 \rfloor$ 个元素。8

```
MERGE-SORT(A, p, r)
 1  if p < r
 2      q = ⌊(p + r)/2⌋
 3      MERGE-SORT(A, p, q)
 4      MERGE-SORT(A, q + 1, r)
 5      MERGE(A, p, q, r)
```

> <span style="color:#7f8c8d;">脚注 8：</span>表达式 $\lceil x \rceil$ 表示大于或等于 $x$ 的最小整数，$\lfloor x \rfloor$ 表示小于或等于 $x$ 的最大整数。这些记号在第 3 章中定义。验证把 $q$ 设为 $\lfloor (p+r)/2 \rfloor$ 会分别得到大小为 $\lceil n/2 \rceil$ 和 $\lfloor n/2 \rfloor$ 的子数组 $A[p..q]$ 与 $A[q+1..r]$ 的最简便方法，是考察由 $p$ 和 $r$ 各自为奇数或偶数所产生的四种情形。

要对整个序列 $A = \langle A[1], A[2], \ldots, A[n] \rangle$ 排序，我们做出初始调用 MERGE-SORT(A, 1, A.length)，其中同样有 $A.length = n$。图 2.4 说明了当 $n$ 是 2 的幂时该过程自底向上（bottom-up）的运行方式。算法包含：合并若干对长度为 1 的项序列，形成长度为 2 的已排序序列；合并若干对长度为 2 的序列，形成长度为 4 的已排序序列；如此继续下去，直到合并两个长度为 $n/2$ 的序列，形成长度为 $n$ 的最终已排序序列。

#### 2.3.2 Analyzing divide-and-conquer algorithms（分析分治法算法）<span style="color:#2471a3;">**[section]**</span>

当一个算法包含对自身的递归调用时，我们常常可以用一个递归方程（recurrence equation）或递归式（recurrence）来描述其运行时间，该递归式用较小输入上的运行时间来描述规模为 $n$ 的问题上的总体运行时间。然后我们就可以利用数学工具来求解这个递归式，并为算法的性能提供界。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.35</span>

**Figure 2.4（图 2.4）**：归并排序（merge sort）在数组 $A = \langle 5, 2, 4, 7, 1, 3, 2, 6 \rangle$ 上的运行过程。随着算法自底向上推进，被合并的已排序序列（sorted sequences）的长度不断增大。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 图 2.4 的读法是自底向上：底部是初始序列，每向上一层就把相邻的两段有序序列合并一次，顶部得到完整的有序序列。
>
> 用 8 个元素走一遍，层次就清楚了：
>
> | 层 | 序列 |
> |----|------|
> | 第 0 层 | 5 / 2 / 4 / 7 / 1 / 3 / 2 / 6 |
> | 第 1 层 | 2,5 / 4,7 / 1,3 / 2,6 |
> | 第 2 层 | 2,4,5,7 / 1,2,3,6 |
> | 第 3 层 | 1,2,2,3,4,5,6,7 |
>
> 层数与代价：8 个元素共 $\log_{2}8=3$ 层合并，加上底下第 0 层，一共 4 层。每一层合并的总工作量都是 $\Theta(n)$——每个元素被搬动一次——所以总代价是 $\Theta(n\log n)$。这张图其实就是recursion tree（递归树）换了一个方向画。
>
> 自底向上与自顶向下是同一棵树。递归版 MERGE-SORT 先在调用栈上“往下走到叶子”，再在回程里合并；图 2.4 把回程画在前、去程隐去，于是看起来像自底向上。两者的合并顺序完全一致，只是执行时机不同。
>
> 一个可核对的细节：第 2 层右边那一组的首元素是 1，所以最终结果开头是 1 而不是 2。很多人凭直觉以为“最小值 2 会先出来”，但 1 在右半部分，必须先合并到第 2 层才能露头——这正好说明“有序性只在段内成立，段间要等合并”。
>
> 为什么这一层层合并是稳定的：所有合并都在相邻两段之间进行，且在相等时先取左段元素，所以相等元素的相对次序从不被打乱。图 2.4 里两个 2 的相对位置（第 1 位的 2 在最后一位的 2 之前）自始至终没变。
>
> 与 cache（缓存）的连接：自底向上的实现可以完全用循环写出，不需要递归栈，也不需要额外的 $\Theta(\log n)$ 栈空间；它在 array（数组）上的访问模式更连续，对 CSAPP 第 6 章的 cache（缓存）更友好。这是“同一个 algorithm（算法）、两种实现”在常数因子上的差异。
>
> 与 6.042J 的连接：这棵树与图论里的 binary tree（二叉树）同构：叶子是 $n$ 个元素，内部节点是 $n-1$ 次合并，节点总数 $2n-1$。$n=8$ 时是 15 个节点，正好等于 8 个叶加 7 次合并。
>
> 收束：看图 2.4 只需抓住一件事——每层都把两个有序段变成一个有序段，段数减半、段长加倍；层数是对数，层内代价是线性，乘起来就是答案。
>
> 还有一个可以自己动手的校验：把第一层的四组按顺序连起来，得到 2,5,4,7,1,3,2,6，正好是原始序列的一个重排。这说明每层只改变分组方式，不改变元素集合——守恒量在每一层都成立，这也是为什么可以在纸上用一张表核对整棵树。
>
> 另一个角度：图 2.4 的每一层都可以并行执行，因为层内各段互不相交。这正是 merge sort（归并排序）容易并行化的结构原因，也是它在多核机器上表现稳定的基础。
>
> 最后一层观察：第 3 层合并的两个输入长度各为 4，输出长度 8；每次合并的输出长度等于两个输入之和。这条长度守恒，就是 $n_1+n_2$ 那个式子的图形版本。
>
> 记住这张图只需一句话：段数每层减半，段长每层加倍，层数是对数；乘起来就是总代价。
>
> 再算一个能核对的界：八元素时，最后那次合并最多比较七次，两次四元素合并各最多三次，四次二元素合并各最多一次，合计上界十七次，正好等于 n 乘 lg n 再减 n 加一。这条式子说明合并的总比较次数比“每层 n 次”还省——因为每层最后一次比较总可以省掉，一段先耗尽，剩下的整段直接搬。

分治法算法运行时间的递归式，来自基本范式的三个步骤。和以前一样，我们令 $T(n)$ 为规模为 $n$ 的问题上的运行时间。如果问题的规模足够小，例如对某个常量 $c$ 有 $n \le c$，那么直接求解花费常量时间，我们将其记作 $\Theta(1)$。假设我们把问题分解为 $a$ 个子问题，每个子问题的规模都是原问题的 $1/b$。（对归并排序而言，$a$ 和 $b$ 都等于 2，但我们会看到许多 $a \ne b$ 的分治法算法。）求解一个规模为 $n/b$ 的子问题需要时间 $T(n/b)$，因此求解 $a$ 个子问题需要时间 $aT(n/b)$。如果分解（divide）问题成子问题需要 $D(n)$ 时间，把子问题的解合并成原问题的解需要 $C(n)$ 时间，我们就得到递归式

```math
T(n) =
\begin{cases}
\Theta(1) & \text{if } n \le c, \\
aT(n/b) + D(n) + C(n) & \text{otherwise}.
\end{cases}
```

在第 4 章中，我们将看到如何求解这种形式的常见递归式。

#### Analysis of merge sort（归并排序的分析）<span style="color:#2471a3;">**[section]**</span>

尽管当元素个数不是偶数时，MERGE-SORT 的伪代码也能正确运行，但如果我们假定原问题的规模是 2 的幂，我们基于递归式的分析就可以简化。那样的话，每个分解步骤都会产生两个规模恰好为 $n/2$ 的子序列。在第 4 章中我们将看到，这一假定并不影响递归式解的增长阶数（order of growth）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> “假定 $n$ 是 2 的幂”是算法分析里的标准便利手法，值得记下它为什么合法——合法的理由是一条夹逼，而不是一条约定。
>
> 直觉先说：非 2 次幂的输入只是让递归树最后一层“缺几块”，树高仍是约 $\lg n$，每层代价仍不超过 $cn$，于是界被夹在相邻两个 2 次幂的界之间，相差至多常数倍。而 $\Theta$ 记号恰好对常数倍不敏感——这就是它合法的全部原因。
>
> 把夹逼写实一次：设 $2^{k-1}<n\le2^{k}$，则 $\lg n$ 落在 $(k-1,k]$。由单调性有 $T(n)\le T(2^{k})$，而 $T(2^{k})=\Theta(2^{k}\lg2^{k})=\Theta(2^{k}k)$；又因为 $2^{k}<2n$ 且 $k\le\lg n+1$，所以 $T(2^{k})=O(n\lg n)$。下界一侧同理，用 $2^{k-1}\ge n/2$ 得 $\Omega(n\lg n)$。上下合起来就是 $\Theta(n\lg n)$。
>
> 一个具体数字感受误差：$n=1000$ 夹在 $2^{9}=512$ 与 $2^{10}=1024$ 之间，$\lg1000\approx9.97$。用 $n=1024$ 的结论去估 1000，偏差只来自 $\lg$ 的 0.03 与常数倍，量级上不到千分之三，完全可以接受。
>
> 这类手法有通用名字：先证好证的稠密子列（$n=2^{k}$），再向一般 $n$ 扩张。它与实分析里“先在整数上证明、再延拓到实数”的思路同源，区别在于这里的扩张靠单调性与常数倍夹逼，而不是靠极限与稠密性。
>
> 诚实态度也要有：便利假设同样要核对边界。脚注 8 用四种奇偶情形枚举来验证把 $q$ 取成 $\lfloor(p+r)/2\rfloor$ 时，两段大小恰好是 $\lceil n/2\rceil$ 与 $\lfloor n/2\rfloor$。$n$ 的奇偶与 $p$ 的奇偶组合起来共四种，逐一验证并不难，但它把“想当然”变成了“已核对”。
>
> 什么时候不能这么做：若 algorithm（算法）对规模敏感（例如要求两段严格相等才正确），或者你要的是精确常数而不是增长阶，这个假设就不再免费。判断标准只有一条——$\Theta$ 结论是否够用。
>
> 与 CSAPP 的连接：这类“先算好算的情形、再补一般情形”的做法，在 CSAPP 的性能测量里对应“先在理想输入上测、再补最坏输入”。区别在于那边你必须报告最坏情况，不能只报理想值，否则结论会被反例推翻。
>
> 收束：以后看到“为简化设 $n$ 为 2 的幂”不必过度警惕，但要能当场说出补偿论证在哪——单调性、常数倍夹逼、$\Theta$ 对常数不敏感，三件缺一不可。
>
> 还可以从另一个方向理解：$\Theta$ 是一族函数的等价类，而“只对 2 的幂证明”只是在这个类的一个无界子集上取了样本。只要子集无界（$2^{k}\to\infty$）且族内单调，样本上的结论就能推广到全族；无界性正是关键。
>
> 反过来，若只在有界子集上验证（例如只测到 $n\le1024$），“测试通过”就推不出“永远正确”——这正是测试与证明的分界：样本集无界，归纳才成立。
>
> 一个实用推论：写报告时若为了简化而假设 $n=2^{k}$，最好在脚注里补一行补偿论证。那一行往往就是“单调性加上 $2^{k}<2n$”，成本极低，却能让结论站得住。
>
> 一个反面教材：若把假设换成“$n$ 是 3 的幂”，结论同样成立，因为 3 的幂也构成无界子列；真正不能用的是“$n$ 有界”或“$n$ 只取某几个特定值”，那时样本覆盖不了全族，推广就断了。
>
> 再补一条 6.042J 的连接：把“只对二的幂成立”推广到一般 n，用的正是强归纳的骨架——先证基数情形，再假设所有更小的情形成立，最后把 n 夹在它两侧的二次幂之间。区别在于这里不是沿自然数逐格走，而是沿“夹进相邻二次幂”这一步跳。学会这种跳法，你就能读懂任何“先假设整齐情形”的证明。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.36</span>

我们按如下方式推理，来建立 $T(n)$ 的递归式，其中 $T(n)$ 是归并排序在 $n$ 个数上的最坏情况运行时间（worst-case running time）。对仅仅一个元素做归并排序花费常量时间。当有 $n > 1$ 个元素时，我们按如下方式分解运行时间。

- **Divide（分解）**：分解步骤只是计算子数组的中间位置，这花费常量时间。因此 $D(n) = \Theta(1)$。
- **Conquer（解决）**：我们递归地求解两个子问题，每个的规模为 $n/2$，这对运行时间的贡献为 $2T(n/2)$。
- **Combine（合并）**：我们已经注意到，MERGE 过程在 $n$ 元素子数组上花费 $\Theta(n)$ 时间，因此 $C(n) = \Theta(n)$。

当我们在归并排序的分析中把函数 $D(n)$ 和 $C(n)$ 相加时，我们是在把一个 $\Theta(n)$ 函数和一个 $\Theta(1)$ 函数相加。这个和是 $n$ 的线性函数（linear function），即 $\Theta(n)$。把它与来自“解决”（conquer）步骤的 $2T(n/2)$ 项相加，就得到归并排序最坏情况运行时间 $T(n)$ 的递归式：

```math
T(n) =
\begin{cases}
\Theta(1) & \text{if } n = 1, \\
2T(n/2) + \Theta(n) & \text{if } n > 1.
\end{cases}
\tag{2.1}
```

在第 4 章中，我们将看到“主定理”（master theorem），可以用它来说明 $T(n)$ 是 $\Theta(n \lg n)$，其中 $\lg n$ 表示 $\log_2 n$。由于对数函数增长得比任何线性函数都慢，因此对足够大的输入，运行时间为 $\Theta(n \lg n)$ 的归并排序，在最坏情况下胜过运行时间为 $\Theta(n^2)$ 的插入排序。

我们并不需要主定理，也能直观地理解为什么递归式 (2.1) 的解是 $T(n) = \Theta(n \lg n)$。让我们把递归式 (2.1) 改写成

```math
T(n) =
\begin{cases}
c & \text{if } n = 1, \\
2T(n/2) + cn & \text{if } n > 1,
\end{cases}
\tag{2.2}
```

其中常量 $c$ 表示求解规模为 1 的问题所需的时间，也代表分解和合并步骤中每个数组元素所需的时间。9

> <span style="color:#7f8c8d;">脚注 9：</span>同一个常量不太可能精确地既表示求解规模为 1 的问题所需的时间，又表示分解与合并步骤中每个数组元素所需的时间。我们可以通过令 $c$ 为这两者中较大的那个，并理解我们的递归式给出运行时间的一个上界（upper bound）；或者令 $c$ 为两者中较小的那个，并理解我们的递归式给出运行时间的一个下界（lower bound），来绕开这一问题。两个界都在 $n \lg n$ 这一量级上，合在一起就给出 $\Theta(n \lg n)$ 的运行时间。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 递归式 (2.2) 不是天上掉下来的，它是分治三步账本逐项过账的结果——每一笔都能说清来源。
>
> 逐项过账：$D(n)=\Theta(1)$ 来自“算中间点只需一次下标运算与一次下取整”；$2T(n/2)$ 来自“递归调用两次、每次规模减半”；$C(n)=\Theta(n)$ 来自 MERGE 的逐元素扫描。三项相加时，$D$ 被 $C$ 吞掉，于是只剩 $2T(n/2)+\Theta(n)$——这就是 (2.1) 的来源。
>
> 最值得建立的直觉是“每层合计 $cn$”：子问题个数变多但每个变小，两个效应恰好抵消——4 个 $T(n/4)$ 的合并代价是 $4\times c(n/4)=cn$，8 个 $T(n/8)$ 亦然。这不是巧合，而是“对半分、线性合并”的结构不变量。
>
> 把它讲成不变量而不是巧合：每层分摊的元素总量恒为 $n$ 个，每个元素在每层恰好被扫描一次，所以每层成本锁定为 $cn$。元素总数守恒，才是这条结论的根；一旦合并代价变成 $\Theta(n^{2})$，每层成本就会随层数增长，整个推导立刻失效。
>
> 于是总时间等于 $cn$ 乘层数，问题坍缩成一问：树有多高？规模每层除以 2，到 1 为止，所以是 $\lg n$ 层再加上叶子那一层，共 $\lg n+1$ 层。
>
> 具体数值：$n=1024$ 时 $\lg n=10$，总代价 $11cn$；$n=10^{6}$ 时 $\lg n\approx19.93$，总代价约 $20.93cn$。规模涨了近一千倍，层数只从 11 涨到 21——这就是对数的形状，也是它值得被单独记一记的原因。
>
> 脚注 9 的方法论值得细读：同一个常数不可能既精确表示“规模 1 的代价”，又表示“分解与合并时每个元素的分摊代价”。解法是让它分别取上界与下界，递归式随之给出上界与下界，两个界都在 $n\lg n$ 量级，合起来就是 $\Theta(n\lg n)$。这是“把不精确的模型变成夹逼工具”的标准动作。
>
> 与 6.042J 的连接：这里是等差求和与几何级数的组合应用。区别在于递归树不是让你硬求和，而是让你发现“每层同值”这个更强的结构，求和因此退化为一次乘法——结构替代了计算。
>
> 收束：递归式不是背下来的，是过账过出来的。能重做这三笔账（分解、递归、合并），你就永远不需要记 (2.2) 的具体形式。
>
> 还有一个可以自己算的对照：若合并代价是 $\Theta(n^{2})$，递归式变成 $2T(n/2)+\Theta(n^{2})$，层和变成 $n^{2},n^{2}/2,\ldots$，总和不超过 $2n^{2}$，答案由根主导。同样是“层和乘层数”，形状完全不同——说明“每层同值”是特例，不是通例。
>
> 另一个细节：$T(1)=c$ 这个 base case（基例）不能省。代进树里看，叶子层有 $n$ 个节点、每个代价 $c$，合计 $cn$，正好接上倒数第二层的层和——层和从根到叶恒为 $cn$，靠的就是这条基例。
>
> 这条“接得上”不是巧合：它等价于 $c\cdot n=c(n/2)\cdot2$，也就是函数 $n$ 的线性性。换成 $n^{2}$ 就接不上，层和才会逐层递减。
>
> 再补一个常被忽略的对照：递归式的解并不唯一，它是一族函数，$\Theta$ 只是把这一族压成一个等价类。所以“解出 (2.2)”的准确说法是“求出它所属的等价类”，而不是“求出唯一的 $T$”。
>
> 再落到机器上：常数 c 在真实机器上不是抽象符号，它对应每次合并把左右两段各读一遍、把结果写回一遍，也就是三趟访存。规模到一千万时，三趟访存乘上十九层，约等于每元素五百多次访存，这个数直接决定它在真实机器上要不要做缓存分块。公式给形状，机器给系数，两者都要，但顺序不能反。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.37</span>

### Section 2.3 Designing algorithms（设计算法）· 续 <span style="color:#2471a3;">**[section]**</span>

图 2.5（Figure 2.5）展示了如何求解递归式（recurrence）(2.2)。为方便起见，我们假设 $n$ 是 2 的精确幂次（exact power of 2）。图的 (a) 部分给出 $T(n)$，我们在 (b) 部分将其展开（expand）为一棵等价于该递归式的树。$cn$ 项是根（root），即递归顶层（top level of recursion）所付出的代价；根的两棵子树（subtree）分别是两个更小的递归式 $T(n/2)$。(c) 部分通过展开 $T(n/2)$ 把这个过程又推进了一步。递归第二层的两个子节点各自付出的代价为 $cn/2$。我们继续展开树中的每个节点，按递归式的决定把它分解为相应的组成部分，直到问题规模缩小到 1，每个规模为 1 的问题代价为 $c$。(d) 部分给出了最终得到的递归树（recursion tree）。

接下来，我们把树中每一层（level）的代价相加。最顶层的总代价为 $cn$；往下第二层的总代价为 $c(n/2) + c(n/2) = cn$；再往下一层的总代价为 $c(n/4) + c(n/4) + c(n/4) + c(n/4) = cn$，依此类推。一般地，顶层以下的第 $i$ 层有 $2^i$ 个节点，每个节点贡献代价 $c(n/2^i)$，因此顶层以下第 $i$ 层的总代价为 $2^i \cdot c(n/2^i) = cn$。最底层有 $n$ 个节点，每个节点贡献代价 $c$，总代价为 $cn$。

图 2.5 中递归树的总层数为 $\lg n + 1$，其中 $n$ 是叶子的数目，对应于输入规模（input size）。一个非正式的归纳论证（inductive argument）可以证明这一论断。基本情况（base case）出现在 $n = 1$ 时，此时树只有一层。由于 $\lg 1 = 0$，我们有 $\lg n + 1$ 给出了正确的层数。现在作为归纳假设（inductive hypothesis），假定具有 $2^i$ 片叶子的递归树的层数为 $\lg 2^i + 1 = i + 1$（因为对任何 $i$ 值，都有 $\lg 2^i = i$）。由于我们假设输入规模是 2 的幂，接下来要考虑的输入规模是 $2^{i+1}$。一棵具有 $n = 2^{i+1}$ 片叶子的树，比具有 $2^i$ 片叶子的树多一层，因此总层数为 $(i+1) + 1 = \lg 2^{i+1} + 1$。

为了计算递归式 (2.2) 所表示的总代价，我们只需把各层的代价全部加起来。递归树有 $\lg n + 1$ 层，每层代价为 $cn$，总代价为 $cn(\lg n + 1) = cn\lg n + cn$。忽略低阶项（low-order term）和常数 $c$，就得到想要的结果 $\Theta(n\lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把上面的过程命名为「递归树求和」模板，它有固定的四步，四步的顺序不能颠倒。
>
> 四步是：① 把递归式逐层展开成树，节点值等于该处的非递归代价；② 求每层节点之和，寻找层和的模式；③ 求树高——规模按 $1/b$ 衰减、到常数截止，故高为 $\log_{b}n$；④ 总代价等于层和乘层数。
>
> 本例对号入座：节点值 $cn$、层和恒为 $cn$、高为 $\lg n$ 再加叶子一层、总代价 $cn(\lg n+1)$。四步走完，答案就在纸上，不需要任何记忆。
>
> 模板的能力远不止本例。第一个变体 $T(n)=T(n/3)+T(2n/3)+cn$：层和仍约 $cn$，但树高由衰减最慢的那条路径决定，即 $2/3$ 那条，于是高为 $\log_{3/2}n$。$n=10^{6}$ 时 $\log_{3/2}10^{6}\approx34.1$，总代价约 $34cn$——比归并排序多，但仍是 $n\log n$ 量级。
>
> 第二个变体 $T(n)=2T(n/2)+n^{2}$：层和变成等比数列 $n^{2},n^{2}/2,n^{2}/4,\ldots$，总和不超过 $2n^{2}$，于是总代价由根节点主导。这正是 6.042J 里几何级数“首项主导”的现象——公比小于 1 时，和不超过首项的两倍。
>
> 由此得到三条判据：层和不变（如 $cn$）就乘层数；层和等比递减就由根主导；层和等比递增就由叶子主导（答案是叶子数乘叶子代价）。三条判据覆盖绝大多数分治递归式，主 theorem（定理）的三分情形其实就是它们的代数化。
>
> 方法论一句：拿到任何分治递归式，先画三层树找层和模式，别急着套主 theorem（定理）。结论往往能被你亲手“看”出来；看出来了再套公式，就不容易把情形记混。
>
> 与 CSAPP 的连接：递归树是调用图的一种特殊形态。CSAPP 第 3 章讲过程调用时画的栈帧增长图，与这里的树是同一件事的两个投影——一个是空间账，一个是时间账。
>
> 收束：模板的真正价值在于它给出了可执行的动作序列——展开、求和、求高、相乘。四个动作，任何分治递归式都能上手，不需要灵感。
>
> 还有一个常被问的问题：树高为什么取最慢衰减的那条路径，而不是最快的？因为总代价由最深的叶子决定，而最深的叶子来自衰减最慢的那一支。$T(n/3)+T(2n/3)$ 里 $2/3$ 那一支最深，所以高是 $\log_{3/2}n$。
>
> 另一个细节：这个变体的层和并不严格等于 $cn$——树不是满的，某些层的节点数略少于理论值。但上界一侧每层仍不超过 $cn$，所以 $O(n\log n)$ 成立；要精确常数得做更细的记账，$\Theta$ 结论不受影响。
>
> 第三个提醒：递归树的叶子不总在同一层。只有当所有分支以相同比例衰减（如 $2T(n/2)$）时树才齐平；结构一旦不对称，就要按最深路径算高、按最宽层算和，两件事分开取。
>
> 顺带说一句：递归树还能给出比主 theorem（定理）更强的信息——每层的代价形状。这在优化实现时很有用：若某一层特别贵，你就知道瓶颈在合并而不在递归。
>
> 这也是为什么很多人先画树、再套公式：树给你结构，公式只给你答案。
>
> 再补一个叶子主导的算例，把三种形态凑齐：若规模每层减半、子问题数变成四倍，那么第 i 层的总代价是 n 乘以二的 i 次方，层和逐层翻倍，最后叶子那一层有 n 的平方个节点，总代价由叶子决定，答案就是 n 的平方。层和不变、递减、递增这三种形态到这里就全了，遇到任何递归式先判断它属于哪一种，剩下的只是套用。

### Exercises <span style="color:#2471a3;">**[exercise]**</span>

**2.3-1**
Using Figure 2.4 as a model, illustrate the operation of merge sort on the array $A = \langle 3, 41, 52, 26, 38, 57, 9, 49\rangle$.

**2.3-2**
Rewrite the MERGE procedure so that it does not use sentinels, instead stopping once either array $L$ or $R$ has had all its elements copied back to $A$ and then copying the remainder of the other array back into $A$.

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.38</span>

> <span style="color:#7f8c8d;">本页为整页插图页，无正文文字，仅含图 2.5（Figure 2.5）。下图为递归树（recursion tree）的结构示意，其后给出该图的中英双语图注。</span>

### Figure 2.5（图 2.5）

**图注：** 图 2.5（Figure 2.5）：如何为递归式 $T(n) = 2T(n/2) + cn$ 构造一棵递归树。(a) 部分给出 $T(n)$，它依次在 (b)–(d) 中逐步展开（expand），最终形成递归树。(d) 中完全展开的树有 $\lg n + 1$ 层（即高度（height）为 $\lg n$，如图所示），每一层贡献的总代价（total cost）为 $cn$。因此总代价为 $cn\lg n + cn$，即 $\Theta(n\lg n)$。

**图中各层代价示意：**（下方的 ASCII 递归树为译者自绘增补，原文仅一张插图；各层数值与图 2.5 一致）

```text
                  cn                     ← 第 0 层（顶层）：总代价 cn
               /      \
           cn/2        cn/2              ← 第 1 层：2 × (cn/2) = cn
          /    \       /    \
        cn/4  cn/4   cn/4  cn/4          ← 第 2 层：4 × (cn/4) = cn
         ⋮     ⋮      ⋮     ⋮
          c     c      c     c           ← 第 lg n 层：n × c = cn
```

共 $\lg n + 1$ 层，每层总代价均为 $cn$，故总代价 $= cn(\lg n + 1) = cn\lg n + cn = \Theta(n\lg n)$。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.39</span>

### Exercises <span style="color:#2471a3;">**[exercise]**</span>（续）

**2.3-3**
Use mathematical induction to show that when $n$ is an exact power of 2, the solution of the recurrence

```math
T(n) =
\begin{cases}
2 & \text{if } n = 2,\\
2T(n/2) + n & \text{if } n = 2^k,\ \text{for } k > 1,
\end{cases}
```

is $T(n) = n\lg n$.

**2.3-4**
We can express insertion sort as a recursive procedure as follows. In order to sort $A[1..n]$, we recursively sort $A[1..n-1]$ and then insert $A[n]$ into the sorted array $A[1..n-1]$. Write a recurrence for the worst-case running time of this recursive version of insertion sort.

**2.3-5**
Referring back to the searching problem (see Exercise 2.1-3), observe that if the sequence $A$ is sorted, we can check the midpoint of the sequence against $v$ and eliminate half of the sequence from further consideration. The binary search algorithm repeats this procedure, halving the size of the remaining portion of the sequence each time. Write pseudocode, either iterative or recursive, for binary search. Argue that the worst-case running time of binary search is $\Theta(\lg n)$.

**2.3-6**
Observe that the while loop of lines 5–7 of the INSERTION-SORT procedure in Section 2.1 uses a linear search to scan (backward) through the sorted subarray $A[1..j-1]$. Can we use a binary search (see Exercise 2.3-5) instead to improve the overall worst-case running time of insertion sort to $\Theta(n\lg n)$?

**2.3-7** ?
Describe a $\Theta(n\lg n)$-time algorithm that, given a set $S$ of $n$ integers and another integer $x$, determines whether or not there exist two elements in $S$ whose sum is exactly $x$.

### Problems <span style="color:#2471a3;">**[problem]**</span>

**2-1** Insertion sort on small arrays in merge sort

Although merge sort runs in $\Theta(n\lg n)$ worst-case time and insertion sort runs in $\Theta(n^2)$ worst-case time, the constant factors in insertion sort can make it faster in practice for small problem sizes on many machines. Thus, it makes sense to coarsen the leaves of the recursion by using insertion sort within merge sort when

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.40</span>

### Problems <span style="color:#2471a3;">**[problem]**</span>（续）

**2-1**（续）Insertion sort on small arrays in merge sort

subproblems become sufficiently small. Consider a modification to merge sort in which $n/k$ sublists of length $k$ are sorted using insertion sort and then merged using the standard merging mechanism, where $k$ is a value to be determined.

a. Show that insertion sort can sort the $n/k$ sublists, each of length $k$, in $\Theta(nk)$ worst-case time.

b. Show how to merge the sublists in $\Theta(n\lg(n/k))$ worst-case time.

c. Given that the modified algorithm runs in $\Theta(nk + n\lg(n/k))$ worst-case time, what is the largest value of $k$ as a function of $n$ for which the modified algorithm has the same running time as standard merge sort, in terms of $\Theta$-notation?

d. How should we choose $k$ in practice?

**2-2** Correctness of bubblesort

Bubblesort is a popular, but inefficient, sorting algorithm. It works by repeatedly swapping adjacent elements that are out of order.

```text
BUBBLESORT(A)
1  for i = 1 to A.length − 1
2      for j = A.length downto i + 1
3          if A[j] < A[j − 1]
4              exchange A[j] with A[j − 1]
```

a. Let $A'$ denote the output of BUBBLESORT($A$). To prove that BUBBLESORT is correct, we need to prove that it terminates and that

```math
A'[1] \le A'[2] \le \cdots \le A'[n],
```

(2.3)

where $n = A.length$. In order to show that BUBBLESORT actually sorts, what else do we need to prove?

The next two parts will prove inequality (2.3).

b. State precisely a loop invariant for the for loop in lines 2–4, and prove that this loop invariant holds. Your proof should use the structure of the loop invariant proof presented in this chapter.

c. Using the termination condition of the loop invariant proved in part (b), state a loop invariant for the for loop in lines 1–4 that will allow you to prove inequality (2.3). Your proof should use the structure of the loop invariant proof presented in this chapter.

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.41</span>

### Problems <span style="color:#2471a3;">**[problem]**</span>（续）

**2-2**（续）Correctness of bubblesort

d. What is the worst-case running time of bubblesort? How does it compare to the running time of insertion sort?

**2-3** Correctness of Horner's rule

The following code fragment implements Horner's rule for evaluating a polynomial

```math
P(x) = \sum_{k=0}^{n} a_k x^k = a_0 + x\left(a_1 + x\left(a_2 + \cdots + x\left(a_{n-1} + xa_n\right)\cdots\right)\right),
```

given the coefficients $a_0, a_1, \ldots, a_n$ and a value for $x$:

```text
1  y = 0
2  for i = n downto 0
3      y = a_i + x · y
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段代码在中国数学史上有更早的出处：Qin Jiushao（秦九韶）在 1247 年成书的 Shushu Jiuzhang（《数书九章》）里，已系统使用同样的嵌套乘法求多项式的值。
>
> 史实部分（已查一手线索）：Qin Jiushao（约 1202–1261）是南宋数学家，1247 年成书 Shushu Jiuzhang（《数书九章》）。William George Horner 的同名方法发表于 1819 年 Philosophical Transactions 第 109 卷 308–335 页，标题为 A new method of solving numerical equations of all orders, by continuous approximation；Horner 本人把优先权归给 Lagrange，而更早的波斯与阿拉伯数学家在 11 至 12 世纪已有类似做法。
>
> 为什么这一重排是本质改进：朴素法算每个 $a_k x^{k}$ 都要从头做 $k$ 次乘法，合计约 $n(n+1)/2$ 次；嵌套形式每个括号恰一次乘、一次加，共 $n$ 次乘、$n$ 次加。$n=100$ 时是 5050 次对 100 次，差 50 倍。
>
> 更深一层：这已经是给定 $x$ 与系数时的乘加次数下界——每一步都要把一个系数纳入，且只能以一次乘加完成，所以 $n$ 次乘、$n$ 次加不可能更少。这是少数“最优性可证”的具体情形。
>
> 数值上的第二个好处：运算次数少意味着舍入误差少。浮点世界里每次乘加都引入一次舍入，嵌套形式把 $n(n+1)/2$ 次乘法带来的误差累积压到 $n$ 次，精度自然更好。这一点在数值分析里常常比速度更重要。
>
> 代码结构怎么读：$y=0$ 起手，逆序扫描 $i$ 从 $n$ 到 0，每步 $y=a_i+x\cdot y$。逆序是关键——它把最高次项留在最内层，于是每往外套一层就升一次幂。若改成顺序扫描，嵌套的方向就反了。
>
> 与 6.042J 的连接：这等价于把多项式写成嵌套形式后，用归纳证明求值正确；习题 (c) 给的不变式正是这条归纳的显式形式，与第 19 页的模板同构。
>
> 与 CSAPP 的连接：$n$ 次乘加在现代处理器上对应 $n$ 条 FMA（fused multiply-add，融合乘加）指令，吞吐可以到每周期一到两条。constant factor（常数因子）的战场又一次出现，但增长阶先由乘加次数锁定——两者不能混谈。
>
> 收束：同一数学对象的不同计算组织方式，运行时间可以差一个量级。这六行代码是本卷最便宜的一次“换 algorithm（算法）”示范，也是“重排即优化”的第一个范例。
>
> 还有一个历史侧面值得知道：Horner 的论文原本讨论的是数值求根（把方程逐步降次），嵌套乘法只是其中的工具；今天教科书把它写成“多项式求值”，其实窄化了原始语境。读原始标题就能看出这一点。
>
> 另一个可算的对照：若系数是整数且 $x$ 很小（比如 $x=2$），朴素法的中间结果会迅速膨胀成天文数字，而嵌套形式每一步只保留一个当前值——这就是它在符号计算与大整数场景里不可替代的原因。
>
> 最后补一句边界：嵌套形式对任意系数与任意 $x$ 都成立，不要求 $x$ 是整数、也不要求系数非负；正因如此，它才同时出现在数值分析与符号计算两个领域。
>
> 一句话：这段代码的价值不在技巧，而在它示范了“同一对象、不同组织、不同代价”这个贯穿全书的主题。
>
> 把规模再推大一档：多项式次数一千时，朴素法要五十万零五百次乘法，嵌套形式只要一千次，差五百倍。这个倍数随次数线性增长，所以次数越大，重排的价值越明显——这也是数值库里的多项式求值几乎从不写成逐项累加的原因。

a. In terms of $\Theta$-notation, what is the running time of this code fragment for Horner's rule?

b. Write pseudocode to implement the naive polynomial-evaluation algorithm that computes each term of the polynomial from scratch. What is the running time of this algorithm? How does it compare to Horner's rule?

c. Consider the following loop invariant:

At the start of each iteration of the for loop of lines 2–3,

```math
y = \sum_{k=0}^{n-(i+1)} a_{k+i+1} x^k.
```

Interpret a summation with no terms as equaling 0. Following the structure of the loop invariant proof presented in this chapter, use this loop invariant to show that, at termination, $y = \sum_{k=0}^{n} a_k x^k$.

d. Conclude by arguing that the given code fragment correctly evaluates a polynomial characterized by the coefficients $a_0, a_1, \ldots, a_n$.

**2-4** Inversions

Let $A[1..n]$ be an array of $n$ distinct numbers. If $i < j$ and $A[i] > A[j]$, then the pair $(i, j)$ is called an inversion of $A$.

a. List the five inversions of the array $\langle 2, 3, 8, 6, 1\rangle$.

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.42</span>

### Problems <span style="color:#2471a3;">**[problem]**</span>（续）

**2-4**（续）Inversions

b. What array with elements from the set $\{1, 2, \ldots, n\}$ has the most inversions? How many does it have?

c. What is the relationship between the running time of insertion sort and the number of inversions in the input array? Justify your answer.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> inversion（逆序对）是连接“排序”与“计数”的桥梁概念：它把一个 algorithm（算法）的运行时间，翻译成一个与输入形状有关的整数。
>
> 为什么 insertion sort（插入排序）的运行时间由逆序数决定：while 循环体执行一次（第 6–7 行）等价于“交换相邻的一对逆序元素”；任何一次相邻交换恰好消去一个 inversion（逆序对），而有序序列的逆序对为零。所以元素移动总数恰好等于初始逆序数，运行时间即逆序数加 $\Theta(n)$ 的骨架代价。
>
> 亲手数一遍：$A=\langle5,2,4,6,1,3\rangle$ 的逆序对是 $(5,2)$、$(5,4)$、$(5,1)$、$(5,3)$、$(2,1)$、$(4,1)$、$(4,3)$、$(6,1)$、$(6,3)$，共 9 个——与第 11 页状态表里数出的 9 次移位完全一致。两条独立的算法（数对与跑代码）给出同一个数，这就是可核对的证据。
>
> 两个极端：逆序最多的是严格递减序列，逆序对数为 $n(n-1)/2$，恰好是最坏情况；最少的是已排序序列，逆序对数为 0，恰好是最好情况。于是“最好”与“最坏”这两个名字，第一次有了精确的计数含义，而不只是两个形容词。
>
> 与 6.042J 的连接：对换是排列的基本生成元，逆序数刻画一个排列到单位排列的“距离”。区别在于置换理论关心奇偶性（它是同态的像），这里关心的是计数本身（它是代价）——同一个量，两种用途。
>
> 分治的做法：用 merge sort（归并排序）数逆序对时，跨左右两半的逆序对可以在 MERGE 扫描中顺带统计——当右半的元素先于左半某元素被复制走，它比左半剩余的全部元素都小，于是只需一次加上“左半剩余个数”。
>
> 算一下这个“顺带”有多便宜：MERGE 本来就是 $\Theta(n)$，加一条累加语句仍是 $\Theta(n)$，总复杂度不变，仍为 $\Theta(n\log n)$。这正是分治的招牌应用之一：合并步不仅产出排序结果，还白拿一份计数信息。
>
> 一个边界要记清：相等元素不算 inversion（逆序对），因为定义要求 $A[i]>A[j]$，是严格大于。这也与 stable（稳定）排序的语义一致——相等不需要交换，交换了反而破坏稳定性。
>
> 收束：能在合并步里顺带统计的东西，通常都与“跨两段的关系”有关。逆序对只是一个样板，同族的问题还有“跨段的距离和”“跨段的第 k 大”，都可以按同一思路改造合并步。
>
> 一个可以自己算的例子：习题 2-4(a) 的 $\langle2,3,8,6,1\rangle$ 里，逆序对是 $(8,6)$、$(8,1)$、$(6,1)$、$(3,1)$、$(2,1)$，共 5 个。五个逆序对意味着 insertion sort（插入排序）在这条输入上恰好做 5 次移位。
>
> 另一个推论：既然逆序数决定代价，“部分有序”的输入对 insertion sort（插入排序）就是友好的——逆序数少、移位就少。这也是它常被当作混合策略里小规模排序器的现实理由。
>
> 一句话把这件事说透：逆序数是输入的属性，运行时间是它的函数；这把“输入分布”与“algorithm（算法）的代价”第一次接了起来，也让 average-case analysis（平均情况分析）有了具体的计数对象。
>
> 记住这条：逆序数既是代价，也是度量。
>
> 再给一个可算的量级：一千个互不相同的数，逆序数最大是四十九万九千五百，正好是最坏情况下 insertion sort（插入排序）的移位次数上界。这个数与 n 的平方同阶，所以最坏情况的二次代价不是估出来的，是数出来的。反过来，若输入几乎有序、逆序数只有几百，插入排序的实际代价就接近线性——同一段代码在两个输入上能差三个数量级，这是“输入分布”第一次进入代价公式。

d. Give an algorithm that determines the number of inversions in any permutation on $n$ elements in $\Theta(n\lg n)$ worst-case time. (Hint: Modify merge sort.)

### Notes for Chapter 2 <span style="color:#2471a3;">**[reference]**</span>

In 1968, Knuth published the first of three volumes with the general title *The Art of Computer Programming* [209, 210, 211]. The first volume ushered in the modern study of computer algorithms with a focus on the analysis of running time, and the full series remains an engaging and worthwhile reference for many of the topics presented here. According to Knuth, the word "algorithm" is derived from the name "al-Khowârizmî," a ninth-century Persian mathematician.

Aho, Hopcroft, and Ullman [5] advocated the asymptotic analysis of algorithms—using notations that Chapter 3 introduces, including $\Theta$-notation—as a means of comparing relative performance. They also popularized the use of recurrence relations to describe the running times of recursive algorithms.

Knuth [211] provides an encyclopedic treatment of many sorting algorithms. His comparison of sorting algorithms (page 381) includes exact step-counting analyses, like the one we performed here for insertion sort. Knuth's discussion of insertion sort encompasses several variations of the algorithm. The most important of these is Shell's sort, introduced by D. L. Shell, which uses insertion sort on periodic subsequences of the input to produce a faster sorting algorithm.

Merge sort is also described by Knuth. He mentions that a mechanical collator capable of merging two decks of punched cards in a single pass was invented in 1938. J. von Neumann, one of the pioneers of computer science, apparently wrote a program for merge sort on the EDVAC computer in 1945.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> John von Neumann（冯·诺伊曼）写归并排序程序这件事，是早期对 algorithm（算法）运行时间做认真分析的罕见范例——它把“机器能做什么”和“要花多久”第一次写在一起。
>
> 人物与时间：von Neumann（1903–1957，生于布达佩斯）横跨纯数学、量子力学、博弈论与计算科学。1945 年他为 EDVAC 写程序时给出了归并排序；1945 年 6 月 30 日的 First Draft of a Report on the EDVAC 确立了存储程序结构。
>
> 更精确的线索（已查一手材料）：他 1945 年写的那段代码被称为 meshing routine（穿插子程序），作用是把两条有序序列合并成一条；随后他与 Herman Goldstine 在 1945 至 1948 年间的一系列 Planning and Coding 报告中给出了详细描述与分析。学界把这批材料视为最早的现代程序之一，Springer 2018 年的专著 Routines of Substitution 专门整理过它。
>
> 动机很有时代感：1938 年出现的collator（机械穿卡归并机）能单遍把两摞穿卡合成一摞，von Neumann 把这一实务提炼成可分析的 algorithm（算法）——机器能做的事，先在纸上写成指令序列，再算清它要跑多久。提炼的方向是“从实物到指令序列”，而不是从数学到公式。
>
> 为什么说它早：Aho、Hopcroft 与 Ullman 在 1970 年代才把渐近分析推广为比较 algorithm（算法）的标准工具；von Neumann 的分析比它早二十多年，而且针对的是一个具体程序的精确计数，不是一般性的阶。
>
> Knuth 的位置也要摆准：1968 年第一卷出版，把“定量分析运行时间”立成纲领；所引 Knuth 第三卷专论排序与查找，对包含 Shell sort（希尔排序）在内的 sorting algorithm（排序算法）做了百科式梳理，是本章最好的延伸读物。
>
> 与 CSAPP 的连接：存储程序结构（指令与数据同处一个存储器）正是 CSAPP 第 3 章那套机器级图景的前提。没有它，“程序的运行时间”这个问题本身都无法提出。
>
> 与 6.042J 的连接：这段历史说明，把直觉写成可分析的对象——这里是“合并两摞穿卡”写成指令序列——与你在 6.042J 里把直观想法写成形式定义，是同一个动作。
>
> 收束：本章末这段 Notes 只有三句话，却串起三条线：机械实务、算法分析、以及把二者接起来的那个人。读史的价值在于看清方法是从哪种现实里长出来的，而不是记住几个年份。
>
> 还有一个细节值得说：von Neumann 的代码写的是“把两条有序序列穿插成一条”，而不是“递归地排序整个数组”——递归版本的清晰表述要等到后来。历史顺序常常是先有工程上的合并，再有算法上的分解。
>
> 另一条时间线：归并排序的递归形式在 1945 年之后很久才成为教科书的标准写法。CLRS 采用自顶向下的 pseudocode（伪代码），是为了让分治范式显形，而不是因为历史上先有它。
>
> 最后提醒：Notes 里的年份只用来定位，不用来背；真正要记的是“机械实务 → 指令序列 → 精确计数”这条方法链条。
>
> 一句话：方法是从实物里长出来的，不是从定义里长出来的。
>
> 再补一条方法上的连线：本页提到的 Shell sort（希尔排序），是 D. L. Shell 在 insertion sort（插入排序）基础上做的改进——先用较大间隔把数组分成若干子序列各自排序，再逐步缩小间隔，最后一遍间隔为一。它说明同一个基本操作、不同的分组顺序，能换出不同的实际代价；这与本章反复出现的主题完全一致：改组织，不改数学。

The early history of proving programs correct is described by Gries [153], who credits P. Naur with the first article in this field. Gries attributes loop invariants to R. W. Floyd. The textbook by Mitchell [256] describes more recent progress in proving programs correct.
