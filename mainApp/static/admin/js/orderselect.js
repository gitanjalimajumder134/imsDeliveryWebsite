$(document).ready(function(){
    
    if (
      window.location.href.includes("add") ||
      window.location.href.includes("change")
    ) {
      $('#id_branchID').select2({
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
      $('#id_product_id').select2({
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
    $('#id_salehub').select2({
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