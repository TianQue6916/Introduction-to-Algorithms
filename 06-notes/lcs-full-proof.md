# LCS 问题全套严格证明

> 从第一性原理出发，自包含。使用"匹配位置"（$i_k, j_k$）替代模糊的"$z_k \neq x_m$"。
> 符号约定：$X[1..i]$ 表示 $X$ 的长度为 $i$ 的前缀；$X[1..0]$ 为空序列。

---

## 一、形式化定义

**定义 1（子序列）** 设 $X = \langle x_1, \ldots, x_m \rangle$ 为有限序列。序列 $Z = \langle z_1, \ldots, z_k \rangle$ 称为 $X$ 的 **subsequence（子序列）**，若存在严格递增的下标序列

$$1 \leqslant i_1 < i_2 < \cdots < i_k \leqslant m$

使得对任意 $t \in [1, k]$，有 $x_{i_t} = z_t$。

记 $Z \sqsubseteq X$。

**定义 2（公共子序列）** $Z$ 是 $X$ 和 $Y$ 的 **common subsequence（公共子序列）**，若 $Z \sqsubseteq X$ 且 $Z \sqsubseteq Y$。

**定义 3（LCS 长度）** $X$ 与 $Y$ 的 **LCS 长度**，记作 $c(X, Y)$，定义为：

$$c(X, Y) = \max\{\,|Z| : Z \sqsubseteq X \text{ 且 } Z \sqsubseteq Y \,\}$

**定义 4（前缀子问题）** 对 $i \in [0, m], j \in [0, n]$，令

$$c[i, j] = c(X[1..i],\, Y[1..j])$

即 $c[i, j]$ 是前缀 $X[1..i]$ 与 $Y[1..j]$ 的 LCS 长度。目标：求 $c[m, n]$。

---

## 二、最优子结构定理（核心）

**定理 1（LCS 最优子结构）** 设 $X = \langle x_1, \ldots, x_m \rangle$, $Y = \langle y_1, \ldots, y_n \rangle$。令 $Z = \langle z_1, \ldots, z_k \rangle$ 是 $X$ 和 $Y$ 的任意一个 LCS。由子序列定义，存在严格递增的匹配下标：

$$1 \leqslant i_1 < i_2 < \cdots < i_k \leqslant m \qquad\text{（Z 在 X 中的匹配下标）}$
$$1 \leqslant j_1 < j_2 < \cdots < j_k \leqslant n \qquad\text{（Z 在 Y 中的匹配下标）}$

满足 $x_{i_t} = y_{j_t} = z_t$ 对所有 $t \in [1, k]$。

则：

### 情况 1：$x_m = y_n$

此时必然 $i_k = m$ 且 $j_k = n$（即 Z 的最后一个字符必须使用 X 和 Y 的末尾位置），且 $Z[1..k-1]$ 是 $X[1..m-1]$ 与 $Y[1..n-1]$ 的 LCS。

### 情况 2：$x_m \neq y_n$

此时 $i_k = m$ 与 $j_k = n$ **不可能同时成立**（否则 $x_m = x_{i_k} = z_k = y_{j_k} = y_n$，矛盾）。因此至少有一个成立：$i_k < m$ 或 $j_k < n$（或两者）。

- **子情况 A（$i_k < m$）：** $Z \sqsubseteq X[1..m-1]$ 且 $Z$ 是 $X[1..m-1]$ 与 $Y$ 的 LCS。
- **子情况 B（$j_k < n$）：** $Z \sqsubseteq Y[1..n-1]$ 且 $Z$ 是 $X$ 与 $Y[1..n-1]$ 的 LCS。

---

## 三、定理 1 的严格证明

### 情况 1 的证明：$x_m = y_n$

**Step 1 — Z 必须使用 $x_m$：**

假设 $i_k < m$（Z 在 X 中的最后一个匹配位置不是 m）。由于 $x_m = y_n$，且 $i_k < m$，我们可以将 $x_m$ 追加到 Z 的末尾，构造

$$Z' = Z \parallel x_m$$

- $Z' \sqsubseteq X$：下标序列 $i_1 < \cdots < i_k < m$ 严格递增。
- $Z' \sqsubseteq Y$：同理，由于 $x_m = y_n$，Y 中的下标序列也可扩展一位。
- $|Z'| = k + 1 > k = |Z|$。

