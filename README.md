🎬 Guide d'Utilisation de Netflix Checker
🚀 Prérequis

assurez-vous d'avoir tout le nécessaire :

    Python 3.x
    Vérifiez son installation avec :

    bash

python --version

Bibliothèques Requises
Installez les bibliothèques indispensables via pip :

bash

    pip install requests selenium colorama

    WebDriver pour Firefox
    Téléchargez GeckoDriver et assurez-vous qu'il est accessible dans votre PATH.

🏁 Étapes pour Exécuter le Script

    Téléchargez le Script
    Clonez le dépôt GitHub ou téléchargez le fichier directement.

    Ouvrez votre Terminal
    Naviguez jusqu'au dossier contenant le script.

    Lancez le Script
    Exécutez la commande suivante :

    bash

python netflixchecker.py

Vérification de Version
Le script vérifiera automatiquement s'il existe une mise à jour. Si oui, il la téléchargera et relancera le script.

Sélectionnez le Fichier combo.json
Une fenêtre de dialogue apparaîtra. Choisissez le fichier contenant les identifiants à tester, structuré comme ceci :

json

    [
        {"email": "user1@example.com", "password": "password1"},
        {"email": "user2@example.com", "password": "password2"}
    ]

    Vérification des Identifiants
    Le script tentera de se connecter à Netflix avec les identifiants fournis en utilisant les proxies configurés. Les résultats de chaque tentative s'afficheront dans le terminal.

    Fin de la Vérification
    Une fois toutes les tentatives effectuées, le script affichera un message de fin.

⚙️ Résolution des Problèmes

    Erreur de Téléchargement
    Vérifiez votre connexion Internet et l'accessibilité du lien.

    Fichier JSON Vide
    Assurez-vous que le fichier contient des données valides.

    Échec de Connexion
    Vérifiez l'exactitude des identifiants et la fonctionnalité des proxies.

🔒 Remarques

    Sécurité : Soyez vigilant lors du test des identifiants pour des services en ligne. Respectez les conditions d'utilisation de Netflix.

    Utilisation des Proxies : La liste des proxies est modifiable dans le code si nécessaire.

Si vous avez besoin de plus d'informations ou d'autres ajustements, n'hésitez pas à me contacter sur Discord !
