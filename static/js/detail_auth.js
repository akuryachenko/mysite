$(function () {
    $("[name='ch']").change(function() {
        var str = $("#form1").serialize();
        var url = $("#form1").attr('action');
        $.post(url, str, function( data ) {
            $( "#form1" ).replaceWith(data);
        });
    });
});

