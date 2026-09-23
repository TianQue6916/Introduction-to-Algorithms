# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk01 · 书页 5–42（第 1 章 + 第 2 章） · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §1.1, p.5</span>

## Chapter 1 · The Role of Algorithms in Computing（算法在计算中的作用）

什么是算法（algorithm）？为什么研究算法是有价值的？相对于计算机所使用的其他技术，算法又扮演着什么角色？在本章中，我们将回答这些问题。

### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

非正式地说，算法是任何定义良好的计算过程（computational procedure），它以某个值或一组值作为输入（input），并产生某个值或一组值作为输出（output）。因此，算法就是一系列计算步骤（computational steps），把输入转换为输出。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 别放过"定义良好（well-defined）"这个限定词——它是整个学科的第一性原理。"良定义"要求每一步都无歧义：给定同样的输入与同样的中间状态，下一步做什么只有唯一的答案，这正是"确定性"的根源。它也是你在 6.042J 里养成的证明次序的来源：在证明一个命题之前必须先把命题的陈述（spec）写精确，否则"证明正确"根本无从谈起——算法的 spec 就是下一段所说的输入/输出关系，"算法正确"的意思是：对所有输入实例，算法产生的输出都满足这个规约。反过来看，如果规约本身有歧义（比如"排序后相等的元素要不要保持原有相对顺序？"），就会出现两个行为不同、却各自"都算对"的算法，正确性的争论永无止境。所以第一性原理是：计算问题的本质是一个从输入到输出的关系，算法是这个关系的有限、无歧义、可执行的描述；先有精确规约，才谈得上算法与正确性。第 2 章的 loop invariant（循环不变式）会把"证明正确性"进一步形式化。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 历史背景：人类基因组计划由美国 NIH 等机构资助，1990 年正式启动，2003 年 4 月 14 日宣布完成，当时覆盖了约 92% 的基因组，被称为当时世界上最大的国际科研合作项目（据离线维基百科）；书中"100,000 个基因"正是 20 世纪 90 年代的流行估计，后来的研究已把这个数字下修到约 2 万。算法在其中做了什么？测序仪读出的只是一段段短片段，需要用拼接（fragment assembly）算法把数百万个短读段按重叠关系组装成完整序列——本质上是超大规模的"拼图"问题；基因识别要在 30 亿个碱基对中找出编码区；数据库检索要在海量序列里快速定位相似片段。其中序列相似性比较用到的核心思想，正是下一页将展示的 longest common subsequence（最长公共子序列）：两段 DNA 公共子序列越长，就越可能同源。CLRS 第三版出版于 2009 年，正值 HGP 完成后基因组数据爆炸的时期，所以本书把它列为算法应用的第一例。

- **互联网（Internet）**使全世界的人们能够快速访问和检索大量信息。借助巧妙的算法，互联网上的站点得以管理和操纵如此庞大的数据量。基本离不开算法的典型问题包括：为数据寻找良好的传输路由（解决此类问题的技术出现在第 24 章），以及利用搜索引擎快速找到承载特定信息的页面（相关技术在第 11 章和第 32 章）。

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.7</span>


### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

- **电子商务（electronic commerce）**使商品和服务得以通过电子方式进行磋商与交换，它依赖于信用卡号、密码、银行对账单等个人信息的私密性。电子商务所采用的核心技术包括公钥密码学（public-key cryptography）和数字签名（digital signatures）（见第 31 章），它们建立在数值算法和数论（number theory）的基础之上。

- **制造业及其他商业企业**常常需要以最有利的方式来分配稀缺资源。石油公司可能想知道把油井布置在何处才能使其期望利润（expected profit）最大化；政治候选人可能想知道把钱花在哪里购买竞选广告，才能使赢得选举的机会最大化；航空公司可能想以尽可能低的成本为航班安排机组人员，同时确保每个航班都有人覆盖并符合政府对机组排班的法规；互联网服务提供商可能想知道在哪里部署额外资源，才能更有效地服务其客户。所有这些都是可以用线性规划（linear programming）解决的问题的例子，我们将在第 29 章中学习线性规划。

虽然这些例子中的某些细节超出了本书的范围，但我们确实给出了适用于这些问题及问题领域的基础技术。我们还将展示如何解决许多具体的问题，包括下面这些：

- 给定一张道路图，图上标出了每对相邻交叉路口之间的距离，我们希望确定从一个交叉路口到另一个交叉路口的最短路线。即使不允许路线自我交叉，可能的路线的数目也可能极其庞大。我们怎样才能在所有可能的路线中选出最短的那条？这里，我们把道路图（它本身就是对实际道路的一种建模）抽象为一个图（graph）（我们将在第六部分和附录 B 中遇到图），并希望在图中找到从一个顶点到另一个顶点的最短路径（shortest path）。我们将在第 24 章看到如何高效地解决这个问题。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 跨课程连接：把道路图抽象成图 $G=(V,E)$，你在 6.042J 的图论部分已经握有全部原材料——图只保留"顶点 + 连接关系"这一结构，丢弃城市名称、路面宽度等无关信息，而建模的本质就是丢弃。6.042J 教过你路径（path）、简单路径（simple path），以及 $n$ 个顶点的图中简单路径长度至多 $n-1$ 这类结构性质；最短路问题问的则是带权版本：在所有从起点到终点的路径中，找边权之和最小的那条。为什么暴力枚举行不通？路线数目随顶点数呈指数级增长——这正是本段说"可能的路线数目极其庞大"的精确含义。第 24 章的 Dijkstra 算法之所以高效，是因为它不枚举路径，而是按"离源点由近到远"的顺序一次性确定所有顶点的最短路。类比成立之处：两者讨论的是同一对象——带权图中的路径；区别在于 6.042J 关心路径的存在性与结构，最短路算法关心的是在所有路径上最优化一个量。带着这个区分去读第六部分，你会发现习题 1.1-4（比较最短路与旅行商问题）问的正是"同对象、不同目标"这种关系。

