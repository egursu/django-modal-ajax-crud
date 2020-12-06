$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function () {
    setTimeout(function () {
        $(".alert").alert('close');
    }, 3000);
});
