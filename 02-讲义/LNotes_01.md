# Lecture 1: Introduction（导论）

> Introduction to Algorithms: 6.006，Massachusetts Institute of Technology
> Instructors: Erik Demaine, Jason Ku, and Justin Solomon

---

## 课程目标

这门课的目标，是教你 solve（求解）computation problems（计算问题），并且把「你的 solution（解）是 correct（正确的）、且 efficient（高效的）」这件事 communicate（传达）清楚。

## Problem（问题）

- 一个 problem 是 problem inputs（问题输入）到 correct outputs（正确输出）的 binary relation（二元关系）。
- 通常不会为所有 input 逐个指定每一个 correct output（太多了！）。
- 而是给出一个 verifiable predicate（可验证谓词，也就是一条 property），correct outputs 必须 satisfy（满足）它。
- 6.006 研究的是 large general input spaces（大型一般输入空间）上的 problem。
- 不一般（not general）的情形：small input instance（小输入实例）。
  - 例子：在这间教室里，是否存在一对同一天生日的学生？
- 一般（general）的情形：arbitrarily large inputs（任意大的输入）。
  - 例子：给定任意 $n$ 个学生，是否存在一对同一天生日的学生？
  - 如果生日只是 365 天之一，那么当 $n > 365$ 时，答案恒为真，这是 pigeon-hole principle（鸽巢原理）。
  - 现在假设可能生日的 resolution（分辨率）超过 $n$（把年份、时刻等都算进去）。

## Algorithm（算法）

- 一个 algorithm 是把每个 input 映射到单一 output 的 procedure（过程），并且是 deterministic（确定性的）。
- 若一个 algorithm 对每一个 problem input 都返回 correct output，我们就说它 solves（解决）了这个 problem。
- 例子：求解 birthday matching（生日配对）的 algorithm
  - 维护一份 names 与 birthdays 的 record（记录），初始为空。
  - 按某种顺序 interview（逐个访问）每个学生。
    - 若该 birthday 已存在于 record 中，返回 found pair（找到的这一对）！
    - 否则把 name 与 birthday 加入 record。
  - 若访问完最后一个学生仍未成功，返回 None。

## Correctness（正确性）

- program 与 algorithm 的 size（代码规模）是固定的，那要怎么 prove correct（证明其正确）？
- 对 small inputs，可以用 case analysis（情形枚举）。
- 对 arbitrarily large inputs，algorithm 必须以某种方式 recursive（递归）或者 loop（循环）。
- 因而必须使用 induction（归纳法）——这正是 recursion 会成为计算机科学核心概念的原因。
- 例子：birthday matching algorithm 的 correctness 证明
  - 对 $k$ 做 induction：$k$ 是 record 中已有的学生数。
  - inductive hypothesis（归纳假设）：若前 $k$ 个学生中含有 match，则在 interview 第 $k+1$ 个学生之前就已经返回了这个 match。
  - base case（基础情形）：$k = 0$，此时前 $k$ 个学生不含任何 match。
  - 假设 induction hypothesis 对 $k = k_0$ 成立，考察 $k = k_0 + 1$。
  - 若前 $k_0$ 个学生中含 match，则由 induction 早已返回了 match。
  - 否则前 $k_0$ 个学生不含 match，于是若前 $k_0 + 1$ 个学生含 match，这个 match 必然含有第 $k_0 + 1$ 个学生。
  - 而 algorithm 恰好直接检查第 $k_0 + 1$ 个学生的 birthday 是否存在于前 $k_0$ 个学生之中。

## Efficiency（效率）

- 一个 algorithm 要多快才能产出 correct output？
  - 可以直接 measure time（测量时间），但我们希望 performance（性能）是 machine independent（与机器无关）的。
  - Idea！去数 algorithm 返回之前执行了多少个 fixed-time operations（固定时间操作）。
  - 这个数目预期会依赖 input 的 size（规模）：input 越大，时间越长。
  - input 的 size 常记作 $n$，但并不总是如此！
  - 若返回时间关于 input 是 polynomial time（多项式时间），就称它 efficient。
  - 有些 problem 根本不存在 efficient algorithm！（见 L20）
