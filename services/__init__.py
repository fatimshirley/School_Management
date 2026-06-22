from database.database import get_connection

def login():
    print("\n===== CONNEXION =====")

    email = input("Email : ").strip()
    password = input("Mot de passe : ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nom, email, role
        FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"\nBienvenue {user[1]} ({user[3]})")
        return {
            "id": user[0],
            "nom": user[1],
            "email": user[2],
            "role": user[3]
        }

    print("Email ou mot de passe incorrect.")
    return None