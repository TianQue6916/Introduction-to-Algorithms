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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这是「代换法=归纳证明的计算化」模板：你在 6.042J 里写过无数遍的数学归纳法，这里被直接搬来分析算法。第一步"猜 $T(n)\le cn\lg n$"，本质是在猜归纳假设本身——你并不是猜一个数，而是猜一条对所有 $m<n$ 成立的不等式；第二步的代换，就是把"假设对 $\lfloor n/2\rfloor$ 成立"当作归纳步的输入，验证它向下传递一层后仍为真。所以"猜"并不可耻：归纳证明的难点从来不在验证，而在提出正确的命题，而好命题的来源是递归树（§4.4）、经验以及相似问题——归并排序 $T(n)=2T(n/2)+n$ 的解你已经见过，猜 $O(n\lg n)$ 不过是模式匹配。与 6.042J 的区别在于：那里证的是孤立命题，这里证的是一族随 $n$ 缩放的命题，因此多出了"选常数 $c$"这一步——$c$ 不是猜出来的，而是被最后一步不等式"逼"出来的。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里藏着全书反复出现的「代数放缩」模板：想证明 $T(n)\le cn^2$ 这类界时，把低阶修正项（如 $(n-1)^2$）直接展开成 $n^2-2n+1$，让主项对齐，剩下的低阶项 $-2n+1$ 再用"更大的常数或更松的余量"吸收掉。习题 4.3-1 就是它的标准实战：对 $T(n)=T(n-1)+n$ 猜 $O(n^2)$，代换得 $c(n-1)^2+n=cn^2-(2c-1)n+c\le cn^2$，只要 $c\ge 1$ 即可收尾。这个模板在两处会再次登场：§4.6 证明主定理时逐层放缩取整误差（$n_j\le n/b^j+b/(b-1)$），第 7 章分析快速排序时把 $\sum k$ 吸收进 $n^2$。它与你在 100B 实分析里"$\epsilon$ 留足余量"的论证习惯同源——先构造出带余项的中间式，再论证余项可被控制；区别只是这里的"余量"是低阶项而不是 $\epsilon$ 邻域。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么"猜 $O(n)$"不能直接当成 $T(n)\le cn$ 来用？回到归纳证明的第一性原理：归纳步唯一的输入就是归纳假设本身，所以假设必须精确到你能在等式里逐项代入。若只写下 $T(\lfloor n/2\rfloor)=O(n)$，这个 $O$ 记号背后藏着一个未知的常数 $c'$，两次递归各带各的 $c'$，而"$O$ 之和为 $O$"只保证存在某个新常数，并不保证它就是你手上那个 $c$——于是 $cn+n$ 里的 $n$ 永远消不掉，松弛的界会在下一层被继续放大。这正是"先证后信"原则的完美训练素材：错误的证明往往每一步单独看都"差不多对"，但归纳法是个放大器，任何一点松动都会随递归深度层层放大。对比上一页正确的处理方式：把假设精确写成 $cn-d$、连减号都代进等式里参与运算，才是归纳法能接受的形式——强弱假设一字之差，成败立判。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里是「变量代换化归」模板：$T(n)=2T(\sqrt n)+\lg n$ 不是主方法认识的标准形状，但令 $m=\lg n$、再令 $S(m)=T(2^m)$，它立刻化归为你已经会解的 $S(m)=2S(m/2)+m$，解出 $S(m)=O(m\lg m)$ 后换回原变量，即得 $O(\lg n\cdot\lg\lg n)$。这与你在微积分里做积分的换元法（substitution，如 $\int 2x\,e^{x^2}\,dx$ 令 $u=x^2$）是同一个思想：换元不改变问题本身，只改变它的表示——选坐标系的标准是"让问题落入已知的标准形式"。两个操作要点：其一，选对换元方向，本题的线索是 $\sqrt n=2^{(\lg n)/2}$，凡参数里出现指数/开方结构时优先取对数；其二，答案必须换回原变量，否则只是解出了另一个问题。习题 4.3-9 的 $3T(\sqrt n)+\log_2 n$ 是现成的练手题，套路完全相同。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这是「递归树求和」模板的第二次实战（chunk01 分析归并排序时我们已经命名过它）：① 逐层展开，写出深度 $i$ 处的结点数与单个结点的代价；② 相乘得每层总代价 $3^i\cdot c(n/4^i)^2=(3/16)^i cn^2$；③ 识别求和结构，用闭式或已知级数封顶。本题的新意在第③步：每层代价按公比 $3/16$ 几何收缩，于是可以放胆把有限和换成无穷等比级数，代价只是上界变松一个常数因子 $16/13$。这个"用无穷和封顶有限和"是有代价核算的：多加的那些正项只让上界更松，不改变渐近阶——这正是渐近分析能容忍的不严谨。记住随之而来的判据：叶子代价 $\Theta(n^{\log_4 3})$ 被根的 $cn^2$ 压制时，根支配全局；下一节主定理的情形 1 说的就是这件事的通用版。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 从第一性原理看，主定理三情形本质是 $f(n)$（每层的分解/合并代价）与 $n^{\log_b a}$（叶子总数）的"三局博弈"：在递归树（§4.6.1 的图 4.7）里，叶子总代价固定为 $\Theta(n^{\log_b a})$，而 $f(n)$ 的层代价随深度变化——$f$ 偏小则层代价层层衰减、总和由叶子主导（情形 1）；$f$ 与叶子同级则每层贡献相同、共 $\lg n$ 层（情形 2）；$f$ 偏大则层代价逐层放大、根主导一切（情形 3）。为什么必须设"多项式差"这道门槛、从而留下 gap？因为判定的机器是等比级数：只有 $f(n)$ 比 $n^{\log_b a}$ 小整整一个 $n^\epsilon$ 因子，层代价才会形成严格几何的衰减/增长序列，求和才有干净的上界；而 $n\lg n$ 与 $n$ 这种只差一个 $\log$ 因子的量，公比退化成随深度缓变的量，级数封顶失效。所以 gap 不是定理的缺陷，而是"几何级数判别法"分辨力的极限。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把上面三道例题的解题动作抽出来，就是主方法的「三步判断次序」模板：第一步，机械地算出 $n^{\log_b a}$——只动 $a$ 与 $b$，完全不看 $f$；第二步，比较 $f(n)$ 与 $n^{\log_b a}$ 以定情形，比较的关键不是"谁大"，而是"是否差一个多项式因子 $n^\epsilon$"；第三步，若落入情形 3，还要再查正则条件 $af(n/b)\le cf(n)$——对幂函数与 $n^k\lg^j n$ 型函数它几乎总成立（想想 $a\cdot(n/b)^k=(a/b^k)n^k$，当 $b^k>a$ 时这个比值自然严格收缩到 $c<1$）。次序不能乱：先比较再算 $n^{\log_b a}$ 容易被直觉带偏，比如 $T(n)=T(2n/3)+1$ 里 $f$ 是常数，必须先算出 $\log_{3/2}1=0$ 才能看出两者同级。这三步恰好对应 §4.6 引理 4.3 的三个 case 的证明入口，到时候可以回来对照。

