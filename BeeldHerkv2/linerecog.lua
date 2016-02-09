local DEBUG = 1;
local BM = 1;
local bmTbl = {};

if (BM >= 1) then
	bmTbl.total = os.clock();
end;

--[[
	Load in basic things
]]
if (BM >= 1) then
	bmTbl.setup = os.clock();
end;

-- Add the ./lua/ folder to the list of paths
package.path = "lua/?.lua;lualib/?.lua;"..package.path;

-- Load in the libs, store them as locals for fast access
local require = require;
local bitmap = require("bitmap");
local libjpeg = require("libjpeg");

-- Localize global libraries
local math = math;
local os = os;
local print = print;
local table = table;

local pixelList = {};
local interval = 4;
local width = 480;
local height = 250;
local distFromTop = 10;
local distFromBottom = 20;
for i = 1, (width - interval) / interval do
	local x = i * interval;
	pixelList[#pixelList + 1] = {x, distFromTop + math.floor((height - (distFromTop + distFromBottom)) * ((width - x * 2) / width) ^ 4)};
end;

if (bmTbl.setup) then
	print("Setup time:", os.clock() - bmTbl.setup);
end;

--[[
	Load in the image
]]
if (BM >= 1) then
	bmTbl.load = os.clock();
end;

local image = libjpeg.load({path = "picture_12.jpg"});
local getPixel, setPixel = bitmap.pixel_interface(image);
local width = image.w - 1;
local height = image.h - 1;

if (bmTbl.load) then
	print("Load time:", os.clock() - bmTbl.load);
end;

--[[
	Get deltas over pixelList
]]
if (BM >= 1) then
	bmTbl.deltas = os.clock();
end;

local deltaList = {};
local previous = pixelList[1];
local previousLuma = getPixel(previous[1], previous[2]);
for i, current in ipairs(pixelList) do
	local luma = getPixel(current[1], current[2]);
	if (DEBUG >= 2) then
		print(i * 2, previousLuma - luma);
	end;

	deltaList[#deltaList + 1] = {math.abs(previousLuma - luma)};
	--[[if (math.abs(previousLuma - luma) > 15) then
		setPixel(current[1], current[2], 128, 255, 255);
		setPixel(current[1] + 1, current[2], 128, 255, 255);
		setPixel(current[1] - 1, current[2], 128, 255, 255);
		setPixel(current[1], current[2] + 1, 128, 255, 255);
		setPixel(current[1], current[2] - 1, 128, 255, 255);
	else
		setPixel(current[1], current[2], 128, 0, 0);
	end;]]

	previous = current;
	previousLuma = luma;
end;

table.sort(deltaList, function(a, b)
	return a[1] < b[1];
end);
for k, v in ipairs(deltaList) do
	local a = k + 1;
	--print(v);
end;

if (bmTbl.deltas) then
	print("Delta time:", os.clock() - bmTbl.deltas);
end;

if (bmTbl.total) then
	print("Total time:", os.clock() - bmTbl.total);
end;

if (DEBUG >= 1) then
	libjpeg.save({bitmap = image, path = "test.jpg"});
end;