/*var Dataset = {
	"vertices": [
		[1, {"origin": 3, "straight": 2, "left": 4}],
		[2, {"origin": 1, "straight": 3, "left": 4}],
		[3, {"origin": 2, "straight": 1, "left": 4}],
		[4, {"origin": 3, "straight": 1, "left": 2}]
	],
	"edges": [
		[1, 2, 0.3],
		[1, 3, 0.5],
		[3, 1, 0.5],
		[2, 3, 0.1],
		[3, 2, 0.1],
		[3, 4, 0.7],
		[4, 2, 0.3],
		[4, 1, 0.8]
	]
};*/

/**var Dataset = {
	"vertices": [
		[1, {"origin": 6, "straight": 2}],
		[2, {"origin": 1, "straight": 3, "left": 4}],
		[3, {"origin": 2, "straight": 7, "left": 9}],
		[4, {"origin": 2, "straight": 5}],
		[5, {"origin": 4, "left": 6, "right": 10}],
		[6, {"origin": 5, "straight": 1}],
		[7, {"origin": 3, "straight": 8}],
		[8, {"origin": 7, "straight": 9}],
		[9, {"origin": 8, "left": 3, "right": 10}],
		[10, {"origin": 9, "straight": 5}],
	],
	"edges": [
		[1, 2, 0.3],
		[2, 1, 0.3],
		[2, 3, 0.3],
		[3, 2, 0.3],
		[6, 1, 0.6],
		[2, 4, 0.3],
		[4, 5, 0.3],
		[3, 9, 0.3],
		[9, 3, 0.3],
		[3, 7, 0.3],
		[7, 3, 0.3],
		[7, 8, 0.3],
		[8, 9, 0.3],
		[9, 8, 0.3],
		[9, 10, 0.3],
		[10, 9, 0.3],
		[5, 10, 0.3],
		[10, 5, 0.3],
		[5, 6, 0.3],
		[6, 5, 0.3],
	]
}**/

/*Dataset for the demo*/
/*var Dataset = {
	"vertices": [
		[1, {"origin": 1, "straight": 2}],
		[2, {"origin": 1, "straight": 3}],
		[3, {"origin": 2, "straight": 11, "right": 4}],
		[4, {"origin": 3, "straight": 5, "left": 10}],
		[5, {"origin": 4, "straight": 15, "right": 6}],
		[6, {"origin": 5, "straight": 7, "left": 15}],
		[7, {"origin": 6, "straight": 8, "left": 15}],
		[8, {"origin": 7, "straight": 9, "left": 15, "right": 12}],
		[9, {"origin": 8, "straight": 10, "left": 5, "right": 14}],
		[10, {"origin": 9, "straight": 11, "left": 4, "right": 14}],
		[11, {"origin": 10, "straight": 13, "left": 3, "right": 12}],
		[12, {"origin": 11, "left": 13, "right": 8}],
		[13, {"origin": 12, "straight": 11}],
		[14, {"origin": 9, "straight": 10}],
		[15, {"origin": 5, "straight": 7, "left": 8, "right": 6}],
	],
	"edges": [
		[1, 2, 0.3],
		[2, 3, 0.3],
		[3, 4, 0.3],
		[4, 5, 0.3],
		[5, 6, 0.4],
		[6, 7, 0.4],
		[7, 8, 0.4],
		[8, 9, 0.3],
		[9, 10, 0.1],
		[10, 11, 0.4],
		[11, 12, 0.3],
		[12, 13, 0.3],
		[13, 11, 0.4],
		[4, 10, 0.4],
		[5, 9, 0.4],
		[5, 10, 0.3],
		[5, 15, 0.3],
		[6, 15, 0.3],
		[7, 15, 0.3],
		[8, 15, 0.3],
		[8, 12, 1],
		[10, 14, 0.2],
		[9, 14, 0.2],
		[11, 3, 0.3],
	]
}*/

