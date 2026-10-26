"""Configuration partagee des tests pytest.

La presence de ce fichier a la racine du projet ajoute le dossier du projet au
`sys.path`, ce qui permet d'importer `server` depuis n'importe quel test.

Les tests doivent etre lances depuis la racine du projet : `pytest`.
"""
import pytest

import server


@pytest.fixture
def client():
    """Client de test Flask isole, utilise par les tests fonctionnels."""
    server.app.config['TESTING'] = True
    with server.app.test_client() as test_client:
        yield test_client
