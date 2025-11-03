<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">Medical Consultation System</h2>
      <p class="login-subtitle">Doctor Login</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="doctor@example.com"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="Enter your password"
            class="form-input"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <div class="demo-credentials">
        <p><strong>Demo Credentials:</strong></p>
        <p>Email: doctor@example.com</p>
        <p>Password: password123</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api/api";
import { useAuth } from "../composables/useAuth";

export default {
  name: "Login",
  setup() {
    const router = useRouter();
    const email = ref("doctor@example.com");
    const password = ref("password123");
    const error = ref("");
    const loading = ref(false);

    const { setToken, setDoctor } = useAuth()

    const handleLogin = async () => {
    error.value = ""
    loading.value = true

    try {
        const response = await api.login(email.value.trim(), password.value)
        setToken(response.data.access_token)

        // Optional: load doctor info
        try {
        const doctorResponse = await api.getCurrentDoctor()
        setDoctor(doctorResponse.data)
        } catch (err) {
        console.error('Failed to load doctor info:', err)
        }

        router.push("/consultations")
    } catch (err) {
        error.value = err.response?.data?.detail || "Login failed"
    } finally {
        loading.value = false
    }
    };

    return {
      email,
      password,
      error,
      loading,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login-container {
  /* min-height: 100vh; */
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.login-subtitle {
  color: #7f8c8d;
  text-align: center;
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.login-btn {
  background: #a5d468;
  color: white;
  border: none;
  padding: 0.875rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.demo-credentials {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
  text-align: center;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.demo-credentials p {
  margin: 0.25rem 0;
}
</style>
