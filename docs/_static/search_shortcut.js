/**
 * Add shortcut `ctrl+k` to focus on search field
 */

$(document).ready(() => {
    $(document).keydown(function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key == "k") {
            event.preventDefault();
            $('#search-input').focus();
        }
    });
    if (navigator.platform.indexOf('Mac') === -1) {
        $('#search-shortcut-sidebar').html("^K"); // if OS isn't Mac change Visual indication of search field
    }
    
    // Show & hide seach input when focusin & focusout
    $('#search-input').focus(() => {
        $('#search-shortcut-sidebar').hide();
    });
    $('#search-input').focusout(() => {
        $('#search-shortcut-sidebar').show();
    });

    // For Search page
            
    if (window.location.pathname === '/search.html') {
        $('form.bd-search').css('visibility','hidden'); // Hide Sidebar Search field
    }
    if (navigator.platform.indexOf('Mac') === -1) {
        $('#search-shortcut-page').html("^K"); // if OS isn't Mac change Visual indication of search field
    }
    $(document).keydown(function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key == "k") {
          event.preventDefault();
          $('#q').focus();
        }
    });
});
