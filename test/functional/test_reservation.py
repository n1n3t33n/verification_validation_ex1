"""Tests fonctionnels — reservation de places.

Bug 3 : un club ne doit pas pouvoir reserver plus de places qu'il n'a de points
(regle des specs : 1 point = 1 place).
"""


def test_reservation_superieure_aux_points_est_refusee(client):
    # Iron Temple possede 4 points : reserver 5 places doit etre refuse.
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '5',
    })

    assert b'pas assez de points' in response.data


def test_reservation_dans_la_limite_des_points_est_acceptee(client):
    # Iron Temple possede 4 points : reserver 3 places doit etre accepte.
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '3',
    })

    assert b'Great-booking complete!' in response.data
