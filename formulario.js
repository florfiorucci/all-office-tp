function validarEnviar(){
    parrafo = document.getElementById("error")
    if(document.formulario.nombre.value.length <= 2){
        document.formulario.nombre.focus()
        parrafo.innerHTML = "Nombre incorrecto."
        return
    }
    ExpReg = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
    validez = ExpReg.test(correo);
    if(document.formulario.correo.value == validez == false){
        document.formulario.correo.focus()
        parrafo.innerHTML = "Correo incorrecto."
        return
    }
    let NumeroEntero = parseInt(document.formulario.celular.value)
    if(isNaN(NumeroEntero)){
        document.formulario.celular.focus()
        parrafo.innerHTML = "Número incorrecto."
        return
    }
    if(document.formulario.interes.selectedIndex == 0){
        document.formulario.interes.focus()
        parrafo.innerHTML = "Elija una opción."
        return 
    }
    if(document.formulario.motivo.selectedIndex == 0){
        document.formulario.motivo.focus()
        parrafo.innerHTML = "Elija una opción."
        return 
    }
    parrafo.innerHTML = "Gracias por completar el formulario. A la brevedad nos pondremos en contacto con usted."
    document.formulario.submit()
}