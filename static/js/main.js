$(document).ready(function () {
    $('#show-contest-form').on('click', function (event) {
        event.preventDefault();
        $('#vote-choice').hide();
        $('#contest-form').show();
    });

    $('#close-section').on('click', function () {
        $('#song-vote-form').submit();
    });

    $('.vote').on('click', function (event) {
        event.preventDefault();
        $('#selected-song-name').text($(this).data("name"));
        $('#selected-song-author').text($(this).data("author"));
        $('.song-data').val($(this).data("id"));
        $('#vote-choice').show();
    });
});