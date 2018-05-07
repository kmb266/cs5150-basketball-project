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
  "opponent": [
    "COL"
  ],
  "in": [],
  "out": [],
  "upOrDown": [
    "withIn",
    None
  ],
  "season": [
    "2018"
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
    "ot1": False,
    "ot2": False,
    "ot3": False,
    "ot4": False,
    "ot5": False,
    "ot6": False,
    "onlyQueryOT": False
  }
}
    return form

def getAverages(players_score, team_score):
    attributes = ["FG", "FGA3", "3PT", "FTA", "FT", "TP", "OREB",
                "DREB", "REB", "AST", "STL", "BLK", "TO", "PF", "PTS"]
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
                    player[attribute] = round(player[attribute] / games_played, 2)

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
                    team[attribute] = round(team[attribute] / games_played, 2)

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
    # form = sampleForm()

    form = tidyForm(form)
    data = retrieveData(form)

    #return what we get
    print data
    sys.stdout.flush()

#start process
if __name__ == '__main__':
    main()
