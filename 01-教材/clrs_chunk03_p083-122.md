# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk03 · 书页 83–122 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §4.2–4.3, p.83</span>

**4.2-6** How quickly can you multiply a $kn \times n$ matrix by an $n \times kn$ matrix, using Strassen's algorithm as a subroutine? Answer the same question with the order of the input matrices reversed.

**4.2-7** Show how to multiply the complex numbers $a + bi$ and $c + di$ using only three multiplications of real numbers. The algorithm should take $a$, $b$, $c$, and $d$ as input and produce the real component $ac - bd$ and the imaginary component $ad + bc$ separately.

### Section 4.3 · The substitution method for solving recurrences（求解递归式的代换法） <span style="color:#2471a3;">**[section]**</span>

既然我们已经看到 recurrence（递归式）如何刻画 divide-and-conquer algorithms（分治算法）的 running time（运行时间），接下来就要学习如何 solve（求解）递归式。本节我们从 "substitution" method（"代换"法）开始。

substitution method 求解递归式包含两个步骤：

1. Guess（猜测）解的形式。
2. 用 mathematical induction（数学归纳法）求出常数，并证明该解是正确的。

我们把猜测的解代入函数中，在对 smaller values（更小的值）应用 inductive hypothesis（归纳假设）时——"代换法"因此得名。这个方法功能强大，但我们必须能够猜出答案的形式，才能应用它。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> substitution method（代换法）这条注要回答的设计问题是：手上只有递归式、没有闭式解的人，凭什么能把「猜」变成「证」。答案是：把待证的不等式本身当成 inductive hypothesis（归纳假设），再检查它能否从规模 $m$ 传递到规模 $n$。
>
> 先把归纳结构讲清楚。数学归纳法要证的是「对所有 $m<n$ 有 $T(m)\le cm\lg m$」，而递归式右边恰好只出现规模 $\lfloor n/2\rfloor$ 与 $\lceil n/2\rceil$ 这类更小的自变量，所以代换这一步就是把假设当作已知条件使用。注意这里用的是 strong induction（强归纳）：假设对一切小于 $n$ 的规模都成立，而不只是对 $n-1$ 成立——递归式一次调用两个子问题，弱归纳根本不够用。归纳法的难点从来不在验证，而在提出命题；命题对不对，取决于你对递归式形状的判断。
>
> 代换的代数只有三行，但每一步都有前提。把假设代入得 $2c\lfloor n/2\rfloor\lg\lfloor n/2\rfloor+n$，用 $\lfloor n/2\rfloor\le n/2$ 与对数的单调性放大到 $cn\lg(n/2)+n$，再用 $\lg(n/2)=\lg n-1$ 得 $cn\lg n-cn+n$。要它不超过 $cn\lg n$，只需 $c\ge1$。关键在于：$c$ 是被这个不等式逼出来的，不是凭空猜的；整条推导只在 $c\ge1$ 时闭合，这正是「选常数」这一步的全部内容。
>
> 用数字复核。取 $T(1)=1$、$T(n)=2T(\lfloor n/2\rfloor)+n$，手推得 $T(2)=4$、$T(4)=12$、$T(8)=32$、$T(16)=80$，一般地 $T(2^k)=2^k(k+1)$。若取 $c=2$、$n=1024$，待证界为 $2\cdot1024\cdot10=20480$，真值 $1024\cdot11=11264$，余量约 45%。若取 $c=1$，$n=1024$ 处界为 10240，小于真值 11264，证明立刻失败；病根更早：$n=2$ 时界为 $1\cdot2\cdot1=2$，而 $T(2)=4$，边界条件直接不成立。
>
> 边界条件为什么会被单独拿出来讲？因为 $\lg1=0$，把 $n=1$ 代进 $cn\lg n$ 得 0，与 $T(1)=1$ 矛盾。标准补救是把递归式的基本情况与归纳证明的基本情况分开：$T(1)$ 只是递归式的种子，不含 $\lfloor n/2\rfloor$ 项；当 $n>3$ 时递归式并不依赖 $T(1)$，所以改取 $n_0=2$，以 $T(2)=4$ 与 $T(3)=5$ 起证，再要求 $c\cdot2\lg2\ge4$ 与 $c\cdot3\lg3\ge5$，两式给出 $c\ge2$ 与 $c\ge1.05$，合并即 $c\ge2$。渐近记号允许丢掉有限多个小 $n$，这一步才合法。
>
> 跨课程连接：6.042J 的 mathematical induction（数学归纳法）证的是单个命题，这里的命题带 $c$ 与 $n_0$ 两个自由参数，于是多出「找常数」与「挑基本情况」两道工序；100B 实分析证极限性质时先固定 $\varepsilon$ 再逐项压，区别是那里压的是误差项，这里压的是低阶项；CSAPP 第 2 章讨论整数溢出时先声明位宽再逐位验证，对象换成了二进制位。三处共用同一骨架：先立一个带参数的断言，再证明存在一组参数使它闭合。
>
> 猜从哪里来？这是代换法唯一没有机械流程的一步。可用的来源有三个：其一是模式匹配，归并排序的 $T(n)=2T(n/2)+n$ 与本题同形，解 $\Theta(n\lg n)$ 已知，猜它只是复用结论；其二是 recursion tree（递归树），逐层写出代价再求和，形状一眼可见；其三是先松后紧，先证 $O(n^2)$ 再往下压。猜错并不致命，因为代换法只检验、不生成；真正致命的是猜对了却把假设写弱，下一注会看到这种失败。
>
> 还可以用一个反例感受「量级必须对」。同一条递归式若猜 $T(n)\le cn$，代换得 $2c\lfloor n/2\rfloor+n\le cn+n$，多出的 $n$ 无论把 $c$ 调多大都消不掉，因为 $c$ 是常数而 $n$ 会一直长；这不是代数失误，而是 $\Theta(n\lg n)$ 的解根本不满足线性界，猜测与事实矛盾。
>
> 收束：代换法不是技巧的集合，而是「把归纳假设当作可传递的不等式」这一条纪律；猜错解只浪费一轮，猜对而假设写得太弱才是真正的失败。

我们可以用代换法来建立递归式解的 upper bound（上界）或 lower bound（下界）。作为一个例子，我们来确定下面这个递归式的上界：

```math
T(n) = 2T(\lfloor n/2 \rfloor) + n,
\tag{4.19}
```

它与递归式 (4.3) 和 (4.4) 相似。

我们猜测解为 $T(n) = O(n \lg n)$。代换法要求我们证明：对适当选取的常数 $c > 0$，有 $T(n) \le cn \lg n$。我们首先假设这个界对所有正数 $m < n$ 成立，特别是对 $m = \lfloor n/2 \rfloor$ 成立，即 $T(\lfloor n/2 \rfloor) \le c\lfloor n/2 \rfloor \lg \lfloor n/2 \rfloor$。代入递归式，得到

```math
\begin{aligned}
T(n) &\le 2(c\lfloor n/2 \rfloor \lg \lfloor n/2 \rfloor) + n \\
     &\le cn \lg (n/2) + n \\
     &= cn \lg n - cn \lg 2 + n \\
     &= cn \lg n - cn + n \\
     &\le cn \lg n\,,
\end{aligned}
```

……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.3, p.84</span>

（接上页）……只要 $c \ge 1$，上面最后一步就成立。

mathematical induction 现在要求我们证明：解对 boundary conditions（边界条件）同样成立。通常，我们通过证明边界条件适合作归纳证明的 base cases（基本情况）来做到这一点。对于递归式 (4.19)，我们必须证明可以选取足够大的常数 $c$，使得界 $T(n) \le cn \lg n$ 对边界条件也成立。

这个要求有时会带来麻烦。姑且假定 $T(1) = 1$ 是该递归式唯一的边界条件。那么当 $n = 1$ 时，界 $T(n) \le cn \lg n$ 给出 $T(1) \le c \cdot 1 \cdot \lg 1 = 0$，这与 $T(1) = 1$ 相矛盾。于是，归纳证明的基本情况无法成立。

只需再稍加一点力气，我们就能克服这一障碍，为特定边界条件证明归纳假设。以递归式 (4.19) 为例，我们利用渐近记号（asymptotic notation）的特性：只需证明当 $n \ge n_0$ 时 $T(n) \le cn \lg n$，其中 $n_0$ 是一个可以由我们自行选择的常数。我们保留那个麻烦的边界条件 $T(1) = 1$，但把它从归纳证明的考虑范围中移除。做法是：先观察到当 $n > 3$ 时，该递归式并不直接依赖 $T(1)$。于是，我们可以用 $T(2)$ 和 $T(3)$ 替代 $T(1)$ 作为归纳证明的基本情况，并取 $n_0 = 2$。注意，我们要区分递归式的基本情况（$n = 1$）与归纳证明的基本情况（$n = 2$ 和 $n = 3$）。由 $T(1) = 1$ 出发，我们可以从递归式推出 $T(2) = 4$ 和 $T(3) = 5$。现在，只需选取足够大的常数 $c$，使得 $T(2) \le c \cdot 2 \lg 2$ 与 $T(3) \le c \cdot 3 \lg 3$ 同时成立，我们就能完成归纳证明 $T(n) \le cn \lg n$（对某个常数 $c \ge 1$）。事实证明，任何 $c \ge 2$ 的选择都足以使 $n = 2$ 与 $n = 3$ 这两个基本情况成立。对我们将要考察的大多数递归式而言，扩展边界条件使归纳假设对小 $n$ 成立是直截了当的，我们不会总是明确写出这些细节。

**Making a good guess（做出好的猜测）**

遗憾的是，并不存在一种通用的方法来猜出递归式的正确解。做出好的猜测需要 experience（经验），偶尔还需要 creativity（创造力）。不过幸运的是，你可以借助一些 heuristics（启发式方法）来帮助自己成为好的猜测者。你还可以使用 recursion trees（递归树）——我们将在 Section 4.4 中见到——来生成好的猜测。

如果一个递归式与你以前见过的某个递归式相似，那么猜测一个相似的解是合理的。例如，考虑递归式

```math
T(n) = 2T(\lfloor n/2 \rfloor + 17) + n,
```

由于 $T$ 在右端的参数中多出了一个 "17"，它看起来很难。然而从直觉上看，这个附加项不会对递归式的解产生实质性影响……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.3, p.85</span>

（接上页）……当 $n$ 很大时，$\lfloor n/2 \rfloor$ 与 $\lfloor n/2 \rfloor + 17$ 的差别并不大：二者都把 $n$ 几乎对半分开。因此，我们猜测 $T(n) = O(n \lg n)$，你可以用代换法验证这一猜测是正确的（见 Exercise 4.3-6）。

