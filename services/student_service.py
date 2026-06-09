from database.database import get_connection #fonction appelée, ouvrant une connexion avec la db sqlite
from models.student import Student
from utils.console import clear
from utils.validator import valider_etudiant
from utils.logger import log_info, log_error
#connexion à la db; import de la fonction get_connection

import sqlite3


def menu_students():
        while True :
            clear()

            print("\n  ETUDIANTS")
            print("1. Ajouter")
            print("2. Modifier")
            print("3. Supprimer")
            print("4. Rechercher")
            print("5. Lister")
            print("0. Quitter")
            
            choix = input("Choix : ").strip()#supprime les espaces inutiles

            if choix == "1":
               matricule = input("Matricule : ")
               nom = input("Nom : ")
               prenom = input("Prenom : ")
               age = input("Age : ")
               classe = input("Classe : ")

               etudiant = Student(matricule, nom, prenom, age, classe)
               ajouter_etudiant(etudiant)
               input("Appuyez sur entrée...")


            elif choix == "2":
                ancien_matricule = input("Ancien matricule : ")
                nouveau_matricule = input("Nouveau matricule : ")
                nom = input("Nouveau nom : ")
                prenom = input("Nouveau prénom : ")
                age = input("Nouvel age : ")
                classe = input("Nouvelle classe : ")

                etudiant = Student (
                    nouveau_matricule,
                    nom,
                    prenom,
                    age,
                    classe
                )

                modifier_etudiant(ancien_matricule, etudiant)
                input("Appuyez sur entrée...")

            

            elif choix == "3":
                matricule = input("Matricule : ")
                supprimer_etudiant(matricule)
                input("Appuyez sur entrée...")
        

            elif choix == "4":
                matricule = input("Matricule : ")
                etudiant = rechercher_etudiant(matricule)

                if etudiant:
                    print(f"""
                          Matricule : {etudiant[0]}
                          Nom       : {etudiant[1]}
                          Prénom    : {etudiant[2]}
                          Age       : {etudiant[3]}
                          Classe    : {etudiant[4]}
                        """) 
                else:
                    print("Aucun étudiant ne correspond à ce matricule.")

                input("Appuyez sur entrée...")
            
            

            elif choix == "5":
                print("\n LA LISTE DES ETUDIANTS")
                lister_etudiants()
                input("Appuyez sur entrée...")
            
        

            elif choix == "0":
                print("Retour au menu principal")
                input("Appuyez sur entrée...")
                break

            else: 
                print("Choix invalide")
                input("Appuyez sur Entrée...")



def ajouter_etudiant(etudiant):

    erreur = valider_etudiant(etudiant)
    if erreur : 
        print(erreur)
        return
    
    conn = get_connection() #conn, consideré comme un cable reliant mon programme à la db
    cursor = conn.cursor() #cursor sert à envoyer des cmd sql à la db; sans cursor, on ne peut pas executer de requetes sql

    
    try:  #essaie d'executer le bloc de code suivant
        cursor.execute("""
            INSERT INTO students
            (matricule, nom, prenom, age, classe)
            VALUES (?, ?, ?, ?, ?)
        """, (
            etudiant.matricule, 
            etudiant.nom, 
            etudiant.prenom, 
            etudiant.age, 
            etudiant.classe
            ))
        
        conn.commit()#sauvegarde
        print("Etudiant ajouté avec succès")
        log_info(f"Etudiant ajouté : {etudiant.matricule}")

    except sqlite3.IntegrityError:
        log_error(f"Ajout impossible : matricule {etudiant.matricule} déjà existant")
        print("Erreur: Ce matricule existe déjà.")

    except Exception as e: #except: intercepte les erreurs; #exception: represente presque toutes les erreurs python
        log_error(f"Erreur ajout étudiant : {e}")
        print(f"Une erreur est survenue : {e} ")

    finally: #execute ce bloc de quoi qu'il arrive
        conn.close()#ferme la connexion avec la db
    




def modifier_etudiant(ancien_matricule, etudiant):

    if not ancien_matricule:
        print("L'ancien matricule ne peut pas être vide.")
        return

    erreur = valider_etudiant(etudiant)
    if erreur:
        print(erreur)
        return

    conn = get_connection()
    cursor = conn.cursor()


    try:
        cursor.execute("""
            UPDATE students
            SET matricule = ?,
                nom = ?,
                prenom = ?,
                age = ?,
                classe = ?
            WHERE matricule = ?
        """, (
            etudiant.matricule,
            etudiant.nom,
            etudiant.prenom,
            etudiant.age,
            etudiant.classe,
            ancien_matricule
        ))

        conn.commit()

        if cursor.rowcount == 0:
            log_error(
               f"Modification impossible : {ancien_matricule} introuvable"
            )
            print("Aucun étudiant trouvé.")
        else:
            print("Étudiant modifié avec succès.")
            log_info(
                f"Modification étudiant : {ancien_matricule} -> {etudiant.matricule}"
            )
      
    except sqlite3.IntegrityError:
            log_error(
                f"Modification refusée : {etudiant.matricule} existe déjà"
            )
            print("Ce nouveau matricule existe déjà.")


    except Exception as e:
            log_error(f"Erreur modification étudiant : {e}")
            print(f"Erreur : {e}")

    finally:
        conn.close()

   

def supprimer_etudiant(matricule):

    if not matricule:
        print("Le matricule ne peut pas etre vide.")
        return
    
    conn =get_connection()
    cursor = conn.cursor()


    try:
        cursor.execute ("""
        DELETE FROM students
        WHERE matricule = ?
    """, (matricule,))
    
        conn.commit()
        
        if cursor.rowcount == 0:
            log_error(
                f"Suppression impossible : {matricule} introuvable"
            )
            print("Aucun étudiant trouvé.")
        else:
            log_info(f"Etudiant supprimé : {matricule}")
            print("Etudiant supprimé avec succès.")

            
    except Exception as e:
        log_error(f"Erreur suppression étudiant : {e}")
        print(f"Impossible de supprimer cet étudiant : {e}")

    finally:
        conn.close()

    

    

def rechercher_etudiant(matricule):

    if not matricule:
        print("Le matricule ne peut pas être vide.")
        return None
    
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT matricule, nom, prenom, age, classe
            FROM students
            WHERE matricule = ?
        """, (matricule,))
        
        etudiant = cursor.fetchone ()
        if etudiant:
            log_info(f"Recherche étudiant : {matricule}")

        return etudiant
    


    except Exception as e:
        log_error(f"Erreur recherche étudiant : {e}")
        print("Une erreur est survenue pendant la recherche.")
        return None

    finally:
        conn.close()


def lister_etudiants():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT matricule, nom, prenom, age, classe
             FROM students
         """)
                       
        rows = cursor.fetchall() #fetchall récupère toutes les lignes du résultat et les mets dans une liste.
     
        if not rows:
            print("La liste des étudiants est vide")
        else :
            for row in rows:
                print(f"""
                      Matricule : {row[0]}
                      Nom       : {row[1]}
                      Prénom    : {row[2]}
                      Age       : {row[3]}
                      Classe    : {row[4]}

                    """)

    except Exception as e:
        log_error(f"Erreur affichage liste étudiants : {e}")
        print("Impossible d'afficher la liste des étudiants")
    
    finally:
        conn.close()



