import predict_match
import imp

predict_match=imp.reload(predict_match)

import pandas as pd

points_table={'CSK':0,'DD':0,'KKR':0,'KXP':0,'MI':0,'RCB':0,'RR':0,'SRH':0}

df_schedule = pd.read_csv('ipl2018_schedule.csv')
df_schedule=df_schedule.dropna()
df_rain = pd.read_csv('ChanceofRain.csv')

for i in range(len(df_schedule)):
    team1=df_schedule['Team1'][i]
    team2=df_schedule['Team2'][i]
    date=df_schedule['Date'][i]
    print("\n----"+team1+" VS "+team2+"----\n")
    #print(team1,team2,type(team1))
    for j in range(len(df_rain)):
        #print("1",team1,team2,date)
        #print("2",df_rain['Team 1'][j],df_rain['Team 2'][j],df_rain['Date'][j])
        
        if((team1==df_rain['Team 1'][j])and(team2==df_rain['Team 2'][j])and(date==df_rain['Date'][j])):
            probability_of_rain=df_rain['Chance of Rain'][j]
            print("Probability of rain is:",probability_of_rain)
            if(probability_of_rain>0.5):
                points_table[team1]+=1
                points_table[team2]+=1
                print("Match interrupted due to rain: DRAW")
            else:
                team1_order=pd.read_csv('2018/'+team1+'.csv')
                team2_order=pd.read_csv('2018/'+team2+'.csv')
                bothteams_order=pd.concat([team1_order,team2_order],axis=1)
                bothteams_order.to_csv("TestInputMatch.csv",index=False)
                match_result=predict_match.main(team1,team2)
                if(match_result==1):
                    points_table[team1]+=2
                elif(match_result==2):
                    points_table[team2]+=2
                else:
                    points_table[team1]+=1
                    points_table[team2]+=1
                
            break;

print(points_table)

import operator
sorted_points_table = sorted(points_table.items(), key=operator.itemgetter(1),reverse=True)

top4=[]

for i in range(0,5):
    top4.append(sorted_points_table[i][0])

def match(team1,team2):
    team1_order=pd.read_csv('2018/'+team1+'.csv')
    team2_order=pd.read_csv('2018/'+team2+'.csv')
    bothteams_order=pd.concat([team1_order,team2_order],axis=1)
    bothteams_order.to_csv("TestInputMatch.csv",index=False)
    match_result=predict_match.main(team1,team2)
    if(match_result==1):
        return team1,team2
    elif(match_result==2):
        return team2,team1
                    
first_finalist,pre_finalist1=match(top4[0],top4[1])
pre_finalist2,temp=match(top4[2],top4[3])
second_finalist,temp=match(pre_finalist1,pre_finalist2)
winner,second=match(first_finalist,second_finalist)

print("--- Winner is: "+winner+" ----")

    
