import sys, json, numpy as np

'''
get the form information from the front end 
'''
def getForm():
    lines = read_in()
    np_lines = np.array(lines)
    return np_lines

'''
retrieve the data from the backend
'''
def retrieveData(form):
    data = {"dataTab" : "players",
            "data" : {
                "players" : [
                    {
                        "name" : "Kyle Brown",
                        "jersey" : "10"
                    },
                    {
                        "name" : "Hasan Atay",
                        "jersey" : "5"
                    }
                ]
            },
            "firstNumber" : form[0]
        }
    return data

def read_in():
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