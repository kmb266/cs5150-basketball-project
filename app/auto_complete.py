import Constants
import sys, json, numpy as np
import ast

'''
get the form information from the front end
'''

def getErrorForm(code, msg):
    data = {"error" : 
                {
                "code" : code,
                "message" : msg
                }
           }
    return data

def getQueryForm(target, form):
	queryForm = {"field" : target}#, "user_input" : form["user_input"]}

	if target == Constants.AC_PLAYER:
		team_id = form["team_id"]
		if form is None:
			return None
		queryForm["team_id"] = team_id

	return queryForm

def retrieveData(form):
    target = form["field"]
    if target is None:
        return getErrorForm(Constants.FormMissingElement, "Missing value for the key 'field'")

    else:
        # position drop down menu 
        if target == Constants.AC_POSITION:
            return {"field" : Constants.AC_POSITION,
                    "data" : ["PG", "SG", "SF", "PF", "C"]}
        else:
    	    queryForm = getQueryForm(target, form)
    	    if queryForm is None:
                return getErrorForm(Constants.FormMissingElement, "Missing value for the key 'team_id'")

    	    #TO-DO: Delete this segment after backend is connected --------------------
            # team drop down menu 
    	    if target == Constants.AC_TEAM:
      		    return {"field" : Constants.AC_TEAM,
                        "data" : [{"id" : 1502, "name" : "Cornell University"}, 
              			          {"id" : 1603, "name" : "Dartmouth College"},
              			          {"id" : 1902, "name" : "Princeton University"},
              			          {"id" : 1807, "name" : "Harvard University"},
              			          {"id" : 1697, "name" : "Yale University"}]}

            # player drop down menu 
    	    elif target == Constants.AC_PLAYER:
                return {"field" : Constants.AC_TEAM,
                        "data" : [{"id" : 1502, "jersey" : 1,  "name" : "Kyle Brown"}, 
                                  {"id" : 1603, "jersey" : 10, "name" : "Matt Morgan"},
                                  {"id" : 1902, "jersey" : 12, "name" : "Jordan Abdur Ra'oof"},
                                  {"id" : 1807, "jersey" : 32, "name" : "Jack Gordon"}]}
            else:
      		    return getErrorForm(Constants.InvalidFormValue, "Wrong value for key 'field'")
      	#----------------------------------------------

def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def getForm():
    # lines = read_in()
    # np_lines = np.array(lines)
    # np_lines = []
    # return np_lines

    # TODO : delete reading lines from command, read from front end
    np_lines = raw_input()
    return json.loads(np_lines)


def main():
    form = getForm()
    form = ast.literal_eval(form)
    
    # TO-DO: delete bottom line when getting form
    # form = {"field" : Constants.AC_TEAM}

    data = retrieveData(form)

    #return what we get
    print data
    sys.stdout.flush()


#start process
if __name__ == '__main__':
    main()
