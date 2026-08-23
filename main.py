import os
import bs4
import requests
import cloudscraper

def get_arbworld_data():
    try:
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )
        url = "https://www.arbworld.net/en/money-way/football"
        response = scraper.get(url, timeout=15)
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

                volume = cols[4].text.strip()
                fav_perc = cols[5].text.strip()

                try:
                    fav_num = float(fav_perc.replace("%", "").strip())
                    kontra_perc = f"{round(100 - fav_num, 1)}%"
                except:
                    kontra_perc = "-"

                matches.append([
                    league, home, away, "-", "-", "-", "-", "-", "-",
                    volume, fav_perc, kontra_perc, "-", "-"
                ])
        return matches
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

WEBAPP_URL = os.environ.get("WEBAPP_URL")
if not WEBAPP_URL:
    print("Error: WEBAPP_URL is not set!")
else:
    data_list = get_arbworld_data()
    if data_list:
        for match in data_list:
            requests.post(WEBAPP_URL, json={"values": match})
        print(f"Στάλθηκαν {len(data_list)} αγώνες.")
    else:
        print("Δεν βρέθηκαν δεδομένα.")
