function [cost,Electricity,eachHoursCost] = CalCost(popTemp,UsersTemp)
%��������ֵ
% cost �����û�һ��ķ���
% Electricity  ÿ���û���ÿ��Сʱ�õ���
% eachHoursCost ÿ��Сʱ�����û��ܵĻ���
Electricity = zeros(length(UsersTemp),24);
idx = 0;%����Ļ������λ��  1��15
for i = 1:length(UsersTemp)
    for j = 1:length(UsersTemp{i}.TimeDuration)
        idx = idx +1;  
        InitialTime = popTemp(idx);   % ÿ���õ�����ʼ������ʱ��   
        TimeDurationTemp = UsersTemp{i}.TimeDuration{j} + InitialTime;   % ���õ���������ʱ��� = ��ʼ����ʱ�� + ����ʱ��
        for eachTime = InitialTime : (InitialTime+ ceil(UsersTemp{i}.TimeDuration{j})-1)  
            if (TimeDurationTemp - eachTime)>=1 % ��ʱ��ι�����һ����Сʱ
                workTime = 1;
            elseif (TimeDurationTemp - eachTime)<0   % ��ʱ���û�й���
                workTime = 0;
            else
                workTime = TimeDurationTemp - eachTime;   % ��ʱ��ι����� ��㼸��Сʱ��pdf�а��Сʱ��
            end
            Electricity(i,eachTime+1) = Electricity(i,eachTime+1)+workTime*UsersTemp{i}.Power{j};  %ͳ��ÿ��Сʱ���õ���
        end
    end
end
% �û����е��õ���
ElecTot = sum(Electricity);
% ��ۺ���
f = @(x)0.06*x.^2;
% ÿ��Сʱ�����û��ܵĻ���
eachHoursCost = f(ElecTot);
% һ�������û��ĵ��
cost = sum(eachHoursCost);

