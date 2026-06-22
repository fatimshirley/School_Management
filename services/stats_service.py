from database.database import get_connection
from services.grade_service import calculer_moyenne_etudiant
from utils.logger import log_info, log_error


def meilleur_etudiant():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT student_id
            FROM grades
            GROUP BY student_id
        """)

        students = cursor.fetchall()

        meilleur_id = None
        meilleure_moyenne = -1

        for s in students:
            student_id = s[0]
            moyenne = calculer_moyenne_etudiant(student_id)

            if moyenne is not None and moyenne > meilleure_moyenne:
                meilleure_moyenne = moyenne
                meilleur_id = student_id

        if meilleur_id:
            cursor.execute("""
                SELECT nom, prenom
                FROM students
                WHERE id = ?
            """, (meilleur_id,))

            student = cursor.fetchone()

            print("\n===== MEILLEUR ÉTUDIANT =====")
            print(f"Nom : {student[0]} {student[1]}")
            print(f"Moyenne : {meilleure_moyenne}/20")

            log_info(
                f"Meilleur étudiant : {student[0]} {student[1]} - moyenne={meilleure_moyenne}"
            )

        else:
            print("Aucune donnée disponible.")

    except Exception as e:
        log_error(f"Erreur meilleur étudiant : {e}")

    finally:
        conn.close()



def moyenne_generale():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT AVG(note) FROM grades")
        result = cursor.fetchone()[0]

        if result is not None:
            print(f"Moyenne générale de l'école : {round(result, 2)}/20")
            log_info(
                f"Moyenne générale école : {round(result, 2)}"
            )
        else:
            print("Aucune note disponible.")

    except Exception as e:
        log_error(f"Erreur moyenne générale : {e}")

    finally:
        conn.close()



def total_absences_ecole():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM absences")
        total = cursor.fetchone()[0]

        print(f"Total des absences dans l'école : {total}")
        log_info(
            f"Total absences école : {total}"
        )

    except Exception as e:
        log_error(f"Erreur total absences : {e}")

    finally:
        conn.close()


def menu_statistics():
    while True:
        print("\n===== STATISTIQUES =====")
        print("1. Meilleur étudiant")
        print("2. Moyenne générale")
        print("3. Total absences")
        print("0. Retour")

        choix = input("Choix : ").strip()

        if choix == "1":
            meilleur_etudiant()

        elif choix == "2":
            moyenne_generale()

        elif choix == "3":
            total_absences_ecole()

        elif choix == "0":
            break

        else:
            print("Choix invalide")

        input("\nEntrée pour continuer...")