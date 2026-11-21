# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk02 · 书页 43–82 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS Chapter 3, §3.1, p.43</span>

## Chapter 3（第 3 章）· Growth of Functions（函数的增长）

第 2 章中定义的算法 running time（运行时间）的 order of growth（增长阶数），给出了算法 efficiency（效率）的一种简单刻画，也让我们能够比较不同算法之间的相对 performance（性能）。一旦 input size（输入规模）$n$ 变得足够大，具有 $\Theta(n \lg n)$ 最坏情况运行时间的 merge sort（归并排序）就会胜过最坏情况运行时间为 $\Theta(n^2)$ 的 insertion sort（插入排序）。虽然我们有时能够确定一个算法的 exact running time（精确运行时间）——正如第 2 章对插入排序所做的那样——但为这点额外的 precision（精度）去付出计算代价通常并不值得。对于足够大的输入，精确运行时间中的 multiplicative constants（乘积常数）与 lower-order terms（低阶项）都会被输入规模自身的影响所支配。当我们考察那些大到使只有运行时间的增长阶数才相关的输入规模时，我们研究的就是算法的 asymptotic efficiency（渐近效率）。也就是说，我们关心的是：在输入规模无限增大的 limit（极限）意义下，算法的运行时间如何随输入规模的增大而增长。通常，一个在渐近意义上更高效的算法，对除极小输入之外的所有输入都会是最佳选择。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "为精确运行时间付出计算代价并不值得"这句话的正确读法是：我们主动放弃了函数取值这一层信息，只保留 order of growth（增长阶数）这一层，于是两个 running time（运行时间）函数之间的关系就不再是普通相等，而是"在 constant factor（常数因子）内是同一个东西"。这种"同一个东西"的严格说法就是 equivalence relation（等价关系），而 Θ-notation（Θ 记号）给出的正是它 —— 这才是它能当等号用的原因。
>
> 把定义摊开看：$f(n)=\Theta(g(n))$ 说的是存在正常数 $c_1$、$c_2$ 与 $n_0$，使 $n\ge n_0$ 时 $0\le c_1 g(n)\le f(n)\le c_2 g(n)$。要验证它是 equivalence relation（等价关系），三条性质都得从这串不等式里抠出来：自反性取 $c_1=c_2=1$、$n_0=1$ 即可；对称性只需把两个常数对调再取倒数，$1/c_1$、$1/c_2$ 仍是正常数，这一步正是定义里写"正的"常数的原因；传递性要把两对常数乘起来 —— 若 $f$ 被 $g$ 夹住、$g$ 又被 $h$ 夹住，则 $c_1c_1'h(n)\le f(n)\le c_2c_2'h(n)$，乘出来的仍是正常数。三条性质里唯一有技术含量的是传递性，而它的关键动作是乘法：只有乘法保证正常数集合封闭。
>
> 于是所有渐近非负的 running time（运行时间）函数被切成一个个 equivalence class（等价类）。取 $f(n)=n^2+3n$ 与 $g(n)=5n^2$ 试一下：$n=1000$ 处 $f=1003000$、$g=5000000$，比值 $0.2006$；$n=10$ 处比值 $0.26$。比值本身随 $n$ 变，却始终被正常数夹住不再跑掉 —— 这就是同类。直接给常数：$c_1=1$、$c_2=4$、$n_0=1$ 时 $n^2\le n^2+3n\le 4n^2$ 对一切 $n\ge 1$ 成立（右边等价于 $3n\le 3n^2$），逐点验算通过。
>
> 在这个视角下三个记号各就各位：O 只有自反性与传递性、没有对称性，所以它是 partial order（偏序）意义上的"$\le$"；Θ 是真正的"$=$"；o 扮演"$<$"，因为它额外要求比值趋于零。把"等价 / 序 / 严格序"这套骨架记住，后面遇到任何一条记号性质，都先问一句"它在实数比较里对应什么"，再回头用 $c_1$、$c_2$ 验证。
>
> 但 equivalence class（等价类）内部并非没有差别，工程上必须补这一句。取插入排序与归并排序的粗略模型：插入排序每对元素比一次、每单位代价 $5n^2$，归并排序每层扫一遍、代价约 $40n\lg n$。令两者相等得 $n=8\lg n$，交叉点在 $n=44$ 附近 —— 我逐点算过：$n=43$ 时 $9245$ 对 $9333$，二次算法仍占优，$n=44$ 时 $9680$ 对 $9608$ 才反超。也就是说 $n<44$ 时，被 Θ 判为更差的那个算法反而更快，因为常数 $5$ 与 $40$ 的差距还没被 $n$ 的增长抹平。
>
> 跨课程连接：CSAPP 第 6 章 cache（高速缓存）给的层级延迟是 L1 命中约 $4$ 个周期、DRAM 约 $200$ 个周期，差 $50$ 倍。在 Θ-notation（Θ 记号）眼里两者都是 $\Theta(1)$，因为 $50$ 是常数；可你写循环时命中率从 $0.99$ 掉到 $0.90$ 就能让总时间翻倍。类比成立的条件很具体：被吞掉的常数不随 $n$ 变化、且不跨越量级。区别在于 CSAPP 把这 $50$ 倍显式建模成 miss penalty（缺失代价）再按 AMAT（平均访存时间）加权，而这里只保证"存在某个常数"，不告诉你它是几：后者给普适性，前者给可预测性。
>
> 所以"不值得算精确运行时间"不是懒惰，而是一次有意识的抽象：换掉函数取值、保留增长阶数，代价是把同一 equivalence class（等价类）内部的常数差异藏起来，收益是让比较变得可判定、可传递。要小心的只有一件事 —— 当 $n$ 落在交叉点附近，或者常数差了 $50$ 倍时，等价类内部的次序才是决定胜负的东西。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把这个证明提炼成可复用的模板，命名为「常数对 $c_1$、$c_2$ 夹逼」，但模板的价值不在三步本身，而在三步之间的依赖顺序：先把 $n_0$ 钉住，$c_1$ 与 $c_2$ 才有可行域；反过来先猜常数再找 $n_0$，等于在没有定义域的式子上解不等式。
>
> 机制值得逐句拆。除以 $n^2$ 之后，原来的三方夹逼变成 $c_1\le\frac12-\frac3n\le c_2$，中间那个量是关于 $n$ 的单调函数，一端趋于 $\frac12$、另一端在 $n$ 小时趋于负无穷。于是上界一侧几乎白送：取 $c_2=\frac12$，右边对一切 $n\ge 1$ 成立，因为减项只会把左边拉小。真正的战场在下界一侧：减项把函数往下拉，你必须在一个"足够大"的 $n$ 之后才开始估，这就是 $n_0$ 必须先进场的原因。$c_1=\frac1{14}$ 正是把 $n\ge 7$ 代入所得的下确界 $\frac12-\frac37$，它不是猜出来的，是被 $n_0$ 算出来的。
>
> 换一组数字把这个依赖关系走一遍。取 $f(n)=3n^2-20n+5$，先问 $f$ 何时非负：解 $3n^2-20n+5\ge 0$ 得 $n\ge 6.41$，所以 $n_0$ 至少要取 $7$，否则 $f$ 为负、下界不等式的左边根本不可能成立。取 $n_0=7$ 时比值 $f(n)/n^2=3-\frac{20}{7}+\frac{5}{49}=0.245$，于是 $c_1\le 0.245$；取宽松些的 $n_0=20$ 则比值升到 $2.0125$，可以干净地取 $c_1=2$、$c_2=3$。我逐点验算过 $n=20$ 到 $199$ 全部落在 $[2,3]$ 内：$n=50$ 处 $2.602$，$n=1000$ 处 $2.980$，确实向 $3$ 爬而不再回头。
>
> 如果偷懒把 $n_0$ 取成 $4$ 会怎样？比值 $3-5+0.3125=-1.6875$，$f$ 本身是负数，无论 $c_1$ 取多小都凑不出 $c_1n^2\le f(n)$ —— 这正是"先定 $n_0$ 后解 $c_1$"的实证，而不是一句口头纪律。同理，$c_2$ 之所以好找，是因为 $f$ 的首项系数天然就是天花板，你只要取略大一点的常数即可；功夫全在吞掉那个负的低阶项上。
>
> 还有一个反直觉的副产品：$n_0$ 取得越大，$c_1$ 的可行域反而越宽。比较三个选择：$n_0=7$ 时下确界 $0.245$，$n_0=20$ 时 $2.013$，$n_0=100$ 时 $2.8005$。也就是说，你可以用"更弱的陈述"（只在更远处成立）换"更好的常数"。这在工程上直接对应一件事：谈论常数因子时必须同时说清在什么规模区间，脱离 $n_0$ 谈常数没有意义。
>
> 把这套模板用到任意 $d$ 次多项式 $p(n)=\sum a_in^i$（要求 $a_d>0$）时，动作一字不改：先解 $p(n)\ge 0$ 得到非负门槛，再在某处读出 $p(n)/n^d$ 的下确界当 $c_1$，最后取 $c_2$ 略大于 $a_d$。书上给 $c_1=a/4$、$c_2=7a/4$、$n_0=2\max(|b|/a,\sqrt{|c|/a})$ 只是这套动作在二次情形的一次具体取值，不是唯一答案 —— 换成 $c_1=a/3$，只要把 $n_0$ 再推远一点照样成立。
>
> 跨课程连接：CSAPP 第 6 章讲 cache（高速缓存）时用的 memory mountain（内存山）实验，本质是同一套夹逼 —— 同一段代码在不同工作集大小下的每字节成本，先被 L1 的下界压住，再被 DRAM 的上界托住，中间的过渡区由工作集与容量的比值决定。类比成立是因为两边都在"用两个常数夹住一个随规模变化的量"；区别在于 CSAPP 的常数是硬件测出来的、随机器变，而这里的常数只需存在、不必知道数值。另一个锚点是 6.042J 的不等式放缩：那里你练的是"把式子放大到好算"，这里练的是"把式子放大到一个常数"，手法同源。
>
> 所以以后遇到任何 Θ 验证题，包括下方二次函数与 Problem 3-1 的 $d$ 次多项式，动作顺序都固定：先确认非负门槛给出 $n_0$ 的下限，再在选定的 $n_0$ 处读出比值的下确界当 $c_1$，最后取首项系数略上方当 $c_2$。把构造常数当成解不等式，就没有"猜数字"这一说了。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "O 与 Ω 拼起来就是 Θ"看起来是同义反复，其实它的每一半都依赖定义里那两个容易被当成装饰的条件：常数必须为正、函数必须渐近非负。定理本身不难，难的是看清哪条前提在某一步放缩里真的被用到了 —— 这才是"先证后信"的意思。
>
> 先把量词摆正。$f=\Theta(g)$ 给的是"存在 $c_1,c_2,n_0$ 使三方夹逼成立"，$f=O(g)$ 给的是"存在 $c,n_0$ 使上方不等式成立"，$f=\Omega(g)$ 给的是"存在 $c,n_0$ 使下方不等式成立"。从左推右只需把同一个 $c_1$、$c_2$ 分别当作两个单边常数交出去，$n_0$ 也照抄。从右推左则要做一次合并：$O$ 侧给的 $n_0'$ 与 Ω 侧给的 $n_0''$ 可能不同，取两者较大者，两个不等式就在同一条射线上同时成立，再令 $c_1$ 取自 Ω 侧、$c_2$ 取自 O 侧即可。整个证明的技术内容只有"取 max"这一个动作，但缺了它，两个界就不在同一定义域上。
>
> 现在用反例检验前提为什么必需。考察线性函数 $an+b$，若允许 $a=0$，它退化为常数 $b$；对 $g(n)=n$，Ω 侧要求 $b\ge cn$ 对一切 $n\ge n_0$ 成立，给定任意 $c>0$ 只需取 $n>b/c$ 就失败，下界一侧直接崩塌，$\Theta(n)$ 的断言随之失效。再看渐近非负：定义里写的是 $0\le c_1g(n)\le f(n)$，若 $f$ 取负值，左边那个 $0\le f(n)$ 根本无从谈起，集合 $\Theta(g(n))$ 就成了空集 —— 这正是为什么全书约定凡进 Θ 的函数渐近非负。
>
> 给一个能算的核对：$f(n)=3n+7$ 与 $g(n)=n$。O 侧取 $c=10$、$n_0=1$：$3n+7\le 10n$ 等价于 $7\le 7n$，成立。Ω 侧取 $c=3$：$3n+7\ge 3n$ 恒成立。两侧都有，于是 $f=\Theta(n)$。把这个例子的系数改成零：$f(n)=5$，则 $5\le 5n$ 说明 $5=O(n)$，但 $5=\Omega(n)$ 不成立 —— 假设存在 $c>0$，取 $n=\max(n_0,\lceil 6/c\rceil)$ 就得到 $5\ge c\cdot 6/c=6$，矛盾。所以 $5\ne\Theta(n)$：$O$ 成立而 $\Theta$ 不成立，这就是"Θ 严格强于 O"的具体形态。
>
> 再补一个常被忽略的点：定理的"当且仅当"要求两侧的 $n_0$ 都能取到有限值。若 $g$ 在某些点上为零，$f/g$ 无定义，此时兜底的不是定理而是"渐近为正"那条全局约定 —— 约定一破，两个单边界就可能各自成立却拼不出夹逼。Exercise 3.1-6 用 worst-case 与 best-case 给 Θ 的版本，也同样卡在这个前提上：最坏情况给上界、最好情况给下界，两者能拼成 Θ 的前提是同一族函数、同一个 $g$、同一个定义域。
>
> 顺带把 Exercise 3.1-7 的 $o(g)\cap\omega(g)=\varnothing$ 接进来：$o$ 要求比值趋于零，$\omega$ 要求比值趋于无穷，同一条射线上不可能两者兼得。这条空集结论与定理 3.1 共用同一套量词骨架，区别只在于把"存在某个常数"换成了"对任意常数"—— 前者允许你挑一个舒服的常数收工，后者要求每一个常数都通过，所以它更强、交集为空。
>
> 跨课程连接：6.042J 里你把关系分成等价关系与偏序，这里完全重合 —— Θ 是等价关系，O 是预序；而"两个界合并成一个夹逼"的手法，在 100B 实分析里是证极限的标准两步：先证 $\limsup\le L$，再证 $\liminf\ge L$，两条单边估计合起来才得到 $\lim=L$。区别在于实分析里的上下极限总存在、且对任意有界序列都能定义，而 O 与 Ω 可能两边都不成立（振荡函数），所以这里的定理是"当且仅当"而不是恒真。
>
> 最后回到 Exercise 3.1-5：亲手补两个方向时，你会看到 $c$ 在 O 一侧只能从上面压、在 Ω 一侧只能从下面托，两边的可行域在 Θ 里才第一次相交，而交出来的就是 $c_1$、$c_2$。定理的每个前提都是某一步放缩的合法性来源，不是技术性啰嗦。

