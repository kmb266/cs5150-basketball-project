from app.db import Game, Team, Player, PlayerIn, PlaysIn
from app.parser import parse_game_file

from datetime import datetime
from sqlalchemy import create_engine

engine = create_engine('sqlite:///basketball.db', echo=True)
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

    # Extract information for the PlaysIn table
    """ TODO: Wrap everything in its own adder function, maybe put this in a file like py2db.py, which converts from 
    the python dictionary to the database"""
    team1 = game_info['t1']
    spec = team1['special']
    stats = team1['stats']

    p1_vh = True if spec['vh'] == 'H' else False
    plays_in_team_one = PlaysIn(team=t1.team_id, game=g.id, fgm=stats['fgm'], fga=stats['fga'],
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

    plays_in_team_two = PlaysIn(team=t1.team_id, game=g.id, fgm=stats['fgm'], fga=stats['fga'],
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
    # for player in team1['players']:
    #     if session.query(Player).filter_by()



    print(team1)

xml_to_database("MBK_0105.xml")
