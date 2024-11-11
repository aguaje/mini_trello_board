MIN_RANKING = 'aaaaa'
MAX_RANKING = 'zzzzz'

"""
For our ranking we are using lowercase letters only in the ranking string.  To convert between the ranking string
(base 26) and a numerical (base10) value, we are going by 'a' = 1, 'b' = 2, ..., 'z' = 26, 'aa' = 27, etc
"""


def convert_base26_to_base10(base26_str: str) -> int:
    result = 0
    for c in base26_str:
        result = result * 26 + (ord(c) - ord('a') + 1)
    return result


def convert_base10_to_base26(base10_num: int) -> str:
    if base10_num <= 0:
        return ''

    result = ''
    while base10_num > 0:
        base10_num -= 1  # Adjust because 'a' = 1
        remainder = base10_num % 26
        result = chr(ord('a') + remainder) + result
        base10_num //= 26
    return result


def get_ranking_between(rank1: str, rank2: str) -> str:
    """
    :param rank1: string rank in base26 (not including bucket number)
    :param rank2: string rank in base26 (not including bucket number)
    :return: string rank in base26 that's in the middle between rank1 and rank2
    """
    rank1_val = convert_base26_to_base10(rank1)
    rank2_val = convert_base26_to_base10(rank2)

    if abs(rank2_val - rank1_val) == 1:
        raise RuntimeError(f'There is no ranking in between {rank1} and {rank2}')

    avg = (rank1_val + rank2_val) // 2
    return convert_base10_to_base26(avg)


def get_next_ranking(highest_rank: str) -> str:
    """
    TODO: improve the algorithm to make rankings more evenly spread apart
    :param highest_rank: string highest existing ranking (not including bucket number)
    :return: string ranking (not including bucket number) in the middle of the highest existing ranking and the
    maximum possible ranking
    """
    return get_ranking_between(highest_rank, MAX_RANKING)
