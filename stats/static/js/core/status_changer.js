$('.btn ink-reaction btn-floating-action btn-info').click(function(){
    var order_id = $(this).id;
    $.get('order/status/'+/order_id,function (r){console.log(r);})
});

$(document).ready(function() {
    $('table.display').DataTable();
} );