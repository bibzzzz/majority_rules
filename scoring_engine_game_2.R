##user_phase_2
config_dir <- "C:\\Users\\habib.adam\\Documents\\personal\\majority_rules\\games\\game_2\\"
source(paste0(config_dir,"config.R"))
source(paste0(game_dir,"answer_file.R"))
source(paste0(game_dir,"searchterm_file.R"))

if (!file.exists(paste0(game_dir,"game_score_totals.csv"))){
  game_score_totals <- data.frame(total_score=rep(0,n_players),row.names=player_list)
}else{
  game_score_totals <- read.csv(file=paste0(game_dir,"game_score_totals.csv"))
}

if (!file.exists(paste0(game_dir,"game_history.csv"))){
  game_history <- NULL
}else{
  game_history <- read.csv(file=paste0(game_dir,"game_history.csv"))
}


#click submit

#######

#player_answer_selections <- sample(1:n_suggestions,n_players) #random execution for testing purposes
##

#read in searchterm_engine output
answer_output <- read.csv(file=paste0(game_dir,"answer_output.csv"))
search_results_table <- read.csv(file=paste0(game_dir,"search_results_table.csv"))

n_suggestions <- length(search_results_table$suggestion)

##output_phase_2
answer_input <- answer_output[player_answer_selections,]

answer_score_output <- NULL
for (answer in answer_input){
  suggestion_postion <- c(1:n_suggestions)[answer==search_results_table$suggestion]
  answer_score_output <- c(answer_score_output,(n_suggestions-suggestion_postion+1))
}

round_scores <- data.frame(question=initial_search_term,answer=answer_input,round_score=answer_score_output,player=player_list)

print(search_results_table)
print(round_scores)

game_history <- rbind(game_history,round_scores)

##

game_score_totals <- game_score_totals + answer_score_output
print(game_score_totals)

#write files
write.csv(game_history,file=paste0(game_dir,"game_history.csv"),row.names=FALSE)
write.csv(game_score_totals,file=paste0(game_dir,"game_score_totals.csv"),row.names=FALSE)
