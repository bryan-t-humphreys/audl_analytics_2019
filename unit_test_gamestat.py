
from utils import get_avg_hangtime, get_event_counts

def game_stat_test(team1_name, team2_name, team_dict, datetime_of_game):

    team1_df = team_dict[team1_name]
    team1_df_filtered = team1_df[team1_df['Opponent'] == team2_name]
    team1_df_filtered2 = team1_df_filtered[team1_df_filtered['Date/Time'] == datetime_of_game]    

    team2_df = team_dict[team2_name]
    team2_df_filtered = team2_df[team2_df['Opponent'] == team1_name]
    team2_df_filtered2 = team2_df_filtered[team2_df_filtered['Date/Time'] == datetime_of_game]    

    ht_team1 = get_avg_hangtime(team1_df_filtered2)
    print("Average Hangtime for Pull:  {0} = {1}".format(team1_name,ht_team1))

    ht_team2 = get_avg_hangtime(team2_df_filtered2)
    print("Average Hangtime for Pull:  {0} = {1}".format(team2_name,ht_team2))

    team1_counts_o, team1_counts_d = get_event_counts(team1_df_filtered2)
    team1_ocounts_o, team1_ocounts_d = get_event_counts(team1_df_filtered2,line='offense')
    team1_dcounts_o, team1_dcounts_d = get_event_counts(team1_df_filtered2,line='defense')

    team2_counts_o, team2_counts_d = get_event_counts(team2_df_filtered2)
    team2_ocounts_o, team2_ocounts_d = get_event_counts(team2_df_filtered2,line='offense')
    team2_dcounts_o, team2_dcounts_d = get_event_counts(team2_df_filtered2,line='defense')

    print("{} Total Stats: \n".format(team1_name))
    print("OFFENSE:")
    print(team1_counts_o)
    print("DEFENSE:")
    print(team1_counts_d)
    print("--------------\n")

    print("{} O-Line Stats: \n".format(team1_name))
    print("OFFENSE:")
    print(team1_ocounts_o)
    print("DEFENSE:")
    print(team1_ocounts_d)
    print("--------------\n")

    print("{} D-Line Stats: \n".format(team1_name))
    print("OFFENSE:")
    print(team1_dcounts_o)
    print("DEFENSE:")
    print(team1_dcounts_d)
    print("--------------\n")

    print("{} Total Stats: \n".format(team2_name))
    print("OFFENSE:")
    print(team2_counts_o)
    print("DEFENSE:")
    print(team2_counts_d)
    print("--------------\n")

    print("{} O-Line Stats: \n".format(team2_name))
    print("OFFENSE:")
    print(team2_ocounts_o)
    print("DEFENSE:")
    print(team2_ocounts_d)
    print("--------------\n")

    print("{} D-Line Stats: \n".format(team2_name))
    print("OFFENSE:")
    print(team2_dcounts_o)
    print("DEFENSE:")
    print(team2_dcounts_d)
    print("--------------\n")