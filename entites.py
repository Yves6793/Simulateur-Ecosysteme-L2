import sqlite3
import os
import webbrowser
import time
import random

class EtreVivant:
    def __init__(self, x, y, energie):
        self.x = x
        self.y = y
        self.energie = energie
        self.est_vivant = True

    def se_deplacer(self, dx, dy):
        if not self.est_vivant: return
        self.x += dx
        self.y += dy
        self.energie -= 1
        print(f"    Deplacement vers ({self.x}, {self.y}). Energie restante : {self.energie}")
        if self.energie <= 0:
            self.est_vivant = False
            print(f"    L'entite en ({self.x},{self.y}) est morte d'epuisement.")

    def afficher_etat(self):
        statut = "Vivant" if self.est_vivant else "Mort"
        print(f"    {self.role} Pos: ({self.x},{self.y}) | Energie: {self.energie} | {statut}")

class Predateur(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Lion"

    def chasser(self, cible):
        if not self.est_vivant:
            print("    Le Lion est mort, il ne peut plus chasser.")
            return False
      
        if self.x == cible.x and self.y == cible.y:
            if isinstance(cible, Proie) and cible.est_vivant:
                print(f"    ALERTE Le Lion a intercepte le Zebre en ({self.x}, {self.y}) et l'a mange")
                self.energie += cible.get_apport_nutritif()
                cible.mourir()
                return True
            else:
                print("    La cible est deja morte ou absente.")
        else:
            print(f"    Le Lion n'a pas pu manger le Zebre.")
            print(f"    Le Zebre est toujours en vie en ({cible.x}, {cible.y}).")
        
        return False

class Proie(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Zebre"

    def brouter(self):
        if self.est_vivant:
            gain = 5
            self.energie += gain
            print(f"    Le Zebre broute paisiblement. Gain d'energie : +{gain} (Total: {self.energie})")
        else:
            print("    Un zebre mort ne peut plus brouter.")

    def se_reproduire(self):
        """Logique de reproduction : cree un nouveau zebre si l'energie est suffisante."""
        if self.est_vivant and self.energie >= 15:
            self.energie -= 7  # Coût énergétique de la reproduction
            # Le petit naît à une position proche
            nouvel_x = self.x + random.randint(-1, 1)
            nouvel_y = self.y + random.randint(-1, 1)
            nouveau_zebre = Proie(nouvel_x, nouvel_y, 10)
            print(f"    REPRODUCTION : Un nouveau zebre est ne en ({nouvel_x}, {nouvel_y}) !")
            return nouveau_zebre
        return None

    def get_apport_nutritif(self):
        return self.energie

    def mourir(self):
        self.est_vivant = False
        self.energie = 0


def saisir(message):
    while True:
        try:
            valeur = int(input(message))
            if valeur < 0: raise ValueError
            return valeur
        except ValueError:
            print(" Erreur : Entrez un nombre entier positif.")

def gerer_bdd(lion, zebre, action):
    conn = sqlite3.connect('ecosysteme.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS simulation 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       lion_e INTEGER, zebre_e INTEGER, action TEXT)''')
    cursor.execute("INSERT INTO simulation (lion_e, zebre_e, action) VALUES (?, ?, ?)",
                   (lion.energie, zebre.energie, action))
    conn.commit()
    conn.close()

def lancer_interface():
    print("\nINTERFACE : Analyse des donnees terminee. Lancement du dashboard...")
    time.sleep(1)
    chemin = os.path.abspath("templates/index.html")
    if os.path.exists(chemin):
        webbrowser.open(f"file:///{chemin}")
    else:
        print(" Erreur : Fichier templates/index.html non trouve.")


if __name__ == "__main__":
    print(" ========== CONFIGURATION DE LA SIMULATION ========== \n")
    print("\n       SIMULATEUR ECOSYSTEM")
    print("       Yves AYIHOSSOU & Carlos AIGBEDE \n")
    print("="*50)

    print("\n-------- PHASE 1 : CONFIGURATION --------")
    lx = saisir("Position X du Lion : ")
    ly = saisir("Position Y du Lion : ")
    le = saisir("Energie initiale du Lion : ")
    lion = Predateur(lx, ly, le)
    
    zx = saisir("Position X du Zebre : ")
    zy = saisir("Position Y du Zebre : ")
    ze = saisir("Energie initiale du Zebre : ")
 
    troupeau = [Proie(zx, zy, ze)]

    print("\n-------- PHASE 2 : ACTIONS DANS LA SAVANE --------\n")
    lion.afficher_etat()
    for z in troupeau:
        z.afficher_etat()
    
    print("\nAction 1 : Le troupeau broute et se reproduit")
    nouveaux_nes = []
    for z in troupeau:
        z.brouter()
        bebe = z.se_reproduire()
        if bebe:
            nouveaux_nes.append(bebe)
    troupeau.extend(nouveaux_nes) 
    
    print("\nAction 2 : Deplacement du Lion")
    dx = saisir("Deplacement X du Lion pour chasser : ")
    dy = saisir("Deplacement Y du Lion pour chasser : ")
    lion.se_deplacer(dx, dy)
    
    print("\nAction 3 : Chasse")
    
    succes = lion.chasser(troupeau[0])
    
    msg = "Chasse reussie" if succes else "La proie a survecu"
    gerer_bdd(lion, troupeau[0], msg)
    
    print("\n-------- RESULTAT FINAL --------")
    lion.afficher_etat()
    print(f"Nombre de zebres dans la savane : {len([z for z in troupeau if z.est_vivant])}")
    for z in troupeau:
        if z.est_vivant:
            z.afficher_etat()
    
    lancer_interface()