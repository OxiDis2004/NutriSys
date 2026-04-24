import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'
import StartView from '@/views/StartView.vue'
import RecommendedView from '@/views/RecommendedView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: App,
    },
    {
      path: '/#start',
      name: 'start',
      component: StartView,
    },
    {
      path: '/#recommended',
      name: 'recommended',
      component: RecommendedView,
    },
    {
      path: '/#food-statistic',
      name: 'food-statistic',
      component: StartView,
    },
    {
      path: '/#water-statistic',
      name: 'water-statistic',
      component: StartView,
    },
    {
      path: '/#food-history',
      name: 'food-history',
      component: StartView,
    }
  ],
})

export default router
