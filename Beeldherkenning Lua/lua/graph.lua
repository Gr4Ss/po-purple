
local graph = {};

local util = util;

-- Make nodes for all pixels that are orthogonally or diagonally next to a black pixel
function graph.getNodes(getPixel, width, height, firstWhite, lastWhite, lowestWhite)
	local count = 0;
	local nodeList = {};
	local nodePositions = {};

	for x = firstWhite, lastWhite do
		for y = lowestWhite, height do
			if (getPixel(x, y) == 255) then
				if ((x + 1 < width and getPixel(x + 1, y) == 0)
						or (x - 1 > 0 and getPixel(x - 1, y) == 0)
						or (y + 1 < height and getPixel(x, y + 1) == 0)
						or (y - 1 > 0 and getPixel(x, y - 1) == 0)
						or (x + 1 < width and y + 1 < height and getPixel(x + 1, y + 1) == 0)
						or (x + 1 < width and y - 1 > 0 and getPixel(x + 1, y - 1) == 0)
						or (x - 1 > 0 and y + 1 < height and getPixel(x - 1, y + 1) == 0)
						or (x - 1 > 0 and y - 1 > 0 and getPixel(x - 1, y - 1) == 0)) then
					count = count + 1;
					nodeList[count] = {x, y, {nil, nil, nil, nil}, nil};
					nodePositions[x * 1000 + y] = nodeList[count];
				end;
			end;
		end;
	end;

	return nodeList, nodePositions;
end;

-- Make edges between all nodes that are orthogonally adjecant
function graph.createEdges(nodeList, nodes)
	local node, currentNode;
	local toRemove = {};
	for i = #nodeList, 1, -1 do
		-- Due to the sorting, all nodes to the left and below have already been visited
		-- Thsu only the top end right has to be checked
		currentNode = nodeList[i];
		node = nodes[currentNode[1] * 1000 + currentNode[2] - 1];
		if (node) then
			currentNode[3][#currentNode[3] + 1] = node;
			node[3][#node[3] + 1] = currentNode;
		end;

		node = nodes[(currentNode[1] - 1) * 1000 + currentNode[2]];
		if (node) then
			currentNode[3][#currentNode[3] + 1] = node;
			node[3][#node[3] + 1] = currentNode;
		end;
	end;
end;

-- Enforce the invariant that no node can have more than two edges
-- Also deletes nodes that do not have any edges
function graph.cleanUpEdges(nodeList, nodes)
	local currentNode;
	for i = #nodeList, 1, -1 do
		currentNode = nodeList[i];
		if (#currentNode[3] == 0) then
			util.deleteNode(currentNode, nodeList, nodes);
		elseif (#currentNode[3] > 2) then
			-- Ensure node has no more than two edges
			if (#currentNode[3] > 2) then
				local x, y = currentNode[1], currentNode[2];
				local leftNode, rightNode = nodes[(x + 1) * 1000 + y], nodes[(x - 1) * 1000 + y];
				if (leftNode and rightNode) then
					for i = #currentNode[3], 1, -1 do
						if (currentNode[3][i] ~= leftNode and currentNode[3][i] ~= rightNode) then
							util.deleteEdge(currentNode, currentNode[3][i]);
						end;
					end;
				else
					for i = #currentNode[3], 1, -1 do
						if (currentNode[3][i] == leftNode or currentNode[3][1] == rightNode) then
							util.deleteEdge(currentNode, currentNode[3][i]);
						end;
					end;
				end;
			end;
		end;
	end;
end;

-- Adds a node and recursively all linked nodes except the previosu node to a group
-- Precondition: all nodes have at most two edges
-- Precondition: no nodes linked to this node (except the previous node) are in a group already
local function addNodeToGroup(node, group, previous)
	-- Add the node to the group
	node[4] = group;
	group[1] = group[1] + 1;

	if (node[3][1] and not node[3][1][4]) then
		addNodeToGroup(node[3][1], group, node);
	end;

	if (node[3][2] and not node[3][2][4]) then
		addNodeToGroup(node[3][2], group, node);
	end;

	-- If this node is an end, set it to be the start or the end
	if (#node[3] == 1) then
		if (group[2] == false) then
			group[2] = node;
		elseif (group[3] == false) then
			group[3] = node;
		else
			-- Should never happen!!!
			-- If this happens, the invariant has failed
			print("Grouping ERROR: more than two ends");
		end;
	end;
end;

-- Sort the edge list of a node
-- Ensures the previous node is always listed first, and the next node second
-- YAY FOR LUA HAVING PROPER TAIL CALLING
local function sortEdges(node, previous)
	if (not node) then
		return;
	end;

	if (not previous) then
		if (#node[3] ~= 1) then
			print("Sort-edges ERROR: start node is not a line-end");
			return;
		else
			return sortEdges(node[3][1], node);
		end;
	else
		if (node[3][1] ~= previous) then
			node[3][1], node[3][2] = node[3][2], node[3][1];
		end;
		return sortEdges(node[3][2], node);
	end;
end;

-- Group all linked nodes together into a curve
-- and store the start and end node.
-- Circular groups will be broken up in their leftmost (and heighest) node
function graph.createGroups(nodeList, nodes)
	local groups = {};
	local group;
	for i = 1, #nodeList do
		if (not nodeList[i][4]) then
			group = {0, false, false};

			addNodeToGroup(nodeList[i], group);

			if (group[1] == 1) then
				group[2], group[3] = nodeList[i], nodeList[i];
			elseif (group[2] == false) then
				group[2] = nodeList[i];
				group[3] = nodeList[i][3][2];
				util.deleteEdge(nodeList[i], nodeList[i][3][2]);
			end;

			if (group[1] > 30) then
				sortEdges(group[2]);
				groups[#groups + 1] = group;
			else
				--util.deleteNode(group[2], nodeList, nodes);
			end;	
		end;
	end;

	return groups;
end;

return graph;