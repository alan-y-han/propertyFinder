import time

import requests
import bs4


def getPlaces(soup, places):
    for listing in soup.findAll('div', attrs={'class': 'listing-results-wrapper'}):
        url = listing.find('a', attrs={'class': 'photo-hover'})
        places.add(url.attrs['href'])


def isNextButton(soup):
    linkbar = soup.find('div', attrs={'class': 'paginate bg-muted'})
    links = linkbar.findAll('a')
    for link in links:
        if link.text == 'Next':
            return True, "https://www.primelocation.com" + link.attrs['href']
    return False, None

    # page = soup.find('div', attrs={'class': 'paginate bg-muted'})
    # return "Next" in page.text


def getNextURL(soup):
    page = soup.find('div', attrs={'class': 'paginate bg-muted'})
    return "https://www.primelocation.com" + list(page.children)[-2].attrs['href']


def scrapeURL(URL):
    places = set()

    # URL = "https://www.primelocation.com/to-rent/property/london/worship-street/ec2a-2ba/?beds_min=3&price_max=3500&transport_type=public_transport&identifier=london%2Fworship-street%2Fec2a-2ba&duration=1800page_size%3D50&q=EC2A%202BA&results_sort=newest_listings&search_source=refine&radius=0&price_frequency=per_month&view_type=list&page_size=50&pn=13"
    soup = bs4.BeautifulSoup(requests.get(URL).text, features="html.parser")
    getPlaces(soup, places)

    while True:
        time.sleep(0.1)

        nextExists, URL = isNextButton(soup)
        if not nextExists:
            break

        print(URL)
        soup = bs4.BeautifulSoup(requests.get(URL).text, features="html.parser")
        getPlaces(soup, places)

    return places

if __name__ == '__main__':

    AmazonURL = "https://www.primelocation.com/to-rent/property/london/worship-street/ec2a-2ba/?beds_min=3&price_max=3500&transport_type=public_transport&identifier=london%2Fworship-street%2Fec2a-2ba&duration=2700page_size=50&q=EC2A%202BA&results_sort=newest_listings&search_source=refine&radius=0&price_frequency=per_month&view_type=list&page_size=50"
    AmazonPlaces = scrapeURL(AmazonURL)
    print(AmazonPlaces)

    ImperialURL = "https://www.primelocation.com/to-rent/property/sw7-2az/?beds_min=3&price_max=3500&transport_type=public_transport&identifier=london%2Fworship-street%2Fec2a-2ba&duration=2700page_size=50&q=EC2A%202BA&results_sort=newest_listings&search_source=refine&radius=0&price_frequency=per_month&view_type=list&page_size=50"
    ImperialPlaces = scrapeURL(ImperialURL)
    print(ImperialPlaces)

    commonPlaces = AmazonPlaces & ImperialPlaces

    print(commonPlaces)