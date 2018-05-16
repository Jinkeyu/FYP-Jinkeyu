clear
clc
close all

% ------------------ initialise the users and its data information ��ʼ���û�����,ȫ����Users�������棬��ν�����ݽṹ��data structure
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

% Time viration constraints 2 hours ʱ��䶯�����ƣ���2Сʱ�ڲ���
hoursLimitation = 2;

%----------------- genetic algorithm settings �Ŵ��㷨��������
% population ��Ⱥ����
numPop = 50;
%iteration times ��������
numGen = 200;
% probability of crossover �������
pc = 0.3;
% probability of mutation �������
pm = 0.1;

% ��ʼ��ÿ������
% 3 users, each one has five appliances so the encoding is 15.�Ŵ��㷨���룬һ��3���û���ÿ���û�5���õ�������˱���Ϊ15λ��ÿһλ�����ʾ���õ����Ǵ�ʲôʱ��ʼ����
% ���磬����PDF�и��ĳ�ʼʱ�䣬����Ӧ���� 
% [ 1 7 18 20 18    1 17 18 21 17   18 18 19 19 17]
pops = {};
lowTimes = [];
upTimes = [];
for ii = 1:numPop
    popTemp = [];
    idx=0; % ����λ����   1��15
    lowTimes = [];
    upTimes = [];
    for i = 1:length(Users)
        for j = 1:length(Users{i}.InitialTime)
            idx = idx +1;
            % ѭ���õ�ÿ���õ�������PDF���趨�ĳ�ʼʱ�䣬�Լ�����ʱ��
            % low up ��ʾ���õ��� ��ʼ����ʱ�� �仯��Χ
            [low,up] = TimeInterval(Users{i}.InitialTime{j},hoursLimitation,Users{i}.TimeDuration{j});
            lowTimes(idx) = low;
            upTimes(idx) = up;
            % �ڱ仯��Χ���������һ��ʱ�䣬��ʾ���õ�����ʱ��
            popTemp(idx) = randi(up-low+1) + low-1;
        end
    end
    pops{ii} = popTemp;
end


gen =0;   % ��������
eachUserCost = zeros(gen,length(Users));  %total cost of each user ÿ���û���һ���ܵĻ���
% evolution ��ʼ����
while(gen<numGen)
    gen = gen+1;
    % calculate cost
    Electricity ={};

    for i = 1:numPop
        % ����ÿ�����壬�����û�һ��ķ���
        [cost(i),Electricity{i},eachHoursCost{i}] = CalCost(pops{i},Users);
        ElectricityTemp = Electricity{i};
        eachHoursElectricityTotal = sum(ElectricityTemp);
        % ����ÿ���û����Գе��ķ���
        for jj = 1:length(Users)
            % scale of cost �������
            partion= ElectricityTemp(jj,:)./(eachHoursElectricityTotal);
            partion(isnan(partion)) =0;
            % ���������ܷ���
            eachUsersCost{i,jj} = sum(partion.* eachHoursCost{i});
        end
    end
    
    % �ҵ�������͵ĸ��壬��������
    [val,index] = min(cost);
    bestIndividual{gen} = pops{index};
    lowestCost(gen) = val;
    % �÷�����͵ĸ��壬ÿ���û����
    for jj= 1:length(Users)
        eachUserCost(gen,jj) = eachUsersCost{index,jj};
    end
    fprintf('genaration %d:  lowestCost is %f\n',gen,val);
    
    
    % �Ŵ��㷨 ѡ�����
    newPop = Selection(pops,cost);
    
    % �Ų��㷨 �������
    for i = 1:2:numPop
        [newPop{i},newPop{i+1}] = CrossOver(newPop{i},newPop{i+1},pc);
    end
    
    % �Ŵ��㷨 �������
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




