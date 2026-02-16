# Quête 10 : Analyse de Performance et Visualisation Graphique

## Objectifs de la quête
- [x] Installer les outils de monitoring (`sysstat`) et de stress test (`stress`).
- [x] Générer un fichier de logs SAR sous charge.
- [x] Développer un script Python pour parser la colonne `%idle` et stocker les données.
- [x] Générer un graphique (image PNG) montrant l'effondrement du `%idle` lors du stress.

---

## 1. Préparation de l'environnement

Nous avons besoin de trois composants : `sysstat` pour capturer les données, `stress` pour simuler une surcharge CPU, et `matplotlib` pour dessiner le graphique.

### Installation
```bash
sudo apt update
sudo apt install sysstat stress python3-pip -y
pip install matplotlib
(Note : Si pip n'est pas installé : sudo apt install python3-matplotlib fonctionne aussi et est souvent plus simple sur Linux).

2. Génération des Données (Le Scénario)
Nous allons créer un scénario en 3 temps :

Calme (5 sec) : Le serveur ne fait rien.

Tempête (10 sec) : On lance stress pour saturer les CPU.

Calme (5 sec) : On arrête le stress.

Pendant ce temps, sar va écrire les statistiques dans un fichier texte toutes les secondes.

Procédure de capture
Ouvrez deux terminaux.

Dans le Terminal 1 (Capture) :
Lancez la commande suivante. Elle va enregistrer l'activité processeur (-u) toutes les 1 seconde pendant 20 secondes et écrire le résultat dans cpu_log.txt.

Bash
sar -u 1 20 > cpu_log.txt
Dans le Terminal 2 (Simulation de charge) :
Attendez environ 5 secondes après avoir lancé la commande précédente, puis lancez :

Bash
stress --cpu 4 --timeout 10
(Ceci va lancer 4 processus qui calculent des racines carrées en boucle pendant 10 secondes).

Résultat :
Une fois terminé, vous avez un fichier cpu_log.txt. Vérifiez son contenu avec cat cpu_log.txt. Vous devriez voir la colonne %idle (tout à droite) passer de ~99.00 à ~0.00 puis remonter.

3. Le Script : Analyseur et Traceur (plot_perf.py)
Ce script va lire le fichier texte, nettoyer les données (attention aux virgules vs points décimaux selon la langue du système), et générer une image.

Code Source
Python
import matplotlib.pyplot as plt
import sys

def analyser_sar(fichier_source):
    timestamps = []
    idle_values = []

    print(f"--- Analyse du fichier {fichier_source} ---")

    try:
        with open(fichier_source, 'r') as f:
            lines = f.readlines()

            # On parcourt chaque ligne du fichier
            for line in lines:
                # On saute les lignes vides ou les en-têtes (qui contiennent "CPU" ou "Linux")
                if "CPU" in line or "Linux" in line or line.strip() == "":
                    continue
                
                # On saute la ligne de "Moyenne" à la fin du fichier
                if "Moyenne" in line or "Average" in line:
                    continue

                # Découpage de la ligne par les espaces
                parts = line.split()

                # Sécurité : une ligne valide de SAR a au moins 3 colonnes (Heure, CPU, ... Idle)
                if len(parts) > 3:
                    try:
                        # 1. Récupération de l'heure (1ère colonne)
                        time_val = parts[0]
                        
                        # 2. Récupération du %idle (Dernière colonne)
                        raw_idle = parts[-1] 
                        
                        # ASTUCE : Gestion de la locale (Virgule vs Point)
                        # En français, SAR écrit "99,00", Python veut "99.00"
                        clean_idle = raw_idle.replace(',', '.')
                        
                        idle_float = float(clean_idle)

                        # Stockage dans nos listes
                        timestamps.append(time_val)
                        idle_values.append(idle_float)
                        
                    except ValueError:
                        # Si la conversion échoue, on ignore la ligne
                        continue

        return timestamps, idle_values

    except FileNotFoundError:
        print(f"Erreur : Le fichier {fichier_source} est introuvable.")
        sys.exit(1)

def generer_graphique(x, y):
    print("--- Génération du graphique ---")
    
    # Création de la figure
    plt.figure(figsize=(10, 6)) # Taille de l'image (10x6 pouces)
    
    # Tracé de la courbe
    # color='red' : ligne rouge
    # marker='o' : points sur la ligne
    plt.plot(x, y, color='tab:red', marker='o', linestyle='-', label='% Idle (Inactivité)')

    # Ajout de titres et labels
    plt.title('Impact du Stress Test sur l\'inactivité CPU (%idle)')
    plt.xlabel('Temps (HH:MM:SS)')
    plt.ylabel('% Idle (0 = Surchargé, 100 = Repos)')
    
    # Ajout d'une grille pour la lisibilité
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotation des étiquettes de temps pour qu'elles ne se chevauchent pas
    plt.xticks(rotation=45)
    
    # Légende
    plt.legend()
    
    # Ajustement automatique des marges
    plt.tight_layout()

    # Sauvegarde dans un fichier (indispensable sur serveur sans écran)
    nom_image = "analyse_cpu.png"
    plt.savefig(nom_image)
    print(f"[+] Graphique sauvegardé sous : {nom_image}")

if __name__ == "__main__":
    fichier = "cpu_log.txt"
    temps, idle = analyser_sar(fichier)
    
    if len(temps) > 0:
        print(f"Données extraites : {len(temps)} points.")
        generer_graphique(temps, idle)
    else:
        print("Aucune donnée valide trouvée dans le fichier.")
4. Exécution et Résultats
Lancez le script :

Bash
python3 plot_perf.py
Récupération de l'image :
Le script a généré analyse_cpu.png.

Si vous êtes sur une VM avec interface graphique, ouvrez le fichier.

Si vous êtes en SSH, vous devez récupérer le fichier sur votre machine hôte (via scp ou un dossier partagé) pour le voir.

Interprétation du graphique :
Vous devriez observer une courbe en forme de "cuvette" (U) inversée ou normale selon le point de vue :

Début : La courbe est haute (~100% idle) -> Le serveur se repose.

Milieu : La courbe chute brutalement (~0% idle) -> Le serveur souffre (stress).

Fin : La courbe remonte (~100% idle) -> Le stress est fini.