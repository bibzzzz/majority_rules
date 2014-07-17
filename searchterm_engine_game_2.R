#########

library(XML)
library(RCurl)
library(stringr)
library(plyr)

#EXECUTE CONFIG#

#game config - exectued upon setup - sourced from game config script that is created by web interface
#config dir is only line that gets updated with creation of new game
config_dir <- "C:\\Users\\habib.adam\\Documents\\personal\\majority_rules\\games\\game_2\\"
source(paste0(config_dir,"config.R"))

#END CONFIG#


################


##user_phase_1
#enter search term - this needs to connect to web platform#
source(paste0(game_dir,"searchterm_file.R"))
#click submit

##

#########

##output_phase_1
#convert search term to url format
search_term <- str_replace_all(initial_search_term," ","+")

search_term_url <- paste0(base_search_url,search_term)
search_results <- getURL(search_term_url)

search_results_table <- ldply(xmlToList(search_results), data.frame)
search_results_table <- search_results_table[as.character(search_results_table$suggestion)!=initial_search_term,]
n_suggestions <- length(search_results_table$suggestion)

if (n_suggestions>=n_players){
  #provide list of possible answers in randomized order 
  answer_output <- data.frame(answer_options=search_results_table$suggestion[sample(1:n_suggestions)])
  #print(answer_output)
  write.csv(answer_output,file=paste0(game_dir,"answer_output.csv"),row.names=FALSE)
  write.csv(search_results_table,file=paste0(game_dir,"search_results_table.csv"),row.names=FALSE)
}else{
  answer_output <- "not enough autocomplete results for this question, please suggest a new one."
  #print("not enough autocomplete results for this question, please suggest a new one.")
  write.csv(answer_output,file=paste0(game_dir,"answer_output.csv"),row.names=FALSE)
}

##

#########