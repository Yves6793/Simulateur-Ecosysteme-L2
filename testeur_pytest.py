import random
from entites import Predateur, Proie

def saisir(message):
    
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier.")

def mode_aleatoire():
    print("\n--------- MODE ALEATOIRE ACTIVE --------")
    lx, ly = random.randint(0, 5), random.randint(0, 5)
    zx, zy = random.randint(0, 5), random.randint(0, 5)
    le, ze = 15, 10
    print(f"Lion genere en ({lx}, {ly}) | Zebre genere en ({zx}, {zy})")
    
    lion = Predateur(lx, ly, le)
    zebre = Proie(zx, zy, ze)
    
    dx, dy = random.randint(-1, 1), random.randint(-1, 1)
    print(f"Mouvement automatique du Lion : dx={dx}, dy={dy}")
    return lion, zebre, dx, dy

def mode_manuel():
    print("\n-------- MODE SAISIE UTILISATEUR ACTIVE --------")
    
    lx = saisir("Position X du Lion : ")
    ly = saisir("Position Y du Lion : ")
    le = saisir("Energie initiale du Lion : ")
    
    zx = saisir("Position X du Zebre : ")
    zy = saisir("Position Y du Zebre : ")
    ze = saisir("Energie initiale du Zebre : ")
    
    lion = Predateur(lx, ly, le)
    zebre = Proie(zx, zy, ze)
    
    print("\nPositions actuelles :")
    lion.afficher_etat()
    zebre.afficher_etat()

    print("\n--------- SAISIE DU MOUVEMENT ---------")
    print(f"Rappel : Le Zebre est en ({zebre.x}, {zebre.y})")
    dx = saisir("Entrez dx (deplacement X) pour le Lion : ")
    dy = saisir("Entrez dy (deplacement Y) pour le Lion : ")
    
    return lion, zebre, dx, dy

def executer_test():

    print("1. Lancer une simulation ALEATOIRE")
    print("2. Lancer une simulation MANUELLE")
    choix = input("\nVotre choix (1 ou 2) : ")
    
    if choix == "1":
        lion, zebre, dx, dy = mode_aleatoire()
    else:
        lion, zebre, dx, dy = mode_manuel()

    print("\n-------- EXECUTION DES ACTIONS --------")
    zebre.brouter()
    lion.se_deplacer(dx, dy)

    print("\n-------- PHASE DE CHASSE --------")
    succes = lion.chasser(zebre)
    
    print("\n--------- BILAN FINAL --------")
    if succes:
        print("RESULTAT : REUSSITE - Le Lion a mange le Zebre ")
    else:
        print("RESULTAT : ECHEC - Le Zebre est toujours en vie.")
    
    lion.afficher_etat()
    zebre.afficher_etat()

if __name__ == "__main__":
    executer_test()