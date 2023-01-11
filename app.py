import streamlit as st
import pandas as pd 
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from helper import GetChaseGraph , GetInningDataFrame,GetMatchDataFrame,\
                    GetScoreCard,GetWicketDf,getOverwiseScore,dataLoaderandPreprocessor,GetHeatMap , GetMatchListBySeason,\
                        GetSeasonList , GetSeasonWiseDetailData , GetSeasonWiseMatchOverwiew ,GetMatchIdFromName,GetMatchResult,\
                            GetPlayerOfMatchTag , GetMatchTossResults,GetBattingSummary,GetBowlingSummary,GetInningScoreTag ,GetWinnerTeam,\
                                GetOrangeCapWinner , GetNumof_FiftiesCenturies , GetSixesAndFoursPerSeason , GetTotalWickets , GetPurpleCapWinner,\
                                GetNumOFvenues,GetNumofTeams , OverallBattingRecSeason,GetHighesScores,GetMost50plus,GetMostFours,GetMostSixes,BestStrikeRates,\
                                    GetSixesInningCard,GetBoundriesInningCards,GetSeasonBowlingRec ,GetMostDotsCard,GetMostEcoCard,GetOverallBatterlist,GetVenueList,\
                                        GetBowlerListforBatter ,GetFallsAgainst,GetComfortBowlers,GetPerBatsmanOverview,GetPertBatsmanOverallGraph,GetStrugglerBowlers,\
                                            BattervsBowlerDetail ,GetVenueListBySeason ,BatterListbySeasonandVenue
                                            

dcount = 0  # generate initialiser for seperate keys in tabs
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)                                   

MatchOverViewDataPath =r"datasets\Updated_Matches.csv"
BallAnalysisDataPath = r"datsets\Updated_Ipl_Ball_By_Ball3.csv"

#Creates the two dataframses from the csv files 

MatchOverviewdF , BallAnalysisdf = dataLoaderandPreprocessor()

st.sidebar.image(r"TeamLogo\iplognew.png")
st.sidebar.title("IPL Data Analysis")


#Creates a selection list for level of analysis

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overview','MatchWiseAnalysis','SeasonWiseAnalysis',"PlayerWiseAnalysis","Batsman Vs Batsman")
)



if user_menu == "Overview":
    text = """
                                                Welcome to IPL Analysis Site.

IPL is the most famous cricket T20 tournament hosted by BBCI.
This site presents the data of last 12 IPL seasons in visual informatics.
This is a beta site . More tools to be added soon.
Thank you 
    """
    st.image(r"TeamLogo\newlog.jpg")
    st.code(text , language = None)

if user_menu == 'MatchWiseAnalysis':
    season = st.sidebar.selectbox(
        "Select Season",
        GetSeasonList()
    )
    if season != "Select Season" :
        match = st.sidebar.selectbox(
            "Select Match",
            GetMatchListBySeason(season)
        )
        col1 , col2 ,col3  = st.columns(3)
        with col1:
            st.subheader(match)
        with col2:
            st.subheader("Season " + season)
        id = GetMatchIdFromName(season , match)
        tab1, tab2 ,tab3 , tab4 , tab5 = st.tabs(["OverView","ScoreCard","RunChase","Overwise Score","Indvidual Battles"])

        with tab1:
            st.code(GetMatchTossResults(id),language=None)
            with st.container():
                col1 ,col2 = st.columns(2)
                with col1 :
                    st.table(GetBattingSummary(id ,1))
                with col2 :
                    st.table(GetBowlingSummary(id ,1))
            with st.container():
                st.code(GetInningScoreTag(id ,1),language=None)
            with st.container():
                col1 ,col2 = st.columns(2)
                with col1 :
                    st.table(GetBattingSummary(id ,2))
                with col2 :
                    st.table(GetBowlingSummary(id ,2))
            with st.container():
                st.code(GetInningScoreTag(id ,2),language=None)
            
            with st.container():
                st.code(GetMatchResult(id))

        with tab2:
            BatFirstTeam = GetInningDataFrame(id,1)["BattingTeam"].unique()[0]
            BatSecondTeam = GetInningDataFrame(id,2)["BattingTeam"].unique()[0]
            tab1, tab2 = st.tabs([BatFirstTeam,BatSecondTeam])
            with tab1:
                st.table(GetScoreCard(id,1))
                st.code(GetInningScoreTag(id ,1),language=None)
            with tab2:
                st.table(GetScoreCard(id,2))
                st.code(GetInningScoreTag(id ,2),language=None)

        with tab3:
            with st.container():
                st.plotly_chart(GetChaseGraph(id))
        
        with tab4:
            with st.container():
                st.plotly_chart(getOverwiseScore(id))

        with tab5:
            with st.container():
                col1 , col2 = st.columns(2)
                with col1:
                    st.pyplot(GetHeatMap(id,1))
                with col2:
                    st.pyplot(GetHeatMap(id,2))
            

