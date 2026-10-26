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
| 2 | `bug/connexion-email-inexistant` | Email inconnu -> crash 500 | ✅ Corrige |
| 3 | `bug/reservation-superieure-aux-points` | Reserver plus que ses points | ✅ Corrige |
| 4 | `bug/reservation-superieure-a-12-places` | Reserver plus de 12 places | ✅ Corrige |
| 5 | `bug/places-insuffisantes-competition` | Reserver plus de places que disponibles | ✅ Corrige |
| 6 | `bug/deduction-des-points` | Points jamais deduits | ✅ Corrige |
| 7 | `fonctionnalite/tableau-des-points` | Tableau public des points (phase 2) | ✅ Fait |
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

### Bug 2 — Connexion avec un email inexistant
**Branche** : `bug/connexion-email-inexistant`

- **Symptome** : `POST /showSummary` avec un email absent de `clubs.json` ->
  `IndexError` -> erreur 500 (plantage).
- **Cause** : `server.py`, `showSummary` -> `[... for club in clubs if ...][0]`
  indexait `[0]` sur une liste vide quand aucun club ne correspondait.
- **Correction** :
  - `server.py` : verification de la liste des correspondances ; si vide, message
    flash « Email inconnu, veuillez reessayer. » et retour a la page d'accueil ;
  - `templates/index.html` : ajout du bloc d'affichage des messages flash.
- **Tests** : `test/functional/test_connexion.py`
  - `test_email_inconnu_ne_plante_pas` : email inconnu -> 200 (plus de 500) ;
  - `test_email_inconnu_affiche_un_message_d_erreur` : message d'erreur present ;
  - `test_email_connu_affiche_le_resume` : email valide -> page « Welcome ».
- **Verification** : cycle TDD rouge (2 echecs sur `IndexError`) puis vert
  (5/5 tests, aucune regression du bug 1).

### Bug 3 — Reserver plus de places que de points
**Branche** : `bug/reservation-superieure-aux-points`

- **Symptome** : un club pouvait reserver plus de places qu'il n'a de points.
- **Cause** : `server.py`, `purchasePlaces` ne comparait jamais les places
  demandees au solde de points du club (regle : 1 point = 1 place).
- **Correction** : ajout d'un garde-fou dans `purchasePlaces` ; si les places
  demandees depassent les points du club, message flash « Vous n'avez pas assez
  de points... » et reservation refusee.
- **Ajout tests** : fixture `reset_donnees` dans `conftest.py` (isolation des
  donnees en memoire entre les tests), et `test/functional/test_reservation.py`
  - `test_reservation_superieure_aux_points_est_refusee` (Iron Temple, 4 pts, 5 places) ;
  - `test_reservation_dans_la_limite_des_points_est_acceptee` (Iron Temple, 3 places).
- **Verification** : cycle TDD rouge (reservation acceptee a tort) puis vert
  (7/7 tests, aucune regression).

### Bug 4 — Reserver plus de 12 places
**Branche** : `bug/reservation-superieure-a-12-places`

- **Symptome** : un club pouvait reserver plus de 12 places (regle : 12 max).
- **Cause** : `server.py`, `purchasePlaces` ne limitait pas le nombre de places.
- **Correction** : constante `MAX_PLACES_PAR_RESERVATION = 12` + garde-fou dans
  `purchasePlaces` ; au-dela de 12 places, message flash « Vous ne pouvez pas
  reserver plus de 12 places. » et reservation refusee.
- **Ajout tests** (`test/functional/test_reservation.py`) :
  - `test_reservation_superieure_a_12_est_refusee` (Simply Lift, 13 places) ;
  - `test_reservation_de_12_places_est_acceptee` (borne exacte, 12 places).
- **Verification** : cycle TDD rouge (13 places accepte a tort) puis vert
  (9/9 tests, aucune regression).

### Bug 5 — Reserver plus de places que disponibles
**Branche** : `bug/places-insuffisantes-competition`

- **Symptome** : un club pouvait reserver plus de places qu'il n'en reste dans
  la competition (surreservation, `numberOfPlaces` devenait negatif).
- **Cause** : `server.py`, `purchasePlaces` ne comparait pas les places
  demandees aux places disponibles.
- **Correction** : garde-fou comparant `placesRequired` a
  `competition['numberOfPlaces']` ; si insuffisant, message flash « Il n'y a pas
  assez de places disponibles... » et reservation refusee.
- **Ajout tests** (`test/functional/test_reservation.py`, + `import server`) :
  - `test_reservation_superieure_aux_places_disponibles_est_refusee` ;
  - `test_reservation_egale_aux_places_disponibles_est_acceptee` (borne exacte).
- **Verification** : cycle TDD rouge (surreservation a -1) puis vert
  (11/11 tests, aucune regression).

### Bug 6 — Deduction des points
**Branche** : `bug/deduction-des-points`

- **Symptome** : une reservation reussie decrementait les places de la
  competition mais ne retirait jamais les points au club.
- **Cause** : `server.py`, `purchasePlaces` ne mettait jamais a jour
  `club['points']`.
- **Correction** : dans la voie de succes, `club['points'] = clubPoints -
  placesRequired` (1 point par place), apres tous les garde-fous (une
  reservation refusee ne deduit rien).
- **Ajout tests** (`test/functional/test_reservation.py`) :
  - `test_points_deduits_apres_reservation_reussie` (Iron Temple 4 -> 2) ;
  - `test_points_non_deduits_si_reservation_refusee` (solde inchange si refus).
- **Verification** : cycle TDD rouge (points non deduits) puis vert
  (13/13 tests, aucune regression).

### Bug 7 — Tableau public des points (phase 2)
**Branche** : `fonctionnalite/tableau-des-points`

- **Besoin** : un tableau public, en lecture seule, listant les points de tous
  les clubs, accessible sans connexion (specs phase 2).
- **Realisation** :
  - `server.py` : nouvelle route `GET /pointsBoard` (sans authentification) qui
    rend le template avec la liste des clubs ;
  - `templates/points.html` : nouveau template listant chaque club et ses points.
- **Tests** : `test/functional/test_tableau_points.py`
  - `test_tableau_points_accessible_sans_connexion` (200 sans login) ;
  - `test_tableau_points_affiche_les_clubs_et_leurs_points` (clubs + points).
- **Verification** : cycle TDD rouge (route 404) puis vert
  (15/15 tests, aucune regression).
