# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Session 9（习题课 9）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Session 9（习题课 9）· 主题：dynamic programming（动态规划）· 本文件是题卷，只含五道题面，不含解答</span>

<!-- page 1/3 -->

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 9-1. Coin Crafting（金币铸造）</span>

Ceal Naffrey（西尔·纳夫里）是一名急需用钱的小偷。他最近弄到了 $n$ 枚完全相同的 gold coin（金币）。每枚金币都带有独特的 marking（标记），一旦拿去出手，很容易被认出来是赃物。不过，凭着他那点业余 craftsman（匠人）手艺，Cael 可以把金币 melt down（熔掉），改铸成别的 golden object（黄金制品）。Ceal 有一个买家，愿意按不同的 rate（价码）收购黄金制品，但同一种制品只买一件。Ceal 已把这 $n$ 件黄金制品编成一张清单，逐件写明两样东西：买家愿意为它支付的 purchase price（买价），是一个正整数（positive integer）；以及它的 melting number（熔铸数），也是一个正整数——即铸造这一件需要熔掉多少枚金币。给定这张清单，描述一个高效的 algorithm（算法），求出 Ceal 通过熔掉手里的金币、铸成黄金制品卖给买家所能取得的 maximum revenue（最大收入）。

> <span style="color:#7f8c8d;">〔原文人名拼写自身不一致：首句作 `Ceal Naffrey`，随后四处作 `Ceal`，中间一处作 `Cael`。译文按原样保留，未作统一——这不是录入错误，而是原文如此。〕</span>

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 9-2. Career Fair Optimization（招聘会最优化）</span>

Tim the Beaver（海狸蒂姆）每场 career fair（招聘会）都到场，不是为了找工作，而是为了领 free swag（免费赠品）。招聘会上有 $n$ 个 booth（摊位），每个摊位发放一种已知类型的赠品。要从 booth $i$ 领到一件赠品，需要在那个摊位前排队 $t_i$ 分钟（$t_i$ 为整数）；该摊位的赠品带有整数 coolness（酷值）$c_i$ 与整数 weight（重量）$w_i$。从一个摊位领到一件赠品之后，Tim 要花整整 $1$ 分钟才能重新排进队里——排同一个摊位或任何别的摊位都一样。Tim 的 backpack（背包）最多能装下总重量 $b$ 的赠品；但任何时刻 Tim 都可以花整数 $h$ 分钟跑回家、把背包腾空、再返回招聘会，而重新排进队里还要另花 $1$ 分钟。已知这场招聘会恰好持续 $k$ 分钟，描述一个 $O(nbk)$ 时间的 algorithm（算法），求出 Tim 在这场招聘会期间能领到的赠品的 maximum total coolness（最大总酷值）。

> <span style="color:#7f8c8d;">〔原抽取串：`having integer coolness ci and integer weight wi`、`standing in line at that booth for integer ti minutes`。上标在文字层丢失，按数学意义重建为 $c_i$、$w_i$、$t_i$。〕</span>

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 9-3. Protein Parsing（蛋白质解析）</span>

Prof. Leric Ander（莱里克·安德教授）的实验室做 DNA 实验。对任何一条 DNA strand（DNA 链，即一串 nucleotide（核苷酸），取值为 A、C、G 或 T）做过实验之后，实验室会把它切成若干段，以便其中任何有用的 protein marker（蛋白质标记）都能用于后续实验。Ander 的实验室编好了一张已知蛋白质标记的清单 $P$，其中每个蛋白质标记都对应一条长度至多 $k$ 个核苷酸的序列。对一条 DNA 链 $S$ 的一个 division（切分）是一个有序序列 $D = (d_1, \dots, d_m)$，每一项都是 DNA 链，且把 $D$ 按序 concatenation（拼接）起来正好得到 $S$。一个切分 $D$ 的 value（价值）是 $D$ 中那些作为蛋白质标记出现在 $P$ 里的 DNA 链的条数。给定一条 DNA 链 $S$ 与蛋白质标记的集合 $P$，描述一个 $O(k(|P| + k|S|))$ 时间的 algorithm（算法），求出 $S$ 的所有切分中可能的最大价值。

> <span style="color:#7f8c8d;">〔原抽取串：`D = (d1, . . . , dm)`。下标在文字层丢失，按数学意义重建为 $d_1, \dots, d_m$。〕</span>

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 9-4. Lazy Egg Drop（懒惰的鸡蛋下落）</span>

