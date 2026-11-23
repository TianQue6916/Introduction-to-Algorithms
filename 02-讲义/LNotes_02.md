# Lecture 2: Data Structures（数据结构）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Data Structure Interfaces（数据结构接口）

- 一个 data structure 是存储 data 的方式，并配有对该 data 执行 operations 的 algorithms。
- 所支持 operations 的 collection 称为 interface（接口），也叫 API 或 ADT（抽象数据类型）。
- interface 是一份 specification（规格说明）：它规定支持哪些 operations——这对应 problem（问题）本身！
- data structure 则是一种 representation（表示）：它规定这些 operations 如何被支持——这对应 solution（解）！
- 本课有两个主要 interface：Sequence（序列）与 Set（集合）。

## Sequence Interface（序列接口，L02、L07）

- 维护一个 items 的 sequence（序列），其 order（顺序）是 extrinsic（外在的）。
- 例：$(x_0, x_1, x_2, \dots, x_{n-1})$（zero indexing，从零开始编号）。
- 约定用 $n$ 表示 data structure 中当前存储的 item 数量。
- 它支持以下 sequence operations：

[Table 1：Sequence interface 的操作清单。原 PDF 用「Container / Static / Dynamic」三行分组的表格形式给出，此处保留分组与原文操作说明]

| 类别 | Operation | 语义 |
|---|---|---|
| Container | `build(X)` | 给定一个 iterable $X$，用 $X$ 中的 items 构造 sequence |
| Container | `len()` | 返回当前存储的 items 数量 |
| Static | `iter_seq()` | 按 sequence order 逐个返回存储的 items |
| Static | `get_at(i)` | 返回第 $i$ 个 item |
| Static | `set_at(i, x)` | 把第 $i$ 个 item 替换为 $x$ |
| Dynamic | `insert_at(i, x)` | 把 $x$ 作为第 $i$ 个 item 插入 |
| Dynamic | `delete_at(i)` | 移除并返回第 $i$ 个 item |
| Dynamic | `insert_first(x)` | 把 $x$ 作为第一个 item 插入 |
| Dynamic | `delete_first()` | 移除并返回第一个 item |
| Dynamic | `insert_last(x)` | 把 $x$ 作为最后一个 item 插入 |
| Dynamic | `delete_last()` | 移除并返回最后一个 item |

- 两种 special case interfaces（特例接口）：
  - stack（栈）：只有 `insert_last(x)` 与 `delete_last()`（后进先出）
  - queue（队列）：只有 `insert_last(x)` 与 `delete_first()`（先进先出）

## Set Interface（集合接口，L03-L08）

- Sequence 关心 extrinsic order（外在顺序），Set 关心 intrinsic order（内在顺序）。
- 维护一个 item 的 set，其中每个 item 有 unique key（唯一键，例如 item $x$ 有 `x.key`）。
- （是 Set 还是 multi-set？这里先限制为 unique keys。）
- 我们常常把 item 的 key 就取作 item 本身，但有时也需要在 key 之外存储更多信息。
- 它支持以下 set operations：

[Table 2：Set interface 的操作清单。原 PDF 同样按 Container / Static / Dynamic / Order 分组]

| 类别 | Operation | 语义 |
|---|---|---|
| Container | `build(X)` | 给定 iterable $X$，用 $X$ 中的 items 构造 set |
| Container | `len()` | 返回当前存储的 item 数量 |
| Static | `find(k)` | 返回 key 为 $k$ 的那个已存储 item |
| Dynamic | `insert(x)` | 把 $x$ 加入 set（若已存在 key 为 `x.key` 的 item，则替换它） |
| Dynamic | `delete(k)` | 移除并返回 key 为 $k$ 的那个已存储 item |
| Order | `iter_ord()` | 按 key order 逐个返回存储的 items |
| Order | `find_min()` | 返回 key 最小的已存储 item |
| Order | `find_max()` | 返回 key 最大的已存储 item |
| Order | `find_next(k)` | 返回 key 大于 $k$ 的所有 item 中 key 最小的那个 |
| Order | `find_prev(k)` | 返回 key 小于 $k$ 的所有 item 中 key 最大的那个 |

- 一种 special case interface：
  - dictionary（字典）：就是去掉 Order operations 的 set
- 在 recitation（习题课）中，你会被要求：给定一个 Sequence data structure，实现一个 Set。

## Array Sequence（数组序列）

- Array 对 static operations 非常合适！`get_at(i)` 与 `set_at(i, x)` 都是 $\Theta(1)$ 时间！
- 但对 dynamic operations 就不那么理想了……
- （为保持一致，我们维护「array 始终是满的」这一 invariant。）
- 于是插入与移除 item 需要：
  - reallocate（重新分配）整个 array
  - 把被修改 item 之后的所有 items 都 shift（平移）过去
- 由此得到 Array 的 worst case（最坏情况）代价：

[Table 3：Array 的 operation 复杂度，worst case，单位 $O(\cdot)$。原 PDF 表格存在单元格合并，文字层只抽出 `n, 1, n, n, n` 五个数值；未抽出的列按正文「插入与移除需要 reallocate 并 shift 后续所有 items」推定为 $n$，已在下表标注 †]

| Data Structure（数据结构） | `build(X)` | `get_at(i)` | `set_at(i, x)` | `insert_first(x)` | `delete_first()` | `insert_last(x)` | `delete_last()` | `insert_at(i, x)` | `delete_at(i)` |
|---|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $1$ | $1^{\dagger}$ | $n$ | $n$ | $n^{\dagger}$ | $n^{\dagger}$ | $n^{\dagger}$ | $n^{\dagger}$ |

## Linked List Sequence（链表序列）

