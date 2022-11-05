<style>
@import "./assets/styles/main.css";
</style>

<template>
  <v-app>
    <!-- Left drawer menu -->
    <v-navigation-drawer app v-model="drawer" temporary>
      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class="blue--text text--accent-4"
        >
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-view-list-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title @click.stop.prevent="openContents()"
              >Contents</v-list-item-title
            >
          </v-list-item>
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-github</v-icon>
            </v-list-item-icon>
            <v-list-item-title @click.stop.prevent="goToGithub()"
              >Github</v-list-item-title
            >
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <!-- Top app bar -->
    <v-card>
      <v-toolbar color="indigo" dark hide-on-scroll flat>
        <v-row>
          <v-col v-if="showDrawerMenu" cols="12" sm="1">
            <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
          </v-col>

          <v-col v-if="showLanguageBar" cols="12" sm="5" class="text-right">
            <v-spacer />
            <div class="pa-2 font-josefin d-inline-block">
              {{ LANGUAGES[langCodeFrom].name }}
            </div>
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon color="yellow" v-bind="attrs" v-on="on">
                  <v-img
                    class="ma-2"
                    :src="getFlagImgPath(langCodeFrom)"
                    width="35px"
                    height="35px"
                  />
                </v-btn>
              </template>
              <v-list>
                <v-list-item v-for="(item, i) in LANGUAGES" :key="i" link>
                  <v-list-item-title @click="changeLangFrom(item.langCode)">
                    <div class="d-flex">
                      <v-img
                        class=""
                        :src="getFlagImgPath(item.langCode)"
                        max-width="35"
                        max-height="35"
                      />
                      <div class="ml-4 align-self-center">{{ item.name }}</div>
                    </div>
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-col>

          <v-col v-if="showLanguageBar" cols="12" sm="5">
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon color="yellow" v-bind="attrs" v-on="on">
                  <v-img
                    class="ma-2"
                    :src="getFlagImgPath(langCodeTo)"
                    width="35px"
                    height="35px"
                  />
                </v-btn>
              </template>
              <v-list>
                <v-list-item v-for="(item, i) in LANGUAGES" :key="i" link>
                  <v-list-item-title @click="changeLangTo(item.langCode)">
                    <div class="d-flex">
                      <v-img
                        class=""
                        :src="getFlagImgPath(item.langCode)"
                        max-width="35"
                        max-height="35"
                      />
                      <div class="ml-4 align-self-center">{{ item.name }}</div>
                    </div>
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <div class="pa-2 font-josefin d-inline-block">
              {{ LANGUAGES[langCodeTo].name }}
            </div>
            <v-spacer />
          </v-col>

          <!-- <v-col cols="12" sm="1" class="text-right">
            <v-btn icon>
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </v-col> -->
        </v-row>

        <template v-slot:extension>
          <v-tabs v-model="tab" align-with-title class="white-transparent">
            <v-tabs-slider color="yellow"></v-tabs-slider>

            <template v-if="$route.params.username">
              <v-tab
                :to="{
                  name: 'docs',
                  params: {
                    username: $route.params.username,
                    from: $route.params.from,
                    to: $route.params.to,
                  },
                }"
                >Load</v-tab
              >
              <v-tab
                :to="{
                  name: 'align',
                  params: {
                    username: $route.params.username,
                    from: $route.params.from,
                    to: $route.params.to,
                  },
                }"
                >Align</v-tab
              >
              <v-tab
                :to="{
                  name: 'create',
                  params: {
                    username: $route.params.username,
                    from: $route.params.from,
                    to: $route.params.to,
                  },
                }"
                >Create</v-tab
              >
            </template>
          </v-tabs>
        </template>
      </v-toolbar>
    </v-card>

    <v-main>
      <v-container class="pb-15">
        <router-view></router-view>
      </v-container>
    </v-main>

    <Footer />
  </v-app>
</template>

<script>
import Footer from "@/components/Footer";
import { LANGUAGES } from "@/common/language.helper";
import { DEFAULT_FROM, DEFAULT_TO } from "@/common/language.helper";
import { API_URL } from "@/common/config";

export default {
  name: "App",
  components: {
    Footer,
  },
  data: () => ({
    API_URL,
    LANGUAGES,
    drawer: false,
    group: null,
    tab: null,
  }),
  methods: {
    getFlagImgPath(code) {
      return `${API_URL}static/flags/flag-${code}-h.svg`;
    },
    changeLangFrom(code) {
      this.$router.push({
        path: `/user/${this.$route.params.username}/${this.$route.name}/${code}/${this.langCodeTo}`,
      });
    },
    changeLangTo(code) {
      this.$router.push({
        path: `/user/${this.$route.params.username}/${this.$route.name}/${this.langCodeFrom}/${code}`,
      });
    },
    goToGithub() {
      window.open("https://github.com/averkij/a-studio", "_blank");
    },
    openContents() {
      this.$router.push({
        path: `/contents`,
      });
    },
  },
  computed: {
    langCodeFrom() {
      let langCode = this.$route.params.from;
      if (this.LANGUAGES[langCode]) {
        return langCode;
      }
      return DEFAULT_FROM;
    },
    langCodeTo() {
      let langCode = this.$route.params.to;
      if (this.LANGUAGES[langCode]) {
        return langCode;
      }
      return DEFAULT_TO;
    },
    showLanguageBar() {
      if (
        this.$route.name == "create" ||
        this.$route.name == "docs" ||
        this.$route.name == "align"
      ) {
        return true;
      }
      return false;
    },
    showDrawerMenu() {
      return this.$route.name != "login" && this.$route.name != "home";
    },
  },
};
</script>
