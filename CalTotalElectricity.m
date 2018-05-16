function totalElectricity = CalTotalElectricity(Users)
to = 0;
for i = 1:length(Users)
    for j = 1:length(Users{i}.TimeDuration)
        Users{i}.TimeDuration{j} * Users{i}.Power{j};
        to = to + Users{i}.TimeDuration{j} * Users{i}.Power{j};
    end
end
totalElectricity = to;