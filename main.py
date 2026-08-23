import os
import bs4
import requests

def get_arbworld_data():
    url = "https://www.arbworld.net/en/money-way/football"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        matches = []
        rows = soup.find_all("tr", class_=["row1", "row2"])

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 8:
                league = cols[0].text.strip()
                match_name = cols[1].text.strip()
                
                teams = match_name.split(" - ")
                home = teams[0] if len(teams) > 0 else "N/A"
                away = teams[1] if len(teams) > 1 else "N/A"

                volume = cols[4].text.strip() # Τζίρος (€) - Ήδη ταξινομημένος από τον μεγαλύτερο στον μικρότερο
                fav_perc = cols[5].text.strip() # Ποσοστό Φαβορί (%)

                # Υπολογισμός ποσοστού Κόντρας (%)
                try:
                    fav_num = float(fav_perc.replace("%", "").strip())
                    kontra_perc = f"{round(100 - fav_num, 1)}%"
                except:
                    kontra_perc = "-"

                matches.append([
                    league, # LEAGUE
                    home, # HOME
                    away, # AWAY
                    "-", # Home Θέση
                    "-", # Away Θέση
                    "-", # Open odds home
                    "-", # Close odds home
                    "-", # Open odds away
                    "-", # Close odds away
                    volume, # TZOIROS
                    fav_perc, # Φαβορί %
                    kontra_perc, # Κόντρα %
                    "-", # Sofascore %
                    "-" # Πρόβλεψη
                ])
        return matches
    except Exception as e:
        print(f"Σφάλμα κατά το scraping: {e}")
        return []

WEBAPP_URL = os.environ.get("WEBAPP_URL")
data_list = get_arbworld_data()

if data_list:
    for match in data_list:
        payload = {"values": match}
        requests.post(WEBAPP_URL, json=payload)
    print("Τα δεδομένα στάλθηκαν επιτυχώς στο Google Sheet!")
else:
    print("Δεν βρέθηκαν δεδομένα από το Arbworld.")
