import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/movies',
      name: 'movies',
      component: () => import('../views/MoviesView.vue')
    },
    {
      path: '/movies/popular',
      name: 'popular',
      component: () => import('../views/PopularMoviesView.vue')
    },
    {
      path: '/movies/similar',
      name: 'similar',
      component: () => import('../views/SimilarMoviesView.vue')
    },
    {
      path: '/movies/plot',
      name: 'plot',
      component: () => import('../views/PlotView.vue')
    },
  ]
})

export default router
