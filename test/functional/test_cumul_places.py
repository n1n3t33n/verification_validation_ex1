"""Tests fonctionnels — cumul des places par club et par competition (bug 12).

La limite de 12 places s'applique au total reserve par un club pour une meme
competition, pas seulement par reservation.
"""


def test_cumul_superieur_a_12_est_refuse(client):
    # Simply Lift (13 points) reserve 7 places sur Spring Festival...
    premiere = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '7',
    })
    assert b'Great-booking complete!' in premiere.data

    # ... puis 6 de plus (7 + 6 = 13 > 12) : la seconde doit etre refusee.
    seconde = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '6',
    })
    assert b'plus de 12 places' in seconde.data


def test_cumul_jusqu_a_12_est_accepte(client):
    # Deux reservations de 5 places (cumul 10 <= 12) doivent etre acceptees.
    premiere = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '5',
    })
    seconde = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '5',
    })

    assert b'Great-booking complete!' in premiere.data
    assert b'Great-booking complete!' in seconde.data
