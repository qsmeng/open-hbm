import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
import GameView from '../views/GameView.vue'
import RuleView from '../views/RuleView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView
    },
    {
      path: '/game',
      name: 'game',
      component: GameView,
      meta: { requiresAuth: true }
    },
    {
      path: '/rule',
      name: 'rule',
      component: RuleView
    }
  ]
})

export default router
