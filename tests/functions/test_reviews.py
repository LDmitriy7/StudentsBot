from functions.reviews import count_avg_rating

r1 = {'rating': {'quality': 4, 'contact': 3, 'terms': 5}}
r2 = {'rating': {'quality': 5, 'contact': 3, 'terms': 4}}
r3 = {'rating': {'quality': 5, 'contact': 4, 'terms': 4}}
r4 = {'rating': {'quality': 2, 'contact': 3, 'terms': 5}}


def test_count_avg_rating():
    result = count_avg_rating([r1, r4, r3, r2])
    assert result == {'quality': 4.0, 'contact': 3.2, 'terms': 4.5}
