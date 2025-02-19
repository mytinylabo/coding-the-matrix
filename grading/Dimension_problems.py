# version code 80e56511a793+
# Please fill out this stencil and submit using the provided submission script.

from vecutil import list2vec
from GF2 import one
from solver import solve
from matutil import listlist2mat, coldict2mat, mat2coldict, mat2rowdict, rowdict2mat
from mat import Mat
from vec import Vec
from The_Basis_problems import vec2rep, subset_basis
from independence import rank, is_independent
from triangular import triangular_solve

# 1: (Problem 6.7.2) Iterative Exchange Lemma
w0 = list2vec([1, 0, 0])
w1 = list2vec([0, 1, 0])
w2 = list2vec([0, 0, 1])

v0 = list2vec([1, 2, 3])
v1 = list2vec([1, 3, 3])
v2 = list2vec([0, 3, 3])

# Fill in exchange_S1 and exchange_S2
# with appropriate lists of 3 vectors

exchange_S0 = [w0, w1, w2]
exchange_S1 = [v0, w1, w2]
exchange_S2 = [v0, v1, w2]
exchange_S3 = [v0, v1, v2]


# 2: (Problem 6.7.3) Another Iterative Exchange Lemma
w0 = list2vec([0, one, 0])
w1 = list2vec([0, 0, one])
w2 = list2vec([one, one, one])

v0 = list2vec([one, 0, one])
v1 = list2vec([one, 0, 0])
v2 = list2vec([one, one, 0])

exchange_2_S0 = [w0, w1, w2]
exchange_2_S1 = [v0, w1, w2]
exchange_2_S2 = [v0, v1, w2]
exchange_2_S3 = [v0, v1, v2]


def exchange(S, A, z):
    u = vec2rep(S, z)
    for i, v in enumerate(S):
        coef = u[i]
        if v not in A and coef != 0:
            return v


# 3: (Problem 6.7.4) Morph Lemma Coding
def morph(S, B):
    '''
    Input:
        - S: a list of distinct Vecs
        - B: a list of linearly independent Vecs all in Span S
    Output: a list of pairs of vectors to inject and eject (see problem description)
    Example:
        >>> # This is how our morph works.  Yours may yield different results.
        >>> # Note: Make a copy of S to modify instead of modifying S itself.
        >>> from vecutil import list2vec
        >>> from vec import Vec
        >>> S = [list2vec(v) for v in [[1,0,0],[0,1,0],[0,0,1]]]
        >>> B = [list2vec(v) for v in [[1,1,0],[0,1,1],[1,0,1]]]
        >>> D = {0, 1, 2}
        >>> morph(S, B) == [(Vec(D,{0: 1, 1: 1, 2: 0}), Vec(D,{0: 1, 1: 0, 2: 0})), (Vec(D,{0: 0, 1: 1, 2: 1}), Vec(D,{0: 0, 1: 1, 2: 0})), (Vec(D,{0: 1, 1: 0, 2: 1}), Vec(D,{0: 0, 1: 0, 2: 1}))]
        True
        >>> S == [list2vec(v) for v in [[1,0,0],[0,1,0],[0,0,1]]]
        True
        >>> B == [list2vec(v) for v in [[1,1,0],[0,1,1],[1,0,1]]]
        True
        >>> from GF2 import one
        >>> D = {0, 1, 2, 3, 4, 5, 6, 7}
        >>> S = [Vec(D,{1: one, 2: one, 3: one, 4: one}), Vec(D,{1: one, 3: one}), Vec(D,{0: one, 1: one, 3: one, 5: one, 6: one}), Vec(D,{3: one, 4: one}), Vec(D,{3: one, 5: one, 6: one})]
        >>> B = [Vec(D,{2: one, 4: one}), Vec(D,{0: one, 1: one, 2: one, 3: one, 4: one, 5: one, 6: one}), Vec(D,{0: one, 1: one, 2: one, 5: one, 6: one})]
        >>> sol = morph(S, B)
        >>> sol == [(B[0],S[0]), (B[1],S[2]), (B[2],S[3])] or sol == [(B[0],S[1]), (B[1],S[2]), (B[2],S[3])]
        True
        >>> # Should work the same regardless of order of S
        >>> from random import random
        >>> sol = morph(sorted(S, key=lambda x:random()), B)
        >>> sol == [(B[0],S[0]), (B[1],S[2]), (B[2],S[3])] or sol == [(B[0],S[1]), (B[1],S[2]), (B[2],S[3])]
        True
    '''
    A = []
    T = S.copy()
    result = []
    for b in B:
        fired = exchange(T, A, b)
        T.remove(fired)
        T.append(b)
        result.append((b, fired))
    return result


