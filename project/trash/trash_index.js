// # FUNCTUNALITY OF THE TIMER



// declare variables
const display = document.getElementById("display");
let timer = null;
let startTime = 0;
let stopTime = 0;
let elapsedTime = 0;
let isRunning = false;

// We are using Unix time (epoch time)

// I AM CURRENTLY TRING TO INTEGRATE DATA SAVING FEATURES INTO MY TIMER. The stopTime is a new added variable)


//this might be redundant and therefore not proper
//but for now Im keeping the timer and how it works
//seperate from the data collection mechanisma id like to put in place just to keep things straight
//Also because im not sure of how to implement the data collection yet.
let startTimestamp = 0;
let stopTimestamp = 0;
// timeClocked should be called elapsed time.
let timeClocked = startTimestamp - stopTimestamp;

//see this is all good but the problem is the variables that i would use to send data over to the server side
//are being used for different calculations can i set those variables to another variable as the progrma is working its way through
// like     the loop or code is running and then at the point that the varaiable startTime (for example) is the value I want I then write
// startTime = startTimestamp ??

// intermediate variables: startTimestamp, stopTimestamp, timeClocked

// define timers start function
function start_stop() {

    // reset all intermediate variables too 0

    // ??? might need to handle this part in python ??? create new log id with the appropriate user_id and timer_id (might need a function to check what the current timers id should be)

    // get current timestamp and hold in startTimestamp variable
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

// define timers reset function
function reset() {

    // reset start all intermediate variable to 0

    clearInterval(timer);
    elapsedTime = 0;
    startTime = 0;
    display.textContent = "00:00:00:00";
    isRunning = false;
}

// define timers update function
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





// FUNCTIONS



function saveTimerEntry() {
    // get startTimestamp
    // get stopTimestamp
    // get timeClocked = startTimestamp - stopTimestamp

    // send POST request to our flask application for proccessing these intermideate variables: start_timestamp, stop_timestamp, and time-clocked
    if (!isRunning && elapsedTime > 0) {
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
        //WHAT IS FETCH WHAT DOE IT DO!??? /save_timer_entry is the problem. its nmot letting me send fricking data

        // This is where we'll make the AJAX call
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
    function discardTimerEntry() {

        // reset all intermediate variables to 0

    }


    // define selectTimer function
    function selectTimer(timerName) {

        document.getElementById("timer_name").textContent = timerName;

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

    function deleteTimer(timerName) {

        document.getElementById("timer_name").textContent = timerName;

        fetch('/delete_timer', {
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










    /* So here are are questions:

    What kind of time format needs to be generated and stored in our intermediate variables so that is can easily be used within Python Flask?

    Is this strategy of taking the timer and merely adding "data recording features" good?

    How do I actually send data over to the server (AJAX THEY SAY) and, once I do how do I "proccess it in the server with python/flask?

    Observation: apparently I can complete the whole functionality of the timer before I have to send the data to the database
    which is nice because this just means one POST request. I was under the impression that'd I have to have continous complicated communication going back and forth between Java and the database
    but no really I just need to have the user hit "Save" and boom a POST request will get sent.


    Do we have the save button written in html and then it triggers the app.py route and the index.js at the same time???

    */

















    // Maybe interact with the CS50 community on the ethicicy of using Bro Codes tutorial verbatim before you change it.

    /*

    is this AJAX? / How you could send data over to the Flask Application?

    fetch('/saveTimer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    */
