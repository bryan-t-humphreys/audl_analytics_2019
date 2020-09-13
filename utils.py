#!/usr/bin/env python
# coding: utf-8

"""utils.py hosts various data computation utility functions for the repository.

Be sure to first create and index the files to search through.  (See stars_index_search.py)

Example:
        from utils import get_event_counts

"""

import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
import statistics

from scipy.stats import nbinom
from itertools import groupby
from plotly.offline import plot, iplot

def get_event_counts(df,line=['offense','defense']):
    ''' Function to obtain offensive and defensive team stats
    
            - Option filter: for 'offense' or 'defense' lines.  Leave line parameter blank for no filter
            - Offensive Event Types:  'Catch', 'Throwaway', 'Goal', 'Drop'
            - Defensive Event Types:  'D', 'Throwaway', 'Goal', 'Pull', 'PullOb'
    
        Parameters:
            df         -     pandas dataframe of the game stats
            line       -     option string ('offense' or 'defense') to filter for specific stats
            
        Returns:
            dict_out_off   -     dictionary output of the offensive stats.  key:(event type), value:(count)
            dict_out_def   -     dictionary output of the defensive stats.  key:(event type), value:(count)
            
    '''
    
    if line == 'offense':
        df1 = df[df.Line == 'O']
    elif line == 'defense':
        df1 = df[df.Line == 'D']
    else:
        df1 = df
    
    dict_out_off = df1[df1['Event Type'] == 'Offense'].groupby('Action')['Event Type'].count().to_dict()
    dict_off = {}
    dict_off['catch'] = dict_out_off.get('Catch',0)
    dict_off['throwaway'] = dict_out_off.get('Throwaway',0)
    dict_off['drop'] = dict_out_off.get('Drop',0)
    dict_off['goal'] = dict_out_off.get('Goal',0)
    dict_off['turnovers'] = dict_off['drop'] + dict_off['throwaway']

    dict_out_def = df1[df1['Event Type'] == 'Defense'].groupby('Action')['Event Type'].count().to_dict()
    dict_def = {}
    dict_def['d'] = dict_out_def.get('D',0)
    dict_def['throwaway'] = dict_out_def.get('Throwaway',0)
    dict_def['pull'] = dict_out_def.get('Pull',0)
    dict_def['pullob'] = dict_out_def.get('PullOb',0)
    dict_def['goal'] = dict_out_def.get('Goal',0)
    dict_def['turnovers'] = dict_def['d'] + dict_def['throwaway']

    return(dict_off,dict_def)

def get_avg_hangtime(df):
    ''' Function to obtain average hangtime (in seconds) of pulls
    
        Parameters:
            df         -     pandas dataframe of the game stats
            
        Returns:
            avg_hangtime   -     float object for the average hangtime
            
    '''
    df_d = df[df['Event Type'] == 'Defense']
    df_d_pullhangtime = df_d[df_d['Action'] == 'Pull']['Hang Time (secs)']
    
    df_pullhangtime_nonan = [i for i in df_d_pullhangtime if (math.isnan(i) == False)]
    
    try:
        avg_hangtime = sum(df_pullhangtime_nonan)/len(df_pullhangtime_nonan)
    except:
        avg_hangtime=None
    
    return(avg_hangtime)

