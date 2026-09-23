# Introduction to Algorithms（算法导论）· Third Edition（第三版）

> <span style="color:#7f8c8d;">CLRS 双语翻译 · chunk06 · 书页 203–242 · 由 clrs_translate 流水线生成</span>

> <span style="color:#7f8c8d;">CLRS §8.4 Bucket sort（桶排序）· 续, p.203</span>

## Section 8.4 · Bucket sort（桶排序）· 续 <span style="color:#2471a3;">**[section]**</span>

```math
\mathrm{E}[n_i^2] = \mathrm{E}\left[\left(\sum_{j=1}^{n} X_{ij}\right)^{2}\right] = \mathrm{E}\left[\sum_{j=1}^{n}\sum_{k=1}^{n} X_{ij}X_{ik}\right] = \mathrm{E}\left[\sum_{j=1}^{n} X_{ij}^{2} + \sum_{1 \le j \le n} \sum_{\substack{1 \le k \le n \\ k \ne j}} X_{ij}X_{ik}\right] = \sum_{j=1}^{n}\mathrm{E}\left[X_{ij}^{2}\right] + \sum_{1 \le j \le n} \sum_{\substack{1 \le k \le n \\ k \ne j}} \mathrm{E}\left[X_{ij}X_{ik}\right], \tag{8.3}
```

其中，最后一行由 linearity of expectation（期望的线性性）得出。我们分别计算这两个 summations（求和式）。Indicator random variable（指示器随机变量）$X_{ij}$ 取值为 1 的 probability（概率）为 $1/n$，否则取值为 0，因此

$\mathrm{E}\left[X_{ij}^{2}\right] = 1^{2} \cdot \dfrac{1}{n} + 0^{2} \cdot \left(1 - \dfrac{1}{n}\right) = \dfrac{1}{n}$。

当 $k \ne j$ 时，random variables（随机变量）$X_{ij}$ 与 $X_{ik}$ 相互 independent（独立），于是

$\mathrm{E}\left[X_{ij}X_{ik}\right] = \mathrm{E}\left[X_{ij}\right]\,\mathrm{E}\left[X_{ik}\right] = \dfrac{1}{n} \cdot \dfrac{1}{n} = \dfrac{1}{n^{2}}$。

把这两个 expected values（期望值）代入 equation (8.3)（式 (8.3)），我们得到

```math
\mathrm{E}[n_i^2] = \sum_{j=1}^{n}\frac{1}{n} + \sum_{1 \le j \le n} \sum_{\substack{1 \le k \le n \\ k \ne j}} \frac{1}{n^{2}} = n \cdot \frac{1}{n} + n(n-1) \cdot \frac{1}{n^{2}} = 1 + \frac{n-1}{n} = 2 - \frac{1}{n},
```

这就证明了 equation (8.2)（式 (8.2)）。

---

> <span style="color:#7f8c8d;">CLRS §8.4 Bucket sort（桶排序）· 续 / Exercises, p.204</span>

## Section 8.4 · Bucket sort（桶排序）· 续 <span style="color:#2471a3;">**[section]**</span>

在 equation (8.1)（式 (8.1)）中使用这个 expected value（期望值），我们得出 bucket sort（桶排序）的 average-case running time（平均情况运行时间）为 $\Theta(n) + n \cdot O(2 - 1/n) = \Theta(n)$。

即使 input（输入）并非取自 uniform distribution（均匀分布），bucket sort 仍可能以 linear time（线性时间）运行。只要输入具有这样的性质——各个 bucket sizes（桶的大小）的平方之和关于元素总数是 linear（线性的），equation (8.1) 就告诉我们 bucket sort 将以线性时间运行。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 回到最基础的假设：桶排序的 $\Theta(n)$ 期望不是"算法突然变聪明了"，而是"信息来源变了"。比较排序只能靠两两比较获取次序信息，被 $\Omega(n\lg n)$ 的信息论下界卡死；桶排序则直接假设输入服从均匀分布，于是"分桶"这一步 $O(n)$ 就让每个元素大致各就各位，桶内只剩零星几个元素交给插入排序收拾——本页式 (8.2) 的计算正是在量化"桶有多均匀"：均匀输入下每个桶期望只装约 1 个元素，$\mathrm{E}[n_i^2]\approx 2$，故 $\sum\mathrm{E}[n_i^2]=O(n)$。与计数排序、基数排序对照，三者是同一策略的三个化身：计数排序利用"键是 $0..k$ 内整数"、基数排序利用"键可拆成 $d$ 位"、桶排序利用"键服从已知分布"——都是用键的结构信息绕过比较下界，代价都是对输入做更强的假设。习题 8.4-5 正是这一思想的推广：对任意可在 $O(1)$ 内求值的连续分布 $P$，用累积分布函数 $P(x)$ 本身当分桶函数即可恢复线性期望。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**8.4-1**
Using Figure 8.4 as a model, illustrate the operation of BUCKET-SORT on the array $A = \langle .79, .13, .16, .64, .39, .20, .89, .53, .71, .42 \rangle$.

**8.4-2**
Explain why the worst-case running time for bucket sort is $\Theta(n^2)$. What simple change to the algorithm preserves its linear average-case running time and makes its worst-case running time $O(n \lg n)$?

**8.4-3**
Let $X$ be a random variable that is equal to the number of heads in two flips of a fair coin. What is $\mathrm{E}[X^2]$? What is $\mathrm{E}^2[X]$?

**8.4-4 ★**
We are given $n$ points in the unit circle, $p_i = (x_i, y_i)$, such that $0 < x_i^2 + y_i^2 \le 1$ for $i = 1, 2, \ldots, n$. Suppose that the points are uniformly distributed; that is, the probability of finding a point in any region of the circle is proportional to the area of that region. Design an algorithm with an average-case running time of $\Theta(n)$ to sort the $n$ points by their distances $d_i = \sqrt{x_i^2 + y_i^2}$ from the origin. (Hint: Design the bucket sizes in BUCKET-SORT to reflect the uniform distribution of the points in the unit circle.)

**8.4-5 ★**
A probability distribution function $P(x)$ for a random variable $X$ is defined by $P(x) = \Pr\{X \le x\}$. Suppose that we draw a list of $n$ random variables $X_1, X_2, \ldots, X_n$ from a continuous probability distribution function $P$ that is computable in $O(1)$ time. Give an algorithm that sorts these numbers in linear average-case time.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8, p.205</span>

## Problems（本章问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-1 · Probabilistic lower bounds on comparison sorting（比较排序的概率下界） <span style="color:#2471a3;">**[problem]**</span>

In this problem, we prove a probabilistic $\Omega(n \lg n)$ lower bound on the running time of any deterministic or randomized comparison sort on $n$ distinct input elements. We begin by examining a deterministic comparison sort $A$ with decision tree $T_A$. We assume that every permutation of $A$'s inputs is equally likely.

a. Suppose that each leaf of $T_A$ is labeled with the probability that it is reached given a random input. Prove that exactly $n!$ leaves are labeled $1/n!$ and that the rest are labeled 0.

b. Let $D(T)$ denote the external path length of a decision tree $T$; that is, $D(T)$ is the sum of the depths of all the leaves of $T$. Let $T$ be a decision tree with $k > 1$ leaves, and let $L_T$ and $R_T$ be the left and right subtrees of $T$. Show that $D(T) = D(L_T) + D(R_T) + k$.

c. Let $d(k)$ be the minimum value of $D(T)$ over all decision trees $T$ with $k > 1$ leaves. Show that $d(k) = \min_{1 \le i \le k-1} \{d(i) + d(k - i) + k\}$. (Hint: Consider a decision tree $T$ with $k$ leaves that achieves the minimum. Let $i_0$ be the number of leaves in $L_T$ and $k - i_0$ the number of leaves in $R_T$.)

d. Prove that for a given value of $k > 1$ and $i$ in the range $1 \le i \le k - 1$, the function $i \lg i + (k - i) \lg(k - i)$ is minimized at $i = k/2$. Conclude that $d(k) = \Omega(k \lg k)$.

e. Prove that $D(T_A) = \Omega(n! \lg n!)$, and conclude that the average-case time to sort $n$ elements is $\Omega(n \lg n)$.

Now, consider a randomized comparison sort $B$. We can extend the decision-tree model to handle randomization by incorporating two kinds of nodes: ordinary comparison nodes and "randomization" nodes. A randomization node models a random choice of the form RANDOM(1, $r$) made by algorithm $B$; the node has $r$ children, each of which is equally likely to be chosen during an execution of the algorithm.

f. Show that for any randomized comparison sort $B$, there exists a deterministic comparison sort $A$ whose expected number of comparisons is no more than those made by $B$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这道题值得当作一次跨课程连接来读：部分 (b)–(e) 证明的"叶子平均深度 $D(T)/k=\Omega(\lg k)$"，本质上就是信息论中熵（entropy）不等式 $\sum_i p_i\lg(1/p_i)$ 的极值形式——在 6.042J 里你见过加权平均，而熵正是"以到达概率为权的叶子深度"这一期望。抛硬币的直觉可以精确化：比较排序的每一步至多提供 1 比特的"是/否"信息，而区分 $n!$ 种等概率排列需要 $\lg(n!)=\Theta(n\lg n)$ 比特，所以"平均"比较次数（本题对叶子深度取期望，而非最坏情况）也不可能更少。部分 (b) 的递推 $D(T)=D(L_T)+D(R_T)+k$ 则是 6.042J 第二章结构归纳的标准手法：整棵树的量 = 左子树量 + 右子树量 + 根的贡献。部分 (f) 更有通用价值：给决策树添上"随机化节点"后，把随机源固定下来，随机算法就"冻结"成一个确定算法——对所有种子取期望，必有某个种子不劣于期望值，于是随机化在比较次数上不可能超越一切确定算法。"固定随机源"这一论证模板在分析任何随机化算法的下界时都会反复出现。

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8, p.206</span>

## Problems（本章问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-2 · Sorting in place in linear time（线性时间原地排序） <span style="color:#2471a3;">**[problem]**</span>

Suppose that we have an array of $n$ data records to sort and that the key of each record has the value 0 or 1. An algorithm for sorting such a set of records might possess some subset of the following three desirable characteristics:

1. The algorithm runs in $O(n)$ time.
2. The algorithm is stable.
3. The algorithm sorts in place, using no more than a constant amount of storage space in addition to the original array.

a. Give an algorithm that satisfies criteria 1 and 2 above.

b. Give an algorithm that satisfies criteria 1 and 3 above.

c. Give an algorithm that satisfies criteria 2 and 3 above.

d. Can you use any of your sorting algorithms from parts (a)–(c) as the sorting method used in line 2 of RADIX-SORT, so that RADIX-SORT sorts $n$ records with $b$-bit keys in $O(bn)$ time? Explain how or why not.

e. Suppose that the $n$ records have keys in the range from 1 to $k$. Show how to modify counting sort so that it sorts the records in place in $O(n + k)$ time. You may use $O(k)$ storage outside the input array. Is your algorithm stable? (Hint: How would you do it for $k = 3$?)

### Problem 8-3 · Sorting variable-length items（变长项的排序） <span style="color:#2471a3;">**[problem]**</span>

a. You are given an array of integers, where different integers may have different numbers of digits, but the total number of digits over all the integers in the array is $n$. Show how to sort the array in $O(n)$ time.

b. You are given an array of strings, where different strings may have different numbers of characters, but the total number of characters over all the strings is $n$. Show how to sort the strings in $O(n)$ time.

(Note that the desired order here is the standard alphabetical order; for example, $a < ab < b$.)

### Problem 8-4 · Water jugs（水罐问题） <span style="color:#2471a3;">**[problem]**</span>

Suppose that you are given $n$ red and $n$ blue water jugs, all of different shapes and sizes. All red jugs hold different amounts of water, as do the blue ones. Moreover, for every red jug, there is a blue jug that holds the same amount of water, and vice versa.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8, p.207</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-4 · Water jugs（水罐问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

Your task is to find a grouping of the jugs into pairs of red and blue jugs that hold the same amount of water. To do so, you may perform the following operation: pick a pair of jugs in which one is red and one is blue, fill the red jug with water, and then pour the water into the blue jug. This operation will tell you whether the red or the blue jug can hold more water, or that they have the same volume. Assume that such a comparison takes one time unit. Your goal is to find an algorithm that makes a minimum number of comparisons to determine the grouping. Remember that you may not directly compare two red jugs or two blue jugs.

a. Describe a deterministic algorithm that uses $\Theta(n^2)$ comparisons to group the jugs into pairs.

b. Prove a lower bound of $\Omega(n \lg n)$ for the number of comparisons that an algorithm solving this problem must make.

c. Give a randomized algorithm whose expected number of comparisons is $O(n \lg n)$, and prove that this bound is correct. What is the worst-case number of comparisons for your algorithm?

### Problem 8-5 · Average sorting（平均排序） <span style="color:#2471a3;">**[problem]**</span>

Suppose that, instead of sorting an array, we just require that the elements increase on average. More precisely, we call an $n$-element array $A$ $k$-sorted if, for all $i = 1, 2, \ldots, n - k$, the following holds:

```math
\frac{\sum_{j=i}^{i+k-1} A[j]}{k} \le \frac{\sum_{j=i+1}^{i+k} A[j]}{k}.
```

a. What does it mean for an array to be 1-sorted?

b. Give a permutation of the numbers $1, 2, \ldots, 10$ that is 2-sorted, but not sorted.

c. Prove that an $n$-element array is $k$-sorted if and only if $A[i] \le A[i + k]$ for all $i = 1, 2, \ldots, n - k$.

d. Give an algorithm that $k$-sorts an $n$-element array in $O(n \lg(n/k))$ time.

