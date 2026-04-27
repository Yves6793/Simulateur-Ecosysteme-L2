import sqlite3
import os

class EtreVivant(object):
    def __init__(self, x, y, energie):
        self.x = x
        self.y = y
        self.energie = energie
        self.est_vivant = True

    def se_deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        self.energie -= 1
        if self.energie <= 0:
            self.est_vivant = False

class Predateur(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Lion"

    def manger(self, cible):
        if self.x == cible.x and self.y == cible.y:
            if isinstance(cible, Proie) and cible.est_vivant:
                print(f" Le {self.role} mange la proie.")
                self.energie += cible.energie  
                cible.est_vivant = False       
                cible.energie = 0
            else:
                print("Rien à manger ici ou la proie est déjà morte.")
        else:
            print("Trop loin pour manger ")

class Proie(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Zèbre"


def saisir(message):
        while True:
            try:
                valeur = int(input(message))
                return valeur
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier vlide (ex:10)")


def initialiser_bdd():
    conn = sqlite3.connect('ecosysteme.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            x INTEGER,
            y INTEGER,
            energie INTEGER,
            est_vivant INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def sauvegarder_simulation(lion, zebre):
    conn = sqlite3.connect('ecosysteme.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entites')
    for animal in [lion, zebre]:
        cursor.execute('''
            INSERT INTO entites (role, x, y, energie, est_vivant)
            VALUES (?, ?, ?, ?, ?)
        ''', (animal.role, animal.x, animal.y, animal.energie, 1 if animal.est_vivant else 0))
    conn.commit()
    conn.close()

def charger_simulation():
    if not os.path.exists('ecosysteme.db'):
        return None
    conn = sqlite3.connect('ecosysteme.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, x, y, energie FROM entites')
    lignes = cursor.fetchall()
    conn.close()
    if not lignes: return None
    
    entites = []
    for l in lignes:
        role, x, y, energie = l
        if role == "Lion":
            entites.append(Predateur(x, y, energie))
        else:
            entites.append(Proie(x, y, energie))
    return entites



if __name__ == "__main__":
    initialiser_bdd()
    
    sauvegarde = charger_simulation()
    
    print("============= CONFIGURATION DE LA SIMULATION ============")
    
    choix = 'n'
    if sauvegarde:
        choix = input("Une sauvegarde existe. La charger ? (o/n) : ").lower()

    if choix == 'o':
        lion, zebre = sauvegarde[0], sauvegarde[1]
    else:
        print("\n-------- Paramètres du Lion --------")
        lx = saisir("Position X du Lion : ")
        ly = saisir("Position Y du Lion : ")
        le = saisir("Énergie initiale du Lion : ")
        lion = Predateur(lx, ly, le)

        print("\n-------- Paramètres du Zèbre --------")
        zx = saisir("Position X du Zèbre : ")
        zy = saisir("Position Y du Zèbre : ")
        ze = saisir("Énergie initiale du Zèbre : ")
        zebre = Proie(zx, zy, ze)

    print("\n\n==============================")
    print("-------- SITUATION INITIALE --------")
    print(f" Lion : Position ({lion.x},{lion.y}), Énergie: {lion.energie}")
    print(f" Zèbre : Position ({zebre.x},{zebre.y}), Énergie: {zebre.energie}")
    print("==============================\n")

  
    lion.manger(zebre)

    print("\n-------- RÉSULTAT APRÈS ACTION --------")
    print(f" Lion : Position ({lion.x},{lion.y}), Énergie: {lion.energie}")
    print(f" Zèbre : Vivant ? {zebre.est_vivant}, Énergie restante: {zebre.energie}")

  
    sauvegarder_simulation(lion, zebre)