# version code c2eb1c41017f+
# Please fill out this stencil and submit using the provided submission script.

from independence import *
from itertools import combinations, chain
import random
from GF2 import one
from vecutil import list2vec


# 1: (Task 7.7.1) Choosing a Secret Vector
def randGF2(): return random.randint(0, 1) * one


def rand_vec():
    return list2vec([randGF2() for i in a0.D])


a0 = list2vec([one, one, 0, one, 0, one])
b0 = list2vec([one, one, 0, 0, 0, one])


def choose_secret_vector(s, t):
    while True:
        u = rand_vec()
        if a0 * u == s and b0 * u == t:
            return u


# 2: (Task 7.7.2) Finding Secret Sharing Vectors
# Give each vector as a Vec instance
found = False
candidates = []
while not found:
    candidates = [[a0, b0]] + [[rand_vec(), rand_vec()] for i in range(4)]
    found = True
    for i, j, k in combinations(candidates, 3):
        if not is_independent(i + j + k):
            found = False
            break

secret_a0 = candidates[0][0]
secret_b0 = candidates[0][1]
secret_a1 = candidates[1][0]
secret_b1 = candidates[1][1]
secret_a2 = candidates[2][0]
secret_b2 = candidates[2][1]
secret_a3 = candidates[3][0]
secret_b3 = candidates[3][1]
secret_a4 = candidates[4][0]
secret_b4 = candidates[4][1]
