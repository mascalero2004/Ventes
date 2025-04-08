
import sqlite3
import random
from datetime import datetime, timedelta
import numpy as np

# Fonctions utilitaires pour générer des données aléatoires
def random_date(start_date, end_date):
    """Génère une date aléatoire entre start_date et end_date"""
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

def random_email(nom, prenom):
    """Génère un email à partir du nom et prénom"""
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    return f"{prenom.lower()}.{nom.lower()}{random.randint(1, 99)}@{random.choice(domains)}"

def generer_donnees():
    conn = sqlite3.connect('ventes_magasin.db')
    cursor = conn.cursor()
    
    # Liste des catégories de produits
    categories = [
        ("Electronique", "Appareils électroniques et gadgets"),
        ("Vêtements", "Vêtements pour hommes, femmes et enfants"),
        ("Alimentation", "Produits alimentaires et boissons"),
        ("Maison", "Meubles et articles de décoration"),
        ("Sports", "Articles de sport et loisirs"),
        ("Beauté", "Produits de beauté et soins personnels"),
        ("Jardin", "Plantes et outils de jardinage"),
        ("Livre", "Livres et magazines"),
        ("Bébé", "Articles pour bébés"),
        ("Automobile", "Pièces et accessoires automobiles")
    ]
    
    # Insertion des catégories
    cursor.executemany("INSERT INTO Categories (nom_categorie, description) VALUES (?, ?)", categories)
    conn.commit()
    
    # Génération des produits (150 produits)
    produits = []
    noms_produits = {
        "Electronique": ["Smartphone", "Ordinateur portable", "Casque audio", "Tablette", "Montre connectée", 
                        "Enceinte Bluetooth", "Chargeur sans fil", "Câble USB", "Disque dur externe", "Clavier sans fil"],
        "Vêtements": ["T-shirt", "Jean", "Robe", "Veste", "Pull", 
                     "Chaussures", "Chaussettes", "Cravate", "Écharpe", "Short"],
        "Alimentation": ["Eau minérale", "Jus de fruits", "Céréales", "Pâtes", "Riz", 
                        "Chocolat", "Biscuits", "Café", "Thé", "Lait"],
        "Maison": ["Canapé", "Table", "Chaise", "Lampe", "Tapis", 
                  "Rideaux", "Coussin", "Vaisselle", "Casserole", "Verres"],
        "Sports": ["Ballon de foot", "Raquette de tennis", "Vélo", "Tapis de yoga", "Haltères", 
                  "Sac de sport", "Chaussures de running", "Maillot de bain", "Lunettes de natation", "Gourde"],
        "Beauté": ["Shampoing", "Gel douche", "Crème hydratante", "Parfum", "Déodorant", 
                  "Maquillage", "Brosse à cheveux", "Rasoir", "Vernis à ongles", "Masque visage"],
        "Jardin": ["Plante d'intérieur", "Tondeuse à gazon", "Pelle", "Râteau", "Arrosoir", 
                  "Pot de fleurs", "Gants de jardinage", "Engrais", "Brouette", "Sécateur"],
        "Livre": ["Roman", "BD", "Livre de cuisine", "Guide de voyage", "Dictionnaire", 
                 "Livre pour enfants", "Biographie", "Science-fiction", "Policier", "Fantasy"],
        "Bébé": ["Couches", "Biberon", "Poussette", "Lit bébé", "Jouet bébé", 
                "Tétine", "Bavoir", "Body", "Crème pour bébé", "Sac à langer"],
        "Automobile": ["Pneu", "Batterie", "Siège auto", "GPS", "Nettoyant vitres", 
                      "Câble de démarrage", "Huile moteur", "Antigel", "Balai d'essuie-glace", "Chargeur allume-cigare"]
    }
    
    for id_categorie in range(1, 11):
        categorie_nom = categories[id_categorie-1][0]
        for produit in noms_produits[categorie_nom]:
            prix = round(random.uniform(5, 500), 2)
            cout = round(prix * random.uniform(0.3, 0.7), 2)
            stock = random.randint(0, 100)
            produits.append((produit, id_categorie, prix, cout, stock))
    
    cursor.executemany("""
    INSERT INTO Produits (nom_produit, id_categorie, prix_unitaire, cout_production, stock_actuel)
    VALUES (?, ?, ?, ?, ?)
    """, produits)
    conn.commit()
    
    # Génération des clients (150 clients)
    noms = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau",
            "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier",
            "Morel", "Girard", "Andre", "Lefevre", "Mercier", "Dupont", "Lambert", "Bonnet", "Francois", "Martinez"]
    
    prenoms = ["Jean", "Pierre", "Paul", "Jacques", "Marie", "Anne", "Sophie", "Nathalie", "Thomas", "François",
              "Nicolas", "Christophe", "Patrick", "Michel", "Philippe", "Isabelle", "Sylvie", "Catherine", "Monique", "Valérie",
              "David", "Daniel", "Eric", "Olivier", "Christine", "Sandrine", "Caroline", "Stéphanie", "Alexandre", "Julien"]
    
    villes = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille",
             "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble", "Dijon", "Angers", "Nîmes", "Villeurbanne"]
    
    clients = []
    for i in range(150):
        nom = random.choice(noms)
        prenom = random.choice(prenoms)
        email = random_email(nom, prenom)
        telephone = f"0{random.randint(1,9)}{random.randint(10,99)}{random.randint(10,99)}{random.randint(10,99)}{random.randint(10,99)}"
        ville = random.choice(villes)
        date_inscription = random_date(datetime(2018, 1, 1), datetime(2022, 12, 31))
        frequence = random.choice(["Occasionnel", "Regulier", "Fidele"])
        clients.append((nom, prenom, email, telephone, ville, date_inscription.strftime('%Y-%m-%d'), frequence))
    
    cursor.executemany("""
    INSERT INTO Clients (nom, prenom, email, telephone, ville, date_inscription, frequence_achat)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, clients)
    conn.commit()
    
    # Génération des ventes (500 ventes)
    ventes = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    for _ in range(500):
        id_produit = random.randint(1, 150)
        id_client = random.randint(1, 150)
        date_vente = random_date(start_date, end_date)
        quantite = random.randint(1, 5)
        
        # Récupération du prix unitaire
        cursor.execute("SELECT prix_unitaire FROM Produits WHERE id_produit = ?", (id_produit,))
        prix_unitaire = cursor.fetchone()[0]
        
        # Calcul du montant total avec possibilité de petite réduction
        reduction = random.choice([0, 0, 0, 0, 0.05, 0.1])  # 20% chance de réduction
        montant_total = round(prix_unitaire * quantite * (1 - reduction), 2)
        
        mode_paiement = random.choice(["Carte", "Especes", "Virement", "Cheque"])
        
        ventes.append((id_produit, id_client, date_vente.strftime('%Y-%m-%d'), quantite, montant_total, mode_paiement))
    
    cursor.executemany("""
    INSERT INTO Ventes (id_produit, id_client, date_vente, quantite, montant_total, mode_paiement)
    VALUES (?, ?, ?, ?, ?, ?)
    """, ventes)
    conn.commit()
    
    # Fermeture de la connexion
    conn.close()
    print("Données générées avec succès!")

if __name__ == "__main__":
    generer_donnees()