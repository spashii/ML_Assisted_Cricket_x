import numpy as np 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
dele=pd.read_csv("deliveries.csv")
matches=pd.read_csv("matches.csv")
matches['match_id'] = matches['id']
matches = matches.drop('id', axis=1)
df = dele.merge(matches, on='match_id', how='left')
teams = set(df.team1.unique()).union(set(df.team2.unique()))
players = set(df.batsman.unique()).union(set(df.bowler.unique())).union(set(df.non_striker.unique()))
players=list(players)
#encoders
batenc = LabelEncoder()
bowlenc=LabelEncoder()
player_encoder = LabelEncoder()
venue_encoder = LabelEncoder()
batenc.fit(df['batting_team'])
bowlenc.fit(df['bowling_team'])
player_encoder.fit(players)
venue_encoder.fit(df.venue)
#adding encoded values to data
df['batting_team_e']=batenc.transform(df['batting_team']).copy()
df['bowling_team_e']=bowlenc.transform(df['bowling_team']).copy()
df['venue_e'] = venue_encoder.transform(df.venue)
df['batsman_e'] = player_encoder.transform(df.batsman)
df['non_striker_e'] = player_encoder.transform(df.non_striker)
df['bowler_e'] = player_encoder.transform(df.bowler)
y = df.total_runs * ((~df.player_dismissed.isnull()).map({True: -1, False: 1}))
#making classes
df['will_be_out'] = y<0
df['four']= (y==4)
df['six']= (y==6)
forest = RandomForestClassifier(n_jobs=-1)
X = df[['batting_team_e','bowling_team_e','batsman_e', 'non_striker_e', 'bowler_e', 'over', 'ball',
        'inning']]
# print(cross_val_score(forest, X, df.will_be_out, cv=10, scoring='roc_auc',n_jobs=-1).mean())
x='Sunrisers Hyderabad'
def predict_out(bat_team,bowl_team,season,batsman,nonstriker,bowler,over,bowl_no,inning):
	train_data=df[(df['season']!=2008)&(df['season']!=2009)]
	X1=train_data[['batting_team_e','bowling_team_e','batsman_e', 'non_striker_e', 'bowler_e', 'over', 'ball',
        'inning']]
    y1=train_data['will_be_out']
	prob=cross_val_score(forest, train_data, train_data.will_be_out, cv=10, scoring='roc_auc',n_jobs=-1).mean()
	X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.2, random_state=40)
	forest.fit(X_train,y_train)
	forest.fit(X,df['will_be_out'])

