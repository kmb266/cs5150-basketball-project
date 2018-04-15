from db import Game, Team, Player, PlayerIn, TeamIn
from parser import parse_game_file
import os
import json

import parse_json

import datetime
from sqlalchemy import create_engine

engine = create_engine('sqlite:///basketball.db', echo=False)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def xml_to_database(xml_file):
    game_info = parse_game_file(xml_file)

    # Extract information for the Game table
    venue = game_info['venue']

    # Check if information for this game has already been added - if it has, then exit the function
    if session.query(Game).filter_by(date=venue['date'], home=venue['home_id']).first():
        return "ERR: Game data already documented. Aborting upload"

    g = Game(date=venue['date'], home=venue['home_id'], visitor=venue['vis_id'], isLeague=venue['is_league'],
             isPlayoff=venue['is_playoff'])
    session.add(g)

    # Extract information for Team table, adding the playing teams to the database if they don't already exist
    t1 = session.query(Team).filter_by(team_id=venue['home_id']).first() # Should only be one team with each id, so we can use first()
    t2 = session.query(Team).filter_by(team_id=venue['vis_id']).first()
    if not t1:
        t1 = Team(team_id=venue['home_id'], name=venue['home_name'])
        session.add(t1)
    if not t2:
        t2 = Team(team_id=venue['vis_id'], name=venue['vis_name'])
        session.add(t2)

    # Extract information for the TeamIn table
    """ TODO: Wrap everything in its own adder function, maybe put this in a file like py2db.py, which converts from
    the python dictionary to the database"""
    team1 = game_info['t1']
    spec = team1['special']
    stats = team1['stats']

    p1_vh = True if spec['vh'] == 'H' else False
    plays_in_team_one = TeamIn(team=team1["id"], game=g.id, fgm=stats['fgm'], fga=stats['fga'],
                                fgm3=stats['fgm3'], fga3=stats['fga3'], fta=stats['fta'], ftm=stats['ftm'],
                                tp=stats['tp'], blk=stats['blk'], stl=stats['stl'], ast=stats['ast'],
                                oreb=stats['oreb'], dreb=stats['dreb'], treb=stats['treb'], pf=stats['pf'],
                                tf=stats['tf'], to=stats['to'],
                                is_home=p1_vh, pts_to=spec['pts_to'], pts_paint=spec['pts_paint'],
                                pts_ch2=spec['pts_ch2'], pts_fastb=spec['pts_fastb'], pts_bench=spec['pts_bench'],
                                ties=spec['ties'], leads=spec['leads'], poss_count=spec['poss_count'],
                                poss_time=spec['poss_time'], score_count=spec['score_count'],
                                score_time=spec['score_time'])

    session.add(plays_in_team_one)

    team2 = game_info['t2']
    spec = team2['special']
    stats = team2['stats']

    p2_vh = True if spec['vh'] == 'H' else False

    plays_in_team_two = TeamIn(team=team2["id"], game=g.id, fgm=stats['fgm'], fga=stats['fga'],
                               fgm3=stats['fgm3'], fga3=stats['fga3'], fta=stats['fta'], ftm=stats['ftm'],
                               tp=stats['tp'], blk=stats['blk'], stl=stats['stl'], ast=stats['ast'],
                               oreb=stats['oreb'], dreb=stats['dreb'], treb=stats['treb'], pf=stats['pf'],
                               tf=stats['tf'], to=stats['to'],
                               is_home=p2_vh, pts_to=spec['pts_to'],
                               pts_paint=spec['pts_paint'],
                               pts_ch2=spec['pts_ch2'], pts_fastb=spec['pts_fastb'], pts_bench=spec['pts_bench'],
                               ties=spec['ties'], leads=spec['leads'], poss_count=spec['poss_count'],
                               poss_time=spec['poss_time'], score_count=spec['score_count'],
                               score_time=spec['score_time'])

    session.add(plays_in_team_two)
    session.commit()

    # Loop through Players and add them to the database if they don't already exist, repeat for team2
    # TODO: uniquely identifying a player is still hard...
    for player in team1['players']:
        p = session.query(Player).filter_by(name=player["name"], team=team1["id"]).first()
        if not p:
            # If the player's not already in the database add him
            p = Player(name=player["name"], team=team1["id"])
            session.add(p)
            session.commit()
        # Some players don't have stats for the game - we ignore those by checking arbitrarily for the fgm stat to exist
        # Example: Keion Green from CENTPENN
        if "fgm" in player:
            game_stats = PlayerIn(player=p.id, game=g.id, fgm=player["fgm"], fga=player["fga"],
                                  fgm3=player["fgm3"], fga3=player["fga3"], ftm=player["ftm"],
                                  fta=player["fta"], tp=player["tp"], blk=player["blk"], stl=player["stl"],
                                  ast=player["ast"], oreb=player["oreb"], dreb=player["dreb"],
                                  treb=player["treb"], pf=player["pf"], tf=player["tf"], to=player["to"],
                                  dq=player["dq"], number=player["uni"])
            session.add(game_stats)

        session.commit()
        # Add stats for the player for the game

        # Now do the same thing for team2

    for player in team2['players']:
        p = session.query(Player).filter_by(name=player["name"], team=team2["id"]).first()
        if not p:
            # If the player's not already in the database add him
            p = Player(name=player["name"], team=team2["id"])
            session.add(p)
            session.commit()
        # Some players don't have stats for the game - we ignore those by checking arbitrarily for the fgm stat to exist
        # Example: Keion Green from CENTPENN
        if "fgm" in player:
            game_stats = PlayerIn(player=p.id, game=g.id, fgm=player["fgm"], fga=player["fga"],
                                  fgm3=player["fgm3"], fga3=player["fga3"], ftm=player["ftm"],
                                  fta=player["fta"], tp=player["tp"], blk=player["blk"], stl=player["stl"],
                                  ast=player["ast"], oreb=player["oreb"], dreb=player["dreb"],
                                  treb=player["treb"], pf=player["pf"], tf=player["tf"], to=player["to"],
                                  dq=player["dq"], number=player["uni"])
            session.add(game_stats)
        session.commit()


def fill_all_xml():
    """
    Obtains all the XML files in the MBKB 2017-2018 XML directory and
    populates the database with game information.
    :return: None, database is updated
    """
    # TODO: Get directory path
    path = None
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            xml_to_database(filename)  # TODO: filename should be a relative path
    pass


def json_to_database(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)

    # skip files that do not have box score data
    if not data["gamepackageJSON"]["header"]["competitions"][0]["boxscoreAvailable"]:
        return

    parse_json.parse_game(data, session)
    parse_json.parse_teams(data, session)
    parse_json.parse_players(data, session)
    parse_json.parse_plays(data, session)

    session.commit()


# xml_to_database("MBK_0105.xml")
# json_to_database("../cached_json/ncb/playbyplay/400990128.json")
# global filename
for filename in os.listdir("../cached_json/ncb/playbyplay"):
    if filename == "400990128.json":
        continue
    json_to_database("../cached_json/ncb/playbyplay/" + filename)

