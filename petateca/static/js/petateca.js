function getCookie(name) {
    // Obtiene una cookie, usado para obtener el CSRF
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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

function lookup( selector, type ) {
   // Magia de /series, se trae los generos, cadenas y listado alfabetico a traves dea jaax (.load)
    $(selector).click(
    function() {
          $('#series_list').html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
          letter = $(this).attr('href');
          newlet = letter.substring(1);
          $('#series_list').load('/series/lookup/' + type + '/' + newlet + '/');
          $(this).addClass('nolink');
          if (typeof ($last) != 'undefined') { $last.removeClass('nolink'); } 
          $last = $(this);
        }
   );
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
    $('#favorite').html('<img src="/static/images/ajax-loading.gif">');
    var url = window.location.pathname;
    if (decision == "yes") {
        $.post(url, {
            'favorite': "favorite",
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function (data) {
            disc_fav_data(data);
        });
    } else if (decision == "no") {
        $.post(url, {
            'no-favorite': "no-favorite",
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function (data) {
            disc_fav_data(data);
        });
    }
}


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


function voting( direction, linktype, linkid ){
    // tratamiento de las votaciones de links
    // campos que vamos a tratar
    var $linkscore = $('span#linkscore' + linkid);
    var dir_down = $('#down_' + linktype + '_' + linkid);
    var dir_up = $('#up_' + linktype + '_' + linkid);
    // loading
    $linkscore.html('<img style="margin-bottom:0 !important;" src="/static/images/ajax-loading.gif">');
    // la url va por tipo
    if ( linktype === 'episode' ) {
        url = '/series/links/vote/episode/';
    } else {
        url = '/series/links/vote/season/';
    }
    // el POST, aka jquery te amo
    $.post(url, { 
                'vote': direction,
                'linkid': linkid,
                'csrfmiddlewaretoken': getCookie('csrftoken')
    }, function (data){ 
        // actualizamos el valor
        $linkscore.html(data.score);

        // actualizamos las imagenes
        if (direction == 'downvote') {
            dir_up.attr('src', '/static/images/voting/aupgrey.gif');
            dir_down.attr('src', '/static/images/voting/adownmod.gif');
        } else if (direction == 'upvote') {
            dir_up.attr('src', '/static/images/voting/aupmod.gif');
            dir_down.attr('src', '/static/images/voting/adowngrey.gif');
        }
      }
    );
    return false;
}

function check_value(selector){
    // Function para checkear que los formularios no esten en blanco
    // FIXME: no funciona el return false
    if (selector.val()==='') {
        selector.addClass('hightlight'); 
        return false;
    } else {selector.removeClass('hightlight');}
}
    

$(document).ready(function () {
    // Rating de estrellas, se envia el rating por post a /serie/nombre
    $('.ratingstar').rating({
        callback: function (value, link) {
            var url = window.location.pathname;
            $.post(url, {
                'rating': value,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            }, function (data) {
                disc_rat_data(data);
            });
        }
    }); 
    // Listado de episodios por temporadas
    $('.season').live('click', function(){ 
            $('#season_list').html('<img src="/static/images/ajax-loading-bar.gif">');
            season = $(this).attr('href');
            $('#season_list').load(season);
            return false; 
        }
    );
    // Listado de actores segun serie
    $('#get_actors').click(
        function(){
            var url = window.location.pathname;
            var serie = url.split('/')[2];
            $.get('/series/lookup/actors/' + serie + '/', {}, 
                function(data){
                    $('#actors_list').html(data);
                }
            ); 
        }
    );

            
        // para el form de add_or_edit_serie
        $('#submit_serie').click(function (event) {
            var $name_es = $('input[name=name_es]');
            var $name_en = $('input[name=name_en]');
            var $description_es = $('textarea[name=description_es]');
            var $description_en = $('textarea[name=description_en]');
            var $network = $('select[name=network]');
            var $runtime = $('input[name=runtime]');

            var post_url = $('form#add_serie_form[action]').attr('action');

            // FIXME: Comprobamos que ningun campo este en blanco, lo suyo seria hacer esto pero no funcioan
           fields = [ $name_es, $name_en, $description_es, $description_en, $network, $runtime ];
           $.each(fields, function(index, f){
               if (f.val()==='') {
                   event.preventDefault();
                   f.addClass('hightlight'); 
                   //return false;
               } else {f.removeClass('hightlight');}
           });
        
           // if ($name_es.val()==='') {
           //     $name_es.addClass('hightlight');
           //     return false;
           // } else {$name_es.removeClass('hightlight');}

           // if ($name_en.val()==='') {
           //     $name_en.addClass('hightlight');
           //     return false;
           // } else {$name_en.removeClass('hightlight');}

           // if ($description_es.val()==='') {
           //     $description_es.addClass('hightlight');
           //     return false;
           // } else {$description_es.removeClass('hightlight');}

           // if ($description_en.val()==='') {
           //     $description_en.addClass('hightlight');
           //     return false;
           // } else {$description_en.removeClass('hightlight');}

           // // TODO: genres hightlight

           // if ($network.val()==='') {
           //     $network.addClass('hightlight');
           //     return false;
           // } else {$network.removeClass('hightlight');}

           // if ($runtime.val()==='') {
           //     $runtime.addClass('hightlight');
           //     return false;
           // } else {$runtime.removeClass('hightlight');}

            // TODO: comprobamos que la duracion sea un numero
        });

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

    // Popup de las series, cuando se pone encima de la imagen
    $('.serie').live('mouseover', function(){
        // Obtenemos el id de la serie y lo buscamos
        var serie = $(this);

        serie.CreateBubblePopup({
            position: 'right',
            align: 'center',
            width: '350',
            innerHtml: '<img src="/static/images/ajax-loading-bar.gif" style="border:0px; vertical-align:middle; margin-right:10px; display:inline;" />',
            innerHtmlStyle: { color:'#fff', 'text-align':'left' },
            themeName: 'all-black',
            themePath: '/static/images/jquerybubblepopup-theme'
        });

        var serie_id = serie.attr('id');
        $.get('/series/lookup/serie/' + serie_id + '/', function(data) {
            serie.SetBubblePopupInnerHtml(data);
        }); 
    });

    $(".zoom").live('click', function(){
    // listado de episodios
        $(this).addClass('selected_list');
        $inside = $(this).siblings();
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        href = $(this).attr('href');
        $inside.load(href);
        return false;
    });

    $(".espoiler").live('click', function(e){
    // descripcion del episodio
        e.preventDefault();
        $(this).parent().addClass('selected_list');
        episodeid = $(this).attr('id');
        $inside = $('#inside' + episodeid);
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        espoiler_id = $(this).attr('rel');
        $inside.load(espoiler_id);
        return false;
    });


    $(".add_link").live('click', function(e){
    // agregar enlace
        e.preventDefault();
        $(this).parent().addClass('selected_list');
        episodeid = $(this).attr('id');
        $inside = $('#inside' + episodeid);
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        episode_rel = $(this).attr('rel');
        $inside.load(episode_rel + episodeid + '/');
        return false;
    });

    $("#add_episode").live('click', function(e){
    // agregar episodio, muestra el formulario
        e.preventDefault();
        $inside = $('#episode_inside');
        episode_href = $(this).attr('href');
        $inside.load(episode_href);
        $(this).hide();
    });

    // agregar episodio, tratamiento del formulario
    $('#submit_episode').live('click', function (e) {
        e.preventDefault();
        var $air_date = $('input[name=air_date]');
        var $title_es = $('input[name=title_es]');
        var $title_en = $('input[name=title_en]');
        var $episode = $('input[name=episode]');
        var post_url = $('form#add_episode_form[action]').attr('action');
    
        // capturamos la temporada y la serie para refrescar una vez se haya agregado 
        var season_serie = post_url.split('/');
        var serie = season_serie[4];
        var season = season_serie[6];

        // FIXME: Comprobamos que ningun campo este en blanco, lo suyo seria hacer esto pero no funcioan
        fields = [ $air_date, $title_es, $title_en, $episode ];
        $.each(fields, function(index, f){
            if (f.val()==='') {
                f.addClass('hightlight'); 
                return false;
            } else {f.removeClass('hightlight');}
        });
    
 //       if ($air_date.val()==='') {
 //           $air_date.addClass('hightlight');
 //           return false;
 //       } else { $air_date.removeClass('hightlight'); }

 //       if ($title_es.val()==='') {
 //           $title_es.addClass('hightlight');
 //           return false;
 //       } else $title_es.removeClass('hightlight');

 //       if ($title_en.val()=='') {
 //           $title_en.addClass('hightlight');
 //           return false;
 //       } else $title_en.removeClass('hightlight');

 //       if ($episode.val()=='') {
 //           $episode.addClass('hightlight');
 //           return false;
 //       } else $episode.removeClass('hightlight');

        // TODO: Comprobamos que la fecha este en un formato valido 

        // TODO: Comprobamos que el numero de episodio sea un entero

        // enviamos la peticion, title = title_en
        $.post(post_url, {
            'air_date': $air_date.val(), 
            'title_es': $title_es.val(), 
            'title_en': $title_en.val(), 
            'title': $title_en.val(), 
            'episode': $episode.val(), 
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function(data) {
                switch (data) {
                    case 'OK':
                        $.jGrowl("El episodio se ha creado exitosamente, gracias por colaborar");
                        $('#season_list').html('<img src="/static/images/ajax-loading-bar.gif">');
                        $('#season_list').load('/series/lookup/serie/' + serie + '/season/' + season + '/');
                        return false; 
                        break;
                    case 'Duplicado':
                        $.jGrowl("Ese episodio ya se encuentra, comprueba el numero");
                        break;
                    default:
                        $.jGrowl("Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net");
                }
        }  
        );  
    });

    // muestra la referencia de idiomas
    $('#language_help').live('click', function() {
        $.jGrowl('<a href="/faq">FAQ</a><b>Referencia de Idiomas:</b><li>en: Inglés<li>es: Español<li>es-es: Español Latino<li>ca: Català<li>jp: Japonés');
    });

    // busqueda en thepiratebay
    $('#search_pb').live('click', function() {
        query = $(this).attr('rel');
        $.jGrowl('Abriendo búsqueda en The Pirate Bay para ' + query);
        window.open( 'http://thepiratebay.org/search/' + query + '/0/7/0');
    });

    // busqueda en torrentz
    $('#search_torrentz').live('click', function() {
        query = $(this).attr('rel');
        $.jGrowl('Abriendo búsqueda en Torrenz para ' + query);
        window.open( 'http://torrentz.eu/search?f=' + query);
    });

    // busqueda en la lista de sinde ;)
    $('#search_listadesinde').live('click', function() {
        query = $(this).attr('rel');
        $.jGrowl('Abriendo búsqueda en La Lista de Sinde para ' + query);
        window.open('http://www.google.com/cse?cx=004411908642504437083%3A1dyk2klbrj8&ie=UTF-8&q=' + query + '&sa=Buscar+descargas!&siteurl=lalistadesinde.net%2F');
    });


    // tratamiento de agregar un link
    $('#submit_link').live('click', function (e) {
        e.preventDefault();
        var url = $('input[name=url]');
        var audio = $('select[name=audio_lang]');
        var subtitle = $('select[name=subtitle]');
        var post_url = $('form#add_link_form[action]').attr('action');
        //Simple validation to make sure user entered something
            //If error found, add hightlight class to the text field
            if (url.val()===''||url.val()==='http://') {
                url.addClass('hightlight');
                return false;
            } else {url.removeClass('hightlight');}

            if (audio.val()==='') {
                $('label[for=id_audio_lang]').addClass('hightlight');
                return false;
            } else {$('label[for=id_audio_lang]').removeClass('hightlight');}

        $.post(post_url, {
            'url': url.val(), 
            'audio_lang': audio.val(), 
            'subtitle': subtitle.val(),
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function(data) {
            if (data.mensaje  == 'Gracias'){
                $.jGrowl("El enlace se ha guardado exitosamente");
            } else if (data.mensaje == 'Link duplicado') {
                $.jGrowl("Link duplicado, prueba a agregar otro");
            } else {
                $.jGrowl("Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net");
            }
        }  
        );  

        return false;
    });


    // tratamiento de las votaciones de links
    $('.votelink').live('click', function(){
        linkid_raw = $(this).attr('id');
        linksplit = linkid_raw.split('_');
        // linkdir = [up, down]
        linkdir = linksplit[0];
        // linktype = [season, episode]
        linktype = linksplit[1];
        // linkid = link.id (ej: 666)
        linkid = linksplit[2];
        // discrimina linkdir
        if (linkdir === 'down') {
            direction = 'downvote';
        } else if (linkdir === 'up') {
            direction ='upvote';
        }
        // envia la votacion
        voting(direction, linktype, linkid);
        return false;
    });

    lookup('.abc', 'letter'); 
    lookup('.genre', 'genre'); 
    lookup('.network', 'network'); 


    // Formulario de agregar temporada
    $('#season_add').bind('click', function(event) {
        // AJAX para traer el formulario
        event.preventDefault();
        $('#season_add_form').load($(this).attr('href'));
        return false;
    });

    $('#form_add_season').live('submit', function(event){
        // AJAX que envia y procesa los resultados al agregar temporada
        var action = $('#form_add_season').attr('action');
        var $id_season = $('#id_season');

        if ($id_season.val()==='') {
            $id_season.addClass('hightlight'); 
            return false;
        } else {$id_season.removeClass('hightlight');}

        $.post(action, {'season': $id_season.val()}, function(data){
            switch (data.message) {
            case 'OK':
                $.jGrowl("Temporada agregada, redireccionando...");
                window.location.replace(data.redirect);
                break;
            case 'Duplicated':
                $.jGrowl("Esa temporada ya se encuentra, comprueba el número.");
                break;
            case 'Error':
                $.jGrowl("Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net");
                break;
            default:
                $.jGrowl("Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net");
                break;
            }
        });
        event.preventDefault();
    });


});
