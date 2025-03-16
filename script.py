import requests
import json
import tkinter as tk
import re

def extract_address_from_file(file_path):
    """
    Reads a text file and returns its content as a string.

    :param file_path: The name of the file to read.
    :return: The content of the file as a string.
    """
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            content = file.read().strip()  # Read and remove leading and trailing spaces
        return content
    except FileNotFoundError:
        return "The specified file does not exist."
    except Exception as e:
        return f"An error occurred: {e}"


def get_status(address: str) -> None:
    """
    Print the status from a given address

    :param address: The address to querry.
    """
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
            # Correctly display JSON
            print(json.dumps(response_json, indent=4))
        else:
            print(f"Erreur: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")


def get_addresses(address: str) -> str:
    # Define API and URL
    url = 'https://mainnet.massa.net/api/v2'
    headers = {
        'Content-Type': 'application/json'
    }

    # Define requests data
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_addresses",
         "params": [[address]]
    }

    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check response status
        if response.status_code == 200:
            # Parse JSON
            response_json = response.json()
            # Correctly display JSON
            print(json.dumps(response_json, indent=4))
            return response_json
        else:
            print(f"Erreur: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    address = extract_address_from_file('address.txt')
    print("Querry on: " + address)
    #get_status(address)
    json_data = get_addresses(address)

    # Extraire les valeurs
    final_balance = json_data["result"][0]["final_balance"]
    final_roll_count = json_data["result"][0]["final_roll_count"]

    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Affichage des valeurs JSON")

    # Créer des étiquettes pour afficher les valeurs
    label_balance = tk.Label(root, text=f"Final Balance: {final_balance}")
    label_balance.pack(pady=5)

    label_roll_count = tk.Label(root, text=f"Final Roll Count: {final_roll_count}")
    label_roll_count.pack(pady=5)

    # Exécuter l'application
    root.mainloop()
