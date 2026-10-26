"""Tests fonctionnels — demarrage de l'application (bug 1 : lancement).

Ces tests verifient que l'application se lance correctement et sert sa page
"""


def test_page_accueil_renvoie_200(client):
    """La page d'accueil doit repondre avec un statut HTTP 200."""
    response = client.get('/')

    assert response.status_code == 200


def test_page_accueil_affiche_le_titre(client):
    """La page d'accueil doit afficher le portail de reservation GUDLFT."""
    response = client.get('/')

    assert b'GUDLFT' in response.data
