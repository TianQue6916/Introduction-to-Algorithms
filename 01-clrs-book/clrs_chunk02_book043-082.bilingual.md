# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk02 · 书页 43–82 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS Chapter 3, §3.1, p.43</span>

## Chapter 3（第 3 章）· Growth of Functions（函数的增长）

第 2 章中定义的算法 running time（运行时间）的 order of growth（增长阶数），给出了算法 efficiency（效率）的一种简单刻画，也让我们能够比较不同算法之间的相对 performance（性能）。一旦 input size（输入规模）$n$ 变得足够大，具有 $\Theta(n \lg n)$ 最坏情况运行时间的 merge sort（归并排序）就会胜过最坏情况运行时间为 $\Theta(n^2)$ 的 insertion sort（插入排序）。虽然我们有时能够确定一个算法的 exact running time（精确运行时间）——正如第 2 章对插入排序所做的那样——但为这点额外的 precision（精度）去付出计算代价通常并不值得。对于足够大的输入，精确运行时间中的 multiplicative constants（乘积常数）与 lower-order terms（低阶项）都会被输入规模自身的影响所支配。当我们考察那些大到使只有运行时间的增长阶数才相关的输入规模时，我们研究的就是算法的 asymptotic efficiency（渐近效率）。也就是说，我们关心的是：在输入规模无限增大的 limit（极限）意义下，算法的运行时间如何随输入规模的增大而增长。通常，一个在渐近意义上更高效的算法，对除极小输入之外的所有输入都会是最佳选择。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这句"为精确运行时间付出计算代价并不值得"，值得用第一性原理想透：既然我们只保留 constant factor（常数因子）意义下的信息，运行时间函数之间就不再是普通的相等，而是"在常数因子内互等价"。这正是你在 MIT 6.042J 学过的 equivalence relation（等价关系）那套骨架：$f(n)=\Theta(g(n))$ 定义的关系满足自反性（$f=\Theta(f)$）、对称性（$f=\Theta(g)$ 蕴含 $g=\Theta(f)$）与传递性，三者在 §3.1 末尾的性质列表中都会逐条用 $c_1$、$c_2$ 的定义验证。于是 Θ 把所有函数切成一个个等价类（equivalence class），$n^2+3n$ 与 $5n^2$ 落在同一个类里。在这个视角下，O 是偏序式的"$\le$"（只有自反与传递，没有对称），Θ 才是真正的"$=$"，o 则扮演"$<$"。三个记号各自的合法运算全部由"等价 / 序 / 严格序"这套骨架一次理清，后面遇到的任何记号性质，都先想想它在实数比较中对应什么。

本章给出若干用于简化算法渐近分析的标准方法。下一节首先定义几种“asymptotic notation（渐近记号）”——我们已经见过的 Θ-notation（Θ 记号）就是其中一例。随后我们给出贯穿全书使用的若干 notational conventions（记号约定），最后回顾算法分析中常见函数的行为。

### Section 3.1 · Asymptotic notation（渐近记号） <span style="color:#2471a3;">**[section]**</span>

我们用来描述算法 asymptotic running time（渐近运行时间）的那些记号，是以 domain（定义域）为自然数集 $\mathbb{N} = \{0, 1, 2, \ldots\}$ 的 functions（函数）来定义的。这类记号很适合描述 worst-case running-time function（最坏情况运行时间函数）$T(n)$，它通常只在整数 input size 上有定义。不过，我们有时也会发现，以多种方式对渐近记号加以 abuse（滥用）反而更方便。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.44</span>

（承上页）例如，我们可能把记号 extend（扩展）到 real numbers（实数）的 domain（定义域）上，或者相反地把它 restrict（限制）到自然数的某个 subset（子集）上。不过我们应当确保真正理解该记号的 precise meaning（精确含义），这样在 abuse（滥用）它时才不至于 misuse（误用）。本节定义基本的渐近记号，并介绍一些常见的滥用方式。

### Asymptotic notation, functions, and running times（渐近记号、函数与运行时间） <span style="color:#2471a3;">**[section]**</span>

我们主要用渐近记号来描述算法的 running times（运行时间），比如说插入排序的最坏情况运行时间是 $\Theta(n^2)$。然而，渐近记号实际上作用于 functions（函数）。回想一下，我们把插入排序的最坏情况运行时间刻画为 $an^2 + bn + c$，其中 $a$、$b$、$c$ 为 constants（常数）。当我们写下“插入排序的运行时间是 $\Theta(n^2)$”时，其实是抽象掉了这个函数的某些细节。由于渐近记号作用于函数，我们所写的 $\Theta(n^2)$ 对应的其实是函数 $an^2 + bn + c$，只是在这个情形下它恰好刻画了插入排序的最坏情况运行时间。

在本书中，我们施加渐近记号的函数通常会刻画算法的运行时间。但渐近记号也可以作用于刻画算法其他方面的函数（例如算法所用的空间量），甚至可以作用于与算法毫无关系的函数。

即便我们用渐近记号来刻画算法的运行时间，也需要弄清指的是哪一种运行时间。有时我们关心的是 worst-case running time（最坏情况运行时间）；但更常见的情况是，我们希望刻画无论输入如何的运行时间。换句话说，我们常常想做出一个覆盖所有 inputs（输入）、而不只是最坏情况的 blanket statement（概括性论断）。我们将会看到一些非常适合刻画“无论输入为何”之运行时间的渐近记号。

### Θ-notation（Θ 记号） <span style="color:#2471a3;">**[definition]**</span>

在第 2 章中，我们求得插入排序的最坏情况运行时间是 $T(n) = \Theta(n^2)$。现在来定义这个记号的含义。对一个给定的函数 $g(n)$，我们用 $\Theta(g(n))$ 表示如下函数集合：

```math
\Theta(g(n)) = \{\, f(n) : \text{there exist positive constants } c_1, c_2, \text{ and } n_0 \text{ such that } 0 \le c_1 g(n) \le f(n) \le c_2 g(n) \text{ for all } n \ge n_0 \,\}.
```

> <span style="color:#7f8c8d;">注 1（原书脚注）：在集合记号之内，冒号（:）的意思是 “such that（使得）”。</span>

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.45</span>

> <span style="color:#7f8c8d;">本页含插图：Figure 3.1（图 3.1）。译者说明：图面为三个并排的子图 (a)、(b)、(c)，各自画出函数 $f(n)$ 与 $g(n)$ 的曲线及其常数倍 $c g(n)$（或 $c_1 g(n)$、$c_2 g(n)$），并用竖直虚线标出 $n_0$ 的位置：(a) 中 $f(n)$ 被夹在 $c_1 g(n)$ 与 $c_2 g(n)$ 之间；(b) 中 $f(n)$ 始终位于 $c g(n)$ 之下或恰好落在其上；(c) 中 $f(n)$ 始终位于 $c g(n)$ 之上或恰好落在其上。</span>

**Figure 3.1（图 3.1）**：Θ、O 与 Ω 记号的 graphic examples（图示例子）。每一部分中所示 $n_0$ 的值都是最小可能值；任何更大的值也同样可行。(a) Θ-notation 把一个函数限制在常数因子范围内。若存在正的 constants（常数）$n_0$、$c_1$、$c_2$，使得在 $n_0$ 处及其右侧，$f(n)$ 的值始终介于 $c_1 g(n)$ 与 $c_2 g(n)$ 之间（含端点），则写作 $f(n) = \Theta(g(n))$。(b) O-notation（O 记号）在常数因子范围内给出一个函数的 upper bound（上界）。若存在正的常数 $n_0$ 与 $c$，使得在 $n_0$ 处及其右侧，$f(n)$ 的值始终位于 $c g(n)$ 之下或恰好落在其上，则写作 $f(n) = O(g(n))$。(c) Ω-notation（Ω 记号）在常数因子范围内给出一个函数的 lower bound（下界）。若存在正的常数 $n_0$ 与 $c$，使得在 $n_0$ 处及其右侧，$f(n)$ 的值始终位于 $c g(n)$ 之上或恰好落在其上，则写作 $f(n) = \Omega(g(n))$。

若存在正的常数 $c_1$ 与 $c_2$，使得当 $n$ 足够大时，$f(n)$ 能被“sandwiched（夹在）” $c_1 g(n)$ 与 $c_2 g(n)$ 之间，那么函数 $f(n)$ 就属于集合 $\Theta(g(n))$。由于 $\Theta(g(n))$ 是一个 set（集合），本可以写作 “$f(n) \in \Theta(g(n))$” 来表示 $f(n)$ 是 $\Theta(g(n))$ 的一个 member（成员）；但本书通常改写为 “$f(n) = \Theta(g(n))$” 来表达同样的意思。你可能会对我们如此滥用 equality（等号）感到困惑，不过本节稍后会说明，这样做自有其好处。

图 3.1(a) 给出了 $f(n) = \Theta(g(n))$ 时函数 $f(n)$ 与 $g(n)$ 的直观图像。对于位于 $n_0$ 处及其右侧的所有 $n$ 值，$f(n)$ 的值都不低于 $c_1 g(n)$，且不高于 $c_2 g(n)$。换句话说，对所有 $n \ge n_0$，函数 $f(n)$ 都在常数因子范围内等于 $g(n)$。此时我们称 $g(n)$ 是 $f(n)$ 的 asymptotically tight bound（渐近紧确界）。

$\Theta(g(n))$ 的定义要求每个成员 $f(n) \in \Theta(g(n))$ 都是 asymptotically nonnegative（渐近非负）的，即只要 $n$ 充分大，$f(n)$ 就非负。（asymptotically positive（渐近为正）的函数，是指对所有充分大的 $n$ 都取正值的函数。）因此，$g(n)$ 自身也必须是渐近非负的，否则集合 $\Theta(g(n))$ 就是 empty（空）的。所以我们约定：凡是在 Θ-notation 中使用的函数都是渐近非负的。这一假设同样适用于本章定义的其他渐近记号。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.46</span>

在第 2 章中，我们引入过 Θ-notation 的一种 informal（非正式）理解，它相当于丢掉 lower-order terms（低阶项），并忽略最高阶项的 leading coefficient（首项系数）。现在我们用正式定义来简要印证这一直觉：证明 $\frac{1}{2}n^2 - 3n = \Theta(n^2)$。为此，必须确定正常数 $c_1$、$c_2$ 与 $n_0$，使得

```math
c_1 n^2 \le \frac{1}{2} n^2 - 3n \le c_2 n^2
```

对所有 $n \ge n_0$ 成立。两边除以 $n^2$ 得

```math
c_1 \le \frac{1}{2} - \frac{3}{n} \le c_2.
```

任取常数 $c_2 \ge 1/2$，就能让右侧不等式对任意 $n \ge 1$ 成立；同样，任取常数 $c_1 \le 1/14$，就能让左侧不等式对任意 $n \ge 7$ 成立。于是，取 $c_1 = 1/14$、$c_2 = 1/2$、$n_0 = 7$，即可验证 $\frac{1}{2}n^2 - 3n = \Theta(n^2)$。当然，这些常数还存在其他取法，但关键在于确实存在某种取法。还要注意，这些常数依赖于函数 $\frac{1}{2}n^2 - 3n$ 本身；属于 $\Theta(n^2)$ 的另一个函数，通常需要不同的常数。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把这个证明提炼成可复用的模板，命名为「常数对 $c_1$、$c_2$ 夹逼」：第一步，找足够小的 $c_1$ 吞掉低阶负项；第二步，找足够大的 $c_2$ 压住首项；第三步，取 $n_0$ 兜住小输入端。本例中 $c_1=1/14$ 从哪来？把 $\frac12-\frac3n$ 在 $n\ge 7$ 处估出下界 $\frac12-\frac37=\frac1{14}$——可见三步有先后依赖：$c_1$ 的可行域依赖 $n_0$，所以正确姿势是先选定 $n_0$，再解出 $c_1$ 与 $c_2$，而不是碰运气猜数字。还要注意对称性：$c_2\ge 1/2$ 几乎白送（首项系数就是天花板），真正的功夫全花在 $c_1$ 上，因为负的低阶项只会往下拉。以后一切 Θ 验证题——包括下方 $an^2+bn+c=\Theta(n^2)$、Problem 3-1 的 $d$ 次多项式——都套这个三步模板，把"构造常数"当成"解不等式"来机械完成。

我们同样可以用正式定义验证 $6n^3 \ne \Theta(n^2)$。为引出矛盾，假设存在 $c_2$ 与 $n_0$，使得对所有 $n \ge n_0$ 都有 $6n^3 \le c_2 n^2$；但两边除以 $n^2$ 得 $n \le c_2/6$，由于 $c_2$ 是常数，这不可能对任意大的 $n$ 成立。

直观上，在确定 asymptotically tight bound 时，渐近为正函数的低阶项可以忽略不计，因为它们在 $n$ 很大时微不足道。当 $n$ 很大时，最高阶项的哪怕一小部分都足以支配全部低阶项。于是，把 $c_1$ 取成略小于最高阶项系数的值、把 $c_2$ 取成略大于它的值，就能使 Θ-notation 定义中的不等式得到满足。最高阶项的系数同样可以忽略，因为它只是让 $c_1$ 与 $c_2$ 改变一个等于该系数的 constant factor（常数因子）。

举个例子，考虑任意的 quadratic function（二次函数）$f(n) = an^2 + bn + c$，其中 $a$、$b$、$c$ 为常数且 $a > 0$。丢掉低阶项并忽略常数，即得 $f(n) = \Theta(n^2)$。形式化地，为证明同一结论，取常数 $c_1 = a/4$、$c_2 = 7a/4$、$n_0 = 2 \cdot \max(|b|/a, \sqrt{|c|/a})$。你可以验证：对所有 $n \ge n_0$，都有 $0 \le c_1 n^2 \le an^2 + bn + c \le c_2 n^2$。一般地，对任意 polynomial（多项式）$p(n) = \sum_{i=0}^{d} a_i n^i$，其中诸 $a_i$ 为常数且 $a_d > 0$，我们有 $p(n) = \Theta(n^d)$（见 Problem 3-1）。

由于任意常数都是 degree（次数）为 0 的多项式，我们可以把任何 constant function（常值函数）表示为 $\Theta(n^0)$，也就是 $\Theta(1)$。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.47</span>

（承上页）不过 $\Theta(1)$ 这种写法是对记号的一个小小的 abuse（滥用），因为该表达式并未指出趋于 infinity（无穷）的是哪个变量。² 我们以后会经常使用记号 $\Theta(1)$，用它来表示某个 constant（常数），或者关于某个变量的 constant function。

> <span style="color:#7f8c8d;">注 2（原书脚注）：真正的问题在于，我们日常的函数记法并不区分 functions（函数）与函数 values（值）。在 λ-calculus（λ 演算）中，函数的 parameters（参数）是明确给出的：函数 $n^2$ 可以写成 $\lambda n.\, n^2$，甚至写成 $\lambda r.\, r^2$。然而，采用更严格的记法会使 algebraic manipulations（代数演算）复杂化，所以我们选择容忍这一滥用。</span>

### O-notation（O 记号） <span style="color:#2471a3;">**[definition]**</span>

Θ-notation 从上下两个方向渐近地 bound（约束）一个函数。当我们只有 asymptotic upper bound（渐近上界）时，就使用 O-notation。对一个给定的函数 $g(n)$，我们用 $O(g(n))$（读作 “big-oh of g of n”，有时也简读作 “oh of g of n”）表示如下函数集合：

```math
O(g(n)) = \{\, f(n) : \text{there exist positive constants } c \text{ and } n_0 \text{ such that } 0 \le f(n) \le c g(n) \text{ for all } n \ge n_0 \,\}.
```

我们用 O-notation 给出一个函数在常数因子范围内的 upper bound（上界）。图 3.1(b) 展示了 O-notation 背后的直觉：对所有位于 $n_0$ 处及其右侧的 $n$ 值，函数 $f(n)$ 的值都位于 $c g(n)$ 之下或恰好落在其上。

我们写 $f(n) = O(g(n))$，表示函数 $f(n)$ 是集合 $O(g(n))$ 的一个 member（成员）。注意 $f(n) = \Theta(g(n))$ 蕴含 $f(n) = O(g(n))$，因为 Θ-notation 是比 O-notation 更强的概念。用 set-theoretic（集合论的）语言写出来就是 $\Theta(g(n)) \subseteq O(g(n))$。因此，我们关于任意二次函数 $an^2 + bn + c$（其中 $a > 0$）属于 $\Theta(n^2)$ 的证明，同时也表明任何这样的二次函数都属于 $O(n^2)$。更出人意料的也许是：当 $a > 0$ 时，任意 linear function（线性函数）$an + b$ 都属于 $O(n^2)$——取 $c = a + |b|$、$n_0 = \max(1, -b/a)$ 便可轻松验证。

