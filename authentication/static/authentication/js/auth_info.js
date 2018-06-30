'use strict';

const getUserInfo = () => {
    let User = {};
    $.get({
        url: '/auth/info/',

        success: response => {
            if (response) {
                User.username = response.username;
                User.avatar = response.avatar;
            }
        }
    });

    return User;
};

export { getUserInfo }
