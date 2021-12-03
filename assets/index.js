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

function init_train() {
    var elInit = document.querySelector('.init')
    var s = `<button role="button" onclick="init_exam('yam')">Yamaut</button>`
    s+=` <button role="button" onclick="init_exam('mec')">Machine</button>`
    s+=` <button role="button" onclick="init_exam('equ')">Navigation</button>`
    
    elInit.innerHTML=s
    elInit.style.display='block'
}

function init_sim() {
    var elInit = document.querySelector('.init')
    var s = `<button role="button" onclick="init_sim_exam('yam')">Yamaut</button>`
    s+=` <button role="button" onclick="init_sim_exam('mec')">Machine</button>`
    s+=` <button role="button" onclick="init_sim_exam('equ')">Navigation</button>`
    
    elInit.innerHTML=s
    elInit.style.display='block'

}

function random(obj) {
    var keys = Object.keys(obj)
    if (keys.length === 0) {
        return null
    }
    var prop = keys[Math.floor(Math.random() * keys.length)]

    return prop
}

function choice(answer, selected) {
    var game_exam = window[`game_${gType}`]
    var exam = window[`q_${gType}`]
    var count_exam = window[`count_${gType}`]
    var mandat = window[`mandatory_${gType}`]

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
        var elCount = document.querySelector('.text')
        elCount.innerHTML = `מספר תשובות נכונות ברצף: ${count['success_count']}/2`
        var elP= document.querySelector('.text-warning1')
        elP.innerHTML=`${count['success_count']/2 *100}%`
        if (count['success_count'] === 2) {
            delete exam[selected];
            var index = mandat.indexOf(parseInt(selected));
            if (index !== -1) {
                mandat.splice(index, 1);
            }

            count_exam['c']++
            if (count_exam['c'] === count_exam['total']) {
                var elem = document.querySelector('.heading1')
                elem.innerHTML = `You are completed the exam!`
                elem = document.querySelector('.text-success')
                elem.innerHTML=`100%`

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
    var elCont=document.querySelector('.container-fluid')
    elCont.style.display="block"
    if (gType === type) {
        return
    }
    gType = type
    init_next()
    var elb = document.querySelector(".next")
    elb.style.display = ""
    var elb = document.querySelector(".next_must")
    elb.style.display = ""
}

function init_must_next()
{
    var mandat = window[`mandatory_${gType}`]
    if (mandat.length === 0) {
        return
    }

    var selected = mandat[Math.floor(Math.random() * mandat.length)]

    render_question(`${selected}`, true)
}


function init_next() {
    if (gType === null) {
        return
    }

    var exam = window[`q_${gType}`]

    var selected = random(exam)
    if (selected === null) {
        return
    }

    render_question(selected, true)
}

function imgError(selected)
{
    render_question(selected, false)
}

function render_question(selected, q_image)
{
    var exam = window[`q_${gType}`]
    var count_exam = window[`count_${gType}`]
    var game_exam = window[`game_${gType}`]
    var mandat = window[`mandatory_${gType}`]

    var que = exam[selected]
    var should_mark = false

    var elQues = document.querySelector('.heading1')
    elQues.innerHTML = `שאלות: ${count_exam['c']}/${count_exam['total']}`
    var elP= document.querySelector('.text-success')
    elP.innerHTML=`${count_exam['c']/count_exam['total']*100}%`


    var elCount = document.querySelector('.text')
    elCount.innerHTML = `מספר תשובות נכונות ברצף: ${game_exam[selected]["success_count"]}/2`
    elP=document.querySelector('.text-warning1')
    elP.innerHTML=`${game_exam[selected]['success_count']/2 * 100}%`

    var elQs = document.querySelector('.question')
    var s = ""
    for (let i = 0; i < mandat.length; i++) {
        var number = mandat[i];
        if (selected === `${number}`) {
            should_mark = true
        }
    }



    var arr = ['1', '2', '3', '4']
    for (var i = 0; i < 4; i++) {
        s = s + `<button class="css-${arr[i]}" onclick="choice('${arr[i]}', ${selected})">${arr[i]}. ${que['opts'][arr[i]]}</button>`
        s = s + "<br><br>"

    }

    s += `<img src="assets/images/${gType}/always.jpg"></img>`

    if (q_image){
        s += `<img src="assets/images/${gType}/${selected}.jpg" onerror="imgError('${selected}')" ></img>`
    }
    
   
    var elquiz = document.querySelector('.quiz')
    var quiz = ''
    var elBathen = document.querySelector('.modal-header')
    var m = ""

    if (should_mark) {
        m =  m + `<h2>(*) ${que['q']}</h2>`
    }
    else {
        m =  m + `<h2>${que['q']}</h2>`
    }
    

    var arr = ['1', '2', '3', '4']
    for (var i = 0; i < 4; i++) {
        quiz = quiz + `<button class="css-${arr[i]}" onclick="choice('${arr[i]}', ${selected})">${arr[i]}. ${que['opts'][arr[i]]}</button>`
        quiz = quiz + "<br><br>"

    }

    quiz += `<img src="assets/images/${gType}/always.jpg"></img>`

    if (q_image){
        quiz += `<img src="assets/images/${gType}/${selected}.jpg" onerror="imgError('${selected}')"></img>`
    }

    elBathen.innerHTML = m;
    elquiz.innerHTML=quiz

}


/*console.log(window[`q_${type}`])
console.log(window[`a_${type}`])
console.log(window[`game_${type}`])
console.log(type);
*/
