import { createRouter, createWebHistory } from 'vue-router'
import parsingView from '../views/client/parsing.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'parsing',
      component: parsingView
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/client/home.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/client/search.vue')
    },
    {
      path: '/info',
      name: 'info',
      component: () => import('../views/client/info.vue')
    },
    // 注册登陆
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/login/register.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/login/login.vue')
    },
    // 仪表盘
    {
      path: '/Dashboard',
      name: 'Dashboard',
      component: () => import('../views/admin/Dashboard.vue')
    },
    // 用户管理
    {
      path: '/FoodData',
      name: 'FoodData',
      component: () => import('../views/admin/FoodData.vue')
    },
    {
      path: '/FoodEdit',
      name: 'FoodEdit',
      component: () => import('../views/admin/FoodEdit.vue')
    },

    // 用户管理管理
    {
      path: '/UserData',
      name: 'UserData',
      component: () => import('../views/admin/UserData.vue')
    },
    {
      path: '/UserEdit',
      name: 'UserEdit',
      component: () => import('../views/admin/UserEdit.vue')
    },
    {
      path: '/LogData',
      name: 'LogData',
      component: () => import('../views/admin/LogData.vue')
    },
    // AI设置
    {
      path: '/AISetting',
      name: 'AISetting',
      component: () => import('../views/admin/AISetting.vue')
    }
  ],

})

export default router