def collect_stats_for_teams(team_dict=None):
    ''' Function to collect the stats of each game into a json-type dictionary
        id: 'team1-team2-date'
         - team1 and team2 are first sorted alphabetically, in order to avoid double counting the same game
    
        Parameters:
            team_dict         -     a dictionary that contains key: team_name, value: dataframe of season play-by-play stats
            
        Returns:
            game_dict         -     a dictionary that contains game stats for each game of the season between all teams/games in the team_dict
            
    '''
    game_dict = {}

    for tm in team_dict.keys():
        df = team_dict[tm]

        for dte in list(set(df['Date/Time'])):
            df_dte = df[df['Date/Time'] == dte ]

            teamz = [tm, df_dte['Opponent'].iloc[0]]
            teamz.sort()
            kee = str(dte.split(" ")[0]) + "|" + teamz[0] + "|" + teamz[1]

            team_offensive_stats, team_defensive_stats = get_event_counts(df_dte)
            oline_offensive_stats, oline_defensive_stats = get_event_counts(df_dte, line="offense")
            dline_offensive_stats, dline_defensive_stats = get_event_counts(df_dte, line="defense")

            if kee not in game_dict.keys():
                game_dict[kee] = {}
                game_dict[kee]["game_date"] = dte
                game_dict[kee]["team1"] = {}
                game_dict[kee]["team2"] = {}

                game_dict[kee]["team1"]["team"] = teamz[0]
                game_dict[kee]["team2"]["team"] = teamz[1]

                game_dict[kee]["team1"]["stats"] = {}
                game_dict[kee]["team2"]["stats"] = {}

                if game_dict[kee]["team1"]["team"] == tm:

                    game_dict[kee]["team1"]["stats"]["avg_hangtime_pull"] = get_avg_hangtime(df_dte)

                    game_dict[kee]["team1"]["stats"]["team_offensive_stats"] = team_offensive_stats
                    game_dict[kee]["team1"]["stats"]["team_defensive_stats"] = team_defensive_stats

                    game_dict[kee]["team1"]["stats"]["oline_offensive_stats"] = oline_offensive_stats
                    game_dict[kee]["team1"]["stats"]["oline_defensive_stats"] = oline_defensive_stats

                    game_dict[kee]["team1"]["stats"]["dline_offensive_stats"] = dline_offensive_stats
                    game_dict[kee]["team1"]["stats"]["dline_defensive_stats"] = dline_defensive_stats

                elif game_dict[kee]["team2"]["team"] == tm:

                    game_dict[kee]["team2"]["stats"]["avg_hangtime_pull"] = get_avg_hangtime(df_dte)

                    game_dict[kee]["team2"]["stats"]["team_offensive_stats"] = team_offensive_stats
                    game_dict[kee]["team2"]["stats"]["team_defensive_stats"] = team_defensive_stats

                    game_dict[kee]["team2"]["stats"]["oline_offensive_stats"] = oline_offensive_stats
                    game_dict[kee]["team2"]["stats"]["oline_defensive_stats"] = oline_defensive_stats

                    game_dict[kee]["team2"]["stats"]["dline_offensive_stats"] = dline_offensive_stats
                    game_dict[kee]["team2"]["stats"]["dline_defensive_stats"] = dline_defensive_stats


            elif kee in game_dict.keys():

                if game_dict[kee]["team1"]["team"] == tm:
                    game_dict[kee]["team1"]["stats"]["avg_hangtime_pull"] = get_avg_hangtime(df_dte)

                    game_dict[kee]["team1"]["stats"]["team_offensive_stats"] = team_offensive_stats
                    game_dict[kee]["team1"]["stats"]["team_defensive_stats"] = team_defensive_stats

                    game_dict[kee]["team1"]["stats"]["oline_offensive_stats"] = oline_offensive_stats
                    game_dict[kee]["team1"]["stats"]["oline_defensive_stats"] = oline_defensive_stats

                    game_dict[kee]["team1"]["stats"]["dline_offensive_stats"] = dline_offensive_stats
                    game_dict[kee]["team1"]["stats"]["dline_defensive_stats"] = dline_defensive_stats

                elif game_dict[kee]["team2"]["team"] == tm:
                    game_dict[kee]["team2"]["stats"]["avg_hangtime_pull"] = get_avg_hangtime(df_dte)

                    game_dict[kee]["team2"]["stats"]["team_offensive_stats"] = team_offensive_stats
                    game_dict[kee]["team2"]["stats"]["team_defensive_stats"] = team_defensive_stats

                    game_dict[kee]["team2"]["stats"]["oline_offensive_stats"] = oline_offensive_stats
                    game_dict[kee]["team2"]["stats"]["oline_defensive_stats"] = oline_defensive_stats

                    game_dict[kee]["team2"]["stats"]["dline_offensive_stats"] = dline_offensive_stats
                    game_dict[kee]["team2"]["stats"]["dline_defensive_stats"] = dline_defensive_stats

    return(game_dict)

