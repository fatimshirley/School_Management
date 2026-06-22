from database.database import get_connection
from models.teacher import Teacher
from utils.console import clear
from utils.logger import log_info, log_error
from utils.validator import valider_professeur
import sqlite3



def create_teacher(conn, user_id, nom, subject_id):

    teacher = Teacher(user_id, nom, subject_id)

    erreur = valider_professeur(teacher)
    if erreur:
        raise ValueError(erreur)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM teachers WHERE nom = ?
    """, (nom,))

    if cursor.fetchone():
        raise ValueError("Ce professeur existe déjà.")

    cursor.execute("""
        INSERT INTO teachers (user_id, nom, subject_id)
        VALUES (?, ?, ?)
    """, (user_id, nom, subject_id))



def ajouter_professeur(nom, email, password, subject_name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM subjects WHERE nom = ?", (subject_name,))
        subject = cursor.fetchone()

        if not subject:
            print("Matière inexistante.")
            return

        subject_id = subject[0]

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
        else:
            cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, 'professeur')
            """, (nom, email, password))
            user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO teachers (user_id, nom, subject_id)
            VALUES (?, ?, ?)
        """, (user_id, nom, subject_id))

        conn.commit()
        print("Professeur ajouté avec succès.")
        log_info(f"Professeur ajouté : {nom}")

    except Exception as e:
        conn.rollback()
        print(f"Erreur : {e}")
        log_error(str(e))

    finally:
        conn.close()


def modifier_professeur(ancien_nom, nouveau_nom, subject_name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM subjects WHERE nom = ?", (subject_name,))
        subject = cursor.fetchone()

        if not subject:
            print("Matière inexistante.")
            return

        subject_id = subject[0]

        cursor.execute("""
            UPDATE teachers
            SET nom = ?, subject_id = ?
            WHERE nom = ?
        """, (nouveau_nom, subject_id, ancien_nom))

        conn.commit()

        if cursor.rowcount == 0:
            print("Professeur introuvable.")
        else:
            print("Professeur modifié avec succès.")

    except Exception as e:
        conn.rollback()
        print(f"Erreur : {e}")

    finally:
        conn.close()


def supprimer_professeur(nom):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM teachers WHERE nom = ?", (nom,))
        conn.commit()

        if cursor.rowcount == 0:
            print("Professeur introuvable.")
        else:
            print("Professeur supprimé.")

    finally:
        conn.close()


def rechercher_professeur(nom):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, user_id, nom, subject_id
            FROM teachers
            WHERE nom = ?
        """, (nom,))

        prof = cursor.fetchone()
        if prof:
            log_info(
                f"Recherche professeur : {nom}"
            )

        return prof

    finally:
        conn.close()


def lister_professeurs():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, user_id, nom, subject_id
            FROM teachers
        """)

        rows = cursor.fetchall()
        log_info(
            f"Liste professeurs affichée : total={len(rows)}"
        )

        for r in rows:
            print(r)

    finally:
        conn.close()



def menu_teacher():
    while True:
        clear()

        print("\n===== PROFESSEURS =====")
        print("1. Ajouter professeur")
        print("2. Modifier professeur")
        print("3. Supprimer professeur")
        print("4. Rechercher professeur")
        print("5. Lister professeurs")
        print("0. Retour")

        choix = input("Choix : ").strip()

        if choix == "1":
            nom = input("Nom : ")
            email = input("Email : ")
            password = input("Password : ")
            subject_name = input("Matière : ")
            ajouter_professeur(nom, email, password, subject_name)

        elif choix == "2":
            ancien = input("Ancien nom : ")
            nouveau = input("Nouveau nom : ")
            subject = input("Matière : ")
            modifier_professeur(ancien, nouveau, subject)

        elif choix == "3":
            nom = input("Nom : ")
            supprimer_professeur(nom)

        elif choix == "4":
            nom = input("Nom : ")
            print(rechercher_professeur(nom))

        elif choix == "5":
            lister_professeurs()

        elif choix == "0":
            break

        else:
            print("Choix invalide")

        input("\nEntrée...")