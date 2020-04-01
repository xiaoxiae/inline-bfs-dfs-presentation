def visit(p):
    """Navštiv vrchol s polem sousednosti začínajícím na pozici p."""
    preprocess(A[p])  # vstoupili jsme do vrcholu
    nextNeighbor(p, true)  # iterujeme přes sousedy


def nextNeighbor(p, ignoreCheck):
    """Vstoupí do vrcholu, pokud je bílý."""
    # TODO
    # pokud je to první vrchol (a chceme to kontrolovat)
    if not ignorecheck and (1 <= A[p] <= n):
        # SUBSTEP 1
    else:
    # SUBSTEP 2
    # pokud jsme prošli všechny sousedy (nebo jsme na konci pole A)
    if 1 <= A[p] <= n or p > n + m + 2:
        # najdeme, kterým vrcholem aktuálně iterujeme
        v = A[iterate_backwards(p)]

        # pokud je to ten startovní, tak DFS skončilo
        if v == v_s:
            T[v] += 1  # invariant 3
            restore()  # obnovení grafu po skončení DFS
        else:
            backtrack(q)

    # buďto se zrekurzeme na bílého souseda, nebo jděme dál
    if isWhite(A[p]):
        follow(p)
    else:
        nextNeighbor(p + 1, False)


def isWhite(v):
    """Vrátí true, pokud je v bílý."""
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
    postprocess()
    nextNeighbor(p + 1, false)