---

> <span style="color:#7f8c8d;">CLRS §3.1, p.49</span>

当我们说一个算法的 running time（不带任何修饰语）是 $\Omega(g(n))$ 时，意思是：对 $n$ 的每个值，无论选取规模为 $n$ 的哪个具体输入，只要 $n$ 充分大，该输入上的运行时间都至少是 $g(n)$ 的常数倍。等价地说，这是在给出算法 best-case running time（最佳情况运行时间）的一个 lower bound（下界）。例如，插入排序的最佳情况运行时间是 $\Omega(n)$，这就蕴含了插入排序的运行时间是 $\Omega(n)$。

插入排序的运行时间因此同时属于 $\Omega(n)$ 与 $O(n^2)$，因为它可以落在 $n$ 的 linear function（线性函数）与 quadratic function（二次函数）之间的任何位置。而且这两个界在渐近意义上已经尽可能 tight（紧）：例如，插入排序的运行时间不是 $\Omega(n^2)$，因为存在某个输入使插入排序以 $\Theta(n)$ 时间运行（例如输入已经有序时）。然而，说插入排序的最坏情况运行时间是 $\Omega(n^2)$ 却并不矛盾，因为确实存在某个输入会使算法花费 $\Omega(n^2)$ 的时间。

### Asymptotic notation in equations and inequalities（等式与不等式中的渐近记号） <span style="color:#2471a3;">**[section]**</span>

我们已经见过如何在数学 formula（公式）内部使用渐近记号。例如，在引入 O-notation 时我们写过 “$n = O(n^2)$”；我们也可以写 $2n^2 + 3n + 1 = 2n^2 + \Theta(n)$。那么该如何解释这类公式呢？

