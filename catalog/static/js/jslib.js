$( document ).ready(function() {
	$("#id_quantity").on('change', function () {
		var form = $(this).closest("form");
        calculate_order_item_price(form);
    });

    $("#id_orderitem").on('change', function () {
		var form = $(this).closest("form");
		var quantity = $('#id_quantity').val()
		if (quantity) {
		    calculate_order_item_price(form);
		}

    });
});

function calculate_order_item_price(form) {
    $.ajax({
        url: form.attr("data-get-order-item-price-url"),
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            $("#id_price").val(data.to_pay)
        },
    });
}

