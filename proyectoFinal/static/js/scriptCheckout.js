var direcciones = document.getElementsByClassName('direccionesCheckout');

function seleccionarDireccion(event) {
    for (let i = 0; i < direcciones.length; i++) {
        direcciones[i].classList.remove('direccionSeleccionada')
    }
    event.classList.add('direccionSeleccionada')
}

document.getElementById('checkoutShippingAddress').onclick  = function(){
    for (let i = 0; i < direcciones.length; i++) {
        direcciones[i].classList.remove('direccionSeleccionada')
    }
}

var estandar = document.getElementById('checkoutShippingStandard');
var express = document.getElementById('checkoutShippingExpress');

var estandarValor = document.getElementById('valorEnvioEstandar').textContent;
var expressValor = document.getElementById('valorEnvioExpress').textContent;

var gastosEnviosSpan = document.getElementById('gastosEnvioSpan');

var precioSpan = document.getElementById('precioSpan');
var precioTotalSpan = document.getElementById('precioTotalSpan');

estandar.click();

estandar.onclick  = function(){
    if(estandarValor == 'Gratis'){
        gastosEnviosSpan.innerHTML = '<i>'+estandarValor+'</i>';
    }else{
        gastosEnviosSpan.innerHTML = estandarValor;
    }
    calcularGastosEnvios();
};

express.onclick  = function(){
    gastosEnviosSpan.innerHTML = expressValor;
    calcularGastosEnvios();
};

function calcularGastosEnvios(){
    if(gastosEnviosSpan.innerHTML == '<i>Gratis</i>'){
        precioTotalSpan.innerHTML = precioSpan.textContent
    }else if(gastosEnviosSpan.innerHTML == '15 €'){
        precioValores = precioSpan.textContent.split(" ");
        gastosDeEnvioValores = gastosEnviosSpan.textContent.split(" ");
        precioTotalSpan.innerHTML = parseInt(precioValores[0])+parseInt(gastosDeEnvioValores[0]) + ' €';
    }else{
        precioValores = precioSpan.textContent.split(" ");
        gastosDeEnvioValores = gastosEnviosSpan.textContent.split(" ");
        precioTotalSpan.innerHTML = parseInt(precioValores[0])+parseInt(gastosDeEnvioValores[0]) + ' €';
    }
}