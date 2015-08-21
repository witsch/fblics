from argparse import ArgumentParser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from requests import get


event = """BEGIN:VEVENT
DTSTART:%(start)s
DTEND:%(end)s
DESCRIPTION:%(description)s
SUMMARY:%(summary)s
END:VEVENT
"""

ics = """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:%(title)s
X-WR-CALDESC:%(description)s
X-WR-TIMEZONE:Europe/Berlin
CALSCALE:GREGORIAN
%(events)s
END:VCALENDAR
"""

date_fmt = '%Y%m%dT%H%M%S'


def parse_arguments():
    parser = ArgumentParser(description='convert Frauen-Bundesliga '
        'schedule to iCalendar data exchange format')
    parser.add_argument('-u', '--url',
        default='http://www.kicker.de/news/fussball/frauen/bundesliga/frauen-bundesliga/2015-16/1-ffc-turbine-potsdam-3443/vereinstermine.html',
        help='URL to fetch game schedules from')
    parser.add_argument('-f', '--filter',
        help='filter calendar entries using the given pattern')
    parser.add_argument('-t', '--turbine',
        dest='filter', action='store_const', const='Turbine Potsdam',
        help='filter calendar entries for Turbine Potsdam')
    return parser.parse_args()


def main():
    args = parse_arguments()
    resp = get(args.url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    container = soup.find(id='ctrl_vereinstermine')
    description = container.text.strip().splitlines()[0]
    title = description.split('-')[0].strip()
    events, info = '', None
    for tr in container.find_all('tr'):
        columns = tr.find_all('td')
        if len(columns) == 7:
            match, _, info, date, location, _, _ = columns
            if args.filter is not None and args.filter not in match.text:
                continue
            if location.text == 'A':
                match = match.text.strip() + ' — ' + title
            else:
                match = title + ' — ' + match.text.strip()
            start = datetime.strptime(date.text[4:], '%d.%m.%y %H:%M')
            end = start + timedelta(hours=1, minutes=45)
            events += event % dict(
                start=start.strftime(date_fmt),
                end=end.strftime(date_fmt),
                summary=match,
                description=info.text.replace('Spt.', 'Spieltag'),
            )
    print(ics % dict(title=title, description=description, events=events))
