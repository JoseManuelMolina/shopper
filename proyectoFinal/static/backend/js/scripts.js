function botonDropdown(id) {

    if (id == "crear") {
        if (document.getElementById("mas-crear").classList.contains("activo")) {
            document.getElementById("mas-crear").classList.remove("activo");
            document.getElementById("mas-crear").classList.remove("rotate-90-ccw");
            document.getElementById("crearDropdown").classList.remove("mostrarDropdown");
            document.getElementById("mas-crear").classList.add("rotate-90-cw");
            document.getElementById("crearDropdown").classList.add("esconderDropdown");
        } else {
            document.getElementById("mas-crear").classList.add("activo");
            document.getElementById("mas-crear").classList.remove("rotate-90-cw");
            document.getElementById("crearDropdown").classList.remove("esconderDropdown");
            document.getElementById("mas-crear").classList.add("rotate-90-ccw");
            document.getElementById("verDropdown").classList.add("mostrarDropdown");
        }
    }else{
        if (document.getElementById("mas-ver").classList.contains("activo")) {
            document.getElementById("mas-ver").classList.remove("activo");
            document.getElementById("mas-ver").classList.remove("rotate-90-ccw");
            document.getElementById("verDropdown").classList.remove("mostrarDropdown");
            document.getElementById("mas-ver").classList.add("rotate-90-cw");
            document.getElementById("verDropdown").classList.add("esconderDropdown");
        } else {
            document.getElementById("mas-ver").classList.add("activo");
            document.getElementById("mas-ver").classList.remove("rotate-90-cw");
            document.getElementById("verDropdown").classList.remove("esconderDropdown");
            document.getElementById("mas-ver").classList.add("rotate-90-ccw");
            document.getElementById("verDropdown").classList.add("mostrarDropdown");
        }
    }

}

function checkboxBackend() {
    var checkbox = document.getElementById("checkboxCrear");
    
    if(checkbox.checked == true){ 
        $('#checkboxCrear').attr('checked', false);
        console.log('activo');
    }
    else{ 
        $('#checkboxCrear').attr('checked', true);
        console.log('inactivo');
    }
}