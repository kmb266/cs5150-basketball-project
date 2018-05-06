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
        team_obj = {"id": team.team_id, "name": team.name}
        result.append(team_obj)

    return json.dumps(result)

    return [{"id" : 1502, "name" : "Cornell University"},
                {"id" : 1603, "name" : "Dartmouth College"},
                {"id" : 1902, "name" : "Princeton University"},
                {"id" : 1807, "name" : "Harvard University"},
                {"id" : 1697, "name" : "Yale University"}]

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
            result.append({"id": player.id, "name": player.name})

    return json.dumps(result)


def masterQuery(json_form):
    data = json.loads(json.dumps(json_form))
    print(data)
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


    if players_in:
        plays = list(filter(lambda p: player_in(p, players_in), plays))

    if players_out:
        plays = list(filter(lambda p: not player_in(p, players_in), plays))


    def generate_box_score(plays):
        """
        Generates a box score for each player involved in the plays listed
        :param plays: The list of plays
        :return: A dict containing box scores for each player
        """
        box_score = {}
        for play in plays:
            if play.player_id and play.player_id not in box_score:
                player = session.query(Player).filter_by(id=play.player_id).first()
                box_score[play.player_id] = {
                    "name": player.name,
                    "fga": 0,
                    "fgm": 0,
                    "fga3": 0,
                    "fgm3": 0,
                    "fta": 0,
                    "ftm": 0,
                    "tp": 0,
                    "oreb": 0,
                    "dreb": 0,
                    "treb": 0,
                    "ast": 0,
                    "stl": 0,
                    "blk": 0,
                    "to": 0,
                    "pf": 0,
                    "pts": 0
                }

            if play.type == "3PTR":
                box_score[play.player_id]["fga3"] += 1
                if play.action == "GOOD":
                    box_score[play.player_id]["fgm3"] += 1
                    box_score[play.player_id]["pts"] += 3
            elif play.type == "JUMPER" or play.type == "LAYUP" or play.type == "DUNK":
                box_score[play.player_id]["fga"] += 1
                if play.action == "GOOD":
                    box_score[play.player_id]["fgm"] += 1
                    box_score[play.player_id]["pts"] += 2
            elif play.action == "REBOUND":
                box_score[play.player_id]["treb"] += 1
                if play.type == "DEF":
                    box_score[play.player_id]["dreb"] += 1
                elif play.type == "OFF":
                    box_score[play.player_id]["oreb"] += 1
            elif play.action == "STEAL":
                box_score[play.player_id]["stl"] += 1
            elif play.action == "BLOCK":
                box_score[play.player_id]["blk"] += 1
            elif play.action == "TURNOVER":
                box_score[play.player_id]["to"] += 1
            elif play.action == "STEAL":
                box_score[play.player_id]["stl"] += 1
            elif play.type == "FT":
                box_score[play.player_id]["fta"] += 1
                if play.action == "GOOD":
                    box_score[play.player_id]["ftm"] += 1
        return box_score

    box_score = generate_box_score(plays)
    return box_score


print(masterQuery({
  "page": "players",
  "position": [],
  "team": [
    "COR"
  ],
  "opponent": [
      "CENTPENN"
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
}))
