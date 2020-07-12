$( document ).ready(function() {
	$("#id_quantity").on('change', function () {
		var form = $(this).closest("form");
 
		$.ajax({
			url: form.attr("data-get-order-item-price-url"),
			data: form.serialize(),
			dataType: 'json',
			success: function (data) {
			$("#id_price").val(data.to_pay)
			},
		});
	  
    });
});

