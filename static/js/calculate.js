function CalculateCo2() {
  var fetch_url = "/calculate";
  fetch(fetch_url)
    .then(response => response.json())
    .then(data =>  document.getElementById("co2-score").innerHTML = "Jouw co2 score is: " + data.co2_score.toFixed(2));
}
