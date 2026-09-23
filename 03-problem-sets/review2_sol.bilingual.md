# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology
Instructors: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Quiz 2 Review（第 2 次测验复习）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Quiz 2 Review Solutions（第 2 次测验复习解答）· 范围：L09-L14 图算法六讲 + PS5-PS6 · 对应 CLRS §22（图的基本算法）、§24（单源最短路径）、§25（全对最短路径）</span>

---

### <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Scope（考试范围）</span>

- Quiz 1 material（第 1 次测验内容）仍属于 fair game（可考范围），但明确不作为重点强调
- 图算法共 6 讲：L09-L14，2 个 Problem Set：PS5-PS6

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条范围界定背后有一个常被忽略的课程设计细节：正常的 6.006 Quiz 2 覆盖 3 个 Problem Set 的图算法内容，但 2020 春的这门课只覆盖了 2 个（PS5+PS6）。🎥 *Jason Ku 在复习课开场专门提醒*："Now, usually this material covers three problem sets worth of material. This term, it's covering two problem sets worth of material. So just keep that in mind when you're studying and you want to go look back on previous material."（翻译：通常这部分内容覆盖三个习题集的量，但这学期只覆盖了两个，所以你在复习和回看往年材料时要记住这一点。）这意味着你拿往年 Quiz 2 真题练习时，有些题目用到的知识点（比如更复杂的图修改技巧）当年考了但你没学——不是你的漏洞，是课程范围确实被压缩了。六讲课的内部递进逻辑是「**遍历（L09-L10 BFS/DFS，含拓扑排序与环检测）→ 加权最短路（L11 DAG 松弛 → L12 Dijkstra → L13 Bellman-Ford）→ 全对最短路（L14 Johnson）**」，这恰好对应 CLRS 的 §22（图基本算法）和 §24（单源最短路）。注意 §22.4 的拓扑排序证明使用了 DFS 完成时间逆序，这个结论在 L11（Weighted Shortest Paths，加权最短路）中被复用为 DAG 松弛正确性的前提——**BFS/DFS 不只是"遍历工具"，它们是最短路算法的地基**。建议复习时先把 BFS 的 level-set invariant（层级不变量）和 DFS 的 parenthesis theorem（括号定理）这两个来自 6.042J 图论的结论复述一遍：前者解释了为什么无权图的最短路就是最少边数，后者解释了为什么拓扑序中所有边方向一致——这两个不变量是所有后续算法正确性证明的共同出发点。

---

### <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Graph Problems（图问题）</span>

- Graph reachability（图可达性）：BFS 或 DFS 在 $O(|E|)$ 时间内完成
- Graph exploration（图探索）/ connected components（连通分量）：通过 Full-BFS 或 Full-DFS
- Topological sort（拓扑排序）/ Cycle detection（环检测）：通过 DFS
- Negative-weight cycle detection（负权环检测）：通过 Bellman-Ford
- Single Source Shortest Paths（SSSP，单源最短路径）

| Restrictions（限制条件） | SSSP Algorithm（单源最短路算法） | Running Time（运行时间）$O(\cdot)$ |
|:---|:---|:---|
| DAG, Any weights（有向无环图，任意权重） | DAG Relaxation（DAG 松弛） | $\|V\| + \|E\|$ |
| General（一般图） | Unweighted（无权） | BFS | $\|V\| + \|E\|$ |
| General（一般图） | Non-negative（非负权） | Dijkstra | $\|V\| \log \|V\| + \|E\|$ |
| General（一般图） | Any（任意权重） | Bellman-Ford | $\|V\| \cdot \|E\|$ |

