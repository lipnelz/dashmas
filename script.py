import requests
import json
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


def get_addresses(address: str) -> None:
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
        else:
            print(f"Erreur: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    address = extract_address_from_file('address.txt')
    print("Querry on: " + address)
    #get_status(address)
    get_addresses(address)
