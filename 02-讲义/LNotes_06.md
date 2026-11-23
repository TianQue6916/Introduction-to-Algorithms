# Lecture 6: Binary Trees I（二叉树之一）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Previously and New Goal（既有成果与新目标）

### Sequence interface 的现状

| Data Structure | `build(X)` | `get_at(i)` | `set_at(i,x)` | `insert_first(x)` | `delete_first()` | `insert_last(x)` | `delete_last()` | `insert_at(i,x)` | `delete_at(i)` |
|---|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $1$ | $1$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Linked List | $n$ | $n$ | $n$ | $1$ | $1$ | $n$ | $n$ | $n$ | $n$ |
| Dynamic Array | $n$ | $1$ | $1$ | $n$ | $n$ | $1^{(a)}$ | $1^{(a)}$ | $n$ | $n$ |
| Goal（目标） | $n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ |

> 表注：$(a)$ = amortized。原 PDF 是合并单元格排版，文字层每行只抽出 5 个数值；上表中 `get_at` / `set_at` 同值合并、`insert_first` / `delete_first` 同值合并、`insert_last` / `delete_last` 同值合并这几处是按 6.006 标准表补全的，标 `†` 的格子为推定值（Array 行 `set_at` 为 $1^{†}$，Linked List 行 `set_at` 为 $n^{†}$）。

### Set interface 的现状

| Data Structure | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Array | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ | $n$ |
| Sorted Array | $n\log n$ | $\log n$ | $n$ | $n$ | $1$ | $1$ | $\log n$ | $\log n$ |
| Direct Access Array | $u$ | $1$ | $1$ | $1$ | $u$ | $u$ | $u$ | $u$ |
| Hash Table | $n^{(e)}$ | $1^{(e)}$ | $1^{(a)(e)}$ | $1^{(a)(e)}$ | $n$ | $n$ | $n$ | $n$ |
| Goal（目标） | $n\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ |

- 注意到两个 interface 的 Goal 行完全一样：**每一个 operation 都是 $O(\log n)$**。这一讲就是奔着它去的。
- 怎么做到？靠 binary tree！

## Binary Tree（二叉树）的基本构造

- 上一讲之前我们用的都是 array 类结构；pointer-based data structure（基于指针的数据结构，如 Linked List）能拿到 worst-case 的性能保证。
- binary tree 就是一种 pointer-based data structure，每个 node 存三个 pointers。
- node 的表示：`node.{item, parent, left, right}`。
- 例子（一棵六个节点的 binary tree）：

```text
           A
         /   \
        B     C
       / \
      D   E
     /
    F
```

[Figure 1：一棵示例 binary tree，共 6 个节点。根是 A；A 的左子 B、右子 C；B 的左子 D、右子 E；D 的左子 F；C、E、F 均无子。原文用 ASCII 字符画，此处按同一结构重画]

对应的 node 表（原 PDF 表 1，逐行是 node / item / parent / left / right）：

| node | item | parent | left | right |
|---|---|---|---|---|
| `<A>` | A | - | `<B>` | `<C>` |
| `<B>` | B | `<A>` | `<D>` | `<E>` |
| `<C>` | C | `<A>` | - | - |
| `<D>` | D | `<B>` | `<F>` | - |
| `<E>` | E | `<B>` | - | - |
| `<F>` | F | `<D>` | - | - |

## Terminology（术语）

- tree 的 root（根）没有 parent（例：`<A>`）。
- tree 的 leaf（叶子）没有 children（例：`<C>`、`<E>`、`<F>`）。
- 在以 `<R>` 为根的树中，定义 node `<X>` 的 depth(`<X>`) 为从 `<X>` 到 `<R>` 的 path 长度。
- 定义 node `<X>` 的 height(`<X>`) 为以 `<X>` 为根的 subtree（子树）中任何 node 的 depth 的最大值。
- Idea：把所有 operations 设计成跑 $O(h)$ 时间，$h$ 是根的 height；然后再去维持 $h = O(\log n)$。
- 一个 binary tree 自带一种 inherent order（固有顺序），就是它的 traversal order（遍历序）：
  - node `<X>` 的 left subtree 里每一个 node 都排在 `<X>` 之前。
  - node `<X>` 的 right subtree 里每一个 node 都排在 `<X>` 之后。
