import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean

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
    home_score = Column(Integer)
    visitor_score = Column(Integer)
    isLeague = Column(Boolean)
    isPlayoff = Column(Boolean)



