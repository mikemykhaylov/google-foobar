from decimal import Decimal, localcontext


def beatty_term(i, r):
    return i * r


def solution(n):
    # This was an additional challenge that I chose to take for fun
    # I got lucky with this challenge, as I wrote my IB math research about the Beatty Sequence :)

    with localcontext() as ctx:
        decimal_n = Decimal(n)

        ctx.prec = 103

        primary_num = Decimal(2).sqrt()

        # From the definition
        complementary_num = Decimal(2) + primary_num

        # Making a recursive call
        def recursive_solution(number):
            # Base case
            if number == 0:
                return 0

            primary_beatty_term = int(beatty_term(number, primary_num))

            # For convenience and conciseness
            primary_beatty_term_divided = int(
                Decimal(primary_beatty_term) / complementary_num
            )

            # Formula derived using complementary sequence property
            return (
                (primary_beatty_term * (primary_beatty_term + 1)) / 2
                - recursive_solution(primary_beatty_term_divided)
                - primary_beatty_term_divided * (primary_beatty_term_divided + 1)
            )

        return str(int(recursive_solution(decimal_n)))
