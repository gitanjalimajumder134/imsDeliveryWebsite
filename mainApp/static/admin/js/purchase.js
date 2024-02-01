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

var hubOptions = [];
$(document).ready(function () {
  if ((window.location.href.includes("add") ||
    window.location.href.includes("change"))) {
      $(`#id_state`).select2({
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
  $('#id_status').css({"pointer-events": "none","background-color": "lightgray"})
  $(".get-item").click(function () {
    /// Initialise Empty Modal ///
    
    var purchase = window.location.href.split("/")
    
    purchase = purchase[purchase.length-3]
    console.log('window', purchase)
    $("select[id^=hub-dropdown-]").find("option").remove().end();
    $("input[id^=qty-]").val("");
    $('.repeaterbody').children('.card-body').remove();
    $('.successMessage').css('display', 'none');
    /// Initialise Empty Modal ///
    ///Fetch Data to populate Modal///
    var allids = $(this)
      .closest(".field-button")
      .siblings(".field-items")
      .children()
      .children()
      .find(":selected")
      .val();
    console.log("ALL IDS ", allids);
    var supplier = $("#id_supplier_name").val();
    var state =  $(`#id_state`).val()

    console.log("SUPPLIER ",  supplier, "allids ",  allids, "state", state);
    // var str = "You Have Entered "
    //     + "Name: " + allids
    //     + " and Marks: " + supplier;
    // $("#modal_body").html(str);

    // "{% url 'site:modal' %}",
    $.ajax({
      type: "GET",
      url: `/site/hub/allocate/${supplier}/${allids}/${purchase}/${state}`,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      success: function (data) {
        console.log("AJAX GOIT ", data);
        $(".supplierid")
          .attr("value", data.allocate[0].supplierid)
          .text(data.allocate[0].supplier);
        $(".itemid")
          .attr("value", data.allocate[0].itemid)
          .text(data.allocate[0].items);
        hubOptions = []
        
        for (allocate = 0; allocate < data.allocate.length; allocate++) {
          console.log("length", data.allocate[allocate].supplier);
          var modalqty = $("#modaltotqty").text(data.allocate[allocate].quantity);
          $("#modalremainingqty").text(data.allocate[allocate].remainingstock);
          $(".hub-dropdown").append(
            $("<option></option>")
              .attr("value", data.allocate[allocate].hubid)
              .text(data.allocate[allocate].hubname)
          );
          console.log(
            "HUB OPTIONS ",
            data.allocate[allocate].hubid,
            " TEXT ",
            data.allocate[allocate].hubname
          );
          hubOptions.push({
            id: data.allocate[allocate].hubid,
            text: data.allocate[allocate].hubname,
          });
        }
        //<option>${data.hublist[i].hubname}<option>
        for (i = 0; i < data.hublist.length; i++) {
          console.log("hublistqty", data.hublist[i].qty);
          prefill_id = i;
          console.log("When ADDing prefill_id", prefill_id);
          $(`.repeaterbody`)
            .append(`<div class="card-body" id = "repeater-${prefill_id}" style="display: flex;width: 100%;">\
                <div class="form-group row" style="width: 45%;">\
                    <label  for="hubname" class="col-sm-3 col-form-label" style="font-size: 18px!important;">Hub Name</label>\
                    <div class="col-sm-8">\
                    <select id="hub-dropdown-${prefill_id}" name= "hub" class="hub-dropdown form-control select2" style="width: 100%;"><option>Select Hub</option></select>\
                </div class="col-sm-8">\
                </div>\
                <div class="form-group row" style="width: 45%;">\
                    <label  class="col-sm-3 col-form-label" style="font-size: 18px!important;">Quantity</label>\
                    <div class="col-sm-8">\
                      <input type="number" class="form-control" name="qty" id="qty-${prefill_id}" placeholder="Quantity" style="max-width: 302px;" value="${data.hublist[i].qty}"> \
                      </div></div><div class="form-group row" style="width: 10%;"><i class="fa fa-trash" id="btn-delete-${prefill_id}" style="float: right;"></i></div></div>\
                `);
          
          for (var hubs = 0; hubs < data.allocate.length; hubs++) {
            console.log("hubs and se ", data.allocate[hubs].hubname , "selected ",  data.hublist[i].hubname);
            $(`#hub-dropdown-${prefill_id}`).append(
              $("<option></option>")
                .attr("value", data.allocate[hubs].hubid)
                .text(data.allocate[hubs].hubname)
                .prop(
                  "selected",
                  data.allocate[hubs].hubname == data.hublist[i].hubname
                    ? true
                    : false
                )
            );
          }
          // prefill_id += 1;
        }
      },
      failure: function (data) {
        console.log("Got an error dude");
      },
    });
    ///Fetch Data to populate Modal///
  });
});

$(document).ready(function () {
  $(function () {
    console.log("LOADED AND REMOVED");
    //$('a:contains("Add another Quantity")').css('display', "none")
    $(".add-row").css("display", "none !important");
    if (!window.location.href.includes("add")) {
      console.log("in change option");
      $("div.add-row").css({ display: "none" });
      // console.log('in add option',add)
    }
    if (window.location.href.includes("add")) {
      console.log("in add option");
      $(".form-group.row.form-row.field-button").css("display", "none");
    }
  });
  if (window.location.href.includes("change")) {
    console.log("status", $("#id_status").val());
    $("#id_status").val("Confirmed");
  }
});

$(function () {
  let c = 0;
  $(document).on("click", ".btn-add", function (e) {
    
    $(".repeaterbody")
      .children(".card-body")
      .each(function () {
        c = Math.max(Number($(this).attr("id").split("-")[1]) + 1, c);
        console.log("Max C ", c);
      });
    // c += 1
    
    e.preventDefault();
    console.log("When ADDing c", c);
    $(
      `.repeaterbody`
    ).append(`<div class="card-body" id = "repeater-${c}" style="display: flex;width: 100%;">\
      <div class="form-group row" style="width: 45%;">\
          <label  for="hubname" class="col-sm-3 col-form-label" style="font-size: 18px!important;">Hub Name</label>\
          <div class="col-sm-8">\
          <select id="hub-dropdown-${c}" name= "hub" class="hub-dropdown form-control select2" style="width: 100%;"><option>Select Hub</option></select>\
      </div class="col-sm-8">\
      </div>\
      <div class="form-group row" style="width: 45%;">\
          <label  class="col-sm-3 col-form-label" style="font-size: 18px!important;">Quantity</label>\
          <div class="col-sm-8">\
            <input type="number" class="form-control" name="qty" id="qty-${c}" placeholder="Quantity" style="max-width: 302px;">\
            </div></div><div class="form-group row" style="width: 10%;"><i class="fa fa-trash" id="btn-delete-${c}" style="float: right;"></i></div></div>\
      `);
    // $(".hub-dropdown")
    //     .find("option")
    //     .remove()
    //     .end()
    //     .append('<option value="">Select Hub</option>')
    //     .val("");

    for (i = 0; i < hubOptions.length; i++) {
      $(`#hub-dropdown-${c}`).append(
        $("<option></option>")
          .attr("value", hubOptions[i].id)
          .text(hubOptions[i].text)
      );
    }
  
    $(`#hub-dropdown-${c}`).select2({
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
  c += 1;
  });
  var remainingqty = 0;

  $(document).ajaxComplete(function () {
    var latestqty = $("#modalremainingqty").text();
    console.log("latest", latestqty);
    remainingqty = latestqty;
    if (Number(remainingqty) > 0) {
      $(`.submitbutton`).addClass("disabled");
      $(".btn-add").css("display", "block");
    }
    if (Number(remainingqty) == 0) {
      $(`.submitbutton`).removeClass("disabled");
      $(".btn-add").css("display", "none");
    }
  });

  var splitsvalue = "";
  $(document).on("click", function (e) {
    console.log("console", e.target.id);
    splitsvalue = e.target.id;
    if (splitsvalue.includes("btn-delete")) {
      splitsvalue = splitsvalue.split("-")[2];
      console.log("split", splitsvalue);
      $(`#repeater-${splitsvalue}`).remove();

      $(".repeaterbody")
        .children(".card-body")
        .each(function () {
          console.log("LATES ADD ", $(this).attr("id"));
          c = Number($(this).attr("id").split("-")[1]);
        });
      // c = c - 1;
      console.log("after remove c", c);
    }
    
    var sumqty = 0;
    var newgqty = 0;
    $(".repeaterbody")
      .children(".card-body")
      .each(function () {
        console.log("LATES new ADD ", $(this).attr("id"));
        q = Number($(this).attr("id").split("-")[1]);
        var a = $(`#qty-${q}`).val();
        sumqty = sumqty + Number(a);
        console.log("val", sumqty, "rema ", remainingqty);
        var quantityvalue = 0;
        if (Number(remainingqty) !== 0) {
          newgqty = Number(remainingqty) - sumqty;
          console.log("REMAIN ", newgqty);
        } else {
          quantityvalue = $(`#modaltotqty`).text();
          newgqty = Number(quantityvalue) - sumqty;
          console.log("NO REMAIN ", quantityvalue);
        }

        var quantity = $("#modalremainingqty").text(newgqty);
        console.log("quantity", remainingqty, "newgqty", newgqty);

        if (Number(newgqty) > 0) {
          $(`.submitbutton`).addClass("disabled");
          $(".btn-add").css("display", "block");
        }
        if (Number(newgqty) == 0) {
          console.log("remain value", Number(newgqty));
          $(`.submitbutton`).removeClass("disabled");
          $(".btn-add").css("display", "none");
        }
        if (Number(newgqty) < 0) {
          $("#modalremainingqty").text(0);
          $(".col-sm-6.text-right").css("color", "red");
          $(`.submitbutton`).addClass("disabled");
        }
      });
  });
  $("#allocationbutton").on("click", function (e) {
    e.preventDefault();
    var arraydetails = [];
    $(".repeaterbody")
      .children(".card-body")
      .each(function () {
        arr = Number($(this).attr("id").split("-")[1]);
        var purchaseorderid =window.location.href.split("/")
        purchaseorderid = purchaseorderid[purchaseorderid.length-3]
        var dictvalue = {
          qty: $(`#qty-${arr}`).val(),
          hub: $(`#hub-dropdown-${arr}`).val(),
          items: $(`.itemid`).val(),
          supplier: $(`.supplierid`).val(),
          purchaseorder: purchaseorderid
        };
        console.log("dictvalue", dictvalue);
        arraydetails.push(dictvalue);
        console.log("array", arraydetails);
      });

    $.ajax({
      type: "POST",
      url: `/site/hubpost/allocate`,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      data: { data: JSON.stringify(arraydetails) },
      // {
      //   'data': JSON.stringify(arraydetails),
      // },
      success: function (data) {
        console.log("suceesss", data);
        $(".successMessage").css("display", "block");
      },
      failure: function (data) {
        console.log("Got an error dude");
      },
    });
  });
});
