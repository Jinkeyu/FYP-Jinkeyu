# 0.0 coding:utf-8 0.0
# 解码并计算值

import math

#针对整个种群的解码函数
def decodechrom(Pop, chrom_length):
    temp = []
    for i in range(len(Pop)):
        temp.append([])
        for j in range(len(Pop[i])):
            t = 0
            for k in range(chrom_length):
                t += Pop[i][j][k] * (math.pow(2, k))
            temp[i].append(t)
    return temp

#计算开始时间的函数
#Pop: 经过解码之后的种群
#Chrom_length: 基因长度
#Timelist    : 供电时间表
def caltimeValue(Pop_decoded,Chrom_length,Timelist):
    Variable = 0 
    Temp_pop_start = []                            #用来记录电器开始工作的时间
    Temp_pop_end = []                              #用来记录电器结束工作的时间
    for i in range(len(Timelist)):
        for j in range(len(Timelist[i])//2):
            Starttime = Timelist[i][2*j]           #获得每个用电器的使用开始和结束时间，由于时间不一定是一段，所以要分情况讨论
            Endtime = Timelist[i][2*j+1]
            if Starttime < Endtime:
                Period = Endtime - Starttime       #计算每个用电器的使用时长
            else:
                Period = (24 - Starttime + Endtime)
            
            Temp_pop_start.append([])
            Temp_pop_end.append([])
            
            #计算用电器开始使用的时间 
            for k in range (len(Pop_decoded[Variable])):        #用电器仅使用一次的情况
                temp = (Starttime - 1.5) + 1.5*2.0*Pop_decoded[Variable][k]/(math.pow(2, Chrom_length) - 1)   #在这里认为电器的使用时间不能被移动1.5小时以上
                if temp > 24.0:
                    temp = temp - 24.0    #调整时间范围，确保时间段落入0——24小时中
                elif temp < 0:
                    temp = -temp 
                Temp_pop_start[Variable].append(temp)
                
                temp = temp + Period      #计算用电器结束使用的时间
                if temp > 24.0:
                    temp = temp - 24.0    #调整时间范围，确保时间段落入0——24小时中
                elif temp < 0:
                    temp = -temp 
                Temp_pop_end[Variable].append(temp)
                
            Variable = Variable + 1
            
    return Temp_pop_start,Temp_pop_end        
    

#解码并计算开始结束时间
def calobjValue(Pop, Chrom_length, Timelist, Species_size):
    Pop_decoded = []                     
    Pop_decoded = decodechrom(Pop, Chrom_length)   #经过解码的种群
    Temp_pop_start,Temp_pop_end = caltimeValue(Pop_decoded, Chrom_length, Timelist)
    return Temp_pop_start, Temp_pop_end


#计算用户电费的程序
def calculateCost(User1):
    Peak_starttime = 6.0       #峰电开始时间
    Peak_endtime = 22.0        #峰电结束时间
    Peak_period = 16.0         #峰电持续时间(Peak_endtime - Peak_starttime)
    
    Valley = 0.6               #谷电电价
    Peak = 1.2                 #峰电电价    
    
    Cost = 0                   #总电费
    Time_slots = 0             #总使用电器时间段数目
    Timelist = []              #开始时间表
    Individual_cost = []       #单项电费表
    
    for i in range((len(User1)//2)):    
        Temp = User1[2*i+1]        #存储电器的使用时间的列表
        Power = User1[2*i][0]         #存储当前使用电器功率值
        Timelist.append(User1[2*i+1][0])
        #print(Temp)
        #考虑所有的情况，一共有12种电费计价方式
        j = 0
        for j in range(len(Temp[0])//2):
            Starttime = Temp[0][2*j]
            Endtime = Temp[0][2*j+1]
            Time_slots = Time_slots + 1
            Last_cost = Cost
            #情况一，开始时间与结束时间在低谷段，开始时间小于或大于结束时间(4种子情况)
            if ((Starttime <= Peak_starttime and Endtime <= Peak_starttime) or (Starttime >= Peak_endtime and Endtime >= Peak_endtime)):
                if(Starttime < Endtime ):
                    Cost = Cost + (Endtime - Starttime)*Valley*Power
                else:
                    Cost = Cost + Peak_period*Peak*Power + ((24.0 - Peak_period) - (Starttime - Endtime))*Valley*Power
            
            #情况二，开始时间小于峰电开始时间，结束时间大于峰电开始时间，结束时间大于或小于峰电结束时间(2种子情况)       
            elif (Starttime <= Peak_starttime and Endtime >= Peak_starttime):
                if(Endtime < Peak_endtime):
                    Cost = Cost + (Peak_starttime - Starttime)*Valley*Power + (Endtime - Peak_starttime)*Peak*Power
                else:
                    Cost = Cost + (Peak_starttime - Starttime)*Valley*Power + \
                                  (Endtime - Peak_endtime)*Valley*Power + \
                                  Peak_period*Peak*Power
            
            #情况三，开始时间处于峰电区间内，结束时间大于或小于开始时间(4种子情况)        
            elif (Starttime >= Peak_starttime and Starttime <= Peak_endtime ):
                    #结束时间大于开始时间，判断结束时间在峰电区间内还是外
                if(Endtime > Starttime):
                    if(Endtime < Peak_endtime):
                        Cost = Cost + (Endtime - Starttime)*Peak*Power
                    else:
                        Cost = Cost + (Peak_endtime - Starttime)*Peak*Power + (Endtime - Peak_endtime)*Valley*Power
                    #结束时间小于开始时间，判断结束时间是否在峰电区间内
                else:
                    if(Endtime < Peak_starttime):
                        Cost = Cost + (Peak_endtime - Starttime)*Peak*Power + (Endtime + 24.0 -Peak_endtime)*Valley*Power
                    else:
                        Cost = Cost + (24.0 - Peak_endtime + Peak_starttime)*Valley*Power + (Peak_endtime - Peak_starttime - (Starttime - Endtime))*Peak*Power
             
            #情况四，开始时间大于峰值结束时间
            elif (Starttime >= Peak_endtime and Endtime <= Peak_endtime):
                if(Endtime < Peak_starttime):
                    Cost = Cost + (24.0 - Starttime + Endtime)*Valley*Power
                else:
                    Cost = Cost + (24.0 - Starttime + Peak_starttime)*Valley*Power + (Endtime - Peak_starttime)*Peak*Power
            
            Individual_cost.append(Cost - Last_cost)
    return Cost , Time_slots , Timelist , Individual_cost

#得到时间表之后，计算每一种情况电费的程序
def calcostValue(Temp_pop_start,Temp_pop_end,User):
    Cost_list = []             #电费列表
    for i in range(len(Temp_pop_start)):
        Cost_list.append([])

    for k in range(len(Temp_pop_start[0])):
        Variable = 0               #电器使用时间段数
        for i in range(len(User)//2):
            for j in range(len(User[2*i + 1][0])//2):        
                User[2*i+1][0][2*j] = Temp_pop_start[Variable][k]
                User[2*i+1][0][2*j + 1] = Temp_pop_end[Variable][k]
                Variable = Variable + 1
        Cost,Time_slots,Timelist,Individual_cost = calculateCost(User)
        for l in range(len(Individual_cost)):
            Cost_list[l].append(Individual_cost[l])
    return Cost_list
            

if __name__ == '__main__':
    pass
