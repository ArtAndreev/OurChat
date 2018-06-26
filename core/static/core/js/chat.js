$(document).ready(() => {
    let form = $('#message__form');
    let input = $('#message__form input');
    let chat = $($('.chat')[0]);

    // event submit form
    form.on('submit', (e) => {
        e.preventDefault();

        let formData = new FormData(e.target);
        let text = formData.get('text');

        // prevent sending empty messages
        if (!text) {
            return;
        }

        $.post({
            url: '/message/send/',
            data: formData,
            processData: false,
            contentType: false,

            success: response => {
                chat.prepend(response.renderedTemplate);

                input.val('');
            }
        })
    });

    // polling
    setInterval(() => {
        const lastId = $('.message').first().data('id');

        $.get({
            url: '/message/get',
            data: {
                last_id: lastId,
            },

            success: response => {
                if (response) {
                    chat.prepend(response);
                }
            }
        })
    }, 1000); // polling time is 1 sec
});
