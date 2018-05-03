'''
Retrieve all the team names and ids. Should return a list of teams with the id and the name of each team.
'''
def getAllTeams():
  return [{"id" : 1502, "name" : "Cornell University"},
            {"id" : 1603, "name" : "Dartmouth College"},
            {"id" : 1902, "name" : "Princeton University"},
            {"id" : 1807, "name" : "Harvard University"},
            {"id" : 1697, "name" : "Yale University"}]

'''
Retrieve all players for the team of the given id.
'''
def getAllPlayers(teamId):
  return [{"id" : 1502, "jersey" : 1,  "name" : "Kyle Brown"},
          {"id" : 1603, "jersey" : 10, "name" : "Matt Morgan"},
          {"id" : 1902, "jersey" : 12, "name" : "Jordan Abdur Ra'oof"},
          {"id" : 1807, "jersey" : 32, "name" : "Jack Gordon"}]
