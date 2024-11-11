import pytest  # for testing exceptions

from src.rank import convert_base26_to_base10, convert_base10_to_base26, get_ranking_between, get_next_ranking, \
    MAX_RANKING


class TestRankingSystem:
    @pytest.mark.parametrize("base26,base10", [
        # Basic conversions
        ('a', 1),
        ('b', 2),
        ('z', 26),
        ('aa', 27),
        ('ab', 28),
        ('ba', 53),
        ('zz', 702),
        ('', 0),
    ])
    def test_conversions(self, base26, base10):
        assert convert_base26_to_base10(base26) == base10
        assert convert_base10_to_base26(base10) == base26

    @pytest.mark.parametrize("rank1,rank2,expected", [
        ('a', 'c', 'b'),
        ('a', 'd', 'b'),
        ('x', 'z', 'y'),
        ('aa', 'ac', 'ab'),
    ])
    def test_get_ranking_between(self, rank1, rank2, expected):
        actual = get_ranking_between(rank1, rank2)
        assert actual == expected
        assert rank1 < actual
        assert actual < rank2

    @pytest.mark.parametrize("rank1,rank2", [
        ('a', 'b'),
        ('ay', 'az'),
        ('y', 'z'),
    ])
    def test_get_ranking_between_error(self, rank1, rank2):
        with pytest.raises(RuntimeError):
            get_ranking_between(rank1, rank2)

    @pytest.mark.parametrize("rank", [
        'aaaaa',
        'mmmmm',
        'xxxxx',
        'yyyyy',
    ])
    def test_get_next_ranking(self, rank):
        next_rank = get_next_ranking(rank)
        assert convert_base26_to_base10(next_rank) > convert_base26_to_base10(rank)
        assert convert_base26_to_base10(next_rank) < convert_base26_to_base10(MAX_RANKING)

    @pytest.mark.parametrize("rank1,rank2", [
        ('aaaaa', 'aaaab'),
        ('aaaab', 'aaaba'),
        ('aaaba', 'aabaa'),
        ('aabaa', 'abaaa'),
        ('abaaa', 'baaaa'),
    ])
    def test_ranking_order(self, rank1, rank2):
        assert convert_base26_to_base10(rank2) > convert_base26_to_base10(rank1)
