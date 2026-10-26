"""Tests fonctionnels — connexion du secretaire (bug 2 : email inconnu).

Verifie que la connexion avec un email absent de la base ne fait plus planter
l'application (plus de 500) et affiche un message d'erreur, et qu'un email
valide affiche bien la page de resume.
"""


def test_email_inconnu_ne_plante_pas(client):
    """Un email inconnu ne doit pas provoquer d'erreur serveur (500)."""
    response = client.post('/showSummary', data={'email': 'inconnu@nulepart.com'})

    assert response.status_code == 200


def test_email_inconnu_affiche_un_message_d_erreur(client):
    """Un email inconnu doit afficher un message d'erreur a l'utilisateur."""
    response = client.post('/showSummary', data={'email': 'inconnu@nulepart.com'})

    assert b'Email inconnu' in response.data


def test_email_connu_affiche_le_resume(client):
    """Un email valide doit afficher la page de resume (Welcome)."""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

    assert response.status_code == 200
    assert b'Welcome' in response.data