做出好猜测的另一种方法是：先证明递归式的 loose（宽松的）upper bound 与 lower bound，然后缩小不确定性的范围。例如，对于递归式 (4.19)，由于其中含有项 $n$，我们可以先取一个下界 $T(n) = \Omega(n)$，并证明一个初始上界 $T(n) = O(n^2)$。然后，我们可以逐步降低上界、抬高下界，直到收敛于正确的、asymptotically tight（渐近紧确）的解 $T(n) = \Theta(n \lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注回答的是：证明 $T(n)\le cn^2$ 时，为什么必须把 $(n-1)^2$ 老老实实展开，而不能凭「感觉差不多」收尾。代数放缩的纪律是：主项对齐之后，余项必须能被同一个常数压住，且符号必须与主项相反。
>
> 机制逐句拆。展开 $c(n-1)^2=cn^2-2cn+c$，加上 $n$ 得 $cn^2-(2c-1)n+c$。要求它不超过 $cn^2$，等价于 $(2c-1)n\ge c$。这条不等式给出两条信息：其一，$c\ge1$ 时左边系数非负，且 $n\ge1$ 时 $(2c-1)n\ge2c-1\ge c$，条件正好闭合；其二，若 $c<1$，系数 $2c-1$ 为负，$n$ 越大左边越小，界随 $n$ 发散。也就是说，余项不但要小，还要随 $n$ 单调朝有利方向走，这一步才叫「吸收」。
>
> 为什么不能靠「把常数取大一点」蒙过去？因为 $c$ 在归纳证明里是全程固定的一个数。若允许 $c$ 随 $n$ 变，每次归纳步都可以换一个更大的常数，那时证明的不是「存在常数 $c$」，而是「对每个 $n$ 存在常数」，后者是空话。这正是 asymptotic notation（渐近记号）的定义要求：常数必须在 $n\to\infty$ 之前就固定下来。
>
> 数字复核。取 $T(1)=1$、$T(n)=T(n-1)+n$，真值为 $n(n+1)/2$。取 $c=2$、$n=100$：界 $2\cdot10^4=20000$，真值 5050，余量约四倍；取 $c=1$ 时界 10000 也成立，余量两倍。再看归纳步的一格：$n=100$ 时 $c(n-1)^2+n=1\cdot99^2+100=9901$，与 $cn^2=10000$ 差 99，而被丢弃的项恰是 $(2c-1)n-c=99$。这说明每一格都有账可对，不是模糊的「低阶项无关紧要」。
>
> 还可以拿它反推猜测的量级。若一开始猜 $O(n)$，代换得 $c(n-1)+n=cn-(c-n)$，当 $n>c$ 时 $c-n$ 为负、被减数为负，反而是 $cn$ 加了一个正数，永远收不回 $cn$。这时正确的反应不是换更花的放缩，而是承认量级错了，把猜测抬到 $cn^2$。书里给的另一条路是两边夹：先证下界 $\Omega(n)$、上界 $O(n^2)$，再用更准的猜测逐步收窄，直到 $\Theta(n\lg n)$。
>
> 跨课程连接：100B 实分析里证 $|a_n-L|<\varepsilon$ 时，先构造带余项的中间不等式，再用 $\varepsilon/2$ 压住两项；这里是同一动作的离散版，区别在于余量是 $n$ 的低阶项而不是 $\varepsilon$ 邻域，且 $c$ 只需存在、不必任意小。6.042J 对递推定义的对象做归纳时要求「搬动项之后阶不升」，与这里的系数比较是同一个判据。
>
> 再补一条判据：临界值往往不够用。若取 $c=1/2$，则 $2c-1=0$，不等式退化为 $0\ge c$，即 $0\ge0.5$，不成立；$c$ 再小则系数为负，越往上越糟。所以线性项的系数必须严格为正，也就是 $c>1/2$ 且留出余量，这与「放缩要留余量」是同一件事。主定理情形 3 的正则条件 $af(n/b)\le cf(n)$ 是同一模板的乘性版本：把「差一个低阶项」换成「差一个常数因子」，判据仍然是「余项方向必须朝有利一侧，且能被固定常数吸收」。
>
> 一个容易忽略的细节：常数 $c$ 一旦选定，就不能在归纳步中途改大。若每一步都换更大的 $c$，证明的其实是「对每个 $n$ 存在常数」，而 asymptotic notation（渐近记号）要的是「存在一个常数对所有充分大的 $n$ 成立」，两者强弱差一个量词顺序，而这一个顺序之差正是全部严谨性所在。
>
> 同一模板在后面复现两次：§4.6 用 $n_j<n/b^j+b/(b-1)$ 把取整误差收进与深度无关的常数；快速排序的平均分析把 $\sum k$ 收进 $n^2$。收束一句：algebraic bounding（代数放缩）只有一条判据——主项对齐之后余项必须被常数压住；压不住时先怀疑量级，再怀疑手法。

**Subtleties（细微之处）**

有时，你可能正确地猜到了递归式解的渐近界，但数学推导却在归纳时走不通。问题往往在于：归纳假设不够强，不足以证明这个详细的界。遇到这种卡壳时，如果你通过减去一个 lower-order term（低阶项）来修改猜测，数学推导往往就能顺利进行。

考虑递归式

```math
T(n) = T(\lfloor n/2 \rfloor) + T(\lceil n/2 \rceil) + 1.
```

我们猜测解为 $T(n) = O(n)$，并尝试证明：对适当选取的常数 $c$，有 $T(n) \le cn$。把猜测代入递归式，我们得到

```math
\begin{aligned}
T(n) &\le c\lfloor n/2 \rfloor + c\lceil n/2 \rceil + 1 \\
     &= cn + 1\,,
\end{aligned}
```

它对任何 $c$ 的取值都不能推出 $T(n) \le cn$。我们可能忍不住想尝试一个更大的猜测，比如 $T(n) = O(n^2)$。虽然这个更大的猜测可以做成，但我们原本的猜测 $T(n) = O(n)$ 是正确的。然而，要证明它是正确的，我们必须使用一个更强的归纳假设。

直觉上，我们的猜测几乎是对的：只差常数 $1$，一个低阶项。然而，除非我们证明归纳假设的确切形式，否则数学归纳法就无法奏效。

我们通过从先前的猜测中减去一个低阶项来克服困难。我们的新猜测是

```math
T(n) \le cn - d\,,
```

其中 $d \ge 0$ 是一个常数。现在我们有

```math
\begin{aligned}
T(n) &\le (c\lfloor n/2 \rfloor - d) + (c\lceil n/2 \rceil - d) + 1 \\
     &= cn - 2d + 1 \\
     &\le cn - d\,,
\end{aligned}
```

……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.3, p.86</span>

（接上页）……只要 $d \ge 1$。与前面一样，我们必须选取足够大的常数 $c$ 来处理边界条件。

你可能觉得"减去一个低阶项"的想法 counterintuitive（有违直觉）。毕竟，如果数学推导走不通，我们应该增大猜测，对吧？未必！用归纳法证明 upper bound（上界）时，证明一个更弱的上界成立反而可能更困难，因为为了证明这个更弱的界，我们必须在证明中归纳地使用同样更弱的界。在我们当前的例子中，当递归式含有不止一个 recursive term（递归项）时，每个递归项都可以各减去一次所设界中的低阶项。在上面的例子中，我们把常数 $d$ 减了两次：一次用于 $T(\lfloor n/2 \rfloor)$ 项，一次用于 $T(\lceil n/2 \rceil)$ 项。最终我们得到不等式 $T(n) \le cn - 2d + 1$，而要找到合适的 $d$ 值使 $cn - 2d + 1$ 小于等于 $cn - d$ 是很容易的。

**Avoiding pitfalls（避免陷阱）**

使用渐近记号（asymptotic notation）时很容易犯错误。例如，对递归式 (4.19)，我们可以"错误地证明"$T(n) = O(n)$：猜测 $T(n) \le cn$，然后论证

```math
\begin{aligned}
T(n) &\le 2(c\lfloor n/2 \rfloor) + n \\
     &\le cn + n \\
     &= O(n)\,,
\end{aligned}
\qquad \text{wrong!!（错误！！）}
```

理由是 $c$ 是一个常数。这里的错误在于：我们没有证明归纳假设的确切形式，也就是说，没有证明 $T(n) \le cn$。因此，当我们想要证明 $T(n) = O(n)$ 时，我们将明确地证明 $T(n) \le cn$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注要回答的是一个看起来矛盾的现象：猜测的渐近界明明是对的，归纳证明却卡住。病根几乎总在 inductive hypothesis（归纳假设）写得太弱，而不是猜测的量级错。修法也不神秘：给假设减去一个低阶项，让归纳步有可消耗的余量。
>
> 先看死局怎么形成。递归式 $T(n)=T(\lfloor n/2\rfloor)+T(\lceil n/2\rceil)+1$，猜 $T(n)\le cn$，代换得 $c\lfloor n/2\rfloor+c\lceil n/2\rceil+1=cn+1$。多出来的 $1$ 与 $c$ 无关，把 $c$ 调多大都消不掉——放大常数只会同时放大等号两边。于是有人退而猜 $O(n^2)$ 蒙混过关，界虽然成立却丢掉了真实的阶。
>
> 正解是把假设加强为 $T(n)\le cn-d$。代入得 $c\lfloor n/2\rfloor-d+c\lceil n/2\rceil-d+1=cn-2d+1$，要求它不超过 $cn-d$，等价于 $d\ge1$。取 $d=1$ 即闭合。注意方向：假设变强了（上界更紧），但归纳步反而通过了，因为那个 $+1$ 被 $-d$ 的余量吃掉。这就是「加强归纳假设」的机制——不是把命题改弱去迁就证明，而是改强到归纳步刚好能闭环。
>
> 数字复核。取 $T(1)=1$，则 $T(2)=2\cdot1+1=3$、$T(4)=2\cdot3+1=7$、$T(8)=15$、$T(16)=31$，即 $T(n)=2n-1$（$n$ 取 2 的幂）。若只用 $cn$ 形式、取 $c=2$：$n=8$ 时归纳步给出 $2\cdot8+1=17$，而目标是 $16$，失败。改用 $cn-1$：$n=8$ 时 $2\cdot8-2+1=15\le15$，恰好取等。可见 $2n-1$ 不是凑出来的，而是被递归式唯一确定的紧界。
>
> 为什么会这样？归纳法是个放大器。每一步只松一点点，递归深度一层层把它累乘，最后全线崩塌；反之每一步留一点余量，也能层层传递到叶。判断一个归纳证明是否可靠，看的是「最坏那一层还剩多少余量」，而不是「平均看起来差不多」。这与先证后信的原则一致：单步近似无法靠直觉担保，必须让不等式在每一层都真的成立。
>
> 跨课程连接：6.042J 的 strong induction（强归纳）已经暗示了这一点——把「对 $n$ 成立」加强为「对一切 $m\le n$ 成立」，正是为了给多分支递归提供输入；区别在于那里加强的是归纳的范围，这里加强的是不等式本身的紧度。CSAPP 第 6 章分析 average memory access time（平均访存时间）时，递推 $AMAT=h+m\cdot AMAT_{next}$ 也要写成带余项的闭式才好求值，例如 $h=1$ 周期、命中率之外有 $m=0.05$ 的缺失率、下一层 10 周期，则 $AMAT=1+0.05\cdot10=1.5$ 周期；区别是 cache 层次有限且固定，而这里的递归深度随 $n$ 增长，所以归纳必须对任意深度成立，不能只验三层。
>
> 还有两种常见写法会把这条注的教训抹掉。第一种是直接把目标改成等式 $T(n)=cn$，等式两边同时被放大，永远证不出矛盾，看起来「通过」实则什么都没证。第二种是省掉 base case（基本情况）的检查：$cn-d$ 形式在 $n=1$ 处给出 $c-d\ge1$，这也是对 $c$ 与 $d$ 的一条约束，必须与归纳步的约束同时满足，取 $c=2$、$d=1$ 时恰好都成立。少了这一步，结论只在 $n\ge n_0$ 上成立，而 $n_0$ 是否覆盖边界要单独交代。
>
> 顺带说清「更弱的界更好证」这个直觉为什么在这里失效。通常界越松越容易成立，但归纳证明的难点不在界本身，而在归纳步能否用得上假设。假设里多一个负项，就等于给每一步预留了消耗额度；额度用完之前，任何 $+1$ 都不会让证明崩掉。这就是为什么加强假设反而让证明变简单——它改变的是可用的余量，不是命题的真值。
>
> 收束：当证明卡在「只差一个常数」时，先别改猜测的量级，改假设的紧度；$cn-d$ 里的那个 $d$ 就是归纳法留给自己的余量。

**Changing variables（改变变量）**

有时，一点点代数处理就能使一个陌生的递归式变得与你见过的某个递归式相似。例如，考虑递归式

```math
T(n) = 2T\left(\sqrt{n}\right) + \lg n\,,
```

它看起来很难。不过，我们可以用 change of variables（变量代换）来简化它。为方便起见，我们不去操心把 $\sqrt{n}$ 这类值取整为整数。令 $m = \lg n$，得到

```math
T(2^m) = 2T(2^{m/2}) + m\,.
```

现在再令 $S(m) = T(2^m)$，就得到新的递归式

```math
S(m) = 2S(m/2) + m\,,
```

……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.3, p.87</span>

（接上页）……它与递归式 (4.19) 非常相似。事实上，这个新递归式的解与它完全相同：$S(m) = O(m \lg m)$。把 $S(m)$ 换回 $T(n)$，我们得到

```math
T(n) = T(2^m) = S(m) = O(m \lg m) = O(\lg n \lg \lg n)\,.
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注的核心是 variable substitution（变量替换）这一化归动作：把一个主方法不认识的递归式，通过换元变成已知的标准形。$T(n)=2T(\sqrt n)+\lg n$ 的关键观察只有一句：在 $n$ 的对数尺度上，开平方就是折半，因为 $\lg\sqrt n=(\lg n)/2$。
>
> 机制写清楚。令 $m=\lg n$，再令 $S(m)=T(2^m)$，则 $T(\sqrt n)=T(2^{m/2})=S(m/2)$，而 $\lg n=m$，于是递归式整体变成 $S(m)=2S(m/2)+m$。这个形状主方法认识：$a=2$、$b=2$、$f(m)=m$，且 $m^{\log_2 2}=m$ 与 $f$ 同级，落入情形 2，得 $S(m)=\Theta(m\lg m)$。
>
> 为什么这一步合法？换元必须是两个定义域之间的双射，否则解出的只是另一个问题。$m=\lg n$ 把 $n$ 的幂次映射到整数，但只覆盖 $n=2^m$ 这些点；对一般 $n$，靠 $T$ 的单调性与取整误差可控（§4.6 会给出 $n_j<n/2^j+2$ 这类界）把结果补全。这一步常被跳过，跳过就等于默认「递归式只在 2 的幂上有定义」，那是个更强的假设，必须明说。
>
> 数字复核。取 $n=2^{16}=65536$，则 $\sqrt n=256=2^8$，再开方得 $16=2^4$，再得 $4=2^2$，再得 $2$。取 $T(2)=1$，逐层回代：$T(4)=2\cdot1+2=4$，$T(16)=2\cdot4+4=12$，$T(256)=2\cdot12+8=32$，$T(65536)=2\cdot32+16=80$。与公式 $m(\lg m+1)$ 对照：$m=16$ 时 $16\cdot5=80$，完全吻合。若 $n=2^{32}$，则 $m=32$，值为 $32\cdot6=192$，增长远慢于 $n$ 本身。
>
> 第二个操作要点是必须换回原变量。解出 $S(m)=\Theta(m\lg m)$ 后要代回 $m=\lg n$，得 $T(n)=\Theta(\lg n\cdot\lg\lg n)$；若停在 $S$ 上，答案描述的是另一个函数，与本题无关。同理，习题 4.3-9 的 $3T(\sqrt n)+\log_2 n$ 换元后得 $S(m)=3S(m/2)+m$，此时 $m^{\log_2 3}$ 严格大于 $m$（指数约 1.585），落情形 1，解为 $\Theta(m^{1.585})$，换回即 $\Theta((\lg n)^{1.585})$——注意这里不再是 $\lg n\lg\lg n$，形状由 $a$ 与 $b$ 决定。
>
> 再补三点容易踩空的地方。第一，换元之后 base case（基本情况）也要跟着换：原来的 $n\ge n_0$ 变成 $m\ge\lceil\lg n_0\rceil$，如果忘了换算，最后得到的界只在 $n$ 很大时才成立，而这类递归式在 $n$ 较小时的行为往往正是边界条件定义的地方。第二，不要写成 $S(m)=T(m)$，$S$ 的定义域是 $m$，$T$ 的定义域是 $n=2^m$，两者相差一次指数映射，混写会让后续所有代入都错位。第三，$\sqrt n$ 在整数上要取整，$\lfloor\sqrt n\rfloor$ 与 $\lceil\sqrt n\rceil$ 都会让 $m$ 变成 $\lfloor m/2\rfloor$ 或 $\lceil m/2\rceil$，按 §4.6 的结论这不影响渐近阶，但推导时要写明用的是哪一种。
>
> 最后回答「为什么偏偏取对数」。递归式里的复合结构是「规模先开方、代价再加一个对数」，而开方在对数坐标下是线性折半；我们要找的正是把非线性复合变成线性缩放的那个坐标。这与解微分方程时选合适的自变量变换是同一件事：坐标系选对了，方程就从「没见过的形状」变成「标准形」。判断是否选对的标准很朴素——换元之后，递归式里出现的每个规模都能写成同一个变量的常数倍或常数分之一。
>
> 跨课程连接：微积分里的换元积分（例如 $\int 2x e^{x^2}dx$ 令 $u=x^2$）与这里同构：换元不改变问题，只改变它的表示；区别是那里换的是积分变量、目标是凑出原函数，这里换的是规模变量、目标是凑出主方法的标准形。Strang 线性代数里的 change of basis（换基）是同一思想的矩阵版：同一个线性映射换一组基表示，特征结构不变；区别在于换基必须用可逆矩阵，而这里的换元只需在 $n$ 的幂次上可逆并配合单调性延拓。
>
> 收束：遇到参数里出现指数或开方结构，先取对数；换元选得对，问题就自己变成老朋友。

**Exercises（习题）** <span style="color:#2471a3;">**[exercise]**</span>

**4.3-1** Show that the solution of $T(n) = T(n - 1) + n$ is $O(n^2)$.

**4.3-2** Show that the solution of $T(n) = T(\lceil n/2 \rceil) + 1$ is $O(\lg n)$.

**4.3-3** We saw that the solution of $T(n) = 2T(\lfloor n/2 \rfloor) + n$ is $O(n \lg n)$. Show that the solution of this recurrence is also $\Omega(n \lg n)$. Conclude that the solution is $\Theta(n \lg n)$.

**4.3-4** Show that by making a different inductive hypothesis, we can overcome the difficulty with the boundary condition $T(1) = 1$ for recurrence (4.19) without adjusting the boundary conditions for the inductive proof.

**4.3-5** Show that $\Theta(n \lg n)$ is the solution to the "exact" recurrence (4.3) for merge sort.

**4.3-6** Show that the solution to $T(n) = 2T(\lfloor n/2 \rfloor + 17) + n$ is $O(n \lg n)$.

**4.3-7** Using the master method in Section 4.5, you can show that the solution to the recurrence $T(n) = 4T(n/3) + n$ is $T(n) = \Theta(n^{\log_3 4})$. Show that a substitution proof with the assumption $T(n) \le cn^{\log_3 4}$ fails. Then show how to subtract off a lower-order term to make a substitution proof work.

**4.3-8** Using the master method in Section 4.5, you can show that the solution to the recurrence $T(n) = 4T(n/2) + n$ is $T(n) = \Theta(n^2)$. Show that a substitution proof with the assumption $T(n) \le cn^2$ fails. Then show how to subtract off a lower-order term to make a substitution proof work.

---

> <span style="color:#7f8c8d;">CLRS §4.3–4.4, p.88</span>

**4.3-9** Solve the recurrence $T(n) = 3T(\sqrt{n}) + \log_2 n$ by making a change of variables. Your solution should be asymptotically tight. Do not worry about whether values are integral.

### Section 4.4 · The recursion-tree method for solving recurrences（求解递归式的递归树法） <span style="color:#2471a3;">**[section]**</span>

虽然你可以用 substitution method（代换法）来简洁地证明递归式的某个解是正确的，但要提出一个好的猜测可能并不容易。画出 recursion tree——正如我们在 Section 2.3.2 分析 merge sort（归并排序）递归式时所做的那样——是提出好猜测的一种直观方法。在递归树中，每个 node（结点）表示递归函数调用集合中某处单个 subproblem（子问题）的 cost（代价）。我们把树中每一层内部的代价求和，得到一组 per-level costs（每层代价），然后再把所有每层代价相加，从而确定递归所有层的总代价。

递归树最适合用来生成好的猜测，随后你可以用代换法加以验证。在用递归树生成好猜测时，你通常可以容忍少量 "sloppiness"（不严谨），因为你稍后就会验证自己的猜测。不过，如果你在画递归树和对代价求和时非常仔细，也可以把递归树直接用作递归式之解的证明。在本节中，我们将用递归树来生成好的猜测；而在 Section 4.6 中，我们将直接用递归树证明构成 master method（主方法）之基础的定理。

例如，让我们看看递归树会如何为递归式 $T(n) = 3T(\lfloor n/4 \rfloor) + \Theta(n^2)$ 提供一个好的猜测。我们先专注于求该解的一个上界。因为我们知道，在求解递归式时 floor（下取整）和 ceiling（上取整）通常无关紧要（这正是一个我们可以容忍的不严谨例子），所以我们为递归式 $T(n) = 3T(n/4) + cn^2$ 构造递归树，其中已写出隐含的常数系数 $c > 0$。

Figure 4.5（图 4.5）展示了我们如何为 $T(n) = 3T(n/4) + cn^2$ 推导出递归树。为方便起见，我们假设 $n$ 恰好是 4 的幂（这又是一个可以容忍的不严谨例子），这样所有 subproblem sizes（子问题规模）都是整数。图的 (a) 部分显示 $T(n)$，我们在 (b) 部分把它展开成一棵等价的树来表示该递归式。根结点处的 $cn^2$ 项表示递归顶层（top level）的代价，根的三棵子树表示规模为 $n/4$ 的子问题所付出的代价。(c) 部分把这个过程再向前推进一步，展开 (b) 中每个代价为 $T(n/4)$ 的结点。根的三个孩子（children）中每一个的代价为 $c(n/4)^2$。我们按照递归式所确定的方式，继续把树中的每个结点分解成它的组成部分来展开。

> <span style="color:#7f8c8d;">[note] 下页含整页插图：图 4.5。</span>

……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.4, p.89</span>

> <span style="color:#7f8c8d;">[note] 本页为整页插图：图 4.5（递归树的构造过程），含 (a)–(d) 四个子图、右侧的层代价标注与底部的总结行。图面结构：(a) 单个结点 $T(n)$；(b) 根结点代价 $cn^2$，其下有三个孩子结点 $T(n/4)$；(c) 根结点代价 $cn^2$，第二层三个结点代价各为 $c(n/4)^2$，其下共九个结点 $T(n/16)$；(d) 完全展开的递归树——第 0 层代价 $cn^2$，第 1 层代价 $(3/16)cn^2$，第 2 层代价 $(3/16)^2 cn^2$，……（每往下一层结点数变为 3 倍、子问题规模缩小为 $1/4$），最底层为 $n^{\log_4 3}$ 个叶子结点 $T(1)$，右侧标注树高 $\log_4 n$，叶子层代价 $\Theta(n^{\log_4 3})$，最下方给出 Total: $O(n^2)$（总代价）。</span>

**Figure 4.5（图 4.5）** 为递归式 $T(n) = 3T(n/4) + cn^2$ 构造 recursion tree（递归树）。(a) 部分显示 $T(n)$，它在 (b)–(d) 部分中被逐步展开而形成递归树。(d) 部分中完全展开的树高度为 $\log_4 n$（共有 $\log_4 n + 1$ 层）。

---

> <span style="color:#7f8c8d;">CLRS §4.4, p.90</span>

由于每往下一层，subproblem size（子问题规模）就缩小为原来的 $1/4$，我们最终必然会到达一个边界条件。距离根结点多远才会到达呢？深度（depth）为 $i$ 的结点，其子问题规模为 $n/4^i$。因此，当 $n/4^i = 1$，即等价地当 $i = \log_4 n$ 时，子问题规模达到 $n = 1$。于是，这棵树共有 $\log_4 n + 1$ 层（深度分别为 $0, 1, 2, \ldots, \log_4 n$）。

接下来我们确定树中每一层的代价。每一层的结点数都是上一层的 3 倍，因此深度 $i$ 处的结点数为 $3^i$。由于从根往下每走一层，子问题规模就缩小为 $1/4$，所以对 $i = 0, 1, 2, \ldots, \log_4 n - 1$，深度 $i$ 处每个结点的代价为 $c(n/4^i)^2$。相乘可知：对 $i = 0, 1, 2, \ldots, \log_4 n - 1$，深度 $i$ 处所有结点的总代价为 $3^i c(n/4^i)^2 = (3/16)^i cn^2$。最底层位于深度 $\log_4 n$，共有 $3^{\log_4 n} = n^{\log_4 3}$ 个结点，每个结点贡献代价 $T(1)$，总代价为 $n^{\log_4 3} T(1)$，即 $\Theta(n^{\log_4 3})$，因为我们假定 $T(1)$ 是一个常数。

现在，我们把所有层的代价加起来，以确定整棵树的代价：

```math
\begin{aligned}
T(n) &= cn^2 + \tfrac{3}{16} cn^2 + \left(\tfrac{3}{16}\right)^{\!2} cn^2 + \cdots + \left(\tfrac{3}{16}\right)^{\!\log_4 n - 1} cn^2 + \Theta\!\left(n^{\log_4 3}\right) \\[4pt]
     &= \sum_{i=0}^{\log_4 n - 1} \left(\tfrac{3}{16}\right)^{\!i} cn^2 + \Theta\!\left(n^{\log_4 3}\right) \\[4pt]
     &= \frac{(3/16)^{\log_4 n} - 1}{(3/16) - 1}\, cn^2 + \Theta\!\left(n^{\log_4 3}\right)
\end{aligned}
```

（最后一步依据 equation (A.5)）。这最后一个公式看起来有些杂乱，直到我们意识到：可以再次利用少量的不严谨性，用一个无穷递减的 geometric series（等比级数）作为上界。回退一步并应用 equation (A.6)，我们有

```math
\begin{aligned}
T(n) &= \sum_{i=0}^{\log_4 n - 1} \left(\tfrac{3}{16}\right)^{\!i} cn^2 + \Theta\!\left(n^{\log_4 3}\right) \\[4pt]
     &< \sum_{i=0}^{\infty} \left(\tfrac{3}{16}\right)^{\!i} cn^2 + \Theta\!\left(n^{\log_4 3}\right) \\[4pt]
     &= \frac{1}{1 - (3/16)}\, cn^2 + \Theta\!\left(n^{\log_4 3}\right) \\[4pt]
     &= \frac{16}{13}\, cn^2 + \Theta\!\left(n^{\log_4 3}\right) \\[4pt]
     &= O(n^2)\,.
\end{aligned}
```

于是，对原递归式 $T(n) = 3T(\lfloor n/4 \rfloor) + \Theta(n^2)$，我们得出了猜测 $T(n) = O(n^2)$。在这个例子中，$cn^2$ 的系数构成一个递减等比级数，由 equation (A.6)，这些系数之和……（下页继续）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注讲 recursion tree（递归树）这套记账法：把递归式按层摊开，每一层写清「结点数乘以单点代价」，再看这个乘积随深度是收缩、持平还是放大。它同时承担两个职责：给出猜测的形状，以及给出上界的核算过程。
>
> 机制分三步，每步都要算对乘法的次序。第一步展开：根结点代价 $cn^2$，第一层三个子问题各 $c(n/4)^2$，第二层九个各 $c(n/16)^2$，第 $i$ 层是 $3^i$ 个结点、单点代价 $c(n/4^i)^2$。第二步相乘：$3^i\cdot c(n/4^i)^2=(3/16)^i cn^2$。这一步是整棵树的支点，因为「结点数乘 $3$」与「单点代价除以 $16$」被合并成一个常数公比 $3/16=0.1875$，与深度 $i$ 无关。第三步封顶：公比严格小于 $1$，于是有限和不超过无穷和 $cn^2/(1-3/16)=16cn^2/13$，常数 $16/13\approx1.231$ 就是「用无穷和换闭式」的全部代价。
>
> 数字复核。取 $n=1024$、$c=1$：根层 $1048576$；第二层 $3\cdot(256)^2=3\cdot65536=196608$；第三层 $9\cdot4096=36864$；第四层 $27\cdot256=6912$；第五层 $81\cdot16=1296$；第六层 $243\cdot1=243$。六层合计 $1048576+196608+36864+6912+1296+243=1290499$，而上界 $16/13\cdot1048576\approx1290555$，几乎贴合，说明公比核算没有漏项。再看叶子：树高 $\log_4 1024=5$，叶子数 $3^5=243$，与 $n^{\log_4 3}=1024^{0.7925}\approx243$ 一致；叶子总代价 243，仅为根的万分之二，所以根支配全局。
>
> 历史与人物：把这类「按层求和」的做法固化成可背诵的三种情形，通常归功于 Bentley、Haken 与 Saxe 在 1980 年发表的一篇文章，CLRS 的章末注释也是这样交代的（卷期细节未能一手核实）。值得记住的不是年份，而是他们当时要解决的问题：分治算法的递归式千变万化，若每次都从头画树，教学与工程都不可行；把「谁支配总和」抽象成三个判据，才能真正把分析变成工具。
>
> 但树只负责猜，不负责证。树里那些「缺失的内部结点」「取整造成的规模偏差」都被默认忽略了，所以算法分析的标准流程是「树给形状、代换法补严格性」，§4.4 末尾那串不等式正是干这件事：设 $T(n)\le dn\lg n$，代入两个不等规模的子问题，最后要求 $d\ge c/(\lg3-2/3)$，其中 $\lg3-2/3\approx0.918$，故 $d\approx1.089c$ 就够。这个常数恰好补上了树里被丢掉的取整误差。
>
> 跨课程连接：100B 实分析的几何级数比较判别法与此同构——找一个公比小于 $1$ 的级数压住目标级数；区别是那里判定收敛与否，这里只关心「多出一个常数因子无伤大雅」。CSAPP 第 6 章算 average memory access time（平均访存时间）时也是同一种逐层记账：设 L1 命中 1 周期、缺失率 5%，L2 访问 10 周期、缺失率 20%，内存 100 周期，则 $AMAT=1+0.05(10+0.2\cdot100)=2.5$ 周期；区别是 cache 层数固定为三四层，而递归树的高度随 $n$ 增长，所以这里必须用无穷级数封顶，那里只需把有限层加起来。
>
> 还要交代「为什么可以换成无穷和」。树是有限高 $\log_4 n\approx5$ 的，把它换成无穷级数等于凭空多加若干正项，上界只会更松、不会更紧；而渐近分析只要求常数因子内正确，所以这种变松是允许的。前提是公比小于 $1$：若公比等于 $1$，无穷和发散，换成无穷和就得到「无穷大」这种废答案；若公比大于 $1$，则是根不重要、必须优先算叶子层。三种走势分别对应下一节主定理的三个情形，树只是把它们的形状提前暴露出来。
>
> 树高与「不完全」这两件事也要一起看。到叶子的最长路径是 $n\to(3/4)n\to(3/4)^2n\to\cdots$，所以高度是 $\log_{4/3}n$ 量级；但树并不完全，越往底层缺失的内部结点越多，底部几层的实际代价小于 $cn^2$。正因为如此，用无穷和封顶得到的 $16cn^2/13$ 是货真价实的上界，而不是恰好相等；若想得到下界，则要反过来只保留那些确实存在的层。
>
> 收束：递归树的判据只有一条——公比是常数就写闭式，公比等于 $1$ 就得乘层数，公比大于 $1$ 就说明根不重要、叶子说话。

---

> <span style="color:#7f8c8d;">CLRS §4.4, p.91</span>

（接上页）……被常数 $16/13$ 从上方界定。由于根结点对总代价的贡献是 $cn^2$，根结点贡献了总代价的一个 constant fraction（常数比例）。换言之，根结点的代价支配着整棵树的总代价。

事实上，如果 $O(n^2)$ 确实是该递归式的上界（我们稍后就会加以验证），那么它必定是一个紧确界（tight bound）。为什么？第一次 recursive call（递归调用）就贡献了 $\Theta(n^2)$ 的代价，所以 $\Omega(n^2)$ 必定是该递归式的一个下界。

现在我们可以用 substitution method（代换法）来验证猜测是正确的，也就是说，$T(n) = O(n^2)$ 是递归式 $T(n) = 3T(\lfloor n/4 \rfloor) + \Theta(n^2)$ 的一个上界。我们要证明：对某个常数 $d > 0$，有 $T(n) \le dn^2$。沿用之前的常数 $c > 0$，我们有

```math
\begin{aligned}
T(n) &\le 3T(\lfloor n/4 \rfloor) + cn^2 \\
     &\le 3d\lfloor n/4 \rfloor^2 + cn^2 \\
     &\le 3d(n/4)^2 + cn^2 \\
     &= \tfrac{3}{16}\, dn^2 + cn^2 \\
     &\le dn^2\,,
\end{aligned}
```

只要 $d \ge (16/13)c$，最后一步就成立。

再看一个更复杂的例子。Figure 4.6 给出了递归式 $T(n) = T(n/3) + T(2n/3) + O(n)$ 的递归树（同样，为简单起见我们省略 floor（下取整）与 ceiling（上取整）函数）。与之前一样，我们令 $c$ 表示 $O(n)$ 项中的常数因子。当我们把图中所示递归树各层上的值横向相加时，每一层得到的都是 $cn$。

> <span style="color:#7f8c8d;">[note] 本页含插图：图 4.6。图面结构：一棵向上省略（顶部以 "…" 表示继续向上）的递归树——根结点代价 $cn$；第 1 层两个结点，代价各为 $c(n/3)$ 与 $c(2n/3)$；第 2 层四个结点，代价分别为 $c(n/9)$、$c(2n/9)$、$c(2n/9)$、$c(4n/9)$；再往下以 "…" 表示继续展开。右侧标注树高 $\log_{3/2} n$，底部给出 Total: $O(n \lg n)$（总代价）。</span>

**Figure 4.6（图 4.6）** 递归式 $T(n) = T(n/3) + T(2n/3) + cn$ 的一棵递归树。

……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.4, p.92</span>

（接上页）……从根到 leaf（叶子）的最长 simple path（简单路径）是 $n \to (2/3)n \to (2/3)^2 n \to \cdots \to 1$。由于当 $k = \log_{3/2} n$ 时 $(2/3)^k n = 1$，所以这棵树的高度（height）为 $\log_{3/2} n$。

从直觉上讲，我们期望递归式的解至多是层数乘以每层的代价，即 $O(cn \log_{3/2} n) = O(n \lg n)$。然而，Figure 4.6 只画出了递归树顶部的若干层，而且并非树中每一层都贡献代价 $cn$。考虑叶子的代价：如果这棵递归树是一棵高度为 $\log_{3/2} n$ 的 complete binary tree（完全二叉树），那么它将有 $2^{\log_{3/2} n} = n^{\log_{3/2} 2}$ 片叶子。由于每片叶子的代价是一个常数，所有叶子的总代价将为 $\Theta(n^{\log_{3/2} 2})$，而由于 $\log_{3/2} 2$ 是一个严格大于 1 的常数，它是 $\omega(n \lg n)$。然而，这棵递归树并不是完全二叉树，因此它的叶子少于 $n^{\log_{3/2} 2}$ 片。此外，随着我们从根往下走，越来越多的 internal nodes（内部结点）缺失。因此，递归树靠近底部的那些层对总代价的贡献小于 $cn$。我们本可以把所有代价精确核算清楚，但请记住：我们只是想提出一个供代换法使用的猜测。让我们容忍这种不严谨，尝试证明上界猜测 $O(n \lg n)$ 是正确的。

事实上，我们确实可以用 substitution method（代换法）来验证 $O(n \lg n)$ 是该递归式解的一个上界。我们证明 $T(n) \le dn \lg n$，其中 $d$ 是一个适当的正常数。我们有

```math
\begin{aligned}
T(n) &\le T(n/3) + T(2n/3) + cn \\
     &\le d(n/3) \lg (n/3) + d(2n/3) \lg (2n/3) + cn \\
     &= \bigl(d(n/3) \lg n - d(n/3) \lg 3\bigr) + \bigl(d(2n/3) \lg n - d(2n/3) \lg (3/2)\bigr) + cn \\
     &= dn \lg n - d\bigl((n/3) \lg 3 + (2n/3) \lg (3/2)\bigr) + cn \\
     &= dn \lg n - d\bigl((n/3) \lg 3 + (2n/3) \lg 3 - (2n/3) \lg 2\bigr) + cn \\
     &= dn \lg n - dn(\lg 3 - 2/3) + cn \\
     &\le dn \lg n\,,
\end{aligned}
```

只要 $d \ge c / (\lg 3 - 2/3)$，最后一步就成立。因此，我们并不需要在递归树中进行更精确的代价核算。

**Exercises（习题）** <span style="color:#2471a3;">**[exercise]**</span>

**4.4-1** Use a recursion tree to determine a good asymptotic upper bound on the recurrence $T(n) = 3T(\lfloor n/2 \rfloor) + n$. Use the substitution method to verify your answer.

**4.4-2** Use a recursion tree to determine a good asymptotic upper bound on the recurrence $T(n) = T(n/2) + n^2$. Use the substitution method to verify your answer.

---

> <span style="color:#7f8c8d;">CLRS §4.4–4.5, p.93</span>

**4.4-3** Use a recursion tree to determine a good asymptotic upper bound on the recurrence $T(n) = 4T(n/2 + 2) + n$. Use the substitution method to verify your answer.

**4.4-4** Use a recursion tree to determine a good asymptotic upper bound on the recurrence $T(n) = 2T(n - 1) + 1$. Use the substitution method to verify your answer.

**4.4-5** Use a recursion tree to determine a good asymptotic upper bound on the recurrence $T(n) = T(n - 1) + T(n/2) + n$. Use the substitution method to verify your answer.

**4.4-6** Argue that the solution to the recurrence $T(n) = T(n/3) + T(2n/3) + cn$, where $c$ is a constant, is $\Omega(n \lg n)$ by appealing to a recursion tree.

**4.4-7** Draw the recursion tree for $T(n) = 4T(\lfloor n/2 \rfloor) + cn$, where $c$ is a constant, and provide a tight asymptotic bound on its solution. Verify your bound by the substitution method.

**4.4-8** Use a recursion tree to give an asymptotically tight solution to the recurrence $T(n) = T(n - a) + T(a) + cn$, where $a \ge 1$ and $c > 0$ are constants.

**4.4-9** Use a recursion tree to give an asymptotically tight solution to the recurrence $T(n) = T(\alpha n) + T((1 - \alpha)n) + cn$, where $\alpha$ is a constant in the range $0 < \alpha < 1$ and $c > 0$ is also a constant.

### Section 4.5 · The master method for solving recurrences（求解递归式的主方法） <span style="color:#2471a3;">**[section]**</span>

master method（主方法）为求解形如下式的 recurrences（递归式）提供了一种"cookbook"（菜谱式的）方法：

```math
T(n) = aT(n/b) + f(n)\,, \tag{4.20}
```

其中 $a \ge 1$ 与 $b > 1$ 均为 constants（常数），而 $f(n)$ 是一个 asymptotically positive function（渐近为正的函数）。要使用 master method，你需要记住 three cases（三种情形），但在此之后，你就能够相当轻松地求解许多递归式，往往连纸笔都不需要。

---

> <span style="color:#7f8c8d;">CLRS §4.5, p.94</span>

（接上页）递归式 (4.20) 描述的是这样一个算法的 running time（运行时间）：它把一个规模为 $n$ 的 problem（问题）分解成 $a$ 个 subproblems（子问题），每个子问题的规模为 $n/b$，其中 $a$ 和 $b$ 是正常数。这 $a$ 个子问题被递归地求解，每个耗费时间 $T(n/b)$。函数 $f(n)$ 涵盖了 problem division（问题分解）以及把各子问题的结果 combine（合并）起来这两件事的代价。例如，由 Strassen's algorithm（Strassen 算法）产生的递归式就具有 $a = 7$、$b = 2$、$f(n) = \Theta(n^2)$。

从技术正确性（technical correctness）的角度看，这个递归式实际上并非 well defined（良定义的），因为 $n/b$ 可能不是 integer（整数）。然而，把 $a$ 项 $T(n/b)$ 中的每一项替换为 $T(\lfloor n/b \rfloor)$ 或 $T(\lceil n/b \rceil)$，都不会影响该递归式的渐近行为。（我们将在下一节证明这个 assertion（断言）。）因此，在书写这种形式的 divide-and-conquer recurrences（分治递归式）时，我们通常觉得省略 floor（下取整）与 ceiling（上取整）函数会更方便。

#### The master theorem <span style="color:#2471a3;">**[section]**</span>

master method 依赖于下面这个 theorem（定理）。

**Theorem 4.1 (Master theorem)（定理 4.1：主定理）** <span style="color:#2471a3;">**[theorem]**</span>

设 $a \ge 1$ 与 $b > 1$ 为常数，$f(n)$ 为一个 function（函数），而 $T(n)$ 由如下递归式在非负整数上定义：

```math
T(n) = aT(n/b) + f(n)\,,
```

其中我们把 $n/b$ 解释为 $\lfloor n/b \rfloor$ 或 $\lceil n/b \rceil$。那么 $T(n)$ 具有如下 asymptotic bounds：

1. 若对某个常数 $\epsilon > 0$ 有 $f(n) = O(n^{\log_b a - \epsilon})$，则 $T(n) = \Theta(n^{\log_b a})$。
2. 若 $f(n) = \Theta(n^{\log_b a})$，则 $T(n) = \Theta(n^{\log_b a} \lg n)$。
3. 若对某个常数 $\epsilon > 0$ 有 $f(n) = \Omega(n^{\log_b a + \epsilon})$，并且若对某个常数 $c < 1$ 以及所有 sufficiently large（充分大的）$n$ 有 $af(n/b) \le cf(n)$，则 $T(n) = \Theta(f(n))$。

在把主定理应用于一些例子之前，让我们先花点时间理解一下它究竟说了什么。在这三种情形的每一种中，我们都是把函数 $f(n)$ 与函数 $n^{\log_b a}$ 进行比较。直观上讲，这两个函数中较大的那个决定了递归式的解。如果像情形 1 那样，函数 $n^{\log_b a}$ 是较大者，那么解就是 $T(n) = \Theta(n^{\log_b a})$。如果像情形 3 那样，函数 $f(n)$ 是较大者，那么解就是 $T(n) = \Theta(f(n))$。如果像情形 2 那样，两个函数大小相同，我们就乘上一个 logarithmic factor（对数因子），此时解为 $T(n) = \Theta(n^{\log_b a} \lg n) = \Theta(f(n) \lg n)$。

除了这个直觉之外，你还需要了解一些 technicalities（技术细节）。在第一种情形中，$f(n)$ 不仅必须小于 $n^{\log_b a}$，它还必须是 polynomially smaller（多项式意义上更小的）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注回答的是：master theorem（主定理）的三个情形到底在比较什么。答案是「每一层的总代价」与「叶子总代价」谁说了算——递归式的解就是这两股力量的胜负，胜者决定渐近阶，败者只贡献常数因子。
>
> 机制先把账本摊开。第 $j$ 层有 $a^j$ 个结点、单点代价 $f(n/b^j)$，层代价为 $a^jf(n/b^j)$；树高 $\log_b n$，叶子总代价固定为 $\Theta(n^{\log_b a})$。三个情形分别对应层代价序列的三种走势：若 $f$ 比 $n^{\log_b a}$ 小一个 $n^{\varepsilon}$ 因子，层代价按 $b^{\varepsilon}$ 逐层衰减，总和被首项（叶子）压住，得 $\Theta(n^{\log_b a})$；若两者同级，层代价是常数列，$\log_b n$ 层相加，得 $\Theta(n^{\log_b a}\lg n)$；若 $f$ 大一个 $n^{\varepsilon}$ 因子且满足正则条件，层代价按 $b^{-\varepsilon}$ 逐层放大，总和被根压住，得 $\Theta(f(n))$。
>
> 数字复核，取 $n=1024$、$b=2$、$a=4$，此时 $n^{\log_2 4}=n^2=1048576$。若 $f(n)=n$（情形 1）：第 $j$ 层代价 $4^j\cdot n/2^j=n\cdot2^j$，从 $1024$ 一路涨到 $1024\cdot2^{10}=1048576$，前十层求和 $1024(2^{11}-1)=2096128$，而同批叶子恰是 $4^{10}=1048576$；两者同阶，但叶子的常数更大，故解为 $\Theta(n^2)$。若 $f(n)=n^2$（情形 2）：每层都是 $1048576$，共 $11$ 层，总和 $11534336\approx n^2\lg n$。若 $f(n)=n^3$（情形 3）：第 $j$ 层 $4^j(n/2^j)^3=n^3/2^j$，几何递减，十层和不超过 $2n^3$，根一层就占一半以上。
>
> 为什么必须要求「多项式差」而不是「大一点就行」？因为判定的机器是几何级数。只有当 $f$ 与 $n^{\log_b a}$ 相差整整一个 $n^{\varepsilon}$，层代价才有与深度无关的常数公比，求和才能被闭式封住。若只差一个对数因子，例如 $f(n)=n\lg n$ 对 $n^{\log_b a}=n$，公比变成 $(\lg n-1)/\lg n$，随深度缓慢趋近 $1$，级数封顶失效——这就是 gap（间隙）的来源，不是定理写漏了，而是判别法的分辨率到此为止。
>
> 跨课程连接：100B 实分析里判断级数收敛，也是先找几何级数做比较对象，区别是那里问「和是否有限」，这里问「和的阶是几」，后者只需要一个常数倍的界。CSAPP 第 6 章 cache 层次的「谁主导」判断与此同形：L1 命中 1 周期、缺失率 5%，L2 访问 10 周期、缺失率 20%，内存 100 周期，则 $AMAT=1+0.05(10+0.2\cdot100)=2.5$ 周期；若某层缺失率过高，这一层就会主导总时间，与「根支配」是同一个判据。区别在于 cache 的层数固定、每层代价是可测的实数，而这里的层数与每层代价都随 $n$ 变化。
>
> 再把情形 2 的 $\lg$ 因子交代清楚。每层代价同为 $\Theta(n^{\log_b a})$，层数是从 $0$ 数到 $\log_b n\=1$ 共 $\log_b n$ 层，所以总和是「每层一个常数」乘「层数」。换成以 $2$ 为底的对数只差一个常数因子 $\log_b 2$，故写作 $\Theta(n^{\log_b a}\lg n)$ 合法。这个因子不是修正式，而是实打实乘出来的：拿 $a=2$、$b=2$、$f(n)=n$ 试，$n=1024$ 时每层 $1024$，共 $11$ 层（含根），总和 $11264$，与 $n\lg n+n$ 完全对上。
>
> 再解释 regularity condition（正则条件）$af(n/b)\le cf(n)$ 的职责。它要求「规模缩小之后代价至少按固定比例下降」，这对幂函数几乎自动成立：$af(n/b)=a(n/b)^k=(a/b^k)n^k$，只要 $b^k>a$ 就得到 $c=a/b^k<1$。没有这条，情形 3 可能失效：若 $f$ 在缩放后并不缩小（例如振荡得厉害），层代价就不是等比放大，根也就压不住总和。正则条件的本质是把「逐层放大」这件事变成可迭代的不等式，迭代 $j$ 次得 $a^jf(n/b^j)\le c^jf(n)$，求和才封得住。
>
> 最后提醒一个直觉陷阱：「$f$ 更大」不等于「多项式更大」。$n\lg n$ 比 $n$ 大，但比值只有 $\lg n$，够不上任何 $n^{\varepsilon}$；反过来 $n^{1.001}$ 比值是 $n^{0.001}$，虽然涨幅极慢，却确实满足多项式更大。判据看的是比值能否被 $n$ 的正幂次压住，而不是谁在某个具体 $n$ 处数值更大。
>
> 收束：三情形不是三个公式，而是「层代价的几何走势」的三种可能；把递归树画出来看清走势，公式会自己浮现。

---

> <span style="color:#7f8c8d;">CLRS §4.5, p.95</span>

（接上页）也就是说，对某个常数 $\epsilon > 0$，$f(n)$ 必须比 $n^{\log_b a}$ 渐近地小一个 $n^{\epsilon}$ 因子。在第三种情形中，$f(n)$ 不仅必须大于 $n^{\log_b a}$，它还必须是 polynomially larger（多项式意义上更大的），并且此外还要满足"regularity" condition（正则条件）$af(n/b) \le cf(n)$。我们将遇到的多数 polynomially bounded（多项式有界的）函数都满足这个条件。

注意，这三种情形并未覆盖 $f(n)$ 的所有可能性。当 $f(n)$ 小于 $n^{\log_b a}$ 但不是多项式意义上更小时，在情形 1 与情形 2 之间存在一个 gap（间隙）。类似地，当 $f(n)$ 大于 $n^{\log_b a}$ 但不是多项式意义上更大时，在情形 2 与情形 3 之间也存在一个间隙。如果函数 $f(n)$ 落入这些间隙之一，或者如果情形 3 中的正则条件不成立，你就无法使用 master method 来求解该递归式。

#### Using the master method（使用主方法） <span style="color:#2471a3;">**[section]**</span>

要使用主方法，我们只需判定主定理的哪种情形适用（如果有的话），然后写下答案即可。

作为第一个例子，考虑

```math
T(n) = 9T(n/3) + n\,.
```

对于这个递归式，我们有 $a = 9$、$b = 3$、$f(n) = n$，于是 $n^{\log_b a} = n^{\log_3 9} = \Theta(n^2)$。由于 $f(n) = O(n^{\log_3 9 - \epsilon})$，其中 $\epsilon = 1$，我们可以应用主定理的情形 1，从而得出解为 $T(n) = \Theta(n^2)$。

现在考虑

```math
T(n) = T(2n/3) + 1\,,
```

其中 $a = 1$、$b = 3/2$、$f(n) = 1$，并且 $n^{\log_b a} = n^{\log_{3/2} 1} = n^0 = 1$。情形 2 适用，因为 $f(n) = \Theta(n^{\log_b a}) = \Theta(1)$，因此该递归式的解为 $T(n) = \Theta(\lg n)$。

对于递归式

```math
T(n) = 3T(n/4) + n \lg n\,,
```

我们有 $a = 3$、$b = 4$、$f(n) = n \lg n$，以及 $n^{\log_b a} = n^{\log_4 3} = O(n^{0.793})$。由于 $f(n) = \Omega(n^{\log_4 3 + \epsilon})$，其中 $\epsilon \approx 0.2$，只要我们能证明正则条件对 $f(n)$ 成立，情形 3 就适用。对充分大的 $n$，我们有 $af(n/b) = 3(n/4)\lg(n/4) \le (3/4)\,n \lg n = cf(n)$，其中 $c = 3/4$。因此，根据情形 3，该递归式的解为 $T(n) = \Theta(n \lg n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注把三道例题的解题动作压成一条可执行的工序：第一步只碰 $a$ 与 $b$，算出基准量 $n^{\log_b a}$；第二步把 $f(n)$ 与基准量相比，比的不是数值大小而是「是否差一个多项式因子」；第三步只在落进情形 3 时才查 regularity condition（正则条件）。顺序不能换，换了就会被直觉带偏。
>
> 为什么第一步必须独立完成？因为 $n^{\log_b a}$ 是这道题的零点，$f$ 的意义只有相对它才成立。同一个 $f(n)=n$，在 $a=9$、$b=3$ 的题里是「比 $n^2$ 小得多」，在 $a=2$、$b=2$ 的题里是「与 $n$ 同级」，在 $a=1$、$b=2$ 的题里却是「比 $1$ 大得多」。先看 $f$ 再算基准量，等于在没有坐标系的情况下判断大小。
>
> 三题的数字并排看一遍。$T(n)=9T(n/3)+n$：$n^{\log_3 9}=n^2$，取 $\varepsilon=1$ 落情形 1，解为 $\Theta(n^2)$；$n=729=3^6$ 时 $n^2=531441$，叶子数 $9^6=531441$，两者相等，正是「$a=b^2$ 时叶子恰好铺满 $n^2$」的重演。$T(n)=T(2n/3)+1$：$b=3/2$，$\log_{3/2}1=0$，基准量是常数 $1$，$f$ 也是常数，同 level（同级）落情形 2，解为 $\Theta(\lg n)$；$n=729$ 时深度 $\ln729/\ln1.5\approx16.26$，即十七层左右。$T(n)=3T(n/4)+n\lg n$：$n^{\log_4 3}=n^{0.7925}$，取 $\varepsilon\approx0.2075$ 落情形 3，再验正则：$3(n/4)\lg(n/4)\le(3/4)n\lg n$ 当 $\lg(n/4)\le\lg n$ 时成立，故 $c=3/4<1$，解为 $\Theta(n\lg n)$。
>
> 第三题正好给出一个可算的量级感：$n=1024$ 时基准量 $1024^{0.7925}\approx243$，而 $f=1024\cdot10=10240$，比值约 $42$。拆开看，$n^{\varepsilon}\approx4.21$ 是多项式差贡献的，剩下的十倍来自对数因子。这说明「多项式更大」是把对数因子排除在外的判据：$42$ 倍里的 $10$ 倍不算数，只有 $4.21$ 倍那部分才算。
>
> 跨课程连接：CSAPP 第 6 章比较两种 cache 设计时，也是先算各自的基准量（缺失率乘缺失代价），再判断哪个量级占优，而不是凭容量大小拍脑袋；区别是那里两个量都是可测实数，这里是关于 $n$ 的函数，比较发生在渐近意义下。6.042J 的分情况证明给出同样的纪律：先确定分类的依据，再逐类处理，分类依据必须在处理之前定好，否则会出现「按结论分类」的循环。
>
> 第二步的「多项式差」还有一个常被忽略的宽松处：$\varepsilon$ 可以任意小，小到 $0.001$ 也算数，只要它是正的常数。因此判据不是「差得明显」，而是「差得能被某个幂函数描述」。反过来，$n\lg n$ 与 $n$ 之间的差虽然随 $n$ 增大而无限变大，却始终被任何 $n^{\varepsilon}$ 压住——它属于「差得无限多，但不够多项式」。把这两种「差」区分开，是这一步唯一的技术难点。
>
> 再看两道对照题，体会为什么不能凭数值大小拍脑袋。$T(n)=2T(n/2)+n\lg n$ 卡在缝里，主方法失效；$T(n)=2T(n/2)+n^{1.5}$ 则干净地落情形 3，解为 $\Theta(n^{1.5})$，因为 $n^{0.5}$ 是货真价实的多项式差。同为「比 $n$ 大」，一个能判、一个不能判，分界线是幂次而不是数值。
>
> 这套工序的适用范围也要说清：它只认 $aT(n/b)+f(n)$ 这一种形状。碰到 $T(n)=T(n-1)+n$ 这种每次只减一的，或 $T(n)=2T(\sqrt n)+\lg n$ 这种参数被开方的，都得先化归（代换法或变量替换），再回到三步走。若 $f$ 落在缝里，CLRS 章末注释给的 Akra–Bazzi method（Akra–Bazzi 方法）能处理更一般的非均衡分治，它的第一步是解方程 $\sum_i a_ib_i^p=1$ 定出临界指数 $p$，主方法里 $p$ 退化为 $\log_b a$。
>
> 如果三步走完发现 $f$ 落在 gap（间隙）里，说明本工具失效，此时换 Akra–Bazzi method（Akra–Bazzi 方法）或退回递归树加代换法，见本章章末注释与下一注。
>
> 收束：三步次序的意义是先把坐标系立起来，再谈谁大谁小；主方法之所以能当菜谱用，靠的就是这个不肯省掉的先后顺序。

主方法并不适用于递归式

```math
T(n) = 2T(n/2) + n \lg n\,,
```

尽管它看起来具有正确的形式：$a = 2$、$b = 2$、$f(n) = n \lg n$，且 $n^{\log_b a} = n$。你可能会误以为情形 3 应当适用，因为

---

> <span style="color:#7f8c8d;">CLRS §4.5, p.96</span>

（接上页）$f(n) = n \lg n$ 渐近地大于 $n^{\log_b a} = n$。问题在于它并不是多项式意义上更大。比值 $f(n)/n^{\log_b a} = (n \lg n)/n = \lg n$ 对任何正常数 $\epsilon$ 都渐近地小于 $n^{\epsilon}$。因此，该递归式落入情形 2 与情形 3 之间的 gap。（解参见 Exercise 4.6-2。）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注回答的是：为什么 $f(n)=n\lg n$ 对基准量 $n$ 恰好卡在缝里。把比值写出来就清楚了：$f(n)/n^{\log_b a}=\lg n$。它趋于无穷，所以不满足情形 2 的「同级」；但它比任何 $n^{\varepsilon}$ 都慢，所以也不满足情形 3 的「多项式更大」。一个只差对数因子的函数，正好落在几何级数判别法的分辨极限之外。
>
> 机制用递归树看最直观。取 $T(n)=2T(n/2)+n\lg n$，第 $j$ 层的层代价是 $2^j\cdot(n/2^j)\lg(n/2^j)=n(\lg n-j)$，从 $n\lg n$ 开始，每深一层减少 $n$。把 $j=0$ 到 $\lg n-1$ 加起来得 $n\cdot(1+2+\cdots+\lg n)=n\cdot\lg n(\lg n+1)/2$，即 $\Theta(n\lg^2 n)$。层代价只按等差递减、不是等比，所以求和出来多一个对数因子。
>
> 数字复核。$n=1024$、$\lg n=10$：各层代价依次是 $10240$、$9216$、$8192$、……、$1024$，共十层，总和 $1024\cdot55=56320$。与 $n\lg n=10240$ 相比，倍数恰是 $5.5=(\lg n+1)/2$，与公式一致。若改用主定理硬套，会误判成情形 2 得 $\Theta(n\lg n)$，差了整整一个 $\lg n$ 因子；在 $n=10^6$ 处这个因子是 $20$，量级判断直接错一个数量级。
>
> 推广也值得记住：若 $f(n)=\Theta(n^{\log_b a}\lg^k n)$，则解为 $\Theta(n^{\log_b a}\lg^{k+1}n)$。递归树里每层代价是 $n^{\log_b a}(\lg n-j)^k$，求和约等于 $n^{\log_b a}$ 乘上 $(\lg n)^{k+1}/(k+1)$，分母 $k+1$ 只是个常数。这条推广（习题 4.6-2）把「卡缝」这一类情形系统化了：缝里的函数不是不能用公式，而是公式要换成「多一次求和」的版本。
>
> 跨课程连接：100B 实分析与 6.042J 里的两个级数是同一现象：$\sum1/n$ 长成 $\ln n$，$\sum1/(n\ln n)$ 长成 $\ln\ln n$，多一个对数因子就多一层对数。区别是那里问级数收敛还是发散，这里问求和的阶是几；共同点是「对数差」在求和时会累积成更高一层的对数，所以绝不能当常数丢掉。CSAPP 第 6 章算 AMAT 时把缺失率当乘数层层相乘，若某层缺失率是 $1/\ln n$ 这种缓慢衰减的形状，同样不能当作常数处理——这与「$n\lg n$ 不是多项式更大」是同一个分辨力问题。
>
> 为什么缝一定存在？因为判定的尺子是幂函数。对任意固定的 $\varepsilon>0$ 都有 $\lg n=O(n^{\varepsilon})$，也就是说对数因子比任何正幂次都慢；但它同时无界增长，不满足「同级」。一个量永远比 $n^{\varepsilon}$ 小、又永远在长大，正好落在两把尺子之间。这不是 CLRS 少写了一个情形，而是「用 $n^{\varepsilon}$ 分级」这套坐标系的固有盲区。
>
> 严格证明要两头都做。上界用树：层代价等差递减，求和得 $n\lg^2n/2$ 量级；下界只需保留后半段那些层，每层代价不小于 $n\lg n/2$，取 $\lg n/2$ 层相加即得 $\Omega(n\lg^2n)$。两个方向合起来才是 $\Theta$，而树本身只负责给形状，常数仍要靠代换法核验——这与 §4.4 的分工完全一致。
>
> 还有一个统一视角：把 $f$ 乘以 $\lg^k n$，解就多乘一个 $\lg n$，相当于在求和里多做一次累加。主定理情形 2 正是 $k=0$ 的特例（$f$ 与基准量同级，层代价是常数列，$\lg n$ 层相加）；而缝里的 $n\lg n$ 对应「比同级多一个对数」，于是求和从「乘层数」升级为「乘层数的平方除以二」。把这几个形状排成一条谱，就不会再把它们当成孤立的特例来背。
>
> 收束：遇到 $f$ 与基准量只差对数因子，先画树再求和，别硬套三情形；缝不是定理的漏洞，而是「等比」这一把尺子的量程边界。

让我们用 master method 来求解我们在 §4.1 和 §4.2 中见过的那些递归式。Recurrence (4.7)（递归式 (4.7)），

```math
T(n) = 2T(n/2) + \Theta(n)\,, \tag{4.7}
```

刻画了 maximum-subarray problem（最大子数组问题）与 merge sort（归并排序）两者的 divide-and-conquer algorithm（分治算法）的 running time（运行时间）。（按照我们的惯例，我们在递归式中省略 base case（基本情况）的陈述。）这里我们有 $a = 2$、$b = 2$、$f(n) = \Theta(n)$，于是 $n^{\log_b a} = n^{\log_2 2} = n$。情形 2 适用，因为 $f(n) = \Theta(n)$，所以我们得到解 $T(n) = \Theta(n \lg n)$。

Recurrence (4.17)（递归式 (4.17)），

```math
T(n) = 8T(n/2) + \Theta(n^2)\,, \tag{4.17}
```

描述的是我们见过的第一个用于 matrix multiplication（矩阵乘法）的 divide-and-conquer algorithm 的运行时间。现在我们有 $a = 8$、$b = 2$、$f(n) = \Theta(n^2)$，于是 $n^{\log_b a} = n^{\log_2 8} = n^3$。由于 $n^3$ 多项式意义上大于 $f(n)$（即 $f(n) = O(n^{3-\epsilon})$，其中 $\epsilon = 1$），情形 1 适用，从而 $T(n) = \Theta(n^3)$。

最后，考虑 recurrence (4.18)（递归式 (4.18)），

```math
T(n) = 7T(n/2) + \Theta(n^2)\,, \tag{4.18}
```

它描述的是 Strassen's algorithm（Strassen 算法）的运行时间。这里我们有 $a = 7$、$b = 2$、$f(n) = \Theta(n^2)$，于是 $n^{\log_b a} = n^{\log_2 7}$。把 $\log_2 7$ 改写为 $\lg 7$，并回忆起 $2.80 < \lg 7 < 2.81$，我们看到 $f(n) = O(n^{\lg 7 - \epsilon})$，其中 $\epsilon = 0.8$。同样，情形 1 适用，我们得到解 $T(n) = \Theta(n^{\lg 7})$。

**Exercises（习题）** <span style="color:#2471a3;">**[exercise]**</span>

**4.5-1** Use the master method to give tight asymptotic bounds for the following recurrences.

a. $T(n) = 2T(n/4) + 1$.

b. $T(n) = 2T(n/4) + \sqrt{n}$.

c. $T(n) = 2T(n/4) + n$.

d. $T(n) = 2T(n/4) + n^2$.

---

> <span style="color:#7f8c8d;">CLRS §4.5–4.6, p.97</span>

**4.5-2** Professor Caesar wishes to develop a matrix-multiplication algorithm that is asymptotically faster than Strassen's algorithm. His algorithm will use the divide-and-conquer method, dividing each matrix into pieces of size $n/4 \times n/4$, and the divide and combine steps together will take $\Theta(n^2)$ time. He needs to determine how many subproblems his algorithm has to create in order to beat Strassen's algorithm. If his algorithm creates $a$ subproblems, then the recurrence for the running time $T(n)$ becomes $T(n) = aT(n/4) + \Theta(n^2)$. What is the largest integer value of $a$ for which Professor Caesar's algorithm would be asymptotically faster than Strassen's algorithm?

**4.5-3** Use the master method to show that the solution to the binary-search recurrence $T(n) = T(n/2) + \Theta(1)$ is $T(n) = \Theta(\lg n)$. (See Exercise 2.3-5 for a description of binary search.)

**4.5-4** Can the master method be applied to the recurrence $T(n) = 4T(n/2) + n^2 \lg n$? Why or why not? Give an asymptotic upper bound for this recurrence.

**4.5-5** <span style="color:#7f8c8d;">$\star$</span> Consider the regularity condition $af(n/b) \le cf(n)$ for some constant $c < 1$, which is part of case 3 of the master theorem. Give an example of constants $a \ge 1$ and $b > 1$ and a function $f(n)$ that satisfies all the conditions in case 3 of the master theorem except the regularity condition.

### Section 4.6 · Proof of the master theorem（主定理的证明） <span style="color:#2471a3;">**[section]**</span>

本节包含 master theorem（Theorem 4.1）的一个 proof（证明）。你不需要理解这个证明，也能够应用 master method。

该证明分为 two parts（两个部分）。第一部分在一个简化假设——$T(n)$ 只定义在 $b > 1$ 的 exact powers 上，即 $n = 1, b, b^2, \ldots$——之下分析 master recurrence（主递归式）(4.20)。这一部分给出了理解主定理为何成立所需的全部 intuition（直觉）。第二部分展示如何把这一分析扩展到所有正整数 $n$；它把数学技巧（mathematical technique）应用于处理 floor（下取整）与 ceiling（上取整）的问题。

在本节中，我们有时会轻微地 abuse（滥用）asymptotic notation（渐近记号），用它来描述那些只定义在 $b$ 的精确幂上的函数的行为。

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.98</span>

（接上页）回忆一下，asymptotic notations（渐近记号）的 definition（定义）要求界必须对 all sufficiently large numbers（所有充分大的数）成立，而不仅仅是那些 $b$ 的幂。由于我们本可以构造一套只适用于集合 $\{b^i : i = 0, 1, 2, \ldots\}$、而不适用于非负数的新渐近记号，所以这种滥用是轻微的（minor）。尽管如此，在一个有限的 domain（定义域）上使用渐近记号时，我们必须时刻保持警惕，以免得出不当的结论。例如，证明当 $n$ 是 2 的精确幂时 $T(n) = O(n)$，并不能保证 $T(n) = O(n)$。函数 $T(n)$ 完全可以定义为

```math
T(n) = \begin{cases} n & \text{if } n = 1, 2, 4, 8, \ldots\,, \\ n^2 & \text{otherwise}\,, \end{cases}
```

在这种情况下，适用于所有 $n$ 值的最好的 upper bound（上界）是 $T(n) = O(n^2)$。正因为这种 drastic consequence（严重的后果），我们绝不会在一个有限的定义域上使用渐近记号，除非从上下文中可以绝对清楚地看出我们正在这样做。

### Section 4.6.1 · The proof for exact powers（精确幂情形的证明） <span style="color:#2471a3;">**[section]**</span>

主定理证明的第一部分在 $n$ 是 $b > 1$ 的精确幂（$b$ 不必是 integer（整数））的假设下，分析主方法的递归式 (4.20)

```math
T(n) = aT(n/b) + f(n)\,.
```

我们把这一分析拆解成三个 lemma（引理）。第一个引理把求解主递归式的问题归约为对一个包含 summation（求和式）的表达式求值的问题。第二个引理确定这个求和式的 bounds（界）。第三个引理把前两个合在一起，证明一个适用于 $n$ 是 $b$ 的精确幂情形的主定理版本。

**Lemma 4.2（引理 4.2）** <span style="color:#2471a3;">**[lemma]**</span>

设 $a \ge 1$ 与 $b > 1$ 为常数，$f(n)$ 是定义在 $b$ 的精确幂上的一个 nonnegative function（非负函数）。用如下递归式在 $b$ 的精确幂上定义 $T(n)$：

```math
T(n) = \begin{cases} \Theta(1) & \text{if } n = 1\,, \\ aT(n/b) + f(n) & \text{if } n = b^i\,, \end{cases}
```

其中 $i$ 是一个 positive integer（正整数）。那么

```math
T(n) = \Theta(n^{\log_b a}) + \sum_{j=0}^{\log_b n - 1} a^j f(n/b^j)\,. \tag{4.21}
```

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>
>
> 我们使用 Figure 4.7 中的 recursion tree（递归树）。树的 root（根）的代价（cost）为 $f(n)$，它有 $a$ 个 children（孩子），每个孩子的代价为 $f(n/b)$。（把 $a$ 看作

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.99</span>

> <span style="color:#7f8c8d;">[note] 本页含整页插图：图 4.7（递归树）。图面结构：一棵完全 $a$ 叉递归树——根结点代价 $f(n)$，它有 $a$ 个孩子，每个孩子代价为 $f(n/b)$；第二层共 $a^2$ 个结点，每个代价为 $f(n/b^2)$；再往下按 $a^j f(n/b^j)$ 的规律继续展开，中间各层以 "…" 表示。右侧标注各 depth（深度）的层代价：第 0 层为 $f(n)$，第 1 层为 $a f(n/b)$，第 2 层为 $a^2 f(n/b^2)$，……，最底层（深度 $\log_b n$）共 $n^{\log_b a}$ 片叶子，每片代价 $\Theta(1)$，合计 $\Theta(n^{\log_b a})$。图底给出 Total: $\Theta(n^{\log_b a}) + \sum_{j=0}^{\log_b n - 1} a^j f(n/b^j)$（总代价）。</span>

**Figure 4.7（图 4.7）** 由 $T(n) = aT(n/b) + f(n)$ 生成的 recursion tree（递归树）。这棵树是一棵 complete $a$-ary tree（完全 $a$ 叉树），有 $n^{\log_b a}$ 片 leaves（叶子），高度为 $\log_b n$。每个 depth（深度）上各结点的代价显示在右侧，它们的和由 equation（式）(4.21) 给出。

> （接上页）一个 integer（整数）会更方便，尤其是在对递归树进行 visualize（可视化）的时候，但数学推导并不需要这样做。）这些孩子中的每一个又有 $a$ 个孩子，于是在深度 2 处共有 $a^2$ 个结点，每个结点的代价为 $f(n/b^2)$。一般地，深度 $j$ 处有 $a^j$ 个结点，每个结点的代价为 $f(n/b^j)$。每片 leaf（叶子）的代价为 $T(1) = \Theta(1)$，并且每片叶子都位于深度 $\log_b n$ 处，因为 $n / b^{\log_b n} = 1$。树中共有 $a^{\log_b n} = n^{\log_b a}$ 片叶子。
>
> 我们可以像图中所示那样，把树中每个深度上各结点的代价相加，从而得到 equation (4.21)。深度 $j$ 处所有 internal nodes（内部结点）的代价为 $a^j f(n/b^j)$，因此所有内部结点的总代价为
>
> ```math
> \sum_{j=0}^{\log_b n - 1} a^j f(n/b^j)\,.
> ```
>
> 在底层的 divide-and-conquer（分治）算法中，这个和表示的是把 problem（问题）分解为 subproblems（子问题）、随后再把各子问题 recombine（重新合并）的代价。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 整棵主定理只靠一行等式支撑：$a^{\log_b n}=n^{\log_b a}$。它看起来像记号的巧合，其实是「沿树数结点」与「按规模数子问题」这两种计数方式必须给出同一个数；而这两种计数一致的唯一理由，是乘法交换律。
>
> 证明只有两行。两边取以 $b$ 为底的对数：左边得 $\log_b n\cdot\log_b a$，右边得 $\log_b a\cdot\log_b n$，两个数相乘与次序无关，故相等。这同时是换底公式 $\log_a n=\log_b n/\log_b a$ 的直接推论：把「$a$ 的多少次方等于 $n$」换成「$b$ 的多少次方等于 $n$」，只差一个固定比例。
>
> 为什么说它是支点？递归树里叶子有两笔账。第一笔沿树走：每下一层规模除以 $b$、结点数乘 $a$，走 $d=\log_b n$ 层到底，叶子数是 $a^d=a^{\log_b n}$。第二笔按子问题记账：每个叶子是规模为 $1$ 的子问题，而规模缩小因子是 $b$，指数 $p$ 满足 $n/b^p=1$，即 $p=\log_b a$，故叶子数是 $n^{\log_b a}$。两笔账算的是同一批叶子，数值必须相同；若不等，式 (4.21) 的总代价就会裂成对不上的两半，三个情形也就无从谈起。
>
> 数字复核三组。取 $a=2$、$b=4$、$n=256$：沿树 $\log_4 256=4$ 层，叶子数 $2^4=16$；按规模算 $n^{\log_4 2}=256^{0.5}=16$，两边相等。取 $a=8$、$b=2$、$n=1024$：叶子数 $8^{10}=2^{30}=1073741824$，而 $1024^{\log_2 8}=1024^3=2^{30}$，仍是同一个数。取 $a=3$、$b=2$、$n=1024$：$3^{10}=59049$，而 $1024^{1.58496}\approx59048.6$，差的那一点来自 $1.58496$ 的截断误差，不是等式失效。
>
> 第一性原理上，这条等式说的是「指数与对数是一对互相翻译的字典」：对数把乘法翻译成加法，指数再把加法翻译回乘法。凡是要把「层数乘出来」与「幂次算出来」对齐的地方，都得用这本字典。它之所以在算法分析里处处出现，是因为分治的两种描述方式天然一种是乘法（每层 $a$ 份）、一种是除法（规模除以 $b$），而它们描述的是同一个过程。
>
> 跨课程连接：6.042J 数论里用费马小定理把巨大指数降到模 $p-1$ 的范围内，用的也是「指数上的加法对应底数上的乘法」这条同构；区别是那里关心同余类，这里关心实数上的增长速度。CSAPP 第 2 章浮点表示把 $2$ 的幂写进指数域并加偏置，本质是把乘性尺度线性化，才能用整数比较大小；区别是那里指数域位宽有限、会发生上溢，而这里的对数定义在整个正实数上。100B 实分析里把 $\ln(ab)=\ln a+\ln b$ 当作基本性质使用，是同一本字典的连续版本。
>
> 写错方向会立刻露馅，值得做一次破坏性检查。若把 $n^{\log_b a}$ 误记成 $a\log_b n$，取 $a=8$、$b=2$、$n=1024$ 会得到 $8\cdot10=80$，而真实叶子数是 $1073741824$，相差七个数量级。指数与对数的位置一旦互换，量级就从「幂」跌成「线性」，而幂与线性正是算法分析里最不能混淆的一对。
>
> 还有一层容易被忽略：这条等式对 $n$ 的任何实数取值都成立，不只对 $b$ 的幂。取 $n=100$、$a=8$、$b=2$：左边 $8^{\log_2 100}=8^{6.6439}\approx1.0\times10^6$，右边 $100^3=10^6$，仍然吻合。正因如此，主定理才敢把 $n/b$ 直接当实数用，把取整的麻烦留到 §4.6 单独处理。
>
> 收束：记住这一行不是为了套公式，而是为了知道「叶子数」与「叶子代价」为什么能互相替换；主定理的三情形，全都建立在这个替换合法之上。

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.100</span>

（接上页）所有叶子合计的代价——也就是求解全部 $n^{\log_b a}$ 个规模为 1 的 subproblems（子问题）的代价——为 $\Theta(n^{\log_b a})$。

就 recursion tree 而言，master theorem 的三种情形分别对应于树的 total cost（总代价）(1) 由叶子中的代价所 dominate（支配）、(2) 在树的各个 level（层）之间均匀分布、或 (3) 由根结点的代价所支配的情形。

式 (4.21) 中的 summation 描述的是底层 divide-and-conquer 算法中 divide（分解）与 combine（合并）步骤的代价。接下来的这个 lemma（引理）为该求和式的增长提供 asymptotic bounds。

**Lemma 4.3（引理 4.3）** <span style="color:#2471a3;">**[lemma]**</span>

设 $a \ge 1$ 与 $b > 1$ 为常数，$f(n)$ 是定义在 $b$ 的 exact powers 上的一个 nonnegative function。由下式定义在 $b$ 的精确幂上的函数 $g(n)$：

```math
g(n) = \sum_{j=0}^{\log_b n - 1} a^j f(n/b^j) \tag{4.22}
```

对 $b$ 的精确幂具有如下渐近界：

1. 若对某个 constant $\epsilon > 0$ 有 $f(n) = O(n^{\log_b a - \epsilon})$，则 $g(n) = O(n^{\log_b a})$。
2. 若 $f(n) = \Theta(n^{\log_b a})$，则 $g(n) = \Theta(n^{\log_b a} \lg n)$。
3. 若对某个常数 $c < 1$ 以及所有 sufficiently large $n$ 有 $af(n/b) \le cf(n)$，则 $g(n) = \Theta(f(n))$。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>
>
> 对于 case 1，我们有 $f(n) = O(n^{\log_b a - \epsilon})$，这蕴含 $f(n/b^j) = O\bigl((n/b^j)^{\log_b a - \epsilon}\bigr)$。把它代入 equation (4.22) 得到
>
> ```math
> g(n) = O\!\left( \sum_{j=0}^{\log_b n - 1} a^j \left( \frac{n}{b^j} \right)^{\log_b a - \epsilon} \right)\,. \tag{4.23}
> ```
>
> 我们通过 factor out（提取公因子）并化简，来估计 O-notation（O 记号）内部的求和式，最后留下的是一个 increasing geometric series（递增的几何级数）：
>
> ```math
> \begin{aligned}
> \sum_{j=0}^{\log_b n - 1} a^j \left( \frac{n}{b^j} \right)^{\log_b a - \epsilon}
> &= n^{\log_b a - \epsilon} \sum_{j=0}^{\log_b n - 1} \left( \frac{a}{b^{\log_b a - \epsilon}} \right)^j \\
> &= n^{\log_b a - \epsilon} \sum_{j=0}^{\log_b n - 1} \bigl(b^{\epsilon}\bigr)^j \\
> &= n^{\log_b a - \epsilon} \, \frac{b^{\epsilon \log_b n} - 1}{b^{\epsilon} - 1}\,.
> \end{aligned}
> ```

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.101</span>

（接上页）

```math
= n^{\log_b a - \epsilon} \, \frac{n^{\epsilon} - 1}{b^{\epsilon} - 1}\,.
```

由于 $b$ 和 $\epsilon$ 都是 constants，我们可以把最后一个表达式改写为 $n^{\log_b a - \epsilon} O(n^{\epsilon}) = O(n^{\log_b a})$。把这个表达式代入 equation (4.23) 中的 summation，得到

```math
g(n) = O(n^{\log_b a})\,,
```

从而证明了 case 1。

因为 case 2 假设 $f(n) = \Theta(n^{\log_b a})$，我们有 $f(n/b^j) = \Theta\bigl((n/b^j)^{\log_b a}\bigr)$。把它代入 equation (4.22) 得到

```math
g(n) = \Theta\!\left( \sum_{j=0}^{\log_b n - 1} a^j \left( \frac{n}{b^j} \right)^{\log_b a} \right)\,. \tag{4.24}
```

我们像在情形 1 中那样估计 Θ-notation（Θ 记号）内部的求和式，但这一次得到的并不是一个 geometric series。相反，我们发现求和式的每一项都是相同的：

```math
\begin{aligned}
\sum_{j=0}^{\log_b n - 1} a^j \left( \frac{n}{b^j} \right)^{\log_b a}
&= n^{\log_b a} \sum_{j=0}^{\log_b n - 1} \left( \frac{a}{b^{\log_b a}} \right)^j \\
&= n^{\log_b a} \sum_{j=0}^{\log_b n - 1} 1 \\
&= n^{\log_b a} \log_b n\,.
\end{aligned}
```

把这个表达式代入 equation (4.24) 中的求和式，得到

```math
\begin{aligned}
g(n) &= \Theta(n^{\log_b a} \log_b n) \\
     &= \Theta(n^{\log_b a} \lg n)\,,
\end{aligned}
```

从而证明了情形 2。

我们类似地证明 case 3。由于 $f(n)$ 出现在 $g(n)$ 的 definition (4.22) 中，并且 $g(n)$ 的所有项都是 nonnegative（非负的），我们可以断言：对 $b$ 的精确幂，$g(n) = \Omega(f(n))$。我们在引理的陈述中假设过，对某个常数 $c < 1$ 以及所有 sufficiently large $n$，$af(n/b) \le cf(n)$。我们把这个假设改写为 $f(n/b) \le (c/a) f(n)$，并对它 iterate（迭代）$j$ 次，得到 $f(n/b^j) \le (c/a)^j f(n)$，或者等价地 $a^j f(n/b^j) \le c^j f(n)$，其中我们假设被迭代的值都是充分大的。这个不等式对除了至多常数个具有最小此类值 $n/b^j$ 的项之外的所有项都成立，对这些例外的项有 $a^j f(n/b^j) = O(1)$。

把它代入 equation (4.22) 并化简，得到一个几何级数；但与情形 1 中的级数不同，这个级数的项是递减的（decreasing）。我们用一个 $O(1)$ 项来捕捉那些未被"n 充分大"假设所覆盖的项：

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.102</span>

（接上页）

```math
\begin{aligned}
g(n) &= \sum_{j=0}^{\log_b n - 1} a^j f(n/b^j) \\
     &\le \sum_{j=0}^{\log_b n - 1} c^j f(n) + O(1) \\
     &\le f(n) \sum_{j=0}^{\infty} c^j + O(1) \\
     &= f(n) \left( \frac{1}{1 - c} \right) + O(1) \\
     &= O(f(n))\,,
\end{aligned}
```

由于 $c$ 是一个 constant。因此，对 $b$ 的 exact powers，我们可以断言 $g(n) = \Theta(f(n))$。随着 case 3 得证，这个 lemma 的 proof 宣告完成。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 三个情形的证明并排看，会发现同一个模板：用 $\varepsilon$ 制造一个严格的几何公比，再用闭式求和封顶。$\varepsilon$ 不是装饰，它是把「缓慢变化的比值」变成「与深度无关的常数倍」的那只旋钮。
>
> 情形 1 的机制。设 $f(n)=O(n^{\log_b a-\varepsilon})$，代进求和式得 $n^{\log_b a-\varepsilon}\sum_j(b^{\varepsilon})^j$。公比 $b^{\varepsilon}>1$ 是递增等比，前 $D$ 项和为 $(b^{\varepsilon D}-1)/(b^{\varepsilon}-1)$，而 $b^{\varepsilon D}=b^{\varepsilon\log_b n}=n^{\varepsilon}$，于是整个和不超过 $n^{\log_b a}/(b^{\varepsilon}-1)$。注意分母是个常数，但它可以很大：$\varepsilon=0.5$、$b=2$ 时为 $1/(\sqrt2-1)\approx2.414$；$\varepsilon=0.1$ 时 $b^{\varepsilon}\approx1.0718$，常数涨到 $13.93$。常数再大也不影响渐近阶，这正是 O 记号允许的宽松。
>
> 情形 3 的机制。正则条件迭代 $j$ 次给出 $a^jf(n/b^j)\le c^jf(n)$，公比 $c<1$ 递减，求和不超过 $f(n)/(1-c)$。取 $c=1/2$ 则界是 $2f(n)$；若 $T(n)=2T(n/2)+n^2$，$n=1024$ 时 $f=1048576$，总和不超过 $2097152$，而根一层就贡献一半以上——「根支配」这句话在数字上就是「首项占一半」。
>
> 情形 2 没有 $\varepsilon$ 可用。每层代价相同，级数退化成常数列，只能老实乘层数 $\log_b n$。这不是技术不足，而是「公比恰好等于 $1$」时几何求和公式的分母为零，闭式退化为线性累加。三种情形的差别，最终都归结为级数的形状：增、平、减。
>
> 数字复核情形 1。取 $T(n)=2T(n/2)+\sqrt n$，则 $\log_2 2=1$、$f=n^{0.5}$，取 $\varepsilon=0.5$。$n=2^{20}=1048576$ 时，层代价为 $2^j(n/2^j)^{0.5}=\sqrt n\cdot(\sqrt2)^j$；前二十层求和 $1024\cdot((\sqrt2)^{20}-1)/(\sqrt2-1)=1024\cdot(1024-1)/0.4142\approx2.53\times10^6$，而不等式给出的界是 $2.414n\approx2.53\times10^6$，两者贴合。若不用 $\varepsilon$ 而直接估，会得到「$\sqrt n$ 乘层数」这种错误的量级。
>
> 跨课程连接：100B 实分析中，Rudin 第 3 章判断级数收敛时，也是找一个几何级数做上界，再用比值小于 $1$ 收尾；区别是那里要证「和有限」，这里只证「和多出一个常数因子无伤大雅」，所以可以把 $\varepsilon$ 取得很小、常数取得很大而不心疼。6.042J 里用 $\varepsilon$ 做估计时同样先固定 $\varepsilon$ 再操作，区别是那里 $\varepsilon$ 是精度参数、越小越难，这里 $\varepsilon$ 是分类参数、越小只是让常数变大。
>
> 情形 3 为什么必须额外要 regularity condition（正则条件），而情形 1 不必？因为情形 1 的衰减已经由假设 $f=O(n^{\log_b a-\varepsilon})$ 打包保证，$f$ 在缩放后自动按 $b^{-\varepsilon}$ 缩小；情形 3 只假设了「$f$ 更大」，没保证「每一层都比上一层多一个固定倍数」，层代价可能忽大忽小、不构成等比。加上 $af(n/b)\le cf(n)$，等于强制「缩放一次至少缩到 $c$ 倍」，迭代 $j$ 次才有 $c^j$ 这个公比。
>
> 还要看清两个方向的求和手法并不对称。情形 1 是递增等比（越往深越贵），求和要从最后一项倒着放大，得到「总和不超前项的常数倍」；情形 3 是递减等比（越往深越便宜），求和从首项正着放大，得到「总和不超首项的常数倍」。同一句「等比封顶」，方向相反，得到的支配者也就相反：一个由叶子说话，一个由根说话。
>
> $\varepsilon$ 与常数之间的取舍也值得量化。$\varepsilon=0.001$、$b=2$ 时 $b^{\varepsilon}-1\approx0.000693$，界前面的常数约 $1443$。渐近阶仍然是 $\Theta(n^{\log_b a})$，但在 $n=10^3$ 这种规模上，这个界比真实值松三个数量级，实用价值很低。这提醒一句：渐近结论只在 $n$ 充分大时可信，小规模必须实测，两者不能互相替代。
>
> 收束：$\varepsilon$-剥离（$\varepsilon$-stripping）的全部内容就是「先把比值变成常数公比，再让等比求和接管」；三个情形只是公比大于、等于、小于 $1$ 的三种命运。

我们现在可以证明一个适用于 $n$ 是 $b$ 的精确幂情形的 master theorem 版本。

**Lemma 4.4（引理 4.4）** <span style="color:#2471a3;">**[lemma]**</span>

设 $a \ge 1$ 与 $b > 1$ 为常数，$f(n)$ 是定义在 $b$ 的精确幂上的一个 nonnegative function。用如下递归式在 $b$ 的精确幂上定义 $T(n)$：

```math
T(n) = \begin{cases} \Theta(1) & \text{if } n = 1\,, \\ aT(n/b) + f(n) & \text{if } n = b^i\,, \end{cases}
```

其中 $i$ 是一个 positive integer。那么，对 $b$ 的精确幂，$T(n)$ 具有如下 asymptotic bounds：

1. 若对某个 constant $\epsilon > 0$ 有 $f(n) = O(n^{\log_b a - \epsilon})$，则 $T(n) = \Theta(n^{\log_b a})$。
2. 若 $f(n) = \Theta(n^{\log_b a})$，则 $T(n) = \Theta(n^{\log_b a} \lg n)$。
3. 若对某个常数 $\epsilon > 0$ 有 $f(n) = \Omega(n^{\log_b a + \epsilon})$，并且若对某个常数 $c < 1$ 以及所有 sufficiently large $n$ 有 $af(n/b) \le cf(n)$，则 $T(n) = \Theta(f(n))$。

> **Proof（证明）** <span style="color:#2471a3;">**[proof]**</span>
>
> 我们使用 Lemma 4.3 中的界来求值 Lemma 4.2 中的 summation (4.21)。对于 case 1，我们有
>
> ```math
> \begin{aligned}
> T(n) &= \Theta(n^{\log_b a}) + O(n^{\log_b a}) \\
>      &= \Theta(n^{\log_b a})\,,
> \end{aligned}
> ```
>
> （证明在第 103 书页继续。）

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.103</span>

> （接上页）**Lemma 4.4（引理 4.4）的 proof（证明）**（续）——对 case 2，我们有
>
> ```math
> \begin{aligned}
> T(n) &= \Theta(n^{\log_b a}) + \Theta(n^{\log_b a} \lg n) \\
>      &= \Theta(n^{\log_b a} \lg n)\,.
> \end{aligned}
> ```
>
> 对 case 3，
>
> ```math
> \begin{aligned}
> T(n) &= \Theta(n^{\log_b a}) + \Theta(f(n)) \\
>      &= \Theta(f(n))\,,
> \end{aligned}
> ```
>
> 因为 $f(n) = \Omega(n^{\log_b a + \epsilon})$。

### Section 4.6.2 · Floors and ceilings（下取整与上取整） <span style="color:#2471a3;">**[section]**</span>

为了完成 master theorem（主定理）的 proof，我们现在必须把分析推广到 master recurrence（主递归式）中出现 floor（下取整）与 ceiling（上取整）的情形，使该 recurrence 对所有 integers（整数）都有定义，而不只是对 $b$ 的 exact powers（精确幂）才有定义。对

```math
\tag{4.25}
T(n) = aT(\lceil n/b \rceil) + f(n)
```

求一个 lower bound（下界），以及对

```math
\tag{4.26}
T(n) = aT(\lfloor n/b \rfloor) + f(n)
```

求一个 upper bound（上界），其实都是 routine（程式化的）工作：在第一种情形下，我们可以把界 $\lceil n/b \rceil \ge n/b$ 一路推进到最后，从而得到 desired result（期望的结果）；在第二种情形下，我们可以把界 $\lfloor n/b \rfloor \le n/b$ 一路推进。我们对 recurrence (4.26) 求 lower bound 所用的技巧，与对 recurrence (4.25) 求 upper bound 所用的技巧大致相同，因此下面只给出后一种界。

我们修改图 4.7 的 recursion tree（递归树），得到图 4.8 中的递归树。当沿着递归树逐层向下时，我们会得到对如下 arguments（参数）的一连串 recursive invocations（递归调用）：

```math
n, \quad \lceil n/b \rceil, \quad \lceil \lceil n/b \rceil / b \rceil, \quad \lceil \lceil \lceil n/b \rceil / b \rceil / b \rceil, \quad \ldots
```

记该 sequence（序列）中的第 $j$ 个元素为 $n_j$，其中

```math
\tag{4.27}
n_j = \begin{cases} n & \text{if } j = 0\,, \\ \lceil n_{j-1}/b \rceil & \text{if } j > 0\,. \end{cases}
```

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.104</span>

> <span style="color:#7f8c8d;">[note] 本页含整页插图：图 4.8（递归树）。图面结构：与图 4.7 类似的一棵 $a$ 叉递归树，但对应的是 $T(n) = aT(\lceil n/b \rceil) + f(n)$：根结点代价 $f(n)$，它有 $a$ 个孩子，每个孩子代价为 $f(n_1)$；第二层共 $a^2$ 个结点，每个代价为 $f(n_2)$；中间各层以 "…" 省略。右侧标注各 depth（深度）的层代价：第 0 层为 $f(n)$，第 1 层为 $a f(n_1)$，第 2 层为 $a^2 f(n_2)$，……，最底层（深度 $\lfloor \log_b n \rfloor$）共 $n^{\log_b a}$ 片叶子，每片代价 $\Theta(1)$，合计 $\Theta(n^{\log_b a})$。图底给出 Total（总代价）：$\Theta(n^{\log_b a}) + \sum_{j=0}^{\lfloor \log_b n \rfloor - 1} a^j f(n_j)$。</span>

**Figure 4.8（图 4.8）** 由 $T(n) = aT(\lceil n/b \rceil) + f(n)$ 生成的 recursion tree（递归树）。recursive argument（递归参数）$n_j$ 由 equation（式）(4.27) 给出。

> （接上页）我们的第一个目标是确定 depth（深度）$k$，使得 $n_k$ 是一个 constant（常数）。利用 inequality（不等式）$\lceil x \rceil \le x + 1$，我们得到

```math
\begin{aligned}
n_0 &\le n\,, \\
n_1 &\le n/b + 1\,, \\
n_2 &\le n/b^2 + 1/b + 1\,, \\
n_3 &\le n/b^3 + 1/b^2 + 1/b + 1\,, \\
    &\;\,\vdots
\end{aligned}
```

一般地，我们有（接下页）

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.105</span>

> （接上页）
>
> ```math
> n_j \le \frac{n}{b^j} + \sum_{i=0}^{j-1} \frac{1}{b^i} < \frac{n}{b^j} + \sum_{i=0}^{\infty} \frac{1}{b^i} = \frac{n}{b^j} + \frac{b}{b-1}\,.
> ```
>
> 令 $j = \lfloor \log_b n \rfloor$，我们得到
>
> ```math
> \begin{aligned}
> n_{\lfloor \log_b n \rfloor} &< \frac{n}{b^{\lfloor \log_b n \rfloor}} + \frac{b}{b-1} \\
> &< \frac{n}{b^{\log_b n - 1}} + \frac{b}{b-1} \\
> &= \frac{n}{n/b} + \frac{b}{b-1} \\
> &= b + \frac{b}{b-1} \\
> &= O(1)\,,
> \end{aligned}
> ```
>
> 从而我们看到，在 depth（深度）$\lfloor \log_b n \rfloor$ 处，problem size（问题规模）至多是一个 constant（常数）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注要回答的是：为什么 $\lfloor n/b\rfloor$、$\lceil n/b\rceil$、$n/b$ 三种写法可以互换。答案不是「差别很小」，而是「差别累积不起来」——取整误差每层只加一，但每往深一层就被再除一次 $b$，累积总和是一个公比 $1/b$ 的几何级数，其和与深度无关。
>
> 机制逐层展开。设 $n_j$ 是第 $j$ 层的规模，由 $\lceil x\rceil\le x+1$ 得 $n_j\le n_{j-1}/b+1$。连续代入：$n_1\le n/b+1$，$n_2\le n/b^2+1/b+1$，一般地 $n_j\le n/b^j+\sum_{i=0}^{j-1}b^{-i}<n/b^j+b/(b-1)$。关键在最后一步：误差项里那个「$1$」在第 $i$ 层引入、到第 $j$ 层已经被除了 $j-i$ 次，于是总和是一个无穷等比级数，上界 $b/(b-1)$ 只与 $b$ 有关。$b=2$ 时界为 $2$，$b=3$ 时为 $1.5$，$b$ 越大误差越无处藏身。
>
> 数字复核。取 $b=2$、$n=1000$，实际序列是 $1000\to500\to250\to125\to63\to32\to16\to8\to4\to2\to1$。第 $4$ 层 $n/2^4=62.5$，加上界 $2$ 得 $64.5$，确实压住实际的 $63$；第 $10$ 层 $n/1024\approx0.977$，加上 $2$ 得 $2.977$，压住实际的 $1$。取 $b=3$、$n=100$：序列 $100\to34\to12\to4\to2\to1$；第 $3$ 层 $100/27\approx3.70$ 加 $1.5$ 得 $5.2$，压住实际的 $4$。
>
> 为什么这个界够用？因为主定理的证明要把 $f(n_j)$ 与 $f(n/b^j)$ 相比。若 $f$ 是多项式或多项式乘对数，$n_j$ 与 $n/b^j$ 只差一个相乘的常数因子，而这个常数落在 $f$ 里就是常数倍，不改变任何渐近结论；三个情形的论证因此可以原封不动搬过来。换句话说，「取整无关紧要」这句话的全部数学内容，就是这行几何级数的界。
>
> 一个容易误读的地方：界里的 $b/(b-1)$ 不是误差的精确值，而是最坏情况的封顶。实际误差往往比它小得多（$n=1000$、$b=2$、第 $4$ 层只差 $0.5$），但证明只需要「有界」，不需要「精确」。这正是渐近分析的一贯做法：能封顶就不必算准。
>
> 跨课程连接：CSAPP 第 2 章讨论浮点舍入时，单个运算的误差有界不难，难的是证明误差随迭代不放大；这里给出「不放大」的机制——几何衰减。区别是浮点误差通常用相对误差描述、且依赖舍入模式，这里是绝对误差、且只依赖 $b$。CSAPP 第 6 章算 average memory access time（平均访存时间）用的是同一个求和形状：$AMAT=h+m\cdot AMAT'$，展开得 $h(1+m+m^2+\cdots)$，只要缺失率 $m<1$ 就被几何级数封住；取 $h=1$、$m=0.05$、下一层 $10$ 周期，两层模型给出 $AMAT=1.5$ 周期，三层模型（$20$ 周期层、缺失率 $0.2$）给出 $2.5$ 周期。区别是 cache 的层数是硬件固定的有限层，而这里的 $j$ 可以走到 $\log_b n$。
>
> 顺带说清 $b>1$ 这个前提为什么不能松。若 $b=1$，递归规模根本不缩小，误差按 $n_j\le n_{j-1}+1$ 线性累积，$j$ 层之后误差是 $j$，与层数同阶，任何封顶都失效；而层数本身又随 $n$ 增长，于是「取整无关紧要」这句话彻底不成立。主定理把 $b>1$ 写进前提，正是为了保证误差有地方衰减，而不是因为记号好看。
>
> 下界方向要做一次镜像。用 $\lfloor x\rfloor\ge x-1$ 得 $n_j\ge n_{j-1}/b-1$，展开后 $n_j>n/b^j-b/(b-1)$，同一个常数又出现了。取 $b=2$、$n=1000$、第 $4$ 层：区间是 $[60.5,64.5]$，实际的 $63$ 落在里面。上下界共用同一个常数，才敢下结论说两者只差常数因子——只证一侧是不够的。
>
> 收束：把「取整不影响阶」当成常识背下来是危险的；它其实是由 $\lceil x\rceil\le x+1$ 加上一次等比求和得来的定理，缺了这一步，主定理的证明就少了一块地基。

由图 4.8，我们看到

```math
\tag{4.28}
T(n) = \Theta(n^{\log_b a}) + \sum_{j=0}^{\lfloor \log_b n \rfloor - 1} a^j f(n_j)\,,
```

它与 equation（式）(4.21) 非常相似，区别只在于这里的 $n$ 是一个 arbitrary integer（任意整数），而不限定为 $b$ 的 exact powers（精确幂）。

现在，我们可以用一种与 Lemma 4.3（引理 4.3）的证明相类似的方式来求值 equation (4.28) 中的 summation（求和式）

```math
\tag{4.29}
g(n) = \sum_{j=0}^{\lfloor \log_b n \rfloor - 1} a^j f(n_j)\,.
```

先从 case 3 入手：若当 $n > b + b/(b-1)$ 时有 $a f(\lceil n/b \rceil) \le c f(n)$，其中 $c < 1$ 是一个 constant（常数），则可以推出 $a^j f(n_j) \le c^j f(n)$。因此，我们可以像 Lemma 4.3 中那样求值 equation (4.29) 中的和。对 case 2，我们有 $f(n) = \Theta(n^{\log_b a})$。如果我们能够证明 $f(n_j) = O(n^{\log_b a} / a^j) = O((n/b^j)^{\log_b a})$，那么 Lemma 4.3 中 case 2 的证明便可顺利通过。注意，$j \le \lfloor \log_b n \rfloor$ 蕴含 $b^j/n \le 1$。界 $f(n) = O(n^{\log_b a})$ 意味着存在某个 constant $c > 0$，使得对所有 sufficiently large（足够大的）$n_j$，有（接下页）

---

> <span style="color:#7f8c8d;">CLRS §4.6, p.106</span>

> （接上页）
>
> ```math
> \begin{aligned}
> f(n_j) &\le c\left(\frac{n}{b^j} + \frac{b}{b-1}\right)^{\log_b a} \\
>        &= c\left(\frac{n}{b^j}\left(1 + \frac{b^j}{n} \cdot \frac{b}{b-1}\right)\right)^{\log_b a} \\
>        &= c\left(\frac{n^{\log_b a}}{a^j}\right)\left(1 + \frac{b^j}{n} \cdot \frac{b}{b-1}\right)^{\log_b a} \\
>        &\le c\left(\frac{n^{\log_b a}}{a^j}\right)\left(1 + \frac{b}{b-1}\right)^{\log_b a} \\
>        &= O\left(\frac{n^{\log_b a}}{a^j}\right),
> \end{aligned}
> ```
>
> 因为 $c\,(1 + b/(b-1))^{\log_b a}$ 是一个 constant（常数）。于是，我们证明了 case 2。case 1 的证明几乎完全相同。关键在于证明界 $f(n_j) = O((n/b^j)^{\log_b a - \epsilon})$，它与 case 2 的相应证明类似，只是代数推导更为 intricate（复杂繁琐）。

至此，我们已经对所有的 integers（整数）$n$ 证明了 master theorem（主定理）中的 upper bounds（上界）。lower bounds（下界）的证明与之类似。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**4.6-1** $\star$

Give a simple and exact expression for $n_j$ in equation (4.27) for the case in which $b$ is a positive integer instead of an arbitrary real number.

**4.6-2** $\star$

Show that if $f(n) = \Theta(n^{\log_b a} \lg^k n)$, where $k \ge 0$, then the master recurrence has solution $T(n) = \Theta(n^{\log_b a} \lg^{k+1} n)$. For simplicity, confine your analysis to exact powers of $b$.

**4.6-3** $\star$

Show that case 3 of the master theorem is overstated, in the sense that the regularity condition $a f(n/b) \le c f(n)$ for some constant $c < 1$ implies that there exists a constant $\epsilon > 0$ such that $f(n) = \Omega(n^{\log_b a + \epsilon})$.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 4, p.107</span>

## Problems for Chapter 4（第 4 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 4-1 · Recurrence examples（递归式例题） <span style="color:#2471a3;">**[problem]**</span>

Give asymptotic upper and lower bounds for $T(n)$ in each of the following recurrences. Assume that $T(n)$ is constant for $n \le 2$. Make your bounds as tight as possible, and justify your answers.

a. $T(n) = 2T(n/2) + n^4$.

b. $T(n) = T(7n/10) + n$.

c. $T(n) = 16T(n/4) + n^2$.

d. $T(n) = 7T(n/3) + n^2$.

e. $T(n) = 7T(n/2) + n^2$.

f. $T(n) = 2T(n/4) + \sqrt{n}$.

g. $T(n) = T(n-2) + n^2$.

### Problem 4-2 · Parameter-passing costs（参数传递的代价） <span style="color:#2471a3;">**[problem]**</span>

Throughout this book, we assume that parameter passing during procedure calls takes constant time, even if an $N$-element array is being passed. This assumption is valid in most systems because a pointer to the array is passed, not the array itself. This problem examines the implications of three parameter-passing strategies:

1. An array is passed by pointer. Time $= \Theta(1)$.
2. An array is passed by copying. Time $= \Theta(N)$, where $N$ is the size of the array.
3. An array is passed by copying only the subrange that might be accessed by the called procedure. Time $= \Theta(q - p + 1)$ if the subarray $A[p \mathrel{..} q]$ is passed.

a. Consider the recursive binary search algorithm for finding a number in a sorted array (see Exercise 2.3-5). Give recurrences for the worst-case running times of binary search when arrays are passed using each of the three methods above, and give good upper bounds on the solutions of the recurrences. Let $N$ be the size of the original problem and $n$ be the size of a subproblem.

b. Redo part (a) for the MERGE-SORT algorithm from Section 2.3.1.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 4, p.108</span>

### Problem 4-3 · More recurrence examples（更多递归式例题） <span style="color:#2471a3;">**[problem]**</span>

Give asymptotic upper and lower bounds for $T(n)$ in each of the following recurrences. Assume that $T(n)$ is constant for sufficiently small $n$. Make your bounds as tight as possible, and justify your answers.

a. $T(n) = 4T(n/3) + n \lg n$.

b. $T(n) = 3T(n/3) + n/\lg n$.

c. $T(n) = 4T(n/2) + n^2 \sqrt{n}$.

d. $T(n) = 3T(n/3 - 2) + n/2$.

e. $T(n) = 2T(n/2) + n/\lg n$.

f. $T(n) = T(n/2) + T(n/4) + T(n/8) + n$.

g. $T(n) = T(n-1) + 1/n$.

h. $T(n) = T(n-1) + \lg n$.

i. $T(n) = T(n-2) + 1/\lg n$.

j. $T(n) = \sqrt{n}\, T(\sqrt{n}) + n$.

### Problem 4-4 · Fibonacci numbers（斐波那契数） <span style="color:#2471a3;">**[problem]**</span>

This problem develops properties of the Fibonacci numbers, which are defined by recurrence (3.22). We shall use the technique of generating functions to solve the Fibonacci recurrence. Define the generating function (or formal power series) $F$ as

```math
F(z) = \sum_{i=0}^{\infty} F_i z^i = 0 + z + z^2 + 2z^3 + 3z^4 + 5z^5 + 8z^6 + 13z^7 + 21z^8 + \cdots\,,
```

where $F_i$ is the $i$th Fibonacci number.

a. Show that $F(z) = z + z F(z) + z^2 F(z)$.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 4, p.109</span>

### Problem 4-4 · Fibonacci numbers（斐波那契数） <span style="color:#2471a3;">**[problem]**</span>（续）

b. Show that

```math
F(z) = \frac{z}{1 - z - z^2} = \frac{z}{(1 - \phi z)(1 - \widehat{\phi} z)} = \frac{1}{\sqrt{5}}\left(\frac{1}{1 - \phi z} - \frac{1}{1 - \widehat{\phi} z}\right),
```

where

```math
\phi = \frac{1 + \sqrt{5}}{2} = 1.61803\ldots \quad\text{and}\quad \widehat{\phi} = \frac{1 - \sqrt{5}}{2} = -0.61803\ldots\,.
```

c. Show that

```math
F(z) = \sum_{i=0}^{\infty} \frac{1}{\sqrt{5}}\left(\phi^i - \widehat{\phi}^{\,i}\right) z^i\,.
```

d. Use part (c) to prove that $F_i = \phi^i/\sqrt{5}$ for $i > 0$, rounded to the nearest integer. (Hint: Observe that $\left|\widehat{\phi}\right| < 1$.)

### Problem 4-5 · Chip testing（芯片测试） <span style="color:#2471a3;">**[problem]**</span>

Professor Diogenes has $n$ supposedly identical integrated-circuit chips that in principle are capable of testing each other. The professor's test jig accommodates two chips at a time. When the jig is loaded, each chip tests the other and reports whether it is good or bad. A good chip always reports accurately whether the other chip is good or bad, but the professor cannot trust the answer of a bad chip. Thus, the four possible outcomes of a test are as follows:

| Chip A says | Chip B says | Conclusion |
|---|---|---|
| B is good | A is good | both are good, or both are bad |
| B is good | A is bad | at least one is bad |
| B is bad | A is good | at least one is bad |
| B is bad | A is bad | at least one is bad |

a. Show that if at least $n/2$ chips are bad, the professor cannot necessarily determine which chips are good using any strategy based on this kind of pairwise test. Assume that the bad chips can conspire to fool the professor.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 4, p.110</span>

### Problem 4-5 · Chip testing（芯片测试） <span style="color:#2471a3;">**[problem]**</span>（续）

b. Consider the problem of finding a single good chip from among $n$ chips, assuming that more than $n/2$ of the chips are good. Show that $\lfloor n/2 \rfloor$ pairwise tests are sufficient to reduce the problem to one of nearly half the size.

c. Show that the good chips can be identified with $\Theta(n)$ pairwise tests, assuming that more than $n/2$ of the chips are good. Give and solve the recurrence that describes the number of tests.

### Problem 4-6 · Monge arrays（蒙日阵列） <span style="color:#2471a3;">**[problem]**</span>

An $m \times n$ array $A$ of real numbers is a **Monge array（蒙日阵列）** if for all $i$, $j$, $k$, and $l$ such that $1 \le i < k \le m$ and $1 \le j < l \le n$, we have

```math
A[i, j] + A[k, l] \le A[i, l] + A[k, j]\,.
```

In other words, whenever we pick two rows and two columns of a Monge array and consider the four elements at the intersections of the rows and the columns, the sum of the upper-left and lower-right elements is less than or equal to the sum of the lower-left and upper-right elements. For example, the following array is Monge:

```math
\begin{pmatrix}
10 & 17 & 13 & 28 & 23 \\
17 & 22 & 16 & 29 & 23 \\
24 & 28 & 22 & 34 & 24 \\
11 & 13 & 6  & 17 & 7  \\
45 & 44 & 32 & 37 & 23 \\
36 & 33 & 19 & 21 & 6  \\
75 & 66 & 51 & 53 & 34
\end{pmatrix}
```

a. Prove that an array is Monge if and only if for all $i = 1, 2, \ldots, m-1$ and $j = 1, 2, \ldots, n-1$, we have

```math
A[i, j] + A[i+1, j+1] \le A[i, j+1] + A[i+1, j]\,.
```

(Hint: For the "if" part, use induction separately on rows and columns.)

b. The following array is not Monge. Change one element in order to make it Monge. (Hint: Use part (a).)

```math
\begin{pmatrix}
37 & 23 & 22 & 32 \\
21 & 6  & 7  & 10 \\
53 & 34 & 30 & 31 \\
32 & 13 & 9  & 6  \\
43 & 21 & 15 & 8
\end{pmatrix}
```

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 4 / Chapter notes, p.111</span>

### Problem 4-6 · Monge arrays（蒙日阵列） <span style="color:#2471a3;">**[problem]**</span>（续）

c. Let $f(i)$ be the index of the column containing the leftmost minimum element of row $i$. Prove that $f(1) \le f(2) \le \cdots \le f(m)$ for any $m \times n$ Monge array.

d. Here is a description of a divide-and-conquer algorithm that computes the leftmost minimum element in each row of an $m \times n$ Monge array $A$:

> Construct a submatrix $A'$ of $A$ consisting of the even-numbered rows of $A$. Recursively determine the leftmost minimum for each row of $A'$. Then compute the leftmost minimum in the odd-numbered rows of $A$.

Explain how to compute the leftmost minimum in the odd-numbered rows of $A$ (given that the leftmost minimum of the even-numbered rows is known) in $O(m + n)$ time.

e. Write the recurrence describing the running time of the algorithm described in part (d). Show that its solution is $O(m + n \log m)$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Monge array（蒙日阵列）这条注处理的是一个结构性问题：一个 $m\times n$ 的矩阵如果满足任意两行两列的四点不等式，就能保证「每行最左最小值的位置随行号不减」。这条性质把逐格搜索的 $O(mn)$ 压到近线性，而它的来源是两百多年前的运输问题。
>
> 历史与人物：Gaspard Monge（1746–1818）在 1781 年的《Mémoire sur la théorie des déblais et des remblais》里研究土方运输——把挖出来的土运到填方处，怎样最省。他要求「运输路线不相交」，这个几何直觉翻译成矩阵语言就是 $A[i,j]+A[k,l]\le A[i,l]+A[k,j]$：对角两项之和不超过交叉两项之和（此出处一手核实于 1781 年论文标题与内容，卷页细节未能一手核实）。Monge 也是画法几何的奠基人、巴黎综合理工学院的创办者之一，但这条注只需要记住他要解决的具体问题：把「不相交」变成一个可检验的不等式。
>
> 机制分两层。第一层是「局部推出全局」：部分 (a) 证明只需检查相邻的 $2\times2$ 子块，即 $A[i,j]+A[i+1,j+1]\le A[i,j+1]+A[i+1,j]$。原因是任意 $i<k$、$j<l$ 的四点不等式，可以沿行方向与列方向把相邻条件累加得到；累加时中间项两两抵消，剩下的正是四个角。第二层是 total monotonicity（总单调性）：设 $f(i)$ 为第 $i$ 行最左最小值的列号，若存在 $i<k$ 使 $f(i)>f(k)$，取 $j=f(k)$、$l=f(i)$（此时 $j<l$），四点不等式立刻与「两个都是最小值」矛盾，故 $f$ 非减。
>
> 用正文那个 $7\times5$ 的矩阵复核。逐行最小值：第一行 $10$ 在第一列，第二行 $16$ 在第三列，第三行 $22$ 在第三列，第四行 $6$ 在第三列，第五行 $23$ 在第五列，第六行 $6$ 在第五列，第七行 $34$ 在第五列。于是 $f=(1,3,3,3,5,5,5)$，确实非减。再抽查两个 $2\times2$：行 $1,2$ 列 $1,2$ 得 $10+22=32\le17+17=34$；行 $4,5$ 列 $3,5$ 得 $6+23=29\le7+32=39$。这两处都成立，说明该矩阵确实蒙日。
>
> 威力的量化。逐格扫描要比较 $mn$ 次，本例是 $35$ 次；SMAWK algorithm（SMAWK 算法）对 $m\times n$ 的总单调矩阵只需 $O(m(1+\log(n/m)))$ 次比较，$m=n$ 时是线性。该算法由 Aggarwal、Klawe、Moran、Shor、Wilber 五人在 1987 年发表于 Algorithmica 的《Geometric applications of a matrix-searching algorithm》中提出（卷期页码一手核实为 2:195–208），名字取五人姓氏首字母。习题 4-6 的 (d)(e) 两问给出另一条分治路线，复杂度 $O(m+n\log m)$，与 SMAWK 的目标相同、手段不同。
>
> 跨课程连接：6.042J 的 partial order（偏序）与这里的关系值得辨清。$f$ 的取值把行排成一条全序链（数值比较给出可比的次序），而偏序只要求自反、反对称、传递，允许不可比；区别在于链来自「最小值位置」这个数值不变量，而不是来自集合包含关系。另一条连接在动态规划：许多区间划分问题的代价矩阵满足 quadrangle inequality（四边形不等式），于是决策点单调，可以把 $O(n^2)$ 的枚举压到近 $O(n)$；区别是那里要在每层 DP 里维护决策点区间，而这里只需一次行最小值查询。
>
> 规模再大一些，差距更明显：$m=n=1000$ 时逐格扫描要 $10^6$ 次比较，而 SMAWK 只需 $O(m+n)$ 量级的两千次左右，相差约五百倍；这也是为什么这条性质在竞赛与工程里被反复使用。
>
> 收束：蒙日性质的价值不在定义式本身，而在它把「全局最优」翻译成「局部不等式」，再翻译成「位置单调」——三步翻译，每一步都可以手算验证。

### Chapter notes（章末注释） <span style="color:#2471a3;">**[reference]**</span>

Divide-and-conquer as a technique for designing algorithms dates back to at least 1962 in an article by Karatsuba and Ofman [194]. It might have been used well before then, however; according to Heideman, Johnson, and Burrus [163], C. F. Gauss devised the first fast Fourier transform algorithm in 1805, and Gauss's formulation breaks the problem into smaller subproblems whose solutions are combined.

The maximum-subarray problem in Section 4.1 is a minor variation on a problem studied by Bentley [43, Chapter 7].

Strassen's algorithm [325] caused much excitement when it was published in 1969. Before then, few imagined the possibility of an algorithm asymptotically faster than the basic SQUARE-MATRIX-MULTIPLY procedure. The asymptotic upper bound for matrix multiplication has been improved since then. The most asymptotically efficient algorithm for multiplying $n \times n$ matrices to date, due to Coppersmith and Winograd [78], has a running time of $O(n^{2.376})$. The best lower bound known is just the obvious $\Omega(n^2)$ bound (obvious because we must fill in $n^2$ elements of the product matrix).

From a practical point of view, Strassen's algorithm is often not the method of choice for matrix multiplication, for four reasons:

1. The constant factor hidden in the $\Theta(n^{\lg 7})$ running time of Strassen's algorithm is larger than the constant factor in the $\Theta(n^3)$-time SQUARE-MATRIX-MULTIPLY procedure.

2. When the matrices are sparse, methods tailored for sparse matrices are faster.（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter notes, p.112</span>

### Chapter notes（章末注释） <span style="color:#2471a3;">**[reference]**</span>（续）

（接上页）

3. Strassen's algorithm is not quite as numerically stable as SQUARE-MATRIX-MULTIPLY. In other words, because of the limited precision of computer arithmetic on noninteger values, larger errors accumulate in Strassen's algorithm than in SQUARE-MATRIX-MULTIPLY.

4. The submatrices formed at the levels of recursion consume space.

The latter two reasons were mitigated around 1990. Higham [167] demonstrated that the difference in numerical stability had been overemphasized; although Strassen's algorithm is too numerically unstable for some applications, it is within acceptable limits for others. Bailey, Lee, and Simon [32] discuss techniques for reducing the memory requirements for Strassen's algorithm.

In practice, fast matrix-multiplication implementations for dense matrices use Strassen's algorithm for matrix sizes above a "crossover point," and they switch to a simpler method once the subproblem size reduces to below the crossover point. The exact value of the crossover point is highly system dependent. Analyses that count operations but ignore effects from caches and pipelining have produced crossover points as low as $n = 8$ (by Higham [167]) or $n = 12$ (by Huss-Lederman et al. [186]). D'Alberto and Nicolau [81] developed an adaptive scheme, which determines the crossover point by benchmarking when their software package is installed. They found crossover points on various systems ranging from $n = 400$ to $n = 2150$, and they could not find a crossover point on a couple of systems.

Recurrences were studied as early as 1202 by L. Fibonacci, for whom the Fibonacci numbers are named. A. De Moivre introduced the method of generating functions (see Problem 4-4) for solving recurrences. The master method is adapted from Bentley, Haken, and Saxe [44], which provides the extended method justified by Exercise 4.6-2. Knuth [209] and Liu [237] show how to solve linear recurrences using the method of generating functions. Purdom and Brown [287] and Graham, Knuth, and Patashnik [152] contain extended discussions of recurrence solving.

Several researchers, including Akra and Bazzi [13], Roura [299], Verma [346], and Yap [360], have given methods for solving more general divide-and-conquer recurrences than are solved by the master method. We describe the result of Akra and Bazzi here, as modified by Leighton [228]. The Akra-Bazzi method works for recurrences of the form

```math
\tag{4.30}
T(x) = \begin{cases} \Theta(1) & \text{if } 1 \le x \le x_0\,, \\[1ex] \displaystyle\sum_{i=1}^{k} a_i T(b_i x) + f(x) & \text{if } x > x_0\,, \end{cases}
```

where

- $x \ge 1$ is a real number,
- $x_0$ is a constant such that $x_0 \ge 1/b_i$ and $x_0 \ge 1/(1 - b_i)$ for $i = 1, 2, \ldots, k$,
- $a_i$ is a positive constant for $i = 1, 2, \ldots, k$,（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter 4 Notes, p.113</span>

## Chapter 4（第 4 章）· Notes for Chapter 4（第 4 章注释） <span style="color:#2471a3;">**[reference]**</span>

（章末 Notes 按规范保留英文原文）

- $b_i$ is a constant in the range $0 < b_i < 1$ for $i = 1, 2, \ldots, k$,
- $k \ge 1$ is an integer constant, and
- $f(x)$ is a nonnegative function that satisfies the polynomial-growth condition: there exist positive constants $c_1$ and $c_2$ such that for all $x \ge 1$, for $i = 1, 2, \ldots, k$, and for all $u$ such that $b_i x \le u \le x$, we have $c_1 f(x) \le f(u) \le c_2 f(x)$. (If $|f'(x)|$ is upper-bounded by some polynomial in $x$, then $f(x)$ satisfies the polynomial-growth condition. For example, $f(x) = x^\alpha \lg^\beta x$ satisfies this condition for any real constants $\alpha$ and $\beta$.)

Although the master method does not apply to a recurrence such as $T(n) = T(\lfloor n/3 \rfloor) + T(\lfloor 2n/3 \rfloor) + O(n)$, the Akra-Bazzi method does. To solve the recurrence (4.30), we first find the unique real number $p$ such that

```math
\sum_{i=1}^{k} a_i b_i^p = 1.
```

(Such a $p$ always exists.) The solution to the recurrence is then

```math
T(n) = \Theta\left(x^p \left(1 + \int_1^x \frac{f(u)}{u^{p+1}}\,du\right)\right).
```

The Akra-Bazzi method can be somewhat difficult to use, but it serves in solving recurrences that model division of the problem into substantially unequally sized subproblems. The master method is simpler to use, but it applies only when subproblem sizes are equal.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Akra–Bazzi method（Akra–Bazzi 方法）要解决的问题很具体：master theorem（主定理）要求所有子问题规模相同，都是 $n/b$；但快速排序按任意比例切分、中位数选择算法一次切成 $n/5$ 与 $7n/10$，这些递归式的子问题规模各不相同，主定理直接失效。
>
> 历史与出处：该方法由 Mohamad Akra 与 Louay Bazzi 在 1998 年提出，论文题为《On the solution of linear recurrence equations》，刊于 Computational Optimization and Applications 第 10 卷第 2 期 195–210 页（此条一手核实）。CLRS 章末注释采用的是一个更易讲的表述，通常归给 Leighton；具体引用编号未能一手核实。记住作者与年份的意义在于：这不是某个习题的技巧，而是把主定理真正推广到非均衡分治的一次完整工作。
>
> 机制的关键是一个方程。设递推形如 $T(x)=\sum_{i=1}^{k}a_iT(b_ix)+f(x)$，其中 $0<b_i<1$，先解 $\sum_i a_ib_i^p=1$ 定出唯一的 $p$。唯一性来自单调性：每个 $b_i^p$ 随 $p$ 严格递减，故左边严格递减，从 $+\infty$ 单调降到 $0$，只穿过 $1$ 一次。为什么要解这个方程？把试探解 $x^p$ 代入齐次部分，得 $\sum_i a_i(b_ix)^p=x^p\sum_i a_ib_i^p$，只有当求和等于 $1$ 时 $x^p$ 才真的是解——$p$ 就是这套缩放递推的特征指数，与线性递推里解特征方程是同一件事。
>
> 主定理是它的特例。取单一项、$b_1=1/b$，方程变成 $a(b^{-1})^p=1$，即 $b^p=a$，故 $p=\log_b a$；代入通解 $T(x)=\Theta(x^p(1+\int_1^xf(u)/u^{p+1}du))$，积分只负责搬运 $f$ 的贡献，形式与主定理逐条对应。
>
> 数字复核两个例子。其一，$T(n)=T(n/3)+T(2n/3)+n$：方程是 $(1/3)^p+(2/3)^p=1$，$p=1$ 时正好 $1/3+2/3=1$，故 $p=1$；积分为 $\int_1^nu/u^2du=\ln n$，于是 $T(n)=\Theta(n(1+\ln n))=\Theta(n\lg n)$。其二，$T(n)=T(n/5)+T(7n/10)+n$：解 $(0.2)^p+(0.7)^p=1$ 得 $p\approx0.8398$（数值二分求得），积分 $\int_1^nu/u^{1.8398}du=(n^{0.1602}-1)/0.1602$，乘回 $n^{0.8398}$ 恰好得 $n/0.1602$，故 $T(n)=\Theta(n)$——这正是中位数选择算法能线性的原因。
>
> $p$ 的直觉解释：规模按 $b_i$ 缩小、份数按 $a_i$ 放大，$p$ 是让两者「收支平衡」的临界指数。主定理里叶子与根对称博弈，这里每一支的权重不同，$p$ 就是加权后的平衡点；$f$ 的贡献通过积分按 $x^p$ 折算，相当于把「每层的代价」连续化后再求和。
>
> 跨课程连接：6.042J 解线性齐次递推 $T(n)=aT(n-1)+b$ 时设 $T(n)=r^n$，得特征方程 $r=a$；这里的 $\sum a_ib_i^p=1$ 是同一个动作的缩放版——把「平移一格」换成「规模乘 $b_i$」，把「$r^n$ 的增长」换成「$x^p$ 的增长」。区别是离散特征根是代数方程的解，这里的 $p$ 一般没有闭式，只能数值求。100B 实分析里用积分估计求和（$\sum f(k)\approx\int f$）也在同一处出现：通解里那个积分就是把层代价的离散求和换成连续积分。
>
> 它的适用边界要说清：$b_i$ 必须是常数，$k$ 必须是常数，且 $f$ 要「温和」——通常要求 $f$ 多项式有界、导数也受多项式控制，指数增长或剧烈振荡的 $f$ 会让通解里的积分失控。还有一类递归式连它也管不了：$T(n)=\sqrt n\cdot T(\sqrt n)+n$ 里子问题的个数本身随 $n$ 变化，不满足「常数个常数比例」的前提，只能退回递归树逐层看。这一点在公开的算法讲义附录里被明确列为方法的例外（一手核实于 Jeff Erickson 的算法讲义附录）。
>
> 顺带体会 $p$ 的符号。若 $\sum_i a_i<1$，则 $p=0$ 时方程左边小于 $1$，需要 $p<0$ 才能补到 $1$；这对应「每一层的总工作量在收缩」，解可能是次线性甚至常数级。主定理三情形把注意力全放在 $p>0$ 的幂次竞争中，反而看不到这个角落；Akra–Bazzi 的通解把 $p$ 当成一个实数参数，符号自然处理。
>
> 收束：遇到子问题规模不齐的分治，先写方程求 $p$，再算积分；主定理能解决的它都能解决，主定理解决不了的它往往也能。

---

> <span style="color:#7f8c8d;">CLRS Chapter 5, §5.1, p.114</span>

## Chapter 5（第 5 章）· Probabilistic Analysis and Randomized Algorithms（概率分析与随机化算法） <span style="color:#2471a3;">**[section]**</span>

本章介绍 probabilistic analysis（概率分析）与 randomized algorithms（随机化算法）。如果你对 probability theory（概率论）的基础知识还不熟悉，应当先阅读 Appendix C（附录 C），其中复习了这些内容。在本书中，我们还会多次重新讨论概率分析与随机化算法。

### Section 5.1 · The hiring problem（雇用问题） <span style="color:#2471a3;">**[section]**</span>

假设你需要雇用一名新的 office assistant（办公室助理）。你之前的几次雇用尝试都不成功，于是决定借助一家 employment agency（职业介绍所）。职业介绍所每天给你送来一名 candidate（候选人），你面试这个人，然后决定是否雇用他。你必须向职业介绍所支付一小笔费用才能面试一名 applicant（申请者）；然而，真正雇用一名申请者的代价要高得多，因为你必须解雇当前的办公室助理，并向职业介绍所支付一笔数额可观的 hiring fee（雇用费）。你承诺在任何时刻都要为这个职位保留最合适的人选。因此你决定：每面试完一名申请者，如果这名申请者比当前的办公室助理更胜任，就解雇当前的助理并雇用这名新申请者。你愿意为这一策略付出相应的代价，但你希望事先估计出这个代价会有多大。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注要回答的是：为什么值得把「招一个助理」郑重其事地抽象成算法问题。剥掉面试、简历这些细节，剩下的是一个纯粹的 online（在线）结构：输入逐个到达，每到一个就必须立刻做不可撤销的决定，而后面还有多少、长什么样，你永远不知道。
>
> 成本模型也值得单独说。这里统计的不是指令条数，而是两种现实成本：每次面试花 $c_i$，每次雇用花 $c_h$，总代价是 $c_in+c_h\cdot k$，其中 $k$ 是雇用次数。这与第 2 章分析运行时间是同一套方法——都在数「某个基本操作发生了多少次」，只是把「操作」换成了「花钱的动作」。建模的第一步永远是选定成本模型，模型选错，后面算得再准也没用。
>
> 最坏情况很悲观。若候选人恰好按能力递增的顺序到达，每一个都比现任强，于是每个都要雇，总代价是 $c_hn$；$n=100$、$c_h=10000$ 时是 $10^6$。但这个最坏情形要求一种极特殊的排列，把它当成「典型情况」是过度悲观。
>
> 概率分析接手。假设到达顺序是均匀随机排列，定义 $X_i$ 为「第 $i$ 个候选人被雇用」的指示器，则 $X_i=1$ 当且仅当他比前 $i-1$ 个都强，概率是 $1/i$（前 $i$ 个里最强的恰落在最后一位）。于是期望雇用次数是 $\sum_{i=1}^n1/i=H_n$，期望总代价是 $c_in+c_hH_n$。取 $n=10$：$H_{10}\approx2.929$，若 $c_i=1$、$c_h=100$，代价约 $10+292.9=302.9$，而最坏是 $1000$，改善约三倍；取 $n=100$：$H_{100}\approx5.187$，代价约 $100+518.7=618.7$，最坏 $10000$，改善约十六倍。候选人增加十倍，雇用次数只从 $2.93$ 涨到 $5.19$，这就是对数的形状。
>
> 方法论上还有一个转折：与其假设「输入是随机的」，不如自己把随机性造出来。这就是 randomized algorithm（随机化算法）的由来——把候选人名单提前拿到，每天随机抽一个来面试，于是顺序由算法控制，分析时对随机数生成器的输出取 expectation（期望），得到的叫 expected running time（期望运行时间），与输入分布决定的 average-case running time（平均情况运行时间）区分开。前者你能保证，后者只能祈祷。
>
> 同族的经典问题是 secretary problem（秘书问题）：必须当场决定要不要录用，不能回头。最优策略是阈值式的——先面试并拒绝前约 $n/e$ 个（$n=100$ 时约 $37$ 个）作为样本，之后遇到第一个比样本中所有人都强的就录用；这个策略选中最优者的概率趋近 $1/e\approx0.368$。它说明在线结构里的最优解往往不是「更聪明的比较」，而是「把一部分信息当学费交掉」。
>
> 跨课程连接：CSAPP 第 11 章讲 socket 时反复强调字节流只能顺序读、读到就消费掉，与这里「输入单向到达、决定不可撤销」是同一个约束；区别是网络层可以用缓冲和重传弥补，雇用决定没有重传。6.042J 的 linearity of expectation（期望线性性）是下一节全部计算的引擎，它允许把总雇用次数拆成逐个候选人的贡献相加，哪怕这些事件之间并不独立。
>
> 收束：雇用问题的价值不在招人，而在它把「在线决策 + 成本模型 + 概率分析」三件事压成一个最小模型；学会在这个模型上提问，比记住 $H_n$ 的数值重要得多。

下面给出的 procedure（过程）HIRE-ASSISTANT 用 pseudocode（伪代码）表达了这一雇用策略。它假设办公室助理职位的候选人编号为 $1$ 到 $n$。该过程假设：在面试完候选人 $i$ 之后，你能够判断候选人 $i$ 是否是你目前为止见过的最佳候选人。为了完成初始化，该过程创建了一个编号为 $0$ 的 dummy candidate（占位候选人），其资历比其他所有候选人都低。

---

> <span style="color:#7f8c8d;">CLRS §5.1, p.115</span>

### Section 5.1 · The hiring problem（雇用问题）（续）

```text
HIRE-ASSISTANT(n)
 1  best = 0          // candidate 0 is a least-qualified dummy candidate
 2  for i = 1 to n
 3      interview candidate i
 4      if candidate i is better than candidate best
 5          best = i
 6          hire candidate i
```

这个问题所用的 cost model（成本模型）与第 2 章描述的模型不同。我们关注的不是 HIRE-ASSISTANT 的 running time（运行时间），而是 interview（面试）与 hire（雇用）所产生的 costs（成本）。表面上看，分析这个算法的成本似乎与分析 merge sort（归并排序）之类的运行时间很不一样；然而，无论分析的是成本还是运行时间，所使用的分析技术是完全相同的：两种情况下我们都在统计某些基本操作被执行的次数。

interviewing cost（面试成本）很低，设为 $c_i$；而 hiring cost（雇用成本）很高，设为 $c_h$。令 $m$ 为被雇用的人数，则与该算法相关的总成本为 $O(c_i n + c_h m)$。无论最终雇用了多少人，我们总是要面试 $n$ 名候选人，因而总是产生与面试相关的成本 $c_i n$。因此我们集中分析 $c_h m$，即雇用成本。这个量随算法每次运行的不同而变化。

这一场景为一种常见的 computational paradigm（计算范式）提供了模型：我们常常需要通过依次检查 sequence（序列）中的每个元素并维护一个当前"winner"（胜者）来找出序列中的最大值或最小值。雇用问题建模的正是"当前胜者是哪个元素"这一判断被更新的频率。

#### Worst-case analysis（最坏情况分析）

在最坏情况下，我们实际上会把面试的每一位候选人都雇用一遍。当候选人严格按资历递增的顺序到来时，就会出现这种情况；此时我们要雇用 $n$ 次，总雇用成本为 $O(c_h n)$。

当然，候选人并不总是按资历递增的顺序到来。事实上，我们既不知道他们到来的顺序，也无法控制这个顺序。因此，很自然地会问：在一个 typical（典型）或 average（平均）的情形下，我们预期会发生什么。

#### Probabilistic analysis（概率分析）

Probabilistic analysis（概率分析）是指在问题分析中使用 probability（概率）。最常见的是用概率分析来分析算法的 running time；有时我们也用它分析其他量，例如过程 HIRE-ASSISTANT 中的雇用成本……（接下页）

---

> <span style="color:#7f8c8d;">CLRS §5.1, p.116</span>

### Section 5.1 · The hiring problem（雇用问题）（续）

（接上页）……在过程 HIRE-ASSISTANT 中的雇用成本。为了进行概率分析，我们必须利用关于输入分布的知识，或对其做出假设，然后分析算法并计算平均情况运行时间——即在所有可能输入的分布上取平均。这样做的实际效果，就是让运行时间在所有可能的输入上取平均；报告时我们将其称为 average-case running time（平均情况运行时间）。

在决定输入分布时必须非常小心。对某些问题，我们可以对全部可能输入组成的集合做出合理的假设，此时概率分析既可以作为设计 efficient algorithm（高效算法）的技术，也可以作为洞察问题的手段。而对另一些问题，我们无法描述一个合理的输入分布，在这些情况下就不能使用概率分析。

对于雇用问题，我们可以假设申请者以 random order（随机顺序）到来。这对本问题意味着什么？我们假设可以比较任意两名候选人并判断谁更胜任；也就是说，候选人之间存在一个 total order（全序）。（total order 的定义见 Appendix B（附录 B）。）于是，我们可以用一个 $1$ 到 $n$ 之间的唯一编号给每名候选人排出名次，用 $\mathrm{rank}(i)$ 表示申请者 $i$ 的 rank（名次），并约定名次越高者越胜任。有序列表 $\langle \mathrm{rank}(1), \mathrm{rank}(2), \ldots, \mathrm{rank}(n) \rangle$ 是列表 $\langle 1, 2, \ldots, n \rangle$ 的一个 permutation（排列）。说申请者以随机顺序到来，等价于说这份名次列表等可能地是 $1$ 到 $n$ 这 $n!$ 个排列中的任何一个。换言之，我们说这些名次构成一个 uniform random permutation（均匀随机排列）；也就是说，$n!$ 种可能的排列中每一种都以相等的 probability（概率）出现。

Section 5.2（第 5.2 节）将给出雇用问题的一个概率分析。

#### Randomized algorithms（随机化算法）

要使用概率分析，我们需要对输入的分布有所了解。但在很多情况下，我们对输入分布几乎一无所知；即便知道一些，也可能无法把这个知识以计算的方式建模。然而，我们常常仍可以把 probability（概率）与 randomness（随机性）当作算法设计与分析的工具，做法是让算法的一部分行为变得 random（随机）。

在雇用问题中，候选人看上去似乎是以随机顺序呈现在我们面前的，但我们无从知道事实是否如此。因此，要为雇用问题开发一种 randomized algorithm（随机化算法），就必须对面试候选人的顺序有更大的控制权。为此，我们把模型稍作修改：假设职业介绍所有 $n$ 名候选人，并且提前把候选人列表发送给我们；每天，我们随机地选择要面试哪名候选人。虽然关于候选人本身（除了他们的名字之外）我们仍然一无所知……

---

> <span style="color:#7f8c8d;">CLRS §5.1, p.117</span>

### Section 5.1 · The hiring problem（雇用问题）（续）

（接上页）……虽然关于候选人本身（除了他们的名字之外）我们仍然一无所知，但我们已经做出了一项重大改变：我们不再去"猜测"候选人会以随机顺序到来，而是获得了对这一过程的控制，并强制实施了随机顺序。

更一般地，如果一个 algorithm（算法）的行为不仅由其 input（输入）决定，还由 random-number generator（随机数生成器）产生的值决定，我们就称它是 randomized（随机的）。我们假设手头有一个随机数生成器 RANDOM。一次调用 RANDOM(a, b) 会返回 $a$ 到 $b$ 之间（含两端）的一个 integer（整数），且每个这样的整数等可能地出现。例如，RANDOM(0, 1) 以 $1/2$ 的概率产生 $0$，以 $1/2$ 的概率产生 $1$；一次调用 RANDOM(3, 7) 返回 $3$、$4$、$5$、$6$ 或 $7$ 之一，每个的概率均为 $1/5$。RANDOM 返回的每个整数都与之前各次调用返回的整数 independent（独立）。你可以把 RANDOM 想象成掷一个有 $(b - a + 1)$ 个面的骰子来得到输出。（在实际中，大多数编程环境提供的是 pseudorandom-number generator（伪随机数生成器）：一种返回"看起来"在统计上随机的数的 deterministic algorithm（确定性算法）。）

在分析 randomized algorithm 的 running time 时，我们是对运行时间关于随机数生成器所返回值的分布取 expectation（期望）。为了把这些算法与输入为随机的算法区分开，我们将随机化算法的运行时间称为 expected running time（期望运行时间）。一般地，当 probability distribution（概率分布）是定义在算法的输入之上时，我们讨论 average-case running time（平均情况运行时间）；而当算法自身做出随机选择时，我们讨论 expected running time（期望运行时间）。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**5.1-1** Show that the assumption that we are always able to determine which candidate is best, in line 4 of procedure HIRE-ASSISTANT, implies that we know a total order on the ranks of the candidates.

**5.1-2 $\star$** Describe an implementation of the procedure RANDOM(a, b) that only makes calls to RANDOM(0, 1). What is the expected running time of your procedure, as a function of $a$ and $b$?

**5.1-3 $\star$** Suppose that you want to output 0 with probability $1/2$ and 1 with probability $1/2$. At your disposal is a procedure BIASED-RANDOM, that outputs either 0 or 1. It outputs 1 with some probability $p$ and 0 with probability $1 - p$, where $0 < p < 1$, but you do not know what $p$ is. Give an algorithm that uses BIASED-RANDOM as a subroutine, and returns an unbiased answer, returning 0 with probability $1/2$ and 1 with probability $1/2$. What is the expected running time of your algorithm as a function of $p$?

---

> <span style="color:#7f8c8d;">CLRS §5.2, p.118</span>

> <span style="color:#7f8c8d;">（注：习题 5.1-3 跨页，其末句"and 1 with probability 1/2. What is the expected running time of your algorithm as a function of p?"已并入上页该题中。）</span>

### Section 5.2 · Indicator random variables（指示器随机变量） <span style="color:#2471a3;">**[section]**</span>

为了分析包括雇用问题在内的许多算法，我们使用 indicator random variable（指示器随机变量）。指示器随机变量提供了一种在 probability（概率）与 expectation（期望）之间进行转换的便捷方法。假设给定一个 sample space（样本空间）$S$ 和一个 event（事件）$A$，那么与事件 $A$ 相关联的 indicator random variable（指示器随机变量）$I\{A\}$ 定义为

```math
I\{A\} = \begin{cases} 1 & \text{if } A \text{ occurs} \\ 0 & \text{if } A \text{ does not occur} \end{cases} \tag{5.1}
```

举一个简单的例子，我们来确定掷一枚 fair coin（均匀硬币）时得到的正面（heads）的期望次数。我们的样本空间为 $S = \{H, T\}$，其中 $\Pr\{H\} = \Pr\{T\} = 1/2$（<span style="color:#7f8c8d;">[note] 译者注：$\Pr\{\cdot\}$ 表示 probability（概率）——此说明为译者增补，原文无</span>，$H$ 表示正面朝上的事件，$T$ 表示反面朝上的事件）。于是我们可以定义一个与"硬币正面朝上"（即事件 $H$）相关联的指示器随机变量 $X_H$。这个变量统计这一次投掷中得到正面的次数：若硬币正面朝上，它取 $1$；否则取 $0$。我们写

```math
X_H = I\{H\} = \begin{cases} 1 & \text{if } H \text{ occurs} \\ 0 & \text{if } T \text{ occurs} \end{cases}
```

一次投掷硬币得到正面的 expected number（期望次数）就是这个指示器变量 $X_H$ 的 expected value（期望值）：

```math
\begin{aligned}
\mathrm{E}[X_H] &= \mathrm{E}[I\{H\}]\\
&= 1 \cdot \Pr\{H\} + 0 \cdot \Pr\{T\}\\
&= 1 \cdot (1/2) + 0 \cdot (1/2)\\
&= 1/2.
\end{aligned}
```

<span style="color:#7f8c8d;">[note] 译者注：$\mathrm{E}[\cdot]$ 表示 expected value（期望值）——此说明为译者增补，原文无。</span>

因此，掷一次均匀硬币得到正面的期望次数是 $1/2$。正如下面这条 lemma（引理）所表明的，与事件 $A$ 相关联的指示器随机变量的期望值等于事件 $A$ 发生的概率。

#### Lemma 5.1（引理 5.1） <span style="color:#2471a3;">**[lemma]**</span>

给定一个样本空间 $S$ 和样本空间 $S$ 中的一个事件 $A$，令 $X_A = I\{A\}$，则 $\mathrm{E}[X_A] = \Pr\{A\}$。

---

> <span style="color:#7f8c8d;">CLRS §5.2, p.119</span>

### Section 5.2 · Indicator random variables（指示器随机变量）（续）

> <span style="color:#2471a3;">**[proof]**</span> **Proof（证明）**  由式 (5.1) 给出的指示器随机变量定义以及期望值的定义，我们有
>
> ```math
> \begin{aligned}
> \mathrm{E}[X_A] &= \mathrm{E}[I\{A\}]\\
> &= 1 \cdot \Pr\{A\} + 0 \cdot \Pr\{\overline{A}\}\\
> &= \Pr\{A\},
> \end{aligned}
> ```
>
> 其中 $\overline{A}$ 表示 $S - A$，即 $A$ 的 complement（补事件）。

对于"统计掷一次硬币得到正面的期望次数"这样的应用，指示器随机变量看起来也许有些笨重，但在分析 repeated random trials（重复随机试验）的情形时，它们非常有用。例如，指示器随机变量为我们提供了一条到达式 (C.37) 结果的简单途径。在式 (C.37) 中，我们通过分别考虑得到 $0$ 次正面、$1$ 次正面、$2$ 次正面等的概率来计算 $n$ 次掷硬币中正面的次数。而式 (C.38) 提出的更简单方法，实际上隐式地使用了指示器随机变量。把这一论证更明确地写出来：令 $X_i$ 是与"第 $i$ 次投掷正面朝上"这一事件相关联的指示器随机变量，即 $X_i = I\{\text{the } i\text{th flip results in the event } H\}$。令 $X$ 是表示 $n$ 次掷硬币中正面总数的 random variable（随机变量），于是

```math
X = \sum_{i=1}^{n} X_i.
```

我们希望计算正面的期望次数，因此对上式两边取期望，得到

```math
\mathrm{E}[X] = \mathrm{E}\left[\sum_{i=1}^{n} X_i\right].
```

上式给出的是 $n$ 个指示器随机变量之和的期望。根据 Lemma 5.1（引理 5.1），我们可以轻松算出每个随机变量的期望；再根据式 (C.21)——linearity of expectation（期望的线性性），就容易算出和的期望：它等于这 $n$ 个随机变量的期望之和。期望的线性性使得指示器随机变量成为一种强大的分析技术；即使各随机变量之间存在 dependence（依赖性），它也依然适用。现在我们就可以轻松算出正面的期望次数了。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注要钉死一句最容易传错的话：期望的线性性不需要独立性。很多人把「独立」当成了期望可加的前提，于是在明明相关的随机变量面前不敢拆项，白绕一大圈。
>
> 机制回到定义。期望是 $\mathrm{E}[X]=\sum_x x\Pr\{X=x\}$，二元情形是对联合分布求和：$\mathrm{E}[X+Y]=\sum_x\sum_y(x+y)p(x,y)$。把求和拆成两部分，先对 $y$ 求和得 $\sum_x x\sum_y p(x,y)=\sum_x x\Pr\{X=x\}$，另一部分同理。整个过程只用到「有限和可以交换次序」和实数加法，与 $X$、$Y$ 是否互相依赖毫无关系。独立性第一次真正被需要，是在 $\mathrm{E}[XY]=\mathrm{E}[X]\mathrm{E}[Y]$ 这一步：乘积的期望要拆成期望的乘积，才必须知道联合分布等于边际之积。
>
> 反例最能说明问题。掷一枚均匀硬币，$X$ 为正面指示器、$Y$ 为反面指示器，则 $Y=1-X$，两者完全相关（知道一个就确定另一个）。但 $\mathrm{E}[X]=\mathrm{E}[Y]=1/2$，$\mathrm{E}[X+Y]=1$，等式照旧成立。若换成 variance（方差），立刻失效：$\mathrm{Var}(X+Y)=0$，而 $\mathrm{Var}(X)+\mathrm{Var}(Y)=1/2$，两者差了整整一倍。差在哪？方差展开后出现 $2\mathrm{Cov}(X,Y)$ 这一项，而协方差恰恰要求「不相关」才为零——独立性的用武之地在这里，不在期望。
>
> 雇用问题里那句常见的「诸 $X_i$ 并不独立」其实说反了：第 $i$ 个候选人是否被雇用，只取决于他在前 $i$ 人中的相对名次，而这段相对名次与更早的记录模式互不影响，所以这些指示器恰好互相独立（取 $n=5$ 穷举 $120$ 种排列可验：$\Pr\{X_2=1,X_3=1,X_4=1\}=5/120=1/24=1/2\cdot1/3\cdot1/4$）。这不是说独立性不重要，而是说这条结论比它需要的条件强得多：即便它们互相纠缠，期望照样可加。用一个不独立的例子做对照更清楚：两次掷币，$Z$ 为「至少一次正面」、$W$ 为「至少一次反面」，则 $\Pr\{Z=1,W=1\}=1/2$，而两边际概率之积是 $9/16$，确实相关；但 $\mathrm{E}[Z+W]=1.5=0.75+0.75$，可加性毫发无损。
>
> 跨课程连接：100B 实分析里 $\int(f+g)=\int f+\int g$ 从不需要 $f$ 与 $g$ 有任何独立性——积分是线性算子，期望不过是概率测度下的积分，所以线性性是继承来的，不是概率论额外赠送的。6.042J 里把期望当加权平均处理，也隐含同一个事实。区别在于：积分对函数线性，概率论里额外的「独立性」管的是乘积与卷积，不管加法。
>
> 把刚才那个反例算到协方差上，数字会更刺眼：$\mathrm{Cov}(X,Y)=\mathrm{E}[XY]-\mathrm{E}[X]\mathrm{E}[Y]=0-1/4=-1/4$，于是 $\mathrm{Var}(X+Y)=1/4+1/4+2\cdot(-1/4)=0$，与「两个 $1/2$ 相加得 $1$」正好差掉那个交叉项。这条算式把「独立性用在哪」落成了一个具体的 $-1/4$。
>
> 同一件事在 condition（条件）语言里也成立：全期望公式 $\mathrm{E}[X]=\mathrm{E}[\mathrm{E}[X|Y]]$ 同样不需要独立，它只用条件期望的定义；只有当你把 $\mathrm{E}[X|Y]$ 简化成 $\mathrm{E}[X]$ 时，才需要「$X$ 的分布不随 $Y$ 变」这个更强的条件。换句话说，独立性让你能「忘掉条件」，但从不阻止你「保留条件再平均」。
>
> 顺带说明一个常被连坐的说法：$X_i$ 同分布时线性性同样不需要「独立同分布」里的前半截，只需要每个 $X_i$ 的边际期望存在且有限；存在性这一步不能省，因为期望只在绝对可和时才定义。
>
> 使用判据只有一句：先问目标量是不是期望。是，就放心拆成逐项之和；要算方差、要算联合分布、要用「概率相乘」，才需要另验独立性。

---

> <span style="color:#7f8c8d;">CLRS §5.2, p.120</span>

### Section 5.2 · Indicator random variables（指示器随机变量）（续）

```math
\begin{aligned}
\mathrm{E}[X] &= \mathrm{E}\left[\sum_{i=1}^{n} X_i\right]\\
&= \sum_{i=1}^{n} \mathrm{E}[X_i]\\
&= \sum_{i=1}^{n} 1/2\\
&= n/2.
\end{aligned}
```

因此，与式 (C.37) 所用的方法相比，指示器随机变量极大地简化了计算。在本书中我们将始终使用指示器随机变量。

#### Analysis of the hiring problem using indicator random variables（用指示器随机变量分析雇用问题）

回到雇用问题，现在我们希望计算雇用一名新办公室助理的 expected number（期望次数）。为了进行 probabilistic analysis（概率分析），我们假设候选人以随机顺序到来，如上一节所讨论的那样。（我们将在 Section 5.3 中看到如何去掉这一假设。）令 $X$ 是一个 random variable（随机变量），其值等于我们雇用新办公室助理的次数。我们可以套用式 (C.20) 给出的期望值定义，得到

```math
\mathrm{E}[X] = \sum_{x=1}^{n} x\,\Pr\{X = x\},
```

但这个计算会相当繁琐。我们改用指示器随机变量来大大简化计算。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这条注定名全书最重要的概率分析模板：indicator random variable（指示器随机变量）求和法。它的四步是固定的：把「某类事件发生了多少次」写成一个整数随机变量 $X$；把 $X$ 拆成 $n$ 个取值 $0$ 或 $1$ 的指示器之和；用 $\mathrm{E}[X_i]=\Pr\{A_i\}$（$A_i$ 表示第 $i$ 个对象身上发生目标事件） 一步算出每一项；再用期望线性性把 $n$ 项相加。
>
> 为什么不能直接求分布？以雇用问题为例，$\Pr\{X=k\}$ 等于「排列中恰有 $k$ 个记录」的概率，其计数是第一类 Stirling 数，写出来是一长串乘积之和，$n=100$ 时根本没法手算。指示器把这个「整体的分布」问题换成 $n$ 个「局部的边际概率」问题，每个边际概率往往一句话就能说清（第 $i$ 个比前面都强，概率 $1/i$）。这是典型的「换一个坐标系」，不是技巧堆叠。
>
> 数字感要建立起来。$n=100$ 时 $H_{100}\approx5.187$，意思是平均只雇五个人左右，而不是一百个；$n=10^6$ 时 $H_n\approx\ln10^6+0.577\approx14.39$，候选人涨到一百万，平均雇用次数才十四次多。同一条模板用在别处也一样干脆：$100$ 次均匀掷币的正面次数期望是 $50$（每枚指示器贡献 $1/2$）；$n$ 顶帽子的错排问题里，拿回自己帽子的人数期望恒为 $1$；随机排列的逆序对期望是 $n(n-1)/4$，$n=100$ 时是 $2475$。三个数都不是凑出来的，都是「$n$ 个 $0/1$ 相加」的直接结果。
>
> 四个步骤里最容易被跳过的是第二步：拆得对不对，取决于每个 $X_i$ 是否只回答一个「是/否」问题。若某个 $X_i$ 还要再分情况，说明拆得不够细，期望那一项就算不出来。第三步依赖引理 5.1（指示器的期望等于事件概率），这一步之所以成立，是因为取值只有 $0$ 和 $1$，加权求和只剩一项。第四步不需要独立性，理由见上一注。
>
> 这个模板在本书的复读率极高：第 7 章把快速排序的总比较次数拆成「每一对元素是否被比较」的指示器之和，得 $2n\ln n$ 量级；第 11 章把哈希表某条链的长度拆成「每个键是否落进这个槽」之和；第 12 章分析二叉搜索树的高度时同样先拆再求和。它们的共同点不是数学难度，而是「把一个算不动的全局量换成 $n$ 个一眼看穿的局部量」这一分解动作。
>
> 跨课程连接：CSAPP 第 6 章统计 cache 命中次数时，命中的总次数天然就是「每次访存是否命中」这些指示器之和，硬件性能计数器做的就是这件事；区别是硬件直接测量，不建模，而这里要在没有测量的情况下预测期望。6.042J 的期望线性性是这四步里第三步到第四步之间的桥，缺了它，拆开也加不起来。
>
> 再补一个读数上的警告。生日问题里 $n=23$ 人共有 $253$ 对，每对同生日的概率是 $1/365$，故「同生日对数」的期望只有 $0.693$；但「至少有一对同生日」的概率却是 $0.507$。期望远小于 $1$ 并不意味着事件罕见，因为计数变量可以取 $2$、$3$ 等更大的值。用指示器和法求期望时，永远要分清「问的是平均值还是概率」。
>
> 收束：遇到「随机过程中某类事件一共发生了多少次」，先别写分布，先问「能不能拆成 $n$ 个是/否」；能拆，问题就已经解完了。

为了使用指示器随机变量，我们不再通过定义一个与"雇用新办公室助理的次数"相关联的变量来计算 $\mathrm{E}[X]$，而是定义 $n$ 个变量，分别对应每名特定的候选人是否被雇用。具体地，令 $X_i$ 是与"第 $i$ 名候选人被雇用"这一事件相关联的指示器随机变量，于是

```math
X_i = I\{\text{candidate } i \text{ is hired}\} = \begin{cases} 1 & \text{if candidate } i \text{ is hired} \\ 0 & \text{if candidate } i \text{ is not hired} \end{cases}
```

并且

```math
X = X_1 + X_2 + \cdots + X_n. \tag{5.2}
```

---

> <span style="color:#7f8c8d;">CLRS §5.2, p.121</span>

### Section 5.2 · Indicator random variables（指示器随机变量）（续）

根据 Lemma 5.1（引理 5.1），我们有

```math
\mathrm{E}[X_i] = \Pr\{\text{candidate } i \text{ is hired}\},
```

因此必须计算 HIRE-ASSISTANT 的第 5–6 行被执行的概率。

在第 6 行中，候选人 $i$ 被雇用，当且仅当候选人 $i$ 比候选人 $1$ 到 $i - 1$ 中的每一位都更优秀。由于我们假设候选人以随机顺序到来，前 $i$ 名候选人是以随机顺序出现的，因此这前 $i$ 名候选人中的任何一名都等可能地是目前为止最优秀的。候选人 $i$ 比候选人 $1$ 到 $i - 1$ 都更胜任的概率是 $1/i$，从而被雇用的概率也是 $1/i$。由 Lemma 5.1 我们得出

```math
\mathrm{E}[X_i] = 1/i. \tag{5.3}
```

现在可以计算 $\mathrm{E}[X]$ 了：

```math
\begin{aligned}
\mathrm{E}[X] &= \mathrm{E}\left[\sum_{i=1}^{n} X_i\right] & & \text{(by equation (5.2))}\\
&= \sum_{i=1}^{n} \mathrm{E}[X_i] & & \text{(by linearity of expectation)}\\
&= \sum_{i=1}^{n} 1/i & & \text{(by equation (5.3))}
\end{aligned}
\tag{5.4}
```

```math
\phantom{\mathrm{E}[X]} = \ln n + O(1) \qquad \text{(by equation (A.7))}\,.
\tag{5.5}
```

尽管我们面试了 $n$ 个人，但平均而言实际只雇用了大约 $\ln n$ 个人。我们把这一结果总结为下面的 lemma（引理）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (5.5) 里那个 $\ln n$ 不是新符号，它就是 harmonic series（调和级数）$H_n=\sum_{i=1}^n1/i=\ln n+O(1)$；本书附录式 (A.7) 复述了这一结果。真正值得咀嚼的是每个 $1/i$ 从哪来：第 $i$ 名候选人被雇用，当且仅当他比前面 $i-1$ 名都强，而「前 $i$ 名里最强的恰是最后一位」的概率是 $1/i$，与他们的具体能力值无关。
>
> 机制据此完全确定：期望雇用次数是 $\sum_i\Pr\{A_i\}=\sum_i1/i$，其中 $A_i$ 表示第 $i$ 人被雇用，天然长成调和级数的形状。这不是「碰巧用了对数」，而是「随机排列的步长在缩小」的直接后果：越往后，要打破已有记录越难，第 $i$ 步的成功率是 $1/i$，于是总期望是这些小概率的累加。
>
> 数字复核。$H_{100}\approx5.18738$，而 $\ln100+\gamma=4.60517+0.57722=5.18239$，两者差 $0.00499$，恰约 $1/(2n)=0.005$——这不是巧合，$H_n$ 的展开下一项就是 $1/(2n)$。把成本合起来：取 $c_i=10$、$c_h=10^4$、$n=100$，总代价约 $10\cdot100+10^4\cdot5.187=1000+51874=52874$，而最坏情况是 $10^4\cdot100=10^6$，平均比最坏低 $18.9$ 倍。注意降幅来自两个方向：面试成本是线性的、压不下去；雇用成本从平方级掉到对数级，这才是主力。
>
> 历史与人物：调和级数发散这件事，十四世纪的 Oresme 已经证明；Euler（欧拉）在 1737 年提交给圣彼得堡科学院的《Variae observationes circa series infinitas》里给出乘积恒等式，并由它推出素数倒数和 $\sum_p1/p$ 发散（论文题名、年份与结论一手核实；卷页细节未能一手核实）。这里要顺手纠正一个常见说法：欧拉得到的结论比「素数有无穷多个」更强——后者是 Euclid 的结论，前者说明素数在自然数里「足够稠密」，稠密到倒数和都发散。调和级数在欧拉手里是工具，不是结论。
>
> 跨课程连接：100B 实分析里比较 $\sum1/n^p$ 的敛散，$p>1$ 收敛、$p=1$ 是临界，此时部分和长成 $\ln n$；用积分判别法 $\int_1^n x^{-p}dx$ 能立刻看出这条临界线，与这里「$H_n\sim\ln n$」是同一个事实的两种写法。区别是实分析关心收敛与发散的两分，这里关心常数因子与阶的精确形状（比如那个 $1/(2n)$ 的修正）。6.042J 里对数的运算律则解释了为什么「除以 $i$」累加会变成「取对数」：乘法变加法，加法累积变对数。
>
> 原文那句「最坏情况被指数级压低」需要修正：降的是阶，不是指数。最坏是 $c_hn$，平均是 $c_h\ln n$，两者之比是 $n/\ln n$——$n=100$ 时约 $21.7$，$n=10^6$ 时约 $72382$。也就是说，规模越大，平均值相对最坏的优势越大，但这个优势是多项式级的（比值本身无界增长），说成「指数级」就把量级关系说错了。真正被指数压低的是「最坏情形出现的概率」：要求 $n$ 个候选人恰好按能力递增到达，概率是 $1/n!$，$n=10$ 时已是 $1/3628800$。这两句话常被混着说，其实是两件事。
>
> 再从积分角度看一眼 $\ln n$ 的来源。把 $\sum_{i=1}^n1/i$ 与 $\int_1^n dx/x$ 对照，前者是阶梯函数下的面积、后者是光滑曲线下的面积，两者只相差一个有界量，即 Euler–Mascheroni 常数 $\gamma\approx0.5772$ 加上 $1/(2n)$ 量级的尾巴）。这就是为什么 $H_n=\ln n+\gamma+O(1/n)$：求和与积分只差「台阶与斜坡」的那点缝隙。100B 里的积分判别法正是把这一步写成定理。
>
> 收束：$\ln n$ 的来源是「第 $i$ 步成功概率 $1/i$」这一条概率事实；记住概率，公式会自己长出来。

#### Lemma 5.2（引理 5.2） <span style="color:#2471a3;">**[lemma]**</span>

假设候选人以随机顺序出现，则算法 HIRE-ASSISTANT 的 average-case total hiring cost（平均情况总雇用成本）为 $O(c_h \ln n)$。

> <span style="color:#2471a3;">**[proof]**</span> **Proof（证明）**  该界直接由雇用成本的定义以及式 (5.5) 得出：式 (5.5) 表明雇用的期望次数约为 $\ln n$。

平均情况雇用成本相对 $O(c_h n)$ 的 worst-case hiring cost（最坏情况雇用成本）是一个显著的改进。

---

> <span style="color:#7f8c8d;">CLRS §5.2–5.3, p.122</span>

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**5.2-1** In HIRE-ASSISTANT, assuming that the candidates are presented in a random order, what is the probability that you hire exactly one time? What is the probability that you hire exactly $n$ times?

**5.2-2** In HIRE-ASSISTANT, assuming that the candidates are presented in a random order, what is the probability that you hire exactly twice?

**5.2-3** Use indicator random variables to compute the expected value of the sum of $n$ dice.

**5.2-4** Use indicator random variables to solve the following problem, which is known as the hat-check problem. Each of $n$ customers gives a hat to a hat-check person at a restaurant. The hat-check person gives the hats back to the customers in a random order. What is the expected number of customers who get back their own hat?

**5.2-5** Let A[1 .. n] be an array of $n$ distinct numbers. If $i < j$ and A[i] > A[j], then the pair $(i, j)$ is called an inversion of A. (See Problem 2-4 for more on inversions.) Suppose that the elements of A form a uniform random permutation of $\langle 1, 2, \ldots, n \rangle$. Use indicator random variables to compute the expected number of inversions.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 习题 5.2-4 的帽子核对是组合数学里的 derangement（错排）问题，习题 5.2-5 的逆序对在 chunk01 的 Problem 2-4 出现过。两题表面无关，实际共用同一台机器：把待求的整数拆成逐对、逐人的指示器之和。
>
> 先看帽子。把帽子随机发还，固定一位顾客，他拿回自己帽子的概率是 $1/n$（他的帽子等可能地落在 $n$ 个位置之一），于是拿回自己帽子的人数期望是 $n\cdot(1/n)=1$。这个 $1$ 与 $n$ 完全无关：$n=4$ 时错排数 $9$、总排列 $24$，概率 $0.375$；$n=5$ 时 $44/120\approx0.3667$；随 $n$ 增大逼近 $1/e\approx0.3679$。期望恒为 $1$ 而概率趋于 $0.368$，两件事并不矛盾——期望小，是因为大多数时候一个人都不撞对，少数时候会有两个、三个甚至更多，把平均值拉回 $1$。
>
> 再看逆序对。均匀随机排列中，任意一对位置 $(i,j)$（$i<j$）构成逆序，当且仅当前面的值大于后面的值；只看这两个位置上的两个数，谁大谁小完全对称，故概率恰为 $1/2$。于是期望逆序数是 $\binom n2/2=n(n-1)/4$：$n=100$ 时 $2475$，而最坏情况（完全逆序）是 $4950$，平均正好是最坏的一半。
>
> 这里的方法论要点是「对称性替代计算」。要直接算 $\Pr\{X=k\}$ 需要 Eulerian number（欧拉数），公式繁琐；但问「某一对是否逆序」只需要两个数的相对大小，概率一眼可见。指示器求和法之所以强，就在于它总能把问题降到「单个局部事件」，而局部事件往往有对称性可用。
>
> 为什么逆序数值得关心？因为插入排序做元素移动的次数恰好等于逆序数：每插入一个元素，它要往左挪的步数就是它与前面元素构成的逆序数。于是「期望逆序数」直接翻译成「插入排序的平均移动次数」，$\Theta(n^2)$ 的最坏情况与平均情况只差常数因子 $2$。这与第 7 章快速排序的情形形成对照：那里平均是 $\Theta(n\lg n)$、最坏是 $\Theta(n^2)$，差距是量级；这里差距只是常数，所以插入排序没有「平均特别好」这回事。
>
> 跨课程连接：6.042J 的计数给出的是「有多少种排列」「有多少个错排」，是精确的整数；这里要的是随机变量的平均，是实数。区别在于计数回答「可能性有多大」的分子，期望回答「长期平均会怎样」。chunk01 的 Problem 2-4 把逆序数当作插入排序运行时间的精确度量，那是算法分析里的「成本模型」；6.042J 的排列计数则是组合工具。两者合起来才够用：先有精确的成本表达式，再用期望把它变成可比较的量级。
>
> 补一条错排自身的递推，便于手算核对：$D_n=(n-1)(D_{n-1}+D_{n-2})$，初值 $D_1=0$、$D_2=1$，于是 $D_3=2$、$D_4=9$、$D_5=44$、$D_6=265$。另一个更直接的恒等式是 $D_n=nD_{n-1}+(-1)^n$，它把「$1/e$ 的误差」写成交替级数的尾项，故 $|D_n/n!-1/e|<1/(n+1)!$，收敛极快：$n=5$ 时差约 $0.0012$。这两个式子都说明了同一件事：错排的概率结构在 $n$ 增大时迅速稳定，而它的期望从头到尾就是 $1$。
>
> 收束：两题都说明同一件事——把「总数」拆成「每个对象是否贡献一」，再用对称性或 $1/n$ 这类一眼可见的概率求和；拆得对，答案往往是个位数。

### Section 5.3 · Randomized algorithms（随机化算法） <span style="color:#2471a3;">**[section]**</span>

在上一节中，我们展示了"知道输入上的一个 distribution（分布）"如何帮助我们分析算法的 average-case behavior（平均情况行为）。但很多时候我们并不具备这样的知识，这就排除了 average-case analysis（平均情况分析）的可能。如 Section 5.1 所述，此时我们或许可以使用 randomized algorithm（随机化算法）。

对于雇用问题这样"假设输入的所有 permutation（排列）等可能地出现"会有帮助的问题，概率分析可以指导随机化算法的开发。我们不去假设输入的分布，而是 impose（施加）一个分布。具体地，在运行算法之前，我们随机地 permute（重排/随机排列）候选人，以强制保证每种排列都等可能地出现。虽然我们修改了算法，但我们仍然预期只雇用大约 $\ln n$ 次新办公室助理。但现在我们预期的是……（接下页）
