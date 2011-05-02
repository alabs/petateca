var options, a;
jQuery(function(){
    // autocomplete en la busqueda
    options = { serviceUrl:'/search/lookup/' };
    a = $('#query').autocomplete(options);
});

$(document).ready(function () {
    // Rating de estrellas, se envia el rating por post a /serie/nombre
    $('.ratingstar').rating({
        callback: function (value, link) {
            var url = window.location.pathname;
            $.post(url, {
                'rating': value,
                'csrfmiddlewaretoken': getCookie('csrftoken'),
            }, function (data) {
                disc_rat_data(data);
            });
        }
    }); 
    // Listado de episodios por temporadas
    $('.season').click( 
        function(){ 
            $('#season_list').html('<img src="/static/images/ajax-loading-bar.gif">');
            season = $(this).attr('href')
            $('#season_list').load(season)
            return false; 
        }
    );
    // Listado de actores segun serie
    $('#get_actors').click(
        function(){
            var url = window.location.pathname;
            var serie = url.split('/')[2];
            $.get('/series/lookup/actors/' + serie, {}, 
                function(data){
                    $('#actors_list').html(data)
                }
            ); 
        }
    );

});


function disc_rat_data(data) {
    // Discriminacion de las votaciones dependiendo la respuesta que llegue
    switch (data) {
        case 'no-user':
            $.jGrowl("Para poder votar debes estar registrado o haber iniciado sesion", {
                header: 'Error'
            });
            break;
        case 'Vote recorded.':
            $.jGrowl("Su voto ha sido guardado");
            break;
        case 'Vote changed.':
            $.jGrowl("Su voto ha sido cambiado");
            break;
    }
}

function disc_fav_data(data) {
    // Discriminacion de los favorites dependiendo de la respuesta
    // tambien actualiza el corazon 
    switch (data) {
    case 'yes':
        $("#favorite").html('<a href="#" onclick="favorite();" id="favorite"><img class="heart_fav" src="/static/images/heart_red.png"></a>');
        $.jGrowl("Has agregado esta serie como favorita");
        break;
    case 'no':
        $("#favorite").html('<a href="#" onclick="favorite();" id="favorite"><img class="heart_fav" src="/static/images/heart_black.png"></a>');
        $.jGrowl("Has quitado esta serie de tus favoritas");
        break;
    case 'no-user':
        $.jGrowl("Para poder votar debes estar registrado o haber iniciado sesion", {
            header: 'Error'
        });
        break;
    }
}

function favorite() {
    // Tratamiento del favorito
    var imgsrc = $("#favorite img").attr('src');
    if (imgsrc == "/static/images/heart_black.png") {
        decision = "yes";
    } else if (imgsrc == "/static/images/heart_red.png") {
        decision = "no";
    }
    console.log(decision);
    $('#favorite').html('<img src="/static/images/ajax-loading.gif">');
    var url = window.location.pathname;
    if (decision == "yes") {
        $.post(url, {
            'favorite': "favorite",
            'csrfmiddlewaretoken': getCookie('csrftoken'),
        }, function (data) {
            disc_fav_data(data);
        })
    } else if (decision == "no") {
        $.post(url, {
            'no-favorite': "no-favorite",
            'csrfmiddlewaretoken': getCookie('csrftoken'),
        }, function (data) {
            disc_fav_data(data);
        })
    }
}

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

    // Popup de cambiar avatar
	$(".avatar_change").colorbox({width:"600px", height:"500px", iframe:true,
     onClosed:function(){ location.reload(true); } });
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


//Uservoice (Sugerencias)
  var uservoiceOptions = {
    key: 'liberateca',
    host: 'liberateca.uservoice.com', 
    forum: '106199',
    alignment: 'left',
    background_color:'#000000', 
    text_color: 'white',
    hover_color: '#0066CC',
    lang: 'es',
    showTab: true
  };
  function _loadUserVoice() {
    var s = document.createElement('script');
    s.src = ("https:" == document.location.protocol ? "https://" : "http://") + "cdn.uservoice.com/javascripts/widgets/tab.js";
    document.getElementsByTagName('head')[0].appendChild(s);
  }
  _loadSuper = window.onload;
  window.onload = (typeof window.onload != 'function') ? _loadUserVoice : function() { _loadSuper(); _loadUserVoice(); };

