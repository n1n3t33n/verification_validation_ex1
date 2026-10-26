"""Test de performance Locust pour l'application GUDLFT.

Simule des secretaires de club qui naviguent, se connectent, consultent les
points et reservent des places. A lancer avec 6 utilisateurs (valeur par defaut
des specs) contre un serveur demarre via `flask run`.

Exemple :
    locust -f locustfile.py --host http://127.0.0.1:5000 \
        --users 6 --spawn-rate 1 --run-time 30s --headless
"""
from locust import HttpUser, task, between


class SecretaireUser(HttpUser):
    # Pause de 1 a 2 secondes entre deux actions (simule un utilisateur humain).
    wait_time = between(1, 2)

    @task
    def page_accueil(self):
        # Page de connexion.
        self.client.get("/")

    @task
    def tableau_des_points(self):
        # Tableau public des points (phase 2).
        self.client.get("/pointsBoard")

    @task
    def connexion_et_liste_competitions(self):
        # Connexion : affiche la liste des competitions (seuil specs : < 5 s).
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def reservation(self):
        # Reservation d'une place : met a jour les points (seuil specs : < 2 s).
        self.client.post("/purchasePlaces", data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "1",
        })
