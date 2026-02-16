# Quête 26 : Changement d'Adresse MAC (MAC Changer)

## Objectifs de la quête
- [x] Comprendre la structure d'une adresse MAC (OUI + NIC).
- [x] Changer manuellement l'adresse MAC d'une interface via le terminal.
- [x] Développer un script Python automatisant cette tâche.
- [x] Implémenter une validation des arguments (Interface et Format).

---

## 1. Comprendre l'Adresse MAC

Une adresse MAC est un identifiant physique unique attribué à chaque carte réseau. Elle est composée de 6 octets (48 bits), généralement notés en hexadécimal.



* **Les 3 premiers octets (OUI) :** Identifient le constructeur (ex: Dell, Apple, Intel).
* **Les 3 derniers octets :** Identifient la carte spécifique (numéro de série).

---

## 2. Méthode Manuelle (Ligne de commande)

Avant de scripter, il faut maîtriser la commande système. Sur Linux, nous utilisons la suite `ip` (plus moderne que `ifconfig`).

**Procédure :**
1.  **Désactiver l'interface :** On ne peut pas changer l'adresse d'une carte active.
    ```bash
    sudo ip link set dev eth0 down
    ```
    *(Remplacez `eth0` par votre interface, visible via `ip a`).*

2.  **Changer l'adresse :**
    ```bash
    sudo ip link set dev eth0 address 00:11:22:33:44:55
    ```

3.  **Réactiver l'interface :**
    ```bash
    sudo ip link set dev eth0 up
    ```

4.  **Vérification :**
    ```bash
    ip link show eth0
    ```

---

## 3. Le Script Python : Automatisation (`mac_changer.py`)

Ce script utilise `subprocess` pour exécuter les commandes vues ci-dessus. Il utilise `argparse` pour récupérer les choix de l'utilisateur et `re` (Expressions Régulières) pour vérifier que le changement a bien eu lieu.

### Code Source

```python
import subprocess
import argparse
import re
import sys

def obtenir_arguments():
    """
    Récupère et parse les arguments de la ligne de commande.
    """
    parser = argparse.ArgumentParser(description="Outil de changement d'adresse MAC")
    
    # Argument 1 : L'interface (ex: eth0, wlan0)
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Interface réseau à modifier")
    
    # Argument 2 : La nouvelle MAC
    parser.add_argument("-m", "--mac", dest="new_mac", required=True, help="Nouvelle adresse MAC")
    
    args = parser.parse_args()
    return args

def verifier_interface(interface):
    """
    Vérifie si l'interface existe sur le système.
    """
    try:
        # On liste les interfaces disponibles
        resultat = subprocess.check_output(["ip", "link", "show"], text=True)
        if interface in resultat:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        print("[!] Erreur : Impossible de lire les interfaces système.")
        sys.exit(1)

def changer_mac(interface, new_mac):
    """
    Exécute la séquence de commandes système pour changer la MAC.
    """
    print(f"[+] Modification de l'adresse MAC pour {interface} vers {new_mac}")
    
    # On utilise subprocess.call pour lancer les commandes séquentiellement
    # 1. Down
    subprocess.call(["ip", "link", "set", "dev", interface, "down"])
    
    # 2. Change
    try:
        subprocess.check_call(["ip", "link", "set", "dev", interface, "address", new_mac])
    except subprocess.CalledProcessError:
        print("[!] Erreur : Format d'adresse MAC invalide ou permissions insuffisantes.")
        sys.exit(1)

    # 3. Up
    subprocess.call(["ip", "link", "set", "dev", interface, "up"])

def recuperer_mac_actuelle(interface):
    """
    Utilise une Regex pour extraire l'adresse MAC depuis la commande 'ip link show'
    """
    try:
        resultat = subprocess.check_output(["ip", "link", "show", interface], text=True)
        
        # Regex pour trouver une MAC (XX:XX:XX:XX:XX:XX)
        mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", resultat)
        
        if mac_search:
            return mac_search.group(0)
        else:
            print("[-] Impossible de lire l'adresse MAC.")
            return None
    except:
        return None

# --- Bloc Principal ---
if __name__ == "__main__":
    # 1. Récupération des arguments
    options = obtenir_arguments()
    
    # 2. Vérification de l'interface
    if not verifier_interface(options.interface):
        print(f"[!] Erreur : L'interface '{options.interface}' n'existe pas sur ce système.")
        print("    Vérifiez avec la commande 'ip a'.")
        sys.exit(1)

    # 3. Affichage avant modification
    mac_actuelle = recuperer_mac_actuelle(options.interface)
    print(f"[*] MAC actuelle : {str(mac_actuelle)}")

    # 4. Modification
    changer_mac(options.interface, options.new_mac)

    # 5. Vérification finale
    mac_finale = recuperer_mac_actuelle(options.interface)
    
    if mac_finale == options.new_mac:
        print(f"[+] Succès ! L'adresse MAC est maintenant : {mac_finale}")
    else:
        print(f"[-] Échec. L'adresse MAC est toujours : {mac_finale}")
4. Exécution et Test
⚠️ Important : Ce script modifie la configuration matérielle, il doit être exécuté avec sudo.

Identifier votre interface :
Tapez ip a dans le terminal. Disons que votre carte s'appelle enp0s3.

Lancer le script (Test d'erreur - Interface inconnue) :

Bash
sudo python3 mac_changer.py -i toto0 -m 00:11:22:33:44:55
Résultat :

Plaintext
[!] Erreur : L'interface 'toto0' n'existe pas sur ce système.
Lancer le script (Succès) :

Bash
sudo python3 mac_changer.py -i enp0s3 -m 00:11:22:33:44:55
Résultat :

Plaintext
[*] MAC actuelle : 08:00:27:1c:4a:9e
[+] Modification de l'adresse MAC pour enp0s3 vers 00:11:22:33:44:55
[+] Succès ! L'adresse MAC est maintenant : 00:11:22:33:44:55