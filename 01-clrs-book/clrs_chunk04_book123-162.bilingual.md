# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk04 · 书页 123–162 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §5.2–5.3, p.123</span>

（接上页）……我们预期对任意 input（输入）都是如此，而不只是对取自某个特定 distribution（分布）的输入。

### Section 5.3 · Randomized algorithms（随机化算法） <span style="color:#2471a3;">**[section]**</span>

让我们进一步考察 probabilistic analysis（概率分析）与 randomized algorithm（随机化算法）之间的区别。在 §5.2 中我们曾断言：假设候选人以随机顺序到来，雇用一位新办公室助理的 expected number（期望次数）约为 $\ln n$。注意，这里的 algorithm（算法）是 deterministic（确定性的）：对任何一个特定输入，雇用新办公室助理的次数总是相同的。此外，雇用新办公室助理的次数随输入不同而不同，它取决于各位候选人的 rank（名次）。由于这个次数只取决于候选人的名次，我们可以按顺序列出各位候选人的名次来表示一个特定输入，即 $\langle rank(1), rank(2), \ldots, rank(n) \rangle$。给定名次表 $A_1 = \langle 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 \rangle$，新办公室助理总会被雇用 10 次，因为每位后继候选人都比前一位更好，于是第 5–6 行在每次 iteration（迭代）中都会被执行。给定名次表 $A_2 = \langle 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 \rangle$，新办公室助理只在第一次迭代时被雇用一次。给定名次表 $A_3 = \langle 5, 2, 1, 8, 4, 7, 10, 9, 3, 6 \rangle$，新办公室助理被雇用三次，分别是在面试名次为 5、8 和 10 的候选人时。回想我们的算法成本取决于雇用新办公室助理的次数，可以看到：既有像 $A_1$ 这样的 expensive inputs（昂贵输入），也有像 $A_2$ 这样的 inexpensive inputs（廉价输入），还有像 $A_3$ 这样的 moderately expensive inputs（成本中等的输入）。

