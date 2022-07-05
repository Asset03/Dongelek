function changeValute(){
    let prices = document.getElementsByClassName("price")
    let currency = document.getElementsByClassName("currency")
    let preValute = document.querySelector(".currency").innerHTML
    let preValuteNominal = "";
    let preValuteValue = "";
    let newValute = document.getElementById("currency_select").value;
    let newValuteName = "";
    let newValuteValue = ""
    let newValuteNominal = ""
    for(let i = 9; newValute[i] != ','; i++){
        newValuteValue += newValute[i];
    }
    let indexOfNominal = newValute.indexOf('"nominal"') + 10
    for(let i = indexOfNominal; newValute[i] != ','; i++){
        newValuteNominal += newValute[i];
    }
    let indexOfName = newValute.indexOf('"name"') + 7
    for(let i = indexOfName; newValute[i] != '}'; i++){
        newValuteName += newValute[i];
    }
    let options = document.getElementsByTagName("option")
    for(let i = 0; i < options.length; i++){
        if(options[i].innerHTML == preValute){
            preValuteNominal = options[i].getAttribute("nominal");
            preValute = options[i].value;
            for(let i = 9; preValute[i] != ','; i++){
                preValuteValue += preValute[i];
            }
            break;
        }
    }
    console.log(newValuteName)
    console.log(newValuteNominal)
    console.log(newValuteValue)
    console.log(preValuteNominal)
    console.log(preValuteValue)
    let converter = parseFloat(newValuteValue) / parseInt(newValuteNominal) * preValuteNominal / preValuteValue;
    console.log(converter)
    for(let i = 0; i < prices.length; i++){
        prices[i].innerHTML = Math.round(parseInt(prices[i].innerHTML) / converter);
        currency[i].innerHTML = newValuteName;
    }
}