if user_menu == "SeasonWiseAnalysis":

    season = st.sidebar.selectbox(
        "Select Season",
        GetSeasonList()
    )
    if season!= "Select Season" :
        Overview,Batting,Bowling = st.tabs(["Overview","Batting","Bowling"])
        with Overview:
            with st.container():
                col1 , col2 , col3,cl4,col5= st.columns(5)
                with col3:
                    WinnerTeam = "##### {}".format(GetWinnerTeam(season))
                    WinnerTag = "###  Winner"
                    st.markdown(WinnerTag ,unsafe_allow_html=False)
                    st.markdown(WinnerTeam)
            st.caption("________")
            with st.container():
                col1 , col2 , col3 ,col4 ,col5 = st.columns(5)
                with col2:
                    Teams = GetNumofTeams(season)
                    tag = "### Teams"
                    winnertag = "##### {}".format(Teams)
                    st.markdown(tag)
                    st.markdown(winnertag)
                with col3:
                    Venue = GetNumOFvenues(season)
                    tag = "### Venues"
                    winnertag = "##### {}".format(Venue)
                    st.markdown(tag)
                    st.markdown(winnertag)
                with col4:
                    tag = "### Season"
                    winnertag = "##### {}".format(season)
                    st.markdown(tag)
                    st.markdown(winnertag)

            st.caption("________")
            with st.container():
                col1 , col2 , col3 ,col4,col5 = st.columns(5) 
                with col2:
                    winner =  GetOrangeCapWinner(season)
                    tag = "### Orange Cap"
                    winnertag = "##### {} ({})".format(winner["batter"] , winner["batsman_run"])
                    st.markdown(tag)
                    st.markdown(winnertag)
                with col3:
                    winner =  GetPurpleCapWinner(season)
                    tag = "### Purple Cap"
                    winnertag = "##### {} ({})".format(winner["bowler"] , winner["isBowlerWicket"])
                    st.markdown(tag)
                    st.markdown(winnertag)
                with col4:
                    wickets = GetTotalWickets(season)
                    tag = "### Wickets"
                    winnertag = "##### {}".format(wickets)
                    st.markdown(tag)
                    st.markdown(winnertag) 
                
            st.caption("________")
            with st.container():
                col1 , col2 , col3,col4 ,col5 ,col6= st.columns(6)
                Fifty , Century = GetNumof_FiftiesCenturies(season)   
                with col2:
                    tag = "### Fifty"
                    winnertag = "##### {}".format(Fifty)
                    st.markdown(tag)
                    st.markdown(winnertag)
                with col3:
                    tag = "### Century"
                    winnertag = "##### {}".format(Century)
                    st.markdown(tag)
                    st.markdown(winnertag)
                
                Fours , Sixes = GetSixesAndFoursPerSeason(season) 
                with col4:
                    tag = "### Fours"
                    winnertag = "##### {}".format(Fours)
                    st.markdown(tag)
                    st.markdown(winnertag)
                with col5:
                    tag = "### Sixes"
                    winnertag = "##### {}".format(Sixes)
                    st.markdown(tag)
                    st.markdown(winnertag)
            st.caption("________")


        
        with Batting:
            MostRun ,Most50, HighestScore , MostFours , MostSixes , MOstSixIni , MostBounIn , BestSr = \
                                        st.tabs(["Most Runs","Most 50+","Highest Score",\
                                            "Most Fours","Most Sixes","Most Sixes(Innings)","Most Boundries(Innings)","Best SR(min 100 balls)"]) 

            with MostRun:
                with st.container():
                    st.table(OverallBattingRecSeason(season).iloc[0:20])       
            
            with Most50:
                with st.container():
                    st.table(GetMost50plus(season).iloc[0:15])

            with HighestScore :
                with st.container():
                    st.table(GetHighesScores(season).iloc[0:15])
            
            with MostFours:
                with st.container():
                    st.table(GetMostFours(season).iloc[0:15])
            
            with MostSixes:
                with st.container():
                    st.table(GetMostSixes(season).iloc[0:15])

            with MOstSixIni:
                with st.container():
                    st.table(GetSixesInningCard(season).iloc[0:15])

            with MostBounIn:
                with st.container():
                    st.table(GetBoundriesInningCards(season))
            with BestSr:
                with st.container():
                    st.table(BestStrikeRates(season).iloc[0:15])


        with Bowling:
            MostWickets, BestEconomy,MostDots = st.tabs(["Most Wickets","Best Economy","Most Dots"])
            with MostWickets:
                with st.container():
                    st.table(GetSeasonBowlingRec(season).iloc[0:10])
            
            with BestEconomy:
                with st.container():
                    st.table(GetMostEcoCard(season).iloc[0:10])
            
            with MostDots:
                with st.container():
                    st.table(GetMostDotsCard(season).iloc[0:10])