- All Pairs Shortest Paths（APSP，全对最短路径）
  - 把某个 SSSP 算法运行 $|V|$ 次
  - Johnson 算法以 $O(|V|^2 \log |V| + |V||E|)$ 解决含负权图的 APSP

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这张表是整个测验的**算法选择决策树**——它编码了一条第一性原理：**对图结构的限制越强，能用的算法越快**。🎥 *Jason Ku 在复习课上用一句话给出了选算法的实战原则*："In general, you want to choose an algorithm that's higher on this list. But sometimes, the algorithms higher on this list don't apply. If on a quiz, you come to a graph for which it's not a DAG, but you use DAG relaxation, that's no longer a correct algorithm."（翻译：一般来说你要选表里靠上的算法，但有时候靠上的算法不适用——如果你在测验里碰到一个不是 DAG 的图却用了 DAG 松弛，那算法就不正确了。）这条建议的深层含义是：**正确性优先于效率**——当你拿不准图的属性时，退到 Bellman-Ford 至少能拿正确性分。四种算法的递进对应 CLRS §24 的四节结构，注意精确编号：DAG 最短路由 §24.2 覆盖（线性时间，前提是无环）、Dijkstra 在 §24.3（贪心策略依赖边权非负、用优先队列实现 $O((|V|+|E|)\log|V|)$）、Bellman-Ford 在 **§24.1**（§24.4 是差分约束系统，§24.5 是正确性证明汇总，不是 Bellman-Ford 本身）。APSP 的 Johnson 算法在 §25.3，先用 Bellman-Ford 做一轮重赋权（rewight），使所有权重非负，再跑 $|V|$ 次 Dijkstra——这是「用一次昂贵的全局预处理换 $|V|$ 次便宜的局部计算」的经典策略，和你之后在 CS144 路由协议里看到的 link-state（链路状态）算法有结构上的同源性。[我的卡点]：注意 BFS 行和 DAG 松弛行的边界——BFS 列在「无权」那行，但 BFS 也能跑在 DAG 上，考试时如果图既是 DAG 又是无权，**两者都是 $O(|V|+|E|)$，选 BFS 更简单**。

---

### <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Graph Problem Strategies（图问题策略）</span>

- Be sure to explicitly describe a graph（务必显式描述图）——用问题的参数来定义图
- 把问题转化为：找 shortest path（最短路）、cycle（环）、topological sort（拓扑排序）、connected components（连通分量）等
- 可以**复制顶点**（duplicate graph vertices）来编码额外信息
- 可以**添加辅助顶点/边**（auxiliary vertices/edges）到图中
- 可以**预处理图**（pre-process the graph），例如删掉图的一部分

### <span style="color:#2471a3;">**[section]**</span> <span style="color:#c0392b">Graph Problem Common Mistakes（图问题常见错误）</span>

- **Define your graphs!（一定要定义你的图！）** 明确说明 vertices（顶点）、edges（边）和 weights（权重），并数清楚它们的数量
  - （例如：构造图 $G = (V, E)$，每个……对应一个顶点，每条……对应一条从 $u$ 到 $v$、权重为 $w$ 的有向边）
- **陈述你要解决的问题**，而不是只说你用来解它的算法
  - （例如：通过运行 DAG Relaxation 从 $s$ 求解 SSSP……）
- **把你解的图问题连回原问题**
  - （例如：$G$ 中从 $s$ 到 $t$ 的路径权重对应沿途缴纳的过路费之和，所以最小权重路径对应最小化过路费的行车路线）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这组「常见错误」可以提炼为一个可复用的**图问题答题框架：建模（Model）→ 陈述（State）→ 回连（Connect）**。第一步要求你写出 $V$、$E$、$w$ 三者各自的基数数量级——这不是卫生习惯，而是复杂度证明的硬需求：你必须知道 $|V|$ 和 $|E|$ 是多少，才能代入算法复杂度公式。第二步「陈述要解的问题」的价值在于**把算法选择和问题定义解耦**——🎥 *Jason Ku 解释了这个评分逻辑*："separating off the problem from your implementation of how you solve that problem can maybe help you get some points for stating the problem you're solving, even if you choose the wrong or an inefficient way to solve it."（翻译：把问题和你的解法实现分开，可能帮你在选错算法或用低效算法时仍然拿到陈述问题的分数。）评分 rubric 实际上是按步骤拆分的：定义图 → 修改图 → 识别问题类型 → 选正确算法 → 分析运行时间 → 连接回原问题，每一步独立给分。第三步「回连」是正确性论证的核心——你需要一句话说明**图上结论与原问题结论之间的双射关系**（例如「最短路径权重 = 最少过路费」）。这个三步框架本质上是数学建模的通用范式——你在 Strang《Linear Algebra and Learning from Data》里看到的 modeling（建模）思路（把现实问题翻译成矩阵运算、求解后再把答案翻译回现实）与它共享同一骨架，只不过这里翻译的目标语言是图论。你在 [prob8sol] 和 [r15]/[r16] 里已经反复使用这个框架：四道题全部是先构造图或 DP 结构、再跑标准算法、最后把图上的解翻译回原问题。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 1. Counting Blobs（数连通块，S18 Quiz 2）</span>

