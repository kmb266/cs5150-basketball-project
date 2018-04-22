import datetime
from db import Game, Team, Player, PlayerIn, TeamIn, Play

def parse_game(data, session):
    """
    adds an entry to the Game table
    returns game_id
    """
    competitions = data["gamepackageJSON"]["header"]["competitions"][0]

    # unique game ID provided by ESPN
    game_id = data["gameId"]

    # date of the game in datetime format
    date = competitions["date"]
    date = datetime.datetime.strptime("2017-11-26T19:00Z", '%Y-%m-%dT%H:%MZ') - datetime.timedelta(hours=4)

    # the id's of the two teams playing
    team_0 = competitions["competitors"][0]["team"]["abbreviation"]
    team_1 = competitions["competitors"][1]["team"]["abbreviation"]

    # parse home and away teams, as well as game score
    if competitions["competitors"][0]["homeAway"] == "home":
        home, visitor = team_0, team_1
        home_score = intf(competitions["competitors"][0]["score"])
        visitor_score = intf(competitions["competitors"][1]["score"])
    else:
        home, visitor = team_1, team_0
        home_score = intf(competitions["competitors"][1]["score"])
        visitor_score = intf(competitions["competitors"][0]["score"])

    # parse winner and loser
    if competitions["competitors"][0]["winner"]:
        winner, loser = team_0, team_1
    else:
        winner, loser = team_1, team_0

    # TODO: isPlayoff the same as isTournament?
    isLeague = competitions["conferenceCompetition"]
    # isPlayoff = data["gamepackageJSON"]["header"]["league"]["isTournament"]

    g = Game(id=game_id,date=date,home=home,visitor=visitor,winner=winner,loser=loser,
        home_score=home_score,visitor_score=visitor_score,isLeague=isLeague)

    session.add(g)
    # session.commit()


import datetime
from db import Game, Team, Player, PlayerIn, TeamIn, Play

def parse_teams(data, session):
    game_id = data["gameId"]

    for team in data["gamepackageJSON"]["boxscore"]["players"]:
        team_id = team["team"]["abbreviation"]
        team_name = team["team"]["shortDisplayName"]

        # Only add team if they are not yet in the db
        t = session.query(Team).filter_by(team_id=team_id).first()
        if not t:
            t = Team(team_id=team_id, name=team_name)
            session.add(t)

        s = parse_stats(team["statistics"][0]["totals"])
        team_stats = TeamIn(team=team_id,game=game_id,fgm=s["fgm"],fga=s["fga"],
            fgm3=s["fgm3"],fga3=s["fga3"],ftm=s["ftm"],fta=s["fta"],tp=s["tp"],
            blk=s["blk"],stl=s["stl"],ast=s["ast"],oreb=s["oreb"],dreb=s["dreb"],
            treb=s["treb"],pf=s["pf"],to=s["to"])
        session.add(team_stats)
        # missing technical fouls, can get from team data

    # session.commit()

import datetime
from db import Game, Team, Player, PlayerIn, TeamIn, Play

def parse_players(data, session):
    game_id = data["gameId"]
    players = data["gamepackageJSON"]["boxscore"]["players"]

    # for each of the two teams
    for team in players:
        team_id = team["team"]["abbreviation"]
        # for every player on that team
        for athlete in team["statistics"][0]["athletes"]:
            athlete_id = intf(athlete["athlete"]["id"])
            athlete_name = athlete["athlete"]["displayName"]
            position = athlete["athlete"]["position"]["displayName"]
            jersey_num = intf(athlete["athlete"]["jersey"])

            # only add player if they are not yet in db, and they played in the game
            p = session.query(Player).filter_by(name=athlete_name, team=team_id).first()
            if (not p) and (not athlete["didNotPlay"]):
                p = Player(name=athlete_name, position=position, team=team_id)
                session.add(p)

            # if they played in the game, add their game stats
            if not athlete["didNotPlay"]:
                # s represents the parsed stats
                s = parse_stats(athlete["stats"])
                player_stats = PlayerIn(game=game_id,player=athlete_id,number=jersey_num,
                    mins=s["mins"],fgm=s["fgm"],fga=s["fga"],fgm3=s["fgm3"],
                    fga3=s["fga3"],ftm=s["ftm"],fta=s["fta"],tp=s["tp"],
                    blk=s["blk"],stl=s["stl"],ast=s["ast"],oreb=s["oreb"],
                    dreb=s["dreb"],treb=s["treb"],pf=s["pf"],to=s["to"])
                session.add(player_stats)

    # session.commit()

import datetime
from db import Game, Team, Player, PlayerIn, TeamIn, Play

def parse_plays(data, session):
    game_id = data["gameId"]
    for play in data["gamepackageJSON"]["plays"]:
        play_id = intf(play["id"])
        period = play["period"]["number"]
        time = play["clock"]["displayValue"]
        scoring_play = play["scoringPlay"]
        shooting_play = play["shootingPlay"]
        score_value = play["scoreValue"]
        home_score = play["homeScore"]
        away_score = play["awayScore"]
        text = play["text"]

        p = Play(id=play_id,game_id=game_id,period=period,time=time,scoring_play=scoring_play,
            shooting_play=shooting_play,score_value=score_value,home_score=home_score,
            away_score=away_score,text=text)
        session.add(p)

    action = Column(String)
    type = Column(String)
    player_id = Column(Integer, ForeignKey('players.id'))


def parse_stats(stats):
    fgm, fga = extract_made_attempted(stats[1])  # Field goals made / attempted
    fgm3, fga3 = extract_made_attempted(stats[2]) # Threes made / attempted
    ftm, fta = extract_made_attempted(stats[3]) # Free throws made / attempted
    mins = intf(stats[0]) # Minutes played
    tp = intf(stats[12])    # Total points
    blk = intf(stats[9])     # Total blocks
    stl = intf(stats[8])     # Total steals
    ast = intf(stats[7])     # Total assists
    oreb = intf(stats[4])    # Total offensive rebounds
    dreb = intf(stats[5])    # Total defensive rebounds
    treb = intf(stats[6])     # Total rebounds (offensive + defensive)
    pf = intf(stats[11])    # Total personal fouls
    to = intf(stats[10])    # Total turnovers

    return {"mins":mins,"fgm":fgm,"fga":fga,"fgm3":fgm3,"fga3":fga3,"ftm":ftm,
        "fta":fta,"tp":tp,"blk":blk,"stl":stl,"ast":ast,"oreb":oreb,"dreb":dreb,
        "treb":treb,"pf":pf,"to":to}

def extract_made_attempted(stat_string):
    split_stats = stat_string.split("-")
    made = split_stats[0]
    attempted = split_stats[1]
    return made, attempted

def intf(s):
    try:
        num = int(s)
    except:
        num = 0
    return num