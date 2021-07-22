def solution(total_lambs):
    max_sum = total_lambs
    max_hench = 0

    while max_sum >= 2 ** max_hench:
        max_sum -= 2 ** max_hench
        max_hench += 1

    min_sum = total_lambs
    min_hench = 0
    prev_prev_given = 0
    prev_given = 0

    while min_sum >= prev_prev_given + prev_given:
        hench_pay = None
        if min_hench == 0:
            hench_pay = 1
        else:
            hench_pay = prev_prev_given + prev_given
        min_sum -= hench_pay
        prev_prev_given = prev_given
        prev_given = hench_pay
        min_hench += 1

    return min_hench - max_hench