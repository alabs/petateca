// notify: severidad y mensaje. 
function notify(severity, message){
  $('#notify').html('<div class="alert-message ' 
      + severity + '"> <a class="close" href="#">×</a> <p> ' + message + '</p></div>').show();
  $('.alert-message').fadeIn()
  window.location.replace('#notify');
}

function notify_bug() {
  message = 'Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net';
  notify('error', message);
}

function error_add(selector){
    selector.parent().parent().addClass('error');
}

function error_remove(selector){
    selector.parent().parent().removeClass('error');
}



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

//function lookup( selector, type ) {
//   // Magia de /series, se trae los generos, cadenas y listado alfabetico a traves dea jaax (.load)
//    $(selector).click(
//    function() {
//          $('#series_list').html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
//          letter = $(this).attr('href');
//          newlet = letter.substring(1);
//          $('#series_list').load('/series/lookup/' + type + '/' + newlet + '/');
//          $(this).addClass('nolink');
//          if (typeof ($last) != 'undefined') { $last.removeClass('nolink'); } 
//          $last = $(this);
//        }
//   );
//}


function disc_fav_data(data) {
  // Discriminacion de los favorites dependiendo de la respuesta
  // tambien actualiza el corazon 
  switch (data) {
  case 'yes':
      $("#favorite").html('<a href="#" onclick="favorite();" id="favorite"><img class="heart_fav" src="/static/images/heart_red.png"></a>');
      // $.jGrowl('Has agregado esta serie como favorita');
      message = 'Has agregado esta serie como favorita';
      notify('success', message);
      break;
  case 'no':
      $("#favorite").html('<a href="#" onclick="favorite();" id="favorite"><img class="heart_fav" src="/static/images/heart_black.png"></a>');
      //$.jGrowl('Has quitado esta serie de tus favoritas');
      message = 'Has quitado esta serie de tus favoritas';
      notify('success', message);
      break;
  case 'no-user':
      // $.jGrowl('Para poder votar debes estar registrado o haber iniciado sesion', {
      //     header: 'Error'
      // });
      message = 'Para poder votar debes estar registrado o haber iniciado sesion';
      notify('error', message);
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


function disc_rat_data(data){
  // Las respuestas cuando se hace un rating, ver en el view de series para el tratamiento
  switch(data)
          {
          //case 'no-user':
          //        $.jGrowl('Para poder votar debes estar registrado o haber iniciado sesion', { header: 'Error' });
          //        break;
          //case 'Vote changed.':
          //        $.jGrowl('Su voto ha sido cambiado'); 
          //        break;
          case 'Ok':
                  // $.jGrowl('Su voto ha sido guardado'); 
                  message = 'Su voto ha sido guardado';
                  notify('success', message);
                  break;
          case 'Error':
                  notify_bug();
                  //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                  break;
          default:
                  notify_bug();
                  //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
          }
}


//Uservoice (Sugerencias)
var uvOptions = {};
(function() {
  var uv = document.createElement('script'); uv.type = 'text/javascript'; uv.async = true;
  uv.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'widget.uservoice.com/FFqUl0DJZxv4hDFg4EbALQ.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(uv, s);
})();


// Google Analytics
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-22940195-1']);
_gaq.push(['_trackPageview']);
(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

// Google + button
gapi.plusone.go();

function voting( direction, linktype, linkid ){
  // tratamiento de las votaciones de links
  // campos que vamos a tratar
  var $linkscore = $('span#linkscore' + linkid);
  var dir_down = $('img#down_' + linktype + '_' + linkid);
  var dir_up = $('img#up_' + linktype + '_' + linkid);

  // loading
  $linkscore.html('<img style="margin-bottom:0 !important;" src="/static/images/ajax-loading.gif">');
  // la url va por tipo
  switch (linktype) {
      case 'episode':
          url = '/series/links/vote/episode/';
          break;
      case 'season':
          url = '/series/links/vote/season/';
          break;
      case 'book':
          url = '/books/links/vote/book/';
          break;
      default:
          notify_bug();
          //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
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

function hide_tagcloud(selector) {
  // muestra el siguiente div que encuentre
     selector 
          .parent()
          .parent()
          .children('div')
          .hide(); 

}

function show_tagcloud(selector) {
  // muestra el siguiente div que encuentre
     selector 
          .parent()
          .parent()
          .children('div')
          .show(); 

}


$(document).ready(function () {

  // Rating de estrellas, se envia el rating por post a /serie/nombre

  $('.ratingstar').rating({
      callback: function (value, link) {
          var url = window.location.pathname + 'rate/';
          if (!value) {
            var value = 0;
          }
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
      $inside.html('<img class="loading-small" src="/static/images/ajax-loading-bar.gif" />');
      serie_season_raw = season_full_id.split('_');
      var serie_id = serie_season_raw[1];
      var season_n = serie_season_raw[3];
      $inside.load('/series/lookup/serie/' + serie_id + '/season/' + season_n + '/');
  });

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
                 // f.addClass('hightlight'); 
                 //f.parents().parents().addClass('error');
                 error_add(f);
                 notify('error', 'Ha ocurrido un error durante el envio, revisa el formulario');
                 //return false;
             } else {
                 //f.removeClass('hightlight');
                 error_remove(f);
                 //f.parents().parents().removeClass('error');
             }
         });
      
         // TODO: genres hightlight

          // TODO: comprobamos que la duracion sea un numero
      });

  // Que cuando se haga click en el rating envia el valor por post
//    $('.ratingstar').rating({ callback: function(value, link){
//            $.post(url, { 'rating': value }, function(data){ disc_rat_data(data); } ); }
//    });


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
             success: function(content) {
                // Set the tooltip content
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
       at: 'right center',
       my: 'left center',
       viewport: $(window),
       adjust: {
          method: 'flip',
          x: 0,
          y: 0
       }
    },
       style: {
          classes: 'ui-tooltip-light'
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

      $inside = $(this).siblings('ul');
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

  $('.add_link_single').live('click', function(e){
  // agregar enlace para libros y peliculas
      e.preventDefault();
      $(this).hide();
      var object_raw = $(this).attr('id');
      var type = object_raw.split('_')[0];
      var object_id = object_raw.split('_')[1];
      $inside = $('#inside_' + type + '_' + object_id);
      $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');
      if ( type === 'book' ) {
          $inside.load('/books/links/add/book/' + object_id + '/');
      } else {
          notify_bug();
          //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
      }
  });

  $('.add_link').live('click', function(e){
  // agregar enlace para listados de series (episodio y temporada)
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
              //f.parents().parents().addClass('error'); 
              error_add(f);
              return false;
          } else {
              error_remove(f);
              //f.parents().parents().removeClass('error');
          }
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
                      //$.jGrowl('El episodio se ha creado exitosamente, gracias por colaborar');
                      notify('success', 'El episodio se ha creado exitosamente, gracias por colaborar');
                      var $inside = $('#inside_serie_' + serie + '_season_' + season);
                      $inside.html('<img src="/static/images/ajax-loading-bar.gif">');
                      $inside.load('/series/lookup/serie/' + serie + '/season/' + season + '/');
                      break;
                  case 'Duplicado':
                      //$.jGrowl('Ese episodio ya se encuentra, comprueba el numero');
                      notify('error', 'Ese episodio ya se encuentra, comprueba el numero');
                      break;
                  default:
                      notify_bug();
                      //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
              }
      }  
      );  
  });

  // muestra la referencia de idiomas
  $('#language_help').live('click', function() {
      //$.jGrowl('<a href="/faq">FAQ</a><b>Referencia de Idiomas:</b><li>en: Inglés<li>es: Español<li>es-es: Español Latino<li>ca: Català<li>jp: Japonés');
      notify('info', '<a href="/faq">FAQ</a><br><b>Referencia de Idiomas:</b><li>en: Inglés<li>es: Español<li>es-es: Español Latino<li>ca: Català<li>jp: Japonés');
    });

    // busqueda en thepiratebay
    $('#search_pb').live('click', function() {
        query = $(this).attr('rel');
        //$.jGrowl('Abriendo búsqueda en The Pirate Bay para ' + query);
        notify('info', 'Abriendo búsqueda en The Pirate Bay para ' + query);
        window.open( 'http://thepiratebay.org/search/' + query + '/0/7/0');
    });

    // busqueda en torrentz
    $('#search_torrentz').live('click', function() {
        query = $(this).attr('rel');
        //$.jGrowl('Abriendo búsqueda en Torrenz para ' + query);
        notify('info', 'Abriendo búsqueda en Torrentz para ' + query);
        window.open( 'http://torrentz.eu/search?f=' + query);
    });

    // busqueda en la lista de sinde 
    $('#search_listadesinde').live('click', function() {
        query = $(this).attr('rel');
        //$.jGrowl('Abriendo búsqueda en La Lista de Sinde para ' + query);
        notify('info', 'Abriendo búsqueda en La Lista de Sinde para ' + query);
        window.open('http://www.google.com/cse?cx=004411908642504437083%3A1dyk2klbrj8&ie=UTF-8&q=' + query + '&sa=Buscar+descargas!&siteurl=lalistadesinde.net%2F');
    });


    // tratamiento de agregar un link
    $('#submit_link').live('click', function (e) {
        e.preventDefault();
        var url = $('input[name=url]');
        var lang = $('select[name=lang]');
        var audio = $('select[name=audio_lang]');
        var subtitle = $('select[name=subtitle]');
        var post_url = $('form#add_link_form[action]').attr('action');
        //Simple validation to make sure user entered something
            //If error found, add hightlight class to the text field
            if (url.val()===''||url.val()==='http://') {
                //url.parents().parents().addClass('error');
                error_add(url);
                return false;
            } else {
                error_remove(url); 
             //   url.parents().parents().removeClass('error');
            }

            if (audio.val()==='') {
                //$('label[for=id_audio_lang]').parents().parents().addClass('error');
                error_add( $('label[for=id_audio_lang]') );
                return false;
            } else {
            //    $('label[for=id_audio_lang]').parents('li').removeClass('error');
                error_remove( $('label[for=id_audio_lang]') );
            }

            if (lang.val()==='') {
             //   $('label[for=id_lang]').parents.('li').addClass('error');
                error_add($('label[for=id_lang]'));
                return false;
            } else {
            //    $('label[for=id_lang]').parents.('li').removeClass('error');
                error_remove($('label[for=id_lang]'));
            }
        $.post(post_url, {
            'url': url.val(), 
            'lang': lang.val(), 
            'audio_lang': audio.val(), 
            'subtitle': subtitle.val(),
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function(data) {
            if (data.mensaje  == 'Gracias'){
                //$.jGrowl('El enlace se ha guardado exitosamente');
                var message = 'El enlace se ha guardado exitosamente.';
                notify('success', message);
                if ( data.type == 'book') {
                    location.reload(true);
                }
            } else if (data.mensaje == 'Link duplicado') {
                var message = 'Link duplicado, prueba a agregar otro';
                notify('error', message);
            } else {
                notify_bug();
                //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
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

    // lookup('.abc', 'letter'); 
    // lookup('.genre', 'genre'); 
    // lookup('.network', 'network'); 


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
            //$id_season.addClass('hightlight'); 
            error_add($id_season);
            return false;
        } else {
            //$id_season.removeClass('hightlight'); 
            error_remove($id_season);
        }

        $.post(action, {
            'season': $id_season.val(),
            'csrfmiddlewaretoken': getCookie('csrftoken')
        }, function(data){
            switch (data.message) {
            case 'OK':
                //$.jGrowl('Temporada agregada, redireccionando...');
                var message = 'Temporada agregada, redireccionando...';
                notify('success', message);
                window.location.replace(data.redirect);
                break;
            case 'Duplicated':
                //$.jGrowl('Esa temporada ya se encuentra, comprueba el número.');
                var message = 'Esa temporada ya se encuentra, comprueba el número.';
                notify('error', message);
                break;
            case 'Error':
                notify_bug();
                //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                break;
            default:
                notify_bug();
                //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                break;
            }
        });
        event.preventDefault();
    });

    $('.comment_form').submit(function(e){
        // Form de comentarios, que no salga sin nada
        $comment = $('.comment_form').children('li').children('div').children('#id_comment');
        if ($comment.val()==='') {
            e.preventDefault();
            error_add($comment);
            notify('error', 'Agrega tu comentario');
        } else {
            error_remove($comment);
        }
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

    // TRACKING
    $('.tracking').live('click', function(){ 
        // Enviamos el valor de ultimo episodio por AJAX
        serie_season_episode = $(this).parent().attr('id').split('_');
        serie_id = serie_season_episode[1];
        season = serie_season_episode[2]; 
        episode = serie_season_episode[3]; 
        $.post('/tracking/set/', {
                'serie_id': serie_id,
                'season': season,
                'episode': episode,
                'csrfmiddlewaretoken': getCookie('csrftoken')
                }, function(data){
                    switch (data) {
                        case 'OK':
                            // $.jGrowl('Has marcado el episodio como visto');
                            notify('success', 'Has marcado el episodio como visto.');
                            check_viewed(serie_id, season, episode);
                            break;
                        case 'Error':
                            notify_bug();
                            //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                            break;
                        default:
                            notify_bug();
                            //$.jGrowl('Ha ocurrido un error durante el envio, reportalo a bugs@liberateca.net');
                            break;
                    }
                }
        );
    });

    $('.serie_hidden').live('click', function(event){
        event.preventDefault();

        var $refresh = $(this).children('.refresh');

        // poor mans toogle
        // comprobamos si ya estaba seleccionada anteriormente
        var check_selected = $(this).attr('class'); 
        if (check_selected.indexOf('selected_list') != -1) {
            // si ya existe lo cerramos
            $(this).removeClass('selected_list');
            $(this).siblings().html('');
            $refresh.hide();
            return false;
        } else { 
            $(this).addClass('selected_list');
        }

        // loading..
        var $inside = $(this).next();
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');

        // conseguimos serie_id
        var serie_id_raw = $(this).attr('id'); 
        var serie_id = serie_id_raw.split('_')[1]; // poker face ('_')

        $.post('/tracking/show/', { 
            'serie_id' : serie_id,
            'csrfmiddlewaretoken': getCookie('csrftoken')
            }, function(data){
                $inside.html(data);
            }
        );

        // mostramos el refresh
        $refresh.show();
    }); 

    $('.refresh').hide();

    $('.refresh').live('click', function(event){
        // recargar los episodios del tracking/seguimiento
        event.preventDefault();

        // loading..
        var $inside = $(this).parent().next();
        $inside.html('<img class="center" src="/static/images/ajax-loading-bar.gif" />');

        // conseguimos serie_id
        var serie_id_raw = $(this).parent().attr('id'); 
        var serie_id = serie_id_raw.split('_')[1]; // poker face ('_')

        $.post('/tracking/show/', { 
            'serie_id' : serie_id,
            'csrfmiddlewaretoken': getCookie('csrftoken')
            }, function(data){
                $inside.html(data);
            }
        );

        event.stopPropagation();
    }); 


    $('.go-jump').live('click', function(event){
        // ir a la pagina de la serie al ser click en la flechita verde
        // especialmente util en seguimiento por ejemplo
        event.preventDefault();
        var href = $(this).attr('rel');
        window.location.href = href;
        event.stopPropagation();
    }); 

    $('.tagcloud').hide();
    $('.show_tagcloud').click( function() { 
        // comprobamos su visibilidad

        var visibilidad_raw = $(this).parent().parent().children('div').attr('style'); 
        var visibilidad = visibilidad_raw.split(': ')[1].split(';')[0]

        // en funcion si esta mostrado o no lo escondemos/monstramos 
        // poor's man toggle :(
        switch(visibilidad) {
            case  "block" : 
                hide_tagcloud($(this));
                break;
            case  "none" : 
                show_tagcloud($(this));
                break;
        }

    });

    

    // Twitter style login
    $(".signin").click(function(e) {          
        e.preventDefault();
        $("fieldset#signin_menu").toggle();
        $(".signin").toggleClass("menu-open");
        $("#username").focus();
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

    // respuesta de parents en threaded comments
    $('.comment_reply_link').click( function(){
       // cuando se hace click en reply...

       $(this).hide();

       // copiamos el form de comentarios 
       var comment_form = $('.wrap_write_comment').html();

       // obtenemos el id del parent
       var parent_id = $(this).attr('href').split('comment_')[1];

        // para el threadedcomments, hace falta pasarle el parametro del parent, ej:
        // <input type="hidden" id="id_parent" value="10" name="parent">
        // sin parent se ve asi
        // <input name="parent" id="id_parent" type="hidden">
       // tambien quitamos el posible hightlight de cuando el form esta vacio
       var reply_form = comment_form
            .replace('name="parent"', 'name="parent" value="' + parent_id + '"')
            .replace('class="hightlight"', '');

       // y lo mostramos
       $(this).parent().parent().append(reply_form);
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

$(function(){
/* 

Navegacion en /series/ y /books/ listado de AJAX con parametros del tipo: 

* /series/#/genre/drama/
* /series/#/network/abc/
* /series/#/letter/A/

Utiliza jquery-BBQ y soporta historial en el navegador y links directos

*/

  $(window).bind( "hashchange", function(e) {
    var url = $.param.fragment();

    $(".navigator").each(function(){

      // iterando cada navigator y buscando los links ...
      var href = $(this).attr( "href" );
      var href_nohash = href.split('#')[1];

      // ..a ver si el navigator que esta en la barra de direcciones
      // es igual que el mio...
      if ( href_nohash === url ) {
          // comprobamos el tipo de peticion y abrimos el tagcloud adecuado
          // ej: genre, network, category, author
          var type = url.split('/')[1]; 

          switch (type) {
              case 'genre':
                  show_tagcloud($('.show_tagcloud.genre'));
                  break;
              case 'network':
                  show_tagcloud($('.show_tagcloud.network'));
                  break;
              case 'category':
                  show_tagcloud($('.show_tagcloud.category'));
                  break;
              case 'author':
                  show_tagcloud($('.show_tagcloud.author'));
                  break;
          }

        // cambiamos el estilo del link clickeado
        $(this).addClass( "nolink" );
      } else {
        $(this).removeClass( "nolink" );
        $('#popularity').removeClass('nolink');      
      }
    });

    // books or series
    var object = document.URL.split('/')[3];

    if (url){
        switch (object) {
            case 'series':
              $('#generic_list').html('<img class="loading" src="/static/images/ajax-loading-bar.gif" />');
              // url que esperamos es algo por el estilo: genre/science-fiction
              console.log(url);
              $('#generic_list').load('/series/lookup' + url);
              break;
            case 'books':
              $('#generic_list').html('<img class="loading" src="/static/images/ajax-loading-bar.gif" />');
              // console.log(url);
              // url que esperamos es algo por el estilo: category/drama
              $('#generic_list').load('/books/lookup' + url);
              break;
        }
    }

  });

  $(window).trigger( "hashchange" );

//  $('#add_book_form, #add_serie_form').highlight();

  $('#js-container').jsquares({
      shuffle_in: false, 
      caption_height: 180,
      caption_width: 330
  });
  $('#js-container-2').jsquares({
      shuffle_in: false, 
      caption_height: 180,
      caption_width: 330
  });

  // marcar en header
  section = document.URL.split('/')[3];
  switch (section) {
    case 'blog': 
      $('#header-blog').addClass('header-selected');
      break;
    case 'serie':
       $('#header-serie').addClass('header-selected');
       break;
    case 'series':
       $('#header-serie').addClass('header-selected');
       if (! $.param.fragment()) {
       // Si no hay # en la URL entonces estamos en /
          $('#popularity').addClass('nolink');      
       } 
       break;
    case 'book':
       $('#header-book').addClass('header-selected');
       break;
    case 'books':
       $('#header-book').addClass('header-selected');
       if (! $.param.fragment()) {
       // Si no hay # en la URL entonces estamos en /
          $('#popularity').addClass('nolink');      
       } 
       break;
  }

  // cerrar el notify
  $('.close').live('click', function() {
    $(this).parent().hide();
  }); 

  // si estamos en la pagina de la API, creamos el menu
  if ( $('.header_api').size() != 0 ) {
    $('.sidebar').html('<h2>Indice</h2>');
    $.toc('h1,h3.header_api').appendTo('.sidebar');
  }

  if ( $('.header').size() != 0 ) {
    $('.sidebar').html('<h2>Indice</h2>');
    $.toc('.content h1,.content h2').appendTo('.sidebar');
  }

  $('a[title], .votelink[title]').qtip({
      position: {
         at: 'middle center',
         my: 'top center',
         adjust: {
            method: 'flip',
            x: 0,
            y: 0
         }
      },
         style: {
            classes: 'ui-tooltip-dark'
         }
  });

  $('.input input, .fieldwrapper input, .fieldwrapper textarea, .fieldwrapper select')
    .live('focus', function(){
      $(this).parent().parent().addClass('over');
    })
    .live('blur', function(){
      $(this).parent().parent().removeClass('over');
  }); 


});
