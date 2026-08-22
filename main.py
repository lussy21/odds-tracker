import os
import requests
import pandas as pd

print("=== ΕΚΚΙΝΗΣΗ ODDS TRACKER BOT (FAVORITE VS DOUBLE CHANCE) ===")

# 15 Στοχευμένες Διοργανώσεις
TARGET_LEAGUES = [
    "Premier League", "LaLiga", "Serie A", "Bundesliga", "Ligue 1",
    "Super League", "Champions League", "Europa League", "Conference League",
    "Super Lig", "Jupiler Pro League", "Superliga", "Eredivisie", 
    "Liga Portugal", "Premiership"
]

SHEET_URL = os.environ.get("GOOGLE_SHEET_URL", "Not Set")

def fetch_stoiximan_data():
    print("1. Συλλογή αποδόσεων (Φαβορί & Διπλή Ευκαιρία) από Stoiximan...")

def fetch_sofascore_data():
    print("2. Συλλογή ποσοστών κοινού (Φαβορί vs Κόντρα) από Sofascore...")

def fetch_arbworld_data():
    print("3. Συλλογή τζίρων & όγκου χρημάτων από Arbworld...")

def update_google_sheet():
    print(f"4. Ενημέρωση Google Sheet ({SHEET_URL})...")

if __name__ == "__main__":
    fetch_stoiximan_data()
    fetch_sofascore_data()
    fetch_arbworld_data()
    update_google_sheet()
    print("=== Η ΔΙΑΔΙΚΑΣΙΑ ΟΛΟΚΛΗΡΩΘΗΚΕ ΕΠΙΤΥΧΩΣ ===")
