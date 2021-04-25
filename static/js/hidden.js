var form = document.getElementById('form-direct');
var formDelivery = document.getElementById('delivery');
var formComunas = document.getElementById('comunas');
var spanTotal = document.getElementById('total');
var Subtotal = document.getElementById('subtotal').value;
var formStreet = document.getElementById('id_street_address');
var formApartment = document.getElementById('id_apartment_address');
var formPostalCode = document.getElementById('id_postal_code');
var formDescription = document.getElementById('id_description');
var fact = document.querySelector('total-price');
var enviar = document.getElementById('totalenv');
var liDelivery = document.getElementById('deli-li');
var ValorDelivery = document.getElementById('deli');
var selectComunas = document.getElementById('selectComuna');
$(document).ready(function(){
    console.log(data)
    formComunas.style.display = 'none';
    form.style.display = 'none';
    spanTotal.innerHTML='$'+Subtotal;
    formStreet.value = 'retiro';
    formApartment.value = 'retiro';
    formPostalCode.value = 'retiro';
    formDescription.value = 'retiro';
    for (var i in data){
        console.log(data[i].fields['precio'])
        selectComunas.innerHTML += 
        `<option>` + data[i].fields['nombre'] + `</option>`
    }

    enviar.value = Subtotal;

    $('#select').on('change',function(){

        var selectValor = $(this).val();
        if(selectValor == 'retiro'){
            formComunas.style.display = 'none';
            form.style.display = 'none';
            spanTotal.innerHTML='$'+Subtotal;
            enviar.value = Subtotal;
            liDelivery.style.display = 'none';
            ValorDelivery.innerHTML= 0;
        };
        if(selectValor == 'starken'){
            formComunas.style.display = 'block';
            form.style.display = 'block';
            spanTotal.innerHTML='$'+Subtotal;
            enviar.value = Subtotal;
            liDelivery.style.display = 'none';
            ValorDelivery.innerHTML= 0;
            formStreet.value = '';
            formApartment.value = '';
            formPostalCode.value = '';
            formDescription.value = '';
            delivery = 0
        };
        if(selectValor == 'delivery'){
            formComunas.style.display = 'block';
            form.style.display = 'block';
            formStreet.value = '';
            formApartment.value = '';
            formPostalCode.value = '';
            formDescription.value = '';
            $('#selectComuna').on('change',function(){
                 if(selectValor === 'delivery'){
                    var valor = $(this).val();
                delivery = 0;
                if(valor !=''){
                    for(var i in data){
                        if(valor === data[i].fields['nombre'] && selectValor === 'delivery'){
                            delivery = parseInt(data[i].fields['precio'])
                        }
                    }
                }
                total = parseInt(Subtotal) + delivery;
                spanTotal.innerHTML='$'+total;
                liDelivery.style.display = 'block';
                ValorDelivery.innerHTML= '$'+delivery;
                enviar.value = total
                }
            });
        };
    });

});