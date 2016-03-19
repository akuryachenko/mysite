$(document).ready(function() {    
    var $radios = $('input:radio[name=ch]');
    if($radios.is(':checked') === false) {
        $('#button1').prop( "disabled", true ); 
        $('#button2').prop( "disabled", true ); 
    }
    $("[name=ch]").change(function() {
        $('#button1').prop( "disabled", false ); 
        $('#button2').prop( "disabled", false ); 
    });
});
