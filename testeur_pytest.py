import random
from entites import Predateur, Proie, saisir

def test_aleatoire():
    print("\n --- MODE TEST ALÉATOIRE ---")

    lx, ly = random.randint(0, 20), random.randint(0, 20)
    zx, zy = random.randint(0, 20), random.randint(0, 20)
    
 
    lion = Predateur(lx, ly, 50)
    zebre = Proie(zx, zy, 20)
    
    print(f"Lion placé en ({lx}, {ly}) avec 50 d'énergie.")
    print(f"Zèbre placé en ({zx}, {zy}) avec 20 d'énergie.")
    
    print("\nAction : Tentative de chasse.")
    lion.manger(zebre)
    
    if not zebre.est_vivant:
        print("Résultat : Le lion a réussi sa chasse !")
    else:
        print(" Résultat : Le zèbre est trop loin, il a survécu.")

def test_manuel():
    print("\n --- MODE RÉCUPÉRATION DES DONNÉES (MANUEL) ---")
    
    lx = saisir("Position X du Lion : ")
    ly = saisir("Position Y du Lion : ")
    le = saisir("Énergie du Lion : ")
    lion = Predateur(lx, ly, le)
    
    zx = saisir("Position X du Zèbre : ")
    zy = saisir("Position Y du Zèbre : ")
    ze = saisir("Énergie du Zèbre : ")
    zebre = Proie(zx, zy, ze)
    
    print("\nAction : Simulation avec vos données...")
    lion.manger(zebre)
    
    if not zebre.est_vivant:
        print(" Résultat : Capture réussie !")
    else:
        print("Résultat : Échec de la capture.")

if __name__ == "__main__":
    print("============================================")
    print("      MODULE DE TEST - ÉCOSYSTÈME L2        ")
    print("============================================")
    print("1. Lancer un test ALÉATOIRE")
    print("2. SAISIR manuellement les données")
    
    
    choix = saisir("\nVotre choix (1 ou 2) : ")
    
    if choix == 1:
        test_aleatoire()
    elif choix == 2:
        test_manuel()
    else:
        print("Choix invalide. Veuillez relancer le testeur.")