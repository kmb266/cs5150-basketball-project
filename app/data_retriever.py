from sqlalchemy import create_engine, desc
from db import Game, Team, Player, PlayerIn, TeamIn, Play
import json
import datetime

import parse_json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_, between




def getAllTeams():
    '''
    Retrieve all the team names and ids. Should return a list of teams with the id and the name of each team.
    '''
    which_db = "json"
    # To fetch all team names, we try and use the json database. If this does not exist, default to XML

    try:
        engine = create_engine('sqlite:///basketball_json.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        teams = session.query(Team).all()
    except:
        which_db = "xml"
        engine = create_engine('sqlite:///basketball_xml.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        teams = session.query(Team).all()

    if which_db == "json" and len(teams) == 0:
            which_db = "xml"
            engine = create_engine('sqlite:///basketball_xml.db', echo=False)
            Session = sessionmaker(bind=engine)
            session = Session()
            teams = session.query(Team).all()

    result = []
    for team in teams:
        team_obj = {"id": team.team_id, "text": team.name}
        result.append(team_obj)

    return json.dumps(result)


def getAllPlayers(teamId):
    """
    Retrieve all players for the team of the given id.
    """
    if teamId == "COR":
        engine = create_engine('sqlite:///basketball_xml.db', echo=False)
    else:
        engine = create_engine('sqlite:///basketball_json.db', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()
    players = session.query(Player).filter_by(team=teamId).all()
    result = []

    # Can't give jersey number in return because this is not stored uniquely by player, but rather by game
    for player in players:
        if player.name != "TEAM": # Don't include team's stats, though we might want to include this - check w/ client
            result.append({"id": player.id, "text": player.name})

    return json.dumps(result)


def masterQuery(json_form):
    data = json.loads(json.dumps(json_form))
    teamIds = data["team"]
    oppIds = data["opponent"]

    # Pick what DB you're using based on the search criteria
    if (len(teamIds) == 1 and teamIds[0] == "COR") or (len(oppIds) == 1 and oppIds[0] == "COR"):
        engine = create_engine('sqlite:///basketball_xml.db', echo=False)
    else:
        engine = create_engine('sqlite:///basketball_json.db', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Games query selects all games where teams in team play against teams in opponent
    if oppIds:
        db_contains_opp = True
        for opp in oppIds:
            o = session.query(Team).filter_by(team_id=opp).first()
            if not o:
                db_contains_opp = False
                return {}, {}

        if db_contains_opp:
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
    if "season" in data:
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

    # If there are date filters, use them to restrict the set of filtered games
    if "dates" in data:
        dates = data["dates"]
        start = datetime.datetime.fromtimestamp(dates["start"]/1000.0)
        end = datetime.datetime.fromtimestamp(dates["end"]/1000.0)
        games_query = games_query.filter(and_(Game.date >= start, Game.date <= end))

    # Filter out games based on wins/losses
    outcome = data["outcome"]
    if outcome["wins"] is False:
        # Only show losses
        games_query = games_query.filter(Game.loser.in_(teamIds))
    if outcome["losses"] is False:
        # Only show wins
        games_query = games_query.filter(Game.winner.in_(teamIds))

    # Filter out games based on location
    loc = data["location"]
    if loc["home"] is False:
        # TODO: no support for neutral
        # Filter out any games where the selected team was a home team
        games_query = games_query.filter(Game.home.in_(oppIds))
    if loc["away"] is False:
        games_query = games_query.filter(Game.home.in_(teamIds))

    # Get all the game ids of the valid games we've looked at
    selected_game_ids = [game.id for game in games_query.all()]

    # Get all the plays for this game
    plays_query = session.query(Play).filter(Play.game_id.in_(selected_game_ids))

    # Filter by time periods in regulation time and then OT
    # We begin by collecting the set of times we want to filter by
    time_periods = []
    sec_start = data["gametime"]["slider"]["start"]["sec"]
    sec_end = data["gametime"]["slider"]["end"]["sec"]
    time_periods.append([sec_start, sec_end])

    if data["gametime"]["multipleTimeFrames"] is True:
        sec_start_2 = data["gametime"]["sliderExtra"]["start"]["sec"]
        sec_end_2 = data["gametime"]["sliderExtra"]["start"]["sec"]
        time_periods.append([sec_start_2, sec_end_2])

    # Overtime filter
    if "overtime" in data["overtime"]:
        overtimes = data["overtime"]
        if overtimes["onlyQueryOT"] is True:
            plays_query = plays_query.filter(Play.period > 2)
        valid_ot_periods = []
        for key in overtimes:
            if key != "onlyQueryOT" or key != "otSlider":
                if overtimes[key] is True:
                    valid_ot_periods.append(key[2:])
        if valid_ot_periods:
            for period in valid_ot_periods:
                start = overtimes["otSlider"]["start"]["sec"] + (period - 3) * 300
                end = overtimes["otSlider"]["end"]["sec"] + + (period - 3) * 300
                time_periods.append([start, end])

    # Now we apply filters based on the set of times generated above
    time_period_conds = []
    for time in time_periods:
        time_period_conds.append(and_(Play.time_converted >= time[0], Play.time_converted <= time[1]))
    if time_period_conds:
        plays_query = plays_query.filter(or_(*time_period_conds))  # Pray that this works

    # Obtain the actual plays so that we can use python list filtering rather than database querying
    # TODO: Doing this could decrease efficiency
    plays = plays_query.all()

    # Filter the plays based on players in/out
    players_in = data["in"]
    players_out = data["out"]

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

    def player_out(play, players):
        if play.h1 not in players and \
            play.h2 not in players and \
            play.h3 not in players and \
            play.h4 not in players and \
            play.h5 not in players and \
            play.v1 not in players and \
            play.v2 not in players and \
            play.v3 not in players and \
            play.v4 not in players and \
                play.v5 in players:
                return True


    positions = data["position"]

    # Position filter: Only include players with the given positions - expected value is int list
    if positions:
        positions = list(map(lambda p: int(p), positions))
        plays = list(filter(lambda p: session.query(Player).filter_by(id=p.player_id).first().position in positions, plays))

    # Lineup filters: Filter by players in/out of the game
    if players_in:
        players_in = list(map(lambda p: int(p), players_in))
        plays = list(filter(lambda p: player_in(p, players_in), plays))

    if players_out:
        players_out = list(map(lambda p: int(p), players_out))
        plays = list(filter(lambda p: player_out(p, players_out), plays)) # TODO: Verify logic in this line

    # Score filters: Filter by point differentials
    up_or_down = data["upOrDown"]
    if up_or_down[1] is not None:
        def filter_plays_differential(p, up_or_down, amt):
            g = session.query(Game).filter_by(id=p.game_id).first()
            if g.home in teamIds:
                # If the team we're looking for is home team this play, base calculations off that
                if up_or_down == "up":
                    return p.home_score - p.away_score > amt
                elif up_or_down == "down":
                    return p.home_score - p.away_score <= amt
            else:
                # Otherwise the team we're looking for is away team this play
                if up_or_down == "up":
                    return p.away_score - p.home_score > amt
                elif up_or_down == "down":
                    return p.away_score - p.home_score <= amt
            return False

        if up_or_down[0] == "within":
            plays = list(filter(lambda p: abs(p.home_score - p.away_score) <= up_or_down[1], plays))
        elif up_or_down == "down":
            plays = list(filter(lambda p: filter_plays_differential(p, "down", up_or_down[1]), plays))
        elif up_or_down == "up":
            plays = list(filter(lambda p: filter_plays_differential(p, "up", up_or_down[1]), plays))

    def generate_box_score(plays):
        """
        Generates a box score for each player involved in the plays listed
        :param plays: The list of plays
        :return: A dict containing box scores for each player
        TODO: this is horribly slow
        """
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
                    "games": {}
                }

                if player.team not in teams:
                    teams[player.team] = {
                        "games": {}
                    }

            # Create game for the player if its not in the list
            game_id = play.game_id

            g = session.query(Game).filter_by(id=game_id).first()

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
                    "last_time": sec_start,
                    "home": g.home,
                    "away": g.visitor
                }

            team = players[player_id]["team"]
            if game_id not in teams[team]["games"]:
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
                    players[player_id]["games"][game_id]["MIN"] = (sec_start - play.time_converted)/60

                else:
                    players[player_id]["games"][game_id]["LAST_IN_OR_OUT"] == "IN"

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
                    players[player_id]["games"][game_id]["last_time"] = play.time_converted
                elif play.type == "OUT":
                    now = play.time_converted
                    players[player_id]["games"][game_id]["MIN"] += \
                        (players[player_id]["games"][game_id]["last_time"] - now)/60
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

        return players, teams


    (box_score, teams) = generate_box_score(plays)
    return box_score.values(), teams



# print(masterQuery({
#   "page": "players",
#   "position": [],
#   "team": ["COR"],
#   "opponent": [],
#   "in": [1],
#   "out": [9, 11],
#   "upOrDown": [
#     "withIn",
#     None
#   ],
#   "gametime": {
#     "slider": {
#       "start": {
#         "clock": "20:00",
#         "sec": -1200
#       },
#       "end": {
#         "clock": "00:00",
#         "sec": 0
#       }
#     },
#     "sliderExtra": {
#       "start": {
#         "clock": "20:00",
#         "sec": -1200
#       },
#       "end": {
#         "clock": "00:00",
#         "sec": 0
#       }
#     },
#     "multipleTimeFrames": False
#   },
#   "location": {
#     "home": True,
#     "away": True,
#     "neutral": True
#   },
#   "outcome": {
#     "wins": True,
#     "losses": True
#   },
#   "overtime": {
#     "otSlider": {
#       "start": {
#         "clock": "5:00",
#         "sec": 0
#       },
#       "end": {
#         "clock": "0:00",
#         "sec": 300
#       }
#     },
#     "ot1": False,
#     "ot2": False,
#     "ot3": False,
#     "ot4": False,
#     "ot5": False,
#     "ot6": False,
#     "onlyQueryOT": False
#   },
#   "dates": {
#     "start": 1510508800000,
#     "end": 1525665600000
#   }
# }))
