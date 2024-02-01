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

var itemOptions = [];
$(document).ready(function () { console.log('hello')
    $(function () {
        if (
            !(window.location.href.includes("add") ||
            window.location.href.includes("change"))
          ) {
            $.ajax({
              type: "GET",
              url: `/site/itemlist`,
              
              success: function (data) {
                console.log("AJAX GOIT ", data);
                
                itemOptions = []
        
                for (itemlist = 0; itemlist < data.itemlist.length; itemlist++) {
                  console.log("length", data.itemlist[itemlist].name);
                  
                  $("#item").append(
                    $("<option></option>")
                      .attr("value", data.itemlist[itemlist].id)
                      .text(data.itemlist[itemlist].name)
                  );
                  console.log(
                    "item OPTIONS ",
                    data.itemlist[itemlist].id,
                    " TEXT ",
                    data.itemlist[itemlist].name
                  );
                  itemOptions.push({
                    id: data.itemlist[itemlist].id,
                    text: data.itemlist[itemlist].name,
                  });
                  
                }
                
                
              },
              failure: function (data) {
                console.log("Got an error dude");
              },
            });
            $('.content-header').append(`<div class="page-content" style="background-color: white">
            <div class="container-fluid">
                    <form method="POST" class="box-typical box-typical-padding">
                    
                        <div class="row">
                            <div class="col-md-3">
                                <fieldset class="form-group">
                                    <label class="form-label semibold" for="exampleInput">Start Date</label>
                                    <div class='input-group date'>
                                        <input  type="date" id="start_date" class="form-control" name="start_date"> 
                                        <span class="input-group-addon"> 
                                            <i class="font-icon font-icon-calend"></i>
                                        </span>
                                    </div>
                                </fieldset>
                            </div>
        
                            <div class="col-md-3">
                                <fieldset class="form-group">
                                    <label class="form-label semibold" for="exampleInput">End Date Date</label>
                                    <div class='input-group date'>
                                        <input  type="date" id="end_date" class="form-control" name="end_date">
                                        <span class="input-group-addon">
                                            <i class="font-icon font-icon-calend"></i>
                                        </span>
                                    </div>
                                </fieldset>
                            </div><div class="col-md-3">
                            <fieldset class="form-group">
                                <label class="form-label semibold" for="exampleCluster">Item</label>
                                <select class="form-control item select2" name="item" id="item">
                                    <option value="">Select Item</option>
                                    
                                                                </select>
                </fieldset>
                </div>
                          <div class="col-md-2">
                          <div class="input-group-btn"> 
                        
                              
                              <button type="button" name="filter_transfer" id="exportfilterbtn" class="btn btn-inline btn-success p-x-3 p-y mt-4">Export
                              </button>
                              </div>
                          </div>
      
                      </div>
            </form></div></div>`);
            for (i = 0; i < itemOptions.length; i++) {
              $(`#item`).append(
                $("<option></option>")
                  .attr("value", itemOptions[i].id)
                  .text(itemOptions[i].text)
              );
            }
            $(`#item`).select2({
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
          $('#exportfilterbtn').on('click', function(event){
            console.log('hello')
            var fromdate = $('#start_date').val()
            var todate = $('#end_date').val()
            var item = $('#item option:selected').val()
            
            console.log('fromdate', fromdate, item)
            var arraydetails = [];
            var dictvalue = {
              fromdate: fromdate,
              todate: todate,
              item: item,
            };
            var data = `{"fromdate":"${fromdate}","todate":"${todate}","item":"${item}"}`;
            console.log("dictvalue", dictvalue);
            arraydetails.push(dictvalue);
            let request = new XMLHttpRequest();
            request.open('POST', '/site/adjustment/export', true);
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
  })
 
    if (
      window.location.href.includes("add") ||
      window.location.href.includes("change")
    ) {
      $(".card-body")
        .find(".field-adjustmentfor")
        .parent()
        .css({ display: "grid", "grid-template-columns": "682px 682px" });
        $(".card-body")
        .find(".field-item")
        .parent()
        .css({ display: "grid", "grid-template-columns": "682px 682px" });
    }
    var value = $("#id_adjustmentfor").val();
    if (value == "") {
      $(".field-adjustableBranch").css("display", "none");
      $("#id_adjustableHub").prop("disabled", true);
      $(".field-adjustableHub").css("display", "flex");
    }
    if (value == "Hub") {
      $(".field-adjustableBranch").css("display", "none");
      $(".field-adjustableHub").css("display", "flex");
    }
    if (value == "Branch") {
      $("#id_adjustableHub").prop("disabled", false);
      $(".field-adjustableHub").css("display", "none");
      $(".field-adjustableBranch").css("display", "flex");
    }
    $("#id_adjustmentfor").on("change", function () {
      console.log("this", $(this));
      var selectVal = $(this).find("option:selected").val();
      console.log("select val:", selectVal);
      if (selectVal == "Hub") {
        $("#id_adjustableHub").prop("disabled", false);
        $("#id_adjustableBranch").val("").trigger("change");
        $(".field-adjustableBranch").css("display", "none");
        $(".field-adjustableHub").css("display", "flex");
      }
      if (selectVal == "Branch") {
        console.log("VAL Branch ", selectVal);
        $("#id_adjustableHub").val("").trigger("change");
        $(".field-adjustableHub").css("display", "none");
        $(".field-adjustableBranch").css("display", "flex");
      }
      if (selectVal == "") {
        $("#id_adjustableHub").prop("selectedIndex", 0);
        $("#id_adjustableBranch").prop("selectedIndex", 0);
        $(".field-adjustableHub").css("display", "flex");
        $(".field-adjustableBranch").css("display", "none");
        $("#id_adjustableHub").prop("disabled", true);
      }
    });
  });
  
  
  