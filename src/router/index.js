import Vue from "vue"
import VueRouter from "vue-router"

Vue.use(VueRouter)

const routes = [
  { path: "/", name: "index", component: require("../views/Index.vue").default },
  { path: "/cameras", name: "cameras", component: require("../views/Cameras.vue").default },
]

const router = new VueRouter({
  routes,
  mode: "history",
  linkExactActiveClass: "active"
})

router.beforeResolve((to, from, next) => {
  if (to.name) {
    window.NProgress.start()
  }
  next()
})
router.afterEach(() => {
  window.NProgress.done()
})

export default router
