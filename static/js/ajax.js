$.ajaxSetup({
	// headers: { "X-CSRFToken": '{{ csrf_token }}' }
	headers: { "X-CSRFToken": $.cookie("csrftoken") },
});

$(document).ready(function(){

	var loadForm = function() {
	  var btn = $(this);
	  $.ajax({
		url: btn.attr("href"),
		type: 'get',
		dataType: 'json',
		beforeSend: function () {
		  $("#modal-ajax").modal("show");
		},
		success: function (data) {
		  $("#modal-ajax .modal-content").html(data.html_form);
		}
	  });
	  return false;
	};
  
	var saveForm = function() {
	  var form = $(this);
	  $.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
		  if (data.form_is_valid) {
			$("#table-ajax tbody").html(data.html_list);
			$("#modal-ajax").modal("hide");
		  }
		  else {
			$("#modal-ajax .modal-content").html(data.html_form);
		  }
		}
	  });
	  return false;
	};
  
	$("body").on('click', '.ajax-load-form', loadForm);
	$("body").on('submit', '.ajax-save-form', saveForm);
});

$('.order').sortable({
    cursor: 'ns-resize',
    axis:   'y',
    update: function(e, ui) {
        href = $(this).attr('data-url');
        $(this).sortable("refresh");
        sorted = JSON.stringify($(this).sortable("toArray"));
        // sorted = $(this).sortable("serialize");
        $.ajax({
            type: 'POST',
            url:  href,
            data: sorted,
            dataType: 'json',
            success: function(msg) {
                //do something with the sorted data
            }
        });
    }
});
