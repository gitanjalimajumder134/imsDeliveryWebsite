$(document).ready(function () {
    $(function () {
        $('#item').select2({
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
        $('#item').select2({
            closeOnSelect: false
        });
        $('#hub').select2({
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
        $('#hub').select2({
            closeOnSelect: false
        });
        $('#branch').select2({
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
        $('#branch').select2({
            closeOnSelect: false
        });
    })
})