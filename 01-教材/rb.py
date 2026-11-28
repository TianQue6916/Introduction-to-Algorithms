# -*- coding: utf-8 -*-
"""Minimal CLRS red-black tree (insert + delete) with instrumentation.
Counts RB-DELETE-FIXUP while-loop iterations and rotations per deletion.
Used to measure the real fix-up cost for the teaching figure of chunk09 §13.4.
"""
import random

RED, BLACK = 1, 0


class Node:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.nil = Node(None, BLACK)
        self.nil.left = self.nil.right = self.nil.parent = self.nil
        self.root = self.nil
        self.rotations = 0
        self.fixup_iters = 0

    # ---------- rotations ----------
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.rotations += 1

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        self.rotations += 1

    # ---------- insert ----------
    def insert(self, key):
        z = Node(key)
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            x = x.left if z.key < x.key else x.right
        z.parent = y
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = z.right = self.nil
        z.color = RED
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        while z.parent.color == RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    # ---------- delete ----------
    def _transplant(self, u, v):
        if u.parent is self.nil:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x):
        while x.left is not self.nil:
            x = x.left
        return x

    def delete(self, z):
        self.rotations = 0
        self.fixup_iters = 0
        y = z
        y_original_color = y.color
        if z.left is self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self._delete_fixup(x)
        return self.fixup_iters, self.rotations

    def _delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            self.fixup_iters += 1
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def nodes(self):
        out, stack, x = [], [], self.root
        while stack or x is not self.nil:
            while x is not self.nil:
                stack.append(x)
                x = x.left
            x = stack.pop()
            out.append(x)
            x = x.right
        return out

    def black_height_ok(self):
        def bh(n):
            if n is self.nil:
                return 1
            l, r = bh(n.left), bh(n.right)
            if l != r or l < 1:
                return -10 ** 6
            return l + (1 if n.color == BLACK else 0)
        return bh(self.root) > 0


def measure(n, trials, rng):
    max_it = max_rot = 0
    for _ in range(trials):
        keys = list(range(n))
        rng.shuffle(keys)
        t = RBTree()
        for k in keys:
            t.insert(k)
        order = t.nodes()
        rng.shuffle(order)
        for z in order:
            it, rot = t.delete(z)
            max_it = max(max_it, it)
            max_rot = max(max_rot, rot)
            assert t.black_height_ok(), "RB invariant broken"
    return max_it, max_rot


if __name__ == "__main__":
    import json
    import math
    rng = random.Random(20261129)
    sizes = [15, 31, 63, 127, 255, 511, 1023, 2047]
    out = []
    for n in sizes:
        it, rot = measure(n, 300 if n <= 255 else 120, rng)
        out.append({"n": n, "max_iters": it, "max_rot": rot,
                    "ceil_lg": math.ceil(math.log2(n + 1))})
        print(n, "max_iters =", it, " max_rot =", rot,
              " ceil(lg(n+1)) =", math.ceil(math.log2(n + 1)))
    json.dump(out, open("rb_measure.json", "w"), indent=1)
