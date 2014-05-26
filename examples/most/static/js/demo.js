var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function () {
    function showNewCityPanel() {
        $('#collapseCityAPI').collapse('show');
        $('#collapseCityNew').collapse('show');
        window.location.hash = 'collapseCityNew';
    }

    function getPatient() {
        var patientSearchString = $("#get_patient_field").val();
        if (patientSearchString) {
            $.ajax({
                url: '/demographics/patient/get/',
                type: 'GET',
                data: {
                    query_string: patientSearchString
                },
                //dataType: 'json',
                dataType: 'text',
                success: function (data, textStatus, jqXHR) {
                    var jsonData = JSON.parse(data);
                    var beautifiedData = JSON.stringify(jsonData, null, 4);
                    $('#get_patient_result_body').html('<div><pre class="pre-scrollable">' + beautifiedData + '</pre></div>');
                    if (jsonData.success) {
                        if ($('#get_patient_result').hasClass('panel-danger')) {
                            $('#get_patient_result').removeClass('panel-danger');
                        }
                        if (!$('#get_patient_result').hasClass('panel-success')) {
                            $('#get_patient_result').addClass('panel-success');
                        }
                    }
                    else {
                        //$('#get_city_result').html('<div>' + data.errors + '</div>');
                        if ($('#get_patient_result').hasClass('panel-success')) {
                            $('#get_patient_result').removeClass('panel-success');
                        }
                        if (!$('#get_patient_result').hasClass('panel-danger')) {
                            $('#get_patient_result').addClass('panel-danger');
                        }
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $('#get_patient_result_body').html('<div>' + textStatus + ': ' + errorThrown + '</div>');
                    if ($('#get_patient_result').hasClass('panel-success')) {
                        $('#get_patient_result').removeClass('panel-success');
                    }
                    if (!$('#get_patient_result').hasClass('panel-danger')) {
                        $('#get_patient_result').addClass('panel-danger');
                    }
                }
            });
        }
    }

    function getCity() {
        var citySearchString = $("#get_city_field").val();
        if (citySearchString) {
            $.ajax({
                url: '/demographics/city/get/',
                type: 'GET',
                data: {
                    query_string: citySearchString
                },
                //dataType: 'json',
                dataType: 'text',
                success: function (data, textStatus, jqXHR) {
                    var jsonData = JSON.parse(data);
                    var beautifiedData = JSON.stringify(jsonData, null, 4);
                    $('#get_city_result_body').html('<div><pre class="pre-scrollable">' + beautifiedData + '</pre></div>');
                    if (jsonData.success) {
                        if ($('#get_city_result').hasClass('panel-danger')) {
                            $('#get_city_result').removeClass('panel-danger');
                        }
                        if (!$('#get_city_result').hasClass('panel-success')) {
                            $('#get_city_result').addClass('panel-success');
                        }
                    }
                    else {
                        //$('#get_city_result').html('<div>' + data.errors + '</div>');
                        if ($('#get_city_result').hasClass('panel-success')) {
                            $('#get_city_result').removeClass('panel-success');
                        }
                        if (!$('#get_city_result').hasClass('panel-danger')) {
                            $('#get_city_result').addClass('panel-danger');
                        }
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $('#get_city_result_body').html('<div>' + textStatus + ': ' + errorThrown + '</div>');
                    if ($('#get_city_result').hasClass('panel-success')) {
                        $('#get_city_result').removeClass('panel-success');
                    }
                    if (!$('#get_city_result').hasClass('panel-danger')) {
                        $('#get_city_result').addClass('panel-danger');
                    }
                }
            });
        }
    }

    $(function () {
        $('#birth_date').datepicker();
    });

    //$('#add_birth_place').click(showNewCityPanel);
    //$('#city').click(showNewCityPanel);

    $('#new_city_form').submit(function (event) {
        event.preventDefault();
        var cityArrayData = $('#new_city_form').serialize().split("&");
        var cityObject = {};
        var cityKW;
        for (var i = 0; i < cityArrayData.length; i++) {
            cityKW = cityArrayData[i].split("=");
            cityObject[cityKW[0]] = cityKW[1].replace(/\+/g, ' ');
        }
        var cityJsonData = JSON.stringify(cityObject);
        $.ajax({
            url: '/demographics/city/new/',
            type: 'POST',
            data: cityJsonData,
            //dataType: 'json',
            dataType: 'text',
            success: function (data, textStatus, jqXHR) {
                var jsonData = JSON.parse(data);
                var beautifiedData = JSON.stringify(jsonData, null, 4);
                $('#new_city_result_body').html('<div><pre class="pre-scrollable">' + beautifiedData + '</pre></div>');
                if (jsonData.success) {
                    if ($('#new_city_result').hasClass('panel-danger')) {
                        $('#new_city_result').removeClass('panel-danger');
                    }
                    if (!$('#new_city_result').hasClass('panel-success')) {
                        $('#new_city_result').addClass('panel-success');
                    }
                }
                else {
                    //$('#new_city_result_body').html('<div>' + data.errors + '</div>');
                    if ($('#new_city_result').hasClass('panel-success')) {
                        $('#new_city_result').removeClass('panel-success');
                    }
                    if (!$('#new_city_result').hasClass('panel-danger')) {
                        $('#new_city_result').addClass('panel-danger');
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#new_city_result_body').html('<div>' + textStatus + ': ' + errorThrown + '</div>');
                if ($('#new_city_result').hasClass('panel-success')) {
                    $('#new_city_result').removeClass('panel-success');
                }
                if (!$('#new_city_result').hasClass('panel-danger')) {
                    $('#new_city_result').addClass('panel-danger');
                }
            }
        });
        return false;
    });

    $('#new_patient_form').submit(function (event) {
        event.preventDefault();
        var patientArrayData = $('#new_patient_form').serialize().split("&");
        var patientObject = {};
        var patientKW;
        for (var i = 0; i < patientArrayData.length; i++) {
            patientKW = patientArrayData[i].split("=");
            patientObject[patientKW[0]] = decodeURIComponent(patientKW[1]).replace(/\+/g, ' ');
        }
        var patientJsonData = JSON.stringify(patientObject);
        $.ajax({
            url: '/demographics/patient/new/',
            type: 'POST',
            data: patientJsonData,
            dataType: 'text',
            success: function (data, textStatus, jqXHR) {
                var jsonData = JSON.parse(data);
                var beautifiedData = JSON.stringify(jsonData, null, 4);
                $('#new_patient_result_body').html('<div><pre class="pre-scrollable">' + beautifiedData + '</pre></div>');
                if (jsonData.success) {
                    if ($('#new_patient_result').hasClass('panel-danger')) {
                        $('#new_patient_result').removeClass('panel-danger');
                    }
                    if (!$('#new_patient_result').hasClass('panel-success')) {
                        $('#new_patient_result').addClass('panel-success');
                    }
                }
                else {
                    if ($('#new_patient_result').hasClass('panel-success')) {
                        $('#new_patient_result').removeClass('panel-success');
                    }
                    if (!$('#new_patient_result').hasClass('panel-danger')) {
                        $('#new_patient_result').addClass('panel-danger');
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#new_patient_result_body').html('<div>' + textStatus + ': ' + errorThrown + '</div>');
                if ($('#new_patient_result').hasClass('panel-success')) {
                    $('#new_patient_result').removeClass('panel-success');
                }
                if (!$('#new_patient_result').hasClass('panel-danger')) {
                    $('#new_patient_result').addClass('panel-danger');
                }
            }
        });
        return false;
    });

    $('#edit_patient_form').submit(function (event) {
        event.preventDefault();
        var patientArrayData = $('#edit_patient_form').serialize().split("&");
        var patientObject = {};
        var patientKW;
        for (var i = 0; i < patientArrayData.length; i++) {
            patientKW = patientArrayData[i].split("=");
            patientObject[patientKW[0]] = decodeURIComponent(patientKW[1]).replace(/\+/g, ' ');
        }
        var patientJsonData = JSON.stringify(patientObject);
        $.ajax({
            url: '/demographics/patient/edit/',
            type: 'POST',
            data: patientJsonData,
            dataType: 'text',
            success: function (data, textStatus, jqXHR) {
                var jsonData = JSON.parse(data);
                var beautifiedData = JSON.stringify(jsonData, null, 4);
                $('#edit_patient_result_body').html('<div><pre class="pre-scrollable">' + beautifiedData + '</pre></div>');
                if (jsonData.success) {
                    if ($('#edit_patient_result').hasClass('panel-danger')) {
                        $('#edit_patient_result').removeClass('panel-danger');
                    }
                    if (!$('#edit_patient_result').hasClass('panel-success')) {
                        $('#edit_patient_result').addClass('panel-success');
                    }
                }
                else {
                    if ($('#edit_patient_result').hasClass('panel-success')) {
                        $('#edit_patient_result').removeClass('panel-success');
                    }
                    if (!$('#edit_patient_result').hasClass('panel-danger')) {
                        $('#edit_patient_result').addClass('panel-danger');
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#edit_patient_result_body').html('<div>' + textStatus + ': ' + errorThrown + '</div>');
                if ($('#edit_patient_result').hasClass('panel-success')) {
                    $('#edit_patient_result').removeClass('panel-success');
                }
                if (!$('#edit_patient_result').hasClass('panel-danger')) {
                    $('#edit_patient_result').addClass('panel-danger');
                }
            }
        });
        return false;
    });

    $( "#get_city_field" ).keypress(function(event) {
        if (event.keyCode == 13) {
            getCity();
        }
    });
    $('#get_city_button').click(getCity);

    $( "#get_patient_field" ).keypress(function(event) {
        if (event.keyCode == 13) {
            getPatient();
        }
    });
    $('#get_patient_button').click(getPatient);

    $( "#birth_place" ).autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "/demographics/city/get/",
                dataType: "json",
                data: {
                    query_string: request.term
                },
                success: function( data ) {
                    response( $.map( data.data, function( item ) {
                        return {
                            label: item.name + (item.province ? ' (' + item.province + ')' : ''),
                            value: item.id
                        }
                    }));
                }
            });
        },
        /*focus: function( event, ui ) {
            $( "#birth_place" ).val( ui.item.label );
            return false;
        },*/
        select: function( event, ui ) {
            $( "#birth_place" ).val( ui.item.label );
            $( "#birth_place_id" ).val( ui.item.value );
            return false;
        },
        minLength: 2,
        open: function() {
            $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
            $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });

    $( "#city" ).autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "/demographics/city/get/",
                dataType: "json",
                data: {
                    query_string: request.term
                },
                success: function( data ) {
                    response( $.map( data.data, function( item ) {
                        return {
                            label: item.name + (item.province ? ' (' + item.province + ')' : ''),
                            value: item.id
                        }
                    }));
                }
            });
        },
        /*focus: function( event, ui ) {
            $( "#city" ).val( ui.item.label );
            return false;
        },*/
        select: function( event, ui ) {
            $( "#city" ).val( ui.item.label );
            $( "#city_id" ).val( ui.item.value );
            return false;
        },
        minLength: 2,
        open: function() {
            $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
            $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });
});
