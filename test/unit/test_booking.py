"""Tests unitaires — regles metier de reservation (module booking)."""
from datetime import datetime

import booking

MAINTENANT = datetime(2030, 1, 1, 0, 0, 0)
FUTURE = "2031-01-01 10:00:00"
PASSEE = "2029-01-01 10:00:00"


def test_reservation_valide_est_autorisee():
    autorise, message = booking.verifier_reservation(
        FUTURE, MAINTENANT, places=2, places_disponibles=25,
        points_club=13, deja_reservees=0)

    assert autorise is True
    assert message is None


def test_competition_passee_est_refusee():
    autorise, message = booking.verifier_reservation(
        PASSEE, MAINTENANT, places=1, places_disponibles=25,
        points_club=13, deja_reservees=0)

    assert autorise is False
    assert "passee" in message


def test_places_nulle_ou_negative_refusee():
    for places in (0, -3):
        autorise, message = booking.verifier_reservation(
            FUTURE, MAINTENANT, places=places, places_disponibles=25,
            points_club=13, deja_reservees=0)

        assert autorise is False
        assert "superieur a zero" in message


def test_plus_que_les_points_refuse():
    autorise, message = booking.verifier_reservation(
        FUTURE, MAINTENANT, places=5, places_disponibles=25,
        points_club=4, deja_reservees=0)

    assert autorise is False
    assert "pas assez de points" in message


def test_cumul_superieur_a_12_refuse():
    autorise, message = booking.verifier_reservation(
        FUTURE, MAINTENANT, places=6, places_disponibles=25,
        points_club=13, deja_reservees=7)

    assert autorise is False
    assert "plus de 12 places" in message


def test_places_indisponibles_refuse():
    autorise, message = booking.verifier_reservation(
        FUTURE, MAINTENANT, places=6, places_disponibles=5,
        points_club=13, deja_reservees=0)

    assert autorise is False
    assert "pas assez de places disponibles" in message