We can also show a lower bound on the time to produce a $k$-sorted array, when $k$ is a constant.

e. Show that we can sort a $k$-sorted array of length $n$ in $O(n \lg k)$ time. (Hint: Use the solution to Exercise 6.5-9.)

f. Show that when $k$ is a constant, $k$-sorting an $n$-element array requires $\Omega(n \lg n)$ time. (Hint: Use the solution to the previous part along with the lower bound on comparison sorts.)

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8, p.208</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-6 · Lower bound on merging sorted lists（合并有序链表的下界） <span style="color:#2471a3;">**[problem]**</span>

The problem of merging two sorted lists arises frequently. We have seen a procedure for it as the subroutine MERGE in Section 2.3.1. In this problem, we will prove a lower bound of $2n - 1$ on the worst-case number of comparisons required to merge two sorted lists, each containing $n$ items.

First we will show a lower bound of $2n - o(n)$ comparisons by using a decision tree.

a. Given $2n$ numbers, compute the number of possible ways to divide them into two sorted lists, each with $n$ numbers.

b. Using a decision tree and your answer to part (a), show that any algorithm that correctly merges two sorted lists must perform at least $2n - o(n)$ comparisons.

Now we will show a slightly tighter $2n - 1$ bound.

c. Show that if two elements are consecutive in the sorted order and from different lists, then they must be compared.

d. Use your answer to the previous part to show a lower bound of $2n - 1$ comparisons for merging two sorted lists.

### Problem 8-7 · The 0-1 sorting lemma and columnsort（0-1 排序引理与 columnsort） <span style="color:#2471a3;">**[problem]**</span>

A compare-exchange operation on two array elements $A[i]$ and $A[j]$, where $i < j$, has the form

```
COMPARE-EXCHANGE(A, i, j)
1  if A[i] > A[j]
2      exchange A[i] with A[j]
```

After the compare-exchange operation, we know that $A[i] \le A[j]$.

An oblivious compare-exchange algorithm operates solely by a sequence of prespecified compare-exchange operations. The indices of the positions compared in the sequence must be determined in advance, and although they can depend on the number of elements being sorted, they cannot depend on the values being sorted, nor can they depend on the result of any prior compare-exchange operation. For example, here is insertion sort expressed as an oblivious compare-exchange algorithm:

```
INSERTION-SORT(A)
1  for j = 2 to A.length
2      for i = j - 1 downto 1
3          COMPARE-EXCHANGE(A, i, i + 1)
```

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8 · Problem 8-7 续, p.209</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-7 · The 0-1 sorting lemma and columnsort（0-1 排序引理与 columnsort）· 续 <span style="color:#2471a3;">**[problem]**</span>

The 0-1 sorting lemma provides a powerful way to prove that an oblivious compare-exchange algorithm produces a sorted result. It states that if an oblivious compare-exchange algorithm correctly sorts all input sequences consisting of only 0s and 1s, then it correctly sorts all inputs containing arbitrary values.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里出现一个值得命名的证明策略模板——「0-1 剥离法」（zero-one principle）：要证明一个比较序列预先固定的算法能排序任意输入，只需检查取值仅为 0/1 的输入。为什么充分？因为"oblivious（不敏于值）"意味着算法每一步 compare-exchange 做什么只取决于预先定好的下标安排，而不取决于元素取值；把每个元素按"是否大于某阈值"映射成 0/1，算法的每一步动作与原输入完全一致，于是 0/1 输入排不对，就必然能反推出某个原输入也排不对——这正是本题让你证明的逆否命题。它的用武之地远超习题：这种"固定比较序列"的模型就是比较网络（sorting network），据离线维基百科，1954 年前后由 Armstrong、Nelson 与 O'Connor 开创并申请专利，1968 年 Batcher 用它设计硬件交换网络，2000 年代以来双调排序网络更成为 GPU 并行排序的主力——比较序列固定意味着硬件可以完全并行。你不妨把 0-1 剥离法记为比较模型证明的通用武器之一，与"对手（adversary）论证"并列：前者说"任意输入的行为由 0/1 骨架决定"，后者说"最坏输入长什么样"。

You will prove the 0-1 sorting lemma by proving its contrapositive: if an oblivious compare-exchange algorithm fails to sort an input containing arbitrary values, then it fails to sort some 0-1 input. Assume that an oblivious compare-exchange algorithm X fails to correctly sort the array $A[1 \ldots n]$. Let $A[p]$ be the smallest value in $A$ that algorithm X puts into the wrong location, and let $A[q]$ be the value that algorithm X moves to the location into which $A[p]$ should have gone. Define an array $B[1 \ldots n]$ of 0s and 1s as follows:

```math
B[i] = \begin{cases} 0 & \text{if } A[i] \le A[p], \\ 1 & \text{if } A[i] > A[p]. \end{cases}
```

a. Argue that $A[q] > A[p]$, so that $B[p] = 0$ and $B[q] = 1$.

b. To complete the proof of the 0-1 sorting lemma, prove that algorithm X fails to sort array $B$ correctly.

Now you will use the 0-1 sorting lemma to prove that a particular sorting algorithm works correctly. The algorithm, columnsort, works on a rectangular array of $n$ elements. The array has $r$ rows and $s$ columns (so that $n = rs$), subject to three restrictions:

- $r$ must be even,
- $s$ must be a divisor of $r$, and
- $r \ge 2s^2$.

When columnsort completes, the array is sorted in column-major order: reading down the columns, from left to right, the elements monotonically increase.

Columnsort operates in eight steps, regardless of the value of $n$. The odd steps are all the same: sort each column individually. Each even step is a fixed permutation. Here are the steps:

1. Sort each column.
2. Transpose the array, but reshape it back to $r$ rows and $s$ columns. In other words, turn the leftmost column into the top $r/s$ rows, in order; turn the next column into the next $r/s$ rows, in order; and so on.
3. Sort each column.
4. Perform the inverse of the permutation performed in step 2.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8 · Problem 8-7 续 / Figure 8.5, p.210</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-7 · The 0-1 sorting lemma and columnsort（0-1 排序引理与 columnsort）· 续 <span style="color:#2471a3;">**[problem]**</span>

```
        (a)         (b)         (c)         (d)         (e)         (f)         (g)         (h)         (i)
      10 14  5    4  1  2    4  8 10    1  3  6    1  4 11    1  4 11    5 10 16    4 10 16    1  7 13
       8  7 17    8  3  5   12 16 18    2  5  7    3  8 14    2  8 12    6 13 17    5 11 17    2  8 14
      12  1  6   10  7  6    1  3  7    4  8 10    6 10 17    3  9 14    7 15 18    6 12 18    3  9 15
      16  9 11   12  9 11    9 14 15    9 13 15    2  9 12    5 10 16    1  4 11    1  7 13    4 10 16
       4 15  2   16 14 13    2  5  6   11 14 17    5 13 16    6 13 17    2  8 12    2  8 14    5 11 17
      18  3 13   18 15 17   11 13 17   12 16 18    7 15 18    7 15 18    3  9 14    3  9 15    6 12 18
```

**Figure 8.5** columnsort 的各个步骤。(a) The input array with 6 rows and 3 columns. (b) After sorting each column in step 1. (c) After transposing and reshaping in step 2. (d) After sorting each column in step 3. (e) After performing step 4, which inverts the permutation from step 2. (f) After sorting each column in step 5. (g) After shifting by half a column in step 6. (h) After sorting each column in step 7. (i) After performing step 8, which inverts the permutation from step 6. The array is now sorted in column-major order.（即：带 6 行 3 列的输入数组；步骤 1 对每列排序后；步骤 2 转置并重排形状后；步骤 3 对每列排序后；执行步骤 4（逆转步骤 2 的排列）后；步骤 5 对每列排序后；步骤 6 按半列平移后；步骤 7 对每列排序后；执行步骤 8（逆转步骤 6 的排列）后。此时数组已按 column-major order（列主序）排好序。）

5. Sort each column.
6. Shift the top half of each column into the bottom half of the same column, and shift the bottom half of each column into the top half of the next column to the right. Leave the top half of the leftmost column empty. Shift the bottom half of the last column into the top half of a new rightmost column, and leave the bottom half of this new column empty.
7. Sort each column.
8. Perform the inverse of the permutation performed in step 6.

Figure 8.5 shows an example of the steps of columnsort with $r = 6$ and $s = 3$. (Even though this example violates the requirement that $r \ge 2s^2$, it happens to work.)

c. Argue that we can treat columnsort as an oblivious compare-exchange algorithm, even if we do not know what sorting method the odd steps use.

Although it might seem hard to believe that columnsort actually sorts, you will use the 0-1 sorting lemma to prove that it does. The 0-1 sorting lemma applies because we can treat columnsort as an oblivious compare-exchange algorithm. A（"A" 字后接下页首行 "couple of definitions"，即 "A couple of definitions…"）

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 8 · Problem 8-7 续 / Chapter notes, p.211</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 8-7 · The 0-1 sorting lemma and columnsort（0-1 排序引理与 columnsort）· 续 <span style="color:#2471a3;">**[problem]**</span>

A couple of definitions will help you apply the 0-1 sorting lemma. We say that an area of an array is clean if we know that it contains either all 0s or all 1s. Otherwise, the area might contain mixed 0s and 1s, and it is dirty. From here on, assume that the input array contains only 0s and 1s, and that we can treat it as an array with $r$ rows and $s$ columns.

d. Prove that after steps 1–3, the array consists of some clean rows of 0s at the top, some clean rows of 1s at the bottom, and at most $s$ dirty rows between them.

e. Prove that after step 4, the array, read in column-major order, starts with a clean area of 0s, ends with a clean area of 1s, and has a dirty area of at most $s^2$ elements in the middle.

f. Prove that steps 5–8 produce a fully sorted 0-1 output. Conclude that columnsort correctly sorts all inputs containing arbitrary values.

g. Now suppose that $s$ does not divide $r$. Prove that after steps 1–3, the array consists of some clean rows of 0s at the top, some clean rows of 1s at the bottom, and at most $2s - 1$ dirty rows between them. How large must $r$ be, compared with $s$, for columnsort to correctly sort when $s$ does not divide $r$?

h. Suggest a simple change to step 1 that allows us to maintain the requirement that $r \ge 2s^2$ even when $s$ does not divide $r$, and prove that with your change, columnsort correctly sorts.

### Chapter notes（本章注记） <span style="color:#2471a3;">**[reference]**</span>

The decision-tree model for studying comparison sorts was introduced by Ford and Johnson [110]. Knuth's comprehensive treatise on sorting [211] covers many variations on the sorting problem, including the information-theoretic lower bound on the complexity of sorting given here. Ben-Or [39] studied lower bounds for sorting using generalizations of the decision-tree model.

Knuth credits H. H. Seward with inventing counting sort in 1954, as well as with the idea of combining counting sort with radix sort. Radix sorting starting with the least significant digit appears to be a folk algorithm widely used by operators of mechanical card-sorting machines. According to Knuth, the first published reference to the method is a 1929 document by L. J. Comrie describing punched-card equipment. Bucket sorting has been in use since 1956, when the basic idea was proposed by E. J. Isaac and R. C. Singleton [188].

Munro and Raman [263] give a stable sorting algorithm that performs $O(n^{1+\epsilon})$ comparisons in the worst case, where $0 < \epsilon \le 1$ is any fixed constant. Although

---

> <span style="color:#7f8c8d;">CLRS Chapter notes for Chapter 8（本章注记）, p.212</span>

### Chapter notes（本章注记）· 续 <span style="color:#2471a3;">**[reference]**</span>

any of the $O(n \lg n)$-time algorithms make fewer comparisons, the algorithm by Munro and Raman moves data only $O(n)$ times and operates in place.

The case of sorting $n$ $b$-bit integers in $o(n \lg n)$ time has been considered by many researchers. Several positive results have been obtained, each under slightly different assumptions about the model of computation and the restrictions placed on the algorithm. All the results assume that the computer memory is divided into addressable $b$-bit words. Fredman and Willard [115] introduced the fusion tree data structure and used it to sort $n$ integers in $O(n \lg n / \lg \lg n)$ time. This bound was later improved to $O(n\sqrt{\lg n})$ time by Andersson [16]. These algorithms require the use of multiplication and several precomputed constants. Andersson, Hagerup, Nilsson, and Raman [17] have shown how to sort $n$ integers in $O(n \lg \lg n)$ time without using multiplication, but their method requires storage that can be unbounded in terms of $n$. Using multiplicative hashing, we can reduce the storage needed to $O(n)$, but then the $O(n \lg \lg n)$ worst-case bound on the running time becomes an expected-time bound. Generalizing the exponential search trees of Andersson [16], Thorup [335] gave an $O(n(\lg \lg n)^2)$-time sorting algorithm that does not use multiplication or randomization, and it uses linear space. Combining these techniques with some new ideas, Han [158] improved the bound for sorting to $O(n \lg \lg n \lg \lg \lg n)$ time. Although these algorithms are important theoretical breakthroughs, they are all fairly complicated and at the present time seem unlikely to compete with existing sorting algorithms in practice.

The columnsort algorithm in Problem 8-7 is by Leighton [227].

---

> <span style="color:#7f8c8d;">CLRS Chapter 9, p.213</span>

## Chapter 9（第 9 章）· Medians and Order Statistics（中位数与顺序统计量）

