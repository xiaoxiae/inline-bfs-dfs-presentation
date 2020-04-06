"""Implementace algoritmu pro vrcholy se stupněm >= 2."""

from typing import *


A = [5, 7, 9, 12, 14, 17, 12, 2, 5, 1, 3, 4, 2, 4, 2, 3, 5, 1, 4]
T = A

n = A[0]
m = A[n + 1]


def pprint():
    """Hezký výpis stavu grafu. Ne, na tuhle část kódu fakt pyšný nejsem."""
    print(
        "|  n |"
        + "T".center(n * 5 - 1)
        + "|"
        + "  m |"
        + "pole sousednosti".center(m * 5 - 1)
        + "|\n"
        + ("|----|" + "-" * (n * 5 - 1) + "|" + "----|" + "-" * (m * 5 - 1) + "|\n")
        + ("| " + " | ".join([str(e).rjust(2) for e in range(len(A))]) + " |\n")
        + ("| " + " | ".join([str(e).rjust(2) for e in A]) + " |\n")
    )


def sorted_to_pointer():
    """Převede setříděnou na pointerovou reprezentaci."""
    for i in range(n + 2, m + n + 2):
        A[i] = T[A[i]]


def pointer_to_swapped():
    """Převede pointerovou na prohozenou."""
    for v in range(1, n + 1):
        if v != T[v]:  # special case pro stupeň 0
            A[T[v]], T[v] = v, A[T[v]]


def swapped_to_sorted():
    """Převede prohozenou na setříděnou."""
    # TODO do budoucna


# setříděná -> prohozená
sorted_to_pointer()
pointer_to_swapped()

v_s = int(input("v_s = "))


def preprocess(v):
    """Custom uživatelova preprocess funkce."""
    print(f"Navštěvuji {v}.")


def postprocess(v):
    """Custom uživatelova postprocess funkce."""
    print(f"Vracím se z {v}.")


def iterate_backwards(p):
    """Iterujeme zpět, dokud nenarazíme na start pole sousednosti vrcholu."""
    return p if A[p] <= n else iterate_backwards(p - 1)


def restore():
    """Opraví reprezentaci."""
    for v in range(1, n + 1):
        T[v] -= 1  # obrácení invariantu 3

    quit()


def visit(p):
    """Navštiv vrchol s polem sousednosti začínajícím na pozici p."""
    preprocess(A[p])  # vstoupili jsme do vrcholu
    nextNeighbor(p, False)  # iterujeme přes sousedy


def nextNeighbor(p, is_first):
    """Hlavní logika přecházení z vrcholu do vrcholu. is_first zamezuje přístupu k
    neexistujícímu indexu (p >= n + m + 2)."""
    # pokud je to první vrchol
    if not is_first and A[p] <= n:
        v = A[p]
        p += 1

        # prohoď prvního a druhého
        # první je uložený v poli sousednosti předka!
        if v == v_s:
            A[T[p - 1]], A[p] = A[p], A[T[p - 1]]
        else:
            A[A[T[p - 1]]], A[p] = A[p], A[A[T[p - 1]]]

        follow(p)  # zkus následovat pointer p

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

            follow(p)  # zkus následovat pointer p

    # pokud jsme prošli všechny sousedy (nebo jsme na konci pole A)
    if p >= n + m + 2 or A[p] <= n:
        # najdeme, kterým vrcholem aktuálně iterujeme
        q = iterate_backwards(p - 1)  # jeho pozice
        v = A[q]

        if v == v_s:  # pokud je to ten startovní, tak DFS skončilo
            T[v] += 1  # invariant 3 musí stále platit
            restore()  # obnovení grafu po skončení DFS
        else:
            backtrack(q)  # jinak se vraťme

    follow(p)  # zkus následovat pointer p


def isWhite(v):
    """Vrátí True, pokud je v bílý (otestuje invariant + začátek)."""
    return (v != v_s) and (1 <= A[T[v]] <= n)


def follow(p):
    """Následuj pointer uložený na pozici p a prozkoumej ho, pokud je bílý. Jinak jdi
    na souseda p + 1."""
    if isWhite(A[A[p]]):
        q = A[p]  # kam ukazuje
        v = A[q]  # jaké je jméno vrcholu, na který ukazuje

        # vytvoření obráceného pointeru
        A[p] = T[v]  # ať nepřijdeme o první vrchol
        T[v] = p  # pointer zpět do p

        visit(q)
    else:
        print(f"- {A[A[p]]} již navštívena")
        nextNeighbor(p + 1, True)


def backtrack(q):
    """Backtrackuj z pozice q vrcholu A[q]."""
    v = A[q]  # jméno vrcholu, ze kterého backtrackujeme
    p = T[v]  # obrácený pointer z v do předchůdce

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