当渐近记号单独地（即不在更大的公式之内）出现在 equation（等式）或 inequality（不等式）的 right-hand side（右端）时，比如 $n = O(n^2)$，我们已经把 equal sign（等号）定义为 set membership（集合隶属关系）：$n \in O(n^2)$。然而一般地，当渐近记号出现在一个公式之中时，我们把它解释为代表某个 anonymous function（匿名函数）——一个我们懒得为其命名的函数。例如，公式 $2n^2 + 3n + 1 = 2n^2 + \Theta(n)$ 的意思是 $2n^2 + 3n + 1 = 2n^2 + f(n)$，其中 $f(n)$ 是集合 $\Theta(n)$ 中的某个函数。在本例中，我们取 $f(n) = 3n + 1$，它确实属于 $\Theta(n)$。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> anonymous function（匿名函数）不是新发明的语法糖，而是你在 6.042J 里学过的量词缩写：渐近记号就是携带存在量词的占位符，写它的时候你承认"这里还差一个函数没命名"，正如积分号里写 $f$ 时不必先给它一个名字。
>
> 严格展开一遍：$2n^2+3n+1=2n^2+\Theta(n)$ 的准确意思是"存在 $f\in\Theta(n)$，使得对一切 $n$ 有 $2n^2+3n+1=2n^2+f(n)$"。这里 $f$ 的身份是明确的 —— 把两边相减得 $f(n)=3n+1$，而 $3n+1\in\Theta(n)$ 可以当场验证：$3n\le 3n+1\le 4n$ 在 $n\ge 1$ 时成立，所以取 $c_1=3$、$c_2=4$、$n_0=1$ 即可。注意"$f$ 属于集合 $O(g)$"与"存在常数 $c$ 与 $n_0$"是同一件事的两种写法：集合定义里的那些常数本身就是被存在量词约束的，所以换一种记法并没有换掉信息。
>
> 量词数目由记号出现次数决定，这一条最容易读错。求和式 $\sum_{i=1}^{n}O(i)$ 里只有一个 anonymous function（匿名函数），它随 $i$ 变化；整式等于把 $i$ 从 $1$ 到 $n$ 的同一个函数求和，而不是把 $n$ 个互不相干的函数加起来。算一遍：若每项就是 $i$，则和是 $\frac{n(n+1)}{2}\le n^2$，取 $c=1$、$n_0=1$ 得 $O(n^2)$；$n=100$ 时 $5050$ 对 $10000$，余量两倍。若误读成"第 $i$ 项有独立常数"，让第 $i$ 项的常数取到 $i$，和就变成 $\sum i^2=\frac{n(n+1)(2n+1)}{6}\approx\frac{n^3}{3}$，$n=100$ 时 $338350$ —— 差了一个整阶。这就是"一个匿名函数"与"$n$ 个"的实际后果，也是书上为什么说 $O(1)+O(2)+\cdots+O(n)$ 没有清晰解释。
>
> 方向性同样要紧。记号出现在等式右端，是存在性陈述：只要找得到某个函数就行。出现在左端则反了过来，$2n^2+\Theta(n)=\Theta(n^2)$ 读作"对任意 $f\in\Theta(n)$，都存在 $g\in\Theta(n^2)$ 使等式成立"。代入 $f(n)=3n$ 得左边 $2n^2+3n$，取 $g$ 就是它本身，验证 $2n^2\le 2n^2+3n\le 5n^2$ 在 $n\ge 1$ 成立（右边等价于 $3n\le 3n^2$）。左端越"模糊"，右端就越"粗"，因为右端必须容纳左端的所有可能取法 —— 这就是为什么链式 $2n^2+3n+1=2n^2+\Theta(n)=\Theta(n^2)$ 的两个等号要分开解释，而不能当成传递的相等来用。
>
> 反方向为什么不成立，用数字看最清楚。$\Theta(n^2)$ 能写成 $2n^2+\Theta(n)$ 吗？取 $n^2$ 本身，它等于 $2n^2+(-n^2)$，而 $-n^2$ 不在 $\Theta(n)$ 里（比值 $-n$ 趋于负无穷），所以拆不出来。也就是说 $2n^2+\Theta(n)$ 这一族函数严格窄于 $\Theta(n^2)$，等式只能单向读。凡遇到两个渐近式相等，都要先问清是右侧存在、还是左侧任意，再问方向能不能倒过来。
>
> 再做一次量级核对：$\sum_{i=1}^{n}O(i)$ 与 $O(n^2)$ 用 $n=1000$ 验一遍，真实和是 $500500$，上界 $c\cdot10^6$ 取 $c=1$ 时余量接近一半；而误读成 $\sum i^2$ 时是 $3.338\times10^{8}$，比 $n^2$ 大了三个数量级 —— 一个量词读错，结论就换了阶。这也解释了为什么书里强调匿名函数的个数等于记号出现的次数：个数是量词个数，量词个数决定你能"自由"到什么程度。
>
> 跨课程连接：6.042J 的量词消去与"存在 / 任意"的交换律，是这段内容的直接前身；C 语言里的 void 指针占位则可以当类比 —— 类型信息暂时留空，用的时候再补上。区别在于指针的补全由你在代码里显式做，漏了会被编译器拦住；而渐近等式里的补全由读者脑补，写反方向编译器不会报错，所以"拿不准就展开成量词"必须变成条件反射。
>
> 收束回正文：这套记法存在的唯一理由是消掉非本质细节，而它成立的前提是"读者随时能把它还原成量词句"。一旦你还原不出来，就说明你已经不是在用渐近记号，而是在用它伪装一个还没想清的量词结构。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (3.1) 对你正在学的 100B 实分析来说是老朋友：$f=o(g)$ 就是 $f/g\to 0$，可以直接调用极限的 $\varepsilon$-$N$ 语言 —— 对任意 $\varepsilon>0$，存在 $n_0$，使得 $n\ge n_0$ 时 $|f(n)/g(n)|<\varepsilon$。把书里集合定义中的"任意常数 $c>0$"读成"任意 $\varepsilon>0$"，两条定义逐字相同，只差一个绝对值。
>
> 值得盯住的是量词顺序。$o$ 的定义是 $\forall c>0\ \exists n_0\ \forall n\ge n_0$，$n_0$ 允许依赖 $c$；若把两个量词交换成 $\exists n_0\ \forall c>0$，那就要求同一个 $n_0$ 对所有 $c$ 都管用 —— 这不可能，因为 $c$ 可以取任意小，比值迟早跌破它。这个"$\forall$ 在前还是 $\exists$ 在前"的分野，你在 6.042J 见过它作为"逐点"与"一致"的差别，在实分析里它就是普通收敛与一致收敛的差别。
>
> 算一个具体数。取 $f(n)=n$、$g(n)=n^2$，比值是 $1/n$，要求 $1/n<\varepsilon$ 即 $n>1/\varepsilon$；取 $\varepsilon=10^{-3}$ 得 $n_0=1001$，取 $\varepsilon=10^{-6}$ 得 $n_0=10^6+1$。风险全在这里：$n_0$ 随 $\varepsilon$ 反比增长，没有统一的 $n_0$。对照 $2n$ 与 $n$：比值恒为 $2$，只要取 $\varepsilon=1$ 就失败，所以 $2n=O(n)$ 却 $2n\ne o(n)$ —— $o$ 的"严格性"正是靠"比值必须归零"这条撑起来的。
>
> 再体会一下"极限陈述"有多松。取 $f(n)=\lg n$ 与 $g(n)=n^{0.001}$：$n=10^6$ 时比值 $19.93/1.014\approx19.7$，$n=10^{12}$ 时比值 $39.86/1.318\approx30.2$ —— 比值还在涨。它确实终将掉头趋零，但拐点在远超任何可造规模的 $n$ 上。所以 $o$ 断言的是无穷远处的行为，不承诺"多大开始就已经变小"。工程上要的是后者，那就必须自己算拐点，不能拿一个 $o$ 交差。
>
> 工程上最该记住的是这条教训：$o$ 只说"终将"，不说"多早"。拿两个具体算法对照，一个代价 $1000\,n\lg n$，另一个 $n^2$：前者是 $o(n^2)$，比值 $\lg n/n\to 0$ 毫无疑问，可两者相等的位置在 $n\approx 1.4\times10^{4}$ —— 我逐点算到 $n=13747$ 才反超（$1.890\times10^{8}$ 对 $1.890\times10^{8}$）。也就是说，在你手上一切小于一万四千的输入里，那个"渐近更差"的二次算法仍然赢。$o$ 给出的信息只值一个"极限符号"，具体取舍必须自己解不等式。
>
> 由此还能推出一个常被忽略的用法：$o$ 适合用来"否定同阶"，不适合用来"推荐实现"。若你要回答"这两个算法是同一档吗"，答案 $f=o(g)$ 就足够；若你要回答"我该用哪个"，还得把常数与阈值一起算出来，否则等于用极限结论替工程决策背书。
>
> 于是五个记号各就各位：O 对 $\le$，Ω 对 $\ge$，Θ 对 $=$，o 对 $<$，ω 对 $>$，其中后两个是"比值趋于 $0$ 或 $\infty$"的严格版本。为什么算法课需要 o 这种严格序？因为要断言"A 渐近快于 B"，光有 $T_A=O(T_B)$ 不够 —— 那只是"不慢于"；$T_A=o(T_B)$ 才排除了两者同阶的可能。
>
> 跨课程连接：100B 的 $\varepsilon$-$N$ 定义与此处定义同构，区别有两点 —— 实分析里的极限必须存在且唯一，而这里函数可能振荡、比值无极限，定义照样能用（这正是它比"用极限定义"更强的地方）；另外本书额外要求渐近非负，只为给不等式免去绝对值符号，数学上并不增加内容。书中也点明，有些作者直接用式 (3.1) 作定义，代价就是丢了振荡情形。
>
> 收束回正文：o 与 ω 是把实数的严格不等号翻译到"比值尺度"上得到的，翻译过程中唯一新增的动作是"让 $n_0$ 依赖 $\varepsilon$"。记住这一条，五个记号的用法就不会串。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> transpose symmetry（转置对称）$f=O(g)\Leftrightarrow g=\Omega(f)$ 看似平凡，其实是一个可以逐字推导的代数恒等式，而且推导过程中只用到一个动作：取倒数。把 $f=O(g)$ 的定义 $f(n)\le c\,g(n)$ 变形为 $f(n)/g(n)\le c$，两边取倒数得 $g(n)/f(n)\ge 1/c$ —— 量词"存在 $c>0$"在这一步自动保持，因为 $1/c$ 仍是正常数。
>
> 这条推导暴露了"渐近为正"这个前提真正的用处：取倒数要求 $f$、$g$ 不为零且同号，否则不等号方向翻转、$1/c$ 也可能不是正常数。所以书上那句"凡进渐近记号的函数都渐近为正"不是洁癖，而是这块地基的一部分 —— 抽掉它，转置对称就不再是一条可以自由使用的规则。
>
> 带数字走一遍。取 $f(n)=3n+7$、$g(n)=n$：$f(n)\le 10n$ 等价于 $7\le 7n$，$n\ge 1$ 时成立，于是 $f=O(g)$ 用 $c=10$、$n_0=1$ 证完。反过来用 $c'=1/10$：$0.1(3n+7)=0.3n+0.7\le n$ 等价于 $0.7\le 0.7n$，同样在 $n\ge 1$ 成立，于是 $g=\Omega(f)$。$n=100$ 时核对：左边 $307\le 1000$，另一边 $30.7\le 100$，两边同时成立。而 $1/10$ 这个常数不是新找的，就是把 $10$ 翻了个身。
>
> 为什么这个对偶值得单独记？因为它让记忆量减半：关于 O 的每一条性质都免费赠送一条 Ω 的对应版本，关于 o 的每一条也免费赠送 ω 的。性质表里"传递性"那五行实际只有三行是独立的，另外两行是镜像。检验对偶有没有用对，办法固定：看常数经过变形后是否仍为正常数、不等号方向是否随之翻转。
>
> 用起来有多省事，试一次就知道。要证 $n^{1.5}=\Omega(n\lg n)$，不必重新找常数、重新取 $n_0$，直接写"由 $n\lg n=O(n^{1.5})$ 转置即得"。数值核对：$n=10^{6}$ 时 $n\lg n\approx1.99\times10^{7}$，$n^{1.5}=10^{9}$，比值约 $50$，确实远在下方之上。同理 $n^{2}=\omega(n\lg n)$ 与 $n\lg n=o(n^{2})$ 是同一句话，$n=10^{6}$ 时 $n^2=10^{12}$ 与 $1.99\times10^{7}$ 差五个数量级。凡涉及 $o$ 与 $\omega$ 的断言，都可以整批翻译成它的镜像，不必重新证。
>
> 这里还有一个容易被忽略的副产品：转置对称把"证明总量"减半。性质表里"传递性"那五行实际只有三行独立，另外两行是镜像；"自反性"三行里 o 与 ω 根本没有自反版本，因为比值恒为 $1$、既不趋于零也不趋于无穷 —— 这个"缺席"本身就是对偶结构的指纹：严格序不满足自反性，正如实数上的 $<$ 不满足 $a<a$。
>
> 跨课程连接：6.042J 关系一章里的 inverse relation（逆关系）是它的骨架 —— 把有序对的次序掉个个儿；实分析里 $\inf S=-\sup(-S)$ 是另一种对偶，取负号把序反转。区别在于取反的手柄不同：加法世界里用"取负"，乘法世界里用"取倒数"。渐近比较量的是常数倍的尺度，所以它属于乘法世界，用倒数；若你误用"取负"，会得到 $f\le cg$ 等价于 $-f\ge -cg$，那不是转置，是同一句话换了个说法。
>
> 再看一个会崩的场合：有的教材允许常数取任意实数（不要求正），此时 $c$ 可能是负的，$1/c$ 可能为负，转置立刻失效，整张性质表都得重写。这说明定义里的每一个字都是"某条性质成立"的代价，改一个字就得赔一桌菜。
>
> 收束回正文：转置对称的作用是让上界与下界成了同一件事的两个朝向，于是后面凡看到"上界"就该顺手想"它的下界镜像长什么样"。这也是为什么 Theorem 3.1 只用一句话就能把 Θ 拆成 O 与 Ω —— 两半本来就互为镜像。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道习题背后藏着一组值得记住的 min/max 运算法则，而它的证明只是「常数对夹逼」模板的第二次演出：找一对常数，把 $\max(f,g)$ 从上下两边夹进 $f+g$ 的常数倍里，动作与注 2 完全一致。
>
> 先看两条不等式，它们逐点成立、与 $n$ 无关：因为 $f$、$g$ 渐近非负，所以 $f\le f+g$ 且 $g\le f+g$，取逐点最大得 $\max(f,g)\le f+g$，这是上界，$c_2=1$。下界要动一下手：$\max\ge f$ 与 $\max\ge g$ 两式相加得 $2\max\ge f+g$，于是 $\max\ge\frac12(f+g)$，$c_1=\frac12$。两条合起来就是 $\frac12(f+g)\le\max(f,g)\le f+g$，$n_0$ 取使非负成立的那个值即可。
>
> 带数字验一遍：$f(n)=n^2$、$g(n)=n^3$，则 $\max=n^3$、$f+g=n^3+n^2$。$n=10$ 时 $\max=1000$、$f+g=1100$，比值 $1.1$，落在 $[\frac12,1]$ 的靠近上端；$n=1000$ 时比值 $1.001$，越来越贴近 $1$。也就是说下界那一半 $\frac12$ 是"最坏情况"的保险，实际往往松得多，但证明只需要它成立。
>
> 顺带把这条法则的同伴列清楚：$\min(f,g)=O(f+g)$ 同样成立（因为 $\min\le f$），但 $\min$ 与 $\max$ 之间一般没有 Θ 关系 —— 取 $f(n)$ 在奇数处为 $n$、偶数处为 $1$，$g$ 反过来，则 $\max$ 与 $\min$ 的比值随 $n$ 无限振荡，任何常数倍都套不住。这是"渐近比较不满足三分律"的一个具体化身。
>
> 真正的红线在混合运算上：渐近记号之间不能随便做减法。试 $O(n^2)-O(n^2)$：取 $2n^2-n^2=n^2$ 得 Θ(n^2)，取 $n^2-n^2=0$ 得零，取 $n^2-2n^2=-n^2$ 得负值 —— 同一个写法能给出三个不同阶的答案，说明它根本没有定义。原因很直接：匿名函数的符号不受控制，"存在某个函数"这句话不承诺它比谁大。
>
> 除法同样不行：取 $f_1=n^3$、$f_2=n^2$，两者都在 $O(n^3)$ 里，商是 $n$；取 $f_1=f_2=n^2$，商是 $1$。于是 $O(n^3)/O(n^3)$ 既可能是 $\Theta(n)$ 也可能 $\Theta(1)$。而加法是安全的：和式里的 $O(g)$ 会把较差的那一项整个吸收掉，$n^2+O(n)=\Theta(n^2)$ 可以直接写，因为被吸收的那项无论如何都超不过 $c\,n$。
>
> 下界那一半在 $\min$ 上就撑不住了：取 $f(n)=n$、$g(n)=n^2$，$\min=n$，而 $f+g=n^2+n$，比值 $1/n\to 0$，所以 $\min$ 连 $\Omega(f+g)$ 都不成立，只剩一个方向的 $O$。$\max$ 能两头都成立，是因为它永远不小于两者的平均值，而 $\min$ 永远不大于平均值 —— 这条不对称正是"和式被大项主导"的代数根源。
>
> 这条法则在分析分治时天天用到。若算法按 $2/3$ 对 $1/3$ 拆分，两侧代价分别是 $T(2n/3)$ 与 $T(n/3)$，你要说"每层总代价由较大那一侧决定"，靠的就是 $\max=\Theta(f+g)$；反过来若两侧都小到可以忽略，那整层代价由合并项决定，靠的是 $f+O(g)=\Theta(f)$。两条法则一上一下，把递归树每层的账封住了。
>
> 跨课程连接：CSAPP 第 6 章的 AMAT（平均访存时间）公式 $\text{hit}+\text{miss\_rate}\times\text{penalty}$ 就是一个加权和，其中最坏项主导总量 —— 命中 4 周期对缺失 200 周期，只要缺失率不为零，第二项就压过第一项，这正是 $\max$ 主导 $f+g$ 的工程版本。区别在于工程里的"主导"要靠实测权重，而这里只保证存在某个常数倍，不保证那个常数好看。
>
> 跨课程连接之二：6.042J 里你练过的不等式链（放大一项、扔掉一项、保留主项）就是这套动作的手工版。区别是那里每一步都要给出理由（正性、单调性），这里把理由压缩成了"渐近非负"这一条全局约定。
>
> 收束：三条法则一起记 —— $\max=\Theta(f+g)$、$\min=O(f+g)$、减法除法一律先展开成量词再动手。凡是混合运算拿不准，回到"匿名函数可以取任意符号"这一条，八成能在十秒内判出它没有定义。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 恒等式 (3.4)--(3.7) 都能用同一个可复用的手法两行证掉，我叫它「区间夹逼展开法」：把取整表达式翻译成"$x$ 落在端点全为整数的哪个区间"，端点整数时取整被冻结，于是嵌套结构可以逐层剥开。它成立的全部秘密在于起手式 (3.3)：$x-1<\lfloor x\rfloor\le x\le\lceil x\rceil<x+1$。
>
> 以 (3.4) 为例走一遍。记 $k=\lceil x/a\rceil$，由定义得 $k-1<x/a\le k$；两边乘正数 $a$ 不改方向，得 $a(k-1)<x\le ak$；再除以正数 $ab$，得 $k-1<\frac{x}{ab}\le k$。而这条式子恰好就是"$\lceil x/(ab)\rceil=k$"的定义，证完。全过程的唯一动作是"乘正数、除正数"，这也是为什么要事先声明 $a$、$b$ 为正 —— 若 $a<0$，不等号翻转，第二步就废了。
>
> 为什么端点整数是关键？因为区间 $(k-1,k]$ 的两个端点都是整数，任何落进去的实数，其向上取整必然是 $k$；一旦端点不是整数，这个"必然"就断了。所以整条方法的适用条件是"你要证的式子里，取整的层次都落在整数端点上"，而不是"任何含取整的式子都能这么剥"。
>
> 找一个会崩的例子，说明这条边界真实存在。(3.4) 之内外都是 ceil，成立；(3.5) 之内外都是 floor，也成立。但把内外混起来就错了：$x=3$、$a=2$、$b=2$ 时，$\lceil 3/2\rceil=2$，$\lfloor 2/2\rfloor=1$；而 $\lfloor 3/4\rfloor=0$。$1\ne 0$，式子崩。原因很清楚：内层向上取整把 $x$ 抬到了区间右端，外层再向下取整就把这次的抬升整个扔掉，方向不一致，抬升与丢弃不能抵消。
>
> 再看 (3.6) 的紧性：$a=7$、$b=2$ 时 $\lceil 7/2\rceil=4$，右边 $(7+1)/2=4$，等号成立。等号能取到说明这个界不能再改小，它不是一个随手写松的估计。这类"取整即区间"的推理在分析递归式 $T(\lceil n/2\rceil)+T(\lfloor n/2\rfloor)$、以及后面证明主方法时都会反复出现，因为一旦取整能被区间夹住，就能把它换成不取整的版本而不改变渐近阶。
>
> 跨课程连接：CSAPP 第 2、3 章讲整数的机器表示时，C 语言的整数除法是向零截断，而这里的 floor 是向负无穷截断。两者在正数上一致，在负数上分道扬镳：$-7/2$ 在 C 里是 $-3$，而 $\lfloor -7/2\rfloor=-4$。同理 $-7\bmod 2$ 在 C 里是 $-1$，而按式 (3.8) 的数学定义，$a\bmod n$ 必须落在 $[0,n)$ 内，答案是 $1$。
>
> 这个差别不是学术细节。写环形缓冲区、哈希表、或者任何用负数取下标的代码时，一旦你依赖"取模必然非负"，就会在负输入上静默越界；编译器不会提醒你，因为两边都"良定义"，只是定义不同。区别在于：数学上的 mod 与 (3.9) 那条 $0\le a\bmod n<n$ 绑在一起，C 的 % 与"与被除数同号"绑在一起，选哪个必须显式决定，不能靠习惯。
>
> 跨课程连接之二：6.042J 里余数与同余类的定义也是这套区间法的静态版本 —— 把整数按"除以 $n$ 的余数"分成 $n$ 个格子，每个格子是一个区间 $[qn,(q+1)n)$ 的整数部分。区别是那里关心分类与运算封闭性，这里关心不等式能否逐层剥开。
>
> 收束：以后遇到含嵌套取整的式子，动作固定 —— 先用 (3.3) 把它夹进整数端点的区间，再看内外取整方向是否一致；方向一致就能剥，方向相反就得另找路子。这条判据比背四条公式管用。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> "底数无关"的依据就是式 (3.15) 最后一条 $\log_b a=\frac{\log_c a}{\log_c b}$：换底只是除以一个常数 $\log_c b$，而 Θ 与 O 恰好对常数因子免疫。但这句结论有一个极易被套错的边界：它只对 logarithm（对数）成立，对 exponential（指数）完全不成立。分不清这两者，后面的比较就会一路错下去。
>
> 先把代数走一遍。$\log_b n=\frac{\ln n}{\ln b}$，于是 $\log_b n$ 与 $\ln n$ 相差因子 $1/\ln b$，与 $\lg n$ 相差 $1/\lg b$；三者互为常数倍，因此同属一个 equivalence class（等价类）。正因为如此，算法书干脆统一用 $\lg n$，省掉每次标注底数的麻烦 —— 这不是约定俗成的偷懒，而是等价性给了你选择的自由。
>
> 换几个具体底看看这些常数有多大。$n=10^{6}$ 时 $\lg n=19.9316$、$\ln n=13.8155$、$\log_{10}n=6$；三者的两两比值分别是 $1.4427$（$\lg$ 与 $\ln$）、$3.3219$（$\lg$ 与 $\log_{10}$）。也就是说，同一件事换三种记法，数值差三倍多，而 Θ 一眼就把这差别抹平了。这也解释了为什么在 O 里写 $\lg n$ 还是 $\ln n$ 无关紧要，但你在实现里选 $\log_2$ 还是 $\ln$ 却会实打实影响常数：前者在二进制分治的计数里更自然，后者在数学推导里更好算。
>
> 换成指数，同样的操作立刻失效。$3^{n}$ 与 $2^{n}$ 不是常数倍关系：$3^{n}=(2^{\lg 3})^{n}\approx(2^{n})^{1.585}$，指数上多了一个 $1.585$ 次方，两者分属不同的阶。所以"换底无害"这条只能在 log 里用；一旦你在指数上换底，必须重新分析。这类错误在复杂度推导里很常见：把 $2^{n}$ 与 $e^{n}$ 当作同阶，或者把 $n^{\log_2 7}$ 与 $n^{3}$ 当作差一个常数。
>
> 再看两条量级关系，它们是把"换底无害"推向极限后的结论。第一，polynomial（多项式）碾压 polylogarithm（多项对数）：$\lg^{b}n=o(n^{a})$ 对任意 $a>0$ 成立；具体地，$n=10^{6}$ 时 $\lg^{10}n\approx9.9\times10^{12}$ 仍大于 $n^{0.1}=3.98$，可见"碾压"发生在极远处，绝不意味着小规模上多项式更大。第二，指数碾压多项式：$n^{b}=o(a^{n})$ 对任意 $a>1$。
>
> 这第二条可以量化得很吓人。取 $1.001^{n}$ 与 $n^{1000}$：$n=10^{6}$ 时前者的指数是 $999.5$、后者的指数是 $13815.5$，多项式遥遥领先；$n=10^{8}$ 时变成 $99950$ 对 $18420.7$，指数彻底反超；两者的交叉点在 $n\approx1.66\times10^{7}$（我用二分法算的）。底数只比 $1$ 大千分之一，翻盘点也就一千六百万 —— 这个数量级恰好是"还能塞进内存的规模"，所以工程上指数算法不是"永远更慢"，而是"在你需要它的规模上必然更慢"。
>
> 跨课程连接：Strang 线性代数里的基变换是同一件事的推广：换基把坐标向量乘以 $P^{-1}$，对象本身不变，只改表示。区别在于基变换是一般的可逆线性变换，会改变范数与角度；而对数换底只是乘一个常数，是一维的相似变换，所以 Θ 只对后者免疫 —— 若你真做一次多变量基变换，范数会变，Θ 就不再免疫。
>
> 跨课程连接之二：CSAPP 讲浮点表示时，相对误差由尾数位数决定，与"你用哪个底做缩放"无关 —— 这是"底只影响尺度、不影响精度结构"的又一次体现。区别是浮点关心的是舍入误差的界，这里关心的是增长阶的界。
>
> 收束回正文：底数无关的依据只有一条换底公式，它的适用范围也只有一条 —— 只对 log。把这两个"只有一条"记住，剩下的比较就不会串味。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 式 (3.18) 的来历可以接到你正在学的 100B：把 $\ln n!$ 写成求和，用积分把它夹住，只能得到 $n\ln n-n+O(\ln n)$；那个看起来"多余"的 $\sqrt{2\pi n}$ 拿不出来，必须靠 Wallis 型积分 $W_n=\int_0^{\pi}\sin^{n}x\,dx$ 的递推另开一条线，再从两条线合拢时把常数 $\sqrt{2\pi}$ 解出来。
>
> 机制分三段。第一段是求和换积分：$\ln n!=\sum_{k=1}^{n}\ln k$ 是 $\int_1^{n}\ln x\,dx$ 的右端点 Riemann 和，而 $\ln$ 是凹函数，右和偏大，偏差累积起来是 $\frac12\ln n$ 量级 —— 这一步只给得出"$n^{n}e^{-n}$ 乘上一个 $n$ 的幂"这个形状，说不清幂次是多少。第二段是 Wallis：$W_n$ 单调递减且 $W_{n}=\frac{n-1}{n}W_{n-2}$，把它与 $W_{n-1}$ 的比值夹住，就能反解出 $\lim \frac{(2n)!!^{2}}{(2n+1)!!^{2}}\cdot\frac{1}{n}=\pi$ 这类极限。第三段是把两段合起来：求和那边留下一个待定常数 $c$，Wallis 那边恰好把它钉成 $\sqrt{2\pi}$。
>
> 数字上体会一下它有多准。$n=10$ 时 $10!=3\,628\,800$，而 $\sqrt{20\pi}(10/e)^{10}=3\,598\,696$，相对误差 $-0.83\%$。到了 $n=100$，误差降到千分之一以下，这也是为什么"近似"这个词在这里毫不心虚：它不是量级近似，而是相对误差趋于零。工程上用它的方式也很直接 —— 想估 $1000!$ 的位数，只需算 $\log_{10}$ 的主项，不必真乘。
>
> Robbins 版本把它变成了严格不等式：$n!=\sqrt{2\pi n}(n/e)^{n}e^{\alpha_n}$，其中 $\frac{1}{12n+1}<\alpha_n<\frac{1}{12n}$。取 $n=10$：区间是 $[0.008264,0.008333]$；而实测 $\ln(3628800/3598696)=0.008296$，正好落在里面。这条式子的价值在于它给出的是双向界，不只是"差不多"，所以可以直接拿去证不等式。
>
> 对算法课更要紧的是它的推论。两边取对数得 $\lg(n!)=n\lg n-1.4427n+O(\lg n)$，于是 $\lg(n!)=\Theta(n\lg n)$（式 (3.19) 第三条）。这条式子接着支撑第 8 章的排序下界：$n$ 个元素有 $n!$ 种排列，任何基于比较的算法都对应一棵二叉树，每个叶子是一种排列，每次比较只走一个分支，树高即最坏比较次数，于是下界是 $\lg(n!)$。
>
> 代入数字看这条下界有多硬：$n=10$ 时 $\lg(10!)=21.79$，也就是说 10 个元素至少要比 21 次多（实际最优算法约 22 次，几乎贴着界）；$n=10^{6}$ 时下界约 $1.849\times10^{7}$ 次比较。整条推理链是：排列计数、阶乘、Stirling、排序下界，四步中没有一步用到具体算法，纯计数 —— 这是"信息量决定代价"最干净的实例。
>
> 史实：带双侧误差界的这个版本出自 Robbins，1955 年发表于 American Mathematical Monthly 62 卷 1 期 26--29 页（我核到的是 JSTOR 2308012 的原文首页）。更早的近似形是 de Moivre 在 1730 年《Miscellanea Analytica》里为逼近二项分布中心项而得到的，Stirling 在同一年独立改进并给出了常数，所以名字落在了 Stirling 头上。
>
> 跨课程连接：100B 实分析里 Wallis 积分与 Gamma 函数是同一个工具箱，Gamma 函数把阶乘从整数延拓到实数，Stirling 就是它在无穷远处的展开；Bertsekas 那本概率教材会接着讲的下一个故事是：de Moivre 用这条近似推出正态曲线（1733），是中心极限定理最早的雏形。区别只在关注点：分析课关心极限存在与误差界，概率课关心分布逼近，算法课关心下界 —— 同一把尺子量三件不同的事。
>
> 收束回正文：记住这条链的顺序，比记住公式本身更重要。因为一旦你知道 $\lg(n!)$ 是从 Wallis 积分来的，就不会再把它当成"书上给的近似"，而会知道它的误差界为什么是 $\frac{1}{12n}$ 这个具体形式。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $\lg^{*}n$ 度量的是"要把一个数反复取对数压到不超过 $1$，需要压几轮"，也就是"2 的幂塔的高度"反过来读。塔每加一层，$\lg^{*}$ 只加 $1$；所以它的值不是"增长得慢"，而是"几乎不动"。
>
> 定义摆一遍：$\lg^{(i)}n$ 表示对 $n$ 连取 $i$ 次对数，$\lg^{*}n=\min\{i\ge 0:\lg^{(i)}n\le 1\}$。注意区分 $\lg^{(i)}n$（复合 $i$ 次）与 $\lg^{i}n$（对数的 $i$ 次幂），这两个符号在排版上只差一点，含义差一个世界。用塔来读最直观：$2=2^{1}$ 时 $\lg^{*}=1$，$4=2^{2}$ 时是 $2$，$16=2^{2^{2}}$ 时是 $3$，$65536=2^{2^{2^{2}}}$ 时是 $4$ —— 每读一层塔加一。
>
> 拿可观测宇宙的原子数算一遍。$10^{80}$ 的对数链是：$10^{80}\to265.754\to8.054\to3.010\to1.590\to0.669$，五步之后才跌到 $1$ 以下，所以 $\lg^{*}(10^{80})=5$。要到 $6$ 需要 $n$ 超过 $2^{65536}$，而这个数约等于 $10^{19728}$ —— 宇宙原子数在它面前相当于零。反过来说，凡是你能构造出来的输入规模（哪怕把每个原子当成一台机器），$\lg^{*}$ 都不超过 $5$。
>
> 它绝不是猎奇符号。disjoint-set forest（并查集）用"按秩合并 + 路径压缩"时，$m$ 次操作的总代价是 $O(m\,\alpha(m,n)+n)$，这里 $\alpha$ 是 Ackermann 函数的对角逆，这个结论出自 Tarjan 1975 年那篇 JACM 论文。Ackermann 的递归只三行：$A(1,j)=2^{j}$，$A(i,1)=A(i-1,2)$，$A(i,j)=A(i-1,A(i,j-1))$；第二个下标上做的是"把上一层的结果再喂回上一层"，于是 $A(2,j)$ 已经是幂塔、$A(3,j)$ 是塔的塔，增长快到无法用初等函数写出。$\alpha$ 就是"要多大的 $i$ 才够"的反函数，实际取值不超过 $4$。
>
> $\lg^{*}$ 与 $\alpha$ 是同一族的两个成员，区别在"压到哪"：$\lg^{*}$ 要求压到常数 $1$ 以下，$\alpha$ 要求压到 $\log n$ 这种随 $n$ 缓慢增长的量之下，所以 $\alpha$ 增长得更慢。直觉上，塔的高度决定要压几轮，而"每轮压扁都是指数式"保证了轮数只能是迭代对数级 —— 这就是"快得不可思议"的分析里常藏着的那一层。
>
> 跨课程连接：6.042J 的递归定义与增长阶比较是它的语法前身；你在图论里见过的"反复取对数"操作与这里同构。更近的锚点是分布式算法：某些着色与分解算法在 $O(\lg^{*}n)$ 轮内收敛，而每一轮只允许邻居之间传常数比特 —— 轮数界之所以能这么小，正因为信息在每轮里被"指数式压缩"了一次。
>
> 区别要讲清：$\lg^{*}$ 是"把数值压小"，分布式轮数是"把不确定性压小"，两者都靠指数式收缩，但后者还受通信半径限制，实际界往往是 $\lg^{*}$ 再乘一个常数或加一个 $\log$ 因子，不能直接照搬。
>
> 还有一个使用上的细节：对实数输入，$\lg^{*}$ 在边界附近会跳。因为链条中间可能出现 $2.011$ 这样略大于 $2$ 的值，多推一轮就多算一次，所以"$\lg^{*}(x)=4$ 还是 $5$"在 $x$ 接近某些阈值时对输入的微小扰动敏感。工程上不必纠结，因为两种取值都只差一，而我们要的是"不超过某个小常数"这个结论。
>
> 收束回正文：以后遇到"某个算法几乎线性、代价里带一个奇怪的小因子"的分析，先想是不是 $\lg^{*}$ 或 $\alpha$ 藏在里面；再想它为什么能这么小 —— 答案永远是"每轮指数式压缩"，而不是"算法特别聪明"。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> golden ratio（黄金比率）的历史比一般人以为的更老，但历史只管它"长什么样"，真正管用它的是方程 $x^2=x+1$ —— 那一行代数才是 $\phi$ 的现代身份证，其余性质都能从它推出来。
>
> 先把定义式当作起点。把线段按"整段比大段等于大段比小段"切开，设整段为 $1$、大段为 $x$，则小段是 $1-x$，条件写成 $\frac{1}{x}=\frac{x}{1-x}$，交叉相乘得 $x^{2}+x-1=0$ 的变形 $x^{2}=x+1$，正根就是 $\phi=\frac{1+\sqrt5}{2}=1.61803\ldots$。同一条二次方程还有负根 $\widehat{\phi}=\frac{1-\sqrt5}{2}=-0.61803\ldots$，书上叫它共轭数，不叫"另一个黄金比"是有道理的：两者都满足同一条方程，但只有正的那个是比值。
>
> 方程还能变形出连分数：由 $x^{2}=x+1$ 两边除以 $x$ 得 $x=1+\frac1x$，代回去得 $\phi=1+\frac{1}{1+\frac{1}{1+\cdots}}$。它的截断依次是 $1$、$2$、$\frac32$、$\frac53$、$\frac85$…… 分子分母正是相邻的 Fibonacci number（斐波那契数）。顺带一个副产品：$\phi$ 的连分数各项全是 $1$，展开得极慢，所以它是"最难被有理数逼近"的那一类无理数 —— 逼近速度的下界恰好就是每步一个常数因子。这一步很关键：它说明"相邻项之比趋于 $\phi$"不是巧合，而是"$\phi$ 是这条递推的特征根"的另一面。
>
> 数字上看看收敛速度。$F_{10}/F_{9}=55/34=1.617647$，与 $\phi$ 差 $3.9\times10^{-4}$；$F_{20}/F_{19}=6765/4181=1.61803396$，差 $2.6\times10^{-8}$。误差大约每步乘 $0.618$，也就是按 $|\widehat{\phi}/\phi|^{i}$ 衰减 —— 指数的底正是"负根与正根之比"，这一点在注 13 里会以矩阵特征值的形式再出现一次。
>
> 顺带说一个常被忽略的细节：相邻项之比的误差是上下振荡的（$1.5$、$1.667$、$1.6$、$1.625$……），不是单调逼近。原因是那个比值带负号：$-\widehat{\phi}^{i}$ 的符号随 $i$ 交替，所以误差一步一侧。工程上这意味着"用 $F_{i+1}/F_i$ 近似 $\phi$"时不能用相邻两次的差来估计误差，会得到虚假的收敛。
>
> 史实方面，一手材料能确认的有三条。其一，Euclid《几何原本》第六卷定义 3（约公元前 300 年）已经用"中末比"（extreme and mean ratio）的措辞定义了这条分割，措辞是"整段比大段如同大段比小段"。其二，Luca Pacioli 的《神圣比例》1498 年在米兰完成、1509 年 6 月 1 日在威尼斯首次印行，书中的多面体木刻据说是据 Leonardo da Vinci 的手绘制作（大都会博物馆的藏书著录即如此记载）。其三，Fibonacci 在 1202 年的《Liber Abaci》第十二章提出兔子问题、引入该序列时，全书并没有提到 $\phi$ —— 两者的联姻是后人的观察。至于"伊斯兰几何装饰大量使用五重对称因此间接依赖 $\phi$"这类说法，我只见到二手转述，未能一手核实，这里只作存疑记录。
>
> 跨课程连接：18.065 与 Strang 的特征值理论在这里直接对上。把递推写成矩阵 $M=\begin{pmatrix}1&1\\1&0\end{pmatrix}$，它的两个特征值正是 $\phi$ 与 $\widehat{\phi}$，而 power iteration（幂迭代）的收敛速率由第二大特征值与最大特征值之比决定，这里就是 $|\widehat{\phi}/\phi|=0.618$，也就是说每多做一次矩阵乘向量，误差就乘一个 $0.618$。区别在于幂法通常要求主特征值占优且为正（否则迭代方向来回翻），而 Fibonacci 的次特征值是负的，所以比值序列才会振荡 —— 这正是"矩阵有负特征值"时的标准现象。
>
> 收束回正文：把 $\phi$ 记成"方程 $x^{2}=x+1$ 的正根"，比记成"$1.618$"有用得多。因为一切关于它的等式 —— 连分数、闭式、$\phi^{2}=\phi+1$、$\phi^{n}=\phi^{n-1}+\phi^{n-2}$ —— 都是这一行方程的不同写法。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 一个只含加法的递推为什么能藏出闭式？因为 $F_i=F_{i-1}+F_{i-2}$ 是一个线性递推，它的全体解在"序列相加与数乘"下封闭，构成一个向量空间；而指数序列 $x^{i}$ 恰好是这个空间里"最简单的方向"。这正是 Strang 线性代数与 18.065 的语言，闭式就是对角化的结果。
>
> 为什么猜 $x^{i}$？因为递推的结构是"平移不变"的：把序列整体右移一位，关系式不变形。在这种结构里，指数序列是最自然的候选 —— 移位只让它乘一个常数 $x$，就像矩阵的特征向量让线性变换退化成数乘一样。把 $F_i=x^{i}$ 代进去得 $x^{i}=x^{i-1}+x^{i-2}$，约掉 $x^{i-2}$ 得特征方程 $x^{2}=x+1$，两根就是注 12 里的 $\phi$ 与 $\widehat{\phi}$。
>
> 于是通解是两个基的线性组合：$F_i=A\phi^{i}+B\widehat{\phi}^{i}$。两个待定系数由两个初始值定：$F_0=0$ 给 $A+B=0$，$F_1=1$ 给 $A\phi+B\widehat{\phi}=1$，解得 $A=\frac{1}{\sqrt5}$、$B=-\frac{1}{\sqrt5}$。这就是式 (3.25) 上面的闭式，整个过程只用到"解二元一次方程组"，没有需要灵感的地方。
>
> 矩阵视角更透。把递推写成 $\begin{pmatrix}F_{i+1}\\F_i\end{pmatrix}=\begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}F_i\\F_{i-1}\end{pmatrix}$，记这个矩阵为 $M$。它的迹是 $1$、行列式是 $-1$，特征多项式 $\lambda^{2}-\lambda-1$ 的两根正是 $\phi$ 与 $\widehat{\phi}$。于是 $M^{i}$ 的左上角元素就是 $F_{i}$，而 $M^{i}=S\Lambda^{i}S^{-1}$，$\Lambda^{i}$ 把两个特征值的幂并列在一条对角线上 —— 闭式的每一项都对应一个对角元。
>
> 数字上收尾。$i=10$ 时 $\phi^{10}/\sqrt5=55.0036$，$\widehat{\phi}^{10}/\sqrt5=-0.0036$，两者相减得 $55.0000$，正是 $F_{10}=55$。再取 $i=20$：$\phi^{20}/\sqrt5=6765.00003$，取整仍是 $6765=F_{20}$。误差项的量级也清楚：$|\widehat{\phi}|^{10}/\sqrt5=0.0036$，而一般地 $|\widehat{\phi}|^{i}/\sqrt5<\frac{1}{\sqrt5}=0.447<\frac12$，所以"$\phi^{i}/\sqrt5$ 四舍五入到最近整数就是 $F_i$"这条在一切 $i$ 上都成立 —— 这就是式 (3.25) 的来源。
>
> 为什么这个误差界这么干净？因为 $|\widehat{\phi}|=0.618<1$，它的幂指数衰减，衰减到 $\frac{1}{\sqrt5}$ 以下之后，剩下的偏移不足半个整数，取整就把它整个吞掉。换句话说，负根在这里的角色是"可忽略的扰动项"，而正根决定增长阶：$F_i=\Theta(\phi^{i})$，指数增长的底就是 $\phi$ 本身。
>
> 跨课程连接：18.065 里的对角化 $A=S\Lambda S^{-1}$ 是同一句台词，但这里有一个必须点明的区别 —— $M$ 不是对称矩阵，两个特征向量并不正交，所以你不能用"正交投影"的直觉去解释它。你能用的是"两个方向各自按 $\phi^{i}$、$\widehat{\phi}^{i}$ 独立演化，再线性叠加"，而这个叠加用的是 $S^{-1}$ 而不是 $S^{T}$。凡是拿对称矩阵的结论去套非对称矩阵，误差就出在这一步。
>
> 第二条连接：生成函数给出另一条完全不同的路。$F$ 的生成函数是 $\frac{x}{1-x-x^{2}}$，把它做部分分式分解，分母的两个根又是 $\phi$ 与 $\widehat{\phi}$，系数又是 $\pm\frac{1}{\sqrt5}$。幂级数与矩阵两条路在同一个终点会合，这不是巧合：生成函数的系数序列恰好是"移位算子"在该函数上的作用痕迹。
>
> 收束回正文：这套"特征方程 -- 特征向量 -- 对角化"的流程对任何常系数线性递推都原样适用，区别只在次数与初始条件个数。还有一个必须预备的例外：特征方程出现重根时 $x^{i}$ 不够用，要补上 $i\,x^{i}$ 这样的项，否则解空间维数凑不齐 —— 这与矩阵不可对角化、只能化成 Jordan 型是同一件事的两面。学会一次，后面遇到 $T(n)=2T(n/2)+n$ 这种线性递推（第 4 章的递归树就是它的展开）时，你会立刻知道"先找不变的方向"。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这个"买低卖高"的故事是一次纯正的 modeling（建模）训练：问题原本长着时间序列的样子，直接在价格上思考就会掉进"最低点必须在最高点之前"的时序陷阱；而把相邻两天的差排成一个数组之后，目标函数变得可分解，"何时买卖"就成了"哪一段之和最大"。
>
> 机制只有一行：把价格记作 $P_0,P_1,\ldots,P_n$，差分记作 $A_k=P_k-P_{k-1}$，则第 $i$ 天后买入、第 $j$ 天后卖出的利润是 $P_j-P_i=\sum_{k=i+1}^{j}A_k$。这叫望远镜求和：中间项两两抵消，只剩首尾。于是"最大化 $P_j-P_i$ 且 $i<j$"与"最大化某段连续 $A$ 的和"是同一件事 —— 一个约束在"两点"，一个约束在"一段"，后者有内在的合并结构，前者没有。
>
> 用书上那张表验一遍。17 天的价格里最低是第 7 天后的 $63$、其后最高是第 11 天后的 $106$，差 $43$；对应的差分是 $A[8..11]=18+20-7+12=43$，两处一致。我按表逐项累加核对过：$18$、$38$、$31$、$43$，最大值确实出现在第 11 天，且此前的最小前缀和出现在第 7 天。这个例子里"买在最低点"恰好也对，所以它不能说明问题有多难。
>
> 真正的反例是图 4.2：价格 $10,11,7,10,6$。全局最低是第 4 天后的 $6$，但它后面没有交易日可以卖出；全局最高是第 1 天后的 $11$，但它前面没有交易日可以买入。于是"锚定最低价"与"锚定最高价"两种策略都失效，最优解是第 2 天后买 $7$、第 3 天后卖 $10$，利润 $3$。这个 $3$ 既不是"最低到最高"的差（$11-6=5$，方向还反了），也不是任何单调极值的组合 —— 它只由时序决定。
>
> 为什么"可分解"是分水岭？因为一旦目标写成"某段的函数值之和"，就可以对区间本身做分治（跨中点的段由左右两半拼成），也可以从左到右增量维护。而原始形式里目标是两个端点的函数，端点一换，中间全变，没有可以复用的小结构。同一个问题，两种表示，一个只能暴力，一个能做线性 —— 这就是"选对表示比设计聪明算法更值钱"的具体含义。
>
> 跨课程连接：这是微积分基本定理的离散版。连续版说 $\int_a^b f'=f(b)-f(a)$，离散版说 $\sum_{k=i+1}^{j}\Delta P_k=P_j-P_i$，两者都把"区间上的累积"换成"端点的差"。区别在于连续版要求可导、离散版只要求相邻两个数有定义，所以离散版的适用面更宽，也更容易在代码里精确实现。
>
> 跨课程连接之二：CSAPP 讲数据表示与传输时提到的 delta encoding（差分编码）是同一手法的工程版 —— 存差分而不是存绝对值，重建时累加。区别在目的：那里是为了压缩与带宽（相邻值差异小，熵低），这里是为了让"区间最优"有结构。同一个变换，一边服务于存储，一边服务于算法，这说明变换本身不预设用途。
>
> 收束：记住这个两步节奏 —— 先找一个让目标函数可分解的表示，再对该表示上的子结构递归或扫描。第 4 章后面的分治与注 17 的线性扫描，都是这条节奏的两种走法。