- 给定两个有序符号序列 $X = \langle x_1, x_2, \ldots, x_m \rangle$ 和 $Y = \langle y_1, y_2, \ldots, y_n \rangle$，我们希望找出 $X$ 和 $Y$ 的一个最长公共子序列（longest common subsequence）。$X$ 的子序列就是把 $X$ 中的某些元素（也可能是全部或没有）删去后所得的结果。例如，$\langle A, B, C, D, E, F, G \rangle$ 的一个子序列可以是 $\langle B, C, E, G \rangle$。$X$ 和 $Y$ 的最长公共子序列的长度给出了这两个序列相似程度的一种度量。例如，如果这两个序列是 DNA 链上的碱基对，那么当它们有一个很长的公共子序列时，我们就可以认为它们是相似的。如果 $X$ 有 $m$ 个符号而 $Y$ 有 $n$ 个符号，那么 $X$ 和 $Y$ 分别有 $2^m$ 和 $2^n$ 个可能的子序列；除非 $m$ 和 $n$ 都非常小，否则选出 $X$ 和 $Y$ 的所有可能子序列并逐一匹配，可能要耗费长得无法接受的时间。我们将在第 15 章看到，如何用一种称为动态规划（dynamic programming）的通用技术来高效地解决这个问题。

---

> <span style="color:#7f8c8d;">CLRS §1.1, p.8</span>


### Section 1.1 · Algorithms（算法） <span style="color:#2471a3;">**[section]**</span>

> <span style="color:#7f8c8d;">**[note]** 本页开头的 longest common subsequence（最长公共子序列）示例收尾两句（"respectively. Selecting all possible subsequences…"）已并入第 7 页对应段落，此处直接接续下一示例。</span>

