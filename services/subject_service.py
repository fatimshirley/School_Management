from database.database import get_connection
from models.subject import Subject
from utils.console import clear
from utils.validator import valider_matiere
from utils.logger import log_info, log_error

import sqlite3


def menu_subject():
    while True:
        clear()

        print("\n  MATIERE")
        print("1. Ajouter une matière")
        print("2. Lister les matières")
        print("0. Retour")

        choix = input("Choix : ").strip()

        if choix == "1":
            nom = input("Nom de la matière : ")

            matiere = Subject(nom)
            ajouter_matiere(matiere)

            input("Appuyez sur entrée...")

        elif choix == "2":
            print("\n LA LISTE DES MATIERES")
            lister_matiere()

            input("Appuyez sur entrée...")

        elif choix == "0":
            print("Retour au menu principal")
            input("Appuyez sur entrée...")
            break

        else:
            print("Choix invalide")
            input("Appuyez sur Entrée...")


def ajouter_matiere(matiere):

    erreur = valider_matiere(matiere)
    if erreur:
        print(erreur)
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO subjects (nom)
            VALUES (?)
        """, (
            matiere.nom,
        ))

        conn.commit()

        print("Matière ajoutée avec succès")
        log_info(f"Matière ajoutée : {matiere.nom}")

    except sqlite3.IntegrityError:
        log_error(
            f"Ajout impossible : {matiere.nom}"
        )
        print("Cette matière existe déjà.")

    except Exception as e:
        log_error(
            f"Erreur ajout matière : {e}"
        )
        print(f"Erreur : {e}")

    finally:
        conn.close()


def lister_matiere():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, nom
            FROM subjects
        """)

        matieres = cursor.fetchall()

        if not matieres:
            print("Aucune matière enregistrée.")
        else:
            for matiere in matieres:
                print(f"""
Id   : {matiere[0]}
Nom  : {matiere[1]}
                """)

    except Exception as e:
        log_error(
            f"Erreur liste matières : {e}"
        )
        print("Impossible d'afficher les matières.")

    finally:
        conn.close()