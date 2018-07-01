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

const messageSendTemplate = (id, text, date, author, avatar, attaches = undefined) => {
    const render_text = (text) => text ? `<span class="message__text">${ text }</span>` : '';

    const render_attaches_block = (attaches) => {
        let block = '';
        if (attaches) {
            block += `<div class="message__attachments-block">`;
            for (let i = 0; i < attaches.length; i++) {
                let subdvach = attaches[i].content_type.substring(0, 5);
                if (subdvach === 'image') {
                    block += `
                        <a href="${attaches[i].url}">
                          <img src="${ attaches[i].url }" class="message__attachment-content mt-10"/>
                        </a>`;
                }
                else {
                    block += `
                        <a class="message__attachment mt-10 link" href="${ attaches[i].url }">${ attaches[i].filename }</a>`;}
            }

            block += `</div>`;
        }

        return block;
    };

    return `
<div class="message message-right message__text-reverse m-10" data-id="${ id }">
  <div class="message__author message-reverse mb-10">
    <img class="user__avatar message__avatar" src="${ avatar }"/>
    <span class="message__name ml-10 mr-10">${ author }</span>
    <span class="message__time">${ moment(date).format('MMMM D, YYYY, h:mm a') }</span>
  </div>
  ${ render_text(text) }
  ${ render_attaches_block(attaches) }  
</div>`;
};


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
        let files = formData.get('attachments');

        // prevent sending empty messages
        if (!text && files.size === 0) {
            return;
        }

        $.post({
            url: '/message/send/',
            data: formData,
            processData: false,
            contentType: false,

            success: response => {
                chat.prepend(() => {
                        if (!response.attaches) {
                            return messageSendTemplate(
                                response.id, response.text, response.date,
                                User.username, User.avatar
                            )
                        }
                        else {
                            return messageSendTemplate(
                                response.id, response.text, response.date,
                                User.username, User.avatar, response.attaches
                            )
                        }
                    });

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
