google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
	let xhr = new XMLHttpRequest();
	xhr.open("GET", "http://raspberrypi.local:8080/data/abc");
	xhr.onload = function () {
		if (xhr.readyState == 4 && xhr.status == 200) {
			setInterval(getData, 1000, draw);
		}
	};
	xhr.send(null);
}

function getData(cb) {
	let xhr = new XMLHttpRequest();
	xhr.open("GET", "http://raspberrypi.local:8080/data/abc");
	xhr.onload = function () {
		if (xhr.readyState == 4 && xhr.status == 200) {
			let data = JSON.parse(xhr.responseText);
			cb(data);

		}
	};
	xhr.send(null);
}

function draw(data) {
	let i = 0;
	data.forEach(row => row[0] = new Date(row[0]));
	data.unshift(["MDATETIME", "AX", "AY", "AZ", "GX", "GY", "GZ", "MX", "MY", "MZ"]);
	console.log(data);
	data = google.visualization.arrayToDataTable(data);
	var options = {
		title: "9dim",
		curveType: "function",
		legend: { position: "bottom" },
	};
	let chart = new google.visualization.LineChart(document.getElementById("chart"));
	chart.draw(data, options);
}
