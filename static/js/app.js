var cookie = document.cookie;
console.log(cookie)
csrftoken = cookie.replace('csrftoken=', "");
csrftoken = csrftoken.split(';')[0]
console.log('token ' + csrftoken)

    
// if(cart == undefined){
//     cart = {}
//     document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
//     console.log(cookie)    
// }





function addProduct(id, type){
    if(user == 'AnonymousUser'){
       cookieAdd(id, type)
    } else{
        $.ajax({
            url : "/update-order",
            method: 'post',
            dataType: 'json',
            data: {
                    'product' : id,
                    'action' : type,
                    // csrfmiddlewaretoken: csrftoken,
                },
        }).done(function(result){

            if(result.created){
                $(".navbar-nav").append(
                    '<li class="nav-item">' +
                        '<div class="shop-card">' +
                            '<img src="/images/'+result.newProduct_image+'"alt="">' +
                             '<div class="name-product-nav">' + result.newProduct + '</div>' +
                             '<div style="display: flex; align-items: center; gap: 7px;">' +
                                '<div id="items-quantity' +result.id + '"></div>' +
                                '<div style="display: flex; flex-direction: column; padding: 17px 7px;">' +
                                    '<i class="bi bi-caret-up"' + "onclick=addProduct(" + result.id + ','+ '"plus"' +")"  + '></i>' +
                                    '<i class="bi bi-caret-down"' +  "onclick=addProduct(" + result.id + ','+ '"less"' +")" + '></i>' +
                                '</div>' +
                             '</div>' +
                             '<strong id="total-product' +result.id + '"></strong>' +
                             '<div><i class="bi bi-trash trash_icon"  onclick="eliminar('+ result.id + ')" id="eliminate' + result.id  + '"></i></div>' +
                        '</div>' +
                    '</li>' 
                )
            }

            $("#total-items").text(result.items)
            $("#items-total-price").text('Total $' + result.total)
            $("#total-product" +  result.id).text('$' + result.product_total)
            $("#items-quantity" + result.id).text(result.items_quantity)
        })
    }
}

function cookieAdd(id, type){
    if (type == 'plus'){
		if (cart[id] == undefined){
            cart[id] = {'quantity':1}

		}else{
			cart[id]['quantity'] += 1
		}
	}

    if (type == 'less'){
		cart[id]['quantity'] -= 1

		if (cart[id]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[id];
		}
	}

    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
    console.log('CART:', cart)

}


function eliminar(id){
    jqxhr = $.ajax('eliminate-item?id=' + id)
    .done(function(result){
        $("#eliminate" + result.id).parent().parent().remove()
        $("#items-total-price").text('Total $' + result.total)
        $("#total-items").text(result.total_items)
        showCheck()
    })
}

function checkOut(event){
    event.preventDefault()


    let jqxhr = $.ajax({
        url : '/order-ended',
        method : 'post',
        dataType : 'json',
        data : {
            'client' : $("#firstName").val(),
            'email' : $("#email").val(),
            'address' : $("#address").val(),
            'country' : $("#country").val(),
            'city' : $("#city").val(),
            'zip' : $("#zip").val(),
            // csrfmiddlewaretoken : csrftoken,
        }
    })
    .done(function(result){
        alert(result)

        cart = {}
        document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'

        window.location.href = "http://127.0.0.1:8000"
        
        
    })

    // $(".form-check :input").prop("disabled", true);
    // $(".form-addres").addClass( " que-mierda-pasa " ).removeClass('form-addres')
    // $(".payment-div").removeClass('payment-div')
}


function showCheck(){
    let x = $("#total-items").text()
    console.log(x)
    if(x == 0){
        $(".Pay-div").hide()
    } else {
        $(".Pay-div").show()
    }
}

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");
    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}
var cart = JSON.parse(getCookie('cart'))
if (cart == undefined){
    cart = {}
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    console.log(document.cookie)
    console.log(cart)
}