经典的 egg drop problem（鸡蛋下落问题）问的是：一栋有 $n$ 层的楼，手头至多 $k$ 个 egg（鸡蛋），至少要做多少次 drop（下落）才能确定 breaking floor（破裂楼层）——所谓破裂楼层，就是从这一层丢下鸡蛋会摔碎的最低那一层。这个问题有 closed form（闭式）解，但也能用 dynamic programming（动态规划）求解（原文在此处标注 `(Exercise!)`，即留作练习）。然而，如果这栋楼没有 elevator（电梯），人们想要的也许反而是最小化 total drop height（总下落高度）：即所有鸡蛋被丢下时所在高度的总和。设这栋楼的 $n$ 层各有已知的正整数 height（高度）$h_i$，且楼层高度随 $i$ 严格递增。给定这些高度，描述一个 $O(n^3k)$ 时间的 algorithm（算法），返回在用至多 $k$ 个鸡蛋确定该楼破裂楼层的前提下，所需的最小 total drop height（总下落高度）。

> <span style="color:#7f8c8d;">〔原抽取串：`known positive integer height hi`、`describe an O(n3k)-time algorithm`。上标在文字层丢失，按数学意义重建为 $h_i$、$O(n^3k)$。〕</span>

<!-- page 2/3 -->

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 9-5. Building a Wall（砌一堵墙）</span>

Problem Session 2 里那片 Porkland（猪肉国）的猪，决定沿着南边国界砌一堵 stone wall（石墙），用来挡住凶恶的 wolf（狼）。这堵墙厚 $1$ 米、长 $n$ 米、高至多 $k$ 米。墙由一大批完全相同的 long stone（长石）砌成：每块长石是一个 $1 \times 1 \times 2$ 米的 rectangular prism（长方体）。长石在墙里既可以竖着摆，也可以横着摆。费很大力气，可以把一块长石敲成两块 $1$ 米见方的 cube stone（方石），但只要可能，猪们并不想用方石。

> <span style="color:#7f8c8d;">〔原抽取串：`each a 1 � 1 � 2 meter rectangular prism`。`�` 是 `×`（U+00D7）在文字层的抽取损失，按数学意义重建为 $1 \times 1 \times 2$。〕</span>

Porkland 南边国界的地面高低不平，不过猪们已经把国界上每一平方米的地都整平到整数米的 elevation（高程）。称一个 border plan（边界规划）为一个 $n \times k$ 的 array（数组）$B$，它描述的是墙还没砌起来时国界的模样。$B[j][i]$ 对应的是这样一格 cubic meter（立方米格）：它的顶面在高程 $k - j$ 处，位于沿国界方向第 $i$ 米处。若这一格是空的、必须被石头盖住，则 $B[j][i]$ 为 `'.'`；若这一格里是 dirt（泥土）、因而本就不该被盖住，则 $B[j][i]$ 为 `'#'`。$B$ 具有这样的性质：若 $B[j][i]$ 被泥土占据，则它下面的每一格 $B[t][i]$ 也都被泥土占据（$t \in \{j, \dots, k - 1\}$）；并且每一列最上面那一格 $B[0][i]$ 初始都是空的。下面是 $n = 10$、$k = 5$ 时一个 $B$ 的例子。

> <span style="color:#7f8c8d;">〔原抽取串：`an n � k array B`、`for t  {j, . . . , k - 1}`。`×` 与 `∈` 在文字层均丢失，按数学意义重建为 $n \times k$ 与 $t \in \{j, \dots, k-1\}$。〕</span>

向边界规划 $B$ 中摆放石头的一次 placement（摆放）是一组 placement triple（摆放三元组）：

- `(i,j,'1')` 放一块方石，盖住 $B[j][i]$；

- `(i,j,'D')` 放一块朝向 down（向下）的长石，盖住 $B[j][i]$ 与 $B[j+1][i]$；以及

- `(i,j,'R')` 放一块朝向 right（向右）的长石，盖住 $B[j][i]$ 与 $B[j][i+1]$。

