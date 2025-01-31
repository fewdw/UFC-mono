import requests
from bs4 import BeautifulSoup

def get_upcoming_events():
    url = "http://www.ufcstats.com/statistics/events/upcoming?page=all"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tbody = soup.find('tbody')

        events = []

        for row in tbody.find_all('tr', class_='b-statistics__table-row'):
            if row.find('a', class_='b-link'):
                event_name = row.find('a', class_='b-link').text.strip()
                event_date = row.find('span', class_='b-statistics__date').text.strip()
                event_link = row.find('a', class_='b-link')['href']
                event_location = row.find_all('td', class_='b-statistics__table-col')[1].text.strip()

                event = {
                    'event_name': event_name,
                    'event_date': event_date,
                    'event_link': event_link,
                    'event_location': event_location,
                    'event_happened': False,
                }
                events.append(event)

        return events
    else:
        Exception("Failed to fetch upcoming events")