# 0.0 coding:utf-8 0.0
# 基因突变

import random


def mutation(pop, pm):
    px = len(pop)
    py = len(pop[0])
    
    for i in range(len(pop)):
        for j in range(len(pop[i])):
            mpoint = random.randint(0, len(pop[i][j])-1)
            if(pop[i][j][mpoint] == 1):
                pop[i][j][mpoint] = 0
            else:
                pop[i][j][mpoint] = 1

if __name__ == '__main__':
    pass
