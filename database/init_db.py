from database.database import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    conn.execute("PRAGMA foreign_keys = ON") # activation des clés etrangères sqlite

    #NOT NULL = CHAMP OBLIGATOIRE
    #CHECK = CONTROLE DE CERTES VALEURS (NOTe, AGE, ROLE)
    #on delete = mieux gerer les suppressions
    cursor.executescript("""
    
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, 
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL 
            CHECK (role IN ('admin', 'professeur', 'etudiant'))
    );

    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        matricule TEXT NOT NULL UNIQUE ,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        age INTEGER NOT NULL
            CHECK(age > 0),
        classe TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );

     CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE
        
    );                    

    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        nom TEXT NOT NULL,    
        subject_id INTEGER NOT NULL,  
                         
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
                         
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
        
    );

    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        note REAL NOT NULL
            CHECK(note >= 0 AND note <= 20),
        FOREIGN KEY (student_id) REFERENCES students(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(id)   
            ON DELETE CASCADE
            ON UPDATE CASCADE           
    );

    CREATE TABLE IF NOT EXISTS absences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        statut TEXT NOT NULL
            CHECK(statut IN ('justifiee', 'non justifiee')),
        FOREIGN KEY (student_id) REFERENCES students(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );

    """)

    conn.commit()
    conn.close()