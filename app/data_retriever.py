from sqlalchemy import create_engine, desc
from db import Game, Team, Player, PlayerIn, TeamIn, Play
import json
import datetime

import parse_json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_, between



'''
Retrieve all the team names and ids. Should return a list of teams with the id and the name of each team.
'''
def getAllTeams():
    engine = create_engine('sqlite:///basketball.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    teams = session.query(Team).all()
    result = []
    for team in teams:
        team_obj = {"id": team.team_id, "text": team.name}
        result.append(team_obj)

    return json.dumps(result)
'''
    return [{"id" : 1502, "text" : "Cornell University"},
                {"id" : 1603, "text" : "Dartmouth College"},
                {"id" : 1902, "text" : "Princeton University"},
                {"id" : 1807, "text" : "Harvard University"},
                {"id" : 1697, "text" : "Yale University"}]
'''

'''
Retrieve all players for the team of the given id.
'''

def getAllPlayers(teamId):
    engine = create_engine('sqlite:///basketball.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    # team = session.query(Team).filter_by(teamId=teamId).first()
    players = session.query(Player).filter_by(team=teamId).all()
    result = []

    # Can't give jersey number in return because this is not stored uniquely by player, but rather by game
    for player in players:
        if player.name != "TEAM": # Don't include team's stats, though we might want to include this - check w/ client
            result.append({"id": player.id, "text": player.name})

    return json.dumps(result)
'''
  return [{"id" : 1502, "name" : "Cornell University"},
                {"id" : 1603, "name" : "Dartmouth College"},
                {"id" : 1902, "name" : "Princeton University"},
                {"id" : 1807, "name" : "Harvard University"},
                {"id" : 1697, "name" : "Yale University"}]
'''


def masterQuery(json_form):
    data = json.loads(json.dumps(json_form))

    #print(data)
    engine = create_engine('sqlite:///basketball.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    teamIds = data["team"]
    oppIds = data["opponent"]
    # player_query = session.query(Player).filter(or_(team= t_id for t_id in teamIds))
    # The player_query now has all the players for all the teams, though I'm not sure if we really need this

    # Games query selects all games where teams in team play against teams in opponent
    if oppIds:
        games_query = session.query(Game).filter(
            or_(
                (and_(Game.home.in_(teamIds), Game.visitor.in_(oppIds))),
                (and_(Game.visitor.in_(teamIds), Game.home.in_(oppIds)))
            )
        )
    else:
        games_query = session.query(Game).filter(
            or_(
                Game.home.in_(teamIds),
                Game.visitor.in_(teamIds)
            )
     )

    # If there's a season, get all games within that season
    seasons = data["season"]
    if seasons:
        # If the list of seasons isn't empty
        # Make a datetime from the season year number
        datetime_ranges = []
        for season in seasons:
            year = int(season)
            start = datetime.datetime(year-1, 6, 2) # Season starts on June 2 of prior year
            end = datetime.datetime(year, 6, 1)   # Season ends on June 1 of this year
            datetime_ranges.append([start, end])
        conds = []
        for d in datetime_ranges:
            conds.append(and_(Game.date>d[0], Game.date< d[1]))
        games_query = games_query.filter(or_(*conds)) # Pray that this works

    # So at this point we should only be looking at games within the seasons selected

    # At the very end, filter the plays by who's in and who's out

    # Get all the game ids of the valid games we've looked at
    selected_game_ids = [game.id for game in games_query.all()]

    plays_query = session.query(Play).filter(Play.game_id.in_(selected_game_ids))

    # At this point, we're looking at all the plays in all the games selected by filters

    # Now apply timing filters

    sec_start = data["gametime"]["slider"]["start"]["sec"]
    sec_end = data["gametime"]["slider"]["end"]["sec"]

    def time_converted(period, time):
        """
        Converts a period & time representation of time into seconds
        :param period:
        :param time:
        :return:
        """

        result = -2400 + ((period-1) * 1200) # Period 1 -> 2400, period 2 -> 1200
        mins_to_secs = 1200 - int(time[:2]) * 60 # 20 mins -> 0, 0 mins -> 1200
        secs_to_secs = int(time[3:])
        return result + mins_to_secs - secs_to_secs

    # TODO: Try and fix this following filter, but because it's not working, for now we substitute with Python filter
    # plays_query.filter(and_(time_converted(Play.period, Play.time) >= sec_start, time_converted(Play.period, Play.time) <= sec_end))
    plays = plays_query.all()
    plays = list(filter(lambda p: time_converted(p.period, p.time) >= sec_start and time_converted(p.period, p.time) <= sec_end, plays))

    # Lastly, filter the plays based on players in/out
    players_in = data["in"]
    players_out = data["out"]
    # plays = plays_query.all()

    def player_in(play, players):
        if play.h1 in players or \
            play.h2 in players or \
            play.h3 in players or \
            play.h4 in players or \
            play.h5 in players or \
            play.v1 in players or \
            play.v2 in players or \
            play.v3 in players or \
            play.v4 in players or \
                play.v5 in players:
                return True

    positions = data["position"]

    # Position filter: Only include players with the given positions - expected value is int list
    if positions:
        plays = list(filter(lambda p: session.query(Player).filter_by(id=p.player_id).first().position in positions, plays))

    # Lineup filters: Filter by players in/out of the game
    if players_in:
        plays = list(filter(lambda p: player_in(p, players_in), plays))

    if players_out:
        plays = list(filter(lambda p: not player_in(p, players_in), plays))

    # Score filters: Filter by point differentials
    up_or_down = data["upOrDown"]
    if up_or_down[1] is not None:
        if up_or_down[0] == "within":
            plays = list(filter(lambda p: abs(p.home_score - p.away_score) <= up_or_down[1], plays))
        elif up_or_down == "down":
            plays = list(filter(lambda p: p.away_score - p.home_score >= up_or_down[1], plays))
        elif up_or_down == "up":
            plays = list(filter(lambda p: p.home_score - p.away_score >= up_or_down[1], plays))




    def generate_box_score(plays):
        """
        Generates a box score for each player involved in the plays listed
        :param plays: The list of plays
        :return: A dict containing box scores for each player
        """
        attributes = ["FG", "FGA3", "3PT", "FTA", "FT", "TP", "OREB",
                "DREB", "REB", "AST", "STL", "BLK", "TO", "PF", "PTS"]
        players = {}
        teams = {}

        for play in plays:
            # Create player if its not in the list
            player_id = play.player_id
            if player_id is None:
                continue
            if player_id and player_id not in players:
                player = session.query(Player).filter_by(id=play.player_id).first()
                players[player_id] = {
                    "name" : player.name,
                    "team" : player.team,
                    "games" : {}
                }

                if player.team not in teams:
                    teams[player.team] = {
                        "games" : {}
                    }

            #Create game for the player if its not in the list
            game_id = play.game_id

            if game_id and game_id not in players[player_id]["games"]:
                players[player_id]["games"][game_id] = {
                    "FGA": 0.0,
                    "FG": 0.0,
                    "FGA3": 0.0,
                    "3PT": 0.0,
                    "FTA": 0.0,
                    "FT": 0.0,
                    "TP": 0.0,
                    "OREB": 0.0,
                    "DREB": 0.0,
                    "REB": 0.0,
                    "AST": 0.0,
                    "STL": 0.0,
                    "BLK": 0.0,
                    "TO": 0.0,
                    "PF": 0.0,
                    "PTS": 0.0,
                    "MIN": 0.0,
                    "LAST_IN_OR_OUT": "OUT", # Used to keep track of whether the last sub in this game was in or out
                    "SEEN": False, # Used to keep track of whether the player has been seen yet
                    "last_time": sec_start
                }

            team = players[player_id]["team"]
            if game_id and team and game_id not in teams[team]["games"]:
                teams[team]["games"][game_id] = {
                    "FGA": 0.0,
                    "FG": 0.0,
                    "FGA3": 0.0,
                    "3PT": 0.0,
                    "FTA": 0.0,
                    "FT": 0.0,
                    "TP": 0.0,
                    "OREB": 0.0,
                    "DREB": 0.0,
                    "REB": 0.0,
                    "AST": 0.0,
                    "STL": 0.0,
                    "BLK": 0.0,
                    "TO": 0.0,
                    "PF": 0.0,
                    "PTS": 0.0
                }

            if not players[player_id]["games"][game_id]["SEEN"]:
                players[player_id]["games"][game_id]["SEEN"] = True
                if play.action == "SUB" and play.type == "OUT":
                    players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "OUT"
                    players[player_id]["games"][game_id]["MIN"] = sec_start - time_converted(play.period, play.time)

                else:
                    players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "IN"
                    # players[player_id]["games"][game_id]["last_time"] = time_converted(play.period, play.time)


                # Player being seen in the game for the first time (includes sub in plays)
            # elif players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "OUT":
            #     players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "IN"
            #     # Get the difference between the last sub in and add this to MINS
            #     now = time_converted(play.period, play.time)
            #     players[player_id]["games"][game_id]["LAST_IN_OR_OUT"]["MINS"] += \
            #         players[player_id]["games"][game_id]["last_time"] - now
            #     players[player_id]["games"][game_id]["last_time"] = now



            if play.type == "3PTR":
                players[player_id]["games"][game_id]["FGA3"] += 1
                teams[team]["games"][game_id]["FGA3"] += 1
                if play.action == "GOOD":
                    players[player_id]["games"][game_id]["3PT"] += 1
                    players[player_id]["games"][game_id]["PTS"] += 3
                    teams[team]["games"][game_id]["3PT"] += 1
                    teams[team]["games"][game_id]["PTS"] += 3
            elif play.action == "SUB":
                if play.type == "IN":
                    players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "IN"
                    players[player_id]["games"][game_id]["SEEN"] = True
                    players[player_id]["games"][game_id]["last_time"] = time_converted(play.period, play.time)
                elif play.type == "OUT":
                    now = time_converted(play.period, play.time)
                    players[player_id]["games"][game_id]["MIN"] += \
                        players[player_id]["games"][game_id]["last_time"] - now
                    players[player_id]["games"][game_id]["last_time"] = now
                    players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "OUT"
            elif play.type == "JUMPER" or play.type == "LAYUP" or play.type == "DUNK":
                players[player_id]["games"][game_id]["FGA"] += 1
                teams[team]["games"][game_id]["FGA"] += 1
                if play.action == "GOOD":
                    players[player_id]["games"][game_id]["FG"] += 1
                    teams[team]["games"][game_id]["FG"] += 1
                    players[player_id]["games"][game_id]["PTS"] += 2
                    teams[team]["games"][game_id]["PTS"] += 2
            elif play.action == "REBOUND":
                players[player_id]["games"][game_id]["REB"] += 1
                teams[team]["games"][game_id]["REB"] += 1
                if play.type == "DEF":
                    players[player_id]["games"][game_id]["DREB"] += 1
                    teams[team]["games"][game_id]["DREB"] += 1
                elif play.type == "OFF":
                    players[player_id]["games"][game_id]["OREB"] += 1
                    teams[team]["games"][game_id]["OREB"] += 1
            elif play.action == "STEAL":
                players[player_id]["games"][game_id]["STL"] += 1
                teams[team]["games"][game_id]["STL"] += 1
            elif play.action == "BLOCK":
                players[player_id]["games"][game_id]["BLK"] += 1
                teams[team]["games"][game_id]["BLK"] += 1
            elif play.action == "TURNOVER":
                players[player_id]["games"][game_id]["TO"] += 1
                teams[team]["games"][game_id]["TO"] += 1
            elif play.action == "STEAL":
                players[player_id]["games"][game_id]["STL"] += 1
                teams[team]["games"][game_id]["STL"] += 1
            elif play.type == "FT":
                players[player_id]["games"][game_id]["FTA"] += 1
                teams[team]["games"][game_id]["FTA"] += 1
                if play.action == "GOOD":
                    players[player_id]["games"][game_id]["FT"] += 1
                    teams[team]["games"][game_id]["FT"] += 1
                    players[player_id]["games"][game_id]["PTS"] += 1
                    teams[team]["games"][game_id]["PTS"] += 1
            elif play.action == "ASSIST":
                players[player_id]["games"][game_id]["AST"] += 1
                teams[team]["games"][game_id]["AST"] += 1
            elif play.action == "FOUL":
                players[player_id]["games"][game_id]["PF"] += 1
                teams[team]["games"][game_id]["PF"] += 1

        # If we're done and the player was last subbed in, fix their minutes by subbing them out
        for player_id in players:
            for game_id in players[player_id]["games"]:
                if players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "IN":
                    players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "OUT"
                    players[player_id]["games"][game_id]["MIN"] += \
                        players[player_id]["games"][game_id]["last_time"] - sec_end # End of normal period game

        # TODO: Right now, we have total time in secs for each player per game in MIN, probably want to divide by 60

        return (players, teams)

    (box_score, teams) = generate_box_score(plays)
    return (box_score.values(), teams)

'''

            if play.player_id and play.player_id not in players:
                player = session.query(Player).filter_by(id=play.player_id).first()
                game = play.game_id
                team = player.team
                players[play.player_id] = {
                    "name": player.name,
                    "FGA": 0.0,
                    "FG": 0.0,
                    "FGA3": 0.0,
                    "3PT": 0.0,
                    "FTA": 0.0,
                    "FT": 0.0,
                    "TP": 0.0,
                    "OREB": 0.0,
                    "DREB": 0.0,
                    "REB": 0.0,
                    "AST": 0.0,
                    "STL": 0.0,
                    "BLK": 0.0,
                    "TO": 0.0,
                    "PF": 0.0,
                    "PTS": 0.0,
                    "games_played" : 1.0,
                    "last_game" : play.game_id,
                    "team" : team
                }
                if team not in team_score:
                    team_score[team] = {
                    "id": team,
                    "games_played" : 1.0,
                    "last_game" : play.game_id
                }
            elif play.player_id and play.player_id in box_score:
                if box_score[play.player_id]["last_game"] != play.game_id:
                    box_score[play.player_id]["games_played"] += 1
                    box_score[play.player_id]["last_game"] = play.game_id

                team = box_score[play.player_id]["team"]
                if team_score[team]["last_game"] != play.game_id:
                    team_score[team]["games_played"] += 1
                    team_score[team]["last_game"] = play.game_id

            if play.type == "3PTR":
                box_score[play.player_id]["FGA3"] += 1
                box_score[play.player_id]["FGA3"] += 1
                if play.action == "GOOD":
                    box_score[play.player_id]["3PT"] += 1
                    box_score[play.player_id]["PTS"] += 3
            elif play.type == "JUMPER" or play.type == "LAYUP" or play.type == "DUNK":
                box_score[play.player_id]["FGA"] += 1
                if play.action == "GOOD":
                    box_score[play.player_id]["FG"] += 1
                    box_score[play.player_id]["PTS"] += 2
            elif play.action == "REBOUND":
                box_score[play.player_id]["REB"] += 1
                if play.type == "DEF":
                    box_score[play.player_id]["DREB"] += 1
                elif play.type == "OFF":
                    box_score[play.player_id]["OREB"] += 1
            elif play.action == "STEAL":
                box_score[play.player_id]["STL"] += 1
            elif play.action == "BLOCK":
                box_score[play.player_id]["BLK"] += 1
            elif play.action == "TURNOVER":
                box_score[play.player_id]["TO"] += 1
            elif play.action == "STEAL":
                box_score[play.player_id]["STL"] += 1
            elif play.type == "FT":
                box_score[play.player_id]["FTA"] += 1
                if play.action == "GOOD":
                    box_score[play.player_id]["FT"] += 1
                    box_score[play.player_id]["PTS"] += 1
            elif play.action == "FOUL":
                box_score[play.player_id]["PF"] += 1

        return (box_score, team_score)

    (box_score, team_score) = generate_box_score(plays)
    return (box_score.values(), team_score)
'''


print(masterQuery({
  "page": "players",
  "position": [],
  "team": [
    "COR"
  ],
  "opponent": [
      "CENTPENN"
  ],
  "in": [],  # Kyle's id is 1 right now
  "out": [],
  "upOrDown": [
    "within",
    15
  ],
  "season": [
    "2018"
  ],
  "gametime": {
    "slider": {
      "start": {
        "clock": "20:00",
        "sec": -1200
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
}))


