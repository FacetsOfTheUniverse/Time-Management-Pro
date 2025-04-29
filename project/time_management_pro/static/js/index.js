// We are using Unix time (epoch time)

// Declare variables
const display = document.getElementById("display");
let timer = null;
let startTime = 0;
let stopTime = 0;
let elapsedTime = 0;
let isRunning = false;


let startTimestamp = 0;
let stopTimestamp = 0;
let timeClocked = startTimestamp - stopTimestamp;



// ---- The Timer Mechanism ----


// Provide Start/Stop functionality to the timer
function start_stop() {

    const button = document.getElementById("start_btn");
    const icon = button.querySelector("i");

    if (isRunning) {
        clearInterval(timer);
        elapsedTime = Date.now() - startTime;
        stopTime = Date.now();
        icon.className = "fa-solid fa-play fa-2x";
        isRunning = false;
    } else {
        startTime = Date.now() - elapsedTime;
        timer = setInterval(update, 10)
        stopTime = 0
        icon.className = "fa-solid fa-stop fa-2x";
        isRunning = true;
    }
}
// Grok AI helped me take my start and stop function and combine them into one button


// Provide Reset functionality to the timer
function reset() {
    // Reset all intermediate variable to 0
    clearInterval(timer);
    elapsedTime = 0;
    startTime = 0;
    display.textContent = "00:00:00:00";
    isRunning = false;
}



// Provide update functionality to the timer
function update() {

    const currentTime = Date.now();
    elapsedTime = currentTime - startTime

    let hours = Math.floor(elapsedTime / (1000 * 60 * 60));
    let minutes = Math.floor(elapsedTime / (1000 * 60) % 60);
    let seconds = Math.floor(elapsedTime / 1000 % 60);
    let milliseconds = Math.floor(elapsedTime % 1000 / 10);

    hours = String(hours).padStart(2, "0");
    minutes = String(minutes).padStart(2, "0");
    seconds = String(seconds).padStart(2, "0");
    milliseconds = String(milliseconds).padStart(2, "0");

    display.textContent = `${hours}:${minutes}:${seconds}:${milliseconds}`;
}

// ---- The basic mechanisms of this timer were based on Bro Codes Java Timer Tutorial



// ---- Functions ----


// Sends timer data, that the user would like to save, to Python for proccessing
function saveTimerEntry() {

    // Message if no timer is chosen and user trys to save
    if (document.getElementById("timer_name").textContent == "Select a Timer") {
        saveMessage.textContent = "Select a Timer!";
        setTimeout(() => {
            saveMessage.textContent = "";
        }, 3000);
    }

    // Make sure the timer only saves valid times
    if (!isRunning && elapsedTime > 0 && document.getElementById("timer_name").textContent !== "Select a Timer") {
        let dataToSend = {
            startTimestamp: startTime,
            stopTimestamp: stopTime,
            timeClocked: elapsedTime
        };

        console.log(startTime)
        console.log(stopTime)
        console.log(elapsedTime)

        clearInterval(timer);
        elapsedTime = 0;
        startTime = 0;
        display.textContent = "00:00:00:00";
        isRunning = false;

        // AJAX Call send POST request to our flask application for proccessing these intermideate variables: start_timestamp, stop_timestamp, and time-clocked
        fetch('/save_timer_entry', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend)
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch((error) => console.error('Error:', error));

        saveMessage.textContent = "Time Logged!";
        setTimeout(() => {
            saveMessage.textContent = "";
        }, 3000);
    }
};



// Enables a user to dinamically change the timers name on index page and at the server
function selectTimer(timerName) {

    // Update Webpage
    document.getElementById("timer_name").textContent = timerName;

    // Send Data to Server
    fetch('/update_timer_name', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                timer_name: timerName
            })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => console.error('Error:', error));
}
