import requests
import json
import datetime

response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/17?expand=team.schedule.next')
data = response.json()
now = datetime.datetime.today().strftime('%Y-%m-%d')
print(now)
#print(type(data))
#print(data)
#print(response.content.decode("utf-8"))
#parsed_json = json.loads(response.text)
#except KeyboardInterrupt
#print(parsed_json["teams"] [0] ["nextGameSchedule"])