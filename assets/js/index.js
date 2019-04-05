window.$ = window.jQuery = require('jquery');
require('bootstrap-sass');

import Vue from 'vue';

import Messages from "./components/Messages.vue";


const app = new Vue({
    el: '#app',
    components: {
        Messages
    }
});
