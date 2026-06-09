def valider_etudiant(etudiant):

    if (
        not etudiant.matricule
        or not etudiant.nom
        or not etudiant.prenom
        or not etudiant.age
        or not etudiant.classe
    ):
        return "Tous les champs doivent être remplis."

    try:
        etudiant.age = int(etudiant.age)
    except ValueError:
        return "L'âge doit être un nombre."

    if etudiant.age <= 0:
        return "L'âge doit être supérieur à 0."

    return None

def valider_professeur(professeur):

    if not professeur.matiere or not professeur.nom:
        return "Tous les champs doivent être remplis."

    return None