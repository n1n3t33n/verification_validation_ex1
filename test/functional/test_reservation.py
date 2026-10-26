"""Tests fonctionnels — reservation de places.

Bug 3 : un club ne doit pas pouvoir reserver plus de places qu'il n'a de points
(regle des specs : 1 point = 1 place).
"""
import server


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


def test_reservation_superieure_a_12_est_refusee(client):
    # Simply Lift a 13 points : 13 places (points OK, places OK) doit etre
    # refuse par la seule limite des 12 places.
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '13',
    })

    assert b'plus de 12 places' in response.data


def test_reservation_de_12_places_est_acceptee(client):
    # Simply Lift a 13 points : reserver exactement 12 places doit etre accepte.
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '12',
    })

    assert b'Great-booking complete!' in response.data


def test_reservation_superieure_aux_places_disponibles_est_refusee(client):
    # On force une competition presque pleine : 5 places restantes.
    for competition in server.competitions:
        if competition['name'] == 'Fall Classic':
            competition['numberOfPlaces'] = '5'

    # Simply Lift (13 points) demande 6 places : <= 12 et <= points, mais
    # > 5 places disponibles -> seule la regle des places doit bloquer.
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '6',
    })

    assert b'pas assez de places disponibles' in response.data


def test_reservation_egale_aux_places_disponibles_est_acceptee(client):
    # Competition avec exactement 5 places restantes.
    for competition in server.competitions:
        if competition['name'] == 'Fall Classic':
            competition['numberOfPlaces'] = '5'

    # Simply Lift demande 5 places : egal aux places disponibles -> accepte.
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'club': 'Simply Lift',
        'places': '5',
    })

    assert b'Great-booking complete!' in response.data
