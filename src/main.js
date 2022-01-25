import "./vendor"

import Vue from "vue"
import App from "./App.vue"
import router from "./router"

import axios from 'axios'
import VueAxios from 'vue-axios'

import "./assets/scss/app.scss"

Vue.config.productionTip = false

Vue.use(VueAxios, axios)

new Vue({
  router,
  render: h => h(App),
  data () {
    return {
      showSidebar: false
    }
  }
}).$mount("#app")
