import json

ErrCodeInvalidPassword = 2
ErrCodeNoAccount = 3


def load_users():
    with open('users.json') as file:
        users = json.load(file)
    return users


def login_user(username, password):
    users = load_users()
    if username in users:
        if users[username]['password'] == password:
            return True
        else:
            return ErrCodeInvalidPassword
    else:
        return ErrCodeNoAccount


def load_games():
    with open('games.json') as file:
        games = json.load(file)
    return games

def add_invitee(invitedPeopleList, name_of_curr_draft):
    games = load_games()
    games[name_of_curr_draft]["invited_people"] = invitedPeopleList
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
        if curr_user in game['invited_people']:
            my_games.append(game)
    return my_games

def list_public_games():
    public_games = []
    games = load_games()
    for game in games:
        if game['privacy'] == "public" and game['status'] == "not_started" and len(game["joined_people"]) <= 15:
            public_games.append(game)
    return public_games