function site(){
    var host = 'http://localhost:8000/'
    var URLactual = window.location;
    if (URLactual == host){
        var elem = document.getElementById('inicio');
        elem.className += 'active';
    }else{
        tienda = host+'product-list/';
        about = host+'about/';
        contact = host+'contact/';
        if(URLactual == tienda){
            var eleme = document.getElementById('tienda');
            eleme.className += 'active';
        }
        if(URLactual == about){
            var eleme = document.getElementById('about');
            eleme.className += 'active';
        }
        if(URLactual == contact){
            var eleme = document.getElementById('contact');
            eleme.className += 'active';
        }

    }
}

site();