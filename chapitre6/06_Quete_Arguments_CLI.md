# Quête 6 : Création d'une Interface CLI Professionnelle

## Objectifs de la quête
- [x] Utiliser le module `argparse` pour analyser les commandes de l'utilisateur.
- [x] Implémenter 3 arguments (Cible, Port, Mode Verbeux) avec options courtes/longues.
- [x] Transmettre les arguments analysés (le dictionnaire d'objets) à une fonction de traitement.

---

## 1. Pourquoi `argparse` plutôt que `sys.argv` ?

`sys.argv` découpe simplement la commande en une liste de chaînes. Si l'utilisateur oublie un argument ou se trompe d'ordre, le script plante.
**`argparse`** est beaucoup plus puissant :
* Il génère automatiquement l'aide (`-h`).
* Il gère les types (convertit automatiquement "80" en entier `80`).
* Il gère les valeurs par défaut.
* Il gère les erreurs proprement.



---

## 2. Le Script : Scanner CLI (`cli_tool.py`)

Nous allons simuler un outil de scan réseau. Le script va parser (analyser) les entrées, stocker les choix de l'utilisateur dans un objet, puis passer cet objet à une fonction `main` pour exécution.

### Code Source

```python
import argparse

def executer_scan(arguments):
    """
    Fonction qui reçoit le paquet d'arguments et simule l'action.
    """
    print("\n--- Démarrage du processus ---")
    
    # On accède aux arguments par leur nom défini dans le parser (dest)
    print(f"[*] Cible verrouillée : {arguments.target}")
    
    if arguments.verbose:
        print(f"[*] Mode verbeux ACTIVÉ : Affichage des détails techniques...")
        print(f"[*] Protocole utilisé : TCP Standard")
    
    print(f"[*] Scan du port {arguments.port} en cours...")
    
    # Simulation de résultat
    print(f"[+] Le port {arguments.port} sur {arguments.target} est OUVERT.")
    print("--- Fin du processus ---\n")

if __name__ == "__main__":
    # 1. Création de l'objet Parser
    # description : Ce qui s'affiche quand on tape --help
    parser = argparse.ArgumentParser(
        description="Outil de scan réseau avancé - Formation Python"
    )

    # 2. Ajout des arguments
    
    # Argument 1 : La Cible (Chaîne de caractères, Obligatoire)
    parser.add_argument(
        "-t", "--target",       # Option courte et longue
        type=str,               # Type attendu
        required=True,          # L'utilisateur DOIT le fournir
        help="Adresse IP ou nom de domaine de la cible."
    )

    # Argument 2 : Le Port (Entier, Optionnel avec valeur par défaut)
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=80,             # Si non précisé, ce sera 80
        help="Port cible à scanner (Défaut: 80)."
    )

    # Argument 3 : Mode Verbeux (Flag booléen)
    # action="store_true" signifie : si l'argument est présent, la variable vaut True. Sinon False.
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Active l'affichage détaillé des opérations."
    )

    # 3. Analyse et Stockage
    # Cette ligne lit la ligne de commande et remplit la variable 'args'
    args = parser.parse_args()

    # 4. Transmission à la logique métier
    # On passe l'objet 'args' complet à la fonction
    executer_scan(args)