另一方面，考虑这样一个随机化算法：先对候选人做 permutation（排列），然后再确定最佳候选人。在这种情况下，我们在算法中进行 randomize（随机化），而不是在输入分布中随机化。给定一个特定输入，比如上面的 $A_3$，我们无法说出最大值会被更新多少次，因为这个量随算法的每次运行而不同。第一次在 $A_3$ 上运行该算法时，可能产生排列 $A_1$ 并执行 10 次更新；而第二次运行时，可能产生排列 $A_2$ 并只执行一次更新。第三次运行时，执行的更新次数又可能是别的某个数。每运行一次该算法，其执行过程都取决于所做的随机选择，并很可能与上一次的执行不同。对于这个算法以及许多其他随机化算法而言，没有任何特定输入能诱发其 worst-case behavior（最坏情况行为）。即使是你最坏的敌人，也无法构造出一个坏的输入数组，因为随机排列使输入顺序变得无关紧要。只有当 random-number generator（随机数生成器）产生一个"不走运"的排列时，随机化算法才会表现糟糕。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 从第一性原理看，这一段揭示的是随机化的本质交换：确定性算法的运行时间完全由输入决定，了解你算法的"敌人"总能构造最坏输入（如恒增序的 $A_1$）；而随机化算法把"输入从哪来"的控制权从敌人手里夺回，换成自己掷骰子——输入顺序被随机排列抹平后，任何固定输入的表现都与随机输入无异，最坏情况从"必然可达"降格为"小概率事件"。这就是 adversarial model（对抗模型）的直觉：分析算法时必须问"最坏情况由谁控制"。你在 6.006/6.046J 会看到同样的操作用在快速排序上：固定取末尾元素做 pivot 会被有序输入打回 $\Theta(n^2)$，改为随机选 pivot 后，期望运行时间 $\Theta(n \lg n)$ 对每个输入都成立。术语上也要分工：对随机输入的分析称 average-case（平均情况），对算法自己掷骰子的分析称 expected（期望）——这正是引理 5.2 与 5.3 对比的要点。CSAPP 中没有"对抗"视角，因为硬件性能不取决于谁在攻击；但散列表（第 11 章）与密码学的分析都建立在这一直觉上。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么范围取 $1$ 到 $n^3$ 就够？用 6.042J 的生日问题直接估算碰撞概率：$n$ 个独立均匀的优先级中任一对重复的概率约 $\binom{n}{2}/n^3 \approx 1/(2n)$，由 union bound（联合界）可知全不相同的概率至少 $1 - 1/n$——这正是习题 5.3-5 要证的界。直觉上，生日问题的阈值在"配对数 $\binom{k}{2}$ 追上天数 $n$"处；这里配对数约 $n^2/2$、编号空间是 $n^3$，余量达 $n$ 倍，重复自然稀有。更值得记住的是设计手法："先枚举理想概率空间，再用确定性过程解码"——我们想从 $n!$ 个排列中均匀抽样却难以直接实现，于是改为给每个元素发独立随机编号，用排序这一确定性过程把编号翻译成排列；只要编号空间足够大、碰撞可忽略，翻译结果就（以高概率）均匀。这种"随机打分 + 确定性解码"的模式，会在第 7 章随机化快速排序（随机选 pivot）与第 11 章散列（随机选散列函数）中以不同面目重现。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里可以提炼出一个可复用的证明模板——「条件概率链」：要证明某过程产出均匀分布，先固定一个具体结果，把"它发生"拆成按时间顺序排列的事件 $E_1, E_2, \ldots, E_n$，用 6.042J 的条件概率乘法法则逐项计算，每一项都利用"剩余选项彼此对称"而等于 $1/(n-i+1)$，连乘即得 $1/n!$。模板的力量在于不需要各步独立，只需要每一步在给定历史下对称；引理 5.5 对 RANDOMIZE-IN-PLACE 的证明（用循环不变式追踪"前缀恰为均匀 $(i-1)$-排列"）正是同一思想的变体。顺带一提，RANDOMIZE-IN-PLACE 就是 Fisher–Yates shuffle（费雪–耶茨洗牌）的现代版本：据离线维基百科，Fisher 与 Yates 于 1938 年在统计表格书中给出纸笔版，经 Knuth 推广后又称 Knuth shuffle。最后注意本页那句提醒："每个元素落到每个位置的概率均为 $1/n$"并不足以保证均匀，习题 5.3-4 的循环移位就是反例——所以必须整条链一起证，而不是逐元素了事。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段递归是 reservoir sampling（蓄水池采样）思想的雏形，值得提前认识：它单遍扫描、只用 $m$ 次随机调用，就从 $n$ 个元素中等可能地抽出 $m$-子集——这正是"数据只能流过一遍、不能回头"场景（未来流式算法的核心约束）所需的采样器。其正确性完全建立在 6.042J 的对称性与归纳上：对前 $n-1$ 个元素用归纳假设得到等可能的 $(m-1)$-子集；再看第 $n$ 个元素，它以 $m/n$ 概率入样（挤掉谁由对称性保证均匀），以 $1 - m/n$ 概率样本不变，两种情形下每个 $m$-子集出现的概率都相等。与"RANDOMIZE-IN-PLACE 后取前 $m$ 个"相比，随机调用从 $n$ 次降到 $m$ 次，在 $n \gg m$ 时是数量级差距。当你学概率论（Bertsekas）时会见到更一般的条件化证明框架；第 9 章的 RANDOMIZED-SELECT 也复用"递归缩小规模 + 每层等概率"的结构。离线维基百科记载，成熟形态的蓄水池采样算法（Algorithm R）由 Jeffrey Vitter 提出。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $k = 23$（火星上 31）是概率论最著名的数字之一。据离线维基百科，该问题通常溯源于 Harold Davenport 约 1927 年的讨论，首次发表是 Richard von Mises 1939 年的版本。"23 人"之所以反直觉，是因为大脑在数"人"，而分析在数"人对"：23 人的房间里有 $\binom{23}{2} = 253$ 对可能的碰撞，与 365 天同量级，概率过半毫不奇怪——这正是阈值 $k(k-1)/2 \approx n^2/2$ 的来历，也解释了为何概率法（$k \approx 1.2\sqrt{n}$）与期望法（$\sqrt{2n}$）两种分析都给出 $\Theta(\sqrt{n})$。6.042J 里你见过两条路：直接组合计数（算"全不同"的概率）与指示器变量法（数碰撞对的期望）；后者妙在只依赖期望的线性性、完全不需要独立性，代价是只给出期望数而非"至少一对"的概率，所以书中明说这是近似分析。这套数学在密码学中有直接后代：birthday attack（生日攻击）对 $l$ 位散列找碰撞约需 $2^{l/2}$ 次尝试而非 $2^l$ 次，第 11 章散列表的碰撞分析用的也是同一套球与箱子模型。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 优惠券收集的 $b \ln b$ 值得展开两点。其一，它在第 11 章散列表中有直接回声：把 $n$ 个键随机散列到 $n$ 个槽，"最后一次命中空槽"的等待就是这里的第 $b$ 阶段；装载因子与链长分布的分析用的全是这套球与箱子模型（习题 5.4-6 请你算期望空箱数）。其二，为什么是 $\ln b$ 而非 $b$？拆开推导看：第 $i$ 阶段还剩 $b-i+1$ 个空箱，每次投掷命中率 $(b-i+1)/b$，期望等待 $b/(b-i+1)$，求和恰为调和数 $b\sum_{i=1}^{b} 1/i \approx b \ln b$——多数阶段很短，只有收尾几个顽固空箱贡献对数因子。它与生日问题的 $\sqrt{n}$ 阈值并列，是随机化分析中最常见的两个"意外常数"。若想看得更细，可用 Poisson approximation（泊松近似）：当单箱期望落球数 $\lambda = n/b$ 较小而箱子数很大时，单箱球数近似服从 Poisson($\lambda$) 分布（可理解为二项分布在"试验多、单次概率小"时的极限），由此能迅速导出"空箱约 $b e^{-\lambda}$ 个"这类公式，比精确组合计算省力得多。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里藏着一条可复用的证明模板，值得命名为「分段放缩」：求 $\mathrm{E}[L] = \sum_j j\,\Pr\{L_j\}$ 这类"取值 × 概率质量"的和时，先找一个阈值 $t$（此处 $t = 2\lceil\lg n\rceil$）把求和劈成两段——低段用"$j \le t$"放大取值、用 $\sum \Pr\{L_j\} \le 1$ 收缩质量；高段用"概率质量 $< 1/n$"收缩（由 Boole 不等式把 $n$ 个单点概率求和）、用 $j \le n$ 放大取值。两段各贡献 $O(t)$ 与 $O(1)$，相加即得 $O(\lg n)$。注意 Boole 不等式（union bound，联合界）在其中的关键角色：各事件 $A_{ik}$ 高度相关、根本不独立，但联合界照用不误——它只要求"并的概率不超过概率之和"，这正是它成为随机算法分析第一工具的原因（生日问题的直接计数里你已见过它的雏形）。你还能在 100B 里认出这个形状：它是离散版的尾部控制——期望被"取值上界 × 尾部质量"与"概率质量 × 取值界"两端夹出，与连续情形下 $\mathrm{E}[L] = \int_0^\infty \Pr\{L > t\}\,dt$ 的分部积分思想同源。以后遇到"期望规模"类问题，先问一句：能不能找到阈值，把质量劈成两半？

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 至此上下界合拢，值得把整场证明的骨架抽出来命名——「上下界夹逼」（在随机变量上的重演）：上界靠"单点概率 $\le 1/2^k$ + Boole 联合界"证明长序列几乎不出现；下界靠「分组放缩」证明短于 $\lfloor(\lg n)/2\rfloor$ 的序列也几乎不出现——把 $n$ 次抛掷切成约 $n/s$ 组互不相交的组，每组全为正面的概率 $\ge 1/\sqrt{n}$，于是"所有组皆败"的概率 $\le (1-1/\sqrt{n})^{n/s} \le e^{-n/(s\sqrt{n})} = O(1/n)$，其中不等式 $1+x \le e^x$ 充当"连乘变指数衰减"的桥梁——与生日问题用它是同一招。第二个模板是「期望值探测」：定义 $X$ 为长度 $k$ 的序列个数，算出 $\mathrm{E}[X] = (n-k+1)/2^k$——$k = (1/2)\lg n$ 时 $\mathrm{E}[X] = \Theta(\sqrt{n}) \gg 1$，断言"很可能出现"；$k = c\lg n$（$c>1$）时 $\mathrm{E}[X] \to 0$，断言"几乎不出现"。这把"存在性"问题转译成"期望计数"问题，与生日的指示器分析同构。但要诚实地认清它的局限：$\mathrm{E}[X] \gg 1$ 本身并不严格蕴含"出现概率高"（严格化需要对补事件用 Markov 不等式或二阶矩方法，那是概率论课的工具），所以本节明说这是 approximate（近似）分析——知道结论的精确边界在哪，与知道结论本身同样重要。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里浮现的是著名的 secretary problem（秘书问题）的影子，本节推导的正是它的经典"先观察后决策"策略：用前 $k$ 位建立基准线，之后遇到首个破纪录者立即出手。最优点 $k = n/e$ 与成功率 $1/e \approx 37\%$ 是同一枚硬币的两面：对 $(k/n)(\ln n - \ln k)$ 求导置零恰得 $\ln(n/k) = 1$，即"观察期长度"与"成功概率"由同一个 $e$ 统治。直觉上，$k$ 太小则基准线太弱（容易被早期的平庸者骗走唯一的雇佣名额），$k$ 太大则最优人选可能已在观察期被放走；$n/e$ 恰好平衡这两种损失。支撑推导的是两件你已有的工具：其一，$\Pr\{O_i\} = k/(i-1)$ 用的是 6.042J 的对称性论证（前 $i-1$ 位中的最大值等可能落在任何位置）；其二，用不等式 (A.12) 把调和和 $\sum 1/i$ 用 $\int dx/x$ 上下夹逼——这是 100B 中"单调递减函数的求和与积分互估"的标准手法，被积函数单调时积分是级数的天然夹具。还有一个反直觉的副产品值得咀嚼：成功率 $1/e$ 不随 $n$ 增大而衰减——只要愿意接受"接近最好"，这个问题的难度对规模是免疫的；这类"先观察后出手"（optimal stopping，最优停时）的思想在你之后学在线算法与决策理论时会以更一般的面貌重现。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题是 Morris counter（莫里斯计数器）的入门。据离线维基百科，Robert Morris 于 1977 年在贝尔实验室发明该算法，动机是真实的工程约束：统计网络中的大数时寄存器位数不够，于是"以精度换容量"，让 $b$ 位计数器只存量级指数（取 $n_i = 2^{i-1}$ 时可数到约 $2^{2^b}$ 量级）。题目中的随机增量规则保证了无偏性（(a) 小问：$n$ 次递增后期望恰为 $n$），方差由序列 $n_i$ 的选取控制（(b) 小问）。其历史地位在于被公认为 streaming algorithms（流式算法）的先驱之一：20 世纪 80 年代初 Philippe Flajolet 对它做了完整分析并命名 approximate counting（近似计数），而"单遍扫描、次线性内存、近似回答"三要素日后发展为 1996 年 Alon、Matias 与 Szegedy 建立的流式算法理论（该论文于 2005 年获哥德尔奖）。做这道题时请体会范式转换：随机化把"精确计数"换成"无偏估计"——这与 §5.3 把"最坏情况"概率化是同一哲学的两面。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这页 Notes 背后有一段值得记录的历史。据离线维基百科：heapsort 与 binary heap（二叉堆）由 J. W. J. Williams 于 1964 年提出（他 1930 年生于英国威尔特郡，在 Elliot Bros.（伦敦）公司工作期间完成此项工作，2012 年逝世）；同年 Robert W. Floyd 发表了改进版本，使数组可以原地完成排序——它延续自 Floyd 对 treesort 的早期研究，也就是今天 BUILD-MAX-HEAP 配合 HEAPSORT 的形态。Williams 的论文还首次把堆确立为独立的数据结构，直接催生了优先队列的高效实现（即 6.5 节）：EXTRACT-MAX 与 INSERT 都只需 $O(\lg n)$，而此前用有序数组摘最大值、用无序数组做插入都免不了 $O(n)$。Notes 提到的 "secretary problems"（秘书问题）你在 5.4.4 节已见其 37% 策略；Karp 与 Rabin 的综述（文献 [200] 与 [288]）则标志着 20 世纪 70 年代末随机化算法成为独立研究领域。一个成果同时开创"排序算法、数据结构、抽象数据类型"三条线索，在算法史上并不多见。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第 8 章的比较排序下界，可以提前用 6.042J 的知识看穿：任何比较排序的执行过程都能画成一棵 decision tree（决策树）——每个内结点是一次比较（两个分支），每个叶结点是一种输出排列。$n$ 个元素有 $n!$ 种可能排列，每一种都必须对应至少一个叶子；而 6.042J 告诉我们高度为 $h$ 的二叉树至多 $2^h$ 个叶子，故 $2^h \ge n!$，即 $h \ge \lg n! = \Theta(n \lg n)$（用 Stirling 近似展开 $\lg n!$），这就是 $\Omega(n \lg n)$ 的全部骨架——排序所需的"信息"必须一次一比特地买回来。计数排序与基数排序绕过下界的方式则更根本：它们根本不做比较，而是"用值本身当下标"（array indexing）直接定位，等于预先用空间把答案编排好，下界的"比较"前提对它们失效。这提醒你：每个下界都绑定一个计算模型，出了模型就没有下界——同样的觉悟在第 9 章的线性时间选择算法中会再次出现。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这张表值得当成"选型速查"来读，而不是死记。决策路径大致是：$n$ 很小（几十以内）→ 插入排序，紧凑内循环带来的低常数与原地性压倒渐近劣势；需要稳定（排序键相同的记录保持原有相对次序）→ 归并排序或第 8 章的计数/基数排序，快排与堆排都不稳定；键是 $[0..k]$ 内的小整数 → 计数排序直接用值当下标，$\Theta(k+n)$；键均匀分布在已知区间 → 桶排序期望 $\Theta(n)$；通用大数组 → 以快排为主（期望 $O(n \lg n)$、常数小），第 7 章会看到工业实现通常叠加堆排序兜底最坏情况。注意两个容易漏看的细节：其一，heapsort 的平均情形一栏是"—"，因为本书没有分析它（实际上它是 $\Theta(n \lg n)$，习题 6.4-5 给出元素互异时最好情形也有 $\Omega(n \lg n)$，所以它是最稳定的"保底"选择）；其二，桶排序最坏 $\Theta(n^2)$ 提醒你"平均"承诺背后总有分布假设——输入一旦偏离均匀，性能保证即告失效，这是第 5 章概率分析与此处工程选型的直接交会点：选随机化算法还是最坏情况算法，取决于你信不信得起"运气差的那一次"。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么完全二叉树塞进数组可以零指针？第一性原理：指针式树需要指针，是因为结点在内存中彼此无关、父子关系只能显式记录；而完全二叉树的形状被"逐层自左填满"唯一固定，$\lfloor i/2 \rfloor$、$2i$、$2i+1$ 这组下标算术就把整棵树的拓扑编码进了下标本身——这是用"规律性形状"换"显式链接"的经典交易。CSAPP 给过你评估这笔交易的尺子：链式存储结点散落各处，每条指针既是额外空间也是一次潜在的 cache miss；连续数组则享受 spatial locality（空间局部性），顺序访问时缓存行整批预取。本页的位运算是这笔交易的进一步红利：LEFT 即 $i$ 左移一位，PARENT 即右移一位——2 的幂让乘除退化为移位，这是"数据结构内存布局影响指令级性能"的直接例证。代价也要看清：数组表示要求结构近乎完全、不适合中途增删结点，所以第 13 章的红黑树仍需指针；堆选数组，是因为它的操作只沿父子路径行走，用不到任意位置的增删。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 「层数翻倍」是给堆量高度的标准数法：完全二叉树第 $h$ 层至多 $2^h$ 个结点，于是高度 $\ge h$ 的堆至少有 $2^h$ 个结点、高度 $\ge h+1$ 的堆至少有 $2^{h+1}$ 个——把 $n$ 夹在 $2^h$ 与 $2^{h+1}$ 之间，就钉死 $h = \lfloor \lg n \rfloor$（习题 6.1-2 要你自己写出这两步夹逼）。这是 6.042J 中"满二叉树第 $h$ 层有 $2^h$ 个结点"这一计数引理的直接重演，只是把对象从证明题换成了数据结构的标尺。为什么全书都要先钉死这个数？因为本页末列出的每个基本过程（MAX-HEAPIFY、BUILD-MAX-HEAP、HEAPSORT 及四个优先队列操作）的运行时间都以高度为自变量——先证"高度 $= \Theta(\lg n)$"这把尺子，后面每个 $O(\lg n)$ 才有据可查。反例检验：$n = 1$ 时 $\lfloor \lg 1 \rfloor = 0$，单结点堆的高度为零条边，与"按 simple downward path 的边数计高"的定义一致；若改按结点数计高，所有结论都会整体偏差 1，这正是定义强调"边数"的原因。（操作）的运行时间至多与树的高度成正比，因而耗时 $O(\lg n)$。本章余下部分将介绍一些基本 procedures（过程），并展示它们如何用在一种 sorting algorithm（排序算法）和一种 priority-queue data structure（优先队列数据结构）中。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么孩子子树至多 $2n/3$？回到完全二叉树的形状约束做最坏情形构造：设整树高度为 $h$，除最底层外全满。最重的孩子子树出现在"最底层恰好半满、且这些结点全挂在同一侧"时——此时该侧子树除了独占上方满层（约 $2^{h-1}$ 个结点），还拿走最底层的一半（约 $2^{h-1}$ 个），合计约 $2^h$ 个；而整树约 $3 \cdot 2^{h-1}$ 个，比值恰趋于 $2/3$。这不是巧合，而是"递归树上取最重分支"的标准论证：分析递归成本时不必精确知道每棵子树多大，只需证明最重分支的规模占比被一个常数钉死——递归式 $T(n) \le T(2n/3) + \Theta(1)$ 由此而来，master theorem（主定理）的情形 2 给出 $\Theta(\lg n)$。若嫌主定理间接，还有更朴素的第二把尺子：MAX-HEAPIFY 每层递归使结点下降一层，故耗时 $O(h)$，而堆高 $\lfloor \lg n \rfloor$ 已在 §6.1 钉死。两种算法（主定理、按层计数）给出同一答案，互为验证——这正是"先证后信"喜欢的双保险。习题 6.2-6 还要求你构造让递归走满一条根到叶路径的输入，把下界 $\Omega(\lg n)$ 补齐，使结论成为紧确界。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么"对 $n$ 个结点各做一次堆化"居然只要 $O(n)$？第一性原理：成本不该按结点个数平均分摊，而应按各结点的高度计价——MAX-HEAPIFY 在高度 $h$ 的结点上花 $O(h)$，而完全二叉树里多数结点住在低层：恰好一半是叶（高度 0，零成本），四分之三的结点高度不超过 1。把"高度 $h$ 的结点至多 $\lceil n/2^{h+1} \rceil$ 个"（习题 6.3-3）与 $O(h)$ 相乘再对 $h$ 求和，得到 $n\sum_h h/2^h$；代入公式 (A.8)（$x = 1/2$ 的等比级数求和）得 $\sum h/2^h = 2$，总成本 $O(2n) = O(n)$。这个"按高度计价"的账本是加权求和思想的直接应用：级数收敛意味着少数高层结点的高成本被多数低层结点摊薄——几何直觉是"越往上，结点越稀、权越轻"。对比朴素的替代方案：逐个调用 MAX-HEAP-INSERT 建堆要 $O(n \lg n)$，因为每次插入的路径必须一路上升到根，无法利用"下方已经整理好"的结构；自底向上正是让"两棵孩子子树已是合法堆"这一 MAX-HEAPIFY 的前提在每次调用时成立（习题 6.3-2 问的"为什么 $i$ 要递减"就是这个方向问题）。这组对比是全书第一个"同一数据结构、不同构造顺序、复杂度差一个对数因子"的实例，第 7 章快排的期望分析与这里有同源的求和手法。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 把循环不变式当模板来收藏：HEAPSORT 的正确性（习题 6.4-2 给出了不变式原文）由"每轮循环开始时，$A[1..i]$ 是含 $i$ 个最小元素的 max-heap，$A[i+1..n]$ 含 $n-i$ 个最大元素且已排序"保证，初始化、保持、终止三步骨架与 chunk01 里插入排序的不变式（"$A[1..j-1]$ 是已排序的前缀"）完全同构——你学的不是某个具体证明，而是"前缀/后缀分解 + 三步归纳"这一可迁移框架。精髓在两处不变式的强弱取舍：插入排序维护"前缀全序"这一强性质，维护代价 $O(n)$（逐个比较后移）；堆排序只维护"前缀成堆"这一弱性质——堆序弱于全序（只约束父子、不约束兄弟），却足以每轮 $O(\lg n)$ 地榨出当前最大值放进前缀末端。这是算法设计的重要一课：不变式越弱、维护越便宜，只要弱性质仍能支撑每步提取所需信息即可。终止时 $i = 1$，后缀已扩成整个数组且有序，正确性水到渠成。与第 5 章引理 5.5 的概率型不变式对照，你还会看到同一模板能携带概率成分——框架的普适性正是它的价值；习题 6.4-3 与 6.4-4 则请你用这个不变式去推已排序输入与最坏情形的运行时间，正好练手。

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

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 堆排序在实践这一仗上输给快排，账要算到内存层次结构头上——正是 CSAPP 第 6 章给你的视角。MAX-HEAPIFY 沿树下降时，下标从 $i$ 走到 $2i$ 或 $2i+1$：每层访问的地址大约翻倍，是典型的"大步长跳跃访问"，相邻两次访存相距越来越远，一个 64 字节的缓存行往往只服务一两次访问，spatial locality（空间局部性）近乎为零；而第 7 章快排的划分过程对数组做顺序双向扫描，每次访存都搭预取器的便车，缓存行被整批消费。渐近复杂度同为 $O(n \lg n)$，常数因子却可能差出数倍——这正是 Part II 导言把 memory hierarchy（存储层次结构）列为工程因素的用意。工业界的折中是 introsort 一类的混合策略：以快排为主力，递归深度超限时切换到堆排序兜底（保住 $O(n \lg n)$ 最坏保证），小片段再交插入排序，三者各取所长；Python 与 Java 的内置排序则走归并路线并追求稳定性。堆排序并未出局：它无递归栈、无退化输入，在内存受限与实时性要求下仍是可靠备胎，习题 6.4-5 更证明了元素互异时它连最好情形也是 $\Omega(n \lg n)$——这份"倔强"恰是它担任保镖的资格。

