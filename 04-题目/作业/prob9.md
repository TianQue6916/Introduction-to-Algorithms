# Introduction to Algorithms: 6.006（算法导论）

Massachusetts Institute of Technology（麻省理工学院）
Instructors（授课教师）: Erik Demaine（埃里克·德梅因）, Jason Ku（顾杰森）, and Justin Solomon（贾斯汀·所罗门）

## <span style="color:#2471a3;">**[session]**</span> <span style="color:#c0392b">Problem Session 9（习题课 9）</span>

> <span style="color:#7f8c8d;">MIT 6.006 Spring 2020, Problem Session 9（习题课 9）· 主题：dynamic programming（动态规划）· 本文件是题卷，只含五道题面，不含解答</span>

<!-- page 1/3 -->

---

### <span style="color:#2471a3;">**[problem]**</span> <span style="color:#c0392b">Problem 9-1. Coin Crafting（金币铸造）</span>

Ceal Naffrey（西尔·纳夫里）是一名急需用钱的小偷。他最近弄到了 $n$ 枚完全相同的 gold coin（金币）。每枚金币都带有独特的 marking（标记），一旦拿去出手，很容易被认出来是赃物。不过，凭着他那点业余 craftsman（匠人）手艺，Cael 可以把金币 melt down（熔掉），改铸成别的 golden object（黄金制品）。Ceal 有一个买家，愿意按不同的 rate（价码）收购黄金制品，但同一种制品只买一件。Ceal 已把这 $n$ 件黄金制品编成一张清单，逐件写明两样东西：买家愿意为它支付的 purchase price（买价），是一个 positive integer（正整数）；以及它的 melting number（熔铸数），也是一个正整数——即铸造这一件需要熔掉多少枚金币。给定这张清单，描述一个高效的 algorithm（算法），求出 Ceal 通过熔掉手里的金币、铸成黄金制品卖给买家所能取得的 maximum revenue（最大收入）。

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

> <span style="color:#7f8c8d;">〔原抽取串：`each a 1 � 1 � 2 meter rectangular prism`。`�` 是 `×` 在文字层被抽坏的痕迹（该字符在源 PDF 里是乘号，编码 U+00D7），按数学意义重建为 $1 \times 1 \times 2$。〕</span>

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

