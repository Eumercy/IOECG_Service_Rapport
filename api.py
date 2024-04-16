from flask import jsonify, request
from database import db
from models import *


def health():
    return jsonify({"status": "up"})        



def get_rapports_for_analysis(id_analyse):
    
    #Récuperer les id_experience de l'analyse
    experiences = Experiences.query.filter_by(id_analysis_experience=id_analyse).all()
    id_experiences = [exp.id_experience for exp in experiences]

    #Récupérer les rapports associés à l'expérience, donc les rapports de l'analyse
    rapports = Rapport.query.filter(Rapport.id_experience_rapport.in_(id_experiences)).all()

    # Convertir les résultats en une liste JSON
    serialized_rapports = [{
                        'id_rapport': rap.id_rapport,
                        'id_experience_rapport': rap.id_experience_rapport, 
                        'created_at': rap.created_at, 
                        'name_rapport': rap.name_rapport} 
                        for rap in rapports] 
    return jsonify(serialized_rapports)


def createRapport(id_experience):
    data = request.json

    print(id_experience)

    id_experience_rapport = data.get("id_experience_rapport")
    created_at = data.get("created_at")
    name_rapport = data.get("name_rapport")

    print(data)

    #Creation du nouveau rapport
    new_rapport = Rapport(id_experience_rapport=id_experience_rapport,created_at=created_at,\
                          name_rapport=name_rapport)
    
    # Ajouter dans la bdd
    db.session.add(new_rapport)
    try:
        # Valider et enregistrer les modifications dans la bdd
        db.session.commit()
        return jsonify({"message": "Experience créé avec succès"}), 201
    except Exception as e:
        # Erreur, annuler les modifications et renvoyer un message d'erreur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    