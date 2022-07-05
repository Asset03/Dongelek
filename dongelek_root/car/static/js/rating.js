
const first = document.getElementById("one");
const second = document.getElementById("two");
const third = document.getElementById("three");
const fourth = document.getElementById("four");
const fifth = document.getElementById("five");

const ratings = [first, second, third, fourth, fifth] 

let star_initial = first.src;
let star_over = first.getAttribute("data-original");

const form = document.querySelector('.rate-form');

const car = document.getElementById("car_id").getAttribute("car")
const csrf = document.getElementsByName('csrfmiddlewaretoken')


ratings.forEach(item=> item.addEventListener('mouseover', event=>{
    let id = event.target.id
    switch(id){
        case "one": fillTheStar(1); return;
        case "two": fillTheStar(2); return;
        case "three": fillTheStar(3); return;
        case "four": fillTheStar(4); return;
        case "five": fillTheStar(5); return;
    }
}))
ratings.forEach(item=> item.addEventListener('mouseout', event=>{
    let id = event.target.id
    switch(id){
        case "one": strokeTheStars(1); return;
        case "two": strokeTheStars(2); return;
        case "three": strokeTheStars(3); return;
        case "four": strokeTheStars(4); return;
        case "five": strokeTheStars(5); return;
    }
}))

ratings.forEach(item=> item.addEventListener('click', event=>{
    let id = event.target.id
    let rating = getNumericValue(id)
    form.addEventListener('submit', e =>{
        e.preventDefault()

        $.ajax({
            type: 'POST',
            url: '/rate-car/',
            data:{
                'csrfmiddlewaretoken': csrf[0].value,
                'car': car,
                'rating': rating,
            },
            success: function(response){
                location.reload()
            },
            error: function(error){
            }
        })
    })
}))

function fillTheStar(ind){
    for(let i = 0; i < ind; i++){
        ratings[i].src = star_over;
    }
}
function strokeTheStars(ind){
    for(let i = 0; i < ind; i++){
        ratings[i].src = star_initial;
    }
}
function getNumericValue(string){
    switch(string){
        case 'one': return 1;
        case 'two': return 2;
        case 'three': return 3;
        case 'four': return 4;
        case 'five': return 5;
    }
    return 0;
}