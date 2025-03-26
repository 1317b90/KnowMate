import { createRouter, createWebHistory } from 'vue-router'
import parsingView from '../views/client/parsing.vue'
import ClientLayout from '../views/client/index.vue'
import AdminLayout from '../views/admin/index.vue'
import LoginLayout from '../views/login/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: ClientLayout,
      children: [
        {
          path: '',
          name: 'parsing',
          component: parsingView
        },
        {
          path: 'home',
          name: 'home',
          component: () => import('../views/client/home.vue')
        },
        {
          path: 'search',
          name: 'search',
          component: () => import('../views/client/search.vue')
        },
        {
          path: 'chat',
          name: 'chat',
          component: () => import('../views/client/chatView.vue')
        },
        {
          path: 'info',
          name: 'info',
          component: () => import('../views/client/info.vue')
        }
      ]
    },
    {
      path: '/',
      component: LoginLayout,
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import('../views/login/login.vue')
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('../views/login/register.vue')
        }
      ]
    },
    {
      path: '/',
      component: AdminLayout,
      children: [
        {
          path: 'Dashboard',
          name: 'Dashboard',
          component: () => import('../views/admin/Dashboard.vue')
        },
        {
          path: 'FoodData',
          name: 'FoodData',
          component: () => import('../views/admin/FoodData.vue')
        },
        {
          path: 'FoodEdit',
          name: 'FoodEdit',
          component: () => import('../views/admin/FoodEdit.vue')
        },
        {
          path: 'UserData',
          name: 'UserData',
          component: () => import('../views/admin/UserData.vue')
        },
        {
          path: 'UserEdit',
          name: 'UserEdit',
          component: () => import('../views/admin/UserEdit.vue')
        },
        {
          path: 'LogData',
          name: 'LogData',
          component: () => import('../views/admin/LogData.vue')
        },
      ]
    }
  ]
})

export default router