- 注意：这是 pointer data structure（指针数据结构），与 Python 的 "list" 没有关系。
- 每个 item 存放在一个 node（节点）中，node 里含有指向 sequence 中下一个 node 的 pointer（指针）。
- 每个 node 有两个 fields（字段）：`node.item` 与 `node.next`。
- 只要重新连接 pointers（relink），就能直接操纵 nodes！
- 维护一个指向 sequence 第一个 node 的 pointer，称为 head（头）。
- 现在可以在 $\Theta(1)$ 时间内从 front（前端）插入与删除！很好！
- （从 back（后端）高效地插入/删除同样可行；这件事你在 PS1 里会做。）
- 但现在 `get_at(i)` 与 `set_at(i, x)` 各自要花 $O(n)$ 时间……很不理想。
- 能不能把两边的优点都拿到？可以！（某种意义上……）
- Linked List 的 worst case 代价：

[Table 4：Linked List 的 operation 复杂度，worst case。原 PDF 同样存在单元格合并，文字层抽出 `n, n, 1, n, n`；按下表标注 † 的列依正文「可对指针 relink，故 front 操作为 $\Theta(1)$；按 index 访问必须沿 `next` 逐个走」推定]

| Data Structure | `build(X)` | `get_at(i)` | `set_at(i, x)` | `insert_first(x)` | `delete_first()` | `insert_last(x)` | `delete_last()` | `insert_at(i, x)` | `delete_at(i)` |
|---|---|---|---|---|---|---|---|---|---|
| Linked List | $n$ | $n$ | $n^{\dagger}$ | $1$ | $1$ | $n$ | $n$ | $n^{\dagger}$ | $n^{\dagger}$ |

## Dynamic Array Sequence（动态数组序列）

- 让 array 对 last（末尾）的 dynamic operations 变得高效。
- Python 的 "list" 就是 dynamic array。
- Idea！多分配一些额外空间，这样就不必每次 dynamic operation 都重新分配。
- fill ratio（填充率）：$0 \le r \le 1$，即 items 数量与已分配空间之比。
- 每当 array 满了（$r = 1$），就在末尾分配 $\Theta(n)$ 的额外空间，使 fill ratio 降到 $r_i$（例如 $1/2$）。
- 这样在下一次 reallocation 之前，必须先插入 $\Theta(n)$ 个 items。
- 单次 operation 可能为了 reallocation 花掉 $\Theta(n)$ 时间。
- 但是，任意 $\Theta(n)$ 个 operations 的序列总共只花 $\Theta(n)$ 时间。
- 因此「平均而言」每个 operation 花 $\Theta(1)$ 时间。

## Amortized Analysis（均摊分析）

- 这是一种 data structure 分析技术，用来把代价分摊到许多 operations 上。
- 若 $k$ 个 operations 的总代价至多为 $k \cdot T(n)$，则称该 operation 具有 amortized cost（均摊代价）$T(n)$。
- 「$T(n)$ amortized」大致就是说：在许多 operations 上「平均」为 $T(n)$。
- 向 dynamic array 中插入元素的 amortized time 是 $\Theta(1)$。
- 更多 amortization analysis 技术见 6.046！

## Dynamic Array Deletion（动态数组的删除）

- 从 back 删除？不费力气就是 $\Theta(1)$ 时间，很好！
- 但空间上可能非常浪费。我们希望 data structure 的 size 维持在 $\Theta(n)$。
- 一个尝试：若 array 非常空，就 resize 到 $r = 1$。但交替进行插入与删除可能很糟……
- Idea！当 $r < r_d$ 时，把 array resize 到 fill ratio $r_i$，其中 $r_d < r_i$（例如 $r_d = 1/4$，$r_i = 1/2$）。
- 这样在下一次昂贵的 resize 之前，必须先做 $\Theta(n)$ 次便宜的 operations。
- 于是可以把额外空间用量限制在 $(1+\varepsilon)n$ 以内，对任意 $\varepsilon > 0$ 都成立。具体取法为

```math
r_d = \frac{1}{1+\varepsilon}, \qquad r_i = \frac{1+\varepsilon}{2}
```

此时 $r_d < r_i$ 自动满足。
- Dynamic arrays 只在 last 方向的 dynamic operations 上做到 $\Theta(1)$ 时间。
- Python List 的 `append` 与 `pop` 是 amortized $O(1)$ 时间，其他 operations 可能是 $O(n)$！
- （从 front 高效地插入/删除同样可行；这件事你在 PS1 里会做。）
- 三种 sequence data structure 的对照：

[Table 5：Array / Linked List / Dynamic Array 的 operation 复杂度总表，worst case。Dynamic Array 的 `insert_last`、`delete_last` 原文件标为 $1^{(a)}$，其中 $(a)$ 表示 amortized]

| Data Structure | `build(X)` | `get_at(i)` | `set_at(i, x)` | `insert_first(x)` | `delete_first()` | `insert_last(x)` | `delete_last()` | `insert_at(i, x)` | `delete_at(i)` |
|---|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $1$ | $1$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Linked List | $n$ | $n$ | $n$ | $1$ | $1$ | $n$ | $n$ | $n$ | $n$ |
| Dynamic Array | $n$ | $1$ | $1$ | $n$ | $n$ | $1^{(a)}$ | $1^{(a)}$ | $n$ | $n$ |

其中 $(a)$ 表示 amortized（均摊）意义下的界：单次操作可能因为 resize 而达到 $\Theta(n)$，但一串操作的均摊代价是 $\Theta(1)$。

---

## 版权页（原第 5 页）

MIT OpenCourseWare，https://ocw.mit.edu
6.006 Introduction to Algorithms，Spring 2020
关于引用这些材料或使用条款的信息，见 https://ocw.mit.edu/terms
