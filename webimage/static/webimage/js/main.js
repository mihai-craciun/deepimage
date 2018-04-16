setSquarePhotos = () => {$('img.card-img-top.gallery-img').height($('img.card-img-top.gallery-img').width())}
$(window).ready(setSquarePhotos)
$(window).resize(setSquarePhotos)