from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from backend import *
from datetime import datetime


invitedPeopleList = []
name_of_curr_draft = ""
curr_game = ""


class LoginScreen(Screen):

    def sign_up(self):
        self.manager.switch_to(self.manager.get_screen("sign_up_screen"))

    def log_in(self, username, password):
        login = login_user(username, password)
        if login == True:
            self.manager.curr_user = username
            self.ids.incorrect.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.manager.current = "login_screen_success"
            self.manager.transition.direction = "left"
        elif login == 2:
            self.ids.incorrect.text = "Wrong password!"
        else:
            self.ids.incorrect.text = "No account is asscoiated with that username."


class CreateNewGame(Screen):
    def login_screen_success(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"

    def create_private(self, NameOfDraft, TimeTillDraft, private):
        good_add = add_game(NameOfDraft, TimeTillDraft, private)
        if good_add:
            self.manager.transition.direction = "left"
            self.manager.current = "list_of_players"
            global name_of_curr_draft
            name_of_curr_draft = NameOfDraft
        else:
            self.ids.good_create.text = "The name of your game has already been used."

    def create_public(self, NameOfDraft, TimeTillDraft, public):
        good_add = add_game(NameOfDraft, TimeTillDraft, public)
        if good_add:
            self.manager.transition.direction = "left"
            self.manager.current = "list_of_players_public"
            global name_of_curr_draft
            name_of_curr_draft = NameOfDraft
        else:
            self.ids.good_create.text = "The name of your game has already been used."


class ListOfPlayersPublic(Screen):
    def start_public(self):
        games = load_games()
        if len(games[name_of_curr_draft]["joined_people"]) >= 1:
            self.manager.transition.direction = "left"
            self.manager.current = "draft_screen"
        else:
            self.ids.notEnufPpl.text = "You have not invited enough people for the game to begin."


class ChoosePrivateGame(Screen):
    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"

    def display_games(self):
        my_games = list_private_games(self.manager.curr_user)
        str_games = ""
        for count in range(len(my_games)):
            if count != 0:
                str_games += (", " + my_games[count])
            else:
                str_games += (my_games[count])
        self.ids.games_private.text = "Games you've been invited to: " + str_games

    def chosen_private(self, nameOfChosen):
        my_games = list_private_games(self.manager.curr_user)
        if nameOfChosen == "":
            self.ids.no_game_selected.text = "You have not entered the name of a game."
        elif nameOfChosen in my_games:
            global curr_game
            curr_game = nameOfChosen
            self.ids.nameOfTheChosen.text = ""
            self.manager.transition.direction = "left"
            self.manager.current = "wait_until_host_starts_game"
        else:
            self.ids.no_game_selected.text = "Invalid game name!"

class JoinPublicGame(Screen):
    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"

    def display_games(self):
        public_games = list_public_games()
        str_games = ""
        for count in range(len(public_games)):
            if count != 0:
                str_games += (", " + public_games[count])
            else:
                str_games += (public_games[count])
        self.ids.games_public.text = str_games

    def chosen_public(self, nameOfChosenPublic):
        public_games = list_public_games()
        if nameOfChosenPublic == "":
            self.ids.no_game_selected.text = "You have not entered the name of a game."
        elif nameOfChosenPublic in public_games:
            global curr_game
            curr_game = nameOfChosenPublic
            self.ids.nameOfTheChosenPublic.text = ""
            self.manager.transition.direction = "left"
            self.manager.current = "wait_until_host_starts_game"
        else:
            self.ids.no_game_selected.text = "Either you have not been invited to the entered game or the game you entered does not exist."


class WaitUntilHost(Screen):
    def leave_draft(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"


class ListOfPLayers(Screen):
    def invite_people(self, InvitePeople):
        users = load_users()
        if InvitePeople in users:
            invitedPeopleList.append(InvitePeople)
            self.ids.InvitePeople.text = ""
            self.ids.noSuch.text = "Your request to the player was submitted."
            bob = "People invited: "
            for count in range(len(invitedPeopleList)):
                if count == 0:
                    bob += str(invitedPeopleList[count])
                else:
                    bob += ", " + str(invitedPeopleList[count])
            self.ids.invitedPeopleState.text = bob
            add_invitee(invitedPeopleList, name_of_curr_draft)
        else:
            self.ids.noSuch.text = "No players with the entered username exist!"

    def start_private(self):
        # need elif that checks whether all of the players invited have logged into the draft
        if len(invitedPeopleList) >= 1:
            self.manager.transition.direction = "left"
            self.manager.current = "draft_screen"
        else:
            self.ids.noSuch.text = "You have not invited enough people for the game to begin."


class DraftScreen(Screen):
    pass


class LeaderboardScreen(Screen):
    pass


class ShareResults(Screen):
    pass


class SignUpScreen(Screen):
    def add_user(self, username, password):
        users = load_users()
        if username not in users:
            users[username] = {'username': username, 'password': password,
                            'time created': datetime.now().strftime("%Y/%m/%d at %H:%M:%S a.m./p.m.")}
            with open('users.json', 'w') as file:
                json.dump(users, file)
            self.manager.current = "sign_up_screen_success"
            self.manager.transition.direction = "left"
        else:
            self.ids.already.text = "An account with that username has already been created." #need suggested usernames popup if first username fails


class SignUpScreenSuccess(Screen):
    def gotologin(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        logout_user() 
        self.manager.curr_user = ""

    def create_new_game(self):
        self.manager.current = "create_new_game"
        self.manager.transition.direction = "left"

    def choose_private(self):
        self.manager.current = "choose_game_private"
        self.manager.transition.direction = "left"

    def join_public(self):
        self.manager.current = "join_game_public"
        self.manager.transition.direction = "left"

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file('design.kv')
        screenManager = RootWidget()
        user = get_current_user()
        if user:
            screenManager.curr_user = user
            screenManager.current = "login_screen_success"
        else:
            screenManager.current = "login_screen"
        return screenManager


if __name__ == "__main__":
    MainApp().run()
