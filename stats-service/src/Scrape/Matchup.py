import requests
from bs4 import BeautifulSoup


def scrape_fight_details(fight_url):
    response = requests.get(fight_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Event details
        event_link = soup.find('h2', class_='b-content__title').find('a')['href']
        event_name = soup.find('h2', class_='b-content__title').find('a').text.strip()

        # Fighter A details
        fighter_a = {
            'name': soup.find_all('h3', class_='b-fight-details__person-name')[0].text.strip(),
            'nickname': soup.find_all('p', class_='b-fight-details__person-title')[0].text.strip().replace('"', ''),
            'tale_of_the_tape': {},
            'striking': {},
            'grappling': {}
        }

        # Fighter B details
        fighter_b = {
            'name': soup.find_all('h3', class_='b-fight-details__person-name')[1].text.strip(),
            'nickname': soup.find_all('p', class_='b-fight-details__person-title')[1].text.strip().replace('"', ''),
            'tale_of_the_tape': {},
            'striking': {},
            'grappling': {}
        }

        # Extract and organize all stats
        rows = soup.find_all('tr', class_='b-fight-details__table-row-preview')

        # Tale of the tape (first 7 rows)
        for row in rows[0:7]:
            key = row.find('td', class_='l-page_align_left').text.strip()
            vals = row.find_all('td')[1:]
            fighter_a['tale_of_the_tape'][key] = vals[0].text.strip()
            fighter_b['tale_of_the_tape'][key] = vals[1].text.strip()

        # Striking stats (next 4 rows)
        for row in rows[7:11]:
            key = row.find('td', class_='l-page_align_left').text.strip()
            vals = row.find_all('td')[1:]
            fighter_a['striking'][key] = vals[0].text.strip()
            fighter_b['striking'][key] = vals[1].text.strip()

        # Grappling stats (next 4 rows)
        for row in rows[11:15]:
            key = row.find('td', class_='l-page_align_left').text.strip()
            vals = row.find_all('td')[1:]
            fighter_a['grappling'][key] = vals[0].text.strip()
            fighter_b['grappling'][key] = vals[1].text.strip()

        return {
            'event_link': event_link,
            'event_name': event_name,
            'fighter_a': fighter_a,
            'fighter_b': fighter_b
        }
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None