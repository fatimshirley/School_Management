from database.database import get_connection
from utils.logger import log_info, log_error

def login():

    while True:
        print("\n===== SYSTEME DE GESTION D'ECOLE =====")
        print("1. Se connecter")
        print("2. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "2":
            return None

        elif choix == "1":

            print("\n===== CONNEXION =====")

            email = input("Email : ").strip()
            password = input("Mot de passe : ").strip()

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, email, role
                FROM users
                WHERE email = ? AND password = ?
            """, (email, password))

            user = cursor.fetchone()
            conn.close()

            if user:

                if user[3] == "etudiant":

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        SELECT matricule
                        FROM students
                        WHERE user_id = ?
                    """, (user[0],))

                    resultat = cursor.fetchone()
                    conn.close()

                    matricule = resultat[0] if resultat else "inconnu"

                    log_info(
                        f"Connexion étudiant : nom={user[1]}, matricule={matricule}, email={user[2]}"
                    )

                else:

                    log_info(
                        f"Connexion : nom={user[1]}, email={user[2]}, role={user[3]}"
                    )

                print(f"\nBienvenue {user[1]} ({user[3]})")

                return {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "role": user[3]
                }

            print("Email ou mot de passe incorrect.")
            log_error(
                 f"Tentative de connexion échouée : {email}"
            )

        else:
            print("Choix invalide.")