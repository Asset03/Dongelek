const car_interested = document.getElementById("car_id").getAttribute("car")
const form_email = document.querySelector('.email-form');
const btn_email = document.querySelector('.my-btn-email');
const csrf_email = document.getElementsByName('csrfmiddlewaretoken')
const user_email = document.querySelector(".seller_info").getAttribute("seller-email")
const user_username = document.querySelector(".seller_info").getAttribute("seller-username")

btn_email.addEventListener('click', event=>{
    form_email.addEventListener('submit', e=>{
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/send-email/',
            data:{
                'csrfmiddlewaretoken': csrf_email[0].value,
                'car_interested':car_interested,
                'seller_email': user_email,
                'seller_username': user_username,
            },
            success:function(response){
            },
            error:function(error){
            }
        })
    })
})