这与 Z 是 LCS 矛盾。故 $i_k = m$。同理 $j_k = n$。因此 $z_k = x_m = y_n$。

**Step 2 — 前缀的最优性（剪切-粘贴）：**

令 $W = Z[1..k-1]$。显然 $W \sqsubseteq X[1..m-1]$ 且 $W \sqsubseteq Y[1..n-1]$（因为 $Z[1..k-1]$ 的所有匹配下标均严格小于 k，而 $i_k = m, j_k = n$）。

假设 $W$ 不是 $X[1..m-1]$ 与 $Y[1..n-1]$ 的 LCS。则存在 $W'$ 满足

$$W' \sqsubseteq X[1..m-1],\quad W' \sqsubseteq Y[1..n-1],\quad |W'| > k-1$$

构造 $Z'' = W' \parallel x_m$（粘贴操作）：

- $W' \sqsubseteq X[1..m-1]$ 且下标严格递增，追加 $x_m$ 后 $Z'' \sqsubseteq X$。
- 同理 $Z'' \sqsubseteq Y$（利用 $x_m = y_n$）。
- $|Z''| = |W'| + 1 > (k-1) + 1 = k = |Z|$。

与 Z 是 X 和 Y 的 LCS 矛盾。故 $W$ 是 $X[1..m-1]$ 与 $Y[1..n-1]$ 的 LCS。

$\square$

### 情况 2 的证明：$x_m \neq y_n$

**前提：** Z 是 X 和 Y 的 LCS，$x_m \neq y_n$。

**断言：** $i_k$ 和 $j_k$ 不可能同时等于 m 和 n。

*证明断言：* 若 $i_k = m$ 且 $j_k = n$，则 $x_m = x_{i_k} = z_k = y_{j_k} = y_n$，与 $x_m \neq y_n$ 矛盾。$\square$

因此 **至少有一个成立：$i_k < m$ 或 $j_k < n$**（两者可以同时成立）。

#### 子情况 A：$i_k < m$（Z 不使用 X 的末尾位置）

**Step 1 — Z 是子问题的可行解：**

由于 $i_1 < \cdots < i_k < m$，Z 的所有匹配下标都严格小于 m。因此 $Z \sqsubseteq X[1..m-1]$。同时 $Z \sqsubseteq Y$（已知）。

故 $Z$ 是 $X[1..m-1]$ 与 $Y$ 的公共子序列。

**Step 2 — Z 是子问题的最优解（剪切-粘贴反证）：**

假设 Z 不是 $X[1..m-1]$ 与 $Y$ 的 LCS。则存在 $W'$ 满足

$$W' \sqsubseteq X[1..m-1],\quad W' \sqsubseteq Y,\quad |W'| > k$

由于 $W' \sqsubseteq X[1..m-1]$ 且 $X[1..m-1]$ 是 $X$ 的前缀，所以 $W' \sqsubseteq X$。

因此 $W'$ 是 $X$ 与 $Y$ 的公共子序列，且 $|W'| > k = |Z|$，与 Z 是 X 和 Y 的 LCS 矛盾。

故 Z 是 $X[1..m-1]$ 与 $Y$ 的 LCS。

#### 子情况 B：$j_k < n$（Z 不使用 Y 的末尾位置）

与子情况 A 完全对称。Z 是 $X$ 与 $Y[1..n-1]$ 的 LCS。

**注：** 当 $i_k < m$ 且 $j_k < n$ 同时成立时，Z 同时是子情况 A 和子情况 B 中的子问题的 LCS。这不构成矛盾——实际上两个结论都成立。

$\square$

---

## 四、Bellman 递推公式

**定理 2（LCS 递推公式）** 对所有 $i \in [0, m]$, $j \in [0, n]$：

$$
c[i, j] = \begin{cases}
0 & \text{若 } i = 0 \text{ 或 } j = 0 \\[6pt]
c[i-1, j-1] + 1 & \text{若 } i, j > 0 \text{ 且 } x_i = y_j \\[6pt]
\max(c[i-1, j],\; c[i, j-1]) & \text{若 } i, j > 0 \text{ 且 } x_i \neq y_j
\end{cases}
$$