def flatten_out_games(game_dict=None):
    ''' Transforms the game stats (calculated in collect_stats_for_teams) from a json-dictonary format to a pandas dataframe

        Parameters:
            game_dict         -     a dictionary that contains game stats for each game of the season between all teams/games in the team_dict
                              -     this input dictionary originates from the collect_stats_for_teams function
            
        Returns:
            df_stats         -     pandas dataframe of the stats
            
    '''
    i = 0
    for game in game_dict.keys():

        try:
            team1_to_commited = max([game_dict[game]['team1']['stats']['team_offensive_stats']['turnovers'],game_dict[game]['team2']['stats']['team_defensive_stats']['turnovers']])
       
            team2_to_commited = max([game_dict[game]['team2']['stats']['team_offensive_stats']['turnovers'],game_dict[game]['team1']['stats']['team_defensive_stats']['turnovers']])

            team1_points_scored = max([game_dict[game]['team1']['stats']['team_offensive_stats']['goal'],game_dict[game]['team2']['stats']['team_defensive_stats']['goal']])
            team2_points_scored = max([game_dict[game]['team2']['stats']['team_offensive_stats']['goal'],game_dict[game]['team1']['stats']['team_defensive_stats']['goal']])

            team1_avg_hangtime= game_dict[game]['team1']['stats']['avg_hangtime_pull']
            team2_avg_hangtime = game_dict[game]['team2']['stats']['avg_hangtime_pull']

            team1_catches= game_dict[game]['team1']['stats']['team_offensive_stats']['catch']
            team2_catches = game_dict[game]['team2']['stats']['team_offensive_stats']['catch']


            dict_row = {'date':game_dict[game]['game_date'],
                        'team1':game_dict[game]['team1']['team'],
                        'team2':game_dict[game]['team2']['team'],
                        'team1_offensive_to_commited': team1_to_commited,
                        'team2_offensive_to_commited': team2_to_commited,
                        'team1_points_scored':team1_points_scored,
                        'team2_points_scored':team2_points_scored,
                        'team1_avg_hangtime_pull':team1_avg_hangtime,
                        'team2_avg_hangtime_pull':team2_avg_hangtime,
                        'team1_catches':team1_catches,
                        'team2_catches':team2_catches}

            df_row = pd.DataFrame.from_dict(dict_row, orient='index').transpose()

            if i == 0:
                df_stats = df_row
            else:
                df_stats = df_stats.append(df_row)
            i = 1
        except:
            pass
    df_stats = df_stats.reset_index(drop=True)
    return(df_stats)

def get_game_stats(team_dict):
    ''' Obtain dictionary and data frame of stats
    
        Parameters:
            team_dict         -     a dictionary that contains key team_name, value dataframe of season play-by-play stats
            
        Returns:
            game_dict         -     dictionary
            df_stats          -     dataframe
    '''
    game_dict = collect_stats_for_teams(team_dict)
    df_stats = flatten_out_games(game_dict)
    return(game_dict,df_stats)

