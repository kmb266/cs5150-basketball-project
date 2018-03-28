import json, datetime, glob
import espn.espn_scraper as espn
from progress_bar import printProgressBar

total_errors = []
game_ids = []
start_yr = 2017
cached_json = 'cached_json'
league = 'ncb'
playbyplay_folder_name = 'playbyplay'

scoreboard_urls = espn.get_all_scoreboard_urls(league, 2017)

def ppjson(data):
    ''' Pretty print json helper '''
    print(json.dumps(data, indent=2, sort_keys=True))

def url_is_before_today(url):
    date_string = url[url.rfind('/') + 1: url.rfind('?')]
    year = int(date_string[:4])
    month = int(date_string[4:6])
    day = int(date_string[-2:])
    return datetime.datetime(year,month,day).date() < datetime.datetime.now().date()

def filter_scoreboards_before_today(scoreboard_url_list):
    today = datetime.datetime.today().date()
    return [url for url in scoreboard_url_list if url_is_before_today(url)]

# this does not work to get updated scorecards. it still looks in the cache.
# TODO: update file in cache if there is a newer one.. maybe record last known run time and get all scoreboards after that date?
filtered_scoreboards = filter_scoreboards_before_today(scoreboard_urls)

scraped_game_ids = [filename.split('/')[-1][:-5] for filename in glob.iglob('{}/{}/{}/*'.format(cached_json, league, playbyplay_folder_name))]

def scrape_espn_scoreboards(withProgress):
    if withProgress: printProgressBar(0, len(filtered_scoreboards), prefix = '{} Scoreboard Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    for i, scoreboard_url in enumerate(filtered_scoreboards):
        if withProgress: printProgressBar(i+1 , len(filtered_scoreboards), prefix = '{} Scoreboard Progress:'.format(start_yr), suffix = 'Complete', length = 50)
        data = espn.get_url(scoreboard_url, cached_path=cached_json)
        for event in data['content']['sbData']['events']:
            game_id = event['competitions'][0]['id']
            if game_id not in scraped_game_ids: game_ids.append(game_id)

def scrape_espn_play_by_plays(withProgress):
    if withProgress: printProgressBar(0, len(game_ids), prefix = '{} PlayByPlay Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    for i,game_id in enumerate(game_ids):
        pbp_url = espn.get_game_url("playbyplay", league, game_id)
        pbp_json = espn.get_url(pbp_url, cached_path=cached_json, game_id=game_id)
        if withProgress: printProgressBar(i+1, len(game_ids), prefix = '{} PlayByPlay Progress:'.format(start_yr), suffix = 'Complete', length = 50)

scrape_espn_scoreboards(True)
scrape_espn_play_by_plays(True)

# print(event['season']['year'],
#       event['competitions'][0]['competitors'][0]['team']['abbreviation'],
#       event['competitions'][0]['competitors'][0]['score'],
#       event['competitions'][0]['competitors'][1]['team']['abbreviation'],
#       event['competitions'][0]['competitors'][1]['score'])
#  5585 files in PlayByPlay
