# Quête 5 : Sockets TCP et Serveur Multithreadé

## Objectifs de la quête
- [x] Développer un serveur et un client utilisant le module `socket`.
- [x] Instaurer une communication bidirectionnelle (Envoi ↔ Réponse).
- [x] Le client doit accepter un message en argument de ligne de commande.
- [x] Le serveur doit utiliser le **multithreading** pour gérer plusieurs clients simultanément.

---

## 1. Concepts : Sockets et Concurrence

### Les Sockets
Un **socket** est un point final d'un flux de communication bidirectionnel entre deux programmes sur un réseau. C'est comme une prise électrique : le serveur attend qu'on s'y branche, et le client apporte la prise mâle.

### Pourquoi le Multithreading ?
Par défaut, un script Python est séquentiel. Si un serveur traite un client (ex: il attend un message), il est "bloqué" et ne peut pas accepter d'autres connexions.
Le **Multithreading** permet au serveur de dire : *"Toi, nouveau client, je te confie à un processus léger (thread) dédié, et moi je retourne écouter la porte pour les suivants."*

---

## 2. Le Serveur (`server_thread.py`)

Ce script écoute sur un port donné. À chaque nouvelle connexion, il lance un thread indépendant.

```python
import socket
import threading

# Configuration du serveur
HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau disponibles
PORT = 9999       # Port d'écoute (doit être > 1024 pour ne pas nécessiter root)

def handle_client(client_socket, address):
    """
    Fonction exécutée dans un thread séparé pour chaque client.
    """
    print(f"[+] Nouvelle connexion acceptée de {address}")

    try:
        # 1. Réception du message (buffer de 1024 octets)
        request = client_socket.recv(1024)
        
        if request:
            # Décodage : Les sockets transmettent des bytes, il faut décoder en string
            msg_recu = request.decode('utf-8')
            print(f"    Message de {address}: {msg_recu}")

            # 2. Préparation et Envoi de la réponse (Bidirectionnel)
            reponse = f"Bien reçu, {address}. J'ai traité : '{msg_recu}'"
            client_socket.send(reponse.encode('utf-8'))
        else:
            print(f"[-] {address} s'est déconnecté sans envoyer de données.")

    except Exception as e:
        print(f"[!] Erreur avec {address}: {e}")
    finally:
        # 3. Fermeture propre de la connexion client
        client_socket.close()
        print(f"[-] Connexion fermée avec {address}")

def start_server():
    # Création du socket (AF_INET = IPv4, SOCK_STREAM = TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Option pour réutiliser l'adresse immédiatement (évite l'erreur "Address already in use")
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5) # File d'attente de 5 connexions max avant rejet
        print(f"[*] Serveur en écoute sur {HOST}:{PORT}")

        while True:
            # Boucle infinie : on attend les clients
            client_sock, addr = server.accept()
            
            # Au lieu de traiter le client ici (ce qui bloquerait),
            # on délègue à un thread.
            client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
            client_handler.start()
            
            # On affiche le nombre de threads actifs (clients connectés - 1 pour le main)
            print(f"[*] Connexions actives : {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[!] Arrêt du serveur demandé.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()