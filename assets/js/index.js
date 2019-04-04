window.$ = window.jQuery = require('jquery');
require('bootstrap-sass');
window.axios = require('axios');
window.axios.defaults.xsrfCookieName = 'csrftoken'
window.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
window.axios.defaults.headers.common = {
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRF-TOKEN' : document.querySelector('[name="csrfmiddlewaretoken"]').getAttribute('value'),
};

import Vue from 'vue';

import Messages from "./components/Messages.vue";


const app = new Vue({
    el: '#app',
    components: {
        Messages
    }
});