一个包含 $n$ 个元素的 set（集合）的第 $i$ 个 order statistic（顺序统计量）就是其中第 $i$ 小的 element（元素）。例如，minimum（最小值）是第 1 个顺序统计量（$i = 1$），maximum（最大值）是第 $n$ 个顺序统计量（$i = n$）。非正式地说，median（中位数）是集合的"半程点"（halfway point）：当 $n$ 为奇数时，中位数唯一，出现在 $i = (n+1)/2$ 处；当 $n$ 为偶数时，有两个中位数，分别出现在 $i = n/2$ 与 $i = n/2 + 1$ 处。因此，无论 $n$ 的奇偶性（parity）如何，中位数都出现在 $i = \lfloor (n+1)/2 \rfloor$（即 lower median，下中位数）与 $i = \lceil (n+1)/2 \rceil$（即 upper median，上中位数）处。不过，为行文简便，本书始终用短语 "the median"（中位数）指称下中位数。

本章讨论从一个包含 $n$ 个互不相同数的集合中 select（选择）第 $i$ 个顺序统计量的问题。为方便起见，我们假设集合中的数互不相同（distinct）——尽管我们所做的几乎所有工作都可以推广到集合含重复值的情形。我们将 selection problem（选择问题）形式化描述如下：

**Input（输入）：** 一个由 $n$ 个（互不相同的）数组成的集合 $A$，以及一个整数 $i$，其中 $1 \le i \le n$。

**Output（输出）：** 元素 $x \in A$，它恰好大于 $A$ 中其余 $i - 1$ 个元素。

我们可以在 $O(n \lg n)$ 时间内求解选择问题，因为可以先用 heapsort（堆排序）或 merge sort（归并排序）对这些数排序，然后简单地索引输出数组中的第 $i$ 个元素即可。本章将给出更快的 algorithm（算法）。

在 Section 9.1（第 9.1 节）中，我们考察从一个元素集合中选取 minimum 与 maximum 的问题。更有趣的是一般性的选择问题，我们将在随后的两节中研究它。Section 9.2（第 9.2 节）分析一个实用的 randomized algorithm（随机化算法），在元素互异的假设下，它达到 $O(n)$ 的 expected running time（期望运行时间）。Section 9.3（第 9.3 节）给出一个更具理论意义的算法，它在 worst case（最坏情况）下也能达到 $O(n)$ 的运行时间。

---

> <span style="color:#7f8c8d;">CLRS §9.1, p.214</span>

### Section 9.1 · Minimum and maximum（最小值与最大值） <span style="color:#2471a3;">**[section]**</span>

确定一个包含 $n$ 个元素的集合的 minimum（最小值）需要多少次 comparison（比较）？我们可以容易地得到一个 $n - 1$ 次比较的 upper bound（上界）：依次检查集合中的每个元素，并持续记录目前为止见过的最小元素。在下面的 procedure（过程）中，我们假设该集合存放在 array（数组）$A$ 中，且 $A.length = n$。

```
MINIMUM(A)
1  min = A[1]
2  for i = 2 to A.length
3      if min > A[i]
4          min = A[i]
5  return min
```

当然，用 $n - 1$ 次比较同样可以找到 maximum（最大值）。

这就是我们所能做到的最好结果吗？是的，因为对确定最小值这一问题，我们可以得到 $n - 1$ 次比较的 lower bound（下界）。可以把任何确定最小值的算法看作元素之间的一场 tournament（锦标赛），其中每次比较就是一场比赛，两个元素中较小者获胜。注意到除冠军之外的每个元素都必定至少输掉一场比赛，我们得出结论：确定最小值至少需要 $n - 1$ 次比较。因此，就所执行的比较次数而言，算法 MINIMUM 是 optimal（最优的）。

#### Simultaneous minimum and maximum（同时求最小值与最大值） <span style="color:#2471a3;">**[section]**</span>

在某些应用中，我们必须同时求出一个 $n$ 元素集合的最小值和最大值。例如，一个 graphics program（图形程序）可能需要把一组 $(x, y)$ 数据进行 scale（缩放），使其适合一个矩形显示屏（rectangular display screen）或其他图形输出设备。为此，程序必须先确定每个坐标的最小值和最大值。

到这里，如何用 $\Theta(n)$ 次比较同时确定 $n$ 个元素的最小值和最大值应该是显而易见的，而且这是 asymptotically optimal（渐近最优的）：只需分别独立地求最小值和最大值，各用 $n - 1$ 次比较，总共 $2n - 2$ 次比较。

事实上，我们可以至多用 $3\lfloor n/2 \rfloor$ 次比较同时找到最小值和最大值。做法是：同时维护到目前为止所见的最小元素和最大元素。我们不是把输入的每个元素与当前最小值和最大值各比较一次（每个元素要付出 2 次比较的代价），而是成对（in pairs）处理元素：先将输入中成对的元素彼此比较，再将较小者与当前最小值比较、较大者与当前最大值比较，即每 2 个元素付出 3 次比较的代价。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这里是「成对打包」模板的一个漂亮实例。朴素做法对每个元素各花 2 次比较（与当前 min、max 各比一次），合计约 $2n$ 次；打包做法先让两个元素互相比 1 次，而这 1 次比较的信息被复用了两次：败者从此不可能再是 max，胜者从此不可能是 min，于是每个元素只需再各比 1 次，每 2 个元素合计 3 次，得 $3\lfloor n/2\rfloor$。信息复用是关键：一次比较淘汰一个候选者，打包让这次淘汰"一石二鸟"。这一界还是最优的——习题 9.1-2★ 要求你证明下界 $\lceil 3n/2\rceil - 2$：把"仍有可能成为 min 或 max 的候选元素个数"当作状态变量，考察每次比较至多让两个候选各退出一个，计数论证便给出下界——"算法与下界相遇"意味着没有任何比较被浪费。这个"先在内部消化、再与外部比较"的打包思想还会再现：第 6 章自底向上建堆只需处理一半的元素、第 7 章三数取中都是它的变奏，值得单独记一笔。

---

> <span style="color:#7f8c8d;">CLRS §9.1–9.2, p.215</span>

如何为当前最小值和最大值设置 initial values（初始值），取决于 $n$ 是奇数还是偶数。若 $n$ 是奇数，我们就把最小值和最大值都设为第一个元素的值，然后成对处理其余元素。若 $n$ 是偶数，我们先对前 2 个元素做 1 次比较以确定最小值和最大值的初始值，然后像 $n$ 为奇数的情形那样成对处理其余元素。

让我们来分析比较的总次数。若 $n$ 是奇数，则我们执行 $3\lfloor n/2 \rfloor$ 次比较。若 $n$ 是偶数，则先执行 1 次初始比较，再执行 $3(n-2)/2$ 次比较，总计 $3n/2 - 2$ 次。因此，无论哪种情况，比较总次数都至多为 $3\lfloor n/2 \rfloor$。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

### Exercise 9.1-1 <span style="color:#2471a3;">**[exercise]**</span>

Show that the second smallest of $n$ elements can be found with $n + \lceil \lg n \rceil - 2$ comparisons in the worst case. (Hint: Also find the smallest element.)

### Exercise 9.1-2 ★ <span style="color:#2471a3;">**[exercise]**</span>

Prove the lower bound of $\lceil 3n/2 \rceil - 2$ comparisons in the worst case to find both the maximum and minimum of $n$ numbers. (Hint: Consider how many numbers are potentially either the maximum or minimum, and investigate how a comparison affects these counts.)

### Section 9.2 · Selection in expected linear time（期望线性时间的选择） <span style="color:#2471a3;">**[section]**</span>

一般的选择问题看起来比求最小值这个简单问题更困难。然而，令人惊讶的是，这两个问题的 asymptotic running time（渐近运行时间）却是相同的：$\Theta(n)$。本节给出求解选择问题的一个 divide-and-conquer（分治）算法。算法 RANDOMIZED-SELECT 以第 7 章的 quicksort（快速排序）算法为模型。与快速排序一样，我们递归地对输入数组进行 partition（划分）；但与对划分两侧都递归处理的快速排序不同，RANDOMIZED-SELECT 只处理划分的一侧。这一差别体现在分析中：quicksort 的 expected running time（期望运行时间）为 $\Theta(n \lg n)$，而 RANDOMIZED-SELECT 的期望运行时间为 $\Theta(n)$（假设元素互异）。

---

> <span style="color:#7f8c8d;">CLRS §9.2, p.216</span>

RANDOMIZED-SELECT 使用 Section 7.3（第 7.3 节）中引入的 RANDOMIZED-PARTITION 过程。因此，与 RANDOMIZED-QUICKSORT 一样，它是一个 randomized algorithm（随机化算法），因为其行为部分地由随机数生成器（random-number generator）的输出决定。下面 RANDOMIZED-SELECT 的代码返回数组 $A[p..r]$ 中第 $i$ 小的元素。

```
RANDOMIZED-SELECT(A, p, r, i)
1  if p == r
2      return A[p]
3  q = RANDOMIZED-PARTITION(A, p, r)
4  k = q - p + 1
5  if i == k               // the pivot value is the answer
6      return A[q]
7  elseif i < k
8      return RANDOMIZED-SELECT(A, p, q - 1, i)
9  else return RANDOMIZED-SELECT(A, q + 1, r, i - k)
```

RANDOMIZED-SELECT 过程的工作方式如下。第 1 行检查递归的 base case（基本情况），即子数组 $A[p..r]$ 只包含一个元素。此时必有 $i = 1$，我们在第 2 行简单地返回 $A[p]$ 作为第 $i$ 小元素。否则，第 3 行对 RANDOMIZED-PARTITION 的调用把数组 $A[p..r]$ 划分为两个（可能为空的）子数组 $A[p..q-1]$ 和 $A[q+1..r]$，使得 $A[p..q-1]$ 中的每个元素都小于或等于 $A[q]$，而 $A[q]$ 又小于 $A[q+1..r]$ 中的每个元素。与快速排序一样，我们把 $A[q]$ 称为 pivot element（主元元素）。第 4 行计算子数组 $A[p..q]$ 中元素的个数 $k$，即划分低侧（low side）的元素个数再加上主元元素本身的 1 个。第 5 行随后检查 $A[q]$ 是否就是第 $i$ 小元素。如果是，则第 6 行返回 $A[q]$。否则，算法要确定第 $i$ 小元素落在子数组 $A[p..q-1]$ 与 $A[q+1..r]$ 中的哪一个之中。若 $i < k$，则目标元素位于划分的低侧，第 8 行在该子数组中递归地选择它。而若 $i > k$，则目标元素位于划分的高侧（high side）。由于我们已经知道有 $k$ 个值小于 $A[p..r]$ 的第 $i$ 小元素——即 $A[p..q]$ 中的那些元素——目标元素就是 $A[q+1..r]$ 中第 $i - k$ 小的元素，第 9 行递归地找出它。这段代码看似允许对含 0 个元素的子数组进行递归调用，但 Exercise 9.2-1 要求你证明这种情况不可能发生。

RANDOMIZED-SELECT 的 worst-case running time（最坏情况运行时间）为 $\Theta(n^2)$，即使求最小值也是如此，因为我们可能极其不走运，总是围绕剩余的最大元素进行划分，而每次划分需要 $\Theta(n)$ 时间。不过我们将会看到，该算法具有线性的期望运行时间；并且由于它是随机化的，没有任何特定输入会必然引发其最坏情况行为。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 本节开篇点破的那个差别，将在这里兑现成递归式的"形状"：quicksort 对划分两侧都递归，$T(n)=T(k)+T(n-k-1)+\Theta(n)$，两层递归叠加出 $\Theta(n\lg n)$；而 RANDOMIZED-SELECT 是「只走一半的递归」——每次调用只进入 $A[p..q-1]$ 或 $A[q+1..r]$ 之一，递归式形如 $T(n)\le T(\max(k-1,\,n-k))+\Theta(n)$。正因为递归是一条链而非二叉分叉，"$\lg$"里的因子被省掉了：期望上规模每步近似折半，$n+n/2+n/4+\cdots<2n$，几何级数求和直接给出线性——这与二分搜索（你已掌握的分治脚手架）同构，而与归并排序（双边递归、$\Theta(n\lg n)$）相对照。最坏情况的来源也一目了然：一旦主元总落在端点，$\max(k-1,n-k)=n-1$，链不缩短，退化成 $\Theta(n^2)$——与 quicksort 的最坏情况完全同源，因为两者共享同一个 RANDOMIZED-PARTITION。"单边递归把对数变线性"是一个可迁移的判据：以后看到任何只递归一侧的分治算法（如快速选择、跳跃表的部分查询），都可用"几何级数"直觉先估一界。

---

> <span style="color:#7f8c8d;">CLRS §9.2, p.217</span>

为了分析 RANDOMIZED-SELECT 的期望运行时间，我们把在一个包含 $n$ 个元素的输入数组 $A[p..r]$ 上的运行时间看作一个随机变量（random variable），记为 $T(n)$，并按下述方式求得 $\mathrm{E}[T(n)]$ 的一个 upper bound（上界）。过程 RANDOMIZED-PARTITION 等可能地（equally likely）返回任何元素作为主元。因此，对每个满足 $1 \le k \le n$ 的 $k$，子数组 $A[p..q]$ 恰好含有 $k$ 个元素（全部小于或等于主元）的 probability（概率）为 $1/n$。对 $k = 1, 2, \ldots, n$，我们定义 indicator random variable（指示器随机变量）$X_k$：

```math
X_k = I\{\text{子数组 } A[p..q] \text{ 恰好含有 } k \text{ 个元素}\},
```

于是，假设元素互异，我们有

```math
\mathrm{E}[X_k] = 1/n\,. \tag{9.1}
```

