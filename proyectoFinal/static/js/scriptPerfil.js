var botonSubmit = document.getElementById("guardarPerfil")

var genero = document.getElementById("id_genero");
var generoHombre = document.getElementById("generoHombre");
var generoMujer = document.getElementById("generoMujer");

var fechaUsuarioInput = document.getElementById("id_fechaNacimiento");
var fechaUsuarioSplit = fechaUsuarioInput.value.split("-");

var fechaUsuarioDia = fechaUsuarioSplit[2];
var fechaUsuarioMes = fechaUsuarioSplit[1];
var fechaUsuarioAño = fechaUsuarioSplit[0];

var fechaDiaInput = document.getElementById("diaNacimiento");
var fechaMesInput = document.getElementById("mesNacimiento");
var fechaAñoInput = document.getElementById("añoNacimiento");


generoMujer.onclick = function() {
    generoHombre.removeAttribute('checked');
    generoMujer.setAttribute('checked', '');
};

generoHombre.onclick = function() {
    generoMujer.removeAttribute('checked');
    generoHombre.setAttribute('checked', '');
};

fechaDiaInput.onchange = function(){

    var fechaDiaValor = $('#diaNacimiento').children("option:selected").val();
    var fechaMesValor = $('#mesNacimiento').children("option:selected").val();
    var fechaAñoValor = $('#añoNacimiento').children("option:selected").val();

    rellenarFecha(fechaDiaValor, fechaMesValor, fechaAñoValor);
};

fechaMesInput.onchange = function(){
    
    var fechaDiaValor = $('#diaNacimiento').children("option:selected").val();
    var fechaMesValor = $('#mesNacimiento').children("option:selected").val();
    var fechaAñoValor = $('#añoNacimiento').children("option:selected").val();

    rellenarFecha(fechaDiaValor, fechaMesValor, fechaAñoValor);
};

fechaAñoInput.onchange = function(){
    
    var fechaDiaValor = $('#diaNacimiento').children("option:selected").val();
    var fechaMesValor = $('#mesNacimiento').children("option:selected").val();
    var fechaAñoValor = $('#añoNacimiento').children("option:selected").val();

    rellenarFecha(fechaDiaValor, fechaMesValor, fechaAñoValor);
};

const esBisiesto = (año) => {
    return (año % 400 === 0) ? true : 
                (año % 100 === 0) ? false : 
                    año % 4 === 0;
};

function borrarOpciones(selectElement) {
    var i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
       selectElement.remove(i);
    }
}

