local bmSetup = os.clock()
--[[
	LOAD LIBRARIES
]]
-- Add the ./lua/ folder to the list of paths
package.path = "lua/?.lua;lualib/?.lua;"..package.path;

-- Load in the libs, store them as locals for fast access
local require = require;
local bitmap = require("bitmap");
local libjpeg = require("libjpeg");

-- Load in the lua code
util = require("util");
local util = util;
local preprocess = require("preprocess");
local graph = require("graph");
local postprocess = require("postprocess");

--[[
	LOCALIZE GLOBALS
]]
local osClock = os.clock;
local print = print;
local tableSort = table.sort;

--[[
	DEFINE VARS
]]
-- Change to your liking
local DEBUG = true; 		-- Do debug prints/paints/etc.
local image = arg[1] or "picture_0";	-- Name of the picture to load in
print("Setup:       ", osClock() - bmSetup);

--[[
	Load in the image, set up some image-related variables
]]
local bmLoad = osClock();

local image = libjpeg.load({path = image..".jpg"});
local getPixel, setPixel = bitmap.pixel_interface(image);
local width = image.w - 1;
local height = image.h - 1;

print("Loading:     ", osClock() - bmLoad);

print("--- PREPROCESS ---");
--[[
	Calculate the min luma value to compensate for different lightning
]]
local bmCalcBlackWhite = osClock();
local minLuma = preprocess.getMinLuma(getPixel, width, height);
print("Calc B-W:    ", osClock() - bmCalcBlackWhite);

--[[
	Turn the image into black/white
]]
local bmBlackWhite = osClock();
local firstWhite, lastWhite, lowestWhite = preprocess.makeBlackWhite(getPixel, setPixel, width, height, minLuma);
print("Black-white: ", osClock() - bmBlackWhite);

--[[DEBUG
if (DEBUG) then
	libjpeg.save({bitmap = image, path = "testBW.jpg"});
end;
--]]

--[[
	Remove noise
]]
local bmNoise = osClock();
preprocess.reduceNoise(getPixel, setPixel, width, height, firstWhite, lastWhite, lowestWhite);
print("Noise:       ", osClock() - bmNoise);
print("Preprocess:  ", osClock() - bmCalcBlackWhite);

--[[DEBUG
if (DEBUG) then
	libjpeg.save({bitmap = image, path = "testNoise.jpg"});
end;
--]]

print("--- GRAPH ---");
--[[
	Find all white pixels adjacent to black pixels
	and turn them into nodes.
]]
local bmGraph = osClock();
local nodeList, nodes = graph.getNodes(getPixel, width, height, firstWhite, lastWhite, lowestWhite);
print("Nodes:       ", osClock() - bmGraph);

--[[
	Sort the nodes based on the sortNodes
]]
local bmSort = osClock();
tableSort(nodeList, util.sortNodes);
print("Sort Nodes:        ", osClock() - bmSort);

--[[
	Generate the edges for all the nodes
]]
local bmEdges = osClock();
graph.createEdges(nodeList, nodes);
graph.cleanUpEdges(nodeList, nodes);
print("Edges:       ", osClock() - bmEdges);

--[[
	Group (in)directly linked nodes together
]]
local bmGrouping = osClock();
local groups = graph.createGroups(nodeList, nodes);
print("Grouping:    ", osClock() - bmGrouping);
print("Graph:       ", osClock() - bmGraph);

print("--- POSTPROCESS ---");
--[[
	Reduce the number of nodes in a group
	Uses the Ramer-Douglas-Peucker algorithm
]]
local bmRDP = osClock();
postprocess.RDP(groups);
print("RDP:         ", osClock() - bmRDP);

--[[
	Link groups together if their end/start are near each other.
]]
local bmLink = osClock();
postprocess.linkGroups(groups);
print("Linking:     ", osClock() - bmLink);

--[[
	Create real points from the remaining nodes
]]
local bmReal = osClock();
local realNodes = postprocess.transformToRealNodes(groups, width, height);
print("Real Nodes:  ", osClock() - bmReal);

--[[
	Merge points at intersections together
]]
local bmMerge = osClock();
postprocess.mergeRealNodes(realNodes);
print("Merge Nodes: ", osClock() - bmMerge);
print("Postprocess: ", osClock() - bmRDP);

print("--- TOTAL ---");
print("Total:       ", osClock() - bmSetup);

--[[
	Debug prints
]]
if (DEBUG) then
	libjpeg.save({bitmap = image, path = "test.jpg"});

	--[[DEBUG: real coordinates
	for k, v in ipairs(realNodes) do
		print(v[1], v[2], #v[3]);
		for k, v1 in pairs(v[3]) do
			print("    "..k, v1[1], v1[2])
		end;
	end;
	--]]

	print("----------------------");
	print("Real points: ", #realNodes);
	print("Total nodes: ", #nodeList);
	print("Total groups: ", #groups);
	print("----------------------");

	print("Percentage skipped: ", 
		((firstWhite + width - lastWhite) * (height - lowestWhite) + width * lowestWhite) / (width * height));
	print("----------------------");

	tableSort(groups, function(a, b)
		return a[1] > b[1];
	end);

	local points = 0;
	for k, v in pairs(groups) do
		print("Group: ", k);
		print("Start: ", v[2][1], v[2][2]);
		print("End:   ", v[3][1], v[3][2]);
		print("Nodes: ", v[1]);
		print("----------------------");
		points = points + v[1];
	end;
end;