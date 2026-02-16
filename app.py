from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super-mns-riz-crousty"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ideabox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

with app.app_context():
    db.create_all()

# Route qui mène vers la page d'accueil d'IdeaBox avec la liste des évènements
@app.route("/", methods=['GET'])
def list_events() :
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template("list-events.html", events=events)

# Routes qui mènent vers la page de création d'un évènement
@app.route("/create-event", methods=['POST'])
def create_event_post() : 
    has_error = False
    
    title = request.form.get("title")
    if not title :
        flash("A name is required.", "error")
        has_error = True
    type = request.form.get("type")
    if not type :
        flash("A type is required.","error")
        has_error = True
    date_str = request.form.get("date")
    if not date_str :
        flash("Date is required.","error")
        has_error = True
    place = request.form.get("place")
    if not place :
        flash("A place is required.","error")
        has_error = True
    description = request.form.get("description")
    if not description :
        flash("A description is required.","error")
        has_error = True
    if has_error:
        return redirect(url_for("create_event_get"))
    
    date = datetime.fromisoformat(date_str)
    
    event = Event(title=title, type=type, date=date, place=place, description=description)
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
    if not event : 
        flash("Entrée d'historique non trouvée", "error")
        return redirect(url_for("list_events"))
    
    db.session.delete(event)
    db.session.commit()
    
    return redirect(url_for("list_events"))

# Route qui affiche les 5 prochains évènements (API)
@app.route("/list-next-five-events")
def list_next_five_events() :
    events = (Event.query
        .filter(func.date(Event.date) >= func.date(func.now()))
        .limit(5)
        .all()
    )
    
    clean_events = []
    for event in events :
        clean_events.append({
            "title": event.title,
            "type": event.type,
            "date": event.date,
            "place": event.place,
            "description": event.description
        })
    return jsonify(
        {
            "next-five-events": clean_events
        }
    )