function rellenarFecha(dia, mes, año){
    var añoActual = new Date().getFullYear();

    borrarOpciones(fechaDiaInput);
    borrarOpciones(fechaMesInput);
    borrarOpciones(fechaAñoInput);

    if(mes === '01' || mes === '03' || mes === '05' || mes === '07' || mes === '08' || mes === '10' || mes === '12' ){
        for (let i = 1; i <= 31; i++) {
            if(i<10){
                if(dia === "0"+i.toString()){
                    var opt = document.createElement("option");
    
                    opt.value = "0"+i.toString();
                    opt.text = "0"+i.toString();
                    opt.selected = true;
                }else{
                    var opt = document.createElement("option");
    
                    opt.value = "0"+i.toString();
                    opt.text = "0"+i.toString();
                }
            }else{
                if(dia === i.toString()){
                    var opt = document.createElement("option");
    
                    opt.value = i;
                    opt.text = i.toString();
                    opt.selected = true;
                }else{
                    var opt = document.createElement("option");
    
                    opt.value = i;
                    opt.text = i.toString();
                }
            }
            
            fechaDiaInput.appendChild(opt);
        }
    }else if(mes === '04' || mes === '06' || mes === '09' || mes === '11' ){
        for (let i = 1; i <= 30; i++) {
            if(i<10){
                if(dia === "0"+i.toString()){
                    var opt = document.createElement("option");
    
                    opt.value = "0"+i.toString();
                    opt.text = "0"+i.toString();
                    opt.selected = true;
                }else{
                    var opt = document.createElement("option");
    
                    opt.value = "0"+i.toString();
                    opt.text = "0"+i.toString();
                }
            }else{
                if(dia === i.toString()){
                    var opt = document.createElement("option");
    
                    opt.value = i;
                    opt.text = i.toString();
                    opt.selected = true;
                }else{
                    var opt = document.createElement("option");
    
                    opt.value = i;
                    opt.text = i.toString();
                }
            }

            fechaDiaInput.appendChild(opt);
        }
    }else{
        if(esBisiesto(año)){
            for (let i = 1; i <= 29; i++) {
                if(i<10){
                    if(dia === "0"+i.toString()){
                        var opt = document.createElement("option");
        
                        opt.value = "0"+i.toString();
                        opt.text = "0"+i.toString();
                        opt.selected = true;
                    }else{
                        var opt = document.createElement("option");
        
                        opt.value = "0"+i.toString();
                        opt.text = "0"+i.toString();
                    }
                }else{
                    if(dia === i.toString()){
                        var opt = document.createElement("option");
        
                        opt.value = i;
                        opt.text = i.toString();
                        opt.selected = true;
                    }else{
                        var opt = document.createElement("option");
        
                        opt.value = i;
                        opt.text = i.toString();
                    }
                }
    
                fechaDiaInput.appendChild(opt);
            }
        }else{
            for (let i = 1; i <= 28; i++) {
                if(i<10){
                    if(dia === "0"+i.toString()){
                        var opt = document.createElement("option");
        
                        opt.value = "0"+i.toString();
                        opt.innerHTML = "0"+i.toString();
                        opt.selected = true;
                    }else{
                        var opt = document.createElement("option");
        
                        opt.value = "0"+i.toString();
                        opt.text = "0"+i.toString();
                    }
                }else{
                    if(dia === i.toString()){
                        var opt = document.createElement("option");
        
                        opt.value = i;
                        opt.innerHTML = i.toString();
                        opt.selected = true;
                    }else{
                        var opt = document.createElement("option");
        
                        opt.value = i;
                        opt.text = i.toString();
                    }
                }
    
                fechaDiaInput.appendChild(opt);
            }
        }
    }

    for (let i = 1; i <= 12; i++) {
        if(i<10){
            if(mes === "0"+i.toString()){
                var opt = document.createElement("option");

                opt.value = "0"+i.toString();
                opt.text = "0"+i.toString();
                opt.selected = true;
            }else{
                var opt = document.createElement("option");

                opt.value = "0"+i.toString();
                opt.text = "0"+i.toString();
            }
        }else{
            if(mes === i.toString()){
                var opt = document.createElement("option");

                opt.value = i;
                opt.text = i.toString();
                opt.selected = true;
            }else{
                var opt = document.createElement("option");

                opt.value = i;
                opt.text = i.toString();
            }
        }

        fechaMesInput.appendChild(opt);
    }

    for (let i = 1920; i <= añoActual; i++) {
        if(año === i.toString()){
            var opt = document.createElement("option");

            opt.value = i;
            opt.text = i.toString();
            opt.selected = true;
        }else{
            var opt = document.createElement("option");

            opt.value = i;
            opt.text = i.toString();
        }

        fechaAñoInput.appendChild(opt);
    }
}

function validarFormulario( ){
    var estado = true;
    var estadoGenero = false;
    var estadoContraseña = false;
    var estadoFechaNacimiento = false;

    var genero = document.getElementById("id_genero");
    var generoHombre = document.getElementById("generoHombre");
    var generoMujer = document.getElementById("generoMujer");

    var contraseña = document.getElementById("id_password");
    var contraseñaUsuario = contraseña.value;
    var contraseñaNueva = document.getElementById("contraseñaNueva");
    var repetirContraseña = document.getElementById("repetirContraseña");

    var fechaDiaValor = $('#diaNacimiento').children("option:selected").val();
    var fechaMesValor = $('#mesNacimiento').children("option:selected").val();
    var fechaAñoValor = $('#añoNacimiento').children("option:selected").val();

    if(generoHombre.hasAttribute('checked')){
        genero.value = 0;
        estadoGenero = true;
    }else if(generoMujer.hasAttribute('checked')){
        genero.value = 1;
        estadoGenero = true;
    }

    if(contraseñaNueva.value == '' && repetirContraseña.value == ''){
        contraseña.value = contraseñaUsuario;
        estadoContraseña = true;
    }else if(contraseñaNueva.value != '' && repetirContraseña.value != ''){
        if (contraseñaNueva.value == repetirContraseña.value){
            contraseña.value = contraseñaNueva.value;
            estadoContraseña = true;
        }
    }else if(contraseñaNueva.value != '' && repetirContraseña.value == ''){
        estadoContraseña = false;
    }else if(contraseñaNueva.value == '' && repetirContraseña.value != ''){
        estadoContraseña = false;
    }

    if(fechaDiaValor != fechaUsuarioDia || fechaMesValor != fechaUsuarioMes || fechaAñoValor != fechaUsuarioAño){
        fechaUsuarioInput.value = fechaAñoValor + '-' + fechaMesValor + '-' + fechaDiaValor;
        estadoFechaNacimiento = true;
    }else{
        estadoFechaNacimiento = true;
    }

    if(estadoGenero && estadoContraseña && estadoFechaNacimiento){
        estado = true;
    }

    return estado;
};

rellenarFecha(fechaUsuarioDia, fechaUsuarioMes, fechaUsuarioAño);