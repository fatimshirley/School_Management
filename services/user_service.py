from database.database import get_connection

ROLES = ["admin", "professeur", "etudiant"]

def ajouter_user(id, name, role):
    if role in ROLES:
        print("role invalide")
        return
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""""
        INSERT INTO users
        (id, name, role)
        VALUES(?, ?, ?)    
        """,
        (id, name, role)
    )
 
    conn.commit()
    conn.close()


def supprimer_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM users 
        WHERE id = ?, name = ?, role = ?
                   
    """,
    (user_id,)
    )

    conn.commit()
    conn.close()


def lister_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall

    conn.close()
    return rows
    