当我们调用 RANDOMIZED-SELECT 并选择 $A[q]$ 作为主元元素时，我们无法 a priori（事先）知道究竟是会立即以正确答案终止，还是要在子数组 $A[p..q-1]$ 上递归，抑或要在子数组 $A[q+1..r]$ 上递归。这一决定取决于第 $i$ 小元素相对于 $A[q]$ 的位置。假设 $T(n)$ 是 monotonically increasing（单调递增）的，我们就可以用对最大可能输入的递归调用所需的时间来 upper-bound（上界）递归调用所需的时间。换言之，为得到一个上界，我们假设第 $i$ 个元素总是位于划分中元素较多的一侧。对一次给定的 RANDOMIZED-SELECT 调用，指示器随机变量 $X_k$ 对恰好一个 $k$ 取值为 1，而对所有其他 $k$ 取值为 0。当 $X_k = 1$ 时，我们可能在其上递归的两个子数组的规模分别为 $k - 1$ 和 $n - k$。因此，我们有 recurrence（递归式）

```math
\begin{aligned}
T(n) &\le \sum_{k=1}^{n} X_k \cdot \Bigl( T\bigl(\max(k-1,\, n-k)\bigr) + O(n) \Bigr)\\
&= \sum_{k=1}^{n} X_k \cdot T\bigl(\max(k-1,\, n-k)\bigr) + O(n)\,.
\end{aligned}
```

---

> <span style="color:#7f8c8d;">CLRS §9.2, p.218</span>

对上式取 expected values（期望值），我们得到

```math
\begin{aligned}
\mathrm{E}[T(n)] &\le \mathrm{E}\!\left[\sum_{k=1}^{n} X_k \cdot T\bigl(\max(k-1,\, n-k)\bigr) + O(n)\right]\\
&= \sum_{k=1}^{n} \mathrm{E}\bigl[X_k \cdot T(\max(k-1,\, n-k))\bigr] + O(n) && \text{(by linearity of expectation)}\\
&= \sum_{k=1}^{n} \mathrm{E}[X_k] \cdot \mathrm{E}\bigl[T(\max(k-1,\, n-k))\bigr] + O(n) && \text{(by equation (C.24))}\\
&= \sum_{k=1}^{n} \frac{1}{n} \cdot \mathrm{E}\bigl[T(\max(k-1,\, n-k))\bigr] + O(n) && \text{(by equation (9.1))}
\end{aligned}
```

其中第一处应用了 linearity of expectation（期望的线性性），第二处由 equation (C.24)（式 (C.24)）得出。为了应用式 (C.24)，我们依赖 $X_k$ 与 $T(\max(k-1,\, n-k))$ 是 independent random variables（独立随机变量）这一事实。Exercise 9.2-2 要求你对这一断言给出理由。

让我们考察表达式 $\max(k-1,\, n-k)$。我们有

```math
\max(k-1,\, n-k) =
\begin{cases}
k-1 & \text{若 } k > \lceil n/2 \rceil,\\[2pt]
n-k & \text{若 } k \le \lceil n/2 \rceil.
\end{cases}
```

若 $n$ 为偶数，则从 $T(\lceil n/2 \rceil)$ 直到 $T(n-1)$ 的每一项都在求和中恰好出现两次；若 $n$ 为奇数，则所有这些项都出现两次，而 $T(\lfloor n/2 \rfloor)$ 出现一次。于是，我们有

```math
\mathrm{E}[T(n)] \le \frac{2}{n} \sum_{k=\lfloor n/2 \rfloor}^{n-1} \mathrm{E}[T(k)] + O(n)\,.
```

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> $\frac{2}{n}$ 这个因子的来历值得拆开看：$X_k$ 取 1 的概率为 $1/n$（主元等可能地是第 $k$ 小），而 $\max(k-1,\,n-k)$ 做了两次"折叠"。其一是取值折叠——求和自变量被 $\max$ 压缩到只剩 $\lfloor n/2\rfloor$ 到 $n-1$ 这"较坏的一半"；其二是路径折叠——$T(n-2)$ 这类项可由 $k=n-1$ 与 $k=2$ 两条路径达到，$n$ 为偶数时每个自变量恰好出现两次，系数由 $1/n$ 翻倍为 $2/n$。两项合写即得 $\frac{2}{n}\sum_{k=\lfloor n/2\rfloor}^{n-1}\mathrm{E}[T(k)]$。这里还需 $X_k$ 与 $T(\max(k-1,n-k))$ 独立，式 (C.24) 才能用得上——主元落点由随机数决定，"第 $i$ 小总在较坏一侧"的最坏假设并不改变主元分布，习题 9.2-2 正要你补这一细节。最后的代换法收尾与 chunk03 中 quicksort 期望的代换同模板：猜 $\mathrm{E}[T(n)]\le cn$、代入、把余项整理成 $cn-(\cdots)$，再选 $c>4a$ 保证负项占优——"猜"的底气正是"每步扔掉一半"的几何级数直觉。

我们用 substitution（代换法）证明 $\mathrm{E}[T(n)] = O(n)$。假设 $\mathrm{E}[T(n)] \le cn$，其中常数 $c$ 满足递归式的 initial conditions（初始条件）。我们假设当 $n$ 小于某个常数时 $T(n) = O(1)$；这个常数稍后选取。我们还选取一个常数 $a$，使得上面的 $O(n)$ 项（它刻画的是算法运行时间的非递归部分，non-recursive component）对所有 $n > 0$ 都以 $an$ 为上界。利用这一 inductive hypothesis（归纳假设），我们有

```math
\begin{aligned}
\mathrm{E}[T(n)] &\le \frac{2}{n} \sum_{k=\lfloor n/2 \rfloor}^{n-1} ck + an\\
&= \frac{2c}{n}\left( \sum_{k=1}^{n-1} k - \sum_{k=1}^{\lfloor n/2 \rfloor - 1} k \right) + an
\end{aligned}
```

---

> <span style="color:#7f8c8d;">CLRS §9.2, p.219</span>

```math
\begin{aligned}
&= \frac{2c}{n}\left( \frac{(n-1)n}{2} - \frac{(\lfloor n/2 \rfloor - 1)\,\lfloor n/2 \rfloor}{2} \right) + an\\
&\le \frac{2c}{n}\left( \frac{(n-1)n}{2} - \frac{(n/2 - 2)(n/2 - 1)}{2} \right) + an\\
&= \frac{2c}{n}\left( \frac{n^2 - n}{2} - \frac{n^2/4 - 3n/2 + 2}{2} \right) + an\\
&= \frac{c}{n}\left( \frac{3n^2}{4} + \frac{n}{2} - 2 \right) + an\\
&= c\left( \frac{3n}{4} + \frac{1}{2} - \frac{2}{n} \right) + an\\
&\le \frac{3cn}{4} + \frac{c}{2} + an\\
&= cn - \left( \frac{cn}{4} - \frac{c}{2} - an \right).
\end{aligned}
```

为了完成证明，我们需要证明：对足够大的 $n$，最后这个表达式至多为 $cn$；等价地，即 $\dfrac{cn}{4} - \dfrac{c}{2} - an \ge 0$。若在两边加上 $\dfrac{c}{2}$ 并提出因子 $n$，我们得到 $n\left(\dfrac{c}{4} - a\right) \ge \dfrac{c}{2}$。只要我们选取常数 $c$ 使得 $\dfrac{c}{4} - a > 0$，即 $c > 4a$，就可以在两边除以 $\dfrac{c}{4} - a$，得到

```math
n \ge \frac{c/2}{c/4 - a} = \frac{2c}{c - 4a}\,.
```

因此，如果我们假设当 $n < \dfrac{2c}{c-4a}$ 时 $T(n) = O(1)$，那么 $\mathrm{E}[T(n)] = O(n)$。

我们的结论是：在元素互异的假设下，我们可以在期望线性时间（expected linear time）内找到任何顺序统计量（order statistic），特别是中位数（median）。

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

### Exercise 9.2-1 <span style="color:#2471a3;">**[exercise]**</span>

Show that RANDOMIZED-SELECT never makes a recursive call to a 0-length array.

### Exercise 9.2-2 <span style="color:#2471a3;">**[exercise]**</span>

Argue that the indicator random variable $X_k$ and the value $T(\max(k-1, n-k))$ are independent.

### Exercise 9.2-3 <span style="color:#2471a3;">**[exercise]**</span>

Write an iterative version of RANDOMIZED-SELECT.

---

> <span style="color:#7f8c8d;">CLRS §9.2–9.3, p.220</span>

### Exercise 9.2-4 <span style="color:#2471a3;">**[exercise]**</span>

Suppose we use RANDOMIZED-SELECT to select the minimum element of the array $A = \langle 3, 2, 9, 0, 7, 5, 4, 8, 6, 1 \rangle$. Describe a sequence of partitions that results in a worst-case performance of RANDOMIZED-SELECT.

### Section 9.3 · Selection in worst-case linear time（最坏情况线性时间的选择） <span style="color:#2471a3;">**[section]**</span>

现在我们考察一个最坏情况下运行时间为 $O(n)$ 的选择算法。与 RANDOMIZED-SELECT 类似，算法 SELECT 也是通过对输入数组递归地进行划分来找到目标元素的。但在这里，我们保证划分（partition）时能得到一次好的切分（good split）。SELECT 使用快速排序中确定性的划分算法 PARTITION（见 Section 7.1，第 7.1 节），只是做了修改，将用作划分基准的元素作为一个输入参数传入。

SELECT 算法通过执行以下步骤来确定一个包含 $n > 1$ 个互异元素的输入数组的第 $i$ 小元素。（若 $n = 1$，则 SELECT 仅仅返回其唯一的输入值作为第 $i$ 小元素。）

1. 将输入数组的 $n$ 个元素划分为 $\lfloor n/5 \rfloor$ 个每组 5 个元素的组（group of 5），以及至多一个由其余 $n \bmod 5$ 个元素组成的组。

2. 对 $\lceil n/5 \rceil$ 个组中的每一组，先用 insertion sort（插入排序）对该组元素（每组至多 5 个）排序，然后从排序后的组元素序列中挑出中位数（median），从而找出每一组的中位数。

3. 对第 2 步中找到的 $\lceil n/5 \rceil$ 个中位数，递归使用 SELECT 找出它们的中位数 $x$。（若有偶数个中位数，则按我们的约定，$x$ 是 lower median（下中位数）。）

4. 用修改后的 PARTITION，围绕 median-of-medians（中位数的中位数）$x$ 对输入数组进行划分。设 $k$ 为划分低侧（low side）元素个数加一，这样 $x$ 就是第 $k$ 小元素，并且划分高侧（high side）有 $n - k$ 个元素。

5. 若 $i = k$，则返回 $x$。否则，若 $i < k$，则在低侧递归使用 SELECT 找第 $i$ 小元素；若 $i > k$，则在高侧找第 $i - k$ 小元素。

为了分析 SELECT 的运行时间，我们首先确定大于划分元素 $x$ 的元素个数的下界。Figure 9.1（图 9.1）有助于我们直观地理解这一 bookkeeping（簿记计数）过程。第 2 步中找到的中位数至少有一半大

---

> <span style="color:#7f8c8d;">CLRS §9.3, p.221</span>

**Figure 9.1（图 9.1）** Analysis of the algorithm SELECT.（算法 SELECT 的分析。）$n$ 个元素用小圆圈表示，每组 5 个元素占据一列。各组的中位数（median）被涂白，中位数的中位数 $x$ 被标注出来。（当对偶数个元素求中位数时，我们采用 lower median（下中位数）。）箭头从较大的元素指向较小的元素，由此可以看出：在 $x$ 右侧，每个完整的 5 元素组中有 3 个元素大于 $x$；在 $x$ 左侧，每个 5 元素组中有 3 个元素小于 $x$。已知大于 $x$ 的元素显示在阴影背景上。

于 $x$ 或等于 $x$。¹ 因此，除了 5 不整除 $n$ 时那个不足 5 个元素的组、以及包含 $x$ 本身的那一个组之外，至少有一半的 $\lceil n/5 \rceil$ 个组各贡献至少 3 个大于 $x$ 的元素。把这两个组排除在外，可知大于 $x$ 的元素个数至少为

```math
3\left(\frac{1}{2}\left\lfloor \frac{n}{5} \right\rfloor - 2\right) \ge \frac{3n}{10} - 6\,.
```

类似地，至少有 $3n/10 - 6$ 个元素小于 $x$。因此，在最坏情况下，第 5 步至多对 $7n/10 + 6$ 个元素递归调用 SELECT。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 为什么每组恰好是 5 个，而不是 3 或 7？这是一笔可以心算的代数账本。$x$ 是各组中位数的中位数，所以约一半的组各自贡献至少 $\lceil g/2\rceil$ 个保证大于（或小于）$x$ 的元素，$g$ 是组大小：$g=3$ 时每侧只能保证淘汰约 $n/3$ 个元素，两个递归的自变量之和 $n/3+2n/3=n$ "不缩水"，$T(n)=T(n/3)+T(2n/3)+\Theta(n)$ 只能解出 $\Theta(n\lg n)$——这正是习题 9.3-1 要你论证的事实。$g=5$ 时每侧保证淘汰 $3n/10-6$，两递归之和 $\frac{n}{5}+\frac{7n}{10}=\frac{9n}{10}<n$，这 0.1 的"缩水率"恰好抵消划分的 $O(n)$ 开销，在下一页代换中体现为负项 $cn-(cn/10+7c+an)$。$g=7$ 也线性（和为 $\frac{6n}{7}$），但每组插入排序与找中位数的常数更大——5 是"能用且最省"的最小选择。所以整个证明的线性性完全悬在"两个递归之和严格小于 $n$"这一个不等式上；这是分析"多个递归调用"型分治的通用判据，比主定理更精细的场合（如本节）全靠它定乾坤。

