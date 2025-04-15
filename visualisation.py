# scripts/04_visualisation_complete.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Configuration de style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
sns.set_palette("husl")

def formatter_euros(x, pos):
    """Formate les nombres en euros"""
    return f'€{x:,.0f}'

def generate_visualizations():
    # Connexion à la base de données
    conn = sqlite3.connect('ventes_magasin.db')
    
    # ==============================================
    # VISUALISATIONS OBLIGATOIRES (ÉTAPE 5 DU TP)
    # ==============================================

    # 1. Évolution temporelle des ventes (Graphique en courbe)
    print("Génération des visualisations obligatoires...")
    query_ca_mensuel = """
    SELECT strftime('%Y-%m', date_vente) as mois, 
           SUM(montant_total) as ca_total,
           COUNT(id_vente) as nb_ventes
    FROM Ventes
    GROUP BY strftime('%Y-%m', date_vente)
    ORDER BY mois
    """
    df_mois = pd.read_sql_query(query_ca_mensuel, conn)
    
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    ax1.plot(df_mois['mois'], df_mois['ca_total'], 
            marker='o', linestyle='-', color='b', label='CA Total')
    ax1.set_title("Évolution mensuelle des ventes", fontsize=18, pad=20)
    ax1.set_xlabel("Mois", fontsize=12)
    ax1.set_ylabel("Chiffre d'affaires (€)", fontsize=12, color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.yaxis.set_major_formatter(FuncFormatter(formatter_euros))
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    ax2 = ax1.twinx()
    ax2.plot(df_mois['mois'], df_mois['nb_ventes'], 
            marker='s', linestyle='--', color='r', label='Nombre de ventes')
    ax2.set_ylabel("Nombre de ventes", fontsize=12, color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('1_evolution_mensuelle.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Répartition des ventes par produit (Diagramme en secteurs)
    query_top_produits = """
    SELECT p.nom_produit, 
           SUM(v.montant_total) as ca_total,
           SUM(v.quantite) as quantite_totale
    FROM Ventes v
    JOIN Produits p ON v.id_produit = p.id_produit
    GROUP BY p.nom_produit
    ORDER BY ca_total DESC
    LIMIT 5
    """
    top_produits = pd.read_sql_query(query_top_produits, conn)
    
    plt.figure(figsize=(10, 8))
    explode = (0.05, 0, 0, 0, 0)
    plt.pie(top_produits['ca_total'], 
            labels=top_produits['nom_produit'], 
            autopct=lambda p: f'{p:.1f}%\n(€{p*sum(top_produits["ca_total"])/100:,.0f})',
            startangle=90,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 10})
    plt.title("Répartition du CA par produit (Top 5)", fontsize=16, pad=20)
    plt.savefig('2_repartition_produits.png', dpi=300, bbox_inches='tight')
    plt.show()


    query_top_produits = """
    SELECT p.nom_produit, 
           SUM(v.montant_total) as ca_total,
           SUM(v.quantite) as quantite_totale
    FROM Ventes v
    JOIN Produits p ON v.id_produit = p.id_produit
    GROUP BY p.nom_produit
    ORDER BY ca_total DESC
    LIMIT 5
    """
    top_produits = pd.read_sql_query(query_top_produits, conn)
    
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=top_produits, x='ca_total', y='nom_produit', 
                         hue='nom_produit', legend=False, palette='viridis')
    plt.title("Top 5 des produits par chiffre d'affaires", fontsize=16, pad=20)
    plt.xlabel("Chiffre d'affaires (€)", fontsize=12)
    plt.ylabel("Produit", fontsize=12)
    barplot.xaxis.set_major_formatter(FuncFormatter(formatter_euros))
    
    for index, value in enumerate(top_produits['ca_total']):
        barplot.text(value, index, f'€{value:,.0f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('3_top5_produits.png', dpi=300, bbox_inches='tight')
    plt.show()

    
    # ==============================================
    # HEATMAP CORRIGÉE (VERSION À GARDER)
    # ==============================================
    query_heatmap = """
    SELECT 
        strftime('%w', date_vente) as jour_semaine,
        strftime('%H', date_vente) as heure,
        COUNT(id_vente) as nb_ventes
    FROM Ventes
    GROUP BY jour_semaine, heure
    ORDER BY jour_semaine, heure
    """
    df_heatmap = pd.read_sql_query(query_heatmap, conn)

    df_heatmap['nb_ventes'] = pd.to_numeric(df_heatmap['nb_ventes'])
    df_heatmap['jour_semaine'] = pd.to_numeric(df_heatmap['jour_semaine'])
    df_heatmap['heure'] = pd.to_numeric(df_heatmap['heure'])

    jours = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    pivot_table = df_heatmap.pivot_table(values='nb_ventes', 
                                    index='heure', 
                                    columns='jour_semaine', 
                                    fill_value=0)
    pivot_table = pivot_table.reindex(range(0, 24))

    plt.figure(figsize=(16, 10))
    sns.heatmap(
        pivot_table,
        cmap='YlOrRd',
        annot=True,
        fmt='g',
        annot_kws={'size': 8, 'color': 'black'},
        linewidths=0.3,
        linecolor='grey',
        cbar_kws={'label': 'Nombre de ventes'},
        vmin=0,
        vmax=pivot_table.max().max()
    )

    plt.title('VENTES PAR HEURE ET JOUR (Données Réelles)', fontsize=18, pad=20)
    plt.xlabel('Jour de semaine', fontsize=14)
    plt.ylabel('Heure de la journée', fontsize=14)
    plt.xticks(ticks=range(7), labels=jours, rotation=45, ha='right')
    plt.yticks(ticks=range(0, 24, 2), labels=[f"{h}:00" for h in range(0, 24, 2)], rotation=0)

    ax = plt.gca()
    ax.add_patch(plt.Rectangle((0, 0), 1, 24, fill=False, edgecolor='blue', lw=2, linestyle='--'))  # Dimanche
    ax.add_patch(plt.Rectangle((1, 0), 1, 24, fill=False, edgecolor='blue', lw=2, linestyle='--'))  # Lundi

    plt.tight_layout()
    plt.savefig('4_heatmap_ventes_corrigee.png', dpi=300, bbox_inches='tight')
    plt.show()

    # ==============================================
    # ANALYSE DES CLIENTS
    # ==============================================
    query_clients = """
    SELECT 
        c.frequence_achat,
        COUNT(v.id_vente) as nb_achats,
        SUM(v.montant_total) as ca_total,
        AVG(v.montant_total) as panier_moyen
    FROM Ventes v
    JOIN Clients c ON v.id_client = c.id_client
    GROUP BY c.frequence_achat
    """
    df_clients = pd.read_sql_query(query_clients, conn)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    sns.barplot(data=df_clients, x='frequence_achat', y='nb_achats', ax=axes[0])
    axes[0].set_title('Nombre de transactions', fontsize=14)
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Nombre d\'achats')
    
    sns.barplot(data=df_clients, x='frequence_achat', y='ca_total', ax=axes[1])
    axes[1].set_title('Chiffre d\'affaires total', fontsize=14)
    axes[1].set_xlabel('')
    axes[1].set_ylabel('CA total (€)')
    axes[1].yaxis.set_major_formatter(FuncFormatter(formatter_euros))
    
    sns.barplot(data=df_clients, x='frequence_achat', y='panier_moyen', ax=axes[2])
    axes[2].set_title('Panier moyen', fontsize=14)
    axes[2].set_xlabel('')
    axes[2].set_ylabel('Montant moyen (€)')
    
    plt.suptitle('Analyse des ventes par type de client', fontsize=16, y=1.05)
    plt.tight_layout()
    plt.savefig('5_analyse_clients.png', dpi=300, bbox_inches='tight')
    plt.show()

    try:
            query_top_clients = """
            SELECT c.nom, 
                SUM(v.montant_total) as ca_total,
                COUNT(v.id_vente) as nb_achats
            FROM Ventes v
            JOIN Clients c ON v.id_client = c.id_client
            GROUP BY c.nom
            ORDER BY ca_total DESC
            LIMIT 5
            """
            top_clients = pd.read_sql_query(query_top_clients, conn)
            
            plt.figure(figsize=(10, 6))
            barplot = sns.barplot(data=top_clients, x='ca_total', y='nom', 
                                hue='nom', legend=False, palette='rocket')
            plt.title("Top 5 des clients par chiffre d'affaires", fontsize=16, pad=20)
            plt.xlabel("Chiffre d'affaires (€)", fontsize=12)
            plt.ylabel("Client", fontsize=12)
            barplot.xaxis.set_major_formatter(FuncFormatter(formatter_euros))
            
            for index, value in enumerate(top_clients['ca_total']):
                barplot.text(value, index, f'€{value:,.0f}', ha='left', va='center', fontsize=10)
            
            plt.tight_layout()
            plt.savefig('6_top5_clients.png', dpi=300, bbox_inches='tight')
            plt.show()
    except Exception as e:
            print(f"Erreur lors de la génération du graphique des clients: {str(e)}")
    
    conn.close()
    print("Visualisations générées avec succès")
    

if __name__ == "__main__":
    generate_visualizations()
