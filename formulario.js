function validarEnviar(){
    parrafo = document.getElementById("error")
    if(document.formulario.nombre.value.length <= 2){
        document.formulario.nombre.focus()
        parrafo.innerHTML = "Escriba su nombre completo."
        return
    }
    let ExpReg =  /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/
    let validez = ExpReg.test(document.formulario.correo.value);
    if(validez == false){
        document.formulario.correo.focus()
        parrafo.innerHTML = "Correo electrónico incorrecto."
        return
    }
    let NumeroEntero = parseInt(document.formulario.celular.value)
    if(isNaN(NumeroEntero)){
        document.formulario.celular.focus()
        parrafo.innerHTML = "Número de telefono incorrecto."
        return
    }
    if(document.formulario.interes.selectedIndex == 0){
        document.formulario.interes.focus()
        parrafo.innerHTML = "Elija el mobiliario de interés."
        return 
    }
    if(document.formulario.motivo.selectedIndex == 0){
        document.formulario.motivo.focus()
        parrafo.innerHTML = "Elija el motivo de su consulta."
        return 
    }
    parrafo.innerHTML = "Gracias por completar el formulario. A la brevedad nos pondremos en contacto con usted."
    document.formulario.submit()
}