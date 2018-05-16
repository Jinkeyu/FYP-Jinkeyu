function [low,up] = TimeInterval(time,hours,TimeDuration)
low = time-hours;
if(low<0)
    low = 0;
end
up = time +hours;
if(up>24-ceil(TimeDuration))
    up = 24-ceil(TimeDuration);
end
