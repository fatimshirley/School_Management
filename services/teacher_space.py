from services.grade_service import (
    ajouter_note,
    modifier_note,
    consulter_notes_etudiant
)

from services.absence_service import (
    enregistrer_absence,
    consulter_absences_etudiant
)


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

        if choix == "1":

            matricule = input("Matricule étudiant : ")
            matiere = input("Nom matière : ")
            note = float(input("Note : "))

            ajouter_note(matricule, matiere, note)

        elif choix == "2":

            student_id = int(input("ID étudiant : "))
            subject_id = int(input("ID matière : "))
            note = float(input("Nouvelle note : "))

            modifier_note(student_id, subject_id, note)

        elif choix == "3":

            student_id = int(input("ID étudiant : "))
            consulter_notes_etudiant(student_id)

        elif choix == "4":

            student_id = int(input("ID étudiant : "))
            date = input("Date (AAAA-MM-JJ) : ")
            statut = input("Statut (justifiee/non justifiee) : ")

            enregistrer_absence(student_id, date, statut)

        elif choix == "5":

            student_id = int(input("ID étudiant : "))
            consulter_absences_etudiant(student_id)

        elif choix == "0":
            break

        else:
            print("Choix invalide")

        input("\nAppuyez sur Entrée...")