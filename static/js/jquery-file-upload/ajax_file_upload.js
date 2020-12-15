$(function () {
    $(".ajax-upload-files").click(function () {
      $("#fileupload").click();
    });
  
    $("#fileupload").fileupload({
      dataType: 'json',
      done: function (e, data) {
        if (data.is_valid) {
          $('table[id*=table-ajax] tbody').prepend(
            "<tr><td><a href='" + data.url + "'>" + data.name + "</a></td></tr>"
          )
        }
      }
    });
  
  });