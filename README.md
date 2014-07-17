majority_rules
==============

code repository for majority rules game


<b>config.R</b> - takes game config inputs defined by users

<b>searchterm_file.R</b> - contains the search term for the round and is continually overwritten by users each round

<b>searhterm_engine_game_2.R</b> - processes the searchterm within searchterm_file.R and outputs the list of suggested autocompletions <b>answer_output.csv</b>, as well as the actual autocomplete results <b>search_results_table.csv</b>

<b>seachterm_engine_execute.bat</b> - batch file to execute the searchterm_engine

<b>answer_file.R</b> - contains a vector of users answers in order of player (eg. [player_1,player_2,player_3...player_n])

<b>scoring_engine_game_2.R</b> - computes the scoring based on the answers and autocompletion results and outputs the scores as they stand after that round <b>game_score_totals.csv</b> and updates the game history containing all previous round results <b>game_history.csv</b>
