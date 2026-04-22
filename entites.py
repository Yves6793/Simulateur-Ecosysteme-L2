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
        self.role = "Prédateur"
    def manger(self, cible):
        if self.x == cible.x and self.y == cible.y:
            if isinstance(cible, Proie) and cible.est_vivant:
                print(f" Le {self.role} mange la proie .")
                self.energie += cible.energie  
                cible.est_vivant = False       
                cible.energie = 0
            else:
                print("Rien à manger ici ou la proie est déjà morte.")
        else:
            print("Trop loin pour manger !")

class Proie(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Proie"


if __name__ == "__main__":
    print("============= CONFIGURATION DE LA SIMULATION ============")
    
    
    print("\n-------- Paramètres du Lion --------")
    lx = int(input("Position X du Lion : "))
    ly = int(input("Position Y du Lion : "))
    le = int(input("Énergie initiale du Lion : "))
    lion = Predateur(x=lx, y=ly, energie=le)

    print("\n-------- Paramètres du Zèbre --------")
    zx = int(input("Position X du Zèbre : "))
    zy = int(input("Position Y du Zèbre : "))
    ze = int(input("Énergie initiale du Zèbre : "))
    zebre = Proie(x=zx, y=zy, energie=ze)

    print("\n")
    print("="*30)
    print("-------- SITUATION INITIALE --------")
    print(f" Lion : Position ({lion.x},{lion.y}), Énergie: {lion.energie}")
    print(f" Zèbre : Position ({zebre.x},{zebre.y}), Énergie: {zebre.energie}")
    print("="*30)

    print("\n-------- ACTION : Tentative de chasse --------")
    lion.manger(zebre)

    print("\n-------- RÉSULTAT APRÈS ACTION --------")
    print(f" Lion : Position ({lion.x},{lion.y}), Énergie: {lion.energie}")
    print(f" Zèbre : Vivant ? {zebre.est_vivant}, Énergie restante: {zebre.energie}")