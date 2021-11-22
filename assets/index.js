console.log(q_equ)

var gType = null
var count_yam = {
    "c": 0,
    "total": Object.keys(q_yam).length
}
var count_mec = {
    "c": 0,
    "total": Object.keys(q_mec).length
}
var count_equ = {
    "c": 0,
    "total": Object.keys(q_equ).length
}

function random(obj) {
    var keys = Object.keys(obj)
    if (keys.length === 0) {
        return null
    }
    var prop = keys[Math.floor(Math.random() * keys.length)]
    console.log(prop)
    return prop
}

function choice(answer, selected) {
    var game_exam = window[`game_${gType}`]
    var exam = window[`q_${gType}`]
    var count_exam = window[`count_${gType}`]

    var count = game_exam[selected]

    document.querySelector('.css-1').disabled = true
    document.querySelector('.css-2').disabled = true
    document.querySelector('.css-3').disabled = true
    document.querySelector('.css-4').disabled = true
    var correct = `${exam[selected]['ans']}`
    if (answer === correct) {
        var element = document.querySelector(`.css-${correct}`)
        element.style.color = "green"
        count['success_count']++
        var elCount = document.querySelector('.count')
        elCount.innerHTML = `count ${count['success_count']}/2`
        if (count['success_count'] === 2) {
            delete exam[selected];
            count_exam['c']++
            if (count_exam['c'] === count_exam['total']) {
                var elQues = document.querySelector('.questions')
                elQues.style.color = "green"
                elQues.innerHTML = `${count_exam['c']}/${count_exam['total']} you are completed the exam!`
            }
        }
    } else {
        var element = document.querySelector(`.css-${answer}`)
        element.style.color = "red"

        var element = document.querySelector(`.css-${correct}`)
        element.style.color = "green"


    }
}

function init_exam(type) {
    if (gType === type) {
        return
    }
    gType = type
    init_next()
    var elb = document.querySelector(".next")
    elb.style.display = ""


}


function init_next() {
    if (gType === null) {
        return
    }

    var should_mark = false

    var exam = window[`q_${gType}`]
    var count_exam = window[`count_${gType}`]
    var game_exam = window[`game_${gType}`]
    var mandat = window[`mandatory_${gType}`]
    var selected = random(exam)
    if (selected === null) {
        return
    }
    var que = exam[selected]

    var elQues = document.querySelector('.questions')
    elQues.innerHTML = `questions ${count_exam['c']}/${count_exam['total']}`
    var elCount = document.querySelector('.count')
    elCount.innerHTML = `count ${game_exam[selected]["success_count"]}/2`

    var elQs = document.querySelector('.question')
    var s = ""
    for (let i = 0; i < mandat.length; i++) {
        var number = mandat[i];
        if (selected === `${number}`) {
            should_mark = true
        }
    }

    if (should_mark) {
        s = s + `<h3>*${que['q']}</h3>`
    }
    else {
        s = s + `<h3>${que['q']}</h3>`
    }

    var arr = ['1', '2', '3', '4']
    for (var i = 0; i < 4; i++) {
        s = s + `<button class="css-${arr[i]}" onclick="choice('${arr[i]}', ${selected})">${arr[i]}. ${que['opts'][arr[i]]}</button>`
        s = s + "<br><br>"

    }

    s += `<img src="assets/images/${gType}/${selected}.jpg"></img>`

    s += `<img src="assets/images/${gType}/always.jpg" alt=""></img>`

    elQs.innerHTML = s
}




/*console.log(window[`q_${type}`])
console.log(window[`a_${type}`])
console.log(window[`game_${type}`])
console.log(type);
*/