> <span style="color:#7f8c8d;">[note] 本页含插图：图 4.1。图面结构：一张折线图（横轴 Day 为第 0–16 天，纵轴 Price 为 \$60–\$120 的股价曲线），下方附一张 17 列的表格。表格第一行为 Day（第 0–16 天），第二行为 Price（收盘价）：100、113、110、85、105、102、86、63、81、101、94、106、101、79、94、90、97；第三行为 Change（相对前一日的价格变化）：—、13、−3、−25、20、−3、−16、−23、18、20、−7、12、−5、−22、15、−4、7。</span>

**Figure 4.1（图 4.1）** Volatile Chemical Corporation（挥发性化学公司）在 17 天期间每日交易结束后的股票价格信息。图中横轴（horizontal axis）表示 day（天），纵轴（vertical axis）表示 price（价格）。表格最下面一行给出的是相对前一天的 change in price（价格变化）。

---

> <span style="color:#7f8c8d;">CLRS §4.1, p.69</span>

> <span style="color:#7f8c8d;">[note] 本页含插图：图 4.2。图面结构：一张折线图（横轴 Day 为第 0–4 天，纵轴为股价曲线），下方附一张 5 列的表格：Day 为第 0–4 天；Price 依次为 10、11、7、10、6；Change 依次为 —、1、−4、3、−4。</span>

