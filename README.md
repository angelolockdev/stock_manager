Gestion de Stock avec Tkinter et SQLite3
Description

Ce projet est une application de gestion de stock simple, développée en Python avec une interface graphique Tkinter et une base de données SQLite3. Elle permet de gérer une liste de produits, d'ajouter des nouveaux produits, de simuler des achats et des ventes, et de générer des rapports de transactions par date.
Fonctionnalités

    Affichage de la liste des produits : Afficher les produits stockés dans la base de données avec leurs détails (nom, quantité, prix).
    Ajout de nouveaux produits : Ajouter un produit avec son nom, quantité et prix.
    Simulation d'achat et vente : Mise à jour du stock en fonction des achats et ventes.
    Génération de rapport par date : Générer un rapport des transactions (achats et ventes) sur une période donnée.

Architecture du Projet

Le projet est structuré selon le principe de la Programmation Orientée Objet (POO) et divisé en plusieurs dossiers pour une meilleure organisation.
Structure du projet

bash

stock_management/
│
├── main.py                # Point d'entrée principal de l'application.
├── requirements.txt       # Liste des dépendances Python.
│
├── controllers/           # Contient les classes qui contrôlent la logique de l'application.
│   └── stock_controller.py # Gère les interactions entre l'interface graphique et la base de données.
│
├── models/                # Contient les classes représentant les modèles de données.
│   ├── product.py         # Modèle Produit.
│   └── transaction.py     # Modèle Transaction.
│
├── views/                 # Contient les classes liées à l'interface graphique Tkinter.
│   └── stock_app.py       # Interface graphique et widgets Tkinter.
│
└── database/              # Contient la classe de gestion de la base de données.
    └── db_manager.py      # Gère les interactions avec SQLite3 (CRUD).

Détails des Dossiers et Fichiers

    main.py : Le point d'entrée du programme. Il initialise l'interface graphique en créant une instance de la classe StockApp qui se trouve dans le dossier views.

    controllers/ : Ce dossier contient la logique de l'application, représentée par le fichier stock_controller.py. Le contrôleur est responsable de la gestion des interactions entre l'interface utilisateur et la base de données, via des méthodes qui manipulent les produits et les transactions.

    models/ : Ce dossier contient les classes modèles qui définissent les entités utilisées dans l'application :
        product.py : Définit la classe Product pour représenter un produit (nom, quantité, prix).
        transaction.py : Définit la classe Transaction pour représenter une transaction (achat ou vente), avec la quantité et la date de la transaction.

    views/ : Ce dossier contient l'interface utilisateur construite avec Tkinter. Le fichier stock_app.py définit la fenêtre principale et tous les widgets (boutons, formulaires) nécessaires à l'interaction avec l'utilisateur.

    database/ : Ce dossier contient db_manager.py, une classe qui gère toutes les interactions avec la base de données SQLite. Cela inclut la création des tables, l'insertion de produits, la mise à jour des quantités de stock, et la génération de rapports de transactions.

Prérequis

    Python 3.x
    Tkinter (inclus dans les distributions Python standard)
    SQLite3 (inclus dans les distributions Python standard)

Installation

    Cloner le projet :

    bash

git clone https://github.com/username/stock_management.git
cd stock_management

Installer les dépendances (si nécessaire) :

bash

pip install -r requirements.txt

Exécuter le programme :

bash

    python main.py

Utilisation

    Ajouter un produit : Cliquez sur "Ajouter Produit", remplissez les champs requis et validez.
    Acheter un produit : Cliquez sur "Acheter Produit", entrez l'ID du produit et la quantité à acheter.
    Vendre un produit : Cliquez sur "Vendre Produit", entrez l'ID du produit et la quantité à vendre.
    Afficher la liste des produits : Cliquez sur "Afficher Produits" pour voir tous les produits.
    Générer un rapport : Cliquez sur "Générer Rapport", entrez une période de dates pour voir les transactions effectuées pendant cette période.

Contribuer

Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations, n'hésitez pas à soumettre une pull request.
Licence

Ce projet est sous licence MIT.