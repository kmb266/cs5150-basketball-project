import sys, json
from data_retriever import masterQuery
from stats_results import stats_calculation

def sampleForm():
    form = {
        "page": "players",
        "position": [],
        "team": [
        "COR"
        ],
        "opponent": [],
        "in": [],
        "out": [],
        "upOrDown": [
        "withIn",
        None
        ],
        "gametime": {
        "slider": {
          "start": {
            "clock": "20:00",
            "sec": -2400
          },
          "end": {
            "clock": "00:00",
            "sec": 0
          }
        },
        "sliderExtra": {
          "start": {
            "clock": "20:00",
            "sec": -2400
          },
          "end": {
            "clock": "00:00",
            "sec": 0
          }
        },
        "multipleTimeFrames": False
        },
        "location": {
        "home": True,
        "away": True,
        "neutral": True
        },
        "outcome": {
        "wins": True,
        "losses": True
        },
        "overtime": {
        "otSlider": {
          "start": {
            "clock": "5:00",
            "sec": -300
          },
          "end": {
            "clock": "0:00",
            "sec": 0
          }
        },
        "ot1": True,
        "ot2": True,
        "ot3": True,
        "ot4": True,
        "ot5": True,
        "ot6": True,
        "onlyQueryOT": False
        },
        "dates": {
        "start": 1509508800000,
        "end": 1525665600000
        }
    }
    return form

def getAverages(players_score, team_score):
    """
    Name: getAverages
    Returns: the average box score for each player
    Arguments:
    players_score: box score for each player in each game
    team_score: box score for the team in each game
    """
    #TODO : MIN, FG%, 3PT%, FT%
    attributes = ["FG", "FGA", "3PT", "FGA3", "FT", "FTA", "OREB", "DREB", "REB", 
    "PF", "AST", "TO", "BLK", "STL", "TP", "PTS", "MIN"]    
    advanced_attributes = ["Usage_Rate", "PIE", "Game_Score"]
    players_boxscore = []
    teams_boxscore = {}

    for values in players_score:
        games = values["games"]
        player = {"name" : values["name"], "team" : values["team"]}
        games_played = len(games)

        for attribute in attributes + advanced_attributes:
            for game, game_boxscore in games.items():
                if attribute in game_boxscore:
                    if attribute in player:
                        player[attribute] += game_boxscore[attribute]
                    else:
                        player[attribute] = game_boxscore[attribute]
            
            if attribute in player:
                player[attribute] = round(player[attribute] / games_played, 2)

        # FG% FT% 3PT%
        if "FG" in player and "FGA" in player and player["FGA"] != 0:
            player["FGPerc"] = round(player["FG"] / player["FGA"], 3)
        else:
            player["FGPerc"] = 0
        if "3PT" in player and "FGA" in player and player["FGA3"] != 0:
            player["FG3Perc"] = round(player["3PT"] / player["FGA3"], 3)
        else:
            player["FG3Perc"] = 0
        if "FT" in player and "FTA" in player and player["FTA"] != 0:
            player["FTPerc"] = round(player["FT"] / player["FTA"], 3)
        else:
            player["FTPerc"] = 0

        players_boxscore.append(player)

    for team_id, values in team_score.items():
        games = values["games"]
        team = {"team_id" : team_id}
        games_played = len(games)

        for attribute in attributes:
            for game, game_boxscore in games.items():
                if attribute in game_boxscore:
                    if attribute in team:
                        team[attribute] += game_boxscore[attribute]
                    else:
                        team[attribute] = game_boxscore[attribute]
            if attribute in team:
                team[attribute] = round(team[attribute] / games_played, 2)
        # FG% FT% 3PT%
        if "FG" in team and "FGA" in team and team["FGA"] != 0:
            team["FGPerc"] = round(team["FG"] / team["FGA"], 3)
        else:
            team["FGPerc"] = 0
        if "3PT" in team and "FGA" in team and team["FGA3"] != 0:
            team["FG3Perc"] = round(team["3PT"] / team["FGA3"], 3)
        else:
            team["FG3Perc"] = 0
        if "FT" in team and "FTA" in team and team["FTA"] != 0:
            team["FTPerc"] = round(team["FT"] / team["FTA"], 3)
        else:
            team["FTPerc"] = 0
        team["MIN"] = 200
        teams_boxscore[team_id] = team

    return (players_boxscore, teams_boxscore)


def filterResults(players_score, team_score, form):
    teamIds = form["team"]
    data = []
    for team_id in teamIds:
        team_boxscore = team_score[team_id]
        team_boxscore["name"] = "TEAM OVERALL"
        data.append(team_boxscore)
        for player in players_score:
            if player["team"] == team_id:
                data.append(player)
    return data

'''
retrieve the data from the backend
'''
def retrieveData(form):
    (players_score, team_score) = masterQuery(form)
    final = {"dataTab" : "players", "data" : players_score, "teamOverall" : team_score}
    stats_calculation(final)

    (players_score, team_score) = getAverages(players_score, team_score)
    players_score = filterResults(players_score, team_score, form)
    #data = json.dumps(data)
    final = {"dataTab" : "players", "data" : players_score, "teamOverall" : team_score}
    final = json.dumps(final)
    return final

def tidyForm(form):
    if ('season' in form) == False:
        form['season'] = None

    return form
'''
get the form information from the front end
'''
def getForm():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    form = getForm()
    #form = sampleForm()

    form = tidyForm(form)
    data = retrieveData(form)

    #return what we get
    print(data)
    sys.stdout.flush()

#start process
if __name__ == '__main__':
    main()
