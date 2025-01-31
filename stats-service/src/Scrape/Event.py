import datetime

import requests
from bs4 import BeautifulSoup


def scrape_event_fights(event_url):
    # Send a GET request to the event URL
    response = requests.get(event_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table body containing the fight data
        tbody = soup.find('tbody', class_='b-fight-details__table-body')

        # Initialize an empty list to store the fight data
        fights = []

        # Loop through each row in the table body
        for row in tbody.find_all('tr', class_='b-fight-details__table-row'):
            # Extract fighter A and fighter B names
            fighter_a = row.find_all('a', class_='b-link')[0].text.strip()
            fighter_b = row.find_all('a', class_='b-link')[1].text.strip()

            # Extract the weight class
            weight_class = row.find('p', class_='b-fight-details__table-text').text.strip()

            # Extract the fight link (using onclick attribute or data-link)
            fight_link = row.get('onclick')
            if fight_link:
                fight_link = fight_link.split("'")[1]  # Extract the URL inside the single quotes
            else:
                fight_link = row.get('data-link')

            # Create a dictionary for the fight and add it to the list
            fight = {
                'fighter_a': fighter_a,
                'fighter_b': fighter_b,
                'weight_class': weight_class,
                'fight_link': fight_link,
            }
            fights.append(fight)

        return fights
    else:
        print(f"Failed to retrieve the event page. Status code: {response.status_code}")
        return []