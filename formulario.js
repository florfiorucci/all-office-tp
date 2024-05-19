function validarEnviar(){
    parrafo = document.getElementById("error")
    // ANALIZO EL NOMBRE
    if(document.formulario.nombre.value.length <= 2){
        // alert("Ingrese un nombre correcto.")
        document.formulario.nombre.focus()
        parrafo.innerHTML = "Nombre incorrecto."
        return
    }
    // ANALIZO LA EDAD
    let edadEntera = parseInt(document.formulario.edad.value)
    if(isNaN(edadEntera)){
        // alert("Tiene que ingresar un número valido en la edad.")
        document.formulario.edad.focus()
        parrafo.innerHTML = "Edad incorrecta."
        return
    }
    else{
        if(edadEntera < 18 || edadEntera > 65){
            // alert("Tiene que ser mayor de edad o tener menos de 65 años.")
            document.formulario.edad.focus()
            parrafo.innerHTML = "Edad incorrecta."
            return 
        }
    }
    // ANALIZO EL DNI
    let DNIentero = parseInt(document.formulario.dni.value)
    if(isNaN(DNIentero)){
        // alert("Tiene que ingresar un número valido en el DNI.")
        document.formulario.dni.focus()
        parrafo.innerHTML = "DNI incorrecto."
        return
    }
    else{
        if(document.formulario.dni.value.length != 8){
            // alert("El dni tiene que tener 8 numeros.")
            document.formulario.dni.focus()
            parrafo.innerHTML = "DNI incorrecto."
            return 
        }
    }
    // ANALIZO SI SELECCIONÓ DE FORMA CORRECTA
    if(document.formulario.interes.selectedIndex == 0){
        // alert("Debe seleccionar un motivo de su contacto.")
        document.formulario.interes.focus()
        parrafo.innerHTML = "Seleccion incorrecta."
        return 
    }

    parrafo.innerHTML = "Gracias por completar el formulario!"
    document.formulario.submit()
}