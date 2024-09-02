from argparse import ArgumentParser
from bs4 import BeautifulSoup
from html import unescape
from ics import Calendar, Event
from json import loads
from requests import get


def parse_arguments():
    parser = ArgumentParser(description='convert kicker.de schedule to ICS')
    parser.add_argument('url', help='URL to fetch game schedules from')
    return parser.parse_args()


def main():
    cal = Calendar()
    args = parse_arguments()
    resp = get(args.url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for match in soup.find_all('script', type='application/ld+json'):
        data = loads(unescape(match.string))
        if data['@type'] == 'SportsEvent':
            cal.events.add(Event(
                name=data['name'],
                begin=data['startDate'],
                duration=dict(hours=1, minutes=45),
                url='https://www.kicker.de' + data['url']))
    print(cal.serialize())
