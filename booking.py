"""Regles metier de reservation.

Fonctions pures (sans effet de bord ni acces au reseau) : elles valident une
demande de reservation a partir de valeurs simples et renvoient une decision.
La vue `purchasePlaces` (server.py) se contente de les appeler puis d'appliquer
l'etat ; aucune regle metier ne reste ainsi dans la vue.
"""
from datetime import datetime

MAX_PLACES_PAR_COMPETITION = 12
FORMAT_DATE = '%Y-%m-%d %H:%M:%S'


def verifier_reservation(date_competition, maintenant, places,
                         places_disponibles, points_club, deja_reservees):
    """Valide une demande de reservation.

    Retourne ``(True, None)`` si la reservation est autorisee, sinon
    ``(False, message)`` avec le message d'erreur a afficher.

    - ``date_competition`` : date de la competition au format texte des JSON ;
    - ``maintenant`` : datetime de reference (injecte pour rester testable) ;
    - ``places`` : nombre de places demandees (entier) ;
    - ``places_disponibles`` : places restantes de la competition ;
    - ``points_club`` : solde de points du club ;
    - ``deja_reservees`` : places deja reservees par ce club sur cette competition.
    """
    if datetime.strptime(date_competition, FORMAT_DATE) < maintenant:
        return False, "Cette competition est deja passee, reservation impossible."
    if places <= 0:
        return False, "Le nombre de places doit etre superieur a zero."
    if places > points_club:
        return False, "Vous n'avez pas assez de points pour reserver autant de places."
    if deja_reservees + places > MAX_PLACES_PAR_COMPETITION:
        return False, "Vous ne pouvez pas reserver plus de 12 places pour cette competition."
    if places > places_disponibles:
        return False, "Il n'y a pas assez de places disponibles pour cette competition."
    return True, None
