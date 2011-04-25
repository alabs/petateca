var options, a;
jQuery(function(){
    // autocomplete en la busqueda
    options = { serviceUrl:'/search/lookup/' };
    a = $('#query').autocomplete(options);
});

$(document).ready(function(){
    // El popup cuando se hace click en login
	$(".login").colorbox({iframe:true, innerWidth:555, innerHeight:324});

    // Que cuando se haga click en el rating envia el valor por post
    $('.ratingstar').rating({ callback: function(value, link){
            $.post(url, { 'rating': value }, function(data){ disc_rat_data(data); } ); }
    });


    // Preloading de las imagenes, para que aparezca el ajax-loading que queda mas 2.0
    $('.prel').each(function () {
        if (this.complete) { return; } 
        $(this).hide();
        $(this).load(function () {
            $(this).width($(this).parent().width()).height($(this).parent().height());
            $(this).fadeIn("slow");
        });
    });

    // ver espoiler en get_season
    $('.show_epi_detail').click(function() {
        $('.epi_detail').toggle('slow');
        return false;
    });

    // ver espoiler en get_episode
    $('#show_epi_detail').click(function() {
        $('#epi_detail').toggle('slow');
        $('#show_epi_detail').hide();
        return false;
    });

    // Popup de añadir enlace
    $('.add_link').colorbox({width:'50%', height:'60%', iframe:true, 
         onClosed:function(){ location.reload(true); } 
    });
});


function disc_rat_data(data){
    // Las respuestas cuando se hace un rating, ver en el view de series para el tratamiento
    switch(data)
            {
            case 'no-user':
                    $.jGrowl("Para poder votar debes estar registrado o haber iniciado sesion", { header: 'Error' });
                    break;
            case 'Vote recorded.':
                    $.jGrowl("Su voto ha sido guardado"); 
                    break;
            case 'Vote changed.':
                    $.jGrowl("Su voto ha sido cambiado"); 
                    break;
            }
}

function getCookie(name) {
    // Obtiene una cookie, usado para obtener el CSRF
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    // los popups de las series cuando se va a /series y que haga la magia :)
  $('.serie').CreateBubblePopup({
    position: 'right',
    align: 'center',
    width: '500',
    innerHtml: '<img src="/static/images/ajax-loading.gif" style="border:0px; vertical-align:middle; margin-right:10px; display:inline;" />',
    innerHtmlStyle: { color:'#fff', 'text-align':'left', 'font-size':'110%' },
    themeName: 'all-grey',
    themePath: '/static/images/jquerybubblepopup-theme'
  });
  $('.serie').mouseover(function(){
    // Obtenemos el id de la serie y lo buscamos
    var serie = $(this);
    var serie_id = serie.attr('id');
    $.get('/series/lookup/serie/' + serie_id, function(data) {
      serie.SetBubblePopupInnerHtml(data);
    }); 
  });
});


function vote(url, linkid, direction) {
    // tratamiento de los votos de episodio
    var $linkscore = $('#linkscore' + linkid);
    $linkscore.html('<img src="/static/images/ajax-loading.gif">');
    // send the post petition with the required data
    $.post(url, { 
                'vote': direction, 
                'linkid': linkid,
                'csrfmiddlewaretoken': getCookie('csrftoken'),
    }, function (data){ 
        // change the value with the new score
        $linkscore.html(data.score);
        // change the image
                if (direction == 'upvote') {
            $('#linkuparrow' + linkid + ' img').attr('src', '/static/images/voting/aupmod.gif');
            $('#linkdownarrow' + linkid + ' img').attr('src', '/static/images/voting/adowngrey.gif');
        } else if (direction == 'downvote') {
            $('#linkuparrow' + linkid + ' img').attr('src', '/static/images/voting/aupgrey.gif');
            $('#linkdownarrow' + linkid + ' img').attr('src', '/static/images/voting/adownmod.gif');
        };
       }
    );
};
