# Quête 3 : Gestion Sécurisée des Fichiers Temporaires

## Objectifs de la quête
- [x] Comprendre l'utilité du module `tempfile` pour la sécurité et la portabilité.
- [x] Développer un script Python qui crée, écrit, lit et supprime proprement un fichier temporaire.

---

## 1. Pourquoi utiliser le module `tempfile` ?

Lorsqu'on développe des scripts, créer des fichiers "en dur" (ex: `open("test.txt", "w")`) pose trois problèmes majeurs :

1.  **Sécurité :** Les fichiers créés peuvent être lisibles par d'autres utilisateurs du système si les permissions ne sont pas gérées strictement.
2.  **Portabilité :** Les chemins changent selon l'OS (Windows utilise `C:\Temp`, Linux utilise `/tmp`). Coder un chemin en dur casse la compatibilité.
3.  **Propreté :** Si le script plante avant de supprimer le fichier, des "déchets" s'accumulent sur le disque.

Le module **`tempfile`** de Python résout tout cela :
* Il choisit automatiquement le bon dossier système.
* Il génère des noms de fichiers aléatoires uniques (impossible à deviner).
* Il gère la suppression automatique du fichier à la fermeture.



---

## 2. Le Script : Manipulation de fichiers temporaires

Nous utilisons ici `NamedTemporaryFile`. L'utilisation du mot-clé `with` (Context Manager) est cruciale : elle garantit que le fichier est fermé et supprimé à la fin du bloc, même si une erreur survient au milieu.

### Fichier : `temp_manager.py`

```python
import tempfile
import os

print("--- Début du traitement des fichiers temporaires ---")

# 1. Création du fichier temporaire
# mode='w+' : Permet d'écrire (w) et de lire (+) en mode texte (pas binaire)
# delete=True : Le fichier sera supprimé dès qu'on le ferme (c'est le défaut)
with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp_file:

    # Affichage du chemin absolu généré par l'OS
    print(f"1. Fichier temporaire créé à l'emplacement : {tmp_file.name}")

    # 2. Écriture de données
    data_to_write = "Ceci est une donnée confidentielle temporaire."
    tmp_file.write(data_to_write)
    print("2. Données écrites dans le fichier.")

    # 3. Préparation à la lecture
    # IMPORTANT : Après l'écriture, le curseur est à la fin du fichier.
    # Il faut le remettre au début (offset 0) pour pouvoir lire.
    tmp_file.seek(0)

    # 4. Lecture et affichage
    content = tmp_file.read()
    print(f"3. Contenu récupéré : '{content}'")

    # Vérification que le fichier existe bien physiquement sur le disque à cet instant
    if os.path.exists(tmp_file.name):
        print("   (Le fichier existe physiquement sur le disque pour l'instant)")

# À partir d'ici, nous sommes sortis du bloc 'with'.
# Le fichier a été fermé et automatiquement supprimé.

print("--- Sortie du bloc contextuel ---")

# 5. Preuve de la suppression
# On essaie d'accéder au chemin du fichier (qui est stocké dans tmp_file.name)
if not os.path.exists(tmp_file.name):
    print("4. Succès : Le fichier temporaire a été automatiquement supprimé.")
else:
    print("4. Échec : Le fichier est toujours présent.")