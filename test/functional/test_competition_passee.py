"""Tests fonctionnels — reservation sur une competition passee (bug 8).

Une competition dont la date est deja passee ne doit plus etre reservable.
"""
from datetime import datetime, timedelta

import server


def test_reservation_sur_competition_passee_est_refusee(client):
    # On force Spring Festival dans le passe.
    date_passee = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    for competition in server.competitions:
        if competition['name'] == 'Spring Festival':
            competition['date'] = date_passee

    # Reservation par ailleurs valide (Simply Lift, 1 place), mais competition
    # passee -> doit etre refusee.
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '1',
    })

    assert b'passee' in response.data


def test_reservation_sur_competition_future_est_acceptee(client):
    # Les competitions sont a venir par defaut (fixture) : la reservation passe.
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '1',
    })

    assert b'Great-booking complete!' in response.data
