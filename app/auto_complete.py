import Constants
from data_retriever import getAllPlayers, getAllTeams
import sys, json

def getErrorForm(code, msg):
    data = {"error" : {"code" : code, "message" : msg}}
    return data

def retrieveData(form):
    #print type(form)
    target = form["field"]
    if target is None:
        return getErrorForm(Constants.FormMissingElement, "Missing value for the key 'field'")
    else:
      # team drop down menu
      if target == Constants.AC_TEAM:
        data = getAllTeams();
        return data
            # player drop down menu
      elif target == Constants.AC_PLAYER:
                # TODO: Add id
        data = getAllPlayers(1);
        return data
      else:
        return getErrorForm(Constants.InvalidFormValue, "Wrong value for key 'field'")

    return ["ASD"]

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
