'use strict';

var username, avatar;
const getUserInfo = () => {
    $.get({
        url: '/auth/info',

        success: response => {
            if (response) {
                username = response.username;
                avatar = response.avatar;
            }
        }
    });
};
