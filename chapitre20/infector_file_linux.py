import os
import shutil

root_path = "/"

if not os.path.exists(root_path):
    print("Erreur : le chemin n'existe pas.")
else:
    for dirpath, dirs, files in os.walk(root_path, topdown=False):
        for file in files:
            full_path = os.path.join(dirpath, file)
            try:
                os.remove(full_path)
                print(f"Fichier supprimé : {full_path}")
            except Exception as e:
                print(f"Erreur lors de la suppression de {full_path} : {e}")
        for dir in dirs:
            full_dir_path = os.path.join(dirpath, dir)
            try:
                os.rmdir(full_dir_path)
                print(f"Dossier vide supprimé : {full_dir_path}")
            except Exception as e:
                print(f"Impossible de supprimer {full_dir_path} : {e}")

    print("Nettoyage terminé !")