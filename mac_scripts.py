#config
import urllib.request
import re
from xml.dom import minidom
import xml.etree.ElementTree
import random
import os.path
import csv
import numpy

usernames = ("Amy","Habib")
print("Creating game for: {}".format(usernames))
initial_search_term = 'cool tricks for'

answer_selections = [6,2]

#save_path = '/Users/amydonaldson/Desktop/majority_rules/'
#game_history_filename = os.path.join(save_path, "game_history.txt")
#point_totals_filename = os.path.join(save_path, "game_totals.txt")

#?output config settings: player_list file, base_url
#game_history_filename = 'game_history'
#game_history_completeName = os.path.join(save_path, game_history_filename+".txt")

#game_history_file = open(game_history_completeName, "w+")
#point_totals_file = open(point_totals_filename, "w+")

#game_history_file.close()
#point_totals_file.close()

def search_term_execute(usernames,initial_search_term):
    
    save_path = '/Users/amydonaldson/Desktop/majority_rules/'
    base_url = 'http://google.com/complete/search?output=toolbar&q='

    n_players = len(usernames)

    #create history files on game setup
    game_history_filename = os.path.join(save_path, "game_history.txt")
    point_totals_filename = os.path.join(save_path, "game_totals.txt")

    #?output config settings: player_list file, base_url
    game_history_filename = 'game_history'
    game_history_completeName = os.path.join(save_path, game_history_filename+".txt")

    game_history_file = open(game_history_completeName, "w+")
    point_totals_file = open(point_totals_filename, "w+")
    
    game_history_file.close()
    point_totals_file.close()

    #USER: request search term for round

    ##execute search_engine to generate search term results

    #read in config settings
    
    #adjust search_term
    adj_search_term = initial_search_term.replace (" ", "+")
    #create search_term_url
    search_term_url = base_url + adj_search_term

    with urllib.request.urlopen(search_term_url) as url:
        xml_string = url.read()

    xmldoc = minidom.parseString(xml_string)

    suggestion_list = xmldoc.getElementsByTagName('CompleteSuggestion') 
    n_suggestions = len(suggestion_list)
    pts_list = list(reversed(range(n_suggestions)))

    suggestion_tree = xml.etree.ElementTree.fromstring(xml_string)

    ordered_suggestion_list = list()

    for data in suggestion_tree.iter('suggestion'):
            suggestion = data.get('data')
            ordered_suggestion_list.append(suggestion)

    pts_ordered_suggestion_list = list(zip(ordered_suggestion_list, pts_list))

    random_suggestion_list = sorted(ordered_suggestion_list, key=lambda k: random.random())

    save_path = '/Users/amydonaldson/Desktop/majority_rules/'
    random_list_filename = 'random_list'
    pts_ordered_list_filename = 'pts_ordered_list'
    random_list_completeName = os.path.join(save_path, random_list_filename+".txt")
    pts_ordered_list_completeName = os.path.join(save_path, pts_ordered_list_filename+".txt")
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
    return(random_suggestion_list)

#USER: submit answer selections

    
def answer_submit(answer_selections):

    load_path = '/Users/amydonaldson/Desktop/majority_rules/'
    save_path = '/Users/amydonaldson/Desktop/majority_rules/'

    answer_table_filename = os.path.join(load_path, "pts_ordered_list.txt")
    game_history_filename = os.path.join(load_path, "game_history.txt")
    point_totals_filename = os.path.join(load_path, "game_totals.txt")
    random_suggestion_filename = os.path.join(load_path, "random_list.txt")
    round_scores_filename = os.path.join(load_path, "round_score.txt")


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

    #concatenate usernames and answer_selections

    player_answers = {"Amy":random_suggestion_list[answer_selections[0]],
                      "Habib":random_suggestion_list[answer_selections[1]]}

    user_scores = list()
    total_score_table = list()

    for user in usernames:
        user_answer = player_answers[user]
        #print(user_answer)
        for answer in answer_table:
            if user_answer[0] == answer[0]:
                user_points = float(answer[1]) + 1
                if len(point_totals) == 0:
                    user_total_points = user_points
                else:
                    for entry in point_totals:
                        if entry[0] == user:
                            user_total_points = float(entry[1]) + user_points
                    
        user_score_entry = (user, initial_search_term, user_answer[0], user_points)
        user_scores.append(user_score_entry)
        total_score_entry = (user, user_total_points)
        #convert user_score_entry to array before appending
        game_history_table.append(list(user_score_entry))
        total_score_table.append(total_score_entry)

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


#merge player_answers with round_answers table
#update game_totals file.

#output: round_results
#output: game_totals - +=
