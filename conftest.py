"""Configuration partagee des tests pytest.

La presence de ce fichier a la racine du projet ajoute le dossier du projet au
`sys.path`, ce qui permet d'importer `server` depuis n'importe quel test.

Les tests doivent etre lances depuis la racine du projet : `pytest`.
"""
from datetime import datetime, timedelta

import pytest

import server


@pytest.fixture
def client():
    """Client de test Flask isole, utilise par les tests fonctionnels."""
    server.app.config['TESTING'] = True
    with server.app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_donnees():
    """Recharge les donnees en memoire avant chaque test.

    Les clubs et competitions sont stockes dans des variables globales que les
    routes modifient (reservations). On les recharge depuis les fichiers JSON
    avant chaque test pour garantir l'isolation.
    """
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    # Par defaut, les competitions de test sont a venir (reservation possible).
    date_future = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
    for competition in server.competitions:
        competition['date'] = date_future
    # On vide le registre des cumuls de reservations entre chaque test.
    server.reservationsParClub = {}
