"""Tests fonctionnels — deconnexion (route logout)."""


def test_logout_redirige_vers_accueil(client):
    """La deconnexion doit rediriger vers la page d'accueil."""
    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'GUDLFT Registration Portal' in response.data
