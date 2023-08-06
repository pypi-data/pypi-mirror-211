**myfootballanalytics** is a user-friendly, in-house developed python-based tool to analyse and visualise football data in order to assess the performance of football clubs and players and extract meaningful insights.

- Website: [https://github.com/isamathr/myfootballanalytics](url)
- Documentation: [https://github.com/isamathr/myfootballanalytics/blob/main/Instructions_manual.pdf](url)

## Capabilities

By using **myfootballanalytics**, you will be able to answer questions such as: 

1. Does Mourinho play the catenaccio of the modern years? 
2. Was Guardiola’s Barcelona better than Heynckes’s Bayern Munich?
3. Is Robert Lewandowski a ’killer’ striker?

and visualise your findings.

## Prerequisites

1. Install Python3 (at least 3.6) directly from its website [https://www.python.org/downloads/](url)
or via anaconda [https://www.anaconda.com/](url)
2. Make sure package manager 'pip' is up-to-date
   
   ```
   python -m pip install --upgrade pip
   ```

3. Install the following external python pachakges using 'pip'
   
   ```
   pip install beautifulsoup4
   pip install requests
   pip install tqdm
   pip install mplsoccer

   ```
## Getting Started

Use the following input file to run the code. 

```
import myfootballanalytics as mfa

update_id_file = True   ## Updates file containing match ids from https://understat.com/
get_data =       False   ## Scrapes data from https://understat.com/ and saves them in the defined directory
analyze_match =  False   ## Plots the position of all shots of a given match and provides a table with information
analyze_league = False   ## Plots xG figure for the teams of the selected league over the selected seasons
analyze_team =   False   ## Plots xG figure for the selected team over the selected seasons

## Relevant if get_data = True
save_csv_file_leagues = True   ## Saves league’s data to csv file

## Relevant if analyze_league = True
save_csv_file_players = True   ## Saves players’ data to csv file

## Relevant if update_id_file = True
parallel = True    ## Activates multiprocessing for faster results.

## Relavant for all tags
save_dir_path = ""  ## Saving directory. Default: current working directory. Empty string activates the default setting. 

## Relevant if get_data = True
leagues = ['PremierLeague','Ligue1','Bundesliga','LaLiga','SerieA']   ## Available leagues: Ligue1, PremierLeague, Bundesliga, LaLiga, SerieA

## Relevant if get_data = True or analyze_league = True or analyze_team = True
seasons = ['2014-2015','2015-2016','2016-2017','2017-2018','2018-2019','2019-2020','2020-2021','2021-2022','2022-2023']

## Relevant if analyze_match = True
home_team = "FC Cologne"  ## Available teams: all teams
away_team = "Bayern Munich"  ## Available teams: all teams
season = "2022-2023"   ## Available season: all seasons

## Relevant if analyze_league = True
league = "Bundesliga"   ## Choose league to analyze. Available leagues: Ligue1, PremierLeague, Bundesliga, LaLiga, SerieA

## Relavant if analyze_team = True
team = "Arsenal"       ## Available teams: all teams

if update_id_file:
    ids = mfa.FindIDs(parallel,save_dir_path)

if get_data:
    data = mfa.DataUpdater(leagues,seasons,save_dir_path,save_csv_file_leagues)
    
if analyze_match:
    md = mfa.MatchDataLoader(home_team,away_team,season,save_dir_path)
    match_data = md.load_match_data()
    
    match = mfa.MatchAnalyzer(match_data)
    table = match.analyze_match()
    print(table)
    
if analyze_league:
    league_data = mfa.LeagueAnalyzer(league,seasons,save_dir_path,save_csv_file_players)
    
if analyze_team:
    td = mfa.TeamDataLoader(seasons,team,save_dir_path)
    team_data = td.load_team_data()
    
    team_analysis = mfa.TeamAnalyzer(team_data,seasons,team)
    team_analysis.analyze_team()
```