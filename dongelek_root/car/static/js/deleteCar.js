const deleteButton = document.getElementsByClassName('delete_button');
const form = document.getElementById('delete-form');
const csrf = document.getElementsByName('csrfmiddlewaretoken');

deleteButtons = [];
for(let i = 0; i < deleteButton.length; i++){
    deleteButtons.push(deleteButton[i]);
}

deleteButtons.forEach(element=> element.addEventListener('click', event=>{
    id = event.target.id;
    form.addEventListener('submit', e=>{
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/delete-car/',
            data:{
                'csrfmiddlewaretoken':csrf[0].value,
                'car': id,
            },
            success: function(response){
                document.location.reload();
            },
            error: function(error){
                document.location.reload();
            },
        })
    });
}));