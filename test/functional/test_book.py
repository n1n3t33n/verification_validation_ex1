"""Tests fonctionnels — acces a la page de reservation (bug 10 : route book).

La route /book ne doit pas planter (500) si le club ou la competition indique
dans l'URL n'existe pas.
"""


def test_book_competition_inexistante_ne_plante_pas(client):
    response = client.get('/book/Inexistante/Simply%20Lift')

    assert response.status_code == 200
    assert b'introuvable' in response.data


def test_book_club_inexistant_ne_plante_pas(client):
    response = client.get('/book/Spring%20Festival/ClubBidon')

    assert response.status_code == 200
    assert b'introuvable' in response.data


def test_book_donnees_valides_affiche_le_formulaire(client):
    response = client.get('/book/Spring%20Festival/Simply%20Lift')

    assert response.status_code == 200
    assert b'Places available' in response.data
