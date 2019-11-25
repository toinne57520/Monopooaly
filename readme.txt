Bienvenue sur le tutoriel du MonoPOOAly !

Vous pouvez jouer en local de 2 à 4 joueurs. Si vous souhaitez connaître les règles du Monopoly, n'hésitez pas à consulter le fichier pdf : regles.pdf

1) Comment jouer ?

Le jeu se lance depuis la console.

La première étape : (fichier main.py)

    Lancer le fichier main.py et suivre les instructions sur la console.

La deuxième étape : (fichier client.py)

    Lancer dans la console autant de fichiers client.py qu'il y a de joueurs.
    Une fois les clients lancés, renseigner le nom de chaque joueur et suivre les indications à l'écran.




2) Quelles sont les notions abordées en cours présentes dans notre projet ?

- Classes et hérédités



- Architecture client / serveur

    Le serveur est lancé lors de l'exécution du fichier main.py. Les clients sont lancés lors de l'exécution du fichier
    client.py. L'ensemble des calculs sont réalisés côté serveur et les résultats sont envoyé via une socket au client
    concerné. Côté client, on affiche via pygame les instructions et on capture les actions des joueurs.

- Multithreading


On vous souhaite de bonnes parties endiablées sur notre jeu !

L'équipe MonoPOOAly
Hortense, Rémi et Antoine