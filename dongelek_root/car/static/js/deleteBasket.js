const form_basket_delete = document.querySelector('.cart-form-delete');
const btn_basket_delete = document.querySelector('.my-btn-cart-delete');
const csrf_basket_delete = document.getElementsByName('csrfmiddlewaretoken')

btn_basket_delete.addEventListener('click', event=>{
    form_basket_delete.addEventListener('submit', e=>{
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '/delete-from-cart/',
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