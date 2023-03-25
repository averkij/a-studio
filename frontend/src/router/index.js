import Vue from "vue";
import VueRouter from "vue-router";
import {
  SettingsHelper
} from "@/common/settings.helper";


Vue.use(VueRouter);

const routes = [{
    path: "/",
    name: "home",
    component: () => import("@/views/Login")
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login"),
    alias: "/user"
  },
  //documents
  {
    path: "/user/:username/docs/:from/:to",
    name: "docs",
    component: () => import("@/views/Documents")
  },
  {
    path: "/user/:username",
    redirect: `/user/:username/docs/${SettingsHelper.getLastLanguageFrom()}/${SettingsHelper.getLastLanguageTo()}`
  },
  {
    path: "/user/:username/docs",
    redirect: `/user/:username/docs/${SettingsHelper.getLastLanguageFrom()}/${SettingsHelper.getLastLanguageTo()}`
  },
  //alignments
  {
    path: "/user/:username/align/:from/:to",
    name: "align",
    component: () => import("@/views/Alignments")
  },
  {
    path: "/user/:username/align",
    redirect: `/user/:username/align/${SettingsHelper.getLastLanguageFrom()}/${SettingsHelper.getLastLanguageTo()}`
  },
  //creation
  {
    path: "/user/:username/create/:from/:to",
    name: "create",
    component: () => import("@/views/Create")
  },
  {
    path: "/user/:username/create",
    redirect: `/user/:username/create/${SettingsHelper.getLastLanguageFrom()}/${SettingsHelper.getLastLanguageTo()}`
  },
  //#contents
  {
    path: "/contents",
    name: "contents",
    component: () => import("@/views/Contents")
  },
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;