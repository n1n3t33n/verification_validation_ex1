# Intro
```
Hey,

Je viens de recevoir le rapport de QA pour la phase 1 du projet. Il y a plusieurs bogues, dont un qui fait planter l'application ! 
Malheureusement, je ne suis pas au bureau pour les prochains jours (un de mes enfants est tombé malade ce week-end). 
Je ne sais pas encore quand je pourrai être là dans la semaine. Pourriez-vous prendre en charge la mise en œuvre du projet ? 
Vous devrez régler les bogues de la phase 1 et mettre en œuvre les éléments de la phase 2 (j'ai ajouté le travail de la phase 2 et les bogues de la section “issues” du repo). 

Vous devrez cloner et forker le repo et le mettre en place sur votre machine locale (tout ce dont vous avez besoin se trouve dans le fichier README). 
Ensuite, passez en revue les bogues dans la section des problèmes, puis essayez de reproduire les problèmes sur votre machine locale pour résoudre les bogues et ajouter la gestion des erreurs. 
Pour gagner du temps de configuration, nous utilisons Flask et JSON pour éviter d'utiliser une base de données. 
La plupart des outils dont vous aurez besoin se trouvent dans le fichier requirements.txt dans le repo, 
mais vous devrez installer Flask et notre framework de test préféré, pytest, ainsi que notre outil de test de performance, Locust. 

Vous devrez également préparer un rapport de test et un rapport de performances, 
conformément au guide de développement à la fin des spécifications fonctionnelles ci-jointes. 
Veillez à suivre toutes les directives, car le QA nous reproche de ne pas respecter les normes. 
Vous devez tester de manière approfondie les résultats requis (à la fois les happy paths et les sad paths) pour toutes les fonctionnalités de l'application.  
Je vous encourage également à adopter une approche de TDD, car cela vous aidera à rationaliser votre travail. 

Une fois que vous aurez terminé, nous ferons un examen de ce que vous avez dans la branche QA du code. 
Nous examinerons les rapports et la manière dont vous avez résolu les problèmes, 
nous examinerons votre code et nous testerons la couverture de la nouvelle fonctionnalité. 

Merci !

```
1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.
   
 6. Flake8 Report

    Le code respecte flake8 (0 violation). Rapport complet : [RAPPORT_FLAKE8.md](RAPPORT_FLAKE8.md).

---

> La section ci-dessous a ete **ajoutee** lors de la reprise du projet
> (corrections de bugs, phase 2, refonte de l'interface, tests, rapports).
> Elle ne modifie pas le contenu d'origine ci-dessus.

## Lancer le projet (ajouts)

### 1. Pre-requis

Depuis le dossier du projet, avec l'environnement virtuel **active** :

```
pip install -r requirements.txt
```

> Sous Windows / PowerShell, l'activation du venv se fait avec
> `venv\Scripts\Activate.ps1` (au lieu de `source bin/activate`).

### 2. Lancer le serveur

Le lancement est configure par le fichier `.flaskenv` (`FLASK_APP=server.py`),
charge automatiquement par `python-dotenv`. Il suffit donc de :

```
flask run
```

L'application repond sur http://127.0.0.1:5000.

### 3. Lancer les tests

Les tests (pytest) sont regroupes dans `test/` (`unit/` et `functional/`).
Depuis la racine du projet :

```
pytest
```

### 4. Couverture de tests

```
coverage run --source=server,booking,conftest -m pytest
coverage report -m      # resume dans la console
coverage html           # rapport HTML detaille dans htmlcov/
```

### 5. Rapport flake8 (style / PEP 8)

La configuration est dans `setup.cfg` (`max-line-length = 99`).

```
flake8 server.py booking.py conftest.py locustfile.py test
```

Code de sortie 0 et aucune ligne affichee = aucune violation.
Synthese : [RAPPORT_FLAKE8.md](RAPPORT_FLAKE8.md).

### 6. Tests de performance (Locust)

Le scenario est dans `locustfile.py`. Demarrer d'abord le serveur
(`flask run`) dans un terminal, puis, dans un second terminal :

```
# Interface web (ouvrir http://localhost:8089, saisir 6 utilisateurs) :
locust -f locustfile.py --host http://127.0.0.1:5000

# Ou sans interface (6 utilisateurs, 30 secondes) :
locust -f locustfile.py --host http://127.0.0.1:5000 --users 6 --spawn-rate 1 --run-time 30s --headless
```

Synthese : [RAPPORT_DE_PERFORMANCE.md](RAPPORT_DE_PERFORMANCE.md).

### Fichiers et documents ajoutes

- `.flaskenv` — configuration du lancement (`flask run`).
- `booking.py` — regles metier de reservation (fonctions pures).
- `conftest.py`, `test/unit/`, `test/functional/` — harnais et tests.
- `static/`, `templates/layout.html` — interface web (CSS, JS, gabarit partage).
- `locustfile.py` — scenario de test de performance.
- `setup.cfg` — configuration flake8.
- `RAPPORT_DE_TEST.md`, `RAPPORT_DE_PERFORMANCE.md`, `RAPPORT_FLAKE8.md` — rapports.
- `test/corrections.md` — journal detaille des corrections.
    


