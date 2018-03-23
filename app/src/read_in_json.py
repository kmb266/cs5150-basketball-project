import json, datetime, glob
game_files = [filename for filename in glob.iglob('/Users/Kyle/Desktop/cs5150/cs5150-basketball-project/cached_json/ncb/playbyplay/*.json')]
print('Total Games: {}'.format(len(game_files)))

with open(filename, 'r') as f:
    asdf = json.load(f)
    for p in asdf['gamepackageJSON']['plays']:
        print('<br>'+p['text'])
