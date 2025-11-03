import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './api/axios'

createApp(App)
  .use(router)
  .mount('#app')