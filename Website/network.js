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

var Dataset = {
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
		[2, 3, 0.2],
		[3, 2, 0.2],
		[6, 1, 0.6],
		[2, 4, 0.3],
		[4, 5, 0.3],
		[3, 9, 0.5],
		[9, 3, 0.5],
		[3, 7, 0.4],
		[7, 3, 0.4],
		[7, 8, 0.5],
		[8, 9, 0.3],
		[9, 8, 0.3],
		[9, 10, 0.3],
		[10, 9, 0.3],
		[5, 10, 0.3],
		[10, 5, 0.3],
		[5, 6, 0.3],
		[6, 5, 0.3],
	]
}

function checkDependencies(edgeset) {
	console.log(edgeset);
	for (i=0; i<edgeset.length; i++) {
		for (j=0; j<edgeset[i].length; j++) {
			
		}
	}
};

console.log(Dataset["vertices"]);

var visSetNodes = new vis.DataSet();

var visSetEdges = new vis.DataSet();


function convertDataSet() {
	for (i in Dataset["vertices"]) {
		var localset = new Set();
		localset = {id: Dataset["vertices"][i][0], label: Dataset["vertices"][i][0]};
		visSetNodes.add(localset);
	}
	for (i in Dataset["edges"]) {
		var localset = new Set();
		localset = {from: Dataset["edges"][i][0], to: Dataset["edges"][i][1], label: Dataset["edges"][i][2], length: 1000*(Dataset["edges"][i][2])*(Dataset["edges"][i][2]), id: (7*Dataset["edges"][i][0] +11*Dataset["edges"][i][1])};
		if (visSetEdges.get({filter: function (item) {return (item.from == localset.to && item.to ==localset.from);}}).length != 0) {
			console.log('from: ', localset.from, ', to: ', localset.to);
			console.log(localset.to);
			visSetEdges.update({id: 7*localset.to+11*localset.from, arrows: { from: {enabled: true, scaleFactor: 1}}});
			visSetEdges.remove({from: localset.to, to: localset.from, label: localset.label, length: localset.length, arrows: { from: {enabled: true, scaleFactor: 1}}});
		} else {
			visSetEdges.add(localset);
		}
	}
};

var container = document.getElementById('mynetwork');

var data = {
	nodes: visSetNodes,
	edges: visSetEdges
};

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
			border: "#3399ff",
			color: "#3399ff"
		}
	},
	nodes: {
		color: {
			border: "#3399ff",
			background: "#3399ff"
		}
	},
	physics:{
		enabled: true
	},
	layout:{
	}
};

function changeNodeColor(nodeid, newColor) {
    data.nodes.update([{id: nodeid, color:{background:newColor}}]);
};

function changeEdgeColor(fromid, toid, newColor) {
	data.edges.update([{id: (7*fromid + 11*toid), color:{color:newColor}}]);
};

var network = new vis.Network(container, data, options);

convertDataSet();

setTimeout(network.fit(), 1000);

function addTeamNameNode(teamname, nodeId) {
	data.nodes.update([{id: nodeId, label: nodeId + " (" + (teamname) + ")"}]);
};

function addTeamNameEdge(teamname, fromNode, toNode, labelDist) {
	data.edges.update([{id: (7*fromNode + 11*toNode), label: labelDist + " (" + (teamname) + ")"}]);
};

function deleteTeamNameNode(nodeId) {
	data.nodes.update([{id: nodeId, label: nodeId}])
};

function addTeamNameEdge(teamname, fromNode, toNode, labelDist) {
	data.edges.update([{id: (7*fromNode + 11*toNode), label: labelDist}])
};

function changePositionTeam(prevPosition, newPosition, teamName) {
	pass;
};

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

//changeNodeColor(1, '#ababab');
//changeEdgeColor(3, 4, '#ab78ab');

var prevPos = 1;
var carPos = 1;
var prevIterator = 1;
var iterator = 1;

/**
setInterval(function(){ 
	prevPos = carPos;
	while (carPos == prevPos) {
	carPos = Math.round(3*Math.random()+1);
	}
	changeNodeColor(carPos, '#ab78ab');
	changeNodeColor(prevPos, '#3399ff');
}, 3000);
	
setInterval(function() {
	prevIterator = iterator;
	iterator = Math.floor(Math.random()*Dataset.edges.length);
	console.log(Dataset.edges[iterator]);
	changeEdgeColor(Dataset.edges[iterator][0],Dataset.edges[iterator][1], '#ab78ab');
	changeEdgeColor(Dataset.edges[prevIterator][0],Dataset.edges[prevIterator][1], '#3399ff');
}, 3000);
**/
	


