
local func = require("linerecog");

local count = 0;
local function getDistance()
	count = count + 1;
	return 2 * count;
end;

local function startCommand(command, arg)
	print(command:upper(), arg);
end;

local function stopCommand()
	print("STOP COMMAND")
end;

local function driveDistance(distance)
	print("Distance ", distance)
end;

local function turnAngle(angle)
	print("Angle", angle / math.pi * 180)
end;

for i = 1, 5 do
	func("l1", getDistance, startCommand, stopCommand, driveDistance, turnAngle);
end;