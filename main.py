import json
import os
import requests

# Παίρνει το Web App URL από τα secrets του GitHub
url = os.environ["WEBAPP_URL"]

# Παράδειγμα δεδομένων (αντιστοιχούν στις στήλες LEAGUE, HOME, AWAY, κτλ.)
data = {
    "values": [
        "Premier League",
        "Arsenal",
        "Chelsea",
        "1",
        "3",
        "2.10",
        "2.05",
        "3.40",
        "3.50",
        "5000",
        "55%",
        "45%",
        "7.8",
        "1X",
    ]
}

# Αποστολή δεδομένων στο Google Sheet
response = requests.post(url, json=data)

if response.status_code == 200:
    print("Τα δεδομένα προστέθηκαν επιτυχώς στο Google Sheet!")
else:
    print(f"Σφάλμα κατά την αποστολή: {response.status_code}")
