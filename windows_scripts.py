#config
import urllib.request
import re
from xml.dom import minidom
import xml.etree.ElementTree
import random
import os
import csv
import numpy
import uuid

  
game_id = str(uuid.uuid4())

game_dir = 'C:\\Users\\habib.adam\\Documents\\dev\\majority_rules\\' + game_id

if not os.path.exists(game_dir):
                os.makedirs(game_dir)


base_url = 'http://google.com/complete/search?output=toolbar&q='
game_history_filename = os.path.join(game_dir, "game_history.txt")
point_totals_filename = os.path.join(game_dir, "game_totals.txt")
player_list_filename = os.path.join(game_dir, "player_list.txt")
q_player_filename = os.path.join(game_dir, "q_player_file.txt")
a_players_filename = os.path.join(game_dir, "a_players_file.txt")

#?output config settings: player_list file, base_url

def setup_game(rounds):
  
  global n_rounds
  n_rounds = int(rounds)

def setup_users(players):

  global usernames
  usernames = list(map(str,players.split(',')))

  global n_players
  n_players = len(usernames)

  print("Creating game for: {}".format(usernames))

  game_history_file = open(game_history_filename, "w+")
  point_totals_file = open(point_totals_filename, "w+")
  player_list_file = open(player_list_filename, "w+")
  q_player_file = open(q_player_filename, "w+")
  a_players_file = open(a_players_filename, "w+")

  game_history_file.close()

  for item in usernames:
      entry = "%s,0\n" % item
      point_totals_file.writelines(entry)

  point_totals_file.close()

  #set first player to initial question master

  q_player = usernames[0]
  global a_players
  a_players = usernames[1:]

  for item in usernames:
      entry = "%s\n" % item
      player_list_file.writelines(entry)

  for item in q_player:
      entry = "%s" % item
      q_player_file.writelines(entry)

  for item in a_players:
      entry = "%s\n" % item
      a_players_file.writelines(entry)

  player_list_file.close()
  q_player_file.close()
  a_players_file.close()

  print("%s, please pose a search term:" %q_player)
  

def play_next_round():


    datafile = open(player_list_filename, 'r+')
    datareader = csv.reader(datafile)
    player_list = list(datareader)

    datafile = open(q_player_filename, 'r+')
    datareader = csv.reader(datafile)
    q_player = list(datareader)

    n_players = len(player_list)

    q_index = []
    
    for x in enumerate(player_list):
        if x[1][0]==q_player[0][0]:
            q_index.append(x[0])
            if (q_index[0] + 1) >= n_players:
                q_index = 0
            else:
                q_index = q_index[0] + 1
                
    global a_players
    a_players = player_list[0:q_index] + player_list[(q_index+1):n_players]
    a_players = sum(a_players,[])
    
    q_player = player_list[q_index]

    print("%s, please pose a search term:" % q_player[0])

    a_players_file = open(a_players_filename, "w")
    q_player_file = open(q_player_filename, "w")

    for item in a_players:
        text_entry = "%s\n"
        line_entry = text_entry % item
        a_players_file.writelines(line_entry)
    a_players_file.close()

    for item in q_player:
      q_player_file.writelines("%s" % item)
    q_player_file.close()
    

