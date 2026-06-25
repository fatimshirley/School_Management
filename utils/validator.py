from datetime import datetime

import unicodedata #sert à manipuler les caractères Unicode, notamment pour supprimer les accents


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

    if not professeur.nom:
        return "le nom est obligatoire."
    
    if professeur.subject_id is None:
        return "La matière est obligatoire."

    return None

def valider_matiere(matiere):

    if not matiere.nom:
        return "Le nom de la matière est obligatoire."

    return None


def valider_utilisateur(utilisateur):

    # nettoyage des données
    name = utilisateur.name.strip()
    email = utilisateur.email.strip()
    password = utilisateur.password.strip()
    role = utilisateur.role.strip().lower()

    # validation champs obligatoires
    if not name or not email or not password or not role:
        return "Tous les champs sont obligatoires."

    # validation email
    if "@" not in email or "." not in email:
        return "Email invalide."

    # validation rôle
    if role not in ("admin", "professeur", "etudiant"):
        return "Rôle invalide."

    # réassignation propre
    utilisateur.name = name
    utilisateur.email = email
    utilisateur.password = password
    utilisateur.role = role

    return None

def valider_grade(grade):

    if grade.student_id is None:
        return "L'étudiant est obligatoire."

    if grade.subject_id is None:
        return "La matière est obligatoire."

    try:
        grade.note = float(grade.note)
    except ValueError:
        return "La note doit être un nombre."

    if grade.note < 0 or grade.note > 20:
        return "La note doit être comprise entre 0 et 20."

    return None




def valider_absence(absence):

    if absence.student_id is None:
        return "L'étudiant est obligatoire."

    if not absence.date:
        return "La date est obligatoire."

    # Validation stricte AAAA-MM-JJ
    try:
        datetime.strptime(absence.date, "%Y-%m-%d")
    except ValueError:
        return "La date doit être au format AAAA-MM-JJ."

    # Normalisation du statut
    statut = absence.statut.strip().lower()

    statut = ''.join(
        c for c in unicodedata.normalize('NFD', statut)
        if unicodedata.category(c) != 'Mn'
    )

    if statut not in ("justifiee", "non justifiee"):
        return "Statut invalide."

    absence.statut = statut

    return None