/*var Dataset = {
	"vertices": [
		[0, {"origin": 1, "left": 2, "right": 5}],
		[1, {"origin": 0, "straight": 2, "left": 4}],
		[2, {"origin": 0, "left": 1, "right": 3}],
		[3, {"origin": 2, "left": 4, "right": 7, "straight": 8}],
		[4, {"origin": 1, "right": 3, "left": 5, "straight": 8}],
		[5, {"origin": 0, "right": 4, "left": 6}],
		[6, {"origin": 5, "straight": 7, "right": 8}],
		[7, {"origin": 3, "right": 6, "straight": 8}],
		[8, {"origin": 3, "left": 4, "straight": 6, "right": 7}]
	],
	"edges": [
		[0, 1, 1.0],
		[0, 2, 4.0],
		[1, 0, 1.0],
		[1, 2, 2.0],
		[1, 4, 4.0],
		[2, 0, 4.0],
		[2, 1, 2.0],
		[2, 3, 5.0],
		[3, 2, 5.0],
		[3, 4, 2.0],
		[3, 7, 4.0],
		[3, 8, 1.5],
		[4, 1, 4.0],
		[4, 5, 2.0],
		[4, 8, 1.5],
		[5, 0, 5.0],
		[5, 4, 2.0],
		[5, 6, 4.0],
		[6, 5, 4.0],
		[6, 7, 4.0],
		[6, 8, 1.5],
		[7, 3, 4.0],
		[7, 6, 4.0],
		[7, 8, 1.5],
		[8, 3, 1.5],
		[8, 4, 1.5],
		[8, 6, 1.5],
		[8, 7, 1.5]
	]
}
*/

var Dataset = [];

$.getJSON("http://localhost:9000/map", function(data) {
	Dataset = data;
	console.log(data);
	convertDataSet();
	network.on("stabilized", function(params) {
		network.fit();
		colorAllPositions;
		makeExternalLegend;
	});
})


/* Variable for the nodes of the dataset */
var visSetNodes = new vis.DataSet();

/* Variable for the edges of the dataset */
var visSetEdges = new vis.DataSet();

/* Converts the dataset from the given assignment, to a dataset usable in the JavaScript Library Vis.js */
function convertDataSet() {
	/* First add the nodes */
	for (i in Dataset["vertices"]) {
		var localset = new Set();
		localset = {id: Dataset["vertices"][i][0], label: Dataset["vertices"][i][0]};
		visSetNodes.add(localset);
	}
	/* Then add the edges */
	for (i in Dataset["edges"]) {
		var localset = new Set();
		minVal = Math.min(Dataset["edges"][i][0], Dataset["edges"][i][1]);
		maxVal = Math.max(Dataset["edges"][i][0], Dataset["edges"][i][1]);
		localset = {from: Dataset["edges"][i][0], to: Dataset["edges"][i][1], label: Dataset["edges"][i][2], length: (Dataset["edges"][i][2])*(Dataset["edges"][i][2]), id: (7*minVal +11*maxVal)};
		if (visSetEdges.get({filter: function (item) {return (item.from == localset.to && item.to ==localset.from);}}).length != 0) {
			minVal = Math.min(localset.to, localset.from);
			maxVal = Math.max(localset.to, localset.from);
			visSetEdges.update({id: 7*minVal+11*maxVal, arrows: { from: {enabled: true, scaleFactor: 1}}});
			visSetEdges.remove({from: minVal, to: maxVal, label: localset.label, length: localset.length, arrows: { from: {enabled: true, scaleFactor: 1}}});
		} else {
			visSetEdges.add(localset);
		}
	}
};

/* Get the HTML-container */
var container = document.getElementById('mynetwork');

/* Requirement for Vis.js*/
var data = {
	nodes: visSetNodes,
	edges: visSetEdges
};

/* Set the options for the canvas and the physics simulation */
var options = {
	edges:{
		smooth: {
			enabled: true,
			type: 'dynamic',
			roundness: 0,
		},
		arrows:{
			to:	{enabled: true, scaleFactor:1}
		},
		color: {
			color: "#3399ff"
		},
		physics: true
	},
	nodes: {
		color: {
			border: "#3399ff",
			background: "#3399ff"
		},
		physics: true
	},
	physics:{
		enabled: true,
		barnesHut: {
			gravitationalConstant: -2000,
			springConstant: 0.09,
			damping: .09,
			avoidOverlap: .3
		},
		stabilization: {
			enabled: true,
			iterations: 100,
			updateInterval: 5,
		}
	},
	layout: {
		randomSeed: 395813
	}
};

