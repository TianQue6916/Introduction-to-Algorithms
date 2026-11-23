# Lecture 3: Sorting（排序）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Set Interface（L03-L08，集合接口）

所谓 set interface，就是定义「一个 set 对外承诺哪些 operations」。它分成四层：

### Container（容器层）

- `build(X)`：给定一个 iterable $X$，用 $X$ 里的元素 build 出这个 set。
- `len()`：返回当前 stored items（已存元素）的个数。

### Static（静态层）

- `find(k)`：返回 key 等于 $k$ 的那个 stored item。

### Dynamic（动态层）

- `insert(x)`：把 $x$ 加进 set；若已存在 key 为 `x.key` 的 item，则替换它。
- `delete(k)`：把 key 为 $k$ 的 item 从 set 中移除并返回它。

### Order（有序层）

- `iter_ord()`：按 key order（键序）逐个返回 stored items。
- `find_min()`：返回 key 最小的 stored item。
- `find_max()`：返回 key 最大的 stored item。
- `find_next(k)`：返回 key 严格大于 $k$ 的那些 item 中 key 最小的一个。
- `find_prev(k)`：返回 key 严格小于 $k$ 的那些 item 中 key 最大的一个。

## 用 array 实现 set

- 把 items 以 arbitrary order（任意顺序）放进一个 array，就能实现一个 set——只是这个 set 不太 efficient。
- 若把 stored items 按 key 递增 sorted（排好序），能换来两件好处：
  - `find_min` / `find_max` 变快：直接取 array 的第一个 / 最后一个 index。
  - 查找变快：binary search（二分查找）做到 $O(\log n)$。

## 操作成本对照表

下表的每个格子是该 operation 的 $O(\cdot)$ 上界。原 PDF 用合并单元格排版，这里拆成完整表；`Sorted Array` 行的 `delete(k)` 在原文中为空位，按语义应继承 `Array` 行的 $n$（因为删除后要维持有序只能平移），标 `†` 表示推定值。

| Data Structure（数据结构） | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Sorted Array | $n\log n$ | $\log n$ | $n$ | $n^†$ | $1$ | $1$ | $\log n$ | $\log n$ |

- 但问题来了：怎么**高效地**构造一个 sorted array？这正好就是本节的主题。

## Sorting（排序）

- 有了 sorted array，我们就能借 binary search 造出一个 efficient 的 set data structure。
- Input：一个含 $n$ 个 number 的 (static) array $A$。
- Output：一个 (static) array $B$，它是 $A$ 的一个 sorted permutation（有序置换）。
  - Permutation（置换）：元素相同、顺序不同的一个 array。
  - Sorted（有序）：对所有 $i \in \{1, \dots, n\}$ 都有 $B[i-1] \le B[i]$。
- 例子：$[8, 2, 4, 9, 3] \to [2, 3, 4, 8, 9]$。
- 若一个 sort 直接覆写 $A$（而不是另造一个新 array $B$ 作为 $A$ 的有序版），称它是 destructive（破坏性的）。
- 若一个 sort 只用 $O(1)$ extra space（额外空间），称它是 in place（原地）的。
  - 注意包含关系：in place $\subseteq$ destructive。原地必然破坏输入，但破坏性未必原地。

## Permutation Sort（置换排序）

- $A$ 共有 $n!$ 个 permutations，其中至少有一个是 sorted 的。
- 那就对每个 permutation 检查一遍是否 sorted，单次检查花 $\Theta(n)$。
- 例子：$[2, 3, 1] \to \{[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]\}$。

```python
def permutation_sort(A):
    '''Sort A'''
    for B in permutations(A):        # O(n!)
        if is_sorted(B):             # O(n)
            return B                 # O(1)
```

