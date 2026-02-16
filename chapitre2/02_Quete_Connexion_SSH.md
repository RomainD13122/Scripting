# Quête 2 : Connexion SSH et Automatisation Python

## Objectifs de la quête
- [x] Établir une connexion SSH manuelle (OpenSSH) entre une machine cliente et un serveur.
- [x] Développer un script Python utilisant le module `spur` pour automatiser cette connexion.

---

## 1. Connexion SSH Manuelle (OpenSSH)

Le protocole SSH (Secure Shell) permet de prendre le contrôle d'une machine à distance de manière sécurisée (chiffrée).



### Prérequis : Préparation du Serveur
Avant de se connecter, il faut s'assurer que la machine cible (le serveur) possède le service SSH actif et connaître son adresse IP.

1.  **Installation du serveur SSH (sur la machine cible) :**
    ```bash
    sudo apt update
    sudo apt install openssh-server -y
    ```
2.  **Vérification du service :**
    ```bash
    sudo systemctl status ssh
    ```
    *Le statut doit indiquer `active (running)`.*

3.  **Récupération de l'adresse IP :**
    ```bash
    ip a
    ```
    *Notons l'adresse IP (ex: `192.168.1.25`) pour la suite.*

### Connexion depuis le Client
Depuis la machine hôte ou une seconde VM (le client) :

1.  **Lancer la commande de connexion :**
    La syntaxe est `ssh utilisateur@adresse_ip`.
    ```bash
    ssh user@192.168.1.25
    ```
2.  **Validation :**
    * À la première connexion, tapez `yes` pour accepter l'empreinte (fingerprint) du serveur.
    * Entrez le mot de passe de l'utilisateur distant.
    * Si le prompt change (ex: `user@serveur:~$`), la connexion est réussie.

---

## 2. Automatisation avec Python et `spur`

Pour automatiser des tâches d'administration, nous remplaçons l'interaction humaine par un script. Nous utilisons ici **`spur`**, une bibliothèque Python conçue pour exécuter des commandes à la fois localement et via SSH de manière simple.

### Étape A : Installation du module

Le module `spur` n'est pas inclus par défaut dans Python. Il faut l'installer via le gestionnaire de paquets `pip`.

```bash
pip install spur