import pandas as pd
import plotly.express as ex
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt
import re


MatchOverViewDataPath =r"datasets\Updated_Matches.csv"
BallAnalysisDataPath = r"datasets\Updated_Ipl_Ball_By_Ball3.csv"
TeamData = pd.read_csv(r"datasets\TeamData.csv")



def dataLoaderandPreprocessor(MatchPath = MatchOverViewDataPath , BallPath = BallAnalysisDataPath):
    #Func for loading and preprocessing the dataset
    MatchOverviewdF= pd.read_csv(MatchPath)
    BallAnalysisdf = pd.read_csv(BallPath)
    bbd_change_dt = BallAnalysisdf.drop(columns=["ID"])
    BallAnalysisdf[bbd_change_dt.dtypes[bbd_change_dt.dtypes == 'int64'].index]=\
                            BallAnalysisdf[bbd_change_dt.dtypes[bbd_change_dt.dtypes == 'int64'].index].astype(np.int16)
    BallAnalysisdf["islegal"] = BallAnalysisdf['extra_type'].apply(lambda x : 1 if x in [np.NAN, 'legbyes', 'byes'] else 0)
    BallAnalysisdf["Season"] =  BallAnalysisdf["Season"].astype(str)
   
    BallAnalysisdf = BallAnalysisdf.merge(MatchOverviewdF[["ID","Date","Venue"]] ,on= "ID",how= 'left')
    BallAnalysisdf["Date"] = pd.to_datetime(BallAnalysisdf["Date"])
    MatchOverviewdF["Season"]=MatchOverviewdF["Season"].str.replace("2020/21","2020")
    MatchOverviewdF["Season"]=MatchOverviewdF["Season"].str.replace("2009/10","2010")
    MatchOverviewdF["Season"]=MatchOverviewdF["Season"].str.replace("2007/08","2008")
    BallAnalysisdf["Season"]=BallAnalysisdf["Season"].str.replace("2020/21","2020")
    BallAnalysisdf["Season"]=BallAnalysisdf["Season"].str.replace("2009/10","2010")
    BallAnalysisdf["Season"]=BallAnalysisdf["Season"].str.replace("2007/08","2008")
    BallAnalysisdf["Venue"] = BallAnalysisdf["Venue"].apply(lambda x : x.split(',')[0])

    return MatchOverviewdF , BallAnalysisdf 

MatchOverviewdF , BallAnalysisdf = dataLoaderandPreprocessor()

def GetTeamJeseyColor(Name):
    #Gets team colour from TeamData
    Team_Data = pd.read_csv(r"datasets\TeamData.csv")
    color = Team_Data[Team_Data["Name"] == Name][["Logo","Color"]].values[0][1]
    return color

def GetTeamName(matchid , inning_no):
    #Gets team name according to argumnets passed
    filt = (BallAnalysisdf["ID"] == matchid) & (BallAnalysisdf["innings"] == inning_no )
    Name = BallAnalysisdf[filt]["BattingTeam"].values[0]
    return Name

def GetMatchDataFrame(matchid):
    #Gets Matchwise dataframe
    Matchdf = BallAnalysisdf.groupby("ID").get_group(matchid)
    return Matchdf

def GetInningDataFrame(matchid ,inning_no):
    InningDf = GetMatchDataFrame(matchid=matchid).groupby('innings').get_group(inning_no)
    return InningDf

def GetWicketDf(InningDf):
    WicketDF = InningDf.groupby("isWicketDelivery").get_group(1)[["bowler","batter","kind","fielders_involved"]]
    return WicketDF

def GetVenueList(batter,season ="Overall"):
    Batterdf = BallAnalysisdf.groupby("batter").get_group(batter)
    if season != "Overall":
        Batterdf = Batterdf.groupby("Season").get_group(season)
    VenueList = Batterdf["Venue"].unique().tolist()
    VenueList.insert(0 ,"Select Venue")
    VenueList.insert(1 , "Overall")
    return VenueList

def GetVenueListBySeason(season ="Overall"):
    Batterdf = BallAnalysisdf
    if season == "Overall":
        Batterdf = Batterdf
    if season != "Overall":
        Batterdf = Batterdf.groupby("Season").get_group(season)
    VenueList = Batterdf["Venue"].unique().tolist()
    VenueList.insert(0 ,"Select Venue")
    VenueList.insert(1 , "Overall")
    return VenueList

