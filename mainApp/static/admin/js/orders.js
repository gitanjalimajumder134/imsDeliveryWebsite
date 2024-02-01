function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


$(document).ready(function(){
  if (window.location.href.indexOf('?') > 0){
    $('.field-branchID').children().eq(1).children().children().eq(1).children().children().css({"pointer-events": "none","background-color": "lightgray"})
    $('.field-product_id').children().eq(1).children().children().eq(1).children().children().css({"pointer-events": "none","background-color": "lightgray"})
  }
  if (
    window.location.href.includes("add") ||
    window.location.href.includes("change")
  ) {
    // $(".card-body")
    //   .find(".field-branchID")
    //   .parent()
    //   .css({ display: "grid", "grid-template-columns": "480px 480px 480px" });
      // $('label').css({ 'min-width': '100%' });
      $('#id_quantity').css({"pointer-events": "none","background-color": "lightgray"})
      
  }


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

  $('#exportfilterbtn').on('click', function(event){
    var branch = $('.form-control option:selected').val()
    branch = branch.split("=")[1]
    var product = $('.admin-filter-Product li.selected a').attr('id')
    product = product.split("-")[1]
    console.log('fromdate', branch,product)
    var arraydetails = [];
    var dictvalue = {
      branch: branch,
      product: product,
    };
    var data = `{"branch":"${branch}","product":"${product}"}`;
    console.log("dictvalue", dictvalue);
    arraydetails.push(dictvalue);
    let request = new XMLHttpRequest();
    request.open('POST', '/site/order/export', true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    // request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
    request.responseType = 'blob';

    request.onload = function (e) {
        if (this.status === 200) {
            let filename = "";
            let disposition = request.getResponseHeader('Content-Disposition');
            // check filename
            if (disposition && disposition.indexOf('attachment') !== -1) {
                let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                let matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
            }
            let blob = this.response;
            if (window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveBlob(blob, filename);
            }
            else {
                let downloadLink = window.document.createElement('a');
                let contentTypeHeader = request.getResponseHeader("Content-Type");
                downloadLink.href = window.URL.createObjectURL(new Blob([blob], {type: contentTypeHeader}));
                downloadLink.download = filename;
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }
        } else {
            alert('Download failed.')
        }
    };
    request.send(data);
    console.log(data)



  })
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
  
  
  $(".admin-filter-branchID select option").each(function (index) {
    console.log('val', $(this).val())
    var value = $(this).val().split("?")[1]
    $(this).attr('id', value)
    var id = $(this).attr('id')
    $(this).attr("id", id.substring().replace("=", "-"));
    var select = $(this).parent()
    console.log('parent class', select)
    $(select).removeAttr("onchange");
    $(select).on("change", onFilterSelectOption);
  });
})