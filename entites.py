import sqlite3
import os
import time
import webbrowser

class EtreVivant(object):
    def __init__(self, x, y, energie):
        self.x, self.y, self.energie = x, y, energie
        self.age = 0
        self.est_vivant = True

    def se_deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        self.energie -= 1
        if self.energie <= 0: self.est_vivant = False

    def vieillir(self) -> None:
        self.age += 1
        self.energie -= 1
        if self.energie <= 0: self.est_vivant = False

class Predateur(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Lion"

    def manger(self, cible):
        print(f"\n[ANALYSE] Tentative d'interaction à la position ({self.x},{self.y})...")
        time.sleep(1) 
        if self.x == cible.x and self.y == cible.y:
            if isinstance(cible, Proie) and cible.est_vivant:
                print(f" >>> SUCCESS: Le {self.role} a capturé la proie !")
                self.energie += cible.energie  
                cible.est_vivant = False       
                cible.energie = 0
                return f"SUCCÈS : Le {self.role} a mangé le {cible.role}."
            else:
                return "ÉCHEC : Cible introuvable ou déjà morte."
        else:
            return "ÉCHEC : Distance trop grande pour chasser."

class Proie(EtreVivant):
    def __init__(self, x, y, energie):
        super().__init__(x, y, energie)
        self.role = "Zèbre"

# --- BLOC 5 : QUALITÉ & SÉCURITÉ ---
def saisir_securise(message):
    """Gère les exceptions de saisie (Bloc 5)."""
    while True:
        try:
            valeur = int(input(message))
            if valeur < 0:
                print("Veuillez entrer un nombre positif.")
                continue
            return valeur
        except ValueError:
            print("Erreur : Entrez un entier valide (chiffres uniquement).")

class TestsQualite:
    """Tests unitaires pour valider la logique POO (Bloc 5)."""
    @staticmethod
    def lancer_tests():
        print("\n[TESTS] Vérification des systèmes...")
        # Test de prédation
        l = Predateur(1, 1, 10)
        z = Proie(1, 1, 5)
        l.manger(z)
        assert l.energie == 15, "Erreur de calcul d'énergie"
        assert z.est_vivant is False, "Erreur de statut de la proie"
        print("[TESTS] Logique de combat : OK")
        print("[TESTS] Tous les tests ont réussi !\n")

# --- BLOC 4 : PERSISTANCE ---
def initialiser_bdd():
    conn = sqlite3.connect('ecosysteme.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS entites 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, x INTEGER, y INTEGER, energie INTEGER, est_vivant INTEGER)''')
    conn.commit()
    conn.close()

def sauvegarder_simulation(lion, zebre):
    conn = sqlite3.connect('ecosysteme.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entites')
    for animal in [lion, zebre]:
        cursor.execute('''INSERT INTO entites (role, x, y, energie, est_vivant) 
                         VALUES (?, ?, ?, ?, ?)''', (animal.role, animal.x, animal.y, animal.energie, 1 if animal.est_vivant else 0))
    conn.commit()
    conn.close()
    print("\n[SYSTÈME] Données synchronisées avec ecosysteme.db")

# --- BLOC 6 : INTERFACE & LIVRAISON ---
def generer_rapport(lion, zebre, message_log):
    chemin_modele = os.path.join("templates", "index.html")
    if not os.path.exists(chemin_modele):
        print(f"\n[ERREUR] Modèle introuvable dans {chemin_modele}")
        return

    with open(chemin_modele, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Remplacement dynamique
    remplacements = {
        "{{MESSAGE}}": message_log,
        "{{LION_X}}": str(lion.x),
        "{{LION_Y}}": str(lion.y),
        "{{LION_ENERGIE}}": str(lion.energie),
        "{{ZEBRE_X}}": str(zebre.x),
        "{{ZEBRE_Y}}": str(zebre.y),
        "{{ZEBRE_ENERGIE}}": str(zebre.energie),
        "{{ZEBRE_STATUS}}": "VIVANT" if zebre.est_vivant else "MORT",
        "{{ZEBRE_CLASS}}": "alive" if zebre.est_vivant else "dead"
    }

    for balise, valeur in remplacements.items():
        contenu = contenu.replace(balise, valeur)

    with open("resultat.html", "w", encoding="utf-8") as f:
        f.write(contenu)
    
    print("[VUE] Rapport 'resultat.html' généré.")
    webbrowser.open("file://" + os.path.realpath("resultat.html"))

# --- EXÉCUTION PRINCIPALE ---
if __name__ == "__main__":
    initialiser_bdd()
    
    # Lancement automatique des tests du Bloc 5
    TestsQualite.lancer_tests()

    print("="*50)
    print("      MONITEUR D'ÉCOSYSTÈME - UNIVERSITY OF PARAKOU")
    print("="*50)

    print("\n--- CONFIGURATION DES ENTITÉS ---")
    lx = saisir_securise("Position X Lion : ") 
    ly = saisir_securise("Position Y Lion : ") 
    le = saisir_securise("Energie Lion : ")
    lion = Predateur(lx, ly, le)  
    
    
    zx = saisir_securise("Position X Zèbre : ")
    zy = saisir_securise("Position Y Zèbre : ") 
    ze = saisir_securise("Energie Zèbre : ")
    zebre = Proie(zx, zy, ze)

    log_action = lion.manger(zebre)

    print("\n" + "="*50)
    print("              BILAN DE L'OPÉRATION")
    print("="*50)
    print(f"STATUT LION  : {'VIVANT' if lion.est_vivant else 'MORT'} | ÉNERGIE: {lion.energie}")
    print(f"STATUT ZÈBRE : {'VIVANT' if zebre.est_vivant else 'MORT'} | ÉNERGIE: {zebre.energie}")
    
    sauvegarder_simulation(lion, zebre)
    generer_rapport(lion, zebre, log_action)