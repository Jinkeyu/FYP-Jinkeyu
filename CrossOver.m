function [popTemp1,popTemp2] = CrossOver(popTemp1,popTemp2,pc)  %Two individuals temp1 temp2
if rand<pc
    point = randi(length(popTemp1));  %generate a random value, the point where goes crossover and mutation 
    Temp = popTemp2(point:end);
    popTemp2 = [popTemp2(1:point-1),popTemp1(point:end)];
    popTemp1 = [popTemp1(1:point-1),Temp];
end