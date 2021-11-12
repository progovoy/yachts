var gState = {}
var gA = {}
var gExam = {}

var gCurrenExamType

function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

function init_exam(type) {
    gCurrenExamType = type;

    if (gExam[type] === undefined) {
        gState[type] = window[`game_${type}`];
        gA[type] = window[`a_${type}`];
        gExam[type] = window[`q_${type}`];
    }

    next()
}

function next(){
    var questions = Object.keys(gExam[gCurrenExamType]);
    var question;
    var idx;
     
    idx = Math.floor(Math.random() * questions.length);
    q_number = questions[idx];
    question = gExam[gCurrenExamType][q_number];

    var elem = document.getElementById("exam");
    var innerContent = `<button role="button" onclick="next(this)">Next</button><br><br>`;
    innerContent += `<p>${question['q']}</p>`;
    for (const [key, value] of Object.entries(question['opts'])) {
        innerContent += `<button role="button" onclick="answer(${q_number}, this)" id=${key} style="width: 45px; height: 20px; text-align: center; color: white; background: #23b7e5; font-size: 13px; border-color: #23b7e5; border-radius:2px; padding: 10px; ">${key}</button>`
        innerContent += `<label id=${key}-lbl>${value}</label><br>`
    }

    innerContent += `<br>`

    elem.innerHTML = innerContent;

    var el_status = document.getElementById("status")

    el_status.innerHTML = `Question Num: ${q_number} <br>`
    el_status.innerHTML += `Total: ${Object.keys(gExam[gCurrenExamType]).length} <br>`
    el_status.innerHTML += `Score: ${gState[gCurrenExamType][q_number]["success_count"]} / 2<br>`;
}

function answer(q_num, b){
    if (gExam[gCurrenExamType][q_num] === undefined){
        return;
    }

    question = gExam[gCurrenExamType][q_num];
    for (const [key, value] of Object.entries(question['opts'])) {
        document.getElementById(key).disabled = true;
    }

    var choice = b.innerText;

    var el_status = document.getElementById("status")

    el_status.innerHTML = `Question Num: ${q_num} <br>`
    el_status.innerHTML += `Total: ${Object.keys(gExam[gCurrenExamType]).length} <br>`
    
    if (choice === gExam[gCurrenExamType][q_num]["ans"]) {
        gState[gCurrenExamType][q_num]["success_count"] += 1
        document.getElementById(choice).style.color = 'green'
        document.getElementById(`${choice}-lbl`).style.color = 'green'
    }
    else {
        gState[gCurrenExamType][q_num]["success_count"] = 0
        document.getElementById(choice).style.color = 'red'
        document.getElementById(`${choice}-lbl`).style.color = 'red'
    }

    el_status.innerHTML += `Score: ${gState[gCurrenExamType][q_num]["success_count"]} / 2<br>`;

    if (gState[gCurrenExamType][q_num]["success_count"] === 2) {
        delete gExam[gCurrenExamType][q_num];
        delete gState[gCurrenExamType][q_num];
        delete gA[gCurrenExamType][q_num];
    }

    if (Object.keys(gExam[gCurrenExamType]).length === 0) {
        el_status.innerHTML += `<p>You are done</p><br>`;
    }
}
