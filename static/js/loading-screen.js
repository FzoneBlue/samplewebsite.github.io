// window.addEventListener('load', function() {
//     var loadingScreen = document.getElementById('loading-screen');
//     var content = document.getElementById('content');
  
//     // Simulasikan waktu loading
//     setTimeout(function() {
//       loadingScreen.classList.add('hidden');
//       content.classList.add('loaded');
//     }, 3000); // Ganti dengan durasi loading yang diinginkan (dalam milidetik)
//   });
  

document.addEventListener('DOMContentLoaded', function() {
    var preloader = document.querySelector('.preloader');
    var content = document.querySelector('.content');
  
    setTimeout(function() {
      preloader.classList.add('hidden');
      content.style.display = 'block';
    }, 3000); // Mengatur waktu loading menjadi 5000ms (5 detik)
  });
  