- 给定一个用零件库表示的机械设计，其中每个零件可能包含其他零件的实例，我们需要按顺序列出这些零件，使得每个零件都出现在使用它的任何零件之前。如果设计包含 $n$ 个零件，那么可能有 $n!$ 种顺序，其中 $n!$ 表示阶乘函数（factorial function）。由于阶乘函数的增长速度甚至比指数函数还快，我们不可能（除非零件很少）逐一生成每种可能的顺序，再验证在该顺序中每个零件是否出现在使用它的零件之前。这个问题是拓扑排序（topological sorting）的一个实例，我们将在第 22 章看到如何高效地解决它。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 跨课程连接：这个"零件必须排在使用它的零件之前"的例子，就是你 6.042J 学过的偏序集（partially ordered set）在工程中的化身。"零件 A 必须排在零件 B 之前"定义了零件集合上的一种二元关系，它满足偏序的三条公理：自反性可弱化看待、反对称（不能既要求 A 在 B 前又要求 B 在 A 前）、传递性（A 在 B 前、B 在 C 前，则 A 在 C 前）。6.042J 里你画过偏序集的 Hasse 图——只画覆盖关系、去掉由自反性和传递性必然推出的边的最简图示。而拓扑排序做的事，用 6.042J 的语言说就是求线性扩张（linear extension）：把偏序的元素排成一个序列，使序列中的先后顺序与偏序完全一致。为什么类比成立？两者共享同一个结构不变量：无环——一旦出现循环依赖（A 依赖 B、B 又依赖 A），反对称性就被破坏，这样的顺序根本不存在。区别在于：Hasse 图是偏序的可视化，拓扑排序是对偏序的一种线性化；而且同一个偏序通常有多个线性扩张——$n!$ 个候选顺序里合法的那些，恰好就是全部线性扩张。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 拓展注：要把"没人找到多项式算法，也没人证明它不存在"这句话读准，需要你在 6.046J Lec16 接触过的 P/NP 框架。P 是"多项式时间内可解"的问题类；NP 是"多项式时间内可验证"的问题类——注意"解"与"验证"的差别：给你一张填好的数独，验证它合法只需扫一遍棋盘，但面对空盘找出填法可能极其困难。P 是否等于 NP 至今未解，是克雷数学研究所 2000 年悬赏百万美元的七大千禧年问题之一。NP 完全问题的严格含义是：它们是 NP 中"最难"的一批，任何 NP 问题都能在多项式时间内归约（reduction）到它们——所以其中任何一个有了多项式算法，全部 NP 问题就都有了，这正是下页"一荣俱荣"的准确说法。实践含义因此非常具体：一旦识别出手头问题是 NP 完全的，就不要再在精确多项式算法上徒劳，而是转向三条出路——近似算法（第 35 章的 traveling-salesman 近似）、启发式与随机化，或挖掘输入的特殊结构。"识别出它是 NP 完全的"本身就是一项有价值的成果。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第一性原理：为什么区区常数因子（$c_1 < c_2$）会被增长率吞没？令交叉点处 $c_1 n^2 = c_2 n \lg n$，化简得 $n / \lg n = c_2 / c_1$。关键在于函数 $n / \lg n$ 单调递增且无上界：$n = 1000$ 时约为 100，$n = 10^6$ 时约为 5 万，$n$ 再增大它只会更大。所以无论 $c_2 / c_1$ 多大——哪怕 $c_1$ 比 $c_2$ 小一千倍——总有一个 $n$ 让 $n/\lg n$ 超过它，这就是交叉点必然存在的代数根源。你在 CSAPP 学到的指令级视角能帮你看清这件事的本质：第 5 章的程序优化（消除循环低效、减少过程调用、提高缓存局部性）确实能把常数因子压低几倍到几十倍，但这些优化改变的是"每一步的代价 $c$"，改变不了"步数随 $n$ 增长的方式"。$c$ 是固定的一次效应，增长率之差却是随 $n$ 无界放大的效应——渐近优势最终总是压倒常数优势。这也划清了两个领域的分工：性能调优决定 $c$，算法设计决定增长率，而后者在规模面前权力更大。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 跨课程连接：计算机 A/B 这组数字的本质是——算法的渐近改进可以碾压硬件 1000 倍的劣势；而你在 CSAPP 学到的机制恰好解释了为什么硬件优势注定只能是"常数级"。流水线让处理器重叠执行多条指令、缓存命中把访存从几十个周期降到几个周期、超标量让每周期发射多条指令——这些机制（CSAPP 第 3、5 章反复出现）决定的是常数因子 $c$ 的取值范围：精巧的机器语言加上手工调度，也许能把 $c$ 压低几倍到几十倍，但永远改变不了"步数是 $n$ 的什么函数"。本例中 A 的硬件快 1000 倍（$10^{10}$ 对 $10^7$ 条指令/秒），却被运行时间之比吞掉：$2n^2 / (50n\lg n) = n/(25\lg n)$，代入 $n = 10^7$ 得约 $1.7\times 10^4$ 倍——增长率优势远大于 1000 倍，硬件优势被彻底淹没。把两个效应摆在一起看：换硬件给出的是有界的常数倍回报，换算法给出的是随 $n$ 无界增长的回报。工程结论由此而来：当数据规模还会增长时，投资"换算法"的上限远高于投资"换硬件"。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 以下为译者根据原文 Problem 1-1 重构的表格示意。**Problem 1-1**（表格，接上页）——下表给出运行时间函数 $f(n)$ 与时间 $t$ 的组合：

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 历史注：文献列表中的 Knuth [209, 210, 211] 就是《The Art of Computer Programming》（TAOCP）。Donald Knuth（1938 年生）于 1962 年着手这个项目，原本只设想一本 12 章的书，结果写着写着成了鸿篇巨制：第一卷 Fundamental Algorithms 于 1968 年出版，全书计划 7 卷，至 2026 年已出到第 4B 卷（据离线维基百科）；他因此被业界称为"算法分析之父"，并于 1974 年获图灵奖。TAOCP 第一次把"算法描述 + 正确性证明 + 精确的运行时间分析"作为一个整体来写作，本书的行文风格正是直接继承于此。"algorithm（算法）"这个词本身来自 9 世纪的波斯数学家 al-Khwārizmī（约 780–约 850）：他在巴格达的智慧宫任职，约 820 年写成《Al-Jabr》——书名正是 algebra（代数）一词的来源；他的名字拉丁化为 Algoritmi，12 世纪其著作经拉丁文译本传入欧洲后，"algorism" 一度专指十进制算术的逐步计算程序，后来逐渐演变为今天的 algorithm。换句话说，"算法"与"代数"这两个词，是同一位 9 世纪学者留给现代计算机科学的双份遗产。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 以下对图面内容的文字描述为译者补充（原文图注仅一句）：图中左侧是桌上牌面朝下的 pile（牌堆），右侧是左手中已按 sorted order（已排序顺序）排好的 cards。

那么，pseudocode（伪代码）与 “real” code（真正的代码）之间的区别在于：在 pseudocode 中，为了 specify（描述）一个给定的 algorithm，我们采用最清晰、最简洁的 expressive method（表达方式）。有时候，最清晰的表达方式是 English（英语），所以如果你在“真正的”代码段落中碰到嵌入的英文短语或句子，不必感到惊讶。pseudocode 与 real code 的另一个区别是：pseudocode 通常不关心 software engineering（软件工程）方面的问题。data abstraction（数据抽象）、modularity（模块化）和 error handling（错误处理）等问题往往会被忽略，目的是更简洁地传达 algorithm 的 essence（精髓）。

我们从 insertion sort 入手，它是针对少量 elements 进行排序的一种高效 algorithm。insertion sort 的工作方式与许多人整理一手 playing cards 的方式相同：我们从一只空的 left hand（左手）以及桌上牌面朝下的 cards 开始，然后一次从桌上取出一张 card（扑克牌），把它插入 left hand 中正确的位置。为了找到一张 card 的正确位置，我们把它与手中已有的每一张 card 从右到左逐一比较，如图 2.1（Figure 2.1）所示。在任何时刻，left hand 中持有的 cards 都是已排序的，而且这些 cards 原本正是桌上 pile 顶部的 cards。

