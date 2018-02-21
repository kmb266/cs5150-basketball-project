import json, datetime, glob
from player_scraper import scrape_all_players

all_players = scrape_all_players()

# These classes are just ideas as to what they could look like
class Player(object):
    """docstring for Player."""
    def __init__(self, arg):
        super(Player, self).__init__()
        self.id = arg['id']
        self.name = all_players[self.id]['name']
        self.team = all_players[self.id]['team']


class Play(object):
    """docstring for Play."""

    def time_to_seconds(self, clock_time):
        hr_sec = clock_time.split(':')
        return int(hr_sec[0]) * 60 + int(hr_sec[1])

    def __init__(self, json_play):
        super(Play, self).__init__()
        self.json_play = json_play
        self.play_id = json_play['id']
        self.scoring_play = json_play['scoringPlay']
        self.away_score = json_play['awayScore']
        self.clock_display = json_play['clock']['displayValue']
        self.time = self.time_to_seconds(json_play['clock']['displayValue'])
        self.score = {'home':json_play['homeScore'], 'away':json_play['awayScore']}
        self.text = json_play['text']
        self.type = json_play['type']
        self.players = None
        self.team = None
        try:
            self.players = [Player(pl['athlete']) for pl in json_play['participants']]
            self.team = json_play['team']['id']
        except KeyError:
            print('no team or participants')

cached_json = 'cached_json'
league = 'ncb'
playbyplay_folder_name = 'playbyplay'

game_files = [filename for filename in glob.iglob('{}/{}/{}/*'.format(cached_json, league, playbyplay_folder_name))]
filename = game_files[5]
easdf = None
ex_obj = None
with open(filename, 'r') as f:
    asdf = json.load(f)
    ex_obj = Play(asdf['gamepackageJSON']['plays'][0])

# Single Play json example
'''
  "awayScore": 0,
  "clock": {
    "displayValue": "19:38"
  },
  "homeScore": 0,
  "id": "400990466101806101",
  "participants": [
    {
      "athlete": {
        "id": "3913167"
      }
    }
  ],
  "period": {
    "number": 1
  },
  "scoreValue": 0,
  "scoringPlay": false,
  "sequenceNumber": "101806101",
  "shootingPlay": false,
  "team": {
    "id": "324"
  },
  "text": "Christian Adams Turnover.",
  "type": {
    "id": "598",
    "text": "Lost Ball Turnover"
  }
'''
