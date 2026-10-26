"""Tests fonctionnels — tableau public des points (bug 7, phase 2).

Un tableau en lecture seule doit lister tous les clubs et leurs points, et etre
accessible sans connexion.
"""


def test_tableau_points_accessible_sans_connexion(client):
    """La page du tableau des points doit repondre 200 sans connexion."""
    response = client.get('/pointsBoard')

    assert response.status_code == 200


def test_tableau_points_affiche_les_clubs_et_leurs_points(client):
    """La page doit afficher chaque club et son solde de points."""
    response = client.get('/pointsBoard')

    assert b'Simply Lift' in response.data
    assert b'Iron Temple' in response.data
    assert b'She Lifts' in response.data
    assert b'13' in response.data  # points de Simply Lift
