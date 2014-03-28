(function(){
  var target = jQuery('#topbarcontainer');
  //var baseURL = portal_url + '/++theme++ploneorg.theme';
  var baseURL = "http://localhost/plone-doc/_static";
  function loadWidgetHTML(callback) {
    jQuery.ajax({
      url: baseURL + "/js/topbar_index.js",
      jsonpCallback: "populateWidget",
      jsonp: false,
      dataType: "jsonp",
      success: function(data){
        var dataHTML = data.join('\n');
        var html = dataHTML.replace(/\{\{ BASE_URL \}\}/g, baseURL);
        target.html(html);
        return callback();
      }
    });
  }
  function loadWidgetCSS() {
    var cssPaths = ['/css/topbar_reset.css', '/css/topbar.css'];
    jQuery.each(cssPaths, function(i, cssPath){
      var cssLink = jQuery('<link>', {
        rel: 'stylesheet',
        type: 'text/css',
        href: baseURL + cssPath
      });
      cssLink.appendTo('head');
    });
  }
  function loadSearchBox(){
    (function() {
      var cx = '000972445131351556642:syx6s4pgdp8';
      var gcse = document.createElement('script');
      gcse.type = 'text/javascript';
      gcse.async = true;
      gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
      '//www.google.com/cse/cse.js?cx=' + cx;
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(gcse, s);
    })();
  }
  function loadMobileJS(){
    jQuery('#sites-select', target).click(function(){
      location.url = jQuery(this).val;
    });

    jQuery('#display_mobile', target).click(function(evt){
      jQuery('#plone-global-topbar-mainlinks', target).toggleClass('mostrar_mobile');
    });
  }

  jQuery(document).ready(function(){
    target.hide();
    loadWidgetHTML(function(){
      loadWidgetCSS();
      loadSearchBox();
      loadMobileJS();
      target.show();
    });
  });
  
})();
