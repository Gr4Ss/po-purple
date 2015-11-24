
local postprocess = {};

local util = util;

local mathAbs = math.abs;
local mathAcos = math.acos;
local mathPi = math.pi;
local mathSqrt = math.sqrt;
local tableRemove = table.remove;
local tableSort = table.sort;

local function getEpsilon(y)
	return math.max(9, (400 - 9) / (400 - 10) * y - 110);
end;

-- Removes points from the group by approximating the group by a similar one with fewer points
-- https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
local function ramerDouglasPeucker(startNode, endNode)
	local max = 0;
	local currentNode = startNode[3][#startNode[3]];
	local distance, node;

	local counter = 0
	while (currentNode ~= endNode) do
		distance = util.distancePointLineToSqr(currentNode, startNode, endNode);
		if (distance > max) then
			max = distance;
			node = currentNode;
		end;
		currentNode = currentNode[3][2]
	end;

	if (node and max > getEpsilon(node[2])) then
		ramerDouglasPeucker(startNode, node);
		ramerDouglasPeucker(node, endNode);
	else
		if (endNode[3][1] ~= startNode) then
			--tableRemove(endNode[3][1][3], 2);
			--tableRemove(startNode[3][#startNode[3]][3], 1);
			--deleteNode(endNode[3][1])

			startNode[3][#startNode[3]] = endNode;
			endNode[3][1] = startNode;
		end;
	end;
end;
postprocess.ramerDouglasPeucker = ramerDouglasPeucker;

function postprocess.RDP(groups)
	for i = 1, #groups do
		ramerDouglasPeucker(groups[i][2], groups[i][3]);
	end;
end;

-- Recursively inverts the order in which nodes are linked
-- Index can be used to ensure the list is traversed in the right direction
local function changeOrder(node, index)
	if (#node[3] == 1) then
		return;
	end;

	node[3][1], node[3][2] = node[3][2], node[3][1];
	return changeOrder(node[3][index], index);
end;

-- Searches for groups that have endpoints close together
-- and merges them into one big group.
-- Runs RDP on merged groups to ensure there are no excessive points
function postprocess.linkGroups(groups)
	local RDP, remove, i;
	for groupNumber, group in ipairs(groups) do
		RDP = false;
		i = #groups;
		while i >= groupNumber + 1 do
			remove = false;
			for j = 2, 3 do
				if (util.distanceToSqr(group[j], groups[i][2]) <= 6 * 6) then
					local oldEnd = group[j];
					local nextNode = groups[i][2][3][1];
					if (j == 2) then
						changeOrder(nextNode, 1);
						oldEnd[3][1], oldEnd[3][2] = nextNode, oldEnd[3][1];
						nextNode[3][2] = group[j];
					else
						oldEnd[3][2] = nextNode;
						nextNode[3][1] = oldEnd;
					end;

					-- Update group start/end
					group[j] = groups[i][3];

					RDP, remove = true, true;
					break;
				end;
				if (util.distanceToSqr(group[j], groups[i][3]) <= 6 * 6) then
					local oldEnd = group[j];
					local nextNode = groups[i][3][3][1];
					if (j == 3) then
						changeOrder(nextNode, 2);
						oldEnd[3][2] = nextNode;
						nextNode[3][1] = oldEnd;
					else
						oldEnd[3][1], oldEnd[3][2] = nextNode, oldEnd[3][1];
						nextNode[3][2] = oldEnd;
					end;

					-- Update group start/end
					group[j] = groups[i][2];


					RDP, remove = true, true;
					break;
				end;
			end;

			if (remove) then
				group[1] = group[1] + groups[i][1] - 1;
				tableRemove(groups, i);
				i = #groups;
			else
				i = i - 1;
			end;
		end;

		if (RDP) then
			postprocess.ramerDouglasPeucker(group[2], group[3]);
		end;
	end;
end;

-- Transforms the list of nodes on the picture to a list of nodes
-- with X and Y coordinates in relation to the robot.
function postprocess.transformToRealNodes(groups, width, height)
	local realNodes = {};
	local pictureToRealNode = {};
	for i = 1, #groups do
		local realX = util.pixelXToReal(groups[i][2][1], groups[i][2][2], width, height);
		local realY = util.pixelYToReal(groups[i][2][2], height);
		realNodes[#realNodes + 1] = {realX, realY, {nil, nil}, groups[i][2]};
		pictureToRealNode[groups[i][2]] = realNodes[#realNodes];

		local currentNode = groups[i][2][3][1];
		while (currentNode) do
			realX = util.pixelXToReal(currentNode[1], currentNode[2], width, height);
			realY = util.pixelYToReal(currentNode[2], height);
			realNodes[#realNodes + 1] = {realX, realY, {nil, nil}, currentNode};
			pictureToRealNode[currentNode] = realNodes[#realNodes];

			currentNode = currentNode[3][2];
		end;
	end;

	for i = 1, #realNodes do
		for j = 1, #realNodes[i][4][3] do
			realNodes[i][3][#realNodes[i][3] + 1] = pictureToRealNode[realNodes[i][4][3][j]];
		end;
	end;

	return realNodes;
end;

-- Merges real nodes together if they are within 3cm of each other,
-- updating the links as well.
-- Also checks for nodes that are close to lines between two other nodes.
-- If there are any, it removes the line.
-- In the end this results in a graph where the nodes are intersections and lines are roads.
-- The roads are sorted counterclockwise to help find a left or right turn.
function postprocess.mergeRealNodes(realNodes)
	-- First merge nodes together
	for i = 1, #realNodes do
		for j = #realNodes, i + 1, -1 do
			if (util.distanceToSqr(realNodes[i], realNodes[j]) < 3 * 3) then
				realNodes[i][1] = (realNodes[i][1] + realNodes[j][1]) / 2;
				realNodes[i][2] = (realNodes[i][2] + realNodes[j][2]) / 2;

				local done = {};
				local toDelete;
				for k, v in pairs(realNodes[i][3]) do
					if (v == realNodes[j]) then
						toDelete = k;
					end;
					done[v] = true;
				end;
				if (toDelete) then
					tableRemove(realNodes[i][3], toDelete);
				end;

				local toDelete = {};
				for k, v in pairs(realNodes[j][3]) do
					if (not done[v] and v ~= realNodes[i]) then
						done[v] = true;
						realNodes[i][3][#realNodes[i][3] + 1] = v;
						for k1, v1 in pairs(v[3]) do
							if (v1 == realNodes[j]) then
								v[3][k1] = realNodes[i];
								break;
							end;
						end;
					else
						for k1, v1 in pairs(v[3]) do
							if (v1 == realNodes[j]) then
								tableRemove(v[3], k1);
								break;
							end;
						end;
					end;
				end;

				tableRemove(realNodes, j);
			end;
		end; 
	end;

	local x, y, x1, y1, len1, x2, y2, len2, list;
	for i = 1, #realNodes do
		if (#realNodes[i][3] > 2) then
			x, y = realNodes[i][1], realNodes[i][2];
			x1, y1 = realNodes[i][3][1][1] - x, realNodes[i][3][1][2] - x;
			len1 = x1 * x1 + y1 * y1;

			list = {{0, realNodes[i][3][1], len1}};
			for j = 2, #realNodes[i][3] do
				x2, y2 = realNodes[i][3][j][1] - x, realNodes[i][3][j][2] - y;
				len2 = x2 * x2 + y2 * y2; 

				list[#list + 1] = {
					(util.sign(x1 * y2 - x2 * y1) * mathAcos((x1 * x2 + y1 * y2) / mathSqrt(len1 * len2))) % (mathPi * 2),
					realNodes[i][3][j],
					len2
				};
			end;

			tableSort(list, util.sortAngles);

			local toRemove = {};
			for j = 1, #list do
				realNodes[i][3][j] = list[j][2];
				local previous = j - 1;
				if (previous == 0) then
					previous = #list;
				end;
				if (mathAbs(list[j][1] - list[previous][1]) < 0.35) then
					if (list[j][3] > list[previous][3]) then
						local dist, bx, by = util.distancePointLineToSqr(list[previous][2], realNodes[i], list[j][2]);
						if (dist < 2 * 2) then
							list[previous][2][1] = bx;
							list[previous][2][2] = by;
							toRemove[#toRemove + 1] = j;
						end;
					else
						local dist, bx, by = util.distancePointLineToSqr(list[j][2], realNodes[i], list[previous][2]);
						if (dist < 2 * 2) then
							list[j][2][1] = bx;
							list[j][2][2] = by;
							toRemove[#toRemove + 1] = previous;
						end;
					end;
				end;
			end;

			-- TODO: ensure edge update happens properly in case nodes aren't linked triangularly
			for j = #toRemove, 1, -1 do
				util.deleteEdge(realNodes[i], realNodes[i][3][toRemove[j]]);
			end;
		end;
	end;
end;

return postprocess;