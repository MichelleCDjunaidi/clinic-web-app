import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import ConsultationList from '../views/ConsultationList.vue'
import NewConsultation from '../views/NewConsultation.vue'

const routes = [
  {
    path: '/',
    redirect: '/consultations'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/consultations',
    name: 'ConsultationList',
    component: ConsultationList,
    meta: { requiresAuth: true }
  },
  {
    path: '/consultations/new',
    name: 'NewConsultation',
    component: NewConsultation,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
// ensures that if no token, redirect back to front
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresGuest && token) {
    next('/consultations')
  } else {
    next()
  }
})

export default router