我们把 insertion sort 的 pseudocode 表示为一个名为 INSERTION-SORT 的 procedure（过程），它以 array（数组）$A[1..n]$ 作为参数，该 array 包含一个长度为 $n$、待排序的 sequence（序列）。（在代码中，$A$ 中 elements 的个数 $n$ 记作 $A.length$。）该 algorithm 对输入的数进行 in place（原地）排序：它在 array $A$ 内部重新排列这些数，任意时刻存储在 array 之外的数至多只有 constant（常数）个。当 INSERTION-SORT procedure 结束时，input array（输入数组）$A$ 中就包含了已排序的 output sequence（输出序列）。

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.18</span>

**Figure 2.2（图 2.2）：** 对 array（数组）$A = \langle 5, 2, 4, 6, 1, 3 \rangle$ 执行 INSERTION-SORT 的操作过程。array indices（数组下标）显示在矩形上方，存储在 array 各位置中的 values（值）显示在矩形内部。(a)–(e) 为第 1–8 行 for loop（for 循环）的各次 iterations（迭代）。在每次 iteration 中，black rectangle（黑色矩形）存放取自 $A[j]$ 的 key（关键字），它会在第 5 行的 test（测试）中与它左侧 shaded rectangles（阴影矩形）中的 values 进行比较。shaded arrows（阴影箭头）表示第 6 行中 array values 向右移动一个位置，black arrows（黑色箭头）表示第 8 行中 key 所移动到的位置。(f) 为最终的 sorted array（已排序数组）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 以下为译者根据原文图 2.2 重构的文本示意图（原文为插图，无此文本表格）：

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这一论证结构值得命名为「循环不变式论证」模板，它可以与你学过的 6.042J 数学归纳法逐条对齐：Initialization（初始化）对应 base case（基例），即证明 $P(2)$；Maintenance（保持）对应 inductive step（归纳步），即证明“$P(j)$ 为真则 $P(j+1)$ 为真”；Termination（终止）则是取“终点”时的推论——在 $j = n+1$ 处实例化不变式。它与纯归纳法的区别原文已点破：归纳法可以无限应用归纳步，而循环必然终止，我们恰恰要利用“终止时刻”这个特殊点，把终止条件（$j > n$）代入不变式，才兑换出真正想证的性质——“整个数组已排序”。换句话说，前两条性质只保证不变式永远为真，第三条才把它变成正确性。今后遇到“某量在每轮循环后都满足某性质”的命题，先问：不变式是什么？终止时它退化成什么？两问即是完整的证明骨架。

下面我们来看看这些 properties 对 insertion sort（插入排序）是如何成立的。

**Initialization（初始化）：** 我们首先证明当 $j = 2$ [1] 时，loop invariant 在第一次 loop iteration 之前成立。因此，subarray（子数组）$A[1..j-1]$ 只包含单独一个 element（元素）$A[1]$，它事实上正是原先位于 $A[1]$ 的 element。此外，这个 subarray 是已排序的（当然，这是平凡的），这就证明了 loop invariant 在 loop 的第一次 iteration 之前成立。

**Maintenance（保持）：** 接下来，我们处理第二个 property：证明每次 iteration 都维持 loop invariant。非形式地说，for loop 的 body（循环体）是这样工作的：把 $A[j-1]$、$A[j-2]$、$A[j-3]$ 等等依次向右移动一个 position（位置），直到为 $A[j]$ 找到合适的 position 为止（第 4–7 行），在那一刻它把 $A[j]$ 的 value（值）插入该 position（第 8 行）。于是 subarray $A[1..j]$ 就由原先位于 $A[1..j]$ 的 elements 组成，但处于 sorted order（已排序顺序）。随后为 for loop 的下一次 iteration 把 $j$ 递增 1，这样就保持了 loop invariant。

对第二个 property 进行更形式化的处理，需要我们为第 5–7 行的 while loop（while 循环）陈述并证明一条 loop invariant。然而，在目前这个阶段，

> <span style="color:#7f8c8d;">**[1]** 当 loop 是 for loop 时，我们在第一次 iteration 之前检查 loop invariant 的时刻，恰好在 loop-counter variable（循环计数器变量）的 initial assignment（初始赋值）之后、loop header（循环头）中第一次 test 之前。就 INSERTION-SORT 而言，这个时刻是在把 2 赋给 variable（变量）$j$ 之后、第一次 test 是否 $j \le A.length$ 之前。</span>

---

> <span style="color:#7f8c8d;">CLRS §2.1, p.20</span>

我们宁可不要陷入这种 formalism（形式化）的细节之中；因此，我们依靠 informal analysis（非形式化的分析）来证明第二个 property（性质）对外层 loop（循环）成立。

