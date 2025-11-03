<template>
  <div id="app">
    <nav v-if="isAuthenticated" class="navbar">
      <div class="nav-container">
        <h1 class="logo">Medical Consultation System</h1>
        <div class="nav-links">
          <router-link to="/consultations" class="nav-link"
            >Consultations</router-link
          >
          <router-link to="/consultations/new" class="nav-link"
            >New Consultation</router-link
          >
          <span class="doctor-name">Dr. {{ doctorName }}</span>
          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "./composables/useAuth";

export default {
  name: "App",
  setup() {
    const router = useRouter();
    const { isAuthenticated, doctor, logout } = useAuth();

    const doctorName = computed(() => doctor.value?.full_name || "");

    const handleLogout = () => {
      logout();
      router.push("/login");
    };

    return {
      isAuthenticated,
      doctorName,
      handleLogout,
    };
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  background: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.1);
}

.doctor-name {
  color: #ecf0f1;
  font-weight: 500;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: #c0392b;
}

.main-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}
</style>
