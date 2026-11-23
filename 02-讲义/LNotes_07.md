# Lecture 7: Binary Trees II: AVL（二叉树之二：AVL）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## Last Time and Today's Goal（上一讲与今天的目标）

### Sequence 方向

| Data Structure | `build(X)` | `get_at(i)` | `set_at(i,x)` | `insert_first(x)` | `delete_first()` | `insert_last(x)` | `delete_last()` | `insert_at(i,x)` | `delete_at(i)` |
|---|---|---|---|---|---|---|---|---|---|
| Binary Tree | $n$ | $h$ | $h$ | $h$ | $h$ | $h$ | $h$ | $h$ | $h$ |
| AVL Tree | $n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ |

### Set 方向

| Data Structure | `build(X)` | `find(k)` | `insert(x)` | `delete(k)` | `find_min()` | `find_max()` | `find_prev(k)` | `find_next(k)` |
|---|---|---|---|---|---|---|---|---|
| Binary Tree | $n\log n$ | $h$ | $h$ | $h$ | $h$ | $h$ | $h$ | $h$ |
| AVL Tree | $n\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ | $\log n$ |

> 表注：原 PDF 用合并单元格排版，文字层每行只抽出 5 个数值，上表按同一合并关系展开——Binary Tree 行所有格子取同一个值 $h$，AVL Tree 行所有格子取 $\log n$（`build` 除外）。

- 上一讲我们把所有 operations 的代价都归到 tree 的 height $h$ 上；这一讲要做的事，就是把 $h$ 钉死成 $O(\log n)$。

## Height Balance（高度平衡）

- 怎么维持 height $h = O(\log n)$，$n$ 是 tree 里 node 的个数？
- 若一棵 binary tree 在 dynamic operations 下能保持 $O(\log n)$ 的 height，就称它是 balanced（平衡的）。
  - 平衡方案有很多种：Red-Black Tree、Splay Tree、2-3 Tree 等等。
  - 最早提出的平衡方案是 AVL Tree（Adelson-Velsky 与 Landis，1962）。

## Rotations（旋转）

- 需要在不改变 traversal order 的前提下降低 tree 的 height，这样才能保证表示的还是同一串 items。
- 怎么在保持 traversal order 的同时改动 tree 的结构？答案是 rotation！
- 例子：`rotate_right(<D>)` 与它的逆操作 `rotate_left(<B>)`：

```text
旋转前:                    旋转后:
        D                        B
       / \                      / \
      B   E        =>          A   D
     / \                          / \
    A   C                        C   E
```

[Figure 1：一次 `rotate_right(<D>)`。D 有左子 B、右子 E；B 有左子 A、右子 C。右旋之后 B 上位成为 subtree 的根，B 的左子仍是 A，B 的右子变成 D；D 的左子变成 C，D 的右子仍是 E。结构变化只涉及 3 个指针重连。原文此图用 ASCII 画法把两棵树并排，中间用 `=>` 连接；`rotate_left(<B>)` 是同一个动作的逆方向]

- 一次 rotation 只重连 $O(1)$ 个 pointers，却改动了 tree 的结构、同时保持 traversal order 不变。

## Rotations Suffice（旋转已足够）