现在我们可以为算法 SELECT 的 worst-case running time（最坏情况运行时间）$T(n)$ 建立一个 recurrence（递归式）。第 1、2、4 步需要 $O(n)$ 时间。（第 2 步包含 $O(n)$ 次对规模为 $O(1)$ 的集合的 insertion sort（插入排序）调用。）第 3 步耗时 $T(\lceil n/5 \rceil)$，第 5 步耗时至多 $T(7n/10 + 6)$，这里假设 $T$ 是 monotonically increasing（单调递增）的。

我们先做一个初看起来似乎没有动机的假设：任何少于 140 个元素的输入需要 $O(1)$ 时间；这一 magic constant（神奇常数）140 的来历稍后自会清楚。于是我们可以得到递归式

<span style="color:#7f8c8d;">¹ 由于我们假设这些数互不相同（distinct），除 $x$ 之外的所有中位数要么都大于 $x$，要么都小于 $x$。</span>

---

> <span style="color:#7f8c8d;">CLRS §9.3, p.222</span>

```math
T(n) \le
\begin{cases}
O(1) & \text{若 } n < 140,\\[2pt]
T(\lceil n/5 \rceil) + T(7n/10 + 6) + O(n) & \text{若 } n \ge 140.
\end{cases}
```

我们用 substitution（代换法）证明运行时间是线性的。更具体地说，我们将证明：对某个适当大的常数 $c$ 和所有 $n > 0$，有 $T(n) \le cn$。我们首先假设：对某个适当大的常数 $c$ 和所有 $n < 140$，有 $T(n) \le cn$；只要 $c$ 足够大，这一假设就成立。我们还选取一个常数 $a$，使得上面的 $O(n)$ 项（它刻画的是算法运行时间的非递归部分，non-recursive component）对所有 $n > 0$ 都以 $an$ 为上界。

将这一 inductive hypothesis（归纳假设）代入递归式的右端（right-hand side），得到

```math
\begin{aligned}
T(n) &\le c\lceil n/5 \rceil + c(7n/10 + 6) + an\\
&\le cn/5 + c + 7cn/10 + 6c + an\\
&= 9cn/10 + 7c + an\\
&= cn - (cn/10 + 7c + an),
\end{aligned}
```

当

```math
-cn/10 + 7c + an \le 0 \tag{9.2}
```

成立时，上式至多为 $cn$。

当 $n > 70$ 时，inequality (9.2)（不等式 (9.2)）等价于不等式 $c \ge 10a\,(n/(n-70))$。因为我们假设 $n \ge 140$，所以有 $n/(n-70) \le 2$，于是选取 $c \ge 20a$ 即可满足不等式 (9.2)。（注意，常数 140 并没有什么特殊之处；我们可以把它换成任何严格大于 70 的整数，然后相应地选择 $c$。）因此，SELECT 的最坏情况运行时间是线性的。

与 comparison sort（比较排序，见 Section 8.1，第 8.1 节）一样，SELECT 和 RANDOMIZED-SELECT 只通过比较元素来确定元素的相对次序（relative order）。回忆第 8 章的内容：在比较模型（comparison model）中，排序需要 $\Omega(n \lg n)$ 时间，即使是平均情况（on average，见 Problem 8-1）也是如此。第 8 章中的线性时间排序算法对输入做了假设；与此相反，本章中的线性时间选择算法不需要对输入做任何假设。它们不受 $\Omega(n \lg n)$ lower bound（下界）的约束，因为它们设法在不排序的情况下解决了选择问题。因此，像本章开篇所介绍的那样，通过"先排序再索引"来求解选择问题，在渐近意义下是 inefficient（低效的）。

---

> <span style="color:#7f8c8d;">CLRS §9.3 Selection in worst-case linear time（最坏情况线性时间的选择）· Exercises, p.223</span>

## Section 9.3 · Selection in worst-case linear time（最坏情况线性时间的选择）· 续 <span style="color:#2471a3;">**[section]**</span>

### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**9.3-1**
In the algorithm SELECT, the input elements are divided into groups of 5. Will the algorithm work in linear time if they are divided into groups of 7? Argue that SELECT does not run in linear time if groups of 3 are used.

**9.3-2**
Analyze SELECT to show that if $n \ge 140$, then at least $\lceil n/4 \rceil$ elements are greater than the median-of-medians $x$ and at least $\lceil n/4 \rceil$ elements are less than $x$.

**9.3-3**
Show how quicksort can be made to run in $O(n \lg n)$ time in the worst case, assuming that all elements are distinct.

**9.3-4 ★**
Suppose that an algorithm uses only comparisons to find the $i$th smallest element in a set of $n$ elements. Show that it can also find the $i - 1$ smaller elements and the $n - i$ larger elements without performing any additional comparisons.

**9.3-5**
Suppose that you have a "black-box" worst-case linear-time median subroutine. Give a simple, linear-time algorithm that solves the selection problem for an arbitrary order statistic.

**9.3-6**
The $k$th quantiles of an $n$-element set are the $k - 1$ order statistics that divide the sorted set into $k$ equal-sized sets (to within 1). Give an $O(n \lg k)$-time algorithm to list the $k$th quantiles of a set.

**9.3-7**
Describe an $O(n)$-time algorithm that, given a set $S$ of $n$ distinct numbers and a positive integer $k \le n$, determines the $k$ numbers in $S$ that are closest to the median of $S$.

**9.3-8**
Let $X[1..n]$ and $Y[1..n]$ be two arrays, each containing $n$ numbers already in sorted order. Give an $O(\lg n)$-time algorithm to find the median of all $2n$ elements in arrays $X$ and $Y$.

**9.3-9**
Professor Olay is consulting for an oil company, which is planning a large pipeline running east to west through an oil field of $n$ wells. The company wants to connect（接下页）

---

> <span style="color:#7f8c8d;">CLRS §9.3 Exercises · 续 / Problems, p.224</span>

**Figure 9.2（图 9.2）** Professor Olay needs to determine the position of the east-west oil pipeline that minimizes the total length of the north-south spurs.（Olay 教授需要确定东西走向输油管道的位置，使南北走向支线的总长度最小。）

**9.3-9 · 续**
a spur pipeline from each well directly to the main pipeline along a shortest route (either north or south), as shown in Figure 9.2. Given the $x$- and $y$-coordinates of the wells, how should the professor pick the optimal location of the main pipeline, which would be the one that minimizes the total length of the spurs? Show how to determine the optimal location in linear time.

## Problems（本章问题） <span style="color:#2471a3;">**[problem]**</span>

### Problem 9-1 · Largest i numbers in sorted order（按已排序顺序找出最大的 i 个数） <span style="color:#2471a3;">**[problem]**</span>

Given a set of $n$ numbers, we wish to find the $i$ largest in sorted order using a comparison-based algorithm. Find the algorithm that implements each of the following methods with the best asymptotic worst-case running time, and analyze the running times of the algorithms in terms of $n$ and $i$.

a. Sort the numbers, and list the $i$ largest.

b. Build a max-priority queue from the numbers, and call EXTRACT-MAX $i$ times.

c. Use an order-statistic algorithm to find the $i$th largest number, partition around that number, and sort the $i$ largest numbers.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 9, p.225</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 9-2 · Weighted median（加权中位数） <span style="color:#2471a3;">**[problem]**</span>

For $n$ distinct elements $x_1, x_2, \ldots, x_n$ with positive weights $w_1, w_2, \ldots, w_n$ such that $\sum_{i=1}^{n} w_i = 1$, the weighted (lower) median is the element $x_k$ satisfying

```math
\sum_{x_i < x_k} w_i < \frac{1}{2} \quad \text{and} \quad \sum_{x_i > x_k} w_i \le \frac{1}{2}.
```

For example, if the elements are $0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2$ and each element equals its weight (that is, $w_i = x_i$ for $i = 1, 2, \ldots, 7$), then the median is $0.1$, but the weighted median is $0.2$.

a. Argue that the median of $x_1, x_2, \ldots, x_n$ is the weighted median of the $x_i$ with weights $w_i = 1/n$ for $i = 1, 2, \ldots, n$.

b. Show how to compute the weighted median of $n$ elements in $O(n \lg n)$ worst-case time using sorting.

c. Show how to compute the weighted median in $\Theta(n)$ worst-case time using a linear-time median algorithm such as SELECT from Section 9.3.

The post-office location problem is defined as follows. We are given $n$ points $p_1, p_2, \ldots, p_n$ with associated weights $w_1, w_2, \ldots, w_n$. We wish to find a point $p$ (not necessarily one of the input points) that minimizes the sum $\sum_{i=1}^{n} w_i \, d(p, p_i)$, where $d(a, b)$ is the distance between points $a$ and $b$.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 加权中位数是普通中位数的一次"加权推广"，可以挂到你 6.042J 学过的累积分布语言上：把权 $w_i$ 看作离散的概率质量，加权中位数就是该分布的 $1/2$ 分位数（quantile）；部分 (a) 说明当 $w_i=1/n$（均匀质量）时它退化为普通下中位数——"中位数"本来就是"分位数"在均匀权重下的特例，两者是同一枚硬币的两面。部分 (d) 的邮局问题给了它一个物理身份：在实数轴上，把 $p$ 从左向右移过某个输入点 $p_k$ 时，目标函数 $\sum w_i|p-p_i|$ 的变化率是"左侧累计权减右侧累计权"，在累计权恰好越过 $1/2$ 的那一点变号，函数先降后升，故加权中位数取到最小——这是"分段线性凸函数在变号点取最小"的离散版本，与 18.02 里"凸函数在梯度为零处取最小"的思路一脉相承。部分 (e) 的曼哈顿距离下 $x$ 与 $y$ 两坐标独立分解，各取一次加权中位数即可。也正因为分位数与顺序统计量是同一个问题的两种语言，部分 (c) 里 SELECT 才能原封不动地以 $\Theta(n)$ 求解它。

d. Argue that the weighted median is a best solution for the 1-dimensional post-office location problem, in which points are simply real numbers and the distance between points $a$ and $b$ is $d(a, b) = |a - b|$.

e. Find the best solution for the 2-dimensional post-office location problem, in which the points are $(x, y)$ coordinate pairs and the distance between points $a = (x_1, y_1)$ and $b = (x_2, y_2)$ is the Manhattan distance given by $d(a, b) = |x_1 - x_2| + |y_1 - y_2|$.

### Problem 9-3 · Small order statistics（小顺序统计量） <span style="color:#2471a3;">**[problem]**</span>

We showed that the worst-case number $T(n)$ of comparisons used by SELECT to select the $i$th order statistic from $n$ numbers satisfies $T(n) = \Theta(n)$, but the constant hidden by the $\Theta$-notation is rather large. When $i$ is small relative to $n$, we can implement a different procedure that uses SELECT as a subroutine but makes fewer comparisons in the worst case.

---

> <span style="color:#7f8c8d;">CLRS Problems for Chapter 9 · 续, p.226</span>

## Problems（本章问题）· 续 <span style="color:#2471a3;">**[problem]**</span>

### Problem 9-3 · Small order statistics（小顺序统计量）· 续 <span style="color:#2471a3;">**[problem]**</span>

a. Describe an algorithm that uses $U_i(n)$ comparisons to find the $i$th smallest of $n$ elements, where

```math
U_i(n) =
\begin{cases}
T(n) & \text{if } i \ge n/2,\\[2pt]
\lfloor n/2 \rfloor + U_i(\lceil n/2 \rceil) + T(2i) & \text{otherwise}.
\end{cases}
```

(Hint: Begin with $\lfloor n/2 \rfloor$ disjoint pairwise comparisons, and recurse on the set containing the smaller element from each pair.)

b. Show that, if $i < n/2$, then $U_i(n) = n + O(T(2i) \lg(n/i))$.

c. Show that if $i$ is a constant less than $n/2$, then $U_i(n) = n + O(\lg n)$.

d. Show that if $i = n/k$ for $k \ge 2$, then $U_i(n) = n + O(T(2n/k) \lg k)$.

### Problem 9-4 · Alternative analysis of randomized selection（随机化选择的另一种分析） <span style="color:#2471a3;">**[problem]**</span>

In this problem, we use indicator random variables to analyze the RANDOMIZED-SELECT procedure in a manner akin to our analysis of RANDOMIZED-QUICKSORT in Section 7.4.2.

As in the quicksort analysis, we assume that all elements are distinct, and we rename the elements of the input array $A$ as $z_1, z_2, \ldots, z_n$, where $z_i$ is the $i$th smallest element. Thus, the call RANDOMIZED-SELECT$(A, 1, n, k)$ returns $z_k$.

For $1 \le i < j \le n$, let

$X_{ijk} = I\{\text{$z_i$ is compared with $z_j$ sometime during the execution of the algorithm to find $z_k$}\}$.

a. Give an exact expression for $\mathrm{E}[X_{ijk}]$. (Hint: Your expression may have different values, depending on the values of $i$, $j$, and $k$.)

b. Let $X_k$ denote the total number of comparisons between elements of array $A$ when finding $z_k$. Show that

```math
\mathrm{E}[X_k] \le 2\left(
\sum_{i=1}^{k} \sum_{j=k}^{n} \frac{1}{j - i + 1}
+
\sum_{j=k+1}^{n} \frac{j - k - 1}{j - k + 1}
+
\sum_{i=1}^{k-2} \frac{k - i - 1}{k - i + 1}
\right).
```

c. Show that $\mathrm{E}[X_k] \le 4n$.

d. Conclude that, assuming all elements of array $A$ are distinct, RANDOMIZED-SELECT runs in expected time $O(n)$.

---

> <span style="color:#7f8c8d;">CLRS Notes for Chapter 9, p.227</span>

