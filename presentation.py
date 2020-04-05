from typing import *
from dataclasses import *

import sys

sys.setrecursionlimit(100)


@dataclass
class ArrayView:
    array: List[int]

    def __getitem__(self, i):
        return self.array[i]

    def __setitem__(self, i, val):
        self.array[i] = val


# the input array
A = [5, 7, 9, 12, 14, 17, 12, 2, 5, 1, 3, 4, 2, 4, 2, 3, 5, 1, 4]

n = A[0]
m = A[n + 1]

T = ArrayView(A)

v_s = 3


def pprint():
    """Pretty print the graph representation."""
    print(
        "|  n |"
        + "T".center(n * 5 - 1)
        + "|"
        + "  m |"
        + "pole sousednosti".center(m * 5 - 1)
        + "|\n"
        + ("|----|" + "-" * (n * 5 - 1) + "|" + "----|" + "-" * (m * 5 - 1) + "|\n")
        + ("| " + " | ".join([str(e).rjust(2) for e in A]) + " |\n")
    )


# THE ALGORITHM CODE
def sorted_to_pointer():
    for i in range(n + 2, m + n + 2):
        A[i] = T[A[i]]


def pointer_to_swapped():
    for v in range(1, n + 1):
        if v != T[v]:  # stupeň 0
            A[T[v]], T[v] = v, A[T[v]]


def swapped_to_sorted():
    for v in range(1, n + 1):
        A[v] = A[T[v]]

    for i in range(n + 2, m + n + 2):
        if A[i] > n:
            A[i] = A[A[i]]

    v = 1
    replaced = False
    for i in range(n + 2, m + n + 2):
        if i != n + 2 and A[i] < prev_A_i and not replaced:
            for bad_v in range(A[i], v):
                tmp = T[bad_v]
                T[bad_v] = A[T[bad_v]]
                A[tmp] = bad_v
                v -= 1

        prev_A_i = A[i]

        # replace greedily
        if A[i] == v:
            A[i] = T[v]
            T[v] = i
            v += 1
            replaced = True
        else:
            replaced = False

        # TODO
        print(i)
        pprint()

        # fix possible mistakes


# transformations
# TODO pprint()
# TODO sorted_to_pointer()
# TODO pprint()
# TODO pointer_to_swapped()
# TODO pprint()
# TODO swapped_to_sorted()
# TODO pprint()


# TODO to be removed
# the input array
A = [5, 9, 7, 9, 9, 7, 12, 1, 17, 2, 12, 14, 3, 14, 4, 12, 17, 5, 14]

n = A[0]
m = A[n + 1]

T = ArrayView(A)


def preprocess(v):
    print(f"Visiting {v}.")


def postprocess(v):
    print(f"Returning from {v}.")


def iterate_backwards(p):
    return p if A[p] <= n else iterate_backwards(p - 1)


def restore():
    print("Obnovení grafu...")
    quit()


def visit(p):
    """Navštiv vrchol s polem sousednosti začínajícím na pozici p."""
    preprocess(A[p])  # vstoupili jsme do vrcholu
    nextNeighbor(p, False)  # iterujeme přes sousedy


def nextNeighbor(p, ignorecheck):
    """Vstoupí do vrcholu TODO."""
    # pokud je to první vrchol
    if not ignorecheck and A[p] <= n:
        v = A[p]
        p += 1

        # prohoď prvního a druhého
        # první je uložený v poli sousednosti předka!
        if v == v_s:
            A[T[p - 1]], A[p] = A[p], A[T[p - 1]]
        else:
            A[A[T[p - 1]]], A[p] = A[p], A[A[T[p - 1]]]

        # buďto prozkoumáme bílého souseda, nebo jdeme na dalšího TODO substep 3
        if isWhite(A[A[p]]):
            follow(p)
        else:
            print(f"- {A[A[p]]} already visited.")
            nextNeighbor(p + 1, True)

    # pokud je to druhý vrchol
    elif A[p - 2] <= n:
        v = A[p - 2]

        # pokud jsou prohozené
        if (v == v_s and A[T[p - 2]] > A[p - 1]) or A[A[T[p - 2]]] > A[p - 1]:
            p -= 1
            if v == v_s:
                A[T[p - 1]], A[p] = A[p], A[T[p - 1]]
            else:
                A[A[T[p - 1]]], A[p] = A[p], A[A[T[p - 1]]]

            # buďto prozkoumáme bílého souseda, nebo jdeme na dalšího TODO substep 3
            if isWhite(A[A[p]]):
                follow(p)
            else:
                print(f"- {A[A[p]]} already visited.")
                nextNeighbor(p + 1, True)

    # pokud jsme prošli všechny sousedy (nebo jsme na konci pole A)
    if p >= n + m + 2 or A[p] <= n:
        # najdeme, kterým vrcholem aktuálně iterujeme
        q = iterate_backwards(p - 1)
        v = A[q]

        # pokud je to ten startovní, tak DFS skončilo
        if v == v_s:
            T[v] += 1  # invariant 3 musí stále platit
            restore()  # obnovení grafu po skončení DFS

        # jinak se vraťme
        else:
            backtrack(q)

    # buďto prozkoumáme bílého souseda, nebo jdeme na dalšího
    if isWhite(A[A[p]]):
        follow(p)
    else:
        print(f"- {A[A[p]]} already visited.")
        nextNeighbor(p + 1, True)


def isWhite(v):
    """Vrátí true, pokud je v bílý (otestuje invariant + začátek)."""
    return (v != v_s) and (1 <= A[T[v]] <= n)


def follow(p):
    """Následuj pointer uložený na pozici p."""
    q = A[p]  # kam ukazuje
    v = A[q]  # jaké je jméno vrcholu, na který ukazuje

    # vytvoření obráceného pointeru
    A[p] = T[v]  # ať nepřijdeme o první vrchol
    T[v] = p  # pointer zpět do p

    visit(q)


def backtrack(q):
    """Backtrackuj z pozice q."""
    v = A[q]  # jméno vrcholu, ze kterého backtrackujeme
    p = T[v]  # orácený pointer z v do předchůdce

    # revertnutí obráceného pointeru
    T[v] = A[p] + 1  # invariant 3
    A[p] = q

    # zpracovali jsme všechny sousedy, tak se vracíme
    postprocess(v)
    nextNeighbor(p + 1, True)


# start DFS from vertex 3
for p in range(n + 2, m + n + 2):
    if A[p] == v_s:
        visit(p)
