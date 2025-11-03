<template>
  <div class="consultation-list">
    <div class="header">
      <h2>Past Consultations</h2>
      <router-link to="/consultations/new" class="btn-primary">
        + New Consultation
      </router-link>
    </div>

    <div v-if="loading" class="loading">Loading consultations...</div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="consultations.length === 0" class="empty">
      <p>No consultations found.</p>
      <router-link to="/consultations/new" class="btn-primary">
        Create your first consultation
      </router-link>
    </div>

    <div v-else class="consultations-table">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Patient Name</th>
            <th>Diagnosis Codes</th>
            <th>Notes</th>
            <th>Doctor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="consultation in consultations" :key="consultation.id">
            <td>{{ formatDate(consultation.consultation_date) }}</td>
            <td class="patient-name">{{ consultation.patient_name }}</td>
            <td>
              <div class="diagnosis-codes">
                <span
                  v-for="diagnosis in consultation.diagnoses"
                  :key="diagnosis.code"
                  class="diagnosis-tag"
                  :title="diagnosis.description"
                >
                  {{ diagnosis.code }}
                </span>
              </div>
            </td>
            <td class="notes">{{ consultation.notes || "-" }}</td>
            <td>{{ consultation.doctor_name }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import api from "../api/api";
import { useAuth } from "../composables/useAuth";

export default {
  name: "ConsultationList",
  setup() {
    const consultations = ref([]);
    const loading = ref(true);
    const error = ref("");
    const { token, logout } = useAuth();

    const loadConsultations = async () => {
      if (!token.value) return; // no token, skip call
      try {
        loading.value = true;
        const response = await api.getConsultations();
        consultations.value = response.data;
      } catch (err) {
        if (err.response?.status === 401) {
          // Token expired or invalid
          logout();
          error.value = "Session expired. Please log in again.";
        } else {
          error.value = "Failed to load consultations.";
          console.error(err);
        }
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    };

    onMounted(() => {
      loadConsultations();
    });

    // Watch token changes (auto reload if user logs in again)
    watch(token, (newVal) => {
      if (newVal) loadConsultations();
      else consultations.value = [];
    });

    return {
      consultations,
      loading,
      error,
      formatDate,
    };
  },
};
</script>


<style scoped>
.consultation-list {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 1.8rem;
  color: #2c3e50;
}

.btn-primary {
  background: #3498db;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #2980b9;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

.error {
  color: #e74c3c;
}

.empty {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.consultations-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8f9fa;
}

th {
  text-align: left;
  padding: 1rem;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.patient-name {
  font-weight: 500;
  color: #2c3e50;
}

.diagnosis-codes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.diagnosis-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: help;
}

.notes {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #7f8c8d;
}

tbody tr:hover {
  background: #f8f9fa;
}
</style>
