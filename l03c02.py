import copy

def get_two_steps(total, start):
    # print(f'Getting combinations of total {total} starting at {start}')
    first = start
    second = total - start
    combinations = []
    while second > first:
        combinations.append([second, first])
        first += 1
        second -= 1
    
    # print(combinations)
    if len(combinations) == 0:
      # print("No combinations found")
      return combinations

    extended_combinations = copy.deepcopy(combinations)
    for combination in combinations:
        # print(f"Expanding on combination {combination}")
        next_step_combinations = get_two_steps(combination[0], combination[1] + 1)
        if len(next_step_combinations) != 0:
          for i in range(len(next_step_combinations)):
              next_step_combinations[i].extend(combination[1:])
          # print(f"Expansion of combination {combination}: {next_step_combinations}")
          extended_combinations.extend(next_step_combinations)
        # else:
          # print(f"No expansion of combination {combination} exists")
    return extended_combinations

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

@Memoize
def get_two_steps_numerical(total, start):
    # print(f'Getting combinations of total {total} starting at {start}')
    # if total < 2*start + 1:
      # print("No combinations found")
      # return 0
    combinations_num = 0

    if total % 2 == 0:
      combinations_num = (total / 2) - start
    else:
      combinations_num = (total + 1) / 2 - start

    expanded_combinations_sum = combinations_num

    # print(expanded_combinations_sum)

    for i in range(int(combinations_num)):
      if total - (i + start) < 2*(start + i + 1) + 1:
        # print(f"Skipping total: {total - (i + start)}, start: {start + i + 1}, too small")
        continue
      expanded_combinations_sum += get_two_steps_numerical(total - (i + start), start + i + 1)

    return int(expanded_combinations_sum)

def solution(n):
    return get_two_steps_numerical(n, 1)

print(solution(200))
# print(len(get_two_steps(50, 1)))