## Chapter notes（第 9 章注释） <span style="color:#2471a3;">**[reference]**</span>

> <span style="color:#7f8c8d;">[note] 按规范，本章 notes（注释/参考文献）保留英文原文，不作翻译；文中受损的数学记号已按原书恢复。</span>

The worst-case linear-time median-finding algorithm was devised by Blum, Floyd, Pratt, Rivest, and Tarjan [50]. The fast randomized version is due to Hoare [169]. Floyd and Rivest [108] have developed an improved randomized version that partitions around an element recursively selected from a small sample of the elements. It is still unknown exactly how many comparisons are needed to determine the median. Bent and John [41] gave a lower bound of $2n$ comparisons for median finding, and Schönhage, Paterson, and Pippenger [302] gave an upper bound of $3n$. Dor and Zwick have improved on both of these bounds. Their upper bound [93] is slightly less than $2.95n$, and their lower bound [94] is $(2 + \epsilon)n$, for a small positive constant $\epsilon$, thereby improving slightly on related work by Dor et al. [92]. Paterson [272] describes some of these results along with other related work.

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这段 notes 简述了 selection problem（选择问题）研究史的三条主线：其一是 worst-case linear-time median-finding algorithm（最坏情况线性时间的中位数查找算法）的诞生——Blum、Floyd、Pratt、Rivest 与 Tarjan [50] 的这一工作正是 §9.3 中 SELECT 算法（即 median-of-medians（中位数的中位数）方法）的出处，而 Hoare [169] 的快速随机化版本则对应本章的 RANDOMIZED-SELECT。其二是"确定中位数究竟需要多少次比较"这一至今悬而未决的问题：Bent 与 John [41] 给出 $2n$ 的 lower bound（下界），Schönhage、Paterson 与 Pippenger [302] 给出 $3n$ 的 upper bound（上界），Dor 与 Zwick 随后把两侧都收紧到上界略小于 $2.95n$、下界为 $(2+\epsilon)n$（$\epsilon$ 为小的正常数）。其三是 Floyd 与 Rivest [108] 基于小子样递归选元的改进随机化版本。Paterson [272] 综述了这些及相关工作。至此，第 9 章"Medians and Order Statistics"（中位数与顺序统计量）全部结束，下一部分进入数据结构。

---

> <span style="color:#7f8c8d;">CLRS Part III, p.228</span>

> <span style="color:#7f8c8d;">[note] 本页为篇章分隔页（part-opening page），原文仅含篇章编号与篇章标题，无正文内容，故不作正文翻译。</span>

## Part III（第三部分）· Data Structures（数据结构） <span style="color:#2471a3;">**[section]**</span>

---

> <span style="color:#7f8c8d;">CLRS Part III Introduction, p.229</span>

## Part III · Data Structures（数据结构）

### Introduction（引言）

Sets（集合）对 computer science（计算机科学）的重要性，正如它们对 mathematics（数学）的重要性一样。数学中的集合是 unchanging（固定不变）的，而算法所操纵的集合却可以 grow（增长）、shrink（收缩），或随时间以其他方式发生 change（变化）。我们把这样的集合称为 dynamic set（动态集合）。接下来的五章将给出一些 basic techniques（基本技术），用于表示 finite dynamic sets（有限动态集合）并在计算机上对它们进行 manipulation（操纵）。

算法可能需要在集合上执行若干种不同类型的 operations（操作）。例如，许多算法只需要三种能力：向集合中 insert（插入）元素、从集合中 delete（删除）元素，以及 test membership（测试成员资格，即判断某元素是否属于集合）。我们把支持这些操作的动态集合称为 dictionary（字典）。另一些算法则需要更复杂的操作。例如，min-priority queue（最小优先队列）——第 6 章在 heap data structure（堆数据结构）的语境中介绍过它——支持向集合中插入元素以及从集合中抽取最小元素这两种操作。实现 dynamic set 的最佳方式，取决于它必须支持哪些操作。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 这半页其实在为整个 Part III 立规矩：dynamic set（动态集合）是一个 abstract data type（抽象数据类型，ADT）——先规定"支持哪些操作、各操作满足什么行为规约"，再让不同数据结构在幕后竞争实现权。这套"接口与实现分离"的思想你在已学的课程里都有雏形：CSAPP 告诉你机器级程序只认地址与字节，C 的数组、struct 与函数调用规约是编译器维护的抽象边界；6.042J 的规约思维（先声明要证的性质，再证明构造满足它）是同一件事的数学版。为什么说"数据结构 = 查询/操作的成本工程"？因为同一逻辑集合，负载不同则最优结构不同：以 SEARCH/INSERT/DELETE 为主就用散列表（第 11 章，期望 $O(1)$），需要 SUCCESSOR/PREDECESSOR 这类全序查询就用红黑树（第 13 章，最坏 $O(\lg n)$），只需取最小元素就用堆（第 6 章）。原书一句"实现 dynamic set 的最佳方式，取决于它必须支持哪些操作"正是接下来五章的路线图：先问操作集合与频次分布，再选实现——这是可以迁移的工程判断力，而非需要背诵的清单。

### Elements of a dynamic set（动态集合的元素）

在 dynamic set 的一个典型 implementation（实现）中，每个 element 由一个 object（对象）来表示；只要我们持有指向该对象的 pointer（指针），就可以 examine（检查）和 manipulate（操纵）它的 attributes（属性）。（Section 10.3 将讨论：在不把 objects 和 pointers 作为基本数据类型的编程环境中，如何实现它们。）某些类型的动态集合假定对象的某个属性是用于标识的 key（关键字）。如果所有 key 都互不相同，我们就可以把这个动态集合看作一个由 key 值构成的集合。object 中还可能包含 satellite data（卫星数据），它们存放在对象的其他属性中、随对象四处携带，但除此之外并不被集合实现所使用。它可能（接下页）

---

> <span style="color:#7f8c8d;">CLRS Part III Introduction · 续, p.230</span>

## Part III · Data Structures（数据结构）· 续

（承上页）它（指表示集合元素的 object）也可能拥有由 set operations（集合操作）所操纵的其他 attributes；这些属性可以包含 data（数据），也可以包含指向该集合中其他 object 的 pointer。

某些动态集合 presuppose（预设）key 取自一个 totally ordered set（全序集合），例如 real numbers（实数）构成的集合，或者按 usual alphabetic ordering（通常的字母序）排列的所有单词构成的集合。total ordering（全序关系）使我们能够定义集合的 minimum element（最小元素），例如，也可以谈论集合中比某个给定元素大的下一个元素。

### Operations on dynamic sets（动态集合上的操作）

对 dynamic set 的 operations 可以分为两类：queries（查询），它们只是 return（返回）关于集合的信息；modifying operations（修改操作），它们会 change（改变）集合。下面列出一些典型的操作。任何具体的应用通常只需要实现其中的少数几个。

**SEARCH$(S, k)$**
一种 query（查询），给定 set（集合）$S$ 和 key value（关键字值）$k$，返回一个指向 $S$ 中某 element 的 pointer $x$，使得 $x.key = k$；若 $S$ 中不存在这样的元素，则返回 NIL。

**INSERT$(S, x)$**
一种 modifying operation（修改操作），把由 $x$ 所指向的 element 加入（augment）set $S$。我们通常假定 element $x$ 中为集合实现所必需的那些 attributes 都已经初始化。

**DELETE$(S, x)$**
一种 modifying operation，给定指向 set $S$ 中某个 element 的 pointer $x$，把 $x$ 从 $S$ 中 remove（移除）。（注意，该操作接受的是指向 element $x$ 的 pointer，而不是 key value。）

**MINIMUM$(S)$**
对 totally ordered set（全序集合）$S$ 的一种 query，返回一个指针，指向 $S$ 中 key（关键字）最小的那个 element。

**MAXIMUM$(S)$**
对 totally ordered set $S$ 的一种 query，返回一个指针，指向 $S$ 中 key 最大的那个 element。

**SUCCESSOR$(S, x)$**
一种 query，给定某个 element $x$，其 key 来自 totally ordered set $S$，返回一个指针，指向 $S$ 中下一个更大的 element；若 $x$ 是 maximum element（最大元素），则返回 NIL。

**PREDECESSOR$(S, x)$**
一种 query，给定某个 element $x$，其 key 来自 totally ordered set $S$，返回一个指针，指向 $S$ 中下一个更小的 element；若 $x$ 是 minimum element（最小元素），则返回 NIL。

---

> <span style="color:#7f8c8d;">CLRS Part III Introduction · 续, p.231</span>

## Part III · Data Structures（数据结构）· 续

在某些情况下，我们可以扩展 queries（查询）SUCCESSOR 与 PREDECESSOR，使它们同样适用于 key 并非互不相同（nondistinct）的集合。对于一个含有 $n$ 个 key 的集合，通常的约定是：先调用一次 MINIMUM，再连续调用 $n - 1$ 次 SUCCESSOR，就能按 sorted order（已排序顺序）enumerates（枚举）出集合中的所有 element。

我们通常以集合的 size（规模）来度量执行一次 set operation（集合操作）所花的时间。例如，Chapter 13 将描述一种 data structure（数据结构），它能对规模为 $n$ 的集合在 $O(\lg n)$ 时间内支持上面列出的任何一种操作。

### Overview of Part III（第三部分概览）

Chapter 10–14 描述了若干种可用于实现 dynamic sets（动态集合）的 data structures；本书后面会使用其中的许多结构，来为各种 problems 构造 efficient algorithms（高效算法）。我们已经在 Chapter 6 中见过另一种重要的数据结构——heap（堆）。

Chapter 10 讲解使用 stack（栈）、queue（队列）、linked list（链表）和 rooted tree（有根树）等简单数据结构的 essentials（基本要素）。它还展示了：在不把 objects（对象）和 pointers（指针）作为 primitives（原语）支持的编程环境中，如何实现它们。如果你修过 introductory programming course（程序设计入门课程），那么这些内容中的大部分对你来说应当是熟悉的。

Chapter 11 介绍 hash tables（散列表），它支持 dictionary operations（字典操作）INSERT、DELETE 与 SEARCH。在最坏情况下，hashing（散列）执行一次 SEARCH 操作需要 $\Theta(n)$ 时间，但 hash-table operations（散列表操作）的 expected time（期望时间）为 $O(1)$。对 hashing 的分析依赖于 probability（概率），但本章的大部分内容并不需要这方面的 background（背景知识）。

Chapter 12 讲述 binary search trees（二叉搜索树），它支持上面列出的所有 dynamic-set operations（动态集合操作）。在最坏情况下，在含有 $n$ 个 element 的树上执行每种操作都需要 $\Theta(n)$ 时间；但在 randomly built binary search tree（随机构建的二叉搜索树）上，每种操作的期望时间为 $O(\lg n)$。binary search trees 还是许多其他数据结构的基础。

Chapter 13 介绍 red-black trees（红黑树），它是 binary search trees 的一种 variant（变体）。与普通的 binary search trees 不同，red-black trees 的良好性能是有保证的：operations 在最坏情况下也只需 $O(\lg n)$ 时间。red-black tree 是一种 balanced search tree（平衡搜索树）；Part V 的 Chapter 18 将介绍另一种平衡搜索树，称为 B-tree（B 树）。尽管 red-black trees 的 mechanics（机理）有些 intricate（错综复杂），但即便不深入钻研其机理，你也能从该章中 glean（领会）到它们的大部分 properties（性质）。不过，你很可能还是会发现，亲手走查（walk through）代码是相当有启发的。

在 Chapter 14 中，我们将展示如何 augment（扩充）red-black trees，使它们支持上述基本操作之外的操作。首先，我们对 red-black trees 进行扩张，以便为一个 key 集合动态维护 order statistics（顺序统计量）。然后，我们再换一种方式对它们进行扩张，以维护 real numbers 的 intervals（区间）。

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.1, p.232</span>

## Chapter 10（第 10 章）· Elementary Data Structures（基本数据结构）

本章将考察用使用 pointer（指针）的 simple data structures（简单数据结构）来表示 dynamic sets（动态集合）的方法。虽然我们可以用指针构造出许多 complex data structures（复杂数据结构），但本章只介绍其中最 rudimentary（基础）的几种：stacks（栈）、queues（队列）、linked lists（链表）和 rooted trees（有根树）。我们还会展示如何从 arrays（数组）中 synthesize（合成）出 objects（对象）与 pointers。

### Section 10.1 · Stacks and queues（栈与队列） <span style="color:#2471a3;">**[section]**</span>

Stacks（栈）与 queues（队列）是这样一类 dynamic sets：由 DELETE 操作从集合中移除哪个 element 是 prespecified（预先规定）的。在 stack 中，被删除的元素是最近插入（inserted）的那个：stack 实现的是 last-in, first-out（后进先出）策略，简称 LIFO。类似地，在 queue 中，被删除的元素总是集合中存在时间最长的那个：queue 实现的是 first-in, first-out（先进先出）策略，简称 FIFO。在计算机上实现 stacks 与 queues 有几种 efficient（高效）的方式。本节将展示如何用一个 simple array（简单数组）来实现它们中的每一种。

### Stacks（栈）

在 stack 上执行的 INSERT 操作常常被称为 PUSH（压入），而 DELETE 操作——它不接受 element 参数——则常常被称为 POP（弹出）。这些名字都是在影射 physical stacks（物理上的堆叠物），例如自助餐厅里由弹簧承托的一摞摞盘子。盘子被 pop 出这摞盘子的顺序，正好与它们被 push 上去时相反，因为只有最顶上的盘子是 accessible（可取）的。

