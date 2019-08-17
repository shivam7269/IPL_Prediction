"""
Preprocessing work :

1. Replace tabs with comma (,) in GvG Probabilities.
2. Convert that into csv by appending .csv to it.

Steps :

1. Read Batsman input from T1
2. Read Bowler input from T2

Loop :
    3. Determine their PvP Probabilities. 
    4. Determine their cluster numbers if PvP doesn't exist.
    5. Find GvG probability.
    6. RandomNumberGenerator of the array.
    7. Update Batsmen and Bowlers accordingly.
"""


import csv
import random


# To identify which cluster the batsman and bowler belong to.
def cluster_number(batsman, bowler) :

    # Determines respective batsman's cluster number
    with open('BattingStats-clustered.csv', 'r') as f:
        bat_cluster_reader = csv.reader(f)
        for row in bat_cluster_reader:
            if batsman == row[1]:
                curr_bat_cluster_num = row[13]


    # Determines respective bowler's cluster number
    with open('BowlingStats-clustered.csv', 'r') as f:
        bow_cluster_reader = csv.reader(f)
        for row in bow_cluster_reader:
            if bowler == row[1]:
                curr_bow_cluster_num = row[11]
    
    if 'curr_bat_cluster_num' in locals() and 'curr_bow_cluster_num' in locals():
        return curr_bat_cluster_num, curr_bow_cluster_num
    else:
        return -1,-1


# Extract the corresponding row from PvP Probabilites file 
# Returns <Combo is existent or not>, <Probabilities list ('None' if it doesn't exist)>
def pvp_plist(batsman, bowler) :
    #print(batsman,bowler,type(batsman),type(bowler))
    pvp_check = False
    with open('2_PvP_probabilities.csv', 'r') as f:
        pvp_reader = csv.reader(f)
        for row in pvp_reader:
            if batsman == row[0] and bowler == row[1]:
                #print(batsman,row[1],type(batsman),type(row[0]))
                #print('l')
                pvp_check = True
                probs_list = row
                
                """
                probs_list 
                0,       1,         2,  3,  4,  5,  6,  7,  8            9
                Batsman, Bowler, 0s, 1s, 2s, 3s, 4s, 6s, Dismissal, BallsFaced
                """
            
    
    if pvp_check :
        #print(probs_list)   
        probs_list = probs_list[2:9]
        #print(probs_list)
        probs_list = list(map(float, probs_list))
        #print(probs_list)

        return pvp_check,probs_list
    else :
        return pvp_check,None
   
# Extract the corresponding row from GvG Probabilites file for non-existent combos
def gvg_plist(bat_cluster_number, bowler_cluster_number) :
    gvg_check = False
    with open('2_GvG_probabilities.csv', 'r') as f:
        gvg_reader = csv.reader(f)
        for row in gvg_reader:
            if bat_cluster_number == row[0] and bowler_cluster_number == row[1]:
                gvg_check = True
                probs_list = row                
                """
                probs_list 
                0,              1,               2,  3,  4,  5,  6,  7,  8
                BatsmanCluster, BowlerCluster, 0s, 1s, 2s, 3s, 4s, 6s, Dismissal
                """
    if gvg_check:
        probs_list=probs_list[0:9]
        probs_list = list(map(float, probs_list))
        probs_list = probs_list[2:]
        return probs_list
    else:
        return None


# The Prediction
def random_pick(some_list, probabilities) :
    
    x = random.uniform(0,sum(probabilities))
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item


