from database.init_db import create_tables
from services.student_service import menu_students
from services.teacher_service import menu_teacher
from utils.logger import log_info


create_tables()

while True:
    print("\n===== GESTION ECOLE =====")
    print("1. Utilisateurs")
    print("2. Etudiants")
    print("3. Professeurs")
    print("4. Matières")
    print("5. Notes")
    print("6. Absences")
    print("7. Statistiques")
    print("8. Quitter")

    choix = input("Votre choix : ").strip()

    if choix == "1":
        print("Module Utilisateurs en cours de développement")

    elif choix == "2":
        log_info("Accès module étudiants")
        menu_students()

    elif choix == "3":
        log_info("Accès module professeurs")
        menu_teacher()

    elif choix == "4":
        print("Module Matières en cours de développement")

    elif choix == "5":
        print("Module Notes en cours de développement")

    elif choix == "6":
        print("Module Absences en cours de développement")

    elif choix == "7":
        print("Module Statistiques en cours de développement")

    elif choix == "8":
        print("Au revoir ")
        break

    else:
        print("Choix invalide")
        