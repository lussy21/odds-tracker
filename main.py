import os
import datetime
import requests
import cloudscraper
from bs4 import BeautifulSoup

def get_complete_data():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    # --- 1. SCRAPING ARBWORLD (Τζίροι & Ποσοστά) ---
    arb_data = {}
    try:
        arb_url = "https://www.arbworld.net/en/money-way/football"
        res_arb = scraper.get(arb_url, timeout=15)
        soup = BeautifulSoup(res_arb.text, "html.parser")
        rows = soup.find_all("tr", class_=["row1", "row2"])

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                match_name = cols[1].text.strip().lower()
                volume = cols[4].text.strip()
                fav_perc = cols[5].text.strip()
                
                # Καθαρισμός τζίρου για ταξινόμηση (π.χ. "€ 5,000" -> 5000)
                try:
                    vol_num = int(volume.replace("€", "").replace(",", "").replace(" ", "").strip())
                except:
                    vol_num = 0

                arb_data[match_name] = {
                    "volume": volume,
                    "vol_num": vol_num,
                    "fav_perc": fav_perc
                }
    except Exception as e:
        print(f"Arbworld Error: {e}")

    # --- 2. API SOFASCORE (Αγώνες & Αποδόσεις) ---
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    sofa_url = f"https://api.sofascore.com/api/v3/scheduled-events/{today}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    final_results = []
    try:
        res_sofa = scraper.get(sofa_url, headers=headers, timeout=15)
        events = res_sofa.json().get('events', [])

        for ev in events:
            league = ev.get('tournament', {}).get('name', '-')
            home = ev.get('homeTeam', {}).get('name', '-')
            away = ev.get('awayTeam', {}).get('name', '-')
            
            home_pos = str(ev.get('homeTeam', {}).get('ranking', '-'))
            away_pos = str(ev.get('awayTeam', {}).get('ranking', '-'))

            # Search Match στο Arbworld
            match_key = f"{home} - {away}".lower()
            arb_info = arb_data.get(match_key, {"volume": "-", "vol_num": 0, "fav_perc": "-"})

            # Υπολογισμός Κόντρας %
            try:
                fav_num = float(arb_info["fav_perc"].replace("%", "").strip())
                kontra_perc = f"{round(100 - fav_num, 1)}%"
            except:
                kontra_perc = "-"

            final_results.append({
                "vol_num": arb_info["vol_num"],
                "row": [
                    league, # LEAGUE
                    home, # HOME
                    away, # AWAY
                    home_pos, # Home Θέση
                    away_pos, # Away Θέση
                    "-", # Open odds home
                    "-", # Close odds home
                    "-", # Open odds away
                    "-", # Close odds away
                    arb_info["volume"], # TZOIROS
                    arb_info["fav_perc"],# Φαβορί %
                    kontra_perc, # Κόντρα %
                    "-", # Sofascore %
                    "-" # Πρόβλεψη
                ]
            })

    except Exception as e:
        print(f"Sofascore Error: {e}")

    # --- 3. ΤΑΞΙΝΟΜΗΣΗ ΒΑΣΕΙ ΤΖΙΡΟΥ (Μεγαλύτερος -> Μικρότερος) ---
    final_results.sort(key=lambda x: x["vol_num"], reverse=True)
    
    return [item["row"] for item in final_results]

# --- 4. ΑΠΟΣΤΟΛΗ ΣΤΟ GOOGLE SHEETS ---
WEBAPP_URL = os.environ.get("WEBAPP_URL")

if WEBAPP_URL:
    data = get_complete_data()
    if data:
        for row in data:
            requests.post(WEBAPP_URL, json={"values": row})
        print(f"Στάλθηκαν {len(data)} αγώνες ταξινομημένοι βάσει τζίρου!")
    else:
        print("Δεν βρέθηκαν δεδομένα.")
else:
    print("Error: WEBAPP_URL is missing!")