![边界规划 B 与其一个完备、不重叠、只用 2 块方石的摆放（原 PDF 第 2 页插图，300 dpi 裁切保留）](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAApMAAAGVCAIAAAAtxe0qAAAACXBIWXMAAC4jAAAuIwF4pT92AAArDklEQVR4nO3diXdUVbaA8feftCKEhCQQGQSJTIEIEYQQRlGgo4ADIDJqA2KDtqCIvm4Qp7YV2wcq4AAyRNTn1KKiYNOiqCg4gBogGEQSxryzutarxa2TunWTZu9zT/n91l5vQUHX21ZuzlcVKvBfDQAAwB//5XoBAADQBJQbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8AnlBgDAJ5QbAACfUG4AAHxCuQEA8Imbcn++e/faNWs2bthw+PBhJws0Q319/ZEjR1xvEcnp06fff++9NatXV23e7MvO+/fv3/Dyy88+88ybb7xx/Phx1+s0wYkTJ8y1YR5z14ukdfbs2frGnDlzxvVqUe3Zs2fTxo3mkv7kk09c79KIxDWQjuvtwtTW1r5SVfXcs8++++67p06dcr1OJN99992LL7xgrocDBw643sUZ7XKb63jyxImFbdqMHT166ODBbVq3fuzRR5V3aJKjR4+uX7du0k03mZ3NweF6nczMBd2lU6cel11WOXZsRXl5QV7eg8uWmbPb9V5p7f/++wnjxpmHd9TIkeOvu65PSUn7du1eXr/e9V6RfPPNN7mtWrX43e+eePxx17uk9emuXWZDe7oXF7teLbPXXn21rG/fosJCc3mYaVdY+N7Wra6XStW/rKzRRzgxv/76q+sFG7fiySfN512/yy83p3HXzp3NobF9+3bXS2Ww8E9/ys3JMVfC8KFD2xYU3Dl/vkdPQM8j7XJPu+WWoRUVNTU1iZ9+vGNHh6Ii8wRKeY0ozKsoUxRzLg8cMGDZ0qVDysvjX27zJMOccVteeSV5i3mx0rdPn0ULFzrcKsTB6upOHTqY9c59nf3qli1t8/PfeOMNh4tFdP348eYouWHChJiX2zyZO1pbmzLmlaLr1cKYT8B5c+ea82H1c88lV43nMW3KbV652o/wvn37TLnr6upcL9iIp//+9+IuXbZ98EHip+bJ/ZNPPGGeGH355ZduFwvx6COPmGf25lFN/PSHH34YOXz47XPmuN3KCdVyf7htm3kJ+NNPP51740svvtituDien5CbN23av39/4sfmjI55uY8dO2Zerb777rsptx84cMA8Of18924nW4X75Zdfzn2ekWSOlYH9++vv0yT/eOedzh07mod98qRJMS+3eUXleosm++O8eb169Pjuu+9cL5LZIw899OOPP9q3m2fS5QMH6u+TkXkyYc4E88Ip5fbF99xjnoY6WSmjo0eP2k8samtrO7ZvH88/QxGlWu4Z06aZJ9EpN5pn1ub4M4eg5ibNEP9y79y58/djxjT6S1MmT354+XLlff4T5rxu1aKF6y3CmOu2b2np2jVrzI8p93n31ptvFhUWJl9deWryxInLH3zQ9RaNMC+ienbrZt+++7PPzMOuv08UGzdsuGrECPv2Pz/wwKwZM/T3cUu13N2Li99+6y379ttmzbpz/nzNTZoh/uUOMXP69AeXLXO9RRO8t3VrzGPz1IoV5uVU4g0ElPu8qygvf/KJJ1xv8R85ceJE2/z8eH7xeec//5mu3Jd07Ki/TxSPPPzw7Ntus2/f+/XXxV266O/jll65zWuUFr/73cHqavuXVj799HWVlWqbNI+/5a6rqzMH99b4va8nnaO1tQPKypb+5S+uF0nryJEj7du1S76dx4tymycZZuFnn3nGnIAvr1//yy+/uN4rre+/+y4/Nzfm78rO6I033ijp2dP1Fo0zj60ptP0na3+8445pt9ziZKWMTCamTJ5s3/7555+bsnz77bf6KzmkV+7a2lrz+Db6zTObN20aMWyY2ibN42+5p0+dWjl2rOstMjMn3TOrVt2zaFHnjh1vufnmOH+f1R23324e1eRP41/u3JycxJuHJ4wbN3P6dPPEqENR0f++/rrr1Rq3ft26Mddc0/Dv96Nt3LBh3ty5t82aZW6M87dI2Gb/4Q+xfWdow7+/CcVcA8+vXZv4ZjBzPs//4x8vveSS5Dt74mbXrl1mPftb164ZNcqU5cNt25xs5YpeuWtqaszj2+gvvf7aa8OGDFHbpHk8LffCu+/uW1pqXsW6XiSzuxYsGFpRkZeT06242DyPdr1OWma3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)

> <span style="color:#7f8c8d;">**Figure（图）· border plan（边界规划）$B$ 与 placement（摆放）$P$:** 横轴 $i = 0, \dots, 9$ 是沿国界方向的米数，纵轴 $j = 0, \dots, 4$ 是行号，$j = 0$ 在最上（顶面高程 $k - 0 = 5$ 米），$j = 4$ 在最下（顶面高程 $1$ 米）。near-black（近黑）方格是 dirt（泥土），即 $B[j][i] = $ `'#'` 的那些格：第 $3$ 行在 $i = 5, 7, 8$ 处，第 $4$ 行在 $i = 2, 5, 6, 7, 8$ 处，共 $8$ 格。浅色空格是必须被盖住的 empty（空的）立方米格，共 $42$ 格——这 $42$ 格正是本次摆放 $P$ 的覆盖目标（$22$ 块石头，其中长石占 $20$ 块、方石占 $2$ 块，$20 \times 2 + 2 \times 1 = 42$）。图中在空白格里画出的粗线，就是 $P$ 中每一块石头的边界：竖放长石（`'D'`）在相邻两行里占同一列，横放长石（`'R'`）在相邻两列里占同一行，方石（`'1'`）只占一格。</span>

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
