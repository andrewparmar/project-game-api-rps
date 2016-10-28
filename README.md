# Udacity Game API Project

What this is about?
-------------------

This is a simple Google App Engine endpoints API project as part of the Udacity Full Stack course. The objective was to develop a simple API with endpoints that will allow anyone to develop a front-end for a fully functional Rock-Paper-Scissors game. The API can be used to start games, keep track of scores for individual users, and even all time top 10 high scores.



How do I use this?
------------------

Quick usage:
1. Goto https://cloud.google.com/appengine/docs/python/download, download and install the App Engine SDK.
Goto the folder containing the app.yaml file.
2. Run the command dev_appserver.py app.yaml
3. Start a Chrome session with special flags by following the instuction here https://developers.google.com/explorer-help/#hitting_local_api
This will allow you to run api explorer locally ove http. Make sure you choose the option to Load Unsafe scripts in the browsser search bar error shiled icon.
4. Goto localhost:8080/_ah/api/explorer
5. Start by creating a new user
6. Create a new game - select the number of rounds and the name of the user creating the game. Copy the urlsafe_key. You will use this when making moves.
7. Choose the make move endpoint to play the game. To make a type one of the following 'ROCK', 'PAPER', or 'SCISSORS' and the player name
8. The output reponse should tell you the result of the round and other game stats
9. Repeat steps 7 and 8 until response shows 'game_over' = True

Explaination of each of the endpoiints
--------------------------------------

rock_paper_scissors.ncreate_user
	Create a User. Requires a unique username
	Takes two arguments, the user's email address, and a username.

rock_paper_scissors.new_game
	Create a new game.
	Takes two argument, a username and an integer which is the desired number of rounds for the game. Ideally, this should be an odd number 3 or above.

rock_paper_scissors.make_move
	Allows the user to make a move. Return the result of the round
	Takes in two arguments. The move which is one of ROCK, PAPER or SCISSOR. The second argument is the username. This endpoint also invokes the computer to make a move. The result of the round is then computed and the result is displayed. Each time a move is made, the rounds left decreases by one until the game is over. At this point, the complete score and outcome of the game is calculated and saved.

rock_paper_scissors.get_game
	Return the current game state.
	Allows the user to retrive the state of any game. Takes the games unique key as the only argument.

rock_paper_scissors.cancel_games
	Allows the user to cancel a game
	Takes the unique game key as the argument. Cancels the game by setting game_cancelled = True. Once cancelled, no moves can be played for the remainder of the rounds of the game.

rock_paper_scissors.get_game_history
	Returns a round by round history of the moves played
	Take the unique game key as the argument. Returns a complete history of all the moves made by the player and the computer during each round. Also states the winner of the round againt each pair of moves for each round.

rock_paper_scissors.get_scores
	Return all scores from each game stored in datastore
	Does not take any arguments. Returns the point tally for player and computer for each game in the datastore.

rock_paper_scissors.get_high_scores
	Returns lis of all the games in datastore, while sorting by highest score first.
	Does not take any arguments.

rock_paper_scissors.get_user_scores
	Returns all of an individual User's scores for each game. Take in the username as the only argument.

rock_paper_scissors.get_user_games
	Returns all games created by a user. Takes in the username as the only argument.

rock_paper_scissor.get_user_rankings
	Returns a list of all the users, ordered by total win_rate. The win rate is caculated by dividing all the points won by a users across all games, divided by the total number of rounds played across all games. The sort order is highest to lowest. The higher the win_rate, the higher the users ranking.

Scorekeeping

The scoring system is based on wins and losses against individual rounds in each rock paper scissor game. Each point won by the player adds one to the players score. Each win by the computer subtracs from the players score. However, the users score cannot drop below 0.
