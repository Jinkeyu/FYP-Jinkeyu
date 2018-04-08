# 0.0 coding:utf-8 0.0
# 交配

import random


def crossover(pop, pc):    #pc crossover probability为交配概率
    for i in range(len(pop)):
        for j in range(len(pop[i]) - 1):
            if(random.random() < pc):
                cpoint = random.randint(0,len(pop[i][0]))     #select random gene period through gene length选出基因长度范围内的随机基因片段（二进制中某一位值）
                temp1 = []
                temp2 = []
                temp1.extend(pop[i][j][0:cpoint])             #exchange the gene with the next one然后将该基因片段和后一个基因片段进行交换
                temp1.extend(pop[i][j+1][cpoint:len(pop[i][j])])
                temp2.extend(pop[i][j+1][0:cpoint])
                temp2.extend(pop[i][j][cpoint:len(pop[i][j])])
                pop[i][j] = temp1
                pop[i][j+1] = temp2

if __name__ == '__main__':
    pass
