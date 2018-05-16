function [cost,Electricity,eachHoursCost] = CalCost(popTemp,UsersTemp)
%函数返回值
% cost 所有用户一天的费用
% Electricity  每个用户，每个小时用电量
% eachHoursCost 每个小时所有用户总的花费
Electricity = zeros(length(UsersTemp),24);
idx = 0;%个体的基因编码位数  1到15
for i = 1:length(UsersTemp)
    for j = 1:length(UsersTemp{i}.TimeDuration)
        idx = idx +1;  
        InitialTime = popTemp(idx);   % 每个用电器开始工作的时间   
        TimeDurationTemp = UsersTemp{i}.TimeDuration{j} + InitialTime;   % 该用电器工作的时间段 = 开始工作时间 + 工作时长
        for eachTime = InitialTime : (InitialTime+ ceil(UsersTemp{i}.TimeDuration{j})-1)  
            if (TimeDurationTemp - eachTime)>=1 % 该时间段工作了一整个小时
                workTime = 1;
            elseif (TimeDurationTemp - eachTime)<0   % 该时间段没有工作
                workTime = 0;
            else
                workTime = TimeDurationTemp - eachTime;   % 该时间段工作了 零点几个小时（pdf中半个小时）
            end
            Electricity(i,eachTime+1) = Electricity(i,eachTime+1)+workTime*UsersTemp{i}.Power{j};  %统计每个小时的用电量
        end
    end
end
% 用户所有的用电量
ElecTot = sum(Electricity);
% 电价函数
f = @(x)0.06*x.^2;
% 每个小时所有用户总的花费
eachHoursCost = f(ElecTot);
% 一天所有用户的电费
cost = sum(eachHoursCost);