若 $B$ 中每一个空的立方米格都被某块石头盖住，则称这次摆放是 complete（完备）的；若没有任何立方米格被一块以上的石头盖住、也没有任何石头压到泥土上，则称它是 non-overlapping（不重叠）的。下面给出该 $B$ 的一个完备、不重叠、且恰好用了 $2$ 块方石的摆放，以及它的图示。

```text
B = [
    '..........',
    '..........',
    '..........',
    '.....#.##.',
    '..#..####.',
]

P = [
    (0,0,'D'), (0,2,'D'), (0,4,'R'), (1,0,'R'), (1,1,'R'),
    (1,2,'1'), (1,3,'R'), (2,2,'R'), (3,0,'D'), (3,3,'R'),
    (3,4,'R'), (4,0,'R'), (4,1,'R'), (4,2,'R'), (6,0,'D'),
    (6,2,'R'), (6,3,'1'), (7,0,'D'), (8,0,'D'), (8,2,'R'),
    (9,0,'D'), (9,3,'D'),
]
```

![边界规划 B 与其一个完备、不重叠、只用 2 块方石的摆放（原 PDF 第 2 页插图，300 dpi 裁切保留）](data:image/png;base64,FIGURE1_BASE64_PLACEHOLDER)

> <span style="color:#7f8c8d;">**Figure（图）· 边界规划 B 与摆放 P（border plan B and placement P）:** 横轴 $i = 0, \dots, 9$ 是沿国界方向的米数，纵轴 $j = 0, \dots, 4$ 是行号，$j = 0$ 在最上（顶面高程 $k - 0 = 5$ 米），$j = 4$ 在最下（顶面高程 $1$ 米）。深色（near-black）方格是 dirt（泥土），即 $B[j][i] = $ `'#'` 的那些格：第 $3$ 行在 $i = 5, 7, 8$ 处，第 $4$ 行在 $i = 2, 5, 6, 7, 8$ 处，共 $8$ 格。浅色空格是必须被盖住的 empty（空的）立方米格，共 $42$ 格——这 $42$ 格正是本次摆放 $P$ 的覆盖目标（$22$ 块石头，其中长石占 $20$ 块、方石占 $2$ 块，$20 \times 2 + 2 \times 1 = 42$）。图中在空白格里画出的粗线，就是 $P$ 中每一块石头的边界：竖放长石（`'D'`）在相邻两行里占同一列，横放长石（`'R'`）在相邻两列里占同一行，方石（`'1'`）只占一格。</span>

> <span style="color:#7f8c8d;">同一张图的 ASCII 文字版（供纯文本检索对照，信息与上图一致）：</span>

```text
        i=0  1  2  3  4  5  6  7  8  9
j=0      ·  ·  ·  ·  ·  ·  ·  ·  ·  ·
j=1      ·  ·  ·  ·  ·  ·  ·  ·  ·  ·
j=2      ·  ·  ·  ·  ·  ·  ·  ·  ·  ·
j=3      ·  ·  ·  ·  ·  ■  ·  ■  ■  ·
j=4      ·  ·  ■  ·  ·  ■  ■  ■  ■  ·
（· = empty（空的），■ = dirt（泥土））
```

**(a)** 给定一个 $n \times k$ 的 border plan（边界规划）$B$，描述一个 $O(2^{2k}kn)$ 时间的 algorithm（算法），返回 $B$ 的一个 complete（完备）、non-overlapping（不重叠）、且所用 cube stone（方石）数尽可能少的 placement（摆放）。

> <span style="color:#7f8c8d;">〔原抽取串：`an O(22kkn)-time algorithm`。指数位在文字层丢失，按数学意义重建为 $O(2^{2k}kn)$。〕</span>

**(b)** 写一个 Python function（函数）`build_wall(B)`，实现你在 (a) 中的 algorithm（算法），只针对 $k = 5$ 的 border plan（边界规划）。

> <span style="color:#7f8c8d;">〔原抽取串：`Write a Python function build wall(B)`。下划线在文字层丢失，重建为 `build_wall(B)`；原始题面在此处把 `for border plans with k = 5` 加粗强调。〕</span>

<!-- page 3/3 -->

---

<span style="color:#2471a3;">**[source]**</span> **Source（来源）:** MIT OpenCourseWare — https://ocw.mit.edu

**6.006 Introduction to Algorithms（算法导论）** — Spring 2020 · [Terms of Use](https://ocw.mit.edu/terms)
