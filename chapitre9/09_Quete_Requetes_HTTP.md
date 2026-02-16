import requests
import json

def fetch_data(url_cible):
    print(f"--- Envoi de la requête vers : {url_cible} ---")

    try:
        # 1. Exécution de la requête GET
        # timeout=5 : On abandonne si le serveur ne répond pas en 5 secondes
        response = requests.get(url_cible, timeout=5)

        # 2. Analyse du Code HTTP (Status Code)
        # 200 = OK, 404 = Non trouvé, 500 = Erreur Serveur
        print(f"[*] Code Statut reçu : {response.status_code}")

        # 3. Vérification du succès
        if response.status_code == 200:
            print("[+] Succès ! La ressource a été récupérée.")
            
            # 4. Traitement des données
            # .text renvoie le contenu brut (string)
            # .json() convertit automatiquement la réponse en dictionnaire Python
            try:
                data = response.json()
                print("\n[+] Contenu de la réponse (JSON formatté) :")
                print(json.dumps(data, indent=4)) # Affichage joli
                
                # Exemple d'extraction précise
                print(f"\n[i] Titre extrait : {data.get('title')}")
                
            except json.JSONDecodeError:
                print("[!] La réponse n'est pas du JSON valide.")
                print(response.text[:100]) # Affiche les 100 premiers caractères
        
        elif response.status_code == 404:
            print("[-] Erreur 404 : La ressource demandée n'existe pas.")
        else:
            print(f"[-] Erreur inattendue : {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("[!] Impossible de se connecter au serveur (Pas d'internet ?).")
    except requests.exceptions.Timeout:
        print("[!] Le serveur est trop lent à répondre.")

if __name__ == "__main__":
    # URL de test qui renvoie un faux article de blog (JSON)
    target = "[https://jsonplaceholder.typicode.com/posts/1](https://jsonplaceholder.typicode.com/posts/1)"
    
    fetch_data(target)
3. Exécution et Analyse
Lancez le script dans votre terminal :

Bash
python3 http_client.py
Résultat attendu (Cas Nominal) :

Plaintext
--- Envoi de la requête vers : [https://jsonplaceholder.typicode.com/posts/1](https://jsonplaceholder.typicode.com/posts/1) ---
[*] Code Statut reçu : 200
[+] Succès ! La ressource a été récupérée.

[+] Contenu de la réponse (JSON formatté) :
{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur..."
}

[i] Titre extrait : sunt aut facere repellat provident occaecati excepturi optio reprehenderit
Test d'erreur (Cas 404) :
Modifiez l'URL dans le script pour pointer vers une ressource inexistante (ex: /posts/99999) et relancez.

Plaintext
[*] Code Statut reçu : 404
[-] Erreur 404 : La ressource demandée n'existe pas.