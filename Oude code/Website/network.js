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

var Dataset = {
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

console.log(Dataset["vertices"][0]);

/** Checks whether there are two-way streets **/
function checkDependencies(edgeset) {
	console.log(edgeset);
	for (i=0; i<edgeset.length; i++) {
		for (j=0; j<edgeset[i].length; j++) {
			
		}
	}
};

/* Variable for the nodes of the dataset */
var visSetNodes = new vis.DataSet();

/* Variable for the edges of the dataset */
var visSetEdges = new vis.DataSet();

/* Converts the dataset from the given assignment, to a dataset usable in the JavaScript Library Vis.js */
function convertDataSet() {
	/* First add the nodes */
	for (i in Dataset["vertices"]) {
		console.log(i)
		var localset = new Set();
		localset = {id: Dataset["vertices"][i][0], label: Dataset["vertices"][i][0]};
		visSetNodes.add(localset);
	}
	/* Then add the edges */
	for (i in Dataset["edges"]) {
		var localset = new Set();
		localset = {from: Dataset["edges"][i][0], to: Dataset["edges"][i][1], label: Dataset["edges"][i][2], length: (Dataset["edges"][i][2])*(Dataset["edges"][i][2]), id: (7*Dataset["edges"][i][0] +11*Dataset["edges"][i][1])};
		if (visSetEdges.get({filter: function (item) {return (item.from == localset.to && item.to ==localset.from);}}).length != 0) {
			visSetEdges.update({id: 7*localset.to+11*localset.from, arrows: { from: {enabled: true, scaleFactor: 1}}});
			visSetEdges.remove({from: localset.to, to: localset.from, label: localset.label, length: localset.length, arrows: { from: {enabled: true, scaleFactor: 1}}});
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

/* Change the position of a team */
function changePositionTeam(prevPosition, newPosition, teamName) {
	pass;
};

/* Converts the dataset to a new one usable in vis */
convertDataSet();

/* Setup a new network */
var network = new vis.Network(container, data, options);

/* */
function showRouteTeam(teamname, nodeList, edgeList) {
	var newColor = '#3399ff';
	switch(teamname) {
		case "Purple":
			newColor = "purplecolor";
		case "Green":
			newColor = "greencolor";
		case "Gold":
			newColor = "goldcolor";
	}
	for (i in nodeList) {
		changeNodeColor(i.id, newColor);
	}
	for (i in edgeList) {
		changeEdgeColor(i.id, newColor);
	}
}

var ownCar = {team: 'Purple', currentNodePos: 1, currentEdgePos: {from: 1, to: 3}};
var otherCar1;
var otherCar2;
var otherCar3;

var prevPos = 1;
var carPos = 1;
var prevIterator = 1;
var iterator = 1;

/* Dynamically lets the network fit to the canvas */
setInterval(function() {network.fit()}, 10);

network.on("stabilizationProgress", function(params) {
	console.log("progress: ", params);
});

network.on("stabilizationIterationsDone", function() {
	console.log("true");
});

network.on("startStabilizing", function() {
	network.on("stabilizationProgress", function(params) {
		console.log("progress: ", params);
	})
	console.log("Starting stabilization");
});

network.on("stabilized", function(params) {
	
	console.log("stabilized", params);
});

$.get("http://localhost:9000/positions", function(data) {
	console.log(data);
	var data2 = $.parseJSON(data);
	console.log(data2.positions);
	for (i in data2.positions) {
		console.log(data2.positions[i][1]);
		changeNodeColor(data2.positions[i][1], "#ab78ab");
	}
});

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
	


