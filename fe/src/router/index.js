import Vue from "vue";
import VueRouter from "vue-router";
import { DEFAULT_FROM, DEFAULT_TO } from "@/common/language.helper";

Vue.use(VueRouter);

const routes = [
  {
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
  {
    path: "/user/:username/items/:from/:to",
    name: "items",
    component: () => import("@/views/Items")
  },
  //obsolete
  {
    path: "/user/:username/items",
    redirect: `/user/:username/items/${DEFAULT_FROM}/${DEFAULT_TO}`
  },
  //documents
  {
    path: "/user/:username/docs/:from/:to",
    name: "docs",
    component: () => import("@/views/Documents")
  },
  {
    path: "/user/:username",
    redirect: `/user/:username/docs/${DEFAULT_FROM}/${DEFAULT_TO}`
  },
  {
    path: "/user/:username/docs",
    redirect: `/user/:username/docs/${DEFAULT_FROM}/${DEFAULT_TO}`
  },
  //alignments
  {
    path: "/user/:username/align/:from/:to",
    name: "align",
    component: () => import("@/views/Alignments")
  },
  {
    path: "/user/:username/align",
    redirect: `/user/:username/align/${DEFAULT_FROM}/${DEFAULT_TO}`
  },
  //creation
  {
    path: "/user/:username/create/:from/:to",
    name: "create",
    component: () => import("@/views/Create")
  },
  {
    path: "/user/:username/create",
    redirect: `/user/:username/create/${DEFAULT_FROM}/${DEFAULT_TO}`
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
