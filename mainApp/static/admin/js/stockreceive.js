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

$(document).ready(function () {
  $(`.get-item.btn.btn-success`).on("click", function (e) {
    var button = e.target.id;
    button = button.split("-")[1];
    console.log("button", button);
    $("#id").val(button);
  });
  $("#modal-form2").submit(function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    console.log("FORM DATA ", formData);
    for (var pair of formData.entries()) {
      console.log(pair[0] + ", " + pair[1]);
    }
    $.ajax({
      type: "POST",
      url: `/site/stockreceivefileupload`,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      data:formData,
      enctype: 'multipart/form-data',
      cache       : false,
      contentType : false,
      processData: false,
      // {
      //   'data': JSON.stringify(arraydetails),
      // },
      success: function (data) {
        console.log("suceesss", data);
        location.href = "/site/stockreceive"
      },
      failure: function (data) {
        console.log("Got an error dude");
      },
    });
  });
});