**证明：** 对 $d = i + j$ 进行强数学归纳。

**基始（$d = 0$）：** $i = j = 0$，$c[0, 0] = 0$（空序列的 LCS 长度显然为 0）。✓

**归纳假设：** 假设对所有满足 $i' + j' < d$ 的 $(i', j')$，定理成立。

**归纳步骤（$i + j = d > 0$）：** 设 $X' = X[1..i]$, $Y' = Y[1..j]$。

---

### 情况 A：$i, j > 0$ 且 $x_i = y_j$

令 $Z$ 是 $X'$ 与 $Y'$ 的任意一个 LCS，$|Z| = c[i, j]$。

由定理 1 情况 1（将 $X'$ 视为 X，$Y'$ 视为 Y，$x_i$ 为末尾字符）：

- $Z$ 以 $x_i = y_j$ 结尾
- $Z[1..k-1]$ 是 $X[1..i-1]$ 与 $Y[1..j-1]$ 的 LCS

因此：

$$c[i, j] = |Z| = |Z[1..k-1]| + 1 = c[i-1, j-1] + 1$$

由归纳假设（$i-1 + j-1 = d-2 < d$），$c[i-1, j-1]$ 已知为正确值。故公式成立。

---

### 情况 B：$i, j > 0$ 且 $x_i \neq y_j$

令 $Z$ 是 $X'$ 与 $Y'$ 的 LCS，$|Z| = k = c[i, j]$。

由定理 1 情况 2，$Z$ 在 $X'$ 中的最后一个匹配下标 $i_k$ 和在 $Y'$ 中的最后一个匹配下标 $j_k$ 不可能同时等于 $i$ 和 $j$。因此至少有一个成立：$i_k < i$ 或 $j_k < j$。

**下界方向（$c[i, j] \geqslant \max(\cdots)$）：**

$X[1..i-1] \sqsubseteq X[1..i]$，所以 $X[1..i-1]$ 与 $Y[1..j]$ 的任何公共子序列也是 $X[1..i]$ 与 $Y[1..j]$ 的公共子序列。因此：

$$c[i, j] \geqslant c[i-1, j]$$

同理 $c[i, j] \geqslant c[i, j-1]$。故：

$$c[i, j] \geqslant \max(c[i-1, j],\, c[i, j-1]) \tag{1}$$

**上界方向（$c[i, j] \leqslant \max(\cdots)$）：**

- 若 $i_k < i$（定理 1 子情况 A）：则 $Z$ 是 $X[1..i-1]$ 与 $Y[1..j]$ 的 LCS，故 $c[i, j] = |Z| = c[i-1, j]$。
- 若 $i_k = i$（即子情况 A 不成立），则由于 $i_k$ 和 $j_k$ 不能同时等于 i 和 j，必有 $j_k < j$。由定理 1 子情况 B，$Z$ 是 $X[1..i]$ 与 $Y[1..j-1]$ 的 LCS，故 $c[i, j] = |Z| = c[i, j-1]$。

每种情况下，$c[i, j]$ 等于 $\{c[i-1, j],\, c[i, j-1]\}$ 中的一个。因此：

$$c[i, j] \leqslant \max(c[i-1, j],\, c[i, j-1]) \tag{2}$

由 (1) 和 (2) 夹逼：

$$c[i, j] = \max(c[i-1, j],\, c[i, j-1])$

由归纳假设（$i-1+j = d-1 < d$，$i+j-1 = d-1 < d$），$c[i-1, j]$ 和 $c[i, j-1]$ 已知为正确值。故公式成立。

---

### 情况 C：$i = 0$ 或 $j = 0$

显然 $c[i, j] = 0$（空序列的 LCS 长度为 0）。✓

由数学归纳法，定理对所有 $(i, j)$ 成立。$\square$

---

## 五、你的核心疑问的形式化回答

### Q：当 $c[i-1, j] = c[i, j-1]$ 时，max 安全吗？

**答：** 安全。从证明的不等式 (1)(2)：

$$c[i-1, j] \leqslant c[i, j] \leqslant \max(c[i-1, j],\, c[i, j-1])$

当 $c[i-1, j] = c[i, j-1] = V$ 时，下界 $\geqslant V$，上界 $\leqslant V$，故 $c[i, j] = V$。max 不是"猜"出来的，是被**不等式夹逼**唯一确定的。