# Computation for every ball in an innings
# 'inn' refers to either first innings or second innings (1 or 2)
def innings(bat_order, bow_order, inn, discrete_list) : 
    
    tot_wickets = 0
    m = 1    # Index of current batsman (Will be swapped in loop)
    n = 0  # Index of standing batsman (Will be swapped in loop)
    m_notout=1
    n_notout=1
    # Assuming that only 5 players bowl
    # 20 elements. Each element represents which bowler has to bowl the respective over.
    bow_index_order = [0,1,0,1,2,3,4,2,3,4,2,3,4,2,3,4,0,1,0,1]  
    x = bow_index_order[0]

    total_runs = 0
    k = -1
    #print(bat_order[n])
    #print(bat_order[m])
    for i in range(0,120) :

        # Swap batsman and Change bowlers for every 6 balls
        if i%6 == 0 :
            k += 1
            x = bow_index_order[k]

            tmp_m = m
            tmp_notout=m_notout
            m = n
            m_notout=n_notout
            n = tmp_m
            n_notout=tmp_notout

        curr_bat = bat_order[m].rstrip() # Current Batsman
        other_bat=bat_order[n].rstrip() #Non-Striker
        curr_bow = bow_order[x].rstrip() # Current Bowler
        
        # Prediction
        existent, pvp_p_list = pvp_plist(curr_bat,curr_bow) 
        #print(pvp_p_list) 
        if existent :
            #print("old")
            #print(pvp_p_list[6])
            m_notout*=float(1-(pvp_p_list[6]))
            prediction = random_pick(discrete_list, pvp_p_list)
            #print(prediction)
        else :
            #print("new")
            #print(curr_bat,curr_bow)
            bat_c_num, bow_c_num = cluster_number(curr_bat, curr_bow)
            gvg_p_list = gvg_plist(bat_c_num, bow_c_num)
            m_notout*=float(1-(gvg_p_list[6]))
            #if gvg_p_list :
            prediction = random_pick(discrete_list, gvg_p_list)
            '''else:
                #checking -- remove
                prediction = random_pick(discrete_list,[0.335856035,0.407689261,0.031890957,0.021696582,0.02209199,0.5,0.180775183])'''
        #print(prediction)        
       # If prediction is a dot ball or 2 runs or 4 runs or 6 runs
        if prediction==0 or prediction==2 or prediction==4 or prediction==6: 
            total_runs+=prediction 

        # If prediction is 1 run or 3 runs, Swap batsmen
        elif prediction==1 or prediction==3:
            total_runs+=prediction
            tmp_m = m
            tmp_notout=m_notout
            m = n
            m_notout=n_notout
            n = tmp_m
            n_notout=tmp_notout
            #print(m,n)
        #print(total_runs)    
        # If prediction is a dismissal, Then arriving batsman replaces the current batsman
        elif m_notout<0.4:
            tot_wickets+=1
            m=max(m,n) + 1
            m_notout=1
            # If they are all out
            if m > 10 :
                break
        
        # If it is second innings and if the team has chased the target
        '''if inn == 2 and total_runs > first_inn_score :
            break
            

        if inn == 1 :
            global first_inn_score
            first_inn_score = total_runs'''
                
    num_of_overs_played = str(int((i+1)/6)) + "." + str((i+1)%6)  
    return total_runs, str(total_runs)+"/"+str(tot_wickets)+" Overs : "+ num_of_overs_played


# MAIN 
    
def main(team1,team2):
    
    t1_bat_order = []
    t1_bow_order = []
    t2_bat_order = []
    t2_bow_order = []

    discrete_list = [0, 1, 2, 3, 4, 6, 7] # Here 7 refers to dismissal, Used for probability distribution.
                                      # See method random_pick()


# Extraction of squads from the CSV and storing them in respective lists
    with open('TestInputMatch2.csv', 'r') as f:
        match_reader = csv.reader(f)
        next(match_reader)
        for row in match_reader:
            t1_bat_order.append(row[0])
            t1_bow_order.append(row[1])
            t2_bat_order.append(row[2])
            t2_bow_order.append(row[3])

    t1_bat_order = [x for x in t1_bat_order if x != '']
    t1_bow_order = [x for x in t1_bow_order if x != '']
    t2_bat_order = [x for x in t2_bat_order if x != '']
    t2_bow_order = [x for x in t2_bow_order if x != '']

    t1_bow_order = t1_bow_order[:5] # Restricting to 5 bowlers
    t2_bow_order = t2_bow_order[:5]
    
  

    innings(t1_bat_order, t2_bow_order, 1, discrete_list)
    first_innings_score, formatted_score1 = innings(t1_bat_order, t2_bow_order, 1, discrete_list)
    print (team1+" Score : " + formatted_score1)

    second_innings_score, formatted_score2 = innings(t2_bat_order, t1_bow_order, 2, discrete_list)
    print (team2+" Score : " + formatted_score2)

    if first_innings_score > second_innings_score :
        print(team1+" wins!")
        return 1
    elif second_innings_score > first_innings_score :
        print(team2+" wins!")
        return 2
    else :
        print("Match Tied.")
        return 0

#main()
main('MI','DD')
