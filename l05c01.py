from math import factorial
from itertools import product
from fractions import gcd

q = {1: [[1]]}


def decompose(n):
    try:
        return q[n]
    except:
        pass

    result = [[n]]

    for i in range(1, n):
        a = n - i
        R = decompose(i)
        for r in R:
            if r[0] <= a:
                result.append([a] + r)

    q[n] = result
    return result


def find_class_members(conj_class):
    # Here we find the number of permutations that are members of a class
    # The steps are as follows: (Example with 1234 and 2 cycles of 2)
    # 1. Take factorial of the element set order (4! = 24)
    # 2. For each cycle of length n, divide by n
    # The reason is that it doesnt matter from which element cycle starts ((12) <-> (21))
    # 3. For k cycles of length n, divide by k!
    # The reason is that it doesnt matter in which order cycles are ((12)(34) <-> (34)(12))

    # Counting the total number of permuted elements
    total_elements = 0

    # Counting the number we divide by in step 2
    inside_cycle_order_divider = 1

    # Counting the number of cycles of length n
    # cycles_number[i] = j -> There are j cycles of length i
    cycles_number = {}

    for cycle in conj_class:
        total_elements += cycle
        inside_cycle_order_divider *= cycle
        cycles_number[cycle] = cycles_number[cycle] + 1 if cycle in cycles_number else 1

    cycles_order_divider = 1

    for i in cycles_number.values():
        cycles_order_divider *= factorial(i)

    return factorial(total_elements) / (
        inside_cycle_order_divider * cycles_order_divider
    )


def solution(w, h, s):
    # Any two permutations with same number of same-length cycles
    # behave similarly, and thus can be considered as one entity
    # Conjugacy classes are enumerated by decomposing the total number of rows/columns
    # Visually they can be represented as various Young diagrams
    col_swaps_conjugacy_classes = decompose(w)
    row_swaps_conjugacy_classes = decompose(h)

    total = 0

    for row_conj_class in row_swaps_conjugacy_classes:
        row_class_members = find_class_members(row_conj_class)
        for col_conj_class in col_swaps_conjugacy_classes:
            col_class_members = find_class_members(col_conj_class)
            # Combining any row class with n cycles and col classes with m cycles
            # partitions the grid into m*n rectangles. In each of those rectangles h*w,
            # the number of cycles would be GCD(h, w). The total number of cycles for a given
            # combination of row and col cycles would be sum of cycles of all rectangles.
            # Therefore, the number of fixed states of the grid (needed for the Burnside's Lemma)
            # is the number of states s^(total cycles)

            rectangles = list(product(row_conj_class, col_conj_class))

            total_cycles = sum(gcd(*rect) for rect in rectangles)

            total += row_class_members * col_class_members * s ** total_cycles

    total = int(total / (factorial(w) * factorial(h)))
    return total

