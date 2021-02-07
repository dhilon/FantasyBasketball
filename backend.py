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
    players = playersFile.readlines()
    playersFile.close()
    nonplayersFile = open('players/under_10.txt')
    nonplayers = nonplayersFile.readlines()
    nonplayersFile.close()
    for count in range (len(players)):
        player = players[count]
        player = player.strip()
        print("---------------- Processing player %s of %s (%s)." % (count, len(players), player))
        if os.path.exists('players/%s.json' % player) or ((player + '\n') in nonplayers):
            print ("---------------- Found player, skipping")
            continue
        try:
            statsPlayer = get_stats(player, ask_matches=False)
            PTSEachSeas = statsPlayer.PTS
            GPEachSeas = statsPlayer.G
            PPG = 0
            totalPTS = 0
            totalGP = 0
            for count in range(len(PTSEachSeas)):
                try:
                    totalGP += GPEachSeas[count]
                    totalPTS += (PTSEachSeas[count] * GPEachSeas[count])
                except:
                    continue
            PPG = totalPTS/totalGP
            if PPG > 10:
                print("----------------  " + player + " was above 10 ppg")
                with open('players/%s.json' % player, 'w') as file:
                    json.dump({player:statsPlayer.to_dict()}, file)
            else:
                print("---------------- " + player + ' was below 10 ppg')
                with open('players/under_10.txt', 'a') as file:
                    file.writelines(player + '\n')
        except:
            print("---------------- " + player + ' was an error')
            with open('players/under_10.txt', 'a') as file:
                file.writelines(player + '\n')