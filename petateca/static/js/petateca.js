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
        $.jGrowl('Has agregado esta serie como favorita');
        break;
    case 'no':
        $("#favorite").html('<a href="#" onclick="favorite();" id="favorite"><img class="heart_fav" src="/static/images/heart_black.png"></a>');
        $.jGrowl('Has quitado esta serie de tus favoritas');
        break;
    case 'no-user':
        $.jGrowl('Para poder votar debes estar registrado o haber iniciado sesion', {
            header: 'Error'
        });
        break;
    }
}

function favorite() {
    // Tratamiento del favorito
    var imgsrc = $('#favorite img').attr('src');
    if (imgsrc == '/static/images/heart_black.png') {
        decision = 'yes';
    } else if (imgsrc == '/static/images/heart_red.png') {
        decision = 'no';
    }
    $('#favorite').html('<img src="/static/images/ajax-loading.gif">');
    var url = window.location.pathname + 'favorite/';
    if (decision == 'yes') {
        $.post(url, {
            'favorite': 'yes',
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function (data) {
            disc_fav_data(data);
        });
    } else if (decision == 'no') {
        $.post(url, {
            'favorite': 'no',
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
            $.jGrowl('Para poder votar debes estar registrado o haber iniciado sesion', {
                header: 'Error'
            });
            break;
        case 'Vote recorded.':
            $.jGrowl('Su voto ha sido guardado');
            break;
        case 'Vote changed.':
            $.jGrowl('Su voto ha sido cambiado');
            break;
    }
}


function disc_rat_data(data){
    // Las respuestas cuando se hace un rating, ver en el view de series para el tratamiento
    switch(data)
            {
            case 'no-user':
                    $.jGrowl('Para poder votar debes estar registrado o haber iniciado sesion', { header: 'Error' });
                    break;
            case 'Vote recorded.':
                    $.jGrowl('Su voto ha sido guardado'); 
                    break;
            case 'Vote changed.':
                    $.jGrowl('Su voto ha sido cambiado'); 
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
    s.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'cdn.uservoice.com/javascripts/widgets/tab.js';
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


function search_lookup(inputString) {
    // busqueda en ajax
    if (inputString.length < 2) {
        $('#suggestions').fadeOut(); // Hide the suggestions box
    } else {
        $.get('/search/lookup/?query=' + inputString, function(data) { // Do an AJAX call
            $('#suggestions').fadeIn(); // Show the suggestions box
            $('#suggestions').html(data); // Fill the suggestions box
            });
    }
}

function check_viewed(serie_id, season_n, episode_n){
    // Recibe cual temporada/episodio es el ultimo visto, marca los anteriores
    //
    // SOLO PARA EL EPISODIO QUE ESTA VISTO
    var episode_id = '#serie_'.concat(serie_id, '_', season_n, '_', episode_n);
    var $episode = $(episode_id);
    var $checkbox = $(episode_id.concat(' input'));
    $checkbox.attr('checked', 'checked');

    // Cuenta atras desde episode_n, marca los checkbox como vistos 
    // y agrega la clase viewed a los links
    for (i = episode_n; i > 0; i--){
        var episode_prev = '#serie_'.concat(serie_id, '_', season_n, '_', i);
        var $checkbox_prev = $(episode_prev.concat(' input'));
        var $link_prev = $(episode_prev.concat(' a'));
        $checkbox_prev.attr('checked', 'checked');
        $link_prev.addClass('viewed');
    }

    // Cuenta atras desde season_n, marca los checkbox como vistos 
    // y agrega la clase viewed a los links
    for (i = season_n; i > 0; i--){
        var season_id = '#serie_'.concat(serie_id, '_season_', i);
        var $season = $(season_id);
        $previous_episodes = $season.next().children().children().children().filter('.episode');
        $previous_episodes.children('input').attr('checked', 'checked');
        $previous_episodes.children('a').addClass('viewed');
    }

    // Marcamos los siguientes como no vistos, por si se equivoca al seleccionarlo
    var episode_n_next = parseInt(episode_n, 10) + 1;
    for (i = episode_n_next; i < 100; i++){
        var episode_next = '#serie_'.concat(serie_id, '_', season_n, '_', i);
        var $checkbox_next = $(episode_next.concat(' input'));
        var $link_next = $(episode_next.concat(' a'));
        $checkbox_next.attr('checked', '');
        $link_next.removeClass('viewed');
    }
}


$(document).ready(function () {
    // Rating de estrellas, se envia el rating por post a /serie/nombre
    $('.ratingstar').rating({
        callback: function (value, link) {
            var url = window.location.pathname + 'rate/';
            $.post(url, {
                'rating': value,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            }, function (data) {
                disc_rat_data(data);
            });
        }
    }); 

    $('.selected_list').live('click', function(event){
        event.preventDefault();
        $(this).siblings().html('');
    });

    // Listado de episodios por temporadas
    $('.season').live('click', function(event){ 
        event.preventDefault();

        // poor mans toogle
        // comprobamos si ya estaba seleccionada anteriormente
        var check_selected = $(this).attr('class'); 
        if (check_selected.indexOf('selected_list') != -1) {
            // si ya existe lo cerramos
            $(this).removeClass('selected_list');
            $(this).siblings().html('');
            return false;
        } else { 
            $(this).addClass('selected_list');
        }


        season_full_id = $(this).attr('id');
        $inside = $('#inside_' + season_full_id);
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        serie_season_raw = season_full_id.split('_');
        var serie_id = serie_season_raw[1];
        var season_n = serie_season_raw[3];
        $inside.load('/series/lookup/serie/' + serie_id + '/season/' + season_n + '/');
    });

    // Listado de actores segun serie
    $('#get_actors').click(
        function(){
            $('#actors_list').html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
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
            // Variables que capturamos
            var $name_es = $('input[name=name_es]');
            var $name_en = $('input[name=name_en]');
            var $description_es = $('textarea[name=description_es]');
            var $description_en = $('textarea[name=description_en]');
            var $network = $('select[name=network]');
            var $runtime = $('input[name=runtime]');

            var post_url = $('form#add_serie_form[action]').attr('action');

            // Comprobamos que ningun campo este en blanco
           fields = [ $name_es, $name_en, $description_es, $description_en, $network, $runtime ];
           $.each(fields, function(index, f){
               if (f.val()==='') {
                   event.preventDefault();
                   f.addClass('hightlight'); 
                   //return false;
               } else {f.removeClass('hightlight');}
           });
        
           // TODO: genres hightlight

            // TODO: comprobamos que la duracion sea un numero
        });

    // El popup cuando se hace click en login
  $('.login').each(function(){
        $login = $(this);
        $login.click( function(){ return false; }); 
        $.get('/accounts/login/', function(data){
            $login.qtip(
            {
                id: 'modal', // Since we're only creating one modal, give it an ID so we can style it
                content: {
                    text: data,
                    title: {
                        text: 'Iniciar sesión',
                        button: true
                    }
                },
                position: {
                    my: 'center', // ...at the center of the viewport
                    at: 'center',
                    target: $(window)
                },
                show: {
                    event: 'click', // Show it on click...
                    solo: true, // ...and hide all other tooltips...
                    modal: true // ...and make it modal
                },
                style: 'ui-tooltip-light ui-tooltip-rounded'
            });
            return false;
        });
     });

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
            $(this).fadeIn('slow');
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
//    $('.add_link').colorbox({width:'50%', height:'60%', iframe:true, 
//         onClosed:function(){ location.reload(true); } 
//    });
//
//    // Popup de cambiar avatar
//	$(".avatar_change").colorbox({width:"600px", height:"500px", iframe:true,
//     onClosed:function(){ location.reload(true); } });
//

//  $('.avatar_change').each(function(){
//        $avatar = $(this);
//        $avatar.click( function(){ return false; }); 
//        $.get('/accounts/avatar/change/', function(data){
//            $avatar.qtip(
//            {
//                id: 'modal', // Since we're only creating one modal, give it an ID so we can style it
//                content: {
//                    text: data,
//                    title: {
//                        text: 'Cambiar avatar',
//                        button: true
//                    }
//                },
//                position: {
//                    my: 'center', // ...at the center of the viewport
//                    at: 'center',
//                    target: $(window)
//                },
//                show: {
//                    event: 'click', // Show it on click...
//                    solo: true, // ...and hide all other tooltips...
//                    modal: true // ...and make it modal
//                },
//                style: 'ui-tooltip-light ui-tooltip-rounded'
//            });
//            return false;
//        });
//     });


    // Popup de las series, cuando se pone encima de la imagen
   $('.serie').live('mouseover', function() {
      var url = '/series/lookup/serie/';
      var id = $(this).attr('id');

      // Setup the tooltip...
      $(this).qtip(
      {
         content: {
            text: 'Cargando...', // Generic loading message so we know the data is coming.
            ajax: {
               url: url + id + '/',
               dataType: 'html', // The script returns HTML
               success: function(html) {
                  // Set the tooltip content
                  var content = html;
                  this.set('content.text', content);
 
                  return false; // Prevent default content update
               }
            }
         },
         overwrite: false, // Make sure another tooltip can't overwrite this one without it being explicitly destroyed
         show: {
            ready: true // Needed to make it show on first mouseover event
         },
         position: {
            my: 'left center',
            at: 'right center'
         },
         style: {
            classes: 'ui-tooltip-imdb ui-tooltip-tipsy ui-tooltip-shadow'
         }
       });
    });

    $('.zoom').live('click', function(){
    // listado de episodios
    
        // poor mans toogle
        // comprobamos si ya estaba seleccionada anteriormente
        var check_selected = $(this).attr('class'); 
        if (check_selected.indexOf('selected_list') != -1) {
            // si ya existe lo cerramos
            $(this).removeClass('selected_list');
            $(this).siblings().html('');
            return false;
        } else { 
            $(this).addClass('selected_list');
        }

        $inside = $(this).siblings();
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        href = $(this).attr('href');
        $inside.load(href);
        return false;
    });

    $('.espoiler').live('click', function(e){
    // descripcion del episodio
        e.preventDefault();
        $(this).parent().addClass('selected_list');
        episodeid = $(this).attr('id');
        var $inside = $('#inside' + episodeid);
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        espoiler_id = $(this).attr('rel');
        $inside.load(espoiler_id);
        return false;
    });


    $('.add_link').live('click', function(e){
    // agregar enlace
        e.preventDefault();
        $(this).parent().addClass('selected_list');
        var episoderaw = $(this).attr('id');
        var type = episoderaw.split('_')[0];
        var episodeid = episoderaw.split('_')[1];
        $inside = $('#inside' + episodeid);
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        if ( type === 'epi' ) {
            $inside.load('/series/links/add/episode/' + episodeid + '/');
        } else {
            $inside.load('/series/links/add/season/' + episodeid + '/');
        }
    });

    $('.no_link').live('click', function(e){
    // agregar enlace cuando no hay ninguno
        e.preventDefault();
        var episoderaw = $(this).attr('id');
        var type = episoderaw.split('_')[0];
        var episodeid = episoderaw.split('_')[1];
        $inside = $('#inside' + episodeid);
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
        if ( type === 'epi' ) {
            $inside.load('/series/links/add/episode/' + episodeid + '/');
        } else {
            $inside.load('/series/links/add/season/' + episodeid + '/');
        }
    });


    $('#add_episode').live('click', function(e){
    // agregar episodio, muestra el formulario
        e.preventDefault();
        $inside = $('#episode_inside');
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
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

        // Comprobamos que ningun campo este en blanco
        fields = [ $air_date, $title_es, $title_en, $episode ];
        $.each(fields, function(index, f){
            if (f.val()==='') {
                f.addClass('hightlight'); 
                return false;
            } else {f.removeClass('hightlight');}
        });
    

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
                        $.jGrowl('El episodio se ha creado exitosamente, gracias por colaborar');
                        var $inside = $('#inside_serie_' + serie + '_season_' + season);
                        $inside.html('<img src="/static/images/ajax-loading-bar.gif">');
                        $inside.load('/series/lookup/serie/' + serie + '/season/' + season + '/');
                        break;
                    case 'Duplicado':
                        $.jGrowl('Ese episodio ya se encuentra, comprueba el numero');
                        break;
                    default:
                        $.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
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

    // busqueda en la lista de sinde 
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
                $.jGrowl('El enlace se ha guardado exitosamente');
            } else if (data.mensaje == 'Link duplicado') {
                $.jGrowl('Link duplicado, prueba a agregar otro');
            } else {
                $.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
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
        $('#inside_season_add').load($(this).attr('href'));
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

        $.post(action, {
            'season': $id_season.val(),
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function(data){
            switch (data.message) {
            case 'OK':
                $.jGrowl('Temporada agregada, redireccionando...');
                window.location.replace(data.redirect);
                break;
            case 'Duplicated':
                $.jGrowl('Esa temporada ya se encuentra, comprueba el número.');
                break;
            case 'Error':
                $.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                break;
            default:
                $.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                break;
            }
        });
        event.preventDefault();
    });

    $('#comment_form').submit(function(){
        // Form de comentarios, que no salga sin nada
        $comment = $('#id_comment');
        if ($comment.val()==='') {
            $comment.addClass('hightlight');
            return false;
        } else {$comment.removeClass('hightlight');}
    });

    $('.tracking').live('click', function(){ 
        // Enviamos el valor de ultima por AJAX
        serie_season_episode = $(this).parent().attr('id').split('_');
        serie_id = serie_season_episode[1];
        season = serie_season_episode[2]; 
        episode = serie_season_episode[3]; 
        $.post('/series/tracking/', {
                'serie_id': serie_id,
                'season': season,
                'episode': episode,
                'csrfmiddlewaretoken': getCookie('csrftoken')
                }, function(data){
                    switch (data) {
                        case 'OK':
                            $.jGrowl('Has marcado el episodio como visto');
                            check_viewed(serie_id, season, episode);
                            break;
                        case 'Error':
                            $.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                            break;
                        default:
                            $.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                            alert(data);
                            break;
                    }
                }
        );
    });

    // Muestra el nombre del usuario al hacer overr
    $('.followers[title]').qtip({
        position: {
            my: 'center', // Use the corner...
            at: 'center' // ...and opposite corner
        },
        style: {
            classes: 'ui-tooltip-shadow ui-tooltip-dark'
        }
    });

    // Twitter style login
    $(".signin").click(function(e) {          
        e.preventDefault();
        $("fieldset#signin_menu").toggle();
        $(".signin").toggleClass("menu-open");
    });
    
    $("fieldset#signin_menu").mouseup(function() {
        return false;
    });
    $(document).mouseup(function(e) {
        if($(e.target).parent("a.signin").length===0) {
            $(".signin").removeClass("menu-open");
            $("fieldset#signin_menu").hide();
        }
    });         


    // jquery sticky footer
    function positionFooter(){
        var padding_top = $("footer").css("padding-top").replace("px", "");
        var page_height = $(document.body).height() - padding_top;
        var window_height = $(window).height();
        var difference = window_height - page_height;
        if (difference < 0) {
            difference = 0;
        }
        $("footer")
            .css({ padding: difference + "px 0 0 0" })
            .css('margin-top', '2em');
    }

    positionFooter(); 
 
    $(window)
        .resize(positionFooter);

});
