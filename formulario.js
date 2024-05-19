function validarEnviar(){
    parrafo = document.getElementById("error")
    // ANALIZO EL NOMBRE
    if(document.formulario.nombre.value.length <= 2){
        // alert("Ingrese un nombre correcto.")
        document.formulario.nombre.focus()
        parrafo.innerHTML = "Nombre incorrecto."
        return
    }
    }
    // ANALIZO EL CELULAR
    let Celentero = parseInt(document.formulario.celular.value)
    if(isNaN(Celentero)){
        // alert("Tiene que ingresar un número valido en el DNI.")
        document.formulario.celular.focus()
        parrafo.innerHTML = "Número incorrecto."
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