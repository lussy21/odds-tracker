import os
import datetime
import requests
import cloudscraper

def get_sofascore_matches():
    # Ημερομηνία σημερινή σε μορφή YYYY-MM-DD
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.sofascore.com/api/v3/scheduled-events/{today}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    scraper = cloudscraper.create_scraper()
    
    try:
        # 1. Λήψη αγώνων από Sofascore
        res = scraper.get(url, headers=headers, timeout=15)
        data = res.json()
        events = data.get('events', [])

        matches = []
        for ev in events[:20]: # Παίρνουμε τους πρώτους 20 αγώνες
            league = ev.get('tournament', {}).get('name', '-')
            home = ev.get('homeTeam', {}).get('name', '-')
            away = ev.get('awayTeam', {}).get('name', '-')
            
            # Θέσεις στη βαθμολογία (αν υπάρχουν)
            home_pos = ev.get('homeTeam', {}).get('ranking', '-')
            away_pos = ev.get('awayTeam', {}).get('ranking', '-')

            # ID Αγώνα για λήψη αποδόσεων από Sofascore
            event_id = ev.get('id')
            open_home, close_home, open_away, close_away = "-", "-", "-", "-"
            
            if event_id:
                try:
                    odds_url = f"https://api.sofascore.com/api/v3/event/{event_id}/odds/1/all"
                    odds_res = scraper.get(odds_url, headers=headers, timeout=5)
                    odds_data = odds_res.json()
                    
                    # Εξαγωγή αποδόσεων
                    choices = odds_data.get('markets', [])[0].get('choices', [])
                    for c in choices:
                        if c.get('name') == '1':
                            close_home = str(c.get('fractionalValue', '-'))
                            open_home = str(c.get('initialFractionalValue', close_home))
                        elif c.get('name') == '2':
                            close_away = str(c.get('fractionalValue', '-'))
                            open_away = str(c.get('initialFractionalValue', close_away))
                except:
                    pass

            matches.append([
                league, # LEAGUE
                home, # HOME
                away, # AWAY
                home_pos, # Home Θέση
                away_pos, # Away Θέση
                open_home, # Open odds home
                close_home, # Close odds home
                open_away, # Open odds away
                close_away, # Close odds away
                "-", # TZOIROS (Arbworld)
                "-", # Φαβορί % (Arbworld)
                "-", # Κόντρα %
                "-", # Sofascore %
                "-" # Πρόβλεψη
            ])
        return matches
    except Exception as e:
        print(f"Error Sofascore: {e}")
        return []

WEBAPP_URL = os.environ.get("WEBAPP_URL")
data_list = get_sofascore_matches()

if data_list:
    for match in data_list:
        payload = {"values": match}
        requests.post(WEBAPP_URL, json=payload)
    print(f"Στάλθηκαν {len(data_list)} αγώνες από το Sofascore επιτυχώς!")
else:
    print("Δεν βρέθηκαν δεδομένα.")
