$(document).ready(function () {
    if ((window.location.href.includes("add") ||
      window.location.href.includes("change"))) {
        $(`#id_state`).select2({
          matcher: function (params, data) {
              if ($.trim(params.term) === '') {
                  return data;
              }
      
              keywords=(params.term).split(" ");
      
              for (var i = 0; i < keywords.length; i++) {
                  if (((data.text).toUpperCase()).indexOf((keywords[i]).toUpperCase()) == -1) 
                  return null;
              }
              return data;
          }
      });
    }
})