**Figure 4.2（图 4.2）** 一个表明 maximum profit（最大利润）并不总是从最低价格开始、也不总是在最高价格结束的例子。同样，横轴表示 day（天），纵轴表示 price（价格）。这里，每股 \$3 的最大利润要通过在第 2 天之后买入、并在第 3 天之后卖出才能获得。第 2 天之后的 \$7 并不是整体上的最低价格，而第 3 天之后的 \$10 也不是整体上的最高价格。

……该反例表明：maximum profit 有时既不是靠在最低价买入得到的，也不是靠在最高价卖出得到的。

### A brute-force solution（暴力求解） <span style="color:#2471a3;">**[section]**</span>

我们可以很容易地为这个问题设计出一个 brute-force solution（暴力法解）：只需尝试每一对可能的 buy and sell dates（买入日期与卖出日期），其中买入日期先于卖出日期。一个为期 $n$ 天的时间段共有 $\binom{n}{2}$ 个这样的日期对。由于 $\binom{n}{2}$ 是 $\Theta(n^2)$ 的，而我们最多只能指望在 constant time（常量时间）内评估每一对日期，因此这种方法需要 $\Omega(n^2)$ 时间。我们能做得更好吗？

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 暴力法的代价账本值得用 6.042J 的计数技术精算一遍，而这个账本其实只有两项：候选总量与单个候选的评估代价，两者相乘就是总代价。整套"枚举所有候选"的思路都是这两个乘数的游戏，谁能把其中一个小下来，谁就赢。
>
> 先数候选。买入日必须严格早于卖出日，所以是"从 $n$ 天里无序选 $2$ 天"，个数 $\binom{n}{2}=\frac{n(n-1)}{2}$，是 $\Theta(n^{2})$。若允许当天买当天卖，还要加上 $n$ 个退化对，总数变成 $\binom{n+1}{2}$，阶不变。这类"从 $n$ 个对象里选固定大小子集"的计数在本书无处不在：插入排序的双重循环遍历所有下标对、所有点对的距离计算、所有边的枚举，用的都是同一个数。
>
> 再数第二个乘数。评估一对日期只需相减，是 $O(1)$，所以总代价 $\Theta(n^{2})$。换成差分表示后，候选变成子数组：长度为 $m=n-1$ 的数组有 $\sum_{L=1}^{m}(m-L+1)=\frac{m(m+1)}{2}$ 个非空连续段，$n=17$ 时 $m=16$，正好 $136$ 个 —— 与 $\binom{17}{2}=136$ 巧合地相等，因为两者都等于"从 $m+1$ 个位置里选两个当端点"。书上写 $\binom{n-1}{2}$，与精确计数的差是一个线性项，$\Theta(n^{2})$ 的结论不受影响。
>
> 关键在于第二个乘数可以被压到 $O(1)$。做法是前缀和：预处理 $P_{k}=\sum_{t\le k}A_{t}$，之后任意段的和 $A[i..j]=P_{j}-P_{i-1}$ 一次减法就够。于是"每个候选 $O(1)$"从一个假设变成了事实，总代价稳稳落在 $\Theta(n^{2})$ 而不是 $\Theta(n^{3})$。这个"预处理一次、查询多次"的模式，是后面散列、前缀积、稀疏表等一系列技巧的雏形。
>
> 给个规模感。$n=1000$ 时 $C(n,2)=499\,500$ 个候选；若每个候选平均花 $5$ 纳秒，总时间 $2.5$ 毫秒。相比之下，分治解法在 $n=1000$ 上只做约 $10^{4}$ 次基本操作，即使每次慢到 $20$ 纳秒也只有 $0.2$ 毫秒。数量级的差距不来自"谁更聪明"，而来自"候选多少"这个乘数 —— 暴力法没有做错任何事，它只是把乘数用满了。
>
> 但别小看暴力法的地位。它是 baseline（基准线）：先有正确但慢的解，"我们能做得更好吗"才成为一个可检验的问题；习题 4.1-3 的交叉点 $n_{0}$ 实验也才有对照物 —— 没有基准，你连"更好"是什么都说不清。工程上更是如此：绝大多数真实系统的第一版就是一个暴力实现，它先把语义钉死，再谈加速。
>
> 跨课程连接：6.042J 的组合计数与求和换序是这本账的数学工具；CSAPP 里估三重循环矩阵乘法的耗时（$n^{3}$ 次乘加）用的是同一个动作 —— 数每层循环的迭代次数再相乘。区别在于 CSAPP 还要再乘上每条指令的周期与 cache（高速缓存）miss 的代价，而这里只数渐进阶：前者给你"几毫秒"，后者只给你"哪一档"。
>
> 还有一条容易漏的边界：候选数是 $\Theta(n^{2})$ 的前提是"每对候选都不同"。如果问题允许重复计数（比如某些滑动窗口问题里同一个段被多个窗口覆盖），乘数就不是 $C(n,2)$ 而是 $n\cdot k$，账本要重写。计数永远要先问"我在数什么东西"，再问"它们是否互异"。
>
> 收束回正文：暴力法的账本只有两行 —— 候选数 $\Theta(n^{2})$、单价 $O(1)$。后面所有改进都在动这两行中的一行：分治把单价保持在 $O(1)$ 但让"有效候选"变少，注 17 的增量法直接让候选数降到 $n$。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 给分治算法记"代价账本"是分析一切分治的通用模板，本题只有三笔：divide（分解）只算下标、$\Theta(1)$；conquer（解决）是两次递归、$2T(n/2)$；combine（合并）是跨中点扫描、$\Theta(n)$。三笔相加得 $T(n)=2T(n/2)+\Theta(n)$，与归并排序的账本逐项同构，所以答案也必然是 $\Theta(n\lg n)$。
>
> 为什么"跨中点"这一类能被单独拎出来算？因为任何连续段 $A[i..j]$ 与中点 $mid$ 的关系只有三种，且互斥又穷尽：完全在左半边、完全在右半边、跨越中点。前两种交给递归，第三种必须在本层解决 —— 这不是技巧，是划分的完备性要求。少了第三类，答案会漏；把第三类也丢给递归，就不是同一个子问题了。
>
> 第三类为什么线性可解？因为任何跨中点的段都能唯一拆成两截：以 $mid$ 结尾的左段与以 $mid+1$ 开头的右段。两截独立，各自最大化再相加即可 —— 左段从 $mid$ 往左扫、累加取最大，右段从 $mid+1$ 往右扫、累加取最大，各扫一遍，总次数正好是区间长度 $n$。这一步把一个看似要枚举 $\Theta(n^{2})$ 段的问题重组成了"可合并的子结构"。
>
> 给个可复核的数字。取 $n=16$ 的差分数组（15 个数）：暴力枚举所有连续段并逐个求和，读元素的总次数是 $\sum_{L=1}^{15}(16-L)\cdot L=680$；分治解法每层扫描一遍共 $16$ 次，递归树有 $\lg 16=4$ 层，总计 $64$ 次。$680/64\approx10.6$，这就是"分治在 $n=16$ 上省下的读次数"的实际倍数。规模再大，倍数还会涨，因为分子是 $n^{3}/6$ 量级、分母是 $n\lg n$。
>
> 递归树视角更直观。每个结点标上本层的合并代价，则每层代价之和都是 $n$（因为每层的子数组总长恰为 $n$），层数是 $\lg n$，乘积 $n\lg n$。这个"每层总和相等"的性质来自"分解只是切分、没有重复"，一旦你的分解产生重叠子问题（例如某些计数问题），这条就不再成立，递归树会变宽，得改用别的方法。还有一个细节值得注意：递归到底层时每个单元素子数组自身就是一个候选段，所以"跨中点合并不覆盖单元素段"这件事并不需要额外处理 —— 长度为 $1$ 的段在 base case 里已经返回过了。
>
> 跨课程连接：CSAPP 第 6 章讲归并排序的 cache（高速缓存）行为时，用的也是"层数乘每层次数"的账本，但每层的常数不一样：外层要读写的数组远超 cache（高速缓存）容量，miss 多；切到子数组小于 L2 之后，所有访存都命中，单价骤降。于是真实最优的 base case 往往不是 $1$，而是几十 —— 这正好对上课后习题 4.1-3 要你实测的交叉点 $n_{0}$。区别在于 CLRS 假设每层单价相同，CSAPP 告诉你每层单价能差上数十倍。
>
> 跨课程连接之二：6.042J 里对递归式做"展开几层看规律"的手法就是递归树的雏形；那里你更关心求和技巧，这里你更关心"每层代价是否相等"。同一棵树，两种提问方式。
>
> 收束：任何分治题先问三个数 —— 一次分解花多少、递归几路、合并多贵。三个数一写，递归式自现，剩下的只是解它。本题的答案之所以与归并排序一字不差，正是因为三个数也一字不差。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道习题指向的是后来被称为 Kadane 算法的线性解法：从左到右扫一遍，只维护一个量 —— "以当前位置结尾的最大子数组和"，每读一个元素要么接到前一个尾巴上，要么另起炉灶，全程 $O(n)$，额外空间 $O(1)$。
>
> 机制的关键是把子问题族设计对。定义 $E_{j}$ 为"所有以 $j$ 结尾的段的和的最大值"，则 $E_{j+1}=\max(A_{j+1},\ E_{j}+A_{j+1})$：以 $j+1$ 结尾的段要么只有它自己，要么是"某个以 $j$ 结尾的段"再接上 $A_{j+1}$，而接上同一个元素不改变"哪个段更好"的排序，所以只需保留最好的那个。这一步就是最优子结构的形式化：整个子问题族被压缩成了一个数。
>
> 全局答案是 $\max_{j}E_{j}$，因为任何段都以某个位置结尾。于是两行循环解决：每步先更新 $E$，再用 $E$ 更新答案。注意 $E$ 允许为负（当前元素是负数且前面没有可接的正尾巴时），但不必清零 —— 清零只对应"允许空段"的变体，那是习题 4.1-4 的内容。
>
> 用书上那 16 个差分跑一遍。前缀和依次是 $0,13,10,-15,5,2,-14,-37,-19,1,-6,6,1,-21,-6,-10,-3$；最大的一段和出现在第 11 个位置（前缀和 $6$），此前的最小前缀和是 $-37$（第 7 个位置），$6-(-37)=43$，与 $A[8..11]$ 的和一致。我按 $E$ 递推也复算过一遍，最大值 $43$ 出现在同一点。两种视角 —— 前缀和差、增量递推 —— 得到同一个数，这不是巧合：$E_{j}=P_{j}-\min_{k\le j}P_{k}$。
>
> 这条恒等式值得单独记：它说明 Kadane 与前缀和最小法是同一个算法的两种写法，一个维护"当前最优尾巴"，一个维护"历史最小前缀"。后者更容易解释"为什么线性"，前者更容易实现成常数空间。看清这一点，你就不必背两套代码。
>
> 史实方面，Bentley 在 1984 年 9 月《Communications of the ACM》的 Programming Pearls 专栏里讲了这个问题的完整演进史：问题由布朗大学的 Ulf Grenander 于 1977 年为图像中的最大似然估计提出，他先给了三次与二次的解法；Michael Shamos 一夜之间给出 $O(n\log n)$ 的分治解；随后 Jay Kadane 在一分钟之内给出线性解。这条线索本身就值得记住 —— 它展示了一次典型的"从 $n^{3}$ 到 $n^{2}$ 到 $n\log n$ 到 $n$"的压缩过程，每一步都在换工具。
>
> 跨课程连接：这是第 14 章 dynamic programming（动态规划）的雏形，区别在于分治把问题切成互不相交的子问题、深度 $\lg n$；动态规划把子问题按规模排成一条链、每个只解一次，靠"只保留必要状态"消掉重复计算。数量感受一下：$n=16$ 的分治要做 $16\times4=64$ 次合并操作，Kadane 只做 $16$ 次加法与 $16$ 次比较。
>
> 更值钱的判断力在这里：分治给出 $\Theta(n\lg n)$ 之后，还能不能再榨？答案是不能 —— 因为它的信息流是"自底向上合并"，每层都要扫一遍。要突破就得换范式，从"分而治之"切到"增量维护"。识别"分治已到顶、该换动态规划"的时机，比记住任何一个公式都更有用。
>
> 收束回正文：这道习题真正教的是"子问题该怎么定义"。定义成"以 $j$ 结尾"这个带方向的族，才让状态只需一个数；若定义成"任意区间"，状态就爆炸回 $\Theta(n^{2})$。子问题的定义方式，决定了算法能不能线性。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Strassen 方法的意义不在"快了这么一点"，而在于它第一次证明了"矩阵乘法需要 $n^{3}$ 次标量乘法"这句话从来没有被证明过，只是被默认为天然下界。1969 年那篇论文的标题直白得刺人：《高斯消元不是最优的》，发表在 Numerische Mathematik 13 卷 4 期 354--356 页。
>
> 机制一句话：用加减法换乘法。八次递归乘法砍成七次，指数从 $\lg 8=3$ 降到 $\lg 7\approx2.8074$；代价是多做常数次 $n/2\times n/2$ 矩阵加减（第 2 步十个 $S_{i}$、第 4 步八次组合，共十八次），而这些加减的代价是 $\Theta(n^{2})$，被 Θ 记号整个吞进 $f(n)$ 项。合法的前提是它只用到环公理（加法交换、乘法对加法分配），所以对任何环上的矩阵都成立 —— 这是"代数算法"的边界，浮点误差分析另有话说。
>
> 拿一个最小的例子把它走完。$A=\begin{pmatrix}1&3\\7&5\end{pmatrix}$、$B=\begin{pmatrix}6&8\\4&2\end{pmatrix}$：$S_{1..10}$ 依次为 $6,4,12,-2,6,8,-2,6,-6,14$；$P_{1..7}$ 依次为 $6,8,72,-10,48,-12,-84$；组合得 $C=\begin{pmatrix}18&14\\62&66\end{pmatrix}$，与朴素算法逐项相符。乘法用 $7$ 次而不是 $8$ 次（省 $12.5\%$），加减用 $18$ 次而不是 $4$ 次（多 $14$ 次）。在小规模上这笔交易明显亏本，胜负要到大规模才翻转。
>
> 翻得有多快？$n=1024$ 时朴素要 $n^{3}=1.074\times10^{9}$ 次标量乘法，Strassen 约 $n^{2.807}=2.818\times10^{8}$，差 $3.81$ 倍；$n=4096$ 时是 $6.872\times10^{10}$ 对 $1.380\times10^{10}$，差 $4.98$ 倍。倍数是乘法关系而不是加法关系，所以"指数上省一点"的收益随 $n$ 单调放大 —— 但要先把加减多出来的常数债还清，这才有工程上的交叉点。
>
> 史实核对几条。Strassen 生于 1936 年，学术出身是概率论（1964 年关于不变原理的那篇论文至今仍被反复引用），矩阵乘法只是跨界的战果之一；1971 年他与 Schönhage 给出大数乘法的 Schönhage--Strassen 算法，1977 年与 Solovay 给出随机素性检测；Knuth Prize 是 2008 年度（他 2009 年 1 月在 SODA 上作获奖演讲，所以我按获奖名单把它记为 2008 年，原注里的 2009 年应是演讲年份）。
>
> 他的动机是第一性原理式的：既然没人证明过 $\Omega(n^{3})$，那么"显然"的 $n^{3}$ 也许并不紧。这与 Karatsuba 在 1960 年一周之内推翻 Kolmogorov 的 $\Omega(n^{2})$ 大数乘法猜想是同一个剧本 —— 后者把四位乘法用三次子乘法代替四次，递归后得到 $n^{\lg 3}\approx n^{1.585}$。两次都是"下界未证，就不必信"，而两次都靠"少做一次乘法、多做一些加减"实现。
>
> 跨课程连接：18.065 与数值线性代数里，矩阵乘法被组织成 BLAS-3（每次搬入 $O(n^{2})$ 数据、做 $O(n^{3})$ 次浮点运算），算术强度是 $n$。blocking（分块）的目标是让数据搬运不成为瓶颈。Strassen 减少的是浮点运算次数，增加的却是访存的不规则性，所以在 cache（高速缓存）受限的机器上常常不敌分块朴素算法，直到 $n$ 达到数百甚至上千才有时。
>
> 区别要说明白：CLRS 的 Θ 分析假设"一次乘法与一次加法同价"，硬件不给这个保证（乘法器延迟数倍于加法器），所以"渐近更优"与"实测更快"之间隔着一个交叉点。这个交叉点正是习题 4.2-3 与 4.1-3 让你亲手测的东西。
>
> 收束回正文：Strassen 的贡献是概念性的 —— 它把"矩阵乘法的复杂度"从一个固定的数变成了一个待求的指数，此后所有 $O(n^{\omega})$ 的竞赛都从这里起跑，而 $\omega<3$ 这件事本身，就是这篇三页论文留下的。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> Strassen 方法的本质一句话：用加减法换乘法。把 $8T(n/2)$ 砍成 $7T(n/2)$，指数从 $\lg 8=3$ 降到 $\lg 7\approx2.8074$，代价是多做常数次加减，好在矩阵加减只要 $\Theta(n^{2})$，渐近上被 Θ 记号吸收。这笔交易为什么划算，答案藏在"$a$ 出现在指数上"这件事里。
>
> 先把指数关系推出来。递归树第 $\ell$ 层有 $a^{\ell}$ 个结点，规模降到 $1$ 需要 $\log_{b}n$ 层，于是叶子数（也就是标量乘法的次数）是 $a^{\log_{b}n}=n^{\log_{b}a}$。这个等式是本注的全部技术内容：$a$ 每变 $1$，指数变 $\log_{b}a$，所以 $a$ 是"铆在指数上的钉子"，动一次，整条曲线换一条。
>
> 用 $b=2$ 举例，$n=1024$ 时层数是 $10$，叶子数 $8^{10}=1.074\times10^{9}$（正是 $n^{3}$），改成 $7$ 次则是 $7^{10}=2.825\times10^{8}$（正是 $n^{2.807}$）。数值巧合不是巧合，是恒等式的直接体现。规模放大到 $n=4096$：$8^{12}=6.872\times10^{10}$ 对 $7^{12}=1.380\times10^{10}$，差 $4.98$ 倍，而 $n=1024$ 时只差 $3.81$ 倍 —— 收益随规模单调增长。
>
> 为什么"多做的加法"真的免费？因为第 2 步的十个 $S_{i}$ 与第 4 步的八次组合，每个都是 $n/2\times n/2$ 矩阵的加减，共 $18$ 次，每次 $n^{2}/4$ 个元素，合计 $4.5n^{2}$ 次标量运算。它是 $n$ 的二次多项式，而递归项是 $n^{2.807}$，前者在渐近上被后者支配。这就是"$f(n)$ 只是被 Θ 吸收的地板"的意思：地板再厚，也厚不过指数。
>
> 同一个思想家族里还有 Karatsuba：把 $n$ 位数乘法拆成两半，用 $3$ 次子乘法代替 $4$ 次，递归后得到 $n^{\lg 3}\approx n^{1.585}$，1960 年发现、1962 年发表。两次改进的动作完全同构 —— 都只动 $a$，都靠"多几次加减"把省下的乘法抵掉。学会看 $a$，你就能一眼认出这两个算法是亲戚。
>
> 反过来，动 $f(n)$ 几乎没有意义。假设你把合并代价从 $n^{2}$ 优化到 $n^{2}/\lg n$（现实中这已经是巨大的工程成就），在 $T(n)=8T(n/2)+f(n)$ 里，指数仍然是 $3$，只是常数变小一点点。而把 $a$ 从 $8$ 改成 $7$，指数就掉了 $0.19$ —— 这是量级上的差别，不是常数上的。
>
> 这里要交代一个前提：叶子数等于标量乘法次数，只在 base case 取 $n=1$、每个叶子做一次乘法时成立。工程实现通常不递归到 $1$，而是在某个阈值 $t$ 处切换成朴素乘法，此时叶子数变成 $(n/t)^{\log_{b}a}\cdot t^{3}$ —— 指数仍是 $\log_{b}a$，只有常数变了。这条恰好说明"换 base case 只动常数，不动指数"，也解释了为什么习题 4.1-3 让你去实测那个阈值。
>
> 跨课程连接：CSAPP 第 3 章讲指令延迟时，整数乘法 `imul` 约 $3$ 个周期、加法约 $1$ 个周期，除法更贵（数十周期）。所以小规模时代数决定胜负：多做的 $18$ 次加法确实要花时间，Strassen 在 $n<100$ 常常输给朴素分块。大规模时指数决定胜负。区别在于 Θ 分析假设乘法加法同价，硬件不给这个承诺 —— 这也解释了为什么"渐近更优"必须配一个实测交叉点才算完整结论。
>
> 还有一条容易被忽略的代价：Strassen 的加减是"数据搬运型"操作，访存量大、局部性差；朴素分块则是访存规整的。所以真实机器上的交叉点往往比"纯运算次数模型"预测的更靠右，这也是它在库里长期只是可选项而非默认的原因。
>
> 收束：在 $aT(n/b)+f(n)$ 型递归里，优化优先级永远固定 —— 先瞄准 $a$，再瞄准 $b$，最后才抠 $f$。记不住这句话时，就回想 $7^{10}$ 与 $8^{10}$ 差的那 $3.8$ 倍：它来自一个整数从 $8$ 变成 $7$。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $\Theta(n^{\lg 7})$ 只是矩阵乘法"军备竞赛"的起点，而不是终点。把这件事看成一个待求的指数 $\omega$（使 $n\times n$ 矩阵乘法可在 $O(n^{\omega+\varepsilon})$ 内完成的最小值），整部历史就是从 $3$ 一路压向 $2$ 的过程，而每压一点都要换一套工具。
>
> 下界为什么只有 $2$？因为输出有 $n^{2}$ 个元素，每个至少写一次，所以任何算法都逃不掉 $\Omega(n^{2})$。这条下界弱得可怜 —— 它只数了输出，没数必要的计算。已知的更强下界要么依赖模型限制，要么只对特定系数域成立，所以"$\omega$ 究竟是不是 $2$"至今是公开问题。
>
> 数字上的推进是这样的：Coppersmith 与 Winograd 在 1990 年把上界压到 $O(n^{2.3755})$（文献里常引作 $2.376$）；Stothers、Vassilevska Williams、Le Gall 在 2010 至 2014 年间把它连番推低，Le Gall 2014 年在 ISSAC 给出的值是 $2.3728639$（靠的是分析 Coppersmith--Winograd 构造的 $32$ 次张量幂）；2024 年 Alman 等人用"更多非对称性"的方法把上界压到 $2.371339$（arXiv:2404.16349）。
>
> 这些数字之间的差别有多大？$n=100$ 时 $n^{3}=10^{6}$，而 $n^{2.371339}=5.53\times10^{4}$，比值约 $18$；$n=1000$ 时是 $10^{9}$ 对 $1.30\times10^{7}$，比值约 $77$。看上去很划算，但这只是"运算次数"的账，常数因子完全没算进去 —— 而这些算法的常数大到离谱：它们要先构造巨型张量、解大规模优化问题才能确定递归基块。
>
> 于是有了 galactic algorithm（银河系算法）这个说法：只有 $n$ 大到现实中根本造不出来时，它才比朴素算法快。文献里的描述很直白 —— 大 O 藏住的常数如此之大，以至于这些算法在实践中从未被使用。这也是它与 Strassen 的关键区别：Strassen 的常数小到可以在 $n$ 上百时开始有用，$O(n^{2.37})$ 家族的常数大到连"上百"这个量级都撑不起。
>
> 顺便把 2024 年之后的情况标注清楚：我检索到的二次引用显示之后还有人报到 $2.371177$ 这样的值，但我只见到转述、未见原论文，按"查不到一手就写明"的规矩，这里只记到 $2.371339$，不再往后延伸。
>
> 跨课程连接：这与 CSAPP 教你的"大 O 不等于快"是同一条教训的两端。CSAPP 那一端说：常数与 cache（高速缓存）行为能颠覆渐进结论，所以要测。这一端说：渐进更优可能工程更差，因为常数大到无法偿还。区别在于 CSAPP 的常数来自硬件层级（几十到几百个周期），这里的常数来自算法构造的复杂度（可能是天文数字），前者可测、后者连测的机会都没有。
>
> 更实际的一条：Strassen 在真实库里是可选项（例如某些 BLAS 实现提供开关），而这些 $O(n^{2.37})$ 算法从未进过任何库。原因不是没人实现，而是实现了也不划算 —— 这条经验对"看到论文里的更优复杂度就想去替换库"的冲动是一剂清醒药。
>
> 收束回正文：把 $\lg 7\approx2.81$ 记作历史坐标 —— 1969 年之前人类以为答案是 $3$，此后的五十五年一直贴着 $2.37$ 附近压线，而理论上限仍是 $2$。这条曲线告诉你：指数上的一点点，值得几代人反复折腾；而"是否值得工程采用"是另一个完全独立的问题。

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
