# Lecture 5: Linear Sorting（线性排序）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Review（回顾）

- Comparison search 的 lower bound：任何含 $n$ 个节点的 decision tree，高度都 $\ge \lceil \lg(n+1)\rceil - 1$。
- 想更快，只能靠 random access indexing：一个 branching factor 为线性的 operation。
- Direct access array 很快，但空间可能是 $\Theta(u)$，很浪费。
- 空间问题的解法是映射（hashing）：把 key space $u$ 压到 $m = \Theta(n)$。
- Hash table 给出 expected $O(1)$ 的 operations，动态场景下是 amortized $O(1)$。
- 注意这个 expectation 与 input 无关：hash function 是从 universal hash family 里随机选的。
- 下面这张 data structure overview 是上一讲的成果盘点。

| Data Structure | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Sorted Array | $n\log n$ | $\log n$ | $n$ | $n$ | $1$ | $1$ | $\log n$ | $\log n$ |
| Direct Access Array | $u$ | $1$ | $1$ | $1$ | $u$ | $u$ | $u$ | $u$ |
| Hash Table | $n^{(e)}$ | $1^{(e)}$ | $1^{(a)(e)}$ | $1^{(a)(e)}$ | $n$ | $n$ | $n$ | $n$ |

> 表注：$(e)$ = expected，$(a)$ = amortized。原 PDF 为合并单元格排版，这里把每格填满；`Direct Access Array` 行的 `delete(k)` / `find_prev` / `find_next` 在文字层残缺，按语义推定为 $1$ / $u$ / $u$。

- 上一讲我们让 `find` 变快了。这一讲的问题是：能不能也让 sort 变快？

## Comparison Sort 的 Lower Bound（下界）

- Comparison model 意味着 algorithm 的 decision tree 是 binary 的，即 branching factor 是常数。
- 要求 leaf 数 $L \ge$ 可能的 output 数。
- Tree height 下界是 $\Omega(\log L)$，所以 worst-case running time 是 $\Omega(\log L)$。
- 给 $n$ 个元素的 array 排序，outputs 共有 $n!$ 个 permutations。
- 于是 height 下界是

```math
\log(n!) \ge \log\left(\left(\frac{n}{2}\right)^{n/2}\right) = \Omega(n\log n)
```

- 所以 merge sort 在 comparison model 里已经是最优的。
- 那能不能利用 direct access array 来突破这个 bound、sort 得更快？

## Direct Access Array Sort（直接访问数组排序）

- 例子：$[5, 2, 7, 0, 4]$。
- 假设所有 keys 都是互不相同的非负整数，落在 $\{0, \dots, u-1\}$，于是 $n \le u$。
- 花 $\Theta(n)$ 把每个 item 插进一个 size 为 $u$ 的 direct access array。
- 再花 $\Theta(u)$ 按它们在 direct access array 中出现的顺序读出来。
- Running time 是 $\Theta(u)$；若 $u = \Theta(n)$，就是 $\Theta(n)$。太好了！

```python
def direct_access_sort(A):
    "Sort A assuming items have distinct non-negative keys"
    u = 1 + max([x.key for x in A])          # O(n) find maximum key
    D = [None] * u                           # O(u) direct access array
    for x in A:                              # O(n) insert items
        D[x.key] = x
    i = 0
    for key in range(u):                     # O(u) read out items in order
        if D[key] is not None:
            A[i] = D[key]
            i += 1
```

- 但如果 key range 更大呢，比如 $u = \Omega(n^2)$ 甚至更大？
- Idea！把每个 key $k$ 表示成一个 tuple $(a, b)$，满足 $k = an + b$ 且 $0 \le b < n$。
- 具体地，取 $a = \lfloor k/n\rfloor < n$ 与 $b = (k \bmod n)$——这其实就是把 $k$ 写成 base-$n$（$n$ 进制）的两位数！
- Python 内建就能做这件事：`(a, b) = divmod(k, n)`。
- 例子（$n = 5$）：$[17, 3, 24, 22, 12] \Rightarrow [(3,2), (0,3), (4,4), (4,2), (2,2)] \Rightarrow [32, 03, 44, 42, 22]$。
- 那 tuple 该怎么 sort？

## Tuple Sort（元组排序）

- 此时 item 的 key 是等长 tuple，即 `x.key = (x.k1, x.k2, x.k2, ...)`。
- 我们希望按 lexicographic（字典序）对所有成分排序，所以第一个 key `k1` 是 most significant（最高位）。
- 怎么排？Idea！用别的 auxiliary sorting algorithm（辅助排序算法）去分别排每一位 key。
- 类比：就像在 spreadsheet 里按多列排序行。
- 那顺序怎么定？从 least significant（最低位）排到 most significant（最高位）！
- 练习（$n = 5$）：$[32, 03, 44, 42, 22] \Rightarrow [42, 22, 32, 03, 44] \Rightarrow [03, 22, 32, 42, 44]$。
- Idea！用 tuple sort，配 auxiliarily 的 direct access array sort，来排 $(a, b)$。
- 但有个问题！即使 input keys 互不相同，也可能有很多整数的 $a$ 值相同、或 $b$ 值相同。
- 所以需要一种允许 repeated keys（重复键）且能保持 input order 的 sort。
- 也就是要求 sort 是 stable（稳定的）：repeated keys 在 output 中的相对次序与 input 中一致。
- 而 direct access array sort 连「排一个含重复 keys 的 array」都做不到！
- 那能不能修改 direct access array sort，让它容纳多个 keys 且保持稳定？

