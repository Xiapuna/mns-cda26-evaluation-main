from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from babel.dates import format_date

app = Flask(__name__)
app.secret_key = "best-teacher"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ideabox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Renvoie un dictionnaire "format_date" aux templates avant chaque rendu de template. Utilisé pour formater la date de la liste des évènements.
@app.context_processor
def inject_format_date():
    return dict(format_date=format_date)

# Création du modèle de la base de données lors de la création d'un évènement 
class Event(db.Model):
    __tablename__ = 'create_event'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable =False)
    place = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    submission_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Représentation sous forme de string de l'instance
    def __repr__(self):
        return f"Event('{self.title}', '{self.type}', '{self.date}', '{self.place}', '{self.description}', '{self.submission_date}')"

# Création de la base de données
with app.app_context():
    db.create_all()

# Route qui mène vers la page d'accueil d'IdeaBox avec la liste des évènements
@app.route("/", methods=['GET'])
def list_events() :
    
    # Requête "SQL" de l'ORM qui selectionne tous les évènements et les trie en fonction de la date
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template("list-events.html", events=events)

# Route qui mène vers la page de création d'un évènement
@app.route("/create-event", methods=['POST'])
def create_event_post() : 
    error = {}
    
    # Title #
    title = request.form.get("title")
    if not title :
        error['title'] = "A name is required."
    
    # Type #
    type = request.form.get("type")
    
    # Date #
    date_str = request.form.get("date")
    if not date_str :
            error['date_str'] = "Date is required." 
    else :
        date = datetime.fromisoformat(date_str)
        if date.date() < datetime.now().date() :
            error['date'] = "An earlier date is impossible."
    
    # Place #
    place = request.form.get("place", "error")
    if not place :
        error['place'] = "A place is required."
    
    # Description #
    description = request.form.get("description")
    if not description :
        error['description'] = "A description is required."
    
    if error :
        return render_template("create-event.html", error=error, data=request.form)
    
    event = Event(title=title, type=type, date=date, place=place, description=description)
    
    # Si l'évènement ne présente pas d'erreur alors il est ajouté et est commité sur la base de données
    db.session.add(event)
    db.session.commit()
    
    flash("Event created successfully!", "success")
    return redirect(url_for("list_events"))


# Route permettant l'affichage de la page de création d'évènements après soumission du form.
@app.route("/create-event", methods=['GET'])
def create_event_get() : 
    
    return render_template("create-event.html")

# Création de la route pour pouvoir supprimer des données (côté utilisateur)  
@app.route("/delete-event/<int:event_id>")
def delete_event(event_id):
    event = Event.query.get(event_id)
    flash(f"Event «{ event.title }» has been deleted", "success")
    
    db.session.delete(event)
    db.session.commit()
    
    return redirect(url_for("list_events"))

# Route qui affiche les 5 prochains évènements à partir de la date du jour (API)
@app.route("/list-next-five-events", methods=['GET'])
def list_next_five_events() :
    events = (Event.query
        .filter(func.date(Event.date) >= func.date(func.now()))
        .order_by(Event.date.asc())
        .limit(5)
        .all()
    )
    
    clean_events = []
    for event in events :
        clean_events.append({
            "id": event.id,
            "title": event.title,
            "type": event.type,
            "date": event.date,
            "place": event.place,
            "description": event.description,
            "submission_date": event.submission_date
        })
    
    return jsonify(
        {
            "next-five-events": clean_events
        }
    )