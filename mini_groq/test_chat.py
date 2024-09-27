import requests

# URL du point de terminaison /chat
url = 'http://localhost:5000/chat'

# Exemple de prompt à envoyer
data = {
    "prompt": "Quel est le capital de la France ?"
}

# Envoyer la requête POST
response = requests.post(url, json=data)

# Afficher la réponse
print("Statut de la réponse :", response.status_code)
print("Contenu de la réponse :", response.json())
