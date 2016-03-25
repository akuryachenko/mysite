$(function () {
    $("[name='ch']").change(function() {
        var str = $("#form1").serialize();
        var url = $(location).attr('pathname');
        $.post(url, str, function( data ) {
            $( "#form1" ).replaceWith(data);
        });
        
        
        
    });
});

