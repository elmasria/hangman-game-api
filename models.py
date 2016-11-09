"""models.py - This file contains the class definitions for the Datastore
entities used by the Game."""


from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):

    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    points = ndb.IntegerProperty(required=True, default=0)

    def to_form(self):
        return UserForm(name=self.name, email=self.email,
                points=self.points)

class UserForm(messages.Message):

    """"User object"""
    name = messages.StringField(1,required=True)
    email = messages.StringField(2)
    points = messages.IntegerField(3,required=True)



class UserForms(messages.Message):

    """Return multiple UserForms"""
    items = messages.MessageField(UserForm, 1, repeated=True)

class Game(ndb.Model):

    """Game object"""
    target = ndb.StringProperty(required=True)
    user_word = ndb.StringProperty(required=True)
    used_char =  ndb.StringProperty(repeated=True)
    steps = ndb.PickleProperty(required=True, default=[])
    attempts_allowed = ndb.IntegerProperty(required=True, default=15)
    attempts_remaining = ndb.IntegerProperty(required=True, default=15)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, user, word, user_word):
        """Creates and returns a new game"""
        game = Game(user=user,
                    target=word,
                    user_word=user_word,
                    attempts_allowed=11,
                    attempts_remaining=11,
                    game_over=False)
        game.put()
        return game

    def to_form(self, message=""):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.user_word = self.user_word
        form.used_char = self.used_char
        form.message = message
        return form


    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True

        user = User.query(User.name == self.user.get().name).get()
        user.points = user.points + self.attempts_remaining + 1
        user.put()
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class GameForm(messages.Message):

    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    user_word = messages.StringField(4, required=True)
    used_char = messages.StringField(5, repeated=True)
    message = messages.StringField(6, required=True)
    user_name = messages.StringField(7, required=True)

class GameForms(messages.Message):

    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):

    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)

class Score(ndb.Model):

    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)


class ScoreForm(messages.Message):

    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):

    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class MakeMoveForm(messages.Message):

    """Used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class StringMessage(messages.Message):

    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
