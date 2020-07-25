$(document).ready(function () {

    $('#follow-button').on('click', function () {
        const csrftoken = Cookies.get('csrftoken');
        var url = $(this).data("url");

        $.post(url, {csrfmiddlewaretoken: csrftoken}, function(){

            var follow_btn = $('#follow-button');
            if (follow_btn.data("follow") !== true) {
                follow_btn.data("follow", true);
                follow_btn.text("Obserwuj");
                var followersNumber = $('#number_of_followers');
                followersNumber.text(Number(followersNumber.text())-1);
            } else {
                follow_btn.data("follow", false);
                follow_btn.text("Nie obserwuj");
                var followersNumber = $('#number_of_followers');
                followersNumber.text(Number(followersNumber.text())+1);
            }
        });

    });

    $('.vote').on('click', function (event) {
        event.preventDefault();
        $('.user-data').val($(this).data("id"));
    });
});