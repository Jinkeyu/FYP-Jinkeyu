# 0.0 coding:utf-8 0.0
# 找出最优解和最优解的基因编码


def best(Pop, Cost_list,Temp_pop_start,Temp_pop_end):
    Best_fit = []                           #optimal value最优解数值
    Best_individual = []                    #optimal gene最优基因
    Best_starttime = []                     #optimal startingtime最优开始时间
    Best_endtime = []                       #optimal ending time最优结束时间
    for i in range(len(Cost_list)):
        Best_fit.append(Cost_list[i][0])    #The first value of variables' lists as optimal value先把每个变量列表中的第一个值作为最优值
        Best_individual.append(Pop[i][0])   #The first of each species as optimal gene把每个物种中的第一个作为最优基因
        Best_starttime.append(Temp_pop_start[i][0]) #第一个开始和结束时间作为最优值
        Best_endtime.append(Temp_pop_end[i][0])
        
    for i in range(len(Cost_list)):
        for j in range(len(Cost_list[i])):
            if(Cost_list[i][j] < Best_fit[i]):
                Best_fit[i] = Cost_list[i][j]
                Best_individual[i] = Pop[i][j]
                Best_starttime[i] = Temp_pop_start[i][j]
                Best_endtime[i] = Temp_pop_end[i][j]
    return Best_individual, Best_fit ,Best_starttime, Best_endtime

if __name__ == '__main__':
    pass