**Termination（终止）：** 最后，我们考察 loop 终止时会发生什么。导致 for loop 终止的 condition（条件）是 $j > A.length = n$。因为 loop 的每次 iteration（迭代）都会使 $j$ 增加 1，所以在那个时刻必定有 $j = n + 1$。把 $n + 1$ 代入 loop invariant（循环不变式）表述中的 $j$，我们得到：subarray（子数组）$A[1..n]$ 由原先位于 $A[1..n]$ 的 elements（元素）组成，但处于 sorted order（已排序顺序）。注意到 subarray $A[1..n]$ 就是整个 array（数组），我们得出结论：整个 array 是已排序的。因此，该 algorithm（算法）是正确的。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这份正确性证明里藏着一个值得咀嚼的递进逻辑：为什么只需“初始化 + 保持 + 终止条件”三样东西就足以推出正确性？关键在于不变式是一个全称命题——它在“每次迭代开始时”为真，而迭代次数有限。初始化给了它一个为真的起点；保持把它沿时间轴一格格传递下去，这正是归纳法传递性的作用；终止条件则指出循环停在哪个具体的 $j$ 上，把不变式在终点实例化，就从“每次迭代前 $A[1..j-1]$ 已排序”这个一般性陈述，落到“$A[1..n]$ 已排序”这个目标结论。用反例检验法拆一下：缺任何一样，论证立即坍塌——没有初始化，起点可能已错；没有保持，中途断链；没有终止条件，不变式纵然为真，也不知道循环停在哪，结论无处落地。这本质上就是 6.042J 里“归纳 + 终点推论”结构的重演，只是归纳对象从自然数换成了迭代轮数。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里的“传递的是指向数组的指针”值得接回 CSAPP 第 3 章的机器级图景：数组名在过程调用中的实际形态，是抄进被调用者 stack frame（栈帧）里的一个地址值，$A[i]$ 就是对“该地址加 $i$ 乘元素大小”处的一次访存。所以 CLRS 的“按值传递 + 对象按指针传递”并非两套规则，而是同一件事：被复制过去的是一个机器字——若变量是标量，这个字就是值本身；若变量是数组或对象，这个字是地址。为什么被调用者改 $A[3]$ 调用者看得见、改参数 $A$ 本身却看不见？因为前者是通过地址改写共享内存，后者只是改写栈帧里那份地址副本。类比成立的原因是两边共享“值即位模式”的表示语义；区别只在于伪代码抹掉了栈帧分配与寄存器传参的细节。想通这一点，本章伪代码与你在 CSAPP 实验里读的汇编就能互相对照了。

返回语句（return statement）会立即将控制权转移回调用过程中的调用点（the point of call）。大多数返回语句还会携带一个要返回给调用者的值。我们的伪代码与许多编程语言不同之处在于：我们允许在一条 return 语句中返回多个值（multiple values）。

