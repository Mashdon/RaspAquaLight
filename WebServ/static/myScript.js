// Var

var allowSendManual = false
/*
--------------------------
--------------------------
 */
// Functions


function rgbToHex(red, green, blue) {
    var rgb = blue | (green << 8) | (red << 16);
    return '#' + (0x1000000 + rgb).toString(16).slice(1)
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function createArray(length) {
    var arr = new Array(length || 0),
        i = length;

    if (arguments.length > 1) {
        var args = Array.prototype.slice.call(arguments, 1);
        while(i--) arr[length-1 - i] = createArray.apply(this, args);
    }

    return arr;
}

function syncRGB(hex) {
    var rgb = hexToRgb(hex);

    $("#html-color-picker").val(hex);

    $("#square-visu").css("background-color", hex);

    $("#r-color-picker").val(rgb.r);
    $("#g-color-picker").val(rgb.g);
    $("#b-color-picker").val(rgb.b);

    if ($("#checkbox-visu").is(":checked")){
        sendManual(true, rgb.r, rgb.g, rgb.b);
    }
}

function sendManual(boo, r, g, b){
    if (allowSendManual) {
        if (typeof(r) === 'undefined') r = 0;
        if (typeof(g) === 'undefined') g = 0;
        if (typeof(b) === 'undefined') b = 0;
        $.ajax({
            url: '/SetManual',
            data: {
                isManual: boo,
                r: r,
                g: g,
                b: b
            },
            type: 'post',
            dataType: 'json'
        });
    }
}

function clearEdit(){
    $("div.well-phase").each(function() {
        $(this).removeClass("well-info");
    });

    $(".button-phase-edit").attr("disabled", false);
    $("#bottom-edit").removeAttr("data-phase-number").fadeOut();
}

function clearUpDownButtons(){
    $(".button-phase-down").attr("disabled", false);
    $(".button-phase-up").attr("disabled", false);

    var nb_phases = $(".div-phase").length;
    $(".button-phase-up[data-phase-number=1]").attr("disabled", true);
    $(".button-phase-down[data-phase-number=" + nb_phases + "]").attr("disabled", true);
}

function changePlacePhase(oldNumber, newNumber){
    if (oldNumber == $("#bottom-edit").attr("data-phase-number")){
        $("#bottom-edit").attr("data-phase-number", newNumber);
        $("#strong-num-phase-edit").html(newNumber);
    }

    $("[data-phase-number=" + oldNumber +"]").attr("data-phase-number", "x");
    $("[data-phase-number=" + newNumber +"]").attr("data-phase-number", oldNumber);
    $("[data-phase-number=x]").attr("data-phase-number", newNumber);

    $(".phase_number[data-phase-number=" + newNumber +"]").html(newNumber);
    $(".phase_number[data-phase-number=" + oldNumber +"]").html(oldNumber);

    if (oldNumber < newNumber){ //down
        $(".div-phase[data-phase-number=" + newNumber +"]").before($(".div-phase[data-phase-number=" + oldNumber +"]"));
    } else {
        $(".div-phase[data-phase-number=" + newNumber +"]").after($(".div-phase[data-phase-number=" + oldNumber +"]"));
    }
}

/*
--------------------------
--------------------------
 */
// Main
$(function() {

    syncRGB(rgbToHex(
        $("#span-manual").attr("data-manual-r"),
        $("#span-manual").attr("data-manual-g"),
        $("#span-manual").attr("data-manual-b")));

    clearUpDownButtons();


    // TEST DE LA PROGRAMATION
    $("#btn-test").click(function(){

        var durationTest = $("#number-test").val();

        if (!isNaN(durationTest)) {
            $('#checkbox-visu').prop('checked', false);
            $("#checkbox-visu").trigger("change");


            durationTest = Math.abs(parseInt(durationTest));
            $("#btn-test").attr("disabled", true);

            $.ajax({
                url: '/StartTest',
                data: {
                    duration: durationTest
                },
                type: 'post',
                dataType: 'json'
            });

            setTimeout(function () {
                $("#btn-test").attr("disabled", false);
            }, (durationTest + 1) * 1000);

        }

    });

    // AJOUT DE PHASE
    $("#btn-add-phase").click(function () {
        var nb_phases = $(".div-phase").length;
        $.ajax({
            url: '/GetNewPhase/' + (nb_phases + 1),
            type: 'get',
            async: false,
            success: function (response) {
                $("#phases").append(response);
            },
            error: function () {
                alert("");
            }
        });

    });

    // SUPPRIMER UNE PHASE
    $('body').on("click", ".button-remove-phase", function () {
        var num_remove = $(this).attr("data-phase-number");
        if (num_remove == $("#bottom-edit").attr("data-phase-number")){
            clearEdit();
        }
        $("div.div-phase[data-phase-number=" + num_remove + "]").remove();

        $("div.div-phase").filter(function(){
            return $(this).attr("data-phase-number") > num_remove;

        }).each(function(){
            var new_num = $(this).attr("data-phase-number") - 1;

            $(this).attr("data-phase-number",new_num);
            $(this).find("strong.phase_number").html(new_num);
            $(this).find("[data-phase-number]").attr("data-phase-number", new_num);
        });
    });


    $('body').on("click", ".button-phase-up", function (){
        var num = parseInt($(this).attr("data-phase-number"));
        changePlacePhase(num, num - 1);
        clearUpDownButtons();
    });

    $('body').on("click", ".button-phase-down", function (){
        var num = parseInt($(this).attr("data-phase-number"));
        changePlacePhase(num, num + 1);
        clearUpDownButtons();
    });


    $("#button-cancel-phase").click(function () {
        $.ajax({
            url: '/GetAllPhases',
            type: 'get',
            success: function (response) {
                $("#phases").html(response);
                clearUpDownButtons();
                clearEdit();
            },
            async: false
        });
    });

    $("#button-save-phase").click(function(){
        var nbPhases = $(".div-phase").length;

        var phases = createArray(nbPhases, 5);

        for(var i = 0; i < nbPhases ; i++){
            var iNum = i + 1
            phases[i][0] = $(".input-name-phase[data-phase-number=" + iNum + "]").val();
            phases[i][1] = $(".input-time-phase[data-phase-number=" + iNum + "]").val();
            phases[i][2] = $(".r-display[data-phase-number=" + iNum + "]").html();
            phases[i][3] = $(".g-display[data-phase-number=" + iNum + "]").html();
            phases[i][4] = $(".b-display[data-phase-number=" + iNum + "]").html();
        }

        var data = {"nbPhases": nbPhases,"phases": phases};
        $.ajax({
            url: '/SavePhases',
            data: data,
            type: 'post',
            //dataType: 'application/json'
        });

        $("#glyph-save").show();
        setTimeout(function () {
            $("#glyph-save").hide()
        }, 1000);
    });


    $("#checkbox-visu").change(function () {
        if (this.checked){
            $("#panel-right").removeClass("panel-default").addClass("panel-danger");
            $("#panel-left").removeClass("panel-primary").addClass("panel-default");
            var hex = $("#html-color-picker").val();
            var rgb = hexToRgb(hex);
            sendManual(true, rgb.r, rgb.g, rgb.b);
        } else {
            $("#panel-left").removeClass("panel-default").addClass("panel-primary");
            $("#panel-right").removeClass("panel-danger").addClass("panel-default");
            sendManual(false);

        }
    }).trigger("change");



    $("#html-color-picker").on("input", function(){
        syncRGB($(this).val());
    });


    $(".rgb-picker").change(function () {
        var hex = rgbToHex($("#r-color-picker").val(), $("#g-color-picker").val(), $("#b-color-picker").val());
        syncRGB(hex);
    });


    $("#button-picker-ok").click(function () {
        var hex = $("#html-color-picker").val();
        var rgb = hexToRgb(hex);
        var num_phase = $("#bottom-edit").attr("data-phase-number");

        $(".r-display[data-phase-number=" + num_phase + "]").html(('000' + rgb.r).substr(-3));
        $(".g-display[data-phase-number=" + num_phase + "]").html(('000' + rgb.g).substr(-3));
        $(".b-display[data-phase-number=" + num_phase + "]").html(('000' + rgb.b).substr(-3));

        clearEdit();
    });


    $("#button-picker-cancel").click(function () {
        clearEdit();
    });



    $("body").on("click", ".button-phase-edit", function () {
        $(".button-phase-edit").attr("disabled", false);
        $(this).attr("disabled", true);
        var num = $(this).attr("data-phase-number");

        $("div.well-phase").each(function() {
            $(this).removeClass("well-info");
        });

        $("div.well-phase[data-phase-number=" + num + "]").addClass("well-info");

        var hex = rgbToHex(
            $(".r-display[data-phase-number=" + num + "]").html(),
            $(".g-display[data-phase-number=" + num + "]").html(),
            $(".b-display[data-phase-number=" + num + "]").html());
        syncRGB(hex);

        $("#strong-num-phase-edit").html(num);
        $("#bottom-edit").attr("data-phase-number", num).fadeIn();

        $('html, body').animate({
            scrollTop: $("#panel-right").offset().top
        }, 500);
    });




    allowSendManual = true;

});