/* Change a node's color to the given color */
function changeNodeColor(nodeid, newColor) {
    data.nodes.update([{id: nodeid, color:{background:newColor}}]);
};

/* Change an edge color to the given color */
function changeEdgeColor(fromid, toid, newColor) {
	data.edges.update([{id: (7*fromid + 11*toid), color:{color:newColor}}]);
};

/* Adds the team name to a give node */
function addTeamNameNode(teamname, nodeId) {
	data.nodes.update([{id: nodeId, label: nodeId + " (" + (teamname) + ")"}]);
};
 /* Adds the team name to a given edge*/
function addTeamNameEdge(teamname, fromNode, toNode, labelDist) {
	data.edges.update([{id: (7*fromNode + 11*toNode), label: labelDist + " (" + (teamname) + ")"}]);
};
 /* Deletes the team name from a given node */
function deleteTeamNameNode(nodeId) {
	data.nodes.update([{id: nodeId, label: nodeId}])
};
 /* Deletes the team  name from a given edge */
function removeTeamNameEdge(teamname, fromNode, toNode, labelDist) {
	data.edges.update([{id: (7*fromNode + 11*toNode), label: labelDist}])
};

function changeTeamPosition(carTeam) {
	if (hasNodePosition(car)) {
		
	}
	else {
		
	}
}

/* Changes the position of a team */
function changePositionTeam(prevPosition, newPosition, teamName) {
	pass;
};


//////////// SETTING UP NETWORK ////////////

/* Converts the dataset to a new one usable in vis */
//convertDataSet();

/* Setup a new network */
var network = new vis.Network(container, data, options);

//changeNodeColor(1, '#ababab');
//changeEdgeColor(3, 4, '#ab78ab');

myPositions = "haha";

carPrevPosMap = [];
carPosMap = [];
carHashMap = {};

function colorAllPositions() {
	$.getJSON("http://localhost:9000/positions", function(data) {
		console.log(data);
		myPositions = data;
		for (i in myPositions["positions"]){
			carPosMap[i] = [myPositions["positions"][i][0], myPositions["positions"][i][1], myPositions["positions"][i][2]];
			carHashMap[hashCode(myPositions["positions"][i][0])] = myPositions["positions"][i][0];
			console.log(carPosMap[i]);
		}
		if (carPrevPosMap.length == 0) {
			for (i in myPositions["positions"]) {
				carPrevPosMap[i] = carPosMap[i];
			}
		}
		for (car in carPosMap) {
			if (carPosMap[car] == carPrevPosMap[car]) {
				if (carPosMap[car][1] == carPosMap[car][2]) {
					//addTeamNameNode(carPosMap[car][0], carPosMap[car][1])
					changeNodeColor(carPosMap[car][1], hexToRgbA(intToRGB(hashCode(carPosMap[car][0]))));
				} else {
					//addTeamNameEdge(carPosMap[car][0], carPosMap[car][1], carPosMap[car][2], 1);
					//addTeamNameEdge(carPosMap[car][0], carPosMap[car][2], carPosMap[car][1], 1);
					changeEdgeColor(carPosMap[car][1], carPosMap[car][2], hexToRgbA(intToRGB(hashCode(carPosMap[car][0]))));
					changeEdgeColor(carPosMap[car][2], carPosMap[car][1], hexToRgbA(intToRGB(hashCode(carPosMap[car][0]))));
				}
			} else {
				console.log("elsing2");
				if (carPosMap[car][1] == carPosMap[car][2]) {
					changeNodeColor(carPrevPosMap[car][1], hexToRgbA(intToRGB(hashCode(carPosMap[car][0]))));
					changeEdgeColor(carPrevPosMap[car][1], carPrevPosMap[car][2], "#3399ff");
				} else {
					console.log(carPosMap[car][1]);
					changeEdgeColor(carPosMap[car][1], carPosMap[car][2], hexToRgbA(intToRGB(hashCode(carPosMap[car][0]))));
					changeNodeColor(carPrevPosMap[car][1], "#3399ff");
				}
			}
		}
		carPrevPosMap = carPosMap;
		
		console.log(carHashMap);
		
		
	});
};

