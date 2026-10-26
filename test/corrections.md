# Journal des corrections — GUDLFT

Correction des bogues de la **phase 1** et implementation de la **phase 2** de
l'application de reservation GUDLFT (projet verification & validation).

## Conventions de travail

- **Une branche par bug/fonctionnalite** : `bug/...`, `fonctionnalite/...`, `amelioration/...`.
- **Tests** regroupes dans `test/` : `unit/`, `integration/`, `functional/`.
- Lancer les tests **depuis la racine** du projet : `pytest`.
- Couverture visee : **>= 60 %** (objectif du guide de developpement).
- On ne fusionne dans la branche principale que lorsque tous les tests passent.

## Environnement

- Python 3.13, **Flask 3.1.3** (mise a niveau depuis 1.1.2 : requise sous
  Python 3.13 et tiree par Locust ; l'application reste compatible).
- Lancement : `flask run`, configure via le fichier `.flaskenv` (`FLASK_APP=server.py`).
- Outils : `pytest`, `coverage`, `locust`.

## Suivi des corrections

| # | Branche | Sujet | Statut |
|---|---------|-------|--------|
| 1 | `bug/lancement-application` | Lancement de l'application | ✅ Corrige |
| 2 | `bug/connexion-email-inexistant` | Email inconnu -> crash 500 | ⏳ A venir |
| 3 | `bug/reservation-superieure-aux-points` | Reserver plus que ses points | ⏳ A venir |
| 4 | `bug/reservation-superieure-a-12-places` | Reserver plus de 12 places | ⏳ A venir |
| 5 | `bug/places-insuffisantes-competition` | Reserver plus de places que disponibles | ⏳ A venir |
| 6 | `bug/deduction-des-points` | Points jamais deduits | ⏳ A venir |
| 7 | `fonctionnalite/tableau-des-points` | Tableau public des points (phase 2) | ⏳ A venir |
| 8 | `amelioration/competitions-passees` | Reservation sur competition passee | ⏳ Optionnel |

---

### Bug 1 — Lancement de l'application
**Branche** : `bug/lancement-application`

- **Symptome** : `flask run` -> « Could not locate a Flask application. You did
  not provide the "FLASK_APP" environment variable ».
- **Cause** : variable `FLASK_APP` non definie et aucun `app.py`/`wsgi.py`.
  Il s'agit d'un probleme de configuration de lancement (phase 0), pas du code metier.
- **Correction** :
  - ajout du fichier `.flaskenv` contenant `FLASK_APP=server.py` ;
  - ajout de la dependance `python-dotenv` (Flask charge `.flaskenv` automatiquement).
- **Tests** : `test/functional/test_lancement.py`
  - `test_page_accueil_renvoie_200` : la page d'accueil repond 200 ;
  - `test_page_accueil_affiche_le_titre` : la page contient « GUDLFT ».
- **Verification** : `flask run` demarre et sert la page d'accueil ; `pytest` au vert.