- 从 root 出发用一个 recursive algorithm 就能按 traversal order 列出所有 nodes：
  - 递归列出 left subtree，列出自己，再递归列出 right subtree。
  - 跑 $O(n)$ 时间，因为每个 node 的列出只花 $O(1)$。
  - 例子：traversal order 是 (`<F>`, `<D>`, `<B>`, `<E>`, `<A>`, `<C>`)。
- 目前 traversal order 与 stored items 之间还没有任何语义关系。
- 后面我们会给 traversal order 赋予语义，用它来实现 Sequence / Set 两种 interface。

## Tree Navigation（树的导航）

### 找 subtree 里的第一个节点

- 找 node `<X>` 的 subtree 在 traversal order 里的第一个 node（最后一个是镜像情形）。
  - 若 `<X>` 有 left child，则递归返回 left subtree 的第一个 node。
  - 否则 `<X>` 自己就是第一个 node，直接返回它。
  - Running time 是 $O(h)$，$h$ 是 tree 的 height。
  - 例子：`<A>` 的 subtree 里第一个 node 是 `<F>`。

### 找 successor / predecessor

- 找 node `<X>` 在 traversal order 中的 successor（后继，predecessor 即前驱是镜像情形）。
  - 若 `<X>` 有 right child，则返回 right subtree 的第一个 node。
  - 否则，沿 parent 往上走，返回「`<X>` 落在其 left subtree 里」的最低那个 ancestor（祖先）。
  - Running time 是 $O(h)$，$h$ 是 tree 的 height。
  - 例子：successor 依次为——`<B>` 的是 `<E>`，`<E>` 的是 `<A>`，`<C>` 的是 None。

## Dynamic Operations（动态操作）

- 任何改动都只涉及单个 item：只增删 leaves，不改中间结构：
  - 在 traversal order 中某个 node 之后插入一个 node（之前是镜像情形）。
  - 从 tree 里移除一个 item。
- 在 traversal order 中把 node `<Y>` 插到 node `<X>` 之后：
  - 若 `<X>` 没有 right child，就把 `<Y>` 设为 `<X>` 的 right child。
  - 否则，把 `<Y>` 设为 `<X>` 的 successor 的 left child（那个 successor 必然没有 left child）。
  - Running time 是 $O(h)$，$h$ 是 tree 的 height。

### 例：把 `<G>` 插到 traversal order 中 `<E>` 之前

```text
插入前:            插入后:
      A                  A
     / \                / \
    B   C              B   C
   / \                / \
  D   E              D   E
 /                  /   /
F                  F   G
```

[Figure 2：原文用 ASCII 字符画给出的插入过程。`<G>` 要插在 `<E>` 之前，而 `<E>` 是 `<B>` 的 right child 且无 left child，因此 `<G>` 直接成为 `<E>` 的 left child。结构变化只有一个指针赋值]

### 例：把 `<H>` 插到 traversal order 中 `<A>` 之后

```text
插入前:            插入后:
      A                  A
     / \                / \
    B   C              B   C
   / \                / \   \
  D   E              D   E   H
 /   /              /   /
F   G              F   G
```

[Figure 3：`<H>` 要插在 `<A>` 之后，而 `<A>` 的 right child 是 `<C>` 且 `<C>` 无 left child，因此 `<H>` 成为 `<C>` 的 left child（按 successor 规则走的是「`<X>` 的 successor 的左子」这条分支）]

### 从 subtree 里删除 `<X>` 上的 item

- 若 `<X>` 是 leaf，直接从 parent 上摘下并 return。
- 否则 `<X>` 至少有一个 child：
  - 若 `<X>` 有 left child，就与 `<X>` 的 predecessor 交换 items，然后递归。
  - 否则 `<X>` 有 right child，就与 `<X>` 的 successor 交换 items，然后递归。
- Running time 是 $O(h)$，$h$ 是 tree 的 height。
- 这个策略的要点：**永远只删 leaf**。非 leaf 的情形靠「与邻位的 leaf 换 item」把要删的东西一路换到叶子上，结构始终合法。

### 例：删除 `<F>`（它是 leaf）

```text
删除前:              删除后:
      A                    A
     / \                  / \
    B   C                B   C
   / \   \              / \   \
  D   E   H            D   E   H
 /   /                /   /
F   G                G   （F 已摘下）
```

[Figure 4：`<F>` 是 `<D>` 的 left child 且无子，删除动作就是把 `<D>` 的 left 指针置空。其余结构不动]

### 例：删除 `<A>`（非 leaf，先换到 leaf）

