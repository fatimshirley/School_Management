from database.database import get_connection
from services.grade_service import calculer_moyenne_etudiant
from utils.logger import log_info, log_error


def recuperer_student_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM students
            WHERE user_id = ?
        """, (user_id,))

        resultat = cursor.fetchone()

        if resultat:
            return resultat[0]

        return None

    except Exception as e:

        log_error(f"Erreur récupération étudiant : {e}")
        return None

    finally:
        conn.close()


def consulter_mes_notes(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT subjects.nom, grades.note
            FROM grades
            JOIN subjects
                ON grades.subject_id = subjects.id
            WHERE grades.student_id = ?
            ORDER BY subjects.nom
        """, (student_id,))

        notes = cursor.fetchall()

        if not notes:
            print("Aucune note enregistrée.")
            return

        print("\n===== MES NOTES =====")

        for matiere, note in notes:
            print(f"Matière : {matiere} | Note : {note}")

    except Exception as e:

        print("Erreur lors de la consultation.")
        log_error(f"Erreur notes étudiant : {e}")

    finally:
        conn.close()


def rechercher_note(student_id):

    matiere = input("Nom de la matière : ")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT grades.note
            FROM grades
            JOIN subjects
                ON grades.subject_id = subjects.id
            WHERE grades.student_id = ?
              AND subjects.nom = ?
        """, (
            student_id,
            matiere
        ))

        resultat = cursor.fetchone()

        if resultat:
            print(f"Votre note en {matiere} est : {resultat[0]}")
        else:
            print("Aucune note trouvée.")

    except Exception as e:

        print("Erreur lors de la recherche.")
        log_error(f"Erreur recherche note : {e}")

    finally:
        conn.close()


def total_absences(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM absences
            WHERE student_id = ?
        """, (student_id,))

        total = cursor.fetchone()[0]

        print(f"Total absences : {total}")

    except Exception as e:

        print("Erreur lors du calcul.")
        log_error(f"Erreur total absences : {e}")

    finally:
        conn.close()


def afficher_absences(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT date, statut
            FROM absences
            WHERE student_id = ?
            ORDER BY date DESC
        """, (student_id,))

        absences = cursor.fetchall()

        if not absences:
            print("Aucune absence enregistrée.")
            return

        print("\n===== MES ABSENCES =====")

        for date, statut in absences:
            print(f"Date : {date} | Statut : {statut}")

    except Exception as e:

        print("Erreur lors de la consultation.")
        log_error(f"Erreur affichage absences : {e}")

    finally:
        conn.close()


def menu_etudiant(user_id):

    student_id = recuperer_student_id(user_id)

    if not student_id:
        print("Profil étudiant introuvable.")
        return

    while True:

        print("\n===== ESPACE ETUDIANT =====")
        print("1. Consulter ma moyenne")
        print("2. Rechercher une note")
        print("3. Afficher toutes mes notes")
        print("4. Total absences")
        print("5. Afficher mes absences")
        print("0. Déconnexion")

        choix = input("Choix : ").strip()

        if choix == "1":

            moyenne = calculer_moyenne_etudiant(
                student_id
            )

            if moyenne is not None:
                print(f"Moyenne générale : {moyenne}/20")
            else:
                print("Aucune note enregistrée.")

        elif choix == "2":
            rechercher_note(student_id)

        elif choix == "3":
            consulter_mes_notes(student_id)

        elif choix == "4":
            total_absences(student_id)

        elif choix == "5":
            afficher_absences(student_id)

        elif choix == "0":
            break

        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")