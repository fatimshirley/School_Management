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
            moyenne = round(resultat[0], 2)

            log_info(
                f"Calcul moyenne : étudiant={student_id}, moyenne={moyenne}"
            )

            return moyenne

        return None

    except sqlite3.Error as e:
        log_error(f"Erreur calcul moyenne : {e}")
        return None

    finally:
        conn.close()


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

            matricule = input("Matricule étudiant : ").strip()
            matiere = input("Matière : ").strip()

            try:
                note = float(input("Note : "))
            except ValueError:
                print("Note invalide.")
                input("Appuyez sur Entrée pour continuer...")
                continue

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM students WHERE matricule = ?",
                (matricule,)
            )
            student = cursor.fetchone()

            if not student:
                print("Étudiant introuvable.")
                conn.close()
                input("Appuyez sur Entrée pour continuer...")
                continue

            cursor.execute(
                "SELECT id FROM subjects WHERE nom = ?",
                (matiere,)
            )
            subject = cursor.fetchone()

            if not subject:
                print("Matière introuvable.")
                conn.close()
                input("Appuyez sur Entrée pour continuer...")
                continue

            conn.close()

            ajouter_note(student[0], subject[0], note)

        
        elif choix == "2":

            matricule = input("Matricule étudiant : ").strip()
            matiere = input("Matière : ").strip()

            try:
                note = float(input("Nouvelle note : "))
            except ValueError:
                print("Note invalide.")
                input("Appuyez sur Entrée pour continuer...")
                continue

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM students WHERE matricule = ?",
                (matricule,)
            )
            student = cursor.fetchone()

            cursor.execute(
                "SELECT id FROM subjects WHERE nom = ?",
                (matiere,)
            )
            subject = cursor.fetchone()

            conn.close()

            if not student or not subject:
                print("Étudiant ou matière introuvable.")
                input("Appuyez sur Entrée pour continuer...")
                continue

            modifier_note(student[0], subject[0], note)

        
        elif choix == "3":

            matricule = input("Matricule étudiant : ").strip()
            matiere = input("Matière : ").strip()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM students WHERE matricule = ?",
                (matricule,)
            )
            student = cursor.fetchone()

            cursor.execute(
                "SELECT id FROM subjects WHERE nom = ?",
                (matiere,)
            )
            subject = cursor.fetchone()

            conn.close()

            if not student or not subject:
                print("Étudiant ou matière introuvable.")
                input("Appuyez sur Entrée pour continuer...")
                continue

            supprimer_note(student[0], subject[0])

        
        elif choix == "4":

            matricule = input("Matricule étudiant : ").strip()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM students WHERE matricule = ?",
                (matricule,)
            )

            student = cursor.fetchone()
            conn.close()

            if not student:
                print("Étudiant introuvable.")
                input("Appuyez sur Entrée pour continuer...")
                continue

            moyenne = calculer_moyenne_etudiant(student[0])

            if moyenne is not None:
                print(f"Moyenne : {moyenne}/20")
            else:
                print("Aucune note trouvée.")

        elif choix == "0":
            break

        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")