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
        default='http://www.ffc-turbine.de/ms01_buli1415.php',
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
    soup = BeautifulSoup(resp.text)
    container = soup.find(id='countrydivcontainer')
    description = container.text.strip().splitlines()[0]
    title = description.split(',')[0]
    events, info = '', None
    for tr in container.find_all('tr'):
        columns = tr.find_all('td')
        if len(columns) == 1:
            info = tr.text
        else:
            date, time, match, score = columns
            if args.filter is not None and args.filter not in match.text:
                continue
            start = datetime.strptime(date.text + time.text, '%d.%m.%Y%H:%M Uhr')
            end = start + timedelta(hours=1, minutes=45)
            events += event % dict(
                start=start.strftime(date_fmt),
                end=end.strftime(date_fmt),
                summary=match.text.replace(' - ', ' — '),
                description=description + r'\n' + info,
            )
    print(ics % dict(title=title, description=description, events=events))
