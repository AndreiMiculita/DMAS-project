import numpy as np
from params import *

#counts number of agents, landmarks and empty houses
def agent_count(city):
    agents = 0
    empty = 0
    landmarks = 0
    for (x,y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            agents += 1
        elif not house.empty:
            landmarks += 1
        else:
            empty +=1
    print("agents, landmarks, empty")
    print(agents, landmarks, empty)
    
#counts hoshen_kopelman clusters for religion
def cluster_religion(city):
    agent_counted = []
    clusters = []
    for (x,y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            agent = house.occupant
            if x==0 and y==0:
                clusters.append([agent.religion.value,[[x,y]]])  
                agent_counted.append([x,y])
            elif x==0:
                for cluster in clusters:
                    if [x,y-1] in cluster[1] and agent.religion.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        break
                if [x,y] not in agent_counted:
                    clusters.append([agent.religion.value,[[x,y]]])
                    agent_counted.append([x,y])
            elif y==0:
                for cluster in clusters:
                    if [x-1,y] in cluster[1] and agent.religion.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        break
                if [x,y] not in agent_counted:
                    clusters.append([agent.religion.value,[[x,y]]])
                    agent_counted.append([x,y])
            else:
                for cluster in clusters:
                    if [x,y-1] in cluster[1] and agent.religion.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        for cluster_check in clusters:
                            if [x-1,y] in cluster_check[1] and agent.religion.value == cluster_check[0] and cluster_check != cluster:
                                for i in cluster_check[1]:
                                    cluster[1].append(i)
                                clusters.remove(cluster_check)
                                break
                        break
                    elif [x-1,y] in cluster[1] and agent.religion.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        for cluster_check in clusters:
                            if [x,y-1] in cluster_check[1] and agent.religion.value == cluster_check[0] and cluster_check != cluster:
                                for i in cluster_check[1]:
                                    cluster[1].append(i)
                                clusters.remove(cluster_check)
                                break
                        break
                if [x,y] not in agent_counted:
                    clusters.append([agent.religion.value,[[x,y]]])
                    agent_counted.append([x,y])
            continue
        
    print("number of religion clusters:", len(clusters))
    total_count = 0
    for i in clusters:
        total_count += len(i[1])
    print("number of agents:", total_count)
    mean_cluster_size = total_count/len(clusters)
    print("average cluster size:", mean_cluster_size)
    return total_count, mean_cluster_size
    #for i in clusters:
     #   print(i)
    
#counts hoshen_kopelman clusters for ethnicity
def cluster_ethnicity(city):
    agent_counted = []
    clusters = []
    for (x,y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            agent = house.occupant
            if x==0 and y==0:
                clusters.append([agent.ethnicity.value,[[x,y]]])  
                agent_counted.append([x,y])
            elif x==0:
                for cluster in clusters:
                    if [x,y-1] in cluster[1] and agent.ethnicity.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        break
                if [x,y] not in agent_counted:
                    clusters.append([agent.ethnicity.value,[[x,y]]])
                    agent_counted.append([x,y])
            elif y==0:
                for cluster in clusters:
                    if [x-1,y] in cluster[1] and agent.ethnicity.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        break
                if [x,y] not in agent_counted:
                    clusters.append([agent.ethnicity.value,[[x,y]]])
                    agent_counted.append([x,y])
            else:
                for cluster in clusters:
                    if [x,y-1] in cluster[1] and agent.ethnicity.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        for cluster_check in clusters:
                            if [x-1,y] in cluster_check[1] and agent.ethnicity.value == cluster_check[0] and cluster_check != cluster:
                                for i in cluster_check[1]:
                                    cluster[1].append(i)
                                clusters.remove(cluster_check)
                                break
                        break
                    elif [x-1,y] in cluster[1] and agent.ethnicity.value == cluster[0]:
                        cluster[1].append([x,y])
                        agent_counted.append([x,y])
                        for cluster_check in clusters:
                            if [x,y-1] in cluster_check[1] and agent.ethnicity.value == cluster_check[0] and cluster_check != cluster:
                                for i in cluster_check[1]:
                                    cluster[1].append(i)
                                clusters.remove(cluster_check)
                                break
                        break
                if [x,y] not in agent_counted:
                    clusters.append([agent.ethnicity.value,[[x,y]]])
                    agent_counted.append([x,y])
            continue
        
    print("number of ethnicity clusters:", len(clusters))
    total_count = 0
    for i in clusters:
        total_count += len(i[1])
    print("number of agents:", total_count)
    mean_cluster_size = total_count/len(clusters)
    print("average cluster size:", mean_cluster_size)
    return total_count, mean_cluster_size
    #for i in clusters:
     #   print(i)

#income comparison   
def income_comparison(city):
    income_happiness = []
    for (x,y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            agent = house.occupant
            house_neighbors = []
            for i in range(x - 1, x + 1 + 1):
                for j in range(y - 1, y + 1 + 1):
                    if i==x or j==y:
                        if 0 <= i < len(city)-1 and 0 <= j < len(city[0])-1:
                            if not city[i][j].empty and city[i][j].occupant != agent and not city[i][j].landmark:
                                house_neighbors.append(city[i][j].occupant)
            income_gap = 0
            for neighbor in house_neighbors:
                income_gap += min(agent.income.value, neighbor.income.value)/max(agent.income.value, neighbor.income.value)
            if income_gap == 0:
                income_happiness.append(0)
            else:
                income_happiness.append(income_gap/len(house_neighbors))
        continue
    print("income gap average is:", sum(income_happiness)/len(income_happiness))
    
    
    
    
    
    
    
    
    
    
    
    
    
    