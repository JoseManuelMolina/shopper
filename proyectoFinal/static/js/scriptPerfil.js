var botonSubmit = document.getElementById("guardarPerfil")

var contraseña = document.getElementById("id_password");
var contraseñaUsuario = contraseña.val()
var contraseñaNueva = document.getElementById("contraseñaNueva");
var repetirContraseña = document.getElementById("repetirContraseña");

botonSubmit.onclick = function(){
    var fecha = "";

    var genero = document.getElementById("id_genero");
    var generoHombre = document.getElementById("generoHombre");
    var generoMujer = document.getElementById("generoMujer");

    if(generoHombre.checked){
        genero.value = 0
    }else if(generoMujer.checked){
        genero.value = 1
    }
};  

contraseñaNueva.onchange  = function() {
    console.log('contraseñaUsuario');
    if(contraseñaNueva == '' && repetirContraseña == ''){
        contraseña.value = contraseñaUsuario
    }else if(contraseñaNueva != '' && repetirContraseña != '' && contraseñaNueva == repetirContraseña){
        contraseña.value = contraseñaNueva.val()
    }
};