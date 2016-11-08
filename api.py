# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
"""


import logging
import endpoints
import words

from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms
from utils import get_by_urlsafe, get_indexes

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))


@endpoints.api(name='hangman', version='v1')
class HangmanAPI(remote.Service):

    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
            request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        word = words.get_random_word()
        word_length = len(word)
        user_word = "".join(str(0) for i in range(word_length))
        print user_word
        game = Game.new_game(user.key, word, user_word)
        num = str(len(game.target))

        return game.to_form('Good luck playing Hangman! {} letters, to find the word'.format(num))

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to guess the word!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over! you missed "{}"'.format(game.target))

        request.guess = request.guess.lower()
        if len(request.guess) > 1:
            game.attempts_remaining -= 1
            if request.guess == game.target:
                game.end_game(True)
                return game.to_form('You win!')

            if game.attempts_remaining < 1:
                game.end_game(False)
                return game.to_form('Game over!')
            else:
                game.put()
                return game.to_form('')
        elif len(request.guess) == 1:
            if not request.guess in game.used_char:
                game.attempts_remaining -= 1

                if game.target.find(request.guess) != -1:
                    indx = get_indexes(request.guess, game.target)
                    new_word = list(game.user_word)
                    for x in indx:
                      new_word[x] = request.guess
                    game.user_word = "".join(new_word)
                    msg = '{} is a good choice'.format(request.guess)
                    if game.user_word == game.target:
                        game.end_game(True)
                        return game.to_form('You win!')
                else:
                  msg = 'wrong choice'

                if game.attempts_remaining < 1:
                    game.end_game(False)
                    return game.to_form('Game over!')
                else:
                    game.put()
                    return game.to_form(msg)
            else:
                return game.to_form('Already Used')

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])


api = endpoints.api_server([HangmanAPI])