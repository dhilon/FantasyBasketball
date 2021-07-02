from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import backend as backend


class LoginScreen(Screen):

    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_in(self, username, password):
        login = backend.login_user(username, password)
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
        good_add = backend.add_game(NameOfDraft, TimeTillDraft, private, self.manager.curr_user)
        if good_add:
            self.manager.transition.direction = "left"
            self.manager.current = "list_of_players"
            self.manager.name_of_curr_draft = NameOfDraft
        else:
            self.ids.good_create.text = "The name of your game has already been used."

    def create_public(self, NameOfDraft, TimeTillDraft, public):
        good_add = backend.add_game(NameOfDraft, TimeTillDraft, public, self.manager.curr_user)
        if good_add:
            self.manager.transition.direction = "left"
            self.manager.current = "list_of_players_public"
            self.manager.name_of_curr_draft = NameOfDraft
        else:
            self.ids.good_create.text = "The name of your game has already been used."


class ListOfPlayersPublic(Screen):
    def start_public(self):
        games = backend.load_games()
        if len(games[self.manager.name_of_curr_draft]["joined_people"]) >= 1:
            self.manager.transition.direction = "left"
            self.manager.current = "draft_screen"
        else:
            self.ids.notEnufPpl.text = "You have not invited enough people for the game to begin."


class ChoosePrivateGame(Screen):
    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"

    def display_games(self):
        my_games = backend.list_private_games(self.manager.curr_user)
        str_games = ""
        for count in range(len(my_games)):
            if count != 0:
                str_games += (", " + my_games[count])
            else:
                str_games += (my_games[count])
        self.ids.games_private.text = "Games you've been invited to: " + str_games #need to add the names of the owners of the games

    def display_owners(self):
        my_owners = backend.list_private_games_owners(self.manager.curr_user)
        str_owners = ""
        for count in range(len(my_owners)):
            if count != 0:
                str_owners += (", " + my_owners[count])
            else:
                str_owners += (my_owners[count])
        self.ids.owners_private.text = "Owners of the games you've been invited to: " + str_owners
    
    def chosen_private(self, nameOfChosen):
        my_games = backend.list_private_games(self.manager.curr_user)
        if nameOfChosen == "":
            self.ids.no_game_selected.text = "You have not entered the name of a game."
        elif nameOfChosen in my_games:
            self.manager.name_of_curr_draft = nameOfChosen
            self.ids.nameOfTheChosen.text = ""
            backend.invitee_joined(self.manager.curr_user, nameOfChosen)
            self.manager.transition.direction = "left"
            self.manager.current = "wait_until_host_starts_game"
        else:
            self.ids.no_game_selected.text = "Invalid game name!"


class JoinPublicGame(Screen):
    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"

    def display_games(self):
        public_games = backend.list_public_games()
        str_games = ""
        for count in range(len(public_games)):
            if count != 0:
                str_games += (", " + public_games[count])
            else:
                str_games += (public_games[count])
        self.ids.games_public.text = str_games

    def chosen_public(self, nameOfChosenPublic):
        public_games = backend.list_public_games()
        if nameOfChosenPublic == "":
            self.ids.no_game_selected.text = "You have not entered the name of a game."
        elif nameOfChosenPublic in public_games:
            self.manager.name_of_curr_draft = nameOfChosenPublic
            self.ids.nameOfTheChosenPublic.text = ""
            self.manager.transition.direction = "left"
            self.manager.current = "wait_until_host_starts_game"
        else:
            self.ids.no_game_selected.text = "Either you have not been invited to the entered game or the game you entered does not exist."


# need three loading dots bouncing up and down as a waiting symbol
class WaitUntilHost(Screen):
    def leave_draft(self):
        backend.remove_joinee(
            self.manager.name_of_curr_draft, self.manager.curr_user)
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen_success"


class ListOfPLayers(Screen):
    def invite_people(self, InvitePeople):
        users = backend.load_users()
        if InvitePeople in users:
            ppl = backend.add_invitee(
                InvitePeople, self.manager.name_of_curr_draft)
            self.ids.InvitePeople.text = ""
            self.ids.noSuch.text = "Your request to the player was submitted."
            bob = "People invited: "
            counter = 0
            for count in ppl:
                if counter == 0:
                    bob += str(count)
                else:
                    bob += ", " + str(count)
            self.ids.invitedPeopleState.text = bob
        else:
            self.ids.noSuch.text = "No players with the entered username exist!"

    def start_private(self):
        if len(self.manager.invitedPeople) >= 1:
            games = backend.load_games()
            if games[self.manager.name_of_curr_draft]["invited_people"] == [self.manager.name_of_curr_draft]["joined_people"]:
                self.manager.transition.direction = "left"
                self.manager.current = "draft_screen"
            else:
                self.ids.noSuch.text = "Not all of the players you have invited have joined."
        else:
            self.ids.noSuch.text = "You have not invited enough people for the game to begin."


class DraftScreen(Screen):
    def show_NBA(self):
        NBA = open("players\over_10.txt")
        self.ids.players.text = NBA.readlines()
        NBA.close()


class LeaderboardScreen(Screen):
    pass


class ShareResults(Screen):
    pass


class SignUpScreen(Screen):
    def add_user(self, username, password):
        user = backend.add_user(username, password)
        if user != backend.ErrCodeUserExists:
            self.manager.current = "sign_up_screen_success"
            self.manager.transition.direction = "left"
        else:
            # need suggested usernames popup if first username fails
            self.ids.already.text = "An account with that username has already been created."


class SignUpScreenSuccess(Screen):
    def gotologin(self):
        self.manager.current = "login_screen"
        self.manager.transition.direction = "right"


class LoginScreenSuccess(Screen): #when you exit the app, I need the user to reenter the app at the exact same screen it was closed at
    def log_out(self):
        self.manager.current = "login_screen"
        self.manager.transition.direction = "right"
        backend.logout_user()
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
        user = backend.get_current_user()
        if user:
            screenManager.curr_user = user
            screenManager.current = "login_screen_success"
        else:
            screenManager.current = "login_screen"
        screenManager.invitedPeopleList = []
        return screenManager


if __name__ == "__main__":
    MainApp().run()
