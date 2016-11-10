# Hangman Game API

API with endpoints that will allow front-end developers to develop a front-end for hangman game.


## About API

### Game Description

Hangman is a word guessing game. Game begins with a random word, and a maximum number of attempts.
Users can make guesses consisting of a single letter or the secret word directly.
Each time the player submit a letter or the secret word incorrectly, they lose one of thier attempts.
For each guess, the response displays the target word with all letters that have not yet been guessed replaced with dash.
More details on the general idea of the game can be described on [Wikipedia Description](https://en.wikipedia.org/wiki/Hangman_(game))

### Game Rules

1. Each user has a points(set to zero when creating user pofile)
2. User can guess the secret word directly or by submitting letter by letter
3. User can guess the secret word by submitting single letter
4. User can't guess the secret word by submitting more than one letter (except the entire word)

### Score

##### Ranking

The Ranking is based on total number of points gained by each user.
Each game user collect point based on:

1. Remaining attenps is set to 15 (currently can't be changed)
2. Each time user submit a wrong chice remaining attenps will be decreased by 1 point
3. Remaining attenps will be added to the current user points
4. When user lose all Remaining attenps game will be set to over and no point will be added
4. First place is based on total number of points gained

##### Dashboard

The dashboard is based on each game remaining attenps number (number of points for user is not taken into consideration)

1. User can appeare more than one time on a dashboard
2. Dashboard sorting is based on date user has start the game and remaining attenps number
3. First place on dashboard is for user that start the game and finish it in the same day from first Attempt

### Endpoints Included

#### create_user

 * Path: 'user'
 * Method: 'POST'
 * Parameters: user_name, email (optional)
 * Returns: Message confirming creation of the User.
 * Description: Creates a new User. user_name provided must be unique. Will raise a ConflictException if a User with that user_name already exists.

#### new_game

 * Path: 'game'
 * Method: 'POST'
 * Parameters: user_name
 * Returns: GameForm with initial game state.
 	* urlsafe_key
    * attempts_remaining
    * game_over
    * user_word (secret word with '-' replacing the letter that have not been guessed yet)
    * used_char (letters that user has submitted)
    * message
    * user_name
 * Description: Creates a new Game. user_name provided must correspond to an existing user. will raise a NotFoundException if not.


#### get_game

 * Path: 'game/{urlsafe_game_key}'
 * Method: 'GET'
 * Parameters: urlsafe_game_key
 * Returns: GameForm with current game state.
 	* urlsafe_key
    * attempts_remaining
    * game_over
    * user_word (secret word with '-' replacing the letter that have not been guessed yet)
    * used_char (letters that user has submitted)
    * message
    * user_name
 * Description: Returns the current state of a game.

#### get_games

 * Path: 'games'
 * Method: 'GET'
 * Parameters: N/A
 * Returns: GameForms with state for each game. (list of GameForm)
 * Description: Returns all games with state for each game.

#### cancel_game

 * Path: 'game/cancel/{urlsafe_game_key}'
 * Method: 'DELETE'
 * Parameters: urlsafe_game_key
 * Returns: StringMessage
 * Description: Cancels requested game if it is not over.

#### get_user_games

 * Path: 'games/user/{user_name}'
 * Method: 'GET'
 * Parameters: user_name, email (optional)
 * Returns: GameForms. (list of GameForm)
 * Description: Get all games for user specified (unordered). user_name provided must correspond to an existing user. will raise a NotFoundException if not.

#### get_game_history

 * Path: 'game/{urlsafe_game_key}/history'
 * Method: 'GET'
 * Parameters: urlsafe_game_key
 * Returns: StringMessage
 * Description: Gets history of moves for any game.

#### get_scores

 * Path: 'scores'
 * Method: 'GET'
 * Parameters: N/A
 * Returns: ScoreForms. (list of ScoreForm)
 * Description: Returns all Scores in the database (unordered).

#### get_user_scores

 * Path: 'scores/user/{user_name}'
 * Method: 'GET'
 * Parameters: user_name, email (optional)
 * Returns: ScoreForms. (list of ScoreForm)
 * Description: Returns all Scores for specified user in the database (unordered).
user_name provided must correspond to an existing user. will raise a NotFoundException if not.

#### get_high_scores

 * Path: 'scores/leader-board'
 * Method: 'GET'
 * Parameters: number_of_results (optional)
 * Returns: ScoreForms. (list of ScoreForm)
 * Description: Get ordered high scores for hangman. Optional parameter will decide how many results to show,
and if no parameter is provided all results will show.


#### get_user_rankings

 * Path: 'users/rankings'
 * Method: 'GET'
 * Parameters: N/A
 * Returns: UserForms. (list of UserForm)
 * Description: Returns all users ordered by highest point.


#### make_move

 * Path: 'game/{urlsafe_game_key}'
 * Method: 'PUT'
 * Parameters: urlsafe_game_key, guess
 * Returns: GameForm with new game state.
 	* urlsafe_key
    * attempts_remaining
    * game_over
    * user_word (secret word with '-' replacing the letter that have not been guessed yet)
    * used_char (letters that user has submitted)
    * message
    * user_nam
 * Description: Accepts a 'guess' and returns the updated state of the game. If this causes a game to end, a corresponding Score entity will be created.

### Forms

#### UserForm

* name (player username)
* email
* points (total number of points)

#### ScoreForm

* user_name
* date
* won (game status)
* guesses (difference between attempts_allowed and attempts_remaining)

## Local Installation

### Prerequisite tools

1. [Create New Project](https://console.developers.google.com/)
2. [Python 2.7](https://www.python.org/downloads/)
3. [Google App Engine](https://cloud.google.com/appengine/)

### Clone Project

1. clone repository or download as zip file
    * git clone ``` https://github.com/elmasria/hangman-game-api.git ```
2. navigate to repository ``` cd hangman-game-api ```
3. Open app.yaml and Update 'application' by your app ID (registered in the App Engine admin console)

### Run Application Locally

1. Open Google App Engine
2. Add Existing Project (Select hangman-game-api folder)
3. Press Run
4. Press Browse
5. To test the API navigate to ``` http://localhost:{SELECTED PORT}/_ah/api/explorer ```


Hint:
While launching chrome to test the API, you will have to launch it using the console as follows:
```
[path-to-Chrome] --user-data-dir=test --unsafely-treat-insecure-origin-as-secure=http://localhost:port
````
