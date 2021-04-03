// function listadoProductos(){
//     $.ajax({
//         dataType: "json",
//         url: '/product-list/',
//         success: function(response){
//             let res = document.querySelector('#products')
//             res.innerHTML = '';
//             for(let i = 0; i < response.length; i++){
//                 departamento = ''
//                 if (response[i]['fields']['departamento'] === 'H'){
//                     departamento = 'Hombre'
//                 }
//                 else{
//                     departamento = 'Mujer'
//                 }
//                 if(response[i]['fields']['discount_price']){
//                     precio = response[i]['fields']['discount_price'];
//                 }else{
//                     precio = response[i]['fields']['price'];
//                 }
//                 res.innerHTML += `
//                 <div class='col-lg-4 col-sm-6 item' 
//                     category="${departamento}" 
//                     price="${response[i]['fields']['price']}
//                 ">
//                     <div class='product-item'>
//                         <div class='pi-pic'>
//                             <a href='http://localhost:8000/product/${response[i]['fields']['slug']}'>
//                                 <img src='http://localhost:8000/media/${response[i]["fields"]["imagen"]}' alt=''>
//                             </a>
//                             <div class='sale pp-sale'>EN VENTA</div>
//                             <div class='icon'>
//                                 <i class='icon_heart_alt'></i>
//                             </div>
//                             <ul>
//                                 <li class='w-icon active'><a href='http://localhost:8000/cart/'><i class='icon_bag_alt'></i></a></li>
//                                 <li class='quick-view'><a href='http://localhost:8000/product/${response[i]['fields']['slug']}'>+ Ver Producto</a></li>
//                             </ul>
//                         </div>
//                         <div class='pi-text'>
//                             <div class='catagory-name'>
//                             ${departamento}
//                             </div>
//                             <a href='#'>
//                                 <h5>${response[i]["fields"]["title"]}</h5>
//                             </a>
//                             <div class='product-price'>
//                             $${precio}
//                             </div>
//                             <div class='product-price'>
//                             </div>
//                         </div>
//                     </div>
//                 </div>
//             `;
//             }
//         },
//         error: function(error){
//             console.log(error)
//         }
//       });
// }

function FiltrosDepartemento(){
        	// AGREGANDO CLASE ACTIVE AL PRIMER ENLACE ====================
            $('.category_list .category_item[category="all"]').addClass('active');
    
    
            $('.category_item').click(function(){
                event.preventDefault();
                var catProduct = $(this).attr('category');
        
                // AGREGANDO CLASE ACTIVE AL ENLACE SELECCIONADO
                $('.category_item').removeClass('active');
                $(this).addClass('active');
        
                // OCULTANDO PRODUCTOS =========================
                $('.item').css('transform', 'scale(0)');
                function hideProduct(){
                    $('.item').hide();
                } setTimeout(hideProduct,400);
        
                // MOSTRANDO PRODUCTOS =========================
                function showProduct(){
                    $('.item[category="'+catProduct+'"]').show();
                    $('.item[category="'+catProduct+'"]').css('transform', 'scale(1)');
                } setTimeout(showProduct,400);
            });
            
                // MOSTRANDO TODOS LOS PRODUCTOS =======================
        
            $('.category_item[category="all"]').click(function(){
                function showAll(){
                    $('.item').show();
                    $('.item').css('transform', 'scale(1)');
                } setTimeout(showAll,400);
            });
}

function filtros(){
    $('#filtros').click(function(){
        event.preventDefault();
    });
}


$(document).ready(function (){
    // listadoProductos();
    FiltrosDepartemento();
    filtros();
});