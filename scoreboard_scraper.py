import requests, json, os
from datetime import datetime
from progress_bar import printProgressBar

game_data_folder = 'games_data/'
scoreboards_folder = 'scoreboards/'

"""
Gets the games of the specific date and returns a json object
date format: 2018/02/01
"""
def get_ncaa_scoreboard(date):
    url = 'http://data.ncaa.com/jsonp/scoreboard/basketball-men/d1/'+date+'/scoreboard.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text[16:-2])
    return data

def create_date(year, month, day):
    if month < 10: month = '0'+str(month)
    if day < 10 : day = '0'+str(day)
    return str(year) + '/' + str(month) + '/' + str(day)

def scrape_season(start_yr):
    try: os.makedirs('{}/{}/{}'.format(game_data_folder,start_yr, scoreboards_folder))
    except Exception: pass
    end_yr = start_yr + 1
    season_yrm = [(start_yr,11),(start_yr,12),(end_yr,1),(end_yr,2),(end_yr,3),(end_yr,4)]
    l = len(season_yrm) * 31 # 186
    printProgressBar(0, l, prefix = '{} Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    progress_num = 1
    for index, month in enumerate(season_yrm):
        for day in range(1,32):
            date = create_date(month[0],month[1],day)
            printProgressBar(progress_num, l, prefix = '{} Progress:'.format(start_yr), suffix = 'Complete', length = 50)
            progress_num += 1
            try: compare_dates = datetime(month[0],month[1],day).date()
            except ValueError as e: continue
            today = datetime.today().date()
            if today > compare_dates:
                filename = game_data_folder +'/'+ str(start_yr) +'/'+ scoreboards_folder +'/'+ date.replace('/','-')+'.txt'
                if not os.path.exists(filename):
                    try:
                        ########  get data here #########
                        data = get_ncaa_scoreboard(date)
                        # for now just write it to a file
                        with open(filename,'a') as outfile:
                            json.dump(data, outfile)
                    except ValueError as e: pass
            elif today == compare_dates:
                filename = game_data_folder +'/'+ str(start_yr) +'/'+ scoreboards_folder +'/'+ date.replace('/','-')+'.txt'
                try:
                    ########  get data for today here #########
                    data = get_ncaa_scoreboard(date)
                    with open(filename,'w') as outfile:
                        json.dump(data, outfile)
                except ValueError as e:
                    pass
            else:
                pass
                # print('{}: is in the future'.format(date))