```text
第 1 步:            第 2 步:            第 3 步:
      A                  E                  E
     / \                / \                / \
    B   C              B   C              B   C
   / \   \            / \   \            / \   \
  D   E   H          D   G   H          D   G   H
 /   /              /                  /
F   G              F                  F
                   （A 换到原 E 位置）
```

[Figure 5：删除 `<A>` 的三步。第 1 步是原树；`<A>` 有 left child，所以与 predecessor（`<E>`）交换 items，得第 2 步；此时 `<A>` 落到一个无子的位置，按叶子情形摘下，得第 3 步。原文此处的 ASCII 图为三列并排，中间用 `=>` 连接]

## Application: Set（应用之一：集合）

- Idea！Set Binary Tree（集合二叉树），也叫 Binary Search Tree / BST：
  - 让 traversal order 就是按 key 递增的 sorted order。
  - 等价说法是 BST Property（BST 性质）：对每个 node，left subtree 里所有 key $\le$ 该 node 的 key $\le$ right subtree 里所有 key。
- 于是可以在 node `<X>` 的 subtree 里用 binary search 的方式在 $O(h)$ 时间内找到 key 为 $k$ 的 node：
  - 若 $k$ 小于 `<X>` 处的 key，递归进 left subtree（或 return None）。
  - 若 $k$ 大于 `<X>` 处的 key，递归进 right subtree（或 return None）。
  - 否则，返回存在 `<X>` 里的那个 item。
- 其他 Set operations 都遵循同一套模式；细节见 recitation（复习课）。

## Application: Sequence（应用之二：序列）

- Idea！Sequence Binary Tree（序列二叉树）：让 traversal order 就是 sequence order（序列序）。
- 怎么在一个 subtree 的 traversal order 里找到第 $i$ 个 node？把这个 operation 叫 `subtree_at(i)`。
- 当然可以把整个 traversal order 遍历一遍，但那很糟，是 $O(n)$。
- 然而，如果我们能在 $O(1)$ 内算出一个 subtree 的 size，就能在 $O(h)$ 时间内解决：
  - 怎么算？先看 left subtree 的 size $n_L$，把它与 $i$ 比较。
  - 若 $i < n_L$，递归进 left subtree。
  - 若 $i > n_L$，递归进 right subtree，同时把 $i$ 换成 $i' = i - n_L - 1$。
  - 否则 $i = n_L$，你已经到达了目标 node！
- 每个 node 的 subtree size 靠 augmentation（增广）维护，就直接挂在那个 node 上：
  - 给每个 node 加一个 `node.size` field。
  - 新增 leaf 时，对所有 ancestor $a$ 做 `a.size += 1`，花 $O(h)$ 时间。
  - 删除 leaf 时，对所有 ancestor $a$ 做 `a.size -= 1`，花 $O(h)$ 时间。
- Sequence 的其他 operations 都能直接从快的 `subtree_at(i)` 推出来。
- 朴素地做，`build(X)` 要 $O(nh)$ 时间，但可以做到 $O(n)$；细节见 recitation。

## So Far（阶段小结）

### Set 方向

| Data Structure | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Binary Tree | $n\log n$ | $h$ | $h$ | $h$ | $h$ | $h$ | $h^†$ | $h^†$ |
| Goal | $n\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ |

### Sequence 方向

| Data Structure | `build(X)` | `get_at(i)` | `set_at(i,x)` | `insert_first(x)` | `delete_first()` | `insert_last(x)` | `delete_last()` | `insert_at(i,x)` | `delete_at(i)` |
|---|---|---|---|---|---|---|---|---|---|
| Binary Tree | $n$ | $h$ | $h$ | $h^†$ | $h^†$ | $h^†$ | $h^†$ | $h$ | $h$ |
| Goal | $n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ |

> 表注：原 PDF 这两张表的文字层每行只抽出 5 个数值（合并单元格），带 `†` 的格子是按各 operation 的实现语义补的推定值，不是原文断言。

- 我们现在卡在同一个地方：所有 operations 都是 $O(h)$，而 $h$ 没有任何保证——最坏情况下一棵退化成 chain 的 binary tree 有 $h = \Theta(n)$，那就什么都不省了。

## Next Time（下一讲）

- 在 insertion 或 deletion 之后，让 binary tree 保持 balanced（平衡）。
- 通过维持 $h = O(\log n)$，把所有 $O(h)$ 的 running time 降到 $O(\log n)$。
