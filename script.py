import requests
import json
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

    # Extract usefull data
    final_balance = json_data["result"][0]["final_balance"]
    final_roll_count = json_data["result"][0]["final_roll_count"]
    cycles = [info["cycle"] for info in json_data["result"][0]["cycle_infos"]]
    ok_counts = [info["ok_count"] for info in json_data["result"][0]["cycle_infos"]]

    # Create main window
    root = tk.Tk()
    root.title("Display Values and Graph")

    # Create Labels
    label_balance = tk.Label(root, text=f"Final Balance: {final_balance}")
    label_balance.pack(pady=5)
    label_roll_count = tk.Label(root, text=f"Final Roll Count: {final_roll_count}")
    label_roll_count.pack(pady=5)

    plot_frame = tk.Frame(root)
    plot_frame.pack(fill=tk.BOTH, expand=True)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cycles, ok_counts, marker='o', linestyle='-', color='b')
    ax.set_title('Validation per Cycle')
    ax.set_xlabel('Cycle')
    ax.set_ylabel('OK Count')
    ax.grid(True)

    # Format x-axis to show decimal values
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Run app
    root.mainloop()
