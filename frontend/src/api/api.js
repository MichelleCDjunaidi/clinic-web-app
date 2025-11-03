import axios from 'axios'

export default {
  // Auth
  login(email, password) {
    return axios.post('/auth/login', { email, password })
  },
  
  register(email, password, full_name) {
    return axios.post('/auth/register', { email, password, full_name })
  },
  
  getCurrentDoctor() {
    return axios.get('/auth/me')
  },
  
  // Diagnosis
  searchDiagnosis(searchTerm) {
    return axios.get('/diagnosis', { params: { search: searchTerm } })
  },
  
  // Consultation
  createConsultation(data) {
    return axios.post('/consultation', data)
  },
  
  getConsultations(skip = 0, limit = 100) {
    return axios.get('/consultation', { params: { skip, limit } })
  }
}