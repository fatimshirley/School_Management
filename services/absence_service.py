from database.database import get_connection
from models.absence import Absence
from utils.logger import log_info, log_error
from utils.validator import valider_absence

import sqlite3


# =========================================================
# MENU ABSENCE
# =========================================================
def menu_absence():
    while True:
        print("\n===== MENU ABSENCE =====")
        print("1. Enregistrer une absence")
        print("2. Marquer absence comme justifiée ou non justifiée")
        print("3. Consulter l'historique des absences")
        print("0. Retour")

        choix = input("Choix : ").strip()

        # =====================================================
        # ENREGISTRER ABSENCE
        # =====================================================
        if choix == "1":

            matricule = input("Matricule étudiant : ").strip()
            date = input("Date (AAAA-MM-JJ) : ").strip()
            statut = input(
                "Statut (justifiee/non justifiee) : "
            ).strip().lower()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM students WHERE matricule = ?",
                (matricule,)
            )

            student = cursor.fetchone()

            conn.close()

            if not student:
                print("Etudiant introuvable.")
            else:
                enregistrer_absence(
                    student[0],
                    date,
                    statut
                )

        # =====================================================
        # MODIFIER ABSENCE
        # =====================================================
        elif choix == "2":

            matricule = input("Matricule étudiant : ").strip()
            date = input("Date (AAAA-MM-JJ) : ").strip()
            statut = input(
                "Statut (justifiee/non justifiee) : "
            ).strip().lower()

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
            else:
                marquer_absence(
                    student[0],
                    date,
                    statut
                )

        # =====================================================
        # CONSULTER HISTORIQUE
        # =====================================================
        elif choix == "3":

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
            else:
                consulter_historique(student[0])

        elif choix == "0":
            break

        else:
            print("Choix invalide.")

        input("Appuyez sur Entrée pour continuer...")


# =========================================================
# ENREGISTRER ABSENCE
# =========================================================
def enregistrer_absence(student_id, date, statut):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        absence = Absence(
            student_id,
            date,
            statut
        )

        erreur = valider_absence(absence)

        if erreur:
            print(erreur)
            return

        cursor.execute("""
            INSERT INTO absences (
                student_id,
                date,
                statut
            )
            VALUES (?, ?, ?)
        """, (
            absence.student_id,
            absence.date,
            absence.statut
        ))

        conn.commit()

        print("Absence enregistrée avec succès.")

        log_info(
            f"Absence ajoutée : "
            f"étudiant={student_id}, "
            f"date={date}, "
            f"statut={statut}"
        )

    except sqlite3.Error as e:

        print("Erreur lors de l'enregistrement.")
        log_error(f"Erreur absence : {e}")

    finally:
        conn.close()


# =========================================================
# MODIFIER ABSENCE
# =========================================================
def marquer_absence(student_id, date, statut):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE absences
            SET statut = ?
            WHERE student_id = ?
            AND date = ?
        """, (
            statut,
            student_id,
            date
        ))

        conn.commit()

        if cursor.rowcount > 0:

            print("Absence mise à jour avec succès.")

            log_info(
                f"Modification absence : "
                f"étudiant={student_id}, "
                f"date={date}, "
                f"statut={statut}"
            )

        else:
            print("Aucune absence trouvée.")

    except sqlite3.Error as e:

        print("Erreur lors de la modification.")
        log_error(
            f"Erreur modification absence : {e}"
        )

    finally:
        conn.close()


# =========================================================
# HISTORIQUE ABSENCES
# =========================================================
def consulter_historique(student_id):

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

        log_info(
            f"Consultation historique absences : "
            f"étudiant={student_id}"
        )

        if not absences:
            print("Aucune absence trouvée.")
            return

        print("\n===== HISTORIQUE DES ABSENCES =====")

        for date, statut in absences:
            print(
                f"Date : {date} | "
                f"Statut : {statut}"
            )

    except sqlite3.Error as e:

        print("Erreur lors de la consultation.")
        log_error(
            f"Erreur historique absence : {e}"
        )

    finally:
        conn.close()


# =========================================================
# CONSULTATION ABSENCES ETUDIANT
# =========================================================
def consulter_absences_etudiant(student_id):

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

        log_info(
            f"Consultation absences : "
            f"étudiant={student_id}"
        )

        if not absences:
            print("Aucune absence trouvée.")
            return

        print("\n===== ABSENCES =====")

        for date, statut in absences:
            print(
                f"Date : {date} | "
                f"Statut : {statut}"
            )

    except sqlite3.Error as e:

        log_error(
            f"Erreur consultation absences : {e}"
        )

    finally:
        conn.close()