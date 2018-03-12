import xml.etree.ElementTree as ET
import sqlalchemy
from datetime import datetime


def parse_venue_info(root_node):
    """
    Retrieves the date, time, and home court information about the game,
    as well as whether or not the game was a leaguegame or a playoff game
    :param root_node:
    :return:
    """
    root = root_node.find('venue')

    # Fetch the id for the home team
    home = root.attrib['homeid']

    # Fetch the id for the visitor team
    vis = root.attrib['visid']

    # Fetch the date (and time) convert to python datetime
    date = root.attrib['date'] + " " + root.attrib['time'].replace('.', '')
    date = datetime.strptime(date, '%m/%d/%Y %I:%M %p')

    # Extract information on whether the game is a league game, playoff game
    is_league = False if root.attrib['leaguegame'] == "N" else True
    is_playoff = False if root.attrib['postseason'] == "N" else True


def get_team_info(team_node):
    # Collecting base information
    id = team_node.attrib['id']
    record = team_node.attrib['record']
    record_divider = record.find('-')
    losses = record[:record_divider]
    wins = record[record_divider + 1:]

    # Information from the linescore node
    linescore = team_node.find('linescore')
    game_score = linescore.attrib['score']
    p1_score = 0
    p2_score = 0
    # TODO: What about OT?
    for lineprd in linescore:
        if lineprd.attrib['prd'] == 1:
            p1_score = lineprd.attrib['score']
        else:
            p2_score = lineprd.attrib['score']

    # Information from the totals node
    totals = team_node.find('totals')
    stats = totals.find('stats')
    stats_dict = {}
    for attrName, attrValue in stats.attrib.items():
        stats_dict[attrName] = attrValue
    print(stats_dict)

    special = totals.find('special')
    spec_dict = {}
    for attrName, attrValue in special.attrib.items():
        spec_dict[attrName] = attrValue
    print(spec_dict)

    players = team_node.findall("player")
    player_list = []
    for player in players:
        this_player = {}
        for attrName, attrValue in player.attrib.items():
            this_player[attrName] = attrValue
        player_stats = player.find('stats')

        # If the player has saved statistics for the game, extract them
        if player_stats:
            for attrName, attrValue in player_stats.attrib.items():
                this_player[attrName] = attrValue
        player_list.append(this_player)


def get_play_info(period_node):
    plays_list = []
    for play in period_node.findall("play"):
        this_play = {}
        for attrName, attrValue in play.attrib.items():
            this_play[attrName] = attrValue
        plays_list.append(this_play)
    return plays_list


def parse_game_file(filename):
    game_data = ET.parse(filename)
    root = game_data.getroot()
    parse_venue_info(root)
    # for child in root:
    #     print(child.tag, child.attrib)
    for team in root.findall("team"):
        get_team_info(team)
    for period in root.findall("period"):
        get_play_info(period)


parse_game_file("MBK_0105.xml")