主方法并不适用于递归式

```math
T(n) = 2T(n/2) + n \lg n\,,
```

尽管它看起来具有正确的形式：$a = 2$、$b = 2$、$f(n) = n \lg n$，且 $n^{\log_b a} = n$。你可能会误以为情形 3 应当适用，因为

---

> <span style="color:#7f8c8d;">CLRS §4.5, p.96</span>

（接上页）$f(n) = n \lg n$ 渐近地大于 $n^{\log_b a} = n$。问题在于它并不是多项式意义上更大。比值 $f(n)/n^{\log_b a} = (n \lg n)/n = \lg n$ 对任何正常数 $\epsilon$ 都渐近地小于 $n^{\epsilon}$。因此，该递归式落入情形 2 与情形 3 之间的 gap。（解参见 Exercise 4.6-2。）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么 $f(n)=n\lg n$ 恰好卡进缝里？把比值摆出来：$f(n)/n^{\log_b a}=\lg n$，它趋于无穷（所以不是情形 2 的"同级"），却比任何 $n^\epsilon$ 都慢（所以也不是情形 3 的"多项式更大"）——一个只差 $\log$ 因子的函数恰好落在几何级数判别法的分辨极限之外。这不是吹毛求疵：$n\lg n$ 正是"每层代价几乎不衰减、却带一个缓慢单调因子"的临界形状，递归树里 $\lg(n/2^j)\cdot(1/2)^j$ 的求和中，几何衰减与 $\lg$ 的缓慢增长部分抵消，正是这种临界性让情形 2 的解多出 $\lg n$、情形 3 的门槛多出 $n^\epsilon$。主定理失效后的接手顺序：先用递归树看出形状（本例将得 $\Theta(n\lg^2 n)$），再用代换法补成严格证明——习题 4.6-2 的推广（$f=\Theta(n^{\log_b a}\lg^k n)\Rightarrow T=\Theta(n^{\log_b a}\lg^{k+1}n)$）正是把这类"卡缝"情形系统化的结果。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 整个主定理的支点其实只有一行：$a^{\log_b n}=n^{\log_b a}$。它来自指数律与对数律的一次交换：两边取 $\log_b$，左边得 $\log_b n\cdot\log_b a$，右边得 $\log_b a\cdot\log_b n$，乘法交换律保证两边相等——这也是你高中背过的换底公式 $\log_a n=\log_b n/\log_b a$ 的直接推论。为什么说它是支点？因为"叶子数"和"叶子代价之和"是从两个方向数同一件事：沿树每下一层规模除以 $b$、结点数乘 $a$，走 $\log_b n$ 层到底，故叶子数为 $a^{\log_b n}$；而把同一批叶子按"规模 1 的子问题"记账，恰好有 $n^{\log_b a}$ 个。两种计数必须给出同一个数，否则式 (4.21) 的总代价公式就裂成对不上的两半。"把指数上的量搬下来当线性系数用"这一把戏，你在 6.042J 数论（费马小定理降指数）和 CSAPP 浮点表示（指数域线性化）里都见过雏形，根子都是这条对数-指数互换律。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把三个 case 的证明并排放，会看到同一个可命名为「$\epsilon$-剥离+等比级数封顶」的模板：$\epsilon$ 的职责是制造一个严格的几何公比，让求和能被闭式封顶。情形 1 里 $\epsilon$ 使公比成为 $b^\epsilon>1$ 的递增等比级数，提出公因式后总和被 $O(n^{\log_b a})$ 吸收；情形 3 里正则条件迭代 $j$ 次得 $a^jf(n/b^j)\le c^jf(n)$，公比 $c<1$，于是 $\sum c^j=1/(1-c)$ 封顶。两个方向共用一句话：渐近界的成立依赖一个严格几何的衰减/增长因子，$\epsilon$ 就是制造这个因子的旋钮。这正是你在 100B 实分析里级数部分（Rudin 第 3 章）的几何级数比较判别法的离散版本：判断 $\sum a_j$ 收敛时找一个几何级数做上界；区别是那里证收敛性，这里证"和多出一个常数因子无伤大雅"。注意情形 2 没有 $\epsilon$ 可用——每层代价相同，级数退化为常数列，只能老实乘层数 $\lg n$；三种情形的差异最终都归结为级数的形状。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段推导是"渐近鲁棒性"思想的最佳展示：取整 $\lceil n/b\rceil$ 每层至多比 $n/b$ 大 $1$，单独看微不足道，但递归会把误差累积 $j$ 层——关键一步是 $n_j<n/b^j+\sum_i 1/b^i<n/b^j+b/(b-1)$：用 $\lceil x\rceil\le x+1$ 逐层展开后，累积误差恰好形成一个公比为 $1/b$ 的无穷等比级数，其和 $b/(b-1)$ 是一个与深度 $j$ 无关的常数！也就是说，取整误差不但没有被递归指数放大，反而被几何衰减封死在常数里——这正是"$\lfloor n/b\rfloor$、$\lceil n/b\rceil$、$n/b$ 三种写法渐近等价"这句话背后的全部数学。之后只需再证 $f(n_j)$ 与 $f(n/b^j)$ 相差一个常数因子（下一页那串不等式做的事），引理 4.3 的三个 case 便可原封不动地搬过来。你在 CSAPP 第 2 章分析浮点舍入误差时处理过同类问题：单次舍入有界不难，难的是论证误差随迭代不累积——这里几何级数给出了"不累积"的保证。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 蒙日阵列（Monge array）得名于法国数学家 Gaspard Monge（1746–1818，画法几何与运输理论的奠基人、巴黎综合理工学院创始人之一）；其定义式 $A[i,j]+A[k,l]\le A[i,l]+A[k,j]$ 就是组合优化里的"四边形不等式"（quadrangle inequality），而部分 (c) 要证的 $f(1)\le f(2)\le\cdots\le f(m)$ 称为总单调性（total monotonicity）——每行最左最小值的位置随行号单调不减。这正是你在 6.042J 学过的偏序（partial order）思想在矩阵上的具象化：行与行之间按"最左最小值位置"排出一条全序链。它的威力在后续：任何满足总单调性的矩阵（蒙日阵是特例），都能用 SMAWK 算法（以 Shor、Moran、Aggarwal、Wilber、Klawe 五位发明者姓氏首字母命名）在近线性时间求出每行最小值，远快于逐格扫描的 $O(mn)$；许多代价函数满足四边形不等式的动态规划（如序列分段问题）因此从 $O(n^2)$ 加速到近 $O(n)$。Problem 4-6 的 (d)(e) 两问正是 SMAWK 的雏形，值得亲手做一遍。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Akra–Bazzi 方法（Mohamad Akra 与 Louay Bazzi 提出，Leighton 改进表述）是主定理的真正推广：它允许 $k$ 个规模各不相同的子问题 $b_ix$（如 $T(n)=T(n/3)+T(2n/3)+n$），而主定理要求所有子问题同规模。用法分两步：先解方程 $\sum_i a_ib_i^p=1$ 定出唯一的 $p$——主定理里它退化为 $a\cdot b^{-p}=1$，即 $p=\log_b a$，所以主定理确是它的特例；再代入 $T(x)=\Theta\bigl(x^p(1+\int_1^x f(u)/u^{p+1}\,du)\bigr)$，用积分处理 $f$ 的贡献。什么时候需要它？凡是"非均衡分治"：快速排序按任意比例切分、本章习题 4.4-9 的 $T(\alpha n)+T((1-\alpha)n)+cn$、以及第 9 章中位数选择算法的 $T(n/5)+T(7n/10)+n$ 都属此类。直觉上，$p$ 是"让叶子权重收支平衡"的临界指数：规模按 $b_i$ 缩小、份数按 $a_i$ 放大，$p$ 恰是两者打平的点，与主定理"叶子与根博弈"的图像一脉相承——只是博弈的双方从对称变成了加权。