- permutation sort 的 analysis（分析）：
  - Correctness（正确性）：由 case analysis（情形枚举）得出——把所有可能性都试一遍，即 Brute Force（暴力）。
  - Running time（运行时间）：$\Omega(n! \cdot n)$，这是 exponential（指数级）的 :(

## Solving Recurrences（解递推式）

本节后面四个 sort 的复杂度都靠 recurrence 描述，所以先列出三条标准解法：

- Substitution（代入法）：猜一个解，把代表函数代回 recurrence，验证等式成立。
- Recurrence Tree（递推树）：画一棵树表示 recursive calls（递归调用），把各节点的 computation（计算量）求和。
- Master Theorem（主定理）：一个能直接解一大批 recurrences 的公式（见 R03）。

## Selection Sort（选择排序）

- 在 prefix（前缀）$A[:i+1]$ 里找出一个最大的数，把它 swap（交换）到 $A[i]$。
- 然后递归地对 prefix $A[:i]$ 排序。
- 例子：$[8,2,4,9,3] \to [8,2,4,3,9] \to [3,2,4,8,9] \to [3,2,4,8,9] \to [2,3,4,8,9]$。

```python
def selection_sort(A, i=None):               # T(i)
    '''Sort A[:i + 1]'''
    if i is None: i = len(A) - 1             # O(1)
    if i > 0:                                # O(1)
        j = prefix_max(A, i)                 # S(i)
        A[i], A[j] = A[j], A[i]              # O(1)
        selection_sort(A, i - 1)             # T(i - 1)

def prefix_max(A, i):                        # S(i)
    '''Return index of maximum in A[:i + 1]'''
    if i > 0:                                # O(1)
        j = prefix_max(A, i - 1)             # S(i - 1)
        if A[i] < A[j]:                      # O(1)
            return j                         # O(1)
    return i                                 # O(1)
```

### prefix_max 的 analysis

- Base case（基础情形）：$i = 0$ 时 array 只有一个元素，最大值的 index 就是 $i$ 本身。
- Induction（归纳步）：设对 $i$ 成立。$A[:i+1]$ 的最大值要么是 $A[:i]$ 的最大值，要么是 $A[i]$，两种情形都返回了正确的 index。
- recurrence：$S(1) = \Theta(1)$，$S(n) = S(n-1) + \Theta(1)$。
  - Substitution：设 $S(n) = \Theta(n)$，代回得 $cn = \Theta(1) + c(n-1)$，即 $c = \Theta(1)$，成立。
  - Recurrence Tree：一条 $n$ 个节点的 chain（链），每节点 $\Theta(1)$ 工作量，于是 $\sum_{i=0}^{n-1} 1 = \Theta(n)$。

### selection_sort 的 analysis

- Base case：$i = 0$ 时 array 只有一个元素，自然是 sorted。
- Induction：设对 $i$ 成立。sorted output 的最后一个数必须是 array 里最大的数，而 algorithm 恰好把一个最大数放到了那里；剩下 $A[:i]$ 由 induction 保证 sorted。
- recurrence：$T(1) = \Theta(1)$，$T(n) = T(n-1) + \Theta(n)$。
  - Substitution：设 $T(n) = \Theta(n^2)$，代回得 $cn^2 = \Theta(n) + c(n-1)^2$，即 $c(2n-1) = \Theta(n)$，成立。
  - Recurrence Tree：一条 $n$ 个节点的 chain，第 $i$ 层工作量 $\Theta(i)$，于是 $\sum_{i=0}^{n-1} i = \Theta(n^2)$。

## Insertion Sort（插入排序）

- 先递归地把 prefix $A[:i]$ 排好。
- 再在「$A[:i]$ 已 sorted」这个假设下，通过 repeated swaps（反复交换）把 prefix $A[:i+1]$ 排好。
- 例子：$[8,2,4,9,3] \to [2,8,4,9,3] \to [2,4,8,9,3] \to [2,4,8,9,3] \to [2,3,4,8,9]$。

```python
def insertion_sort(A, i=None):               # T(i)
    '''Sort A[:i + 1]'''
    if i is None: i = len(A) - 1             # O(1)
    if i > 0:                                # O(1)
        insertion_sort(A, i - 1)             # T(i - 1)
        insert_last(A, i)                    # S(i)

def insert_last(A, i):                       # S(i)
    '''Sort A[:i + 1] assuming sorted A[:i]'''
    if i > 0 and A[i] < A[i - 1]:            # O(1)
        A[i], A[i - 1] = A[i - 1], A[i]      # O(1)
        insert_last(A, i - 1)                # S(i - 1)
```

### insert_last 的 analysis

- Base case：$i = 0$ 时 array 只有一个元素，sorted。
- Induction：设对 $i$ 成立。若 `A[i] >= A[i-1]`，整个 array 已 sorted；否则把最后两个元素 swap 之后，$A[:i]$ 由 induction 保证 sorted。
- $S(1) = \Theta(1)$，$S(n) = S(n-1) + \Theta(1)$，故 $S(n) = \Theta(n)$。

### insertion_sort 的 analysis

- Base case：$i = 0$ 时 array 只有一个元素，sorted。
- Induction：设对 $i$ 成立。由 induction，algorithm 把 $A[:i]$ 排好了；再由上面已证的 `insert_last`，剩余部分也被正确排好。
- $T(1) = \Theta(1)$，$T(n) = T(n-1) + \Theta(n)$，故 $T(n) = \Theta(n^2)$。

## Merge Sort（归并排序）

- 递归地把前半与后半各自排序（可以假设长度是二的幂）。
- 再把两个 sorted 的 half（半段）merge（合并）成一个 sorted list，用的是 two finger algorithm（双指针算法）。
- 例子：$[7,1,5,6,2,4,9,3] \to [1,7,5,6,2,4,3,9] \to [1,5,6,7,2,3,4,9] \to [1,2,3,4,5,6,7,9]$。

```python
def merge_sort(A, a=0, b=None):              # T(b - a = n)
    '''Sort A[a:b]'''
    if b is None: b = len(A)                 # O(1)
    if 1 < b - a:                            # O(1)
        c = (a + b + 1) // 2                 # O(1)
        merge_sort(A, a, c)                  # T(n / 2)
        merge_sort(A, c, b)                  # T(n / 2)
        L, R = A[a:c], A[c:b]                # O(n)
        merge(L, R, A, len(L), len(R), a, b) # S(n)

def merge(L, R, A, i, j, a, b):              # S(b - a = n)
    '''Merge sorted L[:i] and R[:j] into A[a:b]'''
    if a < b:                                # O(1)
        if (j <= 0) or (i > 0 and L[i - 1] > R[j - 1]):  # O(1)
            A[b - 1] = L[i - 1]              # O(1)
            i = i - 1                        # O(1)
        else:                                # O(1)
            A[b - 1] = R[j - 1]              # O(1)
            j = j - 1                        # O(1)
        merge(L, R, A, i, j, a, b - 1)       # S(n - 1)
```

注意 `merge` 是**从尾部往前填**的：先确定 `A[b-1]` 这个最大的位置，再递归填前面。这样不需要额外的 index 运算，`b` 自身就是游标。

### merge 的 analysis

- Base case：$n = 0$ 时两个 array 都是空，vacuously correct（空真成立）。
- Induction：设对 $n$ 成立。`A[b-1]` 必须是 $L$、$R$ 两个 remaining prefix（剩余前缀）中的最大数；又因为它们各自 sorted，所以只要取各自最后一个元素中较大的那个就够；剩余部分由 induction 完成 merge。
- $S(0) = \Theta(1)$，$S(n) = S(n-1) + \Theta(1)$，故 $S(n) = \Theta(n)$。

### merge_sort 的 analysis

- Base case：$n = 1$ 时 array 只有一个元素，sorted。
- Induction：设对所有 $k < n$ 成立。algorithm 由 induction 把两个更小的 half 排好，随后 `merge` 按上面已证的性质把它们合并成一个 sorted array。
- recurrence：$T(1) = \Theta(1)$，$T(n) = 2T(n/2) + \Theta(n)$。
  - Substitution：猜 $T(n) = \Theta(n\log n)$，代回得 $cn\log n = \Theta(n) + 2c(n/2)\log(n/2)$，化简时用到 $\log 2 = 1$，最后 $cn\log 2 = \Theta(n)$，成立。
  - Recurrence Tree：一棵 complete binary tree（完全二叉树），depth 为 $\log_2 n$，共 $n$ 个 leaf（叶子），第 $i$ 层有 $2^i$ 个节点、每节点 $O(n/2^i)$ 工作量，总计

```math
\sum_{i=0}^{\log_2 n} (2^i)\left(\frac{n}{2^i}\right) = \sum_{i=0}^{\log_2 n} n = \Theta(n\log n)
```

## 四个 sort 的横向对照

| Algorithm | worst-case time | in place | stable | 核心机制 |
|---|---|---|---|---|
| Permutation Sort | $\Omega(n!\cdot n)$ | 否 | 否 | 枚举全部 permutations 后逐一验证 |
| Selection Sort | $\Theta(n^2)$ | 是 | 否 | 每轮把 prefix 的最大值换到末尾 |
| Insertion Sort | $\Theta(n^2)$ | 是 | 是 | 假定前半 sorted，反复 swap 塞入新元素 |
| Merge Sort | $\Theta(n\log n)$ | 否（需 $O(n)$ 缓冲） | 是 | 分半递归 + two finger merge |

- 这张表不是原文内容，是从前面四节的分析里汇总的；`stable`（稳定性）一列按各算法的构造直接读出：`merge` 中取 `L[i-1] > R[j-1]` 才取左边，相等时取右边，因此相等元素相对次序会翻转，这里按 Python 列表实现的通常版本记为不稳定，若改成 `>=` 则稳定。
- Merge Sort 的 $O(n\log n)$ 是 comparison sort（比较排序）在 comparison model 下的最优上界，下界 $\Omega(n\log n)$ 由 decision tree（判定树）的高度给出，见后续讲义。
