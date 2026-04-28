Cahier des Charges : Projet Vie Artificielle (L2 IG)
Binôme : Yves AYIHOSSOU et John Carlos AÏGBEDE  
Date : 20 avril 2026
1. Présentation du projet
Notre équipe a choisi le Projet 2 : Simulateur d'Écosystème. L'objectif est de concevoir un univers virtuel sous forme de grille où des entités biologiques évoluent de manière autonome. Nous avons choisi de modéliser une savane où interagissent des prédateurs (Lions) et des proies(Zèbres).
2. Spécifications Fonctionnelles
Environnement : La simulation se déroule sur une grille 2D. Chaque case peut être vide ou occupée par un être vivant. L'environnement gère les limites de l'espace et les déplacements.
Cycle de vie :
Naissance : Les entités sont générées aléatoirement au début ou naissent par reproduction.
Énergie : Chaque entité possède un réservoir d'énergie qui diminue à chaque mouvement.
Mort : Une entité meurt si son énergie tombe à zéro ou si elle est mangée.
Interactions :
Alimentation : Le Lion gagne de l'énergie en consommant un Zèbre. Le Zèbre consomme des ressources végétales simulées sur la grille.
Reproduction : Deux entités de la même espèce sur des cases adjacentes peuvent procréer si leur niveau d'énergie est suffisant.
3. Spécifications Techniques et Contraintes
Langage : Python .
Architecture : Utilisation stricte de la Programmation Orientée Objet (POO).
Classe Mère EtreVivant : Gère la position, l'énergie et les fonctions vitales de base.
Héritage et Polymorphisme : Les classes Prédateur (Lion) et Proie (Zebre) héritent de la classe mère mais redéfinissent la méthode manger() pour illustrer leurs besoins spécifiques.
Gestion des versions : Utilisation obligatoire de Git. Le projet est hébergé sur GitHub pour assurer le travail collaboratif en binôme.
Qualité du code : Application rigoureuse des normes PEP 8. Le code doit être documenté et lisible.
Tests : Validation de la logique algorithmique (déplacements, calculs d'énergie) via des tests unitaires avec Pytest.
Environnement : Utilisation d'un environnement virtuel  pour la gestion des dépendances. Développement mobile facilité par Termux et Acode.
4. Organisation et Jalons (Sprints)
Jalon 1 (20/04/2026) - Bloc 1 : Finalisation du cahier des charges, initialisation du dépôt Git et définition de l'architecture de base.
Jalon 2 (22/04/2026) - Blocs 2 & 3 : Mise en place du Workflow collaboratif et développement de l'architecture POO (Classes et méthodes de base).
Jalon 3 (Dates suivantes) : Développement de l'interface de simulation, intégration des tests unitaires et préparation de la soutenance finale.
