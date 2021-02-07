function cacher() {
    var elmt = document.getElementById('dataTable');
    var elmtHead = document.getElementById('dataTableHead');
    var elmtBody = document.getElementById('dataTableBody');
    if (elmt.style.display == 'none') {
        elmt.style.display = 'block';
        elmtHead.style.display = 'block';
        elmtBody.style.display = 'block';
    } else {
        elmt.style.display = 'none';
        elmtHead.style.display = 'none';
        elmtBody.style.display = 'none';
    }
}

function Montant(r = "") {
    var q_served = document.getElementById('quantity_served');
    var u_price = document.getElementById('unit_price');
    var total_amount = document.getElementById('total_amount');

    if (q_served != null && u_price != null){
        data = q_served.value * u_price.value;
    }else{
        data = 0;
    }
    

    if (r == "result") {
        $("#result").html(data).show();
    } else {
        total_amount.value = data;
        $("#result").html(data).show();
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length;) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    //const csrftoken = getCookie('csrftoken');
}


 (function ($) {
    $(function () {
        $('nav ul li a:not(:only-child)').click(function (e) {
            $(this).siblings('.nav-dropdown').toggle();
            $('.dropdown').not($(this).siblings()).hide();
            e.stopPropagation();
        });
        $('html').click(function () {
            $('.nav-dropdown').hide();
        });
        $('#nav-toggle').click(function () {
            $('nav ul').slideToggle();
        });
        $('#nav-toggle').on('click', function () {
            this.classList.toggle('active');
        });
    });
})(jQuery);

function flashy(message, tags) {
    var data = '<div class="alert alert-' + tags + '" role="alert">' + message + '</div>'
    // var data = '<div class="alert alert-' + tags + '" role="alert">' + message + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button> </div>'

    if (tags == 'success') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "75%" }, 1000, "swing")
            .animate({ marginRight: "50%" }, 200, "swing")
            .animate({ marginRight: "53%" }, 100, "swing")
            .animate({ marginRight: "51%" }, 100, "swing")
            .animate({ marginRight: "52%" }, 100, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .animate({ marginRight: "51%" }, 100, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .delay(2800).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else if (tags == 'warning') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "75%" }, 1100, "swing")
            .animate({ marginRight: "70%" }, 400, "swing")
            .animate({ marginRight: "50%" }, 400, "swing")
            .animate({ marginRight: "55%" }, 200, "swing")
            .animate({ marginRight: "50%" }, 200, "swing")
            .animate({ marginRight: "52%" }, 200, "swing")
            .animate({ marginRight: "50%" }, 200, "swing")
            .animate({ marginRight: "51%" }, 200, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .delay(3500).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else if (tags == 'info') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "75%" }, 1000, "swing")
            .animate({ marginRight: "50%" }, 200, "swing")
            .animate({ marginRight: "53%" }, 100, "swing")
            .animate({ marginRight: "51%" }, 100, "swing")
            .animate({ marginRight: "52%" }, 100, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .animate({ marginRight: "51%" }, 100, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .delay(3100).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else if (tags == 'error') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "75%" }, 1000, "swing")
            .animate({ marginRight: "50%" }, 800, "swing")
            .animate({ marginRight: "54%" }, 100, "swing")
            .animate({ marginRight: "52%" }, 100, "swing")
            .animate({ marginRight: "53%" }, 100, "swing")
            .animate({ marginRight: "51%" }, 100, "swing")
            .animate({ marginRight: "52%" }, 100, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .animate({ marginRight: "51%" }, 100, "swing")
            .animate({ marginRight: "50%" }, 100, "swing")
            .delay(10000).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "75%" }, 1000, "swing")
            .animate({ marginRight: "73%" }, 1000, "swing")
            .animate({ marginRight: "71%" }, 1000, "swing")
            .animate({ marginRight: "69%" }, 1000, "swing")
            .animate({ marginRight: "67%" }, 1000, "swing")
            .animate({ marginRight: "65%" }, 1000, "swing")
            .animate({ marginRight: "63%" }, 1000, "swing")
            .animate({ marginRight: "61%" }, 1000, "swing")
            .animate({ marginRight: "59%" }, 1000, "swing")
            .animate({ marginRight: "57%" }, 1000, "swing")
            .animate({ marginRight: "55%" }, 1000, "swing")
            .animate({ marginRight: "50%" }, 1000, "swing")
            .delay(3500).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
}


$(window).on('load', function () {
    // $('#preloder').removeClass('display-none');
    // $(".loader").fadeIn();
    // $("#preloder").delay(10).fadeOut("slow");

    Montant("result");
});

$(".wait").on('click', function () {
    $('#preloderBtn').removeClass('display-none');
    $(".loaderBtn").fadeIn();

    // $("#preloder").delay(100).fadeOut("slow");
    // $('#preloder').addClass('display-none');
});


function getFileName(input,cible){
    cible.value = input[0].files[0].name
}

$("#id_profile_pic").on('change', function () {
    var filename = this.files[0].name
    $("#picture_name_cible").html(filename).show();
});


$('#add_to_stock').on('click', function () {
    if (document.getElementById('add_to_stock').checked == '') {
        document.getElementById("stock_quantity").style.display = 'none'
    } else {
        document.getElementById("stock_quantity").style.display = 'block'
    }
});

// $('a').on('click', function(){
//     alert('aaaaaaaaaaaaaa');
// })