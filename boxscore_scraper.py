import requests, json, os, glob
from progress_bar import printProgressBar

game_data_folder = 'games_data/'
scoreboards_folder = 'scoreboards/'
boxscores_folder = 'boxscores/'
delimiter = '-'

def get_ncaa_boxscore(url):
    url = 'http://data.ncaa.com' + url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_urls(filename):
    data = json.load(open(filename))
    games = data['scoreboard'][0]['games']
    files = []
    for i in range(len(games)):
        game_id = games[i]['id']
        name_split = [f for f in filename.split('/') if f != '']
        game_date = name_split[1]
        game_tabs = {'meta': {'start_yr':game_date, 'game_id':game_id}}
        game_tabs['files'] = games[i]['tabsArray'][0]
        files.append(game_tabs)
    return files

def get_boxscore_url(game_meta):
    for j in game_meta['files']:
        if j['type'] == 'boxscore': return j['file']
    raise FileNotFoundError

# test
# test = get_urls(game_data_folder+'2017/'+scoreboards_folder+'2018-02-02.txt')
# files = get_ncaa_boxscore(get_boxscore_url(test[0]))

def scrape_game(game_obj):
    start_yr = game_obj['meta']['start_yr']
    current_directory = '{}/{}/{}'.format(game_data_folder, str(start_yr), boxscores_folder)
    try: os.makedirs(current_directory)
    except Exception: pass

    try:
        filename = current_directory + game_obj['meta']['game_id'] + '.txt'
        if not os.path.exists(filename):
            boxscore_url = get_boxscore_url(game_obj)

            ######## get data here ########
            boxscore = get_ncaa_boxscore(boxscore_url)

            with open(filename, 'a') as outfile:
                # 1st line = json game meta data
                json.dump(game_obj, outfile)
                outfile.write('\n')
                # 2nd line = json box score
                json.dump(boxscore, outfile)
    except Exception as e:
        print(game_obj, e)

def scrape_season_boxscore(start_yr):
    files = [filename for filename in glob.iglob('{}/{}/{}/*.txt'.format(game_data_folder, str(start_yr), scoreboards_folder))]
    l = len(files)
    printProgressBar(0, l, prefix = '{} Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    progress_num = 1
    for filename in files:
        printProgressBar(progress_num, l, prefix = '{} Progress:'.format(start_yr), suffix = 'Complete', length = 50)
        progress_num += 1
        url_list = get_urls(filename)
        for game in url_list:
            scrape_game(game)
