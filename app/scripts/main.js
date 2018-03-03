data = [];
function loadData(callback) {
    d3.json("./data/tutf-performances.json", function(json) {
        console.log("Data Retrieved: ", json);
        data = json;
        callback();
    });
}

function plot(athlete, tfEvent, dates, marks, meets) {
    let capFirst = s => s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
    let capFirsts = s => (s.split(" ").map(w => capFirst(w))).join(" ")

    let data = {
      x: dates,
      y: marks,
      mode: "lines+markers",
      name: capFirsts(athlete),
      text: meets,
      marker: { color: "rgb(72, 145, 206)", size: 10, line: { color: "white", width: 0.5 } }
    };

    let layout = {
        hovermode: 'closest',
        title: capFirsts(athlete) + " in the " + tfEvent,
        xaxis: { title: "Time", showgrid: false, zeroline: false },
        yaxis: { title: "Mark", showline: false }
    };

    Plotly.newPlot("plot", [data], layout);
}

function createTimeSeries(first, last, tfEvent) {
    let perfs = []
    let filtered = data.filter(perf => perf.hasOwnProperty("firstname"))
        .filter(perf => perf.firstname.toLowerCase() == first.toLowerCase() &&
            perf.lastname.toLowerCase() == last.toLowerCase())
        .filter(perf => perf.event.toLowerCase() == tfEvent.toLowerCase());
    let mapped = filtered.map(function(perf) {
        let date = new Date(perf.date);
        let mark;
        if (perf.hasOwnProperty("time")) {
            let time;
            if (perf.time.includes(":")) {
                let timeString = perf.time.indexOf(":") == 1 ? "0" + perf.time : perf.time;
                let dateString = "2018-01-01T00:" + timeString;
                let dateWithTime = new Date(dateString);
                let today = new Date();
                today.setTime(dateWithTime.getTime())
                mark = today;
            }
            else
                mark = perf.time
        }
        else if (perf.hasOwnProperty("mark"))
            mark = perf.mark.substring(0, perf.mark.length - 1);
        else if (perf.hasOwnProperty("points"))
            mark = perf.points;
        let meet = perf.meet;
        return { "date": date, "mark": mark, "meet": meet };
    });
    let sorted = mapped.sort((p1, p2) => p1.date - p2.date);
    console.log("Performances: ", sorted)
    return sorted;
}

function plotAthleteProgres(name, tfEvent) {
    let [first, last] = name.split(" ");
    let timeSeries = createTimeSeries(first, last, tfEvent);
    let dates = timeSeries.map(perf => perf.date)
    let marks = timeSeries.map(perf => perf.mark)
    let meets = timeSeries.map(perf => perf.meet)
    plot(name, tfEvent, dates, marks, meets);
}

function query(name, tfEvent) {
    plotAthleteProgres(name, tfEvent);
}

function createSearchLists() {
    let athletes = new Set();
    let events = new Set();
    data.forEach(function(perf) {
        if (perf.hasOwnProperty("firstname")) {
            let first = perf.firstname;
            let last = perf.lastname;
            let tfEvent = perf.event;
            if (!athletes.has(first + " " + last))
                athletes.add(first + " " + last);
            if (!events.has(tfEvent))
                events.add(tfEvent);
        }
    });
    let sortedAthletes = Array.from(athletes.keys()).sort();
    let sortedEvents = Array.from(events.keys());
    console.log("Athletes: ", sortedAthletes)
    console.log("Events: ", sortedEvents)
    return [sortedAthletes, sortedEvents];
}

function allowQueries() {
    [athletes, tfEvents] = createSearchLists();
    d3.select("#searchButton").on("click", function() {
        let name = document.getElementById("name").value;
        let tfEvent = document.getElementById("tfEvent").value;
        query(name, tfEvent);
    });
    d3.selec
}

function onTextUpdate() {
    let name = document.getElementById("name").value;
    // console.log("Text update", name)
}

function run() {
    loadData(allowQueries);
}

run();