如果你以前见过 O-notation，也许会觉得奇怪：我们怎么会写出诸如 $n = O(n^2)$ 这样的式子。在文献中，我们有时会发现 O-notation 被非正式地用来描述渐近紧确界——也就是我们上面用 Θ-notation 定义的那种界。但在本书中，当我们写 $f(n) = O(g(n))$ 时，仅仅是断言 $g(n)$ 的某个常数倍是 $f(n)$ 的一个渐近上界，并不涉及这个上界有多 tight（紧）。把 asymptotic upper bound 与 asymptotically tight bound 区分开来，是算法文献中的标准做法。

利用 O-notation，我们常常只需考察算法的整体结构，就能描述算法的 running time（运行时间）。例如，第 2 章 insertion sort algorithm（插入排序算法）的 doubly nested loop（双重嵌套循环）结构立刻给出其最坏情况运行时间的一个 $O(n^2)$ 上界：内层循环每次迭代的代价以 $O(1)$（constant（常数））为上界，下标 $i$ 与 $j$ 都至多是 $n$，而内层循环对 $i$ 与 $j$ 的 $n^2$ 个取值组合中的每一个至多执行一次。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.48</span>

由于 O-notation 描述的是 upper bound（上界），当我们用它去 bound（约束）一个算法的 worst-case running time（最坏情况运行时间）时，我们得到的是该算法在每一个输入上运行时间的界——也就是前面讨论过的那种 blanket statement。因此，插入排序最坏情况运行时间的 $O(n^2)$ 界同样适用于它在每个输入上的运行时间。然而，插入排序最坏情况运行时间的 $\Theta(n^2)$ 界，并不意味着插入排序在每个输入上的运行时间都有 $\Theta(n^2)$ 界。例如，第 2 章我们看到，当输入已经有序时，插入排序以 $\Theta(n)$ 时间运行。

严格地说，说“插入排序的运行时间是 $O(n^2)$”是一种 abuse（滥用），因为对给定的 $n$，实际运行时间会随规模为 $n$ 的具体输入而变化。当我们说“运行时间是 $O(n^2)$”时，意思是：存在某个属于 $O(n^2)$ 的函数 $f(n)$，使得对任意 $n$ 值，无论选取规模为 $n$ 的哪个具体输入，该输入上的运行时间都以 $f(n)$ 的值为上界。等价地说，我们的意思是最坏情况运行时间是 $O(n^2)$。

### Ω-notation（Ω 记号） <span style="color:#2471a3;">**[definition]**</span>

正如 O-notation 给出函数的 asymptotic upper bound，Ω-notation 给出的是 asymptotic lower bound（渐近下界）。对一个给定的函数 $g(n)$，我们用 $\Omega(g(n))$（读作 “big-omega of g of n”，有时也简读作 “omega of g of n”）表示如下函数集合：

```math
\Omega(g(n)) = \{\, f(n) : \text{there exist positive constants } c \text{ and } n_0 \text{ such that } 0 \le c g(n) \le f(n) \text{ for all } n \ge n_0 \,\}.
```

图 3.1(c) 展示了 Ω-notation 背后的直觉：对所有位于 $n_0$ 处及其右侧的 $n$ 值，$f(n)$ 的值都位于 $c g(n)$ 之上或恰好落在其上。

从我们目前已见过的这些渐近记号的定义出发，容易证明下面这个重要的定理（见 Exercise 3.1-5）。

#### Theorem 3.1（定理 3.1） <span style="color:#2471a3;">**[theorem]**</span>

对任意两个函数 $f(n)$ 与 $g(n)$，有：$f(n) = \Theta(g(n))$ 当且仅当 $f(n) = O(g(n))$ 且 $f(n) = \Omega(g(n))$。

作为应用该定理的一个例子：我们对任意常数 $a$、$b$、$c$（其中 $a > 0$）证明 $an^2 + bn + c = \Theta(n^2)$ 的过程，立即蕴含 $an^2 + bn + c = \Omega(n^2)$ 以及 $an^2 + bn + c = O(n^2)$。在实际中，与其像本例这样用 Theorem 3.1 从渐近紧确界导出渐近上界与下界，我们通常反过来用它从渐近上界与下界证明渐近紧确界。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "O 与 Ω 拼起来就是 Θ"看似显然，但要用你惯用的反例检验法查一查定义的边界条件为何是必需的。考察线性函数 $an+b$：若允许 $a=0$，剩下常数 $b$，则对 $g(n)=n$ 不存在 $c>0$ 使 $b\ge cn$ 对所有大 $n$ 成立——$\Omega(n)$ 一侧直接崩塌，"$\Theta(n)$"的断言随之失效。同样，"渐近非负"也不是摆设：若 $f$ 取负值，定义中 $0\le f(n)\le cg(n)$ 的下半边不等式无从谈起，整个集合就成了空集。这正是"先证后信"的价值：定理的每个前提都是证明中某一步放缩的合法性来源，而不是技术性啰嗦。建议在 Exercise 3.1-5 里亲手补全两个方向的证明，观察 $c$ 与 $n_0$ 在 O 一侧和 Ω 一侧如何各自选取、又在 Θ 中如何扮演 $c_1$ 与 $c_2$ 的角色。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.49</span>

当我们说一个算法的 running time（不带任何修饰语）是 $\Omega(g(n))$ 时，意思是：对 $n$ 的每个值，无论选取规模为 $n$ 的哪个具体输入，只要 $n$ 充分大，该输入上的运行时间都至少是 $g(n)$ 的常数倍。等价地说，这是在给出算法 best-case running time（最佳情况运行时间）的一个 lower bound（下界）。例如，插入排序的最佳情况运行时间是 $\Omega(n)$，这就蕴含了插入排序的运行时间是 $\Omega(n)$。

插入排序的运行时间因此同时属于 $\Omega(n)$ 与 $O(n^2)$，因为它可以落在 $n$ 的 linear function（线性函数）与 quadratic function（二次函数）之间的任何位置。而且这两个界在渐近意义上已经尽可能 tight（紧）：例如，插入排序的运行时间不是 $\Omega(n^2)$，因为存在某个输入使插入排序以 $\Theta(n)$ 时间运行（例如输入已经有序时）。然而，说插入排序的最坏情况运行时间是 $\Omega(n^2)$ 却并不矛盾，因为确实存在某个输入会使算法花费 $\Omega(n^2)$ 的时间。

### Asymptotic notation in equations and inequalities（等式与不等式中的渐近记号） <span style="color:#2471a3;">**[section]**</span>

我们已经见过如何在数学 formula（公式）内部使用渐近记号。例如，在引入 O-notation 时我们写过 “$n = O(n^2)$”；我们也可以写 $2n^2 + 3n + 1 = 2n^2 + \Theta(n)$。那么该如何解释这类公式呢？

