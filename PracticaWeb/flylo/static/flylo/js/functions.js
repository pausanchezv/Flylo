/**
 * Created by pausanchezv on 14/04/2017.
 */

/**
 * Redirecciona a una URL
 * @param url
 */
var redirectTo = function(url) {
    if (url !== '') {
        window.location = url;
    }
};

/**
 * Canvia l'idioma de la web
 * @param lang
 * @param current_language
 * @param current_path
 */
var change_lang = function(lang, current_language, current_path) {
    window.location = current_path.replace("/" + current_language + "/", "/" + lang + "/");
};

/**
 * Selecciona els seients per un vol
 * @param flightId
 * @param textAdded
 * @param textAddToCart
 * @param path
 */
var selectFlightOptions = function(flightId, textAdded, textAddToCart, path) {
    
    if ($("#flight_" + flightId).is(':checked')){
        
        $("#absolute-seat-" + flightId).show();
        $("#lang-add-to-cart-" + flightId).html(textAdded);
        
    } else {

        $("#label_flight_" + flightId).css("opacity", "0.3");
        
        $.get(path, function() {
            $("#user-seats-" + flightId).hide();
            $("#return-flights-" + flightId).css("visibility", "hidden");
            $("#lang-add-to-cart-" + flightId).html(textAddToCart);
            $("#label_flight_" + flightId).css("opacity", "1");
        });
    }

};

/**
 * Selecciona els seients per un vol
 * @param flightId
 */
var selectFlightsReturn = function(flightId) {
    $("#absolute-returns-" + flightId).show();
    $("#compare-" + flightId).hide();
};

/**
 * Selecciona els seients per un vol
 * @param flightId
 * @param innerHtml
 */
var addReturn = function(flightId, innerHtml) {
    $("#absolute-returns-" + flightId).hide();
    $("#return-flights-" + flightId).html('<span style="color: #F60"><u>Ret</u>: ' + innerHtml + '</span>');

    var airlineReturnName = innerHtml.slice(innerHtml.indexOf('(') + 1, innerHtml.indexOf(')'));
    $("#airline_return_" + flightId).val(airlineReturnName);
};

/**
 * Accepta i insereix a l'html el nombre de seients
 * @param flightId
 * @param numSeats
 * @param selectedAirline
 * @param textQuestionReturn
 */
var acceptFlightOptions = function(flightId, numSeats, selectedAirline, textQuestionReturn) {
    $("#user-seats-" + flightId).show();
    $("#absolute-seat-" + flightId).hide();
    $("#num-seats-" + flightId).html(numSeats + " <i class='fa fa-user'></i> <small>(" + selectedAirline + ")</small>");
    $("#return-flights-" + flightId).css("visibility", "visible")
            .html('<a  class="return-button-flights shadow radius-5" href="javascript:" onclick="selectFlightsReturn(' + flightId + ')">' + textQuestionReturn + '</a>');
    $("#airline_return_" + flightId).val('');
    $('#flight-returns-' + flightId + ' option:selected').prop("selected", false);
};

/**
 * Cancel·la el vol de retorn
 * @param flightId
 */
var cancelReturn = function(flightId) {
    $("#absolute-returns-" + flightId).hide();
    $('#flight-returns-' + flightId + ' option:selected').prop("selected", false);
};

/**
 * Tanca un missatge d'error
 * @param id
 */
var closeErrorMessage = function(id) {
    $("#" + id).slideUp(700);
};

/**
 * Es desllissa fins al capdemunt del display
 */
var scrollToTop = function() {
    var body = $("html, body");
    body.stop().animate({scrollTop:0}, '500', 'swing');
};

/**
 * Mostra un missatge d'error
 */
var showErrorMessage = function(message) {
    $("#error_message").show().find("p strong").html("Error: " + message);
    scrollToTop();
};

/**
 * Valida si un string pertany o no a un email
 * @param email
 * @returns {boolean}
 */
function emailValidate(email){
	var filter = /[\w-\.]{2,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}/;
	return filter.test(email);
}

/**
 * Activa el loader si escau
 */
var toggleLoader = function(loader, container, active) {

    if (active && $("#error_message").css('display') == 'none') {
        loader.show();
        container.css("opacity", "0.4");
    } else {
        loader.hide();
        container.css("opacity", "1");
    }
};

/**
 * Submit al clicar intro
 */
var enterKeyEvent = function(field, event, id) {
    var keyCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
    if (keyCode == 13) {
        $("#" + id).trigger('click');
        return false;
    }
    return true;
};