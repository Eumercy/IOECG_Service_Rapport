from sqlalchemy import CheckConstraint
from database import db  

class Modele(db.Model):
    __tablename__ = 'modeles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    project_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    architecture_name = db.Column(db.String(255))
    architecture_version = db.Column(db.String(50))
    architecture_description = db.Column(db.Text)
    total_params = db.Column(db.Integer)
    model_size = db.Column(db.String(50))
    batch_size = db.Column(db.Integer)
    learning_rate = db.Column(db.Float)
    task_nature = db.Column(db.String(50))

    __table_args__ = (
        db.CheckConstraint("task_nature IN ('classification binaire', 'classification multi-class', 'régression')", name='check_task_nature'),
    )