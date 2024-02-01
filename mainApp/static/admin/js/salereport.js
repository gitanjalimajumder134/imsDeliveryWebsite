$(document).ready(function () {
    $(function () {
  $('#branch_id').select2({
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
        $('#branch_id').select2({
            closeOnSelect: false
        });
        $('#pd_id').select2({
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
    })