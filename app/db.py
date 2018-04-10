import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Used to keep track of classes and tables
from sqlalchemy.ext.declarative import declarative_base


# During initial development, use a sqlite DB held in memory for easy setup/teardown
engine = create_engine('sqlite:///basketball.db', echo=True)

# Initialize the base
Base = declarative_base()


# Define database tables
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    home = Column(String)
    # Can use date and home as a primary key: A team can only play one game at any given time
    visitor = Column(String)
    winner = Column(String)
    loser = Column(String)
    # home_score = Column(Integer)
    # visitor_score = Column(Integer)
    isLeague = Column(Boolean)
    isPlayoff = Column(Boolean)
    # How do we store period data - i.e. what if there's 12 OT? Should use PostgreSQL with json


class Team(Base):
    __tablename__ = 'teams'
    team_id = Column(String, primary_key=True)
    name = Column(String)


class PlaysIn(Base):
    __tablename__ = 'teamstats'
    id = Column(Integer, primary_key=True)
    team = Column(String, ForeignKey('teams.team_id'))
    game = Column(Integer, ForeignKey('games.id'))

    # Box Stats
    fgm = Column(Integer)   # Made field goals
    fga = Column(Integer)   # Attempted field goals

    fgm3 = Column(Integer)  # Made threes
    fga3 = Column(Integer)  # Attempted threes

    ftm = Column(Integer)   # Made free throws
    fta = Column(Integer)   # Attempted free throws

    tp = Column(Integer)    # Total points
    blk = Column(Integer)   # Total blocks
    stl = Column(Integer)   # Total steals
    ast = Column(Integer)   # Total assists
    oreb = Column(Integer)  # Total offensive rebounds
    dreb = Column(Integer)  # Total defensive rebounds
    treb = Column(Integer)  # Total rebounds (offensive + defensive)
    pf = Column(Integer)    # Total personal fouls
    tf = Column(Integer)    # Total team fouls
    to = Column(Integer)    # Total turnovers

    # Special Statistics
    is_home = Column(Boolean)
    pts_to = Column(Integer)        # Points scored off of turnovers
    pts_paint = Column(Integer)     # Points scored in the paint
    pts_ch2 = Column(Integer)       # Points scored within the arc but outside the paint?
    pts_fastb = Column(Integer)     # Points scored on fastbreaks
    pts_bench = Column(Integer)     # Points scored by the bench
    ties = Column(Integer)          # Number of times the team tied the game
    leads = Column(Integer)         # Number of times the team took the lead
    poss_count = Column(Integer)    # Number of possessions
    poss_time = Column(Integer)     # Amount of time the team had the ball
    score_count = Column(Integer)   # Amount of possessions the team scored on
    score_time = Column(Integer)    # Amount of time spent on possessions that resulted in scoring TODO: verify this


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(Integer)
    team = Column(String, ForeignKey('teams.team_id'))


class PlayerIn(Base):
    __tablename__ = 'playersin'
    id = Column(Integer, primary_key=True)
    game = Column(Integer, ForeignKey('games.id'))
    player = Column(Integer, ForeignKey('players.id'))
    number = Column(Integer) # Jersey number in that game

    # Player Stats
    fgm = Column(Integer)  # Made field goals
    fga = Column(Integer)  # Attempted field goals

    fgm3 = Column(Integer)  # Made threes
    fga3 = Column(Integer)  # Attempted threes

    ftm = Column(Integer)  # Made free throws
    fta = Column(Integer)  # Attempted free throws

    tp = Column(Integer)    # Total points
    blk = Column(Integer)   # Total blocks
    stl = Column(Integer)   # Total steals
    ast = Column(Integer)   # Total assists
    oreb = Column(Integer)  # Total offensive rebounds
    dreb = Column(Integer)  # Total defensive rebounds
    treb = Column(Integer)  # Total rebounds (offensive + defensive)
    pf = Column(Integer)    # Total personal fouls
    tf = Column(Integer)    # Total team fouls
    to = Column(Integer)    # Total turnovers
    dq = Column(Integer)    # Disqualifications? TODO: review

Base.metadata.create_all(engine)
#
# p1 = Game(date=datetime.now(), home="COR", visitor="BRN", winner="COR", loser="BRN", isLeague=False, isPlayoff=False)
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(p1)
# session.commit()
#
# x = session.query(Game).first()
# print(x.home, x.visitor)











