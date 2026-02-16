# Quête 8 : Pilotage de MySQL via Subprocess

## Objectifs de la quête
- [x] Installer et configurer une base de données MySQL avec un utilisateur dédié.
- [x] Créer une table et y insérer des données de test.
- [x] Utiliser le module `subprocess` pour exécuter une requête SQL depuis Python sans driver spécifique.

---

## 1. Préparation de la Base de Données

Avant de scripter, nous devons préparer le terrain sur la machine virtuelle.



[Image of MySQL database structure]


### Installation (si nécessaire)
```bash
sudo apt update
sudo apt install mysql-server -y
Configuration des Données et Droits
Nous allons créer une base, un utilisateur et quelques données. Connectez-vous à MySQL en root :

Bash
sudo mysql
Une fois dans le prompt MySQL (mysql>), exécutez les commandes suivantes ligne par ligne :

SQL
-- 1. Création de la base de données
CREATE DATABASE IF NOT EXISTS quest_db;

-- 2. Création de l'utilisateur (remplacez 'password123' par un mot de passe fort)
CREATE USER IF NOT EXISTS 'quest_user'@'localhost' IDENTIFIED BY 'password123';

-- 3. Attribution des droits
GRANT ALL PRIVILEGES ON quest_db.* TO 'quest_user'@'localhost';
FLUSH PRIVILEGES;

-- 4. Création de la table et insertion
USE quest_db;
CREATE TABLE IF NOT EXISTS agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    niveau INT
);

INSERT INTO agents (nom, niveau) VALUES ('Bond', 7), ('Hunt', 6), ('Bourne', 8);

-- 5. Sortie
EXIT;
2. Le Script : Interrogation via subprocess
Nous allons utiliser subprocess.run() pour appeler l'exécutable mysql installé sur le système.
La commande système que nous voulons simuler est :
mysql -u quest_user -ppassword123 -D quest_db -e "SELECT * FROM agents;"

Fichier : mysql_wrapper.py
Python
import subprocess

def query_database():
    print("--- Interrogation de la Base de Données via Subprocess ---")

    # 1. Configuration des paramètres
    # Attention : C'est une méthode d'apprentissage. En prod, évitez les mots de passe en clair.
    db_user = "quest_user"
    db_pass = "password123"
    db_name = "quest_db"
    query = "SELECT * FROM agents;"

    # 2. Construction de la commande
    # La commande est une liste de chaînes pour éviter les failles d'injection shell
    # Note importante : Il ne faut PAS d'espace entre -p et le mot de passe pour MySQL CLI
    command = [
        "mysql", 
        f"-u{db_user}", 
        f"-p{db_pass}", 
        f"-D{db_name}", 
        "-e", query
    ]

    try:
        # 3. Exécution du processus
        # capture_output=True : On veut récupérer ce que la commande affiche
        # text=True : On veut recevoir du texte (str) et pas des octets (bytes)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True # Lève une exception si la commande échoue (code != 0)
        )

        # 4. Affichage du résultat (Sortie Standard - stdout)
        print("\n[+] Succès ! Voici les données récupérées :\n")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Gestion des erreurs MySQL (ex: mauvais mot de passe)
        print("\n[!] Erreur lors de l'exécution de la commande MySQL :")
        print(e.stderr)

    except FileNotFoundError:
        # Gestion de l'erreur si mysql n'est pas installé
        print("\n[!] Erreur : La commande 'mysql' est introuvable. Est-elle installée ?")

if __name__ == "__main__":
    query_database()
3. Exécution et Résultats
Lancez le script Python :

Bash
python3 mysql_wrapper.py
Résultat attendu :
Le script va lancer le client MySQL en arrière-plan, récupérer le tableau ASCII généré par MySQL et l'afficher.

Plaintext
--- Interrogation de la Base de Données via Subprocess ---

[+] Succès ! Voici les données récupérées :

id	nom	niveau
1	Bond	7
2	Hunt	6
3	Bourne	8
Conclusion de la Quête 8
Vous avez réussi à faire dialoguer Python et MySQL sans utiliser de driver spécifique.

Avantage : Cette méthode fonctionne dès que le client mysql est installé, sans avoir besoin d'installer des bibliothèques Python (pip install...).

Limitation : Le résultat est une chaîne de caractères brute (format tableau). Pour traiter les données proprement (ex: récupérer juste les noms), il faudrait parser le texte, ce qui est fastidieux. C'est pour cela qu'on préfère généralement des drivers comme mysql-connector pour des applications complexes.