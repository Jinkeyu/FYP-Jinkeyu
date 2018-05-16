clear
clc
close all

% ------------------ initialise the users and its data information 初始化用户数据,全都在Users变量里面，所谓的数据结构，data structure
Users = {};
Users{1}.Appliance = {'Refrigerator','Electric cooker','Air-condition','Television','Washing machine',};
Users{1}.Power = {0.15,0.5,1.5,0.2,0.4};
Users{1}.TimeDuration={23,0.5,3,2,2,};
Users{1}.InitialTime = {1,7,18,20,18};

Users{2}.Appliance = {'Refrigerator','Electric cooker','Air-conditioner','Laptop','Electric heat showers'};
Users{2}.Power = {0.15,0.5,1.5,0.2,0.4};
Users{2}.TimeDuration ={23,0.5,5,2,1};
Users{2}.InitialTime = {1,17,18,21,17};

Users{3}.Appliance = {'Hair dryer','Microwave-oven','Air-condition','Laptop','Electric'};
Users{3}.Power = {0.45,1,1.5,0.2,0.4};
Users{3}.TimeDuration ={0.5,0.5,4,4,1};
Users{3}.InitialTime = {18,18,19,19,17};

% Time viration constraints 2 hours 时间变动的限制，在2小时内波动
hoursLimitation = 2;

%----------------- genetic algorithm settings 遗传算法参数设置
% population 种群个数
numPop = 50;
%iteration times 进化代数
numGen = 200;
% probability of crossover 交叉概率
pc = 0.3;
% probability of mutation 变异概率
pm = 0.1;

% 初始化每个个体
% 3 users, each one has five appliances so the encoding is 15.遗传算法编码，一共3个用户，每个用户5个用电器，因此编码为15位，每一位编码表示该用电器是从什么时候开始工作
% 例如，按照PDF中给的初始时间，编码应该是 
% [ 1 7 18 20 18    1 17 18 21 17   18 18 19 19 17]
pops = {};
lowTimes = [];
upTimes = [];
for ii = 1:numPop
    popTemp = [];
    idx=0; % 编码位数，   1到15
    lowTimes = [];
    upTimes = [];
    for i = 1:length(Users)
        for j = 1:length(Users{i}.InitialTime)
            idx = idx +1;
            % 循环得到每个用电器，在PDF中设定的初始时间，以及工作时长
            % low up 表示该用电器 初始工作时间 变化范围
            [low,up] = TimeInterval(Users{i}.InitialTime{j},hoursLimitation,Users{i}.TimeDuration{j});
            lowTimes(idx) = low;
            upTimes(idx) = up;
            % 在变化范围内随机生成一个时间，表示该用电器的时间
            popTemp(idx) = randi(up-low+1) + low-1;
        end
    end
    pops{ii} = popTemp;
end


gen =0;   % 进化代数
eachUserCost = zeros(gen,length(Users));  %total cost of each user 每个用户的一天总的花费
% evolution 开始进化
while(gen<numGen)
    gen = gen+1;
    % calculate cost
    Electricity ={};

    for i = 1:numPop
        % 计算每个个体，所有用户一天的费用
        [cost(i),Electricity{i},eachHoursCost{i}] = CalCost(pops{i},Users);
        ElectricityTemp = Electricity{i};
        eachHoursElectricityTotal = sum(ElectricityTemp);
        % 计算每个用户各自承担的费用
        for jj = 1:length(Users)
            % scale of cost 计算比例
            partion= ElectricityTemp(jj,:)./(eachHoursElectricityTotal);
            partion(isnan(partion)) =0;
            % 比例乘以总费用
            eachUsersCost{i,jj} = sum(partion.* eachHoursCost{i});
        end
    end
    
    % 找到费用最低的个体，保留下来
    [val,index] = min(cost);
    bestIndividual{gen} = pops{index};
    lowestCost(gen) = val;
    % 该费用最低的个体，每个用户电费
    for jj= 1:length(Users)
        eachUserCost(gen,jj) = eachUsersCost{index,jj};
    end
    fprintf('genaration %d:  lowestCost is %f\n',gen,val);
    
    
    % 遗传算法 选择操作
    newPop = Selection(pops,cost);
    
    % 遗产算法 交叉操作
    for i = 1:2:numPop
        [newPop{i},newPop{i+1}] = CrossOver(newPop{i},newPop{i+1},pc);
    end
    
    % 遗传算法 变异操作
    for i = 1:numPop
        newPop{i} = Mutate(newPop{i},pm,lowTimes,upTimes);
    end
    
    newPop{1} = pops{index};
    pops = newPop;
end

figure
plot(lowestCost,'linewidth',2)
xlabel('generation')
ylabel('cost');
title('Total Cost Of all Users')

figure
subplot(3,1,1)
plot(eachUserCost(:,1),'linewidth',2);
xlabel('generation')
ylabel('cost')
title('Each User''s Cost');
subplot(3,1,2)
plot(eachUserCost(:,2),'linewidth',2);
ylabel('cost')
subplot(3,1,3)
plot(eachUserCost(:,3),'linewidth',2);
ylabel('cost')

best = bestIndividual{end};
idx =0;
for i = 1:length(Users)
    fprintf('\nUser :%d\n',i)
    for j = 1:length(Users{i}.Appliance)
        idx = idx +1;
        fprintf('%s''s Initial time is %d\n',Users{i}.Appliance{j},best(idx));
    end
end




