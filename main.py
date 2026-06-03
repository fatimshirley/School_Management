from database.database import create_tables
from models.student import student
from services.student_service import ajouter_etudiant, lister_etudiants

create_tables()

print("Base créée avec succès")




while True:
    print("\n===== GESTION ECOLE =====")
    print("1. Ajouter étudiant")
    print("2. Lister étudiants")
    print("3. Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        matricule = input("Matricule :")
        nom = input("Nom :")
        prenom = input("Prenom :")
        age = input("Age :")
        classe = input("Classe :")

        ajouter_etudiant(
            matricule, 
            nom, 
            prenom, 
            age, 
            classe)
        print("Etudiant ajouté")



    elif choix == "2":
      
        lister_etudiants()
        print("La liste des étudiants")

    elif choix == "3":
        print("Au revoir")
        break

    else: 
        print("Choix invalide")