如 Figure 10.1（图 10.1）所示，我们可以用一个 array $S[1..n]$ 来实现一个至多包含 $n$ 个 element 的 stack。该 array 有一个 attribute（属性）$S.top$，它 index（索引）最近插入的（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.1, p.233</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 10.1 的示意图：用数组 $S[1..7]$ 实现的栈 $S$ 的三个快照——(a) 栈含 4 个元素，$S.top = 4$，栈顶元素为 9；(b) 依次压入 17、3 之后，$S.top = 6$；(c) 弹出 3 之后，$S.top = 5$，栈顶元素为 17（数组中残留的 3 已不属于栈）。</span>

**Figure 10.1（图 10.1）** 栈 $S$ 的一个 array implementation（数组实现）。栈元素只出现在浅色阴影的位置上。(a) 栈 $S$ 有 4 个元素，栈顶（top）元素是 9。(b) 依次调用 PUSH(S, 17) 与 PUSH(S, 3) 之后的栈 $S$。(c) 调用 POP(S) 返回元素 3——即最近被压入的那个元素——之后的栈 $S$。虽然元素 3 仍出现在数组中，但它已不在栈内；此时栈顶元素是 17。

（接上页）element（元素）。栈由 elements（元素）$S[1..S.top]$ 组成，其中 $S[1]$ 是位于栈底（bottom）的元素，而 $S[S.top]$ 是位于栈顶的元素。

当 $S.top = 0$ 时，栈不含任何元素，即为 empty（空）。我们可以通过 query operation（查询操作）STACK-EMPTY 来测试栈是否为空。如果试图对一个空栈执行 pop 操作，则称栈发生 underflow（下溢），这通常是一个 error（错误）。如果 $S.top$ 超过 $n$，则栈发生 overflow（上溢）。（在我们的 pseudocode（伪代码）实现中，我们并不担心 stack overflow（栈上溢）。）

栈的每一种操作都可以只用几行代码来实现：

```
STACK-EMPTY(S)
1  if S.top == 0
2      return TRUE
3  else return FALSE
```

```
PUSH(S, x)
1  S.top = S.top + 1
2  S[S.top] = x
```

```
POP(S)
1  if STACK-EMPTY(S)
2      error "underflow"
3  else S.top = S.top − 1
4      return S[S.top + 1]
```

图 10.1 展示了 modifying operations（修改操作）PUSH 与 POP 的效果。这三种栈操作中的每一种都只花费 $O(1)$ 的时间。

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.1, p.234</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 10.2 的示意图：用数组 $Q[1..12]$ 实现的队列 $Q$ 的三个快照——(a) 队列含 5 个元素（15、6、9、8、4），位于 $Q[7..11]$，$Q.head = 7$、$Q.tail = 12$；(b) 依次入队 17、3、5 之后，队列发生"环绕"，$Q.head = 7$、$Q.tail = 3$；(c) 出队返回 15 之后，$Q.head = 8$、$Q.tail = 3$，新的队头元素为 6。</span>

**Figure 10.2（图 10.2）** 用数组 $Q[1..12]$ 实现的一个 queue（队列）。队列元素只出现在浅色阴影的位置上。(a) 队列有 5 个元素，位于位置 $Q[7..11]$ 中。(b) 依次调用 ENQUEUE(Q, 17)、ENQUEUE(Q, 3) 与 ENQUEUE(Q, 5) 之后队列的 configuration（布局）。(c) 调用 DEQUEUE(Q) 返回原先位于队头的 key value（关键字值）15 之后队列的布局。新的队头元素的关键字为 6。

#### Queues（队列）

我们把作用在 queue（队列）上的 INSERT 操作称为 ENQUEUE（入队），把 DELETE 操作称为 DEQUEUE（出队）；与 stack（栈）的 POP 操作一样，DEQUEUE 也不接受 element（元素）参数。队列的 FIFO property（FIFO 性质）使它的运作方式像一队等待付款的顾客排成的长队。队列有一个 head（队头）和一个 tail（队尾）。当一个元素被入队时，它在队尾占据自己的位置，就像一位新来的顾客在队尾排队一样。被出队的元素永远是位于队头的那个元素，就像队伍最前面那位等待时间最长的顾客。

图 10.2 展示了用数组 $Q[1..n]$ 实现一个至多包含 $n - 1$ 个元素的队列的一种方法。该队列有一个 attribute（属性）$Q.head$，它 index（索引）——或者说指向——队列的队头。属性 $Q.tail$ 索引新到来的元素将被插入的下一个位置。队列中的元素位于位置 $Q.head, Q.head + 1, \ldots, Q.tail - 1$ 上，其中位置 1 紧随位置 $n$ 之后，构成一种 circular order（环形次序）意义上的 "wrap around"（环绕）。当 $Q.head = Q.tail$ 时，队列为空。初始时，我们有 $Q.head = Q.tail = 1$。如果试图对一个空队列执行 dequeue 操作，则队列发生 underflow（下溢）。（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 第一性原理追问：$S.top$、$Q.head$、$Q.tail$ 到底"是"什么？它们不是指针，只是普通整数下标——栈和队列的全部状态 = 一个数组加上一两个整数。环形队列的取模回绕是"把有限数组当无限资源用"的经典手法：队尾走到 $n$ 就跳回 1，出队腾出的前段空间得以循环复用，避免了朴素实现"整体越用越右移、前面空间全部浪费"的漂移问题。一个容易忽视的细节：书中让队列至多存 $n-1$ 个元素，因为"空"已约定为 $Q.head=Q.tail$，若允许填满，则"满"与"空"在下标上不可区分——这是用一格冗余空间换状态可判定性的设计权衡，也可以改用维护元素计数来替代。连到你学过的 CSAPP：这种手写下标管理正是缓冲区（buffer）的雏形，操作系统与网络代码里的 ring buffer（环形缓冲区）与此同构；而下标忘记回绕、差一错误导致的越界，正是 CSAPP 第 3 章"越界与缓冲区漏洞"在算法课上的温和镜像。习题 10.1-2（一个数组容纳两个栈、两端相向生长）是同一手法的又一次变奏。

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.1, p.235</span>

（接上页）当 $Q.head = Q.tail + 1$，或者同时有 $Q.head = 1$ 与 $Q.tail = Q.length$ 时，队列是 full（满）的；此时如果试图向队列中 enqueue（入队）一个元素，队列将发生 overflow（上溢）。在我们的过程 ENQUEUE 与 DEQUEUE 中，我们省略了对 underflow（下溢）与 overflow（上溢）的错误检查。（Exercise 10.1-4 要求你补充检查这两种错误条件的代码。）这段 pseudocode（伪代码）假定 $n = Q.length$。

```
ENQUEUE(Q, x)
1  Q[Q.tail] = x
2  if Q.tail == Q.length
3      Q.tail = 1
4  else Q.tail = Q.tail + 1
```

```
DEQUEUE(Q)
1  x = Q[Q.head]
2  if Q.head == Q.length
3      Q.head = 1
4  else Q.head = Q.head + 1
5  return x
```

图 10.2 展示了 ENQUEUE 与 DEQUEUE 操作的效果。每个操作都只花费 $O(1)$ 的时间。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**10.1-1**

Using Figure 10.1 as a model, illustrate the result of each operation in the sequence PUSH(S, 4), PUSH(S, 1), PUSH(S, 3), POP(S), PUSH(S, 8), and POP(S) on an initially empty stack S stored in array $S[1..6]$.

**10.1-2**

Explain how to implement two stacks in one array $A[1..n]$ in such a way that neither stack overflows unless the total number of elements in both stacks together is $n$. The PUSH and POP operations should run in $O(1)$ time.

**10.1-3**

Using Figure 10.2 as a model, illustrate the result of each operation in the sequence ENQUEUE(Q, 4), ENQUEUE(Q, 1), ENQUEUE(Q, 3), DEQUEUE(Q), ENQUEUE(Q, 8), and DEQUEUE(Q) on an initially empty queue Q stored in array $Q[1..6]$.

**10.1-4**

Rewrite ENQUEUE and DEQUEUE to detect underflow and overflow of a queue.

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.1–10.2, p.236</span>

**10.1-5**

Whereas a stack allows insertion and deletion of elements at only one end, and a queue allows insertion at one end and deletion at the other end, a deque (double-ended queue) allows insertion and deletion at both ends. Write four $O(1)$-time procedures to insert elements into and delete elements from both ends of a deque implemented by an array.

**10.1-6**

Show how to implement a queue using two stacks. Analyze the running time of the queue operations.

**10.1-7**

Show how to implement a stack using two queues. Analyze the running time of the stack operations.

### Section 10.2 · Linked lists（链表） <span style="color:#2471a3;">**[section]**</span>

linked list（链表）是一种其中的 objects（对象）按 linear order（线性次序）排列的数据结构。然而，与数组不同——数组的线性次序由 array indices（数组下标）决定——链表中的次序由每个对象中的一个 pointer（指针）决定。链表为 dynamic sets（动态集合）提供了一种简单、灵活的 representation（表示），支持（尽管不一定高效）page 230 上列出的所有 operations（操作）。

如 Figure 10.3（图 10.3）所示，doubly linked list（双链表）$L$ 的每个元素都是一个 object（对象），它带有一个 attribute（属性）key（关键字）以及另外两个 pointer attribute（指针属性）：next（后继）与 prev（前驱）。对象还可以包含其他的 satellite data（卫星数据）。给定链表中的一个元素 $x$，$x.next$ 指向它在链表中的 successor（后继），而 $x.prev$ 指向它的 predecessor（前驱）。如果 $x.prev = NIL$，则元素 $x$ 没有前驱，因此它是链表的第一个元素，即 head（表头）。如果 $x.next = NIL$，则元素 $x$ 没有后继，因此它是链表的最后一个元素，即 tail（表尾）。属性 $L.head$ 指向链表的第一个元素。如果 $L.head = NIL$，则链表为空。

链表可以有多种形式。它可以是 singly linked（单链）或 doubly linked（双链）的，可以是 sorted（已排序）或未排序的，还可以是 circular（循环）或非循环的。如果链表是单链的，则省略每个元素中的 prev 指针。如果链表是已排序的，链表的线性次序就对应于其中元素所存储 key（关键字）的线性次序；此时最小的元素就是表头，最大的元素是表尾。如果链表未排序，则各元素可以以任意次序出现。在 circular list（循环链表）中，表头的 prev 指针指向表尾，而表尾的 next 指针指向表头。我们可以把循环链表想象成一个由（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.2, p.237</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 10.3 的示意图：一个含关键字 9、16、4、1 的双链表 $L$ 的三个快照——(a) 初始链表，$L.head$ 指向关键字为 9 的表头；每个元素画出 key、prev、next 三个属性，表尾的 next 与表头的 prev 用斜线表示 NIL；(b) 执行 LIST-INSERT(L, x)（$x.key = 25$）后，关键字 25 的新对象成为新表头，指向旧表头 9；(c) 执行 LIST-DELETE(L, x)（$x$ 指向关键字为 4 的对象）后，元素 4 被从链中拼接出去。</span>

**Figure 10.3（图 10.3）** (a) 一个表示 dynamic set（动态集合）$\{1, 4, 9, 16\}$ 的 doubly linked list（双链表）$L$。链表中的每个元素都是一个 object（对象），它带有存放 key（关键字）的 attribute（属性）以及指向下一个和前一个对象的 pointer（指针，用箭头表示）。表尾（tail）的 next 属性与表头（head）的 prev 属性为 NIL，用一条对角斜线表示。属性 $L.head$ 指向表头。(b) 执行 LIST-INSERT(L, x)（其中 $x.key = 25$）之后，链表有了一个以关键字 25 的新对象作为新的表头。这个新对象指向关键字为 9 的旧表头。(c) 随后调用 LIST-DELETE(L, x)（其中 $x$ 指向关键字为 4 的对象）的结果。

（接上页）elements（元素）构成的环（ring）。在本节余下的部分中，我们假定所处理的链表都是 unsorted（未排序）且 doubly linked（双链）的。

#### Searching a linked list（搜索链表）

过程 LIST-SEARCH(L, k) 用简单的 linear search（线性搜索）在链表 $L$ 中找出第一个 key（关键字）为 $k$ 的元素，并返回指向该元素的 pointer（指针）。如果链表中不出现关键字为 $k$ 的 object（对象），则该过程返回 NIL。对于图 10.3(a) 中的链表，调用 LIST-SEARCH(L, 4) 返回指向第三个元素的指针，而调用 LIST-SEARCH(L, 7) 返回 NIL。

```
LIST-SEARCH(L, k)
1  x = L.head
2  while x ≠ NIL and x.key ≠ k
3      x = x.next
4  return x
```

要搜索一个包含 $n$ 个对象的链表，过程 LIST-SEARCH 在 worst case（最坏情况）下需要 $\Theta(n)$ 的时间，因为它可能必须搜索整个链表。

#### Inserting into a linked list（链表的插入）

给定一个其 key 属性已经设置好的元素 $x$，LIST-INSERT 过程把 $x$ splice（拼接）到链表的前端，如图 10.3(b) 所示。（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.2, p.238</span>

（接上页）

```
LIST-INSERT(L, x)
1  x.next = L.head
2  if L.head ≠ NIL
3      L.head.prev = x
4  L.head = x
5  x.prev = NIL
```

（回想一下，我们的 attribute（属性）记法是可以级联（cascade）的，因此 $L.head.prev$ 表示 $L.head$ 所指向对象的 prev 属性。）在一个包含 $n$ 个元素的链表上，LIST-INSERT 的 running time（运行时间）为 $O(1)$。

#### Deleting from a linked list（链表的删除）

