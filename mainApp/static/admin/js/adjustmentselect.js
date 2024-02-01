$(document).ready(function(){
    $('#id_adjustmentfor').select2({
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
    $('#id_adjustableHub').select2({
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
    $('#id_adjustableBranch').select2({
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
    $('#id_adjustmentType').select2({
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
    
})