import json
import os
from basketball_reference_scraper.players import *
from datetime import datetime

ErrCodeInvalidPassword = 2
ErrCodeNoAccount = 3
ErrCodeUserExists = 4

'''''''''''''''''''''''''''
 User Methods 
'''''''''''''''''''''''''''
def load_users():
    with open('users.json') as file:
        users = json.load(file)
    return users


def login_user(username, password):
    users = load_users()
    if username in users:
        if users[username]['password'] == password:
            with open("current_user.json", "w") as file:
                currentUser = {'current_user': username}
                json.dump(currentUser, file)
            return True
        else:
            return ErrCodeInvalidPassword
    else:
        return ErrCodeNoAccount

def logout_user():
    with open('current_user.json', "w") as file:
        json.dump({'current_user': ''}, file)

def get_current_user(): 
    try:
        with open("current_user.json") as file:
            user = json.load(file)
            user = user['current_user']
    except FileNotFoundError:
        logout_user()
        user = ''
    return user

def add_user(username, password):
    users = load_users()
    if username not in users:
        users[username] = {'username': username, 'password': password,
                        'time created': datetime.now().strftime("%Y/%m/%d at %H:%M:%S a.m./p.m.")}
        with open('users.json', 'w') as file:
            json.dump(users, file)
        return users[username]
    else:
        return ErrCodeUserExists


'''''''''''''''''''''''''''
 Games Methods 
'''''''''''''''''''''''''''
def load_games():
    with open('games.json') as file:
        games = json.load(file)
    return games

def add_invitee(invitedPeople, name_of_curr_draft):
    games = load_games()
    games[name_of_curr_draft]["invited_people"] = invitedPeople
    with open('games.json', 'w') as file:
        json.dump(games, file)

def add_game(name, timeUntil, privacy):
    games = load_games()
    if name in games:
        return False
    games[name] = {'name': name, "timeUntil": timeUntil,
                   'privacy': privacy, "invited_people": [], "status": "not_started", "joined_people": []}
    with open('games.json', 'w') as file:
        json.dump(games, file)
    return True


def list_private_games(curr_user):
    my_games = []
    games = load_games()
    for game in games:
        if curr_user in games[game]['invited_people']:
            my_games.append(game)
    return my_games

def list_public_games():
    public_games = []
    games = load_games()
    for game in games:
        if (games[game]['privacy'] == "public") and (games[game]['status'] == "not_started") and (len(games[game]["joined_people"])) <= 15:
            public_games.append(game)
    return public_games

def get_players_over_ten():
    playersFile = open('br_names.txt', 'r')
    players = playersFile.read()
    playersFile.close()
    delPlayers = []
    for player in players:
        PTSEachSeas = get_stats(player).PTS
        GPEachSeas = get_stats(player).G
        PPG = 0
        for count in range(len(PTSEachSeas)):
            PPG += (PTSEachSeas[count] * GPEachSeas[count])
        if PPG > 10:
            pass
        else:
            delPlayers.append(player)
    for count in delPlayers:
        players = players.delete(count)
    playersFile = open('over_10_players.txt', 'w')
    playersFile.write(players)
    playersFile.close()
    return players
    
    #PTSEachSeas = get_stats(player).PTS ----> 3 problems 1 ----> when averaging the averages player could have played less games in a certain season 2 ----> need way to go thru the diff players 3 ----> automatically gives multiple options need lambda function that will auto choose first option
    