var selects = document.querySelectorAll('.cantidadProducto')

for (let i = 0; i < selects.length; i++) {
    cantidad = selects[i].options[0].value;
    var numero = 1;

    if (cantidad == 1){
        for (let e = 0; e < 6; e++) {
            var opt = document.createElement("option");
            valor = parseInt(cantidad)+numero
            opt.value = valor;
            opt.text = valor;

            selects[i].appendChild(opt);
            numero++;
        }
    } else if (cantidad == 2){
        for (let e = 0; e < 6; e++) {
            if(e<1){
                var opt = document.createElement("option");
                valor = parseInt(cantidad)-numero
                opt.value = valor;
                opt.text = valor;

                selects[i].prepend(opt);
            }else{
                var opt = document.createElement("option");
                valor = parseInt(cantidad)+numero
                opt.value = valor;
                opt.text = valor;

                selects[i].appendChild(opt);
                numero++;
            }
        }
    } else if (cantidad == 3){
        for (let e = 0; e < 6; e++) {
            if(e<1){
                var opt = document.createElement("option");
                valor = parseInt(cantidad)-numero-1
                opt.value = valor;
                opt.text = valor;

                selects[i].insertBefore(opt, selects[i].children[0]);
            }else if(e<2){
                var opt = document.createElement("option");
                valor = parseInt(cantidad)-numero
                opt.value = valor;
                opt.text = valor;

                selects[i].insertBefore(opt, selects[i].children[1]);
            }else{
                var opt = document.createElement("option");
                valor = parseInt(cantidad)+numero
                opt.value = valor;
                opt.text = valor;

                selects[i].appendChild(opt);
                numero++;
            }
        }
    } else if (cantidad > 3){
        for (let e = 0; e < 6; e++) {
            if(e<1){
                var opt = document.createElement("option");
                valor = parseInt(cantidad)-numero-2
                opt.value = valor;
                opt.text = valor;

                selects[i].insertBefore(opt, selects[i].children[0]);
            }else if(e<2){
                var opt = document.createElement("option");
                valor = parseInt(cantidad)-numero-1
                opt.value = valor;
                opt.text = valor;

                selects[i].insertBefore(opt, selects[i].children[1]);
            }else if(e<3){
                var opt = document.createElement("option");
                valor = parseInt(cantidad)-numero
                opt.value = valor;
                opt.text = valor;

                selects[i].insertBefore(opt, selects[i].children[2]);
            }else{
                var opt = document.createElement("option");
                valor = parseInt(cantidad)+numero
                opt.value = valor;
                opt.text = valor;

                selects[i].appendChild(opt);
                numero++;
            }
        }
    }
}