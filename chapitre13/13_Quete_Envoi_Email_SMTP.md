# Quête 13 : Automatisation d'Envoi d'Emails (SMTP)

## Objectifs de la quête
- [x] Configurer un compte Google pour l'accès API (Mots de passe d'application).
- [x] Comprendre le protocole SMTP (Simple Mail Transfer Protocol).
- [x] Développer un script Python utilisant `smtplib` pour envoyer un email authentifié.

---

## 1. Configuration de Sécurité Google (Mise à jour post-2022)

Depuis la désactivation de l'option "Less Secure Apps", nous devons générer un mot de passe spécifique pour notre script Python. Cela permet au script de se connecter sans être bloqué par la validation en deux étapes.

### Procédure de génération du Token
1.  **Activer la 2FA :** Allez sur votre compte Google > Sécurité > **Validation en deux étapes** et activez-la (si ce n'est pas déjà fait).
2.  **Créer un mot de passe d'application :**
    * Toujours dans "Sécurité", cherchez "Mots de passe d'application" (ou tapez-le dans la barre de recherche du compte).
    * Nommez l'application : `Script_Python_Automate`.
    * Cliquez sur **Créer**.
3.  **Récupérer le code :** Google va afficher un code de 16 caractères (ex: `abcd efgh ijkl mnop`).
    * ⚠️ **Copiez ce code.** C'est ce mot de passe que vous utiliserez dans le script, PAS votre mot de passe Gmail habituel.

---

## 2. Le Script : Client SMTP (`send_mail.py`)

Nous utilisons le module standard `smtplib` pour la connexion et `email.mime` pour formater le message (Sujet, Expéditeur, Corps) proprement.

### Code Source

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def envoyer_email():
    print("--- Préparation de l'envoi d'email ---")

    # 1. Configuration du Serveur et des Identifiants
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # Port SSL standard pour Gmail
    
    sender_email = "votre_email@gmail.com"     # Remplacer par votre email
    # Remplacer par le mot de passe d'application de 16 caractères (sans espaces)
    password = "abcd efgh ijkl mnop"           

    receiver_email = "destinataire@example.com" # Remplacer par l'email cible

    # 2. Construction du Message (Format MIME)
    # Cela permet d'avoir un "Sujet" propre et un corps de texte
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Test Automatisé - Quête 13"

    body = """
    Bonjour,

    Ceci est un email envoyé automatiquement via un script Python.
    Le protocole SMTP a fonctionné avec succès avec l'authentification SSL.

    Cordialement,
    Votre Robot Python.
    """
    # Attachement du corps au message
    message.attach(MIMEText(body, "plain"))

    try:
        # 3. Connexion Sécurisée au Serveur
        print(f"[*] Connexion au serveur {smtp_server}:{smtp_port}...")
        
        # SMTP_SSL gère le chiffrement dès le début de la connexion
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            
            # 4. Authentification
            print("[*] Authentification en cours...")
            server.login(sender_email, password)
            
            # 5. Envoi
            print(f"[*] Envoi de l'email à {receiver_email}...")
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("[+] Succès ! Email envoyé.")

    except smtplib.SMTPAuthenticationError:
        print("[!] Erreur d'authentification : Vérifiez votre email ou votre mot de passe d'application.")
    except Exception as e:
        print(f"[!] Erreur technique : {e}")

if __name__ == "__main__":
    envoyer_email()
3. Exécution et Validation
Modification du script :
Ouvrez le fichier et remplacez sender_email par votre Gmail et password par le code de 16 lettres généré à l'étape 1. Remplacez receiver_email par une autre adresse à vous pour tester.

Lancement :

Bash
python3 send_mail.py
Résultat attendu :

Plaintext
--- Préparation de l'envoi d'email ---
[*] Connexion au serveur smtp.gmail.com:465...
[*] Authentification en cours...
[*] Envoi de l'email à mon_autre_compte@example.com...
[+] Succès ! Email envoyé.