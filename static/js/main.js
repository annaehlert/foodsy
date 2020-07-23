$(document).ready(function () {

    $('#close-section').on('click', function () {
        $('#profile-vote-form').submit();
    });

    $('.vote').on('click', function (event) {
        event.preventDefault();
        $('.user-data').val($(this).data("id"));
        $('#vote-choice').show();
    });
});