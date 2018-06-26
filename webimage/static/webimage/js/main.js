setSquarePhotos = () => {$('img.card-img-top.gallery-img').height($('img.card-img-top.gallery-img').width())}
$(window).ready(setSquarePhotos)
$(window).resize(setSquarePhotos)
let loadingSpinner = (button) => {
    $(button).children().addClass('fa-spinner').addClass('fa-spin').removeClass('fa-tags')
}