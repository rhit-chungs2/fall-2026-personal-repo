classdef MyShape < handle
    %UNTITLED13 Summary of this class goes here
    %   Detailed explanation goes here

    properties
       Patch matlab.graphics.primitive.Patch
    end

    methods
        function obj = MyShape(xCoords, yCoords,color)
            %UNTITLED13 Construct an instance of this class
            %   Detailed explanation goes here
            obj.Patch = patch(xCoords,yCoords,color);
        end

        function move(obj,dx,dy)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            %TODO: Implement a move method
            obj.Patch.XData = obj.Patch.XData + dx;
            obj.Patch.YData = obj.Patch.YData + dy;

        end

    end
end