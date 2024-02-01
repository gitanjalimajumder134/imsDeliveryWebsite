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
var huboptions = []
$(document).ready(function () {
  $(function () {
    if (window.location.href.indexOf('?') > 0){
      var urls = window.location.href.split("&")[2]
      urls = urls.split('=')[1]
      var stocktransfer = window.location.href.split("&")[4]
      stocktransfer = stocktransfer.split('=')[1]
      console.log('item', $('#id_SelectTo').siblings().children().children())
      $('#id_transferid-0-item').val(urls)
      $('#id_transferid-0-stocktransfered').val(stocktransfer)
      $("#id_transferid-0-item").css({"pointer-events": "none","background-color": "lightgray"})
      $("#id_transferid-0-stocktransfered").css({"pointer-events": "none","background-color": "lightgray"})
      $("#id_transferid-0-transferablestock").css({"pointer-events": "none","background-color": "lightgray"})
      $("div.add-row").css({ "display": "none" });
      $('#id_SelectTo').siblings().children().children().css({"pointer-events": "none","background-color": "lightgray"})
      $('#id_branchdestination').siblings().children().children().css({"pointer-events": "none","background-color": "lightgray"})
      
     
      
    }
    if (
      window.location.href.includes("change")
    ) {
      
      var transferOnDom = $('.dynamic-transferid').length
      transferOnDom = transferOnDom -1
      $(`#transferid-${transferOnDom}`).css({'display': 'none'})
      console.log('transfer', transferOnDom)
      $("div.add-row").css({ "display": "none" });
    }
  })
  $(function () {
    if (
        !(window.location.href.includes("add") ||
        window.location.href.includes("change"))
      ) {
        $.ajax({
          type: "GET",
          url: `/site/transferitemlist`,
          
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
            huboptions = []
    
            for (hublist = 0; hublist < data.hublist.length; hublist++) {
              console.log("length", data.hublist[hublist].name);
              
              $("#source").append(
                $("<option></option>")
                  .attr("value", data.hublist[hublist].id)
                  .text(data.hublist[hublist].name)
              );
              console.log(
                "Hub OPTIONS ",
                data.hublist[hublist].id,
                " TEXT ",
                data.hublist[hublist].name
              );
              huboptions.push({
                id: data.hublist[hublist].id,
                text: data.hublist[hublist].name,
              });
              
            }
            
            
          },
          failure: function (data) {
            console.log("Got an error dude");
          },
        });
        $('.content-header').append(`<div class="page-content" style="background-color: white">
        <div class="container-fluid">
                <form method="POST" id="transferexportid" class="box-typical box-typical-padding">
                
                    <div class="row">
                    <div class="col-md-3">
                        <fieldset class="form-group">
                            <label class="form-label semibold" for="exampleCluster">Source <span style="color:red">*</span></label>
                            <div class='input-group date'>
                            <select class="form-control source select2" name="source" id="source" required>
                                <option value="">Select Source</option>
                                <option value="all">Select All</option>
                            </select>
                            </div>
                            <p id="sourceError"></p>
                        </fieldset>
                        </div>
                    <div class="col-md-3">
                        <fieldset class="form-group">
                            <label class="form-label semibold" for="exampleCluster">Stock Status <span style="color:red">*</span></label>
                            <div class='input-group date'>
                            <select class="form-control status select2" name="status" id="status" required>
                                <option value="">Select Status</option>
                                <option value="all">Select All</option>
                                <option value="InTransit">In Transit</option>
                                <option value="Delivered">Delivered</option>
                            </select>
                            </div>
                            <p id="statusError"></p>
                        </fieldset>
                        </div>
                        <div class="col-md-3">
                        <fieldset class="form-group">
                            <label class="form-label semibold" for="exampleCluster">Stock To <span style="color:red">*</span></label>
                            <div class='input-group date'>
                            <select class="form-control status select2" name="to" id="to" required>
                                <option value="">Select To</option>
                                <option value="Hub">Hub</option>
                                <option value="Branch">Branch</option>
                            </select>
                            </div>
                            <p id="toError"></p>
                        </fieldset>
                        </div>
                        <div class="col-md-3">
                            <fieldset class="form-group">
                                <label class="form-label semibold" for="exampleInput">Start Date <span style="color:red">*</span></label>
                                <div class='input-group date'>
                                    <input  type="date" id="start_date" class="form-control" name="start_date" required> 
                                    <span class="input-group-addon"> 
                                        <i class="font-icon font-icon-calend"></i>
                                    </span>
                                </div>
                                <p id="start_dateError"></p>
                            </fieldset>
                        </div>
    
                        <div class="col-md-3">
                            <fieldset class="form-group">
                                <label class="form-label semibold" for="exampleInput">End Date <span style="color:red">*</span></label>
                                <div class='input-group date'>
                                    <input  type="date" id="end_date" class="form-control" name="end_date" required>
                                    <span class="input-group-addon">
                                        <i class="font-icon font-icon-calend"></i>
                                    </span>
                                </div>
                                <p id="end_dateError"></p>
                            </fieldset>
                        </div>
                        <div class="col-md-3">
                        <fieldset class="form-group">
                            <label class="form-label semibold" for="exampleCluster">Item <span style="color:red">*</span></label>
                            <div class='input-group date'>
                            <select class="form-control item select2" name="item" id="item" required>
                                <option value="">Select Item</option>
                            </select>
                            </div>
                            <p id="itemError"></p>
                        </fieldset>
                        </div>
                      <div class="col-md-1">
                      <fieldset class="form-group">
                      <div class="input-group-btn" style = "margin-top: 7px "> 
                      <button type="button" name="filter_transfer" id="exportfilterbtn" class="btn btn-inline btn-success p-x-3 p-y mt-4" >Export
                          </button>
                          </div>
                          </fieldset>
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
        for (i = 0; i < huboptions.length; i++) {
          $(`#source`).append(
            $("<option></option>")
              .attr("value", huboptions[i].id)
              .text(huboptions[i].text)
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
      $(`#source`).select2({
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
      $('#source').on('change', function(e){
        var value = e.target.id
        if ($(`#${value} option:selected`).val() != ''){
          $("#sourceError").html("")
        }
      })
      $('#item').on('change', function(e){
        var value = e.target.id
        if ($(`#${value} option:selected`).val() != ''){
          $("#itemError").html("")
        }
      })
      $('#status').on('change', function(e){
        var value = e.target.id
        if ($(`#${value} option:selected`).val() != ''){
          $("#statusError").html("")
        }
      })
      $('#to').on('change', function(e){
        var value = e.target.id
        if ($(`#${value} option:selected`).val() != ''){
          $("#toError").html("")
        }
      })
      $('#start_date').on('change', function(e){
        var value = e.target.id
        if ($(`#${value} option:selected`).val() != ''){
          $("#start_dateError").html("")
        }
      })
      $('#end_date').on('change', function(e){
        var value = e.target.id
        if ($(`#${value} option:selected`).val() != ''){
          $("#end_dateError").html("")
        }
      })
      $('#exportfilterbtn').on('click', function(event){
        console.log('hello')
        
        var fromdate = $('#start_date').val()
        var todate = $('#end_date').val()
        var item = $('#item option:selected').val()
        var stockstatus = $('#status option:selected').val()
        var source = $('#source option:selected').val()
        var to = $('#to option:selected').val()
        if (source.length == ''){
          $("#sourceError").html("This field is required...")
        }
        if (fromdate.length == ''){
          $("#start_dateError").html("This field is required...")
        }
        if (todate.length == ''){
          $("#end_dateError").html("This field is required...")
        }
        if (stockstatus.length == ''){
          $("#statusError").html("This field is required...")
        }
        if (to.length == ''){
          $("#toError").html("This field is required...")
        }
        if (item.length == ''){
          $("#itemError").html("This field is required...")
        }
        console.log('fromdate', fromdate, item)
        if (source.length != '' && fromdate.length != '' && todate.length != '' && stockstatus.length != '' && to.length != '' && item.length != ''){
          var arraydetails = [];
        var dictvalue = {
          fromdate: fromdate,
          todate: todate,
          item: item,
          stockstatus: stockstatus,
          source: source,
          to: to
        };
        var data = `{"fromdate":"${fromdate}","todate":"${todate}","item":"${item}", "stockstatus":"${stockstatus}", "source":"${source}", "to":"${to}"}`;
        console.log("dictvalue", dictvalue);
        arraydetails.push(dictvalue);
        let request = new XMLHttpRequest();
        request.open('POST', '/site/transfer/export', true);
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
        }
        
    
    
    
      })
})
  if (
    window.location.href.includes("add") ||
    window.location.href.includes("change")
  ) {
    $(".card-body")
      .find(".field-selectfrom")
      .parent()
      .css({ display: "grid", "grid-template-columns": "682px 682px" });
    $(".card-body")
      .find(".field-item")
      .parent()
      .css({ display: "grid", "grid-template-columns": "682px 682px" });
  }

  var value = $("#id_SelectTo").val();
  if (value == "") {
    $(".field-hubdestination").css("display", "none");
    $("#id_branchdestination").prop("disabled", true);
  }
  if (value == "Hub") {
    $(".field-branchdestination").css("display", "none");
    $(".field-hubdestination").css("display", "flex");
  }
  if (value == "Branch") {
    $("#id_branchdestination").prop("disabled", false);
    $(".field-hubdestination").css("display", "none");
    $(".field-branchdestination").css("display", "flex");
  }
  console.log("dest", value);
  $("#id_SelectTo").on("change", function () {
    console.log("this", $(this));
    var selectVal = $(this).find("option:selected").val();
    console.log("select val:", selectVal);
    if (selectVal == "Hub") {
      // $('#id_branchdestination option').prop('selected', function() {
      //     return this.defaultSelected;
      // });
      $("#id_branchdestination").val("").trigger("change");
      console.log("VAL HUB ", selectVal);
      $(".field-branchdestination").css("display", "none");
      $(".field-hubdestination").css("display", "flex");
    }
    if (selectVal == "Branch") {
      // $('#id_hubdestination option').prop('selected', function() {
      //     return this.defaultSelected;
      // });
      console.log("VAL Branch ", selectVal);
      $("#id_hubdestination").val("").trigger("change");
      $("#id_branchdestination").prop("disabled", false);
      $(".field-hubdestination").css("display", "none");
      $(".field-branchdestination").css("display", "flex");
    }
    if (selectVal == "") {
      $("#id_hubdestination").prop("selectedIndex", 0);
      $("#id_branchdestination").prop("selectedIndex", 0);
      $(".field-branchdestination").css("display", "flex");
      $(".field-hubdestination").css("display", "none");
      $("#id_branchdestination").prop("disabled", true);
    }
  });
  arritem = {};
  itemlist = [];

  console.log('trigger', $("#id_source").find(':selected').val())
  
  
  $("#id_source").on("change", function (e) {
    console.log("source", e.target.id);
    console.log("selectvalue:", $("select[id^=id_transferid-]").attr("id"));
    $("select[id^=id_transferid-]").find("option").remove().end();
    sourceval = $("#id_source").val();
    console.log('value', sourceval)
    $.ajax({
      type: "GET",
      url: `/site/transferitem/${sourceval}`,
      success: function (data) {
        if(data.data.length == 0){
          alert('No Item Found')
          $("input[id^=id_transferid-][id$=-transferablestock]").val('')
        }
        else{
          console.log("AJAX GOT ", data);
        itemlist = [];
        for (itemval = 0; itemval < data.data.length; itemval++) {
          console.log("data", itemval);
          itemlist.push(data.data[itemval]);

          // arritem.value = data.data[itemval]
        }
        arritem[`${sourceval}`] = itemlist;
        console.log("item", arritem);
        $(`select[id^=id_transferid-][id$=-item]`).append('<option >Select Items</option>')
        for (items = 0; items < arritem[`${sourceval}`].length; items++) {
          $(`select[id^=id_transferid-][id$=-item]`).append(
            $("<option></option>")
              .attr(
                "id",
                "" +
                  arritem[`${sourceval}`][items].totalstock +
                  "=" +
                  arritem[`${sourceval}`][items].itemname
              )
              .attr("value", arritem[`${sourceval}`][items].itemid)
              .text(arritem[`${sourceval}`][items].itemname)
          );
          if (window.location.href.indexOf('?') > 0){
            var itemvalue = window.location.href.split("&")[2]
            itemvalue = itemvalue.split('=')[1]
            if (itemvalue == arritem[`${sourceval}`][items].itemid){
              console.log('itmvl',$('.field-SelectTo').children().eq(1).children().children().eq(1).children().children())
              $('#id_transferid-0-item').val(itemvalue)
              $("input[id^=id_transferid-][id$=-transferablestock]").val(arritem[`${sourceval}`][items].totalstock)
              $("#id_transferid-0-item").css({"pointer-events": "none","background-color": "lightgray"})
              
            }
            else{
              alert('Item has no Stock...!!!')
            }
            
          }
          // $("input[id^=id_transferid-][id$=-transferablestock]").val(arritem[`${sourceval}`][items].totalstock)
        }
        

        console.log("stock", arritem[`${sourceval}`][0].totalstock);
        $("input[id^=id_transferid-][id$=-transferablestock]").css({"pointer-events": "none","background-color": "lightgray"})
        }
        
      },
      failure: function (data) {
        console.log("Got an error dude");
      },
    });
  });
  
  // arrayitem ={}
  if (window.location.href.includes("change")) {
    $('.field-transferdate').css({ display: "none" })
    $("select[id^=id_transferid-]").css({"pointer-events": "none","background-color": "lightgray"})
    $(".field-transferablestock").css({ display: "none" });
     
  }
 
     $(`select[id^=id_transferid-][id$=-item]`).on('change',function (e) {
          console.log("CHANGE");
          console.log('e val', e.target.id)
          var selectitemid = $(this).attr('id')
          console.log('slectitemid:', selectitemid)
          selectitemid = selectitemid.split('-')[1]
          console.log('event val', selectitemid)
          var itemoptionid = $(this).children(":selected").attr('id')
          console.log('itemoption', itemoptionid)
          var items = $(this).children(":selected").attr('id')
          console.log('items get', items )
          itemoptionid = itemoptionid.split('=')[0]
          console.log('id split', itemoptionid,' id split2 ',  items)
          $(`#id_transferid-${selectitemid}-transferablestock`).val(itemoptionid);
      });

  $(document).on("DOMNodeInserted", ".module ", function (e) {
    // console.log('hit');
    if ($(e.target).attr("id")?.includes("transferid")) {
      console.log("hit");
      $(`select[id^=id_transferid-][id$=-item]`).change(function () {
        console.log("CHANGE");

        // var optionSelected = $(this).find("option:selected");
        // var valueSelected = optionSelected.val();
        // var textSelected = optionSelected.text();
        // console.log("CHANGED ", valueSelected, textSelected);

          console.log('e val', e.target.id)
          var selectitemid = $(this).attr('id')
          console.log('slectitemid:', selectitemid)
          selectitemid = selectitemid.split('-')[1]
          console.log('event val', selectitemid)
          var itemoptionid = $(this).children(":selected").attr('id')
          var items = $(this).children(":selected").attr('id')
          itemoptionid = itemoptionid.split('=')[0]
          console.log('id split', itemoptionid,  items)
          $(`#id_transferid-${selectitemid}-transferablestock`).val(itemoptionid);
      });
    }
  });

  $(document).on("click", ".get-item", function (e) {
    id = e.target.id
    id = id.split("-")[1]
    $('.bd-example-modal-xl').remove();
    $(this).after(`<div class="modal fade bd-example-modal-xl" id="modalCategory-${id}" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-xl">\
        <div class="modal-content">\
            <div class="modal-header">\
                <form id="modal-form2-${id}" class="form-horizontal" enctype="multipart/form-data"\  method="POST">\
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">\
                        <span aria-hidden="true">  ×</span>\
                </button>\
    <div id="header-container" style="display: flex;flex-direction: row;align-items: center;justify-content: center; ">\
                    <h5 style="font-weight: 900; ">Receive Transfer </h5>\
                    </div>\
         <div class="card card-info">\
           <div class="modal-body" style= "width: 1105px;">\
                        <div class="card-body"  style="display: flex;width: 100%;">\
                            <div class="form-group row" style="width: 45%;">\
                                    <input type="hidden" class="form-control" name="id" id="id-${id}">\
                                    <label for="file" class="col-md-4 col-form-label" style="font-size: 18px!important;">Select files: <span style="color:red">*</span></label>\
                                    <div class="col-sm-8">\
                                        <input type="file" id="file-${id}" name="file" class="form-control modal-file" style="width: 100%;" required><br><br>\
                                    </div class="col-sm-8">\
                                </div>\
                                <div class="form-group row" style="width: 45%;">\
                                    <label  class="col-md-4 col-form-label" style="font-size: 18px!important;">Received Date: <span style="color:red">*</span></label>\
                                    <div class="col-sm-8">\
                                        <input type="date" class="form-control modal-date" name="receivedate" id="receivedate-${id}" style="max-width: 302px;" required>\
                                    </div>\
                                </div>\
                           </div>\
                           <div class="card-body"  style="display: flex;width: 100%;">\
                           <div class="form-group row" style="width: 45%;">\
                                    <label  class="col-md-4 col-form-label" style="font-size: 18px!important;">Remarks: <span style="color:red">*</span></label>\
                                    <div class="col-sm-8">\
                                        <input type="text" class="form-control modal-remarks" name="remarks" id="remarks-${id}" placeholder="Remarks" style="max-width: 302px;" required>\
                                    </div>\
                                </div>\
                                </div>\
                    <div class="card-footer">\
                        <button type="submit"  class="submitbutton btn btn-info float-right" id="savebutton">Save</button>\
                    </div>\
                  </div>\
        </div> </div>\
    </form>\
            </div>\
        </div>\
    </div></div>\
`)
jQuery.noConflict();
// $(".bd-example-modal-xl").modal('show')
$(`#` + e.target.id).click()
var button = e.target.id;
button = button.split("-")[1];
$("#id").val(button);
// $("#modal-form2").submit(function (e) {
//   e.preventDefault();
//   var formData = new FormData(this);
//   console.log("FORM DATA ", formData);
//   for (var pair of formData.entries()) {
//     console.log(pair[0] + ", " + pair[1]);
//   }
//   $.ajax({
//     type: "POST",
//     url: `/site/stockreceivefileupload`,
//     headers: {
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//     data:formData,
//     enctype: 'multipart/form-data',
//     cache       : false,
//     contentType : false,
//     processData: false,
//     // {
//     //   'data': JSON.stringify(arraydetails),
//     // },
//     success: function (data) {
//       console.log("suceesss", data);
//       location.href = "/mainApp/transfer"
//     },
//     failure: function (data) {
//       console.log("Got an error dude");
//     },
//   });
// });
});

$(function () {
  var dataimg = new FormData(); 
  $(document).on('click', function(event) {

    // const remarksInput = document.getElementById("remarks-61");

    // remarksInput.addEventListener("change", (event) => {
    //   console.log("ADDED EVNT LSTNR ", event)
    // });
  //   HTMLInputElementObject.addEventListener('input', function (evt) {
  //     console.log(" Input " , this.value);
  // });
    console.log("CLICKED ", event.target.id)
    let val = $("#"+ event.target.id).val()
    console.log("VAL ", val)
    $('.modal-remarks').on('input',function(e){
      console.log("HMMM", $(this).val())
      remarks = $(this).val()
      console.log('re', remarks)
      dataimg.set('remarks', remarks);
      // remarks = $(this).val()
  });
  
  $('.modal-date').on('input',function(e){
    console.log("HMMM", $(this).val())
    date = $(this).val()
    console.log('last', date)
    dataimg.set('receivedate', date);
});
$('.modal-file').on('change',function(e){
  
  var d = $(this).prop('files')[0]
  dataimg.set('file', d);
  console.log("HMMM", d)
  
});



   })

$(document).on('click', '#savebutton', function(event) {
  
    event.preventDefault();
    console.log("HERE WE GO : ", id)


    
    dataimg.set('id', id);
    

$.ajax({
  type: "POST",
  url: `/site/stockreceivefileupload`,
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  // data:formData,
  enctype: 'multipart/form-data',
  cache       : false,
  contentType : false,
  processData: false,
  data: dataimg ,
  success: function (data) {
    console.log("suceesss", data);
    location.href = "/mainApp/transfer/"
  },
  failure: function (data) {
    console.log("Got an error dude");
  },
});
  // }

})
});


    
})