布尔运算符（boolean operators）“and”和“or”是短路求值的（short circuiting）。也就是说，当对表达式“$x$ and $y$”求值时，我们先求值 $x$；若 $x$ 的值为 FALSE，则整个表达式不可能为 TRUE，因此我们不再求值 $y$。反之，若 $x$ 的值为 TRUE，则必须求值 $y$ 才能确定整个表达式的值。类似地，在表达式“$x$ or $y$”中，只有当 $x$ 的值为 FALSE 时才求值 $y$。短路运算符使我们能够写出诸如“$x \ne \text{NIL}$ and $x.f = y$”这样的布尔表达式，而不必担心当 $x$ 为 NIL 时求值 $x.f$ 会发生什么。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 短路求值（short-circuit evaluation）不只是语法便利，它是把控制流编码进布尔表达式的一招。用 CSAPP 第 3 章的机器级视角看，“$x$ and $y$”编译出来是“测试 $x$，为假则跳过 $y$ 的求值代码”，本质是一条条件分支指令，而不是把两个布尔值都算出来再相与。更关键的是它关乎正确性而不只是效率：若 $x = \text{NIL}$，$x.f$ 在真实机器上就是对非法地址的解引用，会触发段错误（CSAPP 里熟悉的 SIGSEGV），短路恰好保证这个危险操作永不执行。你在 C 语言里写的惯用法 `if (p && p->next)` 就是同一个模式在字节级的重演。所以读本书伪代码时遇到长串条件，可以默认那是“安全卫兵”式写法：前面的条件先给后面的条件发放“可以求值”的许可证，算法作者靠这一机制免费换来了边界安全。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 追问一层：为什么分析算法前要先立“每条指令常数时间”这条假设？因为不加这条假设，“运行时间”就不是一个良定义的量——同一段代码在解释器、带多级缓存的 x86、GPU 上可以相差几个数量级，没有公共标尺就无法比较算法本身。RAM 模型（RAM model）的做法是先抽掉全部实现差异，把“步数”当作与机器无关的代理变量。它丢掉了什么？缓存层级、流水线、分支预测、虚拟内存——恰是 CSAPP 第 5、6 章优化的全部舞台：一个数组遍历仅因缓存友好与否就可差数倍，而这些全被抹进 $c_i$ 里。为什么抹平后结论仍有用？因为对足够大的 $n$，算法结构决定的主项（如插入排序的内层比较次数）会压倒这些常数级差异，且“$n^2$ 次比较”这类计数结论在任何机器上都成立。代价则是：当两个算法增长阶数相同时，被抹掉的常数因子与缓存行为反而成为胜负手——那是 CSAPP 教你的战场。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里把从 $t_j = j$ 到 $an^2 + bn + c$ 的推演重演一遍，沉淀为可复用的思维模板。第一步，分情形枚举输入的“形状”：已排序给 $t_j = 1$，逆序给 $t_j = j$——这就是最好/最坏/平均三分法。第二步，把每行的“代价乘次数”求和，唯一要下功夫的是 $\sum_{j=2}^{n} j$：用 6.042J 的等差数列配对法立得 $\sum_{j=2}^{n} j = n(n+1)/2 - 1$。第三步合并同类项：$c_5 \cdot n(n+1)/2$ 贡献 $n^2$ 与 $n$ 项，各 $c_i(n-1)$ 只贡献 $n$ 项与常数项，$an^2 + bn + c$ 自然浮现。注意 $n^2$ 的系数只含 $c_5, c_6, c_7$——恰是 while 循环体那三行，这正是“内层循环决定增长阶数”的直接证据。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> “只保留首项”不是偷懒，而是刻意的信息压缩，值得用数字感受量级。设最坏情况为 $an^2 + bn + c$，代入典型常数（$a = 1/2$，$b = 20$，$c = 50$）：$n = 100$ 时首项 5000、低阶项 2050，低阶项还占四成；$n = 10^6$ 时首项 $5 \times 10^{11}$、低阶项约 $2 \times 10^7$，占比骤降到十万分之四。低阶项并非“不存在”，而是随 $n$ 增大被首项按多项式比例碾压——这与你在线性代数中分析矩阵幂 $A^k$ 时只看主导特征值的逻辑同构。CSAPP 给你常数因子的世界（一次访存与一次乘法差几十个周期），Strang 给你结构主导项的世界，$\Theta$ 记号是后者的极端形式：只留增长率。同时记住原文警告：小输入下高增长阶算法可能更快，Problem 2-1 的混合策略正源于此。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把 divide/conquer/combine 记成一个可复用的设计模板，而不只是归并排序的描述。模板的用力于两点：其一，“子问题与原问题相似”保证递归良构——$T(n)$ 的定义里可以合法出现 $T(n/b)$，这正是递归式（recurrence）写得出来的前提；其二，算法的成本核算被模板切成三笔账 $D(n) + aT(n/b) + C(n)$，其中 $D$、$C$ 通常是多项式，递归项是唯一的难点。什么时候用增量法（如插入排序）、什么时候用分治？经验法则是：若“新增一个元素”能利用已有结构以较廉代价吸收，增量法常数小、空间省；若问题能对半劈且合并代价不高于两半之和，分治能把你带进更低的增长阶数。第 4 章的主定理（master theorem）就是这本三步账的定量结算器：给定 $a$、$b$ 与 $D(n)+C(n)$ 的增长阶，直接读出 $T(n)$ 的阶，无需每次画树。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 哨兵（sentinel）是“用存储换分支”的典型交易，值得从第一性原理拆开。不加哨兵时，合并循环的每次迭代都必须回答两个问题：$L$ 空了吗？$R$ 空了吗？——两次边界检查在分支预测失败代价高昂的真实处理器上（CSAPP 第 3 章的条件分支、第 5 章的流水线）并不免费，且让循环体多出两条出口、代码路径翻倍。放入 $\infty$ 哨兵后，两个数组“永远取不完”：$\infty$ 与任何真实元素比较都判负，于是每个非哨兵元素仍按正确顺序被取走；仅当两堆都只剩哨兵时才会“取到” $\infty$，而此时循环恰好已做满 $r - p + 1$ 次迭代，靠 for 循环的计数器自然终止。两个边界检查就这样被一个数学事实——$\infty$ 是全序下的最大元——干净地消掉了。代价是每个数组多一个槽位与两次赋值。这个“让边界条件自然失效”的思想还会在第 10 章链表的 NIL 哨兵处重现。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 下表为译者根据原文图 2.3 的 (a)–(h) 八个分图重构的状态表（原文只有插图，无此表格），用于逐迭代跟踪第 12–17 行的动作（每次迭代取 $L[i]$ 与 $R[j]$ 中较小者写入 $A[k]$）：

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这份证明复用了 p.19 的「循环不变式论证」模板：Initialization 用“$k = p$ 时 $A[p..k-1]$ 为空、含最小 0 个元素”起跳，Maintenance 分 $L[i] \le R[j]$ 与 $L[i] > R[j]$ 两个对称分支各自推进，Termination 把终止值 $k = r + 1$ 代回不变式。要看到的不只是“又证了一遍”，而是模板的可移植性：同一个三段式骨架，装的变量从“数组前缀是否有序”换成“$A[p..k-1]$ 是否恰含最小的 $k - p$ 个元素”，证明结构不变。这正是 CLRS 在小算法上反复演练它的原因——正如你在 6.042J 先把归纳法练成肌肉记忆，再做图论与数论的证明。注意这里的不变式比插入排序的强：它同时约束“已复制部分”与“两个游标所指元素”，是复合不变式；设计不变式的诀窍，是让陈述恰好覆盖终止时你要用的全部信息。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 图 2.4 示意：底部是初始序列（initial sequence），经过多轮 merge（合并）逐层向上，顶部得到已排序序列（sorted sequence）。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> “假定 $n$ 是 2 的幂”是算法分析里的标准便利手法，值得记下它为什么合法。直觉是：非 2 次幂的输入只是让递归树“最后一层缺几块”，树高仍是约 $\lg n$，每层代价仍不超过 $cn$，其界被夹在相邻两个 2 次幂的界之间，相差至多常数倍——而 $\Theta$ 记号恰好对常数倍不敏感（第 3 章将形式化这一点）。这实际上是“先证好证的稠密子列（$n = 2^k$），再向一般 $n$ 扩张”的策略，与你正在学的实分析里“先在整数上证明、再延拓”的思路神似；脚注 8 用四种奇偶情形枚举来验证 $\lceil n/2 \rceil$ 与 $\lfloor n/2 \rfloor$ 的拆分，则是同样的诚实态度：便利假设也要核对边界。以后你看到“为简化设 $n$ 为 2 的幂”都不必过度警惕，但要能说清补偿论证在哪里。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 递归式 (2.2) 不是天上掉下来的，它是分治三步账本逐项过账的结果：$D(n) = \Theta(1)$ 来自“算中间点只需一次下标运算”；$2T(n/2)$ 来自“递归调用两次、每次规模减半”；$C(n) = \Theta(n)$ 来自 MERGE 的逐元素扫描。最值得建立的直觉是“每层合计 $cn$”：子问题个数变多但每个变小，两个效应恰好抵消——4 个 $T(n/4)$ 的合并代价 $4 \times c(n/4) = cn$，8 个亦然。这是“对半分、线性合并”的结构不变量：每层分摊的元素总量恒为 $n$ 个，每个恰被扫描一次，故每层成本锁定为 $cn$。于是总时间等于 $cn$ 乘层数，问题坍缩为一问：树有多高？约 $\lg n$ 层（每层规模除以 2）——这正是下一节递归树的内容。脚注 9 也值得细读：让常量 $c$ 分别取上、下界，就把未必精确的模型变成了夹逼上下的工具。

