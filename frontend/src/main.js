import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from './router'
import store from './store'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.js"
import { faCircleXmark, faEnvelope, faUser, faXmark } from '@fortawesome/free-solid-svg-icons'

// Adding icons to the library
library.add(faCircleXmark)
library.add(faEnvelope)
library.add(faUser)
library.add(faXmark)



createApp(App).use(store).use(router).use(VueAxios, axios).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
