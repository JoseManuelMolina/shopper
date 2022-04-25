function botonDropdown(id) {

    if (id == "crear") {
        if (document.getElementById("mas-crear").classList.contains("display-none")) {
            document.getElementById("mas-crear").classList.remove("display-none");
            document.getElementById("menos-crear").classList.add("display-none");
            document.getElementById("crearDropdown").classList.add("display-none");
        } else {
            document.getElementById("mas-crear").classList.add("display-none");
            document.getElementById("menos-crear").classList.remove("display-none");
            document.getElementById("crearDropdown").classList.remove("display-none");
        }
    }else{
        if (document.getElementById("mas-ver").classList.contains("display-none")) {
            document.getElementById("mas-ver").classList.remove("display-none");
            document.getElementById("menos-ver").classList.add("display-none");
            document.getElementById("verDropdown").classList.add("display-none");
        } else {
            document.getElementById("mas-ver").classList.add("display-none");
            document.getElementById("menos-ver").classList.remove("display-none");
            document.getElementById("verDropdown").classList.remove("display-none");
        }
    }

}