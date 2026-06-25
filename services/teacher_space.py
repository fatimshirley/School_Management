from database.database import get_connection

from services.grade_service import (
    ajouter_note,
    modifier_note,
    consulter_notes_etudiant
)

from services.absence_service import (
    enregistrer_absence,
    consulter_absences_etudiant
)


def obtenir_student_id(matricule):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM students WHERE matricule = ?",
            (matricule,)
        )

        student = cursor.fetchone()

        if student:
            return student[0]

        return None

    finally:
        conn.close()


def menu_professeur():

    while True:

        print("\n===== ESPACE PROFESSEUR =====")
        print("1. Ajouter une note")
        print("2. Modifier une note")
        print("3. Consulter les notes d'un étudiant")
        print("4. Enregistrer une absence")
        print("5. Consulter les absences d'un étudiant")
        print("0. Déconnexion")

        choix = input("Choix : ").strip()

        # =====================================================
        # AJOUT NOTE
        # =====================================================
        if choix == "1":

            matricule = input("Matricule étudiant : ").strip()
            matiere = input("Nom matière : ").strip()

            try:
                note = float(input("Note : "))
            except ValueError:
                print("Note invalide.")
                input("\nAppuyez sur Entrée...")
                continue

            ajouter_note(matricule, matiere, note)

        # =====================================================
        # MODIFICATION NOTE
        # =====================================================
        elif choix == "2":

            matricule = input("Matricule étudiant : ").strip()
            matiere = input("Nom matière : ").strip()

            try:
                note = float(input("Nouvelle note : "))
            except ValueError:
                print("Note invalide.")
                input("\nAppuyez sur Entrée...")
                continue

            modifier_note(matricule, matiere, note)

        # =====================================================
        # CONSULTATION NOTES
        # =====================================================
        elif choix == "3":

            matricule = input("Matricule étudiant : ").strip()

            student_id = obtenir_student_id(matricule)

            if not student_id:
                print("Étudiant introuvable.")
                input("\nAppuyez sur Entrée...")
                continue

            consulter_notes_etudiant(student_id)

        # =====================================================
        # ENREGISTRER ABSENCE
        # =====================================================
        elif choix == "4":

            matricule = input("Matricule étudiant : ").strip()

            student_id = obtenir_student_id(matricule)

            if not student_id:
                print("Étudiant introuvable.")
                input("\nAppuyez sur Entrée...")
                continue

            date = input("Date (AAAA-MM-JJ) : ").strip()

            statut = input(
                "Statut (justifiee/non justifiee) : "
            ).strip()

            enregistrer_absence(
                student_id,
                date,
                statut
            )

        # =====================================================
        # CONSULTATION ABSENCES
        # =====================================================
        elif choix == "5":

            matricule = input("Matricule étudiant : ").strip()

            student_id = obtenir_student_id(matricule)

            if not student_id:
                print("Étudiant introuvable.")
                input("\nAppuyez sur Entrée...")
                continue

            consulter_absences_etudiant(student_id)

        # =====================================================
        # DECONNEXION
        # =====================================================
        elif choix == "0":
            break

        else:
            print("Choix invalide.")

        input("\nAppuyez sur Entrée...")