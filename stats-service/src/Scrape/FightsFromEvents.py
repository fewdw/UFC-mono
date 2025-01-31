import requests
from bs4 import BeautifulSoup


def fight_from_events(event_url):
    response = requests.get(event_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tbody = soup.find('tbody', class_='b-fight-details__table-body')

        fight_links = []

        for row in tbody.find_all('tr', class_='b-fight-details__table-row'):
            fight_link = row.get('onclick')
            if fight_link:
                fight_link = fight_link.split("'")[1]
            else:
                fight_link = row.get('data-link')

            if fight_link:
                fight_links.append(fight_link)

        return fight_links
    else:
        print(f"Failed to retrieve the event page. Status code: {response.status_code}")
        return []
