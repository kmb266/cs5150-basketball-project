import json, datetime, glob
import espn_scraper as espn
from progress_bar import printProgressBar

# constants
cached_json = None
league = 'ncb'

def getStartYr():
    """get the year of the current season if in season,
    or get the start year of the most recent season if out of season"""

    now = datetime.datetime.now()
    if datetime.datetime(year=now.year,month=11,day=1) < now:
        return now.year
    return now.year - 1
def getLastScrapeDate():
    """returns the latest date of games that are stored in the basketball_json.db"""
    # TODO: add logic here to get the latest date of a game scraped in the db
    # for now hard code in 3/1/2018
    return datetime.datetime(year=2018, month=3, day=1)

def ppjson(data):
    ''' Pretty print json helper '''
    print(json.dumps(data, indent=2, sort_keys=True))

def url_is_before_today(url):
    date_string = url[url.rfind('/') + 1: url.rfind('?')]
    year = int(date_string[:4])
    month = int(date_string[4:6])
    day = int(date_string[-2:])
    return datetime.datetime(year,month,day).date() < datetime.datetime.now().date()

def url_is_after_last_scrape(url, last_scrape_date):
    date_string = url[url.rfind('/') + 1: url.rfind('?')]
    year = int(date_string[:4])
    month = int(date_string[4:6])
    day = int(date_string[-2:])
    return datetime.datetime(year,month,day).date() > last_scrape_date

def filter_scoreboards_before_today(scoreboard_url_list, last_scrape_date):
    today = datetime.datetime.today().date()
    return [url for url in scoreboard_url_list if url_is_before_today(url) and url_is_after_last_scrape(url, last_scrape_date)]


def scrape_espn_scoreboards(withProgress, filtered_scoreboards, start_yr):
    if withProgress: printProgressBar(0, len(filtered_scoreboards), prefix = '{} Scoreboard Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    for i, scoreboard_url in enumerate(filtered_scoreboards):
        if withProgress: printProgressBar(i+1 , len(filtered_scoreboards), prefix = '{} Scoreboard Progress:'.format(start_yr), suffix = 'Complete', length = 50)
        data = espn.get_url(scoreboard_url, cached_path=cached_json)
        for event in data['content']['sbData']['events']:
            game_id = event['competitions'][0]['id']
            game_ids.append(game_id)

def scrape_espn_play_by_plays(withProgress, game_ids, start_yr):
    if withProgress: printProgressBar(0, len(game_ids), prefix = '{} PlayByPlay Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    for i,game_id in enumerate(game_ids):
        pbp_url = espn.get_game_url("playbyplay", league, game_id)
        pbp_json = espn.get_url(pbp_url, cached_path=cached_json, game_id=game_id)
        if withProgress: printProgressBar(i+1, len(game_ids), prefix = '{} PlayByPlay Progress:'.format(start_yr), suffix = 'Complete', length = 50)

def main():
    start_yr = getStartYr()
    last_scrape_date = getLastScrapeDate()
    game_ids = []

    scoreboard_urls = espn.get_all_scoreboard_urls(league, start_yr)

    filtered_scoreboards = filter_scoreboards_before_today(scoreboard_urls)

    scrape_espn_scoreboards(False, filtered_scoreboards, start_yr)

    scrape_espn_play_by_plays(False, game_ids, start_yr)

#start process
if __name__ == '__main__':
    main()



# print(event['season']['year'],
#       event['competitions'][0]['competitors'][0]['team']['abbreviation'],
#       event['competitions'][0]['competitors'][0]['score'],
#       event['competitions'][0]['competitors'][1]['team']['abbreviation'],
#       event['competitions'][0]['competitors'][1]['score'])
#  5585 files in PlayByPlay
