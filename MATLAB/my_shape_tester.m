clear
clc
close all


xlim([0 10])
ylim([0 10])

tri = MyShape([1,3,5],[1,4,1],'r');

rect = MyShape([6,9,9,6],[1,1,3,3],'r');

pause(1);

tri.move(0,3);

pause(1);

rect.move(-1,1);

fprintf("done!");