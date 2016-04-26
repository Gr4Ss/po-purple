
local DEBUG = 0;
local BM = 0;
local bmTbl = {};

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
local ipairs = ipairs;
local math = math;
local os = os;
local print = print;
local table = table;

-- Program vars
local width, height = 480, 256;
local getPixel, setPixel;

-- Generate a list of pixels to iterate over
local pixelList1 = {};
--local pixelList2 = {};
--local pixelList3 = {};
--local pixelList4 = {};

do
	--[[local interval = 5;
	local distFromTop = 10;
	local distFromBottom = 20;
	for i = 1, (width / interval) - 1 do
		local x = i * interval;
		local y = math.floor((height - (distFromTop + distFromBottom)) * ((width - x * 2) / width) ^ 4);
		pixelList2[#pixelList2 + 1] = {x, distFromTop + y};
	end;

	for i = 1, (width / interval) - 1 do
		pixelList1[#pixelList1 + 1] = {i * interval, height - distFromBottom};
	end;]]

	local distFromLeft = 5;
	local distFromRight = 5;
	local distFromTop = 15;
	local distFromBottom = 5;
	local interval = 2;

	for i = height - distFromBottom - 1, distFromTop, -interval do
		pixelList1[#pixelList1 + 1] = {distFromLeft, i};
	end;

	for i = distFromLeft + 1, width - distFromRight, interval do
		pixelList2[#pixelList2 + 1] = {i, distFromTop};
	end;

	for i = distFromTop + 1, height - distFromBottom, interval do
		pixelList3[#pixelList3 + 1] = {width - distFromRight, i};
	end;

	for i = width - distFromRight - 1, distFromLeft, -interval do
		pixelList4[#pixelList4 + 1] = {i, height - distFromBottom};
	end;
end;

local function calcDiffs(pixelList, getPixel)
	local previous = pixelList[1];
	local previousLuma = getPixel(previous[1], previous[2]);
	local lumaDiffList = {};
	for i, current in ipairs(pixelList) do
		local luma = getPixel(current[1], current[2]);
		local diff = previousLuma - luma;
		if (diff < -10 or diff > 10) then
			current[3] = diff;
			lumaDiffList[#lumaDiffList + 1] = math.abs(diff);
		end;

		previous = current;
		previousLuma = luma;
	end;

	table.sort(lumaDiffList);

	for i = 1, #lumaDiffList - 1 do
		if (lumaDiffList[i + 1] - lumaDiffList[i] >= 2) then
			if (DEBUG >= 1) then
				print("Threshold:", lumaDiffList[i]);
			end;
			return lumaDiffList[i];
		end;
	end;

	print("No threshold found")
	return 10;
end;

local function getIntersectPoints(pixelList, diffThreshold)
	local pointList = {};
	local inLine;
	for i, current in ipairs(pixelList) do
		if (current[3]) then
			if (current[3] <= -diffThreshold and (not inLine or inLine + (#pixelList / 3) < i)) then
				inLine = i;
				if (DEBUG >= 1) then
					if (DEBUG >= 2) then
						print("Line enter", i);
					end;
					setPixel(current[1], current[2], 128, 255, 255);
					setPixel(current[1] + 1, current[2], 128, 255, 255);
					setPixel(current[1] - 1, current[2], 128, 255, 255);
					setPixel(current[1], current[2] + 1, 128, 255, 255);
					setPixel(current[1], current[2] - 1, 128, 255, 255);
				end;
			elseif (current[3] >= diffThreshold and inLine) then
				if (i - inLine > 1) then
					pointList[#pointList + 1] = {math.floor((pixelList[inLine][1] + current[1]) / 2), math.floor((pixelList[inLine][2] + current[2]) / 2)};
				end;
				inLine = false;
				if (DEBUG >= 1) then
					if (DEBUG >= 2) then
						print("Line exit", i);
					end;
					setPixel(current[1], current[2], 128, 0, 0);
					setPixel(current[1] + 1, current[2], 128, 0, 0);
					setPixel(current[1] - 1, current[2], 128, 0, 0);
					setPixel(current[1], current[2] + 1, 128, 0, 0);
					setPixel(current[1], current[2] - 1, 128, 0, 0);
				end;
			elseif (DEBUG >= 1) then
				setPixel(current[1], current[2], 128, 255, 0);
			end;
		elseif (DEBUG >= 1) then
			setPixel(current[1], current[2], 0, 128, 128);
		end;

		current[3] = false;
	end;

	return pointList;
end;

local function getIntersectPointList(pixelList, getPixel)
	if (BM >= 1) then
		bmTbl.total = os.clock();
	end;

	--[[
		Get diff threshold
	]]
	if (BM >= 1) then
		bmTbl.threshold = os.clock();
	end;

	local diffThreshold = calcDiffs(pixelList, getPixel);

	if (bmTbl.threshold) then
		print("---- Thres time:", os.clock() - bmTbl.threshold);
	end;

	--[[
		Find line points along pixelList
	]]
	if (BM >= 1) then
		bmTbl.points = os.clock();
	end;

	local pointList = getIntersectPoints(pixelList, diffThreshold);

	if (bmTbl.points) then
		print("---- Points time:", os.clock() - bmTbl.points);
	end;

	if (bmTbl.total) then
		print("---- Total time:", os.clock() - bmTbl.total);
	end;

	if (DEBUG >= 1) then
		for k, point in ipairs(pointList) do
			print("Point:", point[1], point[2])
			setPixel(point[1], point[2], 128, 0, 255);
			setPixel(point[1] + 1, point[2], 128, 0, 255);
			setPixel(point[1] - 1, point[2], 128, 0, 255);
			setPixel(point[1], point[2] + 1, 128, 0, 255);
			setPixel(point[1], point[2] - 1, 128, 0, 255);
		end;
	end;
end;

function getAllIntersectPoints()
	local image = libjpeg.load(loadTable);
	local getPxl, setPxl = bitmap.pixel_interface(image);
	if (DEBUG >= 1) then
		getPixel, setPixel = getPxl, setPxl;
	end;

	local returnTable = {};
	returnTable[1] = getIntersectPointList(pixelList1, getPxl);
	returnTable[2] = getIntersectPointList(pixelList2, getPxl);
	returnTable[3] = getIntersectPointList(pixelList3, getPxl);
	returnTable[4] = getIntersectPointList(pixelList4, getPxl);

	return returnTable;
end;

if (bmTbl.setup) then
	print("---- Setup time:", os.clock() - bmTbl.setup);
end;


--[[
	TEST STUFF
]]
--[[DEBUG
local amount = tonumber(arg[2]) or 1;
if (amount ~= 1) then
	DEBUG = 0;
	BM = 0;
end;
local loadTable = {path = arg[1]};

local bmStart = os.clock();
for i = 1, amount do
	if (BM >= 1) then
		bmTbl.funcs = os.clock();
	end;

	local image = libjpeg.load(loadTable);
	local getPxl, setPxl = bitmap.pixel_interface(image);
	if (DEBUG >= 1) then
		getPixel, setPixel = getPxl, setPxl;
	end;

	if (bmTbl.funcs) then
		print("---- Funcs time:", os.clock() - bmTbl.funcs);
	end;

	local returnTable = {};
	returnTable[1] = getIntersectPointList(pixelList1, getPxl);
	returnTable[2] = getIntersectPointList(pixelList2, getPxl);
	returnTable[3] = getIntersectPointList(pixelList3, getPxl);
	returnTable[4] = getIntersectPointList(pixelList4, getPxl);

	if (DEBUG >= 1) then
		libjpeg.save({bitmap = image, path = "test.jpg"});
	end;
end;
print("-----------------------")
print("Amount of runs:", amount);
print("Average time:", (os.clock() - bmStart) / amount);
--]]
