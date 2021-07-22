from functools import reduce

def xor_array(elem, length):
    if length == 1:
        return elem
    if elem % 2 == 0:
        if (length - 1) % 4 == 0:
            return elem + length - 1
        if (length - 1) % 4 == 1:
            return 1
        if (length - 1) % 4 == 2:
            return elem + length
        if (length - 1) % 4 == 3:
            return 0
    else:
        return elem ^ xor_array(elem + 1, length - 1)

def solution(start, length):
    checksum_vals = []
    for skip in range(0, length):
        checked_line_length = length - skip
        checksum_vals.append(xor_array(start + skip * length, checked_line_length))
    return reduce(lambda x, y: x ^ y, checksum_vals)