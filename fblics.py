from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from requests import get


event = """BEGIN:VEVENT
DTSTART:%(start)s
DTEND:%(end)s
DESCRIPTION:1. Frauen-Fußball-Bundesliga\\n%(description)s
SUMMARY:%(summary)s
END:VEVENT
"""

ics = """BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:Frauen-Bundesliga
X-WR-CALDESC:1. Frauen-Fußball-Bundesliga
X-WR-TIMEZONE:Europe/Berlin
CALSCALE:GREGORIAN
%s
END:VCALENDAR
"""

date_fmt = '%Y%m%dT%H%M%S'


def main():
    resp = get('http://www.ffc-turbine.de/ms01_buli1415.php')
    soup = BeautifulSoup(resp.text)
    container = soup.find(id='countrydivcontainer')
    events, description = '', None
    for tr in container.find_all('tr'):
        columns = tr.find_all('td')
        if len(columns) == 1:
            description = tr.text
        else:
            date, time, match, score = columns
            start = datetime.strptime(date.text + time.text, '%d.%m.%Y%H:%M Uhr')
            end = start + timedelta(hours=1, minutes=45)
            events += event % dict(
                start=start.strftime(date_fmt),
                end=end.strftime(date_fmt),
                summary=match.text.replace(' - ', ' — '),
                description=description,
            )
    print(ics % events)
