$(function() {
    $('#sidebar-button').on('click', function() {
        if($('#sidebar-menu:visible').length)
            $('#sidebar-menu').hide();
        else
            $('#sidebar-menu').show();
    });
});
