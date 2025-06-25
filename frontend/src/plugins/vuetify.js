import "@mdi/font/css/materialdesignicons.css";
import 'swiper/css/swiper.min.css'

// import SwiperClass, { Mousewheel, Scrollbar, Lazy } from "swiper";
import SwiperClass from "swiper";
// import Scrollbar from 'swiper/components/scrollbar/scrollbar.esm.js'; // Previous attempt

// configure Swiper to use modules
// SwiperClass.use([Mousewheel, Scrollbar, Lazy]);

// Try to access Scrollbar as a property of SwiperClass, assuming it might be bundled.
if (SwiperClass.Scrollbar) {
  SwiperClass.use([SwiperClass.Scrollbar]);
} else {
  // Fallback or error if not found - for now, let's see if this works
  // console.error("Swiper Scrollbar module not found as a property of SwiperClass");
}

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
