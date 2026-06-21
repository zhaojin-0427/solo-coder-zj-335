import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/profiles'
    },
    {
      path: '/profiles',
      name: 'profiles',
      component: () => import('@/views/Profiles.vue')
    },
    {
      path: '/profiles/:id',
      name: 'profile-detail',
      component: () => import('@/views/ProfileDetail.vue')
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: () => import('@/views/Feedback.vue')
    },
    {
      path: '/adjustments',
      name: 'adjustments',
      component: () => import('@/views/Adjustments.vue')
    },
    {
      path: '/followups',
      name: 'followups',
      component: () => import('@/views/Followups.vue')
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('@/views/Statistics.vue')
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('@/views/TaskCenter.vue')
    }
  ]
})

export default router