// Google Analytics
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-22940195-1']);
  _gaq.push(['_trackPageview']);
  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();


    $(document).ready(function() {  
$(".zoom").click( function(){
    $(this).addClass('selected_list');
    $inside = $(this).siblings();
    $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
    href = $(this).attr('href');
    $inside.load(href);
    return false;
});


$(".espoiler").click( function(e){
    e.preventDefault();
    $(this).parent().addClass('selected_list');
    episodeid = $(this).attr('id');
    $inside = $('#inside' + episodeid);
    $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
    espoiler_id = $(this).attr('rel');
    $inside.load(espoiler_id);
    return false;
});


$(".add_link").click( function(e){
    e.preventDefault();
    $(this).parent().addClass('selected_list');
    episodeid = $(this).attr('id');
    $inside = $('#inside' + episodeid);
    $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
    episode_rel = $(this).attr('rel');
    $inside.load(episode_rel + episodeid + '/');
    return false;
});

      
  //      $('#title').click(function(){  
  //      $(this).addClass('selected_list');
  //    
  //      var toLoad = $(this).attr('href');
  //      $('#content').hide('fast',loadContent);  
  //      $('#load').remove();  
  //      $('#wrapper').append('<span id="load">LOADING...</span>');  
  //      $('#load').fadeIn('normal');  
  //      function loadContent() {  
  //          $('#content').load(toLoad,'',showNewContent())  
  //      }  
  //      function showNewContent() {  
  //          $('#content').show('normal',hideLoader());  
  //      }  
  //      function hideLoader() {  
  //          $('#load').fadeOut('normal');  
  //      }  
  //      $(this).slideDown();
  //      return false;  
  //    
  //      });  
    });  



function voting( direction, linkid ){
    var $linkscore = $('span#linkscore' + linkid);
    $linkscore.html('<img style="margin-bottom:0 !important;" src="/static/images/ajax-loading.gif">');
    $.post('/series/lookup/vote/', { 
                'vote': direction,
                'linkid': linkid,
                'csrfmiddlewaretoken': getCookie('csrftoken'),
    }, function (data){ 
        // change the value with the new score
        $linkscore.html(data.score);

        dir_down = $('#down_' + linkid);
        dir_up = $('#up_' + linkid);
        // change the image
        if (direction == 'downvote') {
            dir_up.attr('src', '/static/images/voting/aupgrey.gif');
            dir_down.attr('src', '/static/images/voting/adownmod.gif');
        } else if (direction == 'upvote') {
            dir_up.attr('src', '/static/images/voting/aupmod.gif');
            dir_down.attr('src', '/static/images/voting/adowngrey.gif');
        };
      }
    );
    return false;
};
    

$('.downvote').click(function(){
    linkid_raw = $(this).attr('id');
    linkid = linkid_raw.split('_')[1];
    direction = $(this).attr('class');
    voting(direction, linkid);
    return false;
});

$('.upvote').click(function(){
    linkid_raw = $(this).attr('id');
    linkid = linkid_raw.split('_')[1];
    direction = $(this).attr('class');
    voting(direction, linkid);
    return false;
});

$('#language_help').click( function() {
    $.jGrowl('<b>Referencia de Idiomas:</b><li>en: Inglés<li>es: Español<li>es-es: Español Latino<li>ca: Català<li>jp: Japonés');
});

$('#submit').click(function (e) {       
    e.preventDefault();
    var url = $('input[name=url]');
    var audio = $('select[name=audio_lang]');
    var subtitle = $('select[name=subtitle]');
    var post_url = $('form#add_link_form[action]').attr('action');
      //Simple validation to make sure user entered something
        //If error found, add hightlight class to the text field
        if (url.val()==''||url.val()=='http://') {
            url.addClass('hightlight');
            return false;
        } else url.removeClass('hightlight');

        if (audio.val()=='') {
            $('label[for=id_audio_lang]').addClass('hightlight');
            return false;
        } else $('label[for=id_audio_lang]').removeClass('hightlight');

    var dataString = 'url='+ url.val() + '&audio_lang=' + audio.val() + '&subtitle=' + subtitle.val() + '&csrfmiddlewaretoken=' + getCookie('csrftoken');
    //alert (dataString);return false;  
    $.ajax({  
      type: "POST",  
      url: post_url,  
      data: dataString,  
      success: function(data) {  
        if (data.mensaje  == 'Gracias'){
            $.jGrowl("El enlace se ha guardado exitosamente");
        }
      }  
    });  

    return false;
});
