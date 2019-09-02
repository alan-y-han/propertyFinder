import bs4
import requests
import time


def getPlaces(soup, places):
    for listing in soup.findAll('div', attrs={'class': 'listing-results-wrapper'}):
        url = listing.find('a', attrs={'class': 'photo-hover'})
        places.add(url.attrs['href'])


def getNextURL(soup):
    linkbar = soup.find('div', attrs={'class': 'paginate bg-muted'})
    links = linkbar.findAll('a')
    for link in links:
        if link.text == 'Next':
            return True, "https://www.primelocation.com" + link.attrs['href']
    return False, None


def scrapeURL(URL):
    places = set()

    soup = bs4.BeautifulSoup(requests.get(URL).text, features="html.parser")
    getPlaces(soup, places)

    while True:
        time.sleep(0.1)  # guard against bugs

        nextExists, URL = getNextURL(soup)
        if not nextExists:
            break

        print(URL)
        soup = bs4.BeautifulSoup(requests.get(URL).text, features="html.parser")
        getPlaces(soup, places)

    return places

if __name__ == '__main__':

    commonURL = "https://www.primelocation.com/to-rent/property/"

    locations = [
        "london/worship-street/ec2a-2ba/?",  # Principal Place (Amazon)
        "sw7-2az/?"                          # Imperial College
    ]

    params = [
        "beds_min=3",
        "duration=2200",  # max commute time (in seconds)
        "price_frequency=per_month",
        "price_max=3500",
        "results_sort=newest_listings",
        "search_source=travel-time",
        "transport_type=public_transport",
        "page_size=50"  # 100 seems to be the unofficial limit?
    ]

    placeSets = []

    for location in locations:
        URL = commonURL + location + "&".join(params)
        placeSets.append(scrapeURL(URL))

    print(set.intersection(*placeSets))