- Asymptotic Notation（渐近记号）：忽略 constant factors（常数因子）与 low order terms（低阶项）
  - upper bounds（上界）$O$、lower bounds（下界）$\Omega$、tight bounds（紧界）$\Theta$
  - 这三种记号都可以读作 $\in$、$=$、is、order
  - 下表中的 time 估计基于 1 GHz single-core machine（单核机器）、每个 cycle 执行一个 operation
  - 宇宙中的粒子总数估计少于 $10^{100}$

[Table 1：input size 与运行时间的数量级对照。原 PDF 为一行 `n = 1000` 加七个 complexity class 的数值行与 time 行，此处重排为三列表格，数值与原文一致]

| complexity class（复杂度类） | value at $n = 1000$（$n=1000$ 时的值） | estimated time（估计时间） |
|---|---|---|
| constant $\Theta(1)$ | $1$ | $1\,\text{ns}$ |
| logarithmic $\Theta(\log n)$ | $\approx 10$ | $10\,\text{ns}$ |
| linear $\Theta(n)$ | $1{,}000$ | $1\,\mu\text{s}$ |
| log-linear $\Theta(n\log n)$ | $\approx 10{,}000$ | $10\,\mu\text{s}$ |
| quadratic $\Theta(n^2)$ | $1{,}000{,}000$ | $1\,\text{ms}$ |
| polynomial $\Theta(n^c)$ | $1000^c$ | $10^{3c-9}\,\text{s}$ |
| exponential $2^{\Theta(n^c)}$ | $2^{1000} \approx 10^{301}$ | $10^{281}$ millenia |

## Model of Computation（计算模型）

- 它是对「机器上哪些 operations 可以在 $O(1)$ 时间内完成」的 specification（规格说明）。
- 本课使用的 model 叫 Word-RAM。
- machine word（机器字）：一块 $w$ bits 的存储单元，$w$ 是 $w$-bit Word-RAM 的 word size（字长）。
- memory（内存）：可寻址的 machine words 序列。
- processor（处理器）支持在 $O(1)$ 个 words（也就是 integers）上做大量 constant time operations：
  - integer arithmetic（整数运算）：`+`、`-`、`*`、`//`、`%`
  - logical operators（逻辑运算）：`&&`、`||`、`!`、`==`、`<`、`>`、`<=`、`=>`
  - bitwise arithmetic（位运算）：`&`、`|`、`<<`、`>>` 等
  - 给定 word $a$，可以读取地址 $a$ 处的 word，也可以把某个 word 写入地址 $a$。
- memory address（内存地址）必须能够访问 memory 中的每一个位置。
  - 要求：$w \ge$ 表示最大 memory address 所需的 bits 数，也就是 $\log_2 n$。
  - 32-bit words → 最大约 4 GB memory；64-bit words → 最大约 16 exabytes memory。
- Python 是一个更复杂的 model of computation，它本身实现在 Word-RAM 之上。

## Data Structure（数据结构）

- 一个 data structure 是存储 non-constant data（非常量数据）的方式，它支持一组 operations。
- 一组 operations 的 collection 称为 interface（接口）。
  - Sequence（序列）：items 带有 extrinsic order（外在顺序，即 first、last、nth）
  - Set（集合）：items 带有 intrinsic order（内在顺序，查询基于 item keys）
- 不同的 data structure 可以实现同一个 interface，但 performance 不同。
- 例子：Static Array（静态数组）——fixed width slots（固定宽度槽）、fixed length（固定长度）、static sequence interface
  - `StaticArray(n)`：分配大小为 $n$、初始化为 0 的 static array，时间 $\Theta(n)$
  - `StaticArray.get_at(i)`：返回 array index $i$ 处存储的 word，时间 $\Theta(1)$
  - `StaticArray.set_at(i, x)`：把 word $x$ 写入 array index $i$，时间 $\Theta(1)$