一个 image（图像）是黑白方形像素组成的 2D 网格（grid），每个白色像素都属于某个 blob（连通块）。两个白色像素**共享网格的一条边**时，它们属于同一个 blob。黑色像素不属于任何 blob。给定表示图像的一个 $n \times m$ array（数组），描述一个 $O(nm)$ 时间的 algorithm（算法）来数出图像中 blob 的个数。

> **[solution] Solution（解答）:**
>
> 构造一个图 $G$：每个白色像素对应一个顶点，若两个顶点对应的像素都是白色且共享网格的一条边，则在它们之间连一条 undirected edge（无向边）。这个图的规模至多为 $O(nm)$ 个顶点、至多 $O(nm)$ 条边（因为每个像素至多与其他四个像素共享边），所以可以在 $O(nm)$ 时间内构造完成。该图的每个 connected component（连通分量）恰好对应一个 blob，因此运行 Full-BFS 或 Full-DFS 在 $O(nm)$ 时间内数出 $G$ 中连通分量的个数即可。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题是「把非图问题建模成图」的入门模板，建模动作只有两个：**对象变顶点、相邻关系变边**。这里"相邻"的定义是题目里唯一的隐藏决策——题目特意强调「共享一条边」而不是「共享一个角」，如果你把对角相邻也算进去，图就会多出斜边，blob 的答案就错了。这提醒你：建模时必须**逐字检查题目给的关系定义**。复杂度论证的妙处在第二条：每个顶点度数不超过 4（上下左右），所以边数自动是 $O(nm)$ 而不是最坏 $O((nm)^2)$——平面网格的结构天然压住了边数。这与你在 CLRS §22.3 看到的 DFS 分析是同一套路：**先数顶点，再借度数或结构数边**。Full-BFS/Full-DFS 与普通 BFS/DFS 的区别只在于外层多包一层循环，让未访问的顶点重新作为起点，从而遍历整个图（包括不连通部分）——这正是 6.042J 图论里 connected component（连通分量）的算法实现：分量是"可达性"关系的等价类，Full-DFS 就是逐类访问。像素图变图的做法在图像处理里很常见，比如 connected-component labeling（连通域标记）就是图像学里给每个 blob 编号的标准操作。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 2. Unicycles（单环图，S18 Quiz 2）</span>

给定一个 connected undirected graph（连通无向图）$G = (V, E)$，边权 $w: E \to \mathbb{Z}^+$ 严格为正，且 $|E| = |V|$，描述一个 $O(|V|)$ 时间的 algorithm（算法），求从 vertex $s$ 到 vertex $t$ 的最小权重 path（路径）。

