# Quête 7 : Interception des Signaux Système (Graceful Shutdown)

## Objectifs de la quête
- [x] Importer le module `signal` pour gérer les interruptions système.
- [x] Créer une boucle infinie simulant un programme longue durée (daemon/serveur).
- [x] Définir une fonction de "callback" pour intercepter `SIGINT` (CTRL-C) et quitter proprement.

---

## 1. Comprendre les Signaux

Un **signal** est une notification envoyée par le système d'exploitation à un processus pour lui indiquer qu'un événement s'est produit.

* **SIGINT (Signal Interrupt) :** Envoyé lorsqu'un utilisateur tape `CTRL+C` dans le terminal.
* **Comportement par défaut :** Python lève une exception `KeyboardInterrupt` qui arrête brutalement le script et affiche une "Traceback" (message d'erreur rouge).

Pour créer des outils professionnels, nous devons "attraper" ce signal pour exécuter une procédure de fermeture propre (sauvegarde des données, fermeture des fichiers logs, déconnexion des sockets).

---

## 2. Le Script : Gestionnaire d'Interruption (`clean_exit.py`)

Nous allons créer un programme qui tourne à l'infini jusqu'à ce qu'on lui demande d'arrêter. Au lieu de planter, il affichera un message personnalisé avant de quitter.

### Code Source

```python
import signal
import sys
import time

def gestionnaire_signal(sig, frame):
    """
    Fonction exécutée UNIQUEMENT quand le signal est reçu.
    :param sig: Le numéro du signal reçu (ici 2 pour SIGINT).
    :param frame: L'état de la pile d'exécution au moment de l'interruption.
    """
    print("\n\n[!] Interruption détectée (CTRL-C).")
    print("[*] Nettoyage des fichiers temporaires...")
    print("[*] Fermeture des connexions...")
    print("[*] Arrêt propre du programme. Au revoir !")
    
    # On force la sortie du programme avec le code 0 (Succès)
    sys.exit(0)

# 1. Enregistrement du signal
# On dit à Python : "Si tu reçois SIGINT, n'arrête pas tout, lance 'gestionnaire_signal' à la place."
signal.signal(signal.SIGINT, gestionnaire_signal)

print("--- Programme en cours d'exécution (Appuyez sur CTRL-C pour arrêter) ---")

# 2. Boucle Infinie (Simulation d'un serveur ou d'un processus long)
compteur = 0
while True:
    print(f"Traitement en cours... {compteur}")
    compteur += 1
    
    # Pause de 1 seconde pour ne pas surcharger le processeur
    time.sleep(1)