- Claim（命题）：用 $O(n)$ 次 rotations，可以把一棵 binary tree 变换成任何一棵与之 traversal order 相同的 binary tree。
- Proof（证明）：在 traversal order 里反复执行「最后一个可能的 right rotation」，得到的树是一条 canonical chain（规范链）。每做一次 rotation，最后一个 node 的 depth 增加 1。最终 chain 中最后一个 node 的 depth 是 $n-1$，所以至多执行 $n-1$ 次 rotations。再把这一串 canonical rotations 逆着做回去，就能到达目标树。
- 所以理论上可以用 $O(n)$ 次 rotations 把 tree 彻底 balance 好，但这太慢 :(
- 我们的目标是：每次 operation 只用 $O(\log n)$ 时间去保持平衡！

## AVL Trees: Height Balance（AVL 树的高度平衡）

- AVL tree 维持 height-balance（高度平衡），也叫 AVL Property：
  - 若一个 node 的左右两个 subtree 的 heights 相差不超过 1，称它 height-balanced。
  - 定义 node 的 skew（偏斜）为 right subtree 的 height 减去 left subtree 的 height。
  - 于是 node 是 height-balanced 等价于它的 skew 属于 $\{-1, 0, 1\}$。
- Claim：若一棵 binary tree 的所有 node 都 height-balanced，则它的 height $h = O(\log n)$（等价地 $n = 2^{\Omega(h)}$）。
- Proof：只需证任何高度为 $h$ 的树里最少 node 数 $F(h)$ 满足 $F(h) = 2^{\Omega(h)}$。

```math
F(0) = 1,\quad F(1) = 2,\quad F(h) = 1 + F(h-1) + F(h-2) \ge 2F(h-2) \;\Longrightarrow\; F(h) \ge 2^{h/2}
```

- 这个递推的含义值得点明：要让高度为 $h$ 而 node 尽量少，两个子树的高度只能是 $h-1$ 与 $h-2$（否则违反 skew $\le 1$），于是出现类似 Fibonacci 的递推，每两层至少翻一倍，这才给出 $2^{h/2}$。
- 现在假设在某棵 height-balanced 的树上加一个或删一个 leaf，结果出现了 imbalance：
  - 只有该 leaf 的 ancestors（祖先们）的 height 或 skew 可能变化。
  - 而 heights 只变化了 $\pm 1$，所以 skews 的绝对值仍然 $\le 2$。
  - Idea：从 leaf 往上、一路修到 root，逐个修复 ancestors 的 height-balance。
  - 具体做法：反复地 rebalance（再平衡）最低的那个不平衡 ancestor，wlog（不失一般性）假设它的 skew 是 2。

## Local Rebalance（局部再平衡）

- 给定 binary tree 的一个 node `<B>`，满足：
  - 它的 skew 是 2，且
  - `<B>` 的 subtree 里其他所有 node 都 height-balanced，
  - 那么 `<B>` 的 subtree 可以通过一次或两次 rotations 变成 height-balanced。
  - （做完之后 `<B>` 的 height 与之前相同，或比之前少 1。）
- Proof：
  - 既然 `<B>` 的 skew 是 2，`<B>` 的 right child `<F>` 必然存在。
  - Case 1：`<F>` 的 skew 是 0；或 Case 2：`<F>` 的 skew 是 1：
    - 对 `<B>` 执行一次 left rotation。

```text
旋转前 (Case 1 / 2):           旋转后:
          B                          F
         / \                        / \
        A   F          =>          B   G
           / \                    / \
          D   G                  A   D
```

[Figure 2：Local Rebalance 的 Case 1 与 Case 2。`<B>` skew 为 2，说明右子树比左子树高 2；右子 `<F>` 的 skew 为 0（Case 1）或 1（Case 2）。一次 `rotate_left(<B>)` 之后 `<F>` 上位，`<B>` 成为 `<F>` 的左子，`<D>`（原 `<F>` 的左子）转挂到 `<B>` 的右侧。原文用 ASCII 画法并排两棵树]

  - 令 $h = \mathrm{height}(\langle A\rangle)$。则 $\mathrm{height}(\langle G\rangle) = h+1$，而 $\mathrm{height}(\langle D\rangle)$ 在 Case 1 中是 $h+1$、在 Case 2 中是 $h$。
  - rotation 之后：
    - `<B>` 的 skew 在 Case 1 中为 1、在 Case 2 中为 0，所以 `<B>` 已 height-balanced。
    - `<F>` 的 skew 为 $-1$，所以 `<F>` 已 height-balanced。
    - `<B>` 的 height 原来是 $h+3$；之后在 Case 1 中仍是 $h+3$，在 Case 2 中是 $h+2$。
  - Case 3：`<F>` 的 skew 是 $-1$，于是 `<F>` 的 left child `<D>` 存在：
    - 先对 `<F>` 执行一次 right rotation，再对 `<B>` 执行一次 left rotation。

```text
旋转前 (Case 3):                旋转后:
          B                          D
         / \                        / \
        A   F          =>          B   F
           / \                    / \ / \
          D   G                  A  C E  G
         / \
        C   E
```

[Figure 3：Local Rebalance 的 Case 3，即所谓 double rotation（双旋）。先 `rotate_right(<F>)` 把 `<D>` 提到 `<F>` 的位置，再 `rotate_left(<B>)` 把 `<D>` 提到整棵 subtree 的根。最终 `<D>` 的两个子分别是 `<B>`（子为 `<A>`、`<C>`）与 `<F>`（子为 `<E>`、`<G>`）。原文用 ASCII 画法并排两棵树]

  - 令 $h = \mathrm{height}(\langle A\rangle)$。则 $\mathrm{height}(\langle G\rangle) = h$，而 $\mathrm{height}(\langle C\rangle)$ 与 $\mathrm{height}(\langle E\rangle)$ 各自要么是 $h$ 要么是 $h-1$。
  - rotation 之后：
    - `<B>` 的 skew 是 0 或 $-1$，所以 `<B>` 已 height-balanced。
    - `<F>` 的 skew 是 0 或 1，所以 `<F>` 已 height-balanced。
    - `<D>` 的 skew 是 0，所以 `<D>` 已 height-balanced。
    - `<B>`（指这棵 subtree 的原根位置）的 height 原来是 $h+3$，之后是 $h+2$。

## Global Rebalance（全局再平衡）

- 从一棵 height-balanced 的树 $T$ 上添加或删除一个 leaf，得到树 $T'$。则 $T'$ 可以通过至多 $O(\log n)$ 次 rotations 变换成一棵 height-balanced 的树 $T''$。
- Proof：
  - 在 $T'$ 与 $T$ 中，只有被影响的那个 leaf 的 ancestors 的 height 不同。
  - 被影响的 leaf 至多有 $h = O(\log n)$ 个 ancestors，它们的 subtrees 可能发生了变化。
  - 令 `<X>` 是「不是 height-balanced」的最低那个 ancestor（其 skew 绝对值为 2）。
  - 若在 $T$ 中**添加**了一个 leaf：
    - insertion 提高了 `<X>` 的 height，所以落入 Local Rebalancing 的 Case 2 或 Case 3。
    - 那次 rotation 会降低 subtree 的 height，所以一次 rotation 之后就平衡了。
  - 若从 $T$ 中**删除**了一个 leaf：
    - deletion 降低的是 `<X>` 某个 child 的 height，而不是 `<X>` 自己的，所以这只是 imbalance 的来源。
    - 它可能把 `<X>` 的 height 降低 1；于是 `<X>` 的 parent 现在可能也 imbalance 了。
    - 所以可能要沿着 `<X>` 的每个 ancestor 都 rebalance 一遍，但这样的 ancestors 至多有 $h = O(\log n)$ 个。
- 于是 insertion / deletion 之后，只用 $O(\log n)$ 次 rotations 就能维持 height-balance！
- 但这要求我们能判断「可能多达 $O(\log n)$ 个 node 是否 height-balanced」——这就引出了下一节。

## Computing Height（计算高度）

- 怎么判断 node `<X>` 是否 height-balanced？算两个 subtree 的 heights！
- 怎么算 node `<X>` 的 height？朴素 algorithm：
  - 递归算 `<X>` 的 left 与 right subtrees 的 height。
  - 取两者最大值再加 1。
  - 这跑 $\Omega(n)$ 时间，因为要对每个 node 都递归一次 :(
- Idea：给每个 node 增广一个「它 subtree 的 height」！（细节留到后面）
- 有了增广，`<X>` 的 height 可以在 $O(1)$ 时间内由两个 children 的 heights 算出：
  - 用 $O(1)$ 时间查 left 与 right subtrees 存好的 heights。
  - 取两者最大值再加 1。
- 在 dynamic operations 期间，tree 形状变了，我们必须同步维护这个 augmentation。
- 做法是：在每一个 subtree 发生变化的 node 上重算 subtree augmentations：
  - 一次 rotation 里被重连的 nodes 在 $O(1)$ 时间更新（它们的 ancestors 不变）。
  - 被插入或删除的 node 的所有 ancestors，靠沿 tree 往上走，在 $O(h)$ 时间更新。

## Steps to Augment a Binary Tree（给二叉树做增广的步骤）

- 一般地，要用一个 subtree property $P$ 去增广一棵 binary tree，你必须做两件事：
  - 说清楚要在每个 node `<X>` 上存什么 subtree property $P(\langle X\rangle)$。
  - 证明如何从 `<X>` 的 children 的 augmentations 在 $O(1)$ 时间内算出 $P(\langle X\rangle)$。
- 只要这两件事成立，stored property $P(\langle X\rangle)$ 就能被维护，而不会改变 dynamic operations 的代价。

## Application: Sequence（应用：序列）

- 对 sequence binary tree，我们需要知道 subtree 的 sizes。
- 若只做 leaf 的插入 / 删除，这很容易；但现在还要处理 rotations，就得多想一步。
- Subtree size 正是一个 subtree property，所以可以用 augmentation 维护：
  - 由两个 children 的 sizes 求和再加 1，就算出了本 node 的 size。
- 关键在于：rotation 会改动 nodes 的父子关系，因此 rotation 中被重连的那几个 node 都要重算 size，这与上一节「重连 nodes 在 $O(1)$ 更新」是同一件事。

## Conclusion（小结）

- Set AVL tree 对所有 set operations 都达到 $O(\lg n)$ 时间，例外是 `build` 花 $O(n\log n)$、`iter` 花 $O(n)$。
- Sequence AVL tree 对所有 sequence operations 都达到 $O(\lg n)$ 时间，例外是 `build` 与 `iter` 花 $O(n)$。
- 两个 interface 的 Goal 行到这里全部达成。整条主线可以概括成：pointer-based 结构给了 worst-case 保证，binary tree 给了 traversal order 这个「免费的序」，AVL 的 skew 约束把 height 钉死在 $O(\log n)$。

## Application: Sorting（应用：排序）

- 任何 Set data structure 都隐含一个 sorting algorithm：先 `build`（或反复 `insert`），再 `iter`。
- 例子：Lecture 5 的 Direct Access Array Sort 就是这种构造。
- AVL Sort 因此是一个新的 $O(n\lg n)$ 时间 sorting algorithm。
- 注意这里没有矛盾：Lecture 5 已经证明 comparison sort 的下界是 $\Omega(n\log n)$，AVL Sort 恰好打到这个下界，说明它是 comparison model 下最优的那一类。