def get_turnover_plot_data(df_stats=None,team=None):
    ''' Obtain turnover stats used for boxplot

        Parameters:
            df_stats         -     the dataframe output from flatten_out_games
            team             -     a string indicating which team to produce the boxplot data for
            
        Returns:
            plot_data       -      dataframe used for plotting
    '''
    o_to_list = []
    d_to_list = []
    date_list = []
    
    for i in range(len(df_stats)):
        df_to_row = df_stats.iloc[i]

        team1 = df_to_row["team1"]
        team2 = df_to_row["team2"]

        
        if team1 == team:
            date_list.append(df_to_row["date"].split(" ")[0])
            o_to_list.append(df_to_row["team1_offensive_to_commited"])
            d_to_list.append(df_to_row["team2_offensive_to_commited"])

        elif team2 == team:
            date_list.append(df_to_row["date"].split(" ")[0])
            d_to_list.append(df_to_row["team1_offensive_to_commited"])
            o_to_list.append(df_to_row["team2_offensive_to_commited"])

    date_list.extend(date_list)
    oos = ["Offense" for i in range(len(o_to_list))]
    dds = ["Defense" for i in range(len(d_to_list))]
    dds.extend(oos)
    median_of_offense = statistics.median(o_to_list)
    median_of_defense = statistics.median(d_to_list)
    d_to_list.extend(o_to_list)

    plot_data = pd.DataFrame({"Date":date_list,"Line":dds, "Turnovers":d_to_list}).sort_values("Date")
    return(plot_data,median_of_offense,median_of_defense)

def plot_turnovers(df_stats,
                   teams_list=['San Jose Spiders', 'Seattle Cascades', 'Los Angeles Aviators', 'San Diego Growlers'],
                   graph_colors_dict={'San Jose Spiders':'gold','Seattle Cascades':'navy','San Diego Growlers':'black','Los Angeles Aviators':'crimson'},
                   sort_by=None
                   ):
    ''' Produce the figure for plotting boxplot of turnovers, by team
        AS OF RIGHT NOW, ONLY TEAMS IN THE WEST DIVISION

        Parameters:
            teams_list       -     list of teams
            df_stats         -     dataframe produced from flatten_out_games function
            
        Returns:
            fig              -      plotly figure for plotting
    '''
    plot_data_dict = {}
    fig = go.Figure()
    j = 0
    for tm in teams_list:
        plot_data_dict[tm],median_o,median_d = get_turnover_plot_data(df_stats, team=tm)
        row_df = pd.DataFrame.from_dict({'Team':tm,'Median_O':median_o,'Median_D':median_d},orient='index').transpose()
        if j == 0:
            df_median = row_df
        else:
            df_median = df_median.append(row_df)
        j+=1

    if sort_by == "offense":
        df_median = df_median.sort_values('Median_O',ascending=False)
    elif sort_by == "defense":
        df_median = df_median.sort_values('Median_D',ascending=True)

    for k in range(len(df_median)):

        row = df_median.iloc[k]
        tm = row['Team']
        print(plot_data_dict[tm]['Turnovers'])
        print(plot_data_dict[tm]['Line'])
        fig.add_trace(go.Box(x=plot_data_dict[tm]['Turnovers'],
                             y=plot_data_dict[tm]['Line'],
                             marker_color=graph_colors_dict[tm],
                             marker_line_color = "black",
                             name=tm)
                    )
    fig.update_layout(title="Turnovers Committed (O) and Turnovers Forced (D), 2019 Season",
                      xaxis_title="Team",
                      yaxis_title="Count of Turnovers",
                      boxmode='group',
                      plot_bgcolor='rgb(220,220,220)',
                      height= 1500
                      )
    
    fig.update_traces(orientation='h')

    return(fig)

def get_season_total_turnovers(df_stats,teams_list):
    j = 0
    for tm in teams_list:
        to_df, _, _ = get_turnover_plot_data(df_stats=df_stats,team=tm)
        tos = sum(to_df['Turnovers'])

        row = pd.DataFrame.from_dict({"Team":tm,"SeasonTurnovers":tos},orient='index').transpose()

        if j == 0:
            df_out = row
        else:
            df_out = df_out.append(row)

        j +=1
    df_out = df_out.reset_index(drop=True)
    return(df_out)

