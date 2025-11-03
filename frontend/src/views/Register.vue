<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">Create an Account</h2>
      <p class="login-subtitle">Just a few more steps...</p>

      <form @submit.prevent="handleRegister" class="login-form">
        <div class="form-group">
          <label for="full_name">Full Name</label>
          <input
            id="full_name"
            v-model="full_name"
            type="text"
            required
            placeholder="Your Name Here"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="email@example.com"
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
            placeholder="min. 8 characters, 1 letter 1 number"
            class="form-input"
          />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? "Registering..." : "Register" }}
        </button>
      </form>

      <div class="demo-credentials">
        <p>Already have an account? <router-link to="/login">Login here</router-link>.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api/api";

export default {
  name: "Register",
  setup() {
    const router = useRouter();
    const full_name = ref("");
    const email = ref("");
    const password = ref("");
    const error = ref("");
    const loading = ref(false);

    const handleRegister = async () => {
      error.value = "";

      if (!email.value || !password.value || !full_name.value) {
        error.value = "All fields are required";
        return;
      }

      loading.value = true;

      try {
        await api.register(email.value.trim(), password.value, full_name.value.trim());
        alert("Account created successfully! Please log in.");
        router.push("/login");
      } catch (err) {
        console.error(err);
        error.value =
          err.response?.data?.errors || "Registration failed. Please try again.";
      } finally {
        loading.value = false;
      }
    };

    return {
      full_name,
      email,
      password,
      error,
      loading,
      handleRegister,
    };
  },
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
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
  background: #53a33a;
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
