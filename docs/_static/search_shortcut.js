/**
 * Add shortcut `ctrl+k` to focus on search field
 */

 $(document).ready(() => {
    if (window.location.pathname === '/search.html') {
        $('form.bd-search').css('visibility','hidden'); // Hide Sidebar Search field

        $(document).keydown(function(event) {
            if ((event.ctrlKey || event.metaKey) && event.key == "k") {
                event.preventDefault();
                $('#q').focus();
            }
        });

        // $("button[type='reset']").on('click',function () {
        //     const formInputs = $('#search-form').find('.form-check-input');
        //     if(formInputs.length) {
        //         formInputs.prop('checked',false);
        //         formInputs.find('#doc_section_all').prop('checked',true);
        //     }
        // });
    } else {
        $(document).keydown(function(event) {
            if ((event.ctrlKey || event.metaKey) && event.key == "k") {
                event.preventDefault();
                $('#search-input').focus();
            }
        });
    }

    if (navigator.platform.indexOf('Mac') === -1) {
        $('#search-shortcut').html("^"); // if OS isn't Mac change visual indication of search field
    }

});
