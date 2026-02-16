# Quête 12 : Création et Gestion de Processus (Multiprocessing)

## Objectifs de la quête
- [x] Utiliser le module `multiprocessing` pour lancer plusieurs processus indépendants.
- [x] Faire générer un nombre aléatoire par chaque processus et simuler une activité longue.
- [x] Identifier les processus créés via la commande système `ps` dans un terminal séparé.
- [x] Implémenter une fermeture propre des processus pour libérer les ressources.

---

## 1. Le Concept : Processus vs Thread

Un **Processus** est une instance d'un programme en cours d'exécution. Il possède son propre PID et son espace mémoire isolé. Si un processus plante, il n'affecte pas les autres (contrairement aux threads).

Pour observer des processus en temps réel, ils doivent rester "vivants" assez longtemps. Nous allons donc utiliser une pause (`time.sleep`) pour nous laisser le temps de taper la commande `ps`.

---

## 2. Le Script : Générateur de Processus (`proc_manager.py`)

Ce script va lancer 5 processus enfants. Chaque enfant va afficher son identifiant système (PID) pour que vous puissiez le retrouver.

### Code Source

```python
import multiprocessing
import random
import time
import os
import sys

def worker_task(nom):
    """
    Fonction exécutée par chaque processus enfant.
    """
    # Récupération du PID (Process ID) actuel
    pid = os.getpid()
    
    # Génération d'un nombre aléatoire
    nombre = random.randint(1000, 9999)
    
    print(f"[+] Processus '{nom}' démarré (PID: {pid}) - Nombre généré : {nombre}")
    
    # Simulation d'une tâche longue (60 secondes) pour permettre l'observation
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        # Permet de gérer l'arrêt si on tue le processus manuellement
        pass
        
    print(f"[-] Processus '{nom}' (PID: {pid}) terminé.")

def main():
    print("--- Démarrage du Gestionnaire de Processus ---")
    print(f"[*] PID du processus Père (Main) : {os.getpid()}")
    
    process_list = []
    nb_processus = 5

    # 1. Création et Démarrage des processus
    for i in range(nb_processus):
        # On crée l'objet Process
        p = multiprocessing.Process(target=worker_task, args=(f"Ouvrier-{i+1}",))
        process_list.append(p)
        
        # On le démarre (ceci appelle la fonction worker_task)
        p.start()

    print(f"\n[*] {nb_processus} processus lancés.")
    print("[*] VITE ! Ouvrez un autre terminal et tapez : ps -fC python3")
    print("[*] Appuyez sur ENTRÉE ici pour arrêter proprement les processus...")
    
    # Le script père attend que l'utilisateur appuie sur Entrée
    input()

    # 2. Nettoyage (Fermeture propre)
    print("\n--- Nettoyage en cours ---")
    for p in process_list:
        if p.is_alive():
            print(f"[*] Arrêt forcé du processus {p.name} (PID: {p.pid})...")
            p.terminate() # Envoie un signal SIGTERM au processus
            p.join()      # Attend que le processus soit bien mort

    print("--- Tous les processus sont fermés. Fin du programme. ---")

if __name__ == "__main__":
    # Protection indispensable pour le multiprocessing (surtout sous Windows/macOS)
    main()
3. Observation et Analyse
Cette partie nécessite d'être rapide ou d'avoir deux fenêtres de terminal ouvertes côte à côte.

Étape 1 : Lancer le script (Terminal A)
Bash
python3 proc_manager.py
Sortie :

Plaintext
--- Démarrage du Gestionnaire de Processus ---
[*] PID du processus Père (Main) : 12345
[+] Processus 'Ouvrier-1' démarré (PID: 12346) - Nombre généré : 8542
[+] Processus 'Ouvrier-2' démarré (PID: 12347) - Nombre généré : 1290
...
[*] VITE ! Ouvrez un autre terminal...
Étape 2 : Espionner avec ps (Terminal B)
Pendant que le script attend, tapez la commande suivante dans le second terminal :

Bash
ps -fC python3
Ou si la commande -C n'est pas dispo sur votre Linux : ps aux | grep python3

Résultat attendu :
Vous allez voir une liste de processus Python.

UID : L'utilisateur qui a lancé le script.

PID : L'identifiant unique. Vous devriez retrouver les PID affichés dans le Terminal A.

PPID (Parent PID) : C'est le plus intéressant ! Regardez la colonne PPID des processus "Ouvriers". Elle doit correspondre au PID du "Père" (12345 dans l'exemple ci-dessus). Cela prouve la hiérarchie des processus.

Étape 3 : Nettoyage
Retournez dans le Terminal A et appuyez sur ENTRÉE.

Sortie :

Plaintext
--- Nettoyage en cours ---
[*] Arrêt forcé du processus Process-1 (PID: 12346)...
[*] Arrêt forcé du processus Process-2 (PID: 12347)...
--- Tous les processus sont fermés. Fin du programme. ---