---

> <span style="color:#7f8c8d;">CLRS Chapter 5, §5.1, p.114</span>

## Chapter 5（第 5 章）· Probabilistic Analysis and Randomized Algorithms（概率分析与随机化算法） <span style="color:#2471a3;">**[section]**</span>

本章介绍 probabilistic analysis（概率分析）与 randomized algorithms（随机化算法）。如果你对 probability theory（概率论）的基础知识还不熟悉，应当先阅读 Appendix C（附录 C），其中复习了这些内容。在本书中，我们还会多次重新讨论概率分析与随机化算法。

### Section 5.1 · The hiring problem（雇用问题） <span style="color:#2471a3;">**[section]**</span>

假设你需要雇用一名新的 office assistant（办公室助理）。你之前的几次雇用尝试都不成功，于是决定借助一家 employment agency（职业介绍所）。职业介绍所每天给你送来一名 candidate（候选人），你面试这个人，然后决定是否雇用他。你必须向职业介绍所支付一小笔费用才能面试一名 applicant（申请者）；然而，真正雇用一名申请者的代价要高得多，因为你必须解雇当前的办公室助理，并向职业介绍所支付一笔数额可观的 hiring fee（雇用费）。你承诺在任何时刻都要为这个职位保留最合适的人选。因此你决定：每面试完一名申请者，如果这名申请者比当前的办公室助理更胜任，就解雇当前的助理并雇用这名新申请者。你愿意为这一策略付出相应的代价，但你希望事先估计出这个代价会有多大。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么值得把"招个助理"郑重其事地抽象成算法问题？第一性原理的答案是：剥离所有细节后，它剩下一个纯粹的在线（online）结构——输入逐个到达，每个元素到达时必须立刻做出不可撤销的决定，而你永远看不到还没到达的输入。快速排序的随机主元、经典的秘书问题（secretary problem）都与它同根。更关键的方法论转折在"估计代价"这四个字里：最坏情况分析给出的 $O(c_h n)$ 太悲观（只在候选人恰好按资历递增到达时发生），而"运气好"是个模糊概念——概率分析的贡献正是把"运气"变成可计算的量：先给输入分布下定义（均匀随机排列），再算期望。你所需的全部工具在 6.042J 已经备好：期望的线性性（linearity of expectation）允许我们把总雇用次数拆成逐个候选人的贡献之和，哪怕这些事件之间并不独立。§5.2 的指示器随机变量就是把这一步做干净的机器。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "期望线性性不需要独立性"是概率分析中最容易被误解的一点，值得用反例把它钉死。取 $X$ 为掷一次均匀硬币的正面指示器、$Y$ 为反面指示器，则 $X$ 与 $Y$ 强相关（$Y=1-X$，知道一个就完全确定另一个），但 $\mathrm{E}[X+Y]=1=\mathrm{E}[X]+\mathrm{E}[Y]$ 依然成立。为什么？回到第一性原理：期望是对概率分布的加权求和，线性性的证明只用到"对联合分布逐行求和时可交换加法次序"——这是实数加法的性质，与两个变量是否互相依赖毫无关系。独立性出场是在别处：方差的可加性 $\mathrm{Var}(X+Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)$、以及多个事件概率相乘，都需要它。所以使用本节模板前必问一句：我的目标量是期望吗？若是，放心拆；若要方差或联合分布，独立性必须另行验证。雇用问题里诸 $X_i$ 恰恰不独立（雇了第 $i$ 人会改变后面被雇用的条件），但结论依然严格成立。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 正式命名这个全书最重要的概率分析模板——「指示器变量求和法」：① 当你要计算"某类复杂事件发生了多少次"时，放弃直接对总次数 $X$ 写分布 $\Pr\{X=x\}$——如上一页开头所示，那条路繁琐得吓人；② 把 $X$ 拆成 $n$ 个 0/1 指示器之和 $X=\sum_i X_i$，每个 $X_i$ 只回答一个简单问题（"第 $i$ 个对象身上是否发生了某事"）；③ 由引理 5.1，$\mathrm{E}[X_i]=\Pr\{\cdot\}$ 一步算出；④ 用期望线性性把 $n$ 个期望相加，全程不需要独立性。这个模板在本书的复读率极高：本章的雇用问题与习题 5.2-4/5.2-5、第 7 章快速排序的总比较次数、第 11 章哈希表链长的期望、第 12 章二叉搜索树的相关期望量，全都靠它一次成型。它的价值不在每一步多深，而在"把一个算不动的量换成 $n$ 个一眼看穿的量"这一分解动作本身——下次遇到任何"随机过程中某事件总数"的分析，先想它。

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
\mathrm{E}[X] &= \mathrm{E}\left[\sum_{i=1}^{n} X_i\right] & & \text{(by equation (5.2))} \tag{5.4}\\
&= \sum_{i=1}^{n} \mathrm{E}[X_i] & & \text{(by linearity of expectation)}\\
&= \sum_{i=1}^{n} 1/i & & \text{(by equation (5.3))}\\
&= \ln n + O(1) & & \text{(by equation (A.7))}\,. \tag{5.5}
\end{aligned}
```

尽管我们面试了 $n$ 个人，但平均而言实际只雇用了大约 $\ln n$ 个人。我们把这一结果总结为下面的 lemma（引理）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (5.5) 里冒出来的 $\ln n$ 不是新东西，它就是你在 6.042J 里证明过的调和级数 $H_n=\sum_{i=1}^n 1/i=\ln n+O(1)$（本书附录式 (A.7) 复述了这一结果；历史上欧拉在 1737 年还曾用调和级数的发散性给"素数无穷多"另证了一条路）。这里每项 $1/i$ 的含义值得咀嚼：第 $i$ 名候选人被雇用，当且仅当他比前面 $i-1$ 名都强，概率恰为 $1/i$——于是"雇用次数"就是把 $n$ 个概率 $1/i$ 的事件计数求和，天然长成调和级数的形状。它与第 7 章快速排序的平均分析同族：那里同样用指示器变量把总比较次数拆成元素对的贡献，求和也归结为 $\sum 1/k$ 型的调和量。把成本合起来看，总代价 $O(c_i n+c_h\ln n)$——最坏情况的 $c_h n$ 在平均意义下被指数级压低，这是"换一个分析视角，换一个更真确的界"的范例。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 习题 5.2-4 的帽子核对问题是组合数学中的经典错排（derangement）问题——6.042J 里你已经见过"没有任何人拿回自己帽子"的排列计数；这里换成了期望版：固定看任意一位顾客，随机排列下他拿回自己帽子的概率是 $1/n$，由指示器求和立得期望 $n\cdot(1/n)=1$，一个漂亮到不可能是巧合的数。习题 5.2-5 的逆序对则在 chunk01 的 Problem 2-4 出现过：逆序数正是插入排序运行时间的精确度量，两题是同一个量的两副面孔。把两题连起来还能得到一个更深的视角：均匀随机排列中每对 $(i,j)$ 构成逆序的概率恰为 $1/2$，故期望逆序数为 $\binom n2/2=n(n-1)/4$——又一次"指示器求和"秒杀组合计数的演示；这也立刻解释了插入排序平均为何要挪 $\Theta(n^2)$ 次、与最坏情况只差常数因子。

### Section 5.3 · Randomized algorithms（随机化算法） <span style="color:#2471a3;">**[section]**</span>

在上一节中，我们展示了"知道输入上的一个 distribution（分布）"如何帮助我们分析算法的 average-case behavior（平均情况行为）。但很多时候我们并不具备这样的知识，这就排除了 average-case analysis（平均情况分析）的可能。如 Section 5.1 所述，此时我们或许可以使用 randomized algorithm（随机化算法）。

对于雇用问题这样"假设输入的所有 permutation（排列）等可能地出现"会有帮助的问题，概率分析可以指导随机化算法的开发。我们不去假设输入的分布，而是 impose（施加）一个分布。具体地，在运行算法之前，我们随机地 permute（重排/随机排列）候选人，以强制保证每种排列都等可能地出现。虽然我们修改了算法，但我们仍然预期只雇用大约 $\ln n$ 次新办公室助理。但现在我们预期的是……（接下页）