if user_menu == "PlayerWiseAnalysis":
    
    batter = st.sidebar.selectbox(
                "Select Batter",
                GetOverallBatterlist()
            )
    
    season = st.sidebar.selectbox(
        "Select Season",
        GetSeasonList(1 , batter)
    )
    if season != "Select Season":
        if season =="Overall":
            Venue = st.sidebar.selectbox(
                "Select Venue",
                GetVenueList(batter)
            )
            if Venue != "Select Venue":
                if Venue == "Overall":
                    bowler = st.sidebar.selectbox(
                        "Select Bowler",
                        GetBowlerListforBatter(batter ,checker=1,season=season , venue = Venue)
                    )
                    if bowler != "Select Bowler":
                        if bowler == "Overall":
                            Overview ,Batting_Averages,Struggles_Against,Score_Against,Falls_Against= \
                                    st.tabs(["Overview","Batting Averages","Struggles Against","Score Against","Falls Against"])
                            with Overview:
                                runtab , fig = GetPerBatsmanOverview(batter)
                                with st.container():
                                    col3, col4 = st.columns(2)
                                    with col3:
                                        st.table(runtab)
                                    with col4:
                                        st.plotly_chart(fig,use_container_width=True, theme = None)

                            with Batting_Averages:
                                with st.container():
                                    st.plotly_chart(GetPertBatsmanOverallGraph(batter) \
                                                    ,use_container_width=True, theme = None)

                            with Struggles_Against:
                                min_balls = 25 
                                Struggledf1 , Bowler_List1 =  GetStrugglerBowlers(batter , min_balls=min_balls)
                                with st.container():
                                    if Struggledf1.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Struggledf1)
                                        with st.expander("See Further Bowler Details "):
                                            bowler1 = st.selectbox("Select Bowler",
                                                                Bowler_List1 ,key=dcount
                                                                    )
                                            dcount+=1
                                            if bowler1 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter , bowler1 , season=season , venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                            with Score_Against:
                                min_balls = 25
                                Scoredf1, Bowler_List2 =  GetComfortBowlers(batter = batter ,season=season,venue = Venue,bowler = bowler , min_balls=min_balls)
                                with st.container():
                                    if Scoredf1.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwers who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Scoredf1)
                                        with st.expander("See Further Bowler Details "):
                                            bowler2 = st.selectbox("Select Bowler",
                                                                Bowler_List2 ,key = dcount
                                                                )
                                            dcount+=1
                                            if bowler2 !="Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter , bowler2 , season=season , venue = Venue )
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)
                            
                            with Falls_Against:

                                Falldf1 , Bowler_List3 =  GetFallsAgainst(batter = batter )
                                with st.container():
                                    st.table(Falldf1)
                                with st.expander("See Further Bowler Details "):
                                    bowler3 = st.selectbox("Select Bowler",
                                                        Bowler_List3,
                                                        key = dcount
                                                        )
                                    dcount+=1
                                    if bowler3 != "Select Bowler":
                                        Details , perc_pie =  BattervsBowlerDetail(batter , bowler3 , season=season , venue = Venue)
                                        with st.container():
                                            st.table(Details)
                                        with st.container():
                                            st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                        if bowler != "Overall":
                            runtab , fig = GetPerBatsmanOverview(batter , season =season,venue=Venue , bowler = bowler)
                            with st.container():
                                col1 , col2 = st.columns(2)
                                with col1:
                                    st.table(runtab)
                                with col2:
                                    st.plotly_chart(fig , theme=None )
                
                if Venue != "Overall":
                    
                    bowler = st.sidebar.selectbox(
                        "Select Bowler",
                        GetBowlerListforBatter(batter ,checker=1,season=season , venue = Venue)
                    )
                    if bowler !="Select Bowler":
                        if bowler == "Overall":
                            Overview ,Struggles_Against,Score_Against,Falls_Against= \
                                        st.tabs(["Overview","Struggles Against","Score Against","Falls Against"])
                            with Overview :
                                runtab ,fig =  GetPerBatsmanOverview(batter,season=season , venue = Venue , bowler = bowler)
                                with st.container():
                                    col3, col4 = st.columns(2)
                                    with col3:
                                        st.table(runtab)
                                    with col4:
                                        st.plotly_chart(fig,use_container_width=True, theme = None)
                            
                            with Struggles_Against:
                                min_balls = 15
                                Struggledf2 , Bowler_List4 =  GetStrugglerBowlers(batter = batter ,season = season ,venue = Venue,bowler = bowler ,min_balls=15)
                                with st.container():
                                    if Struggledf2.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Struggledf2)
                                        with st.expander("See Further Bowler Details "):
                                            bowler4 = st.selectbox("Select Bowler",
                                                                Bowler_List4 ,key=dcount
                                                                    )
                                            dcount+=1
                                            if bowler4 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter , bowler4 , season=season , venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                            with Score_Against:
                                min_balls = 15
                                Scoredf2, Bowler_List5 =  GetComfortBowlers(batter = batter ,season = season ,venue = Venue,bowler = bowler ,min_balls=15)
                                with st.container():
                                    if Scoredf2.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Scoredf2)
                                        with st.expander("See Further Bowler Details "):
                                            bowler5 = st.selectbox("Select Bowler",
                                                                Bowler_List5 ,key = dcount
                                                                    )
                                            dcount+=1
                                            if bowler5 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter , bowler5 , season=season , venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)
                            
                            with Falls_Against:

                                Falldf2 , Bowler_List6 =  GetFallsAgainst(batter = batter ,season = season ,venue = Venue,bowler = bowler)
                                with st.container():
                                    st.table(Falldf2)
                                with st.expander("See Further Bowler Details "):
                                    bowler6 = st.selectbox("Select Bowler",
                                                        Bowler_List6,
                                                        key = dcount
                                                        )
                                    dcount+=1
                                    if bowler6 != "Select Bowler":
                                        Details , perc_pie =  BattervsBowlerDetail(batter , bowler6 , season=season , venue = Venue)
                                        with st.container():
                                            st.table(Details)
                                        with st.container():
                                            st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                        if bowler != "Overall":
                            runtab , fig = GetPerBatsmanOverview(batter , season =season,venue=Venue, bowler = bowler )
                            with st.container():
                                col1 , col2 = st.columns(2)
                                with col1:
                                    st.table(runtab)
                                with col2:
                                    st.plotly_chart(fig , theme=None )




        if season !="Overall":

            Venue = st.sidebar.selectbox(
                "Select Venue",
                GetVenueList(batter ,season = season)
            )
            if Venue !="Select Venue":
                if Venue == "Overall":
                    bowler = st.sidebar.selectbox(
                        "Select Bowler",
                        GetBowlerListforBatter(batter ,checker=1,season=season , venue = Venue)
                    )
                    if bowler != "Select Bowler":
                        if bowler == "Overall":
                            Overview4 ,Struggles_Against4,Score_Against4,Falls_Against4 = \
                                    st.tabs(["Overview","Struggles Against","Score Against","Falls Against"])
                            with Overview4:
                                runtab , fig = GetPerBatsmanOverview(batter = batter ,season = season ,venue = Venue,bowler = bowler)
                                with st.container():
                                    col1 , col2 = st.columns(2)
                                    with col1:
                                        st.table(runtab)
                                    with col2:
                                        st.plotly_chart(fig,use_container_width=True, theme = None)

                            with Struggles_Against4:
                                min_balls = 15
                                Struggledf3 , Bowler_List7 =  GetStrugglerBowlers(batter = batter ,season = season ,venue = Venue,bowler = bowler , min_balls=min_balls)
                                with st.container():
                                    if Struggledf3.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Struggledf3)
                                        with st.expander("See Further Bowler Details "):
                                            bowler7 = st.selectbox("Select Bowler",
                                                                Bowler_List7 ,key=dcount
                                                                    )
                                            dcount+=1
                                            if bowler7 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter, bowler7 ,season = season ,venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                            with Score_Against4:
                                min_balls = 15
                                Scoredf3, Bowler_List8 =  GetComfortBowlers(batter = batter ,season = season ,venue = Venue,bowler = bowler , min_balls=15)
                                with st.container():
                                    if Scoredf3.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Scoredf3)
                                        with st.expander("See Further Bowler Details "):
                                            bowler8 = st.selectbox("Select Bowler",
                                                                Bowler_List8 ,key = dcount
                                                                )
                                            dcount+=1
                                            if bowler8 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter ,bowler8 ,season = season ,venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)
                            
                            with Falls_Against4:
                                print(batter , season , Venue , bowler)
                                Falldf3 , Bowler_List9 =  GetFallsAgainst(batter = batter ,season = season ,venue = Venue,bowler = bowler)
                                with st.container():
                                    st.table(Falldf3)
                                with st.expander("See Further Bowler Details "):
                                    bowler9 = st.selectbox("Select Bowler",
                                                        Bowler_List9,
                                                        key = dcount
                                                        )
                                    dcount+=1
                                    if bowler9 != "Select Bowler":
                                        Details , perc_pie =  BattervsBowlerDetail(batter , bowler9 , season=season , venue = Venue)
                                        with st.container():
                                            st.table(Details)
                                        with st.container():
                                            st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                        if bowler != "Overall":
                            runtab , fig = GetPerBatsmanOverview(batter , season =season,venue=Venue , bowler = bowler)
                            with st.container():
                                col1 , col2 = st.columns(2)
                                with col1:
                                    st.table(runtab)
                                with col2:
                                    st.plotly_chart(fig , theme=None )
                    
                    
                if Venue != "Overall":
                    
                    bowler = st.sidebar.selectbox(
                        "Select Bowler",
                        GetBowlerListforBatter(batter ,checker=1,season=season , venue = Venue)
                    )
                    if bowler != "Select Bowler":
                        if bowler == "Overall":
                            Overview ,Struggles_Against,Score_Against,Falls_Against= \
                                    st.tabs(["Overview","Struggles Against","Score Against","Falls Against"])
                            with Overview :
                                runtab , fig = GetPerBatsmanOverview(batter = batter ,season = season ,venue = Venue,bowler = bowler)
                                with st.container():
                                    col3, col4 = st.columns(2)
                                    with col3:
                                        st.table(runtab)
                                    with col4:
                                        st.plotly_chart(fig,use_container_width=True, theme = None)
                            
                            with Struggles_Against:
                                min_balls = 15
                                Struggledf4 , Bowler_List10 =  GetStrugglerBowlers(batter = batter ,season = season ,venue = Venue,bowler = bowler ,min_balls=15)
                                with st.container():
                                    if Struggledf4.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} balls to batsman .".format(min_balls) , language = None)
                                        st.table(Struggledf4)
                                        with st.expander("See Further Bowler Details "):
                                            bowler10 = st.selectbox("Select Bowler",
                                                                Bowler_List10 ,key=dcount
                                                                    )
                                            dcount+=1
                                            if bowler10 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter , bowler10 , season=season , venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)

                            with Score_Against:
                                min_balls = 15
                                Scoredf4, Bowler_List11 =  GetComfortBowlers(batter = batter ,season = season ,venue = Venue,bowler = bowler ,min_balls=15)
                                with st.container():
                                    if Scoredf4.shape[0] == 0:
                                        st.code("The Batsman must have faced at least {} balls in perticular category . Try reducing the filters".format(min_balls) , language = None)
                                    else:
                                        st.code("This list shows the bolwer who has bowl at least {} ball to batsman .".format(min_balls) , language = None)
                                        st.table(Scoredf4)
                                        with st.expander("See Further Bowler Details "):
                                            bowler11 = st.selectbox("Select Bowler",
                                                                Bowler_List11 ,key = dcount
                                                                    )
                                            dcount+=1
                                            if bowler11 != "Select Bowler":
                                                Details , perc_pie =  BattervsBowlerDetail(batter , bowler11 , season=season , venue = Venue)
                                                with st.container():
                                                    st.table(Details)
                                                with st.container():
                                                    st.plotly_chart(perc_pie , use_container_width=True , theme = None)
                            
                            with Falls_Against:

                                Falldf4 , Bowler_List12 =  GetFallsAgainst(batter = batter ,season = season ,venue = Venue,bowler = bowler)
                                with st.container():
                                    st.table(Falldf4)
                                with st.expander("See Further Bowler Details "):
                                    bowler12 = st.selectbox("Select Bowler",
                                                        Bowler_List12,
                                                        key = dcount
                                                        )
                                    dcount+=1
                                    if bowler12 != "Select Bowler":
                                        Details , perc_pie =  BattervsBowlerDetail(batter , bowler12 , season=season , venue = Venue)
                                        with st.container():
                                            st.table(Details)
                                        with st.container():
                                            st.plotly_chart(perc_pie , use_container_width=True , theme = None)
                        
                        if bowler != "Overall":
                            runtab , fig = GetPerBatsmanOverview(batter , season =season,venue=Venue , bowler = bowler)
                            with st.container():
                                col1 , col2 = st.columns(2)
                                with col1:
                                    st.table(runtab)
                                with col2:
                                    st.plotly_chart(fig , theme=None )

                        
