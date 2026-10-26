"""Tests fonctionnels — robustesse des entrees de reservation (bug 11).

`purchasePlaces` ne doit pas planter (500) si le nombre de places n'est pas un
entier valide, ou si la competition du formulaire est inconnue.
"""


def test_places_non_numerique_ne_plante_pas(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 'abc',
    })

    assert response.status_code == 200
    assert b'nombre de places valide' in response.data


def test_places_vide_ne_plante_pas(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '',
    })

    assert response.status_code == 200
    assert b'nombre de places valide' in response.data


def test_competition_inconnue_ne_plante_pas(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Competition Fantome',
        'club': 'Simply Lift',
        'places': '1',
    })

    assert response.status_code == 200
    assert b'invalide' in response.data
