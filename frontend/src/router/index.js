import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import ConsultationList from '../views/ConsultationList.vue'
import NewConsultation from '../views/NewConsultation.vue'
import { useAuth } from '../composables/useAuth'

const routes = [
  { path: '/', redirect: '/consultations' },
  { path: "/register", name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login, meta: { requiresGuest: true } },
  { path: '/consultations', name: 'ConsultationList', component: ConsultationList, meta: { requiresAuth: true } },
  { path: '/consultations/new', name: 'NewConsultation', component: NewConsultation, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global navigation guard
router.beforeEach((to, from, next) => {
  const { token } = useAuth() // use the reactive composable
  const hasToken = !!token.value

  if (to.meta.requiresAuth && !hasToken) {
    next('/login')
  } else if (to.meta.requiresGuest && hasToken) {
    next('/consultations')
  } else {
    next()
  }
})

export default router