if user_menu == "Batsman Vs Batsman":
    season = st.sidebar.selectbox(
                            "Select Season",
                            GetSeasonList(checker=1)
                        )
    if season != "Select Season":
        Venue = st.sidebar.selectbox(
            "Select Venue",
            GetVenueListBySeason(season= season)
        )
        if Venue != "Select Venue":
            batter1 = st.sidebar.selectbox(
                "Select Batsman 1",
                BatterListbySeasonandVenue(season = season , venue = Venue)
            )
            batter2 = st.sidebar.selectbox(
                "Select Batsman 2",
                BatterListbySeasonandVenue(season = season , venue = Venue)
            )
            
            if (batter1 != "Select Batter") & (batter2 != "Select Batter"):
                Overview , BallsFaced , Batting_Averages = st.tabs(["Overview" ,"How Faced ?","Batting Averages"])
                runtab1 , fig1 = GetPerBatsmanOverview(batter1,season=season , venue = Venue , bowler = "Overall")
                runtab2 , fig2 = GetPerBatsmanOverview(batter2,season=season , venue = Venue , bowler = "Overall")
                with Overview:
                    with st.container():
                        col1 , col2  = st.columns(2)
                        with col1 :
                            st.code(batter1 , language=None)
                            st.table(runtab1)
                        with col2 :
                            st.code(batter2 , language = None)
                            st.table(runtab2)
                
                with BallsFaced :
                    with st.container():
                        col3 , col4  = st.columns(2)
                        with col3 :
                            st.code(batter1 , language=None)
                            fig1.update_layout(title = "")
                            st.plotly_chart(fig1)
                        with col4 :
                            st.code(batter2 , language = None)
                            fig2.update_layout(title = "")
                            st.plotly_chart(fig2)

                








    


    
    

      
     
                
