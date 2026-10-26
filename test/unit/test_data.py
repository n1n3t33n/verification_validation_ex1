"""Tests unitaires — chargement des donnees (fonctions pures de server.py)."""
import server


def test_loadClubs_retourne_une_liste_de_clubs():
    clubs = server.loadClubs()

    assert isinstance(clubs, list)
    assert len(clubs) > 0
    simply_lift = [c for c in clubs if c['name'] == 'Simply Lift']
    assert simply_lift, "Le club 'Simply Lift' doit etre present"
    assert simply_lift[0]['points'] == '13'


def test_chaque_club_a_les_champs_attendus():
    for club in server.loadClubs():
        assert 'name' in club
        assert 'email' in club
        assert 'points' in club


def test_loadCompetitions_retourne_les_competitions():
    noms = [c['name'] for c in server.loadCompetitions()]

    assert 'Spring Festival' in noms
    assert 'Fall Classic' in noms
