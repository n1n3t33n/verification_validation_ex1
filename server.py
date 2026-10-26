import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for,session

import booking


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

# Suivi du cumul de places reservees par (club, competition).
reservationsParClub = {}


def render_welcome(club):
    """Rend la page de resume d'un club (facteur commun a plusieurs vues)."""
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    # request.form.get evite l'erreur 400 si le champ 'email' est absent.
    matching = [c for c in clubs if c['email'] == request.form.get('email', '')]
    if not matching:
        flash("Email inconnu, veuillez reessayer.")
        return render_template('index.html')
    club = matching[0]
    # Ouvre la session du secretaire pour garder le contexte entre les pages.
    session['email'] = club['email']
    return render_welcome(club)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [c for c in competitions if c['name'] == competition]
    # Si le club ou la competition de l'URL est introuvable, on evite le plantage.
    if not foundClub or not foundCompetition:
        flash("Club ou competition introuvable.")
        return render_template('index.html')
    return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0])


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    foundCompetition = [c for c in competitions if c['name'] == request.form.get('competition')]
    foundClub = [c for c in clubs if c['name'] == request.form.get('club')]
    # Donnees de formulaire incompletes ou inconnues : on evite le plantage.
    if not foundCompetition or not foundClub:
        flash("Reservation invalide.")
        return render_template('index.html')
    competition = foundCompetition[0]
    club = foundClub[0]

    # Parsing de l'entree (frontiere) : le nombre de places doit etre un entier.
    try:
        placesRequired = int(request.form.get('places', ''))
    except ValueError:
        flash("Veuillez saisir un nombre de places valide.")
        return render_welcome(club)

    cle = (club['name'], competition['name'])
    dejaReservees = reservationsParClub.get(cle, 0)

    # Toute la regle metier est deportee dans le module booking.
    autorise, message = booking.verifier_reservation(
        date_competition=competition['date'],
        maintenant=datetime.now(),
        places=placesRequired,
        places_disponibles=int(competition['numberOfPlaces']),
        points_club=int(club['points']),
        deja_reservees=dejaReservees,
    )
    if not autorise:
        flash(message)
        return render_welcome(club)

    # Application de l'etat (mutation des donnees en memoire).
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    reservationsParClub[cle] = dejaReservees + placesRequired
    flash('Great-booking complete!')
    return render_welcome(club)


@app.route('/summary')
def summary():
    # Retour au resume du secretaire connecte (via la session), sans re-login.
    email = session.get('email')
    club = [c for c in clubs if c['email'] == email]
    if not club:
        return redirect(url_for('index'))
    return render_welcome(club[0])


@app.route('/pointsBoard')
def pointsBoard():
    # Tableau public des points : accessible sans connexion (lecture seule).
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    # Ferme la session du secretaire.
    session.pop('email', None)
    return redirect(url_for('index'))