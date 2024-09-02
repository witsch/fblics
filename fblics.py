from argparse import ArgumentParser
from bs4 import BeautifulSoup
from html import unescape
from ics import Calendar, Event
from json import loads, dumps
from requests import get


def parse_arguments():
    parser = ArgumentParser(description='convert kicker.de schedule to ICS')
    parser.add_argument('url', help='URL to fetch game schedules from')
    parser.add_argument('-j', '--json', action='store_true', help='dump all JSON-LD parts')
    return parser.parse_args()


def main():
    cal = Calendar()
    args = parse_arguments()
    resp = get(args.url, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for match in soup.find_all('script', type='application/ld+json'):
        data = loads(unescape(match.string))
        if args.json:
            print(dumps(data, indent=2))
        elif data['@type'] == 'SportsEvent':
            cal.events.add(Event(
                name=data['name'],
                begin=data['startDate'],
                duration=dict(hours=1, minutes=45),
                url='https://www.kicker.de' + data['url']))
    if not args.json:
        print(cal.serialize())
