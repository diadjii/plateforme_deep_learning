var slide = new Array("../static/images/imagemasque0.2.jpg",
						"../static/images/imagemasque0.4.jpg", 
						"../static/images/imagemasque0.5.jpg", 
						"../static/images/imagemasque0.6.jpg",
						"../static/images/imagemasque0.8.jpg",
						"../static/images/imagemasque1.0.jpg");
var numero = 0;

function ChangeSlide(sens) {
    numero = numero + sens;
    if (numero < 0)
        numero = slide.length - 1;
    if (numero > slide.length - 1)
        numero = 0;
    document.getElementById("slide").src = slide[numero];
}