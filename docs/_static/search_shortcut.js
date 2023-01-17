/**
 * Add shortcut `ctrl+k` to focus on search field
 */

 $(document).ready(() => {
    if (window.location.pathname === '/search.html') {
        $('form.bd-search .input-group').hide(); // Hide Sidebar Search field

        $(document).keydown(function(event) {
            if ((event.ctrlKey || event.metaKey) && event.key == "k") {
                event.preventDefault();
                $('#q').focus();
            }
        });
        
        $('#q').focus(() => {
            $('#shortcut-page').hide();
        });
        $('#q').blur(() => {
            $('#shortcut-page').show();
        });
        
        
    } else {
        $(document).keydown(function(event) {
            if ((event.ctrlKey || event.metaKey) && event.key == "k") {
                event.preventDefault();
                $('#search-input').focus();
            }
        });

        $('#search-input').focus(() => {
            $('#shortcut').hide();
        });
        $('#search-input').blur(() => {
            $('#shortcut').show();
        });
    }
    
    // if OS isn't Mac change visual indication of search field
    if (navigator.platform.indexOf('Mac') === -1) {
        $('#search-shortcut').html("^");
        $('#search-page-shortcut').html("^");
    }
    
});

function onReset() {
    $('#search-form').trigger('reset');
    $('#search-form').trigger('submit');
}