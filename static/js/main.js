$(document).ready(function () {

    $('#follow-button').on('click', function () {
        const csrftoken = Cookies.get('csrftoken');
        var url = $(this).data("url");
        $.post(url, {csrfmiddlewaretoken: csrftoken}, function(){
            var follow_btn = $('#follow-button');
            if (follow_btn.data("follow") === "true"){
                follow_btn.data("follow", "false");
                follow_btn.text("obserwuj");
            }
            else{
                follow_btn.data("follow", "true");
                follow_btn.text("nie obserwuj");
            }

        });

    });

    $('.vote').on('click', function (event) {
        event.preventDefault();
        $('.user-data').val($(this).data("id"));
    });
});