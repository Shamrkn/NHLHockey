import requests
import json
import datetime
import time
import subprocess as sp

teamID = '17'    #Detroit Redwings Team ID

baseurl = 'https://statsapi.web.nhl.com'

url = 'https://statsapi.web.nhl.com/api/v1/schedule'

ngUpdateSeconds = 3600      #hourly cycle for refreshing next game data




def checkForGameToday():
 
    now = datetime.datetime.today().strftime('%Y-%m-%d')
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
    url = baseurl + '/api/v1/teams/' + str(teamID) + '?expand=team.schedule.next'
    r = requests.get(url)
    parsed_json = json.loads(r.text)
    nextGameInfo = parsed_json["teams"] [0] ["nextGameSchedule"]
    if nextGameInfo["totalItems"] == 1 :
        nextGameData = nextGameInfo["dates"] [0] ["games"] [0] 
        nextGameDate = nextGameData["gameDate"]
        homeData = nextGameData["teams"] ["home"]
        awayData = nextGameData["teams"] ["away"]
        #convert string to date so we can maths

        nextGameText = getFutureGameText(awayData, homeData)
        nextGameTime = datetime.datetime.fromisoformat(nextGameDate[:19])
        
        #===============================================================================
        #==== Use maths to break out time until next game                          =====
        #===============================================================================

        now = datetime.datetime.utcnow()

        i = 0
        while i < ngUpdateSeconds :
            days, hours, minutes, secs = timeUntil(nextGameTime, now)

            if days > 0 :
                print(str(days) + 'd ' + str(hours) + ':' + str(minutes) + ':' + str(secs))
            else :
                print(str(hours) + ':' + str(minutes) + ':' + str(secs))
            time.sleep(1)
            clear()

        print("days difference: " + str(days))
        print("hours difference: " + str(hours))
        print("minutes difference: " + str(minutes))
        print("seconds difference: " + str(secs))
        time.sleep(5)
        clear()
        
        print(nextGameTime)
    else:
        nextGameText = "Error"

def timeUntil(endDateTime, startDateTime):
        #===============================================================================
        #==== Use maths to break out time difference                               =====
        #===============================================================================
    delta = (endDateTime - startDateTime)
    total_secs = delta.seconds
    hours = total_secs // 3600
    secs_remaining = total_secs % 3600
    minutes = secs_remaining // 60
    secs = secs_remaining % 60
    days = int(delta.days)
    hours = int(delta.seconds//3600)
    minutes = int(delta.seconds // 60) % 60

    return days, hours, minutes, secs

def getFutureGameText(awayInfo, homeInfo):
    link = baseurl + awayInfo["team"] ["link"] + '?expand=team.stats'


def clear() :
    tmp = sp.call('clear', shell=True)

def loop() :
        #===============================================================================
        #==== main function that drives the program                                =====
        #===============================================================================
    checkForGameToday()

if __name__ == '__main__':     #program starts from here
    #checkForGameToday()
    try:
        loop()
    except KeyboardInterrupt: #when ctrl+c pressed, clean up resources
        clear()