> **[solution] Solution（解答）:**
>
> 给定一棵带正权边的 weighted tree（加权树）中的两个顶点，它们之间有**唯一**的 simple path（简单路径），这条路径也正是最小权重路径。从任一源点 $s$ 在树中做 depth-first search（深度优先搜索）得到一棵 directed DFS tree（有向 DFS 树），耗时 $O(|V|)$（因为 $|E| = |V| - 1$）。然后按该有向 DFS 树的 topological sort order（拓扑排序序）relax（松弛）边，即可在 $O(|V|)$ 时间内算出从 $s$ 出发的最小权重路径。由于 $G$ 恰好有一个 cycle（环），我们的策略是：**删掉一条边打破这个环**，然后在所得树上计算从 $s$ 到 $t$ 的最小权重路径。
>
> 首先，从 $s$ 运行 depth-first search 找到环上离 $s$ 最近的顶点 $v$，耗时 $O(|V|)$（因为 $|E| = |V|$）。环上有一条边 $e_1$ 不会出现在 DFS 返回的树中（它是回到 $v$ 的 back edge，回边），而环上与 $v$ 关联的另一条边是 DFS 树的单条出边 $e_2$。如果 $s$ 就在环上，则 $v = s$；否则从 $s$ 到 $v$ 的唯一路径既不经过 $e_1$ 也不经过 $e_2$。
>
> 从 $s$ 到 $t$ 的最短路径不可能同时经过 $e_1$ 和 $e_2$，否则该路径会至少两次访问 $v$，从而绕出一个正权重的环。删掉 $e_1$ 或删掉 $e_2$ 都会得到一棵树，其中至少一棵包含从 $s$ 到 $t$ 的最小权重路径。因此，用上述算法分别在这两棵树中求从 $s$ 到 $t$ 的最小权重路径，返回两者中较小者，总时间 $O(|V|)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题的第一性原理入口是**树的最小边数定理**——在 6.042J 的图论中你会学到：连通无向图若要连通 $|V|$ 个顶点，最少需要 $|V|-1$ 条边，达到这个下界的就是树；而本题 $|E|=|V|$ 恰好比树多一条，所以 $G$ 是「一棵树 + 一条额外边」，这条边在树上画出唯一的环。这种图的 cycle rank（环秩 / 圈秩，有时叫 cyclomatic number 或 Betti number）定义为 $|E|-|V|+1=1$，是图论中衡量「图离树有多远」的基本不变量。**正权条件是解题的真正钥匙**：因为所有权重严格为正，绕环走一圈只会增加总权重，所以树中的唯一简单路径自动就是最小权重路径。如果没有正权条件，环上出现零权或负权边时，绕环就可能不增加甚至减少权重，树的唯一简单路径就不再保证是最短路。解法的核心是一个可复用建模模板——**在图上定位"唯一违规结构"（本题是环），枚举破坏它的方式（删 $e_1$ 或 $e_2$），将问题退化到"干净结构"（树）上求解**。🎥 *Jason Ku 在讲解中给出了这个模板的简化实现*："find this thing S prime on the cycle, find the outgoing two edges here, remove one, and then do my tree searching... I get rid of this edge. And I do that once. And I do it again without this edge."（翻译：找到环上的这个顶点 $s'$，找到它的两条出边，删掉一条，然后做树搜索……我删掉这条边试一次，再删掉另一条再试一次。）——他删掉 $s'$（离 $s$ 最近的环上顶点）的两条环边之一各试一次，每次在所得树上跑可达性即可，至多 2 次 $O(|V|)$。注意为什么只试两条边就够了：任何 $s$-$t$ 简单路径至多经过环上两条边中的一条（因为一旦经过 $v$ 就不能回头），删除两条边各自得到的树恰好覆盖了两种候选路径。[我的卡点]：DFS 的 back edge（回边）是定位环的机制——在无向连通图中跑 DFS，**恰好一条**边不会出现在 DFS 树中（因为 $|E|=|V|$ 而树有 $|V|-1$ 条边），这条边就是环上的关键边。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 3. Doh!-nut（多纳圈，S18 Quiz 2）</span>

Momer（荷马·辛普森梗）刚在 FingSprield 发电厂（斯普林菲尔德）的 location $p$（位置）下班，需要开车回 location $h$（家）。但沿途如果他的行车路线**任何时候**驶入离某家 doughnut shop（甜甜圈店）driving distance（行驶距离）$k$ 以内，他就会停下来吃甜甜圈，他的妻子 Harge 会生气。Momer 知道 FingSprield 的布局，可以建模为一组 $n$ 个位置，一些位置对之间有已知行驶距离的双向道路（可假设**每个位置至多与五条道路相连**），以及城里 $d$ 家甜甜圈店的位置。描述一个 $O(n \log n)$ 时间的 algorithm（算法），找出一条从发电厂回家的、避开「距甜甜圈店行驶距离 $k$ 以内」区域的最短行车路线（或者判断这样的路线不存在）。