def list2veclist(*args):
    return [list2vec(l) for l in args]


# 4: (Problem 6.7.5) Row and Column Rank Practice
# Please express each solution as a list of Vecs
row_space_1 = list2veclist([1, 2, 0], [0, 2, 1])
col_space_1 = list2veclist([1, 0], [0, 1])

row_space_2 = list2veclist([1, 4, 0, 0], [0, 2, 2, 0], [0, 0, 1, 1])
col_space_2 = list2veclist([1, 0, 0], [4, 2, 0], [0, 2, 1])

row_space_3 = list2veclist([1])
col_space_3 = list2veclist([1, 2, 3])

row_space_4 = list2veclist([1, 0], [2, 1])
col_space_4 = list2veclist([1, 2, 3], [0, 1, 4])


# 5: (Problem 6.7.6) My Is Independent Procedure
def my_is_independent(L):
    '''
    Input:
        - L: a list of Vecs
    Output:
        - boolean: true if the list is linearly independent
    Examples:
        >>> D = {0, 1, 2}
        >>> L = [Vec(D,{0: 1}), Vec(D,{1: 1}), Vec(D,{2: 1}), Vec(D,{0: 1, 1: 1, 2: 1}), Vec(D,{0: 1, 1: 1}), Vec(D,{1: 1, 2: 1})]
        >>> my_is_independent(L)
        False
        >>> my_is_independent(L[:2])
        True
        >>> my_is_independent(L[:3])
        True
        >>> my_is_independent(L[1:4])
        True
        >>> my_is_independent(L[0:4])
        False
        >>> my_is_independent(L[2:])
        False
        >>> my_is_independent(L[2:5])
        False
        >>> L == [Vec(D,{0: 1}), Vec(D,{1: 1}), Vec(D,{2: 1}), Vec(D,{0: 1, 1: 1, 2: 1}), Vec(D,{0: 1, 1: 1}), Vec(D,{1: 1, 2: 1})]
        True
    '''
    return len(L) == rank(L)


# 6: (Problem 6.7.7) My Rank
def my_rank(L):
    '''
    Input:
        - L: a list of Vecs
    Output:
        - the rank of the list of Vecs
    Example:
        >>> L = [list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]]
        >>> my_rank(L)
        2
        >>> L == [list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]]
        True
        >>> my_rank([list2vec(v) for v in [[1,1,1],[2,2,2],[3,3,3],[4,4,4],[123,432,123]]])
        2
    '''
    return len(subset_basis(L))


# 7: (Problem 6.7.9) Direct Sum Validity
# Please give each answer as a boolean
only_share_the_zero_vector_1 = True
only_share_the_zero_vector_2 = True
only_share_the_zero_vector_3 = True


