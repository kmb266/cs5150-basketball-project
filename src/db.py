import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Used to keep track of classes and tables
from sqlalchemy.ext.declarative import declarative_base


# During initial development, use a sqlite DB held in memory for easy setup/teardown
engine = create_engine('sqlite:///:memory:', echo=True)

# Initialize the base
Base = declarative_base()



# Define database tables
class Player(Base):
    """
    Tracks all of the players. Questions: How should we treat players across seasons if their jersey number changes?
    Should we store career stats here?
    How are players uniquely identified? We would have to keep track of past jersey numbers?
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # What about having a separate DB with a list of numbers and teams that maps to IDs?
    number = Column(Integer) # Jersey Number - TODO: have a different jersey number for every year option? Players can have more than one jersey number per year
    team = Column(String)


class Game(Base):
    __tablename__ = 'players'
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
    team_id = Column(String, primary_key=True)
    name = Column(String)


class PlaysIn(Base):
    team = Column(String, ForeignKey('teams.team_id'))
    game = Column(Integer, ForeignKey('game.id'))

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








