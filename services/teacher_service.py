from database.database import get_connection
from models.teacher import Teacher
from utils.console import clear
from utils.logger import log_info, log_error
from utils.validator import valider_professeur

import sqlite3

def menu_teacher():
        while True :
            clear()

            print("\n  PROFESSEUR")
            print("1. Ajouter")
            print("2. Modifier")
            print("3. Supprimer")
            print("4. Rechercher")
            print("0. Quitter")
            
            choix = input("Choix : ").strip()

            if choix == "1":
               matiere = input("Matière : ")
               nom = input("Nom : ")
               
               professeur = Teacher(matiere, nom)
               ajouter_professeur(professeur)
               
               input("Appuyez sur entrée...")


            elif choix == "2":
                ancienne_matiere = input("Ancienne matière : ")
                nouvelle_matiere = input("Nouvelle matière : ")
                nom = input("Nouveau nom : ")
                
                professeur = Teacher (nouvelle_matiere, nom)


                modifier_professeur(ancienne_matiere, professeur)
                input("Appuyez sur entrée...")

            

            elif choix == "3":
                matiere = input("Matière: ")
                supprimer_professeur(matiere)
                input("Appuyez sur entrée...")
        

            elif choix == "4":
                matiere = input("Matière: ")
                professeur = rechercher_professeurs(matiere)

                if professeur:
                    print(f"""
                    Matière : {professeur[0]}
                    Nom : {professeur[1]}
                """)
                    
                else:
                    print("Aucun professeur trouvé.")

                input("Appuyez sur entrée...")
            
        

            elif choix == "0":
                print("Au revoir")
                input("Appuyez sur entrée...")
                break

            else: 
                print("Choix invalide")
                input("Appuyez sur Entrée...")



def ajouter_professeur(professeur):
    erreur = valider_professeur(professeur)
    if erreur:
        print(erreur)
        return
 
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO teachers
            (matiere, nom)
            VALUES (?, ?)
         """, (
            professeur.matiere,
            professeur.nom
        ))
    
             

        conn.commit()

        print("Professeur ajouté avec succès.")
        log_info(
        f"Professeur ajouté : {professeur.matiere}"
    )

    except sqlite3.IntegrityError:
        log_error(
            f"Ajout impossible : {professeur.matiere}"
        )
        print("Cette matière exixte déjà.")

    except Exception as e :
        log_error(
            f"Erreur ajout professeur : {e}"
        )
        print(f"Erreur : {e}")

    finally :
        conn.close()#ferme


def modifier_professeur( ancienne_matiere, professeur):
   
    if not ancienne_matiere:
        print("L'ancienne matière ne peut pas etre vide.")
        return

    erreur = valider_professeur(professeur)
    if erreur:
        print(erreur)
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE teachers
            SET matiere = ?, nom = ?
            WHERE matiere = ?
        """, (professeur.matiere, 
            professeur.nom,
            ancienne_matiere)
    )
        conn.commit()

        if cursor.rowcount == 0:
            print("Aucun professeur trouvé.")
            log_error(
                f"Modification impossible : {ancienne_matiere}"
        )
        else:
            print("Professeur modifié avec succès")
            log_error(
                f"Modification : {ancienne_matiere} -> {professeur.matiere}"
        )

    except sqlite3.IntegrityError :
        log_error(
            f"Modification refusée : {professeur.matiere}"
        )
        print("Cette matière existe")

    except Exception as e:
        log_error(
            f"Erreur modification professeur : {e}"
        )
        print(f"Erreur : {e}")

    finally:
        conn.close()



def supprimer_professeur(matiere):

    if not matiere:
        print("La matière ne peut pas être vide.") 
        return
    

    conn =get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute ("""
            DELETE FROM teachers
            WHERE matiere = ?
        """, (matiere,))

        conn.commit()

        if cursor.rowcount == 0:
            print("Auncun professeur trouvé.")
            log_error(
                f"Suppression impossible : ; {matiere}"
            )
        else:
            print("Professeur  supprimé")          
            log_info(
                f"Professeur supprimé : {matiere}"
                )
    except Exception as e :
        log_error(
            f"Erreur suppression : {e}"
        )
        print(f"Erreur : {e}")
    
    finally:
        conn.close()

    

def rechercher_professeurs(matiere):

    if not matiere: 
        print("La matière ne peut pas être vide.") 
        return None

    conn = get_connection()
    cursor = conn.cursor()

       
    try :
        cursor.execute("""
            SELECT * FROM teachers
            WHERE matiere = ?
        """, (matiere,))

        professeur = cursor.fetchone()
        
        if professeur:
            log_info(
                f"Recherche professeur : {matiere}"
            )

        return professeur
    
    except Exception as e:
        log_error(
            f"Erreur recherche professeur : {e}"
        )
        print("Une erreur est survenue.")
        return None
    
    finally:
        conn.close()



