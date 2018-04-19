# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:43:14 2017

@author: john
"""

#! python3

#
# genetic.py
#
#---------------------------------------------------------------------
#
#
# the fittest individual will have a chromosome consisting of 30 '1's
#

import random

import matplotlib.pyplot as plt
import math

from geneEncoding import geneEncoding     #multi-species geneEncoding（进行多物种基因编码）
from calobjValue import calobjValue       #calculate the corresponding gene decimal value(计算基因对应的十进制数值)
from calobjValue import calculateCost     #calculate cost(计算每一次电费值)
from calobjValue import calcostValue      #calculate the total cost according to the time schedule(根据得到的时间表计算所有电费的情况)
from best import best
from selection import selection
from crossover import crossover
from mutation import mutation


#first user
#class appliances:
#unit K watt
Television = 200/1000.0                        #Working power
Air_conditioner = 1500/1000.0 
Washing_machine = 400/1000.0 
Electric_cooker = 500/1000.0
Refrigerator = 150/1000.0 

Appliance = [Television,Air_conditioner,Washing_machine,Electric_cooker,Refrigerator]


Television_period = [20.0,22.0]                 #Working period
Air_conditioner_period = [7.0,9.0,18.0,22.0]
Washing_machine_period = [18.0,20.0]
Electric_cooker_period = [7.0,7.5]
Refrigerator_period = [1.0,24.0]

Period = [Television_period,Air_conditioner_period,Washing_machine_period,Electric_cooker_period,Refrigerator_period]

Peak_starttime = 6.0       #peak_start time(峰电开始时间)
Peak_endtime = 22.0        #peak_end time(峰电结束时间)
Peak_period = 16.0         #峰电持续时间(Peak_endtime - Peak_starttime)

Valley = 0.6         #valley price(谷电电价)
Peak = 1.2           #peak price(峰电电价)

User1 = []


#second user
#class appliance
#unit K watts

Television = 200/1000.0 
Air_conditioner = 1500/1000.0 
Washing_machine = 400/1000.0 
Electric_cooker = 500/1000.0
Refrigerator = 150/1000.0

Appliance = [Television,Air_conditioner,Washing_machine,Electric_cooker,Refrigerator]

Television_period = [19.0,21.0]
Air_conditioner_period = [17.0,22.0]
Washing_machine_period = [20.0,21.0]
Electric_cooker_period = [18.0,19.0]
Refrigerator_period = [1.0,24.0]

Period = [Television_period,Air_conditioner_period,Electric_cooker_period,Refrigerator_period]

Peak_starttime = 6.0       #peak_start time(峰电开始时间)
Peak_endtime = 22.0        #peak_end time(峰电结束时间)
Peak_period = 16.0         #峰电持续时间(Peak_endtime - Peak_starttime)

Valley = 0.6         #valley price(谷电电价)
Peak = 1.2           #peak price(峰电电价)
 
 
User2 = []


#get the specific datas of user(获取用户具体的用电数据)

i = 0
while i<5:                                       
    User1.append([])                             
    User1.append([])
    User1[2*i].append(Appliance[i])         #user data, even part decide/choose the type of appliance
    User1[2*i+1].append(Period[i])          #odd part decide the period of appliance
    i = i+1

i = 0
while i<5:
    User2.append([])
    User2.append([])
    User2[2*i].append(Appliance[i])
    User2[2*i+1].append(Period[i])
    i = i+1


Cost, Time_slots , Timelist ,Indivisual_cost = calculateCost(User1)    #(费用，用电时段数以及电器的时间表)
Cost, Time_slots , Timelist ,Indivisual_cost = calculateCost(User2)    


#construct inherit species开始建立遗传种群
Species_size  = Time_slots           # a specie stands for a variable(物种个数，一个物种代表一个变量)
Pop_size = 500		             # the individual number of a species（种群数量，每一个物种中的个体数目）
Iteration = 100                      # species iteration times(种群迭代次数为100次)
Max_value = 240                      # the maximum value allowed in gene（基因中允许出现的最大值  24小时)
Chrom_length = 8                     # chromesome length(染色体长度)
Pc = 0.6		             # copulation probability(交配概率)
Pm = 0.01                            # mutation probability(变异概率)
Results = []	                     # save each generation's best solution(存储每一代的最优解，N个二元组)
Fit_value = []		             # individual(个体适应度)
Fit_mean = []		             # average(平均适应度)
num_users = 2                        # number of users
const_load = []                     # former user schedule load 

for u in range(num_users):
    
    # run genetic algorithm for one user
    Pop = geneEncoding(Species_size,Pop_size,Chrom_length)   #construct ecosphere(建立生物圈)

    for i in range(Iteration):           #begin genetic algorithm(开始进行遗传算法)
        Temp_pop_start,Temp_pop_end = calobjValue(Pop, Chrom_length, Timelist , Species_size)        # calculate power supply time period(计算供电时间)
        # TODO: Redefine calcostValue function based on const_load
        Cost_list = calcostValue(Temp_pop_start, Temp_pop_end, u,) #get the electricity price(得到电费价格表)
        
        Best_gene , Best_Results,Best_starttime,Best_endtime = best(Pop, Cost_list,Temp_pop_start,Temp_pop_end)     #get the best gene and the corresponding power start time and end time(找到最优基因及最优解以及最优解对应的供电起始时间)          
        Results.append([Best_Results, Best_starttime, Best_endtime])  #save the best result of each generation(存储每一代的最优结果)
        selection(Pop,Cost_list)                            #copy the new species(新种群开始进行复制)
        crossover(Pop, Pc)		                             #(对新种群进行交配)
        mutation(Pop, Pm)                                   #对种群进行变异
    
    
    Final_results = []
    for i in range(len(Pop)):
        Final_results.append([])
        for j in range(len(Results)):
            Final_results[i].append(Results[j][0][i])
            
    for i in range(len(Final_results)):
        #Final_results[i] = Final_results[i][1:]
        Final_results[i].sort()
   
    # TODO
    const_load = [Final_results,temp_start_time,temp_end_time] # based on Final_results of other users -> the results of the GA for applicance schedule    
    

for i in range(len(Final_results)):
       print(Final_results[i][0])         #print minimum value打印最小值
print(Best_Results)                #print optimal solution打印最优解
print(Best_gene)		           #print the best individual打印最优个体
print(Best_starttime)              #The optimal Starttime and endtime最佳的用电器开始和结束时间
print(Best_endtime)


print('ok')
X = []
Y = []
for i in range(len(Final_results)):
    X.append([])
    for j in range(len(Final_results[i])-1,-1,-1):
        X[i].append(j)

for i in range(len(Final_results)):
    plt.plot(X[i], Final_results[i])



plt.show()
plt.show()