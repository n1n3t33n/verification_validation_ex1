# Rapport de performance — GUDLFT

## Contexte

Test de charge de l'application de reservation GUDLFT avec **Locust**, conforme
aux exigences des specifications fonctionnelles :

- temps de recuperation de la liste des competitions : **< 5 s** ;
- temps de mise a jour du total de points : **< 2 s** ;
- nombre d'utilisateurs par defaut : **6**.

## Methode

- **Outil** : Locust 2.47.0.
- **Scenario** : `locustfile.py` (classe `SecretaireUser`) — chaque utilisateur
  virtuel enchaine, avec 1 a 2 s de pause, quatre parcours :
  - `GET /` (accueil) ;
  - `GET /pointsBoard` (tableau public des points) ;
  - `POST /showSummary` (connexion + liste des competitions) ;
  - `POST /purchasePlaces` (reservation + mise a jour des points).
- **Cible** : `http://127.0.0.1:5000` (serveur `flask run`).
- **Charge** : 6 utilisateurs, montee de 1 utilisateur/seconde.

### Reproduire le test

1. Terminal 1 : `flask run`.
2. Terminal 2 : `locust -f locustfile.py --host http://127.0.0.1:5000`
   puis, dans l'interface http://localhost:8089, saisir 6 utilisateurs.
   (Variante sans interface : ajouter `--users 6 --spawn-rate 1 --run-time 30s --headless`.)

## Resultats

Mesures sur 111 requetes, **0 % d'echec** :

| Route | Role metier | Mediane | 95e pct | 99e pct | Max | Seuil | Verdict |
|-------|-------------|---------|---------|---------|-----|-------|---------|
| `POST /showSummary` | Liste des competitions | 8 ms | 10 ms | 21 ms | 21 ms | < 5000 ms | OK |
| `POST /purchasePlaces` | Mise a jour des points | 8 ms | 20 ms | 23 ms | 23 ms | < 2000 ms | OK |
| `GET /` | Accueil | 7 ms | 12 ms | 13 ms | 13 ms | — | OK |
| `GET /pointsBoard` | Tableau des points | 7 ms | 10 ms | 18 ms | 18 ms | — | OK |
| **Agrege** | | 8 ms | 12 ms | 21 ms | 23 ms | | 0 echec |

## Analyse

- Tous les temps de reponse sont de l'ordre de **quelques millisecondes**.
- La liste des competitions repond en ~8 ms (seuil 5 s) : marge d'environ x600.
- La mise a jour des points repond en ~8 ms, 23 ms au pire (seuil 2 s) : marge
  d'environ x85 au pire cas.
- **Aucun echec** sur l'ensemble des requetes.

## Conclusion

L'application respecte **tres largement** les seuils de performance des
specifications pour 6 utilisateurs simultanes. Aucune optimisation n'est
necessaire a ce stade.
