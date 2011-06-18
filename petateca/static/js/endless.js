(function($) {
    $(document).ready(function(){
        // initializes links for ajax requests
        $("a.endless_more").live("click", function() {
            var container = $(this).closest(".endless_container");
            var loading = container.find(".endless_loading");
            $(this).hide();
            loading.show();
            var data = "querystring_key=" + $(this).attr("rel").split(" ")[0];
            $.get($(this).attr("href"), data, function(data) {
                container.before(data);
                container.remove();
            });
            return false;
        });
        $("a.endless_page_link").live("click", function() {
            var data = "querystring_key=" + $(this).attr("rel").split(" ")[0];
            $(this).closest(".endless_page_template").load($(this).attr("href"), data);
            return false;
        }); 
    });
})(jQuery);