def GetBowlerListforBatter(batter , checker = 0 , season = "Overall", venue = "Overall"):
    batterdf = BallAnalysisdf.groupby("batter").get_group(batter)
    if season == "Overall":
        if venue == "Overall":
            if checker == 0:
                bowler_list = batterdf["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                return bowler_list
            if checker ==1:
                bowler_list = batterdf["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                bowler_list.insert(1,"Overall")
                return bowler_list
        if venue != "Overall":
            if checker ==0:
                bowler_list = batterdf.groupby("Venue").get_group(venue)["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                return bowler_list
            if checker ==1:
                bowler_list = batterdf.groupby("Venue").get_group(venue)["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                bowler_list.insert(1,"Overall")
                return bowler_list

    if season != "Overall":
        batterdf = batterdf.groupby("Season").get_group(season)
        if venue == "Overall":
            if checker == 0:
                bowler_list = batterdf["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                return bowler_list
            if checker == 1:
                bowler_list = batterdf["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                bowler_list.insert(1,"Overall")
                return bowler_list
        if venue != "Overall":
            if checker == 0:
                bowler_list = batterdf.groupby("Venue").get_group(venue)["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                return bowler_list
            if checker ==1:
                bowler_list = batterdf.groupby("Venue").get_group(venue)["bowler"].unique().tolist()
                bowler_list.insert(0,"Select Bowler")
                bowler_list.insert(1,"Overall")
                return bowler_list

    



def GetOverallBatterlist():
    batter_list = BallAnalysisdf["batter"].unique().tolist()
    return batter_list

def GetScoreCard(matchid , inning_no):
    Inning_df = GetInningDataFrame(matchid , inning_no)
    Scores_Df = Inning_df.groupby("batter",sort =False)\
                        .sum(numeric_only = True)[["batsman_run","islegal"]]
    Scores_Df.rename(columns ={"islegal":"Balls Faced"} , inplace = True)
    WicketDf = GetWicketDf(Inning_df)
    ScoreCard_df = Scores_Df.merge(WicketDf , on = "batter" , how = "left")
    ScoreCard_df["fielders_involved"].fillna("" , inplace = True)
    Not_Out_index = ScoreCard_df[ScoreCard_df['kind'].isna()].index
    ScoreCard_df.loc[Not_Out_index , ['bowler','kind']] = ["",'Not Out']
    ScoreCard_df.rename(columns = {"batter":"Batman" ,"batsman_run":"Runs", "Balls Faced":"Balls" , \
                        "kind":"Wicket Type" , "bowler":"Bowler","fielders_involved":"Fielder Involved"} , inplace = True)
    ScoreCard_df = ScoreCard_df[["Batman" ,"Runs","Balls" ,"Wicket Type","Bowler","Fielder Involved"]]

    return ScoreCard_df

def GetChaseGraph(matchid):
    fig = go.Figure()
    Innings1 = GetInningDataFrame(matchid=matchid,inning_no=1).reset_index()
    Innings2 = GetInningDataFrame(matchid=matchid,inning_no=2).reset_index()
    Innings1["LiveScore"] = Innings1.total_run.cumsum()
    Innings2["LiveScore"] = Innings2.total_run.cumsum()
    BatFirstName = GetTeamName(matchid , 1)
    BatSecondName = GetTeamName(matchid , 2)

    trace = go.Scatter(
        x=(Innings1.index+1)/6, y=Innings1.LiveScore,
        mode="lines+markers",
        name = BatFirstName,
        marker_size = Innings1.isWicketDelivery * 10,
        line_color = GetTeamJeseyColor(BatFirstName),
        marker_color = 'white',
        
    )
    trace2 = go.Scatter(
        x=(Innings2.index+1)/6,
        y=Innings2.LiveScore,
        mode="lines+markers",
        name = BatSecondName,
        marker_size = Innings2.isWicketDelivery * 10,
        line_color = GetTeamJeseyColor(BatSecondName),
        marker_color = 'white'
    )


    data = [trace,trace2]
    layout = go.Layout(
                    xaxis_title='Overs',
                    yaxis_title='Runs Scored',
                    width=1000,
                    height=600

    )
    fig = go.Figure(data=data, layout=layout)
    return fig

def getOverwiseScore(matchid):
    fig = go.Figure()
    Innings1 = GetInningDataFrame(matchid=matchid,inning_no=1).groupby("overs").sum()["total_run"]
    Innings2 = GetInningDataFrame(matchid=matchid,inning_no=2).groupby("overs").sum()["total_run"]
    BatFirstName = GetTeamName(matchid , 1)
    BatSecondName = GetTeamName(matchid , 2)
    fig.add_trace(go.Bar(x=Innings1.index + 1 ,
                    y= Innings1.values,
                    name = BatFirstName,
                    marker_color=GetTeamJeseyColor(BatFirstName)
                    ))
    fig.add_trace(go.Bar(x=Innings2.index + 1 ,
                    y= Innings2.values,
                    name = BatSecondName,
                    marker_color=GetTeamJeseyColor(BatSecondName)
                    ))

    fig.update_layout(
        xaxis_tickfont_size=14,
        width = 1000,
        height = 600,
        yaxis=dict(
            title='Runs',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.5, # gap between bars of adjacent location coordinates.
        bargroupgap=0.0 # gap between bars of the same location coordinate.
    )
    return fig

def GetHeatMap(matchid , inning_no):
    fig,ax = plt.subplots(figsize=(5,5))
    Innings = GetInningDataFrame(matchid=matchid , inning_no=inning_no)
    pivot  = Innings.pivot_table(columns = 'bowler', index = 'batter' ,values= 'batsman_run',aggfunc=np.sum)
    ax = sns.heatmap(pivot,cmap='Reds')
    return fig

def GetSeasonList(checker =  0 , batter = None):
    if batter == None:
        Season_list = BallAnalysisdf["Season"].unique().tolist()
        if checker ==0:
            Season_list.insert(0 , "Select Season")
            return Season_list
        if checker ==1 :
            Season_list.insert(0,"Select Season")
            Season_list.insert(1,"Overall")
            return Season_list
    if batter != None:
        Season_list = BallAnalysisdf.groupby("batter").get_group(batter)["Season"].unique().tolist()
        if checker ==0:
            Season_list.insert(0 , "Select Season")
            return Season_list
        if checker ==1 :
            Season_list.insert(0,"Select Season")
            Season_list.insert(1,"Overall")
            return Season_list

def GetSeasonWiseMatchOverwiew(Season):
    SeasonWiseOverallDf = MatchOverviewdF.groupby("Season").get_group(Season)
    return SeasonWiseOverallDf

def GetSeasonWiseDetailData(Season):
    SeasonWiseDetailDataDf = BallAnalysisdf.groupby("Season").get_group(Season)
    return SeasonWiseDetailDataDf

def GetMatchListBySeason(Season):
    SeasonWiseOverallDf = GetSeasonWiseMatchOverwiew(Season=Season)
    Match_list = SeasonWiseOverallDf["MatchName"].unique().tolist()
    return Match_list

def GetMatchIdFromName(Season,MatchName):
    filt = (MatchOverviewdF["MatchName"] == MatchName) & (MatchOverviewdF["Season"] == Season)
    id = MatchOverviewdF[filt]["ID"].values[0]
    return int(id)

def GetMatchSummary(matchid):
    MatchSeries = MatchOverviewdF[MatchOverviewdF["ID"] == matchid]
    return MatchSeries

def GetMatchTossResults(matchid):
    MatchSeries = GetMatchSummary(matchid)
    return MatchSeries["Toss Results"].values[0]

def GetMatchResult(matchid):
    MatchSeries = GetMatchSummary(matchid)
    return MatchSeries["MatchResultTag"].values[0]

def GetPlayerOfMatchTag(matchid):
    MatchSeries = GetMatchSummary(matchid)
    Tag = "Player of the Match : " + MatchSeries["Player_of_Match"].values[0]
    return Tag

def GetBattingSummary(matchid , inning_no):
    batter_scorecard = GetInningDataFrame(matchid , inning_no).groupby("batter").sum().\
                        sort_values(by = ["batsman_run"] , ascending = False)[["batsman_run","islegal"]].iloc[0:5].reset_index()
    batter_scorecard["Runs"] = batter_scorecard["batsman_run"].apply(str)+" ("+ batter_scorecard["islegal"].apply(str) +")"
    batter_scorecard.rename(columns={"batter":"Batsman"} ,inplace= True)
    batter_scorecard.drop(columns = ["batsman_run","islegal"] , inplace = True)
    return batter_scorecard

def GetBowlingSummary(matchid , inning_no):
    Bowler_Scorecard = GetInningDataFrame(matchid , inning_no).groupby("bowler").sum().\
                        sort_values(by = ["isBowlerWicket","islegal","total_run"] ,\
                        ascending = [False,False,True])[["isBowlerWicket","total_run","islegal"]].iloc[0:5].reset_index()
    Bowler_Scorecard["overs"] = Bowler_Scorecard["islegal"].apply(lambda x : divmod(x , 6))
    Bowler_Scorecard["overs"] = Bowler_Scorecard["overs"].apply(lambda x: str(x[0])+"." +str(x[1]))
    Bowler_Scorecard.drop(columns ='islegal' ,inplace = True)
    Bowler_Scorecard.rename(columns={"bowler":"Bowler","isBowlerWicket":"W" ,"total_run":"R","overs":"O"} , inplace= True)
    return Bowler_Scorecard

def GetInningScoreTag(matchid , inning_no):
    inningdf = GetInningDataFrame(matchid,inning_no)
    BattingTeam = inningdf["BattingTeam"].unique()[0]
    BattingTeam = re.sub('[^A-Z]', '', BattingTeam)
    dict_ =inningdf.sum(numeric_only = True)\
                    [["total_run","isWicketDelivery","extras_run","islegal"]].to_dict()
    dict_.update({"BattingTeam":BattingTeam})
    overs = divmod(int(dict_["islegal"]) ,6)
    Scoretag = "{} : {}/{} ({}.{})                 Extras({})".\
                format(dict_["BattingTeam"] ,dict_["total_run"] , dict_["isWicketDelivery"] ,overs[0],overs[1],dict_["extras_run"])
    return Scoretag


def GetOrangeCapWinner(season):
    bestBatDict = GetSeasonWiseDetailData(season)
    bestBatDict = bestBatDict.groupby("batter").\
                sum(numeric_only =True)["batsman_run"].\
                    sort_values(ascending = False).reset_index().iloc[0].to_dict()
    return bestBatDict

def GetPurpleCapWinner(season):
    bestBowldict =GetSeasonWiseDetailData(season).groupby("bowler").\
                sum(numeric_only =True)["isBowlerWicket"].sort_values(ascending = False).reset_index().loc[0].to_dict()
    return bestBowldict

def GetSixesAndFoursPerSeason(season):
    dict_ = GetSeasonWiseDetailData(season)["batsman_run"].value_counts().to_dict()
    NumofFours = dict_[4]
    NumofSixes =dict_[6]
    return NumofFours , NumofSixes

def GetWinnerTeam(season):
    SeasonDf = GetSeasonWiseMatchOverwiew(season)
    TeamName = SeasonDf[SeasonDf["MatchNumber"] == "Final"]["WinningTeam"].values[0]
    return TeamName

def GetTotalWickets(season):
    SeasonDf = GetSeasonWiseDetailData(season)
    wickets = SeasonDf.sum(numeric_only = True)["isWicketDelivery"]
    return wickets

def GetNumof_FiftiesCenturies(season):
    Multiindex_ball = BallAnalysisdf.set_index(["Season","ID","innings","batter"])
    Fifties = (Multiindex_ball.groupby(level=["Season","ID","innings","batter"],sort=False)\
                        .sum()["batsman_run"] >= 50).loc[season].values.sum()
    Centuries = (Multiindex_ball.groupby(level=["Season","ID","innings","batter"],sort=False)\
                        .sum()["batsman_run"] >= 100).loc[season].values.sum()
    return Fifties , Centuries

def GetNumOFvenues(season):
    venue_list = GetSeasonWiseMatchOverwiew(season)["Venue"].unique()
    return len(venue_list)

def GetNumofTeams(season):
     Team_list = GetSeasonWiseMatchOverwiew(season)["Team1"].unique()
     return len(Team_list)

def OverallBattingRecSeason(season):
    SeasonDf= GetSeasonWiseDetailData(season)
    RunDeliveriesDf =SeasonDf.groupby("batter").sum()[["batsman_run","islegal"]].sort_values(by=["batsman_run"],ascending=False).reset_index()
    FoursSixesDf =SeasonDf.groupby("batter")["batsman_run"].value_counts().to_frame().unstack()["batsman_run"]
    OverallBattingRecSeason = RunDeliveriesDf.merge(FoursSixesDf , how = "left" ,on="batter")
    OverallBattingRecSeason["SR"] = OverallBattingRecSeason["batsman_run"] /OverallBattingRecSeason["islegal"] * 100

    #Getting Fifties and Centuries per Player

    InningWiseRuns= SeasonDf.groupby(["ID","innings","batter"]).sum()["batsman_run"]

    HighestScores = InningWiseRuns.droplevel(["ID","innings"]).reset_index()\
                .sort_values(by=["batter","batsman_run"],ascending =[False ,False]).drop_duplicates(subset = ["batter"])
    HighestScores.rename(columns ={"batsman_run":"HS"} ,inplace = True)

    isFifty = ((InningWiseRuns>= 50) & (InningWiseRuns < 100))
    isFiftydf = isFifty.droplevel(["ID","innings"]).groupby("batter").sum().reset_index()
    isFiftydf.rename(columns = {"batsman_run":"Fifties"} , inplace = True)

    isHundred = (InningWiseRuns>= 100)
    isHundreddf = isHundred.droplevel(["ID","innings"]).groupby("batter").sum().reset_index()
    isHundreddf.rename(columns = {"batsman_run":"Centuries"} , inplace = True)

    OverallBattingRecSeason = OverallBattingRecSeason.merge(isFiftydf , how = "left" ,on = 'batter')\
                                            .merge(isHundreddf ,how = "left" ,on = 'batter')\
                                            .merge(HighestScores , how = "left",on = "batter")

    OverallBattingRecSeason.fillna(0,inplace = True)
    OverallBattingRecSeason.drop(columns=[1,2,3 ],inplace=True)
    cols =OverallBattingRecSeason.drop(columns = ["batter"]).columns
    OverallBattingRecSeason[cols] = OverallBattingRecSeason[cols].astype(np.int32)
    OverallBattingRecSeason.rename(columns={'batter':"Batsman","batsman_run":"R","islegal":"BF",0:"DB",4:"F",6:"S"} , inplace=True)
    OverallBattingRecSeason = OverallBattingRecSeason[["Batsman","R","BF","HS","Fifties","Centuries","F","S","DB","SR"]]
    return OverallBattingRecSeason

def GetMost50plus(season):
    Overalldf =  OverallBattingRecSeason(season)
    Overalldf["50+"] = Overalldf["Fifties"]+ Overalldf["Centuries"]
    Overalldf = Overalldf.sort_values(by = ["50+"] , ascending = False).reset_index()
    Overalldf = Overalldf[["Batsman","50+","Fifties","Centuries","R","BF","SR","F","S"]]
    return Overalldf

def GetMostSixes(season):
    Overalldf =  OverallBattingRecSeason(season)
    Overalldf = Overalldf.sort_values(by = ["S"] , ascending = False).reset_index()
    Overalldf = Overalldf[["Batsman","S","F","R","BF","SR"]]
    return Overalldf

def GetMostFours(season):
    Overalldf =  OverallBattingRecSeason(season)
    Overalldf = Overalldf.sort_values(by = ["F"] , ascending = False).reset_index()
    Overalldf = Overalldf[["Batsman","F","S","R","BF","SR"]]
    return Overalldf

def GetHighesScores(season):
    Overalldf =  OverallBattingRecSeason(season)
    Overalldf = Overalldf.sort_values(by = ["HS"] , ascending = False).reset_index()
    Overalldf = Overalldf[["Batsman","HS","R","BF","Fifties","Centuries","F","S","SR"]]
    return Overalldf

def BestStrikeRates(season):
    Overalldf =  OverallBattingRecSeason(season)
    Overalldf = Overalldf[Overalldf["BF"]>=100]
    Overalldf = Overalldf.sort_values(by = ["SR"] , ascending = False).reset_index()
    Overalldf = Overalldf[["Batsman","SR","R","BF","HS","Fifties","Centuries","F","S"]]
    return Overalldf

def HowScoreddf(season):
    HowScored =GetSeasonWiseDetailData(season).groupby(["ID","innings","batter"])["batsman_run"].value_counts().to_frame()\
                                        .unstack().fillna(0)["batsman_run"].droplevel(["ID","innings"]).astype(np.int32)
    HowScored["T"] = HowScored[4] + HowScored[6]
    HowScored = HowScored.reset_index().drop(columns =[0,1,2,3])
    HowScored.rename(columns = {"batter":"Batsman",6:"6(I)",4:"4(I)","T":"TB"} , inplace=True)
    
    return HowScored

def GetSixesInningCard(season):
    rec_df = OverallBattingRecSeason(season)
    bound_df = HowScoreddf(season)
    bound_df = bound_df.sort_values(by=["6(I)"],ascending = [False]).drop_duplicates(subset=["Batsman"])
    rec_df = rec_df.merge(bound_df , how ="left",on = "Batsman")
    rec_df = rec_df.sort_values(by=["6(I)"],ascending = False )
    return rec_df[["Batsman","6(I)","4(I)","TB","F","S","SR","R","BF","HS"]]

def GetBoundriesInningCards(season):
    rec_df = OverallBattingRecSeason(season)
    bound_df = HowScoreddf(season)
    bound_df = bound_df.sort_values(by=["TB"],ascending = [False]).drop_duplicates(subset = ["Batsman"])
    rec_df = rec_df.merge(bound_df , how ="left",on = "Batsman")
    rec_df = rec_df.sort_values(by=["TB"],ascending = False).reset_index()
    return rec_df[["Batsman","TB","6(I)","4(I)","F","S","SR","R","BF","HS"]]


def GetSeasonBowlingRec(season):
    SeasonDf = GetSeasonWiseDetailData(season)
    BowlerRec= SeasonDf.groupby("bowler").sum()[["total_run","extras_run","isBowlerWicket","islegal"]]
    BowlerRec["Economy"] = (BowlerRec["total_run"]/BowlerRec["islegal"])*6
    BowlerRec["islegal"] = BowlerRec["islegal"].apply(lambda x:divmod(x,6)).apply(lambda x:str(x[0])+"."+str(x[1]))
    BowlerRec = BowlerRec.round(2)
    df1 = SeasonDf.groupby("bowler")["total_run"].value_counts()\
                            .to_frame().unstack().fillna(0)["total_run"].reset_index()
    BowlerRec = BowlerRec.merge(df1 ,how = "left",on = "bowler")
    BowlerRec.drop(columns =[1,2,3,5,7],inplace = True)
    BowlerRec.rename(columns ={"bowler":"Bowler","total_run":"R","isBowlerWicket":"W",0:"Dots",\
                        4:"F",6:"S","islegal":"O" ,"Economy":"Eco.","extras_run":"Extras"},inplace = True)
    BowlerRec = BowlerRec[["Bowler","W","O","R","Eco.","Dots","Extras","F","S"]]
    cols = ["O","Dots","Extras","F","S"]
    BowlerRec[cols] = BowlerRec[cols].astype(np.float64).astype(np.int32)
    BowlerRec =BowlerRec.sort_values(by = ["W"] , ascending = False)
    return BowlerRec.reset_index(drop=True)

def GetMostDotsCard(season):
    Dots_df = GetSeasonBowlingRec(season).sort_values(by=["Dots"] , ascending = False).reset_index(drop = True)
    Dots_df = Dots_df[["Bowler","Dots","W","O","R","Eco.","Extras"]]
    return Dots_df

def GetMostEcoCard(season):
    Eco_df = GetSeasonBowlingRec(season).sort_values(by=["Eco."] , ascending = True).reset_index(drop = True)
    Eco_df = Eco_df[Eco_df["O"] >=5]
    Eco_df = Eco_df[["Bowler","Eco.","W","O","R","Dots","Extras"]]
    return Eco_df



def GetPertBatsmanOverallGraph(batter):
    df = BallAnalysisdf.groupby("batter").get_group(batter)
    BattingAvg  = pd.pivot_table(df , index = ['Season',"ID"] , values=["batsman_run"] , aggfunc=sum).groupby("Season").mean()
    df1inn = df[df["innings"]==1]
    df2inn = df[df["innings"]==2]
    BattingAvg1inn = pd.pivot_table(df1inn , index = ['Season',"ID"] , values=["batsman_run"] , aggfunc=sum).groupby("Season").mean()
    BattingAvg2inn = pd.pivot_table(df2inn , index = ['Season',"ID"] , values=["batsman_run"] , aggfunc=sum).groupby("Season").mean()
    trace = go.Scatter(
            x = BattingAvg1inn.index ,
            y = BattingAvg1inn.batsman_run,
            name = "Batting First",
            line_color ="skyblue")

    trace2 = go.Scatter(
            x = BattingAvg2inn.index ,
            y = BattingAvg2inn.batsman_run,
            name = "Batting Second",
            line_color = "tan")

    trace3= go.Scatter(
                    x = BattingAvg.index ,
                    y = BattingAvg.batsman_run,
                    name = "Total",
                    line_color = "teal")

    data  = [trace , trace2, trace3]

    layout = go.Layout(
            xaxis_title='Season',
            yaxis_title='Batting Average',
            width=1000,
            height=600,
            title = "Season Wise Batting Average",
            title_x = 0.5,
            font=dict(color="white"),
            paper_bgcolor="rgb(0,0,0,0)",
            plot_bgcolor="rgb(0,0,0,0)"
            
    )

    fig = go.Figure(data = data , layout=layout)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def GetPerBatsmanOverview(batter , season ="Overall",venue="Overall" , bowler = "Overall"):
    BatterGroupby = BallAnalysisdf.groupby("batter")
    PertBatterGroupby = BatterGroupby.get_group(batter)
    outdf = PertBatterGroupby
    if season == "Overall":
        if venue == "Overall":
            if bowler == "Overall":
                BatterGroupby = BatterGroupby
                PertBatterGroupby = PertBatterGroupby
            else:
                BatterGroupby = PertBatterGroupby.groupby("bowler")
                PertBatterGroupby = BatterGroupby.get_group(bowler)    
        else:
            BatterGroupby = PertBatterGroupby.groupby("Venue")
            PertBatterGroupby = BatterGroupby.get_group(venue)
            outdf = PertBatterGroupby
            if bowler == "Overall":
                BatterGroupby = BatterGroupby
                PertBatterGroupby = PertBatterGroupby
            else:
                BatterGroupby =  PertBatterGroupby.groupby("bowler")
                PertBatterGroupby = BatterGroupby.get_group(bowler)  
    else:
        BatterGroupby = PertBatterGroupby.groupby("Season")
        PertBatterGroupby = BatterGroupby.get_group(season)
        outdf = PertBatterGroupby
        if venue == "Overall":
            if bowler == "Overall":
                BatterGroupby = BatterGroupby
                PertBatterGroupby = PertBatterGroupby
            else:
                BatterGroupby = PertBatterGroupby.groupby("bowler")
                PertBatterGroupby = BatterGroupby.get_group(bowler) 
        else:
            BatterGroupby = PertBatterGroupby.groupby("Venue")
            PertBatterGroupby = BatterGroupby.get_group(venue)
            outdf = PertBatterGroupby
            if bowler == "Overall":
                BatterGroupby = BatterGroupby
                PertBatterGroupby = PertBatterGroupby
            else:
                BatterGroupby = PertBatterGroupby.groupby("bowler")
                PertBatterGroupby = BatterGroupby.get_group(bowler) 
                
    
    runNballsfaced= PertBatterGroupby.sum(numeric_only=True)[["batsman_run","islegal"]]
    DotFourSixes = PertBatterGroupby["batsman_run"].value_counts().to_frame().unstack().\
                            fillna(0)["batsman_run"].drop(columns =[1,2,3,5] ,errors = "ignore")

    InningsWiseRuns = PertBatterGroupby.groupby(["ID","innings"])["batsman_run"].sum()
    Fifty = ((InningsWiseRuns >= 50 ) & (InningsWiseRuns <=100)).sum()
    Century = (InningsWiseRuns >= 100 ).sum()
    inningsDf = PertBatterGroupby.drop_duplicates(subset=["ID","innings"])
    innings = inningsDf.loc[:,"batter"].shape[0]
    Batsman10HScores = PertBatterGroupby.groupby(["ID","innings"])["batsman_run"].sum()\
                            .sort_values(ascending = False).values.tolist()[0]

    return_dict = runNballsfaced.to_dict()

    return_dict["Runs"] = return_dict.pop("batsman_run")
    return_dict["Balls Faced"] = return_dict.pop("islegal")
    return_dict["Innings"] = innings
    return_dict["Batting Average"] = return_dict["Runs"] / return_dict["Innings"]
    return_dict["Strike Rate"] = return_dict["Runs"]/return_dict["Balls Faced"] * 100
    return_dict["Fifty"] = Fifty
    return_dict["Century"] = Century
    return_dict["Highest Score"] = Batsman10HScores
    try:
        return_dict["Fours"] = DotFourSixes.loc[4]
    except :
        return_dict["Fours"] = 0
    try:
        return_dict["Six"] = DotFourSixes.loc[6]
    except :
        return_dict["Six"] = 0

    fig = ex.pie(DotFourSixes, values=DotFourSixes.values, names=DotFourSixes.index ,title="How the balls faced ?",\
                    color_discrete_sequence=ex.colors.sequential.Inferno)
    fig.update_layout(title_x = 0.5, width = 500,paper_bgcolor='rgba(0,0,0,0)',
                    font = dict(family='Sherif', size=14, color = "teal"))
    BatDetSeries = pd.Series(return_dict).astype(np.int32).rename("Numbers")
    return BatDetSeries , fig

def GetPertBatsmanOverallGraph(batter):

    df = BallAnalysisdf.groupby("batter").get_group(batter)
    BattingAvg  = pd.pivot_table(df , index = ['Season',"ID"] , values=["batsman_run"] , aggfunc=sum).groupby("Season").mean()
    df1inn = df[df["innings"]==1]
    df2inn = df[df["innings"]==2]
    BattingAvg1inn = pd.pivot_table(df1inn , index = ['Season',"ID"] , values=["batsman_run"] , aggfunc=sum).groupby("Season").mean()
    BattingAvg2inn = pd.pivot_table(df2inn , index = ['Season',"ID"] , values=["batsman_run"] , aggfunc=sum).groupby("Season").mean()
    trace = go.Scatter(
            x = BattingAvg1inn.index ,
            y = BattingAvg1inn.batsman_run,
            name = "Batting First",
            line_color ="skyblue")

    trace2 = go.Scatter(
            x = BattingAvg2inn.index ,
            y = BattingAvg2inn.batsman_run,
            name = "Batting Second",
            line_color = "tan")

    trace3= go.Scatter(
                    x = BattingAvg.index ,
                    y = BattingAvg.batsman_run,
                    name = "Total",
                    line_color = "teal")

    data  = [trace , trace2, trace3]

    layout = go.Layout(
            xaxis_title='Season',
            yaxis_title='Batting Average',
            width=1000,
            height=600,
            title = "Season Wise Batting Average",
            title_x = 0.5,
            font=dict(color="white"),
            paper_bgcolor="rgb(0,0,0,0)",
            plot_bgcolor="rgb(0,0,0,0)"
            
    )

    fig = go.Figure(data = data , layout=layout)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def GetBatsmanStrengthAndWeakness(batter , season = "Overall" , venue = "Overall" , bowler = "Overall"):
    Batterdf = BallAnalysisdf.groupby("batter").get_group(batter)
    if season == "Overall":
        if venue == "Overall":
            if bowler =="Overall":
                df = Batterdf
            elif bowler != None:
                df = Batterdf.groupby("bowler").get_group(bowler)       
        else:
            df = Batterdf.groupby("Venue").get_group(venue)  
            if bowler == "Overall":
                df = df
            elif bowler != None:
                df = df.groupby("bowler").get_group(bowler)    
    else:
        df = Batterdf.groupby("Season").get_group(season)
        if venue == "Overall":
            if bowler == "Overall":
                df = df
            elif bowler != None:
                df = df.groupby("bowler").get_group(bowler)       
        else:
            df = df.groupby("Venue").get_group(venue)  
            if bowler == "Overall":
                df = df
            elif bowler != None:
                df = df.groupby("bowler").get_group(bowler)  
    print(df["Season"].unique())
    Total_balls = pd.pivot_table(df , index=["bowler"] ,values=["batsman_run"] , aggfunc="count",fill_value=0).reset_index()
    Total_runs = pd.pivot_table(df , index=["bowler"] ,values=["batsman_run"] , aggfunc="sum",fill_value=0).reset_index()
    HowScoredf = pd.pivot_table(df , index=["bowler"] ,values=["batsman_run"] , aggfunc="value_counts",fill_value=0).reset_index()
    Wickets=  pd.pivot_table(df , index=["bowler"] ,values=["isBowlerWicket"] , aggfunc="sum",fill_value=0).reset_index()
    HowScoredf = HowScoredf.merge(Total_balls , on ="bowler",how = "outer").merge(Wickets , on ="bowler",how = "outer")\
                                .merge(Total_runs , on ="bowler",how = "outer")
    HowScoredf["perc"] = HowScoredf[0] /HowScoredf["batsman_run_y"] * 100 
    HowScoredf["SR"] =  HowScoredf["batsman_run"]/HowScoredf["batsman_run_y"] * 100 
    HowScoredf.rename(columns={"batsman_run_x":"ball_result" ,0:"count","batsman_run_y":"BF","isBowlerWicket":"W","batsman_run":"Run Scored "} ,inplace = True)

    return HowScoredf

def GetStrugglerBowlers(batter , season = "Overall" , venue = "Overall" , bowler = "Overall" ,min_balls = 25):
    print(season)
    HowScoredf = GetBatsmanStrengthAndWeakness(batter , season = season , venue = venue , bowler = bowler)
    BowlerBySr = HowScoredf[HowScoredf["BF"]  > min_balls ].sort_values(by = ["SR"] , ascending = True).drop_duplicates(subset = ["bowler"])
    Struggledf = BowlerBySr.iloc[:5]
    Struggledf = Struggledf.drop(columns = ["ball_result","count","perc"]).reset_index(drop = True)
    bowler_list = Struggledf["bowler"].unique().tolist()
    bowler_list.insert(0, "Select Bowler")
    return Struggledf , bowler_list

def GetComfortBowlers(batter , season = "Overall" , venue = "Overall" , bowler = "Overall" ,min_balls = 25 ):
    HowScoredf = GetBatsmanStrengthAndWeakness(batter , season = season , venue = venue , bowler = bowler)
    BowlerBySr = HowScoredf[HowScoredf["BF"]  > min_balls ].sort_values(by = ["SR"] , ascending = False).drop_duplicates(subset = ["bowler"])
    ScoresDf = BowlerBySr.iloc[:5]
    ScoresDf = ScoresDf.drop(columns = ["ball_result","count","perc"]).reset_index(drop = True)
    bowler_list = ScoresDf["bowler"].unique().tolist()
    bowler_list.insert(0, "Select Bowler")
    return ScoresDf , bowler_list

def GetFallsAgainst(batter , season = "Overall" , venue = "Overall" , bowler = "Overall"):

    HowScoredf = GetBatsmanStrengthAndWeakness(batter , season = season , venue = venue , bowler = bowler)
    HowScoredf = HowScoredf[HowScoredf["W"] != 0]
    Fallsdf = HowScoredf.sort_values(by =["W"] , ascending= False).drop_duplicates(subset = ["bowler"]).iloc[:5]
    Fallsdf = Fallsdf.drop(columns = ["ball_result","count","perc"]).reset_index(drop = True)
    bowler_list = Fallsdf["bowler"].unique().tolist()
    bowler_list.insert(0, "Select Bowler")
    return Fallsdf , bowler_list

def BattervsBowlerDetail(batter ,bowler, season = "Overall" , venue = "Overall"):
    DotFourSixes = GetBatsmanStrengthAndWeakness(batter , season = season , venue = venue , bowler = bowler).groupby("bowler").get_group(bowler)
    fig = ex.pie(DotFourSixes, values=DotFourSixes.perc, names=DotFourSixes.ball_result,title="How the balls faced ?",\
                    color_discrete_sequence=ex.colors.sequential.Emrld)
    fig.update_layout(title_x = 0.5, width = 500,paper_bgcolor='rgba(0,0,0,0)',
                    font = dict(family='Sherif', size=14, color = "teal"))
    DotFourSixes =  DotFourSixes.drop_duplicates("bowler").\
                        drop(columns = ["ball_result","count","perc"]).reset_index(drop = True)
    return DotFourSixes , fig

def BatterListbySeasonandVenue(season = "Overall",venue = "Overall"):
    df = BallAnalysisdf
    if season   == "Overall":
        if venue == "Overall":
            batterlist = df["batter"].unique().tolist()
            batterlist.insert(0 , "Select Batter")
            return batterlist
        
        if venue != "Overall":
            df = df.groupby("Venue").get_group(venue)
            batterlist = df["batter"].unique().tolist()
            batterlist.insert(0 , "Select Batter")
            return batterlist

    
    if season != "Overall":
        df = df.groupby("Season").get_group(season)
        if venue == "Overall":
            batterlist = df["batter"].unique().tolist()
            batterlist.insert(0 , "Select Batter")
            return batterlist
        
        if venue != "Overall":
            df = df.groupby("Venue").get_group(venue)
            batterlist = df["batter"].unique().tolist()
            batterlist.insert(0 , "Select Batter")
            return batterlist