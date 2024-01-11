// var imageElement = document.getElementById('images');

// function changeImage() {
//     imageElement.style.animation = 'fade-out 1s';
//     imageElement.style.opacity = 0;

//     setTimeout(function() {
//         imageElement.src = 'images/NeXicon V3_transparent.png';
//         imageElement.style.animation = 'fade 1s';
//         imageElement.style.opacity = 1;
//     }, 1000);
// }

// setInterval(changeImage, 5000); // Ubah gambar setiap 5 detik (5000 ms)

var images = [
    '/static/images/RaSa DARK VER.png',
    '/static/images/NeXicon V3_transparent.png',

  ];
  var imageIndex = 0;
  var imageElement = document.getElementById('images');
  imageElement.style.transition = 'opacity 2s';
  
  function changeImage() {
    imageElement.style.opacity = 0;
  
    setTimeout(function() {
      imageIndex = (imageIndex + 1) % images.length;
      imageElement.src = images[imageIndex];
      imageElement.style.opacity = 1;
    }, 1700);
  }
  
  setInterval(changeImage, 6000); // Ubah gambar setiap 5 detik (5000 ms)
  
  