- 存储的 word 可以存放一个更大 object 的 address。
- 它相当于 Python 的 tuple 再加上 `set_at(i, x)`；而 Python 的 list 是 dynamic array（见 L02）。

## 代码：birthday_match

以下为原 PDF 第 4 页代码，保留原始结构与行号，注释行给出中文。

```python
 1  def birthday_match(students):
 2      '''
 3      Find a pair of students with the same birthday
 4      Input:  tuple of student (name, bday) tuples
 5      Output: tuple of student names or None
 6      '''
 7      n = len(students)                    # O(1)
 8      record = StaticArray(n)              # O(n)
 9      for k in range(n):                   # n
10          (name1, bday1) = students[k]     # O(1)
11          # Return pair if bday1 in record —— 若 bday1 已在 record 中则返回这一对
12          for i in range(k):               # k
13              (name2, bday2) = record.get_at(i)   # O(1)
14              if bday1 == bday2:           # O(1)
15                  return (name1, name2)    # O(1)
16          record.set_at(k, (name1, bday1)) # O(1)
17      return None                          # O(1)
```

## Example: Running Time Analysis（运行时间分析）

- 共有两个 loop（循环）：外层 $k \in \{0, \dots, n-1\}$，内层 $i \in \{0, \dots, k\}$。
- 于是 running time（运行时间）为

```math
O(n) + \sum_{k=0}^{n-1}\left(O(1) + k \cdot O(1)\right) = O(n^2)
```

- 关于 $n$ 是 quadratic（二次的），属于 polynomial（多项式）。这算 efficient 吗？为 record 换一种 data structure！
- 注意内层 loop 的代价是 $k \cdot O(1)$：第 $k$ 轮要线性扫描 record 中已有的 $k$ 条记录，这才是 $O(n^2)$ 的来源；换成 hash table 后这件事可以降到期望 $O(1)$。

## How to Solve an Algorithms Problem（如何求解一个算法问题）

1. Reduce（归约）到一个你已经会解的 problem（使用现成的 data structure 或 algorithm）。

[Figure 1：本页的三列算法地图。原 PDF 用纯文字列出三组 problem 与对应 lecture，没有图形元素；下面按原三列结构重排为表格，括号内的 L 编号即该内容出现在哪一讲]

| Search Problem（Data Structures） | Sort Algorithms | Shortest Path Algorithms |
|---|---|---|
| Static Array (L01) | Insertion Sort (L03) | Breadth First Search (L09) |
| Linked List (L02) | Selection Sort (L03) | DAG Relaxation (L11) |
| Dynamic Array (L02) | Merge Sort (L03) | Depth First Search (L10) |
| Sorted Array (L03) | Counting Sort (L05) | Topological Sort (L10) |
| Direct-Access Array (L04) | Radix Sort (L05) | Bellman-Ford (L12) |
| Hash Table (L04) | AVL Sort (L07) | Dijkstra (L13) |
| Balanced Binary Tree (L06-L07) | Heap Sort (L08) | Johnson (L14) |
| Binary Heap (L08) | | Floyd-Warshall (L18) |

2. 自己 design（设计）一个 recursive（递归的）algorithm：

- Brute Force（暴力枚举）
- Decrease and Conquer（减治）
- Divide and Conquer（分治）
- Dynamic Programming（动态规划，L15-L19）
- Greedy / Incremental（贪心 / 增量）

---

## 版权页（原第 5 页）

MIT OpenCourseWare，https://ocw.mit.edu
6.006 Introduction to Algorithms，Spring 2020
关于引用这些材料或使用条款的信息，见 https://ocw.mit.edu/terms
