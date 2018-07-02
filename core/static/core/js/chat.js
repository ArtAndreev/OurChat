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

// Rendering templates:

const render_text = (text) => text ? `<span class="message__text">${ text }</span>` : '';

const render_attaches_block = (attaches) => {
    let block = '';
    if (attaches) {
        block += `<div class="message__attachments-block">`;
        for (let i = 0; i < attaches.length; i++) {
            if (attaches[i].content_type.substring(0, 5) === 'image') {
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


const messageGetTemplate = (id, text, date, author, avatar, attaches = undefined) => `
<div class="message m-10" data-id="${ id }">
  <div class="message__author mb-10">
    <img class="user__avatar message__avatar" src="${ avatar }"/>
    <span class="message__name ml-10 mr-10">${ author }</span>
    <span class="message__time">${ moment(date).format('MMMM D, YYYY, h:mm a') }</span>
  </div>
  ${ render_text(text) }
  ${ render_attaches_block(attaches) }  
</div>`;

const messageSendTemplate = (id, text, date, author, avatar, attaches = undefined) => `
<div class="message message-right message__text-reverse m-10" data-id="${ id }">
  <div class="message__author message-reverse mb-10">
    <img class="user__avatar message__avatar" src="${ avatar }"/>
    <span class="message__name ml-10 mr-10">${ author }</span>
    <span class="message__time">${ moment(date).format('MMMM D, YYYY, h:mm a') }</span>
  </div>
  ${ render_text(text) }
  ${ render_attaches_block(attaches) }  
</div>`;


$(document).ready(() => {
    let User = getUserInfo();
    let form = $('#message__form');
    let input = $('#message__form input');
    let chat = $($('.chat')[0]);


    // WebSocket
    // const roomName = room_name_json; // get it from info later
    const webSocketPort = 8001;

    const chatSocket = new WebSocket(
        'ws://' + window.location.hostname + ':' + webSocketPort +
        // '/ws/chat/' + roomName + '/' // for later chat rooms implementation
        '/ws/chat/'
    );

    chatSocket.onopen = (e) => {
        console.log('Chat socket opened.');
    };

    chatSocket.onmessage = (e) => {
        console.log('Got message!');
        const message = e.data;
        debugger;
        chat.prepend(messageGetTemplate(
            message.id,
            message.text,
            message.date,
            message.username,
            message.avatar,
            message.attaches
            )
        );
    };

    chatSocket.onerror = (e) => {
        console.error("Chat socket error occurred: " + e.message);
    };

    chatSocket.onclose = (e) => {
        console.log('Chat socket closed unexpectedly.');
    };


    // event submit form
    form.on('submit', (e) => {
        e.preventDefault();

        let formData = new FormData(e.target);
        let text = formData.get('text');
        let files = formData.getAll('attachments');
        debugger;
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
                chat.prepend(messageSendTemplate(
                    response.id, response.text, response.date,
                    User.username, User.avatar, response.attaches
                    )
                )
            }
        });

        // chatSocket.send(JSON.stringify({
        //     username: User.username,
        //     text: text,
        //     attaches: formData.getAll('attachments'),
        // }));

        input.val('');

    });
});
