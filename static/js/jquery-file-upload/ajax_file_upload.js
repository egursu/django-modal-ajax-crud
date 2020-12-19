$(function() {
  $(".ajax-upload-files").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,
    start: function (e) {
      $("#modal-progress").modal("show");
    },
    stop: function (e) {
      // $("#modal-progress").modal("hide");
      setTimeout(function() {$('#modal-progress').modal('hide');}, 500);
    },
    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({ "width": strProgress, "aria-valuenow": progress });
      $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {
      if (data.result.is_valid) {
        $("table[id*=table-ajax").find('tbody').html(data.result.html_list);
      }
    }
  });

});
