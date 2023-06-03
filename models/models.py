from models import db


class RakingSalesCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    automobiles_model = db.Column(db.String(60), nullable=False)
    automobiles_licensed = db.Column(db.Integer, nullable=False)
    automobiles_ranking = db.Column(db.String(3), nullable=False)
    commercial_model = db.Column(db.String(60), nullable=False)
    commercial_licensed = db.Column(db.Integer, nullable=False)
    commercial_ranking = db.Column(db.String(3), nullable=False)
    month_reference = db.Column(db.String(10), nullable=False)
    year_reference = db.Column(db.String(4), nullable=False)
    reference_information = db.Column(db.String(8), nullable=False)