过程 LIST-DELETE 从链表 $L$ 中删除一个元素 $x$。它必须被给一个指向 $x$ 的 pointer（指针），然后通过更新各指针把 $x$ 从链表中"拼接出去"（splice out）。如果我们想删除一个具有给定 key（关键字）的元素，就必须先调用 LIST-SEARCH 检索出指向该元素的指针。

```
LIST-DELETE(L, x)
1  if x.prev ≠ NIL
2      x.prev.next = x.next
3  else L.head = x.next
4  if x.next ≠ NIL
5      x.next.prev = x.prev
```

图 10.3(c) 展示了如何从链表中删除一个元素。LIST-DELETE 的运行时间为 $O(1)$，但如果我们想删除一个具有给定关键字的元素，则 worst case（最坏情况）下需要 $\Theta(n)$ 的时间，因为我们必须先调用 LIST-SEARCH 来找到该元素。

#### Sentinels（哨兵）

如果我们能够忽略链表 head（表头）与 tail（表尾）处的 boundary conditions（边界条件），LIST-DELETE 的代码本可以更简单：

```
LIST-DELETE′(L, x)
1  x.prev.next = x.next
2  x.next.prev = x.prev
```

sentinel（哨兵）是一个 dummy object（哑对象），它使我们能够简化边界条件。例如，假设我们为链表 $L$ 提供一个对象 $L.nil$，它表示 NIL（接下页）

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 哨兵的价值用一个对照就能看清：LIST-DELETE 需要 4 处分支判断（$x.prev$、$x.next$ 是否为 NIL、$L.head$ 是否要更新），而 LIST-DELETE′ 永远是干净的两行——因为哨兵把"边界"变成了"普通元素"：删除表头时 $x.prev$ 指向哨兵 $L.nil$ 而非 NIL，更新 $L.nil.next$ 恰好顺带完成表头切换，头尾特判被彻底消灭。这与 chunk02 中归并排序用 $\infty$ 哨兵卡片的思路同源：不是让代码学会处理更多特殊情况，而是改造数据结构，让特殊情况根本不存在。为什么这对正确性是大杀器？因为 bug 最爱藏在边界分支里——每个 if 都是一条平时测试不到的执行路径，消掉分支等于整类差一错误失去藏身之处。也要记住本节稍后（p.240）的告诫：哨兵一般不改善渐近时间界，只降低常数因子并提升 clarity（清晰度），且每个哨兵都占存储，链表又多又短时反而浪费内存——所以原则是"确实简化代码时才用"。习题 10.2-4（借哨兵消除搜索循环里的第二个测试）正是这一思想的直接练习。

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.2, p.239</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 10.4 的示意图：一个带哨兵 $L.nil$ 的循环双链表的四个快照——(a) 空链表，仅含哨兵，$L.nil.next$ 与 $L.nil.prev$ 都指向 $L.nil$；(b) 图 10.3(a) 的链表改造成环形，哨兵位于表头 9 与表尾 1 之间；(c) 执行 LIST-INSERT′(L, x)（$x.key = 25$）后，关键字 25 的新对象成为新表头；(d) 删除关键字为 1 的对象后，新的表尾是关键字为 4 的对象。</span>

**Figure 10.4（图 10.4）** 一个带哨兵（sentinel）的 circular, doubly linked list（循环双链表）。哨兵 $L.nil$ 位于表头（head）与表尾（tail）之间。属性 $L.head$ 不再需要，因为我们可以通过 $L.nil.next$ 访问表头。(a) 一个空链表。(b) 图 10.3(a) 中的链表，关键字 9 在表头，关键字 1 在表尾。(c) 执行 LIST-INSERT′(L, x)（其中 $x.key = 25$）之后的链表。新对象成为链表的表头。(d) 删除关键字为 1 的对象之后的链表。新的表尾是关键字为 4 的对象。

（接上页）但具有链表中其他 object（对象）的所有 attribute（属性）。在链表代码中，凡是有对 NIL 的 reference（引用）的地方，我们都把它替换成对 sentinel（哨兵）$L.nil$ 的引用。如图 10.4 所示，这一改动把一个常规的 doubly linked list（双链表）变成了一个 circular, doubly linked list with a sentinel（带哨兵的循环双链表），其中哨兵 $L.nil$ 位于表头与表尾之间。属性 $L.nil.next$ 指向表头，而 $L.nil.prev$ 指向表尾。类似地，表尾的 next 属性与表头的 prev 属性都指向 $L.nil$。由于 $L.nil.next$ 指向表头，我们可以完全去掉属性 $L.head$，把对它的引用替换为对 $L.nil.next$ 的引用。图 10.4(a) 表明，一个空链表仅由哨兵组成，且 $L.nil.next$ 与 $L.nil.prev$ 都指向 $L.nil$。

LIST-SEARCH 的代码保持不变，只是按照上面的说明改变了对 NIL 与 $L.head$ 的引用：

```
LIST-SEARCH′(L, k)
1  x = L.nil.next
2  while x ≠ L.nil and x.key ≠ k
3      x = x.next
4  return x
```

我们使用前面那个两行的过程 LIST-DELETE′ 来从链表中删除一个元素。下面的过程向链表中插入一个元素：（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.2, p.240</span>

（接上页）

```
LIST-INSERT′(L, x)
1  x.next = L.nil.next
2  L.nil.next.prev = x
3  L.nil.next = x
4  x.prev = L.nil
```

图 10.4 展示了 LIST-INSERT′ 与 LIST-DELETE′ 在一个样例链表上的效果。sentinel（哨兵）很少能降低数据结构操作的 asymptotic time bounds（渐近时间界），但它们可以降低 constant factors（常数因子）。在 loop（循环）内使用哨兵所获得的收益，通常在于 clarity（代码更清晰）而非速度；例如，使用哨兵后链表代码变得更简单，但我们在 LIST-INSERT′ 与 LIST-DELETE′ 这两个过程中只节省了 $O(1)$ 的时间。然而在另一些情形中，哨兵的使用有助于收紧循环内的代码，从而降低运行时间中比如 $n$ 或 $n^2$ 的 coefficient（系数）。

我们应当 judiciously（审慎地）使用哨兵。当存在许多小链表时，它们的哨兵所占用的额外存储可能意味着相当可观的内存浪费。在本书中，我们只在哨兵确实能简化代码时才使用它。

#### Exercises（习题） <span style="color:#2471a3;">**[exercise]**</span>

**10.2-1**

Can you implement the dynamic-set operation INSERT on a singly linked list in $O(1)$ time? How about DELETE?

**10.2-2**

Implement a stack using a singly linked list L. The operations PUSH and POP should still take $O(1)$ time.

**10.2-3**

Implement a queue by a singly linked list L. The operations ENQUEUE and DEQUEUE should still take $O(1)$ time.

**10.2-4**

As written, each loop iteration in the LIST-SEARCH′ procedure requires two tests: one for x ≠ L.nil and one for x.key ≠ k. Show how to eliminate the test for x ≠ L.nil in each iteration.

**10.2-5**

Implement the dictionary operations INSERT, DELETE, and SEARCH using singly linked, circular lists. What are the running times of your procedures?

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.2–10.3, p.241</span>

**10.2-6**

The dynamic-set operation UNION takes two disjoint sets $S_1$ and $S_2$ as input, and it returns a set $S = S_1 \cup S_2$ consisting of all the elements of $S_1$ and $S_2$. The sets $S_1$ and $S_2$ are usually destroyed by the operation. Show how to support UNION in $O(1)$ time using a suitable list data structure.

**10.2-7**

Give a $\Theta(n)$-time nonrecursive procedure that reverses a singly linked list of $n$ elements. The procedure should use no more than constant storage beyond that needed for the list itself.

**10.2-8**

★

Explain how to implement doubly linked lists using only one pointer value x.np per item instead of the usual two (next and prev). Assume that all pointer values can be interpreted as $k$-bit integers, and define x.np to be x.np = x.next XOR x.prev, the $k$-bit "exclusive-or" of x.next and x.prev. (The value NIL is represented by 0.) Be sure to describe what information you need to access the head of the list. Show how to implement the SEARCH, INSERT, and DELETE operations on such a list. Also show how to reverse such a list in $O(1)$ time.

### Section 10.3 · Implementing pointers and objects（指针与对象的实现） <span style="color:#2471a3;">**[section]**</span>

在不提供 pointer（指针）与 object（对象）的语言中，我们该如何实现它们？在本节中，我们将看到两种无需显式的 pointer data type（指针数据类型）来实现 linked data structures（链接式数据结构）的方法。我们将从 arrays（数组）与 array indices（数组下标）合成（synthesize）出对象与指针。

#### A multiple-array representation of objects（对象的多数组表示）

我们可以用一个数组对应一个 attribute（属性）的方式，来表示一组具有相同属性的对象。例如，Figure 10.5（图 10.5）展示了如何用三个数组来实现图 10.3(a) 中的链表。数组 key 存放当前 dynamic set（动态集合）中的 key（关键字）值，而 pointer（指针）则存放在数组 next 与 prev 中。对于给定的数组下标 $x$，数组项 $key[x]$、$next[x]$ 与 $prev[x]$ 共同表示链表中的一个 object（对象）。在这种解释之下，指针 $x$ 只不过是 key、next 与 prev 这三个数组的一个公共下标而已。

在图 10.3(a) 中，key 为 4 的对象跟在 key 为 16 的对象之后。在图 10.5 中，key 4 出现在 $key[2]$ 中，key 16 出现在 $key[5]$ 中，因此 $next[5] = 2$ 且 $prev[2] = 5$。虽然常量 NIL 出现在表尾的 next（接下页）

---

> <span style="color:#7f8c8d;">CLRS Chapter 10 · §10.3, p.242</span>

> <span style="color:#7f8c8d;">[note] 本页顶部为图 10.5 的示意图：用三个数组 key、next、prev（下标 1..8）表示的图 10.3(a) 中的链表。数组的每个纵向切片（同一列的 key[x]、next[x]、prev[x]）表示一个 object（对象），浅色阴影的切片是链表元素；存储的 pointer（指针）即顶部所示的数组下标，箭头展示如何解释它们；变量 $L$ 保存表头的下标。其中 $key[2] = 4$、$key[5] = 16$，且 $next[5] = 2$、$prev[2] = 5$。</span>

**Figure 10.5（图 10.5）** 用数组 key、next 与 prev 表示的图 10.3(a) 中的链表。数组的每个 vertical slice（纵向切片）表示一个 object（对象）。存储的 pointer（指针）对应于顶部所示的 array indices（数组下标）；箭头展示了应如何解释它们。浅色阴影的对象位置包含链表元素。变量 $L$ 保存表头（head）的下标。

（接上页）attribute（属性）与表头的 prev 属性中出现，我们通常用一个不可能表示数组实际下标的整数（比如 0 或 $-1$）来充当它。变量 $L$ 保存链表表头的下标。

#### A single-array representation of objects（对象的单数组表示）

计算机内存中的 word（字）通常由 $0$ 到 $M - 1$ 的整数来 address（寻址），其中 $M$ 是一个足够大的整数。在许多 programming languages（编程语言）中，一个 object（对象）占据计算机内存中一段连续的 location（位置）。pointer（指针）就是该对象第一个内存位置的 address（地址），而通过在指针上加一个 offset（偏移量），我们就可以访问对象内部的其他内存位置。

对于不提供显式 pointer data type（指针数据类型）的编程环境，我们可以采用同样的策略来实现对象。例如，图 10.6 展示了如何用一个单一数组 $A$ 来存储图 10.3(a) 与图 10.5 中的链表。一个对象占据一段连续的 subarray（子数组）$A[j..k]$。对象的每个 attribute（属性）对应于 $0$ 到 $k - j$ 范围内的一个 offset（偏移量），而指向该对象的指针就是下标 $j$。在图 10.6 中，与 key、next 和 prev 对应的偏移量分别是 0、1 和 2。给定指针 $i$，要读取 $i.prev$ 的值，我们把指针的值 $i$ 加上偏移量 2，从而读取 $A[i + 2]$。

single-array representation（单数组表示）的灵活之处在于，它允许把不同长度的对象存储在同一个数组中。不过，管理这样一个 heterogeneous（异构）对象集合的问题，要比管理 homogeneous（同构）集合——其中所有对象具有相同的属性——的问题更困难。由于我们将考虑的大多数 data structures（数据结构）都由同构的 elements（元素）组成，因此对本书的目的而言，使用对象的 multiple-array representation（多数组表示）就足够了。

> <span style="color:#1e8449;">**[note] Note（译者注）:**</span> 多数组表示对阵"单数组/常规结构体"表示之争，在真实系统里有个你该认识的名字：结构体数组（array of structures，AoS）对阵字段数组（structure of arrays，SoA）。图 10.5 的三个平行数组是 SoA——同一属性的值连续存放；"每个对象占一段连续内存"是 AoS。为什么语言运行时与性能工程师真的在意这个布局？答案在 CSAPP 第 5、6 章：访存效率由空间局部性决定，而局部性由布局决定。假如程序的主要负载是"顺着 next 指针遍历"，SoA 把 next 数组压成一整块连续内存，硬件预取器每个缓存行能带回一批下标；AoS 则把 key、next、prev 混排在一起，每个缓存行里往往只有一个字段被用到——这正是你在 CSAPP 优化实验中"交换循环嵌套顺序改变命中率"现象的布局版。区别也要认清：AoS 对"同时读取同一对象的全部字段"更友好，SoA 则是 SIMD 向量化与 GPU 编程的标准布局（同字段成批进入向量通道）。把"指针 = 数组下标"再往前推一步：下标可以序列化、可以写入磁盘、可以跨进程共享——这就是持久化、无指针数据结构的出发点。
