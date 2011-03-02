var options, a;
jQuery(function(){
  options = { serviceUrl:'/search/lookup/' };
  a = $('#query').autocomplete(options);
});

$(document).ready(function(){
	$(".login").colorbox({iframe:true, innerWidth:555, innerHeight:324});
        $('.ratingstar').rating({ callback: function(value, link){
                $.post(url, { 'rating': value }, function(data){ disc_rat_data(data); } ); }
        });


    $('.prel').each(function () {
        if (this.complete) { return; } 
        $(this).hide();
        $(this).load(function () {
            $(this).width($(this).parent().width()).height($(this).parent().height());
            $(this).fadeIn("slow");
        });
    });
});


function disc_rat_data(data){
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


function series_bubble(){
        $('.serie').CreateBubblePopup({
                                        position: 'right',
                                        align: 'center',
                                        width: '300',
                                        innerHtml: '<img src="/static/images/ajax-loading.gif" style="border:0px; vertical-align:middle; margin-right:10px; display:inline;" />',
                                        innerHtmlStyle: { color:'#fff', 'text-align':'left', 'font-size':'110%' },
                                        themeName: 'all-grey',
                                        themePath: '/static/images/jquerybubblepopup-theme'
                                      });
        $('.serie').mouseover(function(){
                var serie = $(this);
                var serie_id = serie.attr('id');
                $.get('/series/lookup/serie/' + serie_id, function(data) {
                var seconds_to_wait = 0;
                    function pause(){
                        var timer = setTimeout(function(){
                            seconds_to_wait--;
                            if(seconds_to_wait > 0){
                                pause();
                            }else{
                                //set new innerHtml for the Bubble Popup
                                serie.SetBubblePopupInnerHtml(data, false); //false -> it shows new innerHtml but doesn't save it, then the script is forced to load everytime the innerHtml... 
                                // take a look in documentation for SetBubblePopupInnerHtml() method
                            };
                        },1000);
                    };pause();
                }); 
        });
    };

function seasons_bubble(){
    $('.season_list').CreateBubblePopup({
        selectable: true,
        position: 'top',
        align: 'center',
        width: '300',
        innerHtml: '<img src="/static/images/ajax-loading.gif" style="border:0px; vertical-align:middle; margin-right:10px; display:inline;" />',
        innerHtmlStyle: { 'text-align':'left', 'font-size':'110%' },
        themeName: 'all-grey',
        themePath: '/static/images/jquerybubblepopup-theme',
    });
    $('.season_list').hover(
        function(){
             var serie = $(this);
             var serie_id = serie.attr('id');
             $.get('/series/lookup/season/' + serie_id, function(data) {
                 serie.SetBubblePopupInnerHtml(data, false);
                 $(".serie").FreezeAllBubblePopups();
             });
        },
        function(){
             $(".serie").UnfreezeAllBubblePopups();
        }
    );
};

$(document).ready(function() {
    // para el popup bubble ajax
    series_bubble();
    seasons_bubble();
    // Muestra el dropdown de las seasons en series
//    $('.season_list').hover(
//        function(){
//            var serie = $(this);
//            var serie_id = serie.attr('id');
//            $.get('/series/lookup/season/' + serie_id, function(data) {
//                serie.append(data);
//                serie.find('ul').slideDown('fast');
//            })
//        },
//        function(){
//            serie.slideUp('fast');
//        }
//    );
//
    //$('.cssdropdown li:has(ul)').hover(
    //    function(e)
    //    {
    //        $(this).find('ul').slideDown('fast', function() {
    //            // Evita que aparezca el bubble sobre las temporadas
    //            $(".serie").FreezeAllBubblePopups();
    //        });
    //    },
    //    function(e)
    //    {
    //        $(this).find('ul').slideUp('fast', function(){ 
    //            $(".serie").UnfreezeAllBubblePopups();
    //        });
    //    }
    //);
});
