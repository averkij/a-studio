import "@mdi/font/css/materialdesignicons.css";
import 'swiper/swiper-bundle.css'

import Vue from "vue";
import Vuetify from "vuetify/lib";
import vueNumeralFilterInstaller from "vue-numeral-filter";
import VueAwesomeSwiper from 'vue-awesome-swiper';

Vue.use(Vuetify);
Vue.use(vueNumeralFilterInstaller, { locale: "en-gb" });
Vue.use(VueAwesomeSwiper)

export default new Vuetify({
  icons: {
    iconfont: "mdi"
  }
});

// npm install @mdi/font -D
// npm install @mdi/js -D
