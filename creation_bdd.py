
import sqlite3

def creer_base_de_donnees():
    # Connexion à la base de données (elle sera créée si elle n'existe pas)
    conn = sqlite3.connect('ventes_magasin.db')
    cursor = conn.cursor()
    
    # Suppression des tables existantes (pour éviter les erreurs lors de la ré-exécution)
    cursor.execute("DROP TABLE IF EXISTS Ventes;")
    cursor.execute("DROP TABLE IF EXISTS Produits;")
    cursor.execute("DROP TABLE IF EXISTS Clients;")
    cursor.execute("DROP TABLE IF EXISTS Categories;")
    
    # Création de la table Categories
    cursor.execute("""
    CREATE TABLE Categories (
        id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_categorie TEXT NOT NULL,
        description TEXT
    );
    """)
    
    # Création de la table Produits
    cursor.execute("""
    CREATE TABLE Produits (
        id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_produit TEXT NOT NULL,
        id_categorie INTEGER,
        prix_unitaire REAL NOT NULL,
        cout_production REAL,
        stock_actuel INTEGER,
        FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
    );
    """)
    
    # Création de la table Clients
    cursor.execute("""
    CREATE TABLE Clients (
        id_client INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT,
        email TEXT,
        telephone TEXT,
        ville TEXT,
        date_inscription DATE,
        frequence_achat TEXT CHECK(frequence_achat IN ('Occasionnel', 'Regulier', 'Fidele'))
    );
    """)
    
    # Création de la table Ventes
    cursor.execute("""
    CREATE TABLE Ventes (
        id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produit INTEGER NOT NULL,
        id_client INTEGER,
        date_vente DATE NOT NULL,
        quantite INTEGER NOT NULL,
        montant_total REAL NOT NULL,
        mode_paiement TEXT CHECK(mode_paiement IN ('Carte', 'Especes', 'Virement', 'Cheque')),
        FOREIGN KEY (id_produit) REFERENCES Produits(id_produit),
        FOREIGN KEY (id_client) REFERENCES Clients(id_client)
    );
    """)
    
    # Validation des changements et fermeture de la connexion
    conn.commit()
    conn.close()
    print("Base de données créée avec succès!")

if __name__ == "__main__":
    creer_base_de_donnees()