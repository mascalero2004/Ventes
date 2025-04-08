import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analyser_ventes():
    # Connexion à la base de données
    conn = sqlite3.connect('ventes_magasin.db')
    
    # 1. Extraction des données dans des DataFrames Pandas
    # Requête pour obtenir les données de ventes avec les noms des produits et clients
    query = """
    SELECT 
        v.id_vente,
        v.date_vente,
        p.nom_produit,
        p.prix_unitaire,
        c.nom as nom_client,
        c.prenom as prenom_client,
        v.quantite,
        v.montant_total,
        v.mode_paiement,
        cat.nom_categorie
    FROM Ventes v
    JOIN Produits p ON v.id_produit = p.id_produit
    LEFT JOIN Clients c ON v.id_client = c.id_client
    JOIN Categories cat ON p.id_categorie = cat.id_categorie
    """
    
    ventes_df = pd.read_sql_query(query, conn)
    
    # Conversion de la date en type datetime
    ventes_df['date_vente'] = pd.to_datetime(ventes_df['date_vente'])
    
    # 2. Analyse statistique de base
    print("\n=== Statistiques de base ===")
    print(f"Nombre total de ventes: {len(ventes_df)}")
    print(f"Chiffre d'affaires total: {ventes_df['montant_total'].sum():.2f}€")
    print(f"Montant moyen par vente: {ventes_df['montant_total'].mean():.2f}€")
    print(f"Quantité moyenne par vente: {ventes_df['quantite'].mean():.2f} articles")
    
    # 3. Analyse par produit
    print("\n=== Analyse par produit ===")
    produits_ca = ventes_df.groupby('nom_produit').agg({
        'quantite': 'sum',
        'montant_total': 'sum'
    }).sort_values('montant_total', ascending=False)
    
    print("\nTop 10 des produits par chiffre d'affaires:")
    print(produits_ca.head(10))
    
    # 4. Analyse par catégorie
    print("\n=== Analyse par catégorie ===")
    categories_ca = ventes_df.groupby('nom_categorie').agg({
        'quantite': 'sum',
        'montant_total': ['sum', 'count']
    }).sort_values(('montant_total', 'sum'), ascending=False)
    
    print("\nChiffre d'affaires par catégorie:")
    print(categories_ca)
    
    # 5. Analyse temporelle
    print("\n=== Analyse temporelle ===")
    ventes_df['mois'] = ventes_df['date_vente'].dt.to_period('M')
    ca_mensuel = ventes_df.groupby('mois').agg({
        'montant_total': 'sum',
        'id_vente': 'count'
    }).rename(columns={'montant_total': 'CA_total', 'id_vente': 'nb_ventes'})
    
    print("\nChiffre d'affaires mensuel:")
    print(ca_mensuel)
    
    # 6. Analyse des clients
    print("\n=== Analyse des clients ===")
    clients_df = pd.read_sql_query("SELECT * FROM Clients", conn)
    ventes_client = ventes_df.groupby(['nom_client', 'prenom_client']).agg({
        'montant_total': 'sum',
        'id_vente': 'count'
    }).sort_values('montant_total', ascending=False).rename(columns={
        'montant_total': 'CA_total', 
        'id_vente': 'nb_achats'
    })
    
    print("\nTop 10 des clients par chiffre d'affaires:")
    print(ventes_client.head(10))
    
    # Fermeture de la connexion
    conn.close()
    
    return ventes_df, produits_ca, categories_ca, ca_mensuel, ventes_client

if __name__ == "__main__":
    ventes_df, produits_ca, categories_ca, ca_mensuel, ventes_client = analyser_ventes()
    
    # Sauvegarde des résultats dans des fichiers CSV pour la visualisation
    produits_ca.to_csv('produits_ca.csv')
    categories_ca.to_csv('categories_ca.csv')
    ca_mensuel.to_csv('ca_mensuel.csv')
    ventes_client.to_csv('ventes_client.csv')
    
    print("\nAnalyse terminée. Les résultats ont été sauvegardés dans le dossier .")