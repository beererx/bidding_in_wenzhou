import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import VueCompositionApi from '@vue/composition-api';  
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Content from "../views/Content.vue";
Vue.use(ElementUI);
Vue.use(VueCompositionApi);
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/content/:noteid",
    name: "Content",
    component: Content
  },
  {
    path: "/content/:dt/:noteid",
    name: "Content",
    component: Content
  },
];

const router = new VueRouter({
  routes,
  mode: "history"
});

export default router;
