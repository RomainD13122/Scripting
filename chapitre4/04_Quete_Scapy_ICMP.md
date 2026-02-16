# Quête 4 : Forger et Envoyer des Paquets Réseau avec Scapy

## Objectifs de la quête
- [x] Créer un paquet ICMP (Ping) manuellement avec Scapy.
- [x] Inspecter la structure interne du paquet créé.
- [x] Envoyer le paquet vers un serveur public (Google DNS : 8.8.8.8).
- [x] Capturer et analyser la réponse réseau.

---

## 1. Introduction à Scapy

Scapy est une bibliothèque Python puissante capable de manipuler les paquets réseau. Contrairement aux outils classiques qui envoient des données "déjà prêtes", Scapy nous permet de construire le paquet couche par couche (Layer 2, Layer 3, Layer 4, etc.).



### Prérequis
Scapy nécessite des privilèges élevés pour accéder directement à la carte réseau (Raw Sockets).
1.  **Installation :**
    ```bash
    pip install scapy
    ```
    *(Si vous êtes sur Linux/Mac, il faudra souvent lancer le script avec `sudo`).*

---

## 2. Le Script : Ping Manuel (`scapy_ping.py`)

Dans ce script, nous allons reproduire le fonctionnement de la commande `ping`, mais en construisant nous-mêmes le paquet.

### Concept de l'empilement (Stacking)
Scapy utilise l'opérateur `/` pour empiler les couches réseau.
Pour un Ping, nous avons besoin de :
1.  Une couche **IP** (pour l'adressage : qui envoie, qui reçoit).
2.  Une couche **ICMP** (pour le protocole de contrôle : type "Echo Request").

**Syntaxe :** `Paquet = IP() / ICMP()`

### Code Source

```python
# Importation de toutes les fonctions de Scapy
# Note : Cela peut prendre quelques secondes au chargement
from scapy.all import *
import sys

def scapy_ping(target_ip):
    print(f"--- Création du paquet pour {target_ip} ---")

    # 1. Création du paquet
    # On crée une couche IP avec la destination cible
    # On empile (/) une couche ICMP par défaut (type 8 : Echo Request)
    packet = IP(dst=target_ip) / ICMP()

    # 2. Observation du paquet créé
    # La méthode .show() affiche la structure détaillée des en-têtes
    print("\n[+] Contenu du paquet envoyé :")
    packet.show()

    print(f"\n[+] Envoi du paquet vers {target_ip}...")

    # 3. Envoi et réception
    # sr1 = Send and Receive 1 packet (Envoie et attend 1 seule réponse)
    # timeout=2 : On attend max 2 secondes pour éviter de bloquer indéfiniment
    reply = sr1(packet, timeout=2, verbose=0)

    # 4. Analyse de la réponse
    if reply:
        print("\n[+] Réponse reçue !")
        # On vérifie si la couche ICMP est présente dans la réponse
        if reply.haslayer(ICMP):
            icmp_layer = reply.getlayer(ICMP)
            print(f"    Source  : {reply[IP].src}")
            print(f"    Type    : {icmp_layer.type} (0 = Echo Reply)")
            print(f"    Code    : {icmp_layer.code}")
            
            # Affichage complet de la réponse pour analyse
            print("\n[+] Détails complets de la réponse :")
            reply.show()
    else:
        print("\n[-] Aucune réponse reçue (Timeout ou pare-feu).")

if __name__ == "__main__":
    target = "8.8.8.8" # Google DNS
    scapy_ping(target)