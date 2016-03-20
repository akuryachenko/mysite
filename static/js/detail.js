$(document).ready(function() {    
    $("[class*='modal-trigger']").toggleClass("disabled",true); //disabled view trigger
    $("[class*='modal-trigger']").prop( "href", "#!" );         //disabled activity trigger
    $("#button1").prop( "disabled", true );                     //disabled simple button btn
        
    $("[name='ch']").change(function() {
       $("[class*='modal-trigger']").toggleClass("disabled",false);
       $("[class*='modal-trigger']").prop( "href", "#modal1" );
       $("#button1").prop( "disabled", false );
    });
});

