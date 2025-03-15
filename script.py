import requests
import json
import re


def extract_address_from_file(file_path):
    # Expression régulière pour correspondre à l'adresse
    address_pattern = r'AU[1-9A-HJ-NP-Za-km-z]{50}'

    try:
        # Lire le contenu du fichier
        with open(file_path, 'r') as file:
            content = file.read()

        # Rechercher l'adresse dans le contenu du fichier
        match = re.search(address_pattern, content)

        if match:
            return match.group(0)
        else:
            return "Aucune adresse trouvée."

    except FileNotFoundError:
        return "Le fichier spécifié n'existe pas."


def get_status(address: str) -> None:
    # Define API and URL
    url = 'https://mainnet.massa.net/api/v2'
    headers = {
        'Content-Type': 'application/json'
    }

    # Define requests data
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_status",
         "params": [[address]]
    }

    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check response status
        if response.status_code == 200:
            # Parse JSON
            response_json = response.json()
            print("Réponse de l'API :", response_json)
        else:
            print(f"Erreur: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    address = extract_address_from_file('address.txt')
    print("Querry on: " + address)
    get_status(address)