def get_points_plot_data(df_stats=None,team=None):
    ''' Obtain goals scored and allowed used for histogram

        Parameters:
            df_stats         -     the dataframe output from flatten_out_games
            team             -     a string indicating which team to produce the boxplot data for
            
        Returns:
            plot_data       -      dataframe used for plotting
    '''
    o_points_list = []
    d_points_list = []
    
    for i in range(len(df_stats)):
        df_points_row = df_stats.iloc[i]

        team1 = df_points_row["team1"]
        team2 = df_points_row["team2"]

        
        if team1 == team:
            o_points_list.append(df_points_row["team1_points_scored"])
            d_points_list.append(df_points_row["team2_points_scored"])

        elif team2 == team:
            d_points_list.append(df_points_row["team1_points_scored"])
            o_points_list.append(df_points_row["team2_points_scored"])

    o_points_count = round(sum(o_points_list)/len(o_points_list),2)
    d_points_count = round(sum(d_points_list)/len(d_points_list),2)

    plus_minus = sum(o_points_list) - sum(d_points_list)
    
    plot_data = pd.DataFrame({"Line":['Offense','Defense'], "Points":[o_points_count,d_points_count]})
    return(plot_data, plus_minus)

def plot_goals(teams_list=None,
               df_stats=None, 
               team_col_dict=None
               ):
    ''' Produce the figure for plotting barplot for goals scored/allowed, by team
        AS OF RIGHT NOW, ONLY TEAMS IN THE WEST DIVISION

        Parameters:
            teams_list       -     list of teams
            df_stats         -     dataframe produced from flatten_out_games function
            
        Returns:
            fig              -      plotly figure for plotting
    '''
    plot_data_dict = {}
    points_list_o = []
    points_list_d = []
    tm_colors = []
    plus_minus_list = []
    for tm in teams_list:
        plot_data_dict[tm],plus_minus = get_points_plot_data(df_stats, team=tm)

        points_list_o.append(plot_data_dict[tm]['Points'][0])
        points_list_d.append(plot_data_dict[tm]['Points'][1])
    
        tm_colors.append(team_col_dict[tm])

        plus_minus_list.append(plus_minus)

    df_plot = pd.DataFrame.from_dict({"Team":teams_list,"GoalsScored":points_list_o,"GoalsAllowed":points_list_d,"PlusMinus":plus_minus_list, "Colors":tm_colors},orient='index').transpose()
    df_plot = df_plot.sort_values("PlusMinus",ascending=True)
    hover_text = [str(df_plot['Team'].iloc[i]) + " +/- : " + str(df_plot['PlusMinus'].iloc[i]) for i in range(len(df_plot))]
    df_plot['hover_text'] = hover_text

    fig = go.Figure()

    fig.add_trace(go.Bar(name="Avg. Goals Allowed (Defense)",
                         y=df_plot['Team'],
                         x=df_plot['GoalsAllowed'],
                         text=df_plot['GoalsAllowed'],
                         textposition='auto',
                         textfont=dict(
                                        family="arial",
                                        size=14,
                                        ),
                         marker_line_color="black",
                         hovertext=df_plot['hover_text'],
                         opacity=0.3,
                         orientation='h')
                 )

    fig.add_trace(go.Bar(name="Avg. Goals Scored (Offense)",
                         y=df_plot['Team'],
                         x=df_plot['GoalsScored'],
                         text=df_plot['GoalsScored'],
                         textposition='auto',
                         textfont=dict(
                                        family="arial",
                                        size=14,
                                        ),
                         marker_line_color="black",
                         hovertext=df_plot['hover_text'],
                         opacity=0.6,
                         orientation='h')
                )

    fig.update_layout(title="Avg. Goals Scored (O) and Avg. Goals Allowed (D), 2019 Season: Sorted By Team +/- (Descending, Left to Right)",
                      xaxis_title="Team",
                      yaxis_title="Avg. Goals Per Game (2019 Season)",
                      bargap=0.15, # gap between bars of adjacent location coordinates.
                      bargroupgap=0.1, # gap between bars of the same location coordinate.
                      plot_bgcolor='rgb(220,220,220)',
                      height= 1500
                      #legend_orientation="h"
                      )

    
    fig.update_traces(marker_color=df_plot['Colors'],
                      marker_line_width=2)

    return(fig)

