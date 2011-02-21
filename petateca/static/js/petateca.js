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



$(document).ready(function(){
        $('.serie').CreateBubblePopup({
                                        position: 'top',
                                        align: 'center',
                                        width: '300',
                                        innerHtml: '<img src="/static/images/ajax-loading.gif" style="border:0px; vertical-align:middle; margin-right:10px; display:inline;" />',
                                        innerHtmlStyle: { color:'#FFFFFF', 'text-align':'left', 'font-size':'110%' },
                                        themeName: 'all-black',
                                        themePath: '/static/images/jquerybubblepopup-theme'
                                      });
        $('.serie').mouseover(function(){
                var serie = $(this);
                var serie_id = serie.attr('id');
                $.get('/series/lookup/' + serie_id, function(data) {
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
});
