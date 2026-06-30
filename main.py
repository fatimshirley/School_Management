from database.init_db import create_tables
from database.database import get_connection

from services.student_service import menu_students
from services.teacher_service import menu_teacher
from services.subject_service import menu_subject
from services.user_service import menu_users
from services.grade_service import menu_grade
from services.absence_service import menu_absence
from services.stats_service import menu_statistics

from utils.logger import log_info
from services.auth import login
from services.student_space import menu_etudiant
from services.teacher_space import menu_professeur



def create_default_admin():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE role = 'admin'")
        admin = cursor.fetchone()

        if not admin:
            cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, 'admin')
            """, ("ADMIN", "admin@gmail.com", "admin123"))

            conn.commit()
            print("Admin par défaut créé")

    except Exception as e:
        conn.rollback()
        print(f"Erreur création admin : {e}")

    finally:
        conn.close()



create_tables()
create_default_admin() 

user_connecte = login()

if user_connecte is None:
    print("Au revoir.")
    exit()


if user_connecte["role"] == "etudiant":
    menu_etudiant(user_connecte["id"])
    exit()

elif user_connecte["role"] == "professeur":
    menu_professeur()  
    exit()

elif user_connecte["role"] == "admin":

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
            log_info("Accès module utilisateurs")
            menu_users()

        elif choix == "2":
            log_info("Accès module étudiants")
            menu_students()

        elif choix == "3":
            log_info("Accès module professeurs")
            menu_teacher()

        elif choix == "4":
            log_info("Accès module matières")
            menu_subject()

        elif choix == "5":
            log_info("Accès module Notes")
            menu_grade()

        elif choix == "6":
            log_info("Accès module Absence")
            menu_absence()

        elif choix == "7":
            log_info("Accès module statistiques")
            menu_statistics()

        elif choix == "8":
            print("Au revoir")
            break

        else:
            print("Choix invalide")

