import requests
from bs4 import BeautifulSoup

from src.Request.Odds import get_odds


def scrape_fight_card(fight_urls):
    odds = get_odds()
    fight_details_list = []

    for fight_url in fight_urls:
        response = requests.get(fight_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            event_link = soup.find('h2', class_='b-content__title').find('a')['href']
            event_name = soup.find('h2', class_='b-content__title').find('a').text.strip()

            fighter_a = {
                'name': soup.find_all('h3', class_='b-fight-details__person-name')[0].text.strip(),
                'nickname': soup.find_all('p', class_='b-fight-details__person-title')[0].text.strip().replace('"', ''),
                'tale_of_the_tape': {},
                'striking': {},
                'grappling': {}
            }

            fighter_b = {
                'name': soup.find_all('h3', class_='b-fight-details__person-name')[1].text.strip(),
                'nickname': soup.find_all('p', class_='b-fight-details__person-title')[1].text.strip().replace('"', ''),
                'tale_of_the_tape': {},
                'striking': {},
                'grappling': {}
            }

            rows = soup.find_all('tr', class_='b-fight-details__table-row-preview')

            for row in rows[0:7]:
                key = row.find('td', class_='l-page_align_left').text.strip()
                vals = row.find_all('td')[1:]
                fighter_a['tale_of_the_tape'][key] = vals[0].text.strip()
                fighter_b['tale_of_the_tape'][key] = vals[1].text.strip()

            for row in rows[7:11]:
                key = row.find('td', class_='l-page_align_left').text.strip()
                vals = row.find_all('td')[1:]
                fighter_a['striking'][key] = vals[0].text.strip()
                fighter_b['striking'][key] = vals[1].text.strip()

            for row in rows[11:15]:
                key = row.find('td', class_='l-page_align_left').text.strip()
                vals = row.find_all('td')[1:]
                fighter_a['grappling'][key] = vals[0].text.strip()
                fighter_b['grappling'][key] = vals[1].text.strip()

            fighter_a_name = fighter_a['name']
            fighter_b_name = fighter_b['name']
            matched_odds_entry = None
            for entry in odds:
                if (entry['home_team'] == fighter_a_name and entry['away_team'] == fighter_b_name) or \
                        (entry['home_team'] == fighter_b_name and entry['away_team'] == fighter_a_name):
                    matched_odds_entry = entry
                    break

            fight_odds = []
            if matched_odds_entry:
                for bookmaker in matched_odds_entry.get('bookmakers', []):
                    h2h_market = next((m for m in bookmaker.get('markets', []) if m['key'] == 'h2h'), None)
                    if h2h_market:
                        outcomes = h2h_market['outcomes']
                        if matched_odds_entry['home_team'] == fighter_a_name:
                            a_odd = outcomes[0]['price']
                            b_odd = outcomes[1]['price']
                        else:
                            a_odd = outcomes[1]['price']
                            b_odd = outcomes[0]['price']

                        fight_odds.append({
                            'bookie_key': bookmaker['key'],
                            'bookie_title': bookmaker['title'],
                            fighter_a_name: a_odd,
                            fighter_b_name: b_odd
                        })

            fight_details = {
                'event_link': event_link,
                'event_name': event_name,
                'fighter_a': fighter_a,
                'fighter_b': fighter_b,
                'odds': fight_odds
            }
            fight_details_list.append(fight_details)
        else:
            print(f"Failed to retrieve page for {fight_url}: {response.status_code}")

    return fight_details_list