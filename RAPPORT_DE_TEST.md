# Rapport de test — GUDLFT

## Objectif

Corriger les bogues de la phase 1, implementer la phase 2, et couvrir le code
par des tests. Objectif de couverture du guide : **>= 60 %**.

## Resultat global

- **29 tests**, **100 % reussis**.
- **Couverture : 100 %** (`server.py` et `conftest.py`), mesuree avec `coverage`.

## Outils et methode

- **Framework** : pytest 9.1.1.
- **Couverture** : coverage 7.17.0.
- **Approche TDD** : pour chaque bogue, un (ou plusieurs) test ecrit d'abord et
  verifie **en echec (rouge)**, puis la correction appliquee jusqu'au **vert**,
  sans regression sur les tests precedents.
- **Isolation** : fixture `reset_donnees` (`conftest.py`) qui recharge les
  donnees en memoire, force des dates de competition a venir et vide le registre
  des cumuls avant chaque test.

### Lancer les tests

```
pytest
coverage run --source=server,conftest -m pytest && coverage report -m
```

## Organisation

Les tests sont regroupes dans `test/` (sous-dossier `functional/`). Les tests
sont **fonctionnels** : ils exercent les routes via le client de test Flask,
ce qui donne une couverture de 100 % du comportement reel de l'application.

> Note : les dossiers `test/unit/` et `test/integration/` sont prevus par la
> convention mais restent vides ; la logique metier etant portee par les vues
> (routes), les tests fonctionnels ont ete privilegies. Des tests unitaires de
> `loadClubs` / `loadCompetitions` pourraient les completer si souhaite.

## Inventaire des tests

| Fichier | Nb | Portee |
|---------|----|--------|
| `test_lancement.py` | 2 | Demarrage, page d'accueil |
| `test_connexion.py` | 4 | Connexion (email connu/inconnu/manquant) |
| `test_reservation.py` | 10 | Points, 12 max, places dispo, deduction, 0/negatif |
| `test_book.py` | 3 | Route book (noms invalides) |
| `test_saisie.py` | 3 | Entrees non numeriques / champs manquants |
| `test_cumul_places.py` | 2 | Cumul des 12 places par competition |
| `test_competition_passee.py` | 2 | Refus sur competition passee |
| `test_tableau_points.py` | 2 | Tableau public des points |
| `test_deconnexion.py` | 1 | Deconnexion |
| **Total** | **29** | |

## Correctifs couverts

Les 13 corrections (phase 1, phase 2 et robustesse) sont detaillees dans
`test/corrections.md`, chacune avec son symptome, sa cause, sa correction et ses
tests associes.

## Conclusion

L'ensemble des exigences fonctionnelles est couvert par des tests automatises
passant a 100 %, avec une couverture de code de 100 % — bien au-dela de
l'objectif de 60 %.