### Q：$i_k < m$（位置）vs $z_k \neq x_m$（值），哪个正确？

**答：** 用 **位置**（$i_k$）表述是精确的，用"值不等"（$z_k \neq x_m$）在重复字符下有歧义。但定理 1 的证明中，我们用的是位置 $i_k, j_k$，与字符值无关。CLRS 用了 $z_k \neq x_m$ 作为判定条件，这在**逻辑等效性**上没有问题，因为：

- $i_k < m \implies z_k \neq x_m$ 不成立（反例：X="aba", $i_k$=1, $z_k$='a'=$x_m$）
- 但 $z_k \neq x_m \implies i_k < m$ 成立（若 $i_k = m$ 则 $z_k = x_m$）

CLRS 的条件"$z_k \neq x_m$"是"$i_k < m$"的**充分条件**，而由于两个分支（$z_k \neq x_m$ 和 $z_k \neq y_n$）的互补性（$x_m \neq y_n$ 时至少一个成立），"充分"就足够了。

### Q："两者都不包含"需要第三种情况吗？

**答：** 不需要。当 $i_k < m$ 且 $j_k < n$ 时：

- 定理 1 子情况 A 导出 $c[i, j] = c[i-1, j]$
- 定理 1 子情况 B 导出 $c[i, j] = c[i, j-1]$

两者同时成立。无论用哪个，$c[i, j]$ 的值都等于那个共同的 $V = c[i-1, j] = c[i, j-1]$。这是双重覆盖，不是遗漏。

---

## 六、回溯重构算法

**定理 3（回溯重构正确性）** 设 $c[i, j]$ 是由定理 2 递推正确计算出的表。按以下规则从 $(m, n)$ 回溯构造序列 $Z$（反向构造，最后反转）：

1. 若 $i = 0$ 或 $j = 0$：停止。
2. 若 $x_i = y_j$：将此字符加入 $Z$，回溯到 $(i-1, j-1)$。
3. 若 $x_i \neq y_j$：
   - 若 $c[i-1, j] \geqslant c[i, j-1]$：回溯到 $(i-1, j)$。
   - 否则：回溯到 $(i, j-1)$。

则最终 $Z$ 是 $X$ 与 $Y$ 的一个 LCS。

**证明：**

**（a）合法性：** 每次加入 $Z$ 的字符满足 $x_i = y_j$（规则 2），且回溯步长中 $i$ 和 $j$ 均为非增且至少一个严格递减。因此选出的字符在 X 和 Y 中的下标严格递减（反向读则递增），满足子序列定义。

**（b）最优性（长度 = $c[m, n]$）：** 追踪 $c[i, j]$ 的变化：

- 规则 2：$c[i, j] = c[i-1, j-1] + 1$，$c$ 值减 1，$Z$ 长度增 1。
- 规则 3：$c[i, j] = \max(c[i-1, j], c[i, j-1])$。当 $c[i-1, j] \geqslant c[i, j-1]$ 时，$c[i-1, j] = c[i, j]$（$c$ 值不变）；否则同理。

从 $c[m, n]$ 到 $c[0, 0] = 0$，$c$ 值减少了 $c[m, n]$。由于每次规则 2 恰好减少 1 且加入一字符，最终 $|Z|$ = Z 中字符数 = 规则 2 的执行次数 = $c[m, n]$。$\square$

---

## 七、复杂度分析

- 子问题总数：$(m+1)(n+1) = \Theta(mn)$
- 每个子问题 $O(1)$ 计算（常数次比较和加法）
- **时间复杂度：** $\Theta(mn)$
- **空间复杂度：** $\Theta(mn)$，可优化至 $\Theta(\min(m, n))$（只存两行）

---

## 八、证明链条总图

```
子序列定义（下标严格递增）
       ↓
最优子结构定理（剪切-粘贴反证法，位置层面精确定义）
       ↓
Bellman 递推公式（数学归纳法 + 上下界夹逼）
       ↓
c 表 = 最优长度（独立于回溯）
       ↓
回溯重构算法（基于 c 表结构性质，独立证明合法性 + 最优性）
```

**无循环，每步仅依赖前一步。**
