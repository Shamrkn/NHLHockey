import requests
import json
import datetime
import time

teamID = '17'    #Detroit Redwings Team ID

baseurl = 'https://statsapi.web.nhl.com'

url = 'https://statsapi.web.nhl.com/api/v1/schedule'

now = datetime.datetime.today().strftime('%Y-%m-%d')


def checkForGameToday():
 

    payload = {'teamId': teamID, 'startDate': now, 'endDate': now}
    #===============================================================
    #==== Uncomment This to check daily schedule                ====
    r = requests.get(url, params=payload)
    #===============================================================
    #r = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=17&startDate=2018-02-02&endDate=2018-02-02')
    #print(r.url)
    parsed_json = json.loads(r.text)
    games = parsed_json['totalItems']

    if games == 0:
        #This is where I would show standings and next game date
        print("No Game Today!")
        findNextGame()
        #print(r.url)
    else:
        feed = parsed_json    
        getLiveGameData(feed)




#We have a game today
#TODO: Has the game started?

def getLiveGameData(parsed_json):
    #print("Game today!")
    gameID = parsed_json["dates"] [0] ["games"] [0] ["link"]
    #print(gameID)
    #print(parsed_json["teams"] [0] ["nextGameSchedule"])

    #==================================================================
    #==== Get Info About The Game From The Feed - display DET@CAR
    #==================================================================
    r = requests.get(baseurl+gameID)

    parsed_json = json.loads(r.text)

    #==================================================================
    #==== Parse out team abbreviations
    #==================================================================
    awayTeam = parsed_json["gameData"] ["teams"] ["away"] ["abbreviation"]
    homeTeam = parsed_json["gameData"] ["teams"] ["home"] ["abbreviation"]

    gameTeams = awayTeam + " @ " + homeTeam
    print(gameTeams)
    
    #==================================================================
    #==== Parse out Current Score
    #==================================================================
    homeScore = parsed_json["liveData"] ["linescore"] ["teams"] ["home"] ["goals"]
    awayScore = parsed_json["liveData"] ["linescore"] ["teams"] ["away"] ["goals"]
    score = awayTeam + ': ' + str(awayScore)
    print(score)
    score = homeTeam + ': ' + str(homeScore)
    print(score)
    period = parsed_json["liveData"] ["linescore"] ["currentPeriodOrdinal"]
    timeRemaining = parsed_json["liveData"] ["linescore"] ["currentPeriodTimeRemaining"]
    if timeRemaining == "Final":
        TRDisplay = timeRemaining
    else:
        TRDisplay = timeRemaining + " " + period
    print(TRDisplay)



def findNextGame():
    url = baseurl + '/api/v1/teams/17?expand=team.schedule.next'
    r = requests.get(url)
    parsed_json = json.loads(r.text)
    nextGameInfo = parsed_json["teams"] [0] ["nextGameSchedule"]
    if nextGameInfo["totalItems"] == 1 :
        nextGameData = nextGameInfo["dates"] [0] ["games"] [0] 
        nextGameDate = nextGameData["gameDate"]
        homeData = nextGameData["teams"] ["home"]
        awayData = nextGameData["teams"] ["away"]
        #convert string to date so we can maths
        #nextGameText = datetime.datetime.strptime(nextGameDate, '%Y-%m-%d')
        nextGameText = datetime.datetime.fromisoformat(nextGameDate[:19])
        
        #===============================================================================
        #==== Use maths to break out time until next game                          =====
        #===============================================================================
        delta = (nextGameText - datetime.datetime.utcnow())
        total_secs = delta.seconds
        hours = total_secs // 3600
        secs_remaining = total_secs % 3600
        minutes = secs_remaining // 60
        secs = secs_remaining % 60
        days = int(delta.days)
        hours = int(delta.seconds//3600)
        minutes = int(delta.seconds // 60) % 60
 
        print("days difference: " + str(days))
        print("hours difference: " + str(hours))
        print("minutes difference: " + str(minutes))
        print("seconds difference: " + str(secs))
        
        print(nextGameText)
    else:
        nextGameText = "Error"

def timeUntil():

if __name__ == '__main__':     #program starts from here
    checkForGameToday()