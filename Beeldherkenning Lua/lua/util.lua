
local util = {};

local tableRemove = table.remove;
local mathSqrt = math.sqrt;
local mathAtan = math.atan;
local mathSin = math.sin;

-- Prints the previous node, current node and next node.
function util.printNode(node)
	if (node) then
		print(node[3][1], node, node[3][2]);
	end;
end;

-- Deletes a node and recursively all nodes it is (in)directly linked to
function util.deleteNode(node, nodeList, nodes, previous)
	for i = 1, #nodeList do
		if (nodeList[i] == node) then
			tableRemove(nodeList, i);
			break;
		end;
	end;
	nodes[node[1] * 1000 + node[2]] = nil;

	for k, v in ipairs(node[3]) do
		if (v ~= previous) then
			util.deleteNode(v, nodeList, nodes, node);
		end;
	end;
end;

-- Deletes an edge between two nodes.
function util.deleteEdge(node1, node2)
	for k, v in pairs(node2[3]) do
		if (v == node1) then
			tableRemove(node2[3], k);
			break;
		end;
	end;

	for k, v in pairs(node1[3]) do
		if (v == node2) then
			return tableRemove(node1[3], k);
		end;
	end;
end;

-- Returns true if a pixel is more to the left of another pixel
-- If they are below/above each other, returns true if the pixel is below the other pixel
function util.sortNodes(a, b)
	if (a[1] == b[1]) then
		return a[2] < b[2];
	else
		return a[1] < b[1];
	end;
end;

-- Sort angles in ascending order
function util.sortAngles(a, b)
	return a[1] < b[1];
end;

-- Returns the sign of a number
function util.sign(a)
	if (a < 0) then
		return -1;
	elseif (a > 0) then
		return 1;
	else
		return 0;
	end;
end;

-- Returns the square of the distance of a point to a line formed by two other points
function util.distancePointLineToSqr(point, lineStart, lineEnd)
	local vx, vy = lineEnd[1] - lineStart[1], lineEnd[2] - lineStart[2];
	local wx, wy = point[1] - lineStart[1], point[2] - lineStart[2];

	local c1 = vx * wx + vy * wy;
	local c2 = vx * vx + vy * vy;
	local b = c1 / c2;

	local bx, by = lineStart[1] + b * vx, lineStart[2] + b * vy;
	return (point[1] - bx) * (point[1] - bx) + (point[2] - by) * (point[2] - by), bx, by;
end;

-- Returns the distance between two nodes
function util.distanceToSqr(node1, node2)
	return (node1[1] - node2[1]) * (node1[1] - node2[1]) + (node1[2] - node2[2]) * (node1[2] - node2[2]);
end;

function util.getNextTurn(turnList, commaLocation)
	local nextComma = string.find(turnList, ",", commaLocation);
	if (nextComma) then
		return string.sub(turnList, commaLocation + 1, commaLocation + 1),
			tonumber(string.sub(turnList, commaLocation + 2, nextComma - 1)), nextComma;
	else
		if (commaLocation < #turnList) then
			return string.sub(turnList, commaLocation + 1, commaLocation + 1),
				tonumber(string.sub(turnList, commaLocation + 2, -1)), #turnList;
		else
			return "d", 0, #turnList;
		end;
	end;
end;

-- Transform pixel positions to real coordinates and the other way around.
local startCM = 5.4;
local middleCM = 10.9;
local horizon = -13;
local heightCamera = 3.5;
local baseWidth = 6.7;
local a = mathSqrt(1 + (heightCamera * heightCamera) / (middleCM * middleCM));
local thetaMiddle = mathAtan(heightCamera / middleCM);
local mathSinThetaMiddle = mathSin(thetaMiddle);

function util.pixelYToReal(y, height)
	y = height - y;
	local b = (2 * y / height * (middleCM - startCM)) / (a * a * middleCM * middleCM);
	return -1 * (heightCamera * heightCamera * b + startCM) / (middleCM * b - 1);
end;

function util.realYToPixel(yCM, height)
	local theta = mathAtan(heightCamera / yCM);
	return height - ((yCM - startCM) * mathSin(theta) * height) 
		/ (2 * (middleCM - startCM) * mathSin(mathPi / 2 - theta + thetaMiddle) * mathSinThetaMiddle);
end;

function util.pixelXToReal(x, y, width, height)
	return (-1) * ((height - horizon) / (y - horizon)) * (baseWidth / width) * (x - width / 2.0);
end;

function util.realXToPixel(xCM, yCM, width, height)
	local x = util.realXToPixel(yCM, height);
	return (-1) * xCM / (((x - horizon) / (height - horizon)) * baseWidth / width) + width / 2;
end;

util.startCM = startCM;

return util;