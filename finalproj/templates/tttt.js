google.charts.load("current", { packages: ["imagelinechart"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable(a);

  var chart = new google.visualization.ImageLineChart(
    document.getElementById("chart_div")
  );

  chart.draw(data, { width: 400, height: 240, min: 0 });
}
