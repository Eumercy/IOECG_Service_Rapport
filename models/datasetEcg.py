from sqlalchemy import CheckConstraint
from database import db  

class DatasetsECG(db.Model):
    __tablename__ = 'datasets_ecg'

    id_dataset = db.Column(db.Integer, db.ForeignKey('datasets.id_dataset'), primary_key=True)
    id_ecg = db.Column(db.Integer, db.ForeignKey('ecg.id_ecg'), primary_key=True)