def search_term_execute(search_term):

    global current_search_term
    if search_term:
      current_search_term = search_term
    else:
      current_search_term = ' '

    datafile = open(a_players_filename, 'r')
    datareader = csv.reader(datafile)
    a_players_list = list(datareader)

    datafile = open(q_player_filename, 'r')
    datareader = csv.reader(datafile)
    q_player = list(datareader)[0][0]
    
    #USER: request search term for round

    ##execute search_engine to generate search term results

    #read in config settings
    
    #adjust search_term
    adj_search_term = search_term.replace (" ", "+")
    #create search_term_url
    search_term_url = base_url + adj_search_term

    with urllib.request.urlopen(search_term_url) as url:
        xml_string = url.read()

    xmldoc = minidom.parseString(xml_string)

    suggestion_list = xmldoc.getElementsByTagName('CompleteSuggestion') 

    global n_suggestions
    n_suggestions = len(suggestion_list)

    if n_suggestions >= n_players:
        pts_list = list(reversed(range(n_suggestions)))

        suggestion_tree = xml.etree.ElementTree.fromstring(xml_string)

        ordered_suggestion_list = list()

        for data in suggestion_tree.iter('suggestion'):
                suggestion = data.get('data')
                ordered_suggestion_list.append(suggestion)

        pts_ordered_suggestion_list = list(zip(ordered_suggestion_list, pts_list))

        random_suggestion_list = sorted(ordered_suggestion_list, key=lambda k: random.random())

        global random_list
        random_list = {}
        i = 0
        for item in random_suggestion_list:
            random_list[i] = item
            i += 1
            

        random_list_filename = 'random_list'
        pts_ordered_list_filename = 'pts_ordered_list'
        random_list_completeName = os.path.join(game_dir, random_list_filename+".txt")
        pts_ordered_list_completeName = os.path.join(game_dir, pts_ordered_list_filename+".txt")
        random_list_file = open(random_list_completeName, "w")
        pts_ordered_list_file = open(pts_ordered_list_completeName, "w")

        #output: user_suggestions - randomized order index and autocomplete suggestions

        for item in random_suggestion_list:
          random_list_file.write("%s\n" % item)
        random_list_file.close()

        #output: round_answers - containing answers, the randomized order index, and associated points

        for item in pts_ordered_suggestion_list:
          pts_ordered_list_file.writelines("%s,%d\n" % item)
        pts_ordered_list_file.close()

        #feed options to user
        #print(random_suggestion_list)
        #print(a_players_list,"select answers from the following:")
        #print(random_suggestion_list)

    else:
        print("Not enough autocomplete suggestions, please suggest another search term.")
        print("%s, please pose a search term:" % q_player)


#USER: submit answer selections

    
def answer_submit(user_answers):

    #answer_selections = list(map(int,user_answers.split(',')))
    answer_selections = user_answers
    answer_table_filename = os.path.join(game_dir, "pts_ordered_list.txt")
    round_scores_filename = os.path.join(game_dir, "round_score.txt")
    random_suggestion_filename = os.path.join(game_dir, "random_list.txt")

    datafile = open(answer_table_filename, 'r')
    datareader = csv.reader(datafile)
    answer_table = list(datareader)

    datafile = open(game_history_filename, 'r+')
    datareader = csv.reader(datafile)
    game_history_table = list(datareader)

    datafile = open(point_totals_filename, 'r')
    datareader = csv.reader(datafile)
    point_totals = list(datareader)

    datafile = open(random_suggestion_filename, 'r')
    datareader = csv.reader(datafile)
    random_suggestion_list = list(datareader)

    datafile = open(a_players_filename, 'r')
    datareader = csv.reader(datafile)
    a_players_list = list(datareader)
    
    datafile = open(q_player_filename, 'r')
    datareader = csv.reader(datafile)
    q_player = list(datareader)[0][0]
    
    for item in point_totals:
        if item[0] == q_player:
            q_player_score = float(item[1])

    #concatenate usernames and answer_selections

    player_answers = {}
    i = 0

    for player in a_players_list:
        x = (player[0],random_suggestion_list[answer_selections[i]])
        player_answers[x[0]]=x[1]
        i = i + 1

    global user_scores
    user_scores = list()
    total_score_table = list()

    for user in a_players_list:
        user_answer = player_answers[user[0]]
        #print(user_answer)
        for answer in answer_table:
            if user_answer[0] == answer[0]:
                user_points = float(answer[1]) + 1
                if len(point_totals) == 0:
                    user_total_points = user_points
                else:
                    for entry in point_totals:
                        if entry[0] == user[0]:
                            user_total_points = float(entry[1]) + user_points
                    
        user_score_entry = (user[0], current_search_term, user_answer[0], user_points)
        user_scores.append(user_score_entry)
        total_score_entry = (user[0], user_total_points)
        #convert user_score_entry to array before appending
        game_history_table.append(list(user_score_entry))
        total_score_table.append(total_score_entry)

    total_score_table.append((q_player,q_player_score))

    global game_totals
    game_totals = total_score_table
    
    round_scores_file = open(round_scores_filename, "w")
    game_history_file = open(game_history_filename, "r+")
    point_totals_file = open(point_totals_filename, "r+")

    for item in user_scores:
      round_scores_file.writelines("%s,%s,%s,%d\n" % item)
    round_scores_file.close()

    for item in game_history_table:
        text_entry = "%s,%s,%s,%s\n"
        line_entry = text_entry % tuple(item)
        game_history_file.writelines(line_entry)
    game_history_file.close()

    for item in total_score_table:
      point_totals_file.writelines("%s,%d\n" % item)
    point_totals_file.close()

    #print(user_scores)
    #print(total_score_table)
