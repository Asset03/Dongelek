const car_basket = document.getElementById("car_id").getAttribute("car")
const form_basket = document.querySelector('.cart-form');
const btn_basket = document.querySelector('.my-btn-cart');
const csrf_basket = document.getElementsByName('csrfmiddlewaretoken')

btn_basket.addEventListener('click', event=>{
    form_basket.addEventListener('submit', e=>{
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/add-to-cart/',
            data:{
                'csrfmiddlewaretoken': csrf_basket[0].value,
                'car_basket':car_basket
            },
            success:function(response){
                location.reload()
            },
            error:function(error){
            }
        })  
    })   
})