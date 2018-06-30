'use strict';

import '../css/chat.scss';

import moment from 'moment';

import './csrf'; // import and set csrf header
import { getUserInfo } from '../../../../authentication/static/authentication/js/auth_info';


moment.updateLocale('en', {
    meridiem(hour, minute, isLowerCase) {
        return hour < 12 ? 'a.m.' : 'p.m.';
    }
});

const messageSendTemplate = (id, text, date, author, avatar) => `
<div class="message message-right message__text-reverse m-10" data-id="${ id }">
  <div class="message__author message-reverse mb-10">
    <img class="user__avatar message__avatar" src="${ avatar }"/>
    <span class="message__name ml-10 mr-10">${ author }</span>
    <span class="message__time">${moment(date).format('MMMM DD, YYYY, h:mm a')}</span>
  </div>
  <span class="message__text">${ text }</span>
</div>
`;



$(document).ready(() => {
    let User = getUserInfo();
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
                chat.prepend(messageSendTemplate(response.id, response.text,
                        response.date, User.username, User.avatar));

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
