import requests
from bs4 import BeautifulSoup
from src.Request.Odds import get_odds
from src.Scrape.FightsFromEvents import scrape_fight_links


def scrape_fight_card(event_url):
    fight_urls = scrape_fight_links(event_url)
    odds = get_odds()
    fight_details_list = []

    for fight_url in fight_urls:
        try:
            response = requests.get(fight_url)
            if response.status_code != 200:
                print(f"Failed to retrieve page for {fight_url}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract event details
            event_title = soup.find('h2', class_='b-content__title')
            if not event_title:
                continue

            event_link_tag = event_title.find('a')
            if event_link_tag:
                event_link = event_link_tag.get('href', '')
                event_name = event_link_tag.text.strip()
            else:
                event_link = ''
                event_name = ''

            fighter_names = soup.find_all('h3', class_='b-fight-details__person-name')
            if len(fighter_names) < 2:
                print(f"Incomplete fighter data for {fight_url}")
                continue

            nicknames = soup.find_all('p', class_='b-fight-details__person-title')
            fighter_a = {
                'name': fighter_names[0].text.strip(),
                'nickname': nicknames[0].text.strip().replace('"', '') if len(nicknames) > 0 else '',
                'tale_of_the_tape': {},
                'striking': {},
                'grappling': {}
            }

            fighter_b = {
                'name': fighter_names[1].text.strip(),
                'nickname': nicknames[1].text.strip().replace('"', '') if len(nicknames) > 1 else '',
                'tale_of_the_tape': {},
                'striking': {},
                'grappling': {}
            }

            rows = soup.find_all('tr', class_='b-fight-details__table-row-preview')

            for row in rows[0:7] if len(rows) >= 7 else []:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    key = cells[0].text.strip()
                    fighter_a['tale_of_the_tape'][key] = cells[1].text.strip()
                    fighter_b['tale_of_the_tape'][key] = cells[2].text.strip()

            # Striking (next 4 rows)
            for row in rows[7:11] if len(rows) >= 11 else []:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    key = cells[0].text.strip()
                    fighter_a['striking'][key] = cells[1].text.strip()
                    fighter_b['striking'][key] = cells[2].text.strip()

            for row in rows[11:15] if len(rows) >= 15 else []:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    key = cells[0].text.strip()
                    fighter_a['grappling'][key] = cells[1].text.strip()
                    fighter_b['grappling'][key] = cells[2].text.strip()

            fighter_a_name = fighter_a['name']
            fighter_b_name = fighter_b['name']
            fight_odds = []

            for entry in odds:
                if ('home_team' in entry and 'away_team' in entry and
                        ((entry['home_team'] == fighter_a_name and entry['away_team'] == fighter_b_name) or
                         (entry['home_team'] == fighter_b_name and entry['away_team'] == fighter_a_name))):
                    for bookmaker in entry.get('bookmakers', []):
                        h2h_market = next((m for m in bookmaker.get('markets', []) if m['key'] == 'h2h'), None)
                        if h2h_market:
                            outcomes = h2h_market['outcomes']
                            if entry['home_team'] == fighter_a_name:
                                a_odd = outcomes[0]['price'] if len(outcomes) > 0 else None
                                b_odd = outcomes[1]['price'] if len(outcomes) > 1 else None
                            else:
                                a_odd = outcomes[1]['price'] if len(outcomes) > 1 else None
                                b_odd = outcomes[0]['price'] if len(outcomes) > 0 else None

                            if a_odd is not None and b_odd is not None:
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

        except Exception as e:
            print(f"Error processing {fight_url}: {str(e)}")
            continue

    return {
        "event_link": event_link,
        "event_name": event_name,
        "fights": fight_details_list
    }