def get_sequences(df_input):
    beginning_of_point = '0-0'
    end_of_point = '0-0'
    sequences = {}
    sequences_index = 0
    sequence = []

    prev_event_type = None
    current_event_type = None
    prev_action = None

    for i in range(len(df_input)):
        record = df_input.iloc[i]

        event_type = record['Event Type']
        current_event_type = event_type

        end_of_point = str(record['Our Score - End of Point']) + '-' + str(record['Their Score - End of Point'])
        action = record['Action']
        passer = record['Passer']
        reciever = record['Receiver']
        point_index = beginning_of_point + "||" + end_of_point

        if current_event_type == 'Offense':
            if prev_event_type == 'Defense' or prev_event_type == None:
                sequence = []
                sequence.append(action)

                if (prev_action == 'D' or prev_action == 'Throwaway' or prev_action == 'Goal') and (action == 'Goal' or action == 'Throwaway' or action == 'Drop'):

                    if point_index in sequences.keys():
                        sequences[point_index].append(sequence)
                    elif point_index not in sequences.keys():
                        sequences[point_index] = [sequence]

            elif prev_event_type == 'Offense':
                if prev_action == "Drop" or prev_action == "Throwaway":
                    sequence = []
                    sequence.append(action)
                    if action != "Catch":
                        if prev_point_index in sequences.keys():
                            sequences[prev_point_index].append(sequence)
                        elif prev_point_index not in sequences.keys():
                            sequences[prev_point_index] = [sequence]
                else:
                    sequence.append(action)
                    if action != "Catch":
                        if prev_point_index in sequences.keys():
                            sequences[prev_point_index].append(sequence)
                        elif prev_point_index not in sequences.keys():
                            sequences[prev_point_index] = [sequence]

        if current_event_type == 'Defense':
            if prev_event_type =='Defense':
                pass

            elif prev_event_type == 'Offense':
                if prev_action == "Catch":
                    if prev_point_index in sequences.keys():
                        sequences[prev_point_index].append(sequence)
                    elif prev_point_index not in sequences.keys():
                        sequences[prev_point_index] = [sequence]

        if action == 'Goal':
            beginning_of_point = end_of_point

        if i == (len(df_input)-1):
            if action == 'Catch':
                if prev_point_index in sequences.keys():
                    sequences[prev_point_index].append(sequence)
                elif prev_point_index not in sequences.keys():
                    sequences[prev_point_index] = [sequence]

        prev_event_type = current_event_type
        prev_point_index = point_index
        prev_action = action
    return(sequences)

def convert_date_sequences_to_list_and_count(date_sequences):
    list_of_sequences = []
    ## Place where we can add a filter of the sequences selected for modeling
    for kee1 in date_sequences.keys():
        s = date_sequences[kee1]
        for kee2 in s.keys():
            los = s[kee2]
            for l in los:
                list_of_sequences.append(l)

    counts = [len(i) for i in list_of_sequences]
    counts = [int(i)-1 for i in counts]
    counts.sort()
    counts = counts[:(len(counts)-1)]

    return(counts)

