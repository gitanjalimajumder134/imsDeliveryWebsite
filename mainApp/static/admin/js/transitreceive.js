function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
  }
  function removeModal (id) {
    $(`#modalCategory-${id}`).remove()
    $('.bd-example-modal-xl').remove()
  }
  var itemOptions = [];
$(document).ready(function () {
  console.log('token', getCookie("csrftoken"))
 
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
                      <div class="col-md-2">
                          <fieldset class="form-group">
                              <label class="form-label semibold" for="exampleCluster">Stock Status <span style="color:red">*</span></label>
                              <div class='input-group date'>
                              <select class="form-control status select2" name="status" id="status">
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
                                  <label class="form-label semibold" for="exampleInput">Start Date <span style="color:red">*</span></label>
                                  <div class='input-group date'>
                                      <input  type="date" id="start_date" class="form-control" name="start_date"> 
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
                                      <input  type="date" id="end_date" class="form-control" name="end_date">
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
                              <select class="form-control item select2" name="item" id="item">
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
          var stockstatus = $('#status').val()
          if (fromdate.length == ''){
            $("#start_dateError").html("This field is required...")
          }
          if (todate.length == ''){
            $("#end_dateError").html("This field is required...")
          }
          if (stockstatus.length == ''){
            $("#statusError").html("This field is required...")
          }
          if (item.length == ''){
            $("#itemError").html("This field is required...")
          }
          if (fromdate.length != '' && todate.length != '' && stockstatus.length != '' && item.length != ''){
            var arraydetails = [];
          var dictvalue = {
            fromdate: fromdate,
            todate: todate,
            item: item,
            stockstatus: stockstatus
          };
          var data = `{"fromdate":"${fromdate}","todate":"${todate}","item":"${item}", "stockstatus":"${stockstatus}"}`;
          console.log("dictvalue", dictvalue);
          arraydetails.push(dictvalue);
          let request = new XMLHttpRequest();
          request.open('POST', '/site/transit/export', true);
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
    


  $(document).on("click", ".receivestock", function (e) { 
       const recv = $('#'+ e.target.id).parent().siblings('.field-quantity').text()
       id = e.target.id
       id = id.split("-")[1]
       console.log('hi target', e.target.id)
        console.log('hi', recv, id)
        $('.bd-example-modal-xl').remove();
        $('body').append(`<div class="modal fade bd-example-modal-xl" id="modalCategory-${id}" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-xl">\
        <div class="modal-content">\
            <div class="modal-header">\
                <form id="modal-data-${id}" data-id="${id}" method="POST">\
                <button type="button" class="close" data-dismiss="modal" aria-label="Close" onClick="removeModal(${id})" >\
                        <span aria-hidden="true">  ×</span>\
                </button>\
                <div id="header-container" style="display: flex;flex-direction: row;align-items: center;justify-content: center; ">\
                    <h5 style="font-weight: 900; ">Receive Transit </h5>\
                    </div>\
            <div class="card card-info">\
                <div class="modal-body" style= "width: 1105px;">\
                        <div class="card-body"  style="display: flex;width: 100%;">\
                                <div class="form-group row" style="width: 45%;">\
                                <input type="hidden" class="form-control" name="id" id="id-${id}">\
                                <label for="file" class="col-md-4 col-form-label" style="font-size: 18px!important;">Select files: <span style="color:red">*</span></label>\
                                <div class="col-sm-8">\
                                    <input type="file" id="file-${id}" class="form-control modal-file" name="file" style="width: 100%;" required><br><br>\
                                </div>\
                                </div>\
                                <div class="form-group row" style="width: 45%;">\
                                <label  class="col-sm-4 col-form-label" style="font-size: 18px!important;">Received Date: <span style="color:red">*</span></label>\
                                    <div class="col-sm-8">\
                                        <input type="date" class="form-control modal-date" name="receivedate" id="receivedate-${id}" placeholder="Quantity" style="max-width: 302px;">\
                                    </div>\
                                </div>\
                           </div>\
                           <div class="card-body"  style="display: flex;width: 100%;">\
                           <div class="form-group row" style="width: 45%;">\
                                    <label  class="col-md-4 col-form-label" style="font-size: 18px!important;">Received Stock: <span style="color:red">*</span></label>\
                                    <div class="col-sm-8">\
                                        <input type="text" class="form-control modal-receivedstock"  name="receivedstock" id="receivedstock-${id}" placeholder="" style="max-width: 302px;" required />\
                                    </div>\
                                </div>\
                           <div class="form-group row" style="width: 45%;">\
                                    <label  class="col-md-4 col-form-label" style="font-size: 18px!important;">Remarks: <span style="color:red">*</span></label>\
                                    <div class="col-sm-8">\
                                        <input type="text" class="form-control modal-remarks" name="remarks-${id}" id="remarks-${id}"  placeholder="Remarks" style="max-width: 302px;" required />\
                                    </div>\
                                </div>\
                                </div>\
                        <div class="card-footer">\
                        <button class="submitbutton btn btn-info float-right" id="savebutton">Save</button>\
                        </div>\
                    </div> </div> </div>\
        </form>\
            </div>\
        </div>\
    </div></div>\
`)
     jQuery.noConflict();
  //    $('#modalCategory-' + id).on('shown', function(){
  //     alert("I want this to appear after the modal has opened!");
  // });
      $(`#receivedstock-${id}`).on('focusin', function(){
        // console.log("Saving value " + $(this).val());
        $(this).data('val', recv);
    });

    $('#modalCategory-' + id).find('#receivedstock-' + id).val(recv);
    $(`#` + e.target.id).click()
//   $(document).on('shown.bs.modal','#md-load-test-modal',function(e){
//     console.log('Modal opened', e.target.id);
// });
    var button = e.target.id;
    button = button.split("-")[1];
    $("#id").val(button);

  });

//   $("#savebutton").on('click' , function (e) {
//     e.preventDefault();
//     var formData = new FormData(this);
//     console.log("FORM INIT ");
//     console.log("FORM DATA ", formData);
// // for (var pair of formData.entries()) {
// //   console.log(pair[0] + ", " + pair[1]);
// // }
// // console.log("CSRF TOK :" , getCookie("csrftoken"))

// // $.ajax({
// //   type: "POST",
// //   url: `/site/TransitReceive`,
// //   headers: {
// //     'X-CSRFToken': csrftoken,
// //   },
// //   data:formData,
// //   enctype: 'multipart/form-data',
// //   cache       : false,
// //   contentType : false,
// //   processData: false,
// //   // {
// //   //   'data': JSON.stringify(arraydetails),
// //   // },
// //   success: function (data) {
// //     console.log("suceesss", data);
// //     location.href = "/mainApp/transit/"
// //   },
// //   failure: function (data) {
// //     console.log("Got an error dude");
// //   },
// // });
//   })

function handleInput(e) {


}

$(function () {
  var dataimg = new FormData(); 
  var receivedstock = ''
  $(document).on('click', function(event) {

    // const remarksInput = document.getElementById("remarks-61");

  //   remarksInput.addEventListener("change", (event) => {
  //     console.log("ADDED EVNT LSTNR ", event)
  //   });
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
  $('.modal-receivedstock').on('input',function(e){
    console.log("HMMM", $(this).val())
    receivedstock = $(this).val()
    
});
  $('.modal-date').on('input',function(e){
    console.log("HMMM", $(this).val())
    date = $(this).val()
    console.log('last', date)
    dataimg.set('date', date);
});
$('.modal-file').on('change',function(e){
  
  var d = $(this).prop('files')[0]
  console.log("FILE ", d)
  dataimg.set('file', d);
  console.log("HMMM", d)
  // file = $(this).val()
  // file = file.split('\\')[2]
  // console.log('files', file)
});



//   $('.modal-remarks').bind('input', function() { 
//     console.log("HMMM bind", $(this).val())
//  // get the current value of the input field.
// });

   })

$(document).on('click', '#savebutton', function(event) {
  
  // console.log("ID ", event.target.id);
  var arraydetails = [];
  // if(event.target.id == "savebutton") {
    event.preventDefault();
    console.log("HERE WE GO : ", id)


    
    dataimg.set('id', id);
    // var file = $(`#file-`+id).prop('files');
    // console.log("File ", file)
    var stock = $('#receivedstock-'+ id).val();
    if(receivedstock != ""){
      if (receivedstock == stock){
        receivedstock = stock
        
      }
      else{
        
        receivedstock = receivedstock
      }
    }
    else{
      receivedstock = stock
    }
    dataimg.set('receivedstock', receivedstock);
    console.log("stock ", receivedstock)
    // var date = $(`#receivedate-`+id).val();
    // console.log("stock ", date)
    // var remarks = $(`#remarks-${id}`).val();
    // console.log("remarks ", remarks)

    // var formData = [
    //   {'id' : '61'}, {'receivedstock' : receivedstock} , {'remarks' : remarks}, {'receivedDate' : date}, {'file': file}
    // ]

    // var formData = {
    //   id: id,
    //   file: file,
    //   receivedstock : stock,
    //   receivedate: date,
    //   remarks : remarks
    // }
    // console.log(formData)
    // arraydetails.push(formData);
    // console.log(arraydetails)
    // var formData = new FormData(this);
  //   var formData;
  
    // let formData = $('#'+`modal-data-${id}`).serializeArray();
    // console.log("FORM INIT ", formData);
    
  //   $.each(inputs, function (i, input) {
  //     formData[input.name] = input.value;
  // });
  // let form = $('#modal-data-' + id)[0];
  // let formData = new FormData(form);
  //   console.log("FORM DATA ", formData);
    
// for (var pair of formData.entries()) {
//   console.log(pair[0] + ", " + pair[1]);
// }
console.log("CSRF TOK :" ,  dataimg)

$.ajax({
  type: "POST",
  url: `/site/TransitReceive`,
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  enctype: 'multipart/form-data',
  cache       : false,
  contentType : false,
  processData: false,
  data: dataimg ,
  success: function (data) {
    console.log("suceesss", data);
    location.href = "/mainApp/transit/"
  },
  failure: function (data) {
    console.log("Got an error dude");
  },
});
  

})
});

// $('#'+`modal-data-${id}`).submit(function() {
//   // Get all the forms elements and their values in one step
//   var values = $(this).serialize();
//   console.log("SUBMITTING ", values)
// });
    
})
// $(document).on('click', "#submittransitButton", function() {
//   //  $("#submittransitForm").submit();
//   console.log('trigger', $("#itemname").find(':selected').val(), $("#start_date").val(), $("#end_date").val())
//   var itemname = $("#itemname").find(':selected').val()
//   var startDate = $("#start_date").val()
//   var endDate = $("#end_date").val()
//    $.ajax({
//     type: "GET",
//     url: `/mainApp/transit/${itemname}/${startDate}/${endDate}`,
//     success: function (data) {
      
//       console.log("AJAX GOT ", 'aaa');
      
      
//     },
//     failure: function (data) {
//       console.log("Got an error dude");
//     },
//   });
// });


// document.addEventListener("DOMContentLoaded", function(event) {
//   document.getElementById("submittransitButton").onclick = submitForm;
// });
// function submitForm() {
//   alert(123);
// }  
  