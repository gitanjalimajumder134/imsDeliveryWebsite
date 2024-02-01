(function ($) {
    $(document).ready(function () {
      if (
        !(window.location.href.includes("add") ||
        window.location.href.includes("change"))
      ) {
        $('.datetimeshortcuts').css({ display: "none"})
      }
      /// Filter Multi Select /////
      var r = $(
        '<input id="multifilterbtn" class = "btn btn-success" type="button" value="Filter"/>'
      );
      var exportfile = $(
        '<input id="exportfilterbtn" class = "btn btn-success" type="button" value="Export"/>'
      );
      $("#changelist-filter").append(r);
      
  
      
      
      $("#changelist-filter").append(exportfile);

    //   $('#exportfilterbtn').on('click', function(event){
    //     console.log('hello')
    //     var fromdate = $('#id_transferdate__range__gte').val()
    //     var todate = $('#id_transferdate__range__lte').val()
    //     var source = $('#id_transferdate__range__gte').val()
    //     var fromdate = $('#id_transferdate__range__gte').val()
    //     console.log('fromdate', fromdate)
    //   })
      $("#multifilterbtn").on("click", function (e) {
        e.preventDefault()
        for (i= 0; i < multiSelectFilters.length; i++){
          multiSelectFilters[i] = (multiSelectFilters[i]).replace("-","=")
          console.log("replc", multiSelectFilters)
        }
        console.log('multiselect', multiSelectFilters)
        var queryString = multiSelectFilters.join("&");
  
        console.log("QUERY FOR ", queryString);
        console.log("url", `&${queryString}`);
        let url = window.location.href;
        if (url.indexOf("?") > -1) {
          url = url.slice(0, url.indexOf("?"));
          url += `?${queryString}`;
        } else {
          url += `?${queryString}`;
        }
        console.log('url', url)
        window.location.href = url;
      });
      var BreakException = {};
  
      var multiSelectFilters = [];


      const onFilterSelected = (e) => {
        var target = e.target.id;
        var key = target.split("-")[0];
  
        // console.log("This id", $(`#${target}`))
        // if ($(`#${target}`).parent().hasClass('selected')){
        //     console.log('parent', )
        //     $(`#${target}`).parent().removeClass('selected')
        // }
        // else{
        //     console.log('parent select',)
        //     $(`#${target}`).parent().addClass('selected')
        // }
        // $(`#${target}`).parent().removeClass('selected')
        // $(`#${target}`).parent().each(function(){
        //     $(`#${target}`).parent().addClass('selected')
        // })
  
        console.log("key", key);
  
        // $("#changelist-filter ul > li > a").each(function (index) {
        //     var id = $(this).attr('href')
        //     $(this).parent().removeClass('selected')
        // });
  
        var targetElement = multiSelectFilters.find((el) => el.includes(key));
        console.log("target element", targetElement);
        if (targetElement) {
          var indexOf = multiSelectFilters.indexOf(targetElement);
          console.log("index", indexOf);
          multiSelectFilters.splice(indexOf, 1);
          console.log("if choose target", target);
          multiSelectFilters.push(target);
          console.log("target removed", target);
        } else {
          multiSelectFilters.push(target);
          console.log("target added", target);
          console.log("else choose target", (target));
        }
  
        console.log("Targeted ", targetElement);
        $("#changelist-filter ul > li > a").each(function (index) {
          var id = $(this).attr("href");
          $(this).parent().removeClass("selected");
        });
  
        for (i= 0; i < multiSelectFilters.length; i++){
          $(`#${multiSelectFilters[i]}`).parent().addClass('selected')
        }
        console.log("SELECTED FILTERS ", multiSelectFilters);
        $(".admindatefilter p").find('input').each(function (index) {
          var keys = $(this).attr("name")
          var id = $(this).attr("id")
          $(this).ready(function(){
            var value = $('#'+ id).val();
           
            var targetElements = multiSelectFilters.find((el) => el.includes(keys)); 
            console.log("target element", targetElements); 
            if (targetElements) {
              var indexOf = multiSelectFilters.indexOf(targetElements);
              console.log("index", indexOf);
              multiSelectFilters.splice(indexOf, 1); 
              console.log("if choose target",  value);
              multiSelectFilters.push( keys + "=" + value);
              console.log(" value removed",  keys + "=" + value);
            } else {
              multiSelectFilters.push( keys + "=" + value);
              console.log(" value added",  keys + "=" + value);
              console.log("else choose  value", ( keys + "=" + value));
            }
          })
          
        })
      };

      const onFilterSelectOption = (e) => {
        var target = e.target.value;
        target = target.split("?")[1]
        target = target.replace("=","-")
        var key = target.split("-")[0];
        
        console.log("key", key, target);

      
        var targetElement = multiSelectFilters.find((el) => el.includes(key));
        console.log("target element", targetElement);
        if (targetElement) {
          var indexOf = multiSelectFilters.indexOf(targetElement);
          console.log("index", indexOf);
          multiSelectFilters.splice(indexOf, 1);
          console.log("if choose target", target);
          multiSelectFilters.push(target);
          console.log("target removed", target);
        } else {
          multiSelectFilters.push(target);
          console.log("target added", target);
          console.log("else choose target", (target));
        }
  
        console.log("Targeted ", targetElement);
        $("#changelist-filter ul > li > a").each(function (index) {
          var id = $(this).attr("href");
          $(this).parent().removeClass("selected");
        });
  
        for (i= 0; i < multiSelectFilters.length; i++){
          $(`#${multiSelectFilters[i]}`).parent().addClass('selected')
        }
        console.log("SELECTED FILTERS ", multiSelectFilters);

        
      };
  
      $("#changelist-filter ul > li > a").each(function (index) {
        var id = $(this).attr("href");
        $(this).removeAttr("href");
        console.log("Setting Id ", id.substring(1).replace("=", "-"));
        $(this).attr("id", id.substring(1).replace("=", "-"));
        $(this).on("click", onFilterSelected);
      });
      
      
      $(".admin-filter-source select option").each(function (index) {
        console.log('val', $(this).val())
        var value = $(this).val().split("?")[1]
        $(this).attr('id', value)
        var id = $(this).attr('id')
        $(this).attr("id", id.substring().replace("=", "-"));
        var select = $(this).parent()
        console.log('parent class', select)
        $(select).removeAttr("onchange");
        $(select).on('change', function(e){
            console.log('click')
        })
        $(select).on("change", onFilterSelectOption);
      });

       
      
    });
  })(django.jQuery);
  
