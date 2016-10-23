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

rock_paper_scissors.create_user
	Create a User. Requires a unique username
rock_paper_scissors.new_game
	Create a new game
rock_paper_scissors.make_move

rock_paper_scissors.get_game
	Return the current game state.
rock_paper_scissors.cancel_games
	Allows the user to cancel a game
rock_paper_scissors.get_game_history
	Allows the user to cancel a game
rock_paper_scissors.get_scores
	Return all scores
rock_paper_scissors.get_high_scores
	Allows the user to cancel a game
rock_paper_scissors.get_user_scores
	Returns all of an individual User's scores
rock_paper_scissors.get_user_games
	Returns all of a User's active games








rock_paper_scissors.sayHello

