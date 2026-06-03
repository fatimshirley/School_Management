from database.database import get_connection
#connexion à la db; import de la fonction get_connection


def ajouter_etudiant(matricule, nom, prenom, age, classe):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (matricule, nom, prenom, age, classe)
        VALUES (?, ?, ?, ?, ?)
    """, (matricule, nom, prenom, age, classe))

    conn.commit()#sauvegarde
    conn.close()#ferme


def modifier_etudiant(matricule, nom, prenom, age, classe):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET nom = ?, prenom =?, classe = ?
        WHERE id = ?
    """, (matricule, nom, prenom, age, classe)
    )

    conn.commit()
    conn.close()



def supprimer_etudiant():
    conn =get_connection()
    cursor = conn.cursor()

    cursor.execute (""""
        DELETE FROM students
        WHERE matricule = ?, 
              nom = ?, 
              prenom =?,
                    classe = ?  
        """)
    conn.commit()
    conn.close()

    

def rechercher_etudiant(matricule):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE matricule = ?
    """, (matricule,))

    etudiant = cursor.fetchone()

    conn.close()

    return etudiant


def lister_etudiants():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows :
        print(row)
    conn.close()



