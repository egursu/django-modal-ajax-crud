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

$.ajaxSetup({
  headers: { "X-CSRFToken": getCookie("csrftoken") },
});

$(document).ready(function () {
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("href"),
      type: "get",
      dataType: "json",
      beforeSend: function () {
        $("#modal").modal("show");
      },
      success: function (data) {
        $("#modal .modal-content").html(data.html_form);
        // $("#modal .modal-content").text(data.html_form);
      },
    });
    return false;
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: "json",
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal").modal("hide");
          if (data.redirect) {
            top.location = data.redirect;
          } else {
            $("#table tbody").html(data.html_list);
          }
          // toastr["success"](data.message);
        } else {
          $("#modal .modal-content").html(data.html_form);
          // toastr["error"](data.message);
        }
      },
      error: function (xhr, status, error) {
        var err = JSON.parse(xhr.responseText);
        toastr["error"](err.message);
      },
    });
    return false;
  };

  $("#modal").on("hidden.bs.modal", function (e) {
    $("#modal .modal-content").empty();
  });

  $("body").on("click", ".ajax-load-form", loadForm);
  $("body").on("submit", ".ajax-save-form", saveForm);

  // Order table rows
  $(".order").sortable({
    items: "tr:not(.nosort)",
    handle: "td a.reorder",
    cursor: "ns-resize",
    axis: "y",
    update: function (e, ui) {
      href = $(this).attr("data-url");
      $(this).sortable("refresh");
      sorted = JSON.stringify($(this).sortable("toArray"));
      // sorted = $(this).sortable("serialize");
      $.ajax({
        type: "POST",
        // headers: { "X-CSRFToken": csrftoken },
        url: href,
        data: sorted,
        dataType: "json",
        success: function (data) {
          if (data.is_valid) {
            toastr["info"](data.message);
          } else {
            toastr["warning"](data.message);
          }
        },
        error: function (xhr, status, error) {
          var err = JSON.parse(xhr.responseText);
          toastr["error"](err.message);
        },
      });
    },
  });

  $(".ajax-upload-files").click(function () {
    $("#fileupload").click();
  });
});
