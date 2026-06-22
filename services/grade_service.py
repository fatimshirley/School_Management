from database.database import get_connection
from utils.logger import log_info, log_error
from utils.validator import valider_grade
from models.grade import Grade

import sqlite3


def ajouter_note(student_id, subject_id, note):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO grades (student_id, subject_id, note)
            VALUES (?, ?, ?)
        """, (student_id, subject_id, note))

        conn.commit()

        print("Note ajoutée avec succès.")
        log_info(
            f"Ajout note : étudiant={student_id}, matière={subject_id}, note={note}"
        )

    except sqlite3.Error as e:
        print("Erreur lors de l'ajout de la note.")
        log_error(f"Erreur ajout note : {e}")

    finally:
        conn.close()


def modifier_note(student_id, subject_id, note):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE grades
            SET note = ?
            WHERE student_id = ? AND subject_id = ?
        """, (note, student_id, subject_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Note modifiée avec succès.")
            log_info(
                f"Modification note : étudiant={student_id}, matière={subject_id}, nouvelle_note={note}"
            )
        else:
            print("Aucune note trouvée.")

    except sqlite3.Error as e:
        print("Erreur lors de la modification.")
        log_error(f"Erreur modification note : {e}")

    finally:
        conn.close()


def supprimer_note(student_id, subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM grades
            WHERE student_id = ? AND subject_id = ?
        """, (student_id, subject_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Note supprimée avec succès.")
            log_info(
                f"Suppression note : étudiant={student_id}, matière={subject_id}"
            )
        else:
            print("Aucune note trouvée.")

    except sqlite3.Error as e:
        print("Erreur lors de la suppression.")
        log_error(f"Erreur suppression note : {e}")

    finally:
        conn.close()


def calculer_moyenne_etudiant(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT AVG(note)
            FROM grades
            WHERE student_id = ?
        """, (student_id,))

        resultat = cursor.fetchone()

        if resultat and resultat[0] is not None:
            log_info(
                f"Calcul moyenne : étudiant={student_id}, moyenne={round(resultat[0], 2)}"
            )
            return round(resultat[0], 2)

        return None

    except sqlite3.Error as e:
        log_error(f"Erreur calcul moyenne : {e}")
        return None

    finally:
        conn.close()


def menu_grade():
    while True:
        print("\n===== MENU NOTES =====")
        print("1. Ajouter une note")
        print("2. Modifier une note")
        print("3. Supprimer une note")
        print("4. Calculer la moyenne d'un étudiant")
        print("0. Retour")

        choix = input("Choix : ").strip()

        if choix == "1":
            student_id = int(input("ID étudiant : "))
            subject_id = int(input("ID matière : "))
            note = float(input("Note : "))

            ajouter_note(student_id, subject_id, note)

        elif choix == "2":
            student_id = int(input("ID étudiant : "))
            subject_id = int(input("ID matière : "))
            note = float(input("Nouvelle note : "))

            modifier_note(student_id, subject_id, note)

        elif choix == "3":
            student_id = int(input("ID étudiant : "))
            subject_id = int(input("ID matière : "))

            supprimer_note(student_id, subject_id)

        elif choix == "4":
            student_id = int(input("ID étudiant : "))

            moyenne = calculer_moyenne_etudiant(student_id)

            if moyenne is not None:
                print(f"Moyenne : {moyenne}/20")
            else:
                print("Aucune note trouvée.")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")





def consulter_notes_etudiant(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT s.nom, g.note
            FROM grades g
            JOIN subjects s
                ON g.subject_id = s.id
            WHERE g.student_id = ?
        """, (student_id,))

        notes = cursor.fetchall()

        if not notes:
            print("Aucune note trouvée.")
            return

        print("\n===== NOTES =====")

        for matiere, note in notes:
            print(f"Matière : {matiere} | Note : {note}")

    except sqlite3.Error as e:
        log_error(f"Erreur consultation notes : {e}")

    finally:
        conn.close()