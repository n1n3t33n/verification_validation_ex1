import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for,session


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

# Nombre maximum de places qu'un club peut reserver pour une competition (cumul).
MAX_PLACES_PAR_COMPETITION = 12

competitions = loadCompetitions()
clubs = loadClubs()

# Suivi du cumul de places reservees par (club, competition).
reservationsParClub = {}

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
    return render_template('welcome.html', club=club, competitions=competitions)


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

    # On refuse la reservation si la competition est deja passee.
    dateCompetition = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    if dateCompetition < datetime.now():
        flash("Cette competition est deja passee, reservation impossible.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Le nombre de places doit etre un entier valide.
    try:
        placesRequired = int(request.form.get('places', ''))
    except ValueError:
        flash("Veuillez saisir un nombre de places valide.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # On refuse une demande de places nulle ou negative.
    if placesRequired <= 0:
        flash("Le nombre de places doit etre superieur a zero.")
        return render_template('welcome.html', club=club, competitions=competitions)

    clubPoints = int(club['points'])

    # Un point vaut une place : on refuse si le club demande plus que son solde.
    if placesRequired > clubPoints:
        flash("Vous n'avez pas assez de points pour reserver autant de places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    cle = (club['name'], competition['name'])
    dejaReservees = reservationsParClub.get(cle, 0)
    # Regle metier : au maximum 12 places cumulees par club et par competition.
    if dejaReservees + placesRequired > MAX_PLACES_PAR_COMPETITION:
        flash("Vous ne pouvez pas reserver plus de 12 places pour cette competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    placesDisponibles = int(competition['numberOfPlaces'])

    # On refuse si la competition n'a pas assez de places disponibles.
    if placesRequired > placesDisponibles:
        flash("Il n'y a pas assez de places disponibles pour cette competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    competition['numberOfPlaces'] = placesDisponibles - placesRequired
    # Les points utilises sont deduits du solde du club (1 point par place).
    club['points'] = clubPoints - placesRequired
    # On met a jour le cumul de places reservees pour cette competition.
    reservationsParClub[cle] = dejaReservees + placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/summary')
def summary():
    # Retour au resume du secretaire connecte (via la session), sans re-login.
    email = session.get('email')
    club = [c for c in clubs if c['email'] == email]
    if not club:
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club[0], competitions=competitions)


@app.route('/pointsBoard')
def pointsBoard():
    # Tableau public des points : accessible sans connexion (lecture seule).
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    # Ferme la session du secretaire.
    session.pop('email', None)
    return redirect(url_for('index'))