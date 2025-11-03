import { ref, computed } from 'vue'

const token = ref(localStorage.getItem('token') || null)
const doctor = ref(JSON.parse(localStorage.getItem('doctor') || 'null'))

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setDoctor = (doctorData) => {
    doctor.value = doctorData
    if (doctorData) {
      localStorage.setItem('doctor', JSON.stringify(doctorData))
    } else {
      localStorage.removeItem('doctor')
    }
  }

  const logout = () => {
    setToken(null)
    setDoctor(null)
  }

  return {
    token,
    doctor,
    isAuthenticated,
    setToken,
    setDoctor,
    logout,
  }
}