# 8: (Problem 6.7.11) Direct Sum Unique Representation
def direct_sum_decompose(U_basis, V_basis, w):
    '''
    Input:
        - U_basis: a list of Vecs forming a basis for a vector space U
        - V_basis: a list of Vecs forming a basis for a vector space V
        - w: a Vec in the direct sum of U and V
    Output:
        - a pair (u, v) such that u + v = w, u is in U, v is in V
    Example:

        >>> D = {0,1,2,3,4,5}
        >>> U_basis = [Vec(D,{0: 2, 1: 1, 2: 0, 3: 0, 4: 6, 5: 0}), Vec(D,{0: 11, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}), Vec(D,{0: 3, 1: 1.5, 2: 0, 3: 0, 4: 7.5, 5: 0})]
        >>> V_basis = [Vec(D,{0: 0, 1: 0, 2: 7, 3: 0, 4: 0, 5: 1}), Vec(D,{0: 0, 1: 0, 2: 15, 3: 0, 4: 0, 5: 2})]
        >>> w = Vec(D,{0: 2, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0})
        >>> (u, v) = direct_sum_decompose(U_basis, V_basis, w)
        >>> (u + v - w).is_almost_zero()
        True
        >>> U_matrix = coldict2mat(U_basis)
        >>> V_matrix = coldict2mat(V_basis)
        >>> (u - U_matrix*solve(U_matrix, u)).is_almost_zero()
        True
        >>> (v - V_matrix*solve(V_matrix, v)).is_almost_zero()
        True
        >>> ww = Vec(D,{0: 2, 1: 5, 2: 51, 4: 1, 5: 7})
        >>> (u, v) = direct_sum_decompose(U_basis, V_basis, ww)
        >>> (u + v - ww).is_almost_zero()
        True
        >>> (u - U_matrix*solve(U_matrix, u)).is_almost_zero()
        True
        >>> (v - V_matrix*solve(V_matrix, v)).is_almost_zero()
        True
        >>> U_basis == [Vec(D,{0: 2, 1: 1, 2: 0, 3: 0, 4: 6, 5: 0}), Vec(D,{0: 11, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}), Vec(D,{0: 3, 1: 1.5, 2: 0, 3: 0, 4: 7.5, 5: 0})]
        True
        >>> V_basis == [Vec(D,{0: 0, 1: 0, 2: 7, 3: 0, 4: 0, 5: 1}), Vec(D,{0: 0, 1: 0, 2: 15, 3: 0, 4: 0, 5: 2})]
        True
        >>> w == Vec(D,{0: 2, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0})
        True
    '''
    rep_w = vec2rep(U_basis + V_basis, w)
    rep_u = [rep_w[i] for i in range(len(U_basis))]
    rep_v = [rep_w[len(U_basis) + i] for i in range(len(V_basis))]
    u = coldict2mat(U_basis) * list2vec(rep_u)
    v = coldict2mat(V_basis) * list2vec(rep_v)
    return (u, v)


# 9: (Problem 6.7.12) Is Invertible Function
def is_invertible(M):
    '''
    input: A matrix, M
    outpit: A boolean indicating if M is invertible.

    >>> M = Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): 0, (1, 2): 1, (3, 2): 0, (0, 0): 1, (3, 3): 4, (3, 0): 0, (3, 1): 0, (1, 1): 2, (2, 1): 0, (0, 2): 1, (2, 0): 0, (1, 3): 0, (2, 3): 1, (2, 2): 3, (1, 0): 0, (0, 3): 0})
    >>> is_invertible(M)
    True

    >>> M1 = Mat(({0,1,2},{0,1,2}),{(0,0):1,(0,2):2,(1,2):3,(2,2):4})
    >>> is_invertible(M1)
    False
    '''
    if len(M.D[0]) != len(M.D[1]):
        return False
    return is_independent(list(mat2coldict(M).values()))


# 10: (Problem 6.7.13) Inverse of a Matrix over GF(2)
def find_matrix_inverse(A):
    '''
    Input:
        - A: an invertible Mat over GF(2)
    Output:
        - A Mat that is the inverse of A
    Examples:
        >>> M1 = Mat(({0,1,2}, {0,1,2}), {(0, 1): one, (1, 0): one, (2, 2): one})
        >>> find_matrix_inverse(M1) == Mat(M1.D, {(0, 1): one, (1, 0): one, (2, 2): one})
        True
    '''
    x = []
    n = len(A.D[0])
    for i in range(n):
        bi = list2vec([one if i == j else 0 for j in range(n)])
        x.append(solve(A, bi))
    return coldict2mat(x)


# 11: (Problem 6.7.14) Inverse of a Triangular Matrix
def find_triangular_matrix_inverse(A):
    '''
    Supporting GF2 is not required.

    Input:
        - A: an upper triangular Mat with nonzero diagonal elements
    Output:
        - Mat that is the inverse of A

    Example:
        >>> A = listlist2mat([[1, .5, .2, 4],[0, 1, .3, .9],[0,0,1,.1],[0,0,0,1]])
        >>> find_triangular_matrix_inverse(A) == Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): -0.5, (1, 2): -0.3, (3, 2): 0.0, (0, 0): 1.0, (3, 3): 1.0, (3, 0): 0.0, (3, 1): 0.0, (2, 1): 0.0, (0, 2): -0.05000000000000002, (2, 0): 0.0, (1, 3): -0.87, (2, 3): -0.1, (2, 2): 1.0, (1, 0): 0.0, (0, 3): -3.545, (1, 1): 1.0})
        True
    '''
    x = []
    n = len(A.D[0])
    rowlist = list(mat2rowdict(A).values())
    for i in range(n):
        bi = list2vec([1 if i == j else 0 for j in range(n)])
        x.append(triangular_solve(rowlist, range(n), bi))
    return coldict2mat(x)