function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
} 

function intToRGB(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}

function hexToRgbA(hex){
	hex = "#" + hex;
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',.5)';
    }
    throw new Error('Bad Hex');
}


function makeExternalLegend() {
	var legendDiv = document.getElementById("mylegend");
	for (car in carPosMap) {
		var containerDiv = document.createElement("div");
		var descriptionDiv = document.createElement("button");

		containerDiv.className = 'legend-element-container';
		descriptionDiv.className = "description-container";

		console.log(carPosMap[car][0]);
		descriptionDiv.innerHTML = carPosMap[car][0];
		
		legendDiv.appendChild(containerDiv);
		containerDiv.appendChild(descriptionDiv);
		
		containerDiv.style.width = "100%";
		descriptionDiv.style.width = 100/carPosMap.length + '%';
		descriptionDiv.style.float = 'left';
		descriptionDiv.style.backgroundColor = hexToRgbA(intToRGB(hashCode(carPosMap[car][0])));
		
		$(descriptionDiv).click(function(event) {
			zoomToID(event.target.innerHTML);
		});
		
	}
}

function zoomToID(teamName) {
	for (car in carPosMap) {
		if (carPosMap[car][0] == teamName) {
			console.log(carPosMap[car]);
			zoomNodeID = [carPosMap[car][1], carPosMap[car][2]];
			break;
		}
	}
	
	if (zoomNodeID[0] == zoomNodeID[1]) {
		network.focus(zoomNodeID[0], {
			scale: 2,
			animation: {
				duration: 300,
				easingFunction: "easeInQuad"
			}
			});
	} else {
		nodePositions = network.getPositions(zoomNodeID);
		valX1 = nodePositions[zoomNodeID[0]].x;
		valX2 = nodePositions[zoomNodeID[1]].x;
		valY1 = nodePositions[zoomNodeID[0]].y;
		valY2 = nodePositions[zoomNodeID[1]].y;
		valX = (valX1 + valX2)/2;
		valY = (valY1 + valY2)/2;
		
		network.moveTo({
			position: {x: valX, y: valY},
			scale: 2,
			animation: {
				duration: 300,
				easingFunction: "easeInQuad"
			}
		})
	}
} 


//////////// MAINTAINING THE NETWORK ///////

/* Dynamically lets the network fit to the canvas */
//setInterval(function() {network.fit()}, 10);

var canvas = document.getElementById('mynetwork');
fitToContainer(canvas);

function fitToContainer(canvas){
  // Make it visually fill the positioned parent
  canvas.style.width ='100%';
  canvas.style.height='100%';
  // ...then set the internal size to match
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}

String.prototype.hashCode = function(){
	var hash = 0;
	if (this.length == 0) return hash;
	for (i = 0; i < this.length; i++) {
		char = this.charCodeAt(i);
		hash = ((hash<<5)-hash)+char;
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash;
}


/**
setInterval(function(){ 
	prevPos = carPos;
	randVar = Math.random();
	if (carPos == 1) {
		carPos = 2;
	} else if (carPos == 15) {
		carPos = 14;
	} else {
		if (randVar <= 0.5) {
			carPos -= 1;
		} else {
			carPos += 1;
		}
	}
	console.log(carPos);
	changeNodeColor(carPos, '#ab78ab');
	changeNodeColor(prevPos, '#3399ff');
}, 3000);**/

/**	
setInterval(function() {
	prevIterator = iterator;
	iterator = Math.floor(Math.random()*Dataset.edges.length);
	console.log(Dataset.edges[iterator]);
	changeEdgeColor(Dataset.edges[iterator][0],Dataset.edges[iterator][1], '#ab78ab');
	changeEdgeColor(Dataset.edges[prevIterator][0],Dataset.edges[prevIterator][1], '#3399ff');
}, 3000);
**/
	


