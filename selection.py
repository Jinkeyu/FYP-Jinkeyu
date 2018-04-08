# 0.0 coding:utf-8 0.0
# 选择

import random


def sum(Fit_value):
	total = 0
	for i in range(len(Fit_value)):
		total += Fit_value[i]
	return total


def cumsum(Fit_value):
	for i in range(len(Fit_value)):
		for j in range(len(Fit_value[i])-2, -1, -1):
			t = 0
			k = 0
			while(k <= j):
				t += Fit_value[i][k]
				k += 1
			Fit_value[i][j] = t
			Fit_value[i][len(Fit_value[i])-1] = 1   #计算累计概率，就是1,2,3,...,n个个体加起来的概率和

def selection(Pop, Fit_value):   #fit_value 为费用表
	Newfit_value = []
	# 适应度总和
	total_fit = []
	for i in range(len(Fit_value)):
		total_fit.append(sum(Fit_value[i]))      #calculate the sum of fitness list计算适应度总和列表
	for i in range(len(Fit_value)):
		Newfit_value.append([])
		for j in range(len(Fit_value[i])):
			Newfit_value[i].append(Fit_value[i][j] / total_fit[i])  
			
	# 计算累计概率
	cumsum(Newfit_value)
	
	#获得进行轮盘赌算法的概率值
	ms = []
	for i in range(len(Pop)):
		ms.append([])
		for j in range(len(Pop[i])):
			ms[i].append(random.random())    
			
	for i in range(len(ms)):
		ms[i].sort()
	
	fitin = 0
	newin = 0
	newpop = Pop
	# 转轮盘选择法
	# 使用轮盘赌算法生成新的种群
	for i in range(len(Pop)):
		while newin < len(Pop[i]):
			if(ms[i][newin] < Newfit_value[i][fitin]):    
				newpop[i][newin] = Pop[i][fitin]
				newin = newin + 1
			else:
				fitin = fitin + 1
	Pop = newpop
	

if __name__ == '__main__':
    pass
