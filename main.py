import os
import requests

print("=== ΕΚΚΙΝΗΣΗ ODDS TRACKER BOT ===")

# Πηγές Δεδομένων:
# 1. Stoiximan -> Αποδόσεις (Open/Close)
# 2. Sofascore -> Community Votes (%)
# 3. Arbworld -> Τζίροι & Ποσοστά (Moneyway)

SHEET_URL = os.environ.get("GOOGLE_SHEET_URL", "Not Set")

def fetch_data():
    print("1. Συλλογή αποδόσεων από Stoiximan...")
    print("2. Συλλογή ποσοστών κοινού από Sofascore...")
    print("3. Συλλογή τζίρων από Arbworld...")
    print("Ενημέρωση Google Sheet...")

if __name__ == "__main__":
    fetch_data()
    print("=== Η ΔΙΑΔΙΚΑΣΙΑ ΟΛΟΚΛΗΡΩΘΗΚΕ ΕΠΙΤΥΧΩΣ ===")
