import Constants
import sys, json, numpy as np

'''
get the form information from the front end
'''

def getErrorForm(code, msg):
  data = {"error" : {
            "code" : code,
            "message" : msg
            }
          }
  return data

def retrieveData(form):
  target = form["target"]
  if target is None:
    return getErrorForm(Constants.FormMissingElement, "Missing value for the key 'target'")
  else:
    if target == Constants.AC_POSITION:
      return {"field" : Constants.AC_POSITION,
              "data" : ["PG", "SG", "SF", "PF", "C"]}
    else if target == Constants.AC_TEAM:
      return {"field" : Constants.AC_TEAM,
              "data" : ["Cornell University", "Dartmouth College", "Princeton University", "Harvard University", "Yale University"]}
    else if target == Constants.AC_PLAYER:
      #TO-DO: Add sample players
      return {"field" : Constants.AC_PLAYER}
    else:
      return getErrorForm(Constanst.InvalidFormValue, "Wrong value for key 'target'")

def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def getForm():
    #lines = read_in()
    #np_lines = np.array(lines)
    np_lines = []
    return np_lines


def main():
    form = getForm()

    #TO-DO: delete bottom line when getting form
    form = {"field" : Constants.AC_POSITION}

    data = retrieveData(form)

    #return what we get
    print data
    sys.stdout.flush()


#start process
if __name__ == '__main__':
  main()