import requests
import json
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

def extract_address_from_file(file_path: str) -> str:
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
            print(json.dumps(response_json, indent=4))
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def get_addresses(address: str) -> dict:
    # Define API and URL
    url = 'https://mainnet.massa.net/api/v2'
    headers = {
        'Content-Type': 'application/json'
    }
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
            print(json.dumps(response_json, indent=4))
            return response_json
        else:
            print(f"Error: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def extract_data(json_data: dict) -> Tuple[str, int, List[int], List[int]]:
    """
    Extract useful JSON data.

    :param json_data: Input JSON data to parse.
    :return: Tuple composed of final_balance, final_roll_count, cycles, and ok_counts.
    """
    if "result" in json_data and len(json_data["result"]) > 0:
        result = json_data["result"][0]
        final_balance = result["final_balance"]
        final_roll_count = result["final_roll_count"]
        cycles = [info["cycle"] for info in result["cycle_infos"]]
        ok_counts = [info["ok_count"] for info in result["cycle_infos"]]
        return final_balance, final_roll_count, cycles, ok_counts
    return "", 0, [], []

def refresh_data(address: str, label_balance: tk.Label, label_roll_count: tk.Label, ax: plt.Axes, canvas: FigureCanvasTkAgg) -> None:
    """
    Refresh data and update the UI.

    :param address: Massa node address.
    :param label_balance: Label balance object.
    :param label_roll_count: Label roll count object.
    :param ax: Axes object.
    :param canvas: Canvas object.
    """
    # Get new data
    json_data = get_addresses(address)

     # Extract useful data using the function
    final_balance, final_roll_count, cycles, ok_counts = extract_data(json_data)

    # Update labels
    label_balance.config(text=f"Final Balance: {final_balance}")
    label_roll_count.config(text=f"Final Roll Count: {final_roll_count}")

    # Update plot
    ax.clear()
    ax.plot(cycles, ok_counts, marker='o', linestyle='-', color='b')
    ax.set_title('OK Count par Cycle')
    ax.set_xlabel('Cycle')
    ax.set_ylabel('OK Count')
    ax.grid(True)
    ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    canvas.draw()

###############################################################################

if __name__ == "__main__":
    address = extract_address_from_file('address.txt')
    print("Querry on: " + address)

    #get_status(address)
    json_data = get_addresses(address)

    # Extract useful data using the function
    final_balance, final_roll_count, cycles, ok_counts = extract_data(json_data)

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

    # Create Refresh Button
    refresh_button = tk.Button(root, text="Refresh", command=lambda: refresh_data(address, label_balance, label_roll_count, ax, canvas))
    refresh_button.pack(pady=5)

    # Run app
    root.mainloop()