priority queue 是一种用于维护一个由元素构成的 set（集合）$S$ 的 data structure（数据结构），其中的每个元素都有一个与之关联的值，称为 key（关键字）。max-priority queue 支持下列 operations（操作）：

INSERT(S, x) 把 element（元素）$x$ 插入集合 $S$ 中，这一操作等价于 $S = S \cup \{x\}$。

MAXIMUM(S) 返回 $S$ 中拥有最大 key（关键字）的元素。

EXTRACT-MAX(S) 去掉并返回 $S$ 中拥有最大关键字的元素。

INCREASE-KEY(S, x, k) 将元素 $x$ 的关键字的值增大到新值 $k$，这里假定 $k$ 至少与 $x$ 当前的关键字的值一样大。

在诸多其他应用之中，我们可以用最大优先队列在一台 shared computer（共享计算机）上调度 jobs（作业）。最大优先队列记录着有待执行的作业及它们各自的相对 priorities（优先级）。当一个作业完成或被中断时，scheduler（调度器）通过调用 EXTRACT-MAX，从所有待处理的作业中选出优先级最高的那个作业。调度器随时都可以通过调用 INSERT 把一个新作业加入 queue（队列）。

或者，min-priority queue（最小优先队列）支持 INSERT、MINIMUM、EXTRACT-MIN 和 DECREASE-KEY 操作。最小优先队列可以用于 event-driven simulator（事件驱动的模拟器）。queue 中的 items（项）是要模拟的 events（事件），每个事件都带有一个关联的发生时间，这个时间充当它的 key（关键字）。各事件必须按其发生时间的顺序来模拟，因为对某一事件的模拟可能会导致其他事件在未来被模拟。模拟程序在每一步都调用 EXTRACT-MIN 来选出下一个要模拟的事件。每当新的事件被产生出来时，模拟器就通过调用 INSERT 把它们插入最小优先队列。（接下页）
