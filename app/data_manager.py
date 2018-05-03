import sys, json

'''
retrieve the data from the backend
'''
def retrieveData(form):
    data = {"dataTab" : "players",
            "data" : [
                {
                    "name" : "Kyle Brown",
                    "jersey" : "1",
                    "FG" : 8,
                    "3PT" : 3,
                    "FT" : 2,
                    "OREB" : 1,
                    "DREB" : 7,
                    "REB" : 8,
                    "AST" : 5,
                    "STL" : 2,
                    "BLK" : 1,
                    "TO" : 2,
                    "PF" : 3,
                    "PTS" : 21
                },
                {
                    "name" : "Matt Morgan",
                    "jersey" : "10",
                    "FG" : 5,
                    "3PT" : 4,
                    "FT" : 3,
                    "OREB" : 2,
                    "DREB" : 3,
                    "REB" : 5,
                    "AST" : 7,
                    "STL" : 1,
                    "BLK" : 0,
                    "TO" : 2,
                    "PF" : 3,
                    "PTS" : 17
                },
                {
                    "name" : "Jack Gordon",
                    "jersey" : "32",
                    "FG" : 7,
                    "3PT" : 3,
                    "FT" : 1,
                    "OREB" : 4,
                    "DREB" : 1,
                    "REB" : 5,
                    "AST" : 10,
                    "STL" : 4,
                    "BLK" : 1,
                    "TO" : 4,
                    "PF" : 4,
                    "PTS" : 18
                }
            ]
        }
    return data

'''
get the form information from the front end
'''
def getForm():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    form = getForm()
    data = retrieveData(form)

    #return what we get
    print data
    sys.stdout.flush()

#start process
if __name__ == '__main__':
    main()