def collect_and_plot_passes_nb(teams_list=None,
                               teams_dict=None,
                               plot_output=['single','all'],
                               teams_col_dict=None):
    
    team_sequences = {}
    dict_of_passing_stats = {}
    all_sequences = []

    for tm in teams_list:
        passing_stats = {}
        df = teams_dict[tm]
        list_of_dates = set(df['Date/Time'])
        
        date_sequences = {}
        for d in list_of_dates:
            df_filter = df[df['Date/Time'] == d]
            df_filter = df_filter[df_filter['Event Type'] != 'Cessation']
            opponent = df_filter['Opponent'].iloc[0]
            kee = str(d) + ' | ' + opponent
            date_sequences[kee] = get_sequences(df_filter)
        team_sequences[tm] = date_sequences
        counts = convert_date_sequences_to_list_and_count(date_sequences)
        all_sequences.extend(counts)
            
        x_values_for_barplot = [key for key,group in groupby(counts)]
        y_values_for_barplot = [i/sum([len(list(group)) for key,group in groupby(counts)]) for i in [len(list(group)) for key,group in groupby(counts)]]

        ## (GP) NB Estimation
        mu = sum(counts) / len(counts)
        sigma = math.sqrt(sum([(mu - float(i))**2 for i in counts]) / (len([(mu - float(i))**2 for i in counts])-1))
        r = (mu**2)/(sigma**2 - mu)
        p = (mu)/(sigma**2)

        mean, var, skew, kurt = nbinom.stats(r, p, moments='mvsk')

        passing_stats['nb_probability']=p
        passing_stats['nb_r']=r
        passing_stats['avg_passes']=mean
        passing_stats['var_passes']=sigma**2
        passing_stats['nb_skew']=skew
        passing_stats['nb_kurtosis']=kurt

        dict_of_passing_stats[tm] = passing_stats
        
        if plot_output == 'single':
            x_values_for_nb = np.arange(nbinom.ppf(0.01, r, p),nbinom.ppf(0.9999, r, p))
            y_values_for_nb = nbinom.pmf(x_values_for_nb, r, p)

            fig = go.Figure( data=[go.Bar(x=x_values_for_barplot, 
                                          y=y_values_for_barplot,
                                          marker_color=teams_col_dict[tm],
                                          marker_line_color = "black",
                                          name="Passes Completed"
                                          )
                                   ]
                       )

            fig.add_trace(go.Scatter(x=x_values_for_nb, 
                                     y=y_values_for_nb,
                                     marker_color="black",
                                     mode='lines',
                                     name='Negative Binomial Approximation'))

            fig.update_layout(title="{}: Catch Counts, with Negative Binomial Estimation".format(tm),
                              xaxis_title="n Number of Catches",
                              yaxis_title="Frequency",
                              boxmode='group',
                              plot_bgcolor='rgb(220,220,220)'
                             )

            iplot(fig)
        
    all_sequences.sort()
    
    if plot_output == 'all':
        mu_a = sum(all_sequences) / len(all_sequences)
        sigma_a = math.sqrt(sum([(mu_a - float(i))**2 for i in all_sequences]) / (len([(mu_a - float(i))**2 for i in all_sequences])-1))
        r_a = (mu_a**2)/(sigma_a**2 - mu_a)    
        p_a = (mu_a)/(sigma_a**2)

        mean_a, var_a, skew_a, kurt_a = nbinom.stats(r_a, p_a, moments='mvsk')
        
        x_values_for_barplot_a = [key for key,group in groupby(all_sequences)]
        y_values_for_barplot_a = [i/sum([len(list(group)) for key,group in groupby(all_sequences)]) for i in [len(list(group)) for key,group in groupby(all_sequences)]]

        x_values_for_nb_a = np.arange(nbinom.ppf(0.01, r_a, p_a),nbinom.ppf(0.9999, r_a, p_a))
        y_values_for_nb_a = nbinom.pmf(x_values_for_nb_a, r_a, p_a)

        fig = go.Figure( data=[go.Bar(x=x_values_for_barplot_a, 
                                      y=y_values_for_barplot_a,
                                      marker_color="oldlace",
                                      marker_line_color = "black",
                                      name="Passes Completed"
                                      )
                                ]
                       )

        fig.add_trace(go.Scatter(x=x_values_for_nb_a, 
                                 y=y_values_for_nb_a,
                                 marker_color="black",
                                 mode='lines',
                                 name='Negative Binomial Approximation'))

        fig.update_layout(title="League Wide Catch Counts Per Possession, with Negative Binomial Estimation",
                          xaxis_title="n Number of Catches in a Possession",
                          yaxis_title="Frequency",
                          boxmode='group',
                          plot_bgcolor='rgb(220,220,220)'
                        )

        iplot(fig)
        
    return(dict_of_passing_stats, team_sequences, all_sequences)

