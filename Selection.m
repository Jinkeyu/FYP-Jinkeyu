function newPops = Selection(pops,score)
num = length(pops);  % ���볤��
score = max(score) - score + 0.01;  %�Ŵ��㷨����Ŀ�꺯�������ֵ����������������Сֵ����� �����ֵ��ȥscore��ת��Ϊ����Сֵ���⣬��0��01����ֹ����0��

sumScore = sum(score);  % ���ܷ���
score = score/sumScore; % ����ÿһ�����屻ѡ�еĸ���
P = cumsum(score);  % �����ۼƸ���

newPops = {};
for i = 1:num
    P1 = P;
    P1 = P1 - rand; % �ҵ���ѡ�еĸ�����
    newPops{i} = pops{find(P1>0,1)}; % ѡ���ø���
end
    