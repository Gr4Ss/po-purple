
local drive = {};

local util = util;

local ipairs = ipairs;
local mathAcos = math.acos;
local mathHuge = math.huge;

function drive.findStart(realNodes, zero)
	local start;
	local min = mathHuge;
	for i = 1, #realNodes do
		local dist = util.distanceToSqr(realNodes[i], zero);
		if (dist < min) then
			min = dist;
			start = realNodes[i];
		end;
	end;

	return start;
end;

local minAngle = 170 / 180 * math.pi;

function drive.findTarget(start, nextTurn, intersections)
	local previousNode = start;
	local currentNode = start[3][1];
	local bend = false;
	local turn = false;
	local deadEnd = false;
	local intersectionsAhead = 0;
	while (currentNode) do
		if (#currentNode[3] == 1) then
			deadEnd = true;
			break;
		elseif (#currentNode[3] == 2) then
			local nextNode = currentNode[3][1];
			if (nextNode == previousNode) then
				nextNode = currentNode[3][2];
			end;

			local x1, y1 = nextNode[1] - currentNode[1], nextNode[2] - currentNode[2];
			local x2, y2 = 0, -1;
			local len1, len2 = x1 * x1 + y1 * y1, x2 * x2, y2 * y2;
			if (mathAcos((x1 * x2 + y1 * y2) / mathSqrt(len1 * len2)) > minAngle) then
				previousNode = currentNode;
				currentNode = nextNode;
			else
				bend = true;
				break;
			end;
		elseif (nextTurn) then
			local doBreak = true;
			for k, v in ipairs(currentNode[3]) do
				if (v == previousNode) then
					local next = (k + nextTurn) % #currentNode[3];
					if (next == 0) then next = #currentNode[3] end;

					local nextNode = currentNode[3][k + nextTurn];
					local x1, y1 = nextNode[1] - currentNode[1], nextNode[2] - currentNode[2];
					local x2, y2 = 0, -1;
					local len1, len2 = x1 * x1 + y1 * y1, x2 * x2, y2 * y2;
					if (mathAcos((x1 * x2 + y1 * y2) / mathSqrt(len1 * len2)) > minAngle) then
						previousNode = currentNode;
						currentNode = nextNode;
						doBreak = false;
						break;
					else
						intersectionsAhead = intersectionsAhead + 1;
						if (intersectionsAhead == intersections) then
							turn = true;
							break;
						else
							next = (k + nextTurn) % #currentNode[3];
							if (next == 0) then next = #currentNode[3] end;
							previousNode = currentNode;
							currentNode = currentNode[3][next];
							doBreak = false;
							break;
						end;
					end;
				end;
			end;

			if (doBreak) then
				turn = true;
				break;
			end;
		else
			local doBreak = true;
			for k, v in ipairs(currentNode[3]) do
				if (v ~= previousNode) then
					local x1, y1 = v[1] - currentNode[1], v[2] - currentNode[2];
					local x2, y2 = 0, -1;
					local len1, len2 = x1 * x1 + y1 * y1, x2 * x2, y2 * y2;
					if (mathAcos((x1 * x2 + y1 * y2) / mathSqrt(len1 * len2)) > minAngle) then
						previousNode = currentNode;
						currentNode = v;
						doBreak = false;
						break;
					end;
				end;
			end;

			if (doBreak) then
				deadEnd = true;
				break;
			end;
		end;
	end;

	return currentNode, bend, turn, deadEnd, intersectionsAhead;
end;

return drive;