> **[solution] Solution（解答）:**
>
> 构造一个图 $G$：每个城市位置对应一个顶点，两个位置之间有道路则在它们之间连一条 undirected edge（无向边），每条边以对应道路的正向长度为权重。每个顶点的 degree（度数）被常数（即 5）限制住，所以 $G$ 的边数是 $O(n)$。第一步，找出距甜甜圈店位置行驶距离 $k$ 以内的顶点：创建一个 auxiliary vertex（辅助顶点）$x$，从 $x$ 向每家甜甜圈店位置连一条 0 权重的出边，然后从 $x$ 运行 Dijkstra。把图中所有「从 $x$ 的最短路径长度 $\le k$」的顶点删掉，得到 $G' \subset G$。如果 $p$ 或 $h$ 不在 $G'$ 中，则不存在这样的路线。否则在 $G'$ 中从 $p$ 运行 Dijkstra；如果到 $h$ 没有路径，则不存在有效路线；否则 Dijkstra 找到了从 $p$ 到 $h$ 的最短路径，通过 parent pointers（父指针）返回它。这个算法运行了两次 Dijkstra。由于两种图的规模都是 $O(|V|)$，Dijkstra 的运行时间为 $O(|V| \log |V|) = O(n \log n)$（例如用 binary heap（二叉堆）实现 priority queue（优先队列））。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题是「辅助顶点建模」中最经典的**超级源点（super-source）归约**：当你需要同时从多个源点计算最短路径时，添加一个虚拟顶点 $x$，用 $0$ 权有向边连向所有真实源点，然后从 $x$ 跑一次 SSSP——$x$ 到某顶点的最短距离恰好等于**到最近真实源点**的距离。这个归约成立有三个前提：①边权非负（否则 $0$ 权边可能被负权边"穿越"，Dijkstra 的贪心不变量被破坏）；②边是有向的（从 $x$ 出发但不回到 $x$，否则超级源点可能被"回灌"）；③所有真实源点地位相同（共享同一个禁区半径 $k$）。🎥 *Jason Ku 在板书中讨论了当③不成立时的推广*："What if each donut shop had an amount that Momer liked it? ... I can just make the distance of this frontier for each one of the donut shops the same by modifying the distance of the incoming edge."（翻译：如果每家甜甜圈店有不同的吸引力，导致不同的危险半径呢？我可以通过调整超级源点入边的权重，让每家店的前沿距离变得一样。）——具体做法：设最大半径为 $k_{\max}$，该店连 $0$ 权边；其他店 $i$ 连 $k_{\max}-k_i$ 权边，搜索时阈值统一为 $k_{\max}$。这本质上是用边权差异"吸收"了各店半径差异，使 Dijkstra 仍然一次完成。修剪后的问题变成**不含禁区顶点的普通最短路**——这是预处理（preprocessing）策略的教科书应用：把路径约束（"不能在距离甜甜圈店 $k$ 以内"）转化为图的结构修改（"危险顶点根本不存在"），于是剩下的只是标准 Dijkstra。两处复杂度保障同出一源：度数上界 5 使 $|E|=O(n)$（和 Problem 1 的平面网格度数上界同理），Dijkstra 在稀疏图上是 $O(n\log n)$。这个「超级源点 + 修剪」的组合模式在你之后的系统学习中会反复出现：CS144 的 multicast（多播）路由、甚至操作系统中多进程同步的「屏障」抽象，都共享同一归约骨架。

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 4. Long Shortest Paths（长最短路径）</span>

给定具有 arbitrary edge weights（任意边权）$w: E \to \mathbb{Z}$ 的 directed graph（有向图）$G = (V, E)$，以及两个顶点 $s, t \in V$，描述一个 $O(|V|^3)$ 时间的 algorithm（算法），求从 $s$ 到 $t$ 的、**至少包含 $|V|$ 条边**的任意路径的最小权重。

