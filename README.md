# Monopooaly

Bienvenue sur le tutoriel du MonoPOOAly !

Vous pouvez jouer en local de 2 à 4 joueurs. Si vous souhaitez connaître les règles du Monopoly, c'est par [ici](http://www.regledujeu.fr/monopoly/).


####1. Comment installer le jeu ?

- Se placer dans le dossier de notre projet

- Exécuter la commande ci-dessous dans votre terminal
         
        pip install -r requirements.txt   
   
####2. Comment jouer ?

- Le jeu se lance depuis la console.

- La première étape : (fichier main.py) : exécuter la commande suivante dans le terminal. Vous avez accès à plusieurs scénarios :
un début de partie, une partie plus avancée et une partie proche de la fin. Taper le numéro correspondant à votre souhait.
Indiquer également le nombre de participants.

NB: Pour les scénarios "Partie en cours" et "Fin de partie", nous avons affecté des terrains et des propriétés par défaut et ces modes de jeu ne sont donc disponibles que pour deux joueurs. Il est en revanche possible de jouer jusque 4 joueurs, dans le scénario "Début de partie".

        python main.py

- La deuxième étape : (fichier client.py) : Lancer dans des terminaux différents autant de fichiers client.py qu'il y a de joueurs.
    Une fois les clients lancés, renseigner le nom de chaque joueur.

        python client.py

- Des fenêtres Pygame (une par joueur) s'ouvrent et le jeu peut commencer. Vous pouvez jouer directement sur ces fenêtres sans retourner dans votre terminal. 

####3. Quelles sont les notions abordées en cours présentes dans notre projet ?

- Classes et hérédités


- Architecture client / serveur

    Le serveur est lancé lors de l'exécution du fichier main.py. Les clients sont lancés lors de l'exécution du fichier
    client.py. L'ensemble des calculs sont réalisés côté serveur et les résultats sont envoyé via une socket au client
    concerné. Côté client, on affiche via pygame les instructions et on capture les actions des joueurs.

- Multithreading



Nous vous souhaitons des parties endiablées sur notre jeu !

L'équipe MonoPOOAly
Hortense, Rémi et Antoine