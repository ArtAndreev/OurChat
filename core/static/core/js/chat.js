'use strict';

import '../css/chat.scss';
import '../img/push-pin.svg'
import '../img/right-arrow.svg'

import $ from 'jquery';
import moment from 'moment';

import '../../../../authentication/static/authentication/js/auth_info';
import './csrf';

const messageTemplate = (id, text, time, author) => {
    if (author === undefined) {
        author = this.username
    }
    return `<div class="message">
    <div class="message__author">
      <div class="message__name">
      
${author}
</div>
   <div class="message__time">
${moment(time).format('MMMM Do YYYY, h:mm:ss a')}
</div>
  </div>
   <div class="message__text">
</div>
${text}
</div>
   `};


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
                // debugger;
                chat.prepend(messageTemplate(response.id, response.text,
                        response.date, response.author));

                input.val('');
            }
        })
    });

    // polling
    /*setInterval(() => {
        const lastId = $('.message').first().data('id');

        $.get({
            url: '/message/get',
            data: {
                last_id: lastId,
            },

            success: response => {
                if (response) {
                    chat.prepend(messageTemplate(response.id, response.text,
                        response.time, response.author));
                }
            }
        })
    }, 1000); // polling time is 1 sec*/
});
