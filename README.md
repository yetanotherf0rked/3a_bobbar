
Rules :

- Variables en anglais
- Classes démarre par une maj
- Constantes en maj
- _ pour sep
- Construction MVC

Todo :
- GUI & Paramètrabilité (on reste sur ThorPy, avec Qt c'est compliqué):
    - Scène initiale avec les paramètres avant de lancer les simus
    - Spliter l'écran en deux (à gauche : paramètres, à droite : simu)
        - problème du rafraichissement qui cache le menu : implémenter la simu dans un rect ??)
    - Faire des tests pour déterminer les valeurs limites acceptables par les variables
    - Paramètres initiaux (à choisir avant de lancer une simu)
        - Taille de la grille (resizable window)
        - Population initiale
        - Nombre de Ticks par jour
    - Paramètres modifiables en tps réel :
        - Carctéristiques initiales d'un bob
            - Energie de la mère
            - Energie du fils
            - Mémoire spatiale
            - Champ de vision
        - Coûts en énergie
            - en mouvement
            - en inertie
        - Alimentation
            - nombre de foods sur la grille
            - coût d'un food
        - Représentation spatiale
- Bilans de simulation (Louis)

Idées d'amélioration :
- Mettre des routes/chemins de fer ou autre, quand les bobs passent dessus ils accélèrent