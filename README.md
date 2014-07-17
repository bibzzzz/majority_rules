majority_rules
==============

code repository for majority rules game


config.R - takes game config inputs defined by users

searchterm_file.R - contains the search term for the round and is continually overwritten by users each round

searhterm_engine_game_2.R - processes the searchterm within searchterm_file.R and outputs the list of suggested autocompletions *answer_output.csv*, as well as the actual autocomplete results *search_results_table.csv*

seachterm_engine_execute.bat - batch file to execute the searchterm_engine

answer_file.R - contains a vector of users answers in order of player (eg. [player_1,player_2,player_3...player_n])

scoring_engine_game_2.R - computes the scoring based on the answers and autocompletion results and outputs the scores as they stand after that round *game_score_totals.csv* and updates the game history containing all previous round results *game_history.csv*
