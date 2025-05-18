import random
import smtplib
from email.mime.text import MIMEText

# Fonction pour envoyer un email de vérification
def envoyer_email(destinataire, code):
    """
    Envoie un email contenant le code de vérification au destinataire.

    Args:
        destinataire (str): L'adresse email du destinataire.
        code (str): Le code de vérification à envoyer.

    """
    smtp_server = "smtp.gmail.com"  # Serveur SMTP pour Gmail
    smtp_port = 587  # Port pour une connexion TLS
    sender_email = "sdmoustahy@gmail.com"  # Remplacer par ton adresse
    sender_password = "kaug jmkz vtzh ayas"  # Remplacer par ton mot de passe

    # Création du message
    message = MIMEText(f"""
Bonjour,

Merci de participer à notre système de vote sécurisé.

Voici votre code de vérification personnel : {code}

Veuillez entrer ce code sur la plateforme pour continuer votre processus de vote.

Attention : Ce code est valable pour une seule utilisation et a une durée de validité limitée.

Merci de votre confiance.
Cordialement,
L'équipe Système de Vote Électronique
        """)

    message['Subject'] = "Code de Vérification"  # Sujet de l'email
    message['From'] = sender_email  # Email de l'expéditeur
    message['To'] = destinataire  # Email du destinataire

    try:
        # Connexion au serveur SMTP et envoi du message
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Démarrer la connexion sécurisée
            server.login(sender_email, sender_password)  # Connexion avec les informations d'identification
            server.sendmail(sender_email, destinataire, message.as_string())  # Envoi du message
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")


# Fonction pour générer un code de vérification à 6 chiffres
def generer_code():
    """
    Génère un code de vérification aléatoire à 6 chiffres.

    Returns:
        str: Un code de vérification sous forme de chaîne de caractères.
    """
    return str(random.randint(100000, 999999))  # Code entre 100000 et 999999