当渐近记号单独地（即不在更大的公式之内）出现在 equation（等式）或 inequality（不等式）的 right-hand side（右端）时，比如 $n = O(n^2)$，我们已经把 equal sign（等号）定义为 set membership（集合隶属关系）：$n \in O(n^2)$。然而一般地，当渐近记号出现在一个公式之中时，我们把它解释为代表某个 anonymous function（匿名函数）——一个我们懒得为其命名的函数。例如，公式 $2n^2 + 3n + 1 = 2n^2 + \Theta(n)$ 的意思是 $2n^2 + 3n + 1 = 2n^2 + f(n)$，其中 $f(n)$ 是集合 $\Theta(n)$ 中的某个函数。在本例中，我们取 $f(n) = 3n + 1$，它确实属于 $\Theta(n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里的 anonymous function（匿名函数）不是新发明，而是你在 6.042J 里熟悉的量词缩写："$2n^2+3n+1=2n^2+\Theta(n)$"严格展开是"存在 $f\in\Theta(n)$，使得对所有 $n$ 有 $2n^2+3n+1=2n^2+f(n)$"——渐近记号就是携带存在量词的占位符，正如写 $\int f(x)\,dx$ 时无需给 $f$ 命名。这也解释了"$f(n)$ 在集合 $O(g(n))$ 里"与"存在常数 $c$ 和 $n_0$"为何等价：集合定义里的常数本身就是被 $\exists$ 约束的。特别注意方向性：记号出现在等号右边时是存在性陈述（存在某个匿名函数即可），出现在左边时（见下页规则）则要求对任意取法都成立——所以渐近语境里的"$=$"是带方向的伪对称，严格写法本应是 $\in$。凡遇到拿不准的渐近等式，第一步永远是展开成量词形式，歧义即刻消失。

以这种方式使用渐近记号，有助于消除等式中非本质的细节与杂乱。例如，第 2 章我们把 merge sort（归并排序）的最坏情况运行时间表示为 recurrence（递归式）

```math
T(n) = 2T(n/2) + \Theta(n).
```

如果我们只关心 $T(n)$ 的渐近行为，那么精确写出所有低阶项就毫无意义；它们都被理解为已包含在项 $\Theta(n)$ 所代表的匿名函数之中。

一个 expression（表达式）中匿名函数的个数，被理解为等于渐近记号出现的次数。例如，在表达式

```math
\sum_{i=1}^{n} O(i),
```

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.50</span>

### Section 3.1 · Asymptotic Notation（渐近记号）（续）

（接上页）此时整个 expression（表达式）中只有一个 anonymous function（匿名函数），即关于 $i$ 的那个函数。因此，该表达式并不等同于 $O(1) + O(2) + \cdots + O(n)$——后者其实并没有 clean interpretation（清晰的解释）。

在某些情况下，asymptotic notation 会出现在 equation（等式）的 left-hand side（左边），例如：

```math
2n^2 + \Theta(n) = \Theta(n^2)
```

我们按以下 rule（规则）来 interpret（解释）这样的等式：无论 equal sign（等号）左边的 anonymous functions 如何选取，总有一种办法选取等号右边的 anonymous functions，使该等式 valid（成立）。于是，上面这个例子意味着：对任意函数 $f(n) \in \Theta(n)$，都存在某个函数 $g(n) \in \Theta(n^2)$，使得对所有 $n$ 都有 $2n^2 + f(n) = g(n)$。换句话说，等式的 right-hand side（右边）提供了比左边更粗略的一层 detail（细节）。

我们还可以把若干个这样的关系 chain（串联）在一起，例如：

```math
2n^2 + 3n + 1 = 2n^2 + \Theta(n) = \Theta(n^2)
```

我们可以按照上述规则分别 interpret 其中的每一个等式。第一个等式说的是：存在某个函数 $f(n) \in \Theta(n)$，使得对所有 $n$ 都有 $2n^2 + 3n + 1 = 2n^2 + f(n)$。第二个等式说的是：对任意函数 $g(n) \in \Theta(n)$（例如刚才提到的 $f(n)$），都存在某个函数 $h(n) \in \Theta(n^2)$，使得对所有 $n$ 都有 $2n^2 + g(n) = h(n)$。注意，这一解释蕴含 $2n^2 + 3n + 1 = \Theta(n^2)$，这也正是这种等式串联在直观上带给我们的结论。

**o-notation（o 记号）**

O-notation（O 记号）所提供的 asymptotic upper bound 可能是、也可能不是 asymptotically tight（渐近紧确）的。bound $2n^2 = O(n^2)$ 是渐近紧确的，而 bound $2n = O(n^2)$ 则不是。我们用 o-notation（o 记号）来表示不是渐近紧确的 upper bound。我们把 $o(g(n))$（"little-oh of g of n"，$g(n)$ 的小 o）正式定义为一个 set（集合）：

```math
o(g(n)) = \{ f(n) : \text{对任意正常数 } c > 0,\ \text{存在常数 } n_0 > 0,\ \text{使得对所有 } n \ge n_0 \text{ 都有 } 0 \le f(n) < c\,g(n) \}
```

例如，$2n = o(n^2)$，但 $2n^2 \ne o(n^2)$。

O-notation 与 o-notation 的 definitions（定义）很相似。主要 difference（区别）在于：在 $f(n) = O(g(n))$ 中，bound $0 \le f(n) \le c\,g(n)$ 只需对某个 constant $c > 0$ 成立；而在 $f(n) = o(g(n))$ 中，bound $0 \le f(n) < c\,g(n)$ 需对所有 constant $c > 0$ 成立。直观上，在 o-notation 中，当 $n$ 趋于 infinity（无穷）时，function $f(n)$ 相对于 $g(n)$ 变得 insignificant（微不足道）；也就是说，

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.51</span>

### Section 3.1 · Asymptotic Notation（渐近记号）（续）

```math
\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0 \tag{3.1}
```

有些作者用这个 limit（极限）作为 o-notation 的 definition（定义）；而本书的定义还额外要求 anonymous functions 是 asymptotically nonnegative（渐近非负）的。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (3.1) 对你正在学的 100B 实分析来说是老朋友：$f=o(g)$ 就是 $f/g\to 0$，可以直接调用 Thomson 教材里的极限 $\varepsilon$-$N$ 语言——对任意 $\varepsilon>0$，存在 $n_0$，使得 $n\ge n_0$ 时 $|f(n)/g(n)|<\varepsilon$。把书里集合定义中的"任意常数 $c>0$"读成"任意 $\varepsilon>0$"，两条定义逐字相同；本书额外要求渐近非负，只是为了给不等式免去绝对值符号。于是五个记号各就各位：o 是"$<$"的渐近版（比值趋于 0，$f$ 相对 $g$ 微不足道），ω 是"$>$"的渐近版（比值趋于 $\infty$），而 O 与 Ω 允许比值停在任意正常数处，对应"$\le$"与"$\ge$"。为什么算法课需要 o 这种"严格序"？因为要断言"算法 A 渐近快于 B"，光有 $T_A=O(T_B)$ 不够——那只是"不慢于"；$T_A=o(T_B)$ 才排除了两者同阶的可能。

**ω-notation（ω 记号）**

ω-notation（ω 记号）之于 Ω-notation（Ω 记号），恰如 o-notation 之于 O-notation。我们用 ω-notation 来表示不是 asymptotically tight（渐近紧确）的 lower bound（下界）。一种定义方式是：$f(n) \in \omega(g(n))$ 当且仅当（if and only if）$g(n) \in o(f(n))$。不过，我们正式地把 $\omega(g(n))$（"little-omega of g of n"，$g(n)$ 的小 ω）定义为一个 set（集合）：

```math
\omega(g(n)) = \{ f(n) : \text{对任意正常数 } c > 0,\ \text{存在常数 } n_0 > 0,\ \text{使得对所有 } n \ge n_0 \text{ 都有 } 0 \le c\,g(n) < f(n) \}
```

例如，$n^2/2 = \omega(n)$，但 $n^2/2 \ne \omega(n^2)$。关系 $f(n) = \omega(g(n))$ 蕴含

```math
\lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty
```

（若该 limit 存在）。也就是说，当 $n \to \infty$ 时，$f(n)$ 相对于 $g(n)$ 变得 arbitrarily large（任意大）。

**Comparing functions（函数间的比较）**

许多 real numbers（实数）的 relational properties（关系性质）同样适用于 asymptotic comparisons（渐近比较）。在下面的讨论中，假设 $f(n)$ 与 $g(n)$ 都是 asymptotically positive（渐近为正）的。

Transitivity（传递性）：

- $f(n) = \Theta(g(n))$ 且 $g(n) = \Theta(h(n))$ 蕴含 $f(n) = \Theta(h(n))$；
- $f(n) = O(g(n))$ 且 $g(n) = O(h(n))$ 蕴含 $f(n) = O(h(n))$；
- $f(n) = \Omega(g(n))$ 且 $g(n) = \Omega(h(n))$ 蕴含 $f(n) = \Omega(h(n))$；
- $f(n) = o(g(n))$ 且 $g(n) = o(h(n))$ 蕴含 $f(n) = o(h(n))$；
- $f(n) = \omega(g(n))$ 且 $g(n) = \omega(h(n))$ 蕴含 $f(n) = \omega(h(n))$。

Reflexivity（自反性）：

- $f(n) = \Theta(f(n))$；
- $f(n) = O(f(n))$；
- $f(n) = \Omega(f(n))$。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.52</span>

### Section 3.1 · Asymptotic Notation（渐近记号）（续）

Symmetry（对称性）：$f(n) = \Theta(g(n))$ 当且仅当 $g(n) = \Theta(f(n))$。

Transpose symmetry（转置对称）：$f(n) = O(g(n))$ 当且仅当 $g(n) = \Omega(f(n))$；$f(n) = o(g(n))$ 当且仅当 $g(n) = \omega(f(n))$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> transpose symmetry（转置对称）$f=O(g)\Leftrightarrow g=\Omega(f)$ 看似平凡，其实有精确的代数身份：它是 6.042J 关系一章里逆关系（inverse relation）思想的对偶操作。把 $f=O(g)$ 的定义 $f(n)\le c\,g(n)$ 变形为 $\frac{f(n)}{g(n)}\le c$，取倒数得 $\frac{g(n)}{f(n)}\ge \frac1c$——量词"$\exists c>0$"在取倒数后自动保持（$c'=1/c$ 仍是正常数），于是"上界"的镜像恰好就是"下界"。这种对偶在数学里无处不在：线性代数中 $A$ 可逆当且仅当 $A^{-1}$ 可逆，实分析中 $\inf S=-\sup(-S)$。掌握对偶的收益是记忆量减半：关于 O 的每条性质都免费赠送 Ω 的对应版本，o 与 ω 同理。检验对偶是否用对，就看常数经过变形后是否仍为正常数——这道关卡正是全书要求函数渐近为正的原因。

由于这些 properties（性质）对 asymptotic notations 都成立，我们可以在两个 function $f$ 与 $g$ 之间的 asymptotic comparison（渐近比较）和两个 real numbers（实数）$a$ 与 $b$ 之间的比较之间做一个 analogy（类比）：

- $f(n) = O(g(n))$ 类似于（is like）$a \le b$；
- $f(n) = \Omega(g(n))$ 类似于 $a \ge b$；
- $f(n) = \Theta(g(n))$ 类似于 $a = b$；
- $f(n) = o(g(n))$ 类似于 $a < b$；
- $f(n) = \omega(g(n))$ 类似于 $a > b$。

如果 $f(n) = o(g(n))$，我们称 $f(n)$ 是 asymptotically smaller than（渐近小于）$g(n)$ 的；如果 $f(n) = \omega(g(n))$，我们称 $f(n)$ 是 asymptotically larger than（渐近大于）$g(n)$ 的。

然而，实数有一个 property 并不能 carry over（沿袭）到 asymptotic notation 上：

Trichotomy（三分律）：对任意两个实数 $a$ 与 $b$，以下三种情况必恰好成立其一：$a < b$、$a = b$ 或 $a > b$。

尽管任意两个实数都是 comparable（可比较）的，却并非所有 function 都是 asymptotically comparable（渐近可比较）的。也就是说，对两个函数 $f(n)$ 与 $g(n)$，有可能 $f(n) = O(g(n))$ 与 $f(n) = \Omega(g(n))$ 两者都不成立。例如，我们无法用 asymptotic notation 来比较 function $n$ 与 $n^{1+\sin n}$，因为 $n^{1+\sin n}$ 中的 exponent（指数）在 0 与 2 之间 oscillates（振荡），并取遍其间的所有值。

**Exercises（习题）** <span style="color:#2471a3;">**[exercise]**</span>

**3.1-1**
Let $f(n)$ and $g(n)$ be asymptotically nonnegative functions. Using the basic definition of $\Theta$-notation, prove that $\max(f(n), g(n)) = \Theta(f(n) + g(n))$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道习题背后藏着一组值得记住的 min/max 运算法则：对渐近为正的 $f$ 与 $g$，有 $\max(f,g)=\Theta(f+g)$（即本题），$\min(f,g)=O(f+g)$，但 $\min$ 与 $\max$ 之间一般没有 $\Theta$ 关系——想想 $f$ 与 $g$ 随 $n$ 交替占优的情形。证明思路是把逐点取 max 拆成两条不等式：$f\le f+g$ 与 $g\le f+g$ 给出 $\max\le f+g$，再由 $\max\ge f$、$\max\ge g$ 各取一半得 $\max\ge\frac12(f+g)$，这正是「常数对夹逼」模板的重演。另一条常用规则是 $f(n)+O(g(n))$：出现在和式中的 $O(g)$ 会把"较差的那一项"整个委托给匿名函数吸收。所有这些法则的公共红线是：渐近记号之间不能随便做减法与除法，因为匿名函数的符号不受控制，$O(g)-O(g)$ 甚至可能恒为零。凡遇混合运算，先展开成量词形式再动手，就不会踩坑。

**3.1-2**
Show that for any real constants $a$ and $b$, where $b > 0$,

```math
(n + a)^b = \Theta(n^b) \tag{3.2}
```

---

> <span style="color:#7f8c8d;">CLRS §3.1–3.2, p.53</span>

### Section 3.1 · Asymptotic Notation（渐近记号）（续）

**Exercises（习题）**（续） <span style="color:#2471a3;">**[exercise]**</span>

**3.1-3**
Explain why the statement, "The running time of algorithm A is at least $O(n^2)$," is meaningless.

**3.1-4**
Is $2^{n+1} = O(2^n)$? Is $2^{2n} = O(2^n)$?

**3.1-5**
Prove Theorem 3.1.

**3.1-6**
Prove that the running time of an algorithm is $\Theta(g(n))$ if and only if its worst-case running time is $O(g(n))$ and its best-case running time is $\Omega(g(n))$.

**3.1-7**
Prove that $o(g(n)) \cap \omega(g(n))$ is the empty set.

**3.1-8**
We can extend our notation to the case of two parameters $n$ and $m$ that can go to infinity independently at different rates. For a given function $g(n, m)$, we denote by $O(g(n, m))$ the set of functions

```math
O(g(n,m)) = \{ f(n,m) : \text{there exist positive constants } c, n_0, \text{ and } m_0 \text{ such that } 0 \le f(n,m) \le c\,g(n,m) \text{ for all } n \ge n_0 \text{ or } m \ge m_0 \}
```

Give corresponding definitions for $\Omega(g(n, m))$ and $\Theta(g(n, m))$.

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数） <span style="color:#2471a3;">**[section]**</span>

本节 review（回顾）一些 standard mathematical functions（标准数学函数）与 notations（记号），并探讨它们之间的 relationships（关系）。本节还展示了 asymptotic notations 的使用方法。

**Monotonicity（单调性）**

若 $m \le n$ 蕴含 $f(m) \le f(n)$，则称 function $f(n)$ 是 monotonically increasing（单调递增）的。类似地，若 $m \le n$ 蕴含 $f(m) \ge f(n)$，则称它是 monotonically decreasing（单调递减）的。若 $m < n$ 蕴含 $f(m) < f(n)$，则称 function $f(n)$ 是 strictly increasing（严格递增）的；若 $m < n$ 蕴含 $f(m) > f(n)$，则称它是 strictly decreasing（严格递减）的。

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.54</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

**Floors and ceilings（下取整与上取整）**

对任意 real number（实数）$x$，我们把小于或等于 $x$ 的最大 integer（整数）记作 $\lfloor x \rfloor$（读作 "the floor of x"，即 $x$ 的 floor（下取整）），把大于或等于 $x$ 的最小 integer 记作 $\lceil x \rceil$（读作 "the ceiling of x"，即 $x$ 的 ceiling（上取整））。对所有实数 $x$，

```math
x - 1 < \lfloor x \rfloor \le x \le \lceil x \rceil < x + 1 \tag{3.3}
```

对任意 integer $n$，

```math
\left\lceil n/2 \right\rceil + \left\lfloor n/2 \right\rfloor = n
```

并且对任意实数 $x \ge 0$ 与 integers $a, b > 0$，

```math
\left\lceil \frac{\lceil x/a \rceil}{b} \right\rceil = \left\lceil \frac{x}{ab} \right\rceil \tag{3.4}
```

```math
\left\lfloor \frac{\lfloor x/a \rfloor}{b} \right\rfloor = \left\lfloor \frac{x}{ab} \right\rfloor \tag{3.5}
```

```math
\left\lceil \frac{a}{b} \right\rceil \le \frac{a + b - 1}{b} \tag{3.6}
```

```math
\left\lfloor \frac{a}{b} \right\rfloor \ge \frac{a - b + 1}{b} \tag{3.7}
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 恒等式 (3.4)–(3.7) 都能用一个可复用的「区间夹逼展开法」两行证掉，以 (3.4) 为例。记 $k=\lceil x/a\rceil$，由取整定义有 $k-1<x/a\le k$，两边乘 $a$ 得 $a(k-1)<x\le ak$；再除以 $ab$ 得 $k-1<\frac{x}{ab}\le k$，而这恰好就是 $\lceil\frac{x}{ab}\rceil=k$ 的定义——证明完成。核心手法：把嵌套取整翻译成"$x$ 落在哪个端点为整数的区间"内，端点是整数时取整被"冻结"，便可逐层剥开；万能起手式就是上方 (3.3) 那条 $x-1<\lfloor x\rfloor\le x\le\lceil x\rceil<x+1$。注意 (3.4)、(3.5) 对 $x$ 般的实数成立而不只是整数，这也是区间法比"硬猜"可靠的地方。以后分析 $\lceil n/2\rceil$ 规模的递归（如递归式 (4.3)）或证明主方法时，这套"取整即区间"的翻译会反复出现。

floor function $f(x) = \lfloor x \rfloor$ 是 monotonically increasing（单调递增）的，ceiling function $f(x) = \lceil x \rceil$ 也是如此。

**Modular arithmetic（模运算）**

对任意 integer $a$ 与任意 positive integer（正整数）$n$，值 $a \bmod n$ 是 quotient（商）$a/n$ 的 remainder（余数，或 residue（剩余））：

```math
a \bmod n = a - n \left\lfloor a/n \right\rfloor \tag{3.8}
```

由此可得

```math
0 \le a \bmod n < n \tag{3.9}
```

在"一个 integer 除以另一个 integer 所得 remainder"这一 well-defined（良定义）概念的基础上，为表示余数相等提供专门的 notation（记号）会很方便。如果 $(a \bmod n) = (b \bmod n)$，我们就写作 $a \equiv b \pmod n$，并称 $a$ 与 $b$ 在 modulo（模）$n$ 意义下是 equivalent（等价）的。换句话说，$a \equiv b \pmod n$ 当且仅当 $a$ 与 $b$ 除以 $n$ 时有相同的 remainder。等价地，$a \equiv b \pmod n$ 当且仅当 $n$ 是 $b - a$ 的 divisor（因子）。如果 $a$ 与 $b$ 在模 $n$ 意义下不等价，我们就写作 $a \not\equiv b \pmod n$。

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.55</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

**Polynomials（多项式）**

给定一个 nonnegative integer（非负整数）$d$，一个 degree（次数）为 $d$ 的 polynomial in $n$（$n$ 的多项式）是一个形如

```math
p(n) = \sum_{i=0}^{d} a_i n^i
```

的 function $p(n)$，其中 constants（常数）$a_0, a_1, \ldots, a_d$ 是该 polynomial 的 coefficients（系数），且 $a_d \ne 0$。当且仅当 $a_d > 0$ 时，polynomial 是 asymptotically positive（渐近为正）的。对一个渐近为正的、次数为 $d$ 的 polynomial $p(n)$，我们有 $p(n) = \Theta(n^d)$。对任意实常数 $a \ge 0$，function $n^a$ 是 monotonically increasing（单调递增）的；对任意实常数 $a \le 0$，function $n^a$ 是 monotonically decreasing（单调递减）的。如果 $f(n) = O(n^k)$ 对某个 constant $k$ 成立，我们就称 function $f(n)$ 是 polynomially bounded（多项式有界）的。

**Exponentials（指数）**

对所有实数 $a > 0$、$m$ 与 $n$，我们有以下 identities（恒等式）：

```math
\begin{aligned}
a^0 &= 1, \\
a^1 &= a, \\
a^{-1} &= 1/a, \\
(a^m)^n &= a^{mn}, \\
(a^m)^n &= (a^n)^m, \\
a^m a^n &= a^{m+n}.
\end{aligned}
```

对所有 $n$ 以及 $a \ge 1$，function $a^n$ 关于 $n$ 是 monotonically increasing 的。在方便的时候，我们将假定 $0^0 = 1$。

我们可以借助下面这个事实来 relate（联系）polynomials 与 exponentials 的 rates of growth（增长率）。对所有实常数 $a$ 与 $b$，只要 $a > 1$，就有

```math
\lim_{n \to \infty} \frac{n^b}{a^n} = 0 \tag{3.10}
```

由此可以得出

```math
n^b = o(a^n)
```

因此，任何 base（底数）严格大于 1 的 exponential function（指数函数）都比任何 polynomial function（多项式函数）增长得更快。

用 $e$ 表示 natural logarithm function（自然对数函数）的底，即 $e = 2.71828\ldots$，那么对所有实数 $x$，

```math
e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots = \sum_{i=0}^{\infty} \frac{x^i}{i!} \tag{3.11}
```

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.56</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

（接上页式 (3.11)）其中 "!"（阶乘符号）表示本节稍后定义的 factorial function（阶乘函数）。对所有实数 $x$，我们有 inequality（不等式）

```math
e^x \ge 1 + x \tag{3.12}
```

其中 equality（等号）仅当 $x = 0$ 时成立。当 $|x| \le 1$ 时，我们有 approximation（近似）

```math
1 + x \le e^x \le 1 + x + x^2 \tag{3.13}
```

当 $x \to 0$ 时，用 $1 + x$ 来近似 $e^x$ 相当 good（好）：

```math
e^x = 1 + x + \Theta(x^2)
```

（在这个等式中，asymptotic notation 描述的是 $x \to 0$ 时的 limiting behavior（极限行为），而不是 $x \to \infty$ 时的。）对所有 $x$，我们有

```math
\lim_{n \to \infty} \left(1 + \frac{x}{n}\right)^n = e^x \tag{3.14}
```

**Logarithms（对数）**

我们将使用以下 notations（记号）：

```math
\begin{aligned}
\lg n &= \log_2 n & &\text{（binary logarithm，以 2 为底的对数）},\\
\ln n &= \log_e n & &\text{（natural logarithm，自然对数）},\\
\lg^k n &= (\lg n)^k & &\text{（exponentiation，取幂）},\\
\lg \lg n &= \lg(\lg n) & &\text{（composition，复合）}.
\end{aligned}
```

我们将采用的一个重要 notational convention（记号约定）是：logarithm functions（对数函数）只作用于 formula（公式）中的下一项，因此 $\lg n + k$ 意味着 $(\lg n) + k$，而不是 $\lg(n + k)$。如果我们让 $b > 1$ 保持 constant（不变），那么对 $n > 0$，function $\log_b n$ 是 strictly increasing（严格递增）的。

对所有实数 $a > 0$、$b > 0$、$c > 0$ 以及 $n$，

```math
\begin{aligned}
a &= b^{\log_b a}, \\
\log_c(ab) &= \log_c a + \log_c b, \\
\log_b a^n &= n \log_b a, \\
\log_b a &= \frac{\log_c a}{\log_c b},
\end{aligned} \tag{3.15}
```

```math
\begin{aligned}
\log_b(1/a) &= -\log_b a, \\
\log_b a &= \frac{1}{\log_a b}, \\
a^{\log_b c} &= c^{\log_b a},
\end{aligned} \tag{3.16}
```

（以上每个等式中，logarithm 的 bases（底）均不为 1。）

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.57</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

根据 equation (3.15)（式 (3.15)），把对数的底（base）从一个常数换成另一个常数，只会让 logarithm（对数）的值改变一个 constant factor（常数因子）；因此当我们在意的是增长阶数、不关心常数因子时——例如在 O-notation（O 记号）中——我们常常直接使用记号 $\lg n$。Computer scientist（计算机科学家）觉得 2 是最自然的对数之底，因为太多的 algorithms（算法）与 data structures（数据结构）都涉及把一个问题 split（拆分）成两部分。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "底数无关"的依据就是式 (3.15) 最后一条 $\log_b a=\frac{\log_c a}{\log_c b}$：换底只是除以常数 $\log_c b$，而 Θ 与 O 恰好对常数因子免疫。你在 Strang 线性代数里做基变换、在 CSAPP 里看浮点表示时，都见过同款操作——换基不改变对象本身，只改变表示的尺度。与此配套，请把前几页的两条极限（式 (3.10) 及其推论）内化成量级直觉：多项式碾压 polylog（$\lg^b n=o(n^a)$），指数碾压多项式（$n^b=o(a^n)$，$a>1$）。感受一下差距：取 $1.001^n$ 与 $n^{1000}$，在 $n=10^6$ 时前者约 $e^{1000}$、后者约 $e^{13816}$，多项式仍在领先；到 $n=10^8$，前者已达 $e^{100000}$、后者只有 $e^{18400}$，指数彻底反超。底数哪怕只比 1 大一丝，"自乘迭代"的指数型增长也终将压倒幂次固定的多项式——这就是算法设计把"指数级搜索空间"视为不可逾越红线的原因。

$\ln(1+x)$ 有一个简单的 series expansion（级数展开），当 $|x| < 1$ 时成立：

```math
\ln(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \frac{x^5}{5} - \cdots
```

对 $x > -1$，我们还有如下 inequalities（不等式）：

```math
\frac{x}{1+x} \le \ln(1+x) \le x \tag{3.17}
```

其中 equality（等号）仅在 $x = 0$ 时成立。

如果一个 function（函数）$f(n)$ 满足 $f(n) = O(\lg^k n)$（$k$ 为某个 constant（常数）），我们就称它是 polylogarithmically bounded（多项对数有界的）。通过在 equation (3.10) 中把 $n$ 替换为 $\lg n$、把 $a$ 替换为 $2^a$，我们可以把 polynomial（多项式）与 polylogarithm（多项对数函数）的增长联系起来，得到：

```math
\lim_{n \to \infty} \frac{\lg^b n}{2^{a\lg n}} = \lim_{n \to \infty} \frac{\lg^b n}{n^a} = 0
```

由这个 limit（极限）可以得出：对任意常数 $a > 0$，都有

```math
\lg^b n = o(n^a)
```

也就是说，任何正的 polynomial function（多项式函数）的增长都快于任何 polylogarithmic function（多项对数函数）。

### Factorials（阶乘） <span style="color:#2471a3;">**[section]**</span>

记号 $n!$（读作 “$n$ factorial（阶乘）”）对所有整数 $n \ge 0$ 定义为：

```math
n! = \begin{cases} 1 & \text{if } n = 0, \\ n \cdot (n-1)! & \text{if } n > 0. \end{cases}
```

于是 $n! = 1 \cdot 2 \cdot 3 \cdots n$。

对 factorial function（阶乘函数）的一个 weak upper bound（弱上界）是 $n! \le n^n$，因为阶乘连乘中的 $n$ 个因子每一个都至多是 $n$。Stirling's approximation（斯特林近似）

```math
n! = \sqrt{2\pi n}\left(\frac{n}{e}\right)^n \left(1 + \Theta\left(\frac{1}{n}\right)\right) \tag{3.18}
```

其中 $e$ 是 natural logarithm（自然对数）的底。它给出了一个更紧的 upper bound（上界），同时也给出了一个 lower bound（下界）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (3.18) 的来历可以接到你正在学的 100B：核心工具是 Wallis 型积分 $W_n=\int_0^{\pi}\sin^n x\,dx$，它同时给出 $n!$ 的上界与下界，再对相邻两个 $W_n$ 的递推关系做夹逼，就能挤出 $\sqrt{2\pi n}$ 这个"多余"的因子——这正是下一页式 (3.20)（Robbins 版本）中 $e^{\alpha_n}$ 与 $\frac{1}{12n}$ 精细修正项的来源。历史上，这批近似是 18 世纪 30 年代 de Moivre 与 Stirling 在研究二项分布的大数极限（概率论中最早的中心极限定理雏形）时得到的。对算法课更要紧的推论是式 (3.19) 的第三条：对 (3.18) 两边取对数立得 $\lg(n!)=\Theta(n\lg n)$，而它是第 8 章证明"基于比较的排序下界为 $\Omega(n\lg n)$"的引擎——$n$ 个元素有 $n!$ 种排列，每次比较至多二选一，决策树高度至少 $\lg(n!)$。记住这条推理链：排列计数 $\to$ 阶乘 $\to$ Stirling $\to$ 排序下界。

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.58</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

正如 Exercise 3.2-3 会让你证明的：

```math
n! = o(n^n), \qquad n! = \omega(2^n), \qquad \lg(n!) = \Theta(n\lg n) \tag{3.19}
```

其中斯特林近似（Stirling's approximation）对证明 equation (3.19)（式 (3.19)）很有帮助。下式对一切 $n \ge 1$ 同样成立：

```math
n! = \sqrt{2\pi n}\left(\frac{n}{e}\right)^n e^{\alpha_n} \tag{3.20}
```

其中

```math
\frac{1}{12n+1} < \alpha_n < \frac{1}{12n} \tag{3.21}
```

### Functional Iteration（函数迭代） <span style="color:#2471a3;">**[section]**</span>

我们用记号 $f^{(i)}(n)$ 表示把 function（函数）$f(n)$ 对初始值 $n$ iteratively applied（迭代应用）$i$ 次。形式化地说，设 $f(n)$ 是定义在实数上的函数。对非负整数 $i$，我们 recursively define（递归定义）：

```math
f^{(i)}(n) = \begin{cases} n & \text{if } i = 0, \\ f\left(f^{(i-1)}(n)\right) & \text{if } i > 0. \end{cases}
```

例如，若 $f(n) = 2n$，则 $f^{(i)}(n) = 2^i n$。

### The Iterated Logarithm Function（迭代对数函数） <span style="color:#2471a3;">**[section]**</span>

我们用记号 $\lg^* n$（读作 “log star of $n$”）来表示 iterated logarithm（迭代对数），其定义如下。令 $\lg^{(i)} n$ 就是上文定义的 $f^{(i)}(n)$，其中 $f(n) = \lg n$。由于非正数的对数没有定义，$\lg^{(i)} n$ 仅在 $\lg^{(i-1)} n > 0$ 时才有定义。务必区分 $\lg^{(i)} n$（从 argument（自变量）$n$ 开始连续应用 $i$ 次对数函数）与 $\lg^i n$（$n$ 的对数的 $i$ 次幂）。然后我们把迭代对数函数定义为：

```math
\lg^* n = \min\{\, i \ge 0 : \lg^{(i)} n \le 1 \,\}
```

迭代对数是一个增长得极其缓慢的函数：

```math
\lg^* 2 = 1, \quad \lg^* 4 = 2, \quad \lg^* 16 = 3, \quad \lg^* 65536 = 4, \quad \lg^*\left(2^{65536}\right) = 5
```

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.59</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

由于可观测宇宙（observable universe）中的原子（atom）数量估计约为 $10^{80}$，远小于 $2^{65536}$，因此我们很少会遇到使 $\lg^* n > 5$ 的 input size（输入规模）$n$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $\lg^* n$ 是"2 的幂塔"的逆运算：$2^2=4$，$2^4=16$，$2^{16}=65536$，$2^{65536}$——每登一层塔，$\lg^*$ 只加 1，所以 $\lg^* 65536=4$、$\lg^*(2^{65536})=5$。连可观测宇宙的 $10^{80}$ 个原子也只让 $\lg^*$ 停在 5 附近：这不是"增长慢"，而是"几乎不增长"。它绝非猎奇符号：在并查集（disjoint-set forest）"按秩合并 + 路径压缩"的摊还分析中，单次操作的代价以 $\alpha(n)$、总代价分析中处处出现 $\lg^*$ 级的量（CLRS §21.4，你未来会读到）；在分布式图算法的着色问题里，6.046J 第 19 讲（你已翻译过相关讲义）的轮数界同样是 $\lg^* n$。直觉上，$\lg^*$ 度量的是"要把一个数反复取对数压到常数级，需要压几轮"，而每轮压扁都是指数式的，所以轮数只能是迭代对数级。以后遇到"快得不可思议"的分析时，先想想是不是有一层 $\lg^*$ 藏在里面。

### Fibonacci Numbers（斐波那契数） <span style="color:#2471a3;">**[section]**</span>

我们用如下 recurrence（递归式）来 define（定义）Fibonacci numbers（斐波那契数）：

```math
F_0 = 0, \qquad F_1 = 1, \qquad F_i = F_{i-1} + F_{i-2} \quad \text{for } i \ge 2 \tag{3.22}
```

于是，每个斐波那契数都是前两个数之和，由此产生序列

```math
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, \ldots
```

斐波那契数与 golden ratio（黄金比率）$\phi$ 及其 conjugate（共轭数）$\widehat{\phi}$ 有关，二者是方程

```math
x^2 = x + 1 \tag{3.23}
```

的两个根，并由下面的公式给出（见 Exercise 3.2-6）：

```math
\phi = \frac{1+\sqrt{5}}{2} = 1.61803\ldots \tag{3.24}
```

```math
\widehat{\phi} = \frac{1-\sqrt{5}}{2} = -0.61803\ldots
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 黄金比率的历史比你想象的更老。据离线维基百科：欧几里得《几何原本》（约公元前 300 年）在论线段的"中末比"（extreme and mean ratio）时已研究 $\phi$——正五边形对角线与边之比正是 $\phi$，十二面体与二十面体的构造都离不开它，这是希腊几何传统；文艺复兴时 Luca Pacioli 在 1509 年的《神圣比例》中又给它染上神秘色彩，达·芬奇曾为此书绘制插图。伊斯兰几何装饰传统（伊朗建筑中大量出现的十重对称纹样）同样以正五边形、正十边形为基础，间接依赖 $\phi$。有趣的是，斐波那契 1202 年《计算之书》引入兔子序列时并未提到 $\phi$，两者的联姻是后人发现的：由下面的闭式立即可见相邻两项之比 $F_{i+1}/F_i\to\phi$。对这个"古代几何常数"来说，式 (3.23) 的 $x^2=x+1$ 才是它的现代身份证——一切性质都能从这一行代数方程推出，这正是第一性原理式的化归。

具体地，我们有

```math
F_i = \frac{\phi^i - \widehat{\phi}^i}{\sqrt{5}}
```

我们可以用 induction（归纳法）证明它（Exercise 3.2-7）。由于 $|\widehat{\phi}| < 1$，我们有

```math
\frac{|\widehat{\phi}^i|}{\sqrt{5}} < \frac{1}{\sqrt{5}} < \frac{1}{2}
```

这意味着

---

> <span style="color:#7f8c8d;">CLRS §3.2, p.60</span>

### Section 3.2 · Standard Notations and Common Functions（标准记号与常用函数）（续）

```math
F_i = \left\lfloor \frac{\phi^i}{\sqrt{5}} + \frac{1}{2} \right\rfloor \tag{3.25}
```

也就是说，第 $i$ 个 Fibonacci number（斐波那契数）$F_i$ 等于 $\phi^i/\sqrt{5}$ round（四舍五入）到 nearest integer（最近整数）的结果。因此，Fibonacci numbers（斐波那契数）是 exponentially（指数级）增长的。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么一个只含加法的递推会藏出闭式？用第一性原理拆开：$F_i=F_{i-1}+F_{i-2}$ 是线性递推，其全体解在"序列加法与数乘"下封闭，构成一个向量空间——这正是 Strang 线性代数 / 18.065 的语言。猜一个纯指数解 $F_i=x^i$ 代入，得特征方程 $x^2=x+1$，两根 $\phi$ 与 $\widehat{\phi}$ 就是这空间的一组"特征方向"；通解 $F_i=A\phi^i+B\widehat{\phi}^i$，再由 $F_0=0$、$F_1=1$ 解出 $A=1/\sqrt5$、$B=-1/\sqrt5$。矩阵视角更透彻：把递推写成 $\binom{F_{i+1}}{F_i}=\begin{pmatrix}1&1\\1&0\end{pmatrix}\binom{F_i}{F_{i-1}}$，闭式就是对转移矩阵做对角化（特征值恰为 $\phi,\widehat{\phi}$）的结果。而 $|\widehat{\phi}|<1$ 使 $\widehat{\phi}^i$ 指数衰减，故 $\phi^i/\sqrt5$ 四舍五入就是 $F_i$——式 (3.25)。这套"特征方程—对角化"套路会原封不动地出现在你以后分析任何线性递推的场合。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**3.2-1**

Show that if $f(n)$ and $g(n)$ are monotonically increasing functions, then so are the functions $f(n) + g(n)$ and $f(g(n))$, and if $f(n)$ and $g(n)$ are in addition nonnegative, then $f(n) \cdot g(n)$ is monotonically increasing.

**3.2-2**

Prove equation (3.16).

**3.2-3**

Prove equation (3.19). Also prove that $n! = \omega(2^n)$ and $n! = o(n^n)$.

**3.2-4** $\star$

Is the function $\lceil \lg n \rceil!$ polynomially bounded? Is the function $\lceil \lg\lg n \rceil!$ polynomially bounded?

**3.2-5** $\star$

Which is asymptotically larger: $\lg(\lg^* n)$ or $\lg^*(\lg n)$?

**3.2-6**

Show that the golden ratio $\phi$ and its conjugate $\widehat{\phi}$ both satisfy the equation

```math
x^2 = x + 1
```

**3.2-7**

Prove by induction that the $i$th Fibonacci number satisfies the equality

```math
F_i = \frac{\phi^i - \widehat{\phi}^i}{\sqrt{5}}
```

where $\phi$ is the golden ratio and $\widehat{\phi}$ is its conjugate.

**3.2-8**

Show that $k\ln k = \Theta(n)$ implies $k = \Theta(n/\ln n)$.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 3, p.61</span>

## Problems for Chapter 3（第 3 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 3-1 · Asymptotic behavior of polynomials（多项式的渐近行为） <span style="color:#2471a3;">**[problem]**</span>

Let

```math
p(n) = \sum_{i=0}^{d} a_i n^i
```

where $a_d > 0$, be a degree-$d$ polynomial in $n$, and let $k$ be a constant. Use the definitions of the asymptotic notations to prove the following properties.

a. If $k \ge d$, then $p(n) = O(n^k)$.

b. If $k \le d$, then $p(n) = \Omega(n^k)$.

c. If $k = d$, then $p(n) = \Theta(n^k)$.

d. If $k > d$, then $p(n) = o(n^k)$.

e. If $k < d$, then $p(n) = \omega(n^k)$.

### Problem 3-2 · Relative asymptotic growths（相对渐近增长） <span style="color:#2471a3;">**[problem]**</span>

Indicate, for each pair of expressions $(A, B)$ in the table below, whether $A$ is $O$, $o$, $\Omega$, $\omega$, or $\Theta$ of $B$. Assume that $k \ge 1$, $\epsilon > 0$, and $c > 1$ are constants. Your answer should be in the form of the table with "yes" or "no" written in each box.

| | $A$ | $B$ | $O$ | $o$ | $\Omega$ | $\omega$ | $\Theta$ |
|---|---|---|---|---|---|---|---|
| a. | $\lg^k n$ | $n^{\epsilon}$ | | | | | |
| b. | $n^k$ | $c^n$ | | | | | |
| c. | $\sqrt{n}$ | $n^{\sin n}$ | | | | | |
| d. | $2^n$ | $2^{n/2}$ | | | | | |
| e. | $n^{\lg c}$ | $c^{\lg n}$ | | | | | |
| f. | $\lg(n!)$ | $\lg(n^n)$ | | | | | |

### Problem 3-3 · Ordering by asymptotic growth rates（按渐近增长率排序） <span style="color:#2471a3;">**[problem]**</span>

a. Rank the following functions by order of growth; that is, find an arrangement $g_1, g_2, \ldots, g_{30}$ of the functions satisfying $g_1 = \Omega(g_2)$, $g_2 = \Omega(g_3)$, $\ldots$, $g_{29} = \Omega(g_{30})$. Partition your list into equivalence classes such that functions $f(n)$ and $g(n)$ are in the same class if and only if $f(n) = \Theta(g(n))$.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 3, p.62</span>

## Problems for Chapter 3（第 3 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 3-3 · Ordering by asymptotic growth rates（按渐近增长率排序） <span style="color:#2471a3;">**[problem]**</span>（续）

a.

> <span style="color:#1e8449;">**[note]**</span> 译者注：待排序的 30 个 functions（函数）如下表。

| $\lg(\lg^* n)$ | $2^{\lg^* n}$ | $(\sqrt{2})^{\lg n}$ | $n^2$ | $n!$ |
|---|---|---|---|---|
| $(\lg n)!$ | $(3/2)^n$ | $n^3$ | $\lg^2 n$ | $\lg(n!)$ |
| $2^{2^n}$ | $n^{1/\lg n}$ | $\ln\ln n$ | $\lg^* n$ | $n \cdot 2^n$ |
| $n^{\lg\lg n}$ | $\ln n$ | $1$ | $2^{\lg n}$ | $(\lg n)^{\lg n}$ |
| $e^n$ | $4^{\lg n}$ | $(n+1)!$ | $\sqrt{\lg n}$ | $\lg^*(\lg n)$ |
| $2^{\sqrt{2\lg n}}$ | $n$ | $2^n$ | $n\lg n$ | $2^{2^{n+1}}$ |

> <span style="color:#1e8449;">**[note]**</span> 译者注：表中共 30 个函数，恰为上题 (a) 中需要按 order of growth（增长阶数）排序的对象。

b. Give an example of a single nonnegative function $f(n)$ such that for all functions $g_i(n)$ in part (a), $f(n)$ is neither $O(g_i(n))$ nor $\Omega(g_i(n))$.

### Problem 3-4 · Asymptotic notation properties（渐近记号的性质） <span style="color:#2471a3;">**[problem]**</span>

Let $f(n)$ and $g(n)$ be asymptotically positive functions. Prove or disprove each of the following conjectures.

a. $f(n) = O(g(n))$ implies $g(n) = O(f(n))$.

b. $f(n) + g(n) = \Theta(\min(f(n), g(n)))$.

c. $f(n) = O(g(n))$ implies $\lg(f(n)) = O(\lg(g(n)))$, where $\lg(g(n)) \ge 1$ and $f(n) \ge 1$ for all sufficiently large $n$.

d. $f(n) = O(g(n))$ implies $2^{f(n)} = O\left(2^{g(n)}\right)$.

e. $f(n) = O\left((f(n))^2\right)$.

f. $f(n) = O(g(n))$ implies $g(n) = \Omega(f(n))$.

g. $f(n) = \Theta(f(n/2))$.

h. $f(n) + o(f(n)) = \Theta(f(n))$.

### Problem 3-5 · Variations on O and Ω（O 与 Ω 的变体） <span style="color:#2471a3;">**[problem]**</span>

Some authors define $\Omega$ in a slightly different way than we do; let's use $\Omega^{\infty}$ (read "omega infinity") for this alternative definition. We say that $f(n) = \Omega^{\infty}(g(n))$ if there exists a positive constant $c$ such that $f(n) \ge cg(n) \ge 0$ for infinitely many integers $n$.

a. Show that for any two functions $f(n)$ and $g(n)$ that are asymptotically nonnegative, either $f(n) = O(g(n))$ or $f(n) = \Omega^{\infty}(g(n))$ or both, whereas this is not true if we use $\Omega$ in place of $\Omega^{\infty}$.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 3, p.63</span>

## Problems for Chapter 3（第 3 章的问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 3-5 · Variations on O and Ω（O 与 Ω 的变体） <span style="color:#2471a3;">**[problem]**</span>（续）

b. Describe the potential advantages and disadvantages of using $\Omega^{\infty}$ instead of $\Omega$ to characterize the running times of programs.

Some authors also define $O$ in a slightly different manner; let's use $O'$ for the alternative definition. We say that $f(n) = O'(g(n))$ if and only if $|f(n)| = O(g(n))$.

c. What happens to each direction of the "if and only if" in Theorem 3.1 if we substitute $O'$ for $O$ but still use $\Omega$?

Some authors define $\widetilde{O}$ (read "soft-oh") to mean $O$ with logarithmic factors ignored:

```math
\widetilde{O}(g(n)) = \{\, f(n) : \text{there exist positive constants } c,\ k,\ \text{and } n_0 \text{ such that } 0 \le f(n) \le c\,g(n)\lg^k(n) \text{ for all } n \ge n_0 \,\}
```

d. Define $\widetilde{\Omega}$ and $\widetilde{\Theta}$ in a similar manner. Prove the corresponding analog to Theorem 3.1.

### Problem 3-6 · Iterated functions（迭代函数） <span style="color:#2471a3;">**[problem]**</span>

We can apply the iteration operator $*$ used in the $\lg^*$ function to any monotonically increasing function $f(n)$ over the reals. For a given constant $c \in \mathbb{R}$, we define the iterated function $f_c^*$ by

```math
f_c^*(n) = \min\{\, i \ge 0 : f^{(i)}(n) \le c \,\}
```

which need not be well defined in all cases. In other words, the quantity $f_c^*(n)$ is the number of iterated applications of the function $f$ required to reduce its argument down to $c$ or less.

For each of the following functions $f(n)$ and constants $c$, give as tight a bound as possible on $f_c^*(n)$.

| | $f(n)$ | $c$ | $f_c^*(n)$ |
|---|---|---|---|
| a. | $n-1$ | $0$ | |
| b. | $\lg n$ | $1$ | |
| c. | $n/2$ | $1$ | |
| d. | $n/2$ | $2$ | |
| e. | $\sqrt{n}$ | $2$ | |
| f. | $\sqrt{n}$ | $1$ | |
| g. | $n^{1/3}$ | $2$ | |
| h. | $n/\lg n$ | $2$ | |

---

> <span style="color:#7f8c8d;">CLRS Chapter 3 · Chapter notes, p.64</span>


> <span style="color:#7f8c8d;">[note] 译者说明：按照翻译规范第 7 条，本章末的 Chapter notes（本章注记，即参考文献性内容）保留英文原文。其内容要点：O 记号源自 Bachmann 1892 年的数论著作；o 记号由 Landau 于 1909 年提出；Θ 与 Ω 记号由 Knuth 倡导，用以纠正文献中滥用 O 记号同时表示上下界的做法；式 (3.20) 归功于 Robbins。</span>

Knuth [209] traces the origin of the O-notation to a number-theory text by P. Bachmann in 1892. The o-notation was invented by E. Landau in 1909 for his discussion of the distribution of prime numbers. The Ω and Θ notations were advocated by Knuth [213] to correct the popular, but technically sloppy, practice in the literature of using O-notation for both upper and lower bounds. Many people continue to use the O-notation where the Θ-notation is more technically precise. Further discussion of the history and development of asymptotic notations appears in works by Knuth [209, 213] and Brassard and Bratley [54].

Not all authors define the asymptotic notations in the same way, although the various definitions agree in most common situations. Some of the alternative definitions encompass functions that are not asymptotically nonnegative, as long as their absolute values are appropriately bounded.

Equation (3.20) is due to Robbins [297]. Other properties of elementary mathematical functions can be found in any good mathematical reference, such as Abramowitz and Stegun [1] or Zwillinger [362], or in a calculus book, such as Apostol [18] or Thomas et al. [334]. Knuth [209] and Graham, Knuth, and Patashnik [152] contain a wealth of material on discrete mathematics as used in computer science.

---

> <span style="color:#7f8c8d;">CLRS Chapter 4, p.65</span>

## Chapter 4（第 4 章）· Divide-and-Conquer（分治法）

在 §2.3.1 中，我们已经看到 merge sort（归并排序）如何作为 divide-and-conquer paradigm（分治范式）的一个范例。回顾一下：在 divide-and-conquer 中，我们递归地求解一个问题，并在递归的每一层应用以下三个步骤：

- **Divide（分解）：** 将问题分解为若干 subproblems（子问题），它们是同一个问题的 smaller instances（较小实例）。
- **Conquer（解决）：** 通过递归地求解来 conquer（攻克）这些 subproblems。不过，如果某个 subproblem 的规模已经足够小，就直接以 straightforward manner（直截了当的方式）求解它。
- **Combine（合并）：** 把各 subproblems 的解 combine（合并）为原问题的解。

当 subproblems 大到还可以递归求解时，我们称之为 recursive case（递归情况）。一旦 subproblems 小到我们不再递归，就说递归 "bottoms out"（触底），此时我们到达了 base case（基本情况）。有时，除了那些作为同一问题较小实例的 subproblems 之外，我们还不得不求解一些与原问题并不完全相同的 subproblems；我们把求解这类 subproblems 视为 combine 步骤的一部分。

在本章中，我们将看到更多基于 divide-and-conquer 的 algorithms（算法）。第一个算法解决的是 maximum-subarray problem（最大子数组问题）：它以一个由数组成的 array（数组）作为输入，确定其中 values（值）之和最大的 contiguous subarray（连续子数组）。接着我们会看到两个用于相乘 $n \times n$ matrix（矩阵）的 divide-and-conquer 算法。其中一个的运行时间为 $\Theta(n^3)$，并不比直接相乘 square matrix（方阵）的 straightforward method（直接方法）更好；而另一个，即 Strassen's algorithm（Strassen 算法），运行时间为 $O(n^{2.81})$，在渐近意义上胜过了直接方法。

### Recurrences（递归式）

Recurrence（递归式）与 divide-and-conquer paradigm 相伴而行，因为它们为我们提供了一种刻画 divide-and-conquer 算法 running time（运行时间）的自然方式。A recurrence（递归式）是一个 equation（方程）或 inequality（不等式），它用该函数在

> <span style="color:#7f8c8d;">[note] 本句接下页 "……较小输入上的值来描述该函数"（of its value on smaller inputs）。</span>

---

> <span style="color:#7f8c8d;">CLRS Chapter 4 · Recurrences, p.66</span>

……较小输入上的值来描述该函数（of its value on smaller inputs）。例如，在 §2.3.2 中，我们用如下 recurrence（递归式）描述了 MERGE-SORT 过程的 worst-case running time（最坏情况运行时间）$T(n)$：

```math
T(n) = \begin{cases} \Theta(1) & \text{if } n = 1, \\ 2T(n/2) + \Theta(n) & \text{if } n > 1, \end{cases} \tag{4.1}
```

其解我们当时声称是 $T(n) = \Theta(n \lg n)$。

Recurrences 可以呈现多种形式。例如，一个 recursive algorithm（递归算法）可能把问题分解为规模不等的 subproblems，比如按 $2/3$ 对 $1/3$ 的比例拆分。如果 divide（分解）与 combine（合并）这两个步骤需要 linear time（线性时间），那么这样的算法就会导出递归式 $T(n) = T(2n/3) + T(n/3) + \Theta(n)$。

Subproblems 并不一定被限定为原问题规模的某个 constant fraction（常数比例）。例如，linear search（线性搜索）的 recursive version（递归版本，见 Exercise 2.1-3）只会创建一个 subproblem，它仅比原问题少一个 element（元素）。每次 recursive call（递归调用）只花费 constant time（常量时间），再加上它发起的各次递归调用所花费的时间，由此得到递归式 $T(n) = T(n-1) + \Theta(1)$。

本章给出三种求解 recurrences 的方法——也就是为递归式的解求得渐近的 "$\Theta$" 或 "$O$" bound（界）的方法：

- 在 substitution method（代换法）中，我们先猜测一个界，然后用 mathematical induction（数学归纳法）证明我们的猜测正确。
- recursion-tree method（递归树法）把递归式转换成一棵 tree（树），其 nodes（结点）表示递归的各个层次上产生的 cost（代价）。然后我们运用界定 summations（求和式）的技术来求解该递归式。
- master method（主方法）为如下形式的 recurrences 提供界：

```math
T(n) = aT(n/b) + f(n), \tag{4.2}
```

其中 $a \ge 1$，$b > 1$，而 $f(n)$ 是一个给定的 function（函数）。这样的 recurrences 出现得相当频繁。形如式 (4.2) 的递归式刻画了一个 divide-and-conquer 算法：它创建 $a$ 个 subproblems，每个 subproblem 的规模都是原问题的 $1/b$，并且 divide 与 combine 这两个步骤合计花费 $f(n)$ 时间。

要使用 master method，你需要记住三种 case（情况）；不过一旦记住，你就能够轻松地确定许多简单 recurrences 的 asymptotic bounds（渐近界）。我们将用 master method 来确定求解 maximum-subarray problem（最大子数组问题）与 matrix multiplication（矩阵乘法）的 divide-and-conquer 算法的 running times，以及本书其他地方基于 divide-and-conquer 的其他算法的运行时间。

---

> <span style="color:#7f8c8d;">CLRS Chapter 4 · Recurrences, p.67</span>

偶尔，我们会看到一些 recurrences 并非等式，而是 inequality（不等式），例如 $T(n) \le 2T(n/2) + \Theta(n)$。因为这样的递归式只给出了 $T(n)$ 的一个 upper bound（上界），所以我们将用 O-notation（O 记号）而非 Θ-notation（Θ 记号）来表述它的解。类似地，如果不等号反向，变成 $T(n) \ge 2T(n/2) + \Theta(n)$，那么由于该递归式只给出了 $T(n)$ 的一个 lower bound（下界），我们就会在其解中使用 Ω-notation（Ω 记号）。

### Technicalities in recurrences（递归式中的技术细节）

在实践中，当我们陈述并求解 recurrences 时，会忽略某些 technical details（技术细节）。例如，如果在 $n$ 为奇数时对 $n$ 个 elements 调用 MERGE-SORT，我们最终得到的 subproblems 的规模分别是 $\lfloor n/2 \rfloor$ 和 $\lceil n/2 \rceil$。这两个规模实际上都不是 $n/2$，因为当 $n$ 为奇数时 $n/2$ 不是整数。严格说来，描述 MERGE-SORT 最坏情况运行时间的递归式其实是：

```math
T(n) = \begin{cases} \Theta(1) & \text{if } n = 1, \\ T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + \Theta(n) & \text{if } n > 1. \end{cases} \tag{4.3}
```

Boundary conditions（边界条件）是我们通常忽略的另一类细节。由于算法在 constant-sized input（常量规模输入）上的 running time 是一个常量，所以由算法运行时间导出的 recurrences 一般在 $n$ 充分小时有 $T(n) = \Theta(1)$。因此，为方便起见，我们通常省略递归式边界条件的陈述，并假定 $T(n)$ 在 $n$ 较小时为常量。例如，我们通常把递归式 (4.1) 陈述为：

```math
T(n) = 2T(n/2) + \Theta(n), \tag{4.4}
```

而不显式给出 $n$ 较小时的取值。理由是：尽管改变 $T(1)$ 的值会改变该递归式的 exact solution（精确解），但这个解的改变通常不超过一个 constant factor（常数因子），因此 order of growth（增长阶数）不变。

当我们陈述并求解 recurrences 时，常常会省略 floor（下取整）、ceiling（上取整）以及 boundary conditions。我们放下这些细节径直推进，之后再确定它们是否要紧。它们通常不要紧，但你应当知道它们何时要紧。Experience（经验）会有所帮助，一些定理同样如此——这些定理断言：对于许多刻画 divide-and-conquer 算法的 recurrences 而言，这些细节并不影响其 asymptotic bounds（渐近界）（见 Theorem 4.1，定理 4.1）。不过在本章中，我们将着手处理其中一些细节，并阐释递归式求解方法中的 fine points（精妙之处）。

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.68</span>

### Section 4.1 · The maximum-subarray problem（最大子数组问题） <span style="color:#2471a3;">**[section]**</span>

假设有人向你提供一个投资 Volatile Chemical Corporation（挥发性化学公司）的机会。正如该公司生产的 chemicals（化学品）一样，Volatile Chemical Corporation 的 stock price（股票价格）也相当 volatile（不稳定）。你只被允许一次性购买一个 unit（单位）的 stock（股票），然后在之后的某个日期卖出，且买卖都在当天交易结束（close of trading）之后进行。作为对这一限制的补偿，你可以预先得知未来该股票的价格。你的目标是使 profit（利润）最大化。图 4.1 展示了该股票在 17 天内的价格。你可以在 day 0（第 0 天）之后的任意时刻买入，第 0 天时的价格为每股 \$100。当然，你会想"低价买入，高价卖出"（buy low, sell high）——在尽可能低的价格买入，之后再在尽可能高的价格卖出——以使利润最大化。遗憾的是，在给定的时间段内，你可能未必能先在最低价买入、再在最高价卖出。在图 4.1 中，最低价出现在第 7 天之后，而它晚于出现在第 1 天之后的最高价。

你可能认为：总能通过"在最低价买入"或"在最高价卖出"二者之一来使利润最大化。例如在图 4.1 中，我们通过在第 7 天之后（最低价处）买入即可使利润最大化。如果这个策略总是奏效，那么确定如何使利润最大化就很容易了：找出最高价和最低价，然后从最高价向左回溯找出此前出现的最低价，从最低价向右查找此后出现的最高价，并取差值更大的那一对。图 4.2 给出了一个简单的反例（接下页）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这个"买低卖高"的故事是一次纯正的建模（modeling）训练：问题原本长着时间序列的样子，直接在价格序列上思考会掉进"最低点必须在最高点之前"的时序陷阱——图 4.2 的反例正是用来打脸天真的"锚定最低价"策略的。而书后几页的关键一步，是把相邻两天的 change in price（价格差分）排成数组：一段买卖区间的利润恰好等于对应差分段的和，于是"何时买卖"变成了"哪一段之和最大"。这正是 6.042J 反复强调的问题转化思想：同一个问题在不同表示下难度突变，选对表示常常比设计聪明算法更值钱。差分是离散版的求导，"利润 = 差分之和"就是微积分基本定理的离散影子；分析化学里"由浓度差分推总量"也是同构操作。记住这个两步节奏：先找到一个让目标函数"可分解"的表示，再对该表示上的子结构递归或扫描。

> <span style="color:#7f8c8d;">[note] 本页含插图：图 4.1。图面结构：一张折线图（横轴 Day 为第 0–16 天，纵轴 Price 为 \$60–\$120 的股价曲线），下方附一张 17 列的表格。表格第一行为 Day（第 0–16 天），第二行为 Price（收盘价）：100、113、110、85、105、102、86、63、81、101、94、106、101、79、94、90、97；第三行为 Change（相对前一日的价格变化）：—、13、−3、−25、20、−3、−16、−23、18、20、−7、12、−5、−22、15、−4、7。</span>

**Figure 4.1（图 4.1）** Volatile Chemical Corporation（挥发性化学公司）在 17 天期间每日交易结束后的股票价格信息。图中横轴（horizontal axis）表示 day（天），纵轴（vertical axis）表示 price（价格）。表格最下面一行给出的是相对前一天的 change in price（价格变化）。

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.69</span>

> <span style="color:#7f8c8d;">[note] 本页含插图：图 4.2。图面结构：一张折线图（横轴 Day 为第 0–4 天，纵轴为股价曲线），下方附一张 5 列的表格：Day 为第 0–4 天；Price 依次为 10、11、7、10、6；Change 依次为 —、1、−4、3、−4。</span>

**Figure 4.2（图 4.2）** 一个表明 maximum profit（最大利润）并不总是从最低价格开始、也不总是在最高价格结束的例子。同样，横轴表示 day（天），纵轴表示 price（价格）。这里，每股 \$3 的最大利润要通过在第 2 天之后买入、并在第 3 天之后卖出才能获得。第 2 天之后的 \$7 并不是整体上的最低价格，而第 3 天之后的 \$10 也不是整体上的最高价格。

……该反例表明：maximum profit 有时既不是靠在最低价买入得到的，也不是靠在最高价卖出得到的。

### A brute-force solution（暴力求解） <span style="color:#2471a3;">**[section]**</span>

我们可以很容易地为这个问题设计出一个 brute-force solution（暴力法解）：只需尝试每一对可能的 buy and sell dates（买入日期与卖出日期），其中买入日期先于卖出日期。一个为期 $n$ 天的时间段共有 $\binom{n}{2}$ 个这样的日期对。由于 $\binom{n}{2}$ 是 $\Theta(n^2)$ 的，而我们最多只能指望在 constant time（常量时间）内评估每一对日期，因此这种方法需要 $\Omega(n^2)$ 时间。我们能做得更好吗？

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 暴力法的代价账本值得用 6.042J 的计数技术精算一遍：买入日必须严格早于卖出日，日期对个数是 $\binom{n}{2}=\frac{n(n-1)}{2}=\Theta(n^2)$——从 $n$ 天中无序选 2 天，组合数一步到位；若还允许"当天买当天卖"，则是 $\binom{n}{2}+n=\binom{n+1}{2}$，阶数不变。这正是「枚举所有候选 + 求和计数」模板的前半步：先数清候选总量，再评估单个候选的代价，两者相乘即得总代价（下一页还会展示"借已算出的子数组和把单项代价降到 $O(1)$"的组织技巧）。$\binom{n}{2}=\Theta(n^2)$ 这类估计在本书无处不在：插入排序的双重循环、所有点对的比较都是它。也别小看暴力法的地位：它是 baseline（基准线）——先有正确但慢的解，"我们能做得更好吗"才成为一个可检验的问题，习题 4.1-3 的交叉点 $n_0$ 实验也才有对照物。

### A transformation（一种变换） <span style="color:#2471a3;">**[section]**</span>

为了设计出一个运行时间为 $o(n^2)$ 的 algorithm，我们将以一种略有不同的方式来看待 input（输入）。我们想找出这样一个由若干天组成的序列（days sequence）：从第一天到最后一天，其 net change（净变化）最大。我们不再逐日考察价格，而是转而考察每日的 change in price（价格变化），其中第 $i$ 天的变化是第 $i-1$ 天之后与第 $i$ 天之后这两个价格之差。图 4.1 中的表格在最下面一行给出了这些每日变化。如果我们把这一行当作一个 array（数组）$A$（如图 4.3 所示），那么现在我们要找的就是 $A$ 的那个非空、连续、且各值之和最大的 subarray（子数组）。我们把这个连续子数组称为 maximum subarray（最大子数组）。例如，在图 4.3 的数组中，$A[1..16]$ 的 maximum subarray 是 $A[8..11]$，其 sum（和）为 43。因此，你会希望在第 8 天之前（也就是第 7 天之后）买入股票，并在第 11 天之后卖出，从而获得每股 \$43 的利润。

乍一看，这种 transformation（变换）似乎无济于事。对于一个为期 $n$ 天的时间段，我们仍需检查 $\binom{n-1}{2} = \Theta(n^2)$ 个 subarrays。Exercise 4.1-2（习题 4.1-2）会请你证明

> <span style="color:#7f8c8d;">[note] 本句接下页 "……虽然计算一个子数组的代价可能与该子数组的长度成正比，但在计算所有 Θ(n²) 个子数组的和时，我们可以组织计算，使得在已知先前已算出的子数组和的情况下，每个子数组的和只需 O(1) 时间，于是暴力法解需要 Θ(n²) 时间。"</span>

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.70</span>

> <span style="color:#7f8c8d;">[note] 本页含插图：图 4.3。图面结构：一维数组 $A$，下标 1–16 依次对应值 13、−3、−25、20、−3、−16、−23、18、20、−7、12、−5、−22、15、−4、7；其中下标 8–11 的四个元素（18、20、−7、12）被框出，并标注 "maximum subarray"（最大子数组）。</span>

**Figure 4.3（图 4.3）** 把股票价格变化视为一个 maximum-subarray problem（最大子数组问题）。这里，subarray $A[8..11]$ 的和为 43，它是数组 $A$ 的所有 contiguous subarray（连续子数组）中和最大的一个。

……虽然计算一个 subarray 的 cost（代价）可能与该 subarray 的 length（长度）成正比，但在计算所有 $\Theta(n^2)$ 个 subarray 的和时，我们可以对计算加以组织：在已知先前已算出的 subarray sums（子数组和）的情况下，使每个 subarray 的和只需 $O(1)$ 时间，于是 brute-force solution（暴力法解）需要 $\Theta(n^2)$ 时间。

因此，让我们为 maximum-subarray problem 寻求一个更高效的解法。在这样做时，我们通常会说 "一个"（a）maximum subarray 而非 "那个"（the）maximum subarray，因为达成最大和的 subarray 可能不止一个。

只有当数组包含一些 negative numbers（负数）时，maximum-subarray problem 才有意思。如果数组的所有 entries（元素）都是 nonnegative（非负的），那么 maximum-subarray problem 将毫无挑战性，因为整个数组本身就会给出最大的和。

### A solution using divide-and-conquer（一种使用分治法的解决方案） <span style="color:#2471a3;">**[section]**</span>

让我们思考一下：如何用 divide-and-conquer technique（分治技术）来求解 maximum-subarray problem。假设我们想找出 subarray $\mathit{A}[\mathit{low}..\mathit{high}]$ 的一个 maximum subarray。divide-and-conquer 提示我们：把这个 subarray 分解成两个规模尽可能均等的 subarrays。也就是说，找出该 subarray 的 midpoint（中点），设为 $\mathit{mid}$，然后考虑 subarray $\mathit{A}[\mathit{low}..\mathit{mid}]$ 和 $\mathit{A}[\mathit{mid}+1..\mathit{high}]$。如图 4.4(a) 所示，$\mathit{A}[\mathit{low}..\mathit{high}]$ 的任何 contiguous subarray $\mathit{A}[i..j]$ 必定恰好位于以下三种位置之一：

- 完全位于 subarray $\mathit{A}[\mathit{low}..\mathit{mid}]$ 中，即 $\mathit{low} \le i \le j \le \mathit{mid}$；
- 完全位于 subarray $\mathit{A}[\mathit{mid}+1..\mathit{high}]$ 中，即 $\mathit{mid} < i \le j \le \mathit{high}$；
- 跨越 midpoint（crossing the midpoint），即 $\mathit{low} \le i \le \mathit{mid} < j \le \mathit{high}$。

因此，$\mathit{A}[\mathit{low}..\mathit{high}]$ 的一个 maximum subarray 必定恰好位于这些位置之一。事实上，$\mathit{A}[\mathit{low}..\mathit{high}]$ 的一个 maximum subarray 必定是在以下三种 subarrays 中拥有最大和者：完全位于 $\mathit{A}[\mathit{low}..\mathit{mid}]$ 中的、完全位于 $\mathit{A}[\mathit{mid}+1..\mathit{high}]$ 中的，以及跨越 midpoint 的。我们可以递归地求出 $\mathit{A}[\mathit{low}..\mathit{mid}]$ 和 $\mathit{A}[\mathit{mid}+1..\mathit{high}]$ 的 maximum subarrays，因为这两个 subproblems 都是"求一个 maximum subarray"这一问题的 smaller instances（较小实例）。于是，剩下要做的就是找出一个

> <span style="color:#7f8c8d;">[note] 本句接下页 "……跨越中点的最大子数组（a maximum subarray that crosses the midpoint）"。</span>

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.71</span>

### Section 4.1 · The maximum-subarray problem（最大子数组问题）（续）

**Figure 4.4（图 4.4）** (a) 数组 $A[\mathit{low}..\mathit{high}]$ 的 subarray（子数组）的可能位置：完全位于 $A[\mathit{low}..\mathit{mid}]$ 之中（entirely in $A[\mathit{low}..\mathit{mid}]$）、完全位于 $A[\mathit{mid}+1..\mathit{high}]$ 之中，或者 crossing the midpoint（跨越中点）$\mathit{mid}$。(b) 任何跨越中点的 $A[\mathit{low}..\mathit{high}]$ 的子数组，都由两个子数组 $A[i..\mathit{mid}]$ 与 $A[\mathit{mid}+1..j]$ 组成，其中 $\mathit{low} \le i \le \mathit{mid}$ 且 $\mathit{mid} < j \le \mathit{high}$。

（承上页）……的 maximum subarray（最大子数组），然后取三者中 sum（和）最大的那个子数组。

我们很容易在线性时间内找出跨越中点的最大子数组，所用时间与子数组 $A[\mathit{low}..\mathit{high}]$ 的规模成 linear（线性）关系。这个问题并不是原问题的一个更小的 instance（实例），因为它多了一条限制：所选的子数组必须跨越中点。如 Figure 4.4(b) 所示，任何跨越中点的子数组本身都由两个子数组 $A[i..\mathit{mid}]$ 与 $A[\mathit{mid}+1..j]$ 构成，其中 $\mathit{low} \le i \le \mathit{mid}$ 且 $\mathit{mid} < j \le \mathit{high}$。因此，我们只需找出形如 $A[i..\mathit{mid}]$ 与 $A[\mathit{mid}+1..j]$ 的最大子数组，再将它们 combine（合并）起来即可。过程 FIND-MAX-CROSSING-SUBARRAY 以数组 $A$ 以及下标 $\mathit{low}$、$\mathit{mid}$、$\mathit{high}$ 作为 input（输入），返回一个 tuple（元组），其中包含划定跨越中点的最大子数组边界的下标，以及该最大子数组中各值之和。

```
FIND-MAX-CROSSING-SUBARRAY(A, low, mid, high)
 1  left-sum = -∞
 2  sum = 0
 3  for i = mid downto low
 4      sum = sum + A[i]
 5      if sum > left-sum
 6          left-sum = sum
 7          max-left = i
 8  right-sum = -∞
 9  sum = 0
10  for j = mid + 1 to high
11      sum = sum + A[j]
12      if sum > right-sum
13          right-sum = sum
14          max-right = j
15  return (max-left, max-right, left-sum + right-sum)
```

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.72</span>

### Section 4.1 · The maximum-subarray problem（最大子数组问题）（续）

这一过程的工作方式如下。第 1–7 行在左半部分 $A[\mathit{low}..\mathit{mid}]$ 中寻找 maximum subarray（最大子数组）。由于该子数组必须包含 $A[\mathit{mid}]$，第 3–7 行的 for 循环让下标 $i$ 从 $\mathit{mid}$ 递减到 $\mathit{low}$，因此它考虑的每个子数组都形如 $A[i..\mathit{mid}]$。第 1–2 行 initialize（初始化）变量 `left-sum`（保存迄今找到的最大和）与 `sum`（保存 $A[i..\mathit{mid}]$ 中各元素之和）。每当在第 5 行发现某个子数组 $A[i..\mathit{mid}]$ 的各值之和大于 `left-sum` 时，我们就在第 6 行把 `left-sum` 更新为该子数组的和，并在第 7 行更新变量 `max-left` 来记录这个下标 $i$。第 8–14 行对右半部分 $A[\mathit{mid}+1..\mathit{high}]$ 进行类似处理。这里，第 10–14 行的 for 循环让下标 $j$ 从 $\mathit{mid}+1$ 递增到 $\mathit{high}$，因此它考虑的每个子数组都形如 $A[\mathit{mid}+1..j]$。最后，第 15 行返回划定跨越中点的最大子数组边界的下标 `max-left` 与 `max-right`，以及子数组 $A[\mathit{max\text{-}left}..\mathit{max\text{-}right}]$ 中各值之和 `left-sum + right-sum`。

如果子数组 $A[\mathit{low}..\mathit{high}]$ 包含 $n$ 个元素（即 $n = \mathit{high} - \mathit{low} + 1$），我们声称调用 FIND-MAX-CROSSING-SUBARRAY$(A, \mathit{low}, \mathit{mid}, \mathit{high})$ 需要 $\Theta(n)$ 时间。由于两个 for 循环各自的每次迭代都只需 $\Theta(1)$ 时间，我们只需要统计迭代总次数。第 3–7 行的 for 循环执行 $\mathit{mid} - \mathit{low} + 1$ 次迭代，第 10–14 行的 for 循环执行 $\mathit{high} - \mathit{mid}$ 次迭代，因此迭代总数为

```math
(\mathit{mid} - \mathit{low} + 1) + (\mathit{high} - \mathit{mid}) = \mathit{high} - \mathit{low} + 1 = n.
```

有了这个 linear-time（线性时间）的 FIND-MAX-CROSSING-SUBARRAY 过程，我们就可以写出解决 maximum-subarray problem（最大子数组问题）的 divide-and-conquer（分治法）算法的 pseudocode（伪代码）：

```
FIND-MAXIMUM-SUBARRAY(A, low, high)
 1  if high == low
 2      return (low, high, A[low])        // base case: only one element
 3  else mid = ⌊(low + high)/2⌋
 4      (left-low, left-high, left-sum) =
            FIND-MAXIMUM-SUBARRAY(A, low, mid)
 5      (right-low, right-high, right-sum) =
            FIND-MAXIMUM-SUBARRAY(A, mid + 1, high)
 6      (cross-low, cross-high, cross-sum) =
            FIND-MAX-CROSSING-SUBARRAY(A, low, mid, high)
 7      if left-sum ≥ right-sum and left-sum ≥ cross-sum
 8          return (left-low, left-high, left-sum)
 9      elseif right-sum ≥ left-sum and right-sum ≥ cross-sum
10          return (right-low, right-high, right-sum)
11      else return (cross-low, cross-high, cross-sum)
```

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.73</span>

### Section 4.1 · The maximum-subarray problem（最大子数组问题）（续）

初始调用 FIND-MAXIMUM-SUBARRAY$(A, 1, A.length)$ 将找出 $A[1..n]$ 的一个 maximum subarray（最大子数组）。

与 FIND-MAX-CROSSING-SUBARRAY 类似，recursive procedure（递归过程）FIND-MAXIMUM-SUBARRAY 也返回一个 tuple（元组），其中包含划定最大子数组边界的下标，以及该最大子数组中各值之和。第 1 行测试 base case（基本情况），即子数组只含一个元素的情形。只含一个元素的子数组只有一个子数组——它自身——因此第 2 行返回一个元组，其中包含这个唯一元素的起始与结束下标以及它的值。第 3–11 行处理 recursive case（递归情形）。第 3 行完成 divide（分解）部分，计算出中点下标 `mid`。我们把子数组 $A[\mathit{low}..\mathit{mid}]$ 称为 left subarray（左子数组），把 $A[\mathit{mid}+1..\mathit{high}]$ 称为 right subarray（右子数组）。因为我们知道子数组 $A[\mathit{low}..\mathit{high}]$ 至少包含两个元素，所以左子数组与右子数组各自都至少含有一个元素。第 4–5 行通过递归地在左、右子数组中分别寻找最大子数组来完成 conquer（解决）步骤。第 6–11 行构成 combine（合并）部分。第 6 行寻找一个跨越中点的最大子数组。（回想一下，由于第 6 行求解的子问题并不是原问题的更小实例，我们把它归入合并部分。）第 7 行测试左子数组是否包含具有最大和的子数组，若是，则第 8 行返回该最大子数组。否则，第 9 行测试右子数组是否包含具有最大和的子数组，若是，则第 10 行返回该最大子数组。如果左、右子数组都不包含取得最大和的子数组，那么最大子数组必定跨越中点，第 11 行返回它。

### Analyzing the divide-and-conquer algorithm（分析分治算法） <span style="color:#2471a3;">**[section]**</span>

接下来我们建立一个 recurrence（递归式），用它来描述递归过程 FIND-MAXIMUM-SUBARRAY 的 running time（运行时间）。与我们在 Section 2.3.2 中分析 merge sort（归并排序）时所做的一样，我们做一个简化假设：原问题的规模是 2 的幂，从而所有 subproblem（子问题）的规模都是整数。我们用 $T(n)$ 表示 FIND-MAXIMUM-SUBARRAY 在 $n$ 个元素的子数组上的运行时间。首先，第 1 行需要 constant time（常量时间）。当 $n = 1$ 时的基本情况很简单：第 2 行只需常量时间，因此

```math
T(1) = \Theta(1). \tag{4.5}
```

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.74</span>

### Section 4.1 · The maximum-subarray problem（最大子数组问题）（续）

（承上页）recursive case（递归情形）发生在 $n > 1$ 时。第 1 行与第 3 行只需常量时间。第 4、5 行求解的每个子问题都作用在含 $n/2$ 个元素的子数组上（我们关于原问题规模是 2 的幂的假设保证了 $n/2$ 是整数），因此求解其中每一个都花费 $T(n/2)$ 时间。因为我们必须求解两个子问题——左子数组与右子数组各一个——所以第 4、5 行对运行时间的贡献共计 $2T(n/2)$。如前所述，第 6 行对 FIND-MAX-CROSSING-SUBARRAY 的调用需要 $\Theta(n)$ 时间。第 7–11 行只需 $\Theta(1)$ 时间。因此，对于递归情形，我们有

```math
\begin{aligned}
T(n) &= \Theta(1) + 2T(n/2) + \Theta(n) + \Theta(1) \\
     &= 2T(n/2) + \Theta(n).
\end{aligned} \tag{4.6}
```

把等式 (4.5) 与 (4.6) 结合起来，我们就得到 FIND-MAXIMUM-SUBARRAY 的运行时间 $T(n)$ 的递归式：

```math
T(n) =
\begin{cases}
\Theta(1) & \text{if } n = 1, \\
2T(n/2) + \Theta(n) & \text{if } n > 1.
\end{cases} \tag{4.7}
```

这个递归式与 merge sort（归并排序）的递归式 (4.1) 相同。正如我们将在 Section 4.5 的 master method（主方法）中看到的那样，该递归式的解为 $T(n) = \Theta(n \lg n)$。你也可以重新审视 Figure 2.5 中的 recursion tree（递归树），来理解为什么这个解应当是 $T(n) = \Theta(n \lg n)$。

于是我们看到，divide-and-conquer（分治法）方法得到的算法在渐近意义上快于 brute-force（暴力法）方法。通过 merge sort 以及现在的 maximum-subarray problem（最大子数组问题），我们开始体会到分治法的强大威力。有时它会给出某个问题渐近最快的算法，而有时我们还能做得更好。正如 Exercise 4.1-5 所表明的，事实上存在求解最大子数组问题的 linear-time（线性时间）算法，而且它并不使用分治法。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 给分治算法记"代价账本"是分析一切分治的通用模板，本题三笔账：divide（分解）只算下标，$\Theta(1)$；conquer（解决）是两次递归，$2T(n/2)$；combine（合并）是 FIND-MAX-CROSSING-SUBARRAY 的线性扫描，$\Theta(n)$——合计 $T(n)=2T(n/2)+\Theta(n)$，与归并排序的账本逐项同构，答案自然也是 $\Theta(n\lg n)$。注意"跨中点"设计的巧妙之处：跨越中点的子数组必由"含 $A[\mathit{mid}]$ 的左段"与"含 $A[\mathit{mid}+1]$ 的右段"拼成，两段各自独立扫描、再相加即可——它把一个看似要暴力枚举 $\Theta(n^2)$ 段的问题，重组成了"可合并子结构"，这正是线性合并成为可能的原因。递归树视角同样清晰：每层合并代价合计 $\Theta(n)$，共 $\lg n$ 层，乘积为 $n\lg n$。以后遇到任何分治题，先问三个数：分摊多少、递归几个、合并多贵；账本一立，递归式自现。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**4.1-1**

What does FIND-MAXIMUM-SUBARRAY return when all elements of A are negative?

**4.1-2**

Write pseudocode for the brute-force method of solving the maximum-subarray problem. Your procedure should run in $\Theta(n^2)$ time.

**4.1-3**

Implement both the brute-force and recursive algorithms for the maximum-subarray problem on your own computer. What problem size $n_0$ gives the crossover point at which the recursive algorithm beats the brute-force algorithm? Then, change the base case of the recursive algorithm to use the brute-force algorithm whenever the problem size is less than $n_0$. Does that change the crossover point?

**4.1-4**

Suppose we change the definition of the maximum-subarray problem to allow the result to be an empty subarray, where the sum of the values of an empty subar

---

> <span style="color:#7f8c8d;">CLRS §4.1–4.2, p.75</span>

### Section 4.1 · Exercises（习题）（续） <span style="color:#2471a3;">**[exercise]**</span>

**4.1-4**（承上页）

ray is 0. How would you change any of the algorithms that do not allow empty subarrays to permit an empty subarray to be the result?

**4.1-5**

Use the following ideas to develop a nonrecursive, linear-time algorithm for the maximum-subarray problem. Start at the left end of the array, and progress toward the right, keeping track of the maximum subarray seen so far. Knowing a maximum subarray of $A[1..j]$, extend the answer to find a maximum subarray ending at index $j + 1$ by using the following observation: a maximum subarray of $A[1..j+1]$ is either a maximum subarray of $A[1..j]$ or a subarray $A[i..j+1]$, for some $1 \le i \le j + 1$. Determine a maximum subarray of the form $A[i..j+1]$ in constant time based on knowing a maximum subarray ending at index $j$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道习题指向著名的 Kadane 算法：从左到右扫一遍，维护"以当前位置结尾的最大子数组和"，每读一个元素要么把它接到之前的最大尾巴上，要么另起炉灶，全程 $O(n)$。据 Jon Bentley《编程珠玑》的记述，问题由统计学家 Ulf Grenander 提出、Kadane 在 1984 年给出线性解法。题目中"由 $A[1..j]$ 的答案推出 $A[1..j+1]$ 的答案"正是 dynamic programming（动态规划）的最优子结构思想——按规模从小到大递推，每个子问题只解一次；这是你将在第 14 章系统学到的范式。更有启发的是本节内部的对比：分治给出 $\Theta(n\lg n)$，说明"递归能榨的"已被榨干，再往下的改进要换范式——从"分而治之"切换到"增量维护"，而不是继续在递归里抠常数。识别"分治已到顶、该换动态规划"的时机，是算法设计里比记住公式更值钱的判断力。

### Section 4.2 · Strassen's algorithm for matrix multiplication（Strassen 矩阵乘法算法） <span style="color:#2471a3;">**[section]**</span>

如果你以前见过 matrices（矩阵），那么你很可能知道如何将它们相乘。（否则，你应当阅读 Appendix D（附录 D）中的 Section D.1。）若 $A = (a_{ij})$ 与 $B = (b_{ij})$ 是 $n \times n$ 的 square matrix（方阵），那么在乘积 $C = A \cdot B$ 中，我们对每个 $i, j = 1, 2, \ldots, n$ 定义 entry（元素）$c_{ij}$ 为

```math
c_{ij} = \sum_{k=1}^{n} a_{ik} \cdot b_{kj}. \tag{4.8}
```

我们必须计算 $n^2$ 个矩阵元素，而每个元素都是 $n$ 个值之和。下面的过程接收两个 $n \times n$ 矩阵 $A$ 与 $B$，将它们相乘，并返回它们的 $n \times n$ 乘积 $C$。我们假设每个矩阵都有一个 attributes（属性）rows，给出矩阵的行数。

```
SQUARE-MATRIX-MULTIPLY(A, B)
1  n = A.rows
2  let C be a new n × n matrix
3  for i = 1 to n
4      for j = 1 to n
5          c_ij = 0
6          for k = 1 to n
7              c_ij = c_ij + a_ik · b_kj
8  return C
```

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.76</span>

### Section 4.2 · Strassen's algorithm for matrix multiplication（Strassen 矩阵乘法算法）（续）

SQUARE-MATRIX-MULTIPLY 过程的工作方式如下。第 3–7 行的 for 循环计算第 $i$ 行的各个元素，而在给定行 $i$ 之内，第 4–7 行的 for 循环对每一列 $j$ 计算各元素 $c_{ij}$。第 5 行在我们开始计算等式 (4.8) 给出的和时将 $c_{ij}$ 初始化为 0，而第 6–7 行的 for 循环的每次迭代都向其中加入等式 (4.8) 的又一项。由于三重嵌套的 for 循环中的每一个都恰好执行 $n$ 次迭代，且第 7 行的每次执行只需 constant time（常量时间），所以 SQUARE-MATRIX-MULTIPLY 过程需要 $\Theta(n^3)$ 时间。

你也许一开始会认为，任何 matrix multiplication（矩阵乘法）算法都必须耗费 $\Omega(n^3)$ 时间，因为矩阵乘法的自然定义就需要这么多次 multiplications（乘法）。然而你错了：我们有一种办法可以在 $o(n^3)$ 时间内完成矩阵相乘。在本节中，我们将看到 Strassen 出色的递归算法，用于 $n \times n$ 矩阵相乘。它的运行时间为 $\Theta(n^{\lg 7})$，我们将在 Section 4.5 中加以证明。由于 $\lg 7$ 介于 2.80 与 2.81 之间，Strassen 算法的运行时间为 $O(n^{2.81})$，渐近优于简单的 SQUARE-MATRIX-MULTIPLY 过程。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 据离线维基百科：Strassen 算法由德国数学家 Volker Strassen（1936 年生）于 1969 年发表，第一次证明朴素矩阵乘法的 $n^3$ 并非最优——这在当时震动学界，因为"矩阵乘法需要 $n^3$ 次标量乘法"曾被默认为问题的天然下界。有趣的是，Strassen 的学术出身是概率论（他 1964 年的不变原理论文至今是经典），矩阵乘法只是他跨界的战果之一；此后他与 Schönhage 提出大数乘法的 Schönhage–Strassen 算法（1971 年），与 Solovay 提出随机素性检测的 Solovay–Strassen 测试（1977 年），并因这一系列贡献于 2009 年获 Knuth Prize。他的动机颇具第一性原理味道：既然没人证明过 $\Omega(n^3)$ 下界，"显然"的 $n^3$ 也许就没那么紧——这与 Karatsuba 一周内推翻 Kolmogorov 的 $\Omega(n^2)$ 大数乘法猜想（1960 年）如出一辙。"下界未证，就不必信"，是复杂度研究反复上演的剧本。

### A simple divide-and-conquer algorithm（一个简单的分治算法） <span style="color:#2471a3;">**[section]**</span>

为简单起见，当我们用 divide-and-conquer（分治法）算法计算矩阵乘积 $C = A \cdot B$ 时，假设每个 $n \times n$ 矩阵中的 $n$ 都恰好是 2 的幂。之所以做这个假设，是因为在每个 divide（分解）步骤中，我们都要把 $n \times n$ 矩阵划分成四个 $n/2 \times n/2$ 矩阵；通过假设 $n$ 恰为 2 的幂，我们就能保证只要 $n \ge 2$，维数 $n/2$ 就是整数。

假设我们把 $A$、$B$、$C$ 各自 partition（划分）为四个 $n/2 \times n/2$ 矩阵：

```math
A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \quad
B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}, \quad
C = \begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix}, \tag{4.9}
```

于是可以把等式 $C = A \cdot B$ 改写为

```math
\begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} =
\begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}
\cdot
\begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}. \tag{4.10}
```

等式 (4.10) 对应于如下四个等式：

```math
C_{11} = A_{11} \cdot B_{11} + A_{12} \cdot B_{21}, \tag{4.11}
```

```math
C_{12} = A_{11} \cdot B_{12} + A_{12} \cdot B_{22}, \tag{4.12}
```

```math
C_{21} = A_{21} \cdot B_{11} + A_{22} \cdot B_{21}, \tag{4.13}
```

```math
C_{22} = A_{21} \cdot B_{12} + A_{22} \cdot B_{22}. \tag{4.14}
```

这四个等式中的每一个都指明了两次 $n/2 \times n/2$ 矩阵的 multiplication（乘法），以及它们的 $n/2 \times n/2$ 乘积之间的 matrix addition（矩阵加法）。我们可以利用这些等式构造一个直观的、递归的分治算法：

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.77</span>

### Section 4.2 · Strassen's algorithm for matrix multiplication（Strassen 矩阵乘法算法）（续）

```
SQUARE-MATRIX-MULTIPLY-RECURSIVE(A, B)
 1  n = A.rows
 2  let C be a new n × n matrix
 3  if n == 1
 4      c_11 = a_11 · b_11
 5  else partition A, B, and C as in equations (4.9)
 6      C_11 = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_11, B_11)
             + SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_12, B_21)
 7      C_12 = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_11, B_12)
             + SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_12, B_22)
 8      C_21 = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_21, B_11)
             + SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_22, B_21)
 9      C_22 = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_21, B_12)
             + SQUARE-MATRIX-MULTIPLY-RECURSIVE(A_22, B_22)
10  return C
```

这段 pseudocode（伪代码）掩盖了一个微妙却重要的实现细节：第 5 行如何划分这些矩阵？如果我们要创建 12 个新的 $n/2 \times n/2$ 矩阵，就会耗费 $\Theta(n^2)$ 时间来 copying（复制）元素。事实上，我们可以不复制任何元素就完成划分。诀窍是使用 index calculation（下标计算）：我们用原矩阵的一段行下标范围和一段列下标范围来标识一个 submatrix（子矩阵）。这样，我们最终表示子矩阵的方式与表示原矩阵的方式会略有不同，而这正是我们在此一笔带过的微妙之处。这样做的好处是，既然可以通过下标计算来指定子矩阵，执行第 5 行就只需 $\Theta(1)$ 时间（不过我们将会看到，无论复制还是原地划分，对整体运行时间在渐近意义上并无影响）。

现在，我们推导一个 recurrence（递归式）来刻画 SQUARE-MATRIX-MULTIPLY-RECURSIVE 的 running time（运行时间）。设 $T(n)$ 为用这一过程相乘两个 $n \times n$ 矩阵所需的时间。在 base case（基本情况）中，当 $n = 1$ 时，我们只执行第 4 行的一次 scalar multiplication（标量乘法），因此

```math
T(1) = \Theta(1). \tag{4.15}
```

recursive case（递归情形）发生在 $n > 1$ 时。如前所述，利用下标计算，第 5 行对矩阵的 partition（划分）只需 $\Theta(1)$ 时间。在第 6–9 行中，我们总共递归调用 SQUARE-MATRIX-MULTIPLY-RECURSIVE 八次。由于每次递归调用相乘两个 $n/2 \times n/2$ 矩阵，从而对总运行时间贡献 $T(n/2)$，所以八次递归调用花费的总时间为 $8T(n/2)$。我们还必须计入第 6–9 行中的四次 matrix addition（矩阵加法）。每个这样的矩阵包含 $n^2/4$ 个元素，因此这四次矩阵加法中的每一次都需要 $\Theta(n^2)$ 时间。由于矩阵加法的次数是常量，所以花在矩阵加法上的总时间为……（承下页）

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.78</span>

（接上页）……对 submatrices（子矩阵）做加法——即第 6–9 行——所需时间为 $\Theta(n^2)$。（再次地，我们用 index calculation（下标计算）把矩阵加法的结果放进矩阵 $C$ 的正确位置，每个 entry（条目）的 overhead（开销）为 $\Theta(1)$ 时间。）因此，recursive case（递归情形）的总时间，就是 partitioning time（划分时间）、所有 recursive calls（递归调用）的时间，以及对递归调用所得矩阵做加法的时间之和：

```math
T(n) = \Theta(1) + 8T(n/2) + \Theta(n^2) = 8T(n/2) + \Theta(n^2). \tag{4.16}
```

注意，如果我们改为通过 copying（复制）矩阵来实现划分——这需要耗费 $\Theta(n^2)$ 时间——recurrence（递归式）并不会因此改变，所以 overall running time（总运行时间）只会增加一个 constant factor（常数因子）。

联立 equation（方程）(4.15) 与 (4.16)，就得到 SQUARE-MATRIX-MULTIPLY-RECURSIVE 的 running time（运行时间）所满足的递归式：

```math
T(n) =
\begin{cases}
\Theta(1) & \text{if } n = 1, \\
8T(n/2) + \Theta(n^2) & \text{if } n > 1.
\end{cases}
\tag{4.17}
```

正如我们将在 Section 4.5 的 master method（主方法）中看到的，递归式 (4.17) 的解为 $T(n) = \Theta(n^3)$。因此，这种简单的 divide-and-conquer（分治法）方法并不比直截了当的 SQUARE-MATRIX-MULTIPLY 过程更快。

在继续考察 Strassen's algorithm（Strassen 算法）之前，让我们先回顾一下 equation (4.16) 的各个组成部分是如何得来的。通过下标计算来划分每个 $n \times n$ 矩阵需要 $\Theta(1)$ 时间，但我们要划分的是两个矩阵。虽然你可以说划分这两个矩阵需要 $\Theta(2)$ 时间，但常数 2 已被 Θ-notation（Θ 记号）涵盖（subsume）。两个矩阵相加，设每个矩阵有 $k$ 个 entries（条目），需要 $\Theta(k)$ 时间。由于我们相加的每个矩阵各有 $n^2/4$ 个条目，你可以说每对矩阵相加需要 $\Theta(n^2/4)$ 时间。同样，Θ 记号涵盖了常数因子 $1/4$，于是我们说两个 $n/2 \times n/2$ 矩阵相加需要 $\Theta(n^2)$ 时间。我们有 4 个这样的矩阵加法，我们不再说它们需要 $\Theta(4n^2)$ 时间，而是说它们需要 $\Theta(n^2)$ 时间。（当然，你可能会注意到，我们本可以说这 4 个矩阵加法需要 $\Theta(4n^2/4)$ 时间，而 $4n^2/4 = n^2$；但这里的要点在于：Θ 记号涵盖的是常数因子，无论它是多少。）这样，我们最终得到两个 $\Theta(n^2)$ 项，并可以把它们合并为一项。

然而，当我们考虑 8 个 recursive calls（递归调用）时，就不能仅仅把常数因子 8 涵盖掉了。换言之，我们必须说它们合计需要 $8T(n/2)$ 时间，而不能只说 $T(n/2)$ 时间。回顾 Figure 2.5 中 recurrence（递归式）(2.1)（它与递归式 (4.7) 完全相同，递归情形为 $T(n) = 2T(n/2) + \Theta(n)$）的 recursion tree（递归树），你就能体会其中的原因：因子 2 决定了每个树结点有多少个 children（孩子），而这又决定了树的每一层有多少项贡献到总和之中。如果我们忽略了……（下页继续）

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.79</span>

（接上页）……equation（方程）(4.16) 中的因子 8 或递归式 (4.1) 中的因子 2，那么 recursion tree（递归树）就只会是 linear（线性的），而不是"枝繁叶茂"的（bushy），并且每一层只会给总和贡献一项。

因此请牢记：尽管 asymptotic notation（渐近记号）会涵盖常数乘积因子，但诸如 $T(n/2)$ 这样的 recursive notation（递归记号）却不会。

### Strassen's method（Strassen 方法）

Strassen 方法的关键在于让递归树稍微不那么"枝繁叶茂"。也就是说，它不再对 $n/2 \times n/2$ 矩阵执行 8 次 recursive multiplication（递归乘法），而是只执行 7 次。省去一次 matrix multiplication（矩阵乘法）的代价，是若干次新的 $n/2 \times n/2$ 矩阵加法，但加法的次数仍然只是常数次。与之前一样，当我们建立 recurrence equation（递归方程）来刻画 running time（运行时间）时，这个常数次数的矩阵加法会被 Θ-notation（Θ 记号）所涵盖。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Strassen 方法的本质一句话：用加减法换乘法。把 $8T(n/2)$ 砍成 $7T(n/2)$，指数从 $\lg 8=3$ 降到 $\lg 7\approx 2.81$，代价是多做常数次加减（第 2 步 10 个 $S_i$、第 4 步 8 次组合），好在矩阵加法只要 $\Theta(n^2)$，渐近上被 Θ 记号吸收。为什么这笔交易划算？因为对大矩阵，乘法比加法贵一个数量级以上：硬件上乘法器的延迟远长于加法器，标量乘法的位操作规模也远大于加法。这与 Karatsuba 大数乘法（1960 年发现、1962 年发表，用 3 次子乘法代替朴素的 4 次，递归后达到 $n^{\lg 3}\approx n^{1.58}$）是同一个思想家族：分治递归对"递归调用次数" $a$ 呈指数级敏感，砍一次乘法收益是整个指数的下降，而多做的加法只进常数项。通用教训：在 $aT(n/b)+f(n)$ 型递归里，$a$ 是指数上的钉子，$f(n)$ 只是被 Θ 吸收的地板——优化永远优先瞄准 $a$。

Strassen's method（Strassen 方法）一点也不显而易见。（这也许是本书中最大的 understatement（轻描淡写）。）它包含 4 个步骤：

1. 将输入矩阵 $A$、$B$ 和输出矩阵 $C$ 划分为 $n/2 \times n/2$ 的 submatrices（子矩阵），如 equation (4.9) 所示。与 SQUARE-MATRIX-MULTIPLY-RECURSIVE 中一样，这一步通过下标计算只需 $\Theta(1)$ 时间。
2. 创建 10 个矩阵 $S_1, S_2, \ldots, S_{10}$，每个都是 $n/2 \times n/2$ 的，且都是第 1 步所创建矩阵的和或差。我们可以在 $\Theta(n^2)$ 时间内创建出全部 10 个矩阵。
3. 利用第 1 步创建的子矩阵与第 2 步创建的 10 个矩阵，递归地计算 7 个矩阵积 $P_1, P_2, \ldots, P_7$。每个矩阵 $P_i$ 都是 $n/2 \times n/2$ 的。
4. 通过对各个 $P_i$ 矩阵进行加减组合，计算出结果矩阵 $C$ 所需的子矩阵 $C_{11}, C_{12}, C_{21}, C_{22}$。我们可以在 $\Theta(n^2)$ 时间内计算出全部 4 个子矩阵。

我们稍后就会看到第 2–4 步的细节，但仅凭以上信息，我们已经足以建立 Strassen 方法的运行时间递归式。假设当矩阵规模 $n$ 降到 1 时，我们执行一次简单的 scalar multiplication（标量乘法），就像 SQUARE-MATRIX-MULTIPLY-RECURSIVE 的第 4 行那样。当 $n > 1$ 时，第 1、2、4 步总共需要 $\Theta(n^2)$ 时间，而第 3 步要求我们执行 7 次 $n/2 \times n/2$ 矩阵乘法。于是，我们得到 Strassen's algorithm（Strassen 算法）运行时间 $T(n)$ 的如下递归式：

```math
T(n) =
\begin{cases}
\Theta(1) & \text{if } n = 1, \\
7T(n/2) + \Theta(n^2) & \text{if } n > 1.
\end{cases}
\tag{4.18}
```

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.80</span>

我们用一次矩阵乘法换来了常数次数的矩阵加法——这就是一次 tradeoff（权衡）。一旦我们理解了 recurrence（递归式）及其解，就会看到这种权衡实际上带来了更低的渐近运行时间（asymptotic running time）。根据 Section 4.5 的 master method（主方法），recurrence (4.18) 的解为 $T(n) = \Theta(n^{\lg 7})$。

现在我们来描述细节。在第 2 步中，我们创建如下 10 个矩阵：

```math
\begin{aligned}
S_1 &= B_{12} - B_{22}, & S_2 &= A_{11} + A_{12}, & S_3 &= A_{21} + A_{22}, \\
S_4 &= B_{21} - B_{11}, & S_5 &= A_{11} + A_{22}, & S_6 &= B_{11} + B_{22}, \\
S_7 &= A_{12} - A_{22}, & S_8 &= B_{21} + B_{22}, & S_9 &= A_{11} - A_{21}, \\
S_{10} &= B_{11} + B_{12}.
\end{aligned}
```

由于我们必须做 10 次 $n/2 \times n/2$ 矩阵的加法或减法，这一步确实需要 $\Theta(n^2)$ 时间。

在第 3 步中，我们递归地把 $n/2 \times n/2$ 矩阵乘法执行 7 次，计算出下列 $n/2 \times n/2$ 矩阵；其中每个矩阵都是 $A$ 与 $B$ 的子矩阵乘积的和或差：

```math
\begin{aligned}
P_1 &= A_{11} \cdot S_1 &&= A_{11} \cdot B_{12} - A_{11} \cdot B_{22}, \\
P_2 &= S_2 \cdot B_{22} &&= A_{11} \cdot B_{22} + A_{12} \cdot B_{22}, \\
P_3 &= S_3 \cdot B_{11} &&= A_{21} \cdot B_{11} + A_{22} \cdot B_{11}, \\
P_4 &= A_{22} \cdot S_4 &&= A_{22} \cdot B_{21} - A_{22} \cdot B_{11}, \\
P_5 &= S_5 \cdot S_6 &&= A_{11} \cdot B_{11} + A_{11} \cdot B_{22} + A_{22} \cdot B_{11} + A_{22} \cdot B_{22}, \\
P_6 &= S_7 \cdot S_8 &&= A_{12} \cdot B_{21} + A_{12} \cdot B_{22} - A_{22} \cdot B_{21} - A_{22} \cdot B_{22}, \\
P_7 &= S_9 \cdot S_{10} &&= A_{11} \cdot B_{11} + A_{11} \cdot B_{12} - A_{21} \cdot B_{11} - A_{21} \cdot B_{12}.
\end{aligned}
```

注意，我们需要执行的乘法只是上述方程中间一列的那些。右列只是表明：用第 1 步创建的原始子矩阵来看，这些乘积各等于什么。

第 4 步对第 3 步创建的各个 $P_i$ 矩阵进行加减，构造出乘积 $C$ 的 4 个 $n/2 \times n/2$ 子矩阵。我们从下式开始：

```math
C_{11} = P_5 + P_4 - P_2 + P_6.
```

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.81</span>

把右端展开——每个 $P_i$ 的展开各占一行，并把相互抵消的项垂直对齐——我们可以看到，$C_{11}$ 等于

```math
\begin{aligned}
&\ A_{11} \cdot B_{11} + A_{11} \cdot B_{22} + A_{22} \cdot B_{11} + A_{22} \cdot B_{22} \\
&\quad - A_{22} \cdot B_{11} + A_{22} \cdot B_{21} \\
&\quad - A_{11} \cdot B_{22} - A_{12} \cdot B_{22} \\
&\quad - A_{22} \cdot B_{22} - A_{22} \cdot B_{21} + A_{12} \cdot B_{22} + A_{12} \cdot B_{21} \\[4pt]
=\ &A_{11} \cdot B_{11} + A_{12} \cdot B_{21},
\end{aligned}
```

它对应 equation（方程）(4.11)。

类似地，我们令

```math
C_{12} = P_1 + P_2,
```

于是 $C_{12}$ 等于

```math
\begin{aligned}
&\ A_{11} \cdot B_{12} - A_{11} \cdot B_{22} \\
&\quad + A_{11} \cdot B_{22} + A_{12} \cdot B_{22} \\[4pt]
=\ &A_{11} \cdot B_{12} + A_{12} \cdot B_{22},
\end{aligned}
```

对应 equation (4.12)。

令

```math
C_{21} = P_3 + P_4
```

使 $C_{21}$ 等于

```math
\begin{aligned}
&\ A_{21} \cdot B_{11} + A_{22} \cdot B_{11} \\
&\quad - A_{22} \cdot B_{11} + A_{22} \cdot B_{21} \\[4pt]
=\ &A_{21} \cdot B_{11} + A_{22} \cdot B_{21},
\end{aligned}
```

对应 equation (4.13)。

最后，我们令

```math
C_{22} = P_5 + P_1 - P_3 - P_7,
```

使得 $C_{22}$ 等于

```math
\begin{aligned}
&\ A_{11} \cdot B_{11} + A_{11} \cdot B_{22} + A_{22} \cdot B_{11} + A_{22} \cdot B_{22} \\
&\quad - A_{11} \cdot B_{22} + A_{11} \cdot B_{12} \\
&\quad - A_{22} \cdot B_{11} - A_{21} \cdot B_{11} \\
&\quad - A_{11} \cdot B_{11} - A_{11} \cdot B_{12} + A_{21} \cdot B_{11} + A_{21} \cdot B_{12} \\[4pt]
=\ &A_{22} \cdot B_{22} + A_{21} \cdot B_{12},
\end{aligned}
```

---

> <span style="color:#7f8c8d;">CLRS §4.2, p.82</span>

（接上页）……它对应 equation（方程）(4.14)。总之，在第 4 步中我们对 $n/2 \times n/2$ 矩阵做加法或减法共 8 次，因此这一步确实需要 $\Theta(n^2)$ 时间。

于是我们看到，由第 1–4 步组成的 Strassen's algorithm（Strassen 算法）能产生正确的矩阵乘积，并且 recurrence（递归式）(4.18) 刻画了它的 running time（运行时间）。由于我们将在 Section 4.5 中看到该递归式的解为 $T(n) = \Theta(n^{\lg 7})$，所以 Strassen's method（Strassen 方法）在渐近意义上比直截了当的 SQUARE-MATRIX-MULTIPLY 过程更快。本章末尾的 notes（注释）会讨论 Strassen 算法的一些 practical aspects（实用方面）。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $\Theta(n^{\lg 7})$ 只是矩阵乘法"军备竞赛"的起点。据离线维基百科：Coppersmith 与 Winograd 在 1990 年用"算术级数"方法把指数降到 $O(n^{2.376})$；François Le Gall 在 2014 年给出 $O(n^{2.3728639})$；截至 2024 年，最佳纪录是 $O(n^{2.371339})$。但维基同时指出，这些后续算法几乎全是 galactic algorithm（银河系算法）：大 O 藏住的常数大得离谱，只有矩阵大到现实中根本造不出来时才比朴素算法快，因此工程上硬件友好的朴素算法与 Strassen 变体仍是主角。这场竞赛的镜像问题是：矩阵乘法究竟能否做到 $n^{2+\varepsilon}$（对任意 $\varepsilon>0$）？目前连"指数极限 $\omega=2$"这一猜想都未被证明或否定，而已知下界只有 $n$ 个输出条目给出的平凡 $\Omega(n^2)$。不妨把 $\lg 7\approx 2.81$ 记作历史坐标：1969 年之前是 3，此后人类一直在 2.37 附近压线。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

Note: Although Exercises 4.2-3, 4.2-4, and 4.2-5 are about variants on Strassen's algorithm, you should read Section 4.5 before trying to solve them.

**4.2-1**

Use Strassen's algorithm to compute the matrix product

```math
\begin{pmatrix} 1 & 3 \\ 7 & 5 \end{pmatrix}
\begin{pmatrix} 6 & 8 \\ 4 & 2 \end{pmatrix}.
```

Show your work.

**4.2-2**

Write pseudocode for Strassen's algorithm.

**4.2-3**

How would you modify Strassen's algorithm to multiply $n \times n$ matrices in which $n$ is not an exact power of 2? Show that the resulting algorithm runs in time $\Theta(n^{\lg 7})$.

**4.2-4**

What is the largest $k$ such that if you can multiply $3 \times 3$ matrices using $k$ multiplications (not assuming commutativity of multiplication), then you can multiply $n \times n$ matrices in time $o(n^{\lg 7})$? What would the running time of this algorithm be?

**4.2-5**

V. Pan has discovered a way of multiplying $68 \times 68$ matrices using 132,464 multiplications, a way of multiplying $70 \times 70$ matrices using 143,640 multiplications, and a way of multiplying $72 \times 72$ matrices using 155,424 multiplications. Which method yields the best asymptotic running time when used in a divide-and-conquer matrix-multiplication algorithm? How does it compare to Strassen's algorithm?
