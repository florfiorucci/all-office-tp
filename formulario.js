function validarEnviar(){
    parrafo = document.getElementById("error")
    // ANALIZO EL NOMBRE
    if(document.formulario.nombre.value.length <= 3){
        // alert("Ingrese un nombre correcto.")
        document.formulario.nombre.focus()
        parrafo.innerHTML = "Nombre incorrecto."
        return
    }

    // ANALIZO SI SELECCIONÓ DE FORMA CORRECTA I
    if(document.formulario.interes.selectedIndex == 0){
        // alert("Debe seleccionar un motivo de su contacto.")
        document.formulario.interes.focus()
        parrafo.innerHTML = "Seleccion incorrecta."
        return 
    }
    // ANALIZO SI SELECCIONÓ DE FORMA CORRECTA II
    if(document.formulario.motivo.selectedIndex == 0){
        // alert("Debe seleccionar un motivo de su contacto.")
        document.formulario.motivo.focus()
        parrafo.innerHTML = "Seleccion incorrecta."
        return 
    }
    parrafo.innerHTML = "Gracias por completar el formulario!"
    document.formulario.submit()
}