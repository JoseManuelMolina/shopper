let arrayCirculos = document.getElementsByClassName('colorCircle');

arrayCirculos.forEach(circulo => {
    //console.log(circulo.getAttribute('data-color'));
    circulo.style.backgroundColor = circulo.getAttribute('data-color');
});

let arrayColores = document.getElementsByClassName('colores');

arrayColores.forEach(label => {
    label.addEventListener("click", marcarDesmarcar);
});

function marcarDesmarcar(){
    if(this.hasAttribute('checked')){
        this.removeAttribute('checked');
        this.classList.remove('colorChecked');
    }else{
        this.setAttribute('checked','');
        this.classList.add('colorChecked');
    }
}