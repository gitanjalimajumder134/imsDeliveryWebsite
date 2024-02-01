$(document).ready(function(){
    $('#id_source').select2({
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
    $('#id_branchdestination').select2({
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
    $('#id_hubdestination').select2({
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
    $('#id_SelectTo').select2({
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
    $('#id_selectfrom').select2({
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
    // $('select[id^=id_transferid-][id$=-item]').select2({
    //     matcher: function (params, data) {
    //       if ($.trim(params.term) === '') {
    //           return data;
    //       }
    
    //       keywords=(params.term).split(" ");
    
    //       for (var i = 0; i < keywords.length; i++) {
    //           if (((data.text).toUpperCase()).indexOf((keywords[i]).toUpperCase()) == -1) 
    //           return null;
    //       }
    //       return data;
    //   }
    // });


    
})