> **[solution] Solution（解答）:**
>
> 我们的策略是对每个顶点 $v \in V$ 计算两个中间值：
> 1. $w_1(v)$：从 $s$ 到 $v$、**恰好用 $|V|$ 条边**的任意路径的最小权重；以及
> 2. $w_2(v)$：从 $v$ 到 $t$、用**任意条边**的路径的最小权重。
>
> 首先，为了计算 (1)，我们构造一个类似 Bellman-Ford 的 duplicated graph（复制图），但不含「停留在同一顶点」的边。具体来说，构造图 $G_1$：
>
> - 对每个顶点 $v \in V$ 建 $|V| + 1$ 个顶点：顶点 $v_k$（$k \in \{0, \ldots, |V|\}$）表示「从 $s$ 出发沿一条含 $k$ 条边的路径到达 $v$」；
> - 对每条边 $(u, v) \in E$ 建 $|V|$ 条边：边 $(u_{k-1}, v_k)$，权重与原边相同，$k \in \{1, \ldots, |V|\}$。
>
> 现在，$G_1$ 中从 $s_0$ 到 $v_{|V|}$（对任意 $v \in V$）的路径，恰好对应 $G$ 中从 $s$ 到 $v$ 的、恰含 $|V|$ 条边的路径。所以在 $G_1$ 中从 $s_0$ 求解 SSSP，即可算出到达每个顶点、恰好经过 $|V|$ 条边的最小权重。这个图是 acyclic（无环）的，规模为 $O(|V|(|V| + |E|)) = O(|V|^3)$，因此可以通过 DAG relaxation（DAG 松弛）在 $O(|V|^3)$ 时间内解 $G_1$ 上的 SSSP。
>
> 其次，为了计算 (2)，我们从 $G$ 构造新图 $G_2$：把所有边反向。于是 $G$ 中每条「到达 $t$」的路径都对应 $G_2$ 中从 $t$ 出发的路径，因此在 $G_2$ 中从 $t$ 运行 SSSP，即可算出 $G$ 中从任意 $v$ 到 $t$、用任意条边的最小权重，这可以用 Bellman-Ford 在 $O(|V||E|) = O(|V|^3)$ 时间内完成。
>
> 计算完成后，对所有顶点 $v \in V$ 求 $w_1(v) + w_2(v)$ 的最小值，即为从 $s$ 到 $t$、至少含 $|V|$ 条边的最小权重路径——因为每条这样的路径都可以分解为「前 $|V|$ 条边」加「剩余部分」。这个循环耗时 $O(|V|)$，所以算法总运行时间为 $O(|V|^3)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本题是**分层图（layered graph / state-space graph）**建模的完整展示——它把「路径边数」这个原本在算法运行中动态追踪的量，**物化（reify）为图结构的静态维度**。$G_1$ 的第 $k$ 层顶点 $v_k$ 编码状态「恰好经过 $k$ 条边到达 $v$」，层间边 $(u_{k-1}, v_k)$ 是一次状态转移；于是「恰好 $|V|$ 条边的最短路」从「带约束的最短路」退化为「分层 DAG 上的无约束最短路」，可以直接用 $O(|V|+|E|)$ 的 DAG 松弛秒杀——因为层编号 $k$ 天然给出了拓扑序。这与 [lec16] 的动态规划完全同构：$v_k$ 就是子问题「用恰好 $k$ 条边到达 $v$ 的最小权重」，DP 递推式 $d(v_k) = \min_{(u,v)\in E} \{ d(u_{k-1}) + w(u,v) \}$，拓扑序就是 $k=1,2,\ldots,|V|$——**分层图 = DP 的状态转移图**。🎥 *Jason Ku 用一句话拆解了「至少」到「恰好」的转换*："If I want a path that goes through at least the edges, some prefix of that path uses exactly v edges."（翻译：如果我想要一条至少经过这么多条边的路径，它的某个前缀恰好使用了 $v$ 条边。）——"至少 $|V|$ 条"被分解为「前缀恰好 $|V|$ 条 ($w_1$) + 后缀任意条 ($w_2$)」，对所有中间顶点 $v$ 取 $w_1(v)+w_2(v)$ 的最小值。$G_2$（反向图）的作用是把"从所有 $v$ 到 $t$"这个多源问题归约为从 $t$ 出发的单源问题——边的方向反转后，$G$ 中入边变出边，路径可逆跟踪。值得深入对比的是 CLRS §24.1 的 Bellman-Ford：它的第 $k$ 轮外层循环本质就是在隐式地维护「至多 $k$ 条边的 $\delta_k(s,v)$」；本题把这个隐式结构**显式化为分层图**，换来了精确的边数控制（「恰好」而非「至多」）和 DAG 上的线性时间——代价是图规模膨胀到 $O(|V|^3)$。[我的卡点]：为什么 $G_1$ 是无环的？因为每条边的 $k$ 严格递增（$k-1 \to k$），层编号单调，不存在"向后走"的边——这是分层图自动无环的根本原因，也是 DAG 松弛能用的前提。

---

MIT OpenCourseWare
https://ocw.mit.edu

6.006 Introduction to Algorithms
Spring 2020

> <span style="color:#7f8c8d;">For information about citing these materials or our Terms of Use, visit: https://ocw.mit.edu/terms（引用须知与使用条款见 MIT OCW 官网）</span>
