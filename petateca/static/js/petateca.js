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
console.log(data);
}

