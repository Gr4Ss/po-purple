
local preprocess = {};

local mathAbs = math.abs;
local mathFloor = math.floor;


-- Calculates a minimum luma value for 'white' pixels
function preprocess.getMinLuma(getPixel, width, height)
	local lumaList = {};
	local inList = {};

	-- Count all pixels per luma value
	local luma;
	for x = 0, width do
		for y = 0, height do
			luma = getPixel(x, y);
			lumaList[luma] = (lumaList[luma] or 0) + 1;
		end;
	end;

	-- Determine where the white pixels peak,
	-- where the peak stops and where the black pixels peak
	local inWhite, passedWhite, sum;
	for i = 255, 1, -1 do
		if (not inWhite) then
			if ((lumaList[i] or 0) - (lumaList[i + 1] or 0) > 500) then
				inWhite = i;
			end;
		elseif (not passedWhite) then
			sum = 0;
			for j = i, i - 10, -1 do
				sum = sum + mathAbs((lumaList[j] or 0) - (lumaList[j + 1] or 0));
			end;
			if (sum < 200) then
				passedWhite = i - 10;
			end;
		elseif ((lumaList[i] or 0) - (lumaList[i + 1] or 0) > 250) then
			luma = i;
			break;
		end;
	end;

	-- Find where the black pixels start to peak
	for i = luma, 255 do
		if ((lumaList[i] or 0) - (lumaList[i + 1] or 0) < 0) then
			-- Return the middle between the end of the white pixel peak 
			-- and the start of the black pixel peak
			return mathFloor(passedWhite + i) / 2;
		end;
	end;
end;

-- Set a pixel to white if it is above the minimum luma
-- and within the chroma limits, else make it black.
-- Returns between which x values and from which y value there are white pixels
function preprocess.makeBlackWhite(getPixel, setPixel, width, height, minLuma)
	local luma, b, r, firstWhite, lastWhite, lowestWhite;
	for x = 0, width do
		for y = 0, height do
			luma, b, r = getPixel(x, y);
			if (luma >= minLuma and mathAbs(b / 255 - 0.5) < 0.15 and mathAbs(r / 255 - 0.5) < 0.15) then
				setPixel(x, y, 255, 128, 128);
				if (not firstWhite) then
					firstWhite = x;
				else
					lastWhite = x;
				end;

				if (not lowestWhite or y < lowestWhite) then
					lowestWhite = y;
				end;
			else
				setPixel(x, y, 0, 128, 128);
			end;
		end;
	end;

	return firstWhite or 0, lastWhite or 0, lowestWhite or 0;
end;

-- Makes a pixel black/white if there are three white/black pixels next to it
-- Works recursively if it made a white pixel black
local getPixel, setPixel, width, height;
local function redNoise(x, y)
	local count = 0;
	local color = getPixel(x, y);
	if ((x < width and getPixel(x + 1, y) ~= color) or (x == width and color == 255)) then
		count = count + 1;
	end;
	if ((x > 0 and getPixel(x - 1, y) ~= color) or (x == 0 and color == 255)) then
		count = count + 1;
	end;
	if ((y < height and getPixel(x, y + 1) ~= color) or (y == height and color == 255)) then
		count = count + 1;
	end;
	if ((y > 0 and getPixel(x, y - 1) ~= color) or (y == 0 and color == 255)) then
		count = count + 1;
	end;

	if (count >= 3) then
		setPixel(x, y, 255 - color, 128, 128);
		if (color == 255) then
			if (y - 1 >= 0) then
				redNoise(x, y - 1);
			end;
			if (x - 1 >= 0) then
				return redNoise(x - 1, y);
			end;
		end;
	end;
end;

function preprocess.reduceNoise(getP, setP, w, h, firstWhite, lastWhite, lowestWhite)
	getPixel, setPixel, width, height = getP, setP, w, h;
	for x = firstWhite, lastWhite do
		for y = lowestWhite, height do
			redNoise(x, y);
		end;
	end;
end;

return preprocess;