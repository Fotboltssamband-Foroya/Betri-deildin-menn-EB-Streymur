import requests
from ics import Calendar, Event
from datetime import datetime
import pytz

# API endpoint
url = "https://comet.fsf.fo/data-backend/api/public/areports/run/0/25/?API_KEY=3cab2275c108ec56ece3e0cf3725a68ff061a76af0c2f8c8f16e0bad810126e9a8f6264d9520fc08e130c07fee874268c481886d2d4d6cb30aeb006e08bc6586"
response = requests.get(url)
data = response.json()

calendar = Calendar()
tz = pytz.timezone('Atlantic/Faroe')

for match in data.get('results', []):
    timestamp = match.get("matchDate")
    if not timestamp:
        continue

    description = match.get("matchDescription", "Ókend dystur")
    location = match.get("facility", "Ókend leikvøllur")
    match_status = match.get("matchStatus", "")
    round_number = match.get("round", "")
    competition = match.get("competitionType", "")

    start = datetime.fromtimestamp(timestamp / 1000, tz)

    event = Event()
    event.name = description
    event.begin = start
    event.duration = {"hours": 2}
    event.location = location
    event.description = (
        f"🏆 {competition}\n"
        f"🔁 Umfar: {round_number}\n"
        f"📊 Støða: {match_status}"
    )

    calendar.events.add(event)

with open('betri_deildin.ics', 'w', encoding='utf-8') as f:
    f.write(str(calendar))