---

> <span style="color:#7f8c8d;">CLRS §2.3, p.37</span>

### Section 2.3 Designing algorithms（设计算法）· 续 <span style="color:#2471a3;">**[section]**</span>

图 2.5（Figure 2.5）展示了如何求解递归式（recurrence）(2.2)。为方便起见，我们假设 $n$ 是 2 的精确幂次（exact power of 2）。图的 (a) 部分给出 $T(n)$，我们在 (b) 部分将其展开（expand）为一棵等价于该递归式的树。$cn$ 项是根（root），即递归顶层（top level of recursion）所付出的代价；根的两棵子树（subtree）分别是两个更小的递归式 $T(n/2)$。(c) 部分通过展开 $T(n/2)$ 把这个过程又推进了一步。递归第二层的两个子节点各自付出的代价为 $cn/2$。我们继续展开树中的每个节点，按递归式的决定把它分解为相应的组成部分，直到问题规模缩小到 1，每个规模为 1 的问题代价为 $c$。(d) 部分给出了最终得到的递归树（recursion tree）。

接下来，我们把树中每一层（level）的代价相加。最顶层的总代价为 $cn$；往下第二层的总代价为 $c(n/2) + c(n/2) = cn$；再往下一层的总代价为 $c(n/4) + c(n/4) + c(n/4) + c(n/4) = cn$，依此类推。一般地，顶层以下的第 $i$ 层有 $2^i$ 个节点，每个节点贡献代价 $c(n/2^i)$，因此顶层以下第 $i$ 层的总代价为 $2^i \cdot c(n/2^i) = cn$。最底层有 $n$ 个节点，每个节点贡献代价 $c$，总代价为 $cn$。

图 2.5 中递归树的总层数为 $\lg n + 1$，其中 $n$ 是叶子的数目，对应于输入规模（input size）。一个非正式的归纳论证（inductive argument）可以证明这一论断。基本情况（base case）出现在 $n = 1$ 时，此时树只有一层。由于 $\lg 1 = 0$，我们有 $\lg n + 1$ 给出了正确的层数。现在作为归纳假设（inductive hypothesis），假定具有 $2^i$ 片叶子的递归树的层数为 $\lg 2^i + 1 = i + 1$（因为对任何 $i$ 值，都有 $\lg 2^i = i$）。由于我们假设输入规模是 2 的幂，接下来要考虑的输入规模是 $2^{i+1}$。一棵具有 $n = 2^{i+1}$ 片叶子的树，比具有 $2^i$ 片叶子的树多一层，因此总层数为 $(i+1) + 1 = \lg 2^{i+1} + 1$。

