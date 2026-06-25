from database.database import get_connection
from models.student import Student
from utils.validator import valider_etudiant
from utils.logger import log_info, log_error
import sqlite3



def create_student(conn, user_id, matricule, nom, prenom, age, classe):

    etudiant = Student(user_id, matricule, nom, prenom, age, classe)

    erreur = valider_etudiant(etudiant)
    if erreur:
        log_error(erreur)
        print(f"[ERREUR] {erreur}")
        raise ValueError(erreur)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM students WHERE matricule = ?
    """, (matricule,))

    if cursor.fetchone():
        msg = "Matricule déjà utilisé"
        print(f"[ERREUR] {msg}")
        log_error(msg)
        raise ValueError(msg)

    cursor.execute("""
        INSERT INTO students (user_id, matricule, nom, prenom, age, classe)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        etudiant.user_id,
        etudiant.matricule,
        etudiant.nom,
        etudiant.prenom,
        etudiant.age,
        etudiant.classe
    ))


    log_info(f"Étudiant créé : {matricule}")


def ajouter_etudiant(nom, prenom, age, classe, matricule, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            raise ValueError("Cet email est déjà utilisé.")
            
      
        cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, 'etudiant')
            """, (nom, email, password))

        user_id = cursor.lastrowid
        create_student(conn, user_id, matricule, nom, prenom, age, classe)

        conn.commit()

            
        print("Nouvel utilisateur créé")
        log_info(f"Etudiant ajouté : {matricule}, nom={nom} {prenom}")

    except ValueError as e:
        conn.rollback()
        log_error(str(e))
        print(f"[ERREUR] {e}")

    except sqlite3.IntegrityError:
        conn.rollback()
        msg = "Erreur base de données (doublon)"
        log_error(msg)
        print(f"[ERREUR] {msg}")

    finally:
        conn.close()



def modifier_etudiant(ancien, nom, prenom, age, classe, nouveau):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE students
            SET nom = ?, prenom = ?, age = ?, classe = ?, matricule = ?
            WHERE matricule = ?
        """, (nom, prenom, age, classe, nouveau, ancien))

        conn.commit()

        if cursor.rowcount == 0:
            msg = "Etudiant introuvable"
            print(f"[ERREUR] {msg}")
            log_error(msg)
        else:
            print("Etudiant modifié")
            log_info(f"Modification étudiant : {ancien} → {nouveau}")

    except Exception as e:
        conn.rollback()
        print(f"[ERREUR] {e}")
        log_error(str(e))

    finally:
        conn.close()



def supprimer_etudiant(matricule):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM students WHERE matricule = ?", (matricule,))
        conn.commit()

        if cursor.rowcount == 0:
            print("[ERREUR] Étudiant introuvable")
        else:
            print("Etudiant supprimé")
            log_info(f"Suppression étudiant : {matricule}")

    finally:
        conn.close()



def rechercher_etudiant(matricule):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, matricule, nom, prenom, age, classe
            FROM students
            WHERE matricule = ?
        """, (matricule,))

        etudiant = cursor.fetchone()

        if etudiant:
            log_info(
                f"Recherche étudiant : matricule={matricule}"
            )

        return etudiant

    finally:
        conn.close()



def lister_etudiants():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT user_id, matricule, nom, prenom, age, classe
            FROM students
            ORDER BY nom
        """)

        rows = cursor.fetchall()

        print("\n===== LISTE ÉTUDIANTS =====")
        print(f"Total: {len(rows)}\n")

        if not rows:
            print("[INFO] Aucun étudiant")
            return
        
        log_info(
            f"Affichage liste étudiants : total={len(rows)}"
        ) 

        for r in rows:
            print(f"ID:{r[0]} | Matricule:{r[1]} | Nom:{r[2]} | Prenom:{r[3]} | Age:{r[4]} | Classe:{r[5]}")

    finally:
        conn.close()


def menu_students():
    while True:
        print("\n===== MENU ETUDIANTS =====")
        print("1. Ajouter")
        print("2. Modifier")
        print("3. Supprimer")
        print("4. Rechercher")
        print("5. Lister")
        print("0. Retour")

        choix = input("Choix : ").strip()

        if choix == "1":
            nom = input("Nom : ")
            prenom = input("Prenom : ")
            age = input("Age : ")
            classe = input("Classe : ")
            matricule = input("Matricule : ")
            email = input("Email : ")
            password = input("Password : ")
            

            if not all([
                nom.strip(),
                prenom.strip(),
                age.strip(),
                classe.strip(),
                matricule.strip(),
                email.strip(),
                password.strip()
            ]):
                print("[ERREUR] Tous les champs doivent être remplis.")
                input("Appuyez sur entrée...")
                continue

            ajouter_etudiant(nom, prenom, age, classe, matricule, email, password)
            


        elif choix == "2":
            ancien = input("Ancien matricule : ")
            nom = input("Nom : ")
            prenom = input("Prenom : ")
            age = input("Age : ")
            classe = input("Classe : ")
            nouveau = input("Nouveau matricule : ")

            modifier_etudiant(ancien, nom, prenom, age, classe, nouveau)
            


        elif choix == "3":
            matricule = input("Matricule : ")
            supprimer_etudiant(matricule)
            


        elif choix == "4":
            matricule = input("Matricule : ")
            etudiant = rechercher_etudiant(matricule)

            if etudiant:
                print(etudiant)
            else:
                print("[INFO] Étudiant introuvable")
            

        elif choix == "5":
            print("\n LA LISTE DES ETUDIANTS")
            

        elif choix == "0":
            break

        else:
            print("Choix invalide")
        input("\nAppuyez sur Entrée pour continuer...")    