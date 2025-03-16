# Massa Node Data Visualizer

## Description

This project is a graphical application that visualizes data from a Massa node. It displays information such as the final balance, final roll count, and a graph of N/OK counts per cycle. The application uses `tkinter` for the graphical interface and `matplotlib` for plotting graphs.

## Features

- Display of final balance and final roll count.
- Interactive graph of OK counts per cycle.
- Refresh button to update data.

## Prerequisites

- Python 3.x
- Python libraries: `requests`, `matplotlib`, `tkinter`

## Usage

A file with Massa node address must be next to the `main.py`.

```
dashmas
├── main.py
└── address.txt
```

The content of `address.txt` is the raw Massa node address, shuch as `AU12gAkmGeozFceJD4tQmbVvihYdX2KyWZcYLL8xdYZeP4EuWYdex`

## Documentation

[API](https://docs.massa.net/docs/build/api/jsonrpc)

[MASSA](https://www.massa.net/)