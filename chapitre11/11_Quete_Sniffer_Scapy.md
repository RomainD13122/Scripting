# Quête 11 : Création d'un Sniffer Réseau avec Scapy

## Objectifs de la quête
- [x] Utiliser la fonction `sniff()` de Scapy pour intercepter le trafic en temps réel.
- [x] Définir une fonction de "callback" (`prn`) pour traiter chaque paquet capturé.
- [x] Filtrer et afficher les informations essentielles (IP Source, Destination, Protocole) de manière lisible.
- [x] Générer du trafic (Ping) pour valider le fonctionnement du sniffer.

---

## 1. Comprendre le Sniffing

Le "Sniffing" consiste à écouter tout ce qui passe par la carte réseau, même ce qui ne nous est pas destiné (si la carte le permet, via le mode *promiscuous*).



Scapy simplifie cela avec une seule fonction : `sniff()`.
Elle prend deux arguments principaux pour nous ici :
1.  **`filter`** : Pour ne pas être noyé sous le trafic (ex: ne regarder que le protocole ICMP).
2.  **`prn`** : Une fonction que nous allons écrire, qui sera appelée automatiquement à chaque fois qu'un paquet est attrapé.

---

## 2. Le Script : Sniffer Personnalisé (`my_sniffer.py`)

Ce script va écouter le réseau indéfiniment. Pour éviter d'afficher des pages entières de données hexadécimales, nous allons extraire proprement les IPs et le type de paquet.

### Code Source

```python
from scapy.all import *
import sys

# Cette fonction est appelée AUTOMATIQUEMENT pour chaque paquet capturé
def packet_callback(packet):
    # On vérifie si le paquet possède une couche IP
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = packet[IP].proto
        
        # Détermination du protocole pour l'affichage (1=ICMP, 6=TCP, 17=UDP)
        proto_name = ""
        if protocol == 1:
            proto_name = "ICMP (Ping)"
        elif protocol == 6:
            proto_name = "TCP"
        elif protocol == 17:
            proto_name = "UDP"
        else:
            proto_name = f"Proto-{protocol}"

        # Affichage formaté et lisible
        print(f"[*] Capturé : {proto_name} | {ip_src} -> {ip_dst}")
        
        # Si c'est du TCP/UDP, on affiche aussi les ports
        if packet.haslayer(TCP):
            print(f"    Payload TCP : Port {packet[TCP].sport} -> {packet[TCP].dport}")
        elif packet.haslayer(UDP):
            print(f"    Payload UDP : Port {packet[UDP].sport} -> {packet[UDP].dport}")

def start_sniffer():
    print("--- Démarrage du Sniffer Réseau ---")
    print("[*] En attente de paquets... (CTRL-C pour arrêter)")
    
    # Lancement de l'écoute
    # iface=None : Scapy choisit l'interface par défaut (eth0, wlan0...)
    # store=0    : On ne garde pas les paquets en mémoire (évite de saturer la RAM)
    # prn        : La fonction à appeler pour chaque paquet
    # filter     : Syntaxe BPF (Berkeley Packet Filter). Ici, on écoute tout.
    #              Pour écouter seulement le ping, on mettrait filter="icmp"
    
    try:
        sniff(filter="icmp", prn=packet_callback, store=0)
    except KeyboardInterrupt:
        print("\n[!] Arrêt du sniffer.")
        sys.exit(0)
    except PermissionError:
        print("[!] Erreur : Vous devez être ROOT pour sniffer le réseau (sudo).")

if __name__ == "__main__":
    start_sniffer()
3. Exécution et Génération de Trafic
Comme pour la Quête 4, l'accès à la carte réseau en mode écoute nécessite les privilèges administrateur.

Étape 1 : Lancer le Sniffer
Ouvrez un premier terminal et lancez le script :

Bash
sudo python3 my_sniffer.py
Le script doit afficher "En attente de paquets..." et rester bloqué là.

Étape 2 : Générer du trafic
Ouvrez un second terminal. Nous allons générer du trafic ICMP (Ping) vers Google.

Bash
ping -c 4 8.8.8.8
Étape 3 : Observer la capture
Retournez voir le premier terminal. Vous devriez voir les paquets apparaître en temps réel.

Résultat attendu :

Plaintext
--- Démarrage du Sniffer Réseau ---
[*] En attente de paquets... (CTRL-C pour arrêter)
[*] Capturé : ICMP (Ping) | 192.168.1.25 -> 8.8.8.8
[*] Capturé : ICMP (Ping) | 8.8.8.8 -> 192.168.1.25
[*] Capturé : ICMP (Ping) | 192.168.1.25 -> 8.8.8.8
[*] Capturé : ICMP (Ping) | 8.8.8.8 -> 192.168.1.25
Vous voyez l'aller (Request) de votre machine vers Google, et le retour (Reply) de Google vers votre machine.

4. Analyse Avancée (Optionnelle)
Si vous voulez voir tout le trafic (pas seulement le ping), modifiez la ligne sniff dans le script :

Remplacer :

Python
sniff(filter="icmp", prn=packet_callback, store=0)
Par :

Python
# On exclut le port 22 pour ne pas capturer notre propre connexion SSH si on travaille à distance
sniff(filter="not port 22", prn=packet_callback, store=0)
Lancez ensuite un navigateur web sur la machine ou faites un curl google.com. Vous verrez défiler des paquets TCP et UDP (DNS).