## Counting Sort（计数排序）

- 每个 array index 上不再存单个 item，而是存一条 chain——和 hashing 里的做法一样！
- 为稳定性，chain 这个 data structure 必须记住 items 被加入的先后次序。
- 用一个 sequence data structure（序列结构），它天然维护 insertion order（插入顺序）。
- 插入 item $x$ 时，把它 `insert_last` 到 index `x.key` 那条 chain 的末尾。
- 排序时，按 sequence 顺序把各条 chain 都读一遍，逐个 return items。

```python
def counting_sort(A):
    "Sort A assuming items have non-negative keys"
    u = 1 + max([x.key for x in A])          # O(n) find maximum key
    D = [[] for i in range(u)]               # O(u) direct access array of chains
    for x in A:                              # O(n) insert into chain at x.key
        D[x.key].append(x)
    i = 0
    for chain in D:                          # O(u) read out items in order
        for x in chain:
            A[i] = x
            i += 1
```

- `counting_sort` 的总时间是 $\Theta(n + u)$：$\Theta(n)$ 建 chain，$\Theta(u)$ 扫全表。所以当 $u = O(n)$ 时它是线性的。

## Radix Sort（基数排序）

- Idea！若 $u < n^2$，就用 tuple sort，配 auxiliary counting sort 来排 tuples $(a, b)$。
- 先排 least significant key $b$，再排 most significant key $a$。
- Stability（稳定性）保证先前的排序结果不会被后一次排序打乱。
- 这个 algorithm 的 running time 是 $O(2n) = O(n)$。太好了！
- 推广：若每个 key 都小于 $n^c$，其中 $c = \log_n(u)$ 是正整数，那么每个 key 至多有 $c$ 位 base-$n$ digit。
- 一个 $c$ 位数字可以在 $O(c)$ 时间内写成一个 $c$ 元素 tuple。
- 我们花 $O(n)$ 时间来排这 $c$ 个 base-$n$ digits 中的每一位。
- 所以配 auxiliary counting sort 的 tuple sort 总共跑 $O(cn)$ 时间。
- 若 $c$ 是常数，即每个 key 都 $\le n^c$，这个 sort 就是线性的 $O(n)$！

```python
def radix_sort(A):
    "Sort A assuming items have non-negative keys"
    n = len(A)
    u = 1 + max([x.key for x in A])          # O(n) find maximum key
    c = 1 + (u.bit_length() // n.bit_length())
    class Obj: pass
    D = [Obj() for a in A]
    for i in range(n):                       # O(nc) make digit tuples
        D[i].digits = []
        D[i].item = A[i]
        high = A[i].key
        for j in range(c):                   # O(c) make digit tuple
            high, low = divmod(high, n)
            D[i].digits.append(low)
    for i in range(c):                       # O(nc) sort each digit
        for j in range(n):                   # O(n) assign key i to tuples
            D[j].key = D[j].digits[i]
        counting_sort(D)                     # O(n) sort on digit i
    for i in range(n):                       # O(n) output to A
        A[i] = D[i].item
```

- 注意 `c = 1 + (u.bit_length() // n.bit_length())`：这里用二进制位长之比去估 $\lceil \log_n u\rceil$，是个不取对数函数的廉价上界写法。
- 另外 `radix_sort` 里每一轮 `counting_sort(D)` 都要求 `D` 上的 key 是非负整数，所以循环体先把 `D[j].key` 设成当前这一位 `D[j].digits[i]`——这是「把某一位提出来当 key」的具体做法，也是 radix sort 的整个机制所在。

## 五种 sort 的总对照

原 PDF 的这张表用合并单元格排版，文字层把 $n^2$ 拆成两行（`2` 与 `n`），把 $n + n\log_n u$ 拆成 `n + n log (u)` 与 `n`。这里还原成正确的数学形式，并把 `In-place?` / `Stable?` 两列从 `Y` / `N` 展开成中文可读的「是 / 否」。

| Algorithm | Time $O(\cdot)$ | In-place? | Stable? | Comments |
|---|---|---|---|---|
| Insertion Sort | $n^2$ | 是 | 是 | $O(nk)$，对 $k$-proximate（$k$ 近似有序）输入 |
| Selection Sort | $n^2$ | 是 | 否 | 只要 $O(n)$ 次 swaps |
| Merge Sort | $n\log n$ | 否 | 是 | stable，comparison model 下最优 |
| Counting Sort | $n + u$ | 否 | 是 | $u = O(n)$ 时是 $O(n)$ |
| Radix Sort | $n + n\log_n u$ | 否 | 是 | $u = O(n^c)$ 时是 $O(n)$ |

- 读这张表的正确姿势：只有 Counting Sort 与 Radix Sort 跳出 comparison model，靠的是 $O(1)$ random access indexing 提供的线性 branching factor。
- 代价是它们要求 keys 是**有界整数**（且能当 index 用）。这种 assumption 在真实系统里经常满足（比如 32 位整数 ID），但一旦 key 是任意可比较对象，就退回 comparison model。
- 顺着这条线往下看：Radix Sort 的 $n + n\log_n u$ 与 Sorted Array 的 $n\log n$ 相比，差别就在 $\log_n u$ 与 $\log n$ 这两个量——前者在 $u$ 是多项式大小时是常数。
