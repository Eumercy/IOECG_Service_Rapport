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


def get_rapports_for_projet(id_projet):
    
    #Récuperer des analyses du projet avec les id_projet de l'analyse  
    analyses = Analyse.query.filter_by(id_project=id_projet).all()
    id_analyses = [ana.id_analysis for ana in analyses]

    #Récuperer les experiences de tous le projet grâce aux id_analyses
    experiences = Experiences.query.filter(Experiences.id_analysis_experience.in_(id_analyses)).all()
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



def deleteRapportById(id):
    print(id)
    rapport = Rapport.query.filter_by(id_rapport=id).first()  # on récupère le rapport à supprimer
    if rapport:
        db.session.delete(rapport)
        db.session.commit()
        return jsonify({"message": "Rapport deleted with success"}), 201
    else:
        return jsonify({"error": "Rapport not found"}), 404
    
def getAllRapports():
    all_rapports = Rapport.query.all()  # Récupérer tous les rapports depuis la base de données

    # Créer la liste des rapports pour les renvoyer au client
    serialized_rapports = [{
            "id_rapport": rapport.id_rapport,
            "id_experience_rapport": rapport.id_experience_rapport,
            "created_at": rapport.created_at,
            "name_rapport": rapport.name_rapport
        } for rapport in all_rapports]

    return jsonify(serialized_rapports)


def getRapportById(id):
    print(id)
    rapport = Rapport.query.filter_by(id_rapport=id).first()  # on récupère le rapport par son ID
    if rapport:
        serialized_rapport = {
            "id_rapport": rapport.id_rapport,
            "id_experience_rapport": rapport.id_experience_rapport,
            "created_at": rapport.created_at,
            "name_rapport": rapport.name_rapport
        }
        return jsonify(serialized_rapport)
    else:
        return jsonify({"error": "Rapport not found"}), 404
    
def countEcg(id_datsets):
        ecg=ECG.query.filter_by(id_ecg=id_datsets).all()
        return len(ecg)

def getPrediction (id_rapport):
    rapport = Rapport.query.filter_by(id_rapport=id_rapport).first()
    id_experience = rapport.id_experience_rapport
    experience=Experiences.query.filter_by(id_experience=id_experience).first()
    id_modeles=[ exp for exp in experience.models]
    id_dataset= [exp for exp in experience.datasets]
    print(id_modeles)
    print(id_dataset)
    modeles = Modele.query.filter(Modele.id.in_(id_modeles)).all()
    datasets = Dataset.query.filter(Dataset.id_dataset.in_(id_dataset)).all()
    analyse=Analyse.query.filter_by(id_analysis=experience.id_analysis_experience).first()

    predictionData = {
        'nom_experience': experience.name_experience,
        'evluation': 'ce que le modèle / les modèles evaluent',
        'analyse_onrigine': analyse.name_analysis,
        'predictions':experience.resultat_prediction,
        'f1_score': {
            'precision': 85.25,
            'recall': 74.89,
            'f1_score': 79.63
        },
        'matriceConfusion': {
            'vrais_positifs': 10,
            'faux_positifs': 1,
            'faux_negatifs': 2,
            'vrais_negatifs': 12
        },
        'datasets': [{
                'title': dataset.name_dataset,
                'description': dataset.description_dataset,
                'ecgCount': countEcg(dataset.id_dataset),
                'creationDate': dataset.created_at,
                'type': dataset.type_dataset
            } for dataset in datasets],
        'models': [{
                'name': modele.name,
                'accuracy': modele.learning_rate,
                'trainingTime': modele.task_nature,
                'parameters': modele.description
            } for modele in modeles]
    }
    
    return jsonify(predictionData)
