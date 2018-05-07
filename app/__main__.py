from db import Game, Team, Player, PlayerIn, TeamIn, Play

from parser import parse_game_file
import os
import json

import parse_json

import datetime
from sqlalchemy import create_engine, desc


engine = create_engine('sqlite:///basketball.db', echo=False)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def xml_to_database(xml_file):
    game_info = parse_game_file(xml_file)

    # Extract information for the Game table
    venue = game_info['venue']
    home = venue["home_id"]
    vis = venue["vis_id"]

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

    # Put in information on total game scores
    if team1['special']['vh'] == 'H':
        # team1 is the home team
        g.home_score = team1['stats']['score']
        g.visitor_score = team2['stats']['score']
    else:
        g.home_score = team2['stats']['score']
        g.visitor_score = team1['stats']['score']

    if team1['stats']['score'] > team2['stats']['score']:
        if team1['special']['vh'] == 'H':
            g.winner = team1['id']
            g.loser = team2['id']
        else:
            g.winner = team2['id']
            g.loser = team1['id']
    else:
        if team1['special']['vh'] == 'H':
            g.winner = team2['id']
            g.loser = team1['id']
        else:
            g.winner = team1['id']
            g.loser = team2['id']

    session.add(g)
    session.commit()

    # Loop through Players and add them to the database if they don't already exist, repeat for team2
    starters_team_1 = []
    for player in team1['players']:
        p = session.query(Player).filter_by(name=player["checkname"], team=team1["id"]).first()
        if not p:
            # If the player's not already in the database add him
            p = Player(name=player["checkname"], team=team1["id"])
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
            if "gs" in player:
                starters_team_1.append(p.id)
    session.commit()
        # Add stats for the player for the game

    # Now do the same thing for team2
    starters_team_2 = []
    for player in team2['players']:
        p = session.query(Player).filter_by(name=player["checkname"], team=team2["id"]).first()
        if not p:
            # If the player's not already in the database add him
            p = Player(name=player["checkname"], team=team2["id"])
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
            if "gs" in player:
                starters_team_2.append(p.id)
            session.add(game_stats)
    session.commit()
    # print("TEAM ONE STARTERS", starters_team_1)
    # print("TEAM TWO STARTERS", starters_team_2)

    if team1["id"] == home:
        home_on_court = starters_team_1
        away_on_court = starters_team_2
    else:
        home_on_court = starters_team_2
        away_on_court = starters_team_1

    # Now create a dummy play that initializes the starters
    starters_play = Play(game_id=g.id, period=1, time="20:00", scoring_play=False, shooting_play=False, home_score=0,
                         away_score=0, text="Starters", action="Starters", type="",
                         h1=home_on_court[0], h2=home_on_court[1], h3=
                         home_on_court[2], h4=home_on_court[3],
                         h5=home_on_court[4],
                         v1=away_on_court[0], v2=away_on_court[1], v3=away_on_court[2], v4=away_on_court[3],
                         v5=away_on_court[4])
    session.add(starters_play)
    session.commit()


    plays = game_info["plays"]
    last_v_score = 0
    last_h_score = 0
    for period in plays:
        for play in plays[period]:
            # print(play)
            player_id = session.query(Player).filter_by(name=play["checkname"], team=play["team"]).first().id # This is breaking on file GAME16 in 2014-2015 database
            # Update home_on_court and away_on_court as necessary
            if play["action"] == "SUB":
                if play["type"] == "OUT":
                    if player_id in home_on_court:
                        home_on_court.remove(player_id)
                    elif player_id in away_on_court:
                        away_on_court.remove(player_id)
                if play["type"] == "IN":
                    team = session.query(Player).filter_by(id=player_id).first().team
                    # print(team)
                    if team == home:
                        home_on_court.append(player_id)
                    else:
                        away_on_court.append(player_id)

            # TODO: make sure this loops in order of increasing period, dicts are unpredictable
            if play["action"] == "GOOD":
                # Update the last known score after someone scores
                last_v_score = play["vscore"]
                last_h_score = play["hscore"]
            this_play = Play(
                game_id=g.id, period=period, time=play["time"],
                scoring_play=play["action"] == "GOOD",
                shooting_play=(play["type"] == "LAYUP" or play["type"] == "3PTR" or play["type"] == "JUMPER") if "type" in play else False,
                home_score=last_h_score,
                away_score=last_v_score,
                text="",
                action=play["action"],
                type=play["type"] if "type" in play else "",
                player_id=player_id,
                h1=home_on_court[0] if len(home_on_court) > 0 else -1,
                h2=home_on_court[1] if len(home_on_court) > 1 else -1,
                h3=home_on_court[2] if len(home_on_court) > 2 else -1,
                h4=home_on_court[3] if len(home_on_court) > 3 else -1,
                h5=home_on_court[4] if len(home_on_court) > 4 else -1,
                v2=away_on_court[0] if len(away_on_court) > 0 else -1,
                v1=away_on_court[1] if len(away_on_court) > 1 else -1,
                v3=away_on_court[2] if len(away_on_court) > 2 else -1,
                v4=away_on_court[3] if len(away_on_court) > 3 else -1,
                v5=away_on_court[4] if len(away_on_court) > 4 else -1
            )
            session.add(this_play)
    session.commit()

    # TODO: loop through all the substitution plays, ordering by first the time and then the sub == out,
    # TODO: and then change the columns for the players in the game accordingly. Next, loop through again
    # TODO: now looking at all the non--sub plays, and assign them the same players as the last play
    # Now handle all substitutions, working backwards because sub outs are listed first
    # plays_of_interest = session.query(Play).filter_by(game_id=g.id).order_by(Play.period)\
    #     .order_by(desc(Play.time)).order_by(desc(Play.type)).all()
    #
    # out_ids = []
    # for play in plays_of_interest:
    #     if play.action == "SUB":
    #         print("PLAY INFORMATION", play.period, play.time, play.type)
    #         if play.type == "OUT":
    #             out_ids.append(play.player_id)
    #             # Find the player in the active players list, remove them
    #             if play.h1 == play.player_id:
    #                 play.h1 = -1
    #             if play.h2 == play.player_id:
    #                 play.h2 = -1
    #             if play.h3 == play.player_id:
    #                 play.h3 = -1
    #             if play.h4 == play.player_id:
    #                 play.h4 = -1
    #             if play.h5 == play.player_id:
    #                 play.h5 = -1
    #             if play.v1 == play.player_id:
    #                 play.v1 = -1
    #             if play.v2 == play.player_id:
    #                 play.v2 = -1
    #             if play.v3 == play.player_id:
    #                 play.v3 = -1
    #             if play.v4 == play.player_id:
    #                 play.v4 = -1
    #             if play.v5 == play.player_id:
    #                 play.v5 = -1
    #         if play.type == "IN":
    #             # Find the first open slot
    #             # TODO: will this make issues  with playera from team 1 subbing out and player b from team2 subbing in?
    #             if play.h1 in out_ids:
    #                 out_ids.remove(play.h1)
    #                 play.h1 = play.player_id
    #             elif play.h2 in out_ids:
    #                 out_ids.remove(play.h2)
    #                 play.h2 = play.player_id
    #             elif play.h3 in out_ids:
    #                 out_ids.remove(play.h3)
    #                 play.h3 = play.player_id
    #             elif play.h4 in out_ids:
    #                 out_ids.remove(play.h4)
    #                 play.h4 = play.player_id
    #             elif play.h5 in out_ids:
    #                 out_ids.remove(play.h5)
    #                 play.h5 = play.player_id
    #             elif play.v1 in out_ids:
    #                 out_ids.remove(play.v1)
    #                 play.v1 = play.player_id
    #             elif play.v2 in out_ids:
    #                 out_ids.remove(play.v2)
    #                 play.v2 = play.player_id
    #             elif play.v3 in out_ids:
    #                 out_ids.remove(play.v3)
    #                 play.v3 = play.player_id
    #             elif play.v4 in out_ids:
    #                 out_ids.remove(play.v4)
    #                 play.v4 = play.player_id
    #             elif play.v5 in out_ids:
    #                 out_ids.remove(play.v5)
    #                 play.v5 = play.player_id
    #         session.add(play)
    #         session.commit()


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
#
# xml_to_database("MBK_0105.xml")
# print("FILE 1 DONE")
# xml_to_database("MBK_0112.xml")
# print("FILE 2 DONE")
# xml_to_database("MBK_0113.xml")
# print("FILE 3 DONE")
# xml_to_database("MBK_0120.xml")
# print("FILE 4 DONE")
# xml_to_database("MBK_0127.xml")
# print("FILE 5 DONE")
# xml_to_database("MBK_1110.xml")
# print("FILE 6 DONE")
# xml_to_database("MBK_1113.xml")
# print("FILE 7 DONE")
# xml_to_database("MBK_1117.xml")
# print("FILE 8 DONE")
# xml_to_database("MBK_1119.xml")
# print("FILE 9 DONE")
# xml_to_database("MBK_1124.xml")
# print("FILE 10 DONE")
# xml_to_database("MBK_1127.xml")
# print("FILE 11 DONE")
# xml_to_database("MBK_1202.xml")
# print("FILE 12 DONE")
# xml_to_database("MBK_1216.xml")
# print("FILE 13 DONE")
# xml_to_database("MBK_1220.xml")
# print("FILE 14 DONE")
# xml_to_database("MBK_1223.xml")
# print("FILE 15 DONE")
# xml_to_database("MBK_1228.xml")
# print("FILE 16 DONE")
# xml_to_database("MBK_1230.xml")
# print("FILE 17 DONE")




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
# # global filename
# for filename in os.listdir("../cached_json/ncb/playbyplay"):
#     if filename == "400990128.json":
#         continue
#     json_to_database("../cached_json/ncb/playbyplay/" + filename)


# This loops populates the database using all the xml files
for dir in os.listdir("../xml_data"):
    # print("In directory: {}\n----\n".format(dir))  # TODO: Comment out for production
    for filename in os.listdir("../xml_data/{}".format(dir)):
        if filename.endswith(".xml"):
            fl = "../xml_data/{}/{}".format(dir, filename)
            # print("Trying to populate data from {}".format(fl))
            try:
                xml_to_database(fl)
            except AttributeError:
                print("ERROR: AttributeError in file {}".format(fl))
            except Exception as ex:
                print("ERROR: {} in file {} | Arguments: {}".format(type(ex).__name__, fl, ex.args))


            # print("Finished populating data from {}".format(fl)) # TODO: Comment out for production