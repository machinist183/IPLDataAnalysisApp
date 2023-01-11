
# IPL Data Analysis App
   [main GitHub repo](https://github.com/machinist183/IPLDataAnalysisApp).

   [Application Link](http://172.105.41.201:8501/)
#### -- Project Status: [Active]
          
## Project Intro/Objective
This project is made for analysing the last 12 season of IPL ball by ball dataset containing 225k rows . It has various levels of comparing players based on match , season , venue and bowlers. The project can be usefull getting insights about the players based on season and venue which can be helpfull in selection of fantasy teams . 

### Methods Used
* Data Cleaning and Data Preprocessing
* Inferential Statistics
* Data Grouoing and Aggregation
* Data Visualization
* Cloud Deployment

### Technologies
* Python
* Plotly , Seaborn , Matplotlib
* Pandas, jupyter
* Streamlit
* Linux

## Dataset Description

This project contains three datasets.

1. BallByBall dataset (https://github.com/machinist183/IPLDataAnalysisApp/blob/main/src/datasets/Updated_Ipl_Ball_By_Ball3.csv).
2. MatchSummary dataset(https://github.com/machinist183/IPLDataAnalysisApp/blob/main/src/datasets/Updated_Matches.csv)
3. TeamLData (https://github.com/machinist183/IPLDataAnalysisApp/blob/main/src/datasets/TeamData.csv)

1.BallByBall dataset

    This dataset contains 225954 rows containing the result of each bowl bowled in IPL since it beginning.
    The dataset contains 22 columns as below. The columns are self explainatory :
       ID,innings,overs,ballnumber,batter,bowler,non-striker, extra_type, batsman_run,extras_run, total_run,non_boundary,isWicketDelivery, player_out,kind,
       fielders_involved, BattingTeam, islegal, Season,isBowlerWicket, Date, Venue
2.Match Summary dataset 
   
      This dataset contains the oveview of each match . Its has 950 rows.Each row represents the one match .
      The dataset contains 25 columns and the columns are self explainatory.
         
3.Team Details 

    This dataset contains 12 rows and three columns .Each row represent team.


## Getting Started

1.Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).    
2.Create a virtual python enviornment 
3.Install dependencies using requirement.txt file 

       pip install -r requirement.txt

4.Run application using streamlit.
      
       streamlit  run app.py



