# 0.0 coding:utf-8 0.0
import random


def geneEncoding(Species_size , Pop_size, Chrom_length):
    Pop = []           #二维列表,第一维存储单个物种种群，第二维存储每个种群的所有个体，第三维存储每个个体的所有DNA
    for i in range(Species_size):
	    Pop.append([])   #建立新的物种种群
	    for j in range(Pop_size):
		    Temp = []
		    for k in range(Chrom_length):
			    Temp.append(random.randint(0, 1))
		    Pop[i].append(Temp)

    return Pop

#这一段是用来进行测试的代码，当执行这个文件的时候，下面的程序就会被执行
#if __name__ == '__main__':
    #Species_size = 6
    #Pop_size = 50		# 种群数量
    #Chrom_length = 10		# 染色体长度
    #Pop = geneEncoding(Interation,Pop_size, Chrom_length)
    #print Pop
    #print len(Pop)