为了计算递归式 (2.2) 所表示的总代价，我们只需把各层的代价全部加起来。递归树有 $\lg n + 1$ 层，每层代价为 $cn$，总代价为 $cn(\lg n + 1) = cn\lg n + cn$。忽略低阶项（low-order term）和常数 $c$，就得到想要的结果 $\Theta(n\lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把上面的过程命名为「递归树求和」模板，它有固定的四步：① 把递归式逐层展开成树，节点值等于该处的非递归代价；② 求每层节点之和，寻找“层和”的模式（本例每层恒为 $cn$）；③ 求树高——规模按 $1/b$ 衰减、到常数截止，故高为 $\log_b n$；④ 总代价等于层和乘层数，即 $cn(\lg n + 1)$。模板的能力远不止本例：第 4 章用同一招分析 $T(n) = T(n/3) + T(2n/3) + cn$（层和仍约 $cn$，树高约 $\log_{3/2} n$）与 $T(n) = 2T(n/2) + n^2$（层和成等比数列，不超过 $2n^2$，总代价由根节点主导）——后者正是 6.042J 的几何级数“首项主导”现象。所以拿到任何分治递归式，先别急着套主定理，画三层树找层和模式，主定理的结论往往能被你亲手“看”出来。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段代码在中国数学史上有更早的出处：南宋数学家秦九韶（Qin Jiushao，约 1202–1261）在 1247 年成书的《数书九章》中已系统使用同样的嵌套乘法求多项式的值（据离线维基百科，他被视为独立发现者），比 William George Horner 于 1819 年发表的同一方法早约 570 年，故国内文献常称“秦九韶算法”；维基百科并指出波斯数学家更早知晓，Horner 曾将其归功于 Lagrange。为何这一重排是本质改进？朴素法算每个 $a_k x^k$ 要从头做 $k$ 次乘法，共约 $n(n+1)/2$ 次；嵌套形式每个括号恰一次乘、一次加，共 $n$ 次乘 $n$ 次加，且维基百科指出这已是给定 $x$ 与系数时的乘加次数下限。这再次印证本章主题：同一数学对象的不同计算组织方式，运行时间可差一个量级。习题 (c) 让你用循环不变式证明它，正好再练 p.19 的模板。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 逆序对（inversion）是连接“排序”与“计数”的桥梁概念。为什么插入排序的运行时间由逆序数决定？把 while 循环体执行一次（第 6–7 行）看作“交换相邻的一对逆序元素”，而任何一次相邻交换恰好消去一个逆序对，已排序数组逆序对为零——所以元素移动的总次数恰好等于初始逆序数，运行时间即逆序数加 $\Theta(n)$ 的骨架代价。这与 6.042J 里“置换奇偶性与对换次数”的思想同源：对换是排列的基本生成元，逆序数刻画它到单位排列的“距离”。更漂亮的还在 (d)：用归并排序数逆序对时，跨左右两半的逆序对可在 MERGE 扫描中顺带统计——当右半的元素先于左半某元素被复制走时，它比左半剩余的全部元素都小，一次累加即可——不改变渐近复杂度就得到 $\Theta(n \lg n)$ 的计数算法。这是分治的招牌应用之一：合并步不仅产出排序结果，还白拿一份计数信息。

d. Give an algorithm that determines the number of inversions in any permutation on $n$ elements in $\Theta(n\lg n)$ worst-case time. (Hint: Modify merge sort.)

### Notes for Chapter 2 <span style="color:#2471a3;">**[reference]**</span>

In 1968, Knuth published the first of three volumes with the general title *The Art of Computer Programming* [209, 210, 211]. The first volume ushered in the modern study of computer algorithms with a focus on the analysis of running time, and the full series remains an engaging and worthwhile reference for many of the topics presented here. According to Knuth, the word "algorithm" is derived from the name "al-Khowârizmî," a ninth-century Persian mathematician.

Aho, Hopcroft, and Ullman [5] advocated the asymptotic analysis of algorithms—using notations that Chapter 3 introduces, including $\Theta$-notation—as a means of comparing relative performance. They also popularized the use of recurrence relations to describe the running times of recursive algorithms.

Knuth [211] provides an encyclopedic treatment of many sorting algorithms. His comparison of sorting algorithms (page 381) includes exact step-counting analyses, like the one we performed here for insertion sort. Knuth's discussion of insertion sort encompasses several variations of the algorithm. The most important of these is Shell's sort, introduced by D. L. Shell, which uses insertion sort on periodic subsequences of the input to produce a faster sorting algorithm.

Merge sort is also described by Knuth. He mentions that a mechanical collator capable of merging two decks of punched cards in a single pass was invented in 1938. J. von Neumann, one of the pioneers of computer science, apparently wrote a program for merge sort on the EDVAC computer in 1945.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 冯·诺伊曼（John von Neumann，1903–1957，生于布达佩斯）是横跨纯数学、量子力学、博弈论与计算科学的通才；据离线维基百科，归并排序正是他 1945 年为 EDVAC 编写程序时发明的，1948 年他与 Goldstine 的报告又给出了自底向上版本的详细描述与分析——早期对算法运行时间做认真分析的罕见范例，早于 Aho–Hopcroft–Ullman 推广渐近分析二十多年。动机很有时代感：1938 年发明的机械穿卡归并机（本段提及）能单遍合并两摞穿卡，冯·诺伊曼把这一实务提炼成可分析的算法。至于 Knuth 的《The Art of Computer Programming》：1968 年出第一卷，其定量分析算法运行时间的纲领奠定了现代算法学科；所引 Knuth [211] 即专论排序与查找的后续卷，对排序算法（含 Shell 排序）的百科式梳理是本章最佳延伸读物。

The early history of proving programs correct is described by Gries [153], who credits P. Naur with the first article in this field. Gries attributes loop invariants to R. W. Floyd. The textbook by Mitchell [256] describes more recent progress in proving programs correct.
