from database.database import get_connection
from utils.console import clear
from models.user import User
from utils.validator import valider_utilisateur
from utils.logger import log_info, log_error
from services.student_service import create_student
import sqlite3


# =========================================================
# MENU USERS
# =========================================================
def menu_users():
    while True:
        clear()

        print("\n===== UTILISATEURS =====")
        print("1. Ajouter utilisateur")
        print("2. Supprimer utilisateur")
        print("3. Lister utilisateurs")
        print("0. Retour")

        choix = input("Choix : ").strip()

        if choix == "1":
            name = input("Nom : ")
            email = input("Email : ")
            password = input("Password : ")
            role = input("Role (admin/professeur/etudiant) : ")

            user = User(name, email, password, role)
            ajouter_utilisateur(user)

            input("\nEntrée...")

        elif choix == "2":
            email = input("Email : ")
            supprimer_utilisateur(email)
            input("\nEntrée...")

        elif choix == "3":
            lister_utilisateurs()
            input("\nEntrée...")

        elif choix == "0":
            break

        else:
            print("Choix invalide")
            input("\nEntrée...")


# =========================================================
# AJOUT UTILISATEUR
# =========================================================
def ajouter_utilisateur(user):

    erreur = valider_utilisateur(user)
    if erreur:
        print(erreur)
        log_error(f"Validation user échouée : {erreur}")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # =========================
        # UNIQUE ADMIN
        # =========================
        if user.role == "admin":
            cursor.execute("""
                SELECT id FROM users WHERE role = 'admin'
            """)
            if cursor.fetchone():
                print("Un administrateur existe déjà.")
                return

        # =========================
        # CHECK EMAIL UNIQUE
        # =========================
        cursor.execute("""
            SELECT id FROM users WHERE email = ?
        """, (user.email,))

        if cursor.fetchone():
            print("Email déjà utilisé.")
            return

        # =========================
        # INSERT USER
        # =========================
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            user.name,
            user.email,
            user.password,
            user.role
        ))

        user_id = cursor.lastrowid

        # =========================
        # SI ETUDIANT → CREATION STUDENT
        # =========================
        if user.role == "etudiant":

            print("\n--- Infos étudiant ---")
            matricule = input("Matricule : ")
            prenom = input("Prénom : ")
            age = input("Age : ")
            classe = input("Classe : ")

            create_student(
                conn,
                user_id,
                matricule,
                user.name,
                prenom,
                age,
                classe
            )

        conn.commit()

        print("Utilisateur ajouté avec succès.")
        log_info(f"Utilisateur ajouté : {user.email}")

    except sqlite3.IntegrityError:
        conn.rollback()
        print("Erreur : contrainte base de données.")
        log_error("IntegrityError lors ajout user")

    except ValueError as e:
        conn.rollback()
        print(e)
        log_error(str(e))

    except Exception as e:
        conn.rollback()
        print("Erreur inattendue")
        log_error(f"Erreur ajout user : {e}")

    finally:
        conn.close()


# =========================================================
# SUPPRESSION UTILISATEUR
# =========================================================
def supprimer_utilisateur(email):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if not email:
            print("Email invalide.")
            return

        cursor.execute("""
            DELETE FROM users WHERE email = ?
        """, (email,))

        conn.commit()

        if cursor.rowcount == 0:
            print("Utilisateur introuvable.")
        else:
            print("Utilisateur supprimé.")
            log_info(f"User supprimé : {email}")

    except Exception as e:
        conn.rollback()
        print("Erreur suppression utilisateur.")
        log_error(f"Erreur suppression user : {e}")

    finally:
        conn.close()


# =========================================================
# LISTE UTILISATEURS
# =========================================================
def lister_utilisateurs():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT name, email, role
            FROM users
            ORDER BY name
        """)

        rows = cursor.fetchall()

        if not rows:
            print("Aucun utilisateur.")
            return

        print("\n===== LISTE UTILISATEURS =====")

        for r in rows:
            print(f"Nom: {r[0]} | Email: {r[1]} | Role: {r[2]}")

        log_info("Liste utilisateurs affichée")

    except Exception as e:
        print("Erreur affichage utilisateurs.")
        log_error(f"Erreur listing users : {e}")

    finally:
        conn.close()