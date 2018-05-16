function newPops = Selection(pops,score)
num = length(pops);  % 编码长度
score = max(score) - score + 0.01;  %遗传算法是求目标函数的最大值，我们问题是求最小值，因此 用最大值减去score，转化为求最小值问题，加0。01，防止出现0分

sumScore = sum(score);  % 求总分数
score = score/sumScore; % 计算每一个个体被选中的概率
P = cumsum(score);  % 计算累计概率

newPops = {};
for i = 1:num
    P1 = P;
    P1 = P1 - rand; % 找到被选中的个体编号
    newPops{i} = pops{find(P1>0,1)}; % 选出该个体
end
    