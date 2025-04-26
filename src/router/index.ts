import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useHomeStore } from '@/stores/home'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      alias: '/home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/home/streaming',
      name: 'streaming',
      component: HomeView,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const store = useHomeStore()
  const isLogin = store.isLogin

  if (!isLogin && to.path !== '/login') {
    next('/login')
  } else {
    next()
  }
})

export default router
