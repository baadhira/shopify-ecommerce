$(document).ready(function(){
    $('.addToCartBtn').click(function (e) { 
        e.preventDefault();
        var id = $(this).closest('product_data').find('.prod_id').val();
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'id' : id,
                csrfmiddlewaretoken : token
            },
            dataType: "dataType",
            success: function (response) {
                
            }
        });
        
    });

});