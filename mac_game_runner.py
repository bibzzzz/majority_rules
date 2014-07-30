import mac_scripts


print("WELCOME TO A NEW GAME OF MAJORITY RULES")
round_number = 1

rounds = input("Configure your game - enter how many rounds you want to play: ")
mac_scripts.setup_game(rounds)
print ("Each player will get to ask %s questions..." % rounds)

players = input("Configure your game - enter names of players (seperated by commas): ")
mac_scripts.setup_users(players)


while (round_number <= mac_scripts.n_players*mac_scripts.n_rounds):

       search_term = input("Enter search term:")
       mac_scripts.search_term_execute(search_term)

       while (mac_scripts.n_suggestions < mac_scripts.n_players):
           search_term = input("Enter search term:")
           suggestion_options = mac_scripts.search_term_execute(search_term)          

       #loop through for each user and del entries that are already selected
       user_answers = []
       
       for user in mac_scripts.a_players:
              for item in mac_scripts.random_list:
                     print("%d: %s" % (item,mac_scripts.random_list[item]))
              user_answer_entry = input("%s, please enter your selection from the list above: " % user)
              possible_answers = list(mac_scripts.random_list.keys())
              user_answers.append(int(user_answer_entry))
              del mac_scripts.random_list[int(user_answer_entry)]
              
       #if any user_answers are outside the range then BREAK
       mac_scripts.answer_submit(user_answers)

       print("The scores for this round are: ")
       for item in mac_scripts.user_scores:
              print(item)

       print("The total scores are: ")
       for item in mac_scripts.game_totals:
              print(item)
              
       input("Press ENTER to continue")
       round_number += 1
       if (round_number <= mac_scripts.n_players*mac_scripts.n_rounds):
           mac_scripts.play_next_round()


input("GAME OVER, press ENTER to see results: ")

print(mac_scripts.game_totals)

new_game_selection = input("THANKS FOR PLAYING, PRESS Y TO BEGIN NEW GAME OR ANY OTHER KEY TO END GAME... ")

if str.upper(new_game_selection) == "Y":
    import game_runner
    
