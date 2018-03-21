import json, datetime, glob
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy import stats

class Play(object):
    """docstring for Play."""

    def time_to_seconds(self, clock_time):
        hr_sec = clock_time.split(':')
        if self.period == 1:
            return int(hr_sec[0])*60 + int(hr_sec[1]) + 1200
        else:
            return int(hr_sec[0])*60 + int(hr_sec[1])

    def __init__(self, json_play, home_team_id, team_ids):
        super(Play, self).__init__()
        self.home_team_id = home_team_id
        self.json_play = json_play
        self.period = int(json_play['period']['number'])
        self.play_id = json_play['id']
        self.scoring_play = json_play['scoringPlay']
        self.clock_display = json_play['clock']['displayValue']
        self.time = self.time_to_seconds(json_play['clock']['displayValue'], )
        self.score = {'home':json_play['homeScore'], 'away':json_play['awayScore']}
        self.text = json_play['text']
        self.type = json_play['type']
        self.team_id = None
        self.is_home_team = None
        self.opponent = None
        try:
            self.team_id = json_play['team']['id']
            if team_ids[1] == self.team_id: self.opponent = team_ids[0]
            else: self.opponent = team_ids[1]
            self.is_home_team = self.home_team_id == self.team_id
        except KeyError:
            pass
            # print('no team or participants')
    def __str__(self):
        return 'Period:{} Scoring Play:{} Score(h-a):{}-{} Type:{} ClockTime:{} Time:{} Text:{} opponent:{}'.format(self.period,self.scoring_play, self.score['home'], self.score['away'], self.type, self.clock_display, self.time, self.text,self.opponent)

cached_json = 'cached_json'
league = 'ncb'
playbyplay_folder_name = 'playbyplay'

game_files = [filename for filename in glob.iglob('{}/{}/{}/*'.format(cached_json, league, playbyplay_folder_name))]

games_plays = []

for filename in game_files:
# for filename in game_files[:1800]:
    with open(filename, 'r') as f:
        current_game = []
        asdf = json.load(f)
        home_team_id = asdf['__gamepackage__']['homeTeam']['id']
        away_team_id = asdf['__gamepackage__']['awayTeam']['id']
        for pl in asdf['gamepackageJSON']['plays']: current_game.append((filename.split('/')[-1][:-5], Play(pl, home_team_id, [home_team_id, away_team_id])))
        games_plays.append(current_game)


# testing graphableness of games
plt.figure(figsize=(12,6))
plt.xlim(2400,0)
plt.grid('on')
plt.xticks([2400, 1800, 1200, 600, 0], ['20:00','10:00','20:00','10:00', '0:00'])

all_home_points = []
all_away_points = []

vspenn = []
penn_games = []

for gameP in games_plays:
    h_percentages = []
    a_percentages = []

    h_makes = 0
    h_attempts = 0

    a_makes = 0
    a_attempts = 0

    penn_game_percentages = []
    makes = 0
    attempts = 0
    is_vs_penn = False
    for gp in gameP:
        pl = gp[1]
        game_id = gp[0]
        if 'jumper' in pl.text.lower():
            # do something with the shot attempt
            if pl.is_home_team:
                if pl.scoring_play: h_makes += 1
                h_attempts += 1
                t = (pl.time, h_makes/h_attempts)
                # print(h_makes, h_attempts , ':', h_makes/h_attempts)
                h_percentages.append(t)
            else:
                if pl.scoring_play: a_makes += 1
                a_attempts += 1
                t = (pl.time, a_makes/a_attempts)
                a_percentages.append(t)
            if pl.opponent == '219':
                is_vs_penn = True
                if pl.scoring_play: makes += 1
                attempts += 1
                t = (pl.time, makes/attempts)
                penn_game_percentages.append(t)

    if is_vs_penn:
        penn_game_percentages.append((0, makes/attempts))
        penn_games.append(penn_game_percentages)

    if h_attempts: h_percentages.append((0, h_makes/h_attempts))
    else: h_percentages.append((0,0))
    if a_attempts: a_percentages.append((0, a_makes/a_attempts))
    else: a_percentages.append((0,0))

    home = sorted(h_percentages, key=lambda x: x[0])
    away = sorted(a_percentages, key=lambda x: x[0])
    all_home_points += home
    all_away_points += away

    hx, hy = zip(* home)
    ax, ay = zip(* away)
    plt.plot(hx,hy, label=game_id, color='lightblue', alpha=0.25)
    plt.plot(ax, ay, label=game_id, color='lightblue', alpha=0.25)

x,y = zip( * (all_home_points + all_away_points))
z = np.polyfit(x, y, 3)
xp = np.linspace(0,2400,500)
p = np.poly1d(z)
plt.plot(xp, p(xp), '-', color='green')

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

x2 = np.linspace(0,2400,500)
y2 = x2*slope+intercept

# plt.plot(x2, y2, '--', color='orange')

for penn_game in penn_games:
    pg = sorted(penn_game, key=lambda x: x[0])
    vspenn += pg
    px, py = zip(* pg)
    plt.plot(px,py, label=game_id, color='r', alpha=0.5)

x,y = zip( * vspenn)
z = np.polyfit(x, y, 3)
xp = np.linspace(0,2400,500)
p = np.poly1d(z)
plt.plot(xp, p(xp), '-', color='blue')

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

x2 = np.linspace(0,2400,500)
y2 = x2*slope+intercept

# plt.plot(x2, y2, '--', color='purple')

plt.show()

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
