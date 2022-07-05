const photos = document.getElementsByClassName('photos');
let mainImage = document.getElementById('main_image');
covers = [];
for(let i = 0; i < photos.length; i++){
    covers.push(photos[i]);
}
covers.forEach(element => element.addEventListener('mouseover', event